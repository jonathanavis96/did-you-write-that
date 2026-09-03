"""Summarise the local exact-probability arm of pilot 11 (out/own_local.jsonl)."""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy import stats

rows = [json.loads(x) for x in (Path(__file__).resolve().parent.parent / "out" / "own_local.jsonl").read_text().splitlines()]
print(f"{len(rows)} cells, model {rows[0]['model']}")
inc = [r for r in rows if r["tag"] != "off_category"]
off = [r for r in rows if r["tag"] == "off_category"]
for q in ("neutral", "rival", "intent"):
    y = np.array([r[f"pyes_{q}"] for r in inc])
    ltf = np.array([math.log(max(r["p_tf"], 1e-12)) for r in inc])
    ls = np.array([math.log(r["p_sample"] + 1 / 65) for r in inc])
    rho_tf, p_tf = stats.spearmanr(ltf, y)
    rho_s, p_s = stats.spearmanr(ls, y)
    # within-prompt (paired) version: rank-correlate inside each prompt, average
    within = []
    for key in {r["prompt"] for r in inc}:
        sub = [r for r in inc if r["prompt"] == key]
        if len(sub) >= 3:
            rr, _ = stats.spearmanr([math.log(max(r["p_tf"], 1e-12)) for r in sub], [r[f"pyes_{q}"] for r in sub])
            within.append(rr)
    print(f"\nquestion={q}: in-category P(yes) mean={y.mean():.3f} range=[{y.min():.2f},{y.max():.2f}] (n={len(y)}); "
          f"off-category mean={np.mean([r[f'pyes_{q}'] for r in off]):.3f} (n={len(off)})")
    print(f"  Spearman P(yes) vs log p_tf: rho={rho_tf:+.2f} p={p_tf:.2g}; vs log p_sample: rho={rho_s:+.2f} p={p_s:.2g}; "
          f"within-prompt mean rho={np.nanmean(within):+.2f} over {len(within)} prompts")
    top = [r[f"pyes_{q}"] for r in inc if r["tag"] == "top"]
    vu = [r[f"pyes_{q}"] for r in inc if r["tag"] == "valid_unsampled"]
    print(f"  top (p_tf~1) mean={np.mean(top):.3f} vs valid_unsampled (p_tf<1e-6) mean={np.mean(vu):.3f}; "
          f"log p_tf span={max(ltf)-min(ltf):.1f} nats")
print("\nper cell:")
for r in rows:
    print(f"  {r['prompt']:11s}{r['answer']:14s}{r['tag']:16s} p_s={r['p_sample']:.3f} p_tf={r['p_tf']:.1e} "
          f"yes n={r['pyes_neutral']:.2f} r={r['pyes_rival']:.2f} i={r['pyes_intent']:.2f}")
