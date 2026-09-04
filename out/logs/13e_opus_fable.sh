#!/bin/bash
cd "$(git rev-parse --show-toplevel)" || exit 1
for pass in 1 2 3; do
  # purge API-error rows for these judges/questions before each pass
  .venv/bin/python - <<'PY'
import json
p='out/own_judgements.jsonl'; keep=[]; n=0
for l in open(p):
    r=json.loads(l)
    bad=r.get('judge') in ('opus','fable') and r.get('question') in ('named','named_userturn2') and (str(r.get('raw',''))[:9]=='API Error' or r.get('error') or r.get('yn')=='unparsed')
    if bad: n+=1
    else: keep.append(l)
open(p,'w').writelines(keep); print('purged',n,flush=True)
PY
  SP_MODELS=haiku,opus SP_RUN_JUDGES=opus SP_QUESTIONS=named SP_N=4 SP_LAYOUT=user2 .venv/bin/python selfportrait/ownership.py own
  SP_MODELS=haiku,opus SP_RUN_JUDGES=opus SP_QUESTIONS=named SP_N=4 .venv/bin/python selfportrait/ownership.py own
  SP_MODELS=haiku,opus SP_RUN_JUDGES=fable SP_EFFORT=low SP_QUESTIONS=named SP_N=4 SP_LAYOUT=user2 .venv/bin/python selfportrait/ownership.py own
  SP_MODELS=haiku,opus SP_RUN_JUDGES=fable SP_EFFORT=low SP_QUESTIONS=named SP_N=4 .venv/bin/python selfportrait/ownership.py own
done
echo DONE
