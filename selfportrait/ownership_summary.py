"""Summarise pilot 11 (out/<prefix>_forks.jsonl, out/<prefix>_judgements.jsonl)."""
from __future__ import annotations

import json
import math
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy import stats
from sklearn.linear_model import LogisticRegression

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "out"
PREFIX = os.environ.get("SP_OUT_PREFIX", "own")


def load(p):
    return [json.loads(x) for x in p.read_text().splitlines()] if p.exists() else []


forks = load(OUT / f"{PREFIX}_forks.jsonl")
N = Counter((r["model"], r["prompt"]) for r in forks if r["answer"])
allrows = load(OUT / f"{PREFIX}_judgements.jsonl")
rows = [r for r in allrows if r["yn"] in ("yes", "no")]
JUDGES = sys.argv[1].split(",") if len(sys.argv) > 1 else sorted({r["judge"] for r in allrows})
print(f"judgements: {len(allrows)} rows, {len(rows)} parsed, "
      f"{sum(1 for r in allrows if r['yn']=='unparsed')} unparsed, "
      f"{sum(1 for r in allrows if r.get('error'))} errors")

# pooled Claude (haiku/opus) probability for a (prompt, answer), used as the
# "other-model" fallback when a row carries no other judge's p_* field at all
# (e.g. the gpt judge, which only ever records p_gpt).
def load_json_array(p):
    return json.loads(p.read_text()) if p.exists() else []


_OWN_CELLS = {(c["prompt"], c["answer"]): c for c in load_json_array(OUT / "own_cells.json")}


def other_prob(r, j):
    """Probability under 'the other model' for judge j on row/cell r.

    Exactly one other p_* key present -> use it (the haiku/opus two-judge case).
    None present -> fall back to the pooled Claude probability from own_cells.json.
    More than one -> take the max (not expected in current data).
    """
    ks = sorted(k for k in r if k.startswith("p_") and k not in (f"p_{j}", "p_own"))
    if len(ks) == 1:
        return r.get(ks[0]) or 0.0
    if not ks:
        c = _OWN_CELLS.get((r.get("prompt"), r.get("answer")))
        if c:
            return max(c.get("p_haiku", 0) or 0, c.get("p_opus", 0) or 0)
        return 0.0
    return max(r.get(k) or 0.0 for k in ks)


def eps(judge, prompt):
    return 1.0 / (N[(judge, prompt)] + 1)


def own_logp(r, j):
    return math.log(max(r.get(f"p_{j}", 0.0) or 0.0, eps(j, r["prompt"])))


def other_logp(r, j):
    ks = sorted(k for k in r if k.startswith("p_") and k not in (f"p_{j}", "p_own"))
    po = other_prob(r, j)
    floor = eps(ks[0][2:], r["prompt"]) if len(ks) == 1 else eps(j, r["prompt"])
    return math.log(max(po, floor))


# 1. cell table -----------------------------------------------------------
print("\n== P(yes) by judge x question x cell (n, p_haiku, p_opus) ==")
cells = defaultdict(list)
for r in rows:
    cells[(r["judge"], r["question"], r["prompt"], r["answer"], r["tag"])].append(r["yn"] == "yes")
for j in JUDGES:
    for q in ("neutral", "rival", "intent"):
        print(f"\n-- judge={j} question={q}")
        sub = [(k, v) for k, v in cells.items() if k[0] == j and k[1] == q]
        if JUDGES == ["haiku", "opus"]:
            print(f"{'prompt':11s}{'answer':14s}{'tag':18s}{'n':>3s}{'P(yes)':>8s}{'p_haiku':>9s}{'p_opus':>8s}")
            for (jj, qq, pr, a, tag), v in sorted(sub, key=lambda kv: (kv[0][2], -np.mean(kv[1]))):
                ex = next(r for r in rows if r["judge"] == jj and r["question"] == qq and r["prompt"] == pr and r["answer"] == a)
                print(f"{pr:11s}{a[:13]:14s}{tag:18s}{len(v):3d}{np.mean(v):8.2f}"
                      f"{ex.get('p_haiku', float('nan')):9.2f}{ex.get('p_opus', float('nan')):8.2f}")
        else:
            header = f"{'prompt':11s}{'answer':14s}{'tag':18s}{'n':>3s}{'P(yes)':>8s}"
            header += "".join(f"{'p_'+m:>9s}" for m in JUDGES) + f"{'p_other':>9s}"
            print(header)
            for (jj, qq, pr, a, tag), v in sorted(sub, key=lambda kv: (kv[0][2], -np.mean(kv[1]))):
                ex = next(r for r in rows if r["judge"] == jj and r["question"] == qq and r["prompt"] == pr and r["answer"] == a)
                line = f"{pr:11s}{a[:13]:14s}{tag:18s}{len(v):3d}{np.mean(v):8.2f}"
                line += "".join(f"{(ex.get('p_'+m, 0) or 0):9.2f}" for m in JUDGES)
                line += f"{other_prob(ex, jj):9.2f}"
                print(line)

