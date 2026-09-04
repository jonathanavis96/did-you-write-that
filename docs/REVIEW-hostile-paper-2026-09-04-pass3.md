# Third hostile review of the paper draft (2026-09-04, after the pass-2 revision)

Third referee (Claude Fable 5.1, the same model that wrote passes 1 and 2, as the
Limitations section discloses), working from `paper/main.tex` as it stands (compiles
clean, 18 pages), both earlier reports with their response sections, the pass-2
number-check, the pilot documents, the summary scripts, and direct recomputation from
the row files under `out/`. Per the standing instruction, no number was trusted because
a previous pass matched it: every figure named below was recomputed from the rows in
this pass, including re-running `selfportrait/clean11_summary.py` (both prefixes),
`pilot14_summary.py`, and fresh scripts against `clean11_*`, `clean13_*`, `clean16_*`,
`clean_*` (pilot 15b), `leakgpt_*`, `own_local_*`, `para_local_*`, `para_*` (17b),
`p17c/*` and `listing13.jsonl`.

## Recommendation

Minor-to-major revision. The pass-2 response is nearly all real: every major fix it
claims is in the text where it claims, the fired refuter is reported as fired, the
title no longer asserts the exclusion, the exclusivity sentences admit the Haiku
non-author step, the pilot-16 controls are marked and the load-bearing three rerun
clean (320/320, 320/320, 0/320 reproduce from `clean16_judgements.jsonl`), and about
120 recomputed figures match the rows exactly. What remains is one mislabeled
manipulation on the exact-probability arm that changes what a cross-arm sentence means,
a Method statistics rule that the paper's own reported p-values contradict (the second
revision in a row to misstate this same rule), a structural readability problem, and a
tail of checkable number-hygiene items. Nothing found in this pass changes a direction
or a headline conclusion.

## Verification of the pass-2 response

All eight major items and all twelve minor items of the pass-2 response were checked
against the text and, where numerical, against the rows. Present and correct: the 18.2
refuter reported as fired with the "rank over rounding" retraction (lines 167, 235;
recomputed: 48 distinct values, logit 18.72 to 29.30, ρ=+0.44 p=0.0020, within +0.30
p=0.040); the retitle; the exclusivity rewrite (lines 211, 215, 246; Haiku non-author
0.043, cell p=0.0039, 7/8 prompts p=0.016 all reproduce); the abstract rewrite with the
tab:label range (194/240=0.808 and 32/272=0.118 reproduce); the clean16 rerun; the 3B/
1.5B qualifications; the listing-probe timing and elimination caveat (line 215); the
ideal-observer paragraph (line 248); the Holm families (both re-derived: same six
frame-step survivors even when the actual cell p-values 1.35e-6/2.44e-4/1.46e-6 are
used instead of the 3e-4 bound; exact-arm survivors identical, 0.17 and 0.10 as
stated); the Section 4.6 units; and minors 1–12. Not done despite the response's
"every point was acted on": the Opus prompt-level p=0.06 minimum-attainable note
(pass-2 major 8, last item), the abstract's clean/contaminated mixing (pass-2 major 4,
last sentence), and the within-prompt values for the paragraph 4B rival and 1.5B
coefficients (the response says "added for every exact-arm coefficient"; the paragraph
rival within-prompt +0.35 p=0.014 and the 1.5B −0.82/−0.61 are in no line of the
paper). These reappear below.

## Major points

### 1. The exact one-word arm's "rival" frame is not the rival frame

