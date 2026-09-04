"""Summarise the one-word pilot-11 design (paper sections 4.1-4.4: sec:label,
sec:likelihood, sec:rival, "Explicit self-prediction") from a clean replication's
row files, so every quantity those sections quote can be checked against a rerun.

Reads out/<prefix>_forks.jsonl, out/<prefix>_cells.json, out/<prefix>_judgements.jsonl,
out/<prefix>_judgements_userturn2.jsonl (falling back to question=="named_userturn2"
rows inside the main judgements file, which is where pilot 13e's user-turn rows
actually live for the "own" prefix), out/<prefix>_conf.jsonl, out/<prefix>_explicit.jsonl
and out/<prefix>_within.jsonl. Any missing file prints "<section>: no rows" and the
script continues -- this is meant to run against an in-progress harness without
crashing.

Uses the same log-own-probability convention as ownership_summary.py's own_logp:
raw log(p) except at p==0, where it floors to 1/(N_forks_for_this_prompt + 1) so the
cell does not drop out of the correlation (matches Table tab:rho's caption, "raw
where cells at zero would drop out").
"""
from __future__ import annotations

import json
import math
import os
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "out"
PREFIX = os.environ.get("SP_OUT_PREFIX", "clean11")


def load_jsonl(path: Path):
    if not path.exists():
        return None
    rows = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            break  # truncated last line of an in-progress run
    return rows


def load_json(path: Path):
    return json.loads(path.read_text()) if path.exists() else None


def section(title):
    print(f"\n{'=' * 10} {title} {'=' * 10}")


def no_rows(title):
    print(f"{title}: no rows")


# ---------------------------------------------------------------- loads ------
forks = load_jsonl(OUT / f"{PREFIX}_forks.jsonl")
cells = load_json(OUT / f"{PREFIX}_cells.json")
judgements = load_jsonl(OUT / f"{PREFIX}_judgements.jsonl")
userturn2_file = load_jsonl(OUT / f"{PREFIX}_judgements_userturn2.jsonl")
if not userturn2_file:
    # the Codex harness plants the user-turn control as a second user record (layout "user")
    userturn2_file = load_jsonl(OUT / f"{PREFIX}_judgements_userturn.jsonl")
conf_rows = load_jsonl(OUT / f"{PREFIX}_conf.jsonl")
explicit_rows = load_jsonl(OUT / f"{PREFIX}_explicit.jsonl")
within_rows = load_jsonl(OUT / f"{PREFIX}_within.jsonl")

CELLS = cells or []
TAGMAP = {(c["prompt"], c["answer"]): c["tag"] for c in CELLS}
CELLKEYS = set(TAGMAP)
INCAT_KEYS = {k for k, t in TAGMAP.items() if t != "off_category"}
OFFCAT_KEYS = {k for k, t in TAGMAP.items() if t == "off_category"}
JUDGES = sorted({c["tag"].split("_")[0] for c in CELLS if "_" in c["tag"] and c["tag"].split("_")[0] not in ("valid", "off", "rangeecho")}) or ["haiku", "opus"]
if judgements:
    JUDGES = sorted(set(JUDGES) | {r["judge"] for r in judgements})


def other_prob(row, j):
    """Probability under 'the other model' for judge j: the other p_* field on the
    row/cell if there is exactly one, else the max of whatever p_* fields exist."""
    ks = sorted(k for k in row if k.startswith("p_") and k not in (f"p_{j}", "p_own"))
    if not ks:
        return 0.0
    return max(row.get(k) or 0.0 for k in ks)


# fork counts per (judge, prompt) -> log-own-probability floor 1/(N+1)
FORK_N = Counter((r["model"], r["prompt"]) for r in (forks or []) if r.get("answer"))


def eps(judge, prompt):
    return 1.0 / (FORK_N.get((judge, prompt), 48) + 1)


def own_logp(prompt, judge, p):
    return math.log(max(p or 0.0, eps(judge, prompt)))


def cell_p(judge, prompt, answer):
    for c in CELLS:
        if c["prompt"] == prompt and c["answer"] == answer:
            return c.get(f"p_{judge}", 0.0) or 0.0
    return 0.0


