"""Pilot 11/14, local arm: the same ownership design on a local HF causal-LM with
exact probabilities, generalised into a scale-series instrument. Gives (i) sampling
frequency p_sample from SP_N forks per prompt, (ii) teacher-forced p_tf of each
candidate answer under the model, and (iii) exact P(yes) = p(Yes)/(p(Yes)+p(No)) for
each ownership question after a genuine assistant-turn (or user-turn, see SP_LAYOUT)
prefill. Lets sampling frequency and log-likelihood be compared as predictors, which
the API arm cannot do, and lets the same design run at multiple model scales.

Token handling (unchanged from the original pilot-11 script): p_tf and P(yes) are
both computed by tokenising the candidate string ("Yes"/"No", or the displayed
answer word) with add_special_tokens=False, teacher-forcing it after the prompt's
chat-template prefix, and summing log-softmax over the candidate's own token
positions (lp()). "Yes"/"No" are typically single BPE tokens for these tokenizers
but the code does not assume that: it sums log-probabilities over however many
tokens the candidate string tokenizes to, so P(yes) is exact under the model's own
tokenization, not a first-token approximation.

Env vars (all optional, defaults preserve the original pilot-11 behaviour):
  SP_LOCAL_MODEL   HF model id. Default Qwen/Qwen2.5-1.5B-Instruct.
  SP_LOCAL_OUT     Output path override. Default out/own_local_<slug>.jsonl, where
                    <slug> is derived from SP_LOCAL_MODEL so different scales never
                    collide and the original out/own_local.jsonl (1.5B run already
                    in the repo) is never touched by this script again.
  SP_QUESTIONS     Comma list of QUESTIONS keys from ownership.py. Default: all of
                    them (neutral, named, rival, intent, placebo, rival_norep,
                    rival_norep2), matching the original script's behaviour of
                    computing every question for every cell. "named" has a {word}
                    placeholder, substituted with display(answer, prompt).
  SP_LAYOUT        "assistant" (default, two-turn: user prompt / assistant answer,
                    then the question as a new user turn) or "user2" (pilot 13e's
                    four-turn layout: user prompt / assistant "You go first." /
                    user answer / assistant "Noted.", then the question as a new
                    user turn). Recorded on every row as "layout".
  SP_PROMPTS       Comma list of PROMPTS keys. Default: all of them.
  SP_N             Forks per prompt for the sampling distribution. Default 64.
  SP_THREADS       torch.set_num_threads. Default 8.
  SP_LOCAL_DTYPE   torch dtype name for AutoModelForCausalLM.from_pretrained. Default
                    float32 (preserves the original 1.5B behaviour). Use bf16 for the
                    3B/4B runs to roughly halve resident memory on CPU.
  SP_LOCAL_DEVICE  torch device for the model and inputs. Default "cpu". "cuda" runs
                    on the GPU (on Windows, the RX 6800 through ZLUDA presents as a
                    CUDA device); "dml" uses torch-directml (WSL2, the .venv-dml venv:
                    torch 2.4.1, no bf16, fp32 matches CPU fp32 to ~1e-5 nats).
                    Recorded on every row as "device", with "dtype".

Output: one JSON row per (prompt, answer, question, layout) combination, fields
model, prompt, answer, tag, layout, question, p_yes, p_tf, p_sample, log_p_tf,
log_p_sample (natural log; null, not -inf, when the underlying probability is
exactly 0 so the file stays strict JSON — happens for p_sample when a candidate
answer was probed but never sampled, e.g. off_category or valid_unsampled). Resume: rows already present for a
(prompt, answer, question, layout) combination are skipped; the file is appended to,
not rewritten, and rows are flushed as they complete. Progress is printed every 10
cells, where a cell is one (prompt, answer) pair (i.e. after all questions for that
answer have been probed under the current layout).
"""
from __future__ import annotations

import json
import math
import os
import re
import sys
from collections import Counter
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from selfportrait.ownership import EXTRA, PROMPTS, QUESTIONS, display, norm  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "out"
M = os.environ.get("SP_LOCAL_MODEL", "Qwen/Qwen2.5-1.5B-Instruct")
NF = int(os.environ.get("SP_N", "64"))
LAYOUT = os.environ.get("SP_LAYOUT", "assistant")
QUESTION_KEYS = os.environ.get("SP_QUESTIONS", ",".join(QUESTIONS.keys())).split(",")
PROMPT_KEYS = os.environ.get("SP_PROMPTS", ",".join(PROMPTS.keys())).split(",")
torch.set_num_threads(int(os.environ.get("SP_THREADS", "8")))


def slug_of(model_id: str) -> str:
    """Filesystem-safe, org-prefix-stripped slug: Qwen/Qwen2.5-1.5B-Instruct ->
    qwen2.5-1.5b-instruct."""
    base = model_id.split("/")[-1].lower()
    return re.sub(r"[^a-z0-9._-]+", "-", base).strip("-")


OUT_PATH = Path(os.environ.get("SP_LOCAL_OUT", str(OUT / f"own_local_{slug_of(M)}.jsonl")))

DTYPE = {"float32": torch.float32, "fp32": torch.float32,
          "bf16": torch.bfloat16, "bfloat16": torch.bfloat16,
          "float16": torch.float16, "fp16": torch.float16}[os.environ.get("SP_LOCAL_DTYPE", "float32")]
