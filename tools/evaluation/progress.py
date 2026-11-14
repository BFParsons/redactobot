# Copyright 2026 The Redactobot Authors
# SPDX-License-Identifier: Apache-2.0

"""One iteration of the sub-category loop: re-score the first test set with the current code and
show what changed.

Usage: python3 -P tools/evaluation/progress.py [--guard]
- Replays stored model output (run `c1-topics`) through the current code into run `work`.
- Prints every sub-category whose count changed since the last iteration, the ones still below
  100% in working order, and the overall figures.
- With --guard, also re-scores the second test set (totals only; its misses are never shown).
Needs the dev server on port 5173.
"""

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

T = Path(__file__).parent
ROOT = T.parents[1]
RES = ROOT / "evaluation/results"
STATE = RES / "subcategory-state.json"


def run(*cmd, env=None):
    return subprocess.run(
        [sys.executable, "-P", *cmd],
        cwd=ROOT,
        capture_output=True,
        text=True,
        env=env or os.environ,
    ).stdout


def table(md):
    rows, cat = {}, None
    for line in md.splitlines():
        m = re.match(r"## (.+?): ", line)
        if m:
            cat = m.group(1)
        m = re.match(
            r"\| (.+?) \| (\d+) \| (\d+) \| \d+% \|(?: (\d+) \(\d+%\) \|)?",
            line,
        )
        if m and cat:
            # Flag-only groups are judged by "flagged" (any part highlighted for review), the rest by full coverage.
            rows[f"{cat} / {m.group(1)}"] = [
                int(m.group(4) or m.group(2)),
                int(m.group(3)),
            ]
    return rows


shutil.rmtree(RES / "work", ignore_errors=True)
run(str(T / "run_eval.py"), "work", "--replay", "c1-topics")
now = table(
    run(str(T / "by_subcategory.py"), "work", "--out", "by-subcategory.md")
)
before = json.loads(STATE.read_text()) if STATE.exists() else {}
changed = [(k, before.get(k), v) for k, v in now.items() if before.get(k) != v]
if before:
    print("CHANGED:")
    for k, b, v in changed:
        arrow = (
            "UP  "
            if b and v[0] > b[0]
            else "DOWN" if b and v[0] < b[0] else "    "
        )
        print(f"  {arrow} {k}: {b[0] if b else '?'} -> {v[0]} of {v[1]}")
    if not changed:
        print("  nothing")
STATE.write_text(json.dumps(now, indent=0))
todo = sorted(
    ((v[0] / v[1], k, v) for k, v in now.items() if v[0] != v[1]),
    key=lambda r: (-r[0], -r[2][1]),
)
print(
    f"\nAT 100%: {sum(1 for v in now.values() if v[0] == v[1])} of {len(now)} sub-categories. NEXT:"
)
for r, k, v in todo[:8]:
    print(f"  {100 * r:5.1f}%  {v[0]}/{v[1]}  {k}")
summary = run(str(T / "score.py"), "work")
for line in summary.splitlines():
    if (
        line.startswith("| Core categories")
        or "replacements" in line
        or line.startswith("| Everything")
        or "flag" in line.lower()
    ):
        print(line[:170])
if "--guard" in sys.argv:
    env = dict(os.environ, REDACTOBOT_CORPUS=str(ROOT / "evaluation/corpus2"))
    shutil.rmtree(RES / "work2", ignore_errors=True)
    run(str(T / "run_eval.py"), "work2", "--replay", "c2-topics", env=env)
    print("\nSECOND TEST SET (unseen, totals only):")
    for line in run(str(T / "score.py"), "work2", env=env).splitlines():
        if (
            line.startswith("| Core categories")
            or "replacements" in line
            or line.startswith("| Everything")
            or line.startswith("| Places, passwords")
            or "flag" in line.lower()
        ):
            print(line[:170])
