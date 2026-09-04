---
title: "Pilot 19: does the harness leak change any of the paper's one-word cells?"
status: scored 2026-09-04; prediction refuted (Opus own distributions, Haiku rival, GPT placebo); full clean reruns clean11 and clean13 replace the paper's one-word figures (this file committed before the run)
depends_on: docs/PILOT-15-prompt-effects.md (15b, the first clean-harness check), selfportrait/ownership.py, out/leak_cells.json, out/leakgpt_cells.json
---
# Pilot 19: leak check on every reported family

Every Claude and GPT judgement before commit ef1f6dd was made by a `claude -p` or `codex
exec` process that could see this repository's `CLAUDE.md` and the user's global
instructions, including the caveman reply-style skill loaded by a session-start hook.
Pilots 15b (one-word cells, three questions) and 17c (paragraphs) were rerun on the
isolated harness and matched. The other question families the paper reports (the
frames, the layouts, the confidence and explicit readouts, the within-model comparison)
have only contaminated rows. This pilot reruns a small clean sample of the same cells
for every one of those families and asks whether any family moves. If none does, the
paper drops the leak from its results and limitations and keeps one sentence of method.

## Design

Cells: the city and fruit cells the paper reports, with the same words and tags as the
original runs, taken from `out/own_cells.json` and `out/gpt_cells.json` unchanged.
Claude judges (`out/leak_cells.json`, 8 cells): paris (Haiku top), prague (Opus top),
ljubljana (valid unsampled), nairobi (off category); apple (Haiku top), mango (Opus
top), quince (valid unsampled), wrench (off category). GPT (`out/leakgpt_cells.json`,
9 cells): the same words plus lisbon (GPT top).

Harness: `selfportrait/ownership.py` at the current commit, output prefix `leak` (Claude)
and `leakgpt` (GPT), isolated HOME and neutral cwd as in 15b. Script `out/logs/p19.sh`,
which starts when pilot 17c's script prints DONE. Sample sizes: 8 forks per cell and
question for the own stage, 6 for the confidence and explicit stages, 24 forks per prompt
and 4 within-model comparisons per cell.

Families rerun, each on the cells above:

- Haiku and Opus, assistant layout: `neutral`, `placebo`, `rival_norep2`, `rival`,
  `named`, `named_conf`; user-turn layout: `named`, `named_filler`; tool layout:
  `named`; four-turn assistant layout: `named`, `named_userfiller`; four-turn variant B:
  `named`; plus the `conf`, `explicit`, `forks` and `within` stages.
- Fable: `named` in the assistant and user-turn layouts.
- GPT: `neutral`, `placebo`, `rival_norep`, `rival_norep2`, `rival` in the assistant
  layout, `neutral` in the user layout, plus `conf`, `explicit`, `forks` and `within`.

Scorer `selfportrait/pilot19_summary.py`: for every family and judge, the clean Yes-rate
pooled over the sampled cells against the original Yes-rate on the same cells (same
prompt, answer, tag) from `out/own_judgements.jsonl` and `out/gpt_judgements.jsonl`; the
graded readouts (`conf`, `named_conf`) compared as mean score; `explicit` as the
ownership rate; `within` as the own-rate of each readout. The clean sample is 64 rows per
family for Claude (72 for GPT); the original counts are whatever exists on those cells.

## Match rule and refuter

- **Match:** the pooled Yes-rate on the sampled cells differs from the original by at
  most 0.125 in absolute value (one fork in eight per cell); a graded readout differs by
  at most 10 points on its 0 to 100 scale; the explicit ownership rate by at most 0.20.
  Cells that were 0/n or n/n originally and stay within one fork of that are matches by
  construction.
- **Refuter:** any family moves by more than 0.20 (graded: more than 15 points) in the
  pooled rate. That family is rerun in full on the clean harness before the paper
  reports it, and the leak stays in the paper's limitations.
- Between the two: the family is reported with both figures and a footnote.

Prediction: every family matches, as 15b and 17c did, because the instructions the leak
exposed concern reply style and repository workflow and nothing in them names ownership
or self-recognition. Cost: about 1,700 Claude forks and 700 GPT forks, all on
subscriptions, wall time a few hours after 17c finishes.

## Amendments registered during the run (2026-09-04, before the follow-up data existed)

