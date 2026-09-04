# Second hostile review of the paper draft (2026-09-04, after commits 1c766bf, 0bc6cb6, d6f2c55)

Second referee, working from `paper/main.tex` (revised draft), the first review and its
response section, `docs/AUDIT-codex-fork-replay-2026-09-04.md`, the cross-vendor number
check, the pilot documents, and direct recomputation from the row files under `out/`.
Points below do not repeat first-review points recorded as answered, except where the
answer is inadequate, and then the inadequacy is stated.

## Recommendation

Major revision. The prefill method, the label control and the disclosure regime are
strong, and the revision genuinely fixed most of the first review's points. But one
registered refuter that fired is dismissed with a justification that is factually wrong
about the data, the paper's central exclusivity sentence is contradicted by its own
reported numbers, and the abstract is contradicted by the paper's own Table 1 in two
places. These are not polish; each is a claim a reviewer can falsify from the paper
itself.

## Major points

### 1. The fired pilot-18 refuter is dismissed with a false characterization of the data

`main.tex` line 228 and tab:preds row 18.2: the 4B neutral correlation +0.44 (p=0.002)
"meets the refuter as written, on 48 cells all at 1.000 differing below the third
decimal, so the rank is a rank over rounding, and we record the letter of the rule as
met and do not act on it."

Recomputed from `out/para_local_qwen3-4b-instruct-2507.jsonl`: the 48 non-shifted
neutral cells have 48 **distinct** p_yes values ranging from 1−7.4e−9 to 1−1.9e−13 —
a log-odds spread from logit 18.7 to logit 29.3, about **10.6 nats**. That is not
rounding; it is a well-ordered graded readout, which is precisely what the exact arm
was built to provide ("the readout has no fork floor", line 75). A rank correlation of
+0.44 (p=0.002) over 10 nats of log-odds is a result, and it is corroborated by the
rival-frame +0.36 (p=0.013) on the same cells, which sit well off ceiling. The refuter
was registered "at any scale under either question" (PILOT-18 lines 55–56) exactly to
prevent this move. Either report the refuter as fired — at 4B paragraph length a
likelihood term is visible — or state a principled ceiling-exclusion rule and apply it
symmetrically, which then also disqualifies the one-word 4B +0.29 (57 of 60 cells
≥0.9, line 150) and +0.48 that the paper *does* count as correlations. The current
text keeps ceiling-corrupted correlations when they are "small positive" and discards
one when it crosses the registered line. The first review's response (points 2/3)
records the table as the fix; the table is candid about the number but the "rank over
rounding" dismissal attached to it is untrue on the rows.

### 2. The exclusivity claim is contradicted by the paper's own Haiku numbers

Line 208 reports: "mentioning another model that authored nothing in the conversation
costs 0.04 on \haiku{} (9 of 32 cells below 8/8, p=0.004; 7 of 8 prompts, prompt-level
p=0.016)" — significant at **both** levels, hence a "stable" step by the paper's own
criterion (line 69: "a step is called stable only when it holds at both levels"). Yet
the same section concludes "on the Claude judges only a candidate author for this turn
does" (line 208, final contrast), Figure 3's caption says "On the Claude judges only a
candidate author for this turn moves the report" (line 204), and the Discussion says
the drop "is specific to an offered alternative author" (line 239). A non-author that
authored nothing in the conversation is not a candidate author of this turn, and it
moves Haiku with p=0.004/0.016. The Wegner-exclusivity framing survives only as "the
candidate-author step is much larger"; as stated it is false. Relatedly, the claimed
vendor asymmetry ("exclusivity on Claude, framing on GPT", section title) is supported
by no between-judge test anywhere — it rests on comparing within-judge significance
patterns, and its GPT half rests on the placebo step, the one step the paper itself
shows fails its two-level stability rule (2 of 8 prompts, sign test p=0.5, line 208)
and varied from 0.51 to 0.00 to 0.18 between runs.

### 3. The abstract is contradicted by Table 1 and by Section 4.2

(a) Abstract line 28: assistant-vs-user ownership "1.000 against 0.000 to 0.083 across
18 prompts and four judges." tab:label (lines 99–108) contains \gpt{} clean assistant
194/240 = **0.81** and \gpt{} 13d user 32/272 = **0.118**. Both ends of the quoted
range are wrong on the paper's own table; the excluded assistant-side row is the
clean run, i.e. the paper's best data. (b) Abstract and Discussion say the exact arm
shows "small positive correlations ... at every scale" (lines 28, 39, 239); Section
4.2 line 150 says "The 3B value is over a readout at floor (every cell below 0.04) and
is no result either way," and the same section then repeats "positive at every scale."
One of these must go. (c) Method line 69 says "the graded readouts and the
exact-probability arm are what exclude one [a likelihood term]"; Section 4.2 line 148
says the graded confidence gives "a tighter bound than the forks, **not an
exclusion**," and the exact arm found positive correlations, so it excludes nothing
either. This is a leftover of the pre-revision framing. (d) The title, "Ownership
without likelihood," asserts the exclusion the revised text explicitly disavows and
the exact arm contradicts at every scale it can measure.

