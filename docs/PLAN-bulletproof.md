---
title: "Plan: making the ownership result bulletproof and useful"
status: revised 2026-09-04 after 17b was scored and the harness context leak was found; 17c, 15b and 14 running
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
   A doubt preamble with no rival costs 0.51 of ownership; mentioning that another model
   exists costs a further 0.27; offering that model as a candidate author of this very turn
   adds nothing. On both Claude judges the placebo moves nothing (296/296), the non-author
   mention costs 0.11 / 0.08 and candidate authorship a further 0.13 / 0.26 (Haiku / Opus),
   so exclusivity survives there and the mechanism differs by vendor.
2b. **The label decides (13d, 13e).** The identical word moved from the assistant turn to a
   user turn is owned 1.000 vs 0.000 on Haiku (296/296 vs 0/296), 1.000 vs 0.007 on Fable
   5.1, 1.000 vs 0.135 on Opus (residue: the number prompt) and 1.000 vs 0.118 on GPT
   (residue: the dog prompt), with no own-probability structure in any residue. Four
   judges, two vendors, pre-registered, layouts verified by listing probes.
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
| One-word answers carry no style | Pilot 17 done, 17b running: at paragraph length Opus and GPT pick their own paragraph in forced choice at 0.73 to 0.88, and Opus keeps owning its own paragraph under the rival frame (0.96 vs 0.58 / 0.67). The theory's "no likelihood term" is too strong at this length unless 17b's punctuation normalisation removes the effect | Claude ~$100 total, GPT free |
| ~~Ownership varies four-fold by prompt (number 0.62, dog 0.15) for unknown reasons~~ | Pilot 15: the prompt effect is localised to one prompt per judge, not a general property; pilot 16b localises the Opus case further to the stated range | closed as a threat; open as a curiosity |
| **Every Claude fork and judgement in pilots 11 to 17 carried `~/.claude/CLAUDE.md` and `code/CLAUDE.md`; every GPT one carried `code/AGENTS.md`** (found 2026-09-04 by the 17b skeptic pass: Opus wrote some paragraphs in the CLAUDE.md's caveman register). Harness fixed (HOME isolated, neutral cwd, probe answers NONE) | Pilot 17c (paragraphs, full clean rerun) and pilot 15b (one-word label and rival spot check), both pre-registered, running 2026-09-04 | Claude about $65, GPT free |
| One session day, one Codex template rollout | Test-retest of stage C on a second day, second template | GPT free |
| GPT's modal words overlap Opus's, so "other vendor" cells are mostly Haiku's | Add Gemini as a third source of modal words | Gemini API |
| The rival-frame variance on one-word cells carries authorship information | Pilot 16b: on Haiku it tracks a plain answer-quality judgement (ρ 0.615, in-category 0.98 good, off-category 0.02), with three cells owned above their quality rating | closed on Haiku; not run on Opus or GPT |

Order: 17b (running) decides whether theory row 8 is revised; pilot 14 (running) is the
exact-probability replication; then the 24-fork GPT power run and test-retest.

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
