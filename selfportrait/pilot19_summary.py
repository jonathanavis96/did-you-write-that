"""Score pilot 19 (leak check on every reported family) against its pre-registration
(docs/PILOT-19-leak-check.md).

For every family the paper reports, pools the clean-harness rerun (out/leak_* and
out/leakgpt_*, produced by out/logs/p19.sh) against the original contaminated rows
(out/own_* and out/gpt_*) on the SAME sampled cells, and applies the pre-registered
match/refute rule. Handles a missing or partially written clean file by treating the
family as PENDING rather than crashing -- this lets the script run (and print the
original-side rates for a sanity check) before the p19 run finishes.
"""
import json
from pathlib import Path

MATCH_RATE = 0.125
REFUTE_RATE = 0.20
MATCH_GRADED = 10.0
REFUTE_GRADED = 15.0
MATCH_EXPLICIT = 0.20

CLAUDE_CELLS = json.loads(Path("out/leak_cells.json").read_text())
GPT_CELLS = json.loads(Path("out/leakgpt_cells.json").read_text())
CLAUDE_TAGGED = [(c["prompt"], c["answer"], c["tag"]) for c in CLAUDE_CELLS]
GPT_TAGGED = [(c["prompt"], c["answer"], c["tag"]) for c in GPT_CELLS]
CLAUDE_BARE = [(c["prompt"], c["answer"]) for c in CLAUDE_CELLS]
GPT_BARE = [(c["prompt"], c["answer"]) for c in GPT_CELLS]

_CACHE: dict[tuple[str, str], list[dict]] = {}


def load_jsonl(path: str) -> list[dict]:
    """Read a jsonl file. Missing file -> []. A truncated/in-progress last line is
    dropped rather than raising, so a partially written run doesn't crash the script."""
    p = Path(path)
    if not p.exists():
        return []
    rows = []
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            break
    return rows


def rows_for(prefix: str, stagefile: str) -> list[dict]:
    key = (prefix, stagefile)
    if key not in _CACHE:
        _CACHE[key] = load_jsonl(f"out/{prefix}_{stagefile}")
    return _CACHE[key]


def agg_binary(rows, judge, extra_ok, key_fn, value_field, true_values, ok_values, keys):
    """Group rows into per-cell (k, n) counts, restricted to `keys`.

    extra_ok(r) -> bool: family-specific filter beyond judge match (question/readout).
    key_fn(r) -> cell key.
    value_field/true_values/ok_values: e.g. ("yn", {"yes"}, {"yes", "no"}) or
    ("chosen", {"top"}, {"top", "other"})."""
    g = {k: [0, 0] for k in keys}
    keyset = set(keys)
    for r in rows:
        if r.get("judge") != judge or not extra_ok(r):
            continue
        if r.get(value_field) not in ok_values:
            continue
        k = key_fn(r)
        if k not in keyset:
            continue
        g[k][1] += 1
        if r.get(value_field) in true_values:
            g[k][0] += 1
    return g


def agg_conf(rows, judge, extra_ok, key_fn, keys):
    """Group rows into per-cell lists of the graded `conf` value, restricted to `keys`."""
    g: dict[tuple, list[float]] = {k: [] for k in keys}
    keyset = set(keys)
    for r in rows:
        if r.get("judge") != judge or not extra_ok(r):
            continue
        c = r.get("conf")
        if c is None:
            continue
        k = key_fn(r)
        if k not in keyset:
            continue
        g[k].append(c)
    return g


def agg_forks(rows, model, keys):
    """Per-cell (k, n): k = forks landing on that cell's exact answer, n = all forks
    for that cell's prompt (shared denominator across cells of the same prompt)."""
    keyset = set(keys)
    prompts_needed = {p for p, _ in keyset}
    totals: dict[str, int] = {}
    counts = {k: 0 for k in keys}
    for r in rows:
        if r.get("model") != model or r.get("error"):
            continue
        p = r.get("prompt")
        if p not in prompts_needed:
            continue
        totals[p] = totals.get(p, 0) + 1
        k = (p, r.get("answer"))
        if k in keyset:
            counts[k] += 1
    return {k: [counts[k], totals.get(k[0], 0)] for k in keys}


