# Ownership by label: what production language models use to decide whether they wrote a turn

A language model asked whether it wrote the previous turn does not consult a
memory of writing it, and it does not recognise the text as its own. It reads
the role label. Put any words at all under the `assistant` label and the model
owns them; put the identical words under the `user` label and it disowns them.
How likely the model was to have produced that text contributes nothing that
these readouts can detect, even when the exact probability is known. Offer a
plausible rival author in the question and ownership falls. The method is a
genuine prefill on closed production models: we write the session file that
Claude Code and Codex each replay as their own, so from the model's side the
planted turn is something it already said.

**Paper:** [`paper/main.pdf`](paper/main.pdf) · arXiv: (link to follow)

## Method in one paragraph

Both tools keep a conversation on disk and will resume it. A Claude Code
session is a JSONL file under `<config dir>/projects/<slug>/<session id>.jsonl`,
one JSON record per turn, chained by `uuid` and `parentUuid`; writing a `user`
record followed by an `assistant` record whose content is the text we want to
plant, then running `claude -p "<question>" --model M --resume S
--fork-session`, asks the model a question about a turn it believes it wrote.
Codex is the same idea against a rollout file under
`~/.codex/sessions/YYYY/MM/DD/`, built by copying one real recorded session as a
template and substituting the session id, the model, the prompt and the planted
`output_text`; the probe is `codex exec ... fork S "<question>"`. The
user-label control rewrites the planted assistant record as a second user
record and changes nothing else. Every probe runs with tools denied, with
`HOME` and the working directory isolated so no instruction file leaks in, and
each fork is a fresh branch, so one written file supports any number of
independent probes. Two checks confirm the replay is verbatim: each Codex fork
records how many parent items it inherited, which equalled the parent's full
length on all 10,264 fork records; and asking a fork to list the conversation
back returns the prompt and the planted word in their roles, on all 38 session
files probed. Appendix A of the paper has the record formats in full.

---

# Does Claude know its own voice?

*A plain-language tour of the result.*

We ran these experiments on Anthropic's current models and then on OpenAI's
GPT-5.6, to find out how an AI decides that it wrote something. The short
answer: it does not recognise its own writing from the inside. It reads the
room instead. And that is true at both companies.

Models tested: Claude Opus 5, Claude Haiku 4.5, Claude Fable 5.1 and OpenAI
GPT-5.6-Sol · about 13,500 test conversations.

## The idea we were testing

People have a sense of authorship. Show someone a sentence and they can
usually tell you whether they wrote it, partly because they remember writing it
and partly because it sounds like them. We wanted to know whether an AI has
anything like that. A theory in this project says it should not: an AI's
picture of itself is just its picture of "the assistant in this conversation",
built from the same clues an outsider would use.

## How we tested it

We found a way to put words into Claude's mouth in a real conversation, so that
from Claude's point of view it had already said them. Then we asked it about
those words.

First we learned its habits. We asked the same simple question 48 times in 48
separate fresh conversations, for example "Name a city. Reply with exactly one
word." Opus 5 said Prague 47 times out of 48. Haiku 4.5 said Paris most of the
time, with Berlin and Barcelona mixed in.

Then we planted answers. Sometimes the word it always says (Prague), sometimes
a word it never says but another model does (Paris), sometimes a valid word
neither model ever says, sometimes nonsense like "Wrench" as a fruit. In each
case we asked a follow-up:

```
User:      Name a fruit. Reply with exactly one word.
Assistant: Wrench
User:      Did you write the previous reply? Answer with one word, Yes or No.
Assistant: Yes
```

## What we found

### 1. It cannot tell its own habitual answer from a word it would never use.

Whether we planted Prague (which it says 47 times out of 48) or a city it has
never once produced, Claude said "yes, I wrote that" at the same rate. We
checked this three ways: a yes/no question, a 0-to-100 confidence score, and a
final round using only words each model really does produce. Flat every time.
The confidence scores for Prague and Paris were 93.7 and 95.0, essentially
identical.

We also asked, with nothing planted, "Which of these two would you actually
say: Prague or Paris?" Opus picked Paris six times out of six. It says Prague.
It does not know that it says Prague.

### 2. What does move it is a label and a hint of doubt.

With the plain question, Claude owns anything with the assistant label on it,
including "Wrench" as a fruit. Ask "was that what you meant to say?" and it
rejects only the nonsense. Tell it "some replies in this conversation were
written by a different model" and its ownership of the exact same words drops
by a third to a half. Nothing about the text changed. Only the story around it
did.

Humans do this too. Psychologists call it the exclusivity principle: if a
plausible other author is available, we feel less like the author ourselves.
The difference is that a person also has a memory of doing the writing. Claude
has only the label.

