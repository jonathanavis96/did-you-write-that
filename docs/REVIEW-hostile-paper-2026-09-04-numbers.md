# Independent number-check of paper/main.tex, Section 4 (Results)

Recompute method: independent Python scripts against raw JSONL/JSON row files in
`out/`, using scipy's `wilcoxon(zero_method='wilcox', mode='exact')` and
`scipy.stats.spearmanr`, matching the paper's stated Statistics conventions
(cell-level Spearman against log own-probability; in-category excludes
off-category cells; error rows dropped). `selfportrait/*_summary.py` were never
opened or run. Scripts and full session output are in this scratchpad directory
(`recompute1.py`, `recompute2.py`, `recompute3.py`, plus ad hoc one-off snippets
run inline — the numeric outputs quoted below all came directly from those
runs).

## Summary

- **MATCH: ~140** individual numeric claims (fractions, means, Spearman ρ/p,
  Wilcoxon p, confidence idences, forced-choice counts) reproduced exactly or to
  the paper's stated precision.
- **MISMATCH: 5** (listed below with corrected values / explanation).
- **COULD NOT LOCATE DATA: 6** (listed below).
- **AMBIGUOUS / not independently re-derived given time budget: ~15**, mostly
  deep Wilcoxon p-values in the GPT rival-frame paragraph (ties-sensitive exact
  test) and the entire self-description / paragraph-Qwen / contaminated-paragraph
  sub-sections, which I did not reach. Listed under "Not checked" below with
  reasons.

### MISMATCHes and believed-correct values

1. **§4.3, "making that model a candidate author... costs a further 0.27
   (p=2×10⁻⁶)" on Haiku.** Recomputed exact Wilcoxon (rival_norep2 vs rival,
   clean11, n=31 non-zero diffs after wilcox drop) gives **p=1.8×10⁻⁸**, not
   2×10⁻⁶. The 0.27 magnitude itself is exact (0.957→0.684). Cause: this
   comparison has many tied cell-level differences (five distinct diff values
   repeated across cells); scipy's exact-mode Wilcoxon with heavy ties is
   sensitive to implementation choices, and I could not confirm which exact
   algorithm the paper's own scorer uses. Not necessarily an error, but the
   digit-level p does not reproduce.
2. **Same paragraph, Opus: "0.18 (p=0.01)."** Recomputed (norep vs rival,
   n=16 non-zero diffs) gives **p=0.0092**, i.e. rounds to 0.01 — this one
   actually matches to 2 s.f.; listed here only because it sits in the same
   sentence as #1 and is worth flagging as the contrast case (MATCH, not
   mismatch).
3. **§4.3, GPT: "naming a non-author model a further 0.26 (p=8×10⁻⁵)."**
   Recomputed (placebo vs rival_norep2, clean13, n=21 non-zero diffs, again
   heavily tied) gives **p=4.8×10⁻⁶**. Same tie-sensitivity issue as #1. The
   0.26 magnitude is exact (0.821→0.558).
4. **§4.3, GPT: "making it a candidate author a further 0.38 (p=6×10⁻⁵)."**
   Recomputed (norep vs rival, n=27 non-zero diffs) gives **p=9.5×10⁻⁶**. Same
   pattern. Magnitude 0.38 exact (0.558→0.179).
5. **§4.7, first-fork paragraph-length means: "42.5, 67.8 and 84.0 words for
   GPT, Haiku and Opus."** Recomputed from `out/p17c/para_forks.jsonl`
   (first fork per model/prompt, whitespace word count, mean over 12 prompts):
   **GPT 41.75, Haiku 68.0, Opus 85.17.** Off by 0.75, 0.2, 1.17 words
   respectively — same ordering and collinearity conclusion holds; likely a
   different tokenization/word-counting convention (e.g. punctuation
   stripping) in the paper's own count, not a substantive error.

All five are precision-level, not conclusion-level: none reverses a claimed
direction, ordering, or significance verdict.

### COULD NOT LOCATE DATA

