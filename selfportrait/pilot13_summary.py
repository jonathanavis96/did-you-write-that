#!/usr/bin/env python3
"""Regenerate every table/statistic quoted in docs/PILOT-13-ownership-gpt.md
sections 13b-13e from the raw JSONL in out/. Plain text, stdlib + scipy only.

Usage: .venv/bin/python selfportrait/pilot13_summary.py [13b|13c|13d|13e|all]
"""
import json
import math
import os
import sys
from collections import defaultdict
from scipy.stats import wilcoxon, spearmanr

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GPT_PATH = os.path.join(ROOT, "out/gpt_judgements.jsonl")
OWN_PATH = os.path.join(ROOT, "out/own_judgements.jsonl")
CALIB_PATH = os.path.join(ROOT, "out/gpt_conf_calib.jsonl")


def load_jsonl(path):
    return [json.loads(line) for line in open(path) if line.strip()]


def cell_key(r):
    return (r["prompt"], r["answer"], r["tag"])


def filter_rows(rows, judge=None, question=None, own=False):
    """own=True also drops API-error/errored rows, printing how many were skipped."""
    out, skipped = [], 0
    for r in rows:
        if judge is not None and r.get("judge") != judge:
            continue
        if question is not None and r.get("question") != question:
            continue
        if own:
            raw = r.get("raw") or ""
            if raw.startswith("API Error") or r.get("error"):
                skipped += 1
                continue
        out.append(r)
    if own and skipped:
        print(f"  [skipped {skipped} error rows: judge={judge} question={question}]")
    return out


def cell_means(rows):
    """rows already filtered to one judge x one question -> {cell_key: [yes, n]}."""
    agg = defaultdict(lambda: [0, 0])
    for r in rows:
        k = cell_key(r)
        agg[k][1] += 1
        if r.get("yn") == "yes":
            agg[k][0] += 1
    return agg


def split_incat(agg):
    return ({k: v for k, v in agg.items() if k[2] != "off_category"},
            {k: v for k, v in agg.items() if k[2] == "off_category"})


def frac_of(agg):
    y = sum(v[0] for v in agg.values())
    n = sum(v[1] for v in agg.values())
    return y, n


def pfrac(y, n):
    return f"{y}/{n} = {y/n:.3f}" if n else "n/a"


def by_key(agg, idx):
    """idx=0 prompt, 2 tag (cell_key = (prompt, answer, tag))."""
    d = defaultdict(lambda: [0, 0])
    for k, (y, n) in agg.items():
        d[k[idx]][0] += y
        d[k[idx]][1] += n
    return d


def print_by(agg, idx, label):
    print(f"{label}:")
    for k, (y, n) in sorted(by_key(agg, idx).items()):
        print(f"  {k:16s} {y}/{n}")


def paired_wilcoxon(agg_a, agg_b, cells):
    a = [agg_a.get(c, (0, 0))[0] / agg_a.get(c, (0, 1))[1] if agg_a.get(c, (0, 0))[1] else 0.0 for c in cells]
    b = [agg_b.get(c, (0, 0))[0] / agg_b.get(c, (0, 1))[1] if agg_b.get(c, (0, 0))[1] else 0.0 for c in cells]
    diffs = [x - y for x, y in zip(a, b)]
    mean_diff = sum(diffs) / len(diffs)
    if all(d == 0 for d in diffs):
        return mean_diff, "undefined"
    _, p = wilcoxon(a, b)
    return mean_diff, p


def spearman_vs_own(agg, cells, prob_judge, rows_for_prob, log=False):
    prob_by_cell = {cell_key(r): r.get(f"p_{prob_judge}") for r in rows_for_prob}
    xs, ys = [], []
    for c in cells:
        y, n = agg.get(c, (0, 0))
        p = prob_by_cell.get(c)
        if p is None or n == 0 or (log and p == 0):
            continue
        xs.append(y / n)
        ys.append(math.log(p) if log else p)
    if len(set(xs)) < 2 or len(set(ys)) < 2:
        return None, None, len(xs)
    rho, p = spearmanr(xs, ys)
    return rho, p, len(xs)


