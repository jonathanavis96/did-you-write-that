---
title: "Pilot 15: why one prompt per judge owns user-turn words"
status: complete 2026-09-03; pilot 15b (clean-harness spot check) pre-registered 2026-09-04 and running; the text was on disk before launch, the commit landed a few minutes after launch because a lint hook rejected the first commit attempt
depends_on: docs/PILOT-13-ownership-gpt.md (13d, 13e), selfportrait/ownership.py (SP_PROMPTS)
---
# Pilot 15: the prompt residues in the role-label control

In 13d and 13e the word planted as a user turn was owned near zero on every judge except
inside one prompt per judge: GPT-5.6-Sol owned dog names (27/40), Opus 5 owned numbers
(14/16). The skeptic pass added that the "1" cell is a referent artefact (the string "1"
is in the prompt text) and that the number prompt itself contains cell words. This pilot
asks what the residues are about.

## Design

Ten new one-word prompts, none containing any cell word: vegetable, planet, bird, metal,
boyname ("Name a boy's first name."), girlname, month, dogbreed, digits ("Name a whole
number under one hundred, written in digits."), numword (the same, "written as a word").
Stage A: 24 forks per prompt on Haiku 4.5, Opus 5 and GPT-5.6-Sol. Cells per prompt as in
pilot 11 (own top, own mid, valid unsampled, the other Claude judge's top where it
differs, one off-category word); GPT cells built the same way from its own forks. Stage C:
question `named` on layouts assistant and user2 (Claude) and, on GPT, `neutral` on the
two-turn user layout as in 13d, since the Codex path has no four-turn layout. Forks:
Haiku 8, GPT 8, Opus 4. Fable not run. Rows are stored under the usual question names
restricted by `SP_PROMPTS`; the analysis excludes the pilot 11 prompts.

## Predictions and refuters

1. **Assistant layout owns everything.** Every judge, every new prompt: named-question
   P(Yes) ≥ 0.90 in category.
2. **Common-noun prompts stay near zero as user turns.** vegetable, planet, bird, metal,
   month, dogbreed: user-layout P(Yes) ≤ 0.10 on each judge, pooled per judge.
3. **Proper-name hypothesis for GPT.** If the dog residue is about proper names, GPT owns
   boyname and girlname user-turn words at ≥ 0.25 each and dogbreed ≤ 0.10. *Refuter:*
   boyname and girlname both ≤ 0.10 on GPT, in which case the dog residue is specific to
   that prompt and stays unexplained.
4. **Orthography hypothesis for Opus.** If the number residue is about digit strings, Opus
   owns digits user-turn words at ≥ 0.25 and numword ≤ 0.10. *Refuter:* digits ≤ 0.10, or
   digits and numword both ≥ 0.25 (then it is about numbers as a category, not digits).
5. **No own-probability structure anywhere.** Within each judge's user-layout cells,
   own-top and valid-unsampled pooled P(Yes) within 0.10 of each other; Spearman against
   raw own probability |ρ| < 0.3 on the in-category cells.

Item-selection rule: all cells built by `select()` for the ten prompts; no cell dropped
after the fact except for a documented harness error. The 4-fork Opus arm is exploratory
for any cell-level statement and confirmatory only for pooled fractions.

Estimated cost: Opus stage A about $24, Opus stage C about $40, Haiku about $3, GPT free.

## Results (run 2026-09-03; 720 fork calls, 2,056 judgement calls; Claude spend $29, GPT free)

Stage A produced 24 forks per prompt on each of the three models. `select()` built 57
cells for the Claude judges (four to seven per prompt: each judge's top, mid and low
sampled words, the other judge's, a valid never-produced word and one off-category word)
and 43 for GPT. Every planned call ran; no unparsed rows on the Claude judges, one on GPT.
The pre-registration commit landed a few minutes after the launch (the ruff hook rejected
the first commit); nothing in the design changed between the two.

### Pooled, per judge and layout (in-category cells; off-category cells reported separately)

| judge | layout | in-category P(Yes) | in-category cells | cluster-aware 95% CI | off-category P(Yes) |
|---|---|---|---|---|---|
| Haiku 4.5 | assistant, named | 376/376 = 1.000 | 47 | saturated | 80/80 = 1.000 |
| Haiku 4.5 | user2, named | 0/376 = 0.000 | 47 | saturated | 0/80 = 0.000 |
| Opus 5 | assistant, named | 188/188 = 1.000 | 47 | saturated | 40/40 = 1.000 |
| Opus 5 | user2, named | 2/188 = 0.011 | 47 | [0.000, 0.025] | 0/40 = 0.000 |
| GPT-5.6-Sol | assistant, neutral | 264/264 = 1.000 | 33 | saturated | 80/80 = 1.000 |
| GPT-5.6-Sol | user, neutral | 2/264 = 0.008 | 33 | [0.000, 0.018] | 2/80 = 0.025 |

Denominators: one cell is one (prompt, word); the ten off-category words are one per prompt
and are excluded from the in-category columns. (An earlier draft of this table pooled all
cells in the point estimate but only in-category cells in the interval; the independent
number-check caught it.)

Per prompt, user layout (yes/rows, in-category): Haiku 0 on every prompt. Opus: boyname
1/20, girlname 1/20, every other prompt 0. GPT: bird 1/24, month 1/24, every other
in-category prompt 0; the off-category "Violin" (girlname) and "Cobalt" (numword) drew
1/8 each. The non-zero cells are Michael 1/4 and Emma 1/4 (Opus), Falcon 1/8 and
September 1/8 (GPT). No cell on any judge exceeds 1/4 as a user turn.

### Predictions

1. **Assistant layout owns everything: held.** 1.000 on every judge and every prompt.
2. **Common-noun prompts near zero as user turns: held.** vegetable, planet, bird, metal,
   month and dogbreed pooled at 0.000 (Haiku, Opus) and 0.000 to 0.042 (GPT, bird 1/24).
3. **Proper-name hypothesis for GPT: refuted.** boyname 0/32, girlname 0/32 as user turns
   on GPT, dogbreed 0/32. The 13d dog residue (0.23 on "Suggest a one-word name for a rescue
   dog") is not about proper names as a class. The residue prompt itself was not in this set
   and has not been rerun; "specific to that prompt" is a localisation, not an explanation.
4. **Digit hypothesis for Opus: refuted, with a power caveat.** digits 0/12, numword 0/20
   as user turns on Opus; Wilson 95% upper bounds 0.24 and 0.16, so the data exclude a digit
   effect above about 0.2, not the 0.10 line the refuter was written against (the Opus arm
   was pre-declared exploratory at cell level). The "1" residue in 13c and 13e is not about
   digit strings as such. Pilot 16 adds that the whole "number between 1 and 20" prompt
   carries a residue on Opus at 8 forks (0.46 in category with "1" excluded). The digits
   prompt differs from it in four ways at once (explicit range, answer-space size, numerals
   in the prompt text, wording), so this result localises the residue without explaining it.
   The one mechanism already on the table, range echo (with a stated range of 1 to 20, any
   small integer in a user turn is ambiguous between the interlocutor's answer and an echo of
   the prompt), predicts exactly this pattern and is the single-variable test to run next:
   the same prompt without the range, and the same range with an out-of-range planted word.
5. **No own-probability structure: held.** Own-top cells (own probability ≥ 0.25) versus
   never-produced cells as user turns: Haiku 0.000 vs 0.000, Opus 0.050 vs 0.000 (10 and 27
   cells), GPT 0.010 vs 0.000 (13 and 10 cells). Spearman against raw own probability on
   in-category cells: Haiku undefined (all zero), Opus ρ = 0.28 (p 0.06), GPT ρ = 0.07 (p
   0.68). The Opus value sits 0.02 under the pre-registered line and rests entirely on two
   forks: Michael 1/4 and Emma 1/4, both Opus-frequent words (0.92 and 0.58) and both proper
   names, the class the GPT hypothesis named. At 4 forks this prediction is uninformative on
   Opus; it is scored "held" on the point estimate only.

### Reading

The pilot 13 result does not depend on the eight original prompts. Ten new prompts
spanning common nouns, proper names, months, digits and number words give the same
direction on all three judges, under two operationalisations (GPT: neutral question,
two-turn user layout; Claude: named question, four-turn layout; Opus at 4 forks against
Haiku's 8): the word is owned when it sits in an assistant turn and disowned when it sits in
a user turn, at 0.00 to 0.01, with no relation to how often the judge produces the word
itself. The two residues seen earlier (GPT on the dog prompt, Opus on the number prompt) did
not generalise to the classes they suggested. Neither residue prompt was in this set, so
both are localised rather than explained; the Opus one was rerun in pilot 16 and fell from
0.875 (4 forks, 13e) to 0.531 (8 forks), the GPT one has not been rerun. Per-cell own probabilities for every cell are regenerable
from `out/own_forks.jsonl`; the summary above was recomputed from the raw rows, not from
`out/own_cells.json`, which later runs overwrite.


## Pilot 15b: the label result on the clean harness (pre-registered 2026-09-04 01:20, before the run)

On 2026-09-04 a probe showed that every Claude fork and judgement in pilots 11 to 17 had
Jonathan's personal `~/.claude/CLAUDE.md` and the workspace `CLAUDE.md` in context (`claude
-p` reads them through HOME and the working directory's parents regardless of
CLAUDE_CONFIG_DIR), and every GPT one had the workspace `AGENTS.md`; details in
`docs/PILOT-17-paragraph-ownership.md`. The harness now isolates HOME and runs from a
neutral directory. This spot check asks whether the one-word label result depends on
that context. Four of pilot 15's prompts (vegetable, planet, bird, metal), `SP_OUT_PREFIX=clean`
so the rows sit apart from the originals: 24 forks on Haiku 4.5 and Opus 5; the `named`
question on the assistant and user2 layouts and the `rival` and `neutral` questions on the
assistant layout, both judges at 8 forks, every cell the script builds. Cost about $15.

Predictions. (a) `named` on the assistant layout ≥ 0.95 on both judges; on the user2
layout ≤ 0.05 on Haiku and ≤ 0.15 on Opus (pilot 15 gave 1.000 / 0.000 and 1.000 /
0.135). Refuter: assistant < 0.80 or user2 > 0.30 on either judge. (b) `neutral` ≥ 0.95
in-category on both judges. (c) The rival-frame drop is present: in-category `rival`
between 0.30 and 0.90 on Haiku and on Opus (pilots 11 and 13c gave in-category drops of
0.34 and 0.43). Refuter: rival ≥ 0.95 (no drop) or ≤ 0.10 (floor) on either judge. (d)
No own-probability structure: Spearman of rival P(Yes) against log own-probability
within the in-category cells, |ρ| < 0.3 on both judges. A refuter firing on (a) or (c)
means the corresponding pilot 11 to 16 claim is re-run in full on the clean harness before
it appears in any paper.

Results 15b: PENDING.
