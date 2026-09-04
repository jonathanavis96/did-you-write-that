#!/bin/bash
# Pilot 15b: one-word label and rival spot check on the clean harness. Rows out/clean_*.
cd "$(git rev-parse --show-toplevel)" || exit 1
P=.venv/bin/python
export SP_OUT_PREFIX=clean
PR=vegetable,planet,bird,metal
SP_PROMPTS=$PR SP_MODELS=haiku,opus SP_N=24 $P selfportrait/ownership.py forks
echo FORKS_DONE
for J in haiku opus; do
  SP_PROMPTS=$PR SP_MODELS=haiku,opus SP_RUN_JUDGES=$J SP_QUESTIONS=named,neutral,rival SP_N=8 $P selfportrait/ownership.py own
  SP_PROMPTS=$PR SP_MODELS=haiku,opus SP_RUN_JUDGES=$J SP_QUESTIONS=named SP_N=8 SP_LAYOUT=user2 $P selfportrait/ownership.py own
done
echo DONE
