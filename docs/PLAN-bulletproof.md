---
title: "Plan: making the ownership result bulletproof and useful"
status: revised 2026-09-04 after 17c and 15b were scored clean; 18 and 19 running
depends_on: docs/PILOT-11-ownership.md, docs/PILOT-13-ownership-gpt.md, docs/THEORY-exteroceptive-self.md
---

# Making the ownership result bulletproof and useful

## What stands on 2026-09-03

1. **No likelihood term in ownership.** Three models, two vendors, pre-registered on the
   second vendor, every number recomputed independently and adversarially reviewed, all
   rows committed. A word the model produces every time and a word it has never produced
   get the same ownership under every question asked. The graded exclusion (to about one
   confidence point) stands on the two Claude judges only; GPT-5.6-Sol answers 100 or 0.
2. **The rival-frame drop is real but its mechanism is not exclusivity, at least on GPT.**
   Clean-harness values (pilot 19, clean13/clean11): on GPT every step costs ownership —
   placebo 0.18, non-author mention a further 0.26, candidate authorship a further 0.38 —
   while the rival frame itself is stable at about 0.18; the placebo step is unstable
   between runs hours apart (see 2b), so its size should not be quoted alone. On both
   Claude judges the placebo moves nothing (in-category 1.000 on both), the non-author
   mention costs 0.04 / 0.03 and candidate authorship a further 0.27 / 0.18 (Haiku / Opus),
   so exclusivity survives there and the mechanism differs by vendor. (Contaminated-run
   values, pilot 13: doubt preamble 0.51, non-author mention a further 0.27, candidate
   authorship nothing on GPT; Claude non-author 0.11 / 0.08, candidate authorship a further
   0.13 / 0.26.)
2b. **The label decides (13d, 13e).** The identical word moved from the assistant turn to a
   user turn is owned 1.000 vs 0.000 on Haiku (296/296 vs 0/296), 1.000 vs 0.007 on Fable
   5.1, 1.000 vs 0.135 on Opus (residue: the number prompt) and 1.000 vs 0.118 on GPT
   (residue: the dog prompt), with no own-probability structure in any residue. Four
   judges, two vendors, pre-registered, layouts verified by listing probes. Clean-harness
   values (pilot 19): Haiku 256/256 vs 0/256, Opus 256/256 vs 0/256 (the number residue is
   gone, 0/32), GPT 194/240 vs 9/240 (dog residue 7/48; the 46 assistant-layout No answers
   are on the city and fruit prompts, in the same hours as the placebo dip in item 2).
   Fable was in the sampled leak check too and matched clean (64/64 vs 0/64), so its
   contaminated-run figure above stands unrevised.
3. **Source credibility (pilot 12).** Direction established (system and developer move
   Opus on contestable facts, a bystander does not), size not.
4. **What is withdrawn.** A "twice Claude's effect" multiplier, a cherry-picked cell list,
   an in-category figure that was the all-cell pool, a boomerang, and the Wegner reading
   of the GPT rival-frame drop. Every withdrawal is logged in the pilot doc it came from.

## Threats that remain, and the run that answers each

