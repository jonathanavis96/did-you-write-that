#!/bin/bash
cd "$(git rev-parse --show-toplevel)" || exit 1
P=.venv/bin/python
NEW=salt,leaves,vaccines,thunder,fridge,ice
ALL=sky,tides,bread,sleep,rust,rainbow,salt,leaves,vaccines,thunder,fridge,ice
SP_PROMPTS=$NEW SP_MODELS=haiku,gpt SP_N=24 $P selfportrait/paragraph.py forks
SP_PROMPTS=$NEW SP_MODELS=opus SP_N=24 $P selfportrait/paragraph.py forks
echo FORKS_DONE
SP_PROMPTS=$ALL SP_MODELS=haiku,opus,gpt $P selfportrait/paragraph.py cells
for pass in 1 2; do
  SP_PROMPTS=$NEW SP_MODELS=haiku,opus,gpt SP_RUN_JUDGES=haiku,gpt SP_N=8 SP_QUESTIONS=neutral,placebo,rival $P selfportrait/paragraph.py own
  SP_PROMPTS=$ALL SP_MODELS=haiku,opus,gpt SP_RUN_JUDGES=opus SP_N=8 SP_QUESTIONS=neutral,placebo,rival $P selfportrait/paragraph.py own
  SP_TEXT_NORM=1 SP_PROMPTS=$ALL SP_MODELS=haiku,opus,gpt SP_RUN_JUDGES=opus SP_N=8 SP_QUESTIONS=rival $P selfportrait/paragraph.py own
done
echo OWN_DONE
SP_PROMPTS=$NEW SP_MODELS=haiku,opus,gpt SP_N=8 $P selfportrait/paragraph.py pair
SP_TEXT_NORM=1 SP_PROMPTS=$ALL SP_MODELS=haiku,opus,gpt SP_N=8 $P selfportrait/paragraph.py pair
echo DONE