def pool_kn(cellmap):
    k = sum(v[0] for v in cellmap.values())
    n = sum(v[1] for v in cellmap.values())
    return k, n


def pool_kn_forks(cellmap):
    """Like pool_kn, but the n for cells sharing a prompt must only be counted once."""
    k = sum(v[0] for v in cellmap.values())
    per_prompt = {key[0]: v[1] for key, v in cellmap.items()}
    n = sum(per_prompt.values())
    return k, n


def pool_mean(cellmap):
    allv = [x for vals in cellmap.values() for x in vals]
    return (sum(allv) / len(allv) if allv else None), len(allv)


def rate_verdict(delta, n_clean):
    if n_clean == 0 or delta is None:
        return "PENDING"
    d = abs(delta)
    if d <= MATCH_RATE:
        return "MATCH"
    if d > REFUTE_RATE:
        return "REFUTED"
    return "BETWEEN"


def graded_verdict(delta, n_clean):
    if n_clean == 0 or delta is None:
        return "PENDING"
    d = abs(delta)
    if d <= MATCH_GRADED:
        return "MATCH"
    if d > REFUTE_GRADED:
        return "REFUTED"
    return "BETWEEN"


def explicit_verdict(delta, n_clean):
    if n_clean == 0 or delta is None:
        return "PENDING"
    return "MATCH" if abs(delta) <= MATCH_EXPLICIT else "REFUTED"


def cellstr(key):
    if len(key) == 3:
        return f"{key[0]}:{key[1]}[{key[2]}]"
    return f"{key[0]}:{key[1]}"


def print_kn_cells(clean_map, orig_map, keys):
    for key in keys:
        ck, cn = clean_map.get(key, [0, 0])
        ok, on = orig_map.get(key, [0, 0])
        print(f"      {cellstr(key):40s} clean {ck}/{cn}   orig {ok}/{on}")


def print_conf_cells(clean_map, orig_map, keys):
    for key in keys:
        cv = clean_map.get(key, [])
        ov = orig_map.get(key, [])
        cm = f"{sum(cv) / len(cv):.1f}(n={len(cv)})" if cv else "n/a(n=0)"
        om = f"{sum(ov) / len(ov):.1f}(n={len(ov)})" if ov else "n/a(n=0)"
        print(f"      {cellstr(key):40s} clean {cm:14s} orig {om}")


def report_rate(label, layout, metric, clean_map, orig_map, keys, verdict_fn, pool_fn=pool_kn):
    ck, cn = pool_fn(clean_map)
    ok, on = pool_fn(orig_map)
    crate = ck / cn if cn else None
    orate = ok / on if on else None
    delta = crate - orate if (crate is not None and orate is not None) else None
    v = verdict_fn(delta, cn)
    dstr = f"{delta:+.3f}" if delta is not None else "n/a"
    crs = f"{crate:.3f}" if crate is not None else "n/a"
    ors = f"{orate:.3f}" if orate is not None else "n/a"
    print(f"{label:50s} layout={layout:9s} {metric}: clean {ck}/{cn}={crs}  "
          f"orig {ok}/{on}={ors}  delta={dstr}  -> {v}")
    print_kn_cells(clean_map, orig_map, keys)
    return v


def report_mean(label, layout, metric, clean_map, orig_map, keys, verdict_fn):
    cmean, cn = pool_mean(clean_map)
    omean, on = pool_mean(orig_map)
    delta = cmean - omean if (cmean is not None and omean is not None) else None
    v = verdict_fn(delta, cn)
    dstr = f"{delta:+.2f}" if delta is not None else "n/a"
    cms = f"{cmean:.2f}" if cmean is not None else "n/a"
    oms = f"{omean:.2f}" if omean is not None else "n/a"
    print(f"{label:50s} layout={layout:9s} {metric}: clean n={cn} mean={cms}  "
          f"orig n={on} mean={oms}  delta={dstr}  -> {v}")
    print_conf_cells(clean_map, orig_map, keys)
    return v


