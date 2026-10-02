"""Failure handling of the two fork backends' run(): no real CLI is ever called."""
import subprocess
import sys
from pathlib import Path

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
