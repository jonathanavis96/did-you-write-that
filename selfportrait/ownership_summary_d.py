"""Summarise pilot 11 stage D (out/<prefix>_conf.jsonl, out/<prefix>_explicit.jsonl) and the
casing ablation (out/<prefix>_judgements_lc.jsonl vs out/<prefix>_judgements.jsonl)."""
from __future__ import annotations

import json
import math
import os
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "out"
PREFIX = os.environ.get("SP_OUT_PREFIX", "own")


def load(p):
    return [json.loads(x) for x in p.read_text().splitlines()] if p.exists() else []


def load_json_array(p):
    return json.loads(p.read_text()) if p.exists() else []


_OWN_CELLS = {(c["prompt"], c["answer"]): c for c in load_json_array(ROOT / "out" / "own_cells.json")}


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


def lp(v, n=49):
    return math.log(max(v or 0.0, 1.0 / n))


# ---------------------------------------------------------------- conf -------
conf_path = OUT / f"{PREFIX}_conf.jsonl"
ex_path = OUT / f"{PREFIX}_explicit.jsonl"
allc = load(conf_path)
allex = load(ex_path)
JUDGES = sorted({r["judge"] for r in allc} | {r["judge"] for r in allex})

conf = [r for r in allc if r.get("conf") is not None]
print(f"== stage D confidence: {len(allc)} rows, {len(conf)} parsed, {sum(1 for r in allc if r.get('error'))} errors ==")
for j in JUDGES:
    other = ([m for m in JUDGES if m != j] or ["other"])[0]
    sub = [r for r in conf if r["judge"] == j]
    cells = defaultdict(list)
    for r in sub:
        cells[(r["prompt"], r["answer"], r["tag"])].append(r["conf"])
    print(f"\n-- judge={j}: mean confidence by cell")
    print(f"{'prompt':11s}{'answer':14s}{'tag':18s}{'n':>3s}{'conf':>7s}{'sd':>6s}{'p_'+j:>8s}{'p_'+other:>8s}")
    for (pr, a, tag), v in sorted(cells.items(), key=lambda kv: (kv[0][0], -np.mean(kv[1]))):
        row0 = next(r for r in sub if r["prompt"] == pr and r["answer"] == a)
        print(f"{pr:11s}{a[:13]:14s}{tag:18s}{len(v):3d}{np.mean(v):7.1f}{np.std(v):6.1f}"
              f"{row0.get('p_'+j, 0) or 0:8.2f}{other_prob(row0, j):8.2f}")
    inc = [r for r in sub if r["tag"] != "off_category"]
    off = [r for r in sub if r["tag"] == "off_category"]
    print(f"  in-category mean={np.mean([r['conf'] for r in inc]):.1f} (n={len(inc)}), "
          f"off-category mean={np.mean([r['conf'] for r in off]):.1f} (n={len(off)})")
    # cell-level correlations with own and other log-probability
    cl = defaultdict(list)
    for r in inc:
        cl[(r["prompt"], r["answer"])].append(r["conf"])
    xs_own = [lp(next(r for r in inc if (r["prompt"], r["answer"]) == k).get("p_" + j)) for k in cl]
    xs_oth = [lp(other_prob(next(r for r in inc if (r["prompt"], r["answer"]) == k), j)) for k in cl]
    ys = [np.mean(v) for v in cl.values()]
    ro, po = stats.spearmanr(xs_own, ys)
    rt, pt = stats.spearmanr(xs_oth, ys)
    print(f"  cell-level Spearman(conf, log p_{j}) rho={ro:+.2f} p={po:.2g}; Spearman(conf, log p_{other}) rho={rt:+.2f} p={pt:.2g} ({len(cl)} cells)")
    # dissociators: own-high/other-low vs other-high/own-low
    a = [r["conf"] for r in inc if (r.get("p_" + j) or 0) >= 0.15 and other_prob(r, j) < 0.05]
    b = [r["conf"] for r in inc if other_prob(r, j) >= 0.15 and (r.get("p_" + j) or 0) < 0.05]
    vu = [r["conf"] for r in inc if r["tag"] == "valid_unsampled"]
    if a and b:
        u = stats.mannwhitneyu(a, b)
        print(f"  own-high/other-low mean={np.mean(a):.1f} (n={len(a)}) vs other-high/own-low mean={np.mean(b):.1f} (n={len(b)}); "
              f"Mann-Whitney p={u.pvalue:.2g}; valid_unsampled mean={np.mean(vu):.1f} (n={len(vu)})")

