---
title: "Pilot 16b: the second skeptic pass's five controls"
status: pre-registered 2026-09-03 before the run
depends_on: docs/PILOT-16-label-controls.md, docs/PILOT-15-prompt-effects.md
---
# Pilot 16b: five controls the pilot 16 skeptic asked for

Same 45 cells as pilot 16 (eight prompts) unless stated. Haiku 4.5 at 8 forks; Opus 5 where
named. Harness additions: layout `assist4b`, questions `named_userfiller`, `rival_quality`,
`named_reason_conf`, prompt `number_norange`, and `SP_CELLS_FILE` for planting an explicit
cell list (`out/cells/p16b_rangeecho.json`).

| id | judge | layout | question | what it separates |
|---|---|---|---|---|
| B1 | Haiku | assist4b: user prompt / assistant WORD / user "Thanks." / assistant "Noted." | named | assistant word at a non-final turn: label vs serial position and finality |
| B2 | Haiku | assist4 (word as final assistant turn) | named_userfiller: `Did you write the message "No, you go first." …` | a plausible utterance under a user label: label vs content plausibility |
| B3 | Haiku | assistant | rival_quality: rival preamble + `Is "{word}" a good answer to the question that opened this conversation?` | whether the rival-frame variance is an answer-quality judgement |
| B4 | Opus | user2 | named_reason_conf (0 to 100 plus one sentence of reason), 8 forks; named_conf topped up from 4 to 8 forks | readout format as a variable |
| B5 | Opus, Haiku | user2 | named on `number_norange` ("Pick a number. Reply with just the number.") with 7, 13, 17, 1 planted, and on the ranged number prompt with 47 planted | the range-echo account of the Opus number residue |

## Predictions and refuters

1. **B1 ≥ 0.90** in category. *Refuter:* < 0.75, in which case finality or position, not
   the label, carried A4.
2. **B2 ≤ 0.10**: the model disowns a plausible short utterance that sits under a user
   label, on the same sessions where it owns the word under the assistant label (A4 1.000).
   *Refuter:* ≥ 0.50, in which case the F result (owning "Noted.") is content plausibility,
   not label.
3. **B3 profile matches Ar.** Cell means of rival_quality against pilot 16's rival_named
   over the 45 cells: Spearman ρ ≥ 0.5, in-category ≥ 0.80, off-category ≤ 0.40. If so, the
   rival-frame ownership variance is an answer-plausibility judgement that any reader of the
   transcript could make, which is what the theory expects and what pilot 16's corrected
   wording says; the rival frame then carries no authorship-specific information on Haiku.
   *Alternative:* ρ < 0.2, in which case the ownership readout under the frame carries
   something beyond answer quality, to be characterised before any further claim.
4. **B4: the discrepancy is format.** Reason-format mean ≤ 10 and top-rail rate (≥ 95) ≤
   0.05 over 360 rows; bare-number top-rail rate at 8 forks stays above 0.10 (pilot 16: 29/180
   = 0.16). *Refuter:* reason-format top-rail ≥ 0.10, in which case Opus does claim
   user-turn words at high confidence under some formats and the label result on Opus needs
   the graded arm rerun properly.
5. **B5: range echo.** If the Opus residue is range echo, `number_norange` cells pooled ≤
   0.10 and 47 ≤ 1/8 on Opus (Haiku 0 throughout, as everywhere). *Refuter:* norange pooled
   ≥ 0.30 (the residue survives without a range, so it is about the number prompt or numbers
   on Opus, not echo). 47 ≥ 4/8 would mean any planted number is owned on this prompt.

Estimated cost: Haiku 1,080 calls about $6; Opus 620 calls about $30.

Results: PENDING.
