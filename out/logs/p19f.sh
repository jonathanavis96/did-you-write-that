#!/bin/bash
# clean13 refill: the Codex usage limit hit during the user-layout stage (all 304 rows),
# confidence, explicit and within (every row an error, "try again at 5:25 AM"). Purge the
# error rows and rerun the affected stages once the limit lifts; every stage resumes by
# row count so only the missing rows are requested.
cd /home/grafe/code/claude-self-portrait || exit 1
P=.venv/bin/python
export SP_OUT_PREFIX=clean13 SP_MODELS=gpt SP_CLAUDE_CELLS=out/clean11_cells.json SP_PROMPTS=fruit,city,colour,dog,noun,instrument,language,number
$P - <<'PY'
import json
for name, ok in (("judgements", lambda r: not r.get("error") and r.get("yn") in ("yes", "no")),
                 ("conf", lambda r: not r.get("error") and r.get("conf") is not None),
                 ("explicit", lambda r: not r.get("error") and r.get("chosen") not in (None, "unparsed")),
                 ("within", lambda r: not r.get("error") and (r.get("yn") in ("yes", "no") or r.get("conf") is not None))):
    p = f"out/clean13_{name}.jsonl"
    rows = [json.loads(l) for l in open(p)]
    keep = [r for r in rows if ok(r)]
    open(p, "w").writelines(json.dumps(r) + "\n" for r in keep)
    print(name, "kept", len(keep), "purged", len(rows) - len(keep), flush=True)
PY
while [ "$(date +%H%M)" -lt 0527 ]; do sleep 60; done
echo "REFILL start $(date)"
SP_QUESTIONS=neutral,placebo,rival_norep2,rival,named SP_N=8 $P selfportrait/ownership.py own
SP_QUESTIONS=named SP_N=8 SP_LAYOUT=user $P selfportrait/ownership.py own
echo OWN_DONE
SP_N=6 $P selfportrait/ownership.py conf
SP_N=6 $P selfportrait/ownership.py explicit
SP_N=8 $P selfportrait/ownership.py within
echo DONE
