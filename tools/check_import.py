# Copyright 2026 B Parsons
# SPDX-License-Identifier: Apache-2.0

"""Check document import in a real browser: every fixture through the file picker, plus a
real drop event and a drag-over state. Usage: python3 tools/check_import.py OUT_DIR [URL]
"""

import base64
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
URL = sys.argv[2] if len(sys.argv) > 2 else "http://127.0.0.1:4173/"
FIX = Path(__file__).resolve().parent.parent / "src/core/import/fixtures"

EXPECT = {  # file -> text that must appear, or an error message fragment (prefixed with !)
    "sample.docx": "Met with Margaret Whitfield",
    "sample.xlsx": "Northgate Bookkeeping\t$8,400.00",
    "sample.pptx": "Speaker notes: Mention the $62,000",
    "sample.pdf": "Account 4471-889-2203",
    "sample.odt": "Tom Whitfield",
    "sample.rtf": "Tom Whitfield",
    "sample.eml": "Subject: Year-end filing",
    "sample.html": "Met with Margaret Whitfield.",
    "sample.csv": "Northgate Bookkeeping",
    "utf16.txt": "Zoë Müller",
    "scanned.pdf": "!looks like a scan",
    "sample.doc": "!older Office format",
}
DROP_JS = """async ({name, b64, type}) => {
  const bytes = Uint8Array.from(atob(b64), c => c.charCodeAt(0));
  const dt = new DataTransfer();
  dt.items.add(new File([bytes], name, {type}));
  const fire = (t) => window.dispatchEvent(new DragEvent(t, {dataTransfer: dt, bubbles: true, cancelable: true}));
  fire('dragenter'); fire('dragover');
  await new Promise(r => setTimeout(r, 300));
  window.__overText = document.querySelector('.dropzone').innerText;
  window.__overClass = document.querySelector('.dropzone').className;
  return {name};
}"""

failures, log, outside = [], [], set()
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    page.on(
        "console",
        lambda m: (
            log.append(f"{m.type}: {m.text}") if m.type == "error" else None
        ),
    )
    page.on("pageerror", lambda e: log.append(f"pageerror: {e}"))
    page.on(
        "request",
        lambda r: (
            outside.add(r.url.split("/")[2])
            if r.url.startswith("http") and "127.0.0.1" not in r.url
            else None
        ),
    )
    page.goto(URL)
    page.wait_for_selector(".dropzone")
    page.screenshot(path=str(OUT / "import-1-empty.png"))

    field = "md-outlined-text-field"
    for name, want in EXPECT.items():
        page.set_input_files("#file-input", str(FIX / name))
        page.wait_for_timeout(150)
        for _ in range(
            150
        ):  # poll; the page's security policy blocks injected string code
            if not page.locator(".app-bar md-linear-progress").count():
                break
            page.wait_for_timeout(200)
        page.wait_for_timeout(300)
        value = page.eval_on_selector(field, "e => e.value")
        error = (
            page.locator(".notice.warn").inner_text()
            if page.locator(".notice.warn").count()
            else ""
        )
        chip = (
            page.eval_on_selector("md-input-chip", "e => e.label")
            if page.locator("md-input-chip").count()
            else ""
        )
        ok = (
            (want[1:] in error)
            if want.startswith("!")
            else (want in value and chip == name and not error)
        )
        print(
            f"{'PASS' if ok else 'FAIL'}  {name:13} chip={chip or '-':13} words={len(value.split()):4} error={error.strip()[:70] or '-'}"
        )
        if not ok:
            failures.append(name)
        if name == "sample.xlsx":
            page.screenshot(path=str(OUT / "import-2-added.png"))
        if name == "scanned.pdf":
            page.screenshot(path=str(OUT / "import-3-error.png"))

    # Remove the document with the chip's remove button.
    page.set_input_files("#file-input", str(FIX / "sample.docx"))
    page.wait_for_selector("md-input-chip")
    page.locator("md-input-chip").evaluate(
        "e => e.shadowRoot.querySelector('button.trailing.action, .trailing.action').click()"
    )
    page.wait_for_timeout(300)
    cleared = (
        page.locator("md-input-chip").count() == 0
        and page.eval_on_selector(field, "e => e.value") == ""
    )
    print(f"{'PASS' if cleared else 'FAIL'}  remove chip clears the document")
    if not cleared:
        failures.append("remove")

    # Real drag-over state, then a real drop.
    data = (FIX / "sample.pdf").read_bytes()
    page.evaluate(
        DROP_JS,
        {
            "name": "dropped.pdf",
            "b64": base64.b64encode(data).decode(),
            "type": "application/pdf",
        },
    )
    zone = page.locator(".dropzone")
    over = (
        "over" in (zone.get_attribute("class") or "")
        and "Drop the document" in zone.inner_text()
    )
    page.screenshot(path=str(OUT / "import-4-dragover.png"))
    page.evaluate(
        """async ({name, b64, type}) => {
      const bytes = Uint8Array.from(atob(b64), c => c.charCodeAt(0));
      const dt = new DataTransfer(); dt.items.add(new File([bytes], name, {type}));
      window.dispatchEvent(new DragEvent('drop', {dataTransfer: dt, bubbles: true, cancelable: true}));
    }""",
        {
            "name": "dropped.pdf",
            "b64": base64.b64encode(data).decode(),
            "type": "application/pdf",
        },
    )
    page.wait_for_selector("md-input-chip")
    page.wait_for_timeout(300)
    dropped = page.eval_on_selector(
        "md-input-chip", "e => e.label"
    ) == "dropped.pdf" and "Account 4471-889-2203" in page.eval_on_selector(
        field, "e => e.value"
    )
    still_here = page.url.rstrip("/") == URL.rstrip("/")
    print(f"{'PASS' if over else 'FAIL'}  drag-over highlights the drop zone")
    print(f"{'PASS' if dropped else 'FAIL'}  dropping a PDF adds it")
    print(
        f"{'PASS' if still_here else 'FAIL'}  the browser did not navigate to the dropped file"
    )
    for label, good in (
        ("dragover", over),
        ("drop", dropped),
        ("navigate", still_here),
    ):
        if not good:
            failures.append(label)

    page.set_viewport_size({"width": 400, "height": 800})
    page.screenshot(path=str(OUT / "import-5-compact.png"))
    browser.close()

print("REQUESTS TO OTHER HOSTS:", sorted(outside) or "none")
print("CONSOLE ERRORS:", log or "none")
print("FAILURES:", failures or "none")
sys.exit(1 if failures else 0)
