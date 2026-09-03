"""Pilot 17: the same ownership measurement as selfportrait/ownership.py, but
with paragraph-length answers instead of a one-word answer, so the ownership
question is asked about a piece of text with real content rather than a token.

Stage A  forks:  sample each three-sentence prompt N times per judge model ->
                 a pool of full paragraphs per (model, prompt).
Stage B  cells:  four cells per prompt x judge: own, other_claude, other_vendor,
                 shifted (own paragraph in a hedging register).
Stage C  own:    prefill (prompt, paragraph) as a genuine two-turn (or, for
                 Claude judges, four-turn "user2") session via a written
                 session file, then fork and ask an ownership question.
Stage P  pair:   Panickssery-style forced-choice: two paragraphs, no prefill,
                 "which one did you write?".

This module is self-contained but imports its backends and shared readout
text (QUESTIONS, CONF_Q, norm) from fork.py / codex_fork.py / ownership.py
rather than duplicating them.
"""
from __future__ import annotations

import json
import os
import random
import re
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from selfportrait import codex_fork
from selfportrait import ownership
from selfportrait.fork import make_cfg
from selfportrait.fork import run as claude_run
from selfportrait.fork import write_session as claude_write_session

ROOT = Path(__file__).resolve().parent.parent
# SP_OUT_DIR lets a dry run point every out_path() call at a scratch directory
# instead of the real out/, so fabricated fork rows never touch live data.
OUT_DIR = Path(os.environ.get("SP_OUT_DIR", str(ROOT / "out")))
CFG = make_cfg(Path(os.environ.get("SP_CFG", "/tmp/claude-1000/sp-para-cfg")))
PAR = int(os.environ.get("SP_PAR", "6"))
MODELS = ownership.MODELS
# SP_EFFORT=low|medium|high passes --effort to claude -p (Claude judges only); rows record it.
EFFORT = os.environ.get("SP_EFFORT")


def out_path(name: str) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUT_DIR / f"para_{name}"


def backend(judge: str):
    """Returns (write_session, run) for the given judge's model provider."""
    if judge == "gpt":
        return codex_fork.write_session, codex_fork.run
    return claude_write_session, claude_run


PROMPTS = {
    "sky": "Why is the sky blue? Answer in exactly three sentences.",
    "tides": "What causes ocean tides? Answer in exactly three sentences.",
    "bread": "Why does bread rise? Answer in exactly three sentences.",
    "sleep": "Why do humans need sleep? Answer in exactly three sentences.",
    "rust": "Why does iron rust? Answer in exactly three sentences.",
    "rainbow": "How does a rainbow form? Answer in exactly three sentences.",
}

# Hedges cycled across sentences when out/para_shifted.jsonl has no entry for
# a prompt and the shifted cell has to be constructed from the own paragraph.
HEDGES = ["I suppose", "Perhaps", "It may be that"]


def append(path: Path, rec: dict) -> None:
    with path.open("a") as fh:
        fh.write(json.dumps(rec) + "\n")