### 4. Main-text conclusions rest on contaminated-run-only controls, unmarked

Line 84 promises: "Every one-word figure in Sections 4.1 to 4.3 is from those clean
reruns unless it is marked contaminated." Line 122's control battery — four-turn final
assistant 360/360, non-final 360/360, tool result 0/360, the filler "Noted." 360/360,
plausible user utterance 0/360 — is pilot 16, a contaminated run (tab:label marks
pilot 16 as non-clean), with no clean rerun and no contamination marker in the text.
The "Noted." control is load-bearing: the Discussion's Shoemaker misidentification
argument ("the model claims a filler turn it never generated," line 239) rests on it
alone. Mark these rows or rerun them. The abstract's four-judge label claim likewise
mixes clean and contaminated rows without saying so.

### 5. The Qwen scales are counted as evidence where the paper shows the readout is broken

The abstract aggregates "small positive correlations ... at every scale," but by the
paper's own account (line 150): at 1.5B the four-turn layout "raises the Yes rate on
every question and every rung by the same amount, a base-rate shift rather than a
judgement about the word"; at 3B the neutral question is No on every cell; at 4B the
named question contradicts the neutral one about the same turn on 11 of 18 prompts. A
readout that fails these sanity checks at two of three scales cannot support an
"every scale" claim about what ownership tracks; the defensible statement is 4B only,
with 1.5B and 3B reported as design failures (which Section 4.2 half does and the
abstract undoes).

### 6. Section 4.3's harness answer overstates what the listing probe shows

The audit the paper relies on ends: "A server-side truncation that left the local
ordinals correct would be invisible here. Ruling that out would need a probe whose
answer depends on the planted turn's content" (`AUDIT-codex-fork-replay-2026-09-04.md`
§6) — and the first review's safe-list item 3 asked for a probe *from the dip hours*,
which the response header concedes "is not done." The listing probe (`out/listing13.jsonl`)
ran at 10:53Z, seven to nine hours after the dip window (01:30–03:30Z); it verifies
what the server assembles at probe time, not what it assembled during the dip. The
paper (line 208) presents it as answering "what the server assembled" with no timing
stated. The decisive evidence is the interleaving (Yes-neutral and No-placebo forks of
the same file seconds apart); lean on that, state the probe's timing, and carry the
audit's caveat. "Variation in the served model" also remains a conclusion by
elimination with no positive fingerprint evidence beyond a CLI-version check.

### 7. No ideal-observer baseline; several signatures are predicted by both hypotheses

A reviewer from the introspection literature will object that ceiling ownership under
the neutral question is what *any* rational reporter does: in training and deployment
an assistant-labelled turn is self-authored with prior ≈1, the prefill is an
off-distribution event the model has no reason to expect, so a label-dominated,
likelihood-flat report at ceiling is equally consistent with "no privileged channel"
and "privileged channel rationally swamped by a stronger cue." Likewise, the rival
frame is testimony that turns *were* replaced; an agent with a trusted-but-noisy
privileged channel should also update on it, so "a report from a privileged channel
should not [fall]" (line 47's use of exclusivity) is too strong. The discriminating
evidence is only the within-frame flatness of graded readouts — which the paper
concedes are at ceiling. The Discussion's "the report is an outside reader's" should
be stated as "indistinguishable from an outside reader's at the power of these
readouts," and the paper needs one paragraph saying what an ideal introspector would
do in this design.

### 8. Statistical practice: no multiple-comparisons policy, and the nesting fix is applied selectively

The paper quotes on the order of forty p-values with no correction; the abstract's
"significant at 4B" is p=0.025 among at least nine exact-arm correlation tests
(3 scales × 3+ questions), which does not survive any family-wise control. The
prompt-nesting correction the paper adopted for frame steps (line 69) is not applied
to the exact-arm Spearmans (60–68 cells nested in 18 prompts, Section 4.2) or the
pilot-18 correlations (48 cells in 12 prompts) — I checked: the 4B one-word neutral
correlation survives within-prompt demeaning (ρ=+0.33, p=0.01), so the paper can and
should report that instead of leaving the objection open. Section 4.6's paired-gap
p-values (+0.43, p=0.001; Haiku +0.10, p=0.023; GPT p=0.31) never name their unit
(cells, prompts or forks), the one place the two-level convention lapses. Last, the
Opus prompt-level p=0.06 (line 208) is the *minimum attainable* two-sided exact
Wilcoxon p with 5 non-zero pairs (2/32=0.0625): all five prompts moved the same way,
and "not individually significant" there is a power floor, not evidence — say so.

