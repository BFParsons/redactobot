# Copyright 2026 The Redactobot Authors
# SPDX-License-Identifier: Apache-2.0

"""Hit rate per sub-category of sensitive data.

The answer keys label each item with a free-text subtype (and, for names, a `variant`). This
script groups those labels into a fixed set of sub-categories and reports the catch rate of each.

Usage: python3 -P tools/evaluation/by_subcategory.py RUN [--out FILE.md]
Uses the first test set (evaluation/corpus) unless REDACTOBOT_CORPUS is set. The subtype wording of the
second test set differs, and that set is kept unseen, so it is not broken down here.
"""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
RUN_ARG = sys.argv[1]
import score  # noqa: E402

OUT = (
    sys.argv[sys.argv.index("--out") + 1]
    if "--out" in sys.argv
    else "by-subcategory.md"
)

from subcats import LABEL, sub  # noqa: E402

keys = {
    p.stem: json.loads(p.read_text())
    for p in sorted((score.CORPUS / "keys").glob("doc-*.json"))
}
tally = defaultdict(lambda: defaultdict(Counter))
for doc, key in keys.items():
    f = score.RAW / f"{doc}.json"
    if not f.exists():
        continue
    recs, _, _ = score.score_doc(key, json.loads(f.read_text()))
    for it, st in recs:
        tally[it["category"]][sub(it)][st] += 1

pct = lambda a, b: f"{100 * a / b:.0f}%" if b else "n/a"
out = [
    f"# Hit rate by sub-category (run `{RUN_ARG}`, {len(keys)} documents)",
    "",
    '"Caught" means every character of the value was covered. For the flag-only categories, "Flagged" counts a',
    "value when any part of it was underlined for review. Sub-categories with fewer than 10 occurrences are too small",
    "to read much into.",
    "",
]
order = sorted(
    tally, key=lambda c: -sum(sum(v.values()) for v in tally[c].values())
)
for cat in order:
    subs = tally[cat]
    total = Counter()
    for c in subs.values():
        total.update(c)
    n = sum(total.values())
    flag = cat in score.WARN
    out.append(
        f"## {LABEL.get(cat, cat)}: {pct(total['caught'], n)} of {n}"
        + (
            f" fully covered, {pct(total['caught'] + total['partial'], n)} flagged"
            if flag
            else ""
        )
    )
    out.append("")
    out.append(
        "| Sub-category | Caught | Of | Rate |" + (" Flagged |" if flag else "")
    )
    out.append("|---|---|---|---|" + ("---|" if flag else ""))
    for name, c in sorted(subs.items(), key=lambda kv: -sum(kv[1].values())):
        m = sum(c.values())
        out.append(
            f"| {name} | {c['caught']} | {m} | {pct(c['caught'], m)} |"
            + (
                f" {c['caught'] + c['partial']} ({pct(c['caught'] + c['partial'], m)}) |"
                if flag
                else ""
            )
        )
    out.append("")
(score.ROOT / "evaluation/results" / OUT).write_text("\n".join(out) + "\n")
print("\n".join(out))
