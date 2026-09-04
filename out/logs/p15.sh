#!/bin/bash
cd "$(git rev-parse --show-toplevel)" || exit 1
SP_PROMPTS=vegetable,planet,bird,metal,boyname,girlname,month,dogbreed,digits,numword SP_MODELS=haiku,opus SP_N=24 .venv/bin/python selfportrait/ownership.py forks
SP_PROMPTS=vegetable,planet,bird,metal,boyname,girlname,month,dogbreed,digits,numword SP_MODELS=gpt SP_N=24 .venv/bin/python selfportrait/ownership.py forks
echo FORKS_DONE
SP_PROMPTS=vegetable,planet,bird,metal,boyname,girlname,month,dogbreed,digits,numword SP_MODELS=haiku,opus SP_RUN_JUDGES=haiku SP_QUESTIONS=named SP_N=8 .venv/bin/python selfportrait/ownership.py own
SP_PROMPTS=vegetable,planet,bird,metal,boyname,girlname,month,dogbreed,digits,numword SP_MODELS=haiku,opus SP_RUN_JUDGES=haiku SP_QUESTIONS=named SP_N=8 SP_LAYOUT=user2 .venv/bin/python selfportrait/ownership.py own
SP_PROMPTS=vegetable,planet,bird,metal,boyname,girlname,month,dogbreed,digits,numword SP_MODELS=haiku,opus SP_RUN_JUDGES=opus SP_QUESTIONS=named SP_N=4 .venv/bin/python selfportrait/ownership.py own
SP_PROMPTS=vegetable,planet,bird,metal,boyname,girlname,month,dogbreed,digits,numword SP_MODELS=haiku,opus SP_RUN_JUDGES=opus SP_QUESTIONS=named SP_N=4 SP_LAYOUT=user2 .venv/bin/python selfportrait/ownership.py own
SP_PROMPTS=vegetable,planet,bird,metal,boyname,girlname,month,dogbreed,digits,numword SP_MODELS=gpt SP_QUESTIONS=neutral SP_N=8 .venv/bin/python selfportrait/ownership.py own
SP_PROMPTS=vegetable,planet,bird,metal,boyname,girlname,month,dogbreed,digits,numword SP_MODELS=gpt SP_QUESTIONS=neutral SP_N=8 SP_LAYOUT=user .venv/bin/python selfportrait/ownership.py own
echo DONE
