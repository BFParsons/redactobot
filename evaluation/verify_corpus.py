#!/usr/bin/env python3
# Copyright 2026 B Parsons
# SPDX-License-Identifier: Apache-2.0

"""Self-check for the test corpus answer keys. Does NOT use the tool under test.

Run:  python3 -P eval/verify_corpus.py [--corpus DIR]

For every key item it re-reads the document that was actually written,
extracts its visible text with a format-appropriate reader, normalises
whitespace, and confirms the value appears exactly `occurrences` times as a
standalone token sequence (longer key values are found and masked first, so
"Margaret" inside "Margaret Whitfield" is not counted for "Margaret").
It also checks the key schema, that every distractor is present, that the
checksummed numbers are valid, and that the manifest matches the keys.
Exits non-zero and lists every mismatch.
"""

import argparse
import datetime
import email
import glob
import html.parser
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SEP = " \u00a6 "

CATEGORIES = {
    "person_name",
    "organization_name",
    "email",
    "phone",
    "street_address",
    "postal_code",
    "place",
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
    "device_id",
    "credential",
    "health_info",
    "sensitive_attribute",
    "indirect_identifier",
}
VARIANTS = {
    "full",
    "short",
    "initials",
    "first-name",
    "surname",
    "title-surname",
    "acronym",
    "caps",
    "last-first",
    "nickname",
    "n/a",
}
ITEM_FIELDS = [
    "value",
    "category",
    "subtype",
    "occurrences",
    "entity",
    "canonical",
    "variant",
    "difficulty",
    "why",
]
KEY_FIELDS = [
    "id",
    "file",
    "format",
    "title",
    "doc_type",
    "audience",
    "jurisdiction",
    "word_count",
    "items",
    "distractors",
]


# ---------------------------------------------------------- text readers


def read_plain(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def read_eml(path):
    with open(path, "rb") as f:
        msg = email.message_from_bytes(f.read())
    parts = []
    for h in ("From", "To", "Cc", "Bcc", "Reply-To", "Subject", "Date"):
        for v in msg.get_all(h, []):
            parts.append("%s: %s" % (h, v))
    body = None
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            body = part.get_payload(decode=True).decode(
                part.get_content_charset() or "utf-8"
            )
            break
    if body is None:
        raise ValueError("no text/plain part")
    return "\n".join(parts) + "\n\n" + body


class _Visible(html.parser.HTMLParser):
    BLOCK = {
        "p",
        "div",
        "h1",
        "h2",
        "h3",
        "h4",
        "li",
        "tr",
        "table",
        "ul",
        "ol",
        "br",
        "hr",
        "section",
        "main",
        "header",
        "footer",
        "dl",
        "dt",
        "dd",
        "blockquote",
        "pre",
    }

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "head", "template"):
            self.skip += 1
        elif tag in self.BLOCK:
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "head", "template"):
            self.skip -= 1
        elif tag in ("td", "th"):
            self.out.append(SEP)
        elif tag in self.BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def read_html(path):
    p = _Visible()
    p.feed(read_plain(path))
    p.close()
    return "".join(p.out)


def read_docx(path):
    import docx
    from docx.table import Table
    from docx.text.paragraph import Paragraph

    d = docx.Document(path)
    out = []
    for el in d.element.body.iterchildren():
        if el.tag.endswith("}p"):
            out.append(Paragraph(el, d).text)
        elif el.tag.endswith("}tbl"):
            for row in Table(el, d).rows:
                out.append(SEP.join(c.text for c in row.cells))
    for s in d.sections:
        for part in (s.header, s.footer):
            for p in part.paragraphs:
                out.append(p.text)
    return "\n".join(out)


def read_pptx(path):
    from pptx import Presentation

    out = []
    for slide in Presentation(path).slides:
        for sh in slide.shapes:
            if sh.has_text_frame:
                for p in sh.text_frame.paragraphs:
                    out.append("".join(r.text for r in p.runs))
            if getattr(sh, "has_table", False) and sh.has_table:
                for row in sh.table.rows:
                    out.append(SEP.join(c.text for c in row.cells))
        if slide.has_notes_slide:
            out.append(slide.notes_slide.notes_text_frame.text)
    return "\n".join(out)


def _split_sections(code):
    secs, cur, q, i = [], "", False, 0
    while i < len(code):
        ch = code[i]
        if ch == '"':
            q = not q
            cur += ch
        elif ch == "\\" and not q:
            cur += code[i : i + 2]
            i += 1
        elif ch == ";" and not q:
            secs.append(cur)
            cur = ""
        else:
            cur += ch
        i += 1
    secs.append(cur)
    return secs


