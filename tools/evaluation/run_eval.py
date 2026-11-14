# Copyright 2026 B Parsons
# SPDX-License-Identifier: Apache-2.0

"""Run the evaluation corpus through the app's real pipeline in Chrome.

Usage: python3 -P tools/evaluation/run_eval.py RUN_NAME [--no-model] [--replay OTHER_RUN] [--frameworks frcp52,glba] [--live-topics] [--no-topics] [--judge] [--only doc-001,doc-002] [--limit N]

--replay OTHER_RUN skips the model and reuses the names it returned in OTHER_RUN, so a change to
the code can be measured in seconds without model-to-model variation.

Needs the dev server (npm run dev, port 5173) and the corpus (evaluation/corpus). Each document's
result is written to evaluation/results/RUN_NAME/raw/doc-NNN.json as soon as it finishes, so the
run can be stopped and resumed: documents that already have a result are skipped.
Chrome is launched normally and attached over CDP (Playwright's own launch switches stop
Gemini Nano from loading).
"""

import base64
import json
import subprocess
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
import os  # noqa: E402

CORPUS = Path(
    os.environ.get("REDACTOBOT_CORPUS")
    or os.environ.get("CSA_CORPUS")
    or ROOT / "evaluation/corpus"
)
args = sys.argv[1:]
RUN = args[0]
USE_MODEL = "--no-model" not in args
ONLY = (
    set(args[args.index("--only") + 1].split(",")) if "--only" in args else None
)
LIMIT = int(args[args.index("--limit") + 1]) if "--limit" in args else None
REPLAY = (
    args[args.index("--replay") + 1] if "--replay" in args else None
)  # reuse names from this run
FRAMEWORKS = (
    args[args.index("--frameworks") + 1].split(",")
    if "--frameworks" in args
    else None
)  # default: all rule sets
LIVE_TOPICS = (
    "--live-topics" in args
)  # with --replay: reuse names, but ask the model for sensitive topics
NO_TOPICS = "--no-topics" in args
JUDGE = (
    "--judge" in args
)  # experiment: code first, then the model labels what is left
OUT = ROOT / "evaluation/results" / RUN / "raw"
OUT.mkdir(parents=True, exist_ok=True)
LOG = OUT.parent / "run.log"
# Point this at a static build of the harness (see vite.harness.config.ts) for long runs.
URL = (
    os.environ.get("REDACTOBOT_HARNESS_URL")
    or os.environ.get("CSA_HARNESS_URL")
    or "http://127.0.0.1:5173/tools/evaluation/harness.html"
)
PROFILE = Path.home() / ".cache/client-safe-ai-chrome"


def log(*a):
    line = time.strftime("%H:%M:%S ") + " ".join(str(x) for x in a)
    print(line, flush=True)
    with LOG.open("a") as f:
        f.write(line + "\n")


docs = json.loads((CORPUS / "manifest.json").read_text())
docs = docs["documents"] if isinstance(docs, dict) else docs
todo = [
    d
    for d in docs
    if (not ONLY or d["id"] in ONLY) and not (OUT / f"{d['id']}.json").exists()
]
if LIMIT:
    todo = todo[:LIMIT]
log(f"run={RUN} model={USE_MODEL} to_do={len(todo)} of {len(docs)}")


class NoChrome:
    """Stands in for the Chrome process when the bundled browser is used."""

    def terminate(self):
        pass

    def wait(self, timeout=None):
        pass


def session(p):
    if (REPLAY and not LIVE_TOPICS) or not USE_MODEL:
        # Nothing here needs the on-device model, so the bundled headless browser will do and
        # the real Chrome stays free for a live run. (Attaching to the real Chrome while a live run
        # is using it navigates that run's page away and loses its document.)
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_default_timeout(0)
        page.goto(URL)
        page.wait_for_function("window.redactobotEval !== undefined")
        return NoChrome(), browser, page
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
    browser = p.chromium.connect_over_cdp("http://127.0.0.1:9333")
    ctx = browser.contexts[0]
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.set_default_timeout(0)
    page.goto(URL)
    page.wait_for_function("window.redactobotEval !== undefined")
    status = page.evaluate("window.redactobotEval.status()")
    log("device model:", status)
    if status in ("unsupported", "unavailable"):
        raise SystemExit(
            f"on-device model is {status}; cannot run with the model"
        )
    page.click("#prepare")  # a real click: model loading needs a user gesture
    page.wait_for_function(
        "document.getElementById('state').textContent !== 'loading model…' && document.getElementById('state').textContent !== 'idle'"
    )
    state = page.inner_text("#state")
    if state != "ready":
        raise SystemExit(f"model did not load: {state}")
    return chrome, browser, page


with sync_playwright() as p:
    chrome, browser, page = session(p)
    done = 0
    for d in todo:
        path = CORPUS / d["file"]
        b64 = base64.b64encode(path.read_bytes()).decode()
        result = None
        for attempt in (1, 2):
            t0 = time.time()
            try:
                opts = {"model": USE_MODEL}
                if REPLAY:
                    prior = json.loads(
                        (
                            ROOT
                            / "evaluation/results"
                            / REPLAY
                            / "raw"
                            / f"{d['id']}.json"
                        ).read_text()
                    )
                    opts = {
                        "model": False,
                        "names": prior.get("names")
                        or {"people": [], "companies": []},
                    }
                    if LIVE_TOPICS:
                        opts["topics"] = "live"
                    elif prior.get("topics") is not None:
                        opts["topics"] = prior["topics"]
                if NO_TOPICS:
                    opts["topics"] = "off"
                if JUDGE:
                    opts["judge"] = True
                if FRAMEWORKS:
                    opts["frameworks"] = FRAMEWORKS
                result = page.evaluate(
                    "([n, b, o]) => window.redactobotEval.run(n, b, o)",
                    [path.name, b64, opts],
                )
                break
            except (
                Exception
            ) as err:  # browser or tab died: restart it once and retry
                log(d["id"], f"attempt {attempt} failed: {str(err)[:200]}")
                try:
                    browser.close()
                except Exception:
                    pass
                chrome.terminate()
                chrome.wait(timeout=30)
                chrome, browser, page = session(p)
        if result is None:
            result = {"harnessError": "evaluate failed twice"}
        result["id"] = d["id"]
        result["seconds"] = round(time.time() - t0, 1)
        (OUT / f"{d['id']}.json").write_text(
            json.dumps(result, ensure_ascii=False)
        )
        done += 1
        log(
            d["id"],
            d.get("format", ""),
            f"{result.get('seconds')}s",
            f"dets={len(result.get('detections', []))}",
            f"chunks={result.get('chunks')} chunkErrors={result.get('chunkErrors')}",
            result.get("importError") or result.get("harnessError") or "",
            f"[{done}/{len(todo)}]",
        )
    browser.close()
    chrome.terminate()
    chrome.wait(timeout=30)
log("RUN COMPLETE")
(OUT.parent / "DONE").write_text(time.strftime("%Y-%m-%d %H:%M:%S\n"))
