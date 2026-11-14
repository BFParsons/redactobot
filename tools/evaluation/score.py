# Copyright 2026 The Redactobot Authors
# SPDX-License-Identifier: Apache-2.0

"""Score an evaluation run against the answer keys.

Usage: python3 -P tools/evaluation/score.py RUN_NAME [--split all|dev|heldout] [--misses] [--json]

How scoring works
- Each answer-key item is a sensitive value as written in the document. Every place it appears
  in the text the app extracted is one "occurrence". Longer key values are located first, so
  "Margaret" inside "Margaret Whitfield" is not counted twice.
- An occurrence is CAUGHT when every non-space character of it lies inside a detection,
  PARTLY caught when only some do, MISSED when none do. For names written with a title
  ("Ms. Whitfield") the title itself does not need to be covered.
- An occurrence the key lists but the extracted text does not contain is LOST IN IMPORT and
  counts against the tool.
- The headline is the share of occurrences fully caught. "Core" categories are the 23 the app
  had a detector for when the baseline was run; they are kept fixed so runs can be compared.
  Places, passwords and device IDs gained a simple detector afterwards and are reported on
  their own line. Health details, other sensitive attributes and indirect identifiers have no
  detector and are reported separately.
- Documents are split 70/30 into dev and held-out. Fixes are only ever guided by dev misses;
  held-out shows whether the fixes generalise.
"""

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
import os  # noqa: E402

CORPUS = Path(
    os.environ.get("REDACTOBOT_CORPUS")
    or os.environ.get("CSA_CORPUS")
    or ROOT / "evaluation/corpus"
)
args = sys.argv[1:]
RUN = args[0]
SPLIT = args[args.index("--split") + 1] if "--split" in args else "all"
RAW = ROOT / "evaluation/results" / RUN / "raw"

BUILT = {
    "person_name",
    "organization_name",
    "email",
    "phone",
    "street_address",
    "postal_code",
    "ssn",
    "tax_id",
    "government_id",
    "bank_account",
    "routing_number",
    "iban",
    "payment_card",
    "card_expiry",
    "card_security_code",
    "money_amount",
    "date_of_birth",
    "date",
    "age_over_89",
    "record_number",
    "url",
    "ip_address",
    "vehicle_id",
}
# Categories that had no detector at the baseline and gained a simple one during the fix round.
NEW = {"place", "credential", "device_id"}
# Categories the app flags for review instead of replacing. For these, "flagged" (any part of
# the phrase is highlighted) is the fair measure; "caught" still means every character.
WARN = {"health_info", "sensitive_attribute", "indirect_identifier"}
MODEL_CATEGORIES = {"person_name", "organization_name"}
TITLE = re.compile(
    r"^(?:Mr|Mrs|Ms|Miss|Mx|Dr|Prof|Professor|Hon|Sir|Dame|Judge|Justice|Magistrate|Rev|Reverend|Father|Sister|Pastor|Rabbi|Imam|Sen|Senator|Rep|Atty|Attorney|Officer|Deputy|Trooper|Det|Detective|Sgt|Sergeant|Capt|Captain|Lt|Chief|Nurse|Coach|Doña|Don|Señor|Señora|Mme|Mlle|M|Me|Maître|Lic|Ofc|RN|Sra|Dra|Dre|Herr|Frau|MR|MRS|MS|DR|ms|mr|mrs|dr|ofc|miss)\.?\s+",
    re.I,
)


# A few answer-key values include the label in front of a number ("file LV-2026-0733", "#88214").
# The label itself is not sensitive and need not be covered.
LABELLED = {
    "record_number",
    "bank_account",
    "government_id",
    "tax_id",
    "payment_card",
    "vehicle_id",
    "device_id",
    "place",
}
LABEL_LEAD = re.compile(
    r"^(?:(?:file|case|claim|matter|policy|invoice|account|acct|check|cheque|ref|loan|order|ticket|plate|tag|room|rm|unit|bed)\s+(?:no\.?\s*|#\s*)?|no\.?\s*|#\s*)(?=\S*\d)",
    re.I,
)


def is_heldout(doc_id):
    return int(doc_id.split("-")[1]) % 10 in (3, 6, 9)