def group_tag(row_tag, prompt, answer, judge):
    """Same tag-group bucketing as ownership_summary.py's group()."""
    if row_tag == "off_category":
        return "off_category"
    if row_tag == "valid_unsampled":
        return "valid_unsampled"
    pj = cell_p(judge, prompt, answer)
    other_vals = [c.get(f"p_{m}", 0.0) or 0.0 for c in CELLS if c["prompt"] == prompt and c["answer"] == answer for m in JUDGES if m != judge]
    po = max(other_vals) if other_vals else 0.0
    if pj >= 0.15 and po < 0.05:
        return "own_high_other_low"
    if po >= 0.15 and pj < 0.05:
        return "other_high_own_low"
    if row_tag == f"{judge}_top":
        return "own_top"
    if row_tag == f"{judge}_mid":
        return "own_mid"
    if row_tag == f"{judge}_low":
        return "own_low"
    if row_tag in ("haiku_top", "opus_top") and judge not in ("haiku", "opus"):
        return "other_vendor"
    return "other_ladder"


def clopper_pearson(k, n, alpha=0.05):
    if n == 0:
        return float("nan"), float("nan")
    lo = stats.beta.ppf(alpha / 2, k, n - k + 1) if k > 0 else 0.0
    hi = stats.beta.ppf(1 - alpha / 2, k + 1, n - k) if k < n else 1.0
    return lo, hi


def wilcoxon_p(diffs):
    nz = [d for d in diffs if d != 0]
    if len(nz) < 5:
        return float("nan")
    return stats.wilcoxon(nz).pvalue


# ================================================================= 1 =========
section("1. Own distributions")
if not forks:
    no_rows("own distributions")
else:
    by_mp = defaultdict(list)
    for r in forks:
        by_mp[(r["model"], r["prompt"])].append(r)
    for (model, prompt), rs in sorted(by_mp.items()):
        n = len(rs)
        errs = sum(1 for r in rs if r.get("error"))
        counts = Counter(r["answer"] for r in rs if r.get("answer"))
        print(f"judge={model:8s} prompt={prompt:10s} n={n:3d} errors={errs:2d}  " +
              ", ".join(f"{w}={c}" for w, c in counts.most_common()))

# ================================================================= 2 =========
section("2. Cells")
if not CELLS:
    no_rows("cells")
else:
    pkeys = sorted({k for c in CELLS for k in c if k.startswith("p_")})
    print(f"{'prompt':11s}{'answer':16s}{'tag':22s}" + "".join(f"{k:>9s}" for k in pkeys))
    for c in sorted(CELLS, key=lambda c: (c["prompt"], c["tag"])):
        vals = "".join(f"{(c[k] if c.get(k) is not None else float('nan')):9.3f}" for k in pkeys)
        print(f"{c['prompt']:11s}{c['answer'][:15]:16s}{c['tag']:22s}{vals}")
    n_in = sum(1 for c in CELLS if c["tag"] != "off_category")
    n_off = sum(1 for c in CELLS if c["tag"] == "off_category")
    print(f"\nin-category cells: {n_in}   off-category cells: {n_off}   total: {len(CELLS)}")

# ================================================================= 3 =========
section("3. Per judge x question: pooled P(yes)")
QUESTIONS = ["neutral", "placebo", "rival_norep2", "rival", "named"]
if not judgements:
    no_rows("judgements")
else:
    parsed = [r for r in judgements if r.get("yn") in ("yes", "no") and not r.get("error")]

    def sub_for(j, q, keyset):
        return [r for r in parsed if r["judge"] == j and r["question"] == q and (r["prompt"], r["answer"]) in keyset]

    for j in JUDGES:
        for q in QUESTIONS:
            inc = sub_for(j, q, INCAT_KEYS)
            off = sub_for(j, q, OFFCAT_KEYS)
            if not inc and not off:
                continue
            if inc:
                k = sum(1 for r in inc if r["yn"] == "yes")
                lo, hi = clopper_pearson(k, len(inc))
                below8 = defaultdict(list)
                for r in inc:
                    below8[(r["prompt"], r["answer"])].append(r["yn"] == "yes")
                n_below8 = sum(1 for v in below8.values() if not all(v))
                print(f"judge={j:6s} q={q:14s} in-category  {k:3d}/{len(inc):3d} = {k/len(inc):.3f}  "
                      f"95% CP [{lo:.3f},{hi:.3f}]  cells<8/8: {n_below8}/{len(below8)}")
            if off:
                k = sum(1 for r in off if r["yn"] == "yes")
                lo, hi = clopper_pearson(k, len(off))
                print(f"judge={j:6s} q={q:14s} off-category {k:3d}/{len(off):3d} = {k/len(off):.3f}  95% CP [{lo:.3f},{hi:.3f}]")
            g = defaultdict(list)
            for r in [x for x in parsed if x["judge"] == j and x["question"] == q and (x["prompt"], x["answer"]) in CELLKEYS]:
                g[group_tag(r["tag"], r["prompt"], r["answer"], j)].append(r["yn"] == "yes")
            if g:
                print("    by tag-group: " + "  ".join(f"{k}={np.mean(v):.2f}(n{len(v)})" for k, v in sorted(g.items())))

