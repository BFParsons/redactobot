# Copyright 2026 The Redactobot Authors
# SPDX-License-Identifier: Apache-2.0

# Experiment (14 Nov 2026), see evaluation/MASKER-EXPERIMENT.md. Needs onnxruntime, tokenizers, numpy and the
# masker-mini files (config.json, tokenizer.json, onnx/model_int4.onnx) from huggingface.co/amsintelligence/masker-mini.
"""Run masker-mini (ONNX int4) on paste pieces and write scorer-readable runs.

python run_masker.py MODEL_DIR REPO_DIR SUFFIX PIECES.json
Writes evaluation/results/pg-{mm,mmnames,mmrules}-paste-SUFFIX/raw/*.json in REPO_DIR.
"""

import json
import os
import statistics
import sys
import time
import numpy as np
import onnxruntime as ort
from tokenizers import Tokenizer

model_dir, repo, suffix, pieces_path = sys.argv[1:5]
cfg = json.load(open(os.path.join(model_dir, "config.json"), encoding="utf8"))
id2label = {int(k): v for k, v in cfg["id2label"].items()}
tok = Tokenizer.from_file(os.path.join(model_dir, "tokenizer.json"))
tok.enable_truncation(max_length=512)
opts = ort.SessionOptions()
opts.intra_op_num_threads = 1
opts.inter_op_num_threads = 1
sess = ort.InferenceSession(
    os.path.join(model_dir, "onnx", "model_int4.onnx"),
    opts,
    providers=["CPUExecutionProvider"],
)
inputs = [i.name for i in sess.get_inputs()]

KIND = {
    "GIVEN_NAME": "person",
    "SURNAME": "person",
    "CITY": "place",
    "STREET_NAME": "street",
    "BUILDING_NUMBER": "street",
    "ZIP_CODE": "zip",
    "PHONE": "phone",
    "EMAIL": "email",
    "CREDIT_CARD": "card",
    "DATE": "date",
    "AGE": "age",
    "GOVERNMENT_ID": "government_id",
}


def tag(text):
    enc = tok.encode(text)
    feed = {
        "input_ids": np.array([enc.ids], dtype=np.int64),
        "attention_mask": np.array([enc.attention_mask], dtype=np.int64),
    }
    if "token_type_ids" in inputs:
        feed["token_type_ids"] = np.array([enc.type_ids], dtype=np.int64)
    t0 = time.perf_counter()
    logits = sess.run(None, {k: v for k, v in feed.items() if k in inputs})[0][
        0
    ]
    ms = (time.perf_counter() - t0) * 1000
    labels = logits.argmax(-1)
    # Uncertainty: tokens whose best label wins by a small probability margin.
    ex = np.exp(logits - logits.max(-1, keepdims=True))
    probs = ex / ex.sum(-1, keepdims=True)
    top2 = np.sort(probs, -1)[:, -2:]
    margins = top2[:, 1] - top2[:, 0]
    global last_unsure
    last_unsure = int(
        ((margins < 0.5) & (np.array([e > s for s, e in enc.offsets]))).sum()
    )
    spans, cur = [], None
    for (s, e), lab in zip(enc.offsets, labels):
        if s == e:
            continue
        name = id2label[int(lab)]
        if name == "O":
            if cur:
                spans.append(cur)
                cur = None
            continue
        prefix, kind = name[0], name[2:]
        # Join pieces of one word and continuing tags; start a new span on B/S or a new kind.
        if cur and cur["label"] == kind and (prefix in "IE" or s == cur["end"]):
            cur["end"] = e
        else:
            if cur:
                spans.append(cur)
            cur = {"start": s, "end": e, "label": kind}
        if prefix in "ES":
            spans.append(cur)
            cur = None
    if cur:
        spans.append(cur)
    # Offsets can include the whitespace before a word; trim spans to their visible characters.
    out = []
    for sp in spans:
        st, en = sp["start"], sp["end"]
        while st < en and text[st].isspace():
            st += 1
        while en > st and text[en - 1].isspace():
            en -= 1
        if en > st:
            out.append({**sp, "start": st, "end": en})
    return out, ms, len(enc.ids)


docs = json.load(open(pieces_path, encoding="utf8"))
times, tokens, unsure = [], [], []
out = {v: [] for v in ("mm", "mmnames", "mmrules")}
for d in docs:
    raw = json.load(
        open(
            os.path.join(
                repo,
                "evaluation/results",
                f"pg-det-paste-{suffix}",
                "raw",
                d["file"],
            ),
            encoding="utf8",
        )
    )
    text, rules = raw["text"], raw["detections"]
    model = []
    for p in d["pieces"]:
        spans, ms, n = tag(text[p["start"] : p["end"]])
        unsure.append(
            {
                "file": d["file"],
                "start": p["start"],
                "end": p["end"],
                "unsure": last_unsure,
            }
        )
        times.append(ms)
        tokens.append(n)
        model += [
            {
                "start": s["start"] + p["start"],
                "end": s["end"] + p["start"],
                "text": text[s["start"] + p["start"] : s["end"] + p["start"]],
                "kind": KIND.get(s["label"], "other"),
                "source": "masker",
                "label": s["label"],
            }
            for s in spans
        ]
    names = [m for m in model if m["kind"] == "person"]
    for v, dets in (
        ("mm", model),
        ("mmnames", rules + names),
        ("mmrules", rules + model),
    ):
        folder = os.path.join(
            repo, "evaluation/results", f"pg-{v}-paste-{suffix}", "raw"
        )
        os.makedirs(folder, exist_ok=True)
        json.dump(
            {
                "id": raw.get("id", d["file"][:-5]),
                "text": text,
                "detections": dets,
            },
            open(os.path.join(folder, d["file"]), "w", encoding="utf8"),
        )

times.sort()
print(
    f"{suffix}: {len(times)} pieces, median {statistics.median(times):.1f} ms, p90 {times[int(len(times) * .9)]:.1f} ms, "
    f"mean tokens {statistics.mean(tokens):.0f} (1 CPU thread, int4)"
)

json.dump(
    unsure,
    open(
        os.path.join(os.path.dirname(pieces_path), f"unsure-{suffix}.json"), "w"
    ),
)
