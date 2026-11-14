# Copyright 2026 B Parsons
# SPDX-License-Identifier: Apache-2.0

"""Show what is not fully caught in one sub-category, in context.

Usage: python3 -P tools/evaluation/misses.py RUN CATEGORY ["Sub-category name"] [--n 40] [--dev]
Looks at every document of the first test set (use --dev for development documents only).
Never point this at the second test set: it is kept unseen.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import score  # noqa: E402
from subcats import sub  # noqa: E402

args = sys.argv[1:]
run, category = args[0], args[1]
want = args[2] if len(args) > 2 and not args[2].startswith("--") else None
limit = int(args[args.index("--n") + 1]) if "--n" in args else 40
if "corpus2" in str(score.CORPUS):
    raise SystemExit(
        "The second test set is kept unseen; misses are not shown for it."
    )
shown = 0
for kp in sorted((score.CORPUS / "keys").glob("doc-*.json")):
    if "--dev" in args and score.is_heldout(kp.stem):
        continue
    key = json.loads(kp.read_text())
    res = json.loads((score.RAW / f"{kp.stem}.json").read_text())
    text = res.get("text") or ""
    dets = res.get("detections", [])
    spans = []
    recs, _, _ = score.score_doc(key, res, spans=spans)
    seen = set()
    for (it, st), span in zip(recs, spans):
        if (
            it["category"] != category
            or st == "caught"
            or (want and sub(it) != want)
            or (it["value"], st) in seen
        ):
            continue
        seen.add((it["value"], st))
        if shown >= limit:
            continue
        shown += 1
        if span:
            s, e = span
            ctx = (
                text[max(0, s - 70) : s]
                + "⟦"
                + text[s:e]
                + "⟧"
                + text[e : e + 45]
            )
            over = [
                f"{d['kind']}:{d['text']!r}"
                for d in dets
                if d["start"] < e and d["end"] > s
            ]
        else:
            ctx, over = (
                f"(listed {it.get('occurrences', 1)} time(s); fewer found in the imported text)",
                [],
            )
        print(
            f"{kp.stem} [{st}] {sub(it)} / {it.get('subtype', '')}: {it['value']!r}\n    {ctx!r}\n    overlapping: {over}"
        )
print(f"-- {shown} shown")
