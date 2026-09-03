---
title: "Pilot 14: exact probabilities on a scale series of open models"
status: pre-registered 2026-09-03 before the run; CPU only, free
depends_on: docs/PILOT-11-ownership.md (local arm), selfportrait/ownership_local.py
---
# Pilot 14: the ownership design with exact probabilities, 1.5B to 4B

The reviewer's first objection to pilots 11 and 13 is that own probability is a 48-fork
frequency with a 1/96 floor, measured through an agent harness whose system prompt is in
the stimulus. No free API returns logprobs (Gemini's free tier rejects `responseLogprobs`
on every model, checked 2026-09-03), so the clean version runs locally: teacher-forced
probability of each candidate word, exact P(Yes) = p(Yes)/(p(Yes)+p(No)) after a genuine
assistant-turn prefill, no system prompt, on Qwen2.5-1.5B-Instruct (pilot 11's local
arm), Qwen2.5-3B-Instruct and Qwen3-4B-Instruct-2507 (bf16, CPU; if 4B does not fit in
15 GB the run stops there and says so). Eighteen prompts (pilot 11's eight plus pilot 15's
ten), cells as in the local arm (64 sampled forks per prompt for p_sample, plus the valid
unsampled and off-category words), questions neutral, placebo, rival_norep2 and named,
layouts assistant and user2. Script `selfportrait/ownership_local.py`, rows in
`out/own_local_<model>.jsonl`, summary `selfportrait/ownership_local_summary2.py`.

## Predictions and refuters

1. **The label effect exists at every scale and grows.** Mean P(Yes) under `named`,
   assistant layout minus user2 layout, is positive at 1.5B, 3B and 4B and is larger at 4B
   than at 1.5B. *Refuter:* difference ≤ 0 at any scale.
2. **The likelihood term shrinks with scale.** Pilot 11 found Spearman(P(Yes), log p_tf)
   = +0.37 on the 1.5B intent question. Here, on the neutral question in the assistant
   layout over in-category cells, |ρ| at 4B is smaller than |ρ| at 1.5B. *Refuter:* ρ at
   4B ≥ +0.37 with p < 0.05, in which case the frontier-model null in pilots 11 and 13 is
   a readout-saturation artefact and the theory's "no likelihood term" claim is withdrawn
   for the graded case.
3. **Placebo.** Neutral minus placebo mean P(Yes), assistant layout, within 0.10 at each
   scale. *Refuter:* a drop ≥ 0.25 at any scale.
4. **Rival-not-author.** Placebo minus rival_norep2 reported at each scale; no prediction
   (exclusivity was vendor-specific on the frontier judges).
5. **Off-category** words: under `named` in the assistant layout owned less than
   in-category words by ≥ 0.10 at 1.5B (pilot 11 found the small model detects nonsense),
   and by less at 4B than at 1.5B.

Item selection: every cell the script builds; no cell dropped. Statistics on cell values
(exact probabilities, so no fork-level pseudo-replication arises). Cost: none; wall time
about three hours of CPU.

Results: PENDING.
