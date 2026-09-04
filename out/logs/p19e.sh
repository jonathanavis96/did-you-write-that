#!/bin/bash
# Pilot 19 GPT follow-up. (1) leaky-harness control: the placebo and rival_norep2
# families on the 9 pilot-19 GPT cells with the fork cwd back inside the repo so
# the workspace AGENTS.md is read again; separates leak from model drift.
# (2) clean13: full clean-harness replication of the pilot 13 GPT one-word design.
cd "$(git rev-parse --show-toplevel)" || exit 1
P=.venv/bin/python
export SP_MODELS=gpt SP_PROMPTS=fruit,city,colour,dog,noun,instrument,language,number
echo "LEAKY control start $(date)"
SP_OUT_PREFIX=leakygpt SP_CELLS_FILE=out/leakgpt_cells.json SP_FORK_CWD="$PWD" \
  SP_QUESTIONS=placebo,rival_norep2 SP_N=8 $P selfportrait/ownership.py own
echo LEAKY_DONE
export SP_OUT_PREFIX=clean13 SP_CLAUDE_CELLS=out/clean11_cells.json
SP_N=48 $P selfportrait/ownership.py forks; echo FORKS_DONE
SP_QUESTIONS=neutral,placebo,rival_norep2,rival,named SP_N=8 $P selfportrait/ownership.py own
SP_QUESTIONS=named SP_N=8 SP_LAYOUT=user $P selfportrait/ownership.py own
echo OWN_DONE
SP_N=6 $P selfportrait/ownership.py conf
SP_N=6 $P selfportrait/ownership.py explicit
SP_N=8 $P selfportrait/ownership.py within
echo DONE
