#!/bin/bash
# Pilot 14 on the RX 6800 through torch-directml (.venv-dml). fp32 for the Qwen2.5
# models (exact to ~1e-5 nats vs CPU fp32), fp16 for Qwen3-4B (fp32 does not fit 16 GB).
cd "$(git rev-parse --show-toplevel)" || exit 1
Q=neutral,placebo,rival_norep2,named
for MD in "Qwen/Qwen2.5-1.5B-Instruct fp32" "Qwen/Qwen2.5-3B-Instruct fp32" "Qwen/Qwen3-4B-Instruct-2507 fp16"; do
  set -- $MD
  for L in assistant user2; do
    echo "== $1 $2 $L $(date +%H:%M)"
    SP_LOCAL_MODEL=$1 SP_LOCAL_DTYPE=$2 SP_LOCAL_DEVICE=dml SP_QUESTIONS=$Q SP_LAYOUT=$L SP_N=64 .venv-dml/bin/python selfportrait/ownership_local.py || echo "FAILED $1 $L"
  done
done
echo DONE
