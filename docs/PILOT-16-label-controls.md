---
title: "Pilot 16: controls the skeptic asked for on the role-label result"
status: complete 2026-09-03; the text was on disk before launch, the commit landed a few minutes after launch because a lint hook rejected the first commit attempt
depends_on: docs/PILOT-13-ownership-gpt.md (13e and its skeptic pass), selfportrait/ownership.py
---
# Pilot 16: turn-matched, filler, tool-label and graded controls

The skeptic pass on 13e ranked what is missing before "the label decides" can be quoted:
the two compared layouts differ in turn count and filler as well as in the word's role;
the binary readout sits at a rail in both layouts so no second variable can show; Opus ran
4 forks; and no third label was tried. This pilot supplies each, on the same 45 pilot 11
cells (37 in-category, 8 off-category), verified by listing probes on Haiku for every new
layout and on Opus for the user2 layout.

## Conditions (question in brackets; rows stored as `<question>_<layout>`)

| id | layout | turns | question |
|---|---|---|---|
| A | assistant (13e) | user prompt / assistant WORD | named |
| U | user2 (13e) | user prompt / assistant "You go first." / user WORD / assistant "Noted." | named |
| A4 | assist4 | user prompt / assistant "You go first." / user "No, you go first." / assistant WORD | named |
| F | user2 | as U | named_filler: `Did you write the message "Noted." …` |
| T | tool | user prompt / assistant Bash `cat answer.txt` / tool result WORD / assistant "Noted." | named |
| Ac, Uc | assistant, user2 | as A, U | named_conf (0 to 100) |
| Ar, Ur | assistant, user2 | as A, U | rival_named (rival preamble plus the named question) |

Haiku 4.5: every condition at 8 forks. Opus 5: U and A topped up from 4 to 8 forks; A4,
Ac, Uc at 4 forks; F, T, Ar, Ur not run on Opus (cost). Fable: not run. Opus stays at
default effort; the 13e effort confound with Fable stays open and is recorded as such.

## Predictions and refuters

1. **A4 ≥ 0.90 in category** on both judges. *Refuter:* A4 < 0.75, in which case the
   13e contrast is about turn structure, not the label, and the 13e reading is withdrawn.
2. **F ≥ 0.90**: the model owns the filler assistant turn it never generated, on the same
   sessions where it denies the user-turn word. *Refuter:* F ≤ 0.50.
3. **T ≤ 0.10** in category (Haiku): a tool-result label is not owned either.
4. **Graded readout.** Ac cell means ≥ 80 and Uc cell means ≤ 20 on average. Within each
   layout, on the cells whose mean lies in [15, 85] (pre-specified: if fewer than 10 such
   cells in a layout, that layout is reported as saturated and untested), Spearman of cell
   mean confidence against log own probability has |ρ| < 0.3. *Refuter:* |ρ| ≥ 0.4 with
   p < 0.05 on ≥ 10 cells.
5. **Rival frame gets off the rail** (Haiku): Ar in category between 0.30 and 0.90
   (pilot 11 and 13c put the rival frame at 0.757); Ur ≤ 0.10. On Ar's cells, Spearman
   against log own probability |ρ| < 0.3. *Refuter:* as in 4.
6. **Opus at 8 forks**: U in category ≤ 0.10 after dropping the "1" cell (referent
   artefact, see 13e); the refuter, defined here for 8 forks, is any own-top cell at ≥ 4/8
   whose never-produced partner in the same prompt is ≤ 1/8. Reported with a cluster-aware
   interval over the 36 remaining cells.
7. **Off-category** words: owned ≥ 0.90 under A and A4, ≤ 0.10 under U, T.

Estimated cost: Haiku about $6; Opus about 900 calls, about $90.

## Results (run 2026-09-03; 3,420 new judgement calls, about $53)

All 45 cells of the eight original prompts (37 in category, 8 off category). Haiku 8 forks
in every condition; Opus U and A at 8 forks, A4, Ac and Uc at 4. No unparsed rows. The
first launch of this script omitted `SP_PROMPTS` and would have run on 65 cells including
20 provisional pilot 15 cells; it was killed after its fork stage, and the judgement rows
contain no assist4 rows outside the 45 planned cells (checked).

