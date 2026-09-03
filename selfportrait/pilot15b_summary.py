"""Score pilot 15b (clean-harness one-word spot check) against its pre-registration.

Reads out/clean_judgements.jsonl. Predictions (docs/PILOT-15-prompt-effects.md):
(a) named assistant >= 0.95 both judges; user2 <= 0.05 Haiku, <= 0.15 Opus;
    refuter assistant < 0.80 or user2 > 0.30.
(b) neutral in-category >= 0.95 both judges.
(c) rival in-category between 0.30 and 0.90 both judges; refuter >= 0.95 or <= 0.10.
(d) Spearman of rival P(Yes) vs log own-probability, in-category cells, |rho| < 0.3.
"""
import json
import math
from collections import defaultdict

from scipy.stats import spearmanr

ROWS = [json.loads(line) for line in open("out/clean_judgements.jsonl")]
ROWS = [r for r in ROWS if r.get("yn") in ("yes", "no")]
print(f"parsed rows: {len(ROWS)}")


def cells(judge, question, incat=True):
    g = defaultdict(list)
    for r in ROWS:
        if r["judge"] != judge or r["question"] != question:
            continue
        if incat and r["tag"] == "off_category":
            continue
        g[(r["prompt"], r["answer"], r["tag"])].append(r)
    out = {}
    for k, rs in g.items():
        out[k] = (sum(r["yn"] == "yes" for r in rs), len(rs), rs[0].get(f"p_{judge}") or 0.0)
    return out


def pooled(c):
    y = sum(v[0] for v in c.values())
    n = sum(v[1] for v in c.values())
    return y, n, y / n if n else float("nan")


for j in ("haiku", "opus"):
    print(f"\n== {j} ==")
    for q in ("named", "named_userturn2", "neutral", "rival"):
        c = cells(j, q)
        y, n, p = pooled(c)
        lo = min(v[0] / v[1] for v in c.values())
        hi = max(v[0] / v[1] for v in c.values())
        print(f"{q:16s} in-category cells={len(c):2d}  yes={y:3d}/{n:3d}  P(Yes)={p:.3f}  cell range {lo:.2f}-{hi:.2f}")
    # off-category rows, for completeness
    for q in ("named", "named_userturn2", "neutral", "rival"):
        c = {k: v for k, v in cells(j, q, incat=False).items() if k[2] == "off_category"}
        y, n, p = pooled(c)
        print(f"{q:16s} off-category  cells={len(c):2d}  yes={y:3d}/{n:3d}  P(Yes)={p:.3f}")
    # (d) Spearman rival P(Yes) vs log own p, in-category cells
    c = cells(j, "rival")
    xs = [math.log(max(v[2], 1 / 96)) for v in c.values()]
    ys = [v[0] / v[1] for v in c.values()]
    rho, pval = spearmanr(xs, ys)
    print(f"(d) rival Spearman vs log own-p: rho={rho:+.2f} p={pval:.2f} n={len(c)} (own-p floor 1/96)")
    nz = [(x, y) for x, y in zip(xs, ys) if x > math.log(1 / 96)]
    if len(nz) >= 4:
        rho2, p2 = spearmanr([a for a, _ in nz], [b for _, b in nz])
        print(f"    cells with own-p > 0 only: rho={rho2:+.2f} p={p2:.2f} n={len(nz)}")

cost = sum(r.get("cost") or 0 for r in ROWS)
print(f"\njudgement cost recorded: ${cost:.2f}")
try:
    fc = sum((json.loads(line).get("cost") or 0) for line in open("out/clean_forks.jsonl"))
    print(f"fork cost recorded: ${fc:.2f}")
except FileNotFoundError:
    pass
