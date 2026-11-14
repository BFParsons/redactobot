# Copyright 2026 The Redactobot Authors
# SPDX-License-Identifier: Apache-2.0

"""Show dev-split misses in context, to find out why something was not caught.

Usage: python3 -P tools/evaluation/context.py RUN CATEGORY [SUBSTRING_OF_SUBTYPE] [--status partial|missed|lost] [--n 12]
Only development documents are shown; held-out documents are never printed.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import score  # noqa: E402  (reuses the scorer's matching rules)

args = sys.argv[1:]
run, category = args[0], args[1]
sub = args[2] if len(args) > 2 and not args[2].startswith("--") else ""
status = args[args.index("--status") + 1] if "--status" in args else None
limit = int(args[args.index("--n") + 1]) if "--n" in args else 12
RAW = score.ROOT / "evaluation/results" / run / "raw"

shown = 0
for kp in sorted((score.CORPUS / "keys").glob("doc-*.json")):
    doc = kp.stem
    if score.is_heldout(doc) or shown >= limit:
        continue
    key = json.loads(kp.read_text())
    res = json.loads((RAW / f"{doc}.json").read_text())
    text = res.get("text") or ""
    dets = res.get("detections", [])
    recs, _, _ = score.score_doc(key, res)
    seen = set()
    for it, st in recs:
        if (
            it["category"] != category
            or st == "caught"
            or (status and st != status)
            or sub.lower() not in it.get("subtype", "").lower()
        ):
            continue
        if (it["value"], st) in seen or shown >= limit:
            continue
        seen.add((it["value"], st))
        m = score.pattern_for(it["value"]).search(text)
        if m:
            s, e = m.span()
            ctx = (
                text[max(0, s - 60) : s]
                + "⟦"
                + text[s:e]
                + "⟧"
                + text[e : e + 40]
            )
            over = [
                f"{d['kind']}:{d['text']!r}"
                for d in dets
                if d["start"] < e and d["end"] > s
            ]
        else:
            ctx, over = "(not in imported text)", []
        print(
            f"{doc} [{st}] {it.get('subtype', '')}: {it['value']!r}\n    {ctx!r}\n    overlapping detections: {over}"
        )
        shown += 1
