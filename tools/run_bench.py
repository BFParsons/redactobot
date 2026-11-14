# Copyright 2026 B Parsons
# SPDX-License-Identifier: Apache-2.0

"""Run the benchmark page (bench/index.html) in real Chrome and save results.

Usage: python3 tools/run_bench.py OUT.json [EXTRA_CHROME_ARG ...]

Expects the repository to be served on http://127.0.0.1:3000 (npm run bench).
Chrome is launched directly and attached over CDP, because Playwright's own
launch switches stop Gemini Nano from loading. Writes OUT.json and a
full-page screenshot next to it.
"""

import json
import subprocess
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(sys.argv[1])
EXTRA = sys.argv[2:]  # extra chrome args
PROFILE = Path.home() / ".cache/client-safe-ai-chrome"


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


# Launch real Chrome ourselves: Playwright's default switches (--disable-component-update,
# --disable-background-networking) stop Chrome from fetching Gemini Nano.
chrome = subprocess.Popen(
    [
        "google-chrome",
        f"--user-data-dir={PROFILE}",
        "--remote-debugging-port=9333",
        "--remote-debugging-address=127.0.0.1",
        "--no-first-run",
        "--no-default-browser-check",
        *EXTRA,
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
    page.set_viewport_size({"width": 1200, "height": 900})
    console = []
    page.on("console", lambda m: console.append(f"{m.type}: {m.text}"))
    page.goto("http://127.0.0.1:3000/bench/")
    page.wait_for_function(
        "!document.getElementById('envStatus').textContent.startsWith('Checking')",
        timeout=30000,
    )
    result = {"chrome": browser.version, "env": page.inner_text("#envStatus")}
    log("env:", result["env"])

    page.click("#runPatterns")
    result["patterns"] = page.inner_text("#patternOut")
    log("patterns done")

    if page.is_disabled("#runModel"):
        result["model"] = "skipped: button disabled"
    else:
        page.click("#runModel")
        deadline = time.time() + 60 * 60
        last = ""
        while time.time() < deadline:
            done = page.evaluate(
                """() => !document.getElementById('runModel').disabled"""
            )
            prog = page.inner_text("#dlText")
            if prog and prog != last:
                log(prog)
                last = prog
            if done:
                break
            time.sleep(5)
        result["sessionInfo"] = page.inner_text("#sessionInfo")
        result["model"] = page.inner_text("#modelOut")
        result["raw"] = page.evaluate(
            """() => [...document.querySelectorAll('#modelOut pre')].map(p => p.textContent)"""
        )
    result["console"] = console
    page.screenshot(path=str(OUT.with_suffix(".png")), full_page=True)
    OUT.write_text(json.dumps(result, indent=2))
    log("DONE")
    browser.close()
chrome.terminate()
chrome.wait(timeout=30)
