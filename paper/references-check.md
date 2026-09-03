# references.bib — verification notes

All entries in `references.bib` were verified by fetching a primary or authoritative
secondary page with `fetchurl` on 2026-09-04 and reading title, author list, and year
directly off that page. arXiv entries were fetched as `https://arxiv.org/abs/<id>`
(both the extracted text and the `--raw` HTML, to pull the full author list out of the
`<div class="authors">` block, since the trafilatura extraction drops author bylines).
Classic human-literature entries were verified against Wikipedia (Daniel Wegner,
Self-perception theory, Introspection illusion pages), the Stanford Encyclopedia of
Philosophy "Self-Knowledge" entry, and the Nature Neuroscience article page for
Haggard, Clark & Kalogeras 2002. No entry was written from memory.

Sanity check: `python3` script confirmed 26 entries, no duplicate keys, balanced
braces (see session transcript).

## Verified: 26

### 1. LLM self-recognition / prefill awareness / introspection (13)
- lindsey2026emergent — arXiv:2601.01828, "Emergent Introspective Awareness in Large Language Models," Jack Lindsey. Submitted 5 Jan 2026.
- wang2026prefill — arXiv:2606.12747, "Prefill Awareness in Large Language Models," Wang, Mahajan, Africa, Souly, Taylor, Kirk.
- stamand2026selfgenerated — arXiv:2608.26159, "Self-Generated Text Recognition...," St. Amand et al. (8 authors), v2.
- panickssery2024llm — arXiv:2404.13076, "LLM Evaluators Recognize and Favor Their Own Generations," Panickssery, Bowman, Feng.
- binder2024looking — arXiv:2410.13787, "Looking Inward...," Binder, Chua, Korbak, Sleight, Hughes, Long, Perez, Turpin, Evans.
- kadavath2022language — arXiv:2207.05221, "Language Models (Mostly) Know What They Know," Kadavath et al. (36 authors), v4.
- li2024spartacus — arXiv:2411.10683, "I'm Spartacus, No, I'm Spartacus...," Li, Zhuang, Zhang, Xu, Wang, Xu, Fu, Cheng.
- ardoin2026llm — arXiv:2606.06315, "LLM Self-Recognition: Steering and Retrieving Activation Signatures," Ardoin, Schäfer, Wunder.
- bai2025know — arXiv:2510.03399, "Know Thyself? On the Incapability and Implications of AI Self-Recognition," Bai, Shrivastava, Holtzman, Tan.
- ding2026contextecho — arXiv:2605.24279, "ContextEcho: A Benchmark for Persona Drift in Long Agentic-Coding Sessions," Ding, Yu, Liu, Zhao, Chen, Chen, v2.
- kocielnik2026rethinking — arXiv:2606.12730, "Rethinking Psychometric Evaluation of LLMs...," Kocielnik, Han, Song, Marmarelis, Debnath, Mobbs, Anandkumar, Alvarez.
- deas2025artificial — arXiv:2510.08915, "Artificial Impressions...," Deas, McKeown.
- betley2025tell — arXiv:2501.11120, "Tell me about yourself: LLMs are aware of their learned behaviors," Betley, Bao, Soto, Sztyber-Betley, Chua, Evans.

### 2. Human sense of agency and authorship (5)
- wegner1999apparent — Wegner & Wheatley (1999), "Apparent Mental Causation: Sources of the Experience of Will," American Psychologist 54(7):480–492. Confirmed via the reference list on the Wikipedia "Daniel Wegner" page.
- haggard2002voluntary — Haggard, Clark & Kalogeras (2002), "Voluntary Action and Conscious Awareness," Nature Neuroscience 5:382–385. Confirmed from the article's own page metadata (authors, journal name, volume, page range, publication date all read directly off nature.com/articles/nn827).
- nisbett1977telling — Nisbett & Wilson (1977), "Telling More Than We Can Know: Verbal Reports on Mental Processes," Psychological Review 84(3):231–259. Confirmed via the reference list on the Wikipedia "Introspection illusion" page.
- bem1972selfperception — Bem (1972), "Self-Perception Theory," in Advances in Experimental Social Psychology, Vol. 6, ed. Berkowitz, pp. 1–62, Academic Press. Confirmed via two independent citations on the Wikipedia "Self-perception theory" page (references list and further-reading list, which agree on volume/pages/publisher).
- shoemaker1968selfreference — Shoemaker (1968), "Self-Reference and Self-Awareness," Journal of Philosophy 65:555–567. Confirmed via the bibliography of the Stanford Encyclopedia of Philosophy "Self-Knowledge" entry, which lists it in full (volume 65, pp. 555–567); this replaces the sweep's own flag that the exact wording/venue was only found via WebSearch — the SEP bibliography gives the full, citable reference.

