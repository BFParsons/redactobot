# Copyright 2026 B Parsons
# SPDX-License-Identifier: Apache-2.0

"""Catch rate per rule set.

For each rule set, the corpus is run with ONLY that rule set switched on (replaying the names the
on-device model returned in an earlier live run), and scored against the answer-key categories
that rule set covers. The mapping below says which answer-key categories belong to which rule.

Usage: python3 -P tools/evaluation/by_ruleset.py NAMES_FROM_RUN [--skip-run] [--out FILE.md] [--prefix rule]
Writes evaluation/results/by-ruleset.md (or FILE.md). Set REDACTOBOT_CORPUS to score another corpus.
Where the answer keys mark minors and cardholders (the second corpus does), those names are
scored for the court-filing and payment-card rules.
"""

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import score  # noqa: E402

ROOT = score.ROOT
SOURCE = sys.argv[1]
OUT = (
    sys.argv[sys.argv.index("--out") + 1]
    if "--out" in sys.argv
    else "by-ruleset.md"
)
PREFIX = (
    sys.argv[sys.argv.index("--prefix") + 1]
    if "--prefix" in sys.argv
    else "rule"
)
# HIPAA lists "geographic subdivisions smaller than a State", so a state or province on its own is
# not something that rule asks to have removed. Those key items are left out of HIPAA's score.
REGIONS = (
    set(
        """AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK
OR PA RI SC SD TN TX UT VT VA WA WV WI WY PR AB BC MB NB NL NS NT NU ON PE QC SK YT""".split()
    )
    | {
        x.strip()
        for x in """Alabama,Alaska,
Arizona,Arkansas,California,Colorado,Connecticut,Delaware,Florida,Georgia,Hawaii,Idaho,Illinois,Indiana,Iowa,Kansas,Kentucky,Louisiana,
Maine,Maryland,Massachusetts,Michigan,Minnesota,Mississippi,Missouri,Montana,Nebraska,Nevada,New Hampshire,New Jersey,New Mexico,New York,
North Carolina,North Dakota,Ohio,Oklahoma,Oregon,Pennsylvania,Rhode Island,South Carolina,South Dakota,Tennessee,Texas,Utah,Vermont,Virginia,
Washington,West Virginia,Wisconsin,Wyoming,District of Columbia,Puerto Rico,Alberta,British Columbia,Manitoba,New Brunswick,Newfoundland,
Newfoundland and Labrador,Nova Scotia,Northwest Territories,Nunavut,Ontario,Prince Edward Island,Quebec,Québec,Saskatchewan,Yukon""".split(
            ","
        )
    }
)
# Names that count only for particular people: rule id -> the key flag that marks them.
FLAGGED_NAMES = {"frcp52": "minor", "pci": "cardholder"}
ACCOUNTS = ["bank_account", "iban", "payment_card", "routing_number"]
ADDRESS = ["street_address", "postal_code", "place"]

# rule set id -> (label, citation, answer-key categories it covers, note on what is left out)
RULES = {
    "frcp52": (
        "Federal court filings",
        "Fed. R. Civ. P. 5.2(a)",
        [
            "ssn",
            "tax_id",
            "date_of_birth",
            "bank_account",
            "iban",
            "payment_card",
        ],
        "Names of minors are also covered by the rule, but the answer keys do not say who is a minor, so names are not scored here.",
    ),
    "irc7216": (
        "Tax return information",
        "26 CFR 301.7216-1",
        [
            "person_name",
            "organization_name",
            *ADDRESS,
            "ssn",
            "tax_id",
            "money_amount",
            *ACCOUNTS,
            "email",
            "phone",
        ],
        "",
    ),
    "glba": (
        "Customer financial information",
        "16 CFR 314.2",
        [
            "person_name",
            "email",
            "phone",
            "street_address",
            "postal_code",
            "ssn",
            "tax_id",
            "money_amount",
            *ACCOUNTS,
        ],
        "Consumer report details have no detector and no answer-key category.",
    ),
    "hipaa": (
        "Health information (18 identifiers)",
        "45 CFR 164.514(b)(2)",
        [
            "person_name",
            *ADDRESS,
            "date_of_birth",
            "date",
            "age_over_89",
            "phone",
            "email",
            "ssn",
            "record_number",
            *ACCOUNTS,
            "government_id",
            "vehicle_id",
            "device_id",
            "url",
            "ip_address",
            "tax_id",
            "indirect_identifier",
        ],
        "Biometrics and photographs do not apply to text. A state or province on its own is not scored: this rule lets it stay.",
    ),
    "ccpa": (
        "California sensitive personal information",
        "Cal. Civ. Code 1798.140(ae)",
        [
            "ssn",
            "government_id",
            "bank_account",
            "iban",
            "payment_card",
            "card_security_code",
            "credential",
            "sensitive_attribute",
            "health_info",
        ],
        "Health and other sensitive attributes are in the rule but have no detector.",
    ),
    "pci": (
        "Payment card data",
        "PCI DSS v4.0.1",
        ["payment_card", "card_expiry", "card_security_code"],
        "Cardholder names are covered by the standard, but the answer keys do not say which names are cardholders.",
    ),
    "gdpr": (
        "EU personal data",
        "GDPR Art. 4, 9, 10",
        [
            "person_name",
            "ssn",
            "tax_id",
            "government_id",
            *ACCOUNTS,
            "record_number",
            *ADDRESS,
            "email",
            "url",
            "ip_address",
            "device_id",
            "credential",
            "indirect_identifier",
            "sensitive_attribute",
            "health_info",
        ],
        "",
    ),
    "nist": (
        "US federal PII guidance",
        "NIST SP 800-122",
        [
            "person_name",
            "ssn",
            "tax_id",
            "government_id",
            "bank_account",
            "iban",
            "payment_card",
            "street_address",
            "postal_code",
            "email",
            "date_of_birth",
            "place",
            "money_amount",
            "health_info",
            "sensitive_attribute",
            "indirect_identifier",
        ],
        "",
    ),
}

