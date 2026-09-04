#!/bin/bash
cd "$(git rev-parse --show-toplevel)" || exit 1
H="SP_PROMPTS=fruit,city,colour,dog,noun,instrument,language,number SP_MODELS=haiku,opus SP_RUN_JUDGES=haiku SP_N=8"
env $H SP_QUESTIONS=named SP_LAYOUT=assist4 .venv/bin/python selfportrait/ownership.py own
env $H SP_QUESTIONS=named_filler SP_LAYOUT=user2 .venv/bin/python selfportrait/ownership.py own
env $H SP_QUESTIONS=named SP_LAYOUT=tool .venv/bin/python selfportrait/ownership.py own
env $H SP_QUESTIONS=named_conf,rival_named .venv/bin/python selfportrait/ownership.py own
env $H SP_QUESTIONS=named_conf,rival_named SP_LAYOUT=user2 .venv/bin/python selfportrait/ownership.py own
echo HAIKU_DONE
O="SP_PROMPTS=fruit,city,colour,dog,noun,instrument,language,number SP_MODELS=haiku,opus SP_RUN_JUDGES=opus"
env $O SP_N=8 SP_QUESTIONS=named SP_LAYOUT=user2 .venv/bin/python selfportrait/ownership.py own
env $O SP_N=8 SP_QUESTIONS=named .venv/bin/python selfportrait/ownership.py own
env $O SP_N=4 SP_QUESTIONS=named SP_LAYOUT=assist4 .venv/bin/python selfportrait/ownership.py own
env $O SP_N=4 SP_QUESTIONS=named_conf .venv/bin/python selfportrait/ownership.py own
env $O SP_N=4 SP_QUESTIONS=named_conf SP_LAYOUT=user2 .venv/bin/python selfportrait/ownership.py own
echo DONE
