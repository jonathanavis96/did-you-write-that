---
title: "Pilot 15: why one prompt per judge owns user-turn words"
status: pre-registered 2026-09-03; the text was on disk before launch, the commit landed a few minutes after launch because a lint hook rejected the first commit attempt
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

Results: PENDING.
