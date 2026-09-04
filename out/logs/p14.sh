#!/bin/bash
cd "$(git rev-parse --show-toplevel)" || exit 1
Q=neutral,placebo,rival_norep2,named
for M in "Qwen/Qwen2.5-1.5B-Instruct" "Qwen/Qwen2.5-3B-Instruct" "Qwen/Qwen3-4B-Instruct-2507"; do
  for L in assistant user2; do
    echo "== $M $L $(date +%H:%M)"
    SP_LOCAL_MODEL=$M SP_LOCAL_DTYPE=bf16 SP_THREADS=8 SP_QUESTIONS=$Q SP_LAYOUT=$L SP_N=64 nice -n 10 .venv/bin/python selfportrait/ownership_local.py || echo "FAILED $M $L"
  done
done
echo DONE
# rerun of the two stages that crashed on number_norange before the EXTRA skip was added
for ML in "Qwen/Qwen2.5-1.5B-Instruct user2" "Qwen/Qwen2.5-3B-Instruct assistant"; do
  set -- $ML; echo "== rerun $1 $2 $(date +%H:%M)"
  SP_LOCAL_MODEL=$1 SP_LOCAL_DTYPE=bf16 SP_THREADS=8 SP_QUESTIONS=$Q SP_LAYOUT=$2 SP_N=64 nice -n 10 .venv/bin/python selfportrait/ownership_local.py || echo "FAILED rerun $1 $2"
done
echo RERUN_DONE