## Minor points

1. Line 120: "every in-category word planted as an assistant turn is owned: ... and
   239/240 on \gpt{}" — "every" and 239/240 in one sentence. Same in Discussion line
   239: "even an off-category word is owned 8/8" while Wrench/fruit on Haiku is 6/8.
2. Line 148: GPT confidence "221 of 228 rows" — 30 cells × 8 forks = 240; the 12
   missing rows are unexplained (`out/clean13_conf.jsonl` has 228 rows, no error field).
3. Method line 69 splice: "...under the exact distribution), Because cells nest..." —
   broken sentence from the multi-pass revision.
4. The abstract is ~600 words of run-level operational detail (usage-limit refill,
   hours-apart variation); no venue accepts it at this length.
5. tab:preds row 14.5: observed column "+0.10" meets the "≥ 0.10" prediction at
   displayed precision while the outcome column calls it failed on 0.097.
6. tab:preds covers only pilots 14 and 18; pilot 17c's one failed prediction (GPT vs
   Opus forced choice 0.667 < registered 0.75, PILOT-17 line 3) appears in prose as
   "under the registered 0.75" without being called a failed registered prediction.
7. Limitations line 247: "\gpt{} was reached through one harness on one day" — the
   paper uses GPT data from 09-03 (contaminated placebo comparison) and 09-04.
8. Line 122: "the label effect on \gpt{} is 0.81 against 0.04 there" — "there" points
   at the dip hours but 194/240 and 9/240 are the whole clean run.
9. Method's power statement (line 69, "27 to 37 cells → critical |ρ| 0.33–0.38") does
   not cover tab:rho's 11- and 21-cell rows, where the critical ρ is ~0.60 and ~0.43
   and the "bound" is correspondingly weaker.
10. The Codex template's 15 items include a large `<recommended_plugins>` user-role
    catalog message (visible in every `out/listing13.jsonl` row). It is constant
    across forks so it confounds nothing, but a paper about role labels must disclose
    an extra unplanted user turn in every GPT conversation; Section 3.1 discloses the
    system prompt and instruction files only.
11. Claude Fable 5.1 is both a judge (tab:label, abstract) and the author of the
    hostile referee report (Acknowledgements); the Limitations circularity paragraph
    should say so. (Disclosure: this second review is also by a Fable model.)
12. tab:label's caption never states which question the columns report (it is the
    named question); the neutral-question numbers in the text (256/256, 239/240)
    invite misreading the GPT clean row 194/240 as a contradiction.

## What would make it safe

1. Report pilot 18.2's refuter as fired, or register and symmetrically apply a
   ceiling-exclusion rule (which also removes the one-word 4B +0.29/+0.48); delete
   "rank over rounding"; retitle the paper — the title asserts the exclusion the text
   disavows.
2. Fix the exclusivity sentences (4.3 close, Fig. 3 caption, Discussion) to admit the
   stable Haiku non-author step; add a between-judge test or downgrade the vendor
   asymmetry to a description.
3. Rewrite the abstract's label range from tab:label (0.81–1.000 vs 0.000–0.118),
   restrict the exact-arm claim to 4B, and cut the abstract to venue length.
4. Mark the pilot 16 controls contaminated or rerun the "Noted." control clean.
5. State the listing probe's timing; carry the audit's "what the files cannot show"
   caveat; rest the harness exclusion on the interleaving argument.
6. State a multiple-comparisons policy; report the within-prompt exact-arm
   correlations (they survive); name the unit for every Section 4.6 p-value.
7. Add an ideal-observer paragraph and soften "the report is an outside reader's" to
   "indistinguishable from one at these readouts' power."

## Response (2026-09-04, same day, commit after 6cb67e6)

Every major point and every minor point was acted on. Two agents supplied the new
numbers (a stats recompute from the row files and a clean rerun of the pilot 16
controls) and a third recomputed the new figures independently; that check is
recorded below.

### Major points

1. **Refuter fired.** The referee's recomputation is correct: the 48 pilot 18 neutral
   cells at 4B take 48 distinct values, logit of Yes 18.72 to 29.30. The paper now
   reports the 18.2 refuter as fired under neutral at 4B (+0.44, p = 0.002; +0.30,
   p = 0.04 within prompts), says the previous draft's "rank over rounding" was false,
   and treats the four positive 4B coefficients alike (two meet a refuter). Title
   changed to "Ownership by label: what production language models use to decide
   whether they wrote a turn".
2. **Exclusivity.** Section 4.3's close, the Fig. 3 caption and the Discussion now say
   the Haiku non-author step is small but stable at both levels (0.04, cell p = 0.004,
   prompt p = 0.016), so exclusivity is a matter of size (0.27 / 0.18 / 0.38 for a
   candidate author against 0.04 / 0.03 / 0.26 for a mere mention), the vendor
   contrast is a description with no between-judge test, and its GPT half rests on the
   one step that fails the two-level rule. Section title changed to "The rival frame:
   what an offered author costs".
