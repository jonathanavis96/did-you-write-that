---
title: "Pilot 16: controls the skeptic asked for on the role-label result"
status: pre-registered 2026-09-03; the text was on disk before launch, the commit landed a few minutes after launch because a lint hook rejected the first commit attempt
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

Results: PENDING.
