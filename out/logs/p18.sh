#!/bin/bash
# Pilot 18: paragraph design on the local scale series, RX 6800 via torch-directml.
# Two passes: the first samples every model's paragraphs (stage A) and scores the cells
# whose sources exist; the second fills the other_local cells and pairs, which need the
# other model's stage A rows. Every stage resumes by row key.
cd /home/grafe/code/claude-self-portrait || exit 1
run() { # model dtype other_local
  echo "== $1 $2 other_local=$3 $(date +%H:%M)"
  SP_LOCAL_MODEL=$1 SP_LOCAL_DTYPE=$2 SP_LOCAL_DEVICE=dml SP_N=8 SP_OTHER_LOCAL=$3 \
    .venv-dml/bin/python selfportrait/paragraph_local.py 2>&1 | grep -v "Warning\|warn(" || echo "FAILED $1"
}
for pass in 1 2; do
  echo "== pass $pass"
  run Qwen/Qwen2.5-1.5B-Instruct fp32 Qwen/Qwen2.5-3B-Instruct
  run Qwen/Qwen2.5-3B-Instruct fp32 Qwen/Qwen3-4B-Instruct-2507
  run Qwen/Qwen3-4B-Instruct-2507 fp16 Qwen/Qwen2.5-3B-Instruct
done
echo DONE
