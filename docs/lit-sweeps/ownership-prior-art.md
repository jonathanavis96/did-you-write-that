---
title: "Prior-art check: ownership judgement vs own sampling probability, with framing manipulations"
status: literature sweep, 2026-09-03, all sources fetched with fetchurl and quoted
depends_on: docs/PILOT-11-ownership.md, docs/PILOT-13-ownership-gpt.md
---

# Prior-art check for the ownership-vs-probability measurement

## The question

Has anyone published a measurement of an LLM's ownership judgement ("did you write
this?") of a *planted* assistant turn (genuine prefill, not a described scenario)
against the *model's own sampling probability* for that text (measured by forking the
identical prompt many times, or by teacher-forced log-likelihood), with framing
manipulations — a named rival author, a placebo/intent preamble — layered on top?
Our pilots (`docs/PILOT-11-ownership.md`, `docs/PILOT-13-ownership-gpt.md`) do
exactly this: 48 fresh forks per prompt give the model's own answer distribution; a
word is planted as the model's prior reply via genuine prefill (the session-file
resume trick, not API `prefill`/`assistant` message injection); the model is then
asked Yes/No "Did you write the previous reply?" under neutral, rival ("some turns
were replaced by a different model"), intent, placebo, and rival-not-author frames,
plus a 0-100 confidence and an explicit no-prefill forced choice between its own
modal answer and a rival's.

Below is every paper found that measures a neighbouring thing, with what it actually
measured (quoted from the fetched abstract, not paraphrased from a search snippet),
and how it differs from ours. Search angles run: LLM self-recognition of own
generations; self-prediction/introspection (Binder); emergent introspective
awareness (Lindsey/Anthropic); prefill awareness / models detecting prefilled
assistant turns; authorship attribution of own text; sense of agency / ownership and
Wegner's exclusivity principle applied to LLMs; sycophancy under a "a different model
wrote this" frame; self-recognition via logprob / own-probability as a confidence
signal; "did you write this" prefill ownership experiments generally; LLM
distinguishing own vs. other-model text (identity confusion).

## Closest prior work

**Lindsey, "Emergent Introspective Awareness in Large Language Models," Anthropic,
submitted 5 Jan 2026, arXiv:2601.01828.**
<https://arxiv.org/abs/2601.01828>. Quoted from the abstract: "We investigate whether
large language models can introspect on their internal states... Strikingly, we find
that some models can use their ability to recall prior intentions in order to
distinguish their own outputs from artificial prefills." This is the paper our pilot
docs cite for the mechanism claim ("must involve estimating the likelihood that the
model would have produced a given output token" / "directly introspect on its
previously computed 'intentions'" — those phrases are quoted in
`docs/PILOT-11-ownership.md` from this source, not independently re-verified by this
sweep against the full text, only the abstract was fetched here). It does use genuine
activation injection and prefill, and it does ask the model to identify prefills as
foreign. It does **not** measure ownership against the model's own sampling
probability across a graded set of equally-valid one-word answers, and it does not
run framing manipulations (rival-author, placebo) as an independent variable — the
abstract describes injected-concept detection and prefill-vs-genuine discrimination,
not a probability-gradient design.

**"Prefill Awareness in Large Language Models," submitted 10 Jun 2026,
arXiv:2606.12747.** <https://arxiv.org/abs/2606.12747>. Quoted: "We investigate
whether frontier language models can distinguish between tampered and untampered
assistant-side context, a capability we call prefill awareness... Claude Opus 4.5
detects prefills opposing its preferences in 9-35% of cases with a 0% false positive
rate when prompted... Controlled ablations later also show that detection and
resistance rely on different cues, where stylistic mismatch mainly affects whether
models flag a prefill as foreign, while preference mismatch mainly affects whether
they revert toward their baseline answer." This is the paper our design cites for the
quality/style confound our one-word, same-category design controls for. It manipulates
*preference* mismatch (does the prefilled text agree with the model's stance) and
*style* mismatch, not the model's raw sampling probability for a fixed short answer,
and it does not test a rival-author or placebo framing as we do, nor does it use
genuine session-file prefill on a production Claude Code / Codex CLI session — its
mechanism, per the abstract, is a "binary preference benchmark across three prefill
mechanisms."

**"Self-Generated Text Recognition: Quality Heuristics, Cross-Task Transfer, and
Downstream Bias in LLM Evaluation," v1 7 Jul 2026, v2 28 Aug 2026, arXiv:2608.26159.**
<https://arxiv.org/abs/2608.26159>. Quoted: "Self-Generated Text Recognition
(SGTR)--the ability of an LLM to identify its own outputs--poses risks to AI
safeguards that rely on LLMs as evaluators or monitors... We corroborate previous
observations that a quality heuristic--models attributing authorship to text they
perceive as higher quality--is a dominant confound." This is the source for the
"attribut[e] authorship to text they perceive as higher quality" confound our docs
cite. It studies third-person recognition (is this candidate text mine, shown as a
document to judge), not first-person ownership of a planted reply in one's own
conversation turn, and it does not use own-sampling-probability as an independent
variable or apply rival/placebo framing to a Yes/No ownership question.

**Panickssery, Bowman, Feng, "LLM Evaluators Recognize and Favor Their Own
Generations," NeurIPS 2024, arXiv:2404.13076.**
<https://arxiv.org/abs/2404.13076>. Quoted: "we investigate if self-recognition
capability contributes to self-preference. We discover that, out of the box, LLMs
such as GPT-4 and Llama 2 have non-trivial accuracy at distinguishing themselves from
other LLMs and humans. By fine-tuning LLMs, we discover a linear correlation between
self-recognition capability and the strength of self-preference bias." This is
third-person self-recognition (shown text, asked "who wrote this?") measured against
fine-tuned recognition accuracy, not first-person prefill ownership measured against
sampling probability. No framing manipulation of the kind we use.

**Binder, Chua, et al., "Looking Inward: Language Models Can Learn About Themselves
by Introspection," submitted 17 Oct 2024, arXiv:2410.13787.**
<https://arxiv.org/abs/2410.13787>. Quoted: "We study introspection by finetuning
LLMs to predict properties of their own behavior in hypothetical scenarios... If a
model M1 can introspect, it should outperform a different model M2 in predicting M1's
behavior even if M2 is trained on M1's ground-truth behavior." This measures
*behavioral self-prediction* (hypothetical "what would you do") after fine-tuning for
the task, not ownership of an already-planted turn, and not against sampling
probability from repeated forking. It is the closest prior instrument to our Stage D
"explicit no-prefill forced choice," but theirs requires fine-tuning M1 to predict
itself, where ours uses zero-shot forced choice on a production model.

**Kadavath et al., "Language Models (Mostly) Know What They Know," submitted 11 Jul
2022 (v4 21 Nov 2022), arXiv:2207.05221.** <https://arxiv.org/abs/2207.05221>. Quoted:
"We study whether language models can evaluate the validity of their own claims and
predict which questions they will be able to answer correctly... by asking models to
first propose answers, and then to evaluate the probability 'P(True)' that their
answers are correct." This is self-evaluation of claim *correctness/calibration*, an
adjacent but distinct question from ownership of a planted turn; no prefill, no
framing manipulation, no ownership question of the "did you write this" form.

## Peripheral, not close

- **"I'm Spartacus, No, I'm Spartacus: Measuring and Understanding LLM Identity
  Confusion," submitted 16 Nov 2024, arXiv:2411.10683**
  (<https://arxiv.org/abs/2411.10683>). Quoted: "Large Language Models (LLMs)...
  misrepresent their origins or identities... Our analysis of 27 LLMs revealed that
  25.93% exhibit identity confusion... these issues stem from hallucinations rather
  than replication or reuse." This is about models misstating *which company/model
  they are* (e.g., claiming to be GPT when they are not), not about ownership of a
  specific planted text turn. Not close.
- **"LLM Self-Recognition: Steering and Retrieving Activation Signatures,"
  arXiv:2606.06315** (submitted 4 Jun 2026; abstract fetched 2026-09-03 from
  arxiv.org/abs/2606.06315). Abstract: "large language models (LLMs) implicitly encode
  signals in their generated text that enable self-recognition of their outputs. We
  demonstrate that this capability is reliable, even in low-entropy scenarios, and that it
  can be amplified through targeted intervention. By steering the internal residual stream
  during generation with a random sparse vector, we create a detectable fingerprint …
  This signal is recoverable from the activations of an LLM used as a detector, achieving
  over 98% accuracy". Third-person attribution read out of a detector model's activations
  on open-weight models, with a steering intervention; no first-person ownership question,
  no own-sampling-probability variable, no framing manipulation, no production
  closed-weight model. Its claim that self-recognition is "reliable, even in low-entropy
  scenarios" is the one to contrast with our behavioural result (Opus picks Paris over its
  own 47/48 Prague); cite as the activation-level counterpart.
- Watermarking / stylometric authorship-attribution literature (surfaced under the
  "authorship attribution" search) is about *externally* proving which model produced
  text via statistical signatures in the text itself, not about the model's own
  first-person Yes/No ownership judgement. Not close, not fetched individually.
- Wegner's exclusivity principle: only the original psychology literature
  (Nahmias "Agency, authorship, and illusion," Synofzik "A problem for Wegner and
  colleagues' model of the sense of agency," Wegner/Sparrow "Authorship processes")
  surfaced. No LLM paper applying Wegner's exclusivity principle to a model's
  first-person authorship report was found by this search.
- Sycophancy literature ("From Yes-Men to Truth-Tellers," "Interaction Context Often
  Increases Sycophancy," "It's Not Always Sycophancy," etc.) covers models flipping
  factual or evaluative answers under user pushback or asserted premises generally.
  No paper specifically testing "you are told a different model wrote your own prior
  turn" as a sycophancy/framing manipulation was found.
- Self-recognition-via-own-probability: search returned only papers using
  *sample-consistency* (agreement across repeated samples) as a general confidence
  signal (e.g., "Confidence Improves Self-Consistency in LLMs"), not as an independent
  variable regressed against a first-person ownership judgement of a planted turn.

## Verdict

**We found none.** No paper located in this sweep measures first-person ownership
("did you write this?") of a genuinely prefilled assistant turn against the model's
own sampling-probability distribution for that text (via repeated forking or
teacher-forced likelihood), crossed with framing manipulations naming a rival author
or a placebo/intent preamble. The closest work splits into two lines that our design
sits between but does not overlap: (1) Lindsey (arXiv:2601.01828) and the prefill-
awareness paper (arXiv:2606.12747), both of which use genuine or simulated prefill
and probe whether models detect it as foreign, but neither regresses the ownership
report against the model's own sampling frequency for the specific inserted text, and
neither crosses a rival-author/placebo framing manipulation with a probability
gradient; (2) the self-recognition-as-evaluator line (Panickssery et al.,
arXiv:2404.13076; the SGTR paper, arXiv:2608.26159) which asks models to judge
*externally presented* candidate text for authorship, a third-person task, not
first-person ownership of one's own planted conversational turn, and which uses
recognition *accuracy against ground truth*, not the model's own sampling probability,
as the dependent variable's covariate.

What appears genuinely new in our design, on this search: (a) using the model's own
multi-fork sampling frequency (and, on the local Qwen arm, exact teacher-forced
log-likelihood) as the independent variable predicting a first-person ownership
judgement — no located paper uses own-probability this way; (b) genuine prefill via
the session-file/`--fork-session` and Codex `fork` mechanisms on production
closed-weight models (Opus 5, Haiku 4.5, GPT-5.6-Sol) rather than API-level prefill
injection or fine-tuned self-prediction; (c) the rival-author and placebo/intent
framing manipulations layered onto the same prefilled text, isolating an exclusivity-
style effect (Wegner) from the plausibility/likelihood channel; (d) cross-vendor
replication of the same design (Pilot 13, GPT-5.6-Sol) with pre-registered
predictions.

What we must cite, and for what: Lindsey (arXiv:2601.01828) for the mechanism claim
under test (introspection on prior intentions as the alternative to a label-plus-fit
account) and as the closest existing prefill-detection result; the prefill-awareness
paper (arXiv:2606.12747) for the style/preference-mismatch confound our one-word
same-category design controls for, and as the closest existing framing/detection
result on production Claude models; the SGTR paper (arXiv:2608.26159) for the
quality-heuristic confound in third-person self-recognition; Panickssery et al.
(arXiv:2404.13076) as the foundational self-recognition-drives-self-preference
result; Binder et al. (arXiv:2410.13787) as the closest prior explicit
self-prediction instrument, to contrast against our zero-shot forced-choice Stage D;
Kadavath et al. (arXiv:2207.05221) for the general self-evaluation/calibration
framing our confidence instrument sits inside. This list should replace or supplement
whatever citations are currently in the "Why the design controls what the literature
could not" section of `docs/PILOT-11-ownership.md`, which already names three of
these six (Lindsey, the prefill-awareness paper, and the SGTR paper) — this sweep
confirms those three are indeed the closest work and adds Panickssery, Binder, and
Kadavath as the surrounding self-recognition/self-prediction/self-evaluation
literature that should be acknowledged even though none of them run the
probability-vs-ownership-vs-framing design.

## Sources fetched

All fetched with `fetchurl` on 2026-09-03; abstracts quoted verbatim above.

- <https://arxiv.org/abs/2601.01828> — Lindsey, Emergent Introspective Awareness
- <https://arxiv.org/abs/2606.12747> — Prefill Awareness in Large Language Models
- <https://arxiv.org/abs/2608.26159> — Self-Generated Text Recognition (SGTR)
- <https://arxiv.org/abs/2404.13076> — LLM Evaluators Recognize and Favor Their Own Generations
- <https://arxiv.org/abs/2410.13787> — Looking Inward (Binder et al.)
- <https://arxiv.org/abs/2207.05221> — Language Models (Mostly) Know What They Know (Kadavath et al.)
- <https://arxiv.org/abs/2411.10683> — I'm Spartacus, No, I'm Spartacus (identity confusion)

WebSearch (not fetched as full text, used only to locate the above and to confirm no
closer match exists) covered: self-recognition of own generations; introspection/
self-prediction; emergent introspective awareness; authorship attribution/watermarking;
sense of agency/Wegner and LLMs; sycophancy under a rival-authorship frame; own-
sampling-probability as a self-recognition confidence signal; "did you write this"
prefill ownership experiments; own-vs-other-model text detection.
