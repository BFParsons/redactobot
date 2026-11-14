#!/usr/bin/env python3
# Copyright 2026 The Redactobot Authors
# SPDX-License-Identifier: Apache-2.0

"""Independent self-check for the third test corpus (doc-301 .. doc-360).

Run:  python3 -P evaluation/verify_corpus3.py [--corpus DIR]

Does not import the generator and does not use the tool under test. For
every document it re-reads the file that was actually written with its own
format reader, normalises whitespace and checks that

  * every key value appears exactly `occurrences` times as a standalone
    token sequence (longer key values are found and masked first);
  * the key and item schema is right, including the optional `minor` and
    `cardholder` flags and the single rule for difficulty "hard";
  * checksummed numbers are valid and contact details are fictional;
  * every distractor is present and the manifest matches the keys;
  * LEFTOVER REVIEW: after masking key values, distractors and reviewed
    phrases, every remaining capitalised word, digit-bearing token and
    email/URL-looking token is listed in the key's reviewed_not_sensitive.
    The number of unreviewed leftovers is printed per document.

Exits non-zero on any mismatch or any unreviewed leftover.
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
SEP = " ¦ "

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
HARD_VARIANTS = {"caps", "initials", "last-first", "nickname", "acronym"}
HARD_CATEGORIES = {"health_info", "sensitive_attribute", "indirect_identifier"}
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
    "reviewed_not_sensitive",
]
MASKED = re.compile(r"[xX]{2,}|\*|•|#{2,}|…|\.\.\.")


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
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            body = part.get_payload(decode=True).decode(
                part.get_content_charset() or "utf-8"
            )
            return "\n".join(parts) + "\n\n" + body
    raise ValueError("no text/plain part")


class _Visible(html.parser.HTMLParser):
    BLOCK = {
        "p",
        "div",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
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
        "article",
        "aside",
        "nav",
        "form",
        "fieldset",
        "address",
        "tbody",
        "thead",
        "caption",
        "label",
    }
    HIDDEN = {"script", "style", "head", "template"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.HIDDEN:
            self.skip += 1
        elif tag in self.BLOCK:
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in self.HIDDEN:
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
            if not part.is_linked_to_previous:
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


def _sections(code):
    secs, cur, quoted, i = [], "", False, 0
    while i < len(code):
        ch = code[i]
        if ch == '"':
            quoted = not quoted
            cur += ch
        elif ch == "\\" and not quoted:
            cur += code[i : i + 2]
            i += 1
        elif ch == ";" and not quoted:
            secs.append(cur)
            cur = ""
        else:
            cur += ch
        i += 1
    return secs + [cur]


def show_number(v, code):
    """Render a number the way a spreadsheet displays it for this format code."""
    if code in (None, "General"):
        return str(int(v)) if isinstance(v, float) and v == int(v) else str(v)
    secs = _sections(code)
    neg = v < 0
    sec, sign = (
        (secs[1], "")
        if neg and len(secs) > 1
        else (secs[0], "-" if neg else "")
    )
    before, after, pat, i = "", "", "", 0
    while i < len(sec):
        ch = sec[i]
        if ch == '"':
            j = sec.index('"', i + 1)
            lit, i = sec[i + 1 : j], j + 1
        elif ch == "\\":
            lit, i = sec[i + 1], i + 2
        elif ch in "_*":
            i += 2
            continue
        elif ch == "[":
            i = sec.index("]", i) + 1
            continue
        elif ch in "#0,.?":
            pat += ch
            i += 1
            continue
        else:
            lit, i = ch, i + 1
        if pat:
            after += lit
        else:
            before += lit
    dec = len(pat.split(".", 1)[1]) if "." in pat else 0
    body = ("{:,.%df}" if "," in pat else "{:.%df}") % dec
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


def show_date(v, code):
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

    out = []
    for ws in openpyxl.load_workbook(path).worksheets:
        for row in ws.iter_rows():
            shown = []
            for c in row:
                v = c.value
                if v is None or v == "":
                    continue
                if isinstance(v, (datetime.datetime, datetime.date)):
                    shown.append(show_date(v, c.number_format))
                elif isinstance(v, bool):
                    shown.append(str(v).upper())
                elif isinstance(v, (int, float)):
                    shown.append(show_number(v, c.number_format))
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


_RTF = {}


def convert_rtfs(paths, workdir):
    """Convert all RTFs to text with LibreOffice in one run."""
    if not paths:
        return
    tmp = tempfile.mkdtemp(prefix=".verify_", dir=workdir)
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
                    _RTF[p] = f.read()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def read_rtf(path):
    if path not in _RTF:
        raise ValueError("LibreOffice could not convert the RTF")
    return _RTF[path]


READERS = {
    "txt": read_plain,
    "md": read_plain,
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


def standalone(text, i, j, v):
    if v[0].isalnum() and i > 0:
        p = text[i - 1]
        if p.isalnum() or (
            v[0].isdigit() and p in ".," and i > 1 and text[i - 2].isdigit()
        ):
            return False
    if v[-1].isalnum() and j < len(text):
        q = text[j]
        if q.isalnum() or (
            v[-1].isdigit()
            and q in ".,"
            and j + 1 < len(text)
            and text[j + 1].isdigit()
        ):
            return False
    return True


def count_all(text, values, taken):
    """text is normalised. Longest value first; matched spans are masked in `taken`."""
    counts = {}
    for v in sorted(set(values), key=lambda s: (-len(norm(s)), s)):
        nv = norm(v)
        n, pos = 0, 0
        while nv:
            i = text.find(nv, pos)
            if i < 0:
                break
            j = i + len(nv)
            if not any(taken[i:j]) and standalone(text, i, j, nv):
                n += 1
                for k in range(i, j):
                    taken[k] = 1
                pos = j
            else:
                pos = i + 1
        counts[v] = n
    return counts


_EDGE = ".,;:!?\"'()[]{}<>*_~`|¦-–—/\\=“”‘’•·"
_CAP = re.compile(r"(?:[A-Z]\.)+[A-Z]\b|[A-Z][A-Za-z'’]*")
_DOMAIN = re.compile(r"[A-Za-z0-9]\.[a-z]{2,}(?:/|$)")


def leftovers(text, taken):
    """Distinct uncovered tokens that are capitalised, contain a digit, or look like an email/URL."""
    visible = "".join(" " if taken[k] else ch for k, ch in enumerate(text))
    found = set()
    for chunk in visible.split():
        t = chunk.strip(_EDGE)
        if not t:
            continue
        if t.count("(") > t.count(")"):
            t += ")"
        if any(c.isdigit() for c in t):
            found.add(t)
        elif "@" in t or "://" in t or _DOMAIN.search(t):
            found.add(t)
        else:
            for m in _CAP.finditer(t):
                if m.start() == 0 or not t[m.start() - 1].isalpha():
                    found.add(m.group(0))
    return found


# ----------------------------------------------------- structural checks


def luhn(d):
    t = 0
    for k, ch in enumerate(reversed(d)):
        x = int(ch)
        if k % 2:
            x = x * 2 - 9 if x * 2 > 9 else x * 2
        t += x
    return t % 10 == 0


def ip_fictional(v):
    v = v.strip("[]")
    if ":" in v and not re.fullmatch(r"[\d.]+(:\d+)?", v):
        return v.lower().startswith(("2001:db8", "2001:0db8", "fd", "fe80"))
    m = re.match(r"(\d+)\.(\d+)\.(\d+)\.(\d+)", v)
    if not m:
        return False
    a, b, c, _ = (int(x) for x in m.groups())
    return (
        (a, b, c) in ((192, 0, 2), (198, 51, 100), (203, 0, 113))
        or a == 10
        or (a == 172 and 16 <= b <= 31)
        or (a == 192 and b == 168)
    )


def structural(it, jur):
    v, cat = it["value"], it["category"]
    d = re.sub(r"\D", "", v)
    masked = bool(MASKED.search(v))
    if cat == "payment_card" and len(d) >= 13 and not masked and not luhn(d):
        return "card number fails Luhn"
    if cat == "iban":
        s = re.sub(r"\s", "", v).upper()
        if (
            not re.fullmatch(r"[A-Z]{2}\d{2}[A-Z0-9]+", s)
            or int("".join(str(int(c, 36)) for c in s[4:] + s[:4])) % 97 != 1
        ):
            return "IBAN fails mod-97"
    if cat == "routing_number" and len(d) == 9 and not masked:
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
    if (
        cat == "tax_id"
        and "SIN" in it["subtype"]
        and len(d) == 9
        and not masked
        and not luhn(d)
    ):
        return "SIN fails Luhn"
    if cat in ("email", "url") and "example" not in v.lower():
        return "not a reserved example domain"
    if cat == "ip_address" and not ip_fictional(v):
        return "IP address outside documentation/private ranges"
    if cat == "phone" and jur in ("US", "CA") and not masked:
        s = v.strip()
        if not (s.startswith("+") and not s.startswith("+1")):
            pd = re.sub(r"\D", "", re.split(r"x|ext", s, flags=re.I)[0])
            if len(pd) == 11 and pd[0] == "1":
                pd = pd[1:]
            if (len(pd) == 10 and pd[3:8] != "55501") or (
                len(pd) == 7 and pd[:5] != "55501"
            ):
                return "phone number is not a 555-01xx number"
    return None


def must_be_hard(it):
    cat, v = it["category"], it["value"]
    if cat in HARD_CATEGORIES or it["variant"] in HARD_VARIANTS:
        return True
    if cat in ("person_name", "organization_name"):
        return sum(c.isalpha() for c in v) >= 4 and v.upper() == v
    if MASKED.search(v) and cat not in ("url", "credential", "email"):
        return True
    return False


# ------------------------------------------------------------------ main


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=os.path.join(HERE, "corpus3"))
    ap.add_argument(
        "--quiet",
        action="store_true",
        help="do not print the per-document leftover counts",
    )
    a = ap.parse_args()
    corpus = os.path.abspath(a.corpus)
    keys = []
    for kp in sorted(glob.glob(os.path.join(corpus, "keys", "doc-*.json"))):
        with open(kp, encoding="utf-8") as f:
            keys.append(json.load(f))
    convert_rtfs(
        [
            os.path.join(corpus, k["file"])
            for k in keys
            if k.get("format") == "rtf"
        ],
        corpus,
    )

    problems, n_items, n_left = [], 0, 0
    for key in keys:
        did = key.get("id", "?")
        missing = [f for f in KEY_FIELDS if f not in key]
        for fld in missing:
            problems.append("%s: key missing field %s" % (did, fld))
        if missing:
            continue
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
        items = key["items"]
        values = [it["value"] for it in items]
        if len(set(values)) != len(values):
            problems.append("%s: duplicate values in key" % did)
        taken = bytearray(len(text))
        counts = count_all(text, values, taken)
        flags = {}
        for it in items:
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
            elif it["difficulty"] != "hard" and must_be_hard(it):
                problems.append(
                    "%s: item %r must be marked hard under the corpus rule"
                    % (did, it["value"])
                )
            is_name = it["category"] in ("person_name", "organization_name")
            if is_name:
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
            for flag in ("minor", "cardholder"):
                if flag in it and (
                    it[flag] is not True or it["category"] != "person_name"
                ):
                    problems.append(
                        "%s: item %r has an invalid %s flag"
                        % (did, it["value"], flag)
                    )
            if it["category"] == "person_name":
                flags.setdefault(it["entity"], set()).add(
                    (bool(it.get("minor")), bool(it.get("cardholder")))
                )
            if it["occurrences"] < 1:
                problems.append(
                    "%s: item %r has occurrences < 1" % (did, it["value"])
                )
            if counts[it["value"]] != it["occurrences"]:
                problems.append(
                    "%s: %r (%s) key says %d, document has %d"
                    % (
                        did,
                        it["value"],
                        it["category"],
                        it["occurrences"],
                        counts[it["value"]],
                    )
                )
            s = structural(it, key["jurisdiction"])
            if s:
                problems.append("%s: %r: %s" % (did, it["value"], s))
        for ent, combos in flags.items():
            if len(combos) > 1:
                problems.append(
                    "%s: entity %s has minor/cardholder flags on some written forms only"
                    % (did, ent)
                )
        if any(it.get("cardholder") for it in items) and not any(
            it["category"] == "payment_card" for it in items
        ):
            problems.append(
                "%s: cardholder flagged but no payment_card item" % did
            )

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
        reviewed = key["reviewed_not_sensitive"]
        for r in reviewed:
            if r in vset:
                problems.append(
                    "%s: reviewed entry %r is also a key value" % (did, r)
                )
        count_all(
            text,
            list(key["distractors"]) + [r for r in reviewed if " " in norm(r)],
            taken,
        )
        left = sorted(leftovers(text, taken) - set(reviewed))
        n_left += len(left)
        if not a.quiet:
            print(
                "%s: %d unreviewed leftovers%s"
                % (did, len(left), (": " + "  ".join(left)) if left else "")
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
                or m["format"] != k["format"]
                or m["audience"] != k["audience"]
            ):
                problems.append(
                    "%s: manifest entry disagrees with key" % k["id"]
                )

    if len(keys) == 60:  # whole-corpus requirements
        for c in sorted(CATEGORIES):
            nd = sum(
                1 for k in keys if any(i["category"] == c for i in k["items"])
            )
            if nd < 6:
                problems.append(
                    "corpus: category %s appears in only %d documents (need 6)"
                    % (c, nd)
                )
        for flag in ("minor", "cardholder"):
            nd = sum(1 for k in keys if any(i.get(flag) for i in k["items"]))
            if nd < 10:
                problems.append(
                    "corpus: only %d documents have a %s (need 10)" % (nd, flag)
                )
        if [k["id"] for k in keys] != ["doc-%d" % n for n in range(301, 361)]:
            problems.append("corpus: document ids are not doc-301 .. doc-360")

    for p in problems:
        print("MISMATCH " + p)
    print(
        "verify_corpus3: %d documents, %d items checked, %d mismatches, %d unreviewed leftovers"
        % (len(keys), n_items, len(problems), n_left)
    )
    sys.exit(1 if problems or n_left else 0)


if __name__ == "__main__":
    main()