# ---------------------------------------------------------------- explicit ---
ex = allex
print(f"\n== stage D explicit self-prediction: {len(ex)} rows, {sum(1 for r in ex if r['chosen']=='unparsed')} unparsed, {sum(1 for r in ex if r.get('error'))} errors ==")
for j in JUDGES:
    sub = [r for r in ex if r["judge"] == j and r["chosen"] != "unparsed"]
    cells = defaultdict(list)
    for r in sub:
        cells[(r["prompt"], r["a"], r["b"], r["b_tag"])].append(r["chosen"] == "top")
    print(f"\n-- judge={j}: P(picks own top answer) per pair")
    print(f"{'prompt':11s}{'own top':12s}{'vs':14s}{'b_tag':18s}{'n':>3s}{'P(top)':>8s}{'p_a':>6s}{'p_b':>6s}")
    for (pr, a, b, tag), v in sorted(cells.items()):
        r0 = next(r for r in sub if (r["prompt"], r["a"], r["b"]) == (pr, a, b))
        print(f"{pr:11s}{a[:11]:12s}{b[:13]:14s}{tag:18s}{len(v):3d}{np.mean(v):8.2f}{r0['p_a'] or 0:6.2f}{r0['p_b'] or 0:6.2f}")
    # accuracy: does the pick agree with the empirical distribution? (top has higher p_a than p_b by construction)
    inc = [r for r in sub if r["b_tag"] != "off_category"]
    print(f"  in-category: picks own top {np.mean([r['chosen']=='top' for r in inc]):.2f} of {len(inc)}; "
          f"vs other-model top {np.mean([r['chosen']=='top' for r in inc if r['b_tag'].endswith('_top')]):.2f} "
          f"(n={sum(1 for r in inc if r['b_tag'].endswith('_top'))}); "
          f"vs valid_unsampled {np.mean([r['chosen']=='top' for r in inc if r['b_tag']=='valid_unsampled']):.2f}; "
          f"order effect: first-listed chosen {np.mean([(r['chosen']=='top')==(r['order']==0) for r in inc]):.2f}")

# ---------------------------------------------------------------- casing -----
lc = [r for r in load(OUT / f"{PREFIX}_judgements_lc.jsonl") if r["yn"] in ("yes", "no")]
cap = [r for r in load(OUT / f"{PREFIX}_judgements.jsonl") if r["yn"] in ("yes", "no")]
if lc:
    print(f"\n== casing ablation: lowercase-inserted run ({len(lc)} rows) vs matched capitalised cells ==")
    lc_cells = defaultdict(list)
    for r in lc:
        lc_cells[(r["judge"], r["question"], r["prompt"], r["answer"])].append(r["yn"] == "yes")
    cap_cells = defaultdict(list)
    for r in cap:
        cap_cells[(r["judge"], r["question"], r["prompt"], r["answer"])].append(r["yn"] == "yes")
    for j in JUDGES:
        for q in ("neutral", "rival", "intent"):
            pairs = [(np.mean(lc_cells[k]), np.mean(cap_cells[k])) for k in lc_cells
                     if k[0] == j and k[1] == q and k in cap_cells and k[2] in ("fruit", "colour", "noun", "instrument")]
            if pairs:
                a, b = np.array(pairs).T
                print(f"  judge={j:6s} q={q:8s} lowercase P(yes)={a.mean():.2f} vs capitalised {b.mean():.2f} "
                      f"diff={np.mean(a-b):+.2f} over {len(pairs)} cells (prompts where casing differed)")