Pilot 14 never ran the turns-replaced question. `out/own_local_*.jsonl` contain exactly
four questions at every scale: neutral, placebo, rival_norep2, named — no `rival`. The
`rival_norep2` text (`selfportrait/ownership.py` line 163: "in a separate session, a
different model was asked this same prompt; nothing that model produced is part of this
conversation") is word-for-word the paper's own "Rival, not an author" frame (line 65),
the frame the production sections take pains to distinguish from "rival, turns
replaced". Yet the paper presents the pilot-14 step as the rival frame in three places:
line 150 ("What survives at every scale is that a rival frame drives ownership to the
floor (placebo minus rival +0.57, +0.19 and +0.85 ...)"), tab:preds row 14.4 (line 163,
"placebo minus rival reported"), and Figure 4 (caption line 185, "The rival frame
floors ownership at every scale"; the figure's x-tick, from `paper/figures.py`
`QWEN_QUESTIONS`, is plain "rival" over `rival_norep2` data — in the same paper whose
Figure 2 legend distinguishes "rival, named" from "rival, turns"). The numbers
themselves reproduce exactly as placebo−rival_norep2 over in-category cells (+0.569,
+0.188, +0.849; 18/18 prompts each); only the name is wrong.

The name matters, because correctly labeled it is a finding the paper currently hides
from itself. On the Claude judges the non-author mention costs 0.04 and 0.03 and the
exclusivity story is that only a candidate author for this turn costs much; on the Qwen
models the same non-author mention drives ownership to the floor (−0.85 at 4B). Either
the small models lack the exclusivity gradient — mere mention defeats the report, which
is worth a sentence and bears on how far the Wegner framing generalises — or the arm
cannot support the transfer claim "a rival frame drives ownership to the floor at every
scale" as written, since the manipulation that floors Qwen is the one that costs a
Claude judge 0.03. Fix: rename the frame in all three places, and state the contrast.
(Pilot 18, the paragraph arm, did run the true rival question; nothing there is
affected.)

### 2. The stated Wilcoxon rule is contradicted by the paper's own reported values — again

Line 69 states, as the fix for the pass-1 audit: "cells with a zero difference dropped,
the exact distribution used where the remaining differences are untied and at most 25,
so a step present on 8 of 30 cells and absent on the others has p = 0.0078, and the
tie-corrected normal approximation otherwise." The word "untied" makes this false, and
the sentence's own example violates the rule it states: the eight nonzero GPT placebo
differences are tied (0.375, 0.5×2, 0.625, 0.75×2, 0.875×2), so the printed rule sends
them to the approximation, which is 0.0114, not the reported 0.0078. Likewise the Opus
neutral-against-rival step: 13 nonzero differences, tied (0.125×5, 0.375×2, ...); the
released scorer (`clean11_summary.py::wilcoxon_p`, scipy 1.18 default after dropping
zeros) prints the exact 0.000244, which is what makes line 215's "p < 3×10⁻⁴ for each
of the three judges" true — under the rule as printed that step is 0.00136 and the
three-judge sentence is false. Verified by running the scorer and scipy directly: with
zeros dropped, scipy's default uses the exact (permutation) distribution for ≤25
nonzero differences, ties included, and the approximation above 25 (Haiku and GPT
neutral−rival, n=30, are the approximation values 1.35e-6 and 1.46e-6, exact would be
1.9e-9). Every reported value matches the scorer; the rule text does not match the
scorer. Pilot 19's own number-check note (the 0.0078-vs-0.0114 explanation) shows the
authors know the mechanism; the Method sentence just states it wrongly. Fix: "the
exact distribution whenever at most 25 nonzero differences remain, ties included; the
tie-corrected normal approximation above 25, which is conservative." One sentence; but
a referee who applies the printed rule falsifies two quoted p-values and one
three-judge claim, so it is a major until fixed.

### 3. Structure: the forensics have eaten Section 4.3, and one sentence still asserts what another retracts

Section 4.3 (line 215) is a single ~1,100-word paragraph in which the paper's central
positive result (the step ordering and its two-level tests) shares space with the dip
chronology, the 10,264-record fork audit, the listing-probe timing, the paginated-fork
errors and the usage-limit block. The Method statistics paragraph (line 69) is ~700
words. The abstract is ~350 words, over most venues' caps. This is now a rejection
risk of its own: the defensive apparatus is correct but it is in the reader's way. The
dip forensics (everything from "On the contaminated run (2026-09-03) it cost 0.51" to
"...the 05:40 probe falls inside that re-run") is an appendix with a two-sentence
summary in 4.3.

Related internal contradiction: line 84 ends "so it is variation in the served model,
not the leak" — asserted; line 215 says the served-model attribution "remains a
conclusion by elimination ... no positive fingerprint of a model change." The second is
the honest one; line 84 should claim only "not the leak" and point at Section 4.3 for
the rest.

### 4. Abstract and refuter-count precision

(a) The label range "0.81 to 1.00 ... 0.00 to 0.12 ... across four judges" mixes clean
and contaminated rows unmarked: the 0.12 endpoint (GPT 13d) and the fourth judge
(Fable, 13e) are contaminated-harness rows, in a paper whose selling point is the
contamination discipline. Pass-2 flagged this (major 4, last sentence); the response
fixed the endpoints but not the mixing. Clean-only the range is 0.81–1.00 against
0.00–0.04. (b) "nonsense answers included" is false at the quoted range for GPT: the
range is the named question on in-category cells (tab:label), and GPT's off-category
words under the named question are owned 50/64 = 0.78, below the 0.81 floor
(recomputed from `clean13_judgements.jsonl`; the Claude judges are 64/64). Scope the
clause or quote the neutral question for the nonsense claim. (c) "one registered
refuter fires": tab:preds records three fired refuters (14.1 at 1.5B — against the
label effect, the paper's headline; 18.2; 18.3 at 3B). The abstract names only the one
that concerns the likelihood story. Say "three registered refuters fire, one of them on
the likelihood correlation" or scope the sentence explicitly. (d) Line 235 says of the
four 4B coefficients "which two of them meet" the refuter, while tab:preds 14.2 records
the +0.48 as "refuter not fired" (the placebo question was outside the registration's
scope). Both are defensible alone; adjacent they read as a contradiction. Say: two
exceed the registered threshold, one inside its registered scope (fired), one under a
question the registration did not cover.

## Minor points

1. Line 69: "The frame-step family (nineteen tests: ten over cells, nine over
   prompts)" — the tests listed in Section 4.3 are nine cell-level and ten
   prompt-level (the Opus non-author step has a prompt-level sign test and no quoted
   cell-level p). The pass-2 number-check noted the same reversal in its dispatch;
   the paper kept it.
