#!/bin/bash
# Pilot 19 follow-up: Haiku's non-author rival control (rival_norep2) rerun in full on the
# clean harness so the Haiku exclusivity chain (placebo, non-author, candidate author) is
# reported from one harness alongside the full clean rival family from p19b.sh.
cd /home/grafe/code/claude-self-portrait || exit 1
export SP_OUT_PREFIX=leak SP_CELLS_FILE=out/own_cells.json SP_MODELS=haiku,opus
SP_RUN_JUDGES=haiku SP_QUESTIONS=rival_norep2 SP_N=8 .venv/bin/python selfportrait/ownership.py own
echo DONE_HAIKU_NOREP2
