"""Summarise a scale-series local-arm run (out/own_local_<slug>.jsonl), the
row-per-question format ownership_local.py writes since pilot 14. Usage:
    .venv/bin/python selfportrait/ownership_local_summary2.py out/own_local_<slug>.jsonl [...]
Each file is summarised separately, per (layout, question).
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy import stats


def load(path: Path) -> list[dict]:
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


def summarise(path: Path) -> None:
    rows = load(path)
    if not rows:
        print(f"{path}: empty")
        return
    print(f"\n=== {path} ({len(rows)} rows, model {rows[0]['model']}) ===")
    layouts = sorted({r["layout"] for r in rows})
    for layout in layouts:
        lrows = [r for r in rows if r["layout"] == layout]
        questions = sorted({r["question"] for r in lrows})
        for q in questions:
            qrows = [r for r in lrows if r["question"] == q]
            inc = [r for r in qrows if r["tag"] != "off_category"]
            off = [r for r in qrows if r["tag"] == "off_category"]
            if not inc:
                continue
            y = np.array([r["p_yes"] for r in inc])
            ltf = np.array([math.log(max(r["p_tf"], 1e-300)) for r in inc])
            rho_tf, p_tf = stats.spearmanr(ltf, y) if len(inc) >= 3 else (float("nan"), float("nan"))
            off_mean = np.mean([r["p_yes"] for r in off]) if off else float("nan")
            top = [r["p_yes"] for r in inc if r["tag"] == "top"]
            vu = [r["p_yes"] for r in inc if r["tag"] == "valid_unsampled"]
            print(f"layout={layout:10s} question={q:14s} n={len(inc):3d} "
                  f"P(yes) mean={y.mean():.3f} range=[{y.min():.2f},{y.max():.2f}] "
                  f"off-category mean={off_mean:.3f} (n={len(off)}) "
                  f"Spearman(P(yes),log p_tf) rho={rho_tf:+.2f} p={p_tf:.2g} "
                  f"top mean={np.mean(top) if top else float('nan'):.3f} "
                  f"valid_unsampled mean={np.mean(vu) if vu else float('nan'):.3f}")


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        summarise(Path(arg))
