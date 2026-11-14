#!/usr/bin/env python3
# Copyright 2026 The Redactobot Authors
# SPDX-License-Identifier: Apache-2.0

"""Deterministic generator for the Redactobot independent test corpus.

Run:  python3 -P eval/generate.py

Writes (next to this file):
  corpus/docs/doc-NNN.<ext>     the documents
  corpus/keys/doc-NNN.json      machine-readable answer key
  corpus/keys/doc-NNN.md        human-readable answer key
  corpus/manifest.json

All document content is authored, fictional text held in corpus_src/batch_*.py
with every sensitive value marked inline; the answer keys are derived from
that markup, and occurrence counts are computed from the document text model
(longest value first, masked, standalone-token boundaries). verify_corpus.py
re-derives the counts independently from the files actually written.

No network, no clock: the only randomness is the fixed-seed RNG behind the
--mint helper (used while authoring to mint checksum-valid fake numbers).

Other options (authoring aids):
  --batch a        build only corpus_src/batch_a.py
  --out DIR        write the corpus somewhere else
  --caps           list leftover capitalised words per doc (review aid)
  --mint KIND [-n N] [--salt S]   KIND = card | iban | aba | sin | ssn
"""

import argparse
import base64
import datetime
import glob
import html as htmllib
import importlib
import json
import os
import quopri
import random
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

SEED = 20261111
random.seed(SEED)

CATEGORIES = [
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
]
ALIAS = {
    "money": "money_amount",
    "dob": "date_of_birth",
    "addr": "street_address",
    "zip": "postal_code",
    "rec": "record_number",
    "health": "health_info",
    "attr": "sensitive_attribute",
    "indirect": "indirect_identifier",
    "acct": "bank_account",
    "rtn": "routing_number",
    "card": "payment_card",
    "exp": "card_expiry",
    "cvv": "card_security_code",
    "govid": "government_id",
    "ip": "ip_address",
    "veh": "vehicle_id",
    "dev": "device_id",
    "cred": "credential",
    "age": "age_over_89",
    "taxid": "tax_id",
}
WHY = {
    "person_name": "identifies a person",
    "organization_name": "identifies a client, party or organization",
    "email": "direct contact detail",
    "phone": "direct contact detail",
    "street_address": "locates a person or business",
    "postal_code": "narrows location to a small area",
    "place": "locates the person or matter",
    "ssn": "government identifier unique to a person",
    "tax_id": "tax identifier unique to a person or business",
    "government_id": "official identifier unique to a person",
    "bank_account": "financial account identifier",
    "routing_number": "bank identifier tied to an account",
    "iban": "financial account identifier",
    "payment_card": "payment card number",
    "card_expiry": "payment card detail",
    "card_security_code": "payment card detail",
    "money_amount": "confidential financial detail",
    "date_of_birth": "birth date identifies a person",
    "date": "date tied to a person or matter",
    "age_over_89": "extreme age is identifying",
    "record_number": "record identifier that links to a person or matter",
    "url": "link that reveals a person, account or organization",
    "ip_address": "network identifier",
    "vehicle_id": "identifies a vehicle and its owner",
    "device_id": "identifies a device and its owner",
    "credential": "login secret or account handle",
    "health_info": "health information about a person",
    "sensitive_attribute": "special-category personal attribute",
    "indirect_identifier": "identifies someone by context",
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
}
VARIANT_SUBTYPE = {
    "full": "full name",
    "short": "short form",
    "initials": "initials",
    "first-name": "first name only",
    "surname": "surname only",
    "title-surname": "title + surname",
    "acronym": "acronym",
    "caps": "ALL CAPS",
    "last-first": "Last, First order",
    "nickname": "nickname",
}
AUTO_HARD_VARIANTS = {"caps", "initials", "last-first", "nickname"}
FORMATS = {"txt", "md", "eml", "html", "docx", "pdf", "rtf", "pptx", "xlsx"}
AUDIENCES = {"legal", "accounting", "health", "general"}
JURS = {"US", "CA", "UK", "EU"}
EML_HEADERS = ["From", "To", "Cc", "Bcc", "Reply-To", "Subject", "Date"]
CELL_SEP = " \u00a6 "

MARK = re.compile(r"\[\[(.+?)\|([^\[\]|]+)(?:\|([^\[\]|]*))?\]\]", re.S)


# ----------------------------------------------------------------- checks


def luhn_ok(digits):
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


def iban_ok(s):
    s = re.sub(r"\s+", "", s).upper()
    if not re.fullmatch(r"[A-Z]{2}\d{2}[A-Z0-9]{10,30}", s):
        return False
    r = s[4:] + s[:4]
    n = "".join(str(int(c, 36)) for c in r)
    return int(n) % 97 == 1


def aba_ok(d):
    if len(d) != 9:
        return False
    v = [int(c) for c in d]
    return (
        3 * (v[0] + v[3] + v[6])
        + 7 * (v[1] + v[4] + v[7])
        + (v[2] + v[5] + v[8])
    ) % 10 == 0


