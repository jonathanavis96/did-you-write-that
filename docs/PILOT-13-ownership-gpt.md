---
title: "Pilot 13: pilot 11 replicated on a non-Anthropic judge (GPT-5.6-Sol via Codex CLI)"
status: pre-registered 2026-09-03 before any stage ran; harness being ported
depends_on: docs/PILOT-11-ownership.md, docs/THEORY-exteroceptive-self.md (prediction 8), selfportrait/codex_fork.py
---

# Pilot 13: ownership versus own probability on GPT-5.6-Sol

## Why

Both judges in pilot 11 are Anthropic models. The claim "ownership does not track
own probability" is a claim about Claude until a second vendor shows it. GPT-5.6-Sol
is reachable through the Codex CLI on a ChatGPT subscription, and the same
session-file trick that gave genuine prefill on Claude works there: a rollout JSONL
with a planted assistant turn, forked with `codex exec … fork <id>`. Probe on
2026-09-03: planted "Timbuktu" was read back as the model's own city, and owned with
"Yes".

## Design

Identical to pilot 11 stages A to E with one judge, `gpt` (model `gpt-5.6-sol`), and
the Claude judges' modal answers added as cross-model cells (Opus: Prague, Mango,
Scout, Lantern, Cello, Teal, 17, Python; Haiku: Paris, Apple, Hope, Telescope,
Violin, Azure, 7, Python), so "another model's high-probability text" is text from a
different vendor. Stage A 48 forks per prompt; stage C 8 forks per cell per
question; stage D confidence and explicit forced choice; stage E every produced word
at 12 forks. Same prompts, same question wording, same capitalisation rule, same
scoring code. Outputs under `out/gpt_*`.

Harness difference to record, not remove: Codex prepends its own agent system prompt
(about 14k tokens, "You are Codex, an agent based on GPT-5"), as Claude Code
prepends its own. Both judges therefore answer as a coding agent, which is the
setting the theory is about.

## Predictions, fixed before stage A

Falsifiable statements about the `gpt` judge, evaluated with the pilot 11 scripts.

1. **Role label dispositive.** Neutral question: P(Yes) ≥ 0.9 pooled over in-category
   cells, and ≥ 0.75 over off-category cells (Wrench as a fruit and its kin).
2. **Plausibility filter under doubt.** Intent question: P(Yes) ≥ 0.9 in-category,
   ≤ 0.25 off-category.
3. **Exclusivity.** Rival frame lowers P(Yes) by at least 0.20 against the neutral
   question on the same in-category cells (paired Wilcoxon p < 0.01), with the text
   byte-identical.
4. **No likelihood term.** Over in-category cells, Spearman of rival-frame P(Yes)
   against log own-probability has |ρ| < 0.3 with p > 0.05; the same for the 0–100
   confidence. Mean confidence for the judge's own modal word and for the other
   vendor's modal word differ by less than 3 points, pooled over prompts.
5. **Explicit self-prediction is imperfect where behaviour is deterministic.** In the
   forced choice between its own modal answer and a rival modal answer, the judge
   picks its own in fewer than 0.85 of in-category pairs, and on at least one prompt
   where it produces one word in ≥ 40 of 48 forks it picks the other word in a
   majority of forks.
6. **Stage E.** Inside the judge's own produced set, prompt-fixed-effects slope of
   confidence per nat of log own-probability is below 1.0 point in absolute value, and
   rival-frame P(Yes) against log own-probability has |ρ| < 0.3.

**What would refute pilot 11's reading.** Prediction 4 or 6 failing in the direction
of a positive likelihood term (ρ ≥ 0.5, p < 0.01, or a slope ≥ 2 points per nat)
would mean the Claude null is vendor-specific and the theory's likelihood half is
back in play. Prediction 3 failing (no rival-frame drop) would remove the exclusivity
result from "general" to "Claude".

No directional prediction for the produced/never-produced step under the rival frame
(Opus showed it, Haiku did not).

## Analysis plan

`ownership_summary.py`, `ownership_summary_d.py`, `ownership_summary_e.py` and
`ownership_review_stats.py` with the `gpt_` prefix, plus the independent number-check
pass before any figure is quoted. Costs are subscription quota, not dollars; token
usage per call is recorded.

## Results

PENDING
