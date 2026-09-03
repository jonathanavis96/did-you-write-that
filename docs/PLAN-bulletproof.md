---
title: "Plan: making the ownership result bulletproof and useful"
status: drafted 2026-09-03 after pilots 13, 13b, 13c (GPT); Claude 13c controls running
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
   adds nothing. The Claude judges never had this control; it is running (13c).
3. **Source credibility (pilot 12).** Direction established (system and developer move
   Opus on contestable facts, a bystander does not), size not.
4. **What is withdrawn.** A "twice Claude's effect" multiplier, a cherry-picked cell list,
   an in-category figure that was the all-cell pool, a boomerang, and the Wegner reading
   of the GPT rival-frame drop. Every withdrawal is logged in the pilot doc it came from.

## Threats that remain, and the run that answers each

| threat | run | cost, who |
|---|---|---|
| The Claude rival-frame drop (0.34, 0.43) is also a preamble effect | 13c placebo and rival-not-author on the 45 pilot 11 cells, both judges, 8 forks | ~$15, running |
| Own probabilities are 48-fork frequencies with a 1/96 floor, and an agent harness sits in the stimulus | Same design through the OpenAI or Gemini API with logprobs and no system prompt; stages A to E | API key; ~3,000 calls, $10 to $30 |
| Binary readout at 8 forks cannot exclude a small likelihood term on GPT | 24 forks per cell on the 21 stage E cells, rival and placebo frames | GPT free; Claude ~$20 |
| One-word answers carry no style | Paragraph-length ownership: sample 3-sentence answers, plant own-high, own-low and other-model paragraphs, same frames plus placebo | ~$40 on Claude, GPT free |
| Ownership varies four-fold by prompt (number 0.62, dog 0.15) for unknown reasons | Eight new prompts; test digit vs word answers; test whether the prompt effect tracks the placebo (doubt) or the rival cue | GPT free |
| One session day, one Codex template rollout | Test-retest of stage C on a second day, second template | GPT free |
| GPT's modal words overlap Opus's, so "other vendor" cells are mostly Haiku's | Add Gemini as a third source of modal words | Gemini API |

Order: 13c Claude (running), then the API-with-logprobs replication, then paragraph
length. The first two close the two objections a reviewer raises first.

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
