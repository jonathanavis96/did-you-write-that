#!/bin/bash
cd "$(git rev-parse --show-toplevel)" || exit 1
P=.venv/bin/python
purge() { $P - <<'PY'
import json
p='out/para_judgements.jsonl'; keep=[]; n=0
try:
    for l in open(p):
        r=json.loads(l)
        bad=str(r.get('raw',''))[:9]=='API Error' or r.get('error') or (r.get('yn')=='unparsed' and r.get('conf') is None)
        if bad: n+=1
        else: keep.append(l)
    open(p,'w').writelines(keep)
except FileNotFoundError: pass
print('purged',n,flush=True)
PY
}
SP_MODELS=haiku,gpt SP_N=24 $P selfportrait/paragraph.py forks
SP_MODELS=opus SP_N=24 $P selfportrait/paragraph.py forks
echo FORKS_DONE
SP_MODELS=haiku,opus,gpt $P selfportrait/paragraph.py cells
for pass in 1 2; do
  purge
  SP_MODELS=haiku,opus,gpt SP_RUN_JUDGES=haiku,gpt SP_N=8 SP_QUESTIONS=neutral,placebo,rival,conf,named_para $P selfportrait/paragraph.py own
  SP_MODELS=haiku,opus,gpt SP_RUN_JUDGES=haiku SP_N=8 SP_QUESTIONS=named_para SP_LAYOUT=user2 $P selfportrait/paragraph.py own
  SP_MODELS=haiku,opus,gpt SP_RUN_JUDGES=opus SP_N=4 SP_QUESTIONS=neutral,placebo,rival,conf,named_para $P selfportrait/paragraph.py own
  SP_MODELS=haiku,opus,gpt SP_RUN_JUDGES=opus SP_N=4 SP_QUESTIONS=named_para SP_LAYOUT=user2 $P selfportrait/paragraph.py own
done
echo OWN_DONE
SP_MODELS=haiku,opus,gpt SP_RUN_JUDGES=haiku,gpt SP_N=8 $P selfportrait/paragraph.py pair
SP_MODELS=haiku,opus,gpt SP_RUN_JUDGES=opus SP_N=4 $P selfportrait/paragraph.py pair
echo DONE