2. Line 69: "With 27 to 37 cells the critical |ρ| at p=0.05 is 0.33 to 0.38" — stale;
   tab:rho's rows are 11–32 cells and its caption (correctly) gives 0.60–0.35. The 37
   is the contaminated cell set.
3. Line 122: "The residues are each one prompt" — GPT's clean user-layout Yes count is
   9/240: 7 on the dog prompt, plus Vienna (city, gpt_mid) 1/8 and Telescope (noun,
   haiku_top) 1/8. Two residual rows are not the dog prompt. Also "8/48 on \opus{}"
   for Quickly: the cell is 8/8 forks, the off-category user set is 8/64, and the noun
   prompt's user rows are 8/48 — the text does not say which denominator it means.
4. Line 215: "the rival frame does not swing (0.335, 0.208 on the sampled cells,
   0.179)" — three different bases: 37-cell contaminated in-category, 9-cell sampled
   *including two off-category cells* (in-category only it is 15/56 = 0.268), and
   30-cell clean in-category. Pilot 19's own triple for this claim is 0.153/0.208/
   0.179. After the care taken with Haiku's four rival rates, name these bases too.
5. Line 229 (17b): "picked their own paragraph at 0.77 to 0.92" — the released
   `out/para_pairs.jsonl` gives the four comparison rates 75/96, 75/96, 86/96, 77/96 =
   0.78 to 0.90. The 0.77 and 0.92 endpoints are the six-replication-prompt subset in
   the pilot document (37/48 and 44/48), a subset that also contains a 0.75 the quoted
   range excludes. Quote the pooled range or name the subset. The 0.925/0.062 length
   split reproduces exactly, but only for the Opus-against-Haiku comparison
   (vs-vendor is 0.821/0.292); name the comparison.
