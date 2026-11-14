# Copyright 2026 B Parsons
# SPDX-License-Identifier: Apache-2.0

"""Check the two ways of choosing what is replaced, in a headless browser (no on-device model needed).

Usage: python3 tools/check_modes.py OUT_DIR [URL]
Saves screenshots and prints what was found. Needs the dev server (default http://127.0.0.1:5173/).
"""

import subprocess
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
URL = sys.argv[2] if len(sys.argv) > 2 else "http://127.0.0.1:5173/"
PROFILE = Path.home() / ".cache/client-safe-ai-chrome"
problems = []

# Real Chrome attached over CDP, as in shoot_app.py: the bundled headless browser cannot paint
# this app on every machine (its GPU process crashes).
chrome = subprocess.Popen(
    [
        "google-chrome",
        f"--user-data-dir={PROFILE}",
        "--remote-debugging-port=9333",
        "--remote-debugging-address=127.0.0.1",
        "--no-first-run",
        "--no-default-browser-check",
        "about:blank",
    ],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
time.sleep(4)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://127.0.0.1:9333")
    ctx = browser.contexts[0]
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.set_viewport_size({"width": 1280, "height": 1000})
    page.on("pageerror", lambda e: problems.append(f"pageerror: {e}"))
    page.on(
        "console",
        lambda m: (
            problems.append(f"console {m.type}: {m.text}")
            if m.type == "error"
            else None
        ),
    )
    page.goto(URL)
    page.wait_for_selector("md-filled-button")
    page.get_by_text("Use a sample document").click()

    tabs = page.locator("md-secondary-tab")
    print("tabs:", [t.strip() for t in tabs.all_inner_texts()])
    tabs.nth(1).click()
    page.wait_for_timeout(500)
    print(
        "tiers:",
        [t.strip() for t in page.locator(".tier-head h3").all_inner_texts()],
    )
    rows = page.locator("md-list-item").filter(has=page.locator(".rate"))
    print("rows:", rows.count())
    for i in range(rows.count()):
        r = rows.nth(i)
        print(
            "  ",
            r.locator("[slot=trailing-supporting-text]")
            .inner_text()
            .strip()
            .ljust(12),
            r.locator("[slot=headline]").inner_text().strip(),
        )
    page.screenshot(path=str(OUT / "classes-all.png"), full_page=True)
    print("status:", page.locator("p[role=status]").first.inner_text().strip())

    page.locator("md-filter-chip", has_text="Highly accurate only").click()
    page.wait_for_timeout(400)
    checked = page.evaluate(
        "[...document.querySelector('redactobot-app').renderRoot.querySelectorAll('md-list-item md-checkbox')].filter(c => c.checked).length"
    )
    print("checked after 'Highly accurate only':", checked)
    page.screenshot(path=str(OUT / "classes-high.png"), full_page=True)

    # Phones only: the review screen should highlight the phone number and nothing else.
    page.evaluate(
        """() => { const app = document.querySelector('redactobot-app'); app.setClasses(['phone']); }"""
    )
    page.wait_for_timeout(300)
    page.locator("md-filled-button").first.click()
    page.wait_for_timeout(1500)
    marks = page.locator(".hl").all_inner_texts()
    print("highlights with phones only:", marks)
    page.screenshot(path=str(OUT / "review-phones-only.png"), full_page=True)

    # The choice survives a reload, and "By rule" still works.
    page.reload()
    page.wait_for_selector("md-filled-button")
    saved = page.evaluate(
        "JSON.parse(localStorage.getItem('redactobot.rules.v1'))"
    )
    print("saved:", saved.get("pickBy"), saved.get("classes"))
    page.locator("md-secondary-tab").nth(0).click()
    page.wait_for_timeout(400)
    print("rule rows:", page.locator("md-list-item md-icon-button").count())
    page.screenshot(path=str(OUT / "rules.png"), full_page=True)
    page.evaluate(
        "localStorage.removeItem('redactobot.rules.v1')"
    )  # leave the test profile as it was found
    browser.close()
chrome.terminate()

print("problems:", problems or "none")
