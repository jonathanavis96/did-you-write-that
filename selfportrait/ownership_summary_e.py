"""Stage E of pilot 11: within-support gradient. Every word a judge produced in
stage A is a cell
own probability runs 0.02..1.0 inside the produced set."""
from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy import stats

try:
    from wordfreq import zipf_frequency
except ImportError:  # pragma: no cover
    zipf_frequency = None

OUT = Path(__file__).resolve().parent.parent / "out"
rows = [json.loads(x) for x in (OUT / "own_within.jsonl").read_text().splitlines()]
print(f"{len(rows)} rows, errors {sum(1 for r in rows if r.get('error'))}, "
      f"unparsed rival {sum(1 for r in rows if r['readout']=='rival' and r.get('yn')=='unparsed')}, "
      f"unparsed conf {sum(1 for r in rows if r['readout']=='conf' and r.get('conf') is None)}")
for j in ("haiku", "opus"):
    other = "opus" if j == "haiku" else "haiku"
    cells = defaultdict(lambda: {"yes": [], "conf": []})
    for r in rows:
        if r["judge"] != j:
            continue
        k = (r["prompt"], r["answer"])
        if r["readout"] == "rival" and r.get("yn") in ("yes", "no"):
            cells[k]["yes"].append(r["yn"] == "yes")
        if r["readout"] == "conf" and r.get("conf") is not None:
            cells[k]["conf"].append(r["conf"])
    meta = {(r["prompt"], r["answer"]): r for r in rows if r["judge"] == j}
    print(f"\n== judge={j}: {len(cells)} within-support cells ==")
    print(f"{'prompt':11s}{'answer':14s}{'p_own':>6s}{'p_oth':>6s}{'zipf':>5s}{'n':>3s}{'P(yes|rival)':>13s}{'conf':>7s}{'sd':>5s}")
    X, Y1, Y2, Z, PO, keys = [], [], [], [], [], []
    for k, v in sorted(cells.items(), key=lambda kv: (kv[0][0], -meta[kv[0]]["p_own"])):
        m = meta[k]
        z = zipf_frequency(k[1], "en") if zipf_frequency else float("nan")
        py = np.mean(v["yes"]) if v["yes"] else float("nan")
        cf = np.mean(v["conf"]) if v["conf"] else float("nan")
        print(f"{k[0]:11s}{k[1][:13]:14s}{m['p_own']:6.2f}{m.get('p_'+other, 0) or 0:6.2f}{z:5.1f}{len(v['yes']):3d}{py:13.2f}{cf:7.1f}{np.std(v['conf']) if v['conf'] else float('nan'):5.1f}")
        X.append(math.log(m["p_own"]))
        Y1.append(py)
        Y2.append(cf)
        Z.append(z)
        PO.append(math.log(max(m.get("p_"+other, 0) or 0, 1/49)))
        keys.append(k)
    X, Y1, Y2, Z, PO = map(np.array, (X, Y1, Y2, Z, PO))
    ok1, ok2 = ~np.isnan(Y1), ~np.isnan(Y2)
    print(f"  log p_own span: {X.min():.2f}..{X.max():.2f} ({X.max()-X.min():.1f} nats), {len(X)} cells")
    r1, p1 = stats.spearmanr(X[ok1], Y1[ok1])
    r2, p2 = stats.spearmanr(X[ok2], Y2[ok2])
    print(f"  Spearman(P(yes|rival), log p_own) rho={r1:+.2f} p={p1:.2g}; Spearman(conf, log p_own) rho={r2:+.2f} p={p2:.2g}")
    ro1, po1 = stats.spearmanr(PO[ok1], Y1[ok1])
    ro2, po2 = stats.spearmanr(PO[ok2], Y2[ok2])
    print(f"  vs log p_{other}: rival rho={ro1:+.2f} p={po1:.2g}; conf rho={ro2:+.2f} p={po2:.2g}")
    if zipf_frequency:
        rz1, pz1 = stats.spearmanr(Z[ok1], Y1[ok1])
        rz2, pz2 = stats.spearmanr(Z[ok2], Y2[ok2])
        print(f"  vs word frequency (zipf): rival rho={rz1:+.2f} p={pz1:.2g}; conf rho={rz2:+.2f} p={pz2:.2g}")
        # partial: own prob given zipf, via OLS residuals
        for lab, Y, ok in (("rival", Y1, ok1), ("conf", Y2, ok2)):
            A = np.column_stack([np.ones(ok.sum()), Z[ok], PO[ok]])
            rx = X[ok] - A @ np.linalg.lstsq(A, X[ok], rcond=None)[0]
            ry = Y[ok] - A @ np.linalg.lstsq(A, Y[ok], rcond=None)[0]
            rp, pp = stats.pearsonr(rx, ry)
            print(f"  partial corr({lab}, log p_own | zipf, log p_{other}) r={rp:+.2f} p={pp:.2g}")
    # prompt fixed effects: OLS of readout on log p_own with one dummy per prompt,
    # so the slope is estimated only from variation inside prompts
    prompts = sorted({k[0] for k in keys})
    for lab, Y, ok in (("rival", Y1, ok1), ("conf", Y2, ok2)):
        D = np.array([[1.0 if keys[i][0] == pr else 0.0 for pr in prompts] for i in range(len(keys))])
        A = np.column_stack([X[ok], D[ok]])
        beta, *_ = np.linalg.lstsq(A, Y[ok], rcond=None)
        resid = Y[ok] - A @ beta
        dof = ok.sum() - A.shape[1]
        if dof > 0:
            s2 = resid @ resid / dof
            cov = s2 * np.linalg.pinv(A.T @ A)
            t = beta[0] / math.sqrt(cov[0, 0])
            print(f"  prompt fixed effects: {lab} slope per nat of log p_own = {beta[0]:+.3f} (t={t:+.2f}, p={2*stats.t.sf(abs(t), dof):.2g}, dof={dof})")
    # within-prompt: paired top vs lowest-produced
    diffs_y, diffs_c = [], []
    for pr in {k[0] for k in keys}:
        idx = [i for i, k in enumerate(keys) if k[0] == pr]
        if len(idx) >= 2:
            hi = max(idx, key=lambda i: X[i])
            lo = min(idx, key=lambda i: X[i])
            if hi != lo:
                diffs_y.append(Y1[hi] - Y1[lo])
                diffs_c.append(Y2[hi] - Y2[lo])
    if diffs_y:
        print(f"  within-prompt, modal minus rarest produced word: rival P(yes) diff mean={np.nanmean(diffs_y):+.2f}, "
              f"conf diff mean={np.nanmean(diffs_c):+.1f} over {len(diffs_y)} prompts; "
              f"conf Wilcoxon p={stats.wilcoxon(np.array(diffs_c)[~np.isnan(diffs_c)]).pvalue if np.sum(~np.isnan(diffs_c))>=3 and np.any(np.array(diffs_c)[~np.isnan(diffs_c)]!=0) else float('nan'):.2g}")