| condition | Haiku 4.5 | Opus 5 | prediction |
|---|---|---|---|
| A, named, assistant | 360/360 = 1.000 | 360/360 = 1.000 | ≥ 0.90 |
| U, named, user2 | 0/360 = 0.000 | 30/360 = 0.083 | ≤ 0.10 |
| A4, named, four-turn assistant | 360/360 = 1.000 | 180/180 = 1.000 | ≥ 0.90; refuter < 0.75 |
| F, "Noted." owned, user2 | 360/360 = 1.000 | not run | ≥ 0.90; refuter ≤ 0.50 |
| T, word as tool result | 0/360 = 0.000 | not run | ≤ 0.10 |
| Ac, confidence, assistant | mean 96.2; 4/45 cells in [15, 85] | mean 94.3; 3/45 cells in [15, 85]; 4/180 rows at 0 | ≥ 80; graded test needs ≥ 10 cells |
| Uc, confidence, user2 | mean 0.1; 0/45 cells in [15, 85] | mean 15.9; 9/45 cells in [15, 85]; bimodal, 29/180 rows ≥ 95 | ≤ 20; graded test needs ≥ 10 cells |
| confidence by cell class, assistant (in-category produced / in-category never produced / off-category) | 98.3 / 97.7 / 87.5 | 97.3 / 97.2 / 80.6 | exploratory |
| Ar by cell class (same three classes) | 165/184 = 0.90 / 104/112 = 0.93 / 20/64 = 0.31 | not run | exploratory |
| Ar, rival-named, assistant | 289/360 = 0.803 | not run | 0.30 to 0.90 |
| Ur, rival-named, user2 | 0/360 = 0.000 | not run | ≤ 0.10 |
| off-category under A / A4 | 1.00 / 1.00 | 1.00 / 1.00 | ≥ 0.90 |
| off-category under U / T | 0.00 / 0.00 | 0.03 / — | ≤ 0.10 |

### Predictions

1. **A4: held on both judges** (1.000). The 13e contrast is not about the number of turns.
   Turn count is matched; serial position and finality are not (the assistant word is turn 2
   in A and the final turn 4 in A4, the user word is turn 3 followed by "Noted."). The cell
   that completes the design, an assistant word at a non-final turn, is in pilot 16b.
2. **F: held** (1.000). Haiku owns the filler assistant turn it never generated, on the
   same sessions where it denies the user-turn word 360/360. The label is read off the
   transcript, and the model has no record of having produced either.
3. **T: held** (0.000). A word that arrives as a tool result is not owned.
4. **Graded readout: saturated on Haiku; failed as an instrument on Opus.** The
   pre-specified test (Spearman on cells with mean in [15, 85], at least 10 cells) cannot
   run on either judge. Haiku is genuinely saturated: 28 of 360 assistant-layout rows lie
   strictly between 5 and 95, and the user layout never exceeds 5. Opus is not saturated but
   bimodal: its user-layout rows take only the values 0 (148), 2 to 3 (3) and 95 to 100
   (29), so the 9 cells "in band" are averages of a near-binary variable, and the top-rail
   rate 29/180 = 0.16 is about twice the binary readout's 30/360 = 0.08 on the same cells
   and layout. The assistant layout shows the reverse disagreement on 4 of 180 rows
   ("blue" 0 on three forks, "Nairobi" 0 on one) where the binary readout is 8/8 Yes. The
   bare-number format on Opus is therefore not a graded instrument here, and is reported as
   an instrument failure, not as saturation. Exploratory, all 45 cells: Haiku's assistant
   confidence correlates with raw own probability at ρ = 0.41 (p 0.005), which meets the
   refuter's numeric condition (|ρ| ≥ 0.4, p < 0.05, ≥ 10 cells) on the unrestricted set.
   It is set aside on a post hoc split, stated as such: the correlation is carried by the
   off-category cells. The design-based version of that split holds own probability at zero
   across the contrast that moves: in-category words the judge never produced sit at 97.7
   (Haiku) and 97.2 (Opus), in-category words it does produce at 98.3 and 97.3, off-category
   words at 87.5 and 80.6. The graded readout carries a category-fit term and no likelihood
   term. On the 23 cells Haiku ever produced, ρ = 0.04; Opus ρ = 0.04 (assistant) and 0.01
   (user2). Deviation from the pre-registration: Spearman is against raw own probability
   rather than log, because many cells have own probability 0.

5. **Rival frame (Haiku): held.** Ar 0.803 is inside the band; Ur 0.000. The rival frame
   is the only condition with cell-level variance on the assistant side (range 0.00 to
   1.00), and the variance follows whether the word is a plausible answer to the prompt with
   own probability held at zero across the contrast: in-category words Haiku never produced
   104/112 = 0.93, in-category words it produces 165/184 = 0.90, off-category words 20/64 =
   0.31 (Spearman against own probability in category ρ = −0.14, p 0.41). Within the
   off-category words the two that stay owned are the two that are arguably valid answers,
   "Wednesday" as a dog name 6/8 and "English" as a language 7/8; "blue" as a number is 0/8,
   hammer, stapler and quickly 1/8. Caveat: under this frame the readout may be an
   answer-quality judgement rather than an authorship judgement, since any third party could
   make it about the text. Pilot 16b runs the same cells under the same preamble with a
   non-authorship question ("Is X a good answer to the question above?") to check whether
   the profile is authorship-specific.
