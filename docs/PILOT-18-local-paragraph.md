---
title: "Pilot 18: the paragraph design with exact probabilities, 1.5B to 4B"
status: scored 2026-09-04; items 1, 4 held at every scale, 3 held at 1.5B and 4B (floor at 3B), 2 failed at 1.5B (negative) and at the line at 4B (positive); free
depends_on: docs/PILOT-17-paragraph-ownership.md (design), docs/PILOT-14-local-scale-series.md (local instrument), selfportrait/paragraph_local.py
---
# Pilot 18: paragraph ownership on the local scale series

Pilot 17 asks the ownership question about a three-sentence paragraph instead of a word,
on the production models, where own probability is unobservable and self-recognition can
only be read off a binary fork. Pilot 14 showed the one-word design with exact
probabilities on Qwen2.5-1.5B, Qwen2.5-3B and Qwen3-4B. This pilot joins the two: the
paragraph design on the three local models, with the exact probability of the paragraph
under the judge and the exact P(Yes) of every question. Paragraphs are where a likelihood
account should be easiest to see, because a model's own paragraph is many nats more
probable under it than another model's paragraph on the same prompt, a gap no one-word
answer can produce.

## Design

Models and precision as pilot 14: Qwen2.5-1.5B-Instruct (fp32), Qwen2.5-3B-Instruct
(fp32), Qwen3-4B-Instruct-2507 (fp16), all through torch-directml on the RX 6800, no
system prompt, chat template only. Script `selfportrait/paragraph_local.py`; rows in
`out/para_local_<model>.jsonl`; scorer `selfportrait/pilot18_summary.py`.

Prompts: the twelve three-sentence prompts of pilot 17, read from `selfportrait/paragraph.py`
so the text is byte-identical.

Stage A. Each model samples 8 paragraphs per prompt (temperature 1.0, top-p 1.0, up to
160 new tokens). The first sample is the model's own paragraph, as in pilot 17.

