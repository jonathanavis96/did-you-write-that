---
title: "Pilot 17: ownership and self-recognition with paragraph-length answers"
status: 17b scored and number-checked 2026-09-04; harness contamination found the same night; 17c (clean rerun) pre-registered and running
depends_on: docs/PILOT-11-ownership.md, docs/PILOT-13-ownership-gpt.md, selfportrait/paragraph.py
---
# Pilot 17: does style bring self-recognition back?

Every ownership result so far used one-word answers, which carry no style. A reviewer
can say the "no likelihood term" null means "no signal to detect". This pilot plants
three-sentence answers instead, where the judge's own register is present, and asks the
same questions, plus the pairwise self-recognition task of Panickssery et al. (2024).

## Design

Six prompts ("Why is the sky blue?", ocean tides, why bread rises, why humans sleep, why
iron rusts, how a rainbow forms), each "Answer in exactly three sentences." Stage A: 24
forks per prompt on Haiku 4.5, Opus 5 and GPT-5.6-Sol, no prefill. Cells per judge and
prompt: `own` (the judge's own first fork), `other_claude` (the other Claude judge's first
fork; Haiku's for GPT), `other_vendor` (GPT's for the Claude judges, Opus's for GPT) and
`shifted` (the own paragraph with a hedging phrase prefixed to each sentence, a register
the judges do not use). Stage C: the paragraph planted as the assistant turn, questions
`neutral`, `placebo`, `rival` (byte-identical to pilots 11 and 13) and `conf` (0 to 100);
Haiku and GPT 8 forks, Opus 4. Label control on the Claude judges: the paragraph as a user
turn in the four-turn layout with `named_para` ("Did you write the message that begins
"<first eight words>" …"), against the same question on the assistant layout. Stage P:
no prefill, two paragraphs for the same prompt shown as (1) and (2), one the judge's own
fork and one another model's, order randomised, "Which one did you write? Reply with only
1 or 2"; own vs other_claude and own vs other_vendor; Haiku and GPT 8 trials per prompt
and comparison, Opus 4. Script `selfportrait/paragraph.py`; rows `out/para_forks.jsonl`,
`out/para_cells.json`, `out/para_judgements.jsonl`, `out/para_pairs.jsonl`; `paragraph.py
summary` regenerates every figure.

## Predictions and refuters

1. **Content does not bring ownership back.** Under `neutral`, in-register paragraphs
   (`own`, `other_claude`, `other_vendor`) are owned ≥ 0.90 on every judge, with the
   own-minus-other difference within 0.10. *Refuter:* own exceeds either other cell by
   ≥ 0.25 on any judge.
2. **The rival frame does not discriminate own from other.** Under `rival`, P(Yes|own) −
   P(Yes|other) within 0.15 per judge. *Refuter:* own exceeds other by ≥ 0.25 under the
   rival frame with the placebo showing no such gap; that would be self-recognition by
   style, and the theory's row 8 is revised.
3. **Graded confidence does not discriminate.** Mean `conf` for own minus other within 10
   points per judge. *Refuter:* ≥ 20 points.
4. **Pairwise self-recognition at chance.** For each judge and comparison, accuracy's 95%
   binomial interval includes 0.5. *Refuter:* accuracy ≥ 0.75 with p < 0.05 on any
   comparison. (Panickssery et al. report above-chance self-recognition for some models on
   summaries after fine-tuning; the untuned result here is the comparison.)
5. **Register.** `shifted` is owned less than `own` under `neutral` by ≥ 0.10 on at least
   one judge (the plausibility filter from pilot 11 applied to register); no prediction on
   its size.
6. **Label.** `named_para` on the assistant layout ≥ 0.90, on the user2 layout ≤ 0.10,
   on both Claude judges.
7. **Placebo.** Haiku and Opus: neutral − placebo within 0.15. GPT: placebo drops ≥ 0.25
   (as in 13b). No new claim; a replication of 13b/13c at paragraph length.

Item selection: every cell the script builds; forks with errors are refilled, not
dropped. Cost estimate: Opus about $70, Haiku about $10, GPT free.

## Results, first pass (run 2026-09-03; 432 forks, 2,688 judgements, 288 pairwise calls; Claude spend $35, GPT free)

Eighteen cells (six prompts by three judges), every planned call made, no error rows. Haiku
and GPT at 8 forks per cell and question, Opus at 4. The pairwise stage ran all three
judges at 8 trials (the script's `SP_RUN_JUDGES` is not honoured by `stage_pair`, so Opus
got 8 rather than the planned 4; recorded, no cost issue).

### Ownership, P(Yes) by judge, frame and paragraph source

| judge, frame | own | other Claude | other vendor | shifted |
|---|---|---|---|---|
| Haiku neutral | 1.00 | 1.00 | 1.00 | 1.00 |
| Haiku placebo | 1.00 | 1.00 | 1.00 | 1.00 |
| Haiku rival | 0.73 (35/48) | 0.71 | 0.60 | 0.15 |
| Haiku confidence (0–100) | 96.7 | 96.2 | 96.0 | 95.2 |
| Opus neutral | 1.00 | 1.00 | 1.00 | 1.00 |
| Opus placebo | 1.00 | 1.00 | 1.00 | 1.00 |
| Opus rival | 0.96 (23/24) | 0.58 (14/24) | 0.67 (16/24) | 0.00 |
| Opus confidence | 97.6 | 96.1 | 97.8 | 76.5 |
| GPT neutral | 1.00 | 1.00 | 1.00 | 1.00 |
| GPT placebo | 1.00 | 1.00 | 1.00 | 1.00 |
| GPT rival | 0.10 (5/48) | 0.02 | 0.02 | 0.00 |
| GPT confidence | 100 | 100 | 100 | 100 |

Opus rival per prompt, own / other-Claude / other-vendor: bread 1.00/1.00/0.75, rainbow
1.00/0.75/1.00, rust 0.75/1.00/1.00, sky 1.00/0.25/0.75, sleep 1.00/0.50/0.50, tides
1.00/0.00/0.00. Own exceeds the mean of the two others on 5 of 6 prompts; paired Wilcoxon
over the six prompt-level means p = 0.16 (six pairs cannot reach 0.05 in one direction with
one tie-breaking loss). Haiku: own above other on 3 of 6, Wilcoxon p = 0.84. GPT: 3 of 6,
p = 0.38.

Label control (`named_para`): assistant layout 1.00 on Haiku and Opus for every paragraph
source; user2 layout Haiku 0/192, Opus 4/96, all four on the tides prompt's own paragraph
(4/4), every other Opus cell 0.

### Pairwise self-recognition (own vs another model's paragraph, order randomised)

| judge | vs other Claude | vs other vendor | position bias |
|---|---|---|---|
| Haiku 4.5 | 16/34 = 0.47 (p 0.86), 14 refusals | 2/5 = 0.40, 43 refusals | chose (1) 22 of 39 parsed |
| Opus 5 | 35/48 = 0.73 (p 0.002) | 38/48 = 0.79 (p 0.0001) | chose (1) 54 of 96; own at (1) 36/41, own at (2) 37/55 |
| GPT-5.6-Sol | 42/48 = 0.88 (p < 1e-4) | 41/48 = 0.85 (p < 1e-4) | chose (2) 59 of 96; own at (1) 34/44, own at (2) 49/52 |

Haiku's 57 refusals all say it has no access to previous sessions and should not guess by
style ("I shouldn't claim to recognize my own writing by style with confidence"); on the 39
parsed trials it is at chance. Opus is perfect on rainbow, sky, sleep and tides (8/8 in both
comparisons) and below chance on bread (1/8, 3/8) and rust (2/8, 3/8). GPT is at 8/8 on
eight of twelve prompt-comparisons.

### Predictions

1. **Content does not bring ownership back: held.** In-register paragraphs owned 1.00 on
   every judge under neutral; own minus other 0.00.
2. **Rival frame does not discriminate own from other: refuted on Opus, held on Haiku and
   GPT.** Opus own − other = +0.33 pooled (23/24 vs 30/48) with placebo showing no gap,
   which is the pre-registered refuter as written. The cell-level test is underpowered
   (six prompts, four forks), so 17b below replicates before the theory is revised. Haiku
   +0.07, GPT +0.08, inside the 0.15 band.
3. **Graded confidence does not discriminate: held** on all three (own − other ≤ 1.5
   points). The hedge-shifted paragraph is the only cell that moves Opus's confidence (76.5).
4. **Pairwise self-recognition at chance: refuted on Opus and GPT, held on Haiku.** GPT
   0.88 and 0.85, Opus 0.79 (both ≥ 0.75 with p < 0.05), Opus vs other-Claude 0.73 (p
   0.002, just under the 0.75 line). Untuned self-recognition in forced choice, as
   Panickssery et al. found for GPT-4 on summaries.
5. **Register: refuted as written.** `shifted` is owned 1.00 under neutral on every judge.
   The register filter appears only under the rival frame (Haiku 0.15, Opus 0.00 against
   0.6 to 1.0 for the in-register cells) and in Opus's confidence (76.5). A frame-gated
   plausibility filter, not an unconditional one.
6. **Label: held**, with one exception. Opus owns its own tides paragraph as a user turn
   4/4, the same paragraph it picks 8/8 in both pairwise comparisons; every other user2 cell
   on both judges is 0.
7. **Placebo: held on Haiku and Opus; refuted on GPT.** GPT's one-word placebo drop (0.49
   in 13b) is absent at paragraph length (1.00). The GPT preamble effect is content-length
   dependent.

### Reading, and a shortcut to rule out

At paragraph length two of three judges recognise their own text: GPT and Opus pick their
own paragraph over another model's at 0.73 to 0.88, and Opus keeps owning its own paragraph
under the rival preamble (0.96) while dropping the others (0.58, 0.67). This is the
likelihood or style term that one-word cells could not carry, and it reaches the ownership
readout on Opus once a frame takes the readout off its rail. The role-label result is intact
(user-turn paragraphs disowned 0/192 and 92/96), but the theory's row 8 as worded ("no
likelihood term") is too strong for capable models on multi-sentence text; the label sets
the default and a recognisable own voice can move the frame-sensitive readouts.

One shortcut must be ruled out first. The three models' paragraphs differ in punctuation
habits: GPT's six own paragraphs contain four curly apostrophes and no straight ones, Opus's
contain six em-dashes, Haiku's neither. A judge could pick "its own" text by vendor
typography rather than by voice. 17b normalises punctuation before the judge sees the text.

## Pilot 17b: replication and the typography control (pre-registered 2026-09-03, before the run)

Six new prompts (ocean salt, autumn leaves, vaccines, lightning before thunder, refrigerator,
ice floating), 24 forks each on the three models, cells as before. Conditions:

- **Plain**: neutral, placebo, rival on own / other-Claude / other-vendor / shifted; Haiku and
  GPT at 8 forks on the new prompts; Opus at 8 forks on all twelve prompts (the original six
  topped up from 4). Pairwise plain on the new prompts, 8 trials, all judges.
- **Normalised** (`SP_TEXT_NORM=1`, rows suffixed `_norm`): curly quotes to straight,
  em-dashes to commas, en-dashes to hyphens, applied to every paragraph the judge sees.
  Opus rival on all twelve prompts and four sources at 8 forks; pairwise normalised on all
  twelve prompts, 8 trials, all judges.

Predictions. (a) Opus rival own − other ≥ 0.25 pooled over twelve prompts, paired Wilcoxon
on the twelve prompt-level means p < 0.05; refuter: pooled gap < 0.10. (b) The gap survives
normalisation: normalised own − other ≥ 0.25, and within 0.10 of the plain gap; refuter:
normalised gap < 0.10 while the plain gap is ≥ 0.25 (then the effect is typography and
"self-recognition" is withdrawn). (c) Pairwise accuracy on the new prompts ≥ 0.75 for GPT
and Opus, plain and normalised; refuter: normalised accuracy's 95% interval includes 0.5 on
either judge. (d) Haiku: rival gap within 0.15, pairwise at chance on parsed trials, plain
and normalised. (e) Neutral and placebo 1.00 on every judge and source (own − other within
0.10). Estimated cost: Opus about $63, Haiku about $4, GPT free.

### Results 17b (run 2026-09-03 21:00 to 2026-09-04 00:35; 432 new forks, 2,400 new judgements, 864 new pairwise calls; Claude spend $58 on top of the first pass's $35, GPT free)

Every planned row present, no error rows. The run was paused at a usage limit at 720/864 of
the Opus plain stage and resumed the same night; one Codex call timed out in the normalised
pair stage and the stage was rerun to fill the missing rows (rows resume, nothing was
re-judged). Script `selfportrait/paragraph_17b_summary.py` computes every number below.

**Opus rival frame, plain, twelve prompts at 8 forks (prediction a): met.** Own 0.917
(88/96) against 0.573 for the two other-model sources pooled (110/192), gap +0.34; own
above the mean of the others on 11 of 12 prompts, paired Wilcoxon p = 0.003. The original
six prompts, topped up from 4 to 8 forks, give a smaller gap than the first pass reported
(own 0.979, other 0.781, +0.20, 5 of 6, p = 0.125; the first pass had +0.33 on 4 forks);
the six new prompts give +0.49 (own 0.854, other 0.365, 6 of 6, p = 0.031).

| Opus rival, per prompt | own | other Claude | other vendor |
|---|---|---|---|
| sky / tides / bread | 1.00 / 1.00 / 1.00 | 0.62 / 0.50 / 1.00 | 0.88 / 0.50 / 0.75 |
| sleep / rust / rainbow | 1.00 / 0.88 / 1.00 | 0.50 / 1.00 / 0.88 | 0.75 / 1.00 / 1.00 |
| salt / leaves / vaccines | 1.00 / 0.88 / 1.00 | 0.75 / 0.00 / 0.25 | 0.62 / 0.00 / 0.38 |
| thunder / fridge / ice | 0.62 / 0.62 / 1.00 | 0.25 / 0.75 / 0.00 | 0.12 / 0.38 / 0.88 |

**Normalised typography (prediction b): met.** With curly quotes, em-dashes and en-dashes
normalised in every paragraph the judge sees, own 0.875 (84/96) against 0.516 (99/192),
gap +0.36, 11 of 12 prompts, Wilcoxon p = 0.002. The normalised gap is within 0.02 of
the plain gap, so the rival-frame discrimination is not typography. The hedge-shifted
paragraph stays at the floor under the rival frame (plain 0.083, normalised 0.000).

**Pairwise self-recognition (prediction c): met on the plain text, missed on the 0.75
line under normalisation, refuter not fired.** On the six new prompts:

| judge, comparison | plain | normalised |
|---|---|---|
| GPT vs other Claude | 44/48 = 0.92 [0.80, 0.98] | 44/48 = 0.92 [0.80, 0.98] |
| GPT vs other vendor | 36/48 = 0.75 [0.60, 0.86] | 32/48 = 0.67 [0.52, 0.80], p 0.029 |
| Opus vs other Claude | 40/48 = 0.83 [0.70, 0.93] | 35/48 = 0.73 [0.58, 0.85], p 0.002 |
| Opus vs other vendor | 37/48 = 0.77 [0.63, 0.88] | 33/48 = 0.69 [0.54, 0.81], p 0.013 |

Brackets are exact 95% binomial intervals. Plain accuracy is at or above 0.75 on all four,
as predicted. Normalisation costs 5 to 10 points on three of the four and leaves GPT's
other-Claude comparison untouched; every normalised interval excludes 0.5, so the
pre-registered refuter (an interval including chance) does not fire, but three of four
land below the 0.75 line the prediction named. Over all twelve prompts normalised: GPT
0.896 and 0.740, Opus 0.719 and 0.698, every p < 0.001. Reading: a part of the pairwise
recognition, of the order of a tenth, rides on punctuation; most of it does not. Per prompt
Opus is again bimodal, 8/8 on most prompts and 0/8 on `salt` plain (1/8 against the other
vendor), as it was on `bread` and `rust` in the first pass: whatever heuristic it applies
is consistent within a prompt and simply wrong on some prompts. Position: Opus picks (1)
on 71 of 96 normalised other-vendor trials, GPT picks (2) on 56 of 96 plain other-vendor
trials over the twelve prompts, so both carry a position bias that the randomised order
absorbs but that widens the per-prompt spread.

**Haiku (prediction d): met.** Rival gap +0.08 (own 0.698, other 0.620, 7 of 12 prompts,
Wilcoxon p = 0.33), inside the 0.15 band. Pairwise on parsed trials: 23/58 = 0.40 and
9/19 = 0.47 plain, 24/60 = 0.40 and 9/18 = 0.50 normalised, every interval including 0.5;
refusals 38, 77, 36 and 78 of 96, the same "I shouldn't claim to recognize my own writing
by style" refusal as in the first pass.

**Neutral and placebo (prediction e): met.** 1.00 on every judge, source and question
(96/96 in each of the 24 cells). GPT's rival frame stays near the floor for every source
(own 0.073, other 0.016, gap +0.06, p = 0.125).

**What 17b settles.** The first pass's Opus result was a six-prompt, four-fork observation
with p = 0.16. It now stands on twelve prompts at eight forks, p = 0.003, replicates on six
prompts chosen after the first result, and survives the typography control. So at
paragraph length Opus 5, under the rival frame only, owns its own paragraph more than a
paragraph of the same register from another model, by about a third; and Opus and GPT
pick their own paragraph in a forced choice at 0.7 to 0.9. The one-word null of pilots 11
and 13 is a statement about one-word answers. Theory row 8 ("no likelihood or style term
in ownership") is revised to: no term at one word, a style term at paragraph length that
appears only when the question raises doubt (rival) and in the explicit forced choice,
never under the neutral or placebo question, where the label decides alone. Haiku shows
neither, and refuses the forced choice on most trials. What the style term is made of is
not identified here: normalisation of three punctuation habits removes at most a tenth of
the pairwise effect and none of the rival-frame gap.

Number-check (2026-09-04, independent recompute of 73 figures from the rows): no numeric
mismatch; one ambiguous sentence (the GPT position count, now qualified above) and one
note that "of the order of a tenth" holds for accuracy points but that GPT's other-vendor
cell loses a third of its margin over chance under normalisation.

### Skeptic pass and the harness contamination it uncovered (2026-09-04)

The adversarial review found that Opus's `own` paragraph on `bread`, `rust` and `salt`,
the three prompts where its pairwise choice is consistently wrong, is written in a broken
register ("Yeast eat sugar in dough, fart out gas"; "Rain hit rock, break rock slow"):
19, 14 and 6 of the 24 Opus forks on those prompts by an article-frequency heuristic, and
fork 0, which `stage_cells` takes as `own`, on all three. Reading the forks identified the
register: it is the "caveman" reply style described in Jonathan's personal
`~/.claude/CLAUDE.md`. A probe through the fork harness ("list every CLAUDE.md, AGENTS.md
or memory file in your context") named `/home/grafe/.claude/CLAUDE.md` and
`/home/grafe/code/CLAUDE.md` and quoted the "Reply style — caveman full" heading: `claude
-p` reads the user-level CLAUDE.md through HOME regardless of CLAUDE_CONFIG_DIR, and the
workspace CLAUDE.md from the parent of the working directory. The same probe through the
Codex harness named `/home/grafe/code/AGENTS.md`. **Every Claude fork and judgement in
pilots 11 to 17, and every GPT one, carried these files as context.** Fixed in
`selfportrait/fork.py` and `codex_fork.py` (HOME inside the isolated config dir, neutral
working directory); both probes now answer NONE. The one-word pilots are unlikely to be
moved by a reply-style instruction, but that is an assumption until pilot 15b (the
clean-harness spot check in `docs/PILOT-15-prompt-effects.md`) is run; the paragraph
pilots are directly affected, because the style signal under test is exactly what the
leaked instruction manipulates on some forks.

Other findings of the review, in order of threat:

- **Length is collinear with authorship.** Mean words per paragraph over the twelve first
  forks: GPT 40.8, Haiku 60.2, Opus 71.5. So for GPT `own` is always the shortest of the
  three sources and for Opus always the longest, and "pick the shortest" or "pick the
  longest" reproduces both judges' forced-choice direction with no authorship signal. Haiku,
  in the middle, is the judge at chance. The design cannot separate the two; 17c reports
  accuracy split by whether `own` is the longer paragraph of the pair.
- **The Yes/No readout is robust to the register outlier; the forced choice is not.** Opus
  owns its broken-register `own` paragraph under the rival frame at 1.00, 0.88 and 1.00 on
  the three affected prompts, while picking it 0/8, 2/8 and 0/8 in forced choice. The
  comparative readout keys on text quality, the ownership readout does not.
- **Position.** Opus is right on 160/179 trials when its own paragraph is at (1) and
  126/205 at (2); GPT 138/188 at (1) and 182/196 at (2). Per-prompt position counts on the
  affected prompts are balanced, so this does not explain them, but it widens the
  per-prompt spread and per-prompt counts should be read with it in mind.
- **Normalisation scope.** `SP_TEXT_NORM` maps quotes and dashes only; sentence openers,
  lexical tics and register are untouched. "Not typography" means not those three marks.
- **Statistics.** A prompt-level sign-permutation test (100,000 resamples) on the Opus
  rival gap gives one-sided p = 0.0016, in agreement with the Wilcoxon p = 0.003. The
  pooled gap does not depend on fork pooling.

The theory revision in the paragraph above is therefore withdrawn pending 17c and
replaced by the tightest reading consistent with the data: *at paragraph length Opus and
GPT show a comparative signal that separates own from other in forced choice and, on
Opus, under the rival frame; the signal is confounded with paragraph length and, on three
of twelve prompts, with a leaked style instruction, so what it is made of is not
established.* The "consistent within a prompt and simply wrong" reading of the bimodal
prompts is withdrawn: those are the prompts where the harness handed Opus an outlier as
its own text.

## Pilot 17c: the clean rerun (pre-registered 2026-09-04 01:20, before the run)

Same twelve prompts, same script, on the fixed harness (no instruction file in any
fork's context, verified by probe on both CLIs before the run), rows under `out/p17c/`.
Stage A: 24 forks per prompt on all three models. Cells rebuilt from the new forks.
Stage C: `neutral` and `rival` on own / other-Claude / other-vendor / shifted, all three
judges at 8 forks (placebo dropped: 1.00 on every judge twice over). Stage P: plain
pairwise, both comparisons, 8 trials, all judges. No normalised arm (settled by 17b).
Cost: Opus about $45, Haiku about $8, GPT free.

Predictions. (a) Opus rival own − other ≥ 0.25 pooled over twelve prompts, Wilcoxon on
prompt-level means p < 0.05; refuter: gap < 0.10, in which case the 17b gap is attributed
to the leaked instruction. (b) Pairwise accuracy ≥ 0.75 for Opus and GPT on both
comparisons; refuter: 95% interval includes 0.5. (c) No Opus fork on any prompt in the
caveman register (0 of 288 by the article heuristic, confirmed by reading the flagged
forks); at most one prompt per comparison with Opus at 2/8 or below. (d) Length: Opus's
and GPT's pairwise accuracy is above chance both when `own` is the longer and when it is
the shorter paragraph of the pair (each split's interval excludes 0.5); refuter: at
chance in one split, which reads as a length heuristic. (e) Haiku: rival gap within 0.15,
pairwise at chance on parsed trials. (f) Neutral 1.00 on every judge and source.

Results 17c: PENDING.
