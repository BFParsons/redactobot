# Copyright 2026 B Parsons
# SPDX-License-Identifier: Apache-2.0

"""Score the desktop corpus without passing any answer-key data into detection.

Usage: python tools/evaluation/score_desktop.py RUN_DIRECTORY
Scores exact annotated occurrences, complete significant-character removal, category
agreement, extra redacted characters and document-level residual identifiers. A held
document is counted separately from successful removal. Writes local-only audit files.
"""

import csv
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

KINDS = {
    "NAME": {"person", "company"},
    "ADDRESS": {"street", "places", "region", "zip", "postal_ca"},
    "CREDIT_CARD": {"card", "card_partial"},
    "MRN": {"record"},
    "HEALTH_ID": {"record", "government_id", "passport_dl"},
    "EMAIL": {"email"},
    "PHONE": {"phone"},
    "DOB": {"dob", "date"},
    "ACCOUNT": {"account", "iban"},
    "DRIVERS_LICENSE": {"passport_dl", "government_id"},
    "PASSPORT": {"passport_dl", "government_id"},
    "SIN": {"sin_ca"},
    "SSN": {"ssn"},
    "LICENSE_PLATE": {"vin"},
    "IP_ADDRESS": {"ip"},
}
# Some key entries include the field's generic printed label. Keep strict phrase
# coverage as a second metric, but do not mistake a surviving label for a leaked ID.
LABELS = {
    "MRN": r"(?:medical\s+record|chart|mrn|patient\s+id)(?:\s*(?:number|no\.?|id|#|:))*\s*",
    "HEALTH_ID": r"(?:health\s*(?:card|id|number)|phn|ohip|hin|nhs)(?:\s*(?:number|no\.?|id|#|:))*\s*",
    "DRIVERS_LICENSE": r"(?:(?:driver['’]?s?\s+)?licen[cs]e|dl)(?:\s*(?:number|no\.?|id|#|:))*\s*",
    "LICENSE_PLATE": r"(?:licen[cs]e\s+plate|plate|registration)(?:\s*(?:number|no\.?|id|#|:))*\s*",
    "ACCOUNT": r"(?:bank\s+account|account|acct)(?:\s*(?:number|no\.?|id|#|:))*\s*",
    "SSN": r"(?:ssn|social\s+security)(?:\s*(?:number|no\.?|id|#|:))*\s*",
    "SIN": r"(?:sin|social\s+insurance)(?:\s*(?:number|no\.?|id|#|:))*\s*",
    "PASSPORT": r"passport(?:\s*(?:number|no\.?|id|#|:))*\s*",
}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def pattern(value):
    body = r"\s+".join(re.escape(part) for part in value.split())
    return re.compile(
        (r"(?<!\w)" if value[:1].isalnum() else "")
        + body
        + (r"(?!\w)" if value[-1:].isalnum() else "")
    )


def offsets(text):
    """JavaScript UTF-16 offsets -> Python code-point offsets, including emoji."""
    result = [0]
    for index, char in enumerate(text):
        if ord(char) > 0xFFFF:
            result.append(index)
        result.append(index + 1)
    return result


def percentile(values, q):
    if not values:
        return None
    ordered = sorted(values)
    return round(ordered[min(len(ordered) - 1, int((len(ordered) - 1) * q))], 2)