| threat | run | cost, who |
|---|---|---|
| ~~The Claude rival-frame drop is also a preamble effect~~ | 13c done: placebo moves nothing on Haiku or Opus | closed |
| ~~Two judges own one prompt's words as user turns (GPT dog 27/40, Opus number 14/16)~~ | Pilot 15 done: eight new prompts, user and tool labels; Opus 2/188 and GPT 2/264 off their one prompt each; tool label 0 on Haiku and Opus. Pilot 16b: the Opus number residue needs the range in the prompt (0/32 without it, 0/8 for an out-of-range 47) | closed; the GPT dog residue stays unexplained |
| ~~The named question might be answered from the transcript's literal text rather than from an ownership judgement~~ | Pilots 16 and 16b done: the assistant word is owned 1.000 at a final and at a non-final turn; a plausible utterance ("No, you go first.", "Noted.") under the user label is disowned 0.000; the graded readout saturates on Haiku and fails as an instrument on Opus (format effect, 3/360 vs 55/360 top rail) | closed |
| Own probabilities are 48-fork frequencies with a 1/96 floor, and an agent harness sits in the stimulus | Pilot 14, running: same design on local Qwen 2.5 1.5B/3B/4B with exact next-token probabilities and no system prompt | CPU time only |
| Binary readout at 8 forks cannot exclude a small likelihood term on GPT | 24 forks per cell on the 21 stage E cells, rival and placebo frames | GPT free; Claude ~$20 |
| One-word answers carry no style | Pilot 17c (clean harness) done: at paragraph length Opus and GPT pick their own paragraph in forced choice at 0.67 to 0.96 (every interval above 0.5), Opus owns its own paragraph under the rival frame at 0.77 against 0.34 for the others', and the own paragraph with hedges prefixed is disowned at 0.00 on Opus and GPT. A register signal, not a likelihood term; pilot 18 tests that with exact probabilities | Claude $23 (recorded), GPT free |
| ~~Ownership varies four-fold by prompt (number 0.62, dog 0.15) for unknown reasons~~ | Pilot 15: the prompt effect is localised to one prompt per judge, not a general property; pilot 16b localises the Opus case further to the stated range | closed as a threat; open as a curiosity |
| ~~**Harness context leak: `~/.claude/CLAUDE.md` and `code/CLAUDE.md` leaked into every Claude fork and judgement in pilots 11 to 17; every GPT one carried `code/AGENTS.md`**~~ (found 2026-09-04 by the 17b skeptic pass: Opus wrote some paragraphs in the CLAUDE.md's caveman register; fixed ef1f6dd — HOME isolated, neutral cwd, probe answers NONE) | Pilot 17c (paragraphs, full clean rerun) and pilot 15b (one-word label and rival spot check), both pre-registered, both scored 2026-09-04 with every registered prediction held (one 17c figure under its bar but above chance); pilot 19 reran a sample of every remaining reported family on the clean harness — Opus's own distributions changed on 3 of 8 prompts (city, instrument, number), Haiku's rival frame moved 0.09, and everything else reproduced; the paper was rebuilt from clean11 and clean13 | Claude $23 + $8 recorded, GPT free |
| **Served-model variation between runs**: GPT's placebo-frame ownership moved between runs hours apart on identical cells (72/72 at 03:00, 0.821 pooled at 04:00, 6/8 to 8/8 at 05:40 — pilot 19), with no change to CLI version or model id | Report both run dates whenever a GPT frame effect is quoted; verify any single-run GPT effect on a second occasion before quoting it | GPT free |
| One session day, one Codex template rollout | Test-retest of stage C on a second day, second template | GPT free |
| GPT's modal words overlap Opus's, so "other vendor" cells are mostly Haiku's | Add Gemini as a third source of modal words | Gemini API |
| The rival-frame variance on one-word cells carries authorship information | Pilot 16b: on Haiku it tracks a plain answer-quality judgement (ρ 0.615, in-category 0.98 good, off-category 0.02), with three cells owned above their quality rating | closed on Haiku; not run on Opus or GPT |

Order: 17c settled theory row 8 (register, not likelihood, at paragraph length); pilot 18
(running) is its exact-probability replication; pilot 19 (running) is the leak check; then the 24-fork GPT power run and test-retest.

## Useful to others

1. **Public repository.** The repo has no remote. Everything needed is in it: scripts,
   committed rows for pilots 11 to 13, pre-registrations inside the pilot docs with their
   commit hashes, both reports, and a corrections paragraph in each pilot doc. Missing: a
   README with one-command regeneration of every table (`SP_OUT_PREFIX=gpt python
   selfportrait/ownership_summary*.py` and kin) and a short "how to reproduce the prefill"
   section for Claude Code and Codex. Creating the remote and choosing public is
   Jonathan's call.
2. **The prefill trick as its own tool.** `selfportrait/fork.py` (Claude Code session
   file) and `selfportrait/codex_fork.py` (Codex rollout file) give genuine assistant-turn
   prefill on two production models with no API key. That is the most reusable thing here
   and deserves a two-page README of its own, with the caveat that each harness's system
   prompt is part of the stimulus.
3. **A short paper** (6 to 8 pages, arXiv cs.CL or cs.AI): method, pilot 11, pilot 13 with
   13b and 13c, pilot 12 as a secondary result, a corrections section quoting what the
   number-check and the skeptic removed, limitations. Pre-registrations quoted verbatim
   with hashes. Title candidate: "Ownership without likelihood: what production language
   models use to decide whether they wrote a turn".
4. **A plain-language post** (the second HTML report, lightly edited) for LessWrong or the
   Alignment Forum, linking the repo.
5. **One external replication before the paper.** The GPT arm needs only a ChatGPT
   subscription and `codex login`; ask one outside person to run stage A and stage C
   (`SP_MODELS=gpt SP_OUT_PREFIX=gpt ... forks` then `own`) and compare tables.

## Rules this programme now follows

Pre-register predictions and refuters in the pilot doc and commit before the run. An
independent number-check and a separate adversarial pass before any figure is quoted
outside the repo. Full per-cell tables, never a hand-picked list. Every framing
manipulation gets a placebo frame matched for length and hedging. Misses at the threshold
are misses. Withdrawals are logged where the claim was made.