def print_spearman(label, agg, cells, prob_judge, rows, log=False):
    rho, p, m = spearman_vs_own(agg, cells, prob_judge, rows, log=log)
    if rho is None:
        print(f"{label}: undefined (constant input) (n={m})")
    else:
        print(f"{label}: rho={rho:.2f} p={p:.2f} (n={m})")


def frame_table(rows_source, judge, frames, own=False, show_all45=False):
    """Print in-cat/off-cat P(Yes) for each (label, question) frame; return {question: agg}."""
    agg_by = {}
    for label, q in frames:
        rows = filter_rows(rows_source, judge=judge, question=q, own=own)
        agg = cell_means(rows)
        agg_by[q] = agg
        incat, off = split_incat(agg)
        line = f"{label:52s} in-cat {pfrac(*frac_of(incat))}   off-cat {pfrac(*frac_of(off))}"
        if show_all45:
            line += f"   all45 {pfrac(*frac_of(agg))}"
        print(line)
    return agg_by


def paired_series(agg_by, pairs, ncells, cells):
    for a, b, label in pairs:
        d, p = paired_wilcoxon(agg_by[a], agg_by[b], cells)
        print(f"Paired ({ncells} cells) {label}: {d:+.3f}  Wilcoxon p={p}")


def section_13b():
    print("=" * 70)
    print("Pilot 13b")
    print("=" * 70)
    gpt = load_jsonl(GPT_PATH)
    frames = [
        ("neutral", "neutral"), ("placebo", "placebo"), ("rival", "rival"),
        ("rival named, not a candidate author (first wording)", "rival_norep"),
    ]
    agg_by = frame_table(gpt, "gpt", frames)
    incat34 = {k for k in agg_by["neutral"] if k[2] != "off_category"}
    print()
    paired_series(agg_by, [
        ("neutral", "placebo", "neutral - placebo"),
        ("placebo", "rival", "placebo - rival"),
        ("neutral", "rival_norep", "neutral - rival-not-author (first wording)"),
    ], 34, incat34)

    print()
    placebo_rows = filter_rows(gpt, judge="gpt", question="placebo")
    placebo_incat, _ = split_incat(cell_means(placebo_rows))
    print_by(placebo_incat, 0, "Placebo by prompt")

    print()
    print("Placebo against own probability, selected cells:")
    prob = {cell_key(r): r.get("p_gpt") for r in placebo_rows}
    for k, (y, n) in sorted(placebo_incat.items()):
        if k[1].lower() in ("mango", "quince", "lisbon", "vienna", "cello", "piano"):
            print(f"  {k[1]:10s} (own p={prob.get(k)}) {y}/{n}")

    print()
    print("Calibration (out/gpt_conf_calib.jsonl), file order, 6 forks/item:")
    by_item = defaultdict(list)
    for r in load_jsonl(CALIB_PATH):
        by_item[r["item"]].append(r["conf"])
    inter = total = 0
    for item, vals in by_item.items():
        total += len(vals)
        inter += sum(1 for v in vals if v not in (0, 100))
        print(f"  {item:14s} {', '.join(str(int(v)) for v in vals)}")
    print(f"  intermediate (not 0/100): {inter}/{total}")