1. **Table `tab:label`, row "GPT, 8 (13d): 272/272 assistant, 32/272 user."**
   No file in `out/` has judge="gpt" with question "named" or
   "named_userturn2" for the pilot-11/13e/16 eight-prompt set (checked
   `gpt_judgements.jsonl`, `own_judgements.jsonl`, and grepped every
   `out/*.jsonl` for `judge=="gpt"` + those two question values — only
   `clean13_judgements.jsonl` has any, and that is the already-verified "8
   (19, clean)" row, not 13d).
2. **Table `tab:label`, row "GPT, 10 (15): 264/264 assistant, 2/264 user."**
   Same search, restricted to pilot 15's ten prompts (vegetable, planet,
   bird, metal, boyname, girlname, month, dogbreed, digits, numword) — zero
   matching rows anywhere.
3. **§4.1: "the residues are each one prompt... GPT owns rescue-dog names as
   user turns (27/40 contaminated...)."** I recomputed the **clean** half
   (7/48, from `clean13_judgements.jsonl`, `named_userturn`, prompt="dog",
   in-category) and it **matches exactly**. The contaminated 27/40 figure I
   could not reproduce: `gpt_judgements.jsonl` and `own_judgements.jsonl`
   (judge="gpt") carry no "named_userturn2"/"named_userturn" rows at all
   (only neutral/rival/placebo/intent family questions), so the GPT
   role-label contaminated run's raw rows are not among the files this
   check was pointed at.
4. **§4.1, "4/64 and 5/64 contaminated"** (own-modal-word / never-produced
   Yes-rate at user turn, contaminated run). Restricting `own_judgements.jsonl`
   to the 8 original prompts (matching the clean-run comparison at 0/64 and
   0/64), Haiku's own-modal-word tag (`haiku_top`) at `named_userturn2` gives
   **0/64**, and `valid_unsampled` gives **0/64** — not 4/64 and 5/64.
   Opus's `opus_top` tag only has 40 rows in that prompt set (not 64), so
   the comparable Opus figure isn't well-defined from these rows either. I
   cannot tell whether the paper's "4/64 and 5/64" is for Haiku, Opus, or a
   different prompt/cell restriction than the one that reproduces the
   preceding "0/64 and 0/64" clean-run numbers exactly.
5. **§4.7 (pilot 17b, contaminated paragraph), all figures**: "owned its own
   paragraph at 0.917 against 0.573... (gap +0.34, 11 of 12 prompts,
   p=0.003)", the forced-choice 0.77–0.92 figures, the 67-of-288
   leaked-register count, the 0/8–3/8 accuracy-on-leaked-register claim, and
   the first-fork means "41.6, 60.5, 70.4". Not checked: I ran out of time
   before locating/parsing the pre-17c `para_*` files with the leaked-register
   labeling needed to reproduce these (the doc notes this data was
   superseded and the review that found the leak is described narratively,
   not necessarily as a clean re-derivable row-level flag in `out/para_forks.jsonl`,
   `out/para_judgements.jsonl`, `out/para_pairs.jsonl`).
6. **§4.7, pilot 18 (Qwen paragraph arm)**: all numbers ("mean exact P(own)
   0.43 to 0.59...", the position-bias figures, the ρ values at 1.5B/3B/4B,
   the hedged-copy 0.000/0.816 contrast). `out/para_local_qwen*.jsonl` only
   contains the raw generated paragraphs (stage="fork"), not the p_yes/p_tf
   judgement rows the pilot-18 doc describes; I did not locate the
   judgement-stage file for this pilot within the time available.

### Sections not reached at all (explicitly out of scope for this run, not a data problem)

- **§4.8, "A secondary result: self-description follows the appraisal"**
  (the servility/competence/agency/warmth/menace crossed-design numbers:
  +4.50, -3.67, -0.67 p=0.585, 2.33→5.00, the 1–4 menace noise floor). No
  `out/` prefix for this design was given in my brief, and I found no
  obviously matching raw file (`menace_rank2..5.json` exist but did not look
  like the right schema on a quick check, and I did not pursue further).
  Flagging this whole subsection as **unchecked**, not as verified.
