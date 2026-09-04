#!/bin/bash
# Pilot 19 follow-up: the Haiku rival family crossed the refuter line on the 8 sampled cells
# (clean 23/64 vs original 36/64), so per the pre-registration it is rerun in full on the
# clean harness: all 45 own_cells.json cells, 8 forks each, under the leak prefix (the 8
# sampled cells are already there and are skipped by the resume logic).
cd "$(git rev-parse --show-toplevel)" || exit 1
export SP_OUT_PREFIX=leak SP_CELLS_FILE=out/own_cells.json SP_MODELS=haiku,opus
SP_RUN_JUDGES=haiku SP_QUESTIONS=rival SP_N=8 .venv/bin/python selfportrait/ownership.py own
echo DONE_HAIKU_RIVAL