def section_13c():
    print("=" * 70)
    print("Pilot 13c")
    print("=" * 70)
    gpt = load_jsonl(GPT_PATH)
    own = load_jsonl(OWN_PATH)

    print("-- GPT --")
    agg_by = frame_table(gpt, "gpt", [
        ("neutral", "neutral"), ("placebo", "placebo"),
        ("rival named, not an author, referent fixed", "rival_norep2"),
        ("rival (turns replaced)", "rival"),
        ("rival named, not an author, first wording", "rival_norep"),
    ])
    incat34 = {k for k in agg_by["neutral"] if k[2] != "off_category"}
    paired_series(agg_by, [
        ("neutral", "rival_norep2", "neutral - fixed-wording"),
        ("placebo", "rival_norep2", "placebo - fixed-wording"),
        ("rival_norep2", "rival", "fixed-wording - rival"),
    ], 34, incat34)

    fixed_rows = filter_rows(gpt, judge="gpt", question="rival_norep2")
    fixed_incat, _ = split_incat(cell_means(fixed_rows))
    print_by(fixed_incat, 2, "By tag (rival_norep2)")
    print_by(fixed_incat, 0, "By prompt (rival_norep2)")
    print_spearman("Spearman rival_norep2 vs raw own prob", fixed_incat, incat34, "gpt", fixed_rows)
    placebo_rows = filter_rows(gpt, judge="gpt", question="placebo")
    print_spearman("Spearman placebo vs raw own prob",
                    split_incat(cell_means(placebo_rows))[0], incat34, "gpt", placebo_rows)

    print()
    print("-- Haiku 4.5 (pilot 11 cells) --")
    hframes = [("neutral", "neutral"), ("placebo", "placebo"),
               ("rival_norep2", "rival_norep2"), ("rival", "rival")]
    hagg = frame_table(own, "haiku", hframes, own=True, show_all45=True)
    incat37 = {k for k in hagg["neutral"] if k[2] != "off_category"}
    paired_series(hagg, [
        ("neutral", "placebo", "neutral - placebo"),
        ("neutral", "rival_norep2", "neutral - rival_norep2"),
        ("rival_norep2", "rival", "rival_norep2 - rival"),
        ("neutral", "rival", "neutral - rival"),
    ], 37, incat37)
    h_rn2_rows = filter_rows(own, judge="haiku", question="rival_norep2", own=True)
    h_rn2_incat, _ = split_incat(cell_means(h_rn2_rows))
    print_by(h_rn2_incat, 2, "By tag (haiku rival_norep2)")
    print_spearman("Spearman rival_norep2 vs raw own prob", h_rn2_incat, incat37, "haiku", h_rn2_rows)
    print("Off-category words, selected:")
    for q in ("placebo", "rival_norep2", "rival"):
        _, off = split_incat(hagg[q])
        for k, (y, n) in sorted(off.items()):
            if k[1].lower() in ("wrench", "stapler"):
                print(f"  {q:14s} {k[1]:10s} {y}/{n}")

    print()
    print("-- Opus 5 (pilot 11 cells) --")
    oagg = frame_table(own, "opus", hframes, own=True)
    o37 = {k for k in oagg["neutral"] if k[2] != "off_category"}
    print_by(split_incat(oagg["rival_norep2"])[0], 2, "rival_norep2 by tag")
    print_by(split_incat(oagg["rival"])[0], 2, "rival by tag")
    paired_series(oagg, [
        ("neutral", "placebo", "neutral - placebo"),
        ("placebo", "rival_norep2", "placebo - rival_norep2"),
        ("rival_norep2", "rival", "rival_norep2 - rival"),
        ("neutral", "rival", "neutral - rival"),
    ], 37, o37)
    o_rn2 = filter_rows(own, judge="opus", question="rival_norep2", own=True)
    o_rn2_incat, _ = split_incat(cell_means(o_rn2))
    o_rv = filter_rows(own, judge="opus", question="rival", own=True)
    o_rv_incat, _ = split_incat(cell_means(o_rv))
    print_spearman("Spearman rival_norep2 vs raw own prob", o_rn2_incat, o37, "opus", o_rn2)
    print_spearman("Spearman rival vs raw own prob", o_rv_incat, o37, "opus", o_rv)
    print_spearman("Spearman rival_norep2 vs log own prob", o_rn2_incat, o37, "opus", o_rn2, log=True)
    print_spearman("Spearman rival vs log own prob", o_rv_incat, o37, "opus", o_rv, log=True)
    print("Cells not at 8/8 under rival_norep2 (opus):")
    for k, (y, n) in sorted(o_rn2_incat.items()):
        if n and y < n:
            print(f"  {k[0]:10s} {k[1]:10s} {k[2]:16s} {y}/{n}")