# ================================================================= 4 =========
section("4. Frame chain (paired over in-category cells, cell P(yes))")
if not judgements:
    no_rows("frame chain")
else:
    STEPS = [("neutral", "placebo"), ("placebo", "rival_norep2"), ("rival_norep2", "rival"),
              ("neutral", "rival"), ("placebo", "rival")]
    for j in JUDGES:
        cellq = defaultdict(dict)
        for r in parsed:
            if r["judge"] == j and (r["prompt"], r["answer"]) in INCAT_KEYS:
                cellq[(r["prompt"], r["answer"])].setdefault(r["question"], []).append(r["yn"] == "yes")
        cellmean = {k: {q: np.mean(v) for q, v in d.items()} for k, d in cellq.items()}
        for qa, qb in STEPS:
            pairs = [(d[qa], d[qb]) for d in cellmean.values() if qa in d and qb in d]
            if not pairs:
                continue
            a, b = np.array(pairs).T
            diffs = a - b
            higher = int(np.sum(diffs > 0))
            lower = int(np.sum(diffs < 0))
            p = wilcoxon_p(list(diffs))
            print(f"judge={j:6s} {qa:13s} - {qb:13s}: mean diff={diffs.mean():+.3f}  "
                  f"higher={higher} lower={lower} (n={len(pairs)})  Wilcoxon p={p:.3g}")
        off = [r for r in parsed if r["judge"] == j and (r["prompt"], r["answer"]) in OFFCAT_KEYS]
        for q in ("neutral", "rival"):
            sub = [r for r in off if r["question"] == q]
            if sub:
                k = sum(1 for r in sub if r["yn"] == "yes")
                print(f"judge={j:6s} off-category {q:8s}: {k}/{len(sub)} = {k/len(sub):.3f}")

# ================================================================ 4b =========
section("4b. Frame chain, prompt level (paired over prompts, prompt mean of in-category cell P(yes))")
if not judgements:
    no_rows("frame chain, prompt level")
else:
    STEPS_P = [("neutral", "placebo"), ("placebo", "rival_norep2"), ("rival_norep2", "rival"),
               ("neutral", "rival"), ("placebo", "rival")]
    for j in JUDGES:
        cellq = defaultdict(dict)
        for r in parsed:
            if r["judge"] == j and (r["prompt"], r["answer"]) in INCAT_KEYS:
                cellq[(r["prompt"], r["answer"])].setdefault(r["question"], []).append(r["yn"] == "yes")
        cellmean = {k: {q: float(np.mean(v)) for q, v in d.items()} for k, d in cellq.items()}
        for qa, qb in STEPS_P:
            byprompt = defaultdict(list)
            for (prompt, answer), d in cellmean.items():
                if qa in d and qb in d:
                    byprompt[prompt].append((d[qa], d[qb]))
            if not byprompt:
                continue
            diffs = []
            for prompt in sorted(byprompt):
                vals = byprompt[prompt]
                diffs.append(float(np.mean([a for a, _ in vals]) - np.mean([b for _, b in vals])))
            arr = np.array(diffs)
            higher = int(np.sum(arr > 0))
            lower = int(np.sum(arr < 0))
            tied = int(np.sum(arr == 0))
            p_w = wilcoxon_p(diffs)
            nnz = higher + lower
            p_s = stats.binomtest(higher, nnz, 0.5).pvalue if nnz else float("nan")
            fw = "nan" if p_w != p_w else f"{p_w:.3g}"
            fs = "nan" if p_s != p_s else f"{p_s:.3g}"
            print(f"judge={j:6s} {qa:13s} - {qb:13s}: mean diff={arr.mean():+.3f}  "
                  f"higher={higher} lower={lower} tied={tied} (n prompts={len(diffs)})  "
                  f"Wilcoxon p={fw}  sign p={fs}")