# ---- family list, matching out/logs/p19.sh exactly -------------------------------
FAMILIES = []
for _judge in ("haiku", "opus"):
    for _q in ("neutral", "placebo", "rival_norep2", "rival", "named"):
        FAMILIES.append({"judge": _judge, "question": _q, "suffix": "", "layout": "assistant",
                          "kind": "own_yn", "cells": "claude"})
    FAMILIES.append({"judge": _judge, "question": "named_conf", "suffix": "", "layout": "assistant",
                      "kind": "own_conf", "cells": "claude"})
    for _q in ("named", "named_filler"):
        FAMILIES.append({"judge": _judge, "question": _q, "suffix": "_userturn2", "layout": "user2",
                          "kind": "own_yn", "cells": "claude"})
    FAMILIES.append({"judge": _judge, "question": "named", "suffix": "_tool", "layout": "tool",
                      "kind": "own_yn", "cells": "claude"})
    for _q in ("named", "named_userfiller"):
        FAMILIES.append({"judge": _judge, "question": _q, "suffix": "_assist4", "layout": "assist4",
                          "kind": "own_yn", "cells": "claude"})
    FAMILIES.append({"judge": _judge, "question": "named", "suffix": "_assist4b", "layout": "assist4b",
                      "kind": "own_yn", "cells": "claude"})
    for _kind in ("conf_stage", "explicit", "forks", "within_yn", "within_conf"):
        FAMILIES.append({"judge": _judge, "question": None, "suffix": "", "layout": "assistant",
                          "kind": _kind, "cells": "claude"})

for _judge, _layout, _suffix in (("fable", "assistant", ""), ("fable", "user2", "_userturn2")):
    FAMILIES.append({"judge": _judge, "question": "named", "suffix": _suffix, "layout": _layout,
                      "kind": "own_yn", "cells": "claude"})

for _q in ("neutral", "placebo", "rival_norep", "rival_norep2", "rival"):
    FAMILIES.append({"judge": "gpt", "question": _q, "suffix": "", "layout": "assistant",
                      "kind": "own_yn", "cells": "gpt"})
FAMILIES.append({"judge": "gpt", "question": "neutral", "suffix": "_userturn", "layout": "user",
                  "kind": "own_yn", "cells": "gpt"})
for _kind in ("conf_stage", "explicit", "forks", "within_yn", "within_conf"):
    FAMILIES.append({"judge": "gpt", "question": None, "suffix": "", "layout": "assistant",
                      "kind": _kind, "cells": "gpt"})


def own_key(r):
    return (r.get("prompt"), r.get("answer"), r.get("tag"))


def explicit_key(r):
    return (r.get("prompt"), r.get("b"), r.get("b_tag"))


def within_key(r):
    return (r.get("prompt"), r.get("answer"))


