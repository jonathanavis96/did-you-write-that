#!/bin/bash
# Reruns only the normalised pair stage of pilot 17b; rows resume, so each pass fills what
# the previous one lost to a single Codex timeout.
cd "$(git rev-parse --show-toplevel)" || exit 1
ALL=sky,tides,bread,sleep,rust,rainbow,salt,leaves,vaccines,thunder,fridge,ice
for pass in 1 2 3; do
  echo "== pair retry pass $pass $(date +%H:%M)"
  SP_TEXT_NORM=1 SP_PROMPTS=$ALL SP_MODELS=haiku,opus,gpt SP_N=8 .venv/bin/python selfportrait/paragraph.py pair && break
done
echo PAIR_DONE
