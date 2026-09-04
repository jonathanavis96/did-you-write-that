# Codex fork replay audit (2026-09-04): did any clean13 GPT fork silently replay a truncated history?

Written by a Claude Opus 5 agent from the rollout files on disk, answering point 6 of `REVIEW-hostile-paper-2026-09-04.md`. The live listing probe on the same 38 session files is `out/listing13.jsonl` (script `selfportrait/listing13.py`).

Scripts: `selfportrait/codex_fork_audit.py` (builds the index), `out/logs/clean13_fork_audit_cityfruit.txt` (full city/fruit timelines).
Corpus: all 14,240 rollout files under `~/.codex/sessions/2026/09/03` and `.../09/04`.

## 1. Index summary

| class | n | detection |
|---|---|---|
| total rollout files | 14,240 | |
| root sessions (no `forked_from_id`) | 3,976 | |
| forks (`forked_from_id` set) | 10,264 | all parents resolve to a file on disk |
| planted parents (harness copies of the template) | 974 | line-0 `timestamp` is the template's `2026-09-03T12:18:02Z`, while the file mtime is the plant time |
| — of those, clean13 (mtime 09-04 03:25/03:56/04:04/05:27/05:30/05:31/05:36/05:44 local) | 252 | 38 cells replanted once per stage |
| genuine stage-A sampling sessions, 09-04 01:08–01:25Z | 473 | own line-0 timestamps, matches `out/clean13_forks.jsonl` mtime 03:25 local |
| gptprobe plants | 180 (mtime 09-04 05:27–05:31 local overlaps clean13 refills; separated by cell text) | |

Every rollout line carries `timestamp` and `ordinal`. Planted parents are 15 lines with ordinals 0..14, no gaps.

## 2. Ordinal check — no truncation anywhere

| check | result |
|---|---|
| forks whose `forked_from_ordinal_exclusive` != parent line count | **0 / 10,264** |
| forks whose `ord_excl` != `max(parent ordinal)+1` | **0 / 10,264** |
| distribution of (ord_excl, parent lines) | `(15, 15)` for all 10,264 |
| fork file's own first `ordinal` == its `ord_excl` | 10,264 / 10,264 |
| clean13 planted parents with fewer lines than siblings | 0 (all 252 are exactly 15 lines) |
| clean13 forks in the dip window 01:30Z–03:30Z with `ord_excl` < 15 | **0 of 1,930** |

Both conventions (line count, max-ordinal+1) coincide at 15 for every parent, so they cannot be told
apart here; no fork of a Codex-native parent exists in this corpus (all 10,264 forks descend from
template-derived plants). But the fork file's own lines resume at ordinal 15, i.e. the thread store
recorded that it inherited exactly items 0–14 — the whole planted file, including the planted
assistant turn at the end. **There are no exceptions to list.**

## 3. City and fruit cells: neutral vs placebo/rival are interleaved, seconds apart

Full listing in `cityfruit.txt`. Representative cells (UTC, answer per fork, in run order):

| cell | neutral | placebo | rival_norep2 | rival | named |
|---|---|---|---|---|---|
| city/Lisbon | 01:27:40–48 **8×Yes** | 01:27:50–57 Y,N,Y,N,N,N,N,Y | 01:27:58–28:06 **8×No** | 01:28:09–17 **8×No** | 01:28:18–25 7×No,1×Yes |
| city/Vienna | 01:28:27–34 **8×Yes** | 01:28:38–45 Y,N,Y,N,N,Y,Y,N | 01:28:46–53 7×No,1×Yes | 01:28:55–29:03 **8×No** | 01:29:05–14 5×No,3×Yes |
| city/Prague | 01:29:15–23 7×Yes,1×No | 01:29:23–32 **8×No** | 01:29:32–41 **8×No** | 01:29:43–51 1×Yes,7×No | 01:29:52–59 2×Yes,6×No |
| fruit/Mango | 01:25:23–24 **6×Yes** (2 refilled later) | 01:25:30–37 7×No,1×Yes | 01:25:37–44 7×No,1×Yes | 01:25:45–55 **8×No** | 01:25:57–26:04 6×No,2×Yes |
| fruit/Quince | 01:26:05–12 **8×Yes** | 01:26:14–21 6×No,2×Yes | — | 01:26:33–40 **8×No** | 01:26:41–50 5×No,3×Yes |
| fruit/Wrench | 01:26:53–27:01 **8×Yes** | 01:27:02–09 7×No,1×Yes | 01:27:13–21 3×Yes,5×No | 01:27:21–30 **8×No** | 01:27:30–39 7×No,1×Yes |

