"""Pilot 17c scoring: predictions (a) to (f) of the 17c pre-registration in
docs/PILOT-17-paragraph-ownership.md, from SP_OUT_DIR (default out/p17c):
para_forks.jsonl, para_cells.json, para_judgements.jsonl, para_pairs.jsonl.
Run with SP_OUT_DIR=out to reproduce 17b's plain-arm figures as a regression check."""
import collections
import json
import os
import re
from pathlib import Path

from scipy.stats import binomtest, wilcoxon

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(os.environ.get("SP_OUT_DIR", ROOT / "out" / "p17c"))
PROMPTS = ["sky", "tides", "bread", "sleep", "rust", "rainbow",
           "salt", "leaves", "vaccines", "thunder", "fridge", "ice"]
OTHER = ("other_claude", "other_vendor")
JUDGES = ("haiku", "opus", "gpt")


def load(name):
    p = OUT / name
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()] if p.exists() else []


F = load("para_forks.jsonl")
J = load("para_judgements.jsonl")
P = [r for r in load("para_pairs.jsonl") if not r["comparison"].endswith("_norm")]
C = json.loads((OUT / "para_cells.json").read_text()) if (OUT / "para_cells.json").exists() else {}


def words(t):
    return re.findall(r"[A-Za-z']+", t or "")


def article_rate(t):
    w = words(t)
    return (sum(1 for x in w if x.lower() in ("a", "an", "the")) / len(w), len(w)) if w else (0.0, 0)


def caveman(t):
    """Register flag: fewer than 2.5 articles per 100 words on a paragraph of 20+ words."""
    rate, n = article_rate(t)
    return n >= 20 and rate < 0.025


def pyes(rows):
    ys = [r["yn"] for r in rows if r.get("yn") in ("yes", "no")]
    return (sum(1 for y in ys if y == "yes") / len(ys), len(ys)) if ys else (float("nan"), 0)


def gap(judge, question):
    def pm(cell):
        return {p: pyes([r for r in J if r["judge"] == judge and r["question"] == question
                         and r["cell"] == cell and r["prompt"] == p]) for p in PROMPTS}
    own, oth = pm("own"), [pm(c) for c in OTHER]
    own_v = [own[p][0] for p in PROMPTS]
    oth_v = [(oth[0][p][0] + oth[1][p][0]) / 2 for p in PROMPTS]
    n_own = sum(own[p][1] for p in PROMPTS)
    n_oth = sum(o[p][1] for o in oth for p in PROMPTS)
    pooled_own = sum(own[p][0] * own[p][1] for p in PROMPTS) / n_own if n_own else float("nan")
    pooled_oth = sum(o[p][0] * o[p][1] for o in oth for p in PROMPTS) / n_oth if n_oth else float("nan")
    diffs = [a - b for a, b in zip(own_v, oth_v)]
    wp = wilcoxon(own_v, oth_v).pvalue if len(set(diffs)) > 1 and any(d != 0 for d in diffs) else float("nan")
    return dict(pooled_own=pooled_own, pooled_oth=pooled_oth, gap=pooled_own - pooled_oth, n_own=n_own,
                n_oth=n_oth, wins=sum(1 for d in diffs if d > 0), ties=sum(1 for d in diffs if d == 0),
                wilcoxon_p=wp, per_prompt={p: (own[p][0], oth[0][p][0], oth[1][p][0]) for p in PROMPTS})


def show_gap(label, g):
    print(f"{label}: own {g['pooled_own']:.3f} (n={g['n_own']}) other {g['pooled_oth']:.3f} (n={g['n_oth']}) "
          f"gap {g['gap']:+.3f}; own>other on {g['wins']}/12 prompts, {g['ties']} ties; Wilcoxon p={g['wilcoxon_p']:.4f}")
    print("    " + ", ".join(f"{p} {o:.2f}/{oc:.2f}/{ov:.2f}" for p, (o, oc, ov) in g["per_prompt"].items()))


def acc(rows, label):
    parsed = [r for r in rows if r["correct"] is not None]
    k, n = sum(1 for r in parsed if r["correct"]), len(parsed)
    if n == 0:
        print(f"{label}: no parsed trials ({len(rows)} refusals)")
        return
    bt = binomtest(k, n, 0.5)
    ci = bt.proportion_ci(0.95, method="exact")
    pos1 = sum(1 for r in parsed if r["answer"] == 1)
    print(f"{label}: {k}/{n} = {k / n:.3f} [95% {ci.low:.2f}, {ci.high:.2f}] p={bt.pvalue:.4f}; "
          f"{len(rows) - n} refusals; chose (1) {pos1}/{n}")
    return parsed


