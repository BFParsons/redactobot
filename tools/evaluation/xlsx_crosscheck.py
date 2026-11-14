# Copyright 2026 B Parsons
# SPDX-License-Identifier: Apache-2.0

"""Independent check of the Excel importer: compare the text the app extracted from each
.xlsx in the corpus with what LibreOffice displays for the same workbook.

LibreOffice prints the workbook to PDF (cells as displayed), pdftotext reads it back, and every
printed token that contains a digit is looked up in the app's text. (LibreOffice's CSV export
was tried first and writes raw numbers, so it cannot check display formats.)

Usage: python3 -P tools/evaluation/xlsx_crosscheck.py RUN_NAME
Examples are shown for development documents only.
"""

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN = sys.argv[1]
total = missing = 0
for doc in sorted((ROOT / "evaluation/corpus/docs").glob("*.xlsx")):
    heldout = int(doc.stem.split("-")[1]) % 10 in (3, 6, 9)
    text = json.loads(
        (
            ROOT / "evaluation/results" / RUN / "raw" / f"{doc.stem}.json"
        ).read_text()
    ).get("text", "")
    have = set(re.split(r"[\s]+", text))
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(
            [
                "soffice",
                "--headless",
                f"-env:UserInstallation=file://{tmp}/profile",
                "--convert-to",
                "pdf",
                "--outdir",
                tmp,
                str(doc),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        shown = subprocess.run(
            ["pdftotext", "-layout", f"{tmp}/{doc.stem}.pdf", "-"],
            capture_output=True,
            text=True,
        ).stdout
    tokens = [
        t
        for t in re.split(r"\s+", shown)
        if re.search(r"\d", t)
        and "#" not in t
        and not re.fullmatch(r"\d{1,2}", t)
    ]
    lost = [t for t in tokens if t not in have and t not in text]
    total += len(tokens)
    missing += len(lost)
    eg = (
        ""
        if heldout or not lost
        else "  e.g. " + "; ".join(repr(c) for c in lost[:8])
    )
    if (
        "--shapes" in sys.argv
    ):  # show only the shape of what differs, not the content
        import collections

        shape = lambda t: re.sub(
            r"[a-z]", "a", re.sub(r"[A-Z]", "A", re.sub(r"\d", "9", t))
        )
        print(
            "   shapes:",
            dict(collections.Counter(shape(t) for t in lost).most_common(8)),
        )
    print(
        f"{doc.stem} {'held-out' if heldout else 'dev':8} printed tokens with digits={len(tokens):4} not in app text={len(lost):3}{eg}"
    )
print(
    f"TOTAL tokens={total} not in app text={missing} ({100 * missing / max(total, 1):.1f}%)"
)
