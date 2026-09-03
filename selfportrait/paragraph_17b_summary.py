"""Pilot 17b scoring: the pre-registered predictions (a) to (e) of
docs/PILOT-17-paragraph-ownership.md, computed from out/para_judgements.jsonl and
out/para_pairs.jsonl. Every number in the 17b results section comes from this script.

Prompt sets: ORIG = pilot 17's six prompts, NEW = 17b's six. Rows from the normalised
run carry a "_norm" suffix on question / comparison.
"""
import json
import collections
from pathlib import Path

from scipy.stats import wilcoxon, binomtest

OUT = Path(__file__).resolve().parent.parent / "out"
ORIG = ["sky", "tides", "bread", "sleep", "rust", "rainbow"]
NEW = ["salt", "leaves", "vaccines", "thunder", "fridge", "ice"]
ALL = ORIG + NEW
OTHER = ("other_claude", "other_vendor")


def load(name):
    return [json.loads(line) for line in (OUT / name).read_text().splitlines() if line.strip()]


J = load("para_judgements.jsonl")
P = load("para_pairs.jsonl")


def pyes(rows):
    ys = [r["yn"] for r in rows if r.get("yn") in ("yes", "no")]
    return (sum(1 for y in ys if y == "yes") / len(ys), len(ys)) if ys else (float("nan"), 0)


def prompt_means(judge, question, cell, prompts):
    """P(Yes) per prompt for one judge, question, cell."""
    out = {}
    for p in prompts:
        rows = [r for r in J if r["judge"] == judge and r["question"] == question
                and r["cell"] == cell and r["prompt"] == p]
        out[p] = pyes(rows)
    return out


def gap(judge, question, prompts):
    own = prompt_means(judge, question, "own", prompts)
    oth = [prompt_means(judge, question, c, prompts) for c in OTHER]
    own_v = [own[p][0] for p in prompts]
    oth_v = [(oth[0][p][0] + oth[1][p][0]) / 2 for p in prompts]
    n_own = sum(own[p][1] for p in prompts)
    pooled_own = sum(own[p][0] * own[p][1] for p in prompts) / n_own
    n_oth = sum(o[p][1] for o in oth for p in prompts)
    pooled_oth = sum(o[p][0] * o[p][1] for o in oth for p in prompts) / n_oth
    diffs = [a - b for a, b in zip(own_v, oth_v)]
    nonzero = [d for d in diffs if d != 0]
    wp = wilcoxon(own_v, oth_v).pvalue if len(nonzero) >= 1 and len(set(diffs)) > 1 else float("nan")
    wins = sum(1 for d in diffs if d > 0)
    return dict(pooled_own=pooled_own, pooled_oth=pooled_oth, gap=pooled_own - pooled_oth,
                n_own=n_own, n_oth=n_oth, wins=wins, ties=sum(1 for d in diffs if d == 0),
                wilcoxon_p=wp, per_prompt={p: (own[p][0], oth[0][p][0], oth[1][p][0]) for p in prompts})


def show_gap(label, g):
    print(f"{label}: own {g['pooled_own']:.3f} (n={g['n_own']}) other {g['pooled_oth']:.3f} "
          f"(n={g['n_oth']}) gap {g['gap']:+.3f}; own>other on {g['wins']}/{len(g['per_prompt'])} "
          f"prompts, {g['ties']} ties; Wilcoxon p={g['wilcoxon_p']:.3f}")
    for p, (o, oc, ov) in g["per_prompt"].items():
        print(f"    {p:9s} own {o:.2f}  other_claude {oc:.2f}  other_vendor {ov:.2f}")


def pair_acc(judge, comparison, prompts):
    rows = [r for r in P if r["judge"] == judge and r["comparison"] == comparison and r["prompt"] in prompts]
    parsed = [r for r in rows if r["correct"] is not None]
    k = sum(1 for r in parsed if r["correct"])
    n = len(parsed)
    if n == 0:
        return dict(k=0, n=0, refusals=len(rows))
    bt = binomtest(k, n, 0.5)
    ci = bt.proportion_ci(0.95, method="exact")
    pos1 = sum(1 for r in parsed if r["answer"] == 1)
    return dict(k=k, n=n, acc=k / n, p=bt.pvalue, lo=ci.low, hi=ci.high,
                refusals=len(rows) - n, chose1=pos1,
                per_prompt={p: (sum(1 for r in parsed if r["prompt"] == p and r["correct"]),
                                sum(1 for r in parsed if r["prompt"] == p)) for p in prompts})


