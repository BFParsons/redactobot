# Copyright 2026 The Redactobot Authors
# SPDX-License-Identifier: Apache-2.0

"""Generate import test files with real authoring tools (python-docx, openpyxl, python-pptx,
LibreOffice). All content is fictional. Run: python3 tools/make_fixtures.py
"""

import datetime
import subprocess
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "src/core/import/fixtures"
OUT.mkdir(parents=True, exist_ok=True)

# ---- Word ----
from docx import Document

d = Document()
d.sections[0].header.paragraphs[0].text = "Raman & Associates CPA"
d.sections[0].footer.paragraphs[0].text = "Confidential. File no. 2026-0147"
d.add_heading("Client meeting notes", level=1)
d.add_paragraph(
    "Met with Margaret Whitfield regarding Whitfield & Daughters Holdings Ltd."
)
p = d.add_paragraph("Her son ")
p.add_run("Tom Whitfield").bold = True
p.add_run(" joined by phone.\tFollow up: margaret@whitfieldholdings.example")
t = d.add_table(rows=3, cols=2)
for r, (a, b) in enumerate(
    [
        ("Item", "Amount"),
        ("Division sale", "$1,250,000"),
        ("Holdback", "$400,000"),
    ]
):
    t.cell(r, 0).text = a
    t.cell(r, 1).text = b
d.add_paragraph("Account 4471-889-2203 at Cascadia Credit Union.")
d.save(OUT / "sample.docx")

# ---- Excel ----
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.title = "Ledger"
ws.append(["Date", "Payee", "Amount", "Account"])
rows = [
    (
        datetime.date(2026, 3, 14),
        "Northgate Bookkeeping",
        8400,
        "4471-889-2203",
    ),
    (
        datetime.date(2026, 5, 2),
        "Harbourline Marine Supply",
        62000.5,
        "5520-114-9087",
    ),
]
for r in rows:
    ws.append(list(r))
for row in ws.iter_rows(min_row=2):
    row[0].number_format = "yyyy-mm-dd"
    row[2].number_format = '"$"#,##0.00'
ws["A5"] = "Total"
ws["C5"] = "=SUM(C2:C3)"
ws2 = wb.create_sheet("Contacts")
ws2.append(["Name", "Phone"])
ws2.append(["Daniel Okafor", "604-555-0142"])
wb.save(OUT / "sample.xlsx")

# ---- PowerPoint ----
from pptx import Presentation

prs = Presentation()
s = prs.slides.add_slide(prs.slide_layouts[1])
s.shapes.title.text = "Year-end review"
s.placeholders[1].text = (
    "Client: Margaret Whitfield\nSale to Harbourline Marine Supply"
)
s.notes_slide.notes_text_frame.text = "Mention the $62,000 warranty dispute."
s = prs.slides.add_slide(prs.slide_layouts[1])
s.shapes.title.text = "Next steps"
s.placeholders[1].text = "Call Daniel Okafor at 604-555-0142"
prs.save(OUT / "sample.pptx")

# ---- Formats LibreOffice can write from the Word file ----
for fmt in ("pdf", "odt", "rtf", "doc"):
    subprocess.run(
        [
            "soffice",
            "--headless",
            "--convert-to",
            fmt,
            "--outdir",
            str(OUT),
            str(OUT / "sample.docx"),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

# ---- A PDF with no text layer (stands in for a scan) ----
from reportlab.pdfgen import canvas

c = canvas.Canvas(str(OUT / "scanned.pdf"))
c.rect(72, 600, 300, 100, fill=1)
c.showPage()
c.save()

# ---- Email ----
(OUT / "sample.eml").write_bytes(
    b"From: Priya Raman <priya@raman-cpa.example>\r\n"
    b"To: =?UTF-8?Q?Margaret_Whitfield?= <margaret@whitfieldholdings.example>\r\n"
    b"Subject: =?UTF-8?B?WWVhci1lbmQgZmlsaW5nIOKAkyBuZXh0IHN0ZXBz?=\r\n"
    b"Date: Sat, 14 Mar 2026 09:12:00 -0700\r\n"
    b"MIME-Version: 1.0\r\n"
    b'Content-Type: multipart/alternative; boundary="b1"\r\n'
    b"\r\n"
    b"--b1\r\n"
    b'Content-Type: text/plain; charset="utf-8"\r\n'
    b"Content-Transfer-Encoding: quoted-printable\r\n"
    b"\r\n"
    b"Hi Margaret,\r\n\r\nPlease confirm the transfer of $310,500.75 from account 5520-114-9087 =\r\n"
    b"before Friday. Caf=C3=A9 meeting works for me.\r\n\r\nPriya\r\n"
    b"--b1\r\n"
    b'Content-Type: text/html; charset="utf-8"\r\n'
    b"\r\n"
    b"<p>Hi Margaret,</p><p>HTML version</p>\r\n"
    b"--b1--\r\n"
)

# ---- Web page, CSV, UTF-16 text ----
(OUT / "sample.html").write_text(
    "<!doctype html><html><head><title>Notes</title><style>p{color:red}</style>"
    "<script>var secret='should not appear';</script></head><body><h1>Meeting notes</h1>"
    "<p>Met with <b>Margaret Whitfield</b>.</p><ul><li>Account 4471-889-2203</li><li>Phone 604-555-0142</li></ul>"
    "<table><tr><td>Sale</td><td>$1,250,000</td></tr></table></body></html>",
    encoding="utf-8",
)
(OUT / "sample.csv").write_text(
    'Payee,Amount\nNorthgate Bookkeeping,"$8,400"\n', encoding="utf-8"
)
(OUT / "utf16.txt").write_bytes(
    "Client: Zoë Müller, account 4471-889-2203".encode("utf-16")
)
(OUT / "latin1.txt").write_bytes("Client: Zoë Müller".encode("cp1252"))

print("wrote", ", ".join(sorted(p.name for p in OUT.iterdir())))
