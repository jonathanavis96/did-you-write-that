"""Writers that append to their own JSONL output must cut off a torn last line left by a
killed run before appending, or the next row is glued onto the fragment and lost."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from selfportrait import gpt_conf_calib, listing13  # noqa: E402

GOOD = {"sid": "old", "result": "x"}
TORN = '{"sid": "half'


def run_listing13(tmp_path, monkeypatch, out):
    session = tmp_path / "rollout-1.jsonl"
    session.write_text(json.dumps({"payload": {"id": "new"}}) + "\n")
    monkeypatch.setattr(listing13, "OUT", out)
    monkeypatch.setattr(listing13, "PATTERN", str(session))
    monkeypatch.setattr(listing13.codex_fork, "run",
                        lambda *a, **k: {"result": "listed", "error": None})
    listing13.main()
    return "new"


def run_gpt_conf_calib(tmp_path, monkeypatch, out):
    monkeypatch.setenv("SP_N", "1")
    monkeypatch.setattr(gpt_conf_calib, "ITEMS", {"coin_two": "a coin"})
    monkeypatch.setattr(gpt_conf_calib, "out_path", lambda name: out)
    monkeypatch.setattr(gpt_conf_calib, "run", lambda cfg, q: {"result": "25", "error": None})
    gpt_conf_calib.main()
    return "coin_two"


@pytest.mark.parametrize("runner,key", [(run_listing13, "sid"), (run_gpt_conf_calib, "item")])
def test_resume_after_torn_line(tmp_path, monkeypatch, runner, key):
    out = tmp_path / "out.jsonl"
    out.write_text(json.dumps(GOOD) + "\n" + TORN)
    want = runner(tmp_path, monkeypatch, out)
    rows = [json.loads(ln) for ln in out.read_text().splitlines() if ln.strip()]
    assert rows[0] == GOOD
    assert [r[key] for r in rows[1:]] == [want]
    assert out.read_text().endswith("\n")
