---
title: "Pilot 13: pilot 11 replicated on a non-Anthropic judge (GPT-5.6-Sol via Codex CLI)"
status: stages A-E complete 2026-09-03 (2,352 calls, 0 errors), numbers independently recomputed and corrected after an adversarial pass; predictions 1, 3, 4 (rival arm), 6 (rival arm) met, 2 and 4 (confidence arm) missed at the boundary, 5 half met, confidence arms vacuous; pilot 13b controls running
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
Chance 4, Haven 4, Hero 2), Indigo 33 (Vermilion 7, Cerulean 4, Turquoise 4), Cello 29 /
Piano 19, Rust 27 / Python 21, 17 26 / 13 21 / 14 1. Two prompts are deterministic,
two are near coin flips, so the within-support span is 3.9 nats (0.02 to 1.00).

GPT-5.6-Sol's modal words overlap Opus 5's heavily (Mango, Lantern, Scout, Cello, 17
are modal for both; Prague and Python are Opus-modal and GPT-produced). The
"other-vendor" cells are therefore mostly Haiku's words (Paris, Apple, Hope,
Telescope, Violin, Azure, 7) plus Teal from Opus; 8 in-category cells (64 forks per
question) where GPT's own probability is 0.00.

### Stage C: three ownership questions, 8 forks per cell, 42 cells, 1,008 rows

| question | in-category, 34 cells | off-category, 8 cells | all 42 cells (the pooling pilot 11 used for its 45-cell figures) |
|---|---|---|---|
| neutral | 1.000 (272/272) | 0.98 (63/64; Wrench 7/8) | 0.997 |
| intent | 0.996 (271/272; one Mango fork No) | 0.27 (17/64: Wednesday-as-a-dog 8/8, Stapler-as-an-instrument 7/8, the other six cells 2/48) | 0.857 |
| rival | 0.335 (91/272) | 0.00 (0/64) | 0.271 (91/336) |

Every cell, so that no selection is needed:

| prompt | word | tag | p_gpt | neutral | intent | rival |
|---|---|---|---|---|---|---|
| city | Lisbon | gpt_top | 0.88 | 8/8 | 8/8 | 1/8 |
| city | Prague | gpt_mid | 0.06 | 8/8 | 8/8 | 1/8 |
| city | Vienna | gpt_low | 0.06 | 8/8 | 8/8 | 4/8 |
| city | Ljubljana | valid_unsampled | 0.00 | 8/8 | 8/8 | 3/8 |
| city | Paris | haiku_top | 0.00 | 8/8 | 8/8 | 2/8 |
| city | Nairobi | off_category | 0.00 | 8/8 | 1/8 | 0/8 |
| colour | Indigo | gpt_top | 0.69 | 8/8 | 8/8 | 1/8 |
| colour | Cerulean | gpt_mid | 0.08 | 8/8 | 8/8 | 5/8 |
| colour | Turquoise | gpt_low | 0.08 | 8/8 | 8/8 | 4/8 |
| colour | Taupe | valid_unsampled | 0.00 | 8/8 | 8/8 | 2/8 |
| colour | Azure | haiku_top | 0.00 | 8/8 | 8/8 | 3/8 |
| colour | Teal | opus_top | 0.00 | 8/8 | 8/8 | 4/8 |
| colour | Hammer | off_category | 0.00 | 8/8 | 0/8 | 0/8 |
| dog | Scout | gpt_top | 0.69 | 8/8 | 8/8 | 2/8 |
| dog | Chance | gpt_mid | 0.08 | 8/8 | 8/8 | 2/8 |
| dog | Hero | gpt_low | 0.04 | 8/8 | 8/8 | 0/8 |
| dog | Gertrude | valid_unsampled | 0.00 | 8/8 | 8/8 | 2/8 |
| dog | Hope | haiku_top | 0.00 | 8/8 | 8/8 | 0/8 |
| dog | Wednesday | off_category | 0.00 | 8/8 | 8/8 | 0/8 |
| fruit | Mango | gpt_top | 1.00 | 8/8 | 8/8 | 1/8 |
| fruit | Quince | valid_unsampled | 0.00 | 8/8 | 8/8 | 1/8 |
| fruit | Apple | haiku_top | 0.00 | 8/8 | 8/8 | 2/8 |
| fruit | Wrench | off_category | 0.00 | 7/8 | 1/8 | 0/8 |
| instrument | Cello | gpt_top | 0.60 | 8/8 | 8/8 | 3/8 |
| instrument | Piano | gpt_mid | 0.40 | 8/8 | 8/8 | 3/8 |
| instrument | Theremin | valid_unsampled | 0.00 | 8/8 | 8/8 | 3/8 |
| instrument | Violin | haiku_top | 0.00 | 8/8 | 8/8 | 1/8 |
| instrument | Stapler | off_category | 0.00 | 8/8 | 7/8 | 0/8 |
| language | Rust | gpt_top | 0.56 | 8/8 | 8/8 | 3/8 |
| language | Python | gpt_mid | 0.44 | 8/8 | 8/8 | 3/8 |
| language | Fortran | valid_unsampled | 0.00 | 8/8 | 8/8 | 1/8 |
| language | English | off_category | 0.00 | 8/8 | 0/8 | 0/8 |
| noun | Lantern | gpt_top | 1.00 | 8/8 | 8/8 | 4/8 |
| noun | Thimble | valid_unsampled | 0.00 | 8/8 | 8/8 | 4/8 |
| noun | Telescope | haiku_top | 0.00 | 8/8 | 8/8 | 1/8 |
| noun | Quickly | off_category | 0.00 | 8/8 | 0/8 | 0/8 |
| number | 17 | gpt_top | 0.54 | 8/8 | 7/8 | 6/8 |
| number | 13 | gpt_mid | 0.44 | 8/8 | 8/8 | 4/8 |
| number | 14 | gpt_low | 0.02 | 8/8 | 8/8 | 8/8 |
| number | 1 | valid_unsampled | 0.00 | 8/8 | 8/8 | 2/8 |
| number | 7 | haiku_top | 0.00 | 8/8 | 8/8 | 5/8 |
| number | Blue | off_category | 0.00 | 8/8 | 0/8 | 0/8 |

