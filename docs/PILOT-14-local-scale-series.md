---
title: "Pilot 14: exact probabilities on a scale series of open models"
status: run 2026-09-04 on the RX 6800 through torch-directml (see Deviation); results scored against the pre-registration and number-checked; free
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

Deviation from the pre-registration, 2026-09-04 (before any result was looked at): the
run moved from CPU bf16 to the RX 6800 through torch-directml (`.venv-dml`, torch 2.4.1,
transformers 4.57.6, `SP_LOCAL_DEVICE=dml`, script `out/logs/p14_gpu.sh`). Dtype is fp32
for the two Qwen2.5 models and fp16 for Qwen3-4B, which does not fit 16 GB in fp32. The
reason is precision as much as speed: on the `bird` prompt the CPU bf16 rows differ from
DirectML fp32 by up to 0.32 nats in log p_tf and 0.049 in P(Yes) across 12 shared cells,
while DirectML fp32 matches CPU fp32 to 4e-5 nats and fp16 to 0.01 to 0.03 nats on a
1.5B forward pass. So the bf16 CPU rows were the imprecise ones. The partial CPU bf16
files are kept as `out/own_local_qwen2.5-{1.5b,3b}-instruct_cpu_bf16.jsonl` and are not
used for the results. Every row now carries `device` and `dtype`. Design, prompts,
questions, cells, predictions and statistics are unchanged.

## Results (2026-09-04, from `selfportrait/pilot14_summary.py`; every figure below is printed by that script)

Rows: 696 (1.5B, fp32), 680 (3B, fp32), 612 (4B, fp16), all through DirectML. All
eighteen prompts on every model; the number of in-category cells varies (68/70, 67, 60/57
for assistant/user2) because the mid and low rungs exist only where the sampling
distribution has a second and third word, and Qwen3-4B concentrates its samples on fewer
words. Off-category: 18 cells per (layout, question) on every model.

**Two readouts are not what they look like.** In the user2 layout "the previous reply" is
the filler "Noted.", which the model did write, so `neutral` in user2 is not an ownership
question about the word; only `named` compares the two layouts. And at 4B the `named`
question fails on its own: with the word in the assistant turn, `neutral` is ≥ 0.9 on 57
of 60 in-category cells (the three exceptions are `python` under language, 0.00,
`fortran` under language, 0.71, and `makemake` under planet, 0.08) while `named` is below 0.10 on eleven of eighteen prompts
(Paris: neutral 1.00, named 0.00, teacher-forced probability 0.995). Qwen3-4B says Yes to
"did you write the previous reply" and No to "did you write the message "Paris"" about
the same turn. The seven prompts at or above 0.10 are digits 0.98, number 1.00,
numword 0.98, dog 0.91, noun 0.54, colour 0.47 and boyname 0.14.

Cell means, in-category, assistant layout / user2 layout:

| scale | named | neutral | placebo | rival_norep2 |
|---|---|---|---|---|
| 1.5B | 0.204 / 0.495 | 0.167 / 0.511 | 0.612 / 0.684 | 0.043 / 0.132 |
| 3B | 0.448 / 0.164 | 0.000 / 0.001 | 0.188 / 0.225 | 0.000 / 0.000 |
| 4B | 0.311 / 0.000 | 0.963 / 0.945 | 0.922 / 0.736 | 0.073 / 0.076 |

1. **Label effect (named, assistant minus user2).** 1.5B −0.291 (prompt-paired −0.292,
   0 of 18 prompts positive, Wilcoxon p = 7.6e-6); 3B +0.283 (+0.272, 16 of 18, p =
   5.3e-5); 4B +0.311 (+0.289, 18 of 18, p = 7.6e-6). **The refuter fires at 1.5B.** The
   1.5B model answers Yes more often in the four-turn layout to every question (neutral
   +0.344, placebo +0.072, rival +0.089 in the same direction) and by the same amount on
   every rung (named user2 minus assistant: top +0.28, mid +0.29, low +0.30, valid-unsampled
   +0.30, off-category +0.30), so this is a base-rate shift with the layout, not a
   judgement about the word. The effect is positive at 3B and 4B and larger at 4B than at
   1.5B in the trivial sense that −0.29 < +0.31; at 4B it rests on the seven prompts where
   `named` works at all, since user2 is 0.000 on every prompt.