6. The within-prompt coefficients for the paragraph 4B rival (+0.35, p=0.014) and the
   1.5B paragraph questions (−0.82, −0.61) are absent from the paper although the
   pass-2 response says they were added; they reproduce and they strengthen the 4B
   rival point (it survives demeaning), so include them.
7. Line 215: the Opus prompt-level p=0.06 is 0.0625, the minimum attainable two-sided
   value with five movers and three ties; "directionally consistent but not
   individually significant" is a power floor there, not evidence of absence (pass-2
   major 8, still unaddressed).
8. GPT stage E (tab:rho row, +0.11): two of the 168 rival rows died on the
   "paginated fork" error, so 2 of the 21 cells have 7 forks; line 215's "produced no
   row" is about judgement rows, but the released `clean13_within.jsonl` does contain
   the two error records — one clause ("two stage-E rival calls errored and their
   cells have seven forks") spares the next checker the confusion this pass had.
9. Line 219: Haiku's explicit rate "0.80" has no denominator (144 pairs; Opus's "of
   142" is 144 minus 2 unparsed rows, also worth a word since the checker must
   discover the unparsed rows to reproduce 0.91).
10. Abstract "up to 18 prompts": no row of tab:label exceeds 10 prompts; 18 is the
    union of distinct prompts across pilots (8 original + 10 of pilot 15). Say so.
11. Line 150: "the within-prompt value ranks exact probabilities below 0.04 against
    each other" — the values below 0.04 are the P(Yes) readouts, not the exact
    probabilities. As written it says the predictor is at floor; it is the readout.
12. Line 231: "68 of 72 trials where its paragraph was the longer" — the table row
    (17c.4) correctly says "longer by more than a word"; the body's bare "longer"
    conflicts with counting rainbow (own shorter by one word) in the within-a-word
    set. Add the three words.

## What was recomputed and matched (so the next pass need not re-fight it)

Table 2 (all nine rows, including GPT stage E +0.11 p=0.62 at 21 cells); Table 3 (all
twelve rates); the full frame-step chain at both levels on all three judges (scorer
values); the label control including GPT 194/240, 9/240, the 46 in-category named No
rows all on city and fruit; off-category 60/64, 63/64, 64/64 neutral and 64/64,
64/64, 50/64 named; clean16 320/320, 320/320, 0/320; the confidence descriptives
(Lisbon 96.0, Paris 95.5, off-category 45.0/59.2, produced-vs-never 95.4/95.4 and
96.1/95.6, sd<6.3 on 63/64, FE slopes +0.02 p=0.89 and +0.02 p=0.70, ranges 94.4–98.0
and 95.0–97.4); GPT confidence 221/7 of 228 at 38 cells × 6 forks, min cell mean 83.3;
the own distributions (every count in line 61); explicit self-prediction (0.91 of 142,
0.80, 0.76 of 132, and every named pair including Prague 6/6, Teal-over-Indigo 6/6,
Lisbon 3/6 four times); pilot 15b in full (136/136, 0/136, 0.647, 0.838, −0.29 p=0.26,
−0.09 p=0.72, Neptune 2/8, Titanium 8/8); leakgpt placebo 72/72; pilot 14 in full
(both Holm families re-derived; +0.16/+0.14/+0.29, within +0.49/+0.40/+0.33, placebo
+0.48 p=1.0e-4, named −0.06, 14.3 and 14.5 observed values, label −0.29/+0.28/+0.31,
the 11-of-18 named failure under the pilot's below-0.10 criterion, the 27.0-nat 1.5B
range); pilot 18 in full (48 distinct values, logit 18.72–29.30, +0.44 p=0.0020,
within +0.30 p=0.040, +0.36 p=0.013, +0.73/−0.24 subsets, −0.66/−0.47, 18.1/18.3/18.4/
18.5 observed values, 2.83 nats per token, shifted 1.5 nats and 0.000-vs-0.816); pilot
17b (0.917/0.573, +0.344, 11/12, p=0.0029, lengths 41.6/60.5/70.4 and 17c's
42.5/67.8/84.0 from the cells files under the alphabetic-token definition,
0.925/0.062); pilot 17c (0.771/0.339, 0.667/0.562, 0.083/0.031, shifted 0/96, 9/96,
0/96, 1152/1152, 92/96, 83/96, 89/96, 64/96); and the listing probe (38/38 with the
planted turn in the assistant role, plugin-catalog turn visible in every transcript).