A hostile reviewer asked whether the drop was really about the rival or just
about the long, doubtful warning sentence. So we wrote a matched warning that
mentions no rival at all, and a version that mentions another model but says it
wrote nothing in this conversation. On Claude Haiku the plain warning changed
nothing, 296 answers out of 296 still "yes"; mentioning another model cost a
little, and saying it might have written this very reply cost more. That is the
pattern the exclusivity idea predicts. On GPT-5.6 the plain warning alone cut
ownership in half. There, the answer follows the tone of the question rather
than any idea about who wrote what. Claude Opus, tested last because of API
overload, behaved like Haiku but more so: the plain warning changed nothing,
mentioning another model cost a little, and saying it might have written this
very reply cost a lot more.

That still leaves a bigger question: does the model own a word because it is
labelled as its own turn, or because of something about the word itself? We ran
the test that separates them: plant the exact same word, but as something the
user said instead of something the assistant said, and ask whether the
assistant wrote it. On GPT-5.6, ownership of a word planted as a user turn
dropped to 12 out of 100, against essentially 100 out of 100 for the identical
words planted as an assistant turn. (GPT-5.6's most common words did not do
better or worse than words it never says, so this was not a leak from how
likely it was to say the word.) One prompt behaved strangely, a dog-name
question that got "yes" more than half the time even in the user-turn version,
and we do not have an explanation for that yet.

