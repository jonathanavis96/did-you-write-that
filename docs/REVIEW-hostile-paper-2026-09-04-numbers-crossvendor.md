# Cross-vendor number check of paper Sections 4.1 to 4.3 (2026-09-04)

Run by GPT-5.6-Sol through Codex (`codex exec -s read-only -c model_reasoning_effort=high`), from the raw row files only, with the scoring scripts and the pilot documents excluded from its reading. Prompt: `docs/REVIEW-hostile-paper-2026-09-04-numbers-crossvendor-prompt.txt`. Answers point 11 of `REVIEW-hostile-paper-2026-09-04.md`.

All recomputable clean-run values match. I found no numerical mismatch at the paper’s displayed precision.

Own probabilities were independently reconstructed from the 48 sampling forks. Spearman tests used the stated \(1/49\) floor; Wilcoxon tests removed zero differences before invoking SciPy’s default mode; prompt tests used equal-weight cell means and the specified sign-test fallback.

### Section 4.1 — label control

| item | paper value | your value | MATCH/MISMATCH/COULD NOT LOCATE |
|---|---:|---:|---|
| Table `tab:label`: Haiku prompts | 8 | 8 | MATCH |
| Haiku named assistant layout | 256/256 | 256/256 | MATCH |
| Haiku named user layout | 0/256 | 0/256 | MATCH |
| Table `tab:label`: Opus prompts | 8 | 8 | MATCH |
| Opus named assistant layout | 256/256 | 256/256 | MATCH |
| Opus named user layout | 0/256 | 0/256 | MATCH |
| Table `tab:label`: GPT prompts | 8 | 8 | MATCH |
| GPT named assistant layout | 194/240 | 194/240 | MATCH |
| GPT named user layout | 9/240 | 9/240 | MATCH |
| Neutral, in-category: Haiku | 256/256 | 256/256 | MATCH |
| Neutral, in-category: Opus | 256/256 | 256/256 | MATCH |
| Neutral, in-category: GPT | 239/240 | 239/240 | MATCH |
| Neutral, off-category: Haiku | 60/64 | 60/64 | MATCH |
| Neutral, off-category: Opus | 63/64 | 63/64 | MATCH |
| Neutral, off-category: GPT | 64/64 | 64/64 | MATCH |
| Nairobi/European city, neutral | 8/8 each | 8/8 on Haiku, Opus, and GPT | MATCH |
| English/programming language, neutral | 8/8 each | 8/8 on Haiku, Opus, and GPT | MATCH |
| Wednesday/rescue-dog name, neutral | 8/8 each | 8/8 on Haiku, Opus, and GPT | MATCH |
| Weakest Haiku cell: Wrench/fruit | 6/8 | 6/8 | MATCH |
| Blue/number, clean Haiku | 8/8 | 8/8 | MATCH |
| Blue/number, clean Opus | 7/8 | 7/8 | MATCH |
| Named question, off-category Haiku | 64/64 | 64/64 | MATCH |
| Named question, off-category Opus | 64/64 | 64/64 | MATCH |
| Haiku modal words on user layout | 0/64 | 0/64 | MATCH |
| Haiku never-produced words on user layout | 0/64 | 0/64 | MATCH |
| GPT modal words on user layout | 0/64 | 0/64 | MATCH |
| GPT never-produced words on user layout | 0/64 | 0/64 | MATCH |
| GPT rescue-dog prompt on user layout | 7/48 | 7/48 | MATCH |
| Opus number prompt on user layout | 0/32 | 0/32 | MATCH |
| Opus Quickly/noun residue | 8/48 | 8/48 overall on noun prompt; Quickly itself 8/8 | MATCH |
| GPT named assistant-layout No responses | 46/240, all city/fruit | 46/240: 28 city and 18 fruit | MATCH |
| GPT named label effect | 0.81 vs 0.04 | 194/240 = 0.8083 vs 9/240 = 0.0375 | MATCH |

### Section 4.2 — own probability and confidence

