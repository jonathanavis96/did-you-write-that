---
title: "Prefill tools: genuine assistant-turn prefill on two production CLIs, no API key"
status: written 2026-09-03, standalone tool description; depends on selfportrait/fork.py and selfportrait/codex_fork.py
---

# The trick

`claude -p` and `codex exec` both refuse assistant-turn input on the command line: you can
send a prompt, not a fake reply the model should treat as its own. But both CLIs resume a
past session from a file on disk and replay that file's turns verbatim before adding the new
prompt. If the file on disk already contains an assistant turn we chose, resuming it puts our
text in the assistant role of the model's real context, on the real deployed model, with no
fine-tuning and no API-level prefill parameter. That is what `selfportrait/fork.py` (Claude
Code) and `selfportrait/codex_fork.py` (Codex) do. Both expose the same two functions,
`write_session(cfg, messages, ...)` and `run(cfg, prompt, model, resume=sid, ...)`, so pilot
code written against one works against the other by swapping the import.

# Claude Code

**What gets written, and where.** `fork.py`'s `write_session` writes one JSONL file per
session at `<CLAUDE_CONFIG_DIR>/projects/<slug-of-cwd>/<sid>.jsonl`, where `<slug-of-cwd>` is
the working directory path with `/` replaced by `-` (the same layout Claude Code itself uses
for real sessions under `~/.claude/projects/`). Each line is one record: `user` records carry
`{"role": "user", "content": text}` under `message`, `promptSource: "sdk"`; `assistant` records
carry a full API-shaped message block (`model`, `id`, `content: [{"type": "text", "text": ...}]`,
`stop_reason: "end_turn"`, token usage) under `message`. Records chain by `parentUuid`, so the
file is a linear conversation, and `sid` is either supplied or a fresh `uuid4`.

The harness runs under an isolated `CLAUDE_CONFIG_DIR` (`make_cfg`): a fresh directory,
`.credentials.json` copied in from `~/.claude/` at mode 600, and a `settings.json` that denies
every built-in tool. This is not incidental to the trick — it means the model that answers the
probe has no tools, so a probe run against attacker-controlled planted text (as several pilots
in this repo do) cannot act on an injected instruction even if it wanted to.

**The resume command.**

```bash
claude -p "<probe>" --model <m> --output-format json \
  --resume <sid> --fork-session \
  --disallowed-tools Bash Read Write Edit WebFetch WebSearch Glob Grep Task Agent
```

`--fork-session` matters: without it, a second `--resume` on the same `sid` would append to
that session file rather than starting a fresh branch from it, so a second probe would see the
first probe's exchange too. With it, each `run()` call forks a clean copy from the written
state, so one written transcript can be probed many times independently (the
snapshot-then-probe pattern this repo's `EXPERIMENT-fork-isolated-measurements.md` calls
fork-isolated measurement, run here on the real system rather than a research harness).
`--effort low|medium|high` is accepted here too and is recorded on the output row when a pilot
passes it; it has no Codex equivalent.

**Why this is genuine prefill.** The model's context for the probe call is exactly: the system
prompt, the written user/assistant turns from the session file, in order, then the new probe as
a final user turn. The assistant text sits in the assistant role because the API message it was
built into literally has `"role": "assistant"`; there is no marker distinguishing "text a human
wrote for the model" from "text the model actually sampled". That is the whole basis for
treating the model's answer to "did you write the previous reply?" as evidence about what the
model uses to judge authorship, rather than a report grounded in some privileged internal
signal — see `docs/METHOD-ownership-measurement.md`.

**Caveat: consecutive user records.** Claude Code's own session-loading logic does not expect
two `user` records back to back with no assistant turn between them; empirically it either
merges them into one turn or pads the gap with a synthetic assistant turn reading "No response
requested." (documented from observation in `docs/PILOT-13-ownership-gpt.md`, not from Claude
Code's source). A written session must therefore alternate roles and end on an assistant record
for the layout to survive replay as written. The role-label control in
`docs/METHOD-ownership-measurement.md` (planting a word as a user turn instead of an assistant
turn) needs four turns on the Claude Code path for exactly this reason: user prompt, assistant
"You go first.", user WORD, assistant "Noted." — never two bare user turns.

# Codex

**What gets written, and where.** `codex_fork.py`'s `write_session` does not build a rollout
from scratch; it copies a real one-turn template session
(`~/.codex/sessions/YYYY/MM/DD/rollout-<timestamp>-<uuid>.jsonl`, the default pinned by
`DEFAULT_TEMPLATE_SID`, overridable via `SP_CODEX_TEMPLATE`) and rewrites it in place: every
occurrence of the old session id is replaced with a fresh `uuid4`, the first non-preamble user
`response_item`'s text is replaced with the real prompt (skipping the CLI's own
`<recommended_plugins>` preamble turn, which is left untouched), and the assistant
`response_item`'s `output_text` is replaced with the text we want the model to believe it wrote.
Any `turn_context` record's `model` field is also rewritten to the target model. The result is
written to a new file at `~/.codex/sessions/<year>/<month>/<day>/rollout-<timestamp>-<new
sid>.jsonl`. For the role-label control, `write_session` instead takes two `user` messages and
turns the template's assistant record itself into a second user record (`role: "user"`,
`content: [{"type": "input_text", ...}]`) rather than needing any assistant turn at all — Codex
does not show Claude Code's consecutive-user-record problem, so a bare second user turn is
sufficient.

