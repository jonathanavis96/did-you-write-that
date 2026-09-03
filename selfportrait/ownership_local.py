"""Pilot 11, local arm: the same ownership design on Qwen2.5-1.5B-Instruct with
exact probabilities. Gives (i) sampling frequency p_sample from 64 forks per prompt,
(ii) teacher-forced p_tf of each candidate answer, and (iii) exact
P(yes) = p(Yes)/(p(Yes)+p(No)) for the ownership question after a genuine
assistant-turn prefill. Lets sampling frequency and log-likelihood be compared as
predictors, which the API arm cannot do.
"""
from __future__ import annotations

import json
import math
import os
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
torch.set_num_threads(int(os.environ.get("SP_THREADS", "8")))
tok = AutoTokenizer.from_pretrained(M)
model = AutoModelForCausalLM.from_pretrained(M, dtype=torch.float32).eval()


def ids_of(msgs):
    p = tok.apply_chat_template(msgs, add_generation_prompt=True, tokenize=False)
    return tok(p, return_tensors="pt", add_special_tokens=False).input_ids


@torch.no_grad()
def lp(ids, cand):
    c = tok(cand, add_special_tokens=False, return_tensors="pt").input_ids
    x = torch.cat([ids, c], 1)
    lg = model(x).logits[0, ids.shape[1] - 1:-1].float()
    return float(torch.log_softmax(lg, -1).gather(1, c[0].unsqueeze(1)).sum())


@torch.no_grad()
def sample(msgs, n):
    ids = ids_of(msgs)
    outs = []
    for i in range(0, n, 16):
        o = model.generate(ids, do_sample=True, temperature=1.0, top_p=1.0, max_new_tokens=8,
                           num_return_sequences=min(16, n - i), pad_token_id=tok.eos_token_id)
        outs += [tok.decode(x[ids.shape[1]:], skip_special_tokens=True) for x in o]
    return outs


def main():
    out = OUT / "own_local.jsonl"
    rows = []
    for key, text in PROMPTS.items():
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
        # also include the API judges' top answers so the three judges share cells
        for extra in os.environ.get("SP_EXTRA_" + key.upper(), "").split(","):
            if extra and norm(extra) not in cands:
                cands[norm(extra)] = "api_top"
        base = ids_of([{"role": "user", "content": text}])
        for a, tag in cands.items():
            shown = display(a, key)
            p_tf = math.exp(lp(base, shown))  # teacher-forced prob of the exact reply text
            rec = {"model": M, "prompt": key, "answer": a, "tag": tag,
                   "p_sample": dist[a] / NF, "p_tf": p_tf}
            for q, qtext in QUESTIONS.items():
                ids = ids_of([{"role": "user", "content": text},
                              {"role": "assistant", "content": shown},
                              {"role": "user", "content": qtext}])
                ly, ln = lp(ids, "Yes"), lp(ids, "No")
                rec[f"pyes_{q}"] = math.exp(ly) / (math.exp(ly) + math.exp(ln))
            rows.append(rec)
            print(f"  {a:14s} {tag:16s} p_s={rec['p_sample']:.3f} p_tf={p_tf:.2e} "
                  f"yes: n={rec['pyes_neutral']:.2f} r={rec['pyes_rival']:.2f} i={rec['pyes_intent']:.2f}", flush=True)
    out.write_text("".join(json.dumps(r) + "\n" for r in rows))
    print("wrote", out)


if __name__ == "__main__":
    main()
