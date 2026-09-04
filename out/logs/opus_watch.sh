#!/bin/bash
# exits when the Opus refill loop finishes (log says DONE) or after 6 hours
cd "$(git rev-parse --show-toplevel)" || exit 1
for i in $(seq 1 720); do
  grep -q DONE out/logs/claude_13c_loop.log 2>/dev/null && { echo "opus loop DONE"; tail -n 3 out/logs/claude_13c_loop.log; exit 0; }
  sleep 30
done
echo "watch timed out after 6h"; tail -n 3 out/logs/claude_13c_loop.log
