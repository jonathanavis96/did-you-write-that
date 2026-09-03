---
title: "Pilot 18: the paragraph design with exact probabilities, 1.5B to 4B"
status: pre-registered 2026-09-04 (this file committed before the run); free
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

Results 18: PENDING.
