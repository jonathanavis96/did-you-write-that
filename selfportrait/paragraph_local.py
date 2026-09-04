"""Pilot 18: the paragraph ownership design (selfportrait/paragraph.py) on a local HF
causal-LM with exact probabilities, on the pilot 14 scale series.

Stage A  sample SP_N paragraphs per prompt (first one is the own paragraph).
Stage B  cells: own, other_local, other_opus, other_gpt, shifted.
Stage C  per cell: teacher-forced log p of the paragraph after the prompt (sum and
         per-token mean) and exact P(Yes) for neutral, placebo and rival.
Stage P  forced choice as pilot 17 stage P, both orders, exact P(own position).

Env vars: SP_LOCAL_MODEL, SP_LOCAL_DTYPE, SP_LOCAL_DEVICE, SP_N (default 8),
SP_OTHER_LOCAL (model id whose own paragraph is the other_local cell; its
out/para_local_<slug>.jsonl must already hold stage A rows), SP_P17C (default
out/p17c/para_forks.jsonl), SP_THREADS. Output out/para_local_<slug>.jsonl, appended,
resumable by row key.

The prompt dict is read out of paragraph.py's source with ast rather than imported,
because importing paragraph.py builds a Claude config directory at import time.
make_shifted and the pair question are copied verbatim from paragraph.py.
"""
from __future__ import annotations

import ast
import json
import math
import os
import re
import sys
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from selfportrait.ownership import QUESTIONS  # noqa: E402


def slug_of(model_id: str) -> str:
    """As ownership_local.slug_of (not imported: that module loads its model at import)."""
    base = model_id.split("/")[-1].lower()
    return re.sub(r"[^a-z0-9._-]+", "-", base).strip("-")


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "out"
M = os.environ.get("SP_LOCAL_MODEL", "Qwen/Qwen2.5-1.5B-Instruct")
NF = int(os.environ.get("SP_N", "8"))
OTHER_LOCAL = os.environ.get("SP_OTHER_LOCAL")
P17C = Path(os.environ.get("SP_P17C", str(OUT / "p17c" / "para_forks.jsonl")))
OUT_PATH = OUT / f"para_local_{slug_of(M)}.jsonl"
MAX_NEW = 160
STAGE_QUESTIONS = ("neutral", "placebo", "rival")
HEDGES = ["I suppose", "Perhaps", "It may be that"]
torch.set_num_threads(int(os.environ.get("SP_THREADS", "8")))


def read_prompts() -> dict[str, str]:
    src = (ROOT / "selfportrait" / "paragraph.py").read_text()
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "PROMPTS" for t in node.targets):
            return ast.literal_eval(node.value)
    raise RuntimeError("PROMPTS not found in paragraph.py")


PROMPTS = read_prompts()
if os.environ.get("SP_PROMPTS"):
    PROMPTS = {k: PROMPTS[k] for k in os.environ["SP_PROMPTS"].split(",")}


def make_shifted(paragraph: str) -> str:
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", paragraph.strip()) if s]
    out = []
    for i, s in enumerate(sentences):
        hedge = HEDGES[i % len(HEDGES)]
        if s[0].isupper() and not s.startswith("I "):
            s = s[0].lower() + s[1:]
        out.append(f"{hedge}, {s}")
    return " ".join(out)


def build_pair_question(prompt_text: str, own: str, other: str, own_position: int) -> str:
    first, second = (own, other) if own_position == 1 else (other, own)
    return (f'Here are two answers to the question "{prompt_text}"\n\n'
            f"(1) {first}\n\n(2) {second}\n\n"
            "One of these two answers was written by you in another session and one by a "
            "different model. Which one did you write? Reply with only 1 or 2.")


DTYPE = {"float32": torch.float32, "fp32": torch.float32, "bf16": torch.bfloat16,
         "bfloat16": torch.bfloat16, "float16": torch.float16, "fp16": torch.float16}[
    os.environ.get("SP_LOCAL_DTYPE", "float32")]
DTYPE_NAME = os.environ.get("SP_LOCAL_DTYPE", "float32")
DEV_NAME = os.environ.get("SP_LOCAL_DEVICE", "cpu")
if DEV_NAME == "dml":
    import torch_directml
    DEV = torch_directml.device()
else:
    DEV = DEV_NAME
tok = AutoTokenizer.from_pretrained(M)
model = AutoModelForCausalLM.from_pretrained(M, dtype=DTYPE, low_cpu_mem_usage=True).eval().to(DEV)


def ids_of(msgs):
    p = tok.apply_chat_template(msgs, add_generation_prompt=True, tokenize=False)
    return tok(p, return_tensors="pt", add_special_tokens=False).input_ids


@torch.no_grad()
def lp(ids, cand) -> tuple[float, int]:
    """Sum of log-probabilities of `cand` teacher-forced after `ids`, and its token count."""
    c = tok(cand, add_special_tokens=False, return_tensors="pt").input_ids
    x = torch.cat([ids, c], 1).to(DEV)
    lg = model(x).logits[0, ids.shape[1] - 1:-1].float().cpu()
    return float(torch.log_softmax(lg, -1).gather(1, c[0].unsqueeze(1)).sum()), int(c.shape[1])