def section_13d():
    print("=" * 70)
    print("Pilot 13d")
    print("=" * 70)
    gpt = load_jsonl(GPT_PATH)

    print("-- GPT arm (question neutral_userturn) --")
    rows = filter_rows(gpt, judge="gpt", question="neutral_userturn")
    incat, off = split_incat(cell_means(rows))
    print(f"in-category {pfrac(*frac_of(incat))}   off-category {pfrac(*frac_of(off))}")
    for k, (y, n) in sorted(off.items()):
        if k[1].lower() in ("wrench", "english", "wednesday"):
            print(f"  {k[1]:10s} {y}/{n}")
    print_by(incat, 2, "By tag")
    for k, (y, n) in sorted(incat.items()):
        if k[1].lower() in ("mango", "lantern", "lisbon"):
            print(f"  own-top {k[1]:10s} {y}/{n}")
    print_by(incat, 0, "By prompt")
    print("Dog prompt, per answer:")
    for k, (y, n) in sorted(incat.items()):
        if k[0] == "dog":
            print(f"  {k[1]:12s} {y}/{n}")
    y, n = frac_of({k: v for k, v in incat.items() if k[0] != "dog"})
    print(f"Outside dog prompt: {pfrac(y,n)}")

    print()
    print("-- Corrections after independent number-check (13b-13d) --")
    placebo_incat, _ = split_incat(cell_means(filter_rows(gpt, judge="gpt", question="placebo")))
    n_y, n_n = by_key(placebo_incat, 0)["number"]
    print(f"Placebo by prompt 'number': {n_y}/{n_n}")
    incat34 = set(placebo_incat)
    rival_incat, _ = split_incat(cell_means(filter_rows(gpt, judge="gpt", question="rival")))
    _, p = paired_wilcoxon(placebo_incat, rival_incat, incat34)
    print(f"placebo - rival Wilcoxon p = {p}")
    fixed_rows = filter_rows(gpt, judge="gpt", question="rival_norep2")
    fixed_incat, _ = split_incat(cell_means(fixed_rows))
    _, p = paired_wilcoxon(placebo_incat, fixed_incat, incat34)
    print(f"placebo - fixed-wording Wilcoxon p = {p}")
    print_spearman("rival_norep2 vs log own prob", fixed_incat, incat34, "gpt", fixed_rows, log=True)


def section_13e():
    print("=" * 70)
    print("Pilot 13e")
    print("=" * 70)
    own = load_jsonl(OWN_PATH)

    print("-- Haiku 4.5, question 'named' --")
    for label, q in [("word as assistant turn", "named"), ("word as user turn (four-turn layout)", "named_userturn2")]:
        rows = filter_rows(own, judge="haiku", question=q, own=True)
        incat, off = split_incat(cell_means(rows))
        print(f"{label:42s} in-cat {pfrac(*frac_of(incat))}   off-cat {pfrac(*frac_of(off))}")
        print_spearman("  Spearman vs own prob", incat, set(incat), "haiku", rows)

    print()
    print("=" * 70)
    print("13e: Opus 5 and Fable 5.1")
    print("=" * 70)
    for judge in ("opus", "fable"):
        print(f"-- {judge} --")
        for label, q in [("assistant layout", "named"), ("user layout", "named_userturn2")]:
            rows = filter_rows(own, judge=judge, question=q, own=True)
            incat, off = split_incat(cell_means(rows))
            print(f"  {label:20s} in-cat {pfrac(*frac_of(incat))}   off-cat {pfrac(*frac_of(off))}")

        u_rows = filter_rows(own, judge=judge, question="named_userturn2", own=True)
        u_incat, _ = split_incat(cell_means(u_rows))
        print_by(u_incat, 2, f"  {judge} user layout by tag".replace("  ", "  "))
        print_by(u_incat, 0, f"  {judge} user layout by prompt")
        print(f"  {judge} user layout, Yes cells:")
        for k, (y, n) in sorted(u_incat.items()):
            if y > 0:
                print(f"    {k[0]:10s} {k[1]:10s} {k[2]:16s} {y}/{n}")
        prob_judge = judge if judge == "haiku" else ("opus" if judge == "opus" else "opus")
        print_spearman(f"  Spearman user layout vs raw own prob ({prob_judge})",
                        u_incat, set(u_incat), prob_judge, u_rows)


SECTIONS = {"13b": section_13b, "13c": section_13c, "13d": section_13d, "13e": section_13e}


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which == "all":
        for f in (section_13b, section_13c, section_13d, section_13e):
            f()
            print()
    elif which in SECTIONS:
        SECTIONS[which]()
    else:
        print(f"unknown section {which!r}; choose from 13b 13c 13d 13e all", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
