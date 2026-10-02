"""The resumable stages re-read their own append-only output; a run killed mid-append
leaves a torn last line that must not stop the next run from resuming."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from selfportrait.jsonl import load  # noqa: E402


def test_missing_file_is_empty(tmp_path):
    assert load(tmp_path / "nope.jsonl") == []


def test_torn_last_line_and_blank_lines_are_skipped(tmp_path, capsys):
    p = tmp_path / "forks.jsonl"
    p.write_text(json.dumps({"a": 1}) + "\n\n" + json.dumps({"a": 2}) + "\n" + '{"a": 3, "ra')
    assert load(p) == [{"a": 1}, {"a": 2}]
    assert "torn" in capsys.readouterr().err


def test_corrupt_middle_line_still_raises(tmp_path):
    p = tmp_path / "forks.jsonl"
    p.write_text('{"a": 1}\nnot json\n{"a": 2}\n')
    with pytest.raises(json.JSONDecodeError):
        load(p)


@pytest.mark.parametrize("module", ["ownership", "paragraph"])
def test_resume_after_torn_line_keeps_the_new_row(tmp_path, capsys, module):
    """load -> append -> load: the resumed run's row must not be glued onto the fragment."""
    import importlib

    stage = importlib.import_module(f"selfportrait.{module}")
    p = tmp_path / "forks.jsonl"
    good = json.dumps({"a": 1}) + "\n" + json.dumps({"a": 2, "s": "é"}) + "\n"
    p.write_bytes(good.encode() + b'{"a": 3, "ra')  # run killed mid-append
    assert stage.load(p) == [{"a": 1}, {"a": 2, "s": "é"}]
    stage.append(p, {"a": 3})  # resumed run redoes the row
    data = p.read_bytes()
    assert data == good.encode() + (json.dumps({"a": 3}) + "\n").encode()
    assert b'"ra' not in data
    assert stage.load(p) == [{"a": 1}, {"a": 2, "s": "é"}, {"a": 3}]
    stage.append(p, {"a": 4})
    assert stage.load(p)[-2:] == [{"a": 3}, {"a": 4}]
    assert "12 bytes" in capsys.readouterr().err


def test_append_leaves_a_newline_terminated_file_byte_identical(tmp_path):
    from selfportrait import ownership

    p = tmp_path / "forks.jsonl"
    before = b'{"a": 1}\n{"b":   2}\n'
    p.write_bytes(before)
    ownership.append(p, {"c": 3})
    assert p.read_bytes() == before + b'{"c": 3}\n'