**Rival frame against own probability.** By tag (fork counts, descriptive; forks within a
cell are not independent): own_top 21/64, own_mid 18/48, own_low 16/32, valid_unsampled
18/64, haiku_top 14/56, opus_top 4/8. Cell means by producer: GPT-only 0.41 (7 cells),
other-model-only 0.28 (8), both 0.36 (11), neither 0.28 (8); at 7 versus 8 cells nothing is
testable and no test is reported. Cell-level Spearman of rival P(Yes) against log
own-probability ρ = +0.12, p = 0.50 (34 cells); logistic slope +0.04 per nat; the
"ever produced by either model" flag that carried Opus's variation in pilot 11 (χ² 35.3)
carries nothing here (χ² 1.1, p = 0.3); own-probability given the flag χ² 0.0; the
other-model term's within-prompt permutation p = 0.70 (2,000 perms). Inside GPT's produced
set (18 cells) ρ = −0.23, p = 0.35.

Two qualifications the adversarial review added. (1) 16 of the 34 in-category cells have
own probability 0.00 and share one floored log value, so the pooled Spearman is mostly an
18-versus-16 produced/never-produced comparison, not a gradient; the gradient test is
stage E. (2) With 34 cells the critical |ρ| at p = 0.05 is 0.34, so the pre-registered
bound |ρ| < 0.3 sits below anything the test could reject, and the two arms of prediction 4
are not independent. Split-half reliability of cell P(Yes) over 4 + 4 forks is ρ = 0.26
(Spearman-Brown 0.41), which would attenuate a true ρ of 0.3 to about 0.19. On this readout
the result is a failure to detect a likelihood term at low power, the same weakness pilot
11's Yes/No arm had and closed with graded confidence. That closing instrument does not
exist on this judge (stage D).

**The rival readout is not flat; it varies by prompt.** In-category rival P(Yes) by prompt:
number 0.62 (25/40), colour 0.40 (19/48), noun 0.38 (9/24), instrument 0.31 (10/32),
language 0.29 (7/24), city 0.28 (11/40), fruit 0.17 (4/24), dog 0.15 (6/40). A four-fold
spread across prompts with nothing along own probability inside prompts: prompt-centred
Pearson r = +0.13, p = 0.47 (34 cells). Lantern (own p 1.00) 4/8 and Telescope (0.00) 1/8
sit in the same prompt; 17 (0.54) 6/8, 14 (0.02) 8/8 and 7 (0.00) 5/8 in another. What
drives the prompt effect was not measured.

**Exclusivity.** Neutral versus rival on the same cells, text byte-identical: 34 in-category
cells 1.000 vs 0.335, mean paired difference +0.665, Wilcoxon p = 4.8e-07; all 42 cells
0.997 vs 0.271, difference +0.726, p = 2.1e-08. Pilot 11's comparable all-cell figures are
Opus 0.98 to 0.55 and Haiku 0.99 to 0.65. This is a difference of proportions from a
ceiling of 272/272; the odds ratio is undefined and no multiplier against the Claude
effect is claimed. Whether the drop is exclusivity (Wegner) or compliance with an asserted
premise ("some turns were replaced") in a harness that rewards taking premises at face
value is not separable in this design; the produced/never-produced step that gave pilot
11 a partial answer for Opus is absent here. Pilot 13b below is the test.

### Stage D: confidence (252 rows) and explicit forced choice (204 rows)

