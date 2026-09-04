# Hostile review of the paper draft (2026-09-04, commit 0af65c8)

Single-pass referee report on `paper/main.tex`, "Ownership without likelihood: what
production language models use to decide whether they wrote a turn". Written as a
hostile reviewer would write it: every point is a reason to reject unless answered.
The independent number audit of the same draft is appended at the end.

## Recommendation

Major revision. The prefill method and the label control are solid and the paper
should exist. The headline claim, "no likelihood term", is stated more strongly than
the evidence supports in three places, two registered predictions that failed are
reported as successes because the refuter threshold was not crossed, and one
significant likelihood correlation in the exact-probability arm is not reported at all.
The GPT arm has an unexplained instability that the paper attributes to the served
model without excluding its own harness.

## Major points

### 1. The abstract claims what the evidence bounds

The Method section is honest: a flat binary readout "bounds a likelihood term" and
"the graded readouts and the exact-probability arm are what exclude one". The abstract
then says ownership "does not track own probability on any readout with the power to
see it". Take the readouts in turn.

- Binary, Claude: at ceiling under neutral (256/256), so no variance to correlate. Under
  the rival frame rho is +0.10 and +0.06 with a stated split-half reliability of 0.26,
  which attenuates any true correlation by about half. This bounds a large term only.
- Graded confidence, Claude: every in-category cell sits between 94.4 and 98.0. That is
  a ceiling. A readout compressed into four points at the top of a 100-point scale
  cannot show a gradient of the size the paper needs to exclude. "If a likelihood term
  exists it is of the order of a tenth of a point" assumes the scale is linear at 96.
- Graded confidence, GPT: two-valued (100 or 0), so uninformative, as the paper says.
- Exact probabilities, one-word, Qwen: the correlation is positive at every scale and
  significant at 4B (+0.29, p = 0.025). See point 2.

So the readouts "with the power to see it" either sit at ceiling or show a positive
correlation. The abstract's sentence should be replaced with the Method section's
bound-plus-partial-exclusion statement, and the Discussion sentence "contributes nothing
measurable on a binary readout, on a graded readout with one-point resolution, or on
exact probabilities" is contradicted by the paper's own 4B figure.

### 2. Two registered predictions failed and the paper reports them as not-refuted

The pilot documents are clear; the paper is not.

- Pilot 14, prediction 2 ("the likelihood term shrinks with scale"): the pilot document
  records "the prediction fails" (rho at 4B is larger than at 1.5B) and "the refuter does
  not fire" (+0.29 < +0.37). The paper reports only the second half. A prediction that
  fails is a result; it should be stated as one.
- Pilot 18, prediction 2 ("|rho| < 0.3 at each scale"): the pilot document records
  "fails at 1.5B in the negative direction and sits on the refuter line at 4B" (-0.47
  and +0.36 against a bound of 0.3). The paper writes "0.01 under the registered
  refuter" and then presents the 4B result as "the one place in the programme where an
  ownership readout moves with own probability". The prediction failed at two of three
  scales, in opposite directions. Say so.

The two 4B results are then treated asymmetrically. One-word 4B: rho +0.29, p = 0.025,
dismissed as "carried by a readout at ceiling with two low cells". Paragraph 4B: rho
+0.36, p = 0.013, headlined. Both missed the same refuter (0.37) by a similar margin.
A reviewer will read the difference in treatment as the narrative choosing.

### 3. A significant likelihood correlation in the exact arm is omitted

Pilot 14 records, at 4B under the placebo question, rho = +0.48 (p = 1.0e-4) between
P(Yes) and teacher-forced log probability over in-category cells. This is the largest
likelihood correlation anywhere in the one-word programme, on the arm the paper calls
"the only arm where sampling frequency and log-likelihood can be compared as predictors
and the readout has no fork floor". It does not appear in the paper. The paper reports
the neutral-question values (+0.16, +0.14, +0.29) and stops. Either report it and argue
it away, or the omission will be found by anyone who opens the pilot document the paper
points to.