def show_pair(label, a):
    if a["n"] == 0:
        print(f"{label}: no parsed trials ({a['refusals']} refusals)")
        return
    print(f"{label}: {a['k']}/{a['n']} = {a['acc']:.3f} [95% {a['lo']:.2f}, {a['hi']:.2f}] p={a['p']:.4f}; "
          f"{a['refusals']} refusals; chose (1) {a['chose1']}/{a['n']}")
    print("    per prompt: " + ", ".join(f"{p} {k}/{n}" for p, (k, n) in a["per_prompt"].items()))


print("=== counts ===")
print("judgement rows", len(J), "pair rows", len(P),
      "errors", sum(1 for r in J + P if r.get("error")))
for judge in ("haiku", "opus", "gpt"):
    for q in ("neutral", "placebo", "rival", "rival_norm"):
        c = collections.Counter(r["prompt"] in NEW for r in J if r["judge"] == judge and r["question"] == q)
        if c:
            print(f"  {judge:5s} {q:10s} rows: orig {c[False]} new {c[True]}")

print("\n=== (a) Opus rival, plain, twelve prompts ===")
ga = gap("opus", "rival", ALL)
show_gap("opus rival ALL", ga)
show_gap("opus rival ORIG only", gap("opus", "rival", ORIG))
show_gap("opus rival NEW only", gap("opus", "rival", NEW))

print("\n=== (b) Opus rival, normalised, twelve prompts ===")
gb = gap("opus", "rival_norm", ALL)
show_gap("opus rival_norm ALL", gb)
print(f"plain gap {ga['gap']:+.3f} vs normalised {gb['gap']:+.3f}: difference {abs(ga['gap'] - gb['gap']):.3f}")
sh_plain = pyes([r for r in J if r["judge"] == "opus" and r["question"] == "rival" and r["cell"] == "shifted"])
sh_norm = pyes([r for r in J if r["judge"] == "opus" and r["question"] == "rival_norm" and r["cell"] == "shifted"])
print(f"shifted under rival: plain {sh_plain[0]:.3f} (n={sh_plain[1]}), normalised {sh_norm[0]:.3f} (n={sh_norm[1]})")

print("\n=== (c) pairwise, GPT and Opus ===")
for judge in ("gpt", "opus"):
    for comp in ("own_vs_other_claude", "own_vs_other_vendor"):
        show_pair(f"{judge} {comp} plain NEW", pair_acc(judge, comp, NEW))
        show_pair(f"{judge} {comp} plain ORIG", pair_acc(judge, comp, ORIG))
        show_pair(f"{judge} {comp} norm NEW", pair_acc(judge, comp + "_norm", NEW))
        show_pair(f"{judge} {comp} norm ORIG", pair_acc(judge, comp + "_norm", ORIG))
        show_pair(f"{judge} {comp} norm ALL", pair_acc(judge, comp + "_norm", ALL))

print("\n=== (d) Haiku ===")
show_gap("haiku rival ALL", gap("haiku", "rival", ALL))
show_gap("haiku rival NEW", gap("haiku", "rival", NEW))
for comp in ("own_vs_other_claude", "own_vs_other_vendor"):
    show_pair(f"haiku {comp} plain ALL", pair_acc("haiku", comp, ALL))
    show_pair(f"haiku {comp} norm ALL", pair_acc("haiku", comp + "_norm", ALL))

print("\n=== (e) neutral and placebo, every judge and source ===")
for judge in ("haiku", "opus", "gpt"):
    for q in ("neutral", "placebo"):
        cells = {c: pyes([r for r in J if r["judge"] == judge and r["question"] == q and r["cell"] == c])
                 for c in ("own", "other_claude", "other_vendor", "shifted")}
        print(f"  {judge:5s} {q:8s} " + "  ".join(f"{c} {v[0]:.3f}/{v[1]}" for c, v in cells.items()))

print("\n=== GPT rival (context) ===")
show_gap("gpt rival ALL", gap("gpt", "rival", ALL))

print("\n=== cost ===")
cost = collections.defaultdict(float)
for name in ("para_forks.jsonl", "para_judgements.jsonl", "para_pairs.jsonl"):
    for r in load(name):
        cost[r.get("judge") or r.get("model")] += r.get("cost") or 0
print({k: round(v, 2) for k, v in cost.items()}, "total", round(sum(cost.values()), 2))
