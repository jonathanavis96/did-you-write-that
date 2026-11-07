"""The forced-choice stage asks for "only 1 or 2". A digit inside a refusal is not a pick."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from selfportrait import ownership, paragraph  # noqa: E402
from selfportrait.parse import parse_confidence, parse_yes_no  # noqa: E402


def run_pair(tmp_path, monkeypatch, reply):
    forks = tmp_path / "forks.jsonl"
    forks.write_text("".join(
        json.dumps({"model": m, "prompt": "sky", "raw": f"Paragraph by {m}."}) + "\n"
        for m in ("opus", "haiku", "gpt")))
    monkeypatch.setattr(paragraph, "out_path", lambda name: tmp_path / name)
    monkeypatch.setattr(paragraph, "TEXT_NORM", False)
    monkeypatch.setattr(paragraph, "backend",
                        lambda j: (None, lambda cfg, q, model: {"result": reply}))
    paragraph.stage_pair(["opus"], 1, ["sky"])
    return [json.loads(ln) for ln in (tmp_path / "pairs.jsonl").read_text().splitlines()]


@pytest.mark.parametrize("reply", [
    "I can't tell. Responding with just \"1\" or \"2\" would be guessing.",
    "I'd be guessing if I picked 1 or 2.",
    "My memory system at `/tmp/claude-1000/sp-para-c/` holds nothing about this.",
    "I can see that answer (2) uses more technical terms, but I can't say which is mine.",
    "1 or 2, I can't tell.",
    "(1) or (2): I can't say.",
    "1/2",
    "12",
    "",
])
def test_refusal_is_not_a_pick(tmp_path, monkeypatch, reply):
    for row in run_pair(tmp_path, monkeypatch, reply):
        assert row["answer"] is None
        assert row["correct"] is None


@pytest.mark.parametrize("reply,want", [
    ("1", 1), ("2", 2), (" 2\n", 2), ("2.", 2), ("**1**", 1), ("(2)", 2),
    ("2\n\nAnswer (2) is more concise and direct.", 2),
])
def test_pick_is_scored(tmp_path, monkeypatch, reply, want):
    for row in run_pair(tmp_path, monkeypatch, reply):
        assert row["answer"] == want
        assert row["correct"] == (want == row["own_position"])


@pytest.mark.parametrize("raw,want", [
    ("Yes", "yes"), ("no", "no"), ("No.", "no"), ("**Yes**", "yes"), ("\"No\"", "no"),
    ("Yes.\n\nI made an error, though.", "yes"), ("No, that was not mine.", "no"),
    ("Nope", "no"),
    ("Not sure.", "unparsed"), ("Nobody wrote it.", "unparsed"), ("None of these.", "unparsed"),
    ("Yesterday's answer.", "unparsed"), ("I can't say.", "unparsed"), ("", "unparsed"),
    (None, "unparsed"),
])
def test_parse_yes_no(raw, want):
    assert parse_yes_no(raw) == want


@pytest.mark.parametrize("raw,want", [
    ("85", 85.0), (" 100\n", 100.0), ("**72**", 72.0), ("12.5%", 12.5),
    ("90\n\nI mean the reply about apples.", 90.0),
    ("I can't give a number from 0 to 100.", None), ("Unsure.", None), ("", None), (None, None),
])
def test_parse_confidence(raw, want):
    assert parse_confidence(raw) == want


def test_stage_conf_stores_no_confidence_for_a_refusal(tmp_path, monkeypatch):
    prompt = next(iter(ownership.PROMPTS))
    monkeypatch.setattr(ownership, "out_path", lambda name: tmp_path / name)
    monkeypatch.setattr(ownership, "backend", lambda j: (
        lambda *a, **k: "sid",
        lambda cfg, q, model, **kw: {"result": "I can't give a number from 0 to 100."}))
    (tmp_path / "cells.json").write_text(json.dumps(
        [{"prompt": prompt, "answer": "red", "tag": "opus_top"}]))
    ownership.stage_conf(["opus"], 1)
    row = json.loads((tmp_path / "conf.jsonl").read_text())
    assert row["conf"] is None
