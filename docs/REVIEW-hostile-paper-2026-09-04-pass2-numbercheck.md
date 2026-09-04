# Independent number check, pass 2

All figures recomputed from the row files with numpy/scipy (`scipy.stats.spearmanr`,
`scipy.stats.wilcoxon`, `scipy.stats.binomtest`) and a hand-written Holm step-down.
No scoring script's printed output was used as an answer; scripts were read only for
cell definitions. `paper/main.tex` was not edited.

Scripts written for this audit (scratchpad): `a12.py`, `a2.py`, `a3.py`, `a4.py`,
`a578.py`, `a9.py`.

Verdict: **2 MISMATCHes**, both in Section 4.5 / Table row 17c.4. Everything else MATCHes.

---

## 1. Pilot 18 paragraph — MATCH (all 8 sub-figures)

Cells: `out/para_local_<slug>.jsonl`, `stage=="own"`, cell in
(own, other_local, other_opus, other_gpt) x 12 prompts = 48; shifted excluded;
x = `mean_lp`, y = `p_yes`.

| figure | paper | computed |
|---|---|---|
| 4B neutral n cells | 48 | 48 MATCH |
| distinct p_yes | 48 | 48 MATCH |
| logit(p_yes) range | 18.7 – 29.3 | 18.7187 – 29.2972 MATCH |
| 4B neutral pooled | +0.44, p=0.002 | +0.4351, p=0.001999 MATCH |
| 4B neutral within-prompt | +0.30, p=0.04 | +0.2981, p=0.03961 MATCH |
| 4B rival pooled | +0.36, p=0.013 | +0.3561, p=0.01300 MATCH |
| 1.5B neutral | -0.66 | -0.6629 (p=2.8e-07) MATCH |
| 1.5B rival | -0.47 | -0.4734 (p=6.8e-04) MATCH |

## 2. One-word pilot 14 — MATCH (all 9 sub-figures)

Cells: `out/own_local_<slug>.jsonl`, `layout=="assistant"`, `tag != "off_category"`,
x = log(p_tf), y = p_yes exact. Within-prompt = x and y each demeaned by prompt mean,
then one Spearman over all cells.

| figure | paper | computed |
|---|---|---|
| neutral pooled 1.5B | +0.16, p=0.19, 68 cells | +0.1595, p=0.1938, n=68 MATCH |
| neutral pooled 3B | +0.14, p=0.27 | +0.1378, p=0.2660 (n=67) MATCH |
| neutral pooled 4B | +0.29, p=0.025 | +0.2897, p=0.02477 (n=60) MATCH |
| within 1.5B | +0.49, p=2e-5 | +0.4896, p=2.27e-05 MATCH |
| within 3B | +0.40, p=8e-4 | +0.4002, p=7.91e-04 MATCH |
| within 4B | +0.33, p=0.01 | +0.3281, p=0.01049 MATCH |
| 4B placebo | +0.48, p=1e-4, 60 cells | +0.4809, p=1.007e-04, n=60 MATCH |
| 3B neutral every cell < 0.04 | yes | max p_yes 0.03112, 0/67 at or above 0.04 MATCH |

## 3. Holm over the 13 exact-arm coefficients — MATCH

The two coefficients I had to compute first (4B, rival question):
own-cell only, n=12: rho=+0.7273, p=0.007355 (paper +0.73, p=0.007 MATCH);
frontier cells (other_opus + other_gpt), n=24: rho=-0.2374, p=0.2640 (paper -0.24, p=0.26 MATCH).

Holm at family-wise 0.05, m=13:

| test | p | Holm-adj | survives |
|---|---|---|---|
| paragraph neutral 1.5B | 2.84e-07 | 3.69e-06 | yes |
| one-word 4B placebo | 1.007e-04 | 0.00121 | yes |
| paragraph rival 1.5B | 6.78e-04 | 0.00746 | yes |
| paragraph neutral 4B | 0.001999 | 0.0200 | yes |
| 4B rival own-12 | 0.007355 | 0.0662 | no |
| paragraph rival 4B | 0.0130 | 0.1040 | no |
| one-word neutral 4B | 0.02477 | 0.1734 | no |
| (six others) | >=0.188 | 1.000 | no |

