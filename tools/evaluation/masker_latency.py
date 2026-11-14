# Copyright 2026 B Parsons
# SPDX-License-Identifier: Apache-2.0

"""Time masker-mini (ONNX int4) on paste pieces at 1, 2, 4 and 8 CPU threads.

Usage: python3 tools/evaluation/masker_latency.py MODEL_DIR PIECES.json RAW_DIR

Prints the median and 90th-percentile latency per piece for the pieces of
the first 20 documents. Part of the masker-mini experiment
(evaluation/MASKER-EXPERIMENT.md); not used by the application.
"""

import json
import os
import statistics
import sys
import time
import numpy as np
import onnxruntime as ort
from tokenizers import Tokenizer

m, pieces = sys.argv[1], sys.argv[2]
tok = Tokenizer.from_file(os.path.join(m, "tokenizer.json"))
tok.enable_truncation(max_length=512)
docs = json.load(open(pieces, encoding="utf8"))
texts = []
for d in docs[:20]:
    raw = json.load(
        open(os.path.join(sys.argv[3], d["file"]), encoding="utf8")
    )["text"]
    texts += [raw[p["start"] : p["end"]] for p in d["pieces"]]
for threads in (1, 2, 4, 8):
    o = ort.SessionOptions()
    o.intra_op_num_threads = threads
    s = ort.InferenceSession(
        os.path.join(m, "onnx", "model_int4.onnx"),
        o,
        providers=["CPUExecutionProvider"],
    )
    names = [i.name for i in s.get_inputs()]
    ts = []
    for t in texts:
        e = tok.encode(t)
        feed = {
            "input_ids": np.array([e.ids]),
            "attention_mask": np.array([e.attention_mask]),
            "token_type_ids": np.array([e.type_ids]),
        }
        t0 = time.perf_counter()
        s.run(
            None, {k: v.astype(np.int64) for k, v in feed.items() if k in names}
        )
        ts.append((time.perf_counter() - t0) * 1000)
    ts.sort()
    print(
        f"threads={threads}: median {statistics.median(ts):.1f} ms, p90 {ts[int(len(ts)*.9)]:.1f} ms over {len(ts)} pieces"
    )