**The resume command.**

```bash
codex exec --skip-git-repo-check -s read-only --json -m gpt-5.6-sol fork <uuid> "<probe>"
```

`-s read-only` matches Claude Code's tool-denial: the model cannot act on anything in the
planted or probed text. `fork <uuid>` is the equivalent of `--resume --fork-session`: it starts
a new turn from the named session's recorded state without mutating that session file, so the
same written rollout can be forked repeatedly. Output is streamed JSON events; `run()` parses
`thread.started` for the session id, the `item.completed` event of type `agent_message` for the
reply text, and `turn.completed` for usage.

**Why this is genuine prefill.** Same argument as Claude Code: the rewritten rollout's assistant
`response_item` carries `role: "assistant"` in the same schema a real turn would, so from the
model's perspective at fork time there is no way to distinguish planted text from a turn it
actually sampled, other than by judging the text itself.

**Caveat: the harness system prompt is part of the stimulus.** Codex prepends its own agent
system prompt ahead of every session, roughly 14k tokens beginning "You are Codex, an agent
based on GPT-5" (quoted in `docs/PILOT-13-ownership-gpt.md`). That system prompt, not just the
planted turns, is present for every probe and must be reported as part of the stimulus when
comparing results across harnesses — it is one plausible source of any Claude-versus-GPT
difference that is not really about the planted text.

# Shared caveats

- **Always verify a new layout with a listing probe before trusting scored results from it.**
  The recommended probe text, from `docs/METHOD-ownership-measurement.md`, is: "List every
  message in this conversation so far in order, as 'role: text', verbatim." Run it once per new
  message-list shape (new turn count, new role pattern) before running the real probes on that
  shape, because both harnesses have replay quirks (Claude Code's user-turn merging above) that
  silently change what the model actually sees.
- **Histories must alternate roles and end on an assistant record.** This is required on the
  Claude Code path (see above) and is good practice on Codex too, since an ownership question
  ("did you write the previous reply?") is only well posed when the previous record is in fact
  an assistant turn.
- **Effort is Claude-only.** `SP_EFFORT` / `--effort low|medium|high` has no Codex analogue;
  pilots that vary it record `effort: None` on GPT rows.
- **Observed cost per call, 2026-09-03 session:** Haiku judges, a few cents per call; Opus
  judges, about $0.10 per call; Claude Fable 5.1 at low effort, about $0.08 per call; Codex
  (GPT-5.6-Sol), no dollar cost on a ChatGPT subscription. These are order-of-magnitude
  figures from running the pilots in this repo, not a priced rate card — see
  `docs/METHOD-ownership-measurement.md`'s "Costs on 2026-09-03" line for the aggregate numbers
  behind them.

# Minimal example

Claude Code:

```python
from pathlib import Path
from selfportrait.fork import make_cfg, write_session, run

cfg = make_cfg(Path("/tmp/prefill-demo"))
sid = write_session(cfg, [
    {"role": "user", "content": "Name a fruit. Reply with exactly one word."},
    {"role": "assistant", "content": "Mango"},
], model="claude-opus-5")

r = run(cfg, "Did you write the previous reply? Yes or No.",
        model="claude-opus-5", resume=sid)
print(r["result"])
```

Codex:

```python
from pathlib import Path
from selfportrait import codex_fork

sid = codex_fork.write_session(None, [
    {"role": "user", "content": "Name a fruit. Reply with exactly one word."},
    {"role": "assistant", "content": "Mango"},
], model="gpt-5.6-sol")

r = codex_fork.run(None, "Did you write the previous reply? Yes or No.",
                    model="gpt-5.6-sol", resume=sid)
print(r["result"])
```

Both functions take the same shape of `messages` list and return a dict with `result`,
`session_id`, `cost` (Claude only; Codex reports `None`), `is_error`, and `usage` — that
uniform interface is what lets `selfportrait/ownership.py` pick the backend with one `if judge
== "gpt"` branch (`backend()`, near the top of the file) and run the identical pilot logic
against either model.

See `docs/METHOD-ownership-measurement.md` for how this primitive is used to measure ownership
against a model's own sampling distribution, and `docs/PLAN-bulletproof.md` ("Useful to
others") for why this is called out as a reusable tool independent of the pilots built on it.
