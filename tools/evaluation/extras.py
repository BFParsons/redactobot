# Copyright 2026 The Redactobot Authors
# SPDX-License-Identifier: Apache-2.0

"""Show what the app replaced (or flagged) that the answer key does not list, in context.

Usage: python3 -P tools/evaluation/extras.py RUN [KIND] [--flags] [--n 60]
KIND is a detector kind such as company, person, record. With --flags, the flag-only kinds
(health, sensitive) are listed instead of replacements.
Never point this at the second test set: it is kept unseen.
"""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import score  # noqa: E402

args = sys.argv[1:]
kind = next(
    (a for a in args[1:] if not a.startswith("--") and not a.isdigit()), None
)
limit = int(args[args.index("--n") + 1]) if "--n" in args else 60
if "corpus2" in str(score.CORPUS):
    raise SystemExit(
        "The second test set is kept unseen; nothing is shown for it."
    )
FLAG_KINDS = {"health", "sensitive", "indirect"}
count, where = Counter(), defaultdict(list)
for kp in sorted((score.CORPUS / "keys").glob("doc-*.json")):
    key = json.loads(kp.read_text())
    res = json.loads((score.RAW / f"{kp.stem}.json").read_text())
    text = res.get("text") or ""
    _, extra, _ = score.score_doc(key, res)
    for d in extra:
        if (d["kind"] in FLAG_KINDS) != ("--flags" in args) or (
            kind and d["kind"] != kind
        ):
            continue
        k = (d["kind"], d["text"], d.get("source", ""))
        count[k] += 1
        if len(where[k]) < 1:
            where[k].append(
                f"{kp.stem}: "
                + repr(
                    text[max(0, d["start"] - 45) : d["start"]]
                    + "⟦"
                    + d["text"]
                    + "⟧"
                    + text[d["end"] : d["end"] + 30]
                )
            )
print(f"{sum(count.values())} extra detections, {len(count)} distinct")
for (k, t, src), n in count.most_common(limit):
    print(f"{n:3d} {k}/{src}: {where[(k, t, src)][0][:190]}")
