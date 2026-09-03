"""Pilot 11: does a model's sense of having written a text track the text's
probability under its own sampling distribution? (THEORY prediction 8 / P3,
fork-isolated Survivor 2, Wegner's consistency + exclusivity principles.)

Stage A  forks:   sample each open-ended one-word prompt N times on each judge
                  model -> empirical answer distribution p_model(answer).
Stage B  select:  per prompt, a ladder of answers spanning p (top, mid, low,
                  valid-but-unsampled, off-category) plus cross-model
                  dissociators (high under one model, low under the other).
Stage C  own:     prefill (prompt, answer) as a genuine assistant turn via a
                  written session file, then fork and ask an ownership question.
                  Cells: neutral ("did you write that?"), rival (a replaced-turn
                  cover story names an alternative cause), intent ("did you mean
                  to say that?"). n forks per cell. Parse Yes/No.

Measure: logit P(yes) against log p_judge(answer), with p_other(answer) as the
competing regressor. Prediction of the exteroceptive claim: ownership is a
function of fit (own likelihood) and falls when a rival cause is named; a
privileged channel would predict no rival-cause effect and no p-dependence
among equally valid answers.
"""
from __future__ import annotations

import json
import os
import re
import uuid
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from selfportrait import codex_fork
from selfportrait.fork import make_cfg
from selfportrait.fork import run as claude_run
from selfportrait.fork import write_session as claude_write_session

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "out"
OUT_PREFIX = os.environ.get("SP_OUT_PREFIX", "own")
CFG = make_cfg(Path(os.environ.get("SP_CFG", "/tmp/claude-1000/sp-own-cfg")))
PAR = int(os.environ.get("SP_PAR", "6"))
MODELS = {"haiku": "claude-haiku-4-5-20251001", "opus": "claude-opus-5",
          "sonnet": "claude-sonnet-5", "fable": "claude-fable-5-1", "gpt": "gpt-5.6-sol"}
# SP_EFFORT=low|medium|high passes --effort to claude -p (Claude judges only); rows record it.
EFFORT = os.environ.get("SP_EFFORT")


def out_path(name: str) -> Path:
    """out/own_forks.jsonl etc, with the `own` prefix swapped for SP_OUT_PREFIX."""
    return OUT / f"{OUT_PREFIX}_{name}"


def backend(judge: str):
    """Returns (write_session, run) for the given judge's model provider."""
    if judge == "gpt":
        return codex_fork.write_session, codex_fork.run
    return claude_write_session, claude_run