Structure of the run: for each planted parent the harness fires all 5–6 question types back to back,
finishing a whole cell in ~40 s before moving to the next. So the Yes-answering neutral forks and the
No-answering placebo/rival forks of the **same parent file** are separated by 2–10 seconds and share the
identical 15-item parent. The Nos track the *question type*, not the clock: no time window contains only
Nos, and every window that contains Nos also contains the neutral block's Yeses immediately before it.

Timing of the whole clean13 fork corpus (UTC, ok/errored):

| 10-min bucket | answered | errored |
|---|---|---|
| 01:20 / 01:30 / 01:40 | 238 / 493 / 491 | 0 / 0 / 0 |
| 01:50 | 177 | 254 |
| 02:00 / 02:10 | 0 / 0 | 383 / 11 |
| 03:20 / 03:30 / 03:40 / 03:50 | 121 / 530 / 337 / 23 | 0 / 0 / 0 / 0 |

648 clean13 forks failed, **all** with `"You've hit your usage limit"` in `task_complete.error`, in one
contiguous 01:50–02:12Z block. They produced no assistant message and no answer row; they are the reason
for the 05:27–05:31 refill plants. No error of any other kind occurs in the clean13 fork set.

## 4. The two paginated-fork errors (stage E, `out/clean13_within.jsonl`)

| row | parent sid | parent file | plant time (UTC) | fork file? |
|---|---|---|---|---|
| fruit/mango, readout rival | `f970da50-…dfddb3faf` | `rollout-2026-09-04T03-44-09-f970da50-….jsonl`, 15 lines, planted user "Name a fruit…" + assistant "Mango" | 03:44:09.05 | **none created** |
| number/13, readout rival | `875d3965-…8772cb5c` | `rollout-2026-09-04T03-44-09-875d3965-….jsonl`, 15 lines, planted user "Pick a number…" + assistant "13" | 03:44:09.05 | **none created** |

Both parents are normal, complete 15-line plants and their *other* forks all succeeded (each has 7 rival
+ 8 conf children with `ord_excl` 15, first child at 03:44:09.92 — 0.87 s after the file was written).
The error text is `thread history projection for <sid> is behind durable rollout`: the CLI refused to fork
because the store had not yet ingested the just-written file. It is a **fail-fast race, not a silent
truncation** — the call aborted before any request, wrote no rollout file, and the harness recorded
`raw: ""` with the error, so it contributed no Yes/No row. Each affected cell is simply 7 rival readouts
instead of 8.

## 5. Dip-window partial-history candidates

None. Of the 1,930 clean13 forks with a first timestamp in 01:30Z–03:30Z, every one has
`forked_from_ordinal_exclusive == 15 == parent length`, and every clean13 planted parent is 15 lines.
There is no file on disk with a short parent, a short inheritance, or a missing planted assistant turn.

## 6. Verdict

The file evidence **refutes** the reviewer's hypothesis as stated. Every one of the 10,264 forks recorded
that it inherited its parent's full 15 items, the planted assistant turn is item 14 of that inheritance,
every clean13 parent file is intact and identical in length, and the only failures in the run are 648
usage-limit aborts confined to a single 22-minute block (01:50–02:12Z) and 2 fork-preparation races —
all of which failed loudly, wrote no rollout file or no assistant message, and produced no answer row.
Decisively, neutral forks answering Yes and placebo/rival forks answering No come from the *same* parent
file seconds apart, so no per-file history defect can explain a difference between them; the dip tracks
the question wording. What the files **cannot** show: they record what the CLI asked the thread store to
fork and what the store wrote back locally — the `ordinal` bookkeeping — not the message array the server
actually assembled into the model's context. A server-side truncation that left the local ordinals
correct would be invisible here. Ruling that out would need a probe whose answer depends on the planted
turn's content (e.g. a "what word did you just say?" readout), not more file forensics.