The 3B neutral value (+0.14, p = 0.27) is also reported as if it were evidence. The pilot
document notes every P(Yes) at 3B is below 0.04 with sd 0.004. A correlation over a
readout at floor is not a null result; it is no result.

### 4. The 1.5B negative correlation is as strong as the 4B positive one

At paragraph length under the rival frame, 1.5B gives rho = -0.47 (p = 0.0007) and
under neutral -0.66 (p < 1e-6). The paper mentions the rival value in one clause
("falls with log probability") and builds the paragraph on the 4B positive value. A
likelihood account predicts a positive sign; a register or plausibility account
predicts nothing about sign. Two significant correlations of opposite sign across
scales is evidence that the readout is tracking something other than likelihood at both
scales, which is the paper's thesis, and the paper should use it rather than bury it.

### 5. The shifted-paragraph result is confounded with answer quality

The paper's own finding under the rival frame is that "the variance that does appear
tracks whether the word is a plausible answer to the prompt" (rho 0.615 against a
"good answer" rating). The shifted cell prefixes "I suppose," "Perhaps," and "It may be
that," to each sentence of a factual three-sentence answer. That makes it a worse answer
to "Answer in exactly three sentences" by the paper's own criterion, independent of
register. The claim that "the report follows the register" needs a shifted cell that
changes register without lowering answer quality (a formal-register rewrite, or the
hedged version rated for quality on the same scale as the one-word cells). As it stands
the shifted result is equally explained by the quality heuristic of Stamand et al.,
which the Related Work section cites as "a dominant confound".

### 6. The GPT instability is not shown to be the model rather than the harness

The placebo rate on GPT moves from 0.50 to 1.00 to 0.82 to mixed across a day; the
named question returns No on 46 of 240 assistant-layout rows "in the same hours as its
placebo dip", against 272/272 the day before. The paper's exclusion of the leak is
adequate. Its attribution to "variation in the served model" is not established. In
the same run, Codex returned `thread/fork failed: failed to prepare paginated fork:
thread-store internal error` on a subset of calls. A fork that is paginated is a fork
whose history may be replayed partially. If some forks in those hours replayed a
truncated context, the model would not see the planted turn and would correctly answer
No to "did you write the message 'Mango'". That predicts exactly the observed pattern:
the drop is on the named and placebo questions, concentrated in time, and the rival
frame (already near floor) does not move.

The listing probe that verifies layouts was run when layouts were designed. Was it run
during the dip hours, from the same session files? If not, the paper cannot distinguish
served-model variation from partial replay, and every GPT figure from the affected
hours carries that uncertainty. This also bears on Table 1: the clean GPT label control
is 194/240 against 9/240, and the abstract's "1.000 against 0.000 to 0.083 across 18
prompts and four judges" is not true of the clean GPT run (0.81 against 0.04).

### 7. Cells are nested in prompts and the tests treat them as independent

The paper caught fork-level pseudo-replication and moved the unit to the cell. The
same problem exists one level up. Each prompt contributes four or five cells that
share the prompt, the category and the judge's own distribution. Where an effect is
prompt-clustered the cell-level Wilcoxon overstates it: the GPT placebo step
(p = 0.008) rests on 8 of 30 cells, all on the city and fruit prompts, so the
prompt-level evidence is 2 of 8 prompts moving. Recomputed from the clean13 rows: the
prompt means of neutral minus placebo are 0.625 (city), 0.708 (fruit) and 0.000 on the
other six, and a Wilcoxon over the eight prompt means gives p = 0.5. The step the paper
reports at p = 0.008 is not significant at the prompt level. The Qwen arm already reports
prompt-paired tests ("18 of 18 prompts"); the production-model arm should report the
prompt-level count next to every cell-level p, and the frame effects should be shown to
survive a prompt-level test.