def score(run):
    manifest = read(run / "manifest.json")
    corpus = Path(manifest["corpus"])
    answer_path = run / "answerkey.csv"
    if (
        hashlib.sha256(answer_path.read_bytes()).hexdigest()
        != manifest["answerkeySha256"]
    ):
        raise ValueError("Saved answer key changed")
    with answer_path.open(encoding="utf-8-sig", newline="") as source:
        rows = list(csv.DictReader(source))
    expected = defaultdict(list)
    for row_number, row in enumerate(rows, 2):
        row["row"] = row_number
        expected[row["file"]].append(row)
    files = {file["name"]: file for file in manifest["files"]}
    missing_files = sorted(set(expected) - set(files))
    key_errors = []
    results = {}
    audit = []
    for mode in ("local", "nano"):
        counts = defaultdict(Counter)
        documents = Counter()
        times = []
        network_attempts = 0
        per_file = []
        for name, file in files.items():
            items = sorted(
                expected.get(name, []), key=lambda row: int(row["start_char"])
            )
            if "importError" in file:
                documents["import_failed"] += 1
                for row in items:
                    counts[row["pii_type"]]["import_lost"] += 1
                    counts[row["pii_type"]]["total"] += 1
                continue
            local = read(run / "local" / f"{file['index']}.json")
            result_path = run / mode / f"{file['index']}.json"
            if not result_path.exists():
                documents["pending"] += 1
                continue
            result = local if mode == "local" else read(result_path)
            text = local["text"]
            ds = (
                result["findings"]
                if mode == "local"
                else result["report"]["findings"]
            )
            ds = [d for d in ds if d.get("enabled", True)]
            offset_map = offsets(text)
            covered = [False] * len(text)
            mandatory = [False] * len(text)
            kinds = [set() for _ in text]
            for d in ds:
                start, end = offset_map[d["start"]], offset_map[d["end"]]
                if text[start:end] != d["text"]:
                    raise ValueError("Detection offset mismatch")
                for i in range(start, end):
                    covered[i] = True
                    if mode == "local" or d.get("bucket") == "local-only":
                        mandatory[i] = True
                    kinds[i].add(d["kind"])
            annotated = [False] * len(text)
            assigned = Counter()
            document_counts = Counter()
            mandatory_counts = Counter()
            raw = (corpus / name).read_text(encoding="utf-8-sig")
            for row in items:
                value, category = row["text"], row["pii_type"]
                raw_start, raw_end = int(row["start_char"]), int(
                    row["end_char"]
                )
                if mode == "local" and raw[raw_start:raw_end] != value:
                    key_errors.append(
                        {
                            "file": name,
                            "row": row["row"],
                            "issue": "source offsets do not match annotated text",
                        }
                    )
                matches = list(pattern(value).finditer(text))
                identity = (category, value)
                occurrence = assigned[identity]
                assigned[identity] += 1
                if occurrence >= len(matches):
                    state, correct, start, end = (
                        "import_lost",
                        False,
                        None,
                        None,
                    )
                    identity_state = "import_lost"
                else:
                    start, end = matches[occurrence].span()
                    significant = [
                        i for i in range(start, end) if text[i].isalnum()
                    ]
                    if not significant:
                        significant = [
                            i
                            for i in range(start, end)
                            if not text[i].isspace()
                        ]
                    counts[category]["strict_phrase_full"] += int(
                        all(covered[i] for i in significant)
                    )
                    label = re.match(
                        r"^" + LABELS.get(category, r"(?!)"),
                        text[start:end],
                        re.I,
                    )
                    value_start = start
                    if (
                        label
                        and label.end()
                        and not text[start + label.end() - 1].isalnum()
                        and any(
                            char.isdigit()
                            for char in text[start + label.end() : end]
                        )
                    ):
                        value_start += label.end()
                        significant = [
                            i for i in significant if i >= value_start
                        ]
                    for i in range(start, end):
                        annotated[i] = True
                    caught = sum(covered[i] for i in significant)
                    state = (
                        "full"
                        if caught == len(significant)
                        else "partial" if caught else "missed"
                    )
                    protected = sum(mandatory[i] for i in significant)
                    identity_state = (
                        "full"
                        if protected == len(significant)
                        else "partial" if protected else "missed"
                    )
                    correct = state == "full" and all(
                        kinds[i] & KINDS.get(category, set())
                        for i in significant
                    )
                counts[category][state] += 1
                counts[category]["category_correct"] += int(correct)
                counts[category]["total"] += 1
                counts[category]["mandatory_identity_full"] += int(
                    identity_state == "full"
                )
                document_counts[state] += 1
                mandatory_counts[identity_state] += 1
                if state != "full" or not correct:
                    audit.append(
                        {
                            "mode": mode,
                            "file": name,
                            "row": row["row"],
                            "category": category,
                            "value": value,
                            "state": state,
                            "category_correct": correct,
                            "start": start,
                            "end": end,
                            "overlapping": [
                                {"kind": d["kind"], "text": d["text"]}
                                for d in ds
                                if start is not None
                                and offset_map[d["start"]] < end
                                and offset_map[d["end"]] > start
                            ],
                        }
                    )
            documents["scored"] += 1
            if items and not any(
                document_counts[state]
                for state in ("partial", "missed", "import_lost")
            ):
                documents["zero_residual_annotated_identifiers"] += 1
            if items and not any(
                mandatory_counts[state]
                for state in ("partial", "missed", "import_lost")
            ):
                documents["zero_residual_in_identity_preview"] += 1
            if not items:
                documents["unannotated_documents"] += 1
            documents["extra_redacted_alphanumeric_chars"] += sum(
                covered[i] and not annotated[i] and char.isalnum()
                for i, char in enumerate(text)
            )
            documents["unannotated_alphanumeric_chars"] += sum(
                not annotated[i] and char.isalnum()
                for i, char in enumerate(text)
            )
            if mode == "nano":
                documents[result["gate"]] += 1
                documents["incomplete"] += int(not result["report"]["complete"])
                network_attempts += result.get("blockedNetworkAttempts", 0)
                if result["gate"] == "eligible" and any(
                    mandatory_counts[s]
                    for s in ("partial", "missed", "import_lost")
                ):
                    documents["eligible_with_residual_identifier"] += 1
            times.append(result["elapsedMs"])
            per_file.append(
                {
                    "file": name,
                    **document_counts,
                    "ms": round(result["elapsedMs"], 2),
                    **({"gate": result["gate"]} if mode == "nano" else {}),
                }
            )
        totals = Counter()
        for category, count in counts.items():
            totals.update(count)
            count["full_removal_percent"] = (
                round(100 * count["full"] / count["total"], 2)
                if count["total"]
                else 0
            )
            count["category_correct_percent"] = (
                round(100 * count["category_correct"] / count["total"], 2)
                if count["total"]
                else 0
            )
        results[mode] = {
            "categories": dict(counts),
            "totals": dict(totals),
            "documents": dict(documents),
            "timing_ms": {
                "median": percentile(times, 0.5),
                "p95": percentile(times, 0.95),
                "total": round(sum(times), 2),
            },
            "blocked_network_attempts": network_attempts,
        }
        (run / f"{mode}-file-scores.json").write_text(
            json.dumps(per_file, indent=2), encoding="utf-8"
        )
    summary = {
        "answer_key_rows": len(rows),
        "answer_key_categories": sorted({row["pii_type"] for row in rows}),
        "missing_files": missing_files,
        "key_offset_errors": key_errors,
        "results": results,
        "limitations": [
            "The answer key does not label places independently; ADDRESS measures whole-address coverage.",
            "Full removal excludes known generic ID labels; strict_phrase_full includes them.",
            "mandatory_identity_full counts only details removed before cloud cleanup, not facts assigned to cloud cleanup.",
            "Extra redacted characters are an audit proxy, not verified false positives: the key may omit sensitive material.",
            "The local pass excludes Nano and is not considered a completed privacy approval.",
            "A review hold is reported separately from full removal.",
        ],
    }
    (run / "scores.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    (run / "audit.json").write_text(
        json.dumps(audit, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(
        json.dumps({**summary, "key_offset_errors": len(key_errors)}, indent=2)
    )
    return summary


if __name__ == "__main__":
    score(Path(sys.argv[1]))