# ================================================================= 5 =========
section("5. Label control (named question: assistant vs user2 layout)")
if userturn2_file:
    user2_rows = [r for r in userturn2_file if r.get("yn") in ("yes", "no") and not r.get("error")]
    user2_source = f"{PREFIX}_judgements_userturn2.jsonl"
elif judgements:
    user2_rows = [r for r in judgements if r.get("question") in ("named_userturn2", "named_userturn") and r.get("yn") in ("yes", "no") and not r.get("error")]
    user2_source = f"{PREFIX}_judgements.jsonl (question=named_userturn2 or named_userturn)"
else:
    user2_rows = []
    user2_source = None

assist_rows = [r for r in (judgements or []) if r.get("question") == "named" and r.get("yn") in ("yes", "no") and not r.get("error")]

if not assist_rows and not user2_rows:
    no_rows("label control")
else:
    print(f"(user2 source: {user2_source})")
    for j in JUDGES:
        a_inc = [r for r in assist_rows if r["judge"] == j and (r["prompt"], r["answer"]) in INCAT_KEYS]
        u_inc = [r for r in user2_rows if r["judge"] == j and (r["prompt"], r["answer"]) in INCAT_KEYS]
        a_off = [r for r in assist_rows if r["judge"] == j and (r["prompt"], r["answer"]) in OFFCAT_KEYS]
        u_off = [r for r in user2_rows if r["judge"] == j and (r["prompt"], r["answer"]) in OFFCAT_KEYS]
        if not a_inc and not u_inc:
            continue

        def yn(rs):
            return sum(1 for r in rs if r["yn"] == "yes"), len(rs)

        ak, an = yn(a_inc)
        uk, un = yn(u_inc)
        print(f"judge={j:6s} in-category   assistant {ak}/{an}   user2 {uk}/{un}")
        ak, an = yn(a_off)
        uk, un = yn(u_off)
        print(f"judge={j:6s} off-category  assistant {ak}/{an}   user2 {uk}/{un}")

        ga = defaultdict(list)
        gu = defaultdict(list)
        for r in [x for x in assist_rows if x["judge"] == j and (x["prompt"], x["answer"]) in CELLKEYS]:
            ga[group_tag(r["tag"], r["prompt"], r["answer"], j)].append(r["yn"] == "yes")
        for r in [x for x in user2_rows if x["judge"] == j and (x["prompt"], x["answer"]) in CELLKEYS]:
            gu[group_tag(r["tag"], r["prompt"], r["answer"], j)].append(r["yn"] == "yes")
        tags = sorted(set(ga) | set(gu))
        for t in tags:
            av, uv = ga.get(t, []), gu.get(t, [])
            a_str = f"{sum(av)}/{len(av)}" if av else "-"
            u_str = f"{sum(uv)}/{len(uv)}" if uv else "-"
            print(f"    tag-group={t:20s} assistant {a_str:8s} user2 {u_str:8s}")

        per_prompt = defaultdict(list)
        for r in u_inc + u_off:
            per_prompt[r["prompt"]].append(r["yn"] == "yes")
        if per_prompt:
            print("    user2 by prompt: " + "  ".join(f"{p}={sum(v)}/{len(v)}" for p, v in sorted(per_prompt.items())))

# ================================================================= 6 =========
section("6. Off-category detail (judge, prompt, answer) x question")
if not judgements:
    no_rows("off-category detail")
else:
    keys = sorted(OFFCAT_KEYS)
    for j in JUDGES:
        for prompt, answer in keys:
            line_parts = []
            for q in ("neutral", "rival", "named"):
                sub = [r for r in parsed if r["judge"] == j and r["question"] == q and r["prompt"] == prompt and r["answer"] == answer]
                if sub:
                    k = sum(1 for r in sub if r["yn"] == "yes")
                    line_parts.append(f"{q}={k}/{len(sub)}")
            if line_parts:
                print(f"judge={j:6s} prompt={prompt:10s} answer={answer:12s} " + "  ".join(line_parts))

# ================================================================= 7 =========
section("7. Ownership vs log own-probability (tab:rho)")
if not judgements:
    no_rows("ownership vs own-probability")