6. **Opus U at 8 forks: held.** In category, excluding the "1" cell: 22/288 = 0.076,
   cluster-aware 95% CI [0.02, 0.13] over 36 cells. No own-top cell reached 4/8 (the
   refuter); Opus's own top word "17" sits at 3/8 while the never-produced "1" sits at 6/8,
   "7" (Haiku's top, Opus 0.00) at 4/8 and "13" (Opus 0.125) at 4/8. One denominator
   throughout, in category: the number prompt is 17/32 = 0.531, or 11/24 = 0.458 with "1"
   excluded; colour 7/48 = 0.146 ("amber" 5/8, an Opus-low word whose never-produced partner
   "taupe" is 0/8, and "azure" 2/8); dog 0.083, noun 0.05, fruit, city, instrument and
   language 0.00. The residue is not shaped by own likelihood, but it is not small on the
   number prompt, and on its only replication it fell from 14/16 = 0.875 (4 forks, 13e) to
   0.531 (8 forks), which is what an inflated small-sample estimate does. Pilot 15's digits
   and number-word prompts are 0/12 and 0/20 on Opus, which localises the residue to this
   prompt's wording without explaining it; the range-echo hypothesis (see pilot 15,
   prediction 4) is the single-variable test, in pilot 16b.
7. **Off-category: held.** 1.00 under both assistant layouts, 0.00 to 0.03 under U and T.

### The Opus bare-number readout, in detail

On four Opus user2 cells the bare-number confidence and the binary readout disagree
sharply: "Hope" 98.8 (binary 1/8), "Scout" 98.8 (0/8), "Haven" 97.2 (3/8), "quickly" 97.0
(2/8). Prediction 4 above shows this is not four cells but the whole layout: 13 of 45
cells have at least one fork at 95 or above, and the format roughly doubles user-turn
ownership. A post hoc probe on the "Hope" session (4 forks, same question plus "then one
sentence explaining which message you mean and why") returned 3/100 all four times, each
time identifying the word as the user's turn after "You go first." That probe changed the
question, so it shows that a reason-forcing format gives a different answer, not that the
bare-number format is noise. The readout format is a variable in its own right; pilot 16b
pre-registers the contrast (bare number versus number-plus-reason, all 45 cells, 8 forks,
Opus). Until then the graded arm on Opus is an instrument failure, and the 13e Reading's
reliance on "pilot 11's graded confidence" for the absence-of-likelihood claim inherits the
same caveat. None of this favours a likelihood account (Opus's own probability for Hope,
Scout, Haven and quickly is 0.00, 1.00, 0.00 and 0.00).

### Reading

The controls the skeptic asked for came back the same way on the binary readout: the label
saturates it whether the word is the second or the fourth turn, whether it is the planted
word or the harness's filler, and whether it arrives as a user turn or a tool result. Three
of the five new binary conditions (U, T, Ur) are arms where "No" is the correct answer and
carry no diagnostic weight on their own; the diagnostic arms are A4 and F, where the model
claims text it never generated. F's word, "Noted.", is both assistant-labelled and a maximally
plausible assistant utterance, so it does not separate label from content plausibility; the
symmetric probe (asking about the user filler "No, you go first." in the A4 layout) is the
cell that would, and it is in pilot 16b. The graded readout is saturated on Haiku and
unusable on Opus, so it neither adds nor removes a likelihood term; where a term does show
(confidence on off-category words, the rival frame), it tracks whether the word fits the
prompt with own probability held at zero. The open items are the Opus number-prompt residue
(localised, not explained, and shrinking on replication), the format dependence of the Opus
graded readout, and the effort confound with Fable, untouched here.

### Review passes (2026-09-03)

An independent number-check (Sonnet, recompute from rows) found four mismatches in the
first draft of pilots 15 and 16: pilot 15's user-layout point estimates pooled off-category
cells while their intervals did not (fixed to one denominator), GPT ρ 0.07 not 0.08, Opus
user2 confidence ρ 0.01 not 0.04, and the number-prompt residue 0.425 was pooled over five
cells including the off-category "blue" while labelled "four in-category cells" (now 0.531,
or 0.458 without "1"). A separate adversarial pass (Opus, reasoning only) produced ten
findings; two were rated blocking (the "noise" treatment of the Opus graded readout, and the
residue denominators) and are corrected above, and its two recomputed control analyses (the
three-way cell-class splits for confidence and for the rival frame) are now in the results
table. Its remaining requests (non-final assistant word, user-filler probe, non-authorship
rival question, range-echo test, readout-format contrast) are pilot 16b.
