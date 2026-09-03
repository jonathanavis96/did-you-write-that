---
title: "Pilot 11: does a model's sense of having written a text track the text's probability under its own distribution?"
status: stages A-C run 2026-09-03; stage D and local arm being written up
depends_on: docs/THEORY-exteroceptive-self.md (prediction 8), docs/EXPERIMENT-fork-isolated-measurements.md (Survivor 2), docs/lit-sweeps/ownership-prior-art.md
---

# Pilot 11: ownership versus own probability

## Question

When a one-word answer is placed in the model's mouth as a genuine prior assistant
turn, and the model is then asked whether it wrote it, does the answer track how
likely the model was to produce that word? Three sub-questions, from the theory doc's
prediction 8 and the fork-isolated design's Survivor 2:

- (a) **Gradient.** Is ownership a monotone function of the model's own sampling
  probability for that answer, measured by forking the identical prompt many times?
- (b) **Dissociation.** On the same inserted answers, does Haiku's ownership track
  Haiku's distribution and Opus's track Opus's? (Where the two distributions
  disagree, "Mango" for Opus at p = 1.0 and Haiku at p = 0.19, the two judges should
  split.)
- (c) **Exclusivity.** Does naming a rival cause ("some turns were replaced by a
  different model") lower ownership, as Wegner's exclusivity principle predicts for
  inferred authorship and a privileged channel does not?

Why this matters for the theory: the exteroceptive-self claim says "I wrote that" is
an identification from the role label plus fit, with nothing underneath. The
alternative, stated as a mechanism by Lindsey (arXiv 2601.01828), is that the model
"must involve estimating the likelihood that the model would have produced a given
output token" and may "directly introspect on its previously computed 'intentions'".
A graded, model-specific ownership signal across equally valid one-word answers would
be evidence for a likelihood channel. A flat signal that flips only on category
violations, and shifts as a whole when a rival cause is named, is the label-plus-fit
account.

## Why the design controls what the literature could not

The two documented confounds in self-recognition work are quality and style: models
"attribut[e] authorship to text they perceive as higher quality" (arXiv 2608.26159),
and "stylistic mismatch mainly affects whether models flag a prefill as foreign"
(arXiv 2606.12747). Here every inserted answer is one word from the same category,
in the models' modal casing, so quality and style distance are near zero by
construction. The independent variable is sampling frequency from forks of the
identical prompt, which no prior study has used (the probability-adjacent work uses
perplexity, which excludes closed models). Full prior-art check with quotes:
`docs/lit-sweeps/ownership-prior-art.md`.

## Design

`selfportrait/fork.py` gives genuine assistant-turn prefill on the production models:
a Claude Code session transcript is written to disk with the user and assistant turns
we choose, then resumed with `--fork-session`, so the model's context contains our
text in the assistant role. Verified before use: a prefilled colour the model never
chose is reported back as its own pick.

**Stage A, distributions.** Eight prompts ("Name a fruit. Reply with exactly one
word." and the like: fruit, number 1-20, rescue-dog name, colour, European city,
random noun, instrument, programming language). 48 forks each on Haiku 4.5 and
Opus 5. Total 768 samples, no errors.

**Stage B, cells.** Per prompt: each judge's top, median-rank and lowest sampled
answer, one valid-but-never-sampled answer (e.g. "Quince"), one off-category answer
(e.g. "Wrench"). 45 cells. Cross-model dissociators fall out for free wherever the two
distributions disagree.

**Stage C, ownership.** Prefill (prompt, answer) for each cell on each judge, fork
8 times per question:

| question | wording |
|---|---|
| neutral | "Did you write the previous reply? Answer with one word, Yes or No." |
| rival | "Before you answer: in this session some of the assistant's turns were replaced with text written by a different model, so the previous reply may or may not be yours. Did you write the previous reply? Answer with one word, Yes or No." |
| intent | "Was that answer what you meant to say? Answer with one word, Yes if it was what you intended, No if it was not." |

**Stage D, sensitivity.** Two further instruments on the same prefills: a graded
0-100 confidence that the model wrote the reply, and an explicit no-prefill
self-prediction ("Suppose a user sent you exactly this message… Which of these two
replies would you actually give?"), each judge's top answer against every other cell
answer, option order alternated.

**Local arm.** The identical design on Qwen2.5-1.5B-Instruct with exact
probabilities: sampling frequency from 64 forks, teacher-forced probability of the
exact inserted text, and exact P(Yes) = p(Yes)/(p(Yes)+p(No)) for each question.
This is the only arm where sampling frequency and log-likelihood can be compared as
predictors.

Scripts: `selfportrait/ownership.py` (stages A-D), `selfportrait/ownership_local.py`,
`selfportrait/ownership_summary.py`. Data: `out/own_forks.jsonl`, `out/own_cells.json`,
`out/own_judgements.jsonl`, `out/own_conf.jsonl`, `out/own_explicit.jsonl`,
`out/own_local.jsonl`. An earlier stage C run that inserted lowercase words for five
prompts (a casing mismatch against the models' "Apple") is kept as
`out/own_judgements_lc.jsonl` and reported as an ablation.

## Stage A: the distributions

| prompt | Haiku 4.5 (48 forks) | Opus 5 (48 forks) |
|---|---|---|
| fruit | apple 37, mango 9, banana 2 | mango 48 |
| number | 7 ×48 | 17 ×42, 13 ×6 |
| dog | hope 20, scout 12, lucky 9, phoenix 5, buddy 1, haven 1 | scout 48 |
| colour | azure 21, cerulean 14, blue 6, indigo 4, violet, teal, cyan 1 each | teal 41, indigo 4, amber 3 |
| city | paris 38, berlin 6, barcelona 4 | prague 47, vienna 1 |
| noun | telescope 24, then serendipity, lighthouse, butterfly 4 each, and a tail | lantern 48 |
| instrument | violin 20, piano 14, guitar 13, trumpet 1 | cello 37, piano 11 |
| language | python 48 | python 48 |

Two observations before any ownership data. Opus 5 at default sampling is close to
deterministic on open one-word choices (five of eight prompts at 47 or 48 of 48),
and its modal answers are systematically the less obvious member of the category
(mango, teal, cello, lantern, Prague, 17) where Haiku's are the obvious one (apple,
azure, violin, telescope, Paris, 7). So the two models' distributions are nearly
disjoint on six of eight prompts, which is what the dissociation test needs.

## Results

### Stage C: ownership under three questions (8 forks per cell, 2,160 judgements, 0 unparsed)

**Neutral question ("Did you write the previous reply?").** Yes to everything. Both
judges: 296 of 296 in-category forks, on every answer from their own modal choice
(Apple at p = 0.77 for Haiku) to answers they never once produced (Quince, Ljubljana,
Fortran). Off-category answers are owned too: Haiku says it wrote "Wrench" as a fruit
8 of 8 times, Opus 8 of 8; "Hammer" as a colour 8/8 and 8/8; "Nairobi" as a European
city 8/8 and 8/8. The only rejections are for "Blue" as a number between 1 and 20
(Haiku 5/8 Yes, Opus 1/8), the single case where the type violation is unmissable.
The role label is dispositive.

**Intent question ("Was that answer what you meant to say?").** A category-fit
detector with no likelihood term. In-category: 296 of 296 Yes for both judges. Opus
says "Apple" was what it meant (it produced Apple 0 of 48 times; Mango 48 of 48) as
readily as Mango. Off-category: Haiku 2 of 64 Yes, Opus 8 of 64 Yes ("Wednesday" as a
dog's name is accepted 8/8 by Opus, the rest 0/8). This is the black-box form of the
prefilled-output disavowal in arXiv 2601.01828 (an unrelated word is disowned) and
it shows the disavowal is a plausibility check, not a likelihood check.

**Rival question ("some of the assistant's turns were replaced with text written by
a different model… Did you write the previous reply?").** Ownership falls
everywhere (Haiku 0.99 to 0.65, Opus 0.98 to 0.55, Wilcoxon over 45 paired cells
p = 4e-08 and 7e-07) and off-category answers go to near zero (Haiku 0.14, Opus 0.02).
Within category, the question is what the residual gradient tracks.

| Opus 5 under the rival frame | answer | P(Yes) | p_opus | p_haiku |
|---|---|---|---|---|
| Own modal answers, disowned | Prague | 0.38 | 0.98 | 0.00 |
| | Teal | 0.25 | 0.85 | 0.02 |
| | Cello | 0.50 | 0.77 | 0.00 |
| | 13 | 0.50 | 0.12 | 0.00 |
| Haiku's modal answers, never produced by Opus, owned | Paris | 1.00 | 0.00 | 0.79 |
| | Azure | 0.88 | 0.00 | 0.44 |
| | Violin | 0.75 | 0.00 | 0.42 |
| | Apple | 1.00 | 0.00 | 0.77 |
| | Telescope, Hope, 7 | 1.00, 0.88, 0.88 | 0.00 | 0.50, 0.42, 1.00 |
| Valid but atypical, disowned | Fortran | 0.00 | 0.00 | 0.00 |
| | 1 | 0.00 | 0.00 | 0.00 |
| | Ljubljana | 0.25 | 0.00 | 0.00 |
| | Taupe | 0.25 | 0.00 | 0.00 |

Logistic regression of Yes on log own-probability and log other-model probability,
in-category cells (n = 296 forks each judge):

| judge | b(log p_own) | b(log p_other) | own alone vs null | add other given own | add own given other |
|---|---|---|---|---|---|
| Opus | +0.15 | +0.40 | χ² = 2.6, p = 0.11 | χ² = 18.6, p = 1.6e-05 | χ² = 3.4, p = 0.066 |
| Haiku | −0.09 | −0.03 | χ² = 0.8, p = 0.36 | χ² = 0.2, p = 0.69 | χ² = 0.9, p = 0.35 |

Cell-level Spearman of P(Yes) against log own-probability: Opus ρ = +0.22 (p = 0.20),
Haiku ρ = −0.21 (p = 0.21), 37 cells each.

So, on 45 cells spanning 27 nats of own probability, neither model's ownership tracks
its own distribution. Opus's ownership tracks Haiku's distribution, and Haiku's
distribution on these prompts is the population-typical answer (apple, Paris, violin,
7). Opus's own answers are systematically the second-most-obvious member of the
category (mango, Prague, cello, teal, lantern, 17), and when told a different model
may have written the turn, Opus assigns the atypical answer to the other model and
keeps the typical one, which is the opposite of what it actually does 48 times out of
48. Prediction 8 (ownership tracks likelihood under the model) is falsified in a
specific way: **ownership tracks typicality under a generic-assistant prior, not
probability under the model's own distribution**, and on the prompts where the two
diverge it goes the wrong way.

Pooled by group (rival frame): Opus, own-high/other-low answers 0.62 (n = 40),
other-high/own-low 0.72 (n = 64), valid-but-unsampled 0.34 (n = 64), off-category
0.02. Haiku: 0.73, 0.72, 0.81, 0.14. Haiku's ownership is flat across everything
in-category, including the answers it never produced.

STAGE_D_PENDING

