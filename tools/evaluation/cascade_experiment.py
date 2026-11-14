# Copyright 2026 The Redactobot Authors
# SPDX-License-Identifier: Apache-2.0

"""Write cascade runs that route the least certain paste pieces to Nano.

Usage: python3 tools/evaluation/cascade_experiment.py REPO_DIR SUFFIX [DIR]

Reads unsure-SUFFIX.json (from DIR, default: next to this script), ranks the
pieces by their "unsure" score, and for 0, 10, 25, 50 and 100 percent routed
writes evaluation/results/pg-cascN-paste-SUFFIX/raw/*.json in REPO_DIR: the
pg-mmrules run plus the pg-nano detections that fall inside routed pieces.
Part of the masker-mini experiment (evaluation/MASKER-EXPERIMENT.md); not
used by the application.
"""

import json
import os
import sys

repo, suffix = sys.argv[1], sys.argv[2]
unsure = json.load(
    open(
        os.path.join(
            sys.argv[3] if len(sys.argv) > 3 else os.path.dirname(__file__),
            f"unsure-{suffix}.json",
        )
    )
)
order = sorted(range(len(unsure)), key=lambda i: -unsure[i]["unsure"])
for pct in (0, 10, 25, 50, 100):
    routed = set(order[: round(len(order) * pct / 100)])
    by_file = {}
    for i, u in enumerate(unsure):
        by_file.setdefault(u["file"], []).append((u, i in routed))
    out = os.path.join(
        repo, "evaluation/results", f"pg-casc{pct}-paste-{suffix}", "raw"
    )
    os.makedirs(out, exist_ok=True)
    for f, pieces in by_file.items():
        base = json.load(
            open(
                os.path.join(
                    repo,
                    "evaluation/results",
                    f"pg-mmrules-paste-{suffix}",
                    "raw",
                    f,
                ),
                encoding="utf8",
            )
        )
        nano = json.load(
            open(
                os.path.join(
                    repo,
                    "evaluation/results",
                    f"pg-nano-paste-{suffix}",
                    "raw",
                    f,
                ),
                encoding="utf8",
            )
        )["detections"]
        extra = [
            d
            for d in nano
            if any(r and u["start"] <= d["start"] < u["end"] for u, r in pieces)
        ]
        json.dump(
            {**base, "detections": base["detections"] + extra},
            open(os.path.join(out, f), "w", encoding="utf8"),
        )
print("cascade runs written for", suffix)
