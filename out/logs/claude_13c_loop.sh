#!/bin/bash
# refill loop: run stage own for the 13c questions, purge overload rows, repeat until clean
cd "$(git rev-parse --show-toplevel)" || exit 1
for i in $(seq 1 12); do
  SP_MODELS=haiku,opus SP_RUN_JUDGES=opus SP_QUESTIONS=placebo,rival_norep2 SP_N=8 .venv/bin/python selfportrait/ownership.py own
  n=$(.venv/bin/python - <<'PY'
p='out/own_judgements.jsonl'; rows=open(p).readlines()
keep=[l for l in rows if not ('"raw": "API Error' in l or '"error": "' in l)]
open(p,'w').writelines(keep); print(len(rows)-len(keep))
PY
)
  echo "pass $i purged $n"
  [ "$n" = "0" ] && break
  sleep 60
done
echo DONE
