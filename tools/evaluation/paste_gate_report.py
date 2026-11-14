# Copyright 2026 The Redactobot Authors
# SPDX-License-Identifier: Apache-2.0

"""Summarize paste-gate runs from paste_gate_compare.ts across both corpora.

Usage: PYTHONUTF8=1 python -P tools/evaluation/paste_gate_report.py [variant ...]
Default variants: det-paste det-doc. Corpus 2 is the unseen set: totals only.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VARIANTS = sys.argv[1:] or ["det-paste", "det-doc"]
CRIT = [
    "person_name",
    "email",
    "phone",
    "street_address",
    "ssn",
    "government_id",
    "tax_id",
    "date_of_birth",
    "bank_account",
    "routing_number",
    "iban",
    "payment_card",
    "card_security_code",
    "card_expiry",
    "credential",
]
SECOND = [
    "organization_name",
    "record_number",
    "postal_code",
    "place",
    "ip_address",
    "url",
    "device_id",
    "vehicle_id",
    "date",
    "money_amount",
    "age_over_89",
]


def score(run, corpus):
    env = {
        **os.environ,
        "REDACTOBOT_CORPUS": f"evaluation/{corpus}",
        "PYTHONUTF8": "1",
    }
    out = subprocess.run(
        [sys.executable, "-P", "tools/evaluation/score.py", run, "--json"],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return json.loads(out)


def pct(s, cats):
    c = t = 0
    for k in cats:
        b = s["by_category"].get(k)
        if b:
            c += b["caught"]
            t += b["total"]
    return f"{100 * c / t:5.1f}%" if t else "   - "


print(
    f"{'run':<22}{'person':>8}{'org':>8}{'critical':>10}{'second':>9}{'over-red':>10}"
)
for corpus, suffix in [("corpus3", "c3"), ("corpus2", "c2")]:
    for v in VARIANTS:
        s = score(f"pg-{v}-{suffix}", corpus)
        over = 100 * s["extra_detections"] / max(1, s["detections"])
        print(
            f"{v + ' ' + suffix:<22}{pct(s, ['person_name']):>8}{pct(s, ['organization_name']):>8}"
            f"{pct(s, CRIT):>10}{pct(s, SECOND):>9}{over:>9.1f}%"
        )