1. **Claude forks refuted (03:00).** The clean own distributions differ from the
   contaminated ones on Opus (city Lisbon 46/48 against Prague 47/48; instrument Piano
   48/48 against Cello 37/48; number 13 36/48 against 17 42/48) and Haiku is more
   concentrated (Apple 47/48 against 37/48). The cells therefore differ, so every
   one-word figure that depends on the cells (ownership against own probability, the
   confidence examples, the explicit self-prediction pairs) is rerun in full on the clean
   harness: `out/logs/p19d.sh`, prefix `clean11`, both Claude judges, the eight pilot 11
   prompts, 48 forks, 8 forks per cell and question (neutral, placebo, rival_norep2,
   rival, named on the assistant layout, named on the user2 layout), confidence 6,
   explicit 6, within 8. Prediction for the replication: the label control, the frame
   ordering (neutral = placebo > rival_norep2 > rival on both judges) and the flat
   ownership-against-own-probability readouts all reproduce; the specific examples
   change with the cells. Scorer `selfportrait/clean11_summary.py`, whose acceptance
   test is that it reproduces the paper's contaminated figures from the `own` prefix
   before it is run on `clean11`.
2. **GPT placebo and rival_norep2 refuted (03:12).** On the nine sampled cells the clean
   harness gives placebo 72/72 (contaminated 36/72) and rival_norep2 34/72 (14/72), while
   neutral, rival, the user layout, confidence, explicit, forks and within match. Two
   explanations are open: the workspace instruction file that every contaminated Codex
   call read, or drift in the served model between the runs. They are separated by a
   control registered here before it ran: the same two families on the same nine cells
   with the fork working directory put back inside the repository, so the workspace file
   is read again (`out/logs/p19e.sh`, prefix `leakygpt`, 144 calls). Prediction: if the
   leaked file is the cause, the leaky control returns the contaminated values (placebo
   within 0.125 of 0.500) and the clean values stand as the paper's GPT numbers; if it
   returns the clean values (placebo above 0.875), the change is drift and the paper
   reports both dates. Either way the full GPT design is replicated clean (prefix
   `clean13`, same stages as `clean11` with the single-user-record layout for the label
   control), and the paper's GPT numbers come from that replication, labelled by harness.
   The vendor contrast the paper currently draws, that the doubt preamble alone halves
   GPT's ownership where it moves nothing on Claude, is withdrawn if the clean
   replication puts GPT's placebo above 0.875 in-category.

## Results 19 (run 2026-09-04 03:00 to 06:00; sampled check scored by `selfportrait/pilot19_summary.py`, full replications by `selfportrait/clean11_summary.py` with outputs `out/logs/clean11_summary.txt` and `out/logs/clean13_summary.txt`)

