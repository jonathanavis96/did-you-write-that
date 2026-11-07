"""The label control compares layouts over the same sampled cells, so both layouts must
draw the same distribution. torch and transformers are stubbed: the fake RNG, like torch's
global one, carries on from wherever it was unless it is seeded."""
import importlib
import json
import random
import sys
import types
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

WORDS = [f"word{i}" for i in range(40)]


def stub_torch(monkeypatch, manual_seed=lambda s: None):
    torch = types.ModuleType("torch")
    torch.no_grad = lambda: (lambda f: f)
    torch.float32 = torch.bfloat16 = torch.float16 = object()
    torch.set_num_threads = lambda n: None
    torch.manual_seed = manual_seed

    class Stub:
        from_pretrained = staticmethod(lambda *a, **k: Stub())
        eval = to = lambda self, *a: self

    transformers = types.ModuleType("transformers")
    transformers.AutoTokenizer = transformers.AutoModelForCausalLM = Stub
    monkeypatch.setitem(sys.modules, "torch", torch)
    monkeypatch.setitem(sys.modules, "transformers", transformers)


@pytest.fixture
def local(monkeypatch, tmp_path):
    rng = random.Random(1234)
    seeds = []

    def manual_seed(s):
        seeds.append(s)
        rng.seed(s)

    stub_torch(monkeypatch, manual_seed)
    monkeypatch.setenv("SP_LOCAL_OUT", str(tmp_path / "out.jsonl"))
    monkeypatch.setenv("SP_PROMPTS", "fruit,number")
    monkeypatch.setenv("SP_QUESTIONS", "neutral")
    monkeypatch.setenv("SP_N", "12")
    sys.modules.pop("selfportrait.ownership_local", None)
    mod = importlib.import_module("selfportrait.ownership_local")
    monkeypatch.setattr(mod, "sample", lambda msgs, n: rng.choices(WORDS, k=n))
    monkeypatch.setattr(mod, "ids_of", lambda msgs: None)
    monkeypatch.setattr(mod, "lp", lambda ids, cand: -1.0)
    mod.test_seeds = seeds
    yield mod
    sys.modules.pop("selfportrait.ownership_local", None)


def cells(rows, layout):
    return {(r["prompt"], r["answer"], r["tag"], r["p_sample"]) for r in rows if r["layout"] == layout}


def read(mod):
    return [json.loads(ln) for ln in mod.OUT_PATH.read_text().splitlines()]


def test_both_layouts_plant_the_same_cells(local, monkeypatch):
    monkeypatch.setattr(local, "LAYOUT", "assistant")
    local.main()
    monkeypatch.setattr(local, "LAYOUT", "user2")
    local.main()
    rows = read(local)
    assert cells(rows, "assistant") == cells(rows, "user2")
    assert len(cells(rows, "assistant")) > 2


def test_each_prompt_has_its_own_seed_and_rows_record_it(local):
    local.main()
    assert len(set(local.test_seeds)) == 2
    assert {r["seed"] for r in read(local)} == set(local.test_seeds)


def test_resume_after_torn_line_keeps_every_row(local):
    good = {"prompt": "x", "answer": "y", "question": "neutral", "layout": "assistant"}
    local.OUT_PATH.write_text(json.dumps(good) + "\n" + '{"prompt": "half')
    local.main()
    rows = read(local)
    assert rows[0] == good
    assert len(rows) > 1


def test_paragraph_local_resumes_after_a_torn_line(monkeypatch, tmp_path):
    stub_torch(monkeypatch)
    sys.modules.pop("selfportrait.paragraph_local", None)
    mod = importlib.import_module("selfportrait.paragraph_local")
    out = tmp_path / "para.jsonl"
    good = '{"stage": "fork", "prompt": "sky", "raw": "x"}\n'
    out.write_text(good + '{"stage": "fo')
    monkeypatch.setattr(mod, "OUT_PATH", out)
    monkeypatch.setattr(mod, "PROMPTS", {})
    mod.main()
    sys.modules.pop("selfportrait.paragraph_local", None)
    assert out.read_text() == good
