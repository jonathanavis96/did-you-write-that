---
title: "Pilot 15: why one prompt per judge owns user-turn words"
status: complete 2026-09-03; the text was on disk before launch, the commit landed a few minutes after launch because a lint hook rejected the first commit attempt
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

| judge | layout | in-category P(Yes) | cells | cluster-aware 95% CI | off-category P(Yes) |
|---|---|---|---|---|---|
| Haiku 4.5 | assistant, named | 456/456 = 1.000 | 57 | saturated | 1.000 |
| Haiku 4.5 | user2, named | 0/456 = 0.000 | 57 | saturated | 0.000 |
| Opus 5 | assistant, named | 228/228 = 1.000 | 57 | saturated | 1.000 |
| Opus 5 | user2, named | 2/228 = 0.009 | 57 | [0.000, 0.025] | 0.000 |
| GPT-5.6-Sol | assistant, neutral | 344/344 = 1.000 | 43 | saturated | 1.000 |
| GPT-5.6-Sol | user, neutral | 4/344 = 0.012 | 43 | [0.000, 0.018] | 0.025 |

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
   dog") is not about proper names as a class, and stays specific to that prompt, unexplained.
4. **Digit hypothesis for Opus: refuted.** digits 0/12, numword 0/20 as user turns on Opus.
   The "1" residue in 13c and 13e is therefore not about digit strings. Pilot 16 (below)
   adds that the whole "number between 1 and 20" prompt carries a residue on Opus at 8
   forks, so the residue is prompt-specific, not orthographic.
5. **No own-probability structure: held.** Own-top cells (own probability ≥ 0.25) versus
   never-produced cells as user turns: Haiku 0.000 vs 0.000, Opus 0.050 vs 0.000 (10 and 27
   cells), GPT 0.010 vs 0.000 (13 and 10 cells). Spearman against raw own probability on
   in-category cells: Haiku undefined (all zero), Opus ρ = 0.28 (p 0.06, driven by the two
   1/4 cells Michael and Emma, both Opus-frequent words), GPT ρ = 0.08 (p 0.68). The Opus
   value is the only hint of a likelihood term in the whole pilot and rests on two forks.

### Reading

The pilot 13 result does not depend on the eight original prompts. Ten new prompts
spanning common nouns, proper names, months, digits and number words give the same
picture on all three judges: the word is owned when it sits in an assistant turn and
disowned when it sits in a user turn, at 0.00 to 0.01, with no relation to how often the
judge produces the word itself. The two residues seen earlier (GPT on the dog prompt, Opus
on the number prompt) did not generalise to the classes they suggested and are best
described as prompt-specific. Per-cell own probabilities for every cell are regenerable
from `out/own_forks.jsonl`; the summary above was recomputed from the raw rows, not from
`out/own_cells.json`, which later runs overwrite.
