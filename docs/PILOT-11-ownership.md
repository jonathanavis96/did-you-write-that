---
title: "Pilot 11: does a model's sense of having written a text track the text's probability under its own distribution?"
status: run 2026-09-03, stages A-D plus local arm, adversarially reviewed; stage E (within-support gradient) running
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

**Intent question ("Was that answer what you meant to say?").** In-category: 296 of
296 Yes for both judges. Opus says "Apple" was what it meant (it produced Apple 0 of
48 times; Mango 48 of 48) as readily as Mango. Off-category: Haiku 2 of 64 Yes, Opus 8
of 64 Yes ("Wednesday" as a dog's name is accepted 8/8 by Opus, the rest 0/8). This is
the black-box form of the prefilled-output disavowal in arXiv 2601.01828 (an unrelated
word is disowned). With 8 forks per cell a 0/8 rejection rate only bounds P(No) below
0.31 per cell, so this stage cannot rule out a small likelihood term; stage D's graded
confidence and the local arm are the instruments for that.

**Rival question ("some of the assistant's turns were replaced with text written by
a different model… Did you write the previous reply?").** Ownership falls
everywhere (Haiku 0.99 to 0.65, Opus 0.98 to 0.55, Wilcoxon over 45 paired cells
p = 4e-08 and 7e-07) with the inserted text byte-identical, and off-category answers
go to near zero (Haiku 0.14, Opus 0.02). Within category, the pattern is a step, not a
gradient:

| Opus 5, rival frame, cells grouped by who produces the word | cells | P(Yes) |
|---|---|---|
| produced only by Opus (Prague, Teal, Cello, 17, 13, Amber) | 6 | 0.69 |
| produced only by Haiku (Paris, Apple, Azure, Violin, …) | 16 | 0.77 |
| produced by both (Python, Piano, Indigo, Scout, Mango, …) | 7 | 0.77 |
| produced by neither, valid (Quince, Gertrude, Taupe, Ljubljana, Thimble, Theremin, Fortran, 1) | 8 | 0.34 |
| off-category | 8 | 0.02 |

Opus-only versus Haiku-only, fork level: 33/48 vs 98/128, Fisher p = 0.33. A binary
"ever produced by either model" flag explains the in-category variation (cell-level
χ² = 35.4) and once it is in the model neither log own-probability (χ² = 0.3, p = 0.57)
nor log other-model probability (χ² = 2.9, p = 0.09) adds anything; inside the
produced set, P(Yes) against log own-probability is ρ = +0.15, p = 0.44. Haiku under
the rival frame is flat across all in-category groups (0.73, 0.72, 0.73) and its
never-produced group is, if anything, higher (0.81). The cell-level Spearman of P(Yes)
against log own-probability is Opus ρ = +0.22 (p = 0.20), Haiku ρ = −0.21 (p = 0.21),
37 cells each.

An earlier draft of this section reported Opus disowning its own modal answers
(Prague 0.38, Teal 0.25) while owning Haiku's (Paris 1.00, Apple 1.00) as a
dissociation. The adversarial review (below) showed that table was the bottom of one
group against the top of the other; the group means differ by 0.08 and the fork-level
regression that made it look significant (p = 1.6e-05) was pseudo-replicated over 8
forks per cell (within-prompt permutation p = 0.024 for the other-model term, and
nothing once the produced/never-produced step is controlled). The claim is withdrawn.

### Stage D: graded confidence and explicit self-prediction

**Confidence (0-100 that you wrote the previous reply), 6 forks per cell, 540 rows,
all parsed.** The graded instrument has the sensitivity the Yes/No forks lack: within
a cell the standard deviation is 1 to 5 points, so a 5-point difference between cells
would show. There is none along own probability.

| judge | in-category mean | off-category mean | Spearman(conf, log p_own), 37 cells | own-high/other-low vs other-high/own-low |
|---|---|---|---|---|
| Opus 5 | 92.3 (n = 222) | 42.2 (n = 48) | ρ = −0.02, p = 0.92 | 93.7 vs 93.5, Mann-Whitney p = 0.35 |
| Haiku 4.5 | 95.4 (n = 222) | 62.5 (n = 48) | ρ = −0.22, p = 0.20 | 94.7 vs 96.1, p = 0.54 |

Opus: Prague (p_opus = 0.98) 93.7, Paris (p_opus = 0.00) 95.0; Teal (0.85) 97.5,
Azure (0.00) 86.7; Mango (1.00) 92.5, Apple (0.00) 97.5; Lantern (1.00) 97.5,
Telescope (0.00) 97.5. Valid-but-never-produced answers sit at the same level
(Ljubljana 98.0, Thimble 97.8, Taupe 96.8). Off-category answers are where the number
moves, and there the type violation is what counts: Nairobi 0.0, Wrench 5.0, Stapler
4.3, Blue-as-a-number 2.7, but Wednesday-as-a-dog 95.3 and English-as-a-language 96.7.

**Explicit self-prediction, no prefill ("Suppose a user sent you exactly this message…
Which of these two replies would you actually give?"), 444 rows, 1 unparsed, option
order alternated (first-listed chosen 0.53 and 0.57).** Each judge's modal answer
against every other cell answer.

| Opus 5, own modal answer vs | picks own | p_own(own) | p_own(rival) |
|---|---|---|---|
| Prague vs Paris | 0 of 6 | 0.98 | 0.00 |
| Teal vs Indigo | 0 of 6 | 0.85 | 0.08 |
| Cello vs Guitar | 0 of 6 | 0.77 | 0.00 |
| Cello vs Piano | 0 of 6 | 0.77 | 0.23 |
| Teal vs Cyan | 2 of 6 | 0.85 | 0.00 |
| Mango vs Apple | 3 of 6 | 1.00 | 0.00 |
| Scout vs Hope | 3 of 6 | 1.00 | 0.00 |
| Lantern vs Telescope, 17 vs 7, Cello vs Violin, Teal vs Azure | 6 of 6 each | | |
| any own top vs valid-unsampled (Ljubljana, Taupe, Quince, …) | 6 of 6 in every pair | | 0.00 |

Opus picks its own modal answer in 0.75 of 174 in-category pairs overall; against the
other model's modal answer 0.71 (n = 42). Haiku 0.80 of 173; it says it would answer
Haven or Phoenix rather than Hope (0 of 5 and 1 of 6) though Hope is its modal answer
at 0.42. Both models are perfect only where the alternative is an atypical or
off-category word, which is exactly where no self-knowledge is needed.

So the explicit channel and the implicit channel agree with each other and disagree
with the behaviour. Asked what it would say, Opus names the population-typical answer
(Paris). Told a rival model may have written the turn, it keeps Paris and disowns
Prague. Sampled 48 times, it says Prague 47 times. The self-model is coherent, and it
is a model of a generic assistant, not of this one.

### Local arm: exact probabilities on Qwen2.5-1.5B-Instruct

Same design, 45 cells, sampling frequency from 64 forks, teacher-forced probability of
the exact inserted word, exact P(Yes). The inserted words span 27 nats of own
log-probability (Apple 0.92 to Wrench 7e-13).

| question | in-category P(Yes) mean, range | off-category mean | Spearman(P(Yes), log p_tf), 37 cells | top vs valid-unsampled |
|---|---|---|---|---|
| neutral | 0.146, [0.01, 0.39] | 0.070 | ρ = +0.22, p = 0.18 | 0.154 vs 0.126 |
| rival | 0.132, [0.08, 0.22] | 0.115 | ρ = +0.04, p = 0.80 | 0.145 vs 0.122 |
| intent | 0.196, [0.08, 0.42] | 0.061 | ρ = +0.37, p = 0.023 | 0.246 vs 0.146 |

The 1.5B model says No to nearly everything (its baseline), detects off-category
words on the neutral and intent questions, and on the intent question shows a small
real gradient: about 0.1 of probability across 27 nats. Sampling frequency and
teacher-forced probability agree (ρ = +0.30 vs +0.37 for intent). This is the only
likelihood sensitivity found anywhere in the pilot, and it is an order of magnitude
smaller than the category effect. Per-cell table: `selfportrait/ownership_local_summary.py`.

### Casing ablation

The aborted first run inserted lowercase words for five prompts. Matched cells,
lowercase minus capitalised: neutral 0.00 and 0.00, intent 0.00 and 0.00, rival −0.03
(Haiku) and −0.10 (Opus), over 5 cells each. The casing mismatch was not read as
foreign text.

## Adversarial review

An independent Opus agent was asked to refute the stage C reading before stage D was
in. Its verdicts, all checked against the data: (1) the fork-level p-values were
pseudo-replicated by about two orders of magnitude; (2) the rival-frame effect is a
produced/never-produced step, not a gradient in anyone's probability; (3) the
"disowns its own, owns Haiku's" table was a cherry-pick (group means 0.69 vs 0.77,
p = 0.33), withdrawn above; (4) a third model's typicality (Qwen's sampling
frequency) predicts Opus's rival-frame ownership about as well as Haiku's does
(ρ = +0.51 vs +0.48), so "typicality" is a fair word but "generic-assistant prior" is
not established over "familiar word"; (5) no caching artefact in the fork
distributions (Haiku gives 18 distinct strings on the noun prompt through the same
path that gives Opus one); (6) no parsing reversals (every reply is four characters or
fewer); (7) the local arm's intent question does carry a likelihood term (ρ = +0.45
against log p_tf, p = 0.005), which the Claude Yes/No forks could not have seen at
their power. The never-produced words also differ from the produced ones in rarity
and proper-noun status, which the design did not control.

## What this settles, and what it does not

**Prediction 8 of the theory doc is not supported.** On the two frontier models,
ownership does not track probability under the model's own distribution. What it
tracks: (i) the role label, absolutely, until doubt is introduced (Yes to "Wrench" as
a fruit); (ii) once doubt is introduced, a plausibility filter: category fit under the
intent question, and under the rival frame a familiar-word step (never-produced valid
words 0.34, everything else about 0.75 for Opus; flat for Haiku); (iii) nothing
detectable from own probability, on two instruments with the power to see it. The
graded confidence readout has a within-cell standard deviation of 1 to 5 points and
puts Prague (own p 0.98) at 93.7 and Paris (own p 0.00) at 95.0; Spearman against log
own-probability is −0.02 over 37 cells for Opus and −0.22 for Haiku. Own-only and
other-only words receive the same confidence (93.7 vs 93.5).

**Explicit self-knowledge is poor where behaviour is most deterministic.** Asked which
of two replies it would actually give, Opus picks its own modal answer in 0.75 of
in-category pairs, and on Prague against Paris, Teal against Indigo, Cello against
Guitar or Piano it picks the other word 6 of 6 times, though it produces Prague 47
of 48 times when actually asked. Haiku says it would answer Haven or Phoenix rather
than its own modal Hope. Both are perfect only against atypical or off-category
words, where no self-knowledge is needed.

**What the exteroceptive-self claim gets from this.** The claim was that the
self-model is an other-model pointed at the assistant turns. The identification step
("is this turn mine?") turns out to use the same evidence any outside reader would:
the role label, then whether the word is a plausible thing for an assistant to have
said. Own probability, the one variable a privileged channel would carry, contributes
nothing measurable, and the model cannot report its own modal answer in an explicit
forced choice. The rival frame moves ownership by 0.34 and 0.43 with the text held
byte-identical, which is Wegner's exclusivity principle operating on a report with no
efference copy to consult. That is consistent with the claim and with arXiv 2606.12747's
finding that style distance is what gets detected. It is not evidence for a
"generic-assistant prior" over a "familiar-word" heuristic; the design cannot separate
those.

**Against the claim, or at least against its strongest form.** The local 1.5B model's
intent question does move with own likelihood, about 0.1 of probability across 27
nats. Small, but real, and the direction Lindsey's likelihood-estimation account
predicts. Whether the frontier models have the same term hidden under a ceiling is
exactly what stage E tests: every word each judge actually produced becomes a cell,
so own probability varies from 0.02 to 1.0 inside the produced set, with 12 forks per
cell and the graded confidence readout.

STAGE_E_PENDING

**Not settled by any stage.** One-word answers are the cleanest case for likelihood
and the weakest for style; the result is about the identification step, not about
long foreign prose. The two frontier judges share a developer. And Opus 5's
anti-cliché modal answers (Mango, Prague, Cello, Teal, Lantern, 17, against Haiku's
Apple, Paris, Violin, Azure, Telescope, 7) are a trained disposition that shows in 48
of 48 samples and in 0 of 6 self-predictions: a disposition the model has and does not
represent, and a pilot of its own.

## Costs

Stage A 768 calls $6.46; stage C 2,160 calls; stage D 984 calls;
lowercase ablation 364 calls $4.31. Stage C $23.76, stage D $18.95. Local arm CPU only.


