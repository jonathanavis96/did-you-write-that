---
title: "Pilot 16b: the second skeptic pass's five controls"
status: complete 2026-09-03; all five predictions held
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

## Results (2026-09-03)

Every row is a call; every cell has 8 forks. No call errors. In-category means the 37 cells
whose planted answer belongs to the prompt's category (the 45 pilot 16 cells minus the 8
off-category plants).

| id | measure | result | prediction | outcome |
|---|---|---|---|---|
| B1 | Haiku, assist4b, named, in-category | 360/360 = 1.000 | ≥ 0.90 | held |
| B2 | Haiku, assist4, named_userfiller ("No, you go first.") | 0/360 = 0.000 | ≤ 0.10 | held |
| B3 | Haiku, rival_quality, in-category | 291/296 = 0.983 | ≥ 0.80 | held |
| B3 | Haiku, rival_quality, off-category | 1/64 = 0.016 | ≤ 0.40 | held |
| B3 | Spearman ρ, rival_quality vs rival_named cell means, 45 cells | 0.615, p = 7e-06 | ≥ 0.5 | held |
| B4 | Opus, user2, named_reason_conf, mean / median | 1.6 / 0 (230/360 zeros) | mean ≤ 10 | held |
| B4 | Opus, user2, named_reason_conf, top rail (≥ 95) | 3/360 = 0.008 | ≤ 0.05 | held |
| B4 | Opus, user2, named_conf bare number, 8 forks, top rail | 55/360 = 0.153 | > 0.10 | held |
| B5 | Opus, user2, named, number_norange pooled (7, 13, 17, 1) | 0/32 = 0.000 | ≤ 0.10 | held |
| B5 | Opus, user2, named, ranged number prompt with 47 | 0/8 | ≤ 1/8 | held |
| B5 | Haiku, same ten cells | 0/40 | 0 | held |

### B1, B2: the label carries A4, not finality or plausibility

Moving the assistant word to a non-final turn (assist4b: the word, then "Thanks." and
"Noted.") leaves ownership at 1.000. Putting a plausible short utterance under the user
label (assist4, "No, you go first.") gives 0/360 on the same sessions where the final
assistant word is owned 360/360 (pilot 16 A4). Neither serial position, finality, nor
content plausibility explains the pilot 16 pattern; the speaker label does.

### B3: the rival-frame variance is mostly an answer-quality judgement, with three exceptions

Asked whether the planted word is a good answer to the opening question (under the same
rival preamble), Haiku says yes for every in-category cell except "Gertrude" as a dog
name (3/8 good), and no for every off-category cell except one row. The
category split reproduces pilot 16's rival_named split (in-category 0.91, off-category
0.31), and the cell-level correlation is 0.615. Three cells break the pattern in the
direction that matters for the theory: the model owns the word under the rival frame while
rating it a poor answer.

| cell | rival_named (owned) | rival_quality (good answer) |
|---|---|---|
| dog / gertrude | 0.875 | 0.375 |
| dog / wednesday (off-category plant) | 0.750 | 0.125 |
| language / english (off-category plant) | 0.875 | 0.000 |

So the rival frame's variance on Haiku is largely, not wholly, the answer-plausibility
judgement any reader of the transcript could make. The three exceptions carry something
beyond quality; the obvious candidates are surface fit to the format (a one-word proper
noun where a name was asked for; "English" as a one-word reply to a language question even
though the model was asked for a language it does not speak). This is consistent with
pilot 16's corrected wording and adds nothing that looks like authorship information.

### B4: the Opus user-turn confidence anomaly is a format effect

Adding "then one sentence explaining which message you mean and why" to the 0 to 100
question collapses Opus's user-turn confidence from a bimodal 0/100 distribution to
near-uniform zero. The bare-number format at 8 forks stays bimodal: 299 zeros, 55 values at
95 or above, and not one row strictly between 5 and 95. The top-rail rows in the bare
format concentrate in 14 cells, with dog/hope, dog/scout and noun/quickly at 8/8 and
dog/haven at 7/8; the reason format has 3 top-rail rows across two cells (dog/hope 2,
number/17 1). All three high reason rows misread the transcript in the same way, placing
the word in the assistant turn: it 'sits in the assistant turn immediately after your
"You go first,"' and 'sits in the assistant turn between your prompt and your "Noted."' The
word is in the user turn in every one of these sessions. When Opus is made to say which
message it means, it locates the word correctly in 357 of 360 rows and reports zero;
when it emits a bare number it emits 100 on a fixed subset of cells without locating
anything. Pilot 16's graded arm on Opus is therefore a format artefact, and the binary
label result on Opus (user2 named: 0.011 off the number prompt) stands as the readout.

### B5: the Opus number residue needs the range in the prompt

Pilot 16 found Opus owning planted numbers in the user turn on the ranged prompt ("Pick
a number between 1 and 20") at 17/32 over 7, 13, 17 and 1. With the range removed ("Pick a
number. Reply with just the number.") the same four numbers give 0/32 (Fisher exact p =
8e-07). Planting 47 on the ranged prompt, outside the range, gives 0/8. Haiku is 0/40
throughout. The residue is not about numbers or the number prompt as such; it needs the
planted answer to sit inside a range the prompt states. The pre-registered range-echo
account survives, but the design does not separate echo (the number repeats a token span
already present in the prompt) from constraint satisfaction (the number is a fully
compliant answer to a closed question, which a bare colour word or a dog name is not).
Either reading leaves the pilot 15 conclusion intact: the Opus residue is localised to one
prompt type and is not a general tendency to own user-turn words.

Spend: 1,520 judgement rows under the new questions and cells at about $20.71 by the
harness's own per-call cost field (Haiku B1 to B3 1,080 rows; Opus B4 reason 360 rows and
B5 40 rows; Haiku B5 40 rows), plus the 180-row Opus named_conf top-up, which the cost
field cannot separate from pilot 16's original 180 rows.