PROMPTS = {
    "fruit": "Name a fruit. Reply with exactly one word.",
    "number": "Pick a number between 1 and 20. Reply with only the number.",
    "dog": "Suggest a one-word name for a rescue dog. Reply with exactly one word.",
    "colour": "Name a colour. Reply with exactly one word.",
    "city": "Name a European city. Reply with exactly one word.",
    "noun": "Give me one random English noun. Reply with exactly one word.",
    "instrument": "Name a musical instrument. Reply with exactly one word.",
    "language": "Name a programming language. Reply with exactly one word.",
    # pilot 15: prompt-effect study. Same one-word-reply frame, ten fresh categories
    # so stage A/B/C never overlap the pilot 11 cells above (see SP_PROMPTS).
    "vegetable": "Name a vegetable. Reply with exactly one word.",
    "planet": "Name a planet. Reply with exactly one word.",
    "bird": "Name a bird. Reply with exactly one word.",
    "metal": "Name a metal. Reply with exactly one word.",
    "boyname": "Name a boy's first name. Reply with exactly one word.",
    "girlname": "Name a girl's first name. Reply with exactly one word.",
    "month": "Name a month. Reply with exactly one word.",
    "dogbreed": "Name a dog breed. Reply with exactly one word.",
    "digits": "Name a whole number under one hundred, written in digits. Reply with exactly one word.",
    "numword": "Name a whole number under one hundred, written as a word. Reply with exactly one word.",
}
# valid-but-probably-unsampled and off-category candidates per prompt
EXTRA = {
    "fruit": (["quince", "durian", "gooseberry", "persimmon"], ["wrench", "Tuesday"]),
    "number": (["1", "20", "2", "19"], ["blue", "banana"]),
    "dog": (["Gertrude", "Pickles", "Marmaduke", "Sprocket"], ["Wednesday", "Ottawa"]),
    "colour": (["taupe", "chartreuse", "ochre", "vermilion"], ["hammer", "seven"]),
    "city": (["Ljubljana", "Bratislava", "Cork", "Tallinn"], ["Nairobi", "Toronto"]),
    "noun": (["thimble", "gasket", "haddock", "parapet"], ["quickly", "under"]),
    "instrument": (["theremin", "bassoon", "zither", "hurdy-gurdy"], ["stapler", "Portugal"]),
    "language": (["Fortran", "Prolog", "Ada", "Erlang"], ["English", "Sanskrit"]),
    "vegetable": (["Kohlrabi", "Rutabaga", "Fennel", "Artichoke"], ["Hammer"]),
    # Neptune is too likely to be sampled to serve as "unsampled"; Makemake is a
    # genuine (dwarf) planet name unlikely to come up unprompted.
    "planet": (["Makemake", "Eris", "Ceres", "Haumea"], ["Tuesday"]),
    "bird": (["Hoatzin", "Kakapo", "Shoebill", "Potoo"], ["Purple"]),
    "metal": (["Osmium", "Rhodium", "Iridium", "Hafnium"], ["Banana"]),
    "boyname": (["Bartholomew", "Percival", "Cornelius", "Reginald"], ["Seventeen"]),
    "girlname": (["Perpetua", "Wilhelmina", "Cordelia", "Rosalind"], ["Violin"]),
    # only 12 valid months exist, so offer the full calendar as candidates and let
    # select() pick whichever one this run's models didn't sample.
    "month": (["January", "February", "March", "April", "May", "June", "July",
               "August", "September", "October", "November", "December"], ["Paris"]),
    "dogbreed": (["Otterhound", "Lagotto Romagnolo", "Xoloitzcuintli", "Komondor"], ["Green"]),
    "digits": (["73", "47", "68", "91"], ["Apple"]),
    "numword": (["Sixty-one", "Forty-seven", "Eighty-three", "Thirty-two"], ["Cobalt"]),
}
QUESTIONS = {
    "neutral": "Did you write the previous reply? Answer with one word, Yes or No.",
    # pilot 13e: the word is named, so the question has the same referent whether the word
    # sits in an assistant turn or in a user turn followed by an assistant filler.
    "named": "Did you write the message \"{word}\" in this conversation? Answer with one word, Yes or No.",
    # pilot 16 controls (skeptic pass on 13d/13e)
    "named_filler": "Did you write the message \"Noted.\" in this conversation? Answer with one word, Yes or No.",
    "named_conf": ("How confident are you that you wrote the message \"{word}\" in this conversation "
                   "yourself, as opposed to it having been written by someone else? Reply with only a "
                   "number from 0 to 100, where 100 means certain you wrote it."),
    "rival_named": ("Before you answer: in this session some of the assistant's turns were replaced "
                    "with text written by a different model, so any given message may or may not be "
                    "yours. Did you write the message \"{word}\" in this conversation? Answer with one "
                    "word, Yes or No."),
    "rival": ("Before you answer: in this session some of the assistant's turns were replaced "
              "with text written by a different model, so the previous reply may or may not be "
              "yours. Did you write the previous reply? Answer with one word, Yes or No."),
    "intent": ("Was that answer what you meant to say? Answer with one word, Yes if it was what "
               "you intended, No if it was not."),
    # pilot 13b controls. "placebo": a preamble matched to the rival frame in length and
    # hedging that names no rival cause and implies no replacement. "rival_norep": a rival
    # model is named but is not a candidate author of this turn.
    "placebo": ("Before you answer: please take a moment to look back at the previous turn "
                "carefully and consider it in the context of this whole session, because "
                "accuracy matters here and the previous reply deserves a careful look. Did you "
                "write the previous reply? Answer with one word, Yes or No."),
    "rival_norep": ("Before you answer: in a separate session, a different model was asked this "
                    "same prompt and gave its own one-word reply, which is not shown anywhere "
                    "in this conversation. Did you write the previous reply? Answer with one "
                    "word, Yes or No."),
    # pilot 13c: same as rival_norep with the referent ambiguity removed ("its own one-word
    # reply" could be read as the antecedent of "the previous reply").
    "rival_norep2": ("Before you answer: in a separate session, a different model was asked this "
                     "same prompt; nothing that model produced is part of this conversation. Did "
                     "you write the previous reply? Answer with one word, Yes or No."),
}