def ssn_ok(d):
    return not (
        d[:3] in ("000", "666")
        or d[0] == "9"
        or d[3:5] == "00"
        or d[5:] == "0000"
    )


# ------------------------------------------------------------- counting


def norm_ws(s):
    return re.sub(r"\s+", " ", s).strip()


def count_and_mask(text, values):
    """Count standalone occurrences of each value, longest first, masking as we go.
    Returns (counts, masked_text). text must already be whitespace-normalised.
    """
    buf = list(text)
    counts = {}
    order = sorted(set(values), key=lambda v: (-len(norm_ws(v)), v))
    for v in order:
        nv = norm_ws(v)
        s = "".join(buf)
        n = 0
        start = 0
        spans = []
        while nv:
            i = s.find(nv, start)
            if i < 0:
                break
            j = i + len(nv)
            ok = True
            if nv[0].isalnum() and i > 0:
                p = text[i - 1]
                if p.isalnum():
                    ok = False
                elif (
                    nv[0].isdigit()
                    and p in ".,"
                    and i > 1
                    and text[i - 2].isdigit()
                ):
                    ok = False
            if ok and nv[-1].isalnum() and j < len(text):
                q = text[j]
                if q.isalnum():
                    ok = False
                elif (
                    nv[-1].isdigit()
                    and q in ".,"
                    and j + 1 < len(text)
                    and text[j + 1].isdigit()
                ):
                    ok = False
            if ok:
                n += 1
                spans.append((i, j))
                start = j
            else:
                start = i + 1
        for i, j in spans:
            for k in range(i, j):
                buf[k] = "\x00"
        counts[v] = n
    return counts, "".join(buf)


# ---------------------------------------------------------------- markup


class Collector:
    def __init__(self, doc_id, ents, errors):
        self.doc_id = doc_id
        self.ents = ents or {}
        self.errors = errors
        self.items = {}

    def err(self, msg):
        self.errors.append("%s: %s" % (self.doc_id, msg))

    def add(self, value, tag, why=None, raw=None):
        value = value.strip()
        tag = tag.strip()
        if "\n" in value:
            self.err("value spans lines: %r" % value)
        m = re.fullmatch(r"([po]\d+):([a-z\-]+?)(!?)(?::(.+))?", tag)
        if m:
            ent, variant, hard, sub = m.groups()
            cat = "person_name" if ent[0] == "p" else "organization_name"
            if ent not in self.ents:
                self.err("unknown entity %s for %r" % (ent, value))
            if variant not in VARIANTS:
                self.err("bad variant %r for %r" % (variant, value))
            item = dict(
                value=value,
                category=cat,
                subtype=sub or VARIANT_SUBTYPE.get(variant, variant),
                occurrences=0,
                entity=ent,
                canonical=self.ents.get(ent),
                variant=variant,
                difficulty=(
                    "hard"
                    if (hard or variant in AUTO_HARD_VARIANTS)
                    else "standard"
                ),
                why=why or WHY[cat],
            )
        else:
            m = re.fullmatch(r"([a-z_]+)(!?)(?::(.+))?", tag)
            if not m:
                self.err("bad tag %r for %r" % (tag, value))
                return
            c, hard, sub = m.groups()
            cat = ALIAS.get(c, c)
            if cat not in CATEGORIES or cat in (
                "person_name",
                "organization_name",
            ):
                self.err("bad category %r for %r" % (c, value))
                return
            item = dict(
                value=value,
                category=cat,
                subtype=sub or cat.replace("_", " "),
                occurrences=0,
                entity=None,
                canonical=None,
                variant="n/a",
                difficulty="hard" if hard else "standard",
                why=why or WHY[cat],
            )
        if raw is not None:
            item["raw_cell_value"] = raw
        old = self.items.get(value)
        if old is None:
            self.items[value] = item
        elif old["category"] != item["category"]:
            self.err(
                "value %r marked as both %s and %s"
                % (value, old["category"], item["category"])
            )

    def strip(self, text):
        def rep(m):
            self.add(m.group(1), m.group(2), m.group(3) or None)
            return m.group(1).strip()

        out = MARK.sub(rep, text)
        if "[[" in out or "]]" in out:
            self.err(
                "leftover markup brackets near: %r"
                % out[max(0, out.find("[[") - 20) : out.find("[[") + 60]
            )
        return out


# ---------------------------------------------------------------- blocks


def parse_blocks(text):
    blocks = []
    lines = text.strip("\n").split("\n")
    i = 0
    while i < len(lines):
        ln = lines[i].rstrip()
        s = ln.strip()
        if not s:
            i += 1
            continue
        if s.startswith("## "):
            blocks.append(("h2", s[3:].strip()))
        elif s.startswith("# "):
            blocks.append(("h1", s[2:].strip()))
        elif s.startswith("- "):
            blocks.append(("li", s[2:].strip()))
        elif s == "---":
            blocks.append(("pagebreak", ""))
        elif s.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                r = lines[i].strip()
                if r.endswith("|"):
                    r = r[:-1]
                rows.append([c.strip() for c in r[1:].split("|")])
                i += 1
            w = max(len(r) for r in rows)
            rows = [r + [""] * (w - len(r)) for r in rows]
            blocks.append(("table", rows))
            continue
        else:
            blocks.append(("p", s))
        i += 1
    return blocks


