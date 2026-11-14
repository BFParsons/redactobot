# Copyright 2026 B Parsons
# SPDX-License-Identifier: Apache-2.0

"""Drive the app in real Chrome and save screenshots of each screen.

Usage: python3 tools/shoot_app.py OUT_DIR [URL]
Chrome is launched normally and attached over CDP, because Playwright's own launch
switches stop Gemini Nano from loading (see bench/RESULTS.md).
"""

import subprocess
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
URL = sys.argv[2] if len(sys.argv) > 2 else "http://127.0.0.1:4173/"
PROFILE = Path.home() / ".cache/client-safe-ai-chrome"

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
log = []
try:
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9333")
        ctx = browser.contexts[0]
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.on(
            "console",
            lambda m: (
                log.append(f"{m.type}: {m.text}")
                if m.type in ("error", "warning")
                else None
            ),
        )
        page.on("pageerror", lambda e: log.append(f"pageerror: {e}"))
        requests = []
        page.on("request", lambda r: requests.append(r.url))

        def shot(name, full=True):
            page.wait_for_timeout(600)
            page.screenshot(path=str(OUT / f"{name}.png"), full_page=full)

        page.set_viewport_size({"width": 1280, "height": 900})
        page.goto(URL)
        page.wait_for_selector("md-filled-button")
        shot("1-compose-empty")
        page.get_by_text("Use a sample document").click()
        shot("2-compose-sample")
        page.locator("md-list-item md-icon-button").first.click()
        shot("3-rule-dialog", full=False)
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)
        page.get_by_text("Find private details").click()
        page.wait_for_timeout(1500)
        shot("4-review-scanning")
        t0 = time.time()
        while time.time() - t0 < 240:
            if not page.locator("md-linear-progress").count():
                break
            time.sleep(2)
        print(f"scan finished after {time.time() - t0:.0f}s")
        shot("5-review-done")
        print("NOTICE:", page.locator(".notice").first.inner_text())
        print(
            "FOUND:",
            " | ".join(
                page.locator(
                    "aside md-list-item [slot=headline]"
                ).all_inner_texts()
            ),
        )
        page.get_by_text("What the cloud will see", exact=True).click()
        shot("6-review-cloud-view")
        print("CLOUD VIEW:\n" + page.locator(".doc").inner_text())
        ctx.grant_permissions(["clipboard-read", "clipboard-write"])
        page.get_by_text("Copy replaced text").click()
        page.wait_for_timeout(400)
        clip = page.evaluate("navigator.clipboard.readText()")
        print(
            "COPY:",
            (
                "PASS"
                if clip == page.locator(".doc").inner_text()
                or "[PERSON_1]" in clip
                and "Margaret" not in clip
                else "FAIL"
            ),
            len(clip),
            "chars",
        )
        shot("6b-review-copied")
        page.get_by_text("Your document", exact=True).click()
        page.emulate_media(color_scheme="dark")
        shot("7-review-dark")
        page.emulate_media(color_scheme="light")
        page.set_viewport_size({"width": 400, "height": 800})
        shot("8-review-compact")
        page.set_viewport_size({"width": 700, "height": 900})
        shot("9-review-medium")
        outside = sorted(
            {
                u.split("/")[2]
                for u in requests
                if u.startswith("http") and "127.0.0.1" not in u
            }
        )
        print("REQUESTS TO OTHER HOSTS:", outside or "none")
        browser.close()
finally:
    chrome.terminate()
    chrome.wait(timeout=30)
print("CONSOLE:", log or "clean")