else:
    for j in JUDGES:
        for q in QUESTIONS + ["rival_named"]:
            sub = [r for r in parsed if r["judge"] == j and r["question"] == q and (r["prompt"], r["answer"]) in INCAT_KEYS]
            if len(sub) < 4:
                continue
            cellyn = defaultdict(list)
            for r in sub:
                cellyn[(r["prompt"], r["answer"])].append(r["yn"] == "yes")
            xs, ys = [], []
            for (pr, a), v in cellyn.items():
                xs.append(own_logp(pr, j, cell_p(j, pr, a)))
                ys.append(np.mean(v))
            rho, p = stats.spearmanr(xs, ys)
            print(f"judge={j:6s} readout={q:14s} rho={rho:+.2f} (p={p:.2g})  n={len(cellyn)} cells")

    if conf_rows:
        cparsed = [r for r in conf_rows if r.get("conf") is not None and not r.get("error")]
        for j in JUDGES:
            sub = [r for r in cparsed if r["judge"] == j and (r["prompt"], r["answer"]) in INCAT_KEYS]
            if len(sub) < 4:
                continue
            cellconf = defaultdict(list)
            for r in sub:
                cellconf[(r["prompt"], r["answer"])].append(r["conf"])
            xs, ys = [], []
            for (pr, a), v in cellconf.items():
                xs.append(own_logp(pr, j, cell_p(j, pr, a)))
                ys.append(np.mean(v))
            rho, p = stats.spearmanr(xs, ys)
            print(f"judge={j:6s} readout=confidence     rho={rho:+.2f} (p={p:.2g})  n={len(cellconf)} cells")
    else:
        no_rows("confidence vs own-probability")

# ================================================================= 8 =========
section("8. Confidence")
if not conf_rows:
    no_rows("confidence")
else:
    cparsed = [r for r in conf_rows if r.get("conf") is not None and not r.get("error")]
    for j in JUDGES:
        sub = [r for r in cparsed if r["judge"] == j]
        if not sub:
            continue
        cellconf = defaultdict(list)
        for r in sub:
            cellconf[(r["prompt"], r["answer"], r["tag"])].append(r["conf"])
        print(f"\n-- judge={j}: per-cell confidence")
        for (pr, a, tag), v in sorted(cellconf.items()):
            print(f"  {pr:11s}{a[:15]:16s}{tag:22s} n={len(v):2d} mean={np.mean(v):6.1f} sd={np.std(v):5.1f}")
        inc = [r for r in sub if (r["prompt"], r["answer"]) in INCAT_KEYS]
        off = [r for r in sub if (r["prompt"], r["answer"]) in OFFCAT_KEYS]
        if inc:
            print(f"  in-category mean={np.mean([r['conf'] for r in inc]):.1f} (n={len(inc)})")
        if off:
            print(f"  off-category mean={np.mean([r['conf'] for r in off]):.1f} (n={len(off)})")
        prod = [r for r in inc if (r.get(f"p_{j}") or 0) > 0]
        never = [r for r in inc if (r.get(f"p_{j}") or 0) == 0]
        if prod and never:
            print(f"  produced (own p>0) mean={np.mean([r['conf'] for r in prod]):.1f} (n={len(prod)})  "
                  f"never-produced (own p==0) mean={np.mean([r['conf'] for r in never]):.1f} (n={len(never)})")

        other = ([m for m in JUDGES if m != j] or ["other"])[0]
        print(f"  per-prompt: own-top conf vs {other}-top conf vs valid_unsampled conf")
        for prompt in sorted({c["prompt"] for c in CELLS}):
            own_top = next((c["answer"] for c in CELLS if c["prompt"] == prompt and c["tag"] == f"{j}_top"), None)
            other_top = next((c["answer"] for c in CELLS if c["prompt"] == prompt and c["tag"] == f"{other}_top"), None)
            vu = next((c["answer"] for c in CELLS if c["prompt"] == prompt and c["tag"] == "valid_unsampled"), None)

            def mean_conf(answer):
                if answer is None:
                    return None
                vals = [r["conf"] for r in sub if r["prompt"] == prompt and r["answer"] == answer]
                return np.mean(vals) if vals else None

            ot, oth, vut = mean_conf(own_top), mean_conf(other_top), mean_conf(vu)
            parts = []
            if own_top is not None and ot is not None:
                parts.append(f"{own_top}={ot:.1f}")
            if other_top is not None and oth is not None:
                parts.append(f"{other_top}({other})={oth:.1f}")
            if vu is not None and vut is not None:
                parts.append(f"{vu}(unsampled)={vut:.1f}")
            if parts:
                print(f"    {prompt:11s} " + "  vs  ".join(parts))