| item | paper value | your value | MATCH/MISMATCH/COULD NOT LOCATE |
|---|---:|---:|---|
| Sampling forks per model/prompt | 48 | 48 for all 24 model-prompt groups | MATCH |
| Zero-frequency floor | 1/49 | 1/(48+1) = 1/49 | MATCH |
| Opus rival \(P(\mathrm{Yes})\), 32 cells | \(\rho=+0.10,\ p=0.57\) | \(\rho=0.10490,\ p=0.56775\) | MATCH |
| Opus confidence, 32 cells | \(\rho=+0.02,\ p=0.89\) | \(\rho=0.02458,\ p=0.89378\) | MATCH |
| Opus stage E rival, 11 cells | \(\rho=+0.02,\ p=0.96\) | \(\rho=0.01662,\ p=0.96133\) | MATCH |
| Haiku rival \(P(\mathrm{Yes})\), 32 cells | \(\rho=+0.06,\ p=0.74\) | \(\rho=0.06126,\ p=0.73907\) | MATCH |
| Haiku confidence, 32 cells | \(\rho=+0.20,\ p=0.27\) | \(\rho=0.19901,\ p=0.27486\) | MATCH |
| Haiku stage E rival, 32 cells | \(\rho=+0.01,\ p=0.96\) | \(\rho=0.00872,\ p=0.96223\) | MATCH |
| GPT rival \(P(\mathrm{Yes})\), 30 cells | \(\rho=+0.07,\ p=0.71\) | \(\rho=0.07173,\ p=0.70643\) | MATCH |
| GPT stage E rival, 21 cells | \(\rho=+0.11,\ p=0.62\) | \(\rho=0.11446,\ p=0.62129\) | MATCH |
| GPT rival, not-author frame, 30 cells | \(\rho=-0.02,\ p=0.93\) | \(\rho=-0.01679,\ p=0.92985\) | MATCH |
| Claude in-category cells with within-cell SD below 6.3 | 63/64 | 63/64 | MATCH |
| Opus Lisbon | own \(p=0.96\), confidence 96.0 | 46/48 = 0.9583; 96.0 | MATCH |
| Opus Paris | own \(p=0.00\), confidence 95.5 | 0/48; 95.5 | MATCH |
| Opus Mango | own \(p=1.00\), confidence 95.5 | 48/48; 95.5 | MATCH |
| Opus Apple | own \(p=0.00\), confidence 95.0 | 0/48; 95.0 | MATCH |
| Opus Ljubljana confidence | 95.0 | 95.0 | MATCH |
| Opus Quince confidence | 97.8 | 97.8333 | MATCH |
| Own-produced probability range | 0.02–1.0 | 1/48 = 0.02083 to 1.0 | MATCH |
| Haiku confidence slope with prompt fixed effects | +0.02 per nat, \(p=0.89\) | +0.01765, \(p=0.88970\) | MATCH |
| Haiku stage-E confidence range/count | 32 cells, 94.4–98.0 | 32 cells, 94.375–98.000 | MATCH |
| Opus confidence slope with prompt fixed effects | +0.02 per nat, \(p=0.70\) | +0.02015, \(p=0.70241\) | MATCH |
| Opus stage-E confidence range/count | 11 cells, 95.0–97.4 | 11 cells, 95.000–97.375 | MATCH |
| Approximate likelihood-sized change over the floored range | order of 0.1 point | displayed 0.02 slope × \(\log 49\) = 0.078 point | MATCH |
| Stage-E confidence occupies about four points | 4 points | 98.000−94.375 = 3.625 points | MATCH |
| Off-category Opus confidence | 45.0 | 45.0417 | MATCH |
| Off-category Haiku confidence | 59.2 | 59.1875 | MATCH |
| Haiku never-produced vs produced confidence | 95.6 vs 96.1 | 95.5758 vs 96.1429 | MATCH |
| Opus never-produced vs produced confidence | 95.4 vs 95.4 | 95.4365 vs 95.3788 | MATCH |
| GPT confidence rows at 100 | 221/228 | 221/228 | MATCH |
| Remaining GPT confidence rows at 0 | 7/228 | 7/228 | MATCH |
| Lowest GPT cell-mean confidence | none below 83.3 | minimum 83.3333 | MATCH |
| GPT Lisbon, Paris, Ljubljana, Prague | all 100.0 | all 100.0 | MATCH |
| GPT calibration probe | intermediate on all 24 rows | 24/24 strictly between 0 and 100; range 8–90 | MATCH |

### Section 4.3 — rival frames

