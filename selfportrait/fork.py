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
# Claude Code reads ~/.claude/CLAUDE.md through HOME regardless of CLAUDE_CONFIG_DIR, and
# CLAUDE.md / AGENTS.md from every parent of the working directory. Until 2026-09-04 every
# fork therefore carried Jonathan's personal CLAUDE.md (including a "caveman" reply-style
# section that Opus 5 sometimes obeyed in its paragraphs) and the workspace CLAUDE.md.
# Forks now run with HOME inside the isolated config dir and from a neutral directory
# with no instruction files above it; the probe "list every CLAUDE.md in your context"
# answers NONE under this setting and named both files without it.
NEUTRAL_CWD = Path(os.environ.get("SP_FORK_CWD", "/tmp/claude-1000/sp-cwd"))
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


def write_session(cfg: Path, messages: list[dict], cwd: Path = NEUTRAL_CWD,
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
        elif m["role"] == "tool_use":
            # assistant turn that calls a tool; m["content"] is the command string
            rec["type"] = "assistant"
            rec["message"] = {"model": model, "id": "msg_" + u.replace("-", "")[:24],
                              "type": "message", "role": "assistant",
                              "content": [{"type": "tool_use", "id": m["tool_id"], "name": "Bash",
                                           "input": {"command": m["content"],
                                                     "description": "Read the stored answer"}}],
                              "stop_reason": "tool_use", "stop_sequence": None,
                              "usage": {"input_tokens": 1, "output_tokens": 1}}
            rec["requestId"] = "req_" + u.replace("-", "")[:24]
        elif m["role"] == "tool_result":
            # tool output carrying the word; rendered by Claude Code as "tool: <word>"
            rec["type"] = "user"
            rec["message"] = {"role": "user", "content": [{"type": "tool_result",
                              "tool_use_id": m["tool_id"], "content": m["content"], "is_error": False}]}
            rec["toolUseResult"] = {"stdout": m["content"], "stderr": "", "interrupted": False, "isImage": False}
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
        cwd: Path = NEUTRAL_CWD, timeout: int = 300, extra: list[str] | None = None) -> dict:
    cmd = ["claude", "-p", prompt, "--model", model, "--output-format", "json", *NOTOOLS]
    cwd.mkdir(parents=True, exist_ok=True)
    home = cfg / "home"
    home.mkdir(exist_ok=True)
    if resume:
        cmd += ["--resume", resume, "--fork-session"]
    if extra:
        cmd += extra
    env = dict(os.environ, CLAUDE_CONFIG_DIR=str(cfg), HOME=str(home))
    try:
        p = subprocess.run(cmd, cwd=str(cwd), env=env, capture_output=True, text=True,
                           timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"result": None, "error": f"timeout after {timeout}s", "rc": None}
    try:
        d = json.loads(p.stdout)
    except json.JSONDecodeError:
        return {"result": None, "error": (p.stdout + p.stderr)[-500:], "rc": p.returncode}
    if not isinstance(d, dict):
        return {"result": None, "error": (p.stdout + p.stderr)[-500:], "rc": p.returncode}
    return {"result": d.get("result"), "session_id": d.get("session_id"),
            "cost": d.get("total_cost_usd"), "is_error": d.get("is_error"),
            "usage": d.get("usage")}