## What would make it safe

1. Rename the pilot-14 frame everywhere it appears (line 150, tab:preds 14.4, Figure 4
   caption and x-tick) and add the sentence the correct name makes available: on the
   Qwen models the non-author mention alone floors ownership, so the exclusivity
   gradient of Section 4.3 is a production-model finding that the small models do not
   show.
2. Restate the Wilcoxon rule as the scorer's actual behaviour (exact at ≤25 nonzero
   differences, ties included; approximation above) — the quoted values then all
   stand as printed.
3. Move the GPT dip forensics and run chronology to an appendix; make line 84 claim
   only what line 215 defends.
4. Quote the clean-only label range in the abstract (or mark the mixed rows), scope
   "nonsense answers included", and count the fired refuters as three.
5. Sweep the minor list: the ten/nine reversal, the 27-to-37 stale range, the GPT
   residue sentence, the rival triple's bases, the 17b range, the missing
   within-prompt values, the 0.0625 floor note, and the small denominators.

## Response (2026-09-04, same day)

### Major points

1. **Pilot 14 frame renamed.** Section 4.2, tab:preds 14.4 and the Figure 4 caption and
   x-tick now call the pilot 14 step the non-author frame ("rival, not author") and say
   the turns-replaced frame was not run on that arm and that earlier drafts misnamed
   it. The contrast is stated: the mention that costs the Claude judges 0.04 / 0.03 and
   GPT 0.26 floors the Qwen models, so the exclusivity gradient is a production-model
   finding the small models do not share.
2. **Wilcoxon rule restated** as the scorer's behaviour: exact permutation distribution
   whenever at most 25 nonzero differences remain, ties included; tie-corrected normal
   approximation above 25. Every quoted p-value stands as printed.
3. **Structure.** The dip forensics (424 words, from the contaminated-run 0.51 to the
   05:40 probe) moved to a new Appendix "The GPT placebo dip"; Section 4.3 keeps a
   two-sentence summary and a pointer. The leak section's close now claims only "not
   the leak" and defers the attribution to Section 4.3 as a conclusion by elimination.
4. **Abstract** rewritten at 335 words: clean-run label range only (0.81 to 1.00 against
   0.00 to 0.04), the nonsense clause scoped to the neutral question, three fired
   refuters with one on the likelihood correlation; the "18 prompts" and the mixed
   contaminated rows are gone. Section 4.6's "which two of them meet" now says two
   exceed the threshold, one inside its registered scope and one under a question the
   registration did not cover.

### Minor points

1. Nine over cells, ten over prompts. 2. Power range restated for 30 to 32 cells with
the 11- and 21-cell values. 3. GPT residue: 7 of 48 on the dog prompt plus two single
rows on city and noun; Opus Quickly given as 8 of 8 forks and its only off-category
user-layout Yes rows. 4. The rival triple names its three bases and adds the
in-category sampled value 0.268. 5. 17b forced choice quoted pooled, 0.78 to 0.90 with
the four counts (75, 75, 86, 77 of 96; verified from `out/para_pairs.jsonl`). 6.
Within-prompt values added for the paragraph 4B rival (+0.35, p = 0.014) and the 1.5B
questions (−0.61, −0.82). 7. Opus prompt-level p given as 0.0625, the attainable
minimum, and the sentence says it is a power floor. 8. tab:rho caption notes the two
errored GPT stage E calls and the two seven-fork cells. 9. Denominators added (144
pairs, two unparsed; Haiku 0.80 of 144). 10. "18 prompts" removed from the abstract.
11. "ranks readouts that all sit below 0.04". 12. "longer by more than a word". The
0.925 / 0.062 length split named in minor 5 does not appear in the paper text.