# 2. pooled by tag group ---------------------------------------------------
print("\n== P(yes) pooled, by judge x question x tag-group ==")


def group(r, j):
    if r["tag"] == "off_category":
        return "off_category"
    if r["tag"] == "valid_unsampled":
        return "valid_unsampled"
    pj, po = r.get(f"p_{j}", 0) or 0, other_prob(r, j)
    if pj >= 0.15 and po < 0.05:
        return "own_high_other_low"
    if po >= 0.15 and pj < 0.05:
        return "other_high_own_low"
    if r["tag"] == f"{j}_top":
        return "own_top"
    if r["tag"] == f"{j}_mid":
        return "own_mid"
    if r["tag"] == f"{j}_low":
        return "own_low"
    if r["tag"] in ("haiku_top", "opus_top") and j not in ("haiku", "opus"):
        return "other_vendor"
    return "other_ladder"


for j in JUDGES:
    for q in ("neutral", "rival", "intent"):
        g = defaultdict(list)
        for r in rows:
            if r["judge"] == j and r["question"] == q:
                g[group(r, j)].append(r["yn"] == "yes")
        if g:
            print(f"judge={j:6s} q={q:8s} " + "  ".join(f"{k}={np.mean(v):.2f}(n{len(v)})" for k, v in sorted(g.items())))

# 3. logistic regression: yes ~ log p_judge + log p_other, in-support ------
print("\n== logistic regression, in-support answers only (off_category excluded) ==")
for j in JUDGES:
    other = ([m for m in JUDGES if m != j] or ["other"])[0]
    for q in ("neutral", "rival", "intent"):
        sub = [r for r in rows if r["judge"] == j and r["question"] == q and r["tag"] != "off_category"]
        if len(sub) < 20:
            continue
        y = np.array([r["yn"] == "yes" for r in sub], int)
        if y.min() == y.max():
            print(f"judge={j} q={q}: all {'yes' if y[0] else 'no'} (n={len(y)}), no fit")
            continue
        X = np.array([[own_logp(r, j), other_logp(r, j)] for r in sub])
        def fit(Xm):
            m = LogisticRegression(penalty=None, max_iter=2000).fit(Xm, y)
            p = np.clip(m.predict_proba(Xm)[:, 1], 1e-9, 1 - 1e-9)
            return m, -2 * np.sum(y * np.log(p) + (1 - y) * np.log(1 - p))
        m_full, d_full = fit(X)
        _, d_own = fit(X[:, :1])
        _, d_oth = fit(X[:, 1:])
        d_null = -2 * (y.sum() * math.log(y.mean()) + (len(y) - y.sum()) * math.log(1 - y.mean()))
        print(f"judge={j:6s} q={q:8s} n={len(y):3d}  b(log p_{j})={m_full.coef_[0][0]:+.2f}  "
              f"b(log p_{other})={m_full.coef_[0][1]:+.2f} | "
              f"LR own-only vs null chi2={d_null-d_own:.1f} p={stats.chi2.sf(d_null-d_own,1):.2g}; "
              f"add other|own chi2={d_own-d_full:.1f} p={stats.chi2.sf(d_own-d_full,1):.2g}; "
              f"add own|other chi2={d_oth-d_full:.1f} p={stats.chi2.sf(d_oth-d_full,1):.2g}")
        # cell-level Spearman
        cl = defaultdict(list)
        for r in sub:
            cl[(r["prompt"], r["answer"])].append(r["yn"] == "yes")
        xs = [own_logp(next(r for r in sub if (r["prompt"], r["answer"]) == k), j) for k in cl]
        ys = [np.mean(v) for v in cl.values()]
        rho, pv = stats.spearmanr(xs, ys)
        print(f"{'':22s} cell-level Spearman(P(yes), log p_{j}) rho={rho:+.2f} p={pv:.2g} ({len(cl)} cells)")

# 4. question framing effect, paired by cell --------------------------------
print("\n== framing effect: mean P(yes) per question, paired by (judge,prompt,answer) ==")
for j in JUDGES:
    byq = defaultdict(dict)
    for (jj, q, pr, a, tag), v in cells.items():
        if jj == j:
            byq[(pr, a)][q] = np.mean(v)
    for qa, qb in (("neutral", "rival"), ("neutral", "intent"), ("intent", "rival")):
        pairs = [(d[qa], d[qb]) for d in byq.values() if qa in d and qb in d]
        if pairs:
            a, b = np.array(pairs).T
            w = stats.wilcoxon(a, b) if np.any(a != b) else None
            print(f"judge={j:6s} {qa}={a.mean():.2f} vs {qb}={b.mean():.2f}  diff={np.mean(a-b):+.2f} "
                  f"({len(pairs)} cells; Wilcoxon p={w.pvalue:.2g})" if w else f"judge={j} {qa} vs {qb}: identical")
