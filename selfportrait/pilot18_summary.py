"""Score pilot 18 (paragraph design, local scale series) against its pre-registration
(docs/PILOT-18-local-paragraph.md). Reads out/para_local_<model>.jsonl for the three
Qwen models. Items:
1. neutral: own minus mean of the other-author cells, paired over prompts (|d| < 0.10;
   refuter d >= +0.25 with Wilcoxon p < 0.05)
2. Spearman of P(Yes) against mean per-token log p over the 48 non-shifted cells, rival
   and neutral (|rho| < 0.3; refuter rho >= +0.37, p < 0.05)
3. placebo minus rival over all cells (>= 0.25; refuter < 0.10)
4. forced choice: mean exact P(own) per comparison over prompts (0.40 to 0.60 at 1.5B and
   3B; refuter >= 0.70 with >= 10/12 prompts above 0.5); P(choose 1) position bias
5. rival own minus shifted, reported
"""
import json
import statistics
from collections import defaultdict
from pathlib import Path

from scipy.stats import spearmanr, wilcoxon

ROOT = Path(__file__).resolve().parent.parent
MODELS = ["qwen2.5-1.5b-instruct", "qwen2.5-3b-instruct", "qwen3-4b-instruct-2507"]
OTHER = ("other_local", "other_opus", "other_gpt")
AUTHOR_CELLS = ("own",) + OTHER


def rows_for(slug):
    p = ROOT / "out" / f"para_local_{slug}.jsonl"
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()]


def paired(a, b):
    d = [x - y for x, y in zip(a, b)]
    nz = [x for x in d if x != 0]
    p = wilcoxon(nz).pvalue if len(nz) >= 5 else float("nan")
    return statistics.fmean(d), sum(x > 0 for x in d), sum(x < 0 for x in d), p


for slug in MODELS:
    rows = rows_for(slug)
    own_rows = [r for r in rows if r["stage"] == "own"]
    prompts = sorted({r["prompt"] for r in own_rows})
    P = {(r["prompt"], r["cell"], r["question"]): r for r in own_rows}
    forks = [r for r in rows if r["stage"] == "fork"]
    print(f"\n===== {slug}: {len(forks)} forks, {len(own_rows)} own rows, "
          f"{sum(r['stage'] == 'pair' for r in rows)} pair rows, {len(prompts)} prompts")
    cells_present = sorted({r["cell"] for r in own_rows})
    print("cells:", cells_present)

    # cell means per question
    for q in ("neutral", "placebo", "rival"):
        line = []
        for c in ("own",) + OTHER + ("shifted",):
            v = [P[(p, c, q)]["p_yes"] for p in prompts if (p, c, q) in P]
            line.append(f"{c}={statistics.fmean(v):.3f}(n{len(v)})" if v else f"{c}=--")
        print(f"{q:8s} " + "  ".join(line))

    # item 1
    ok = [p for p in prompts if all((p, c, "neutral") in P for c in AUTHOR_CELLS)]
    own = [P[(p, "own", "neutral")]["p_yes"] for p in ok]
    oth = [statistics.fmean(P[(p, c, "neutral")]["p_yes"] for c in OTHER) for p in ok]
    d, w, lo, pv = paired(own, oth)
    print(f"(1) neutral own - other: {d:+.3f}  own>other {w}/{len(ok)}, own<other {lo}/{len(ok)}, "
          f"Wilcoxon p={pv:.3g}")

    # item 2
    for q in ("rival", "neutral"):
        xs, ys = [], []
        for p in prompts:
            for c in AUTHOR_CELLS:
                if (p, c, q) in P:
                    xs.append(P[(p, c, q)]["mean_lp"])
                    ys.append(P[(p, c, q)]["p_yes"])
        rho, pv = spearmanr(xs, ys)
        print(f"(2) {q:7s} Spearman P(Yes) vs mean per-token log p: rho={rho:+.2f} p={pv:.3g} n={len(xs)}")
    own_lp = [P[(p, "own", "rival")]["mean_lp"] for p in prompts if (p, "own", "rival") in P]
    oth_lp = [P[(p, c, "rival")]["mean_lp"] for p in prompts for c in OTHER if (p, c, "rival") in P]
    print(f"    mean per-token log p: own {statistics.fmean(own_lp):.2f}, other cells {statistics.fmean(oth_lp):.2f}")

    # item 3
    keys = [(p, c) for p in prompts for c in AUTHOR_CELLS + ("shifted",)
            if (p, c, "placebo") in P and (p, c, "rival") in P]
    pl = [P[(p, c, "placebo")]["p_yes"] for p, c in keys]
    rv = [P[(p, c, "rival")]["p_yes"] for p, c in keys]
    d, w, lo, pv = paired(pl, rv)
    print(f"(3) placebo - rival over {len(keys)} cells: {d:+.3f}  placebo>rival {w}, < {lo}, p={pv:.3g}")

    # item 4
    pairs = [r for r in rows if r["stage"] == "pair"]
    by = defaultdict(lambda: defaultdict(list))
    for r in pairs:
        by[r["comparison"]][r["prompt"]].append(r)
    for comp, d_ in sorted(by.items()):
        per_prompt = [statistics.fmean(x["p_own"] for x in v) for v in d_.values()]
        pos1 = [x["p_choose_1"] for v in d_.values() for x in v]
        print(f"(4) {comp:20s} mean P(own)={statistics.fmean(per_prompt):.3f}  "
              f"prompts>0.5: {sum(x > 0.5 for x in per_prompt)}/{len(per_prompt)}  "
              f"min {min(per_prompt):.2f} max {max(per_prompt):.2f}  P(choose 1)={statistics.fmean(pos1):.3f}")

    # item 5
    ok = [p for p in prompts if (p, "own", "rival") in P and (p, "shifted", "rival") in P]
    d, w, lo, pv = paired([P[(p, "own", "rival")]["p_yes"] for p in ok],
                         [P[(p, "shifted", "rival")]["p_yes"] for p in ok])
    print(f"(5) rival own - shifted: {d:+.3f}  own>shifted {w}/{len(ok)}, p={pv:.3g}")
    words = [r["words"] for r in own_rows if r["cell"] == "own" and r["question"] == "neutral"]
    print(f"    own paragraph words: mean {statistics.fmean(words):.1f}, min {min(words)}, max {max(words)}")
