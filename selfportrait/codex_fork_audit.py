"""Index every Codex rollout file for the fork-replay audit
(docs/AUDIT-codex-fork-replay-2026-09-04.md).

For each rollout under ~/.codex/sessions/2026/09/03 and 2026/09/04 records the session
id, the parent it was forked from, ``forked_from_ordinal_exclusive`` (how many parent
items the fork inherited), the ordinals present in the file, the user and assistant
message texts, and any error carried by the task_complete event. Planted parents written
by codex_fork.write_session copy the template verbatim, so their line-0 timestamp is the
template's while their mtime is the plant time.

Writes out/logs/codex_fork_index.json (one object per rollout file; 28 MB, gitignored,
rebuilt by running this script). The audit
document's tables were derived from that index.
"""
from __future__ import annotations

import glob
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "out" / "logs" / "codex_fork_index.json"
PATTERN = "~/.codex/sessions/2026/09/0[34]/rollout-*.jsonl"


def index_file(path: str) -> dict | None:
    try:
        lines = open(path).read().splitlines()
    except OSError:
        return None
    recs = []
    for line in lines:
        if not line.strip():
            continue
        try:
            recs.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    if not recs:
        return None
    meta = recs[0].get("payload", {}) if recs[0].get("type") == "session_meta" else {}
    users: list[str] = []
    asst: list[str] = []
    err = None
    task_complete = False
    for rec in recs:
        kind = rec.get("type")
        payload = rec.get("payload", {})
        if kind == "response_item" and payload.get("type") == "message":
            content = payload.get("content") or []
            text = content[0].get("text", "") if content else ""
            if payload.get("role") == "user":
                users.append(text)
            elif payload.get("role") == "assistant":
                asst.append(text)
        elif kind == "event_msg" and payload.get("type") == "task_complete":
            task_complete = True
            err = payload.get("error")
    return {
        "path": path,
        "sid": meta.get("session_id"),
        "parent": meta.get("forked_from_id"),
        "ord_excl": meta.get("forked_from_ordinal_exclusive"),
        "ts0": recs[0].get("timestamp"),
        "mtime": os.path.getmtime(path),
        "n_lines": len(recs),
        "ords": [rec.get("ordinal") for rec in recs],
        "has_event": any(rec.get("type") == "event_msg" for rec in recs),
        "users": users,
        "asst": asst,
        "err": err,
        "task_complete": task_complete,
    }


def main() -> None:
    files = sorted(glob.glob(os.path.expanduser(PATTERN)))
    rows = [r for r in (index_file(p) for p in files) if r is not None]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(rows))
    forks = [r for r in rows if r["parent"]]
    by_sid = {r["sid"]: r for r in rows if r["sid"]}
    short = [
        r for r in forks
        if r["parent"] in by_sid and r["ord_excl"] != by_sid[r["parent"]]["n_lines"]
    ]
    print(f"{len(rows)} rollout files, {len(forks)} forks, "
          f"{len(short)} forks whose inherited ordinal count differs from the parent length")


if __name__ == "__main__":
    main()
