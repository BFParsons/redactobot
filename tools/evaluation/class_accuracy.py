# Copyright 2026 The Redactobot Authors
# SPDX-License-Identifier: Apache-2.0

"""Write taxonomy/accuracy.js: how often each category of value was fully caught on the unseen test set.

Usage: python3 -P tools/evaluation/class_accuracy.py [RUN]      (default run: c2-round4)
The app's "By type of data" picker ranks its classes with these figures, so the ranking shown to
users is the measured one. Only totals are read from the unseen set; no document is inspected.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

T = Path(__file__).parent
ROOT = T.parents[1]
run = sys.argv[1] if len(sys.argv) > 1 else "c2-round4"
env = dict(os.environ, REDACTOBOT_CORPUS=str(ROOT / "evaluation/corpus2"))
out = subprocess.run(
    [sys.executable, "-P", str(T / "score.py"), run],
    cwd=ROOT,
    env=env,
    capture_output=True,
    text=True,
).stdout

measured = {}
in_table = False
for line in out.splitlines():
    if line.startswith("## By category"):
        in_table = True
        continue
    if in_table and line.startswith("## "):
        break
    m = re.match(
        r"\| ([a-z_0-9]+)(?: \([^)]*\))? \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \|",
        line,
    )
    if in_table and m:
        name, caught, partly, missed, lost, total = m.group(1), *map(
            int, m.groups()[1:]
        )
        measured[name] = {"caught": caught, "partly": partly, "of": total}
flag = re.search(
    r"flagged for review \(any part highlighted\) \| (\d+) \| (\d+) \|", out
)
if not measured or not flag:
    sys.exit("could not read the score table for run " + run)
measured["flagged"] = {
    "caught": int(flag.group(1)),
    "partly": 0,
    "of": int(flag.group(2)),
}

body = json.dumps(measured, indent=2, sort_keys=True)
(ROOT / "taxonomy/accuracy.js").write_text(
    "// Written by tools/evaluation/class_accuracy.py. Do not edit by hand.\n"
    f"// Source: evaluation run `{run}` on the second test set (60 documents whose misses are never inspected).\n"
    "// caught = every letter and digit of the value was replaced; of = values in the answer keys.\n"
    "// `flagged` counts sensitive facts with any part underlined for review.\n"
    f"export const MEASURED_RUN = {json.dumps(run)};\n"
    f"export const MEASURED = {body};\n"
)
print(f"wrote taxonomy/accuracy.js from {run}: {len(measured)} categories")