keys = {
    p.stem: json.loads(p.read_text())
    for p in sorted((score.CORPUS / "keys").glob("doc-*.json"))
}
rows = []
for rid, (label, cite, cats, note) in RULES.items():
    run = f"{PREFIX}-{rid}"
    if "--skip-run" not in sys.argv:
        subprocess.run(
            [
                sys.executable,
                "-P",
                str(Path(__file__).parent / "run_eval.py"),
                run,
                "--replay",
                SOURCE,
                "--frameworks",
                rid,
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    raw = ROOT / "evaluation/results" / run / "raw"
    tally = {"all": Counter(), "heldout": Counter(), "flag": Counter()}
    by_cat = {}
    for doc, key in keys.items():
        recs, _, _ = score.score_doc(
            key, json.loads((raw / f"{doc}.json").read_text())
        )
        flag = FLAGGED_NAMES.get(rid)
        for it, st in recs:
            wanted = it["category"] in cats or (
                flag and it["category"] == "person_name" and it.get(flag)
            )
            if not wanted or (
                rid == "hipaa"
                and it["category"] == "place"
                and it["value"].strip().rstrip(".") in REGIONS
            ):
                continue
            if flag and it["category"] == "person_name":
                it = dict(it, category=f"{flag}_name")
            # Sensitive topics are flagged for review, not replaced: any highlight on the phrase counts.
            tally["flag"][
                (
                    "caught"
                    if st == "caught"
                    or (st == "partial" and it["category"] in score.WARN)
                    else st
                )
            ] += 1
            tally["all"][st] += 1
            by_cat.setdefault(it["category"], Counter())[st] += 1
            if score.is_heldout(doc):
                tally["heldout"][st] += 1
    rows.append((rid, label, cite, cats, note, tally, by_cat))

pct = lambda c: 100 * c["caught"] / max(sum(c.values()), 1)
rows.sort(key=lambda r: -pct(r[5]["all"]))
out = [
    "# Catch rate by rule set",
    "",
    "Each rule set was run on its own (only its checks switched on) over the 100 fictional documents, and scored",
    "against the kinds of information that rule covers. Names are replayed from the final live model run.",
    '"Caught" means every character of the value was covered. See RESULTS.md for method and limits.',
    "",
    '"Counting flags" also counts a health or other sensitive detail as found when any part of it is underlined for review.',
    "",
    "| Rank | Rule set | Caught | Of | Rate | Counting flags | Held-out part |",
    "|---|---|---|---|---|---|---|",
]
for n, (rid, label, cite, cats, note, tally, by_cat) in enumerate(rows, 1):
    a, h = tally["all"], tally["heldout"]
    out.append(
        f"| {n} | {label} ({cite}) | {a['caught']} | {sum(a.values())} | {pct(a):.1f}% | {pct(tally['flag']):.1f}% | {pct(h):.1f}% |"
    )
out.append("")
for rid, label, cite, cats, note, tally, by_cat in rows:
    out += [f"## {label}", ""]
    if note:
        out += [note, ""]
    out += ["| Kind of information | Caught | Of | Rate |", "|---|---|---|---|"]
    for cat, c in sorted(by_cat.items(), key=lambda kv: -pct(kv[1])):
        out.append(
            f"| {cat.replace('_', ' ')} | {c['caught']} | {sum(c.values())} | {pct(c):.1f}% |"
        )
    out.append("")
(ROOT / "evaluation/results" / OUT).write_text("\n".join(out) + "\n")
print("\n".join(out))