def unbold(s):
    return s.replace("**", "")


def bold_runs(s):
    """Split 'a **b** c' into [(text, bold)]."""
    out = []
    for k, part in enumerate(s.split("**")):
        if part:
            out.append((part, k % 2 == 1))
    return out or [("", False)]


def blocks_text(blocks):
    lines = []
    for kind, val in blocks:
        if kind == "table":
            for r in val:
                lines.append(CELL_SEP.join(unbold(c) for c in r))
        elif kind == "pagebreak":
            continue
        else:
            lines.append(unbold(val))
    return "\n".join(lines)


# ------------------------------------------------------------- renderers


def render_docx(blocks, path):
    from docx import Document
    from docx.enum.text import WD_BREAK

    doc = Document()
    fixed = datetime.datetime(2026, 1, 1)
    doc.core_properties.created = fixed
    doc.core_properties.modified = fixed
    doc.core_properties.author = ""
    doc.core_properties.title = ""

    def fill(par, s):
        for t, b in bold_runs(s):
            r = par.add_run(t)
            if b:
                r.bold = True

    for kind, val in blocks:
        if kind == "h1":
            doc.add_heading(unbold(val), level=1)
        elif kind == "h2":
            doc.add_heading(unbold(val), level=2)
        elif kind == "li":
            fill(doc.add_paragraph(style="List Bullet"), val)
        elif kind == "pagebreak":
            doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        elif kind == "table":
            t = doc.add_table(rows=len(val), cols=len(val[0]))
            t.style = "Table Grid"
            for ri, row in enumerate(val):
                for ci, c in enumerate(row):
                    cell = t.cell(ri, ci)
                    par = cell.paragraphs[0]
                    if ri == 0:
                        r = par.add_run(unbold(c))
                        r.bold = True
                    else:
                        fill(par, c)
            doc.add_paragraph()
        else:
            fill(doc.add_paragraph(), val)
    doc.save(path)


def inline_html(s):
    return "".join(
        (
            ("<b>%s</b>" % htmllib.escape(t, quote=False))
            if b
            else htmllib.escape(t, quote=False)
        )
        for t, b in bold_runs(s)
    )


def render_html(blocks, path, page_title):
    o = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        "<title>%s</title>" % htmllib.escape(page_title),
        "<style>body{font-family:Georgia,serif;max-width:52em;margin:2em auto;line-height:1.45}"
        "table{border-collapse:collapse}td,th{border:1px solid #999;padding:4px 8px;text-align:left}"
        "h1{font-size:1.4em}h2{font-size:1.1em}</style>",
        "</head>",
        "<body>",
        "<main>",
    ]
    in_list = False
    for kind, val in blocks:
        if kind == "li":
            if not in_list:
                o.append("<ul>")
                in_list = True
            o.append("<li>%s</li>" % inline_html(val))
            continue
        if in_list:
            o.append("</ul>")
            in_list = False
        if kind == "h1":
            o.append("<h1>%s</h1>" % inline_html(val))
        elif kind == "h2":
            o.append("<h2>%s</h2>" % inline_html(val))
        elif kind == "pagebreak":
            o.append("<hr>")
        elif kind == "table":
            o.append("<table>")
            for ri, row in enumerate(val):
                tag = "th" if ri == 0 else "td"
                o.append(
                    "<tr>"
                    + "".join(
                        "<%s>%s</%s>" % (tag, inline_html(c), tag) for c in row
                    )
                    + "</tr>"
                )
            o.append("</table>")
        else:
            o.append("<p>%s</p>" % inline_html(val))
    if in_list:
        o.append("</ul>")
    o += ["</main>", "</body>", "</html>", ""]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(o))


def rtf_esc(s):
    out = []
    for ch in s:
        c = ord(ch)
        if ch in "\\{}":
            out.append("\\" + ch)
        elif c < 128:
            out.append(ch)
        else:
            out.append("\\u%d?" % (c if c < 32768 else c - 65536))
    return "".join(out)


def inline_rtf(s):
    return "".join(
        ("{\\b %s}" % rtf_esc(t)) if b else rtf_esc(t) for t, b in bold_runs(s)
    )