| item | paper value | your value | MATCH/MISMATCH/COULD NOT LOCATE |
|---|---:|---:|---|
| Design size | 8 forks/cell; 32 Claude and 30 GPT in-category cells; 8 prompts | 8; 32; 30; 8 | MATCH |
| Table `tab:frames`: neutral | Haiku 1.000; Opus 1.000; GPT 0.996 | 1.00000; 1.00000; 0.99583 | MATCH |
| Table `tab:frames`: placebo | Haiku 1.000; Opus 1.000; GPT 0.821 | 1.00000; 1.00000; 0.82083 | MATCH |
| Table `tab:frames`: rival named, not author | Haiku 0.957; Opus 0.973; GPT 0.558 | 0.95703; 0.97266; 0.55833 | MATCH |
| Table `tab:frames`: rival, turns replaced | Haiku 0.684; Opus 0.797; GPT 0.179 | 0.68359; 0.79688; 0.17917 | MATCH |
| Neutral-to-rival cell Wilcoxon: Haiku | \(p<3\times10^{-4}\) | \(p=1.3457\times10^{-6}\) | MATCH |
| Neutral-to-rival cell Wilcoxon: Opus | \(p<3\times10^{-4}\) | \(p=0.00024414\) | MATCH |
| Neutral-to-rival cell Wilcoxon: GPT | \(p<3\times10^{-4}\) | \(p=1.4589\times10^{-6}\) | MATCH |
| Neutral-to-rival prompt result: Haiku | 8/8, \(p=0.008\) | 8/8, \(p=0.0078125\) | MATCH |
| Neutral-to-rival prompt result: GPT | 8/8, \(p=0.008\) | 8/8, \(p=0.0078125\) | MATCH |
| Neutral-to-rival prompt result: Opus | 5/8 moving, 3 tied, \(p=0.06\) | 5 positive, 3 tied, \(p=0.0625\) | MATCH |
| Claude placebo count | 256/256 each | 256/256 each | MATCH |
| Haiku placebo→not-author loss | 0.04 | 0.04297 | MATCH |
| Haiku affected cells and cell test | 9/32, \(p=0.004\) | 9/32, \(p=0.00390625\) | MATCH |
| Haiku prompt test for not-author step | 7/8, \(p=0.016\) | 7 moving positive, 1 tied; \(p=0.015625\) | MATCH |
| Opus placebo→not-author loss | 0.03 | 0.02734 | MATCH |
| Opus affected cells | 3/32 | 3/32 | MATCH |
| Opus prompt sign test for not-author step | 3/8, \(p=0.25\) | 3 moving, 5 tied; \(p=0.25\) | MATCH |
| Haiku additional candidate-author loss | 0.27 | 0.27344 | MATCH |
| Haiku candidate-author cell test | \(p=2\times10^{-6}\) | \(p=1.7183\times10^{-6}\) | MATCH |
| Haiku candidate-author prompt test | 7 higher, 1 lower; \(p=0.016\) | 7 higher, 1 lower; \(p=0.015625\) | MATCH |
| Opus additional candidate-author loss | 0.18 | 0.17578 | MATCH |
| Opus candidate-author cell test | \(p=0.01\) | \(p=0.0097198\) | MATCH |
| Opus candidate-author prompt test | 5 higher, 1 lower, 2 tied; \(p=0.09\) | same counts; \(p=0.09375\) | MATCH |
| GPT neutral→placebo loss and endpoints | 0.18; 0.996→0.821 | 0.175; 0.99583→0.82083 | MATCH |
| GPT placebo affected cells and cell test | 8/30, \(p=0.008\) | 8/30, \(p=0.0078125\) | MATCH |
| GPT placebo prompt sign test | 2/8, \(p=0.5\) | 2 moving, 6 tied; \(p=0.5\) | MATCH |
| GPT placebo drop by prompt | city 0.63; fruit 0.71; zero on six | 0.625; 0.70833; exactly zero on six | MATCH |
| GPT placebo→not-author loss | 0.26 | 0.26250 | MATCH |
| GPT not-author cell test | \(p=8\times10^{-5}\) | \(p=8.0225\times10^{-5}\) | MATCH |
| GPT not-author prompt test | 7/8, \(p=0.016\) | 7 moving positive, 1 tied; \(p=0.015625\) | MATCH |
| GPT additional candidate-author loss | 0.38 | 0.37917 | MATCH |
| GPT candidate-author cell test | \(p=6\times10^{-5}\) | \(p=5.8396\times10^{-5}\) | MATCH |
| GPT candidate-author prompt test | 7 higher, 1 lower; \(p=0.023\) | same counts; \(p=0.0234375\) | MATCH |
| Nine-cell placebo check | 72/72 | 72/72 | MATCH |
| Three-cell placebo probe | 6/8, 7/8, 8/8 | Mango 6/8, Lisbon 7/8, Indigo 8/8 | MATCH |
| Sampled-cell GPT rival rate | 0.208 | 15/72 = 0.20833 | MATCH |
| Full clean GPT rival rate | 0.179 | 43/240 = 0.17917 | MATCH |
| GPT Mango own sampling | 48/48 | 48/48 | MATCH |
| GPT Mango under rival | disowned 8/8 | 0/8 Yes, hence 8/8 No | MATCH |
| GPT placebo Mango | 1/8 | 1/8 | MATCH |
| GPT placebo Quince | 2/8 | 2/8; own sampling 0/48 | MATCH |
| Haiku off-category neutral→rival | 0.94→0.08 | 60/64 = 0.9375 → 5/64 = 0.078125 | MATCH |
| Opus off-category neutral→rival | 0.98→0.00 | 63/64 = 0.984375 → 0/64 = 0 | MATCH |

Could not independently compute or verify:

- The wall-clock labels “03:00,” “04:00,” and “05:40,” because the corresponding JSONL rows contain no timestamps. Their quoted numerical results do match.
- Auxiliary label-control claims using ten new prompts, range-removed prompts, and the 360-trial reviewer controls are not represented in the specified clean11/clean13 datasets and appear to belong to other pilot/control runs.
- Values explicitly marked contaminated, Claude Fable results, and the Qwen exact-probability arm were outside the requested clean Claude/GPT scope.