def fmt_number(v, code):
    """Render a number the way a spreadsheet shows it for the given format code."""
    if code in (None, "General"):
        if isinstance(v, float) and v == int(v):
            return str(int(v))
        return str(v)
    secs = _split_sections(code)
    neg = v < 0
    if neg and len(secs) > 1:
        sec, sign = secs[1], ""
    else:
        sec, sign = secs[0], ("-" if neg else "")
    before, after, numpat, i = "", "", "", 0
    while i < len(sec):
        ch = sec[i]
        lit = None
        if ch == '"':
            j = sec.index('"', i + 1)
            lit = sec[i + 1 : j]
            i = j + 1
        elif ch == "\\":
            lit = sec[i + 1]
            i += 2
        elif ch in "_*":
            i += 2
            continue
        elif ch == "[":
            i = sec.index("]", i) + 1
            continue
        elif ch in "#0,.?":
            numpat += ch
            i += 1
            continue
        else:
            lit = ch
            i += 1
        if numpat:
            after += lit
        else:
            before += lit
    dec = len(numpat.split(".", 1)[1]) if "." in numpat else 0
    body = ("{:,.%df}" if "," in numpat else "{:.%df}") % dec
    return sign + before + body.format(abs(v)) + after


_MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def fmt_date(v, code):
    def rep(m):
        t = m.group(0)
        if t.startswith('"'):
            return t[1:-1]
        if t.startswith("\\"):
            return t[1]
        return {
            "yyyy": "%04d" % v.year,
            "yy": "%02d" % (v.year % 100),
            "mmmm": _MONTHS[v.month - 1],
            "mmm": _MONTHS[v.month - 1][:3],
            "mm": "%02d" % v.month,
            "m": str(v.month),
            "dd": "%02d" % v.day,
            "d": str(v.day),
        }.get(t, t)

    return re.sub(r'"[^"]*"|\\.|yyyy|yy|mmmm|mmm|mm|m|dd|d', rep, code)


def read_xlsx(path):
    import openpyxl

    wb = openpyxl.load_workbook(path)
    out = []
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            shown = []
            for c in row:
                v = c.value
                if v is None or v == "":
                    continue
                if isinstance(v, (datetime.datetime, datetime.date)):
                    shown.append(fmt_date(v, c.number_format))
                elif isinstance(v, bool):
                    shown.append(str(v).upper())
                elif isinstance(v, (int, float)):
                    shown.append(fmt_number(v, c.number_format))
                else:
                    shown.append(str(v))
            if shown:
                out.append(SEP.join(shown))
    return "\n".join(out)


def read_pdf(path):
    r = subprocess.run(
        ["pdftotext", "-layout", "-enc", "UTF-8", path, "-"],
        capture_output=True,
        timeout=120,
    )
    if r.returncode != 0:
        raise ValueError(
            "pdftotext failed: %s" % r.stderr.decode("utf-8", "replace")[:200]
        )
    return r.stdout.decode("utf-8")


def _strip_rtf(src):
    out, i, depth, skip_depth = [], 0, 0, None
    n = len(src)
    while i < n:
        ch = src[i]
        if ch == "{":
            depth += 1
            if (
                src.startswith("{\\fonttbl", i)
                or src.startswith("{\\colortbl", i)
                or src.startswith("{\\stylesheet", i)
                or src.startswith("{\\info", i)
                or src.startswith("{\\*", i)
            ):
                if skip_depth is None:
                    skip_depth = depth
            i += 1
        elif ch == "}":
            if skip_depth is not None and depth == skip_depth:
                skip_depth = None
            depth -= 1
            i += 1
        elif ch == "\\":
            nx = src[i + 1] if i + 1 < n else ""
            if nx in "\\{}":
                if skip_depth is None:
                    out.append(nx)
                i += 2
            elif nx == "'":
                if skip_depth is None:
                    out.append(
                        bytes([int(src[i + 2 : i + 4], 16)]).decode("cp1252")
                    )
                i += 4
            else:
                m = re.match(r"\\([a-zA-Z]+)(-?\d+)? ?", src[i:])
                if not m:
                    i += 2
                    continue
                word, arg = m.group(1), m.group(2)
                i += m.end()
                if skip_depth is not None:
                    continue
                if word in ("par", "line", "row", "page"):
                    out.append("\n")
                elif word in ("tab", "cell"):
                    out.append("\t")
                elif word == "bullet":
                    out.append("\u2022")
                elif word == "u" and arg is not None:
                    cp = int(arg)
                    out.append(chr(cp + 65536 if cp < 0 else cp))
                    if i < n and src[i] == "?":
                        i += 1
        elif ch in "\r\n":
            i += 1
        else:
            if skip_depth is None:
                out.append(ch)
            i += 1
    return "".join(out)