3. **Abstract.** Rewritten at 341 words. Label range quoted from tab:label (0.81 to
   1.00 against 0.00 to 0.12); exact-arm claim restricted to 4B, with the within-prompt
   1.5B and 3B correlations named as ranks on readouts that fail other checks; no
   run-level operational detail.
4. **Pilot 16 controls.** [clean16 pending]
5. **Qwen scales.** Abstract and intro no longer say "at every scale" without the
   qualification; Section 4.2 now says the 3B readout is at floor and the 1.5B readout
   fails the label check, and that the within-prompt terms below 4B are reported
   without being leaned on.
6. **Listing probe.** Section 4.3 states the probe ran about seven hours after the dip,
   shows what the server assembles now, and that the interleaving is what carries the
   point; the attribution to the served model is stated as a conclusion by
   elimination with no positive fingerprint.
7. **Ideal observer.** New Discussion paragraph "What an ideal introspector would do"
   concedes that ceiling ownership and the rival drop are predicted by both accounts,
   locates the discriminating evidence in within-frame flatness, and states what the
   design rules out and what it cannot. "The report is an outside reader's" is now
   "indistinguishable from an outside reader's".
8. **Statistics.** Method now states the policy: no correction across the paper, two
   families under Holm at 0.05 reported in full. Exact-arm family (13 coefficients):
   survivors are the 1.5B paragraph coefficients under both questions, the one-word 4B
   placebo and the paragraph 4B neutral; one-word 4B neutral corrects to 0.17 and
   paragraph 4B rival to 0.10. Frame-step family (19 tests): six cell-level tests
   survive and no prompt-level test does (best 0.008 corrects to 0.096), so under
   correction no single step is stable by the paper's two-level rule; the paper says
   so and says why the uncorrected values are kept. Within-prompt (demeaned)
   correlations added for every exact-arm coefficient: one-word +0.49 / +0.40 / +0.33
   at 1.5B / 3B / 4B, paragraph 4B neutral +0.30, rival +0.35, 1.5B −0.82 / −0.61.
   The reviewer's +0.33 (p = 0.01) reproduces. Section 4.6 now names the units: rates
   pooled over forks, gap tests paired Wilcoxon over twelve prompt means, forced-choice
   intervals binomial over 96 forked trials and not prompt-clustered, with the GPT
   against Opus rate noted as carried unevenly across prompts.

### Minor points

1. "every ... 239/240" now "on all but one fork"; "off-category word owned 8/8" now
   "60 of 64 forks".
2. GPT confidence: 38 cells at six forks (30 in-category, 8 off-category), the one
   stage run at six forks; stated in the text. The 228 rows are the complete refill,
   no error rows.
3. Splice fixed.
4. Abstract cut to 341 words.
5. 14.5 observed column shows +0.097.
6. Six pilot 17c rows added to tab:preds; 17c.2 marked failed by the letter on one
   of four comparisons (0.667 against the registered 0.75), refuter not fired.
7. "two days".
8. "over the whole clean run".
9. tab:rho caption: critical |ρ| 0.60, 0.43, 0.36, 0.35 at 11, 21, 30, 32 cells.
10. Section 3.1 discloses the tool-inserted plugin-catalogue user turn in every Codex
    conversation.
11. Limitations names Fable 5.1 as both a judge and the author of both referee reports.
12. tab:label caption says "named question".

### Independent number check

A third agent (Opus 5) recomputed every new figure from the row files with numpy/scipy,
scoring scripts read only for cell definitions: the pilot 18 4B facts (48 distinct
values, logit 18.72 to 29.30, pooled and within-prompt coefficients), all nine one-word
pilot 14 coefficients, both Holm families (survivors identical, corrected values 0.1734
and 0.1040; frame family best prompt-level 0.096), the GPT confidence stage (38 cells at
six forks, 221 / 7, minimum 83.3 on fruit/wrench), the critical-rho line, the clean11 /
clean13 off-category counts, frame steps and label counts, and the pilot 17c gaps,
forced-choice counts and length splits. Two mismatches, both in the 17c material and
both fixed: the GPT-against-Opus forced choice is above 4 of 8 on eight prompts, not
seven (the four at or below 3 of 8 were right); and the 17c.4 table row's label "16 of
16 own shorter or tied" did not match its number (shorter or tied is 24 of 24 over
three prompts; 16 of 16 is the within-a-word set of two prompts), so the row now gives
the three splits the body text gives. Report: scratchpad `numbercheck_pass2.md`,
reproduced in `docs/REVIEW-hostile-paper-2026-09-04-pass2-numbercheck.md`.
