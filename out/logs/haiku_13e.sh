#!/bin/bash
cd "$(git rev-parse --show-toplevel)" || exit 1
SP_MODELS=haiku,opus SP_RUN_JUDGES=haiku SP_QUESTIONS=named SP_N=8 SP_LAYOUT=user2 .venv/bin/python selfportrait/ownership.py own
SP_MODELS=haiku,opus SP_RUN_JUDGES=haiku SP_QUESTIONS=named SP_N=8 .venv/bin/python selfportrait/ownership.py own
echo DONE