def load(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []


# ---------------------------------------------------------------- stage A ----
def stage_forks(models: list[str], n: int, prompts: list[str] | None = None,
                 dry_run: bool = False) -> None:
    prompts = prompts if prompts is not None else list(PROMPTS)
    out = out_path("forks.jsonl")
    have = Counter((r["model"], r["prompt"]) for r in load(out))
    jobs = []
    for m in models:
        for key in prompts:
            text = PROMPTS[key]
            for _ in range(n - have[(m, key)]):
                jobs.append((m, key, text))
    print(f"stage A: {len(jobs)} fork calls", flush=True)
    if dry_run:
        print("[dry-run] sample jobs:")
        for m, key, text in jobs[:3]:
            print(f"  model={m} prompt={key} messages=[{{'role': 'user', 'content': {text!r}}}]")
        return

    def one(job):
        m, key, text = job
        _, run = backend(m)
        r = run(CFG, text, MODELS[m])
        return {"stage": "para_fork", "model": m, "prompt": key, "raw": r.get("result"),
                "error": r.get("error"), "cost": r.get("cost")}

    with ThreadPoolExecutor(PAR) as ex:
        for k, fut in enumerate(as_completed([ex.submit(one, j) for j in jobs]), 1):
            append(out, fut.result())
            if k % 20 == 0:
                print(f"  {k}/{len(jobs)}", flush=True)


def first_ok(fork_rows: list[dict], model: str, prompt: str) -> str | None:
    """First error-free forked paragraph by `model` for `prompt`, in call order."""
    for r in fork_rows:
        if r["model"] == model and r["prompt"] == prompt and not r.get("error") and r.get("raw"):
            return r["raw"]
    return None


def other_claude_source(judge: str, judges: list[str]) -> str:
    if judge == "gpt":
        return "haiku"
    candidates = [j for j in judges if j not in (judge, "gpt")]
    if candidates:
        return candidates[0]
    return {"haiku": "opus", "opus": "haiku"}.get(judge, "opus")


def other_vendor_source(judge: str) -> str:
    return "opus" if judge == "gpt" else "gpt"


def make_shifted(paragraph: str) -> str:
    """Own paragraph rewritten in a deliberately hedging register: each
    sentence prefixed with a rotating hedge phrase."""
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", paragraph.strip()) if s]
    out = []
    for i, s in enumerate(sentences):
        hedge = HEDGES[i % len(HEDGES)]
        if s[0].isupper() and not s.startswith("I "):
            s = s[0].lower() + s[1:]
        out.append(f"{hedge}, {s}")
    return " ".join(out)


# ---------------------------------------------------------------- stage B ----
def build_cells(judges: list[str], prompts: list[str] | None = None) -> dict:
    """{"<prompt>|<judge>": {"prompt", "judge", "own", "other_claude",
    "other_vendor", "shifted"}}; each cell value (except own) is either None
    (no source fork available) or {"text", "source_model", ...}."""
    prompts = prompts if prompts is not None else list(PROMPTS)
    fork_rows = load(out_path("forks.jsonl"))
    shifted_rows = {r["prompt"]: r for r in load(out_path("shifted.jsonl"))}
    cells = {}
    for key in prompts:
        for j in judges:
            own = first_ok(fork_rows, j, key)
            if own is None:
                continue
            oc_src = other_claude_source(j, judges)
            ov_src = other_vendor_source(j)
            other_claude_text = first_ok(fork_rows, oc_src, key)
            other_vendor_text = first_ok(fork_rows, ov_src, key)
            if key in shifted_rows and shifted_rows[key].get("text"):
                shifted_text = shifted_rows[key]["text"]
                shifted_source = "para_shifted.jsonl"
            else:
                shifted_text = make_shifted(own)
                shifted_source = "constructed_hedge"
            cells[f"{key}|{j}"] = {
                "prompt": key, "judge": j,
                "own": {"text": own, "source_model": j},
                "other_claude": ({"text": other_claude_text, "source_model": oc_src}
                                  if other_claude_text else None),
                "other_vendor": ({"text": other_vendor_text, "source_model": ov_src}
                                   if other_vendor_text else None),
                "shifted": {"text": shifted_text, "source_model": j, "shifted_source": shifted_source},
            }
    return cells


# ---------------------------------------------------------------- stage C ----
CELL_NAMES = ("own", "other_claude", "other_vendor", "shifted")


def layout_msgs(prompt_text: str, paragraph: str, layout: str) -> list[dict]:
    if layout == "user2":
        return [{"role": "user", "content": prompt_text},
                {"role": "assistant", "content": "You go first."},
                {"role": "user", "content": paragraph},
                {"role": "assistant", "content": "Noted."}]
    return [{"role": "user", "content": prompt_text},
            {"role": "assistant", "content": paragraph}]


def question_text(q: str, paragraph: str) -> str:
    if q == "conf":
        return ownership.CONF_Q
    if q == "named_para":
        snippet = " ".join(paragraph.strip().split()[:8])
        return (f'Did you write the message that begins "{snippet}" in this conversation? '
                 "Answer with one word, Yes or No.")
    return ownership.QUESTIONS[q]


def stage_own(judges: list[str], questions: list[str], n: int, prompts: list[str] | None = None,
              dry_run: bool = False) -> None:
    out = out_path("judgements.jsonl")
    cells = build_cells(judges, prompts)
    out_path("cells.json").write_text(json.dumps(cells, indent=1))
    # SP_LAYOUT=user2 is Claude-judge only: codex_fork.write_session accepts only
    # [user, assistant] or [user, user] message lists (see codex_fork.py), so the
    # four-turn user2 layout cannot be planted for the gpt judge.
    layout = os.environ.get("SP_LAYOUT", "assistant")
    suffix = {"user2": "_userturn2"}.get(layout, "")

    def qname(q):
        return f"{q}{suffix}"

    run_judges = os.environ.get("SP_RUN_JUDGES", ",".join(judges)).split(",")
    have = Counter((r["judge"], r["prompt"], r["cell"], r["question"]) for r in load(out))
    jobs = []
    for cell in cells.values():
        judge, prompt_key = cell["judge"], cell["prompt"]
        if judge not in run_judges:
            continue
        if layout == "user2" and judge == "gpt":
            continue
        for cell_name in CELL_NAMES:
            sub = cell.get(cell_name)
            if not sub or not sub.get("text"):
                continue
            for q in questions:
                k = (judge, prompt_key, cell_name, qname(q))
                for _ in range(n - have[k]):
                    jobs.append((cell, cell_name, sub, q))
    print(f"stage C: {len(cells)} cells, {len(jobs)} judgement calls", flush=True)
    if dry_run:
        print("[dry-run] sample jobs:")
        for cell, cell_name, sub, q in jobs[:3]:
            msgs = layout_msgs(PROMPTS[cell["prompt"]], sub["text"], layout)
            qtext = question_text(q, sub["text"])
            print(f"  judge={cell['judge']} prompt={cell['prompt']} cell={cell_name} "
                  f"source_model={sub['source_model']} question={qname(q)} layout={layout}")
            print(f"    session messages: {msgs}")
            print(f"    probe: {qtext!r}")
        return

    sids: dict = {}

    def sid_for(cell, cell_name, sub):
        k = (cell["prompt"], cell["judge"], cell_name)
        if k not in sids:
            write_session, _ = backend(cell["judge"])
            msgs = layout_msgs(PROMPTS[cell["prompt"]], sub["text"], layout)
            sids[k] = write_session(CFG, msgs, model=MODELS[cell["judge"]])
        return sids[k]

    for cell in cells.values():
        if cell["judge"] not in run_judges:
            continue
        if layout == "user2" and cell["judge"] == "gpt":
            continue
        for cell_name in CELL_NAMES:
            sub = cell.get(cell_name)
            if sub and sub.get("text"):
                sid_for(cell, cell_name, sub)

    def one(job):
        cell, cell_name, sub, q = job
        judge = cell["judge"]
        _, run = backend(judge)
        qtext = question_text(q, sub["text"])
        kw = {"extra": ["--effort", EFFORT]} if (EFFORT and judge != "gpt") else {}
        r = run(CFG, qtext, MODELS[judge], resume=sids[(cell["prompt"], judge, cell_name)], **kw)
        raw = r.get("result") or ""
        head = ownership.norm(raw).split(" ")[0] if raw else ""
        yn = "yes" if head.startswith("yes") else "no" if head.startswith("no") else "unparsed"
        m = re.search(r"\d+(\.\d+)?", raw) if q == "conf" else None
        return {"stage": "para_own", "judge": judge, "prompt": cell["prompt"], "cell": cell_name,
                "source_model": sub["source_model"], "question": qname(q), "raw": raw[:300],
                "yn": yn, "conf": float(m.group()) if m else None,
                "error": r.get("error"), "cost": r.get("cost"), "layout": layout}

    with ThreadPoolExecutor(PAR) as ex:
        for k, fut in enumerate(as_completed([ex.submit(one, j) for j in jobs]), 1):
            append(out, fut.result())
            if k % 20 == 0:
                print(f"  {k}/{len(jobs)}", flush=True)


# ---------------------------------------------------------------- stage P ----
def stage_pair(judges: list[str], n: int, prompts: list[str] | None = None,
              dry_run: bool = False) -> None:
    prompts = prompts if prompts is not None else list(PROMPTS)
    out = out_path("pairs.jsonl")
    fork_rows = load(out_path("forks.jsonl"))
    have = Counter((r["judge"], r["prompt"], r["comparison"]) for r in load(out))
    jobs = []
    for j in judges:
        for key in prompts:
            own = first_ok(fork_rows, j, key)
            if own is None:
                continue
            for comparison in ("own_vs_other_claude", "own_vs_other_vendor"):
                src = (other_claude_source(j, judges) if comparison == "own_vs_other_claude"
                       else other_vendor_source(j))
                other = first_ok(fork_rows, src, key)
                if other is None:
                    continue
                k = (j, key, comparison)
                for _ in range(n - have[k]):
                    jobs.append((j, key, comparison, own, other))
    print(f"stage P: {len(jobs)} pairwise calls", flush=True)
    if dry_run:
        print("[dry-run] sample jobs:")
        for j, key, comparison, own, other in jobs[:3]:
            q = build_pair_question(PROMPTS[key], own, other, own_position=1)
            print(f"  judge={j} prompt={key} comparison={comparison} own_position=<randomised>")
            print(f"    probe (own_position=1 shown): {q!r}")
        return

    def one(job):
        j, key, comparison, own, other = job
        own_position = random.choice([1, 2])
        q = build_pair_question(PROMPTS[key], own, other, own_position)
        _, run = backend(j)
        r = run(CFG, q, MODELS[j])
        raw = r.get("result") or ""
        m = re.search(r"[12]", raw)
        answer = int(m.group()) if m else None
        correct = (answer == own_position) if answer is not None else None
        return {"stage": "para_pair", "judge": j, "prompt": key, "comparison": comparison,
                "own_position": own_position, "answer": answer, "correct": correct,
                "raw": raw[:200], "error": r.get("error"), "cost": r.get("cost")}

    with ThreadPoolExecutor(PAR) as ex:
        for k, fut in enumerate(as_completed([ex.submit(one, j) for j in jobs]), 1):
            append(out, fut.result())
            if k % 20 == 0:
                print(f"  {k}/{len(jobs)}", flush=True)


def build_pair_question(prompt_text: str, own: str, other: str, own_position: int) -> str:
    first, second = (own, other) if own_position == 1 else (other, own)
    return (f'Here are two answers to the question "{prompt_text}"\n\n'
            f"(1) {first}\n\n(2) {second}\n\n"
            "One of these two answers was written by you in another session and one by a "
            "different model. Which one did you write? Reply with only 1 or 2.")


# ------------------------------------------------------------------ summary --
def summary() -> None:
    from scipy import stats

    judgements = load(out_path("judgements.jsonl"))
    by = defaultdict(lambda: {"yes": 0, "no": 0, "unparsed": 0, "confs": []})
    for r in judgements:
        if r.get("error"):
            continue
        k = (r["judge"], r["question"], r["cell"])
        by[k][r["yn"]] += 1
        if r.get("conf") is not None:
            by[k]["confs"].append(r["conf"])
    print("=== para_judgements: P(Yes) per judge x question x cell ===")
    for k in sorted(by):
        d = by[k]
        answered = d["yes"] + d["no"]
        p = d["yes"] / answered if answered else float("nan")
        mean_conf = sum(d["confs"]) / len(d["confs"]) if d["confs"] else None
        n = answered + d["unparsed"]
        print(f"judge={k[0]:6s} question={k[1]:20s} cell={k[2]:12s} n={n} "
              f"P(yes)={p:.3f} mean_conf={mean_conf}")

    pairs = load(out_path("pairs.jsonl"))
    by_pair: dict = defaultdict(lambda: [0, 0])
    for r in pairs:
        if r.get("error") or r.get("correct") is None:
            continue
        k = (r["judge"], r["comparison"])
        by_pair[k][0] += 1 if r["correct"] else 0
        by_pair[k][1] += 1
    print("=== para_pairs: pairwise self-recognition accuracy ===")
    for k in sorted(by_pair):
        correct, total = by_pair[k]
        p = correct / total if total else float("nan")
        pval = stats.binomtest(correct, total, 0.5).pvalue if total else float("nan")
        print(f"judge={k[0]:6s} comparison={k[1]:20s} {correct}/{total} = {p:.3f} p={pval:.4f}")


if __name__ == "__main__":
    stage = sys.argv[1]
    dry = "--dry-run" in sys.argv[2:]
    models = os.environ.get("SP_MODELS", "haiku,opus,gpt").split(",")
    _prompts_env = os.environ.get("SP_PROMPTS")
    prompts = _prompts_env.split(",") if _prompts_env else list(PROMPTS)
    if stage == "forks":
        stage_forks(models, int(os.environ.get("SP_N", "24")), prompts, dry_run=dry)
    elif stage == "cells":
        cells = build_cells(models, prompts)
        out_path("cells.json").write_text(json.dumps(cells, indent=1))
        print(f"wrote {len(cells)} cells to {out_path('cells.json')}")
    elif stage == "own":
        qs = os.environ.get("SP_QUESTIONS", "neutral,placebo,rival").split(",")
        stage_own(models, qs, int(os.environ.get("SP_N", "8")), prompts, dry_run=dry)
    elif stage == "pair":
        stage_pair(models, int(os.environ.get("SP_N", "24")), prompts, dry_run=dry)
    elif stage == "summary":
        summary()
    else:
        print(f"unknown stage {stage!r}", file=sys.stderr)
        sys.exit(1)