def pair_rows(judge, comp):
    return [r for r in P if r["judge"] == judge and r["comparison"] == comp]


def own_longer(r):
    cell = C.get(f"{r['prompt']}|{r['judge']}")
    if not cell:
        return None
    own_n = len(words(cell["own"]["text"]))
    oth_n = len(words(cell[r["comparison"].replace("own_vs_", "")]["text"]))
    return None if own_n == oth_n else own_n > oth_n


print("=== counts ===")
print("forks", len(F), "judgements", len(J), "pairs", len(P), "cells", len(C),
      "errors", sum(1 for r in F + J + P if r.get("error")))
print("forks per model:", dict(collections.Counter(r["model"] for r in F)))
print("judgement rows per judge/question:", {(j, q): sum(1 for r in J if r["judge"] == j and r["question"] == q)
                                             for j in JUDGES for q in ("neutral", "rival")})

print("\n=== (a) Opus rival gap ===")
show_gap("opus rival", gap("opus", "rival"))

print("\n=== (b) pairwise Opus and GPT; (d) length split ===")
for judge in ("opus", "gpt", "haiku"):
    for comp in ("own_vs_other_claude", "own_vs_other_vendor"):
        rows = pair_rows(judge, comp)
        parsed = acc(rows, f"{judge} {comp}") or []
        per = {p: (sum(1 for r in parsed if r["prompt"] == p and r["correct"]),
                   sum(1 for r in parsed if r["prompt"] == p)) for p in PROMPTS}
        print("    per prompt: " + ", ".join(f"{p} {k}/{n}" for p, (k, n) in per.items()))
        low = [p for p, (k, n) in per.items() if n and k <= 2]
        print(f"    prompts at <=2/8: {low}")
        longer = [r for r in rows if own_longer(r) is True]
        shorter = [r for r in rows if own_longer(r) is False]
        acc(longer, f"    own longer ({len({r['prompt'] for r in longer})} prompts)")
        acc(shorter, f"    own shorter ({len({r['prompt'] for r in shorter})} prompts)")

print("\n=== (c) register check on Opus forks ===")
op = [r for r in F if r["model"] == "opus" and not r.get("error")]
flag = [r for r in op if caveman(r["raw"])]
print(f"opus forks {len(op)}, flagged {len(flag)}:",
      [(r["prompt"], round(article_rate(r['raw'])[0], 3), r["raw"][:60]) for r in flag])
for m in ("haiku", "opus", "gpt"):
    fr = [r for r in F if r["model"] == m and not r.get("error")]
    fl = [r for r in fr if caveman(r["raw"])]
    print(f"  {m}: {len(fl)}/{len(fr)} flagged; mean words {sum(len(words(r['raw'])) for r in fr) / max(len(fr), 1):.1f}")
own_flag = [(k, caveman(v["own"]["text"])) for k, v in C.items() if k.endswith("|opus")]
print("  opus own-cell paragraphs flagged:", [k for k, f in own_flag if f])

print("\n=== (e) Haiku rival gap ===")
show_gap("haiku rival", gap("haiku", "rival"))
print("\n=== GPT rival gap (context) ===")
show_gap("gpt rival", gap("gpt", "rival"))

print("\n=== (f) neutral, every judge and source ===")
for judge in JUDGES:
    cells = {c: pyes([r for r in J if r["judge"] == judge and r["question"] == "neutral" and r["cell"] == c])
             for c in ("own", "other_claude", "other_vendor", "shifted")}
    print(f"  {judge:5s} " + "  ".join(f"{c} {v[0]:.3f}/{v[1]}" for c, v in cells.items()))
sh = {j: pyes([r for r in J if r["judge"] == j and r["question"] == "rival" and r["cell"] == "shifted"]) for j in JUDGES}
print("  shifted under rival:", {j: f"{v[0]:.3f}/{v[1]}" for j, v in sh.items()})

print("\n=== paragraph length by source (first fork per prompt) ===")
for m in ("haiku", "opus", "gpt"):
    firsts = {}
    for r in F:
        if r["model"] == m and not r.get("error") and r["prompt"] not in firsts:
            firsts[r["prompt"]] = len(words(r["raw"]))
    print(f"  {m}: mean {sum(firsts.values()) / max(len(firsts), 1):.1f} words over {len(firsts)} prompts")

print("\n=== cost ===")
cost = collections.defaultdict(float)
for r in F + J + P:
    cost[r.get("judge") or r.get("model")] += r.get("cost") or 0
print({k: round(v, 2) for k, v in cost.items()}, "total", round(sum(cost.values()), 2))
