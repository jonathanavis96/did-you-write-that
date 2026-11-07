"""Failed calls stay on file as error rows, but a resumed stage must call them again:
a row only counts towards SP_N if it holds an answer."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from selfportrait import listing13, ownership, paragraph  # noqa: E402

OK = {"error": None}
FAILED = {"error": "timeout after 300s"}
OWN_PROMPT = next(iter(ownership.PROMPTS))
PARA_PROMPT = "sky"


def rows(path):
    return [json.loads(ln) for ln in path.read_text().splitlines()]


def wire(module, monkeypatch, tmp_path, reply="50"):
    """Route `module`'s output into tmp_path and count the model calls."""
    calls = []

    def run(cfg, q, model, **kw):
        calls.append(q)
        return {"result": reply}

    monkeypatch.setattr(module, "backend", lambda j: (lambda *a, **k: "sid", run))
    monkeypatch.setattr(module, "out_path", lambda name: tmp_path / name)
    monkeypatch.setattr(module, "PAR", 1)
    return calls


def seed(path, row):
    """One good row and one failed row under the same key."""
    path.write_text(json.dumps({**row, **OK}) + "\n" + json.dumps({**row, **FAILED}) + "\n")


def own_cell(answer="red", **kw):
    return {"prompt": OWN_PROMPT, "answer": answer, "tag": "opus_top", "p_opus": 0.5, **kw}


@pytest.mark.parametrize("module", [ownership, paragraph])
def test_stage_forks_retries_failed_rows(module, monkeypatch, tmp_path):
    calls = wire(module, monkeypatch, tmp_path)
    key = OWN_PROMPT if module is ownership else PARA_PROMPT
    seed(tmp_path / "forks.jsonl", {"model": "opus", "prompt": key, "answer": "a"})
    module.stage_forks(["opus"], 2, [key])
    assert len(calls) == 1


def test_ownership_stage_own_retries_failed_rows(monkeypatch, tmp_path):
    calls = wire(ownership, monkeypatch, tmp_path)
    cells = tmp_path / "chosen.json"
    cells.write_text(json.dumps([own_cell()]))
    monkeypatch.setenv("SP_CELLS_FILE", str(cells))
    seed(tmp_path / "judgements.jsonl", {"judge": "opus", "prompt": OWN_PROMPT, "answer": "red",
                                         "question": "neutral"})
    ownership.stage_own(["opus"], ["neutral"], 2)
    assert len(calls) == 1


def test_ownership_stage_conf_retries_failed_rows(monkeypatch, tmp_path):
    calls = wire(ownership, monkeypatch, tmp_path)
    (tmp_path / "cells.json").write_text(json.dumps([own_cell()]))
    seed(tmp_path / "conf.jsonl", {"judge": "opus", "prompt": OWN_PROMPT, "answer": "red"})
    ownership.stage_conf(["opus"], 2)
    assert len(calls) == 1


@pytest.mark.parametrize("failed_order", [0, 1])
def test_ownership_stage_explicit_refills_the_failed_order(monkeypatch, tmp_path, failed_order):
    calls = wire(ownership, monkeypatch, tmp_path)
    (tmp_path / "cells.json").write_text(json.dumps([
        own_cell("red"), own_cell("blue", tag="opus_low", p_opus=0.1)]))
    out = tmp_path / "explicit.jsonl"
    row = {"judge": "opus", "prompt": OWN_PROMPT, "a": "red", "b": "blue"}
    out.write_text(json.dumps({**row, "order": 1 - failed_order, **OK}) + "\n"
                   + json.dumps({**row, "order": failed_order, **FAILED}) + "\n")
    ownership.stage_explicit(["opus"], 2)
    assert len(calls) == 1
    assert rows(out)[-1]["order"] == failed_order


def test_ownership_stage_within_retries_failed_rows(monkeypatch, tmp_path):
    calls = wire(ownership, monkeypatch, tmp_path)
    (tmp_path / "forks.jsonl").write_text(json.dumps(
        {"model": "opus", "prompt": OWN_PROMPT, "answer": "red"}) + "\n")
    with (tmp_path / "within.jsonl").open("w") as fh:
        for readout, extra in (("rival", FAILED), ("conf", OK)):
            fh.write(json.dumps({"judge": "opus", "prompt": OWN_PROMPT, "answer": "red",
                                 "readout": readout, **extra}) + "\n")
    ownership.stage_within(["opus"], 1)
    assert len(calls) == 1


def test_paragraph_stage_own_retries_failed_rows(monkeypatch, tmp_path):
    calls = wire(paragraph, monkeypatch, tmp_path)
    (tmp_path / "forks.jsonl").write_text(json.dumps(
        {"model": "opus", "prompt": PARA_PROMPT, "raw": "Own text."}) + "\n")
    monkeypatch.setattr(paragraph, "CELL_NAMES", ("own",))
    seed(tmp_path / "judgements.jsonl", {"judge": "opus", "prompt": PARA_PROMPT, "cell": "own",
                                         "question": "neutral"})
    paragraph.stage_own(["opus"], ["neutral"], 2, [PARA_PROMPT])
    assert len(calls) == 1


def test_paragraph_stage_pair_retries_failed_rows(monkeypatch, tmp_path):
    calls = wire(paragraph, monkeypatch, tmp_path, reply="1")
    (tmp_path / "forks.jsonl").write_text("".join(
        json.dumps({"model": m, "prompt": PARA_PROMPT, "raw": f"By {m}."}) + "\n"
        for m in ("opus", "haiku", "gpt")))
    monkeypatch.setattr(paragraph, "TEXT_NORM", False)
    for comparison in ("own_vs_other_claude", "own_vs_other_vendor"):
        with (tmp_path / "pairs.jsonl").open("a") as fh:
            row = {"judge": "opus", "prompt": PARA_PROMPT, "comparison": comparison}
            fh.write(json.dumps({**row, **OK}) + "\n" + json.dumps({**row, **FAILED}) + "\n")
    paragraph.stage_pair(["opus"], 2, [PARA_PROMPT])
    assert len(calls) == 2


def test_listing13_retries_failed_sessions(monkeypatch, tmp_path):
    out = tmp_path / "out.jsonl"
    out.write_text(json.dumps({"sid": "done", "result": "x", "error": None}) + "\n"
                   + json.dumps({"sid": "failed", "result": None, "error": "timeout after 900s"}) + "\n")
    monkeypatch.setattr(listing13, "OUT", out)
    assert listing13.load_done() == {"done"}