def run(fam):
    judge = fam["judge"]
    claude_side = fam["cells"] == "claude"
    clean_prefix = "leak" if claude_side else "leakgpt"
    orig_prefix = "own" if claude_side else "gpt"
    tagged_keys = CLAUDE_TAGGED if claude_side else GPT_TAGGED
    bare_keys = CLAUDE_BARE if claude_side else GPT_BARE
    kind = fam["kind"]
    layout = fam["layout"]

    if kind == "own_yn":
        qname = fam["question"] + fam["suffix"]
        clean_rows = rows_for(clean_prefix, "judgements.jsonl")
        orig_rows = rows_for(orig_prefix, "judgements.jsonl")

        def extra_ok(r, qname=qname):
            return r.get("question") == qname

        clean_map = agg_binary(clean_rows, judge, extra_ok, own_key, "yn", {"yes"}, {"yes", "no"}, tagged_keys)
        orig_map = agg_binary(orig_rows, judge, extra_ok, own_key, "yn", {"yes"}, {"yes", "no"}, tagged_keys)
        return report_rate(f"{judge} / {qname}", layout, "Yes-rate", clean_map, orig_map, tagged_keys, rate_verdict)

    if kind == "own_conf":
        qname = fam["question"] + fam["suffix"]
        clean_rows = rows_for(clean_prefix, "judgements.jsonl")
        orig_rows = rows_for(orig_prefix, "judgements.jsonl")

        def extra_ok(r, qname=qname):
            return r.get("question") == qname

        clean_map = agg_conf(clean_rows, judge, extra_ok, own_key, tagged_keys)
        orig_map = agg_conf(orig_rows, judge, extra_ok, own_key, tagged_keys)
        return report_mean(f"{judge} / {qname} (graded)", layout, "mean conf", clean_map, orig_map,
                            tagged_keys, graded_verdict)

    if kind == "conf_stage":
        clean_rows = rows_for(clean_prefix, "conf.jsonl")
        orig_rows = rows_for(orig_prefix, "conf.jsonl")
        clean_map = agg_conf(clean_rows, judge, lambda r: True, own_key, tagged_keys)
        orig_map = agg_conf(orig_rows, judge, lambda r: True, own_key, tagged_keys)
        return report_mean(f"{judge} / conf-stage", layout, "mean conf", clean_map, orig_map,
                            tagged_keys, graded_verdict)

    if kind == "explicit":
        clean_rows = rows_for(clean_prefix, "explicit.jsonl")
        orig_rows = rows_for(orig_prefix, "explicit.jsonl")
        clean_map = agg_binary(clean_rows, judge, lambda r: True, explicit_key, "chosen",
                                {"top"}, {"top", "other"}, tagged_keys)
        orig_map = agg_binary(orig_rows, judge, lambda r: True, explicit_key, "chosen",
                               {"top"}, {"top", "other"}, tagged_keys)
        return report_rate(f"{judge} / explicit", layout, "own-pick rate", clean_map, orig_map,
                            tagged_keys, explicit_verdict)

    if kind == "forks":
        clean_rows = rows_for(clean_prefix, "forks.jsonl")
        orig_rows = rows_for(orig_prefix, "forks.jsonl")
        clean_map = agg_forks(clean_rows, judge, bare_keys)
        orig_map = agg_forks(orig_rows, judge, bare_keys)
        return report_rate(f"{judge} / forks", layout, "own-answer rate", clean_map, orig_map,
                            bare_keys, rate_verdict, pool_fn=pool_kn_forks)

    if kind == "within_yn":
        clean_rows = rows_for(clean_prefix, "within.jsonl")
        orig_rows = rows_for(orig_prefix, "within.jsonl")

        def extra_ok(r):
            return r.get("readout") == "rival"

        clean_map = agg_binary(clean_rows, judge, extra_ok, within_key, "yn", {"yes"}, {"yes", "no"}, bare_keys)
        orig_map = agg_binary(orig_rows, judge, extra_ok, within_key, "yn", {"yes"}, {"yes", "no"}, bare_keys)
        return report_rate(f"{judge} / within (rival)", layout, "own-choice Yes-rate", clean_map, orig_map,
                            bare_keys, rate_verdict)

    if kind == "within_conf":
        clean_rows = rows_for(clean_prefix, "within.jsonl")
        orig_rows = rows_for(orig_prefix, "within.jsonl")

        def extra_ok(r):
            return r.get("readout") == "conf"

        clean_map = agg_conf(clean_rows, judge, extra_ok, within_key, bare_keys)
        orig_map = agg_conf(orig_rows, judge, extra_ok, within_key, bare_keys)
        return report_mean(f"{judge} / within (conf)", layout, "mean conf", clean_map, orig_map,
                            bare_keys, graded_verdict)

    raise ValueError(f"unknown family kind {kind!r}")


tally: dict[str, int] = {}
non_match: list[str] = []
for _fam in FAMILIES:
    _label = f"{_fam['judge']}/{_fam['question'] or _fam['kind']}{_fam['suffix']}"
    _v = run(_fam)
    tally[_v] = tally.get(_v, 0) + 1
    if _v != "MATCH":
        non_match.append(f"{_label} [{_fam['layout']}] -> {_v}")

print("\n=== summary ===")
for _k in ("MATCH", "BETWEEN", "REFUTED", "PENDING"):
    print(f"{_k}: {tally.get(_k, 0)}")
print(f"\nnon-MATCH families ({len(non_match)}):")
for _line in non_match:
    print(f"  {_line}")