def pattern_for(value):
    tokens = value.split()
    body = r"\s+".join(re.escape(t) for t in tokens)
    left = r"(?<![A-Za-z0-9])" if value[:1].isalnum() else ""
    right = r"(?![A-Za-z0-9])" if value[-1:].isalnum() else ""
    return re.compile(left + body + right)


def score_doc(key, result, which="detections", spans=None):
    """Return one record per key occurrence."""
    out = []
    text = result.get("text")
    items = sorted(key["items"], key=lambda i: -len(i["value"]))
    if text is None:  # import failed outright
        for it in items:
            for _ in range(it.get("occurrences", 1)):
                out.append((it, "lost"))
        return out, [], 0
    covered = bytearray(len(text))
    dets = result.get(which, [])
    for d in dets:
        for i in range(d["start"], d["end"]):
            covered[i] = 1
    claimed = bytearray(len(text))
    truth = bytearray(len(text))
    for it in items:
        found = 0
        for m in pattern_for(it["value"]).finditer(text):
            s, e = m.span()
            if any(claimed[s:e]):
                continue
            for i in range(s, e):
                claimed[i] = 1
                truth[i] = 1
            found += 1
            cs = s
            if it["category"] == "person_name":
                t = TITLE.match(text[s:e])
                if t:
                    cs = s + t.end()
            elif it["category"] in LABELLED:
                t = LABEL_LEAD.match(text[s:e])
                if t:
                    cs = s + t.end()
            ce = e
            if it["category"] in MODEL_CATEGORIES and re.search(
                r"['’]s$", text[s:e]
            ):
                ce = (
                    e - 2
                )  # "Peggy's": the possessive ending is not part of the name
            chars = [i for i in range(cs, ce) if text[i].isalnum()] or [
                i for i in range(cs, ce) if not text[i].isspace()
            ]
            hit = sum(covered[i] for i in chars)
            if (
                hit
                and hit < len(chars)
                and it["category"] in ("place", "street_address")
            ):
                # "Culebra Rd and N. Zarzamora St", "Route 66 near Fanning Drive": the joining word names nothing
                left = "".join(
                    text[i] if (i in set(chars) and not covered[i]) else " "
                    for i in range(cs, ce)
                ).split()
                if all(
                    w.lower() in ("and", "near", "at", "off", "by", "of", "the")
                    for w in left
                ):
                    hit = len(chars)
            out.append(
                (
                    it,
                    (
                        "caught"
                        if hit == len(chars)
                        else "partial" if hit else "missed"
                    ),
                )
            )
            if spans is not None:
                spans.append((s, e))
        for _ in range(max(0, it.get("occurrences", 1) - found)):
            out.append((it, "lost"))
            if spans is not None:
                spans.append(None)
    # Detections that touch no key value at all: over-redaction.
    extra = [d for d in dets if not any(truth[d["start"] : d["end"]])]
    distractor_hits = sum(
        1
        for d in extra
        if any(
            pattern_for(x).search(d["text"]) or d["text"] in x
            for x in key.get("distractors", [])
        )
    )
    return out, extra, distractor_hits


def pct(n, d):
    return f"{100 * n / d:5.1f}%" if d else "   n/a"


