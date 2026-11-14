# Copyright 2026 B Parsons
# SPDX-License-Identifier: Apache-2.0

"""Re-score the third test set (the working set) with the current code.

Usage: python3 -P tools/evaluation/progress3.py [--replay RUN]
Without --replay the on-device model is off (pattern and rule detection only), which takes
under a minute. With --replay RUN, stored model output from that run is used.
Prints the totals and the per-category table. Needs the dev server on port 5173.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

T = Path(__file__).parent
ROOT = T.parents[1]
env = dict(os.environ, REDACTOBOT_CORPUS=str(ROOT / "evaluation/corpus3"))
run = "work3"
shutil.rmtree(ROOT / "evaluation/results" / run, ignore_errors=True)
extra = (
    ["--replay", sys.argv[sys.argv.index("--replay") + 1]]
    if "--replay" in sys.argv
    else ["--no-model"]
)
# The dev server reloads the page when source files have just changed, which can cut a run short.
# The run skips documents that are already done, so trying again finishes it.
for _ in range(4):
    subprocess.run(
        [sys.executable, "-P", str(T / "run_eval.py"), run, *extra],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
    )
    if (
        len(
            list((ROOT / "evaluation/results" / run / "raw").glob("doc-*.json"))
        )
        >= 60
    ):
        break
out = subprocess.run(
    [sys.executable, "-P", str(T / "score.py"), run],
    cwd=ROOT,
    env=env,
    capture_output=True,
    text=True,
).stdout
show = False
for line in out.splitlines():
    if (
        line.startswith("| Everything")
        or line.startswith("| Core")
        or line.startswith("| Places, pass")
        or "flagged for review" in line
        or "touched nothing" in line
    ):
        print(line[:150])
    if line.startswith("## By category"):
        show = True
    elif line.startswith("## ") and show:
        break
    if (
        show
        and line.startswith("| ")
        and "100.0%" not in line
        and "Caught" not in line
    ):
        print(line[:120])