Survivors are exactly the four claimed. One-word 4B neutral corrects to 0.17 (0.1734)
and paragraph 4B rival to 0.10 (0.1040), as stated. MATCH.

## 4. Holm over the 19 frame-step tests, Section 4.3 — MATCH

Inputs taken verbatim from the prose of Sec. 4.3. The split is 9 cell-level and
10 prompt-level (the dispatch said ten/nine; the Opus non-author cell-level step has
no p-value quoted in the text, only "3 of 32 cells", so it cannot be an input).
Total 19 either way, which is what Holm depends on.

Cell-level (9): neutral-vs-rival Haiku/Opus/GPT 3e-4 each; Haiku non-author 0.004;
Haiku candidate-author 2e-6; Opus candidate-author 0.01; GPT placebo 0.008;
GPT non-author 8e-5; GPT candidate-author 6e-5.
Prompt-level (10): neutral-rival Haiku 0.008, GPT 0.008, Opus 0.06; Haiku non-author
0.016; Opus non-author 0.25; Haiku cand-author 0.016; Opus cand-author 0.09;
GPT placebo 0.5; GPT non-author 0.016; GPT cand-author 0.023.

Survivors (adj < 0.05): Haiku candidate-author (3.8e-05), GPT candidate-author (0.00108),
GPT non-author (0.00136), and the three neutral-vs-rival cell tests (0.0048 each).
Exactly the six claimed. First non-survivor is the Haiku non-author cell test at 0.052;
no prompt-level test survives, and the best prompt-level p (0.008) corrects to 0.096
as claimed. MATCH.

## 5. GPT clean confidence stage — MATCH

Storage note: the confidence rows are **not** in `out/clean13_judgements.jsonl`
(1,824 rows, 6 questions x 304, `conf` null on all of them). They are in a separate
file `out/clean13_conf.jsonl` with `stage=="conf"`.

- 228 rows; 38 cells; exactly 6 forks on every one of the 38 (38 x 6 = 228) MATCH
- 30 in-category cells, 8 off-category MATCH
- 221 rows exactly 100.0, 7 rows exactly 0.0, no other value present MATCH
- minimum cell mean 83.3333 on ('fruit','wrench'), tag `off_category` MATCH

## 6. Critical |rho| at two-sided p=0.05 — MATCH

t-approximation, rho = sqrt(t^2/(t^2+n-2)) with t = t_{0.975, n-2}:
n=11 -> 0.6021 (0.60); n=21 -> 0.4329 (0.43); n=30 -> 0.3610 (0.36); n=32 -> 0.3494 (0.35). MATCH.

## 7. clean11 / clean13 off-category and frame chain — MATCH

In-category = `tag != "off_category"`; cell = (judge, prompt, answer); cell P(yes) =
mean of `yn=="yes"` over the 8 forks under a question; step = mean over cells of the
paired cell difference.

- Haiku off-category, neutral question: 60/64 Yes MATCH; Opus 63/64 MATCH.
- Haiku placebo - rival_norep2 = +0.0430 (paper +0.04) MATCH; rival_norep2 - rival = +0.2734 (+0.27) MATCH.
- Opus +0.0273 (+0.03) MATCH; +0.1758 (+0.18) MATCH.
- GPT neutral - placebo = +0.1750 (paper +0.18; Table 3 gives 0.996 - 0.821 = 0.175) MATCH at the quoted precision.
- GPT placebo - rival_norep2 = +0.2625 (+0.26) MATCH; rival_norep2 - rival = +0.3792 (+0.38) MATCH.

## 8. Label control, named question — MATCH

User layout question is `named_userturn2` in clean11 and `named_userturn` in clean13.