### 3. Sycophancy and capitulation under pushback (7)
- sharma2023towards — arXiv:2310.13548, "Towards Understanding Sycophancy in Language Models," Sharma et al. (19 authors), v4.
- fanous2025syceval — arXiv:2502.08177, "SycEval: Evaluating LLM Sycophancy," Fanous, Goldberg, Agarwal, Lin, Zhou, Daneshjou, Koyejo, v4.
- jain2025interaction — arXiv:2509.12517, "Interaction Context Often Increases Sycophancy in LLMs," Jain, Park, Viana, Wilson, Calacci, v3.
- joswin2026mechanistic — arXiv:2607.00415, "A Mechanistic View of Authority Hierarchy in LLM Sycophancy," Joswin, Medicherla, Mammen.
- mammen2026who — arXiv:2601.13433, "Who Endorsed It? Measuring Authority Bias Across Expertise Levels in Language Models," Mammen, Joswin, Venkitachalam, v4.
- huang2026vulnerability — arXiv:2601.13590, "Vulnerability of LLMs' Stated Beliefs?...," Huang, Kwak, An, v3.
- maltbie2026intersectional — arXiv:2604.11609, "Intersectional Sycophancy...," Maltbie, Raval, v2.
- nogueira2026measuring — arXiv:2604.21564, "Measuring Opinion Bias and Sycophancy via LLM-based Persuasion," Nogueira et al. (10 authors), v2.

### 4. Cross-model self-preference (1, shared with section 1)
- panickssery2024llm (see above) — the foundational self-recognition-drives-self-preference result.

## Unverified: 0

Every candidate identifier named in the dispatch prompt and in the three lit-sweep
files (within the requested topic scope) was successfully fetched and its title,
authors, and year confirmed. Nothing had to be dropped to references-check.md's
unverified bucket.

## Title/description mismatches worth flagging

- **lindsey2026emergent (arXiv:2601.01828).** The dispatch prompt describes this as
  "the Anthropic introspection paper by Lindsey (**2025**, 'Emergent introspective
  awareness in large language models')." The fetched arXiv abs page shows it was
  **submitted 5 Jan 2026**, not 2025, and the arXiv ID itself (`2601.*`) encodes a
  January-2026 submission. Title and single-author byline (Jack Lindsey) match the
  prompt's description exactly; only the year is off. The bib entry uses `year =
  {2026}`, the year read from the fetched page, not the year given in the dispatch
  prompt.
- Everything else fetched matches the sweep documents' descriptions (title, author
  count, and abstract content) with no discrepancies worth flagging — in particular,
  Kadavath et al. 2207.05221 is a 36-author OpenAI/Anthropic-era paper (v4, 21 Nov
  2022) exactly as the ownership sweep describes it, and the SGTR paper
  (2608.26159) matches its v2 (28 Aug 2026) description precisely.

## Deliberately excluded (in scope of the sweeps but out of scope of this bib)

- From `docs/lit-sweeps/source-credibility-prior-art.md`: arXiv:2605.23938
  ("Authority Inversion...") and arXiv:2505.21091 ("Position is Power...") were read
  but excluded — neither is about self-recognition, prefill detection, introspection,
  sycophancy, persona induction, self-knowledge, or identity-as-attractor specifically
  (one is sensor-vs-user trust, the other is demographic bias in system prompts).
  Hovland & Weiss (1951) and the Wikipedia "boomerang effect" page, both quoted in
  that sweep, were also excluded: the dispatch prompt restricts classic
  human-literature citations to the named list (Wegner & Wheatley 1999, Wegner 2002,
  Bem 1972, Shoemaker 1968, Gilbert's rank theory, Haggard on sense of agency, Nisbett
  & Wilson 1977) sourced only from `neuroscience-agency.md`, `social-psychology.md`,
  and `philosophy-linguistics.md`, and Hovland & Weiss / the boomerang effect are not
  on that list.
- **Wegner (2002), *The Illusion of Conscious Will*** — named in the dispatch prompt
  as a target, but not found actually cited in `neuroscience-agency.md`,
  `social-psychology.md`, or `philosophy-linguistics.md`. Those files cite Wegner's
  theory of apparent mental causation via the Wegner & Wheatley (1999) journal
  article and the Wikipedia "Daniel Wegner" page, not the 2002 book by name or ISBN.
  Per the dispatch prompt's instruction to "take only those actually named in the
  sweeps," the 2002 book is omitted from the bib rather than guessed at.
- **Gilbert's rank theory** — not named in any of the three sweep files. The only
  "Gilbert" appearing in `philosophy-linguistics.md` is Dennett's fictional
  novel-writing-machine character "Gilbert," unrelated to Paul Gilbert's rank theory
  of social status/mood. Omitted.
- From `docs/lit-sweeps/llm-novelty.md`: arXiv:2512.13762 (learned incapacity/learned
  helplessness analogy) and arXiv:2608.01326 (context compaction theory) were read but
  excluded as off-topic for this bib (refusal/contingency and formal compaction
  theory, not self-recognition/prefill/introspection/sycophancy/persona/self-knowledge).
  Several other IDs in that file's "papers overlapping the working hypothesis" list
  (2510.24797, 2410.18819, 2407.01505, 2412.00207, 2601.15334, 2601.14553, 2608.01017,
  2607.21558) are explicitly marked "UNVERIFIED, title only" by the sweep itself — not
  fetched there, and not independently fetched for this task since none is named in
  the dispatch prompt's required list; they are left out of the bib rather than cited
  on a title-only basis.