_RTF_CACHE = {}


def convert_rtfs(paths):
    """Convert all RTFs with LibreOffice in one go; fall back to a plain stripper."""
    if not paths or not shutil.which("soffice"):
        return
    tmp = tempfile.mkdtemp(prefix="csai_verify_")
    try:
        subprocess.run(
            [
                "soffice",
                "--headless",
                "-env:UserInstallation=file://%s/profile" % tmp,
                "--convert-to",
                "txt:Text (encoded):UTF8",
                "--outdir",
                tmp,
            ]
            + paths,
            capture_output=True,
            timeout=600,
        )
        for p in paths:
            t = os.path.join(
                tmp, os.path.splitext(os.path.basename(p))[0] + ".txt"
            )
            if os.path.exists(t):
                with open(t, encoding="utf-8-sig") as f:
                    _RTF_CACHE[p] = f.read()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def read_rtf(path):
    if path in _RTF_CACHE:
        return _RTF_CACHE[path]
    with open(path, encoding="ascii") as f:
        return _strip_rtf(f.read())


READERS = {
    "txt": read_plain,
    "md": read_plain,
    "csv": read_plain,
    "eml": read_eml,
    "html": read_html,
    "docx": read_docx,
    "pptx": read_pptx,
    "xlsx": read_xlsx,
    "pdf": read_pdf,
    "rtf": read_rtf,
}


# ------------------------------------------------------------- counting


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def boundary_ok(text, i, j, v):
    if v[0].isalnum() and i > 0:
        p = text[i - 1]
        if p.isalnum():
            return False
        if v[0].isdigit() and p in ".," and i > 1 and text[i - 2].isdigit():
            return False
    if v[-1].isalnum() and j < len(text):
        q = text[j]
        if q.isalnum():
            return False
        if (
            v[-1].isdigit()
            and q in ".,"
            and j + 1 < len(text)
            and text[j + 1].isdigit()
        ):
            return False
    return True


def count_all(text, values):
    """text is normalised. Longest value first; matched spans are masked."""
    taken = bytearray(len(text))
    counts = {}
    for v in sorted(set(values), key=lambda s: (-len(norm(s)), s)):
        nv = norm(v)
        n, pos = 0, 0
        while nv:
            i = text.find(nv, pos)
            if i < 0:
                break
            j = i + len(nv)
            if not any(taken[i:j]) and boundary_ok(text, i, j, nv):
                n += 1
                for k in range(i, j):
                    taken[k] = 1
                pos = j
            else:
                pos = i + 1
        counts[v] = n
    return counts


# ----------------------------------------------------- checksum checks


def luhn(d):
    t = 0
    for k, ch in enumerate(reversed(d)):
        x = int(ch)
        if k % 2:
            x = x * 2 - 9 if x * 2 > 9 else x * 2
        t += x
    return t % 10 == 0


def structural(it):
    v, cat = it["value"], it["category"]
    d = re.sub(r"\D", "", v)
    masked = bool(re.search(r"[xX*\u2022#]", v))
    if cat == "payment_card" and len(d) >= 13 and not masked and not luhn(d):
        return "card number fails Luhn"
    if cat == "iban":
        s = re.sub(r"\s", "", v).upper()
        r = s[4:] + s[:4]
        if (
            not re.fullmatch(r"[A-Z0-9]+", s)
            or int("".join(str(int(c, 36)) for c in r)) % 97 != 1
        ):
            return "IBAN fails mod-97"
    if cat == "routing_number" and len(d) == 9:
        x = [int(c) for c in d]
        if (
            3 * (x[0] + x[3] + x[6])
            + 7 * (x[1] + x[4] + x[7])
            + x[2]
            + x[5]
            + x[8]
        ) % 10:
            return "routing number fails ABA checksum"
    if cat == "ssn" and len(d) == 9 and not masked:
        if (
            d[:3] in ("000", "666")
            or d[0] == "9"
            or d[3:5] == "00"
            or d[5:] == "0000"
        ):
            return "SSN structurally implausible"
    if cat in ("email", "url") and "example" not in v.lower():
        return "not a reserved example domain"
    return None


