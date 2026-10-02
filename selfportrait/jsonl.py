"""Reader and appender for the append-only JSONL files the resumable stages write and re-read."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def load(path: Path) -> list[dict]:
    """Rows of `path`, or [] if it does not exist.

    Blank lines are skipped. Text after the last newline is a torn append from a run
    killed mid-write: it is dropped with a warning so the next run can resume (the row
    is simply redone, and append() cuts the fragment off first). A bad complete line is
    real corruption and raises.
    """
    if not path.exists():
        return []
    text = path.read_text()
    complete, _, torn = text.rpartition("\n")
    if torn.strip():
        print(f"warning: {path}: skipping torn last line ({len(torn)} chars)",
              file=sys.stderr, flush=True)
    return [json.loads(ln) for ln in complete.splitlines() if ln.strip()]


def drop_torn_tail(path: Path) -> int:
    """Truncate `path` to the end of its last newline-terminated line.

    Returns the number of bytes dropped (0, and the file untouched, when it is missing,
    empty or already ends in a newline).
    """
    try:
        fh = path.open("rb+")
    except FileNotFoundError:
        return 0
    with fh:
        size = fh.seek(0, os.SEEK_END)
        if size == 0:
            return 0
        fh.seek(size - 1)
        if fh.read(1) == b"\n":
            return 0
        # Walk back in blocks to the last newline; keep everything up to and including it.
        end, block = size, 1 << 16
        keep = 0
        while end > 0:
            start = max(0, end - block)
            fh.seek(start)
            nl = fh.read(end - start).rfind(b"\n")
            if nl != -1:
                keep = start + nl + 1
                break
            end = start
        fh.truncate(keep)
    dropped = size - keep
    print(f"warning: {path}: dropped {dropped} bytes of a torn last line before appending",
          file=sys.stderr, flush=True)
    return dropped


def append(path: Path, rec: dict) -> None:
    """Append `rec` as one line, first cutting off any torn last line a killed run left."""
    drop_torn_tail(path)
    with path.open("a") as fh:
        fh.write(json.dumps(rec) + "\n")