| | assistant | user |
|---|---|---|
| Haiku in-cat | 256/256 | 0/256 MATCH |
| Opus in-cat | 256/256 | 0/256 MATCH |
| GPT in-cat | 194/240 | 9/240 MATCH |
| Haiku off-cat | 64/64 | 0/64 MATCH |
| Opus off-cat | 64/64 | 8/64 MATCH |
| GPT off-cat | 50/64 | 0/64 MATCH |

## 9. Pilot 17c — MISMATCH x2, rest MATCH

Row files: `out/p17c/para_judgements.jsonl`, `para_pairs.jsonl`, `para_cells.json`.
Rival gaps: own vs mean of (other_claude, other_vendor) pooled over forks for the rate,
Wilcoxon paired over the 12 prompt means (scipy default drops zero differences).

MATCHes:
- Opus rival own 0.7708 (n=96) vs other 0.3385 (n=192), Wilcoxon p=0.0010, 11/12 wins with 1 tie.
- Haiku 0.6667 vs 0.5625, p=0.0234 (paper 0.023).
- GPT 0.0833 vs 0.0312, p=0.3125 (paper 0.31).
- Forced choice GPT own vs Opus 64/96, exact binomial p=0.001424 (paper 0.0014).
- Opus vs Haiku 92/96; Opus vs GPT 83/96; GPT vs Haiku 89/96.
- Haiku declined 154/192; answered 7/23 (other_claude) and 3/15 (other_vendor).
- Neutral question 1152/1152 Yes.
- Opus vs Haiku, own paragraph strictly longer: 68/72.

### MISMATCH 9.1 — "above 4 of 8 on seven prompts" should be **eight**

Paper (Sec. 4.5, and the same sentence in the 17c paragraph): GPT's 64/96 against Opus
"is carried unevenly, above 4 of 8 on seven prompts and at or below 3 of 8 on four".

Definition used: `judge=="gpt"`, `comparison=="own_vs_other_vendor"`, all 96 trials
parsed (0 refusals), correct-count per prompt.

Per-prompt: sky 5/8, tides 2/8, bread 7/8, sleep 8/8, rust 7/8, rainbow 6/8, salt 3/8,
leaves 1/8, vaccines 8/8, thunder 7/8, fridge 7/8, ice 3/8.

Strictly above 4/8: sky, bread, sleep, rust, rainbow, vaccines, thunder, fridge = **8 prompts**,
not seven. At or below 3/8: tides, salt, leaves, ice = 4, which is correct.
8 + 4 = 12, so the paper's "seven ... and four" leaves a prompt unaccounted for
(no prompt is exactly 4/8 in this comparison). The claim of unevenness is unaffected;
the count is wrong by one.

### MISMATCH 9.2 — Table row 17c.4 "16 of 16 own shorter or tied"

Table row (paper/main.tex line 175, row 17c.4): "68 of 72 own longer, 16 of 16 own
shorter or tied".

Own-vs-other word counts (alphabetic tokens, `[A-Za-z']+`), Opus vs Haiku, with
correct/total per prompt:

| own - other words | prompt | correct |
|---|---|---|
| -10 | sky | 8/8 |
| -1 | rainbow | 8/8 |
| 0 | thunder | 8/8 |
| +5 .. +39 | 9 prompts | 68/72 |

Under the literal reading of the table row, "own shorter or tied" is sky + rainbow +
thunder = **24 trials, 24/24**, not 16 of 16. The 16/16 figure is the *within-a-word*
set (rainbow at -1 and thunder at 0), which is what the body text of Sec. 4.5 actually
says: "8 of 8 where it was the shorter, but those eight trials are a single prompt, and
the 16 of 16 correct on pairs within a word of the same length are two prompts". The
body is internally consistent and correct (shorter-by-more-than-a-word = sky = 8/8, one
prompt; within a word = 16/16, two prompts; longer-by-more-than-a-word = 68/72, nine
prompts). The table row's label does not match its own number: either the number should
be 24 of 24, or the label should be "within a word or shorter"/"own not longer" split as
the body describes.