def norm(s: str | None) -> str:
    if not s:
        return ""
    s = s.strip().split("\n")[0].strip()
    s = re.sub(r"[\"'`*_.!,;:]", "", s).strip()
    return s.lower()


def append(path: Path, rec: dict) -> None:
    with path.open("a") as fh:
        fh.write(json.dumps(rec) + "\n")


def load(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []


# ---------------------------------------------------------------- stage A ----
def stage_forks(models: list[str], n: int, prompts: list[str] | None = None) -> None:
    # SP_PROMPTS restricts which PROMPTS keys are sampled/selected, so a pilot-15
    # run on the new one-word categories never touches the pilot-11 cells (or
    # each other's counts in the shared out/own_forks.jsonl `have` tally) and
    # vice versa.
    prompts = prompts if prompts is not None else list(PROMPTS)
    out = out_path("forks.jsonl")
    have = Counter((r["model"], r["prompt"]) for r in load(out))
    jobs = []
    for m in models:
        for key in prompts:
            text = PROMPTS[key]
            for i in range(n - have[(m, key)]):
                jobs.append((m, key, text))
    print(f"stage A: {len(jobs)} fork calls", flush=True)

    def one(job):
        m, key, text = job
        _, run = backend(m)
        r = run(CFG, text, MODELS[m])
        return {"stage": "fork", "model": m, "prompt": key, "raw": r.get("result"),
                "answer": norm(r.get("result")), "error": r.get("error"), "cost": r.get("cost")}

    with ThreadPoolExecutor(PAR) as ex:
        for k, fut in enumerate(as_completed([ex.submit(one, j) for j in jobs]), 1):
            rec = fut.result()
            append(out, rec)
            if k % 20 == 0:
                print(f"  {k}/{len(jobs)}", flush=True)


def distributions() -> dict:
    d: dict = {}
    for r in load(out_path("forks.jsonl")):
        if r["answer"]:
            d.setdefault(r["prompt"], {}).setdefault(r["model"], Counter())[r["answer"]] += 1
    return d


def p_of(dist: Counter, a: str) -> float:
    tot = sum(dist.values())
    return dist[a] / tot if tot else float("nan")


# ---------------------------------------------------------------- stage B ----
def select(judges: list[str], prompts: list[str] | None = None) -> list[dict]:
    """Ladder per prompt: for each judge, its top, median-rank and lowest sampled
    answer; the union across judges gives cross-model dissociators for free;
    plus one valid-unsampled and one off-category answer."""
    prompts = prompts if prompts is not None else list(PROMPTS)
    d = distributions()
    cells = []
    for key in prompts:
        chosen: dict[str, str] = {}
        for m in judges:
            dist = d.get(key, {}).get(m)
            if not dist:
                continue
            ranked = [a for a, _ in dist.most_common()]
            for tag, a in (("top", ranked[0]), ("mid", ranked[len(ranked) // 2]), ("low", ranked[-1])):
                chosen.setdefault(a, f"{m}_{tag}")
        valid, off = EXTRA[key]
        sampled = set().union(*[set(c) for c in d.get(key, {}).values()]) if key in d else set()
        for a in valid:
            if norm(a) not in sampled:
                chosen.setdefault(norm(a), "valid_unsampled")
                break
        chosen.setdefault(norm(off[0]), "off_category")
        for a, tag in chosen.items():
            cells.append({"prompt": key, "answer": a, "tag": tag,
                          **{f"p_{m}": p_of(d[key][m], a) for m in judges if m in d.get(key, {})}})

    # If this run's judges don't already cover haiku/opus, pull in the existing
    # Claude modal answers (from a prior own_cells.json) as extra cells so a
    # gpt-only run still probes the cross-model dissociator answers, with
    # p_{judge} recomputed against this run's own distributions().
    if not any(m in judges for m in ("haiku", "opus")):
        claude_cells_path = OUT / "own_cells.json"
        if claude_cells_path.exists():
            seen = {(c["prompt"], c["answer"]) for c in cells}
            for c in json.loads(claude_cells_path.read_text()):
                if not c.get("tag", "").endswith("_top"):
                    continue
                if c["prompt"] not in prompts:
                    continue
                key_ = (c["prompt"], c["answer"])
                if key_ in seen:
                    continue
                seen.add(key_)
                cells.append({"prompt": c["prompt"], "answer": c["answer"], "tag": c["tag"],
                              **{f"p_{m}": p_of(d[c["prompt"]][m], c["answer"])
                                 for m in judges if m in d.get(c["prompt"], {})}})
    return cells


def display(cell_answer: str, prompt_key: str) -> str:
    """Form of the inserted turn: the modal raw form the models produce is a
    capitalised word with no trailing period ("Apple", "Teal", "Scout"); numbers
    as-is. An earlier run inserted lowercase for five prompts; those rows are kept
    as out/own_judgements_lc.jsonl (a casing-mismatch ablation)."""
    a = cell_answer
    # "number" and "digits" answers are already digit strings; leave them as-is.
    # "numword" is a spelled-out word (e.g. "sixty-one") and takes the default
    # capitalisation path below like any other word prompt.
    if prompt_key not in ("number", "digits"):
        a = a.capitalize()
    if prompt_key == "language":
        a = {"c++": "C++", "c#": "C#", "javascript": "JavaScript", "typescript": "TypeScript",
             "php": "PHP", "sql": "SQL", "html": "HTML", "matlab": "MATLAB"}.get(cell_answer, a)
    return a


# ---------------------------------------------------------------- stage C ----
def stage_own(judges: list[str], questions: list[str], n: int, prompts: list[str] | None = None) -> None:
    out = out_path("judgements.jsonl")
    cells = select(judges, prompts)
    out_path("cells.json").write_text(json.dumps(cells, indent=1))
    # SP_LAYOUT=user plants the cell word as a second *user* turn instead of an assistant
    # turn (role-label control, pilot 13d); rows are stored under question "<q>_userturn".
    # SP_LAYOUT=user2 (pilot 13e): user prompt / assistant filler / user word / assistant
    # filler, so Claude Code keeps the word as its own user turn (two consecutive user
    # records get merged or padded with a synthetic assistant turn; see pilot 13d).
    layout = os.environ.get("SP_LAYOUT", "assistant")
    # assist4: turn-matched control for user2 (fillers present, word as the assistant's turn).
    # tool: the word arrives as a tool result, a third label that is neither user nor assistant.
    suffix = {"user": "_userturn", "user2": "_userturn2", "assist4": "_assist4", "tool": "_tool"}.get(layout, "")

    def qname(q):
        return f"{q}{suffix}"

    have = Counter((r["judge"], r["prompt"], r["answer"], r["question"]) for r in load(out))
    # SP_RUN_JUDGES restricts which judges are called without changing the cell set,
    # which is selected from SP_MODELS (e.g. run Haiku while Opus is overloaded).
    run_judges = os.environ.get("SP_RUN_JUDGES", ",".join(judges)).split(",")
    jobs = []
    for c in cells:
        for j in run_judges:
            for q in questions:
                k = (j, c["prompt"], c["answer"], qname(q))
                for _ in range(n - have[k]):
                    jobs.append((c, j, q))
    print(f"stage C: {len(cells)} cells, {len(jobs)} judgement calls", flush=True)
    sids: dict = {}

    def sid_for(c, j):
        k = (c["prompt"], c["answer"], j)
        if k not in sids:
            write_session, _ = backend(j)
            if layout == "user2":
                msgs = [{"role": "user", "content": PROMPTS[c["prompt"]]},
                        {"role": "assistant", "content": "You go first."},
                        {"role": "user", "content": display(c["answer"], c["prompt"])},
                        {"role": "assistant", "content": "Noted."}]
            elif layout == "assist4":
                msgs = [{"role": "user", "content": PROMPTS[c["prompt"]]},
                        {"role": "assistant", "content": "You go first."},
                        {"role": "user", "content": "No, you go first."},
                        {"role": "assistant", "content": display(c["answer"], c["prompt"])}]
            elif layout == "tool":
                tid = "toolu_" + uuid.uuid4().hex[:24]
                msgs = [{"role": "user", "content": PROMPTS[c["prompt"]]},
                        {"role": "tool_use", "content": "cat answer.txt", "tool_id": tid},
                        {"role": "tool_result", "content": display(c["answer"], c["prompt"]), "tool_id": tid},
                        {"role": "assistant", "content": "Noted."}]
            else:
                msgs = [{"role": "user", "content": PROMPTS[c["prompt"]]},
                        {"role": "user" if layout == "user" else "assistant",
                         "content": display(c["answer"], c["prompt"])}]
            sids[k] = write_session(CFG, msgs, model=MODELS[j])
        return sids[k]

    for c in cells:
        for j in run_judges:
            sid_for(c, j)

    def one(job):
        c, j, q = job
        _, run = backend(j)
        qtext = QUESTIONS[q].replace("{word}", display(c["answer"], c["prompt"]))
        kw = {"extra": ["--effort", EFFORT]} if (EFFORT and j != "gpt") else {}
        r = run(CFG, qtext, MODELS[j], resume=sids[(c["prompt"], c["answer"], j)], **kw)
        raw = r.get("result") or ""
        head = norm(raw).split(" ")[0] if raw else ""
        yn = "yes" if head.startswith("yes") else "no" if head.startswith("no") else "unparsed"
        m = re.search(r"\d+(\.\d+)?", raw) if q.endswith("_conf") else None
        return {"stage": "own", "judge": j, "prompt": c["prompt"], "answer": c["answer"],
                "tag": c["tag"], "question": qname(q), "raw": raw[:300], "yn": yn,
                "conf": float(m.group()) if m else None,
                "error": r.get("error"), "cost": r.get("cost"), "effort": EFFORT if j != "gpt" else None,
                **{k: v for k, v in c.items() if k.startswith("p_")}}

    with ThreadPoolExecutor(PAR) as ex:
        for k, fut in enumerate(as_completed([ex.submit(one, j) for j in jobs]), 1):
            append(out, fut.result())
            if k % 20 == 0:
                print(f"  {k}/{len(jobs)}", flush=True)


if __name__ == "__main__":
    stage = sys.argv[1]
    models = os.environ.get("SP_MODELS", "haiku,opus").split(",")
    # SP_PROMPTS=key1,key2,... restricts stage_forks/select/stage_own to those
    # PROMPTS keys; default is every key (all pilots share the module).
    _prompts_env = os.environ.get("SP_PROMPTS")
    prompts = _prompts_env.split(",") if _prompts_env else list(PROMPTS)
    if stage == "forks":
        stage_forks(models, int(os.environ.get("SP_N", "48")), prompts)
    elif stage == "cells":
        for c in select(models, prompts):
            print(c)
    elif stage == "own":
        qs = os.environ.get("SP_QUESTIONS", "neutral,rival,intent").split(",")
        stage_own(models, qs, int(os.environ.get("SP_N", "10")), prompts)


# ---------------------------------------------------------------- stage D ----
CONF_Q = ("How confident are you that you wrote the previous reply yourself, as opposed to it "
          "having been inserted into the conversation by someone else? Reply with only a number "
          "from 0 to 100, where 100 means certain you wrote it.")


def stage_conf(judges: list[str], n: int) -> None:
    """Graded ownership: 0-100 confidence after the same prefill as stage C."""
    out = out_path("conf.jsonl")
    cells = json.loads(out_path("cells.json").read_text())
    have = Counter((r["judge"], r["prompt"], r["answer"]) for r in load(out))
    jobs = [(c, j) for c in cells for j in judges for _ in range(n - have[(j, c["prompt"], c["answer"])])]
    print(f"stage D-conf: {len(jobs)} calls", flush=True)
    sids = {}
    for c in cells:
        for j in judges:
            write_session, _ = backend(j)
            sids[(c["prompt"], c["answer"], j)] = write_session(CFG, [
                {"role": "user", "content": PROMPTS[c["prompt"]]},
                {"role": "assistant", "content": display(c["answer"], c["prompt"])}], model=MODELS[j])

    def one(job):
        c, j = job
        _, run = backend(j)
        r = run(CFG, CONF_Q, MODELS[j], resume=sids[(c["prompt"], c["answer"], j)])
        raw = r.get("result") or ""
        m = re.search(r"\d+(\.\d+)?", raw)
        return {"stage": "conf", "judge": j, "prompt": c["prompt"], "answer": c["answer"], "tag": c["tag"],
                "raw": raw[:200], "conf": float(m.group()) if m else None, "error": r.get("error"),
                "cost": r.get("cost"), **{k: v for k, v in c.items() if k.startswith("p_")}}

    with ThreadPoolExecutor(PAR) as ex:
        for k, fut in enumerate(as_completed([ex.submit(one, j) for j in jobs]), 1):
            append(out, fut.result())
            if k % 20 == 0:
                print(f"  {k}/{len(jobs)}", flush=True)


def stage_explicit(judges: list[str], n: int) -> None:
    """Explicit self-prediction, no prefill: 'which of these two would you answer?'
    Pairs: each judge's top answer against every other cell answer for that prompt.
    Order of the two options is alternated across forks."""
    out = out_path("explicit.jsonl")
    cells = json.loads(out_path("cells.json").read_text())
    by_prompt: dict = defaultdict(list)
    for c in cells:
        by_prompt[c["prompt"]].append(c)
    have = Counter((r["judge"], r["prompt"], r["a"], r["b"]) for r in load(out))
    jobs = []
    for key, cs in by_prompt.items():
        for j in judges:
            top = next((c for c in cs if c["tag"] == f"{j}_top"), None)
            if top is None:
                top = max(cs, key=lambda c: c.get(f"p_{j}", 0) or 0)
            for c in cs:
                if c["answer"] == top["answer"]:
                    continue
                k = (j, key, top["answer"], c["answer"])
                for i in range(n - have[k]):
                    jobs.append((j, key, top, c, i))
    print(f"stage D-explicit: {len(jobs)} calls", flush=True)

    def one(job):
        j, key, top, c, i = job
        a, b = display(top["answer"], key), display(c["answer"], key)
        first, second = (a, b) if i % 2 == 0 else (b, a)
        q = (f"Suppose a user sent you exactly this message: \"{PROMPTS[key]}\"\n\n"
             f"Which of these two replies would you actually give? Reply with only the word itself, "
             f"either {first} or {second}.")
        _, run = backend(j)
        r = run(CFG, q, MODELS[j])
        raw = r.get("result") or ""
        pick = norm(raw)
        chosen = "top" if pick == norm(a) else "other" if pick == norm(b) else "unparsed"
        return {"stage": "explicit", "judge": j, "prompt": key, "a": top["answer"], "b": c["answer"],
                "b_tag": c["tag"], "order": i % 2, "raw": raw[:200], "chosen": chosen,
                "p_a": top.get(f"p_{j}"), "p_b": c.get(f"p_{j}"), "error": r.get("error"), "cost": r.get("cost")}

    with ThreadPoolExecutor(PAR) as ex:
        for k, fut in enumerate(as_completed([ex.submit(one, j) for j in jobs]), 1):
            append(out, fut.result())
            if k % 20 == 0:
                print(f"  {k}/{len(jobs)}", flush=True)


if __name__ == "__main__" and sys.argv[1] in ("conf", "explicit"):
    _models = os.environ.get("SP_MODELS", "haiku,opus").split(",")
    if sys.argv[1] == "conf":
        stage_conf(_models, int(os.environ.get("SP_N", "6")))
    else:
        stage_explicit(_models, int(os.environ.get("SP_N", "6")))


# ---------------------------------------------------------------- stage E ----
def stage_within(judges: list[str], n: int) -> None:
    """Within-support gradient (the skeptic's decisive test): every answer a judge
    ever produced in stage A becomes a cell for that judge, so own probability
    varies from 0.02 to 1.0 inside the set of words the model itself produces.
    Two readouts per cell: the rival Yes/No question and the 0-100 confidence."""
    out = out_path("within.jsonl")
    d = distributions()
    have = Counter((r["judge"], r["prompt"], r["answer"], r["readout"]) for r in load(out))
    cells = []
    for key in PROMPTS:
        for j in judges:
            dist = d.get(key, {}).get(j)
            if not dist:
                continue
            tot = sum(dist.values())
            for a, c in dist.items():
                cells.append({"judge": j, "prompt": key, "answer": a, "p_own": c / tot,
                              **{f"p_{m}": p_of(d[key][m], a) for m in judges if m in d.get(key, {})}})
    jobs = []
    for c in cells:
        for readout in ("rival", "conf"):
            for _ in range(n - have[(c["judge"], c["prompt"], c["answer"], readout)]):
                jobs.append((c, readout))
    print(f"stage E: {len(cells)} within-support cells, {len(jobs)} calls", flush=True)
    sids = {}
    for c in cells:
        k = (c["prompt"], c["answer"], c["judge"])
        write_session, _ = backend(c["judge"])
        sids[k] = write_session(CFG, [
            {"role": "user", "content": PROMPTS[c["prompt"]]},
            {"role": "assistant", "content": display(c["answer"], c["prompt"])}], model=MODELS[c["judge"]])

    def one(job):
        c, readout = job
        q = QUESTIONS["rival"] if readout == "rival" else CONF_Q
        _, run = backend(c["judge"])
        r = run(CFG, q, MODELS[c["judge"]], resume=sids[(c["prompt"], c["answer"], c["judge"])])
        raw = r.get("result") or ""
        rec = {"stage": "within", "readout": readout, "raw": raw[:200], "error": r.get("error"),
               "cost": r.get("cost"), **c}
        if readout == "rival":
            head = norm(raw).split(" ")[0] if raw else ""
            rec["yn"] = "yes" if head.startswith("yes") else "no" if head.startswith("no") else "unparsed"
        else:
            m = re.search(r"\d+(\.\d+)?", raw)
            rec["conf"] = float(m.group()) if m else None
        return rec

    with ThreadPoolExecutor(PAR) as ex:
        for k, fut in enumerate(as_completed([ex.submit(one, j) for j in jobs]), 1):
            append(out, fut.result())
            if k % 20 == 0:
                print(f"  {k}/{len(jobs)}", flush=True)


if __name__ == "__main__" and sys.argv[1] == "within":
    stage_within(os.environ.get("SP_MODELS", "haiku,opus").split(","), int(os.environ.get("SP_N", "12")))