def render_rtf(blocks, path):
    o = [
        "{\\rtf1\\ansi\\ansicpg1252\\deff0{\\fonttbl{\\f0\\froman Times New Roman;}}",
        "\\paperw12240\\paperh15840\\margl1440\\margr1440\\f0\\fs22",
    ]
    for kind, val in blocks:
        if kind == "h1":
            o.append(
                "{\\pard\\sb240\\sa120\\b\\fs30 %s\\par}" % rtf_esc(unbold(val))
            )
        elif kind == "h2":
            o.append(
                "{\\pard\\sb180\\sa80\\b\\fs24 %s\\par}" % rtf_esc(unbold(val))
            )
        elif kind == "li":
            o.append(
                "{\\pard\\li360\\fi-200\\sa60 \\bullet  %s\\par}"
                % inline_rtf(val)
            )
        elif kind == "pagebreak":
            o.append("\\page")
        elif kind == "table":
            n = len(val[0])
            w = 9000 // n
            for ri, row in enumerate(val):
                o.append(
                    "\\trowd\\trgaph80"
                    + "".join("\\cellx%d" % (w * (k + 1)) for k in range(n))
                )
                o.append(
                    "".join(
                        "\\pard\\intbl %s\\cell "
                        % (
                            ("{\\b %s}" % rtf_esc(unbold(c)))
                            if ri == 0
                            else inline_rtf(c)
                        )
                        for c in row
                    )
                    + "\\row"
                )
            o.append("\\pard\\par")
        else:
            o.append("{\\pard\\sa120 %s\\par}" % inline_rtf(val))
    o.append("}")
    with open(path, "w", encoding="ascii", newline="\n") as f:
        f.write("\n".join(o) + "\n")


def render_pptx(blocks, path):
    from pptx import Presentation
    from pptx.util import Inches, Pt

    prs = Presentation()
    prs.core_properties.created = datetime.datetime(2026, 1, 1)
    prs.core_properties.modified = datetime.datetime(2026, 1, 1)
    slides = []
    for kind, val in blocks:
        if kind == "h1":
            slides.append((val, []))
        elif kind == "pagebreak":
            continue
        else:
            slides[-1][1].append((kind, val))
    for title, items in slides:
        slide = prs.slides.add_slide(prs.slide_layouts[5])
        slide.shapes.title.text = unbold(title)
        texts = [(k, v) for k, v in items if k != "table"]
        tables = [v for k, v in items if k == "table"]
        top = 1.5
        if texts:
            hgt = (
                min(5.0, 0.42 * len(texts) + 0.3)
                if not tables
                else min(2.2, 0.42 * len(texts) + 0.3)
            )
            tb = slide.shapes.add_textbox(
                Inches(0.6), Inches(top), Inches(8.8), Inches(hgt)
            )
            tf = tb.text_frame
            tf.word_wrap = True
            first = True
            for k, v in texts:
                par = tf.paragraphs[0] if first else tf.add_paragraph()
                first = False
                for t, b in bold_runs(v):
                    r = par.add_run()
                    r.text = t
                    r.font.size = Pt(16)
                    if b or k == "h2":
                        r.font.bold = True
            top += hgt + 0.2
        for rows in tables:
            shape = slide.shapes.add_table(
                len(rows),
                len(rows[0]),
                Inches(0.6),
                Inches(top),
                Inches(8.8),
                Inches(0.38 * len(rows)),
            )
            for ri, row in enumerate(rows):
                for ci, c in enumerate(row):
                    cell = shape.table.cell(ri, ci)
                    cell.text = unbold(c)
                    for p in cell.text_frame.paragraphs:
                        for r in p.runs:
                            r.font.size = Pt(12)
            top += 0.38 * len(rows) + 0.3
    prs.save(path)