DEV_NAME = os.environ.get("SP_LOCAL_DEVICE", "cpu")
if DEV_NAME == "dml":
    import torch_directml
    DEV = torch_directml.device()
else:
    DEV = DEV_NAME
DTYPE_NAME = os.environ.get("SP_LOCAL_DTYPE", "float32")
tok = AutoTokenizer.from_pretrained(M)
model = AutoModelForCausalLM.from_pretrained(M, dtype=DTYPE).eval().to(DEV)


def ids_of(msgs):
    p = tok.apply_chat_template(msgs, add_generation_prompt=True, tokenize=False)
    return tok(p, return_tensors="pt", add_special_tokens=False).input_ids


@torch.no_grad()
def lp(ids, cand):
    c = tok(cand, add_special_tokens=False, return_tensors="pt").input_ids
    x = torch.cat([ids, c], 1).to(DEV)
    lg = model(x).logits[0, ids.shape[1] - 1:-1].float().cpu()
    return float(torch.log_softmax(lg, -1).gather(1, c[0].unsqueeze(1)).sum())


@torch.no_grad()
def sample(msgs, n):
    ids = ids_of(msgs).to(DEV)
    outs = []
    for i in range(0, n, 16):
        o = model.generate(ids, do_sample=True, temperature=1.0, top_p=1.0, max_new_tokens=8,
                           num_return_sequences=min(16, n - i), pad_token_id=tok.eos_token_id)
        outs += [tok.decode(x[ids.shape[1]:], skip_special_tokens=True) for x in o]
    return outs


def question_msgs(prompt_text: str, shown: str):
    """The conversation prefix before the ownership question, per SP_LAYOUT."""
    if LAYOUT == "user2":
        return [{"role": "user", "content": prompt_text},
                {"role": "assistant", "content": "You go first."},
                {"role": "user", "content": shown},
                {"role": "assistant", "content": "Noted."}]
    return [{"role": "user", "content": prompt_text},
            {"role": "assistant", "content": shown}]


def safe_log(p: float) -> float | None:
    """None (not -inf) when p==0, so the JSONL stays strict JSON; p_sample can be
    exactly 0 for a candidate that was never sampled (off_category, valid_unsampled,
    or any low-probability candidate outrun by SP_N)."""
    return math.log(p) if p > 0 else None


def load_have(path: Path) -> set:
    if not path.exists():
        return set()
    have = set()
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        have.add((r["prompt"], r["answer"], r["question"], r["layout"]))
    return have


def main():
    have = load_have(OUT_PATH)
    fh = OUT_PATH.open("a")
    cell_count = 0
    for key in PROMPT_KEYS:
        if key not in EXTRA:
            # pilot 16b/16c prompts (number_norange, number_only_norange, number_1000)
            # have no EXTRA ladder and are not part of the local series.
            print(f"skip {key}: no EXTRA entry", flush=True)
            continue
        text = PROMPTS[key]
        raw = sample([{"role": "user", "content": text}], NF)
        dist = Counter(norm(r) for r in raw if norm(r))
        print(key, dist.most_common(6), flush=True)
        ranked = [a for a, _ in dist.most_common()]
        cands = {ranked[0]: "top"}
        if len(ranked) > 2:
            cands[ranked[len(ranked) // 2]] = "mid"
        if len(ranked) > 1:
            cands[ranked[-1]] = "low"
        valid, off = EXTRA[key]
        for v in valid:
            if norm(v) not in dist:
                cands[norm(v)] = "valid_unsampled"
                break
        cands[norm(off[0])] = "off_category"
        for extra in os.environ.get("SP_EXTRA_" + key.upper(), "").split(","):
            if extra and norm(extra) not in cands:
                cands[norm(extra)] = "api_top"
        base = ids_of([{"role": "user", "content": text}])
        for a, tag in cands.items():
            shown = display(a, key)
            p_tf = math.exp(lp(base, shown))
            p_sample = dist[a] / NF
            qmsgs = question_msgs(text, shown)
            for q in QUESTION_KEYS:
                combo = (key, a, q, LAYOUT)
                if combo in have:
                    continue
                qtext = QUESTIONS[q].replace("{word}", shown)
                ids = ids_of(qmsgs + [{"role": "user", "content": qtext}])
                ly, ln = lp(ids, "Yes"), lp(ids, "No")
                p_yes = math.exp(ly) / (math.exp(ly) + math.exp(ln))
                rec = {"model": M, "prompt": key, "answer": a, "tag": tag, "layout": LAYOUT,
                       "question": q, "p_yes": p_yes, "p_tf": p_tf, "p_sample": p_sample,
                       "log_p_tf": safe_log(p_tf), "log_p_sample": safe_log(p_sample),
                       "device": DEV_NAME, "dtype": DTYPE_NAME}
                fh.write(json.dumps(rec) + "\n")
                fh.flush()
                have.add(combo)
            print(f"  {a:14s} {tag:16s} p_s={p_sample:.3f} p_tf={p_tf:.2e}", flush=True)
            cell_count += 1
            if cell_count % 10 == 0:
                print(f"  ... {cell_count} cells done", flush=True)
    fh.close()
    print("wrote", OUT_PATH)


if __name__ == "__main__":
    main()