# ------------------------------------------------------------------ main


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=os.path.join(HERE, "corpus"))
    a = ap.parse_args()
    corpus = os.path.abspath(a.corpus)
    key_paths = sorted(glob.glob(os.path.join(corpus, "keys", "doc-*.json")))
    problems = []
    keys = []
    for kp in key_paths:
        with open(kp, encoding="utf-8") as f:
            keys.append(json.load(f))
    convert_rtfs(
        [
            os.path.join(corpus, k["file"])
            for k in keys
            if k.get("format") == "rtf"
        ]
    )

    n_items = 0
    for key in keys:
        did = key.get("id", "?")
        for fld in KEY_FIELDS:
            if fld not in key:
                problems.append("%s: key missing field %s" % (did, fld))
        path = os.path.join(corpus, key["file"])
        if not os.path.exists(path):
            problems.append(
                "%s: document file missing: %s" % (did, key["file"])
            )
            continue
        if not os.path.exists(os.path.join(corpus, "keys", did + ".md")):
            problems.append("%s: human-readable key (.md) missing" % did)
        try:
            text = norm(READERS[key["format"]](path))
        except Exception as e:
            problems.append(
                "%s: cannot read document: %s: %s" % (did, type(e).__name__, e)
            )
            continue
        values = [it["value"] for it in key["items"]]
        if len(set(values)) != len(values):
            problems.append("%s: duplicate values in key" % did)
        counts = count_all(text, values)
        for it in key["items"]:
            n_items += 1
            for fld in ITEM_FIELDS:
                if fld not in it:
                    problems.append(
                        "%s: item %r missing field %s"
                        % (did, it.get("value"), fld)
                    )
            if it["category"] not in CATEGORIES:
                problems.append(
                    "%s: item %r has unknown category %r"
                    % (did, it["value"], it["category"])
                )
            if it["variant"] not in VARIANTS:
                problems.append(
                    "%s: item %r has unknown variant %r"
                    % (did, it["value"], it["variant"])
                )
            if it["difficulty"] not in ("standard", "hard"):
                problems.append(
                    "%s: item %r has bad difficulty" % (did, it["value"])
                )
            if it["category"] in ("person_name", "organization_name"):
                if (
                    not it["entity"]
                    or not it["canonical"]
                    or it["variant"] == "n/a"
                ):
                    problems.append(
                        "%s: name item %r lacks entity/canonical/variant"
                        % (did, it["value"])
                    )
            elif (
                it["entity"] is not None
                or it["canonical"] is not None
                or it["variant"] != "n/a"
            ):
                problems.append(
                    "%s: non-name item %r must have null entity/canonical"
                    % (did, it["value"])
                )
            got = counts[it["value"]]
            if it["occurrences"] < 1:
                problems.append(
                    "%s: item %r has occurrences < 1" % (did, it["value"])
                )
            if got != it["occurrences"]:
                problems.append(
                    "%s: %r (%s) key says %d, document has %d"
                    % (did, it["value"], it["category"], it["occurrences"], got)
                )
            s = structural(it)
            if s:
                problems.append("%s: %r: %s" % (did, it["value"], s))
        vset = set(values)
        for dstr in key["distractors"]:
            if dstr in vset:
                problems.append(
                    "%s: distractor %r is also a key value" % (did, dstr)
                )
            elif norm(dstr) not in text:
                problems.append(
                    "%s: distractor %r not found in document" % (did, dstr)
                )
        wc = len([w for w in text.split(" ") if w and w != SEP.strip()])
        if key["format"] not in ("pdf", "rtf") and wc != key["word_count"]:
            problems.append(
                "%s: word_count key says %d, document has %d"
                % (did, key["word_count"], wc)
            )

    mpath = os.path.join(corpus, "manifest.json")
    if not os.path.exists(mpath):
        problems.append("manifest.json missing")
    else:
        with open(mpath, encoding="utf-8") as f:
            man = json.load(f)
        if [m["id"] for m in man] != [k["id"] for k in keys]:
            problems.append("manifest ids do not match keys")
        for m, k in zip(man, keys):
            if (
                m["item_count"] != len(k["items"])
                or m["file"] != k["file"]
                or m["word_count"] != k["word_count"]
            ):
                problems.append(
                    "%s: manifest entry disagrees with key" % k["id"]
                )

    for p in problems:
        print("MISMATCH " + p)
    print(
        "verify_corpus: %d documents, %d items checked, %d mismatches"
        % (len(keys), n_items, len(problems))
    )
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
