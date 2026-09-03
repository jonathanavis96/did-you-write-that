"""Genuine assistant-turn prefill on Claude via the Claude Code CLI.

`claude -p` cannot take assistant turns, but it resumes sessions from a JSONL
transcript on disk and sends that transcript to the API verbatim. So writing a
transcript with the assistant turns we choose, then `--resume SID --fork-session`,
is a real prefill: the model's context contains our text in the assistant role.
Each probe forks the session, so one written state can be probed many times
(the snapshot-then-probe protocol of ContextEcho, on the real system).

Uses an isolated CLAUDE_CONFIG_DIR (credentials copied, all tools denied).
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTOOLS = ["--disallowed-tools", "Bash", "Read", "Write", "Edit", "WebFetch",
           "WebSearch", "Glob", "Grep", "Task", "Agent"]


def make_cfg(dir_: Path) -> Path:
    dir_.mkdir(parents=True, exist_ok=True)
    os.chmod(dir_, 0o700)
    src = Path.home() / ".claude" / ".credentials.json"
    dst = dir_ / ".credentials.json"
    if src.exists() and not dst.exists():
        shutil.copy(src, dst)
        os.chmod(dst, 0o600)
    (dir_ / "settings.json").write_text(json.dumps({"permissions": {"deny": [
        "Bash", "Read", "Write", "Edit", "WebFetch", "WebSearch", "Glob", "Grep"]}}))
    return dir_


def _slug(cwd: Path) -> str:
    return str(cwd).replace("/", "-")


def write_session(cfg: Path, messages: list[dict], cwd: Path = ROOT,
                  sid: str | None = None, model: str = "claude-opus-5") -> str:
    """messages: [{"role": "user"|"assistant", "content": str}, ...]. Returns sid."""
    sid = sid or str(uuid.uuid4())
    pdir = cfg / "projects" / _slug(cwd)
    pdir.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    parent = None
    lines = []
    for m in messages:
        u = str(uuid.uuid4())
        rec = {"parentUuid": parent, "isSidechain": False, "type": m["role"],
               "uuid": u, "timestamp": now, "cwd": str(cwd), "sessionId": sid,
               "version": "2.1.259", "gitBranch": "main", "userType": "external"}
        if m["role"] == "user":
            rec["message"] = {"role": "user", "content": m["content"]}
            rec["promptSource"] = "sdk"
            rec["entrypoint"] = "sdk-cli"
        else:
            rec["message"] = {"model": model, "id": "msg_" + u.replace("-", "")[:24],
                              "type": "message", "role": "assistant",
                              "content": [{"type": "text", "text": m["content"]}],
                              "stop_reason": "end_turn", "stop_sequence": None,
                              "usage": {"input_tokens": 1, "output_tokens": 1}}
            rec["requestId"] = "req_" + u.replace("-", "")[:24]
        lines.append(json.dumps(rec))
        parent = u
    (pdir / f"{sid}.jsonl").write_text("\n".join(lines) + "\n")
    return sid


def run(cfg: Path, prompt: str, model: str = "opus", resume: str | None = None,
        cwd: Path = ROOT, timeout: int = 300, extra: list[str] | None = None) -> dict:
    cmd = ["claude", "-p", prompt, "--model", model, "--output-format", "json", *NOTOOLS]
    if resume:
        cmd += ["--resume", resume, "--fork-session"]
    if extra:
        cmd += extra
    env = dict(os.environ, CLAUDE_CONFIG_DIR=str(cfg))
    p = subprocess.run(cmd, cwd=str(cwd), env=env, capture_output=True, text=True, timeout=timeout)
    try:
        d = json.loads(p.stdout)
    except json.JSONDecodeError:
        return {"result": None, "error": (p.stdout + p.stderr)[-500:], "rc": p.returncode}
    return {"result": d.get("result"), "session_id": d.get("session_id"),
            "cost": d.get("total_cost_usd"), "is_error": d.get("is_error"),
            "usage": d.get("usage")}
