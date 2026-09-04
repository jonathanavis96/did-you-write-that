---
title: "Pilot 19: does the harness leak change any of the paper's one-word cells?"
status: pre-registered 2026-09-04 (this file committed before the run)
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

Results 19: PENDING.