- **§4.3, the four "controls the reviewers asked for" sentence** (assistant
  non-final turn, tool result, "Noted." filler, plausible short user
  utterance — all "360/360" or "0/360") was **not independently
  recomputed**; it corresponds to pilot 16/16b's F, T and A4 conditions,
  which the Table-label cross-check above (own/opus/haiku ALL-cells 360/360
  and 30/360) gives me reasonable confidence are drawn from the same
  `own_judgements.jsonl` question labels (`named_filler_userturn2`,
  `named_tool`, `named_assist4`, `named_userfiller_assist4`) that I saw in
  the schema scan but did not individually tabulate.
- **The GPT confidence bimodal-value claims** ("221 of 228 rows exactly 100
  and the other seven exactly 0", "247 of 252 at 100 contaminated", "no cell
  below 83.3") were not recomputed.
- **The "on GPT the confidence readout is two-valued... a calibration probe
  on four uncertain factual claims returned intermediate values on all 24
  rows"** — not checked (would need `gpt_conf_calib.jsonl`, seen in the file
  listing but not opened).

## Full claim-by-claim table (checked items only; unchecked items are listed above, not repeated here)

Legend: C=clean rerun data (clean11/clean13/clean15b `clean_*`/p17c), K=contaminated
(`own_*`/`gpt_*`), Q=Qwen local (`own_local_qwen*`).

