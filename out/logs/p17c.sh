#!/bin/bash
# Pilot 17c: clean-harness rerun of 17/17b. Rows under out/p17c/.
cd "$(git rev-parse --show-toplevel)" || exit 1
P=.venv/bin/python
export SP_OUT_DIR=out/p17c
ALL=sky,tides,bread,sleep,rust,rainbow,salt,leaves,vaccines,thunder,fridge,ice
SP_PROMPTS=$ALL SP_MODELS=haiku,gpt SP_N=24 $P selfportrait/paragraph.py forks
SP_PROMPTS=$ALL SP_MODELS=opus SP_N=24 $P selfportrait/paragraph.py forks
echo FORKS_DONE
SP_PROMPTS=$ALL SP_MODELS=haiku,opus,gpt $P selfportrait/paragraph.py cells
for pass in 1 2; do
  SP_PROMPTS=$ALL SP_MODELS=haiku,opus,gpt SP_RUN_JUDGES=haiku,opus,gpt SP_N=8 SP_QUESTIONS=neutral,rival $P selfportrait/paragraph.py own
done
echo OWN_DONE
for pass in 1 2 3; do
  SP_PROMPTS=$ALL SP_MODELS=haiku,opus,gpt SP_N=8 $P selfportrait/paragraph.py pair && break
done
echo DONE
