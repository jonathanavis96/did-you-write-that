#!/bin/bash
# Pilot 19 follow-up, full clean replication of the pilot 11 one-word design on both Claude
# judges under the clean11 prefix. Triggered by the pre-registered refuter on the forks
# family: on the clean harness Opus answers Lisbon 23/24 for the city prompt where the
# contaminated forks gave Prague 47/48, so the cells (and the own-probabilities every
# correlation uses) must be rebuilt from clean forks. 48 forks per prompt as in pilot 11;
# cells selected by the same ladder; neutral, placebo, non-author rival, rival and the
# named label question on the assistant layout, named on the user layout; confidence,
# explicit self-prediction and within-model stages.
cd "$(git rev-parse --show-toplevel)" || exit 1
export SP_OUT_PREFIX=clean11 SP_MODELS=haiku,opus SP_PROMPTS=fruit,city,colour,dog,noun,instrument,language,number
P=.venv/bin/python
SP_N=48 $P selfportrait/ownership.py forks
echo FORKS_DONE
for J in haiku opus; do
  echo "== $J $(date +%H:%M)"
  SP_RUN_JUDGES=$J SP_QUESTIONS=neutral,placebo,rival_norep2,rival,named SP_N=8 $P selfportrait/ownership.py own
  SP_RUN_JUDGES=$J SP_QUESTIONS=named SP_N=8 SP_LAYOUT=user2 $P selfportrait/ownership.py own
done
echo OWN_DONE
SP_N=6 $P selfportrait/ownership.py conf
SP_N=6 $P selfportrait/ownership.py explicit
SP_N=8 $P selfportrait/ownership.py within
echo DONE