DATE_TOKENS = re.compile(r"yyyy|yy|mmmm|mmm|mm|m|dd|d")
MONTHS = [
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


def date_display(iso, fmt):
    y, mo, d = (int(x) for x in iso.split("-"))

    def rep(m):
        t = m.group(0)
        return {
            "yyyy": "%04d" % y,
            "yy": "%02d" % (y % 100),
            "mmmm": MONTHS[mo - 1],
            "mmm": MONTHS[mo - 1][:3],
            "mm": "%02d" % mo,
            "m": str(mo),
            "dd": "%02d" % d,
            "d": str(d),
        }[t]

    return DATE_TOKENS.sub(rep, fmt)


AMT_FMT = {
    "usd": ('"$"#,##0.00', "$", 2, False),
    "usd0": ('"$"#,##0', "$", 0, False),
    "acct": ('"$"#,##0.00_);\\("$"#,##0.00\\)', "$", 2, True),
    "num": ("#,##0.00", "", 2, False),
    "numacct": ("#,##0.00_);\\(#,##0.00\\)", "", 2, True),
    "cad": ('"C$"#,##0.00', "C$", 2, False),
    "gbp": ('"\u00a3"#,##0.00', "\u00a3", 2, False),
    "eur": ('"\u20ac"#,##0.00', "\u20ac", 2, False),
}


def amt_display(v, fmt):
    code, sym, dec, paren = AMT_FMT[fmt]
    s = sym + ("{:,.%df}" % dec).format(abs(v))
    if v < 0:
        s = "(%s)" % s if paren else "-" + s
    return s


def build_xlsx(sheets, col, path):
    """Returns the text model. Writes the workbook."""
    from openpyxl import Workbook
    from openpyxl.styles import Font
    from openpyxl.utils import get_column_letter

    wb = Workbook()
    wb.properties.created = datetime.datetime(2026, 1, 1)
    wb.properties.modified = datetime.datetime(2026, 1, 1)
    wb.remove(wb.active)
    lines = []
    for name, rows in sheets:
        ws = wb.create_sheet(name)
        widths = {}
        for ri, row in enumerate(rows, 1):
            shown = []
            for ci, c in enumerate(row, 1):
                if c is None or c == "":
                    continue
                cell = ws.cell(row=ri, column=ci)
                if isinstance(c, tuple):
                    kind, v, fmt, tag = c
                    if kind == "date":
                        y, mo, d = (int(x) for x in v.split("-"))
                        cell.value = datetime.date(y, mo, d)
                        cell.number_format = fmt
                        disp = date_display(v, fmt)
                        col.add(disp, tag, raw=v)
                    elif kind == "amt":
                        cell.value = v
                        cell.number_format = AMT_FMT[fmt][0]
                        disp = amt_display(v, fmt)
                        col.add(disp, tag, raw=repr(v))
                    else:
                        cell.value = v
                        disp = str(v)
                        col.add(disp, tag, raw=repr(v))
                elif isinstance(c, str):
                    disp = col.strip(c)
                    cell.value = disp
                    if ri == 1:
                        cell.font = Font(bold=True)
                else:
                    cell.value = c
                    disp = str(c)
                shown.append(disp)
                widths[ci] = max(widths.get(ci, 8), min(60, len(disp) + 2))
            if shown:
                lines.append(CELL_SEP.join(shown))
        for ci, w in widths.items():
            ws.column_dimensions[get_column_letter(ci)].width = w
    wb.save(path)
    return "\n".join(lines)


def build_eml(doc_id, headers, body, enc, path):
    def crlf(s):
        return s.replace("\r\n", "\n").replace("\n", "\r\n")

    def qp(s):
        return quopri.encodestring(s.encode("utf-8")).decode("ascii")

    def b64(s):
        raw = base64.b64encode(s.encode("utf-8")).decode("ascii")
        return "\n".join(raw[i : i + 76] for i in range(0, len(raw), 76)) + "\n"

    body = body.strip("\n") + "\n"
    is_ascii = all(ord(c) < 128 for c in body)
    if enc == "plain" and any(len(l) > 900 for l in body.split("\n")):
        enc = "qp"
    out = []
    for h in EML_HEADERS:
        if headers.get(h):
            out.append("%s: %s" % (h, headers[h]))
    out.append("Message-ID: <%s.%d@mail.example>" % (doc_id, SEED))
    out.append("MIME-Version: 1.0")
    if enc == "plain":
        out.append(
            'Content-Type: text/plain; charset="%s"'
            % ("us-ascii" if is_ascii else "utf-8")
        )
        out.append(
            "Content-Transfer-Encoding: %s" % ("7bit" if is_ascii else "8bit")
        )
        out.append("")
        out.append(body)
    elif enc == "qp":
        out.append('Content-Type: text/plain; charset="utf-8"')
        out.append("Content-Transfer-Encoding: quoted-printable")
        out.append("")
        out.append(qp(body))
    elif enc == "base64":
        out.append('Content-Type: text/plain; charset="utf-8"')
        out.append("Content-Transfer-Encoding: base64")
        out.append("")
        out.append(b64(body))
    elif enc == "multipart":
        bnd = "=_csai_%s_alt" % doc_id
        paras = re.split(r"\n\s*\n", body.strip("\n"))
        h = (
            "<html><body>\n"
            + "\n".join(
                "<p>%s</p>"
                % "<br>\n".join(
                    htmllib.escape(l, quote=False) for l in p.split("\n")
                )
                for p in paras
            )
            + "\n</body></html>\n"
        )
        out.append('Content-Type: multipart/alternative; boundary="%s"' % bnd)
        out.append("")
        out.append("This is a multi-part message in MIME format.")
        out.append("--" + bnd)
        out.append('Content-Type: text/plain; charset="utf-8"')
        out.append("Content-Transfer-Encoding: quoted-printable")
        out.append("")
        out.append(qp(body))
        out.append("--" + bnd)
        out.append('Content-Type: text/html; charset="utf-8"')
        out.append("Content-Transfer-Encoding: quoted-printable")
        out.append("")
        out.append(qp(h))
        out.append("--" + bnd + "--")
        out.append("")
    else:
        raise ValueError("bad eml enc %r" % enc)
    data = crlf("\n".join(out))
    with open(path, "wb") as f:
        f.write(data.encode("utf-8"))


def docx_to_pdf(pairs, errors):
    """pairs: [(docx_path, pdf_path)]"""
    if not pairs:
        return
    tmp = tempfile.mkdtemp(prefix="csai_lo_")
    try:
        outdir = os.path.dirname(pairs[0][1])
        cmd = [
            "soffice",
            "--headless",
            "-env:UserInstallation=file://%s/profile" % tmp,
            "--convert-to",
            "pdf",
            "--outdir",
            outdir,
        ] + [p[0] for p in pairs]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
        for src, dst in pairs:
            if not os.path.exists(dst):
                errors.append(
                    "PDF conversion failed for %s: %s"
                    % (os.path.basename(src), r.stderr.strip()[:200])
                )
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ------------------------------------------------------------------ lint

UNMARKED = [
    ("email", re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")),
    ("url", re.compile(r"https?://\S+|www\.\S+")),
    (
        "money",
        re.compile(
            r"(?:C\$|US\$|[$\u00a3\u20ac])\s?\d[\d,.]*|\b\d[\d,.]*\s?(?:USD|CAD|EUR|GBP)\b"
        ),
    ),
    ("number-like", re.compile(r"\d[\d\-\s./()]{6,}\d")),
]


def lint_item(doc_id, it, errors):
    v, cat = it["value"], it["category"]
    digits = re.sub(r"\D", "", v)
    if cat in ("email", "url") and "example" not in v.lower():
        errors.append(
            "%s: %s %r does not use a reserved example domain"
            % (doc_id, cat, v)
        )
    if (
        cat == "payment_card"
        and len(digits) >= 13
        and not re.search(r"[xX*\u2022#]", v)
    ):
        if not luhn_ok(digits):
            errors.append("%s: card %r fails Luhn" % (doc_id, v))
    if cat == "iban" and not iban_ok(v):
        errors.append("%s: IBAN %r fails mod-97" % (doc_id, v))
    if cat == "routing_number" and len(digits) == 9 and not aba_ok(digits):
        errors.append("%s: routing number %r fails ABA checksum" % (doc_id, v))
    if (
        cat == "ssn"
        and len(digits) == 9
        and not re.search(r"[xX*\u2022#]", v)
        and not ssn_ok(digits)
    ):
        errors.append("%s: SSN %r is structurally implausible" % (doc_id, v))
    if (
        cat == "tax_id"
        and "SIN" in it["subtype"]
        and len(digits) == 9
        and not luhn_ok(digits)
    ):
        errors.append("%s: SIN %r fails Luhn" % (doc_id, v))


# ------------------------------------------------------------------ build


def build_doc(d, out, errors, warnings, pdf_jobs, show_caps):
    doc_id = "doc-%03d" % d["id"]
    fmt = d["fmt"]
    for k, allowed in (
        ("fmt", FORMATS),
        ("audience", AUDIENCES),
        ("jur", JURS),
    ):
        if d[k] not in allowed:
            errors.append("%s: bad %s %r" % (doc_id, k, d[k]))
    col = Collector(doc_id, d.get("ents"), errors)
    path = os.path.join(out, "docs", "%s.%s" % (doc_id, fmt))

    if fmt == "xlsx":
        text = build_xlsx(d["sheets"], col, path)
    elif fmt == "eml":
        headers = {h: col.strip(v) for h, v in d["headers"].items()}
        for h in headers:
            if h not in EML_HEADERS:
                errors.append("%s: unsupported header %s" % (doc_id, h))
            if any(ord(c) > 127 for c in headers[h]):
                errors.append("%s: non-ASCII in header %s" % (doc_id, h))
        body = col.strip(d["body"]).strip("\n")
        build_eml(doc_id, headers, body, d.get("enc", "plain"), path)
        text = (
            "\n".join(
                "%s: %s" % (h, headers[h])
                for h in EML_HEADERS
                if headers.get(h)
            )
            + "\n\n"
            + body
        )
    elif fmt in ("txt", "md"):
        text = col.strip(d["body"]).strip("\n") + "\n"
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
    else:
        blocks = parse_blocks(col.strip(d["body"]))
        text = blocks_text(blocks)
        if fmt == "docx":
            render_docx(blocks, path)
        elif fmt == "pdf":
            tmpdocx = os.path.join(out, ".build", "%s.docx" % doc_id)
            render_docx(blocks, tmpdocx)
            pdf_jobs.append((tmpdocx, path))
        elif fmt == "html":
            render_html(blocks, path, d["doc_type"].capitalize())
        elif fmt == "rtf":
            render_rtf(blocks, path)
        elif fmt == "pptx":
            if not blocks or blocks[0][0] != "h1":
                errors.append(
                    "%s: pptx body must start with '# slide title'" % doc_id
                )
            else:
                render_pptx(blocks, path)

    ntext = norm_ws(text)
    items = list(col.items.values())
    distractors = list(d.get("distractors", []))
    counts, masked = count_and_mask(ntext, [it["value"] for it in items])
    for it in items:
        it["occurrences"] = counts[it["value"]]
        if it["occurrences"] == 0:
            errors.append(
                "%s: value %r never appears standalone (swallowed by a longer value?)"
                % (doc_id, it["value"])
            )
        lint_item(doc_id, it, errors)
    keyvals = set(col.items)
    for s in distractors:
        if s in keyvals:
            errors.append("%s: distractor %r is also a key value" % (doc_id, s))
        elif norm_ws(s) not in ntext:
            errors.append(
                "%s: distractor %r not found in document" % (doc_id, s)
            )
    _, masked2 = count_and_mask(masked, distractors + list(d.get("ok", [])))
    for label, rx in UNMARKED:
        for m in rx.finditer(masked2):
            frag = m.group(0)
            if "\x00" in frag or re.fullmatch(r"\d\d [+-]\d{4}", frag):
                continue
            warnings.append("%s: unmarked %s: %r" % (doc_id, label, frag))
    words = [w for w in ntext.split(" ") if w and w != CELL_SEP.strip()]
    wc = len(words)
    length = d.get("length", "normal")
    if length == "long" and not 1200 <= wc <= 2500:
        warnings.append(
            "%s: long doc has %d words (want 1200-2500)" % (doc_id, wc)
        )
    if length == "short" and wc >= 80:
        warnings.append("%s: short doc has %d words (want < 80)" % (doc_id, wc))
    if length == "normal" and fmt != "xlsx" and not 140 <= wc <= 700:
        warnings.append(
            "%s: normal doc has %d words (want about 150-600)" % (doc_id, wc)
        )
    if show_caps:
        caps = sorted(
            set(
                re.findall(
                    r"\b[A-Z][A-Za-z'\u2019-]+\b", masked2.replace("\x00", " ")
                )
            )
        )
        print("%s leftover capitalised: %s" % (doc_id, " ".join(caps)))

    key = dict(
        id=doc_id,
        file="docs/%s.%s" % (doc_id, fmt),
        format=fmt,
        title=d.get("title") or d["doc_type"].capitalize(),
        doc_type=d["doc_type"],
        audience=d["audience"],
        jurisdiction=d["jur"],
        word_count=wc,
        items=items,
        distractors=distractors,
    )
    with open(
        os.path.join(out, "keys", doc_id + ".json"),
        "w",
        encoding="utf-8",
        newline="\n",
    ) as f:
        json.dump(key, f, ensure_ascii=False, indent=1)
        f.write("\n")
    write_key_md(
        key, os.path.join(out, "keys", doc_id + ".md"), d.get("used_by")
    )
    return key


USED_BY = {
    "legal": "lawyers, paralegals and legal assistants",
    "accounting": "accountants, bookkeepers and tax preparers",
    "health": "clinicians and health-practice administrative staff",
    "general": "office managers, HR and operations staff",
}


def write_key_md(key, path, used_by=None):
    def cell(s):
        return str(s).replace("|", "\\|").replace("\n", " ")

    o = [
        "# %s" % key["title"],
        "",
        "- **Document:** `%s` (%s, %d words)"
        % (key["file"], key["format"], key["word_count"]),
        "- **Document type:** %s" % key["doc_type"],
        "- **Jurisdiction:** %s" % key["jurisdiction"],
        "- **Who would use it:** %s" % (used_by or USED_BY[key["audience"]]),
        "- **Sensitive items:** %d (%d marked hard)"
        % (
            len(key["items"]),
            sum(1 for i in key["items"] if i["difficulty"] == "hard"),
        ),
        "",
        "## Sensitive items",
        "",
        "| Value | Category | Subtype | Refers to | Difficulty | Why it is sensitive | Times |",
        "|---|---|---|---|---|---|---|",
    ]
    for it in key["items"]:
        o.append(
            "| %s | %s | %s | %s | %s | %s | %d |"
            % (
                cell(it["value"]),
                it["category"],
                cell(it["subtype"]),
                cell(it["canonical"] or ""),
                it["difficulty"],
                cell(it["why"]),
                it["occurrences"],
            )
        )
    o += [
        "",
        "## Look-alikes that are not sensitive (must not be redacted)",
        "",
    ]
    o += ["- %s" % cell(s) for s in key["distractors"]] or ["- (none)"]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(o) + "\n")


# ------------------------------------------------------------------ mint


def mint(kind, n, salt):
    rng = random.Random("%d-%s-%s" % (SEED, salt, kind))
    dg = lambda k: "".join(str(rng.randrange(10)) for _ in range(k))
    for _ in range(n):
        if kind == "card":
            pre, ln = rng.choice(
                [
                    ("4", 16),
                    ("51", 16),
                    ("55", 16),
                    ("34", 15),
                    ("37", 15),
                    ("6011", 16),
                    ("4", 16),
                ]
            )
            body = pre + dg(ln - len(pre) - 1)
            chk = next(c for c in "0123456789" if luhn_ok(body + c))
            s = body + chk
            if ln == 16:
                print(
                    s,
                    " ".join(s[i : i + 4] for i in range(0, 16, 4)),
                    "-".join(s[i : i + 4] for i in range(0, 16, 4)),
                    sep="   ",
                )
            else:
                print(s, "%s %s %s" % (s[:4], s[4:10], s[10:]), sep="   ")
        elif kind == "iban":
            cc, bban = rng.choice(
                [
                    (
                        "GB",
                        lambda: rng.choice(["NWBK", "BARC", "LOYD", "HBUK"])
                        + dg(14),
                    ),
                    ("DE", lambda: dg(18)),
                    (
                        "NL",
                        lambda: rng.choice(["RABO", "INGB", "ABNA"]) + dg(10),
                    ),
                    ("IE", lambda: rng.choice(["AIBK", "BOFI"]) + dg(14)),
                    ("FR", lambda: dg(23)),
                ]
            )
            b = bban()
            for k in range(2, 99):
                s = "%s%02d%s" % (cc, k, b)
                if iban_ok(s):
                    break
            print(
                s,
                " ".join(s[i : i + 4] for i in range(0, len(s), 4)),
                sep="   ",
            )
        elif kind == "aba":
            while True:
                s = rng.choice(
                    [
                        "01",
                        "02",
                        "03",
                        "04",
                        "05",
                        "06",
                        "07",
                        "08",
                        "09",
                        "10",
                        "11",
                        "12",
                    ]
                ) + dg(7)
                if aba_ok(s):
                    break
            print(s)
        elif kind == "sin":
            body = str(rng.randrange(1, 8)) + dg(7)
            s = body + next(c for c in "0123456789" if luhn_ok(body + c))
            print(
                s,
                "%s-%s-%s" % (s[:3], s[3:6], s[6:]),
                "%s %s %s" % (s[:3], s[3:6], s[6:]),
                sep="   ",
            )
        elif kind == "ssn":
            while True:
                s = "%03d%02d%04d" % (
                    rng.randrange(1, 900),
                    rng.randrange(1, 100),
                    rng.randrange(1, 10000),
                )
                if ssn_ok(s):
                    break
            print(
                s,
                "%s-%s-%s" % (s[:3], s[3:5], s[5:]),
                "%s %s %s" % (s[:3], s[3:5], s[5:]),
                sep="   ",
            )
        else:
            sys.exit("unknown mint kind")


# ------------------------------------------------------------------ main


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch")
    ap.add_argument("--out", default=os.path.join(HERE, "corpus"))
    ap.add_argument("--caps", action="store_true")
    ap.add_argument("--mint")
    ap.add_argument("-n", type=int, default=5)
    ap.add_argument("--salt", default="x")
    a = ap.parse_args()
    if a.mint:
        mint(a.mint, a.n, a.salt)
        return

    names = sorted(
        os.path.basename(p)[:-3]
        for p in glob.glob(os.path.join(HERE, "corpus_src", "batch_*.py"))
    )
    if a.batch:
        names = ["batch_" + a.batch]
    docs = []
    for nm in names:
        docs += importlib.import_module("corpus_src." + nm).DOCS
    docs.sort(key=lambda d: d["id"])

    out = os.path.abspath(a.out)
    for sub in ("docs", "keys", ".build"):
        p = os.path.join(out, sub)
        shutil.rmtree(p, ignore_errors=True)
        os.makedirs(p)

    errors, warnings, pdf_jobs, keys = [], [], [], []
    seen = set()
    for d in docs:
        if d["id"] in seen:
            errors.append("duplicate doc id %s" % d["id"])
        seen.add(d["id"])
        try:
            keys.append(build_doc(d, out, errors, warnings, pdf_jobs, a.caps))
        except Exception as e:  # keep going so every problem is listed
            errors.append(
                "doc-%03d: build failed: %s: %s"
                % (d["id"], type(e).__name__, e)
            )
    docx_to_pdf(pdf_jobs, errors)
    shutil.rmtree(os.path.join(out, ".build"), ignore_errors=True)

    manifest = [
        dict(
            id=k["id"],
            file=k["file"],
            format=k["format"],
            doc_type=k["doc_type"],
            audience=k["audience"],
            jurisdiction=k["jurisdiction"],
            word_count=k["word_count"],
            item_count=len(k["items"]),
        )
        for k in keys
    ]
    with open(
        os.path.join(out, "manifest.json"), "w", encoding="utf-8", newline="\n"
    ) as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
        f.write("\n")

    # ---- report
    def tally(fn):
        t = {}
        for k in keys:
            t[fn(k)] = t.get(fn(k), 0) + 1
        return dict(sorted(t.items()))

    total = sum(len(k["items"]) for k in keys)
    hard = sum(1 for k in keys for i in k["items"] if i["difficulty"] == "hard")
    print("documents: %d" % len(keys))
    print("by format: %s" % tally(lambda k: k["format"]))
    print("by audience: %s" % tally(lambda k: k["audience"]))
    print("by jurisdiction: %s" % tally(lambda k: k["jurisdiction"]))
    print("doc types: %d distinct" % len(set(k["doc_type"] for k in keys)))
    print("word counts: %s" % " ".join(str(k["word_count"]) for k in keys))
    print(
        "items: %d total, %d hard (%.1f%%)"
        % (total, hard, 100.0 * hard / max(1, total))
    )
    print("category: items / documents")
    for c in CATEGORIES:
        ni = sum(1 for k in keys for i in k["items"] if i["category"] == c)
        nd = sum(1 for k in keys if any(i["category"] == c for i in k["items"]))
        print("  %-20s %5d / %3d" % (c, ni, nd))
    for w in warnings:
        print("WARN " + w)
    for e in errors:
        print("ERROR " + e)
    print(
        "generate: %d documents, %d items, %d warnings, %d errors"
        % (len(keys), total, len(warnings), len(errors))
    )
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
