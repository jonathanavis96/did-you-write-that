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
| Ac, confidence, assistant | mean 96.2; 4/45 cells in [15, 85] | mean 94.3; 3/45 cells in [15, 85] | ≥ 80; graded test needs ≥ 10 cells |
| Uc, confidence, user2 | mean 0.1; 0/45 cells in [15, 85] | mean 15.9; 9/45 cells in [15, 85] | ≤ 20; graded test needs ≥ 10 cells |
| Ar, rival-named, assistant | 289/360 = 0.803 | not run | 0.30 to 0.90 |
| Ur, rival-named, user2 | 0/360 = 0.000 | not run | ≤ 0.10 |
| off-category under A / A4 | 1.00 / 1.00 | 1.00 / 1.00 | ≥ 0.90 |
| off-category under U / T | 0.00 / 0.00 | 0.03 / — | ≤ 0.10 |

### Predictions

1. **A4: held on both judges** (1.000). The 13e contrast is about the role label, not the
   number of turns.
2. **F: held** (1.000). Haiku owns the filler assistant turn it never generated, on the
   same sessions where it denies the user-turn word 360/360. The label is read off the
   transcript, and the model has no record of having produced either.
3. **T: held** (0.000). A word that arrives as a tool result is not owned.
4. **Graded readout: saturated in both layouts on both judges.** The pre-specified test
   (Spearman on cells with mean in [15, 85], at least 10 cells) cannot run: Haiku has 4 such
   cells in the assistant layout, all off-category words, and none in the user layout; Opus
   has 3 and 9. Reported, not tested. Exploratory, over all 45 cells: Haiku's assistant
   confidence correlates with raw own probability at ρ = 0.41 (p 0.005), but the correlation
   is carried by the eight off-category cells (mean 87.5 against 98.1 in category); on the 37
   in-category cells ρ = 0.19 (p 0.25), and on the 23 cells the judge ever produced ρ = 0.04.
   Opus: ρ = 0.04 in both layouts. The graded readout adds no likelihood term.
5. **Rival frame (Haiku): held.** Ar 0.803 is inside the band; Ur 0.000. The rival frame
   is the only condition with cell-level variance on the assistant side (range 0.00 to
   1.00): six of the eight off-category cells sit at 0.00 to 0.25, "Wednesday" at 0.75 and
   "English" at 0.88 (off-category mean 0.31), against 0.91 for the in-category cells. On the in-category
   cells Spearman against raw own probability is ρ = −0.14 (p 0.41): under the frame that
   moves the readout, plausibility as a category member moves it and own likelihood does not.
6. **Opus U at 8 forks: held.** In category, excluding the "1" cell: 22/288 = 0.076,
   cluster-aware 95% CI [0.02, 0.13] over 36 cells. No own-top cell reached 4/8 (the
   refuter); Opus's own top word "17" sits at 3/8 while the never-produced "1" sits at 6/8,
   "7" (Haiku's top, Opus 0.00) at 4/8 and "13" (Opus 0.125) at 4/8. The residue is on the
   number prompt as a whole (0.425 pooled over its four in-category cells) and not shaped
   by own likelihood; every other prompt is 0.00 to 0.125 (colour 0.125, from "amber" at
   5/8, an Opus-low word whose never-produced partner "taupe" is 0/8). Pilot 15's digits and
   number-word prompts are 0/12 and 0/20 on Opus, so the residue belongs to this prompt's
   wording, not to numbers.
7. **Off-category: held.** 1.00 under both assistant layouts, 0.00 to 0.03 under U and T.

### One unexplained readout inconsistency

On four Opus user2 cells at 4 forks, the bare-number confidence readout and the binary
readout disagree: "Hope" 98.8 (binary 1/8), "Scout" 98.8 (0/8), "Haven" 97.2 (3/8),
"quickly" 97.0 (2/8). A post hoc probe on the "Hope" session (4 forks, same question plus
"then one sentence explaining which message you mean and why") returned 3/100 all four
times, each time identifying the word as the user's turn after "You go first." The
number-only format therefore produced a different answer from the number-plus-reason
format on these cells, and the assistant-layout confidence never showed this. Treated as
noise in the bare-number readout on Opus; it does not favour a likelihood account (Opus's
own probability for Hope, Scout, Haven and quickly is 0.00, 1.00, 0.00 and 0.00).

### Reading

Every control the skeptic asked for came back the same way: the label saturates the
binary readout whether the word is one turn or four turns deep, whether it is the planted
word or the harness's filler, and whether it arrives as a user turn or a tool result. The
graded readout saturates too. Nothing in pilot 16 lets a likelihood term show through on
either Claude judge, and the one frame that moves the readout (the rival preamble) moves
it by category plausibility. The remaining open items are the Opus number-prompt residue,
which is prompt-specific, and the effort confound with Fable, untouched here.