# ================================================================= 9 =========
section("9. Explicit self-prediction")
if not explicit_rows:
    no_rows("explicit self-prediction")
else:
    exparsed = [r for r in explicit_rows if r.get("chosen") in ("top", "other") and not r.get("error")]
    for j in JUDGES:
        sub = [r for r in exparsed if r["judge"] == j]
        if not sub:
            continue
        inc = [r for r in sub if r.get("b_tag") != "off_category"]
        if inc:
            frac = np.mean([r["chosen"] == "top" for r in inc])
            print(f"judge={j:6s} picks own top word: {frac:.2f} of {len(inc)} in-category pairs")
        pairs = defaultdict(list)
        for r in sub:
            pairs[(r["prompt"], r["a"], r["b"], r["b_tag"])].append(r["chosen"])
        print(f"-- judge={j}: per pair, chosen==top count / n")
        for (pr, a, b, btag), v in sorted(pairs.items()):
            top_n = sum(1 for c in v if c == "top")
            print(f"  {pr:11s}{a[:11]:12s}vs {b[:13]:14s}{btag:18s} {top_n}/{len(v)}")
        flips = [(k, v) for k, v in pairs.items() if sum(1 for c in v if c == "other") >= 5]
        if flips:
            print(f"-- judge={j}: pairs picking the OTHER word >=5/6 times")
            for (pr, a, b, btag), v in flips:
                other_n = sum(1 for c in v if c == "other")
                print(f"  {pr:11s}{a} vs {b} ({btag}): other {other_n}/{len(v)}")

# ================================================================ 10 =========
section("10. Stage E (within-support gradient)")
if not within_rows:
    no_rows("stage E")
else:
    for j in JUDGES:
        cellw = defaultdict(lambda: {"yes": [], "conf": []})
        meta = {}
        for r in within_rows:
            if r["judge"] != j or r.get("error"):
                continue
            k = (r["prompt"], r["answer"])
            meta[k] = r
            if r["readout"] == "rival" and r.get("yn") in ("yes", "no"):
                cellw[k]["yes"].append(r["yn"] == "yes")
            if r["readout"] == "conf" and r.get("conf") is not None:
                cellw[k]["conf"].append(r["conf"])
        if not cellw:
            continue
        print(f"judge={j:6s} n cells={len(cellw)}")
        X, Y1 = [], []
        for k, v in cellw.items():
            m = meta[k]
            if v["yes"]:
                X.append(math.log(max(m.get("p_own", 0.0) or 0.0, 1e-6)))
                Y1.append(np.mean(v["yes"]))
        if len(X) >= 4:
            rho, p = stats.spearmanr(X, Y1)
            print(f"  Spearman(rival P(yes), log p_own) rho={rho:+.2f} p={p:.2g}  n={len(X)}")

        confs = [np.mean(v["conf"]) for v in cellw.values() if v["conf"]]
        if confs:
            print(f"  cell confidence range: {min(confs):.1f} to {max(confs):.1f}")

        keys = [k for k, v in cellw.items() if v["conf"]]
        if len(keys) >= 4:
            Xc = np.array([math.log(max(meta[k].get("p_own", 0.0) or 0.0, 1e-6)) for k in keys])
            Yc = np.array([np.mean(cellw[k]["conf"]) for k in keys])
            prompts = sorted({k[0] for k in keys})
            D = np.array([[1.0 if k[0] == pr else 0.0 for pr in prompts] for k in keys])
            A = np.column_stack([Xc, D])
            beta, *_ = np.linalg.lstsq(A, Yc, rcond=None)
            resid = Yc - A @ beta
            dof = len(keys) - A.shape[1]
            if dof > 0:
                s2 = resid @ resid / dof
                cov = s2 * np.linalg.pinv(A.T @ A)
                t = beta[0] / math.sqrt(cov[0, 0]) if cov[0, 0] > 0 else float("nan")
                p = 2 * stats.t.sf(abs(t), dof) if not math.isnan(t) else float("nan")
                print(f"  confidence slope per nat (prompt fixed effects) = {beta[0]:+.3f}  p={p:.3g}  n={len(keys)}")