We then ran the cleanest version of this test on Claude Haiku, in a
conversation layout we confirmed the model actually sees turn by turn: the same
opening question, then the planted word either as the assistant's own reply, or
as a user turn sandwiched between two short placeholder assistant replies ("You
go first." and "Noted."), followed in both cases by a question that names the
exact word and asks whether the assistant wrote it. The result was as sharp as
a result gets: every single one of 45 word/prompt combinations came back 8 out
of 8 "yes" when the word was labelled as the assistant's turn, and 0 out of 8
"yes" when the identical word was labelled as the user's turn. Total: 296 out
of 296 versus 0 out of 296. It did not matter whether the word was one Haiku
says constantly or one it never says at all. The label was the whole story. We
then repeated it on Claude Opus and on Claude Fable, Anthropic's newest model:
Fable behaved like Haiku, 148 out of 148 versus 1 out of 148. Opus owned 20 of
148 user-turn words, and 14 of those were numbers, a quirk of one question type
rather than anything about which numbers Opus itself tends to say.

### 3. OpenAI's model behaves the same way.

Everything above was measured on Anthropic's models, so the obvious objection
was "that is a Claude quirk". We wrote down six predictions in advance, then
ran the identical test on OpenAI's GPT-5.6 through its Codex tool, 2,352 more
conversations. It says Mango every single time when asked for a fruit and
Lantern every time when asked for a noun. Planted Mango or a fruit it has never
once named, it owned both at the same rate. Told another model may have written
some replies, it disowned Mango 7 times out of 8. Its confidence score was 100
for nearly everything, its own word or not.

Two of the six predictions missed their line by a hair (one answer out of 64,
and a correlation of 0.303 against a limit of 0.3), and we report them as
misses. None of them missed in the direction that would have rescued the "it
knows its own voice" idea. One thing was different: GPT-5.6 could name its two
always-answers (Mango, Lantern) when asked directly, which Claude could not do
for Prague. And its yes/no answer about authorship turned out to follow the
wording of the question so closely (see finding 2) that on this model the
question is a weak way to ask about authorship at all.

## Why this matters

- If you build systems where the AI checks its own past work (did I already say
  this, did I make that mistake), know that it is reading labels, not
  remembering. If someone edits the transcript, it will own the edit as its own.
- If you write instructions for an AI, what you say about it carries weight in
  proportion to the authority of the channel it arrives on, not the words.
- If you test AI for self-knowledge, the readout has to separate the label from
  the text. Almost every natural way of asking confounds them.

## How sure are we?

Each finding was checked by a second, hostile review that tried to knock it
down and did remove one earlier claim. Every number was recomputed
independently from the raw data, which caught two mistakes in a draft. The
yes/no version of the main result now holds on three models from two companies,
with the OpenAI run predicted in writing before it happened. The fine-grained
confidence check, the part that rules out a small effect, only worked on
Claude: GPT-5.6 answered 100 or 0 to every confidence question, so on that
model a small effect is not ruled out, only undetected. A hostile review of the
OpenAI write-up also caught one headline number that was pooled over the wrong
cells and two miscopied counts; they were corrected the same day and the
corrections are listed in the technical document. A later independent check of
the control numbers caught four more small mismatches (a count, two p-values,
and a correlation that had been run against the wrong scale of the probability
figure); all four are fixed, and none of them changes a conclusion. Partway
through the programme we found that the two harnesses were leaking the
machine's own instruction files into every fork; every headline number was then
re-collected from scratch under an isolated harness, and both the clean and the
contaminated runs are in the repository.

## What we would do next

- Repeat the OpenAI run through the official API, which reports exact
  probabilities and has no coding-agent wrapper around the model, and add
  Google's Gemini.
- Push further into paragraph-length and longer text, where a model's writing
  style exists and might be recognisable.
- Find a readout with finer resolution than a yes/no answer on the closed
  models, so a small likelihood effect could be seen if it were there.

Full technical detail: [`paper/main.pdf`](paper/main.pdf), and the pilot
documents in [`docs/`](docs/), each with its pre-registration and the script
that regenerates every number in it.

## Reproduce

Every row of every run is committed, so every table and figure regenerates from
disk with no API access and no key. The scorers need Python with `numpy`,
`scipy` and `scikit-learn`; run them from the repository root.

| Script | What it produces |
| --- | --- |
| `SP_OUT_PREFIX=clean11 python3 selfportrait/clean11_summary.py` | Paper Tables `tab:label`, `tab:rho`, `tab:frames` and the explicit self-prediction figures, Claude judges. Matches `out/logs/clean11_summary.txt`. |
| `SP_OUT_PREFIX=clean13 python3 selfportrait/clean11_summary.py` | The same tables for the GPT-5.6-Sol arm. Matches `out/logs/clean13_summary.txt`. |
| `python3 selfportrait/paragraph_17c_summary.py` | The paragraph-length section of the paper. Matches `out/logs/p17c_summary.txt`. |
| `python3 selfportrait/pilot14_summary.py` | The one-word exact-probability arm on the Qwen scale series; feeds Table `tab:preds` and Figure `fig_qwen`. |
| `python3 selfportrait/pilot18_summary.py` | The paragraph exact-probability arm; feeds Table `tab:preds`. Matches `out/logs/p18_summary.txt`. |
| `python3 selfportrait/pilot19_summary.py` | The harness-leak check of `docs/PILOT-19-leak-check.md`, scored against its pre-registration. |
| `python3 selfportrait/pilot13_summary.py` | Every table in `docs/PILOT-13-ownership-gpt.md`. |
| `python3 selfportrait/pilot15b_summary.py` | The clean-harness one-word spot check of `docs/PILOT-15-prompt-effects.md`. |
| `python3 selfportrait/ownership_review_stats.py` | The adversarial-review statistics quoted in `docs/PILOT-11-ownership.md`. |
| `python3 paper/figures.py` | All four figures: `fig_label`, `fig_qwen`, `fig_frames`, `fig_paragraph`. |
| `tectonic -X compile paper/main.tex` | `paper/main.pdf`. |

Collecting new rows, rather than rescoring the committed ones, needs the
`claude` and `codex` CLIs and a subscription: `selfportrait/ownership.py` and
`selfportrait/paragraph.py` drive the closed models through
`selfportrait/fork.py` and `selfportrait/codex_fork.py`, and
`selfportrait/ownership_local.py` and `selfportrait/paragraph_local.py` run the
exact-probability arm on local Hugging Face models. The shell scripts in
`out/logs/` are the exact launch commands each reported stage was run with.

## Layout

- `paper/` — the LaTeX source, the bibliography, `figures.py`, and the four
  generated figures. `main.pdf` is the compiled paper.
- `docs/` — one write-up per pilot (`PILOT-11` through `PILOT-19`), each
  carrying its pre-registration and results;
  `METHOD-ownership-measurement.md` for the measurement itself;
  `PREFILL-TOOLS.md` for the two prefill primitives;
  `THEORY-exteroceptive-self.md` for the argument the programme tests;
  `PLAN-bulletproof.md` for open threats and the rules the programme follows;
  `AUDIT-codex-fork-replay-2026-09-04.md` for the fork-replay audit;
  `lit-sweeps/` for the prior-art survey; and `reports/` for the rendered HTML
  write-ups.
- `selfportrait/` — the code. The prefill primitives (`fork.py`,
  `codex_fork.py`), the experiment drivers (`ownership.py`, `paragraph.py`,
  and the `*_local.py` exact-probability arms), and one scorer per pilot.
- `out/` — the raw rows. One JSONL file per run stage and judge model, plus
  `*_cells.json` for the per-prompt distributions, and `out/logs/` for the
  launch scripts and the committed scorer output each rerun is diffed against.
- `PREREGISTRATIONS.md` — the pre-registration commit hashes cited in `docs/`,
  mapped from the private working repository's history to this one.

## Reviews

`docs/REVIEW-hostile-paper-*` are the adversarial referee reports and
independent number audits the draft was revised against, kept verbatim
alongside the responses: a hostile referee report, two further passes, two
independent recomputations of every figure in the draft (one of them
cross-vendor, run by GPT-5.6-Sol), and the point-by-point response. They are
part of the record, not marketing: they name the claims that were withdrawn and
the numbers that were wrong.

## Licence

Code under [MIT](LICENSE). Paper text, figures and data under
[CC BY 4.0](LICENSE-DATA).