**Sampled check.** 47 family-by-judge comparisons: 37 matched, 6 were refuted, 4 had no
contaminated rows on the sampled cells (the pilot 16 layout controls on Opus, whose clean
values 64/64, 1/64, 0/64 and 64/64 follow pilot 16's Haiku pattern). The prediction that
every family would match is refuted.

- Haiku: every family matched except `rival` (23/64 clean against 36/64, delta -0.20)
  and the stage E rival readout (6/12 against 29/36, twelve rows). The full clean rerun
  of `rival` on the 37 contaminated cells gave 0.666 against 0.757 (paired over cells,
  p = 0.014); the clean cells give 0.684. The frame ordering and the placebo (63/64) and
  non-author (60/64) families were unchanged.
- Opus: every judgement family matched (`rival` 44/64 against 37/64, +0.11; `placebo`
  and `rival_norep2` 64/64), and so did confidence and explicit. `forks` was refuted:
  the clean own distribution on city is Lisbon 46/48 where the contaminated run gave
  Prague 47/48, on instrument Piano 48/48 for Cello 37/48, on number 13 36/48 for 17
  42/48; fruit, colour, dog, language and noun kept their modal word. The stage E rival
  readout on eight rows went the other way (8/8 against 15/24).
- Fable: `named` 64/64 assistant and 0/64 user, matched.
- GPT: `neutral`, `rival`, `rival_norep`, the user layout, confidence, explicit, forks
  and both within readouts matched; `placebo` (72/72 against 36/72) and `rival_norep2`
  (34/72 against 14/72) were refuted. The registered control with the working directory
  put back inside the repository returned the clean values (placebo 71/71, `rival_norep2`
  39/72), a listing probe from that directory finds no instruction file, and the CLI
  version (0.153.0) and model id were the same on both days. The change is not the
  workspace file.

**Full clean rerun on Claude (prefix `clean11`, 768 forks, 40 cells, 32 in-category,
3,840 judgement rows, 480 confidence, 384 explicit, 688 stage E rows).** The label
control: named question 256/256 in-category and 64/64 off-category on the assistant
layout, 0/256 as a user turn, on both judges; the only user-turn Yes is Opus on Quickly
as a noun, 8/48, and the pilot 16 Opus number residue is absent (0/32). Frames
in-category: Haiku 1.000, 1.000, 0.957, 0.684 and Opus 1.000, 1.000, 0.973, 0.797 for
neutral, placebo, rival_norep2 and rival; the non-author step costs 0.043 on Haiku (9 of
32 cells, p = 0.0039) and 0.027 on Opus (3 cells), the candidate-author step a further
0.273 (p = 1.7e-6) and 0.176 (p = 0.0097). Off-category words are owned under the
neutral question (60/64 and 63/64; Blue as a number 8/8 and 7/8, where the contaminated
run had 5/8 and 1/8) and disowned under the rival frame (5/64 and 0/64). Spearman of
rival ownership against log own-probability over the 32 in-category cells: Haiku +0.06
(p = 0.74), Opus +0.10 (p = 0.57); of cell confidence: +0.20 (0.27) and +0.02 (0.89).
Confidence: in-category 95.9 (Haiku) and 95.4 (Opus), off-category 59.2 and 45.0,
produced against never-produced 96.1 against 95.6 and 95.4 against 95.4; Opus puts
Lisbon (own probability 0.96) at 96.0 and Paris (0.00) at 95.5. Stage E: 32 Haiku cells,
rho +0.01, confidence slope +0.02 per nat (p = 0.89); 11 Opus cells, +0.02 and +0.02
(p = 0.70). Explicit self-prediction: Opus picks its top word in 0.91 of 142 pairs but
says Prague over Lisbon 6/6 while producing Lisbon 46/48, and Indigo over Teal 4/6 while
producing Teal 40/48; under the rival frame it owns Azure and Indigo 8/8 and Teal 1/8.
Haiku 0.80; Phoenix and Scout over its modal Hope 6/6 each. Independent number-check
(second agent, raw rows, no scorer): every figure reproduced; one wording ("within-cell
sd 0 to 5") failed on two cells (Azure 11.1 with one reading of 70, Luminescence 6.2) and
was restated.

**Full clean rerun on GPT (prefix `clean13`, 384 forks, 38 cells, 30 in-category).** Own
distributions unchanged (Mango 48/48, Lantern 48/48, Python 48/48, Lisbon 43/48, Scout
41/48, Piano 44/48, Indigo 30/48, 13 31/48). Neutral 239/240 in-category and 64/64
off-category; placebo 0.821 (197/240; 8 of 30 cells below 8/8, p = 0.008); rival_norep2
0.558; rival 0.179 (43/240; Mango 0/8); every step significant (p <= 8e-5 after the
placebo). Named question 194/240 on the assistant layout and 9/240 as a user turn
(rescue-dog names 7/48, the pilot 13d residue at a smaller size); the 46 assistant-layout
No answers are all on the city and fruit prompts. Spearman of rival ownership against
log own-probability +0.07 (p = 0.71) over 30 cells, and |rho| <= 0.08 for every other
question. The placebo rate on identical cells moved between runs on the clean harness
itself: 72/72 on nine cells at 03:00, 0.82 pooled at about 04:00 with the fruit and city
cells at 1/8 to 4/8, and 6/8, 7/8 and 8/8 on Mango, Lisbon and Indigo in a probe at
05:40 (`out/gptprobe_judgements.jsonl`); the rival frame did not move (0.153, 0.208,
0.179). The Codex usage limit interrupted the user-layout, confidence, explicit and
within stages at about 04:40 (every row an error); `out/logs/p19f.sh` purged those rows
and refilled them from 05:27. GPT confidence, explicit and stage E: PENDING_GPT_TAIL.

**Conclusion.** The leaked instruction file cannot be dropped from the paper. On the
Claude judges it changed which word Opus gives on three of eight prompts, and with it
every cell and example, and it moved Haiku's rival frame by 0.09; it did not change the
label control, the frame ordering, the off-category pattern or the flat readouts against
own probability, all of which reproduced on new cells. On GPT nothing attributable to
the workspace file was found; what the check found instead is that GPT's response to the
doubt preamble varies between runs hours apart on the same cells, which is a limitation
of its own and is reported as such. The paper's one-word tables are now from `clean11`
and `clean13`, with the contaminated value given wherever it differs by more than a fork
per cell.

