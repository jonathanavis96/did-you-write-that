#!/bin/bash
# Clean rerun of the pilot 16 label controls on the clean11 cells (40), Haiku only,
# 8 forks per cell. Prefix clean16, cells planted from out/clean11_cells.json so no
# resampling of forks. Harness: selfportrait/fork.py isolated HOME + neutral cwd.
cd "$(git rev-parse --show-toplevel)" || exit 1
export SP_OUT_PREFIX=clean16 SP_CELLS_FILE=out/clean11_cells.json
export SP_MODELS=haiku,opus SP_RUN_JUDGES=haiku SP_N=8
P=.venv/bin/python
echo "== F named_filler user2 $(date +%H:%M)"
SP_QUESTIONS=named_filler SP_LAYOUT=user2 $P selfportrait/ownership.py own
echo "== T named tool $(date +%H:%M)"
SP_QUESTIONS=named SP_LAYOUT=tool $P selfportrait/ownership.py own
echo FT_DONE
echo "== A4 named assist4 $(date +%H:%M)"
SP_QUESTIONS=named SP_LAYOUT=assist4 $P selfportrait/ownership.py own
echo DONE