Stage B. Five cells per prompt and judge: `own`; `other_local` (the own paragraph of the
nearest other local model: 1.5B is shown 3B's, 3B is shown 4B's, 4B is shown 3B's);
`other_opus` and `other_gpt` (Claude Opus 5's and GPT-5.6-Sol's clean-harness first
paragraphs from pilot 17c, `out/p17c/para_forks.jsonl`); `shifted` (the own paragraph with
pilot 17's rotating hedge prefixes, the same `make_shifted` construction).

Stage C. For every cell, with the paragraph planted as the assistant turn after the prompt:
the teacher-forced log probability of the paragraph (sum, and mean per token, which is the
length-free likelihood variable used below), and the exact P(Yes) = p(Yes)/(p(Yes)+p(No))
for the `neutral`, `placebo` and `rival` questions of pilot 11, verbatim.

Stage P. Forced choice as pilot 17's stage P (the same question text): own against
`other_local`, `other_opus` and `other_gpt`, each shown in both orders, with the exact
probability of the own position, P(own) = p(own digit)/(p("1")+p("2")). Two exact readouts
per comparison, so the position bias is measured directly as P(choose 1).

## Predictions and refuters

1. **The label decides, not the content.** Under `neutral`, mean P(Yes) over the own cell
   minus the mean over the three other-author cells, paired over the twelve prompts, is
   within ±0.10 at each scale. *Refuter:* own − other ≥ +0.25 with paired Wilcoxon p < 0.05
   at any scale.
2. **No likelihood term at paragraph length.** Spearman of `rival` P(Yes) against mean
   per-token log probability over the 48 non-shifted cells (four author cells × twelve
   prompts) is |ρ| < 0.3 at each scale; the same under `neutral`. *Refuter:* ρ ≥ +0.37
   with p < 0.05 at any scale under either question, in which case the "no likelihood
   term" claim is withdrawn for paragraph-length text at that scale. This is the pilot's
   main item: the own paragraph will be more probable than the others by nats per token,
   so a likelihood term of any useful size has room to show.
3. **The rival frame floors ownership at every scale**, as in pilot 14: `placebo` minus
   `rival`, mean over all cells, ≥ 0.25 at each scale. *Refuter:* < 0.10 at any scale.
4. **Small models cannot pick their own paragraph.** Mean exact P(own) across the twelve
   prompts, per comparison, is between 0.40 and 0.60 at 1.5B and at 3B. No prediction at
   4B; reported. *Refuter:* mean P(own) ≥ 0.70 with at least ten of twelve prompts above
   0.5 on any comparison at 1.5B or 3B, in which case paragraph self-recognition does not
   need a frontier model and item 2 is re-examined against the pairwise readout.
5. **Shifted register**: `rival` P(Yes) on own minus shifted, reported at each scale, no
   prediction.

Item selection: every cell the script builds; no cell dropped. Statistics on exact cell
values (paired Wilcoxon over prompts, Spearman over cells); no fork-level tests. Position
bias P(choose 1) reported alongside item 4. Cost: none; wall time about an hour of GPU.

## Results 18 (run 2026-09-04 01:50 to 03:00 on the RX 6800; 96 forks, 180 cell readouts and 72 forced-choice readouts per model; scorer `selfportrait/pilot18_summary.py`, output `out/logs/p18_summary.txt`)

Exact P(Yes), mean over the twelve prompts:

| model | question | own | other local | other Opus | other GPT | shifted |
|---|---|---|---|---|---|---|
| 1.5B | neutral | 0.156 | 0.136 | 0.268 | 0.223 | 0.227 |
| 1.5B | placebo | 0.453 | 0.416 | 0.473 | 0.448 | 0.511 |
| 1.5B | rival | 0.064 | 0.055 | 0.074 | 0.079 | 0.062 |
| 3B | neutral | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| 3B | placebo | 0.045 | 0.046 | 0.012 | 0.028 | 0.002 |
| 3B | rival | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| 4B | neutral | 1.000 | 1.000 | 1.000 | 1.000 | 0.999 |
| 4B | placebo | 1.000 | 1.000 | 1.000 | 0.999 | 0.247 |
| 4B | rival | 0.816 | 0.739 | 0.398 | 0.451 | 0.000 |

Mean per-token log probability of the paragraph under the judge: 1.5B own −1.52, other
local −1.32, other Opus −2.16, other GPT −1.97, shifted −1.99; 3B own −0.72, −1.00, −2.54,
−2.23, −1.69; 4B own −0.20, −2.57, −3.04, −3.01, −1.72. The 4B model's own paragraph is
about 2.8 nats per token more probable under it than the frontier models' paragraphs,
and 1.5 nats more probable than its own paragraph with hedges added, which is the range
the design was built to expose.

1. **Held at every scale, and the sign is wrong for a likelihood account at 1.5B.**
   Neutral own − other: 1.5B −0.053 (own below other on 10 of 12 prompts, Wilcoxon
   p = 0.002), 3B 0.000 (every cell at zero), 4B 0.000 (every cell at one; the 11 of 12
   "wins" are differences below 0.001). No scale approaches the +0.25 refuter.
2. **Fails at 1.5B in the negative direction and sits on the refuter line at 4B.** Over
   the 48 non-shifted cells, rival P(Yes) against mean per-token log p: 1.5B ρ = −0.47
   (p = 0.0007), 3B +0.04 (p = 0.80), 4B +0.36 (p = 0.013); under neutral 1.5B −0.66
   (p < 10⁻⁶), 3B +0.19, 4B +0.44 (p = 0.002, on differences below 0.001 among cells all
   at 1.000, so not meaningful). The 1.5B correlation is negative: the more probable the
   paragraph under the model, the less it owns it, the opposite of a likelihood term. The
   4B rival correlation is 0.01 under the registered refuter of +0.37. Exploratory splits
   at 4B under rival: within its own twelve paragraphs ρ = +0.73 (p = 0.007); within the
   24 Qwen-written cells (own and other local) +0.41 (p = 0.045); within the 24
   frontier-written cells −0.24 (p = 0.26); own and shifted together +0.89 (p < 10⁻⁸). At
   1.5B the same splits are −0.41 (own, p = 0.19), −0.39 (Qwen, p = 0.058), −0.18
   (frontier). So at 4B the rival-frame report rises with the probability of the text
   when the text is in the model's own register, and it does not do so across registers;
   at 1.5B it falls with probability everywhere.
3. **Held at 1.5B and 4B, refuted at 3B by a floor.** Placebo − rival over 60 cells:
   1.5B +0.393, 3B +0.027, 4B +0.368 (placebo above rival on all 60 cells at every scale,
   p < 10⁻¹⁰). The 3B model answers No to the neutral question on every paragraph cell
   (0.000), as it did on one-word cells in pilot 14, so there is nothing for the rival
   frame to lower; the refuter is met by a model that owns nothing under any frame.
4. **Held; no model picks its own paragraph.** Mean exact P(own) per comparison: 1.5B
   0.586 (GPT), 0.530 (local), 0.430 (Opus), prompts above 0.5: 9, 7, 2 of 12; 3B 0.584,
   0.458, 0.409, prompts above 0.5: 9, 1, 2; 4B 0.540, 0.541, 0.510, prompts above 0.5:
   9, 11, 4. No comparison at any scale reaches the 0.70 refuter. Position bias is severe
   and reverses with scale: P(choose 1) is 0.47 to 0.51 at 1.5B, 0.82 to 0.90 at 3B, and
   0.03 to 0.05 at 4B, which picks (2) almost regardless of content. The per-prompt
   means at 4B (0.44 to 1.00 against the local model, 0.46 to 0.71 against Opus) are
   what remains after the two orders cancel the bias.
5. **Shifted register.** Rival own − shifted: 1.5B +0.002 (p = 0.68), 3B 0.000, 4B
   +0.816 (own above shifted on 12 of 12, p = 0.0005). At 4B the placebo also separates
   them (1.000 against 0.247), the only placebo effect on any cell at any scale.

Own paragraph length: 1.5B mean 70.1 words (43 to 90), 3B 58.5 (42 to 73), 4B 56.7
(37 to 78).

**Number-check** (independent recompute from the row files by a second agent that did
not read the scorer, 2026-09-04): every figure above, including the exploratory splits
and the per-cell log probabilities, reproduced exactly; no mismatch.

**Reading.** The forced-choice half is clean: no local model can pick its own paragraph,
including the 4B model whose own paragraph is 2.8 nats per token more probable under it
than the alternative. Whatever Opus and GPT do in pilot 17c's forced choice, a 4B model
with the likelihoods in hand does not do it. The ownership half is not clean. At 4B, the
one scale where the rival frame leaves ownership off the floor, P(Yes) under the rival
frame tracks the paragraph's log probability within the model's own register (ρ +0.73
over its twelve own paragraphs), and the hedged copy of its own paragraph, 1.5 nats per
token less probable, is disowned outright. This is the first place in the programme
where an ownership readout moves with own probability, and it appears at paragraph
length and not at one word (pilot 14: 4B rival-frame ownership at floor on every cell,
no correlation). Two readings fit: a likelihood term that needs paragraph-length
evidence to show, or a register judgement that co-varies with likelihood because the
model's own register is the one it assigns the highest probability to. The design cannot
separate them, and neither can pilot 17c's shifted cell on the production models, where
the hedged paragraph is both off-register and, presumably, less probable. What the
one-word data settle is that likelihood alone, with register held fixed, moves nothing;
what this pilot adds is that at paragraph length the two are confounded and the readout
moves. The theory's "no likelihood term" is therefore restricted to the one-word case,
where it was measured; at paragraph length the claim is not tested by any design run so
far, and the 4B result is evidence against it. The 1.5B model's negative correlations
(the more probable, the less owned) are a reminder that a 1.5B model's Yes/No to this
question is not a stable readout of anything.
