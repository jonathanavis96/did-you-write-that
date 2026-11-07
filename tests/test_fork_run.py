"""Failure handling of the two fork backends' run(): no real CLI is ever called."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from selfportrait import codex_fork, fork  # noqa: E402


def _raise_timeout(cmd, **kw):
    raise subprocess.TimeoutExpired(cmd, kw.get("timeout"))


def test_codex_run_timeout_returns_error_row(monkeypatch, tmp_path):
    # A hung `codex exec` must become an error row like fork.run's, not an exception
    # that aborts the whole ThreadPool stage via fut.result().
    monkeypatch.setattr(codex_fork.subprocess, "run", _raise_timeout)
    r = codex_fork.run(None, "probe", cwd=tmp_path, timeout=7)
    assert r["result"] is None
    assert r["error"] == "timeout after 7s"


def test_claude_run_non_object_json_returns_error_row(monkeypatch, tmp_path):
    # stdout that parses as JSON but is not an object (e.g. the --verbose event list)
    # must not crash on d.get().
    def fake(cmd, **kw):
        return subprocess.CompletedProcess(cmd, 0, stdout='[{"type": "system"}]', stderr="")

    monkeypatch.setattr(fork.subprocess, "run", fake)
    r = fork.run(tmp_path, "probe", cwd=tmp_path / "cwd")
    assert r["result"] is None
    assert "system" in r["error"]


def _claude_reply(monkeypatch, payload):
    def fake(cmd, **kw):
        return subprocess.CompletedProcess(cmd, 1, stdout=json.dumps(payload), stderr="")

    monkeypatch.setattr(fork.subprocess, "run", fake)


def test_claude_api_error_is_an_error_row_not_an_answer(monkeypatch, tmp_path):
    # claude -p reports an API failure as JSON with is_error true and the message in result.
    _claude_reply(monkeypatch, {"is_error": True, "result": "API Error: 529 overloaded",
                                "session_id": "s", "total_cost_usd": 0})
    r = fork.run(tmp_path, "probe", cwd=tmp_path / "cwd")
    assert r["result"] is None
    assert r["error"] == "API Error: 529 overloaded"
    assert r["is_error"] is True


def test_claude_json_with_no_result_is_an_error_row(monkeypatch, tmp_path):
    _claude_reply(monkeypatch, {"is_error": False, "subtype": "error_max_turns"})
    r = fork.run(tmp_path, "probe", cwd=tmp_path / "cwd")
    assert r["result"] is None
    assert "error_max_turns" in r["error"]


def test_claude_success_keeps_its_fields(monkeypatch, tmp_path):
    _claude_reply(monkeypatch, {"is_error": False, "result": "Yes", "session_id": "s",
                                "total_cost_usd": 0.01, "usage": {"input_tokens": 1}})
    r = fork.run(tmp_path, "probe", cwd=tmp_path / "cwd")
    assert r == {"result": "Yes", "session_id": "s", "cost": 0.01, "is_error": False,
                 "usage": {"input_tokens": 1}}
    assert r.get("error") is None


@pytest.mark.parametrize("cwd,slug", [
    ("/tmp/claude-1000/sp-cwd", "-tmp-claude-1000-sp-cwd"),
    ("/home/user/.cache/burn_1/wt.x", "-home-user--cache-burn-1-wt-x"),
])
def test_session_file_lands_where_claude_code_looks(tmp_path, cwd, slug):
    # Claude Code names a project directory by replacing every non-alphanumeric character
    # of the cwd with "-"; a file written anywhere else makes --resume fail.
    sid = fork.write_session(tmp_path, [{"role": "user", "content": "hi"}], cwd=Path(cwd))
    assert (tmp_path / "projects" / slug / f"{sid}.jsonl").exists()
