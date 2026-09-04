#!/bin/bash
cd "$(git rev-parse --show-toplevel)" || exit 1
P=.venv/bin/python
PR=fruit,city,colour,dog,noun,instrument,language,number
H="SP_PROMPTS=$PR SP_MODELS=haiku,opus SP_RUN_JUDGES=haiku SP_N=8"
O="SP_PROMPTS=$PR SP_MODELS=haiku,opus SP_RUN_JUDGES=opus SP_N=8"
env $H SP_QUESTIONS=named SP_LAYOUT=assist4b $P selfportrait/ownership.py own
env $H SP_QUESTIONS=named_userfiller SP_LAYOUT=assist4 $P selfportrait/ownership.py own
env $H SP_QUESTIONS=rival_quality $P selfportrait/ownership.py own
echo HAIKU_DONE
env $O SP_QUESTIONS=named_reason_conf,named_conf SP_LAYOUT=user2 $P selfportrait/ownership.py own
for j in opus haiku; do
  SP_CELLS_FILE=out/cells/p16b_rangeecho.json SP_MODELS=haiku,opus SP_RUN_JUDGES=$j SP_QUESTIONS=named SP_N=8 SP_LAYOUT=user2 $P selfportrait/ownership.py own
done
echo DONE