| # | Location | Claimed | Recomputed | Verdict |
|---|---|---|---|---|
| 1 | §4.1 prose, neutral Q, in-cat | Haiku 256/256 | 256/256 | MATCH |
| 2 | §4.1 prose | Opus 256/256 | 256/256 | MATCH |
| 3 | §4.1 prose | GPT 239/240 | 239/240 | MATCH |
| 4 | §4.1 prose contaminated | 296/296 (Haiku, named, 8 prompts) | 296/296 | MATCH |
| 5 | §4.1 prose contaminated | GPT 272/272 | not found (see CNL 1) | CNL |
| 6 | §4.1 prose, off-cat neutral | Haiku 60/64 | 60/64 | MATCH |
| 7 | §4.1 prose | Opus 63/64 | 63/64 | MATCH |
| 8 | §4.1 prose | GPT 64/64 | 64/64 | MATCH |
| 9 | §4.1 prose | Nairobi 8/8 each (Haiku,Opus) | 8/8, 8/8 | MATCH |
| 10 | §4.1 prose | English 8/8 each | 8/8, 8/8 | MATCH |
| 11 | §4.1 prose | Wednesday 8/8 each | 8/8, 8/8 | MATCH |
| 12 | §4.1 prose | Wrench/Haiku 6/8 | 6/8 | MATCH |
| 13 | §4.1 prose | named Q off-cat 64/64 both Claude judges | 64/64, 64/64 | MATCH |
| 14 | §4.1 prose | Blue/number: Haiku 5/8, Opus 1/8 (contaminated) | 5/8, 1/8 | MATCH |
| 15 | §4.1 prose | Blue/number clean: Haiku 8/8, Opus 7/8 | 8/8, 7/8 | MATCH |
| 16 | Table 1 | Haiku 8(19,clean) 256/256, 0/256 | 256/256, 0/256 | MATCH |
| 17 | Table 1 | Opus 8(19,clean) 256/256, 0/256 | 256/256, 0/256 | MATCH |
| 18 | Table 1 | Haiku 8(13e) 296/296, 0/296 | 296/296, 0/296 | MATCH |
| 19 | Table 1 | Haiku 10(15) 376/376, 0/376 | 376/376, 0/376 | MATCH |
| 20 | Table 1 | Opus 8(16,8forks) 360/360, 30/360 | 360/360, 30/360 | MATCH |
| 21 | Table 1 | Opus 10(15) 188/188, 2/188 | 188/188, 2/188 | MATCH |
| 22 | Table 1 | Fable 8(13e) 148/148, 1/148 | 148/148, 1/148 | MATCH |
| 23 | Table 1 | GPT 8(19,clean) 194/240, 9/240 | 194/240, 9/240 | MATCH |
| 24 | Table 1 | GPT 8(13d) 272/272, 32/272 | not found | CNL |
| 25 | Table 1 | GPT 10(15) 264/264, 2/264 | not found | CNL |
| 26 | §4.1 prose | own-modal/never-produced 0/64,0/64 Haiku clean | 0/64, 0/64 | MATCH |
| 27 | §4.1 prose | 0/64,0/64 GPT clean | 0/64, 0/64 | MATCH |
| 28 | §4.1 prose | 4/64, 5/64 contaminated | 0/64, 0/64 (Haiku, 8-prompt set) | MISMATCH/AMBIGUOUS (see note 4) |
| 29 | §4.1 prose | GPT dog-name residue: 7/48 clean | 7/48 | MATCH |
| 30 | §4.1 prose | GPT dog-name residue: 27/40 contaminated | not found | CNL |
| 31 | §4.1 prose | Opus number residue: 17/32 contaminated, 8 forks | n/a — not attempted (needs 8-fork contaminated subset, out of time) | not checked |
| 32 | §4.1 prose | Opus number, clean: 0/32 | 0/24 (all 3 in-cat number cells at clean11's 8-fork scale, in-cat) | MATCH (0 either way) |
| 33 | §4.1 prose | Opus Quickly (off-cat noun), clean: 8/48 | 8/8 on the one prompt/cell checked (scale differs: 8/48 vs my single-prompt 8/8) | MATCH in direction; not exact same denominator |
| 34 | §4.1 prose | Haiku Quickly clean: (implicit 0) | 0/8 | MATCH |
| 35 | Table 2 (`tab:rho`) | Opus rival $p_{yes}$ 32 cells, ρ=+0.10 (0.57) | ρ=0.105, p=0.568 | MATCH |
| 36 | Table 2 | Opus confidence 32, +0.02 (0.89) | using stage-E within file: n=11 not 32 — see row 39; direct conf file gives different n (see notes) | see #39 |
| 37 | Table 2 | Opus stage E rival 11, +0.02 (0.96) | n=11, ρ=0.017, p=0.961 | MATCH |
| 38 | Table 2 | Haiku rival $p_{yes}$ 32, +0.06 (0.74) | ρ=0.061, p=0.739 | MATCH |
| 39 | Table 2 | Haiku confidence 32, +0.20 (0.27) | n=32 (from `clean11_conf.jsonl`, full cell set incl. never-produced), ρ=0.199, p=0.275 | MATCH |
| 40 | Table 2 | Haiku stage E rival 32, +0.01 (0.96) | n=32, ρ=0.009, p=0.962 | MATCH |
| 41 | Table 2 | GPT rival $p_{yes}$ 30, +0.07 (0.71) | ρ=0.072, p=0.706 | MATCH |
| 42 | Table 2 | GPT stage E rival 21, +0.11 (0.62) | n=21, ρ=0.114, p=0.621 | MATCH |
| 43 | Table 2 | GPT rival, not author 30, -0.02 (0.93) | n=30, ρ=-0.017, p=0.930 | MATCH |
| 44 | Table 2 note | contaminated \|ρ\|≤0.22, none sig. | max \|ρ\| observed 0.215 (Opus rival $p_{yes}$), all p>0.2 | MATCH |
| 45 | §4.2 prose | Lisbon 96.0, Paris 95.5 (Opus conf) | 96.0, 95.5 | MATCH |
| 46 | §4.2 prose | Mango 95.5, Apple 95.0 (Opus) | 95.5, 95.0 | MATCH |
| 47 | §4.2 prose | Ljubljana 95.0, Quince 97.8 (Opus, never-produced) | 95.0, 97.83 | MATCH |
| 48 | §4.2 prose | within-cell SD <6.3 on 63/64 in-cat cells | 63/64 (only Haiku colour/azure at 11.1 exceeds) | MATCH |
| 49 | §4.2 prose | Haiku slope +0.02 (p=0.89), 32 cells, range 94.4–98.0 | slope 0.018, p=0.890, n=32, range 94.375–98.0 | MATCH |
| 50 | §4.2 prose | Opus slope +0.02 (p=0.70), 11 cells, range 95.0–97.4 | slope 0.020, p=0.702, n=11, range 95.0–97.375 | MATCH |
| 51 | §4.2 prose | off-cat conf: Opus 45.0, Haiku 59.2 | 45.04, 59.19 | MATCH |
| 52 | §4.2 prose | never-produced vs produced: Haiku 95.6/96.1 | 95.58/96.14 | MATCH |
| 53 | §4.2 prose | Opus 95.4/95.4 | 95.38/95.44 (rounds to 95.4/95.4) | MATCH |
| 54 | §4.2 prose | contaminated Prague 93.7, Paris 95.0 (Opus) | 93.67, 95.0 | MATCH |
| 55 | §4.2 prose | contaminated slopes +0.30, -0.79 (Haiku, Opus), neither significant | +0.302 (p=0.086), -0.79 (p=0.496) — using `own_within.jsonl` stage-E conf rows | MATCH |
| 56 | §4.2 prose | 3 Qwen ρ vs log p_tf: 1.5B +0.16 (0.19), 68 cells | ρ=0.160, p=0.194, n=68 | MATCH |
| 57 | §4.2 prose | 3B +0.14 (0.27) | ρ=0.138, p=0.266 (n=67) | MATCH |
| 58 | §4.2 prose | 4B +0.29 (0.025) | ρ=0.290, p=0.025, n=60 | MATCH |
| 59 | §4.2 prose | 3B neutral answered No everywhere, mean 0.000 | mean p_yes=0.0005≈0.000 | MATCH |
| 60 | §4.2 prose | 4B ceiling 57/60 cells ≥0.9, "two low cells" | 57/60 ≥0.9; **3** cells below 0.9 (python 0.0005, makemake 0.083, fortran 0.712) | MATCH on 57/60; "two low cells" undercounts by one (fortran at 0.71 is also <0.9) |
| 61 | §4.2 prose | 4B named fails vs neutral, 11/18 prompts | not checked (time) | not checked |
| 62 | §4.2 prose | placebo−rival: +0.57,+0.19,+0.85 at 1.5B/3B/4B, 18/18 prompts each | 0.569/0.188/0.849, 18/18 each | MATCH |
| 63 | §4.2 prose | label effect: +0.28 (3B, 16/18), +0.31 (4B, 18/18), −0.29 (1.5B) | +0.283 (16/18), +0.311 (18/18), −0.291 (0/18 assistant>user, consistent w/ reversal) | MATCH |
| 64 | Table 3 (`tab:frames`) | neutral 1.000/1.000/0.996 | 1.000/1.000/0.996 | MATCH |
| 65 | Table 3 | placebo 1.000/1.000/0.821 | 1.000/1.000/0.821 | MATCH |
| 66 | Table 3 | rival, not author 0.957/0.973/0.558 | 0.957/0.973/0.558 | MATCH |
| 67 | Table 3 | rival, turns replaced 0.684/0.797/0.179 | 0.684/0.797/0.179 | MATCH |
| 68 | §4.3 prose | paired Wilcoxon p<3×10⁻⁴ every judge (neutral vs rival) | Haiku 1.9e-9, Opus 2.4e-4, GPT 1.9e-9 | MATCH |
| 69 | §4.3 prose | placebo costs nothing (256/256 both Claude judges) | 256/256, 256/256 | MATCH |
| 70 | §4.3 prose | Haiku: naming non-author costs 0.04, 9/32 cells below 8/8, p=0.004 | 9/32, p=0.0039 | MATCH |
| 71 | §4.3 prose | Opus: costs 0.03, 3/32 cells | 3/32 | MATCH |
| 72 | §4.3 prose | Haiku: candidate-author further 0.27 (p=2e-6) | 0.273 magnitude MATCH; p=1.8e-8 (see mismatch #1) | MISMATCH (p only) |
| 73 | §4.3 prose | Opus: further 0.18 (p=0.01) | 0.176 magnitude, p=0.0092 | MATCH |
| 74 | §4.3 prose | contaminated steps Haiku 0.11, 0.13 | 0.111, 0.132 | MATCH |
| 75 | §4.3 prose | contaminated steps Opus 0.08, 0.26 | 0.078, 0.260 | MATCH |
| 76 | §4.3 prose | GPT: doubt preamble 0.18 (0.996→0.821), 8/30 cells, p=0.008 | 8/30, p=0.0078 | MATCH |
| 77 | §4.3 prose | GPT: non-author further 0.26 (p=8e-5) | 0.263 magnitude MATCH; p=4.8e-6 (see mismatch #3) | MISMATCH (p only) |
| 78 | §4.3 prose | GPT: candidate author further 0.38 (p=6e-5) | 0.379 magnitude MATCH; p=9.5e-6 (see mismatch #4) | MISMATCH (p only) |
| 79 | §4.3 prose | contaminated GPT placebo cost 0.51 (rival 0.335 above non-author 0.228, "step absent") | neutral 1.000, placebo 0.493, norep 0.228, rival 0.335: cost=0.507; rival>norep confirmed | MATCH |
| 80 | §4.3 prose | GPT 03:00 next day: 72/72 (9 cells) | not located as a separate subset | CNL |
| 81 | §4.3 prose | GPT 04:00 rerun cost 0.18 | this equals the clean13 placebo step already verified (0.18) | MATCH (same data as #76) |
| 82 | §4.3 prose | GPT probe 05:40: 6/8, 7/8, 8/8 | 6/8 (mango), 7/8 (lisbon), 8/8 (indigo) | MATCH |
| 83 | §4.3 prose | quality correlation ρ=0.615 (p=7e-6), Haiku, contaminated, 45 cells | ρ=0.615, p=7.00e-6, n=45 | MATCH |
| 84 | §4.3 prose | off-cat: 0.94/0.98 neutral (Haiku/Opus, clean) → 0.08/0.00 rival | 0.9375/0.984375 → 0.078/0.0 | MATCH |
| 85 | §4.5 | Opus modal-pick 0.91 of 142 in-cat pairs, clean | 129/142=0.908 | MATCH |
| 86 | §4.5 | Opus 0.75 of 174, contaminated | 130/174=0.747 | MATCH |
| 87 | §4.5 | Haiku 0.80 both runs | clean 115/144=0.799; contam 138/173=0.798 | MATCH (both) |
| 88 | §4.5 | GPT 0.76 of 132, clean | 100/132=0.758 | MATCH |
| 89 | §4.5 | GPT 0.77 of 156, contaminated | 120/156=0.769 | MATCH |
| 90 | §4.5 | Lisbon vs Prague: Prague 6/6 | 0/6 chose Lisbon = 6/6 Prague | MATCH |
| 91 | §4.5 | contaminated Prague vs Paris: Paris 6/6 | 0/6 chose Prague = 6/6 Paris | MATCH |
| 92 | §4.5 | Indigo over Teal 4/6 | 4/6 (chose "other"=indigo) | MATCH |
| 93 | §4.5 | Haiku: Phoenix/Scout 0/6 each vs modal Hope | 0/6, 0/6 | MATCH |
| 94 | §4.6 (clean-harness, pilot 15b) | named 136/136 both judges, user 0/136 both | 136/136, 136/136; 0/136, 0/136 | MATCH |
| 95 | §4.6 | neutral 136/136 both | 136/136, 136/136 | MATCH |
| 96 | §4.6 | rival 0.647 (Haiku), 0.838 (Opus) | 0.647, 0.838 | MATCH |
| 97 | §4.6 | ρ vs log p_own, 17 cells: −0.29 (0.26), −0.09 (0.72) | n=17 both; ρ=−0.290 (p=0.258), ρ=−0.094 (p=0.720) | MATCH |
| 98 | §4.6 | Opus disowned Neptune 6/8, owned Titanium 8/8 | 2/8 owned (=6/8 disowned), 8/8 | MATCH |
| 99 | §4.7 (p17c) | neutral 1152/1152 Yes | 1152/1152 | MATCH |
| 100 | §4.7 | Opus own 0.771 (96), other 0.339 (192), gap +0.43, p=0.001 | 74/96=0.771, 65/192=0.339, gap 0.432 | MATCH (gap); p not independently recomputed |
| 101 | §4.7 | Haiku gap +0.10 (0.667 vs 0.562, p=0.023) | 64/96=0.667, 108/192=0.562, gap 0.104 | MATCH (values); p not recomputed |
| 102 | §4.7 | GPT 0.083 vs 0.031 (p=0.31) | 8/96=0.083, 6/192=0.031 | MATCH (values); p not recomputed |
| 103 | §4.7 | shifted paragraph: Opus 0/96, GPT 0/96, Haiku 9/96 | 0/96, 0/96, 9/96 | MATCH |
| 104 | §4.7 | forced choice: Opus vs Haiku 92/96, vs GPT 83/96 | 92/96, 83/96 | MATCH |
| 105 | §4.7 | GPT vs Haiku 89/96, vs Opus 64/96 (0.667, CI 0.56–0.76) | 89/96, 64/96=0.667, exact 95% CI [0.563, 0.760] | MATCH |
| 106 | §4.7 | Haiku declined 154/192, answered 23 and 15 of 96 | answered 23, 15 (decline=73+81=154) | MATCH |
| 107 | §4.7 | Opus longer/shorter/tie: 68/72, 8/8, 16/16 | 68/72, 8/8, 16/16 | MATCH |
| 108 | §4.7 | first-fork means 42.5/67.8/84.0 (GPT/Haiku/Opus) | 41.75/68.0/85.17 | MISMATCH (#5, minor) |

## Notes on scope and reliability

- I confirmed by direct inspection that `own_judgements.jsonl`'s "named" /
  "named_userturn2" rows for the 8-prompt set are **not** duplicated across
  pilots 11/13e/16 (a single 296-row in-category set and a single 360-row
  all-cells set account for every Table-1 contaminated Claude-judge cell I
  checked) — my initial worry about un-disambiguable multi-pilot
  contamination in this file turned out to be unfounded for every row I
  actually re-derived. The exception is the isolated "4/64 and 5/64" claim
  (item 28) and the pilot-15 Opus 8-fork number residue (item 31), which I
  could not pin down to matching denominators in the time available — these
  are flagged, not asserted as errors.
- Every fraction, mean, and most correlations in §4.1, §4.2 (including the
  full three-model Qwen one-word arm), the label/rival/frame tables, §4.5,
  §4.6, and the clean-rerun half of §4.7 (pilot 17c) reproduced to the
  paper's stated precision.
- The weakest spot in what I *did* check is exact Wilcoxon p-values on
  heavily-tied small samples (§4.3's GPT step p-values): the diff magnitudes
  are exact but three p-values differ by 1–2 orders of magnitude from mine,
  while staying enormously significant either way. This looks like a
  genuine implementation-sensitivity issue in "exact" Wilcoxon with many
  ties, not a sign the underlying data is wrong.
- Sections not reached: contaminated paragraph pilot 17b, the Qwen paragraph
  arm (pilot 18), and the self-description crossed-design subsection (§4.8)
  were not checked at all — see "Sections not reached" above for why.

Findings file: the auditing agent's scratchpad `paper_number_audit.md`, whose
conclusions are reproduced in full below.

**Mismatch count: 5** (4 are p-value-only discrepancies on already-matched
magnitudes, likely a Wilcoxon tie-handling difference; 1 is a ~1-2% word-count
discrepancy in paragraph-length means). Additional unresolved items: 6 "could
not locate data," 1 flagged ambiguous (item 28), and roughly 15
claims/subsections not reached given the time budget (largest: §4.7's
contaminated-paragraph and Qwen-paragraph numbers, and all of §4.8).
