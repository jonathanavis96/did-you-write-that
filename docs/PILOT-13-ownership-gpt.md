---
title: "Pilot 13: pilot 11 replicated on a non-Anthropic judge (GPT-5.6-Sol via Codex CLI)"
status: complete 2026-09-03; stages A-E run (2,352 calls, 0 errors); predictions 1, 3, 4 (rival arm), 6 met; 2 and 4 (confidence arm) missed at the boundary; 5 half met; numbers pending independent check
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

All five stages ran on 2026-09-03 through `codex exec … fork`, model `gpt-5.6-sol`,
read-only sandbox, 2,352 calls, 0 errors after one transient "thread history
projection" failure was purged and refilled. Codex returned per-call usage but the
harness did not persist it to the row files, so the pre-registered "token usage per
call is recorded" did not happen; the figure from the feasibility probe stands
(about 14k input tokens per call, mostly cached system prompt). No dollar cost.

### Stage A: GPT-5.6-Sol's own distribution (48 forks per prompt)

Mango 48/48, Lantern 48/48, Lisbon 42 (Prague 3, Vienna 3), Scout 33 (Beacon 5,
Chance 4, Haven 4), Indigo 33 (Vermilion 7, Cerulean 4, Turquoise 4), Cello 29 /
Piano 19, Rust 27 / Python 21, 17 26 / 13 21 / 14 1. Two prompts are deterministic,
two are near coin flips, so the within-support span is 3.9 nats (0.02 to 1.00).

GPT-5.6-Sol's modal words overlap Opus 5's heavily (Mango, Lantern, Scout, Cello, 17
are modal for both; Prague and Python are Opus-modal and GPT-produced). The
"other-vendor" cells are therefore mostly Haiku's words (Paris, Apple, Hope,
Telescope, Violin, Azure, 7) plus Teal from Opus; 8 in-category cells (64 forks per
question) where GPT's own probability is 0.00.

### Stage C: three ownership questions, 8 forks per cell, 42 cells, 1,008 rows

| question | in-category P(Yes) | off-category P(Yes) |
|---|---|---|
| neutral | 1.000 (272/272) | 0.98 (63/64; Wrench 7/8) |
| intent | 0.996 (271/272; one Mango fork No) | 0.27 (17/64: Wednesday-as-a-dog 8/8, Stapler-as-an-instrument 7/8, Nairobi 1/8, Wrench 1/8, rest 0/8) |
| rival | 0.27 (72/272) | 0.00 (0/64) |

Rival frame by who produces the word (fork level): GPT-only 23/56 = 0.41, Haiku-or-Opus-only
18/64 = 0.28, both 32/88 = 0.36, neither 18/64 = 0.28; GPT-only vs other-only Fisher
p = 0.18. By tag: own_top 21/64 = 0.33, own_mid 18/48 = 0.38, own_low 16/32 = 0.50,
valid_unsampled 18/64 = 0.28, haiku_top 14/56 = 0.25, opus_top 4/8. Cell-level Spearman
of rival P(Yes) against log own-probability ρ = +0.12, p = 0.50 (34 cells); logistic
slope on log p_gpt +0.04. The "ever produced by either model" flag that carried
Opus's rival-frame variation (χ² 35.3) carries nothing here (χ² 1.1, p = 0.3);
own-probability given the flag χ² 0.0 (p = 0.86); other-model coefficient −0.027,
within-prompt permutation p = 0.70 (2,000 perms). Inside GPT's produced set (18 cells)
ρ = −0.23, p = 0.35.

Cells worth seeing: Mango (own p 1.00) rival 1/8, Lisbon (0.88) 1/8, Indigo (0.69)
1/8, Scout (0.69) 1/8; the number 14 (0.02) 8/8, 13 (0.44) 8/8, Haven (0.08) 5/8.
Neutral question versus rival question on the same 34 in-category cells: 1.00 vs 0.27,
mean paired difference +0.73, Wilcoxon p = 2.1e-08. Intent vs rival 0.996 vs 0.27.

