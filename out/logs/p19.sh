#!/bin/bash
# Pilot 19: leak check. The paper's one-word cells (city, fruit: Paris, Prague, Ljubljana,
# Nairobi, Apple, Mango, Quince, Wrench; Lisbon for GPT) re-run on the isolated harness,
# 8 forks per cell, for every question family the paper reports. Rows out/leak_* (Claude)
# and out/leakgpt_* (GPT). Waits for pilot 17c to finish so the two do not share rate limits.
cd /home/grafe/code/claude-self-portrait || exit 1
until grep -q '^DONE' out/logs/p17c.log; do sleep 30; done
P=.venv/bin/python
PR=city,fruit
# --- Claude judges -------------------------------------------------------------
export SP_OUT_PREFIX=leak SP_CELLS_FILE=out/leak_cells.json SP_PROMPTS=$PR
export SP_MODELS=haiku,opus,fable
for J in haiku opus; do
  echo "== $J $(date +%H:%M)"
  SP_RUN_JUDGES=$J SP_QUESTIONS=neutral,placebo,rival_norep2,rival,named,named_conf SP_N=8 $P selfportrait/ownership.py own
  SP_RUN_JUDGES=$J SP_QUESTIONS=named,named_filler SP_N=8 SP_LAYOUT=user2 $P selfportrait/ownership.py own
  SP_RUN_JUDGES=$J SP_QUESTIONS=named SP_N=8 SP_LAYOUT=tool $P selfportrait/ownership.py own
  SP_RUN_JUDGES=$J SP_QUESTIONS=named,named_userfiller SP_N=8 SP_LAYOUT=assist4 $P selfportrait/ownership.py own
  SP_RUN_JUDGES=$J SP_QUESTIONS=named SP_N=8 SP_LAYOUT=assist4b $P selfportrait/ownership.py own
done
echo "== fable $(date +%H:%M)"
SP_RUN_JUDGES=fable SP_QUESTIONS=named SP_N=8 $P selfportrait/ownership.py own
SP_RUN_JUDGES=fable SP_QUESTIONS=named SP_N=8 SP_LAYOUT=user2 $P selfportrait/ownership.py own
echo "== claude conf/explicit $(date +%H:%M)"
SP_MODELS=haiku,opus SP_N=6 $P selfportrait/ownership.py conf
SP_MODELS=haiku,opus SP_N=6 $P selfportrait/ownership.py explicit
echo "== claude forks/within $(date +%H:%M)"
SP_MODELS=haiku,opus SP_N=24 $P selfportrait/ownership.py forks
SP_MODELS=haiku,opus SP_N=4 $P selfportrait/ownership.py within
echo CLAUDE_DONE
# --- GPT ------------------------------------------------------------------------
export SP_OUT_PREFIX=leakgpt SP_CELLS_FILE=out/leakgpt_cells.json SP_MODELS=gpt
echo "== gpt $(date +%H:%M)"
SP_QUESTIONS=neutral,placebo,rival_norep,rival_norep2,rival SP_N=8 $P selfportrait/ownership.py own
SP_QUESTIONS=neutral SP_N=8 SP_LAYOUT=user $P selfportrait/ownership.py own
SP_N=6 $P selfportrait/ownership.py conf
SP_N=6 $P selfportrait/ownership.py explicit
SP_N=24 $P selfportrait/ownership.py forks
SP_N=4 $P selfportrait/ownership.py within
echo DONE
