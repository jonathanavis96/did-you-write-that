"""Genuine assistant-turn prefill on Codex (GPT via `codex exec`), mirroring
selfportrait/fork.py's interface for Claude.

`codex exec` cannot take assistant turns as input either, but it forks a
previous session from a rollout JSONL file on disk. We plant a fresh rollout
by copying a real one-turn template session and replacing (a) the session id
everywhere it occurs, (b) the user response_item's text (the actual prompt,
not the <recommended_plugins> preamble) and (c) the assistant response_item's
text (the answer we want the model to believe it wrote). Then
`codex exec --skip-git-repo-check -s read-only --json fork <sid> "PROBE"`
forks it; the model sees the planted text as its own prior turn.

Template: the newest file matching
~/.codex/sessions/*/*/*/rollout-*-<SP_CODEX_TEMPLATE_SID>.jsonl, overridable
via SP_CODEX_TEMPLATE (a full path to a template rollout file).
"""
from __future__ import annotations

import json
import os
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Codex loads AGENTS.md from the working directory's ancestors: run from the repo, every
# GPT fork before 2026-09-04 carried /home/grafe/code/AGENTS.md (workspace rules, no style
# instruction). Forks now run from a neutral directory with nothing above it; see fork.py.
NEUTRAL_CWD = Path(os.environ.get("SP_FORK_CWD", "/tmp/claude-1000/sp-cwd"))
SESSIONS_DIR = Path.home() / ".codex" / "sessions"
DEFAULT_TEMPLATE_SID = "01a06734-65d6-7a72-8f33-6e9d09a0c445"
DEFAULT_TEMPLATE = (SESSIONS_DIR / "2026" / "09" / "03"
                    / f"rollout-2026-09-03T14-18-02-{DEFAULT_TEMPLATE_SID}.jsonl")
TEMPLATE = Path(os.environ.get("SP_CODEX_TEMPLATE", str(DEFAULT_TEMPLATE)))
PREAMBLE_MARK = "<recommended_plugins>"


def _template_sid(path: Path) -> str:
    # rollout-<timestamp>-<uuid>.jsonl -> the uuid is the session id used
    # throughout the file's payloads.
    stem = path.stem
    parts = stem.split("-")
    return "-".join(parts[-5:])


def write_session(cfg, messages: list[dict], cwd: Path = NEUTRAL_CWD,
                   sid: str | None = None, model: str = "gpt-5.6-sol") -> str:
    """messages: exactly one user turn and one assistant turn (any order).
    Returns the new session id, planted as a rollout file under
    ~/.codex/sessions/YYYY/MM/DD/."""
    roles = [m["role"] for m in messages]
    if sorted(roles) == ["assistant", "user"]:
        user_text = next(m["content"] for m in messages if m["role"] == "user")
        asst_text = next(m["content"] for m in messages if m["role"] == "assistant")
        extra_user = None
    elif roles == ["user", "user"]:
        # role-label control: the planted word arrives as a second user turn and the
        # template's assistant record is dropped.
        user_text, extra_user = messages[0]["content"], messages[1]["content"]
        asst_text = None
    else:
        raise ValueError(f"codex_fork.write_session needs one user and one assistant "
                          f"message, or two user messages, got roles={roles!r}")

    if not TEMPLATE.exists():
        raise FileNotFoundError(f"codex template rollout not found: {TEMPLATE}")
    old_sid = _template_sid(TEMPLATE)
    lines = TEMPLATE.read_text().splitlines()

    new_sid = sid or str(uuid.uuid4())
    out_lines = []
    seen_user = False
    for line in lines:
        rec = json.loads(line)
        if old_sid in line:
            line = line.replace(old_sid, new_sid)
            rec = json.loads(line)

        if rec.get("type") == "response_item":
            payload = rec.get("payload", {})
            if payload.get("role") == "user" and payload.get("content"):
                text = payload["content"][0].get("text", "")
                if not text.startswith(PREAMBLE_MARK) and not seen_user:
                    payload["content"][0]["text"] = user_text
                    seen_user = True
                    line = json.dumps(rec)
            elif payload.get("role") == "assistant" and payload.get("content"):
                content = payload["content"][0]
                if content.get("type") == "output_text":
                    if asst_text is None:
                        # replace the assistant record with a second user record
                        payload["role"] = "user"
                        payload["content"] = [{"type": "input_text", "text": extra_user}]
                        payload.pop("phase", None)
                    else:
                        content["text"] = asst_text
                    line = json.dumps(rec)
        elif rec.get("type") == "turn_context":
            payload = rec.get("payload", {})
            if payload.get("model") != model:
                payload["model"] = model
                cm = payload.get("collaboration_mode", {}).get("settings", {})
                if "model" in cm:
                    cm["model"] = model
                line = json.dumps(rec)
        out_lines.append(line)

    if not seen_user:
        raise RuntimeError("codex_fork.write_session: template has no non-preamble user turn")

    now = datetime.now(timezone.utc)
    dest_dir = SESSIONS_DIR / now.strftime("%Y") / now.strftime("%m") / now.strftime("%d")
    dest_dir.mkdir(parents=True, exist_ok=True)
    fname = f"rollout-{now.strftime('%Y-%m-%dT%H-%M-%S')}-{new_sid}.jsonl"
    (dest_dir / fname).write_text("\n".join(out_lines) + "\n")
    return new_sid


def run(cfg, prompt: str, model: str = "gpt-5.6-sol", resume: str | None = None,
        cwd: Path = NEUTRAL_CWD, timeout: int = 300, extra: list[str] | None = None) -> dict:
    cwd.mkdir(parents=True, exist_ok=True)
    cmd = ["codex", "exec", "--skip-git-repo-check", "-s", "read-only", "--json",
           "-m", model]
    if extra:
        cmd += extra
    if resume:
        cmd += ["fork", resume, prompt]
    else:
        cmd += [prompt]
    p = subprocess.run(cmd, cwd=str(cwd), stdin=subprocess.DEVNULL,
                        capture_output=True, text=True, timeout=timeout, check=False)
    text = None
    thread_id = None
    usage = None
    for line in p.stdout.splitlines():
        line = line.strip()
        if not line or not line.startswith("{"):
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        t = ev.get("type")
        if t == "thread.started":
            thread_id = ev.get("thread_id")
        elif t == "item.completed" and ev.get("item", {}).get("type") == "agent_message":
            text = ev["item"].get("text")
        elif t == "turn.completed":
            usage = ev.get("usage")
    if text is None:
        return {"result": None, "error": (p.stdout + p.stderr)[-500:], "rc": p.returncode}
    return {"result": text, "session_id": thread_id, "cost": None,
            "is_error": False, "usage": usage}