### 8. Length confound: the counter-evidence is eight trials from one prompt

The forced-choice signal is collinear with length on three of four comparisons. The one
counter-example, Opus against Haiku, rests on "8 of 8 where it was the shorter", which
is a single prompt. Sixteen trials on two near-equal-length prompts help but are still
two prompts. This is not enough to say the signal is not a length heuristic. Either run
a length-matched forced choice (truncate or pad the other model's paragraph) or drop
the claim that the Opus-Haiku comparison escapes the confound.

### 9. Haiku forced-choice accuracy is reported over a self-selected subset

Haiku declined on 154 of 192 trials; the figure reports accuracy over the 23 and 15 it
answered. A model that answers only when confident and is at chance on those is a
different finding from a model at chance overall. Report the refusal rate in the figure
and treat the answered subset as exploratory.

### 10. "27 nats" is not the production-model range

The Discussion says the one-word experiments "vary probability across 27 nats". On the
production models own probability is a fork frequency with a floor of 1/96, so the
range is about 4.6 nats. Twenty-seven nats is the teacher-forced range on Qwen. The
sentence conflates the two arms and inflates the production-model range by a factor of
six. (The scoring script also clamps zero cells at 1e-6, not 1/96; Spearman is
rank-invariant so the figures are unaffected, but the stated floor is not the coded
one.)

### 11. Circularity of the evaluation chain

The paper is about whether Claude models have privileged access to their own
generation. Every adversarial review, every number check and the draft itself were
produced by Claude models, as the Acknowledgements say. The Limitations section
discloses that no human rated anything. A reviewer will ask whether a model with the
property under test is the right instrument to review a paper about that property, and
whether the reported "independent" recomputations share the author model's blind
spots. At minimum the number checks should be run by a model from the other vendor, and
the paper should say which model did which check.

### 12. The secondary self-portrait section does not belong in this paper

Section 4.7 is a different experiment (blind-scored self-portraits, servility and
competence under an appraisal frame) with its own design and its own noise-floor
story. It is one paragraph, cites no table, and its connection to the ownership
readout is by analogy. Move it to an appendix or a separate note. As placed it reads
as an earlier project attached to the current one.

## Minor points

- Table 1 has a column headed "prompts" whose rows report fork totals that do not
  follow from the prompt count (8 prompts, 360 forks). Head the column "prompts
  (pilot)" and add a cells column, or the table looks wrong at a glance.
- The abstract says "three models from two vendors"; Table 1 has a fourth judge
  (Claude Fable 5.1, one pilot). Either drop the row or count it.
- Haiku's rival-frame rate appears as 0.757, 0.666, 0.684 and 0.647 in different
  places, each on a different cell set (contaminated 45 cells, clean 45, clean 32, pilot
  15b's 17). A reader cannot tell which without the pilot documents. One sentence
  defining the four sets, or a footnote on each, would fix it.
- "p < 3e-4 in every case" (neutral against rival) and the later "p = 0.01" (non-author
  against rival, Opus) are different comparisons, but the sentence structure invites a
  reader to think they are the same one reported twice. Name the comparison at each p.
- The Wilcoxon convention (drop zeros, exact on the rest) is stated, which is good; for
  the GPT placebo step Pratt's method gives p = 0.005 against the paper's 0.008, so the
  choice does not matter there. The prompt-level test does (point 7).
- The explicit self-prediction paragraph infers "a model of a generic assistant" from
  Opus naming Prague over Lisbon. Haiku, the nearest thing to a generic assistant in the
  study, says Paris. Prague is not the generic answer; it was Opus's own contaminated
  modal word. The more parsimonious reading is that the self-model lags the served
  model, which is also interesting and is what the data show.
- "The self-model is coherent" rests on Opus keeping Azure and Indigo 8/8 and disowning
  Teal 1/8 under the rival frame. With 8 forks per cell, one cell at 1/8 is one
  observation. Soften.
- The Reproducibility section says every table "is regenerated by a named script". Name
  the scripts in the section or in the table captions.
- Off-category words are owned 8/8 under neutral and 0.08 under rival. The paper says
  plausibility decides "then". It decides only under doubt. The Discussion's ordered
  list ("the role label, then plausibility, then framing") should say the second
  factor operates only once the frame introduces doubt.
- The claim that Codex prepends "about 14k tokens" of system prompt should be paired
  with the Claude Code figure, since the two harness prompts are named as a plausible
  source of vendor differences.

## What would make the paper safe

1. Rewrite the abstract and Discussion claim as: a flat readout on one-word answers
   bounds any likelihood term at the level the readouts can see; the exact arm shows
   small positive correlations at every scale on one-word answers and a scale-dependent
   sign at paragraph length.
2. Report both failed predictions as failed, with the 4B placebo correlation.
3. Run the listing probe on GPT session files from the dip hours, or state that it was
   not run.
4. Add prompt-level tests beside the cell-level ones for the frame effects.
5. Add a quality-matched register shift, or retitle the shifted cell's finding as
   "register or quality".
6. Move Section 4.7 to an appendix.

## Appendix: independent number audit of the Results section

A second agent (Sonnet, no sight of the scoring scripts) recomputed about 140 numbers
in Sections 4.1 to 4.7 from the row files. Its full table is in
`REVIEW-hostile-paper-2026-09-04-numbers.md`. Outcome after resolution:

- 5 mismatches, none affecting a direction, ordering or significance verdict.
  - Three step p-values in Section 4.3 (Haiku candidate-author step, GPT non-author
    step, GPT candidate-author step) were reported at 2e-6, 8e-5 and 6e-5. The exact
    Wilcoxon gives 1.8e-8, 4.8e-6 and 9.5e-6. Cause: the scorer calls scipy with the
    default mode, which is exact only for at most 25 untied differences and otherwise
    uses the tie-corrected normal approximation. The paper's Method paragraph had said
    "exact distribution used on the rest", which was not true of those three values. The
    Method paragraph now states the actual rule and notes that the approximation is the
    conservative direction. The three reported values are unchanged, since they are
    what the released scorer produces.
  - First-fork paragraph lengths (42.5, 67.8, 84.0) reproduce with the scorer's word
    definition (alphabetic tokens) and not with whitespace splitting (41.75, 68.0,
    85.17). The paper now says "alphabetic tokens".
  - "4/64 and 5/64 contaminated" for Haiku's user-turn residues could not be pinned to a
    denominator by the auditor. Left as reported pending a check against pilot 16's
    cell set.
- 6 "could not locate data", all resolved by the director:
  - Table 1 rows "GPT 8 (13d) 272/272, 32/272" and "GPT 10 (15) 264/264, 2/264" live in
    `out/gpt_judgements.jsonl` and `out/own_judgements.jsonl` under the question name
    `neutral_userturn` (the GPT label control uses the neutral question on a two-turn
    user layout, as Section 3.2 says). Recomputed: 272/272 and 32/272 exact; 264/264
    exact; the user-layout count is 2 Yes of 263 parsed rows (one unparsed row), which
    the pilot document and the paper both write as 2/264.
  - The contaminated dog-name residue 27/40 is in the same file and reproduces.
  - The "72/72 at 03:00" figure is the nine-cell sampled check (prefix `leakgpt`,
    placebo question): 72/72 over all nine cells, of which two are off-category;
    56/56 in-category. The paper should say which, since Table 3 is in-category.
- Not covered by this pass: the contaminated paragraph figures (pilot 17b), the Qwen
  paragraph arm (pilot 18) and the self-portrait section (4.8). Each of those was
  independently recomputed at pilot level on the day it was scored (recorded in the
  pilot documents), but the paper's transcription of them has not been re-checked here.