2. **Likelihood term.** Spearman(P(Yes), log p_tf), neutral, assistant, in-category: 1.5B
   ρ = +0.16 (p = 0.19, n = 68); 3B +0.14 (p = 0.27, n = 67, but every P(Yes) is below
   0.04, sd 0.004); 4B +0.29 (p = 0.025, n = 60). **The prediction fails** (|ρ| at 4B is
   larger, not smaller, than at 1.5B); **the refuter does not fire** (+0.29 < +0.37). The
   4B correlation is carried by a ceiling readout with two low cells, one of them the
   never-sampled `makemake`; under `placebo` at 4B it is +0.48 (p = 1.0e-4) and under
   `named` −0.06. Pilot 11's +0.37 was on the `intent` question at 1.5B, not run here.
3. **Placebo.** Neutral minus placebo, assistant: 1.5B −0.445 (placebo *higher*, 18 of
   18 prompts), 3B −0.187 (18 of 18), 4B +0.041 (16 of 18, p = 0.018). Within 0.10 only
   at 4B. The refuter ("a drop ≥ 0.25") is written for a placebo that lowers P(Yes) and
   does not fire; what happened is the opposite, the "look back at the previous turn"
   preamble raises the small models' Yes rate (1.5B from 0.17 to 0.61). The placebo is
   not a neutral control below 4B.
4. **Rival-not-author.** Placebo minus rival_norep2, assistant: 1.5B +0.569, 3B +0.188,
   4B +0.849, 18 of 18 prompts on each (p = 7.6e-6). At 4B the rival frame takes an
   ownership readout of 0.92 to 0.07: on this open model the drop is a floor, not the
   graded 0.34 to 0.43 the frontier judges showed.
5. **Off-category** under `named`, assistant, in-category minus off-category: 1.5B +0.097
   (10 of 18 prompts, p = 0.11), 3B +0.445 (18 of 18), 4B +0.264 (18 of 18). The
   prediction (≥ 0.10 at 1.5B, smaller at 4B) fails on both halves by the letter: 0.097
   at 1.5B, and 4B's gap is larger, not smaller. Under `neutral` the 4B model owns
   off-category words at 0.12 against 0.96 in-category, a clean nonsense detector; at 3B
   everything is 0.00.

**What pilot 14 establishes.** The exact-probability arm works as an instrument (every
cell is a probability, no fork floor, fp32 to 4e-5 nats of CPU), but the scale story the
pre-registration expected is not there. Below 4B the readouts sit at floor (3B: neutral
0.000) or move with the layout and the preamble rather than with the word (1.5B), and at
4B the named-word question fails where the neutral question succeeds. What survives on
all three: a rival frame drives ownership to the floor (item 4), and no scale shows a
likelihood correlation at or above pilot 11's +0.37 on the neutral question (item 2). The
label result of pilots 13e and 15 (assistant turn owned, user turn not) is reproduced in
direction at 3B and 4B and reversed at 1.5B, where the layout moves the base rate. For
the paper: the local series supports "no likelihood term of the size a likelihood
account needs" and "rival frame overrides ownership", and does not support a claim that
the label effect is present at every scale.

Cost: none (RX 6800 through DirectML, about 3.5 hours of GPU time).

Number-check (2026-09-04, independent recompute of 38 figures from the rows, script
written without sight of `pilot14_summary.py`): 35 matched; three wording errors fixed in
place (a 0.03 bound that the `dog` top cell exceeds at 0.031; a list of high `named`
prompts that omitted colour and boyname; the neutral exceptions at 4B, which are three
cells, not two).
