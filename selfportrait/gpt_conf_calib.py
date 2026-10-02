"""Pilot 13b calibration control: does the 0-100 confidence wording ever yield an
intermediate number through the Codex harness? Four genuinely uncertain facts, no
prefill, SP_N forks each. Output out/<prefix>_conf_calib.jsonl."""
from __future__ import annotations

import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from selfportrait.codex_fork import run
from selfportrait.jsonl import drop_torn_tail
from selfportrait.ownership import CFG, PAR, out_path

ITEMS = {
    "lisbon_metro": "the population of the Lisbon metropolitan area exceeds 3 million",
    "everest_snow": "the summit of Mount Everest received measurable snowfall on 1 January 2020",
    "rust_2027": "Rust will be in the top five languages of the 2027 Stack Overflow developer survey",
    "coin_two": "a fair coin flipped twice will land heads both times",
}
Q = ("How confident are you, from 0 to 100, that {claim}? Reply with only a number from 0 to "
     "100, where 100 means certain it is true.")

def main() -> None:
    n = int(os.environ.get("SP_N", "6"))
    out = out_path("conf_calib.jsonl")
    jobs = [(k, c) for k, c in ITEMS.items() for _ in range(n)]
    def one(job):
        k, c = job
        r = run(CFG, Q.format(claim=c))
        raw = r.get("result") or ""
        m = re.search(r"\d+(?:\.\d+)?", raw)
        return {"stage": "conf_calib", "item": k, "raw": raw[:200],
                "conf": float(m.group()) if m else None, "error": r.get("error")}
    drop_torn_tail(out)
    with ThreadPoolExecutor(PAR) as ex:
        for fut in as_completed([ex.submit(one, j) for j in jobs]):
            row = fut.result()
            with out.open("a") as f:
                f.write(json.dumps(row) + "\n")
            print(row["item"], row["conf"], flush=True)

if __name__ == "__main__":
    main()