def main():
    keys = {
        p.stem: json.loads(p.read_text())
        for p in sorted((CORPUS / "keys").glob("doc-*.json"))
    }
    ids = [
        i
        for i in keys
        if SPLIT == "all" or (SPLIT == "heldout") == is_heldout(i)
    ]
    missing = [i for i in ids if not (RAW / f"{i}.json").exists()]
    ids = [i for i in ids if i not in missing]

    rows, rows_pattern, extras = [], [], []
    import_failures, chunk_errors, chunks, model_seconds = [], 0, 0, 0.0
    for i in ids:
        result = json.loads((RAW / f"{i}.json").read_text())
        if result.get("importError") or result.get("harnessError"):
            import_failures.append(
                (i, result.get("importError") or result.get("harnessError"))
            )
        chunk_errors += result.get("chunkErrors") or 0
        chunks += result.get("chunks") or 0
        model_seconds += (result.get("modelMs") or 0) / 1000
        recs, extra, _ = score_doc(keys[i], result)
        rows += [(i, it, st) for it, st in recs]
        extras += [(i, d) for d in extra]
        recs_p, _, _ = score_doc(keys[i], result, "patternOnly")
        rows_pattern += [(i, it, st) for it, st in recs_p]

    def tally(rs, pred=lambda it: True):
        c = Counter(st for _, it, st in rs if pred(it))
        return c["caught"], sum(c.values()), c

    report = {
        "run": RUN,
        "split": SPLIT,
        "documents": len(ids),
        "not_run": missing,
        "import_failures": import_failures,
        "chunks": chunks,
        "chunk_errors": chunk_errors,
        "model_seconds": round(model_seconds),
    }
    lines = []
    w = lines.append
    w(f"# Evaluation: run `{RUN}`, split `{SPLIT}`")
    w("")
    w(
        f"{len(ids)} documents, {len(rows)} occurrences of sensitive values in the answer keys."
        + (f" {len(missing)} documents not run." if missing else "")
    )
    w("")
    built = lambda it: it["category"] in BUILT
    c_all, n_all, _ = tally(rows)
    c_b, n_b, cb = tally(rows, built)
    c_nb, n_nb, _ = tally(rows, lambda it: not built(it))
    c_pb, n_pb, _ = tally(rows_pattern, built)
    report.update(
        caught_all=c_all,
        total_all=n_all,
        caught_built=c_b,
        total_built=n_b,
        caught_not_built=c_nb,
        total_not_built=n_nb,
        caught_built_pattern_only=c_pb,
    )
    w("| Measure | Caught | Of | Rate |")
    w("|---|---|---|---|")
    w(
        f"| Everything in the answer keys | {c_all} | {n_all} | {pct(c_all, n_all)} |"
    )
    c_new, n_new, _ = tally(rows, lambda it: it["category"] in NEW)
    c_none, n_none, _ = tally(
        rows, lambda it: not built(it) and it["category"] not in NEW
    )
    report.update(
        caught_new=c_new, total_new=n_new, caught_none=c_none, total_none=n_none
    )
    w(
        f"| Core categories (23 with a detector at baseline) | {c_b} | {n_b} | {pct(c_b, n_b)} |"
    )
    w(
        f"| Same, with the on-device model switched off (code only) | {c_pb} | {n_pb} | {pct(c_pb, n_pb)} |"
    )
    w(
        f"| Places, passwords, device IDs (simple detector added after baseline) | {c_new} | {n_new} | {pct(c_new, n_new)} |"
    )
    w(
        f"| Health details, sensitive attributes, indirect identifiers: fully covered | {c_none} | {n_none} | {pct(c_none, n_none)} |"
    )
    _, _, cw = tally(rows, lambda it: it["category"] in WARN)
    flagged = cw["caught"] + cw["partial"]
    report.update(flagged_warn=flagged)
    w(
        f"| Same three, flagged for review (any part highlighted) | {flagged} | {n_none} | {pct(flagged, n_none)} |"
    )
    w("")
    w(
        f"Within core categories: {cb['partial']} partly caught, {cb['missed']} missed, {cb['lost']} lost in import."
    )
    w(
        f"Model: {chunks} chunks, {chunk_errors} failed after one retry, {round(model_seconds / 60, 1)} minutes of model time."
    )
    if import_failures:
        w(
            f"Import failures: {len(import_failures)} documents: "
            + "; ".join(f"{i}: {m}" for i, m in import_failures)
        )
    w("")

    def table(title, keyfn, rs=rows, pred=lambda it: True, order=None):
        groups = defaultdict(Counter)
        for i, it, st in rs:
            if pred(it):
                groups[keyfn(i, it)][st] += 1
        w(f"## {title}")
        w("")
        w("| | Caught | Partly | Missed | Lost in import | Total | Rate |")
        w("|---|---|---|---|---|---|---|")
        names = order or sorted(
            groups, key=lambda g: (-(sum(groups[g].values())), str(g))
        )
        table_data = {}
        for g in names:
            c = groups[g]
            n = sum(c.values())
            w(
                f"| {g} | {c['caught']} | {c['partial']} | {c['missed']} | {c['lost']} | {n} | {pct(c['caught'], n)} |"
            )
            table_data[str(g)] = dict(
                caught=c["caught"],
                partial=c["partial"],
                missed=c["missed"],
                lost=c["lost"],
                total=n,
            )
        w("")
        return table_data

    report["by_category"] = table(
        "By category",
        lambda i, it: it["category"]
        + (
            ""
            if built(it)
            else (
                " (added after baseline)"
                if it["category"] in NEW
                else " (flag only)"
            )
        ),
    )
    report["by_difficulty"] = table(
        "By difficulty (core categories)",
        lambda i, it: it.get("difficulty", "standard"),
        pred=built,
    )
    report["by_variant"] = table(
        "Names by written form",
        lambda i, it: it.get("variant", "n/a"),
        pred=lambda it: it["category"] in MODEL_CATEGORIES,
    )
    report["by_format"] = table(
        "By file format (core categories)",
        lambda i, it: keys[i].get("format", "?"),
        pred=built,
    )
    report["by_audience"] = table(
        "By audience (core categories)",
        lambda i, it: keys[i].get("audience", "?"),
        pred=built,
    )

    # Over-redaction
    FLAG_KINDS = {
        "health",
        "sensitive",
        "indirect",
    }  # highlighted for review, never replaced by default
    flags_extra = [(i, d) for i, d in extras if d["kind"] in FLAG_KINDS]
    extras = [(i, d) for i, d in extras if d["kind"] not in FLAG_KINDS]
    by_kind = Counter(d["kind"] for _, d in extras)
    all_dets = [
        d
        for i in ids
        for d in json.loads((RAW / f"{i}.json").read_text()).get(
            "detections", []
        )
    ]
    total_flags = sum(1 for d in all_dets if d["kind"] in FLAG_KINDS)
    total_dets = len(all_dets) - total_flags
    report.update(
        detections=total_dets,
        extra_detections=len(extras),
        flags=total_flags,
        extra_flags=len(flags_extra),
    )
    w("## Over-redaction")
    w("")
    w(
        f"{len(extras)} of {total_dets} replacements ({pct(len(extras), total_dets).strip()}) touched nothing in the answer key. "
        "These would be replaced unnecessarily (the user can untick them, and the value is restored afterwards)."
    )
    if total_flags:
        w("")
        w(
            f"Separately, {len(flags_extra)} of {total_flags} sensitive-topic flags ({pct(len(flags_extra), total_flags).strip()}) "
            "touched nothing in the answer key. Flags only underline text; nothing is replaced."
        )
    w("")
    w("| Detector | Extra detections |")
    w("|---|---|")
    for k, n in by_kind.most_common(12):
        w(f"| {k} | {n} |")
    w("")

    if "--misses" in args:
        w("## What was missed (core categories)")
        w("")
        sub = defaultdict(lambda: [0, 0, []])
        for i, it, st in rows:
            if not built(it):
                continue
            k = (it["category"], it.get("subtype", ""))
            sub[k][1] += 1
            if st != "caught":
                sub[k][0] += 1
                if len(sub[k][2]) < 4:
                    sub[k][2].append(f"`{it['value']}` ({st}, {i})")
        w("| Category | Subtype | Not caught | Of | Examples |")
        w("|---|---|---|---|---|")
        for (cat, st), (m, n, ex) in sorted(
            sub.items(), key=lambda kv: -kv[1][0]
        ):
            if m:
                w(f"| {cat} | {st} | {m} | {n} | {'; '.join(ex)} |")
        w("")
        w("### Most common extra detections")
        w("")
        for (kind, text), n in Counter(
            (d["kind"], d["text"]) for _, d in extras
        ).most_common(40):
            w(f"- {kind}: `{text}` ×{n}")
        w("")

    out_dir = RAW.parent
    suffix = "" if SPLIT == "all" else f"-{SPLIT}"
    (out_dir / f"report{suffix}.md").write_text("\n".join(lines) + "\n")
    (out_dir / f"summary{suffix}.json").write_text(json.dumps(report, indent=1))
    print(
        "\n".join(lines)
        if "--json" not in args
        else json.dumps(report, indent=1)
    )


if __name__ == "__main__":
    main()
