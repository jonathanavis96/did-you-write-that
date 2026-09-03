"""Pilot 14 scoring: the five pre-registered items of docs/PILOT-14-local-scale-series.md,
computed from out/own_local_<slug>.jsonl (DirectML rows). Cell values are exact
probabilities, so statistics are on cells and on prompt-level means (paired by prompt)."""
import json
import math
from pathlib import Path

import numpy as np
from scipy import stats

OUT = Path(__file__).resolve().parent.parent / "out"
FILES = {
    "1.5B": "own_local_qwen2.5-1.5b-instruct.jsonl",
    "3B": "own_local_qwen2.5-3b-instruct.jsonl",
    "4B": "own_local_qwen3-4b-instruct-2507.jsonl",
}


def load(name):
    return [json.loads(x) for x in (OUT / name).read_text().splitlines() if x.strip()]


def cells(rows, layout, question, incat=True):
    return [r for r in rows if r["layout"] == layout and r["question"] == question
            and ((r["tag"] != "off_category") if incat else (r["tag"] == "off_category"))]


def prompt_means(rs):
    d = {}
    for r in rs:
        d.setdefault(r["prompt"], []).append(r["p_yes"])
    return {p: float(np.mean(v)) for p, v in d.items()}


def paired(a, b):
    """Prompt-level paired difference a - b: mean, wins, Wilcoxon p."""
    ps = sorted(set(a) & set(b))
    d = [a[p] - b[p] for p in ps]
    nz = [x for x in d if x != 0]
    wp = stats.wilcoxon(nz).pvalue if len(nz) >= 5 else float("nan")
    return dict(n=len(ps), mean=float(np.mean(d)), wins=sum(1 for x in d if x > 0),
                losses=sum(1 for x in d if x < 0), p=wp)


def fmt(d):
    return f"mean {d['mean']:+.3f} over {d['n']} prompts, +{d['wins']}/-{d['losses']}, Wilcoxon p={d['p']:.3g}"


for scale, name in FILES.items():
    R = load(name)
    print(f"\n=== {scale}: {name} ({len(R)} rows, {R[0]['model']}, {R[0]['device']}/{R[0]['dtype']}) ===")
    print("prompts", len({r['prompt'] for r in R}), "in-category cells per (layout,question):",
          {(la, q): len(cells(R, la, q)) for la in ("assistant", "user2") for q in ("named", "neutral")})
    A = {q: cells(R, "assistant", q) for q in ("named", "neutral", "placebo", "rival_norep2")}
    U = {q: cells(R, "user2", q) for q in ("named", "neutral", "placebo", "rival_norep2")}
    m = lambda rs: float(np.mean([r["p_yes"] for r in rs]))  # noqa: E731
    print("cell means  assistant:", {q: round(m(v), 3) for q, v in A.items()},
          " user2:", {q: round(m(v), 3) for q, v in U.items()})
    # 1. label effect under named: assistant - user2
    print("(1) named assistant-user2: cells", f"{m(A['named']) - m(U['named']):+.3f};",
          "prompt-paired", fmt(paired(prompt_means(A["named"]), prompt_means(U["named"]))))
    print("    neutral assistant-user2 (context):", f"{m(A['neutral']) - m(U['neutral']):+.3f}")
    # 2. likelihood term: Spearman(P(yes), log p_tf), neutral, assistant, in-category
    y = [r["p_yes"] for r in A["neutral"]]
    x = [math.log(max(r["p_tf"], 1e-300)) for r in A["neutral"]]
    rho, p = stats.spearmanr(x, y)
    print(f"(2) Spearman neutral/assistant rho={rho:+.3f} p={p:.3g} (n={len(y)}); P(yes) sd={np.std(y):.3f}")
    for q in ("named", "placebo"):
        yy = [r["p_yes"] for r in A[q]]
        xx = [math.log(max(r["p_tf"], 1e-300)) for r in A[q]]
        rr, pp = stats.spearmanr(xx, yy)
        print(f"    {q}: rho={rr:+.3f} p={pp:.3g}")
    # 3. placebo
    print(f"(3) neutral-placebo assistant: cells {m(A['neutral']) - m(A['placebo']):+.3f};",
          fmt(paired(prompt_means(A["neutral"]), prompt_means(A["placebo"]))))
    # 4. rival
    print(f"(4) placebo-rival_norep2 assistant: cells {m(A['placebo']) - m(A['rival_norep2']):+.3f};",
          fmt(paired(prompt_means(A["placebo"]), prompt_means(A["rival_norep2"]))))
    # 5. off-category under named, assistant
    off = cells(R, "assistant", "named", incat=False)
    print(f"(5) named assistant in-category {m(A['named']):.3f} - off-category {m(off):.3f} = "
          f"{m(A['named']) - m(off):+.3f};", fmt(paired(prompt_means(A["named"]), prompt_means(off))))
    offn = cells(R, "assistant", "neutral", incat=False)
    print(f"    neutral: in {m(A['neutral']):.3f} off {m(offn):.3f}; user2 neutral off {m(cells(R, 'user2', 'neutral', False)):.3f}")
    # per-prompt named, both layouts
    pa, pu = prompt_means(A["named"]), prompt_means(U["named"])
    print("    per prompt named A/U: " + ", ".join(f"{p} {pa[p]:.2f}/{pu[p]:.2f}" for p in sorted(pa)))