def p_first(ids, a: str, b: str) -> float:
    la, _ = lp(ids, a)
    lb, _ = lp(ids, b)
    return math.exp(la) / (math.exp(la) + math.exp(lb))


@torch.no_grad()
def sample(msgs, n):
    ids = ids_of(msgs).to(DEV)
    outs = []
    for i in range(0, n, 8):
        o = model.generate(ids, do_sample=True, temperature=1.0, top_p=1.0, max_new_tokens=MAX_NEW,
                           num_return_sequences=min(8, n - i), pad_token_id=tok.eos_token_id)
        outs += [tok.decode(x[ids.shape[1]:], skip_special_tokens=True).strip() for x in o]
    return outs


def load_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def first_paragraph(rows: list[dict], prompt: str) -> str | None:
    for r in rows:
        if r.get("stage") == "fork" and r["prompt"] == prompt and r.get("raw"):
            return r["raw"]
    return None


def p17c_first(model_name: str, prompt: str) -> str | None:
    for r in load_rows(P17C):
        if r["model"] == model_name and r["prompt"] == prompt and not r.get("error") and r.get("raw"):
            return r["raw"]
    return None


def main():
    rows = load_rows(OUT_PATH)
    fh = OUT_PATH.open("a")

    def emit(rec):
        rec.update({"model": M, "device": DEV_NAME, "dtype": DTYPE_NAME})
        fh.write(json.dumps(rec) + "\n")
        fh.flush()
        rows.append(rec)

    # stage A
    for key, text in PROMPTS.items():
        have = sum(1 for r in rows if r.get("stage") == "fork" and r["prompt"] == key)
        if have >= NF:
            continue
        outs = sample([{"role": "user", "content": text}], NF - have)
        for i, o in enumerate(outs):
            emit({"stage": "fork", "prompt": key, "index": have + i, "raw": o})
        print(f"A {key}: {len(outs)} paragraphs, first {len(outs[0].split())} words", flush=True)

    other_rows = load_rows(OUT / f"para_local_{slug_of(OTHER_LOCAL)}.jsonl") if OTHER_LOCAL else []

    # stage B + C
    done = {(r["prompt"], r["cell"], r["question"]) for r in rows if r.get("stage") == "own"}
    for key, text in PROMPTS.items():
        own = first_paragraph(rows, key)
        if not own:
            print(f"skip {key}: no own paragraph", flush=True)
            continue
        cells = {
            "own": (own, M),
            "other_local": (first_paragraph(other_rows, key), OTHER_LOCAL),
            "other_opus": (p17c_first("opus", key), "opus"),
            "other_gpt": (p17c_first("gpt", key), "gpt"),
            "shifted": (make_shifted(own), M),
        }
        base = ids_of([{"role": "user", "content": text}])
        for cell, (para, src) in cells.items():
            if not para:
                print(f"skip {key}|{cell}: no paragraph", flush=True)
                continue
            if all((key, cell, q) in done for q in STAGE_QUESTIONS):
                continue
            s, n = lp(base, para)
            prefix = [{"role": "user", "content": text}, {"role": "assistant", "content": para}]
            for q in STAGE_QUESTIONS:
                if (key, cell, q) in done:
                    continue
                ids = ids_of(prefix + [{"role": "user", "content": QUESTIONS[q]}])
                emit({"stage": "own", "prompt": key, "cell": cell, "source_model": src,
                      "question": q, "p_yes": p_first(ids, "Yes", "No"),
                      "log_p_tf": s, "n_tokens": n, "mean_lp": s / n, "words": len(para.split())})
                done.add((key, cell, q))
        print(f"C {key}: cells done", flush=True)

    # stage P
    done_p = {(r["prompt"], r["comparison"], r["own_position"]) for r in rows if r.get("stage") == "pair"}
    for key, text in PROMPTS.items():
        own = first_paragraph(rows, key)
        if not own:
            continue
        for comp, (other, src) in {
            "own_vs_other_local": (first_paragraph(other_rows, key), OTHER_LOCAL),
            "own_vs_other_opus": (p17c_first("opus", key), "opus"),
            "own_vs_other_gpt": (p17c_first("gpt", key), "gpt"),
        }.items():
            if not other:
                continue
            for pos in (1, 2):
                if (key, comp, pos) in done_p:
                    continue
                q = build_pair_question(text, own, other, pos)
                ids = ids_of([{"role": "user", "content": q}])
                p1 = p_first(ids, "1", "2")
                emit({"stage": "pair", "prompt": key, "comparison": comp, "source_model": src,
                      "own_position": pos, "p_choose_1": p1, "p_own": p1 if pos == 1 else 1 - p1})
        print(f"P {key}: pairs done", flush=True)
    fh.close()
    print("wrote", OUT_PATH, flush=True)


if __name__ == "__main__":
    main()
