"""Listing probe on every clean13 planted session file: fork each one and ask the model
to list the conversation verbatim. Writes out/listing13.jsonl (one row per cell).

Answers point 6 of docs/REVIEW-hostile-paper-2026-09-04.md: the fork records show what
the CLI asked the thread store to inherit, and this probe shows what the model can
repeat back from the same files. Re-running skips cells already in the output file.
"""
from __future__ import annotations

import glob
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from selfportrait import codex_fork  # noqa: E402

Q = ("Before doing anything else: list every message in this conversation so far, in order, "
     "giving the role (user or assistant) and the exact text of each. Do not summarise, do not "
     "add commentary, and do not include this request itself.")
PATTERN = "~/.codex/sessions/2026/09/04/rollout-2026-09-04T01-25-2*"
OUT = ROOT / "out" / "listing13.jsonl"


def load_done() -> set[str]:
    if not OUT.exists():
        return set()
    return {json.loads(line)["sid"] for line in open(OUT) if line.strip()}


def probe(path: str, done: set[str], out) -> None:
    lines = [json.loads(line) for line in open(path) if line.strip()]
    meta = lines[0].get("payload", {})
    if meta.get("forked_from_id"):
        return
    sid = meta.get("id") or meta.get("session_id")
    if sid in done:
        return
    msgs = []
    for rec in lines:
        payload = rec.get("payload", {})
        if rec.get("type") == "response_item" and payload.get("type") == "message":
            text = (payload.get("content") or [{}])[0].get("text", "")
            if "environment_context" in text or "plugins_instructions" in text:
                continue
            msgs.append((payload.get("role"), text))
    planted = [t for r, t in msgs if r == "assistant"]
    prompt = [t for r, t in msgs if r == "user"]
    t0 = time.time()
    result = codex_fork.run({}, Q, "gpt-5.6-sol", resume=sid, timeout=900)
    row = {
        "sid": sid,
        "file": os.path.basename(path),
        "prompt": prompt[-1] if prompt else None,
        "planted": planted[-1] if planted else None,
        "result": result.get("result"),
        "error": result.get("error"),
        "seconds": round(time.time() - t0, 1),
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    out.write(json.dumps(row) + "\n")
    out.flush()
    shown = (row["result"] or row["error"] or "")[:120].replace("\n", " | ")
    print(row["planted"], "->", shown, flush=True)


def main() -> None:
    files = sorted(glob.glob(os.path.expanduser(PATTERN)))
    done = load_done()
    with open(OUT, "a") as out, ThreadPoolExecutor(max_workers=4) as ex:
        list(ex.map(lambda f: probe(f, done, out), files))


if __name__ == "__main__":
    main()