### Stage D: confidence (252 rows) and explicit forced choice (204 rows)

**Confidence is binary on this model.** Of 252 rows, 247 are exactly 100 and 5 are
exactly 0; in-category 202/204 are 100 (the two zeros: one Lantern fork, one Piano
fork), off-category 45/48 (Nairobi 1 zero, Stapler 2). In-category mean 99.0,
off-category 93.8. Cell-level Spearman(conf, log p_own) ρ = −0.303, p = 0.081 over 34
cells, a statistic on a variable with two values, pulled negative by the two in-category
zeros both landing on produced words. Own modal word 97.9 (n = 48, Lantern's zero) vs
other vendor's modal word 100.0 (n = 48): gap 2.1 points, the wrong sign for a
likelihood term. Own-high/other-low 100.0 (n = 12) vs other-high/own-low 100.0 (n = 48).
The graded readout that pilot 11 leaned on (Opus SD 1 to 5 points within cell) does not
exist on GPT-5.6-Sol; the rival frame is the only readout with variance.

**Explicit self-prediction (no prefill, option order alternated; first-listed chosen
0.65).** Picks own modal answer in 0.77 of 156 in-category pairs; vs the other vendor's
top 0.79 (n = 48); vs valid-unsampled 0.94.

| GPT-5.6-Sol, own modal answer vs | picks own | p_own(own) | p_own(rival) |
|---|---|---|---|
| Mango vs Apple / Quince / Wrench | 6 of 6 each | 1.00 | 0.00 |
| Lantern vs Telescope / Thimble / Quickly | 6 of 6 each | 1.00 | 0.00 |
| Lisbon vs Ljubljana | 3 of 6 | 0.88 | 0.00 |
| Lisbon vs Prague, Lisbon vs Vienna | 3 of 6 each | 0.88 | 0.06 |
| Lisbon vs Paris | 5 of 6 | 0.88 | 0.00 |
| Indigo vs Teal | 2 of 6 | 0.69 | 0.00 |
| Indigo vs Azure / Cerulean | 3 of 6 each | 0.69 | 0.00 / 0.08 |
| Rust vs Python | 1 of 6 | 0.56 | 0.44 |
| 17 vs 13 | 3 of 6 | 0.54 | 0.44 |
| Scout vs anything, Cello vs Violin / Theremin / Stapler | 6 of 6 each | | |

Unlike Opus (Prague vs Paris 0/6 at p_own 0.98), GPT-5.6-Sol names its deterministic
answers: Mango and Lantern 6/6 against every rival. Its failures are on the graded
prompts: it is at chance on Lisbon against a city it has never produced (Ljubljana,
3/6), picks Teal over Indigo 4/6 when it produces Indigo 33/48 and Teal 0/48, and
picks Python over Rust 5/6 on a near coin flip.

### Stage E: within-support gradient, 21 produced words, 12 forks each, 504 rows

Rival P(Yes) against log own-probability inside the produced set: ρ = −0.10, p = 0.66;
against log other-probability ρ = −0.06; against word frequency ρ = +0.13; partial
correlation with own-probability given frequency and other-probability r = +0.10,
p = 0.66; prompt fixed effects slope −0.001 per nat (t = −0.03, p = 0.97). Confidence is
100 in all 252 stage E rows (SD 0), so every confidence statistic is undefined and the
slope is 0.000 by construction. Extremes: Mango (1.00) 2/12, Lisbon (0.88) 1/12,
Scout (0.69) 1/12; 13 (0.44) 8/12, Vermilion (0.15) 5/12, 14 (0.02) 3/12. Modal minus
rarest produced word within prompt: −0.04 over 6 prompts.

## Predictions scored

| # | prediction | result | verdict |
|---|---|---|---|
| 1 | neutral ≥ 0.9 in-category, ≥ 0.75 off-category | 1.00, 0.98 | met |
| 2 | intent ≥ 0.9 in-category, ≤ 0.25 off-category | 0.996, 0.27 (17/64; threshold is 16/64) | in-category met; off-category missed by one fork, Wednesday 8/8 and Stapler 7/8 accepted as in pilot 11 |
| 3 | rival drop ≥ 0.20, Wilcoxon p < 0.01, text identical | −0.73, p = 2.1e-08 | met; twice the Claude effect (Opus −0.43, Haiku −0.34) |
| 4 | rival \|ρ\| < 0.3, p > 0.05 vs log p_own | ρ = +0.12, p = 0.50 | met |
| 4 | confidence \|ρ\| < 0.3, p > 0.05 | ρ = −0.303, p = 0.081 | p arm met; \|ρ\| arm missed by 0.003 on a two-valued variable; sign opposite to a likelihood term |
| 4 | own-modal vs other-vendor-modal confidence gap < 3 | 97.9 vs 100.0, gap 2.1 | met (wrong sign for likelihood) |
| 5 | explicit picks own < 0.85 in-category | 0.77 | met |
| 5 | on a ≥ 40/48 prompt, picks the other word in a majority | Mango 6/6, Lantern 6/6, Lisbon 3/6 in three pairs | not met; GPT knows its deterministic answers |
| 6 | stage E confidence slope < 1 pt/nat; rival \|ρ\| < 0.3 | 0.000 (degenerate); ρ = −0.10, p = 0.66 | met, confidence arm vacuous |

**Refuters.** None fired. No positive likelihood term appeared anywhere: the strongest
own-probability association in any readout is ρ = +0.12, and the two confidence
statistics that brush the pre-registered boundary point the wrong way. The rival-frame
drop is present and larger than on Claude. The Claude null on ownership versus own
probability is not vendor-specific.

**What differs from Claude, and was not predicted.** (1) Confidence is a two-valued
readout on GPT-5.6-Sol (100 or 0), so the graded instrument that closed pilot 11's
ceiling loophole is unavailable here; the rival frame is the only graded readout and it
is flat. (2) The rival frame is close to a blanket disavowal (0.27 in-category, 0.00
off-category): GPT-5.6-Sol disowns its own 48/48 word (Mango 1/8, 2/12) once told some
turns were replaced. Opus kept 0.55 and Haiku 0.65. (3) The produced/never-produced
step that Opus showed (0.69 to 0.77 produced vs 0.34 never-produced) is absent, as on
Haiku. (4) Explicit self-prediction is better than Opus's on deterministic prompts
(Mango, Lantern 6/6 vs Opus's Prague 0/6) and no better on graded ones.

**Reading.** Ownership on a second vendor is again label-plus-plausibility-plus-
exclusivity with no likelihood term: a word the model produces every time and a word it
has never produced get the same Yes under the neutral question, the same Yes under the
intent question, the same near-No under the rival frame, and the same 100 on confidence.
The exclusivity effect, which pilot 11 called the one thing that moves ownership with the
text held fixed, is the largest effect in this pilot. Prediction 8 of the theory doc
("ownership reads the label, not the likelihood") now holds on three models from two
vendors; the theory's likelihood half (Lindsey-style likelihood estimation feeding
ownership) has no support on any of them.

**Caveats.** One judge, one session day, one Codex system prompt. Off-category intent
is one fork over threshold, and the confidence arm of prediction 4 is 0.003 over on a
degenerate variable; both are reported as misses because the thresholds were fixed in
advance, and neither is in the direction the refuter needed. Own probabilities are fork
frequencies at 48 per prompt (floor 1/96 in logs), not logprobs. Codex's read-only
sandbox and 14k-token agent prompt are part of the stimulus. Numbers above await the
independent recompute.

## Costs

2,352 Codex calls on a ChatGPT subscription, no dollar cost; rate limits were not hit.
Wall-clock about 3.5 hours at roughly 5.3 s per call. Data under `out/gpt_*.jsonl`
(gitignored, 2,352 rows).