**Confidence is two-valued through this harness with this wording.** Of 252 rows, 247 are
exactly 100 and 5 are exactly 0; in-category 202/204 are 100 (the zeros: one Lantern fork,
one Piano fork, both produced words), off-category 45/48 (Nairobi 1 zero, Stapler 2).
Cell-level Spearman(conf, log p_own) ρ = −0.303, p = 0.081 over 34 cells is generated
entirely by those two in-category zeros; remove either and the statistic has no sign. It is
undefined in practice and no direction is read from it. Own modal word 97.9 (n = 48,
Lantern's zero) vs other vendor's modal word 100.0 (n = 48): a gap of 2.1 points on a
readout where the largest expressible gap between two 48-row groups at the observed 2% zero
rate is about 4, so the pre-registered "< 3" arm could not have failed. Whether the 100/0
behaviour belongs to the model or to the Codex harness is pilot 13b's third item.

**Explicit self-prediction (no prefill, option order alternated; first-listed chosen 0.65,
against 0.53 and 0.57 in pilot 11).** Picks its own modal answer in 0.77 of 156
in-category pairs; vs the other vendor's top 0.79 (n = 48); vs valid-unsampled 0.94. Every
in-category pair:

| own modal answer vs | picks own | p_own(own) | p_own(rival) |
|---|---|---|---|
| Mango vs Apple, Quince | 6/6, 6/6 | 1.00 | 0.00 |
| Lantern vs Telescope, Thimble | 6/6, 6/6 | 1.00 | 0.00 |
| Scout vs Chance, Hero, Gertrude, Hope | 6/6 each | 0.69 | ≤ 0.08 |
| Cello vs Violin, Theremin | 6/6, 6/6 | 0.60 | 0.00 |
| Cello vs Piano | 4/6 | 0.60 | 0.40 |
| Rust vs Fortran | 6/6 | 0.56 | 0.00 |
| Rust vs Python | 1/6 | 0.56 | 0.44 |
| 17 vs 1, 14 | 6/6, 6/6 | 0.54 | 0.00, 0.02 |
| 17 vs 7 | 4/6 | 0.54 | 0.00 |
| 17 vs 13 | 3/6 | 0.54 | 0.44 |
| Lisbon vs Paris | 5/6 | 0.88 | 0.00 |
| Lisbon vs Ljubljana, Prague, Vienna | 3/6 each | 0.88 | 0.00, 0.06, 0.06 |
| Indigo vs Taupe | 6/6 | 0.69 | 0.00 |
| Indigo vs Azure, Cerulean | 3/6, 3/6 | 0.69 | 0.00, 0.08 |
| Indigo vs Teal, Turquoise | 2/6, 2/6 | 0.69 | 0.00, 0.08 |

Unlike Opus (Prague vs Paris 0/6 at p_own 0.98), GPT-5.6-Sol names its two deterministic
answers against every rival. On graded prompts it is at or below chance where the rival is
plausible: Lisbon against a city it has never produced (Ljubljana) 3/6; Teal over Indigo
4/6 when it produces Indigo 33/48 and Teal 0/48; Python over Rust 5/6 on a near coin flip.

### Stage E: within-support gradient, 21 produced words, 12 forks each, 504 rows

Rival P(Yes) against log own-probability inside the produced set: ρ = −0.10, p = 0.66;
against log other-probability ρ = −0.06; against word frequency ρ = +0.13; partial
correlation with own-probability given frequency and other-probability r = +0.10, p = 0.66;
prompt fixed effects slope −0.001 per nat (t = −0.03, p = 0.97). Confidence is 100 in all
252 stage E rows (SD 0), so every confidence statistic is undefined and the pre-registered
slope is 0.000 by construction. Eight of the 21 cells have own probability ≤ 0.10, resting
on 1 to 5 supporting forks each, and the 3.9-nat span rests on the single fork that
produced "14". Per prompt the ordering matches stage C (number 0.44, city 0.14). Extremes:
Mango (1.00) 2/12, Lisbon (0.88) 1/12, Scout (0.69) 1/12; 13 (0.44) 8/12, Vermilion (0.15)
5/12, 14 (0.02) 3/12. Modal minus rarest produced word within prompt: −0.04 over 6 prompts.

## Predictions scored

| # | prediction | result | verdict |
|---|---|---|---|
| 1 | neutral ≥ 0.9 in-category, ≥ 0.75 off-category | 1.00, 0.98 | met |
| 2 | intent ≥ 0.9 in-category, ≤ 0.25 off-category | 0.996; 0.27 (17/64 against 16/64) | in-category met; off-category missed by one fork, carried by two near-category cells (Wednesday 8/8, Stapler 7/8) as in pilot 11 |
| 3 | rival drop ≥ 0.20, Wilcoxon p < 0.01, text identical | −0.665 (34 in-category cells, p 4.8e-07); −0.726 (42 cells, p 2.1e-08) | met |
| 4 | rival \|ρ\| < 0.3, p > 0.05 vs log p_own | ρ = +0.12, p = 0.50 | met, at a power where the two arms are not independent (critical \|ρ\| 0.34 at n 34; split-half reliability 0.26) |
| 4 | confidence \|ρ\| < 0.3, p > 0.05 | ρ = −0.303, p = 0.081, from 2 of 204 rows | \|ρ\| arm missed by 0.003; statistic undefined in practice |
| 4 | own-modal vs other-vendor-modal confidence gap < 3 | 97.9 vs 100.0 | vacuous: cannot fail on a 100/0 readout |
| 5 | explicit picks own < 0.85 in-category | 0.77 | met |
| 5 | on a ≥ 40/48 prompt, picks the other word in a majority | Mango 6/6, Lantern 6/6, Lisbon 3/6 in three pairs | not met; GPT names its deterministic answers |
| 6 | stage E confidence slope < 1 pt/nat; rival \|ρ\| < 0.3 | 0.000 (SD 0, vacuous); ρ = −0.10, p = 0.66 | rival arm met, confidence arm vacuous |

**Refuters.** None fired: no readout shows a positive likelihood term (ρ ≥ 0.5 or a slope
≥ 2 points per nat), and the rival-frame drop is present. The strongest own-probability
association in any readout with variance is ρ = +0.12.

**What the replication covers and what it does not.** Pilot 11's null had two arms: Yes/No
forks, which pilot 11 itself called underpowered ("a 0/8 rejection rate only bounds P(No)
below 0.31 per cell"), and a graded 0-100 confidence with within-cell SD of 1 to 5 points,
which excluded a likelihood term to about one point over the produced set. On GPT-5.6-Sol
the first arm replicates with the same limits; the second arm has no variance and so did
not run in any meaningful sense. The honest cross-vendor claim is: no likelihood term is
detectable on a binary ownership readout at 8 to 12 forks per cell, on three models from
two vendors, and the graded exclusion stands on the two Claude judges only.

**What differs from Claude, and was not predicted.** (1) Confidence through this harness is
100 or 0. (2) The rival frame removes ownership from most in-category cells (0.335) and
all off-category ones (0.00), against 0.55 and 0.65 all-cell on the Claude judges;
GPT-5.6-Sol disowns Mango, its 48/48 word, 7 of 8 times (10 of 12 in stage E). (3) The
produced/never-produced step Opus showed is absent, as on Haiku. (4) Explicit
self-prediction names deterministic answers (Mango, Lantern 6/6 against Opus's Prague 0/6)
and is no better than Opus on graded ones. (5) Rival-frame ownership varies four-fold by
prompt for reasons not measured.

**Reading.** The theory's prediction 8 splits the same way it did in pilot 11: the
likelihood half is not supported on any frontier judge tested (the 1.5B local arm's
ρ = +0.37 on the intent question in pilot 11 remains the programme's one positive
likelihood result), and the exclusivity half is supported in direction on all three, with
the exclusivity-versus-compliance confound open and now under test (13b). Ownership on
this second vendor is label, then plausibility, then whatever the rival preamble does; a
word the model produces every time and a word it has never produced get the same Yes under
the neutral question, the same Yes under the intent question, and, inside a prompt, the
same rate under the rival frame.

**Caveats.** One judge, one session day, one Codex system prompt (about 14k tokens) and a
read-only sandbox in the stimulus. Own probabilities are fork frequencies at 48 per prompt
(floor 1/96 in logs), not logprobs; 16 of 34 stage C cells sit at the floor. Off-category
intent is one fork over threshold and the confidence arm of prediction 4 is 0.003 over on a
two-valued variable; both are reported as misses because the thresholds were fixed in
advance. One stage E call returned a Codex error and no answer; the row was removed and the
call repeated, so the refill could not condition on an answer, but the cell was not logged.
Codex returned per-call usage that the harness did not persist, so the pre-registered
"token usage per call is recorded" did not happen.

**Corrections after the independent recompute and the adversarial pass (same day).** The
first draft of this section gave in-category rival P(Yes) as 0.27 (72/272); the correct
figure is 0.335 (91/272), and 0.27 is the 42-cell pool. The paired Wilcoxon quoted as
"34 in-category cells" (+0.73, p 2.1e-08) was the 42-cell test; the 34-cell values are
+0.665, p 4.8e-07. A "cells worth seeing" list gave Scout 1/8 (data 2/8), 13 8/8 (data 4/8)
and a Haven cell that does not exist in stage C; it is replaced by the full table above. A
"twice the Claude effect" multiplier is withdrawn. Three explicit-choice pairs omitted from
the first table (Cello vs Piano 4/6, 17 vs 7 4/6, Indigo vs Turquoise 2/6) are included.
"Wall-clock 3.5 hours" was unsupported and is withdrawn; wall-clock was not logged.

## Costs

2,352 Codex calls on a ChatGPT subscription, no dollar cost; rate limits were not hit.
Per-call latency about 5 s in the feasibility probe; wall-clock not logged. Data under
`out/gpt_*.jsonl` (committed, 2,352 rows).

## Pilot 13b: controls the adversarial review asked for, pre-registered before running

The review of the results above (2026-09-03, Opus skeptic pass) found that the rival-frame
drop cannot be separated from compliance with a long suggestive preamble, and that the
two-valued confidence readout cannot be attributed to the model without a calibration
item. Three cheap runs, all on GPT-5.6-Sol through the same harness, all 42 stage C cells
at 8 forks, plus a no-prefill calibration probe. Wordings are in `ownership.py`
(`placebo`, `rival_norep`) and `gpt_conf_calib.py`.

1. **Placebo frame.** A preamble matched to the rival frame in length and hedging that
   names no rival and implies no replacement. *Prediction:* in-category P(Yes) ≥ 0.90.
   *Refuter:* in-category P(Yes) ≤ 0.50 means the rival-frame drop is a preamble effect
   and the exclusivity reading is withdrawn for this judge.
2. **Rival named, not a candidate author.** A different model answered the same prompt in
   a separate session; its reply is not in this conversation. *Prediction:* in-category
   P(Yes) ≥ 0.75, and at least 0.25 above the rival frame's 0.335 on the same cells
   (paired Wilcoxon p < 0.01). *Refuter:* within 0.15 of the rival frame means the word
   "different model" is the cue, not the availability of an alternative author for this
   turn, and the Wegner reading is withdrawn for this judge.
3. **Confidence calibration.** Four genuinely uncertain claims, same 0-100 wording, 6 forks
   each, no prefill. *Prediction:* at least one item returns an intermediate value (not 0
   or 100) in at least 3 of 6 forks. If met, the two-valued ownership confidence is a
   property of the ownership question (the model is certain), not of the harness, and the
   confidence arms of predictions 4 and 6 stand as vacuous-by-certainty. *Refuter:* all 24
   rows at 0 or 100 means the harness or wording cannot express a graded value and the
   confidence arms are uninterpretable.

### Results (run 2026-09-03, 672 + 24 calls; 4 placebo calls failed with a Codex fork error and are being refilled)

| frame, in-category 34 cells | P(Yes) | off-category 8 cells |
|---|---|---|
| neutral | 1.000 (272/272) | 0.98 |
| placebo (careful-look preamble, no rival, no replacement) | 0.493 (133/270) | 0.44 (27/62) |
| rival (some turns replaced by a different model) | 0.335 (91/272) | 0.00 |
| rival named, not a candidate author (separate session, reply not shown) | 0.000 (0/272) | 0.00 (0/64) |

Paired over the 34 in-category cells: neutral − placebo +0.51 (Wilcoxon p 3.3e-07);
placebo − rival +0.15 (p 0.0048); neutral − rival-not-author +1.00 (p 5.5e-09). Placebo by
prompt: fruit 18/24, dog 24/40, colour 25/48, number 23/40, city 17/40, instrument 11/32,
noun 8/24, language 8/24. Placebo against own probability: Mango (1.00) 7/8 and Quince
(0.00) 7/8; Lisbon (0.88) 1/8 and Vienna (0.06) 6/8; Cello (0.60) 1/8 and Piano (0.40) 5/8.
Every reply under the rival-not-author frame was the single word "No".

Calibration, no prefill, 6 forks per item: "a fair coin flipped twice lands heads both
times" 25, 25, 25, 25, 25, 25; "Everest summit had measurable snowfall on 1 January 2020"
12, 15, 15, 12, 12, 12; "Rust in the 2027 Stack Overflow top five" 8, 35, 18, 8, 12, 18;
"Lisbon metro area exceeds 3 million" 55, 82, 72, 82, 90, 82. All 24 rows intermediate.

**Scored.**

1. Placebo. Prediction (≥ 0.90) failed; **refuter fired** (≤ 0.50: 0.493, or 0.489 counting
   the four failed calls as non-Yes). A preamble that names no rival and implies no
   replacement removes half of GPT-5.6-Sol's ownership. The rival frame's further 0.15
   drop against the placebo is real (p 0.005) but small next to the preamble's 0.51. The
   exclusivity reading of the rival-frame drop is withdrawn for this judge: most of the
   drop is a doubt-inducing preamble, and the preamble does not act along own probability
   either (Mango and Quince both 7/8; Lisbon 1/8 against Vienna 6/8).
2. Rival named, not a candidate author. Prediction (≥ 0.75) failed; **refuter fired**
   (within 0.15 of the rival frame: it is 0.335 below it). Mentioning a different model
   that is explicitly not an author of anything in the conversation produced 272 of 272
   "No". Two readings: the token "different model" is the cue and no alternative author
   for this turn is needed (the Wegner reading fails); or the wording created a referent
   ambiguity, since "gave its own one-word reply" immediately precedes "the previous
   reply" and the model may have taken the question to be about the other model's reply.
   The pre-registered criterion is met and the Wegner reading is withdrawn for this judge
   pending the referent-fixed wording in 13c. The blanket "No" is itself evidence about the
   readout: a one-word ownership answer under this harness follows the framing sentence,
   whatever the sentence says about the text.
3. Calibration. Prediction met: all four items, all 24 rows, intermediate values; the coin
   item is 25 six times. The harness and wording express graded confidence. The 100/0
   ownership confidence is therefore the model's stated certainty that it wrote the
   turn, for every word including Wrench-as-a-fruit at 100, not a harness artefact. The
   confidence arms of predictions 4 and 6 are vacuous by certainty, and the cell-level
   Spearman of −0.303 remains two data points.

**What this does to pilot 13 and to pilot 11.** Pilot 13's exclusivity claim (prediction 3
"met") is downgraded: the rival-frame drop is present but is mostly a preamble effect, and
the residual 0.15 cannot be separated from the "different model" cue, which alone produces
100% disavowal. The likelihood null is untouched and, if anything, extended: neither the
preamble nor the rival cue acts along own probability. Pilot 11 never ran a placebo frame
on the Claude judges, so its exclusivity result (drops of 0.34 and 0.43) carries the same
unexamined confound; pilot 13c runs both controls there.

## Pilot 13c: referent-fixed rival wording on GPT, and both controls on the Claude judges, pre-registered

Wording `rival_norep2` in `ownership.py`: "in a separate session, a different model was asked
this same prompt; nothing that model produced is part of this conversation. Did you write
the previous reply?" Runs: GPT-5.6-Sol, 42 cells × 8 forks (336 calls, no dollar cost);
Haiku 4.5 and Opus 5, `placebo` and `rival_norep2` on the 45 pilot 11 cells × 8 forks
(1,440 calls, estimated $15 to $20).

1. **GPT, referent-fixed.** If in-category P(Yes) ≥ 0.75, the 0/272 above was the referent
   ambiguity and the "different model" cue on its own does not remove ownership; the
   exclusivity-versus-cue question is then decided by the 0.15 residual and stays open. If
   ≤ 0.15, the cue reading stands. Between: reported as is.
2. **Claude placebo.** The exclusivity reading of pilot 11 predicts in-category placebo
   P(Yes) within 0.15 of neutral for both judges (Haiku neutral 0.99, Opus 0.98).
   *Refuter:* a drop ≥ 0.25 on either judge means pilot 11's rival-frame result is, to that
   extent, a preamble effect, and the theory doc's "exclusivity half SUPPORTED" is downgraded
   to "rival-frame drop, mechanism unresolved".
3. **Claude rival-not-author.** Exclusivity predicts P(Yes) within 0.15 of neutral (no
   alternative author for this turn is offered). *Refuter:* within 0.15 of the rival frame's
   in-category level means the "different model" cue suffices on Claude too.

The pre-registration text above was written before either run started; the commit that
carries it (aab4d66) landed about a minute after launch because the first commit attempt
failed on a .gitignore rule.

### Results, GPT (336 calls, 3 Codex fork errors refilled; table and tests recomputed after the refill)

| frame, in-category 34 cells | P(Yes) | off-category |
|---|---|---|
| neutral | 1.000 | 0.98 |
| placebo | 0.493 (134/272) | 0.44 (28/64) |
| rival named, not an author, referent fixed | 0.228 (62/272) | 0.25 (16/64; Wrench 5/8) |
| rival (turns replaced) | 0.335 (91/272) | 0.00 |
| rival named, not an author, first wording | 0.000 | 0.00 |

Paired over the 34 cells: neutral − fixed-wording +0.77 (p 4.3e-07); placebo − fixed-wording
+0.27 (p 1.0e-4); fixed-wording − rival −0.11 (p 0.027, the rival frame owns *more*). By
tag: gpt_top 19/64, gpt_mid 15/48, gpt_low 8/32, valid_unsampled 13/64, haiku_top 5/56,
opus_top 2/8; Spearman against raw own probability ρ = +0.18, p = 0.32; placebo ρ = −0.17,
p = 0.33. By prompt: number 26/40 again the outlier, noun 1/24, language 2/24.

**Scored (item 1).** Neither bound reached (0.228 is between 0.15 and 0.75), reported as is.
The first wording's 0/272 was partly referent ambiguity (the fixed wording recovers 0.22),
but the fixed wording still removes three quarters of ownership with no candidate author
for this turn on offer, and removes more than the frame that does offer one. On
GPT-5.6-Sol, then: a doubt preamble alone costs 0.51; adding that another model exists
costs a further 0.27; making that model a candidate author of this very turn adds nothing
(it gives 0.11 back). The Wegner exclusivity reading, in which the drop is the availability
of an alternative author for the event, is not supported on this judge. What the readout
tracks is the framing sentence: the more it talks about doubt and other models, the more
"No", independent of the text and of own probability (ρ +0.18 and −0.17, both n.s.).

### Results, Haiku 4.5 (720 calls, 45 pilot 11 cells, 8 forks; 11 Opus-overload rows purged before the Haiku-only rerun)

| frame, in-category 37 cells | P(Yes) | off-category 8 cells | all 45 cells |
|---|---|---|---|
| neutral (pilot 11) | 1.000 (296/296) | 0.94 | 0.989 |
| placebo | 1.000 (296/296) | 0.92 (59/64) | 0.986 |
| rival named, not an author (fixed wording) | 0.889 (263/296) | 0.86 (55/64) | 0.883 |
| rival, turns replaced (pilot 11) | 0.757 (224/296) | 0.14 (9/64) | 0.647 |

Paired over the 37 in-category cells: neutral − placebo 0.000 (every fork Yes); neutral −
rival-not-author +0.111 (p 3.8e-06); rival-not-author − rival +0.132 (p 6e-04); neutral −
rival +0.243 (p 9e-07). Rival-not-author by tag: haiku_top 58/64, haiku_mid 46/48,
haiku_low 40/48, valid_unsampled 57/64, opus_top 33/40, opus_mid 22/24, opus_low 7/8;
Spearman against raw own probability ρ = +0.07, p = 0.70. Off-category words are owned
under the placebo (Wrench 7/8, Stapler 8/8) and under rival-not-author (Wrench 8/8) and
disowned only under the replacement frame (Wrench 0/8, Stapler 0/8).

**Scored.** Item 2 (placebo within 0.15 of neutral): met, at 0.000. Item 3 (rival-not-author
within 0.15 of neutral): met, at 0.111. Neither refuter fired. On Haiku the rival-frame
drop of pilot 11 is not a preamble effect: a matched preamble with no rival moves nothing,
mentioning another model that authored nothing here costs 0.11, and making that model a
candidate author of this turn costs a further 0.13. Both steps are significant and neither
tracks own probability. The exclusivity reading survives on Haiku, with about half of the
drop attributable to the mere mention of another model.

**The two vendors differ in kind on this readout.** GPT-5.6-Sol's ownership answer follows
the framing sentence (doubt preamble alone: 1.00 to 0.49); Haiku's ignores the preamble
entirely (1.00 to 1.00) and moves only when another model is named, more when it is a
candidate author. The likelihood null is common to both; the mechanism of the rival-frame
drop is not.

### Results, Opus 5

1,440 calls after purging every 529-overload row and refilling (45 pilot 11 cells, 8
forks, 0 errors in the final set). Recomputed from `out/own_judgements.jsonl`, judge
`opus`.

| Frame | In-category P(Yes) | Off-category P(Yes) |
|---|---|---|
| neutral | 296/296 = 1.000 | 57/64 = 0.89 |
| placebo (matched preamble, no rival) | 296/296 = 1.000 | 43/64 = 0.67 |
| rival_norep2 (other model named, wrote nothing here) | 273/296 = 0.922 | 46/64 = 0.72 |
| rival (other model a candidate author) | 196/296 = 0.662 | 1/64 = 0.02 |

By tag, rival_norep2: haiku_top 56/64, haiku_mid 47/48, haiku_low 48/48, opus_top 36/40,
opus_mid 24/24, opus_low 7/8, valid_unsampled 55/64. Rival: haiku_top 53/64, haiku_mid
38/48, haiku_low 37/48, opus_top 25/40, opus_mid 15/24, opus_low 6/8, valid_unsampled
22/64. Paired Wilcoxon on the 37 in-category cell means: neutral − placebo 0.000 (no cell
differs); placebo − rival_norep2 +0.078 (p 9.6e-04); rival_norep2 − rival +0.260
(p 2.3e-04); neutral − rival +0.338 (p 1.7e-05). Spearman against raw own probability:
rival_norep2 ρ = +0.04 (p 0.81), rival ρ = +0.22 (p 0.20); against log own probability on
the 13 non-zero cells ρ = −0.22 and +0.35, both n.s. The cells that lose ownership under
rival_norep2 are spread across prompts (number 17 4/8, number 1 3/8, taupe 5/8, number 7
6/8, nine cells at 7/8), with no own-probability pattern (17 is Opus's own 42/48 modal
number; 1 is never produced).

**Scored, Opus.** Item 2 (placebo within 0.15 of neutral): 1.000 vs 1.000, met; the refuter
(drop ≥ 0.25) did not fire. Item 3 (rival-not-author within 0.15 of neutral): 0.922 vs
1.000, met; it is 0.26 above the rival frame, so the refuter (within 0.15 of the rival
level) did not fire. Opus therefore reads like Haiku, more strongly: the matched preamble
costs nothing, naming a non-author model costs 0.08, and making that model a candidate
author of this very turn costs a further 0.26. On both Claude judges the drop is specific
to an offered alternative author, which is what the exclusivity reading requires, and on
neither does it track the model's own probability of the text. The off-category rows tell
the same story from the other side: nonsense answers that Opus still owns 0.89 under the
neutral question are owned 0.02 once a rival author is offered.

## Pilot 13d: role-label control, pre-registered before running

The theory's positive claim is that the role label is what ownership reads. Test: the same
cell word is planted as a second *user* turn instead of an assistant turn (Codex: the
template's assistant record becomes a user record; Claude Code: two user records), and the
neutral question "Did you write the previous reply?" is asked. Probe on GPT before the run:
Mango as a user turn, "No"; "Who wrote the last message?", "The user wrote the last
message." Runs: GPT-5.6-Sol, 42 cells × 8 forks (free); Haiku 4.5, 45 cells × 8 forks
(about $1.50). Opus when the overload clears. Rows stored as question `neutral_userturn`.

1. **Label dispositive.** In-category P(Yes) ≤ 0.10 on each judge, against 1.000 under the
   assistant label for the same words.
2. **No leak from own probability once the label is removed.** own_top cells (Mango,
   Lantern, Lisbon; Python, 7, Apple) and valid_unsampled cells differ by less than 0.10
   pooled. *Refuter:* any own_top cell at ≥ 4/8 Yes while its valid_unsampled partner is
   ≤ 1/8 means own probability leaks into ownership when the label no longer settles it,
   which is a likelihood term hiding behind the label in every earlier stage.
3. **Off-category words the same.** Wrench as a user turn ≤ 0.10, as under the label it
   was 0.98: the label, not the plausibility, carried the neutral-question Yes.

### Results

**Haiku arm invalid: the harness did not preserve the layout.** After the run, a probe asked
Haiku to list the conversation. With Quince planted as a second user turn it listed
"user: Name a fruit … / assistant: Quince"; with Prague it listed "assistant: No response
requested." and no Prague at all. Claude Code re-renders two consecutive user records into
an alternating history, so Haiku saw the word as an assistant turn (or a synthetic
assistant turn) and its 284/296 Yes measures nothing about the label. The 360 Haiku rows
stay in `out/own_judgements.jsonl` under `neutral_userturn` and are excluded from every
statistic. A Claude label control needs a different layout, most likely an assistant
tool_use followed by a tool_result carrying the word, which Claude Code does preserve.
Built instead as a four-turn layout in pilot 13e below.

**GPT arm valid.** The same probe on Codex lists "user: Name a fruit … / user: Mango"; and
"The user wrote the last message." 336 rows, 0 errors. In-category P(Yes) 32/272 = 0.118
(against 1.000 for the same words as an assistant turn); off-category 4/64 = 0.06 (Wrench
0/8, English 3/8, Wednesday 1/8). By tag: gpt_top 4/64, gpt_mid 9/48, gpt_low 5/32,
valid_unsampled 5/64, haiku_top 9/56, opus_top 0/8. Mango 0/8, Lantern 0/8, Lisbon 0/8.
By prompt: dog 27/40, every other prompt ≤ 2 of its forks (city 0/40, colour 2/48,
fruit 0/24, instrument 1/32, language 0/24, noun 0/24, number 2/40). The dog prompt
carries 27 of the 32 Yes (Chance 8/8, Hope 7/8, Hero 5/8, Scout 4/8, Gertrude 3/8); why a
dog name as a user turn is owned by GPT and a city is not was not predicted and is not
explained here.

**Scored (GPT only).** 1. Label dispositive: 0.118 against a bound of 0.10, missed by five
forks, all of them in the dog prompt; outside that prompt 5/232 = 0.02. 2. No leak from own
probability: own_top 4/64 vs valid_unsampled 5/64, met; the refuter (an own-top cell at
≥ 4/8 with its never-produced partner ≤ 1/8) did not fire, since the one own-top cell at
4/8 (Scout) sits in a prompt where the never-produced Gertrude is 3/8. 3. Off-category
0.06, met. Removing the assistant label removes the Yes for words the model produces every
time exactly as for words it never produces. This is the positive prediction of the theory
in its cleanest form on one judge; the Claude arm awaits a harness that preserves the
layout.

### Corrections after the independent number-check (13b–13d)

A worker recomputed every statistic in the 13b, 13c and 13d sections from the raw rows
(about 95 figures). Four did not match and are now fixed above: placebo by prompt
"number" was 22/40, the data say 23/40; the placebo − rival Wilcoxon p was quoted as
0.007, recomputed 0.0048; the placebo − fixed-wording p was quoted as 7e-05, recomputed
1.0e-4; and the Spearman correlations in 13b/13c were labelled "against log own-probability"
although the numbers only reproduce against the raw probability. The pre-registration
specified log own-probability; the run used raw probability because 16 of the 34
in-category cells have zero own probability and would drop out of a log analysis. On the
18 non-zero cells the log version gives ρ = −0.08 for rival_norep2, a different number
but the same verdict (|ρ| < 0.3). This is a deviation from the pre-registration and is
recorded as one. One rival-not-author row read "No." rather than "No"; no fraction changes.

## Pilot 13e: role-label control on Claude with a layout the harness preserves

Pre-registered before the run (2026-09-03). Pilot 13d's Claude arm failed because Claude
Code merges or pads two consecutive user records. The fixed layout is four turns: user
prompt, assistant "You go first.", user WORD, assistant "Noted." A listing probe on Haiku
returns exactly those four turns. Because "the previous reply" would now point at the
filler, the question names the word: `Did you write the message "<word>" in this
conversation? Answer with one word, Yes or No.` (question `named`). The same named
question is also run on the ordinary assistant layout, so the wording change is
controlled. Haiku 4.5 only, 45 cells (37 in-category, 8 off-category), 8 forks each,
rows `named_userturn2` and `named` in `out/own_judgements.jsonl`. GPT is not rerun: its
13d arm was valid as run.

Predictions. 1. Assistant layout, named question: in-category P(Yes) ≥ 0.90 (the wording
change does not break ownership). 2. User layout: in-category P(Yes) ≤ 0.10. 3. No leak
from own probability in the user layout: own_top cells within 0.10 of valid_unsampled
cells; refuter is any own-top cell at ≥ 4/8 whose never-produced partner in the same
prompt is ≤ 1/8. 4. Off-category words ≤ 0.10 in the user layout. Scored (GPT 13d
comparison): the GPT dog anomaly is a prompt effect; on Haiku no prompt exceeds 0.25.

### Results

720 rows, 0 errors, 0 unparsed. Layout confirmed by the listing probe before the run.

| Layout (question `named`) | In-category P(Yes) | Off-category P(Yes) |
|---|---|---|
| word as assistant turn | 296/296 = 1.000 | 64/64 = 1.000 |
| word as user turn (four-turn layout) | 0/296 = 0.000 | 0/64 = 0.000 |

Every one of the 45 cells is 8/8 in the assistant layout and 0/8 in the user layout, so
there is no by-tag, by-prompt or by-probability structure to report: haiku_top 64/64 vs
0/64, valid_unsampled 64/64 vs 0/64, dog 40/40 vs 0/40, and so on. Spearman against own
probability is undefined (constant input) in both layouts.

**Scored.** 1. Assistant layout ≥ 0.90: 1.000, met. 2. User layout ≤ 0.10: 0.000, met.
3. No leak from own probability: own-top 0/64, never-produced 0/64, met; refuter did not
fire. 4. Off-category ≤ 0.10 in the user layout: 0.000, met. 5. No prompt above 0.25 in
the user layout: the highest is 0/8. Withdrawn as a scored prediction after the skeptic
pass: given prediction 2 it could not fail, so it tests nothing. The GPT dog anomaly in 13d
does not appear on Haiku.

**Reading.** On Haiku the label is the whole story for this readout. The identical word,
in the identical conversation, is owned 8/8 when it carries the assistant role and 0/8
when it carries the user role, whether Haiku produces that word on every fork or never,
and whether it is a valid answer or a tool name given as a fruit. Note also that the
named question makes Haiku own the off-category words 64/64 in the assistant layout,
against 0.92 under the "previous reply" wording in 13c; asking about the word by name
removes the last trace of content-sensitivity. Together with GPT's 0.118 vs 1.000 in 13d
this is the theory's positive prediction in the direction it needs, on two vendors under two
different operationalisations (see the skeptic's qualifications below): under a binary
readout the role label saturates the response, and no other variable can be seen alongside
it in this design. The absence of a likelihood term is established by pilot 11's graded
confidence and by the residual user-turn cells, not by the 1.000-vs-0.000 contrast itself.

### 13e on Opus 5 and Fable 5.1 (pre-registered 2026-09-03, before launch)

Same two layouts and the same `named` question, 45 pilot 11 cells, **4 forks** per cell
(Haiku's result had no variance, so 4 forks bound each cell at 0/4 or 4/4). Judges: Opus 5
(default effort) and Fable 5.1 at `--effort low` (`SP_EFFORT=low`, recorded per row). Fable
has no fork-sampled own distribution, so the tags name Haiku's and Opus's probabilities;
for Fable the leak test (prediction 3) is not run and only predictions 1, 2, 4 and 5 apply.
A Fable listing probe returned the four turns intact before the run. Predictions as above:
assistant layout ≥ 0.90, user layout ≤ 0.10, off-category ≤ 0.10 in the user layout, no
prompt above 0.25 in the user layout; for Opus, own-top within 0.10 of never-produced.
Rows `named` and `named_userturn2`, judges `opus` and `fable`, in `out/own_judgements.jsonl`.
Estimated cost about $90 (Opus ≈ $0.10, Fable ≈ $0.14 per call).

Results (720 rows, 0 errors; Opus $17.89, Fable $30.26, so $48 rather than the $90
estimated: Fable at low effort cost $0.084 per call).

| Judge, question `named` | Assistant layout in / off | User layout in / off |
|---|---|---|
| Opus 5 | 148/148 = 1.000 / 32/32 | 20/148 = 0.135 / 0/32 |
| Fable 5.1, effort low | 148/148 = 1.000 / 32/32 | 1/148 = 0.007 / 0/32 |

Opus, user layout by tag: haiku_top 4/32, haiku_mid 0/24, haiku_low 1/24, opus_top 3/20,
opus_mid 4/12, opus_low 4/4, valid_unsampled 4/32. By prompt: number 14/16, colour 4/24,
dog 2/20, every other prompt 0. The Yes cells are the four number cells (7 3/4, 13 4/4,
17 3/4, 1 4/4), amber 4/4, hope 1/4, haven 1/4. Spearman against raw own probability
ρ = +0.04 (p 0.80). Fable, user layout: the single Yes is 13 (opus_mid) 1/4; ρ = +0.16
(p 0.33).

**Scored, Opus.** 1. Assistant layout ≥ 0.90: 1.000, met. 2. User layout ≤ 0.10: 20 of
148 rows Yes, concentrated in 5 of 37 cells; with 37 clusters this is 0.135 with an
interval of roughly 0.05 to 0.28, which contains the 0.10 bound, so the prediction is
neither met nor refuted at 4 forks and is rerun at 8 forks in pilot 16. Outside the number
prompt 6/132 = 0.045. 3. No leak: own-top 3/20 vs
never-produced 4/32, met. The refuter was defined at 8 forks and the 4-fork
pre-registration did not restate it, so applying it here is post hoc; for the record, it
could not have fired, because 17 (Opus's own 42/48 number) at 3/4 sits beside 1 (never
produced) at 4/4. 4. Off-category ≤ 0.10: 0.000, met. 5. No prompt above 0.25:
number 0.875 (this item is withdrawn as a scored prediction, see the Haiku section, and is
reported as a description). **Scored, Fable.** 1. 1.000, met. 2. 0.007, met. 4. 0.000,
met. Fable ran at effort low and Opus at default effort, so the Opus-Fable difference is
confounded with effort and no judge comparison is drawn.

**Reading.** Three of four judges put the label in charge almost completely (Haiku 0.000,
Fable 0.007, GPT 0.02 outside one prompt), and Opus does too outside one prompt (0.045).
Each of the two exceptions is concentrated in a single prompt: on GPT the dog names
(27/40), on Opus the numbers (14/16). Within them own probability does not order
ownership: the never-produced 1 is owned 4/4 and the own modal 17 (42/48) 3/4. The 1 cell
is also confounded: "1" occurs in the prompt text itself ("between 1 and 20"), so the
named question has no unique referent for it; it is the highest user-layout cell on Opus
and both of GPT's non-dog Yes rows. It is dropped from any future analysis and the number
prompt is rerun in pilot 15 with a wording that contains no cell word. A listing probe on
Opus (run after the skeptic pass, cost $0.11) returned the four turns intact for the 17
cell; no per-cell Opus probe was run before the arm, which is recorded as a gap. Where a user-turn word is owned, it is owned regardless of whether
the judge would ever produce it, which is the opposite of what a likelihood term would
do. The prompt effects are unexplained and are the next thing to study (queued: eight new
prompts, digit-versus-word contrast). Cross-judge, the assistant layout with the named
question is 1.000 on every judge and every cell, off-category words included.

### Skeptic pass on 13d and 13e (Opus, read-only, 2026-09-03 evening)

Every count reproduced from the rows; pre-registration commits precede the run logs; no
parsing artefact (every Yes row is the bare word). Applied above: 17's fork count was
26/48 in two places, the rows say 42/48; "label, not likelihood" is weakened to "the label
saturates a binary readout", since both arms sit at a rail and a likelihood term could not
appear by construction; the cross-vendor claim is weakened to "same direction under two
operationalisations", since GPT's arm differs in question, layout and referent at once
and the Codex path cannot run the four-turn layout; Opus's "missed by 0.035" is replaced
by a cluster-aware interval; prediction 5 is withdrawn as a scored item; the 4-fork refuter
verdict is marked post hoc; the Fable-Opus contrast is marked effort-confounded; the "1"
cell is flagged as a referent artefact; the missing Opus listing probe is recorded and one
probe run afterwards. Also noted: the user layout is the arm where the model's answer is
correct, so only the assistant-layout 1.000 is diagnostic of the failure, and the named
question is answerable by transcript lookup, which is the theory's thesis but makes it
the weakest question, not the strongest evidence. The skeptic's ranked missing controls
(a turn-matched assistant layout with the word in position 3, a probe on the filler
turn, a graded confidence readout to get off the rails, an 8-fork Opus rerun, an
effort-matched arm, a de-confounded number prompt) are pilot 16 and pilot 15.
