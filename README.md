```text
██████╗ ███████╗██████╗  █████╗  ██████╗████████╗ ██████╗ ██████╗  ██████╗ ████████╗
██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗██╔═══██╗╚══██╔══╝
██████╔╝█████╗  ██║  ██║███████║██║        ██║   ██║   ██║██████╔╝██║   ██║   ██║
██╔══██╗██╔══╝  ██║  ██║██╔══██║██║        ██║   ██║   ██║██╔══██╗██║   ██║   ██║
██║  ██║███████╗██████╔╝██║  ██║╚██████╗   ██║   ╚██████╔╝██████╔╝╚██████╔╝   ██║
╚═╝  ╚═╝╚══════╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝    ╚═╝
```

```text
        ┌──┐            ┌──┐
        │  │            │  │        user@redactobot:~$ paste client-notes.txt
     ┌──┴──┴────────────┴──┴──┐
     │  ┌──────────────────┐  │      Met with ████████████████ about the
     │  │   ▄██▄    ▄██▄   │  │      ██████████████ filing. Call ████████████.
     │  │   ▀██▀    ▀██▀   │  │
     │  │       ▀▀▀▀       │  │      > 3 private details removed on this device
     │  └──────────────────┘  │      > nothing left your computer
     │  ▓▓▓▓  [REDACTED]   o  │      > safe to paste into your AI chat
     └────────────────────────┘
```

<div align="center">

**Scrub private details out of your text *before* an AI ever sees them.**
On your device. In your browser. Before you hit paste.

**Try it: [redactobot.org](https://redactobot.org)** (desktop Chrome)

`v0.3.0` · `Apache-2.0` · `Chrome 148+` · `Firebase AI Logic` · `Gemini Nano + Gemini` · built for **#BuildHybridAI 2026**

</div>

---

## `$ redactobot --help`

```text
USAGE
    Paste into ChatGPT, Claude or Gemini    ->  the Chrome extension cleans it first
    Open a document in the web app          ->  review, clean, copy, ask or release

WHAT IT REMOVES
    names · companies · emails · phones · addresses · government IDs
    bank and card numbers · passwords · IP and device IDs · dates · money amounts
    health details and other sensitive personal facts

WHERE IT RUNS
    Step 1  on your device     pattern rules + Gemini Nano (Chrome's built-in AI)
    Step 2  in the cloud       optional, and only ever sees the already-scrubbed text

WHAT IT NEVER DOES
    send your raw text anywhere · press Send for you
    claim the result is perfectly anonymous
```

## `$ redactobot --what`

Lawyers, accountants, FOIA officers and anyone else with confidential text want to use AI
chatbots, and can't paste client details into them. Redactobot sits between your clipboard
and the chatbot:

```text
"Met with Margaret Whitfield (margaret@whitfield.example, 604-555-0142)."
                                   │
                             [ REDACTOBOT ]      <- runs locally, in Chrome
                                   │
"Met with [PERSON_1] ([EMAIL_1], [PHONE_1])."
```

The chatbot gets the placeholders. You keep the real values. In the document app, the
answer comes back with the real names restored on your device.

It comes in two parts:

| | What it is | Use it for |
|---|---|---|
| **Chrome extension** | A `Redactobot` switch under the chat box on ChatGPT, Claude and Gemini | Everyday pasting into AI chats |
| **Web app** | A full review screen for documents and long text | Files, careful review, cloud Q&A, FOIA releases |

## `$ redactobot --how`

Hybrid AI as a **pipeline**, not a fallback. The two models do different jobs, and the
private one always goes first.

```text
   YOUR TEXT
       │
       v
 ┌───────────────────────────── ON YOUR DEVICE ──────────────────────────────┐
 │ 1. RULES     29 pattern detectors with real checksums (Luhn, IBAN,        │
 │              routing, SSN ranges), name-cue rules, offline place list     │
 │ 2. ROUTER    do the rules explain every possible name? if yes, skip AI    │
 │ 3. NANO      Gemini Nano finds the names, places and sensitive facts      │
 │              the rules can't. InferenceMode.ONLY_ON_DEVICE. No fallback.  │
 │ 4. REVIEW    you see every replacement and can change any of them         │
 │ 5. REPLACE   [PERSON_1], [ACCOUNT_2] ... the mapping stays in memory      │
 └────────────────────────────────────┬──────────────────────────────────────┘
                                      │  placeholders only
                                      v
 ┌───────────────────────── OPTIONAL, IN THE CLOUD ──────────────────────────┐
 │ 6. CLEANUP   Gemini removes leftover sensitive facts (e.g. conditions)    │
 │ 7. ASK       Gemini answers your question about the scrubbed text         │
 │              InferenceMode.ONLY_IN_CLOUD, behind Firebase App Check       │
 └────────────────────────────────────┬──────────────────────────────────────┘
                                      v
 ┌───────────────────────────── ON YOUR DEVICE ──────────────────────────────┐
 │ 8. RESTORE   real values are put back into the answer, locally            │
 └───────────────────────────────────────────────────────────────────────────┘
```

Every AI call, on-device and cloud, goes through **Firebase AI Logic** (`firebase/ai`).

**The rules that don't bend**

```text
[+] Raw text never goes to the cloud. Detection has no cloud fallback.
[+] If a needed local check can't finish, the paste is held, not sent.
[+] The cloud only ever receives placeholder text, and you see the exact text first.
[+] The placeholder-to-real-value mapping is never saved or sent anywhere.
[+] The extension never presses Send.
[+] The site turns off camera, microphone, location and other browser features
    it never uses, and is served over HTTPS only.
[!] Removing names does not guarantee anonymity. Always read the result.
```

## `$ redactobot install`

**You need:** Node 24.15+ (or 26+), desktop Chrome 148+, and a computer that can run Gemini
Nano (about 22 GB free disk, and 16 GB RAM or a GPU with more than 4 GB of memory).

```sh
git clone https://github.com/BFParsons/redactobot.git
cd redactobot
npm install
```

### Web app

The hosted copy is at **https://redactobot.org**. To run it yourself:

```sh
npm run dev          # → http://127.0.0.1:5173
```

Local detection, review and replacement work with no Firebase setup at all.

### Chrome extension

**The quick way: download it.**

1. Download `redactobot-extension-0.3.0.zip` from the
   [latest release](https://github.com/BFParsons/redactobot/releases/latest) and unzip it.
2. Open `chrome://extensions` and turn on **Developer mode** (top right).
3. Click **Load unpacked** and choose the unzipped folder.
4. Open ChatGPT, Claude or Gemini and switch **Redactobot** on under the chat box.

This is the same package submitted to the Chrome Web Store. It makes no network requests
and asks only for `storage` and `offscreen`; cloud cleanup is on the website, not in the
extension.

**Or build it yourself:**

```sh
npm run build:extension      # development build → extension/build
npm run package:extension    # the published build, zipped → extension/releases
```

Load `extension/build` the same way. In the extension's settings, click **Prepare
on-device AI**, then **Test a fictional paste**, and refresh any open chat tabs. The
development build can use cloud cleanup with your own Firebase project and an App Check
debug token; the published build cannot, by design.

### Cloud cleanup (optional)

1. Create a Firebase project with a Web app. Enable **AI Logic** with the **Gemini Developer API**.
2. Copy `.env.example` to `.env.local` and fill in the Firebase web app settings.
3. For local testing, create an **App Check debug token** in the Firebase console and set
   `VITE_APPCHECK_DEBUG_TOKEN` to it.
4. Restart `npm run dev`, or rebuild and reload the extension.

The cloud model defaults to `gemini-3.5-flash-lite` (`VITE_CLOUD_MODEL` changes it).

> Keep `.env.local` and debug tokens private. Never publish a build that contains a debug
> token; a public release needs production App Check.

## `$ redactobot guide --extension`

```text
 ChatGPT / Claude / Gemini
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │ Message...                                                                  │
 │                                                                             │
 │  Herding the tensors...    0:23  ████░░░░░░    Redactobot [ON]   Data types │
 └─────────────────────────────────────────────────────────────────────────────┘
```

1. **Switch it on.** The `Redactobot` switch under the chat box starts **Off** on every page
   load and only affects that tab. Nothing loads until you switch it on.
2. **Wait for the bar, if there is one.** After a break, Chrome needs a minute or two to
   load its on-device model. A progress bar in the site's own colours shows it, with a
   rotating set of fifty loading messages ("Triangulating the parabolas…") to pass the
   time. The bar only moves forward. Switch off and loading stops at once.
3. **Paste as usual.** Clear private details are swapped for placeholders before the text
   reaches the chat box. This usually takes well under two seconds.
4. **Review when asked.** If something is uncertain, a small review opens. Choose
   **Use this text** to paste your edited version, or **Ignore** to paste the original.
5. **Choose what to check.** **Data types** opens 12 categories, from names to indirect
   identity clues. Pattern-only choices never wake the AI model.

Settings also offer **Load on-device AI when Chrome starts** (off by default) and optional
cloud cleanup. The extension checks **pasted and dropped text** only: not typing, file
uploads or images.

## `$ redactobot guide --app`

1. **Add text.** Paste notes or open a file. Supported: PDF (with text), Word, Excel,
   PowerPoint, OpenDocument, RTF, `.eml`, HTML, CSV and plain text. Files are read on your
   device and never uploaded. No document to hand? **Use a sample document** cycles through
   thirty fictional ones, such as a Death Star workplace incident report, a House Atreides
   relocation claim and Dr. Jones's faculty expense review.
2. **Pick what to replace.** Choose by **Data type** (sorted by measured accuracy) or by
   **Regulatory** rule: HIPAA Safe Harbor, Fed. R. Civ. P. 5.2, IRC § 7216, GLBA, CCPA,
   PCI DSS, GDPR and NIST SP 800-122. FOIA release is in the same list.
3. **Find private details.** The cleaned text types out live. Placeholders are highlighted;
   sensitive topics that were flagged but not removed show in red, and one click removes them.
4. **Read the verdict.** Green: it looks clean. Orange: something needs your eye first.
5. **Use it.** Copy the cleaned text into any AI chat, or prepare an exact preview and run
   cloud cleanup and a question. Real values are restored in the answer locally.

### While the model starts

Chrome can take a minute or two to load its on-device model after a break. The app starts
loading it as soon as the page opens and shows a progress card, so a scan never begins
half-ready. While you wait:

```text
 Folding the matrices into swans...
 ████████████░░░░░░░░░░░░░░░░░░░░   About 38%   0:29
 Your local AI is getting set up. It will take a moment.
 In the meantime, why not listen to smooth jazz?      [ > Play smooth jazz ]
```

- Fifty loading messages rotate above the bar.
- **Play smooth jazz** plays "Waiting Room", an original loop synthesised in your browser.
  It stops by itself when the model is ready.
- While it plays, musical notes appear in the robot's eyes in the logo and drift away.

### FOIA release mode (US)

Switch **Output** to **FOIA release (US)** and the same detections become a release marked
the way a FOIA officer marks one:

```text
                                                        ╔═══════════════════╗
  CLIENT MEETING NOTES                                  ║ RELEASED IN PART  ║
  Prepared by ████████████ (b)(6)                       ║   (b)(4)  (b)(6)  ║
  regarding ██████████████████ (b)(4)                   ╚═══════════════════╝
```

Each withholding is a black box as long as the text it hides, labelled with its exemption
at the place of deletion (5 U.S.C. § 552(b)). Personal details default to `(b)(6)`,
business details to `(b)(4)`; a **Law enforcement record** option adds `(b)(7)(C)`. Change
any exemption per data type, or release that type. Print or save as PDF. FOIA mode never
uses the cloud. The defaults are a starting point, not a legal determination.

### Display and accessibility

Light, dark or system theme · colour-blind friendly palette · reduced motion · skip link ·
full keyboard use · screen-reader status and progress · Windows high-contrast support ·
contrast of at least 8.2:1 on status colours · a layout that works on phones.

## `$ redactobot stats`

Small development measurements on fictional documents, not a guarantee.

```text
TESTS        758 unit tests · 20 end-to-end tests on the real extension in Chromium
ACCURACY     rules + Gemini Nano, unseen test set, paste-sized text:
                 person names ........ 93.9% caught
                 critical details .... 95.1% caught
             rules alone, unseen test set, whole documents:
                 person names ........ 92.8% caught
SPEED        name-free paste ......... 1-40 ms   (rules decide; the model is skipped)
             short paste with a name . about 0.3 s
             dense 150-word paste .... about 1.3-1.4 s median (warm model, RTX 4070)
             cold start .............. 1-3 minutes after a break, with a progress bar
NETWORK      zero JavaScript network requests during local scanning
```

Method and full results: [`evaluation/`](evaluation) (accuracy, routing, speed log,
research notes) and [`bench/RESULTS.md`](bench/RESULTS.md).

## `$ redactobot limits`

```text
[!] Detection can miss details, and what remains can still identify someone.
[!] The on-device model needs desktop Chrome 148+ on capable hardware. In other
    browsers Redactobot says so, explains how to get it, and still runs the rules.
[!] No OCR: scanned documents and images are not read.
[!] The extension covers pasted and dropped text, not typing or uploads.
[!] Chat sites change their layouts; the extension may need updates.
[!] Rule lists (HIPAA, GDPR, FOIA ...) describe what each rule names. Redactobot never
    claims a document complies with any of them. See taxonomy/SOURCES.md.
[!] Installed through Developer mode; not yet on the Chrome Web Store.
```

## `$ redactobot credits`

### Open-source code that ships in Redactobot

| Package | Used for | Licence |
|---|---|---|
| [firebase](https://github.com/firebase/firebase-js-sdk) 13.3.0 | Firebase AI Logic (on-device and cloud inference), App Check | Apache-2.0 |
| [lit](https://github.com/lit/lit) 3.3.3 | Web components for the app | BSD-3-Clause |
| [@material/web](https://github.com/material-components/material-web) 2.5.0 | Material Design 3 components | Apache-2.0 |
| [pdfjs-dist](https://github.com/mozilla/pdf.js) 6.5 | Reading text from PDFs, locally | Apache-2.0 |
| [fflate](https://github.com/101arrowz/fflate) 0.8 | Unzipping Office and OpenDocument files, locally | MIT |
| [@fontsource/roboto](https://github.com/fontsource/font-files) 5.3.0 | Roboto typeface, self-hosted | OFL-1.1 |
| [@material-symbols/svg-400](https://github.com/marella/material-symbols) 0.48 | Icons (Material Symbols) | Apache-2.0 |

### Open-source tools used to build and test it

| Package | Used for | Licence |
|---|---|---|
| [vite](https://github.com/vitejs/vite) 8.3.8 | Build and dev server | MIT |
| [typescript](https://github.com/microsoft/TypeScript) 7.0.2 | Type checking | Apache-2.0 |
| [vitest](https://github.com/vitest-dev/vitest) 5.1.0 | Unit tests | MIT |
| [playwright](https://github.com/microsoft/playwright) 1.65 | End-to-end tests of the real extension | Apache-2.0 |
| [jsdom](https://github.com/jsdom/jsdom) 31 | Browser environment for unit tests | MIT |
| [prettier](https://github.com/prettier/prettier) 3.10.1 | Code formatting (Google style options) | MIT |
| [oxlint](https://github.com/oxc-project/oxc) 1.93.0 | Linting | MIT |
| [Black](https://github.com/psf/black) 26.10 | Python formatting (run separately, not installed by npm) | MIT |
| [@material/material-color-utilities](https://github.com/material-foundation/material-color-utilities) 0.3.0 | Generating the colour theme | Apache-2.0 |
| [@types/node](https://github.com/DefinitelyTyped/DefinitelyTyped) | Type definitions | MIT |
| Python with NumPy, SciPy and Pillow | Evaluation scoring and logo background removal (`tools/`) | BSD-3-Clause, HPND |

### Open data

| Data | Used for | Licence |
|---|---|---|
| [GeoNames](https://www.geonames.org/) `cities15000` | Offline list of 34,215 cities, to tell places from people | CC BY 4.0 ([notice](taxonomy/places-data.NOTICE)) |
| [US Social Security Administration baby names](https://www.ssa.gov/oact/babynames/limits.html) | Given-name list for the name rules | Public domain ([notice](src/core/given-names-ssa.NOTICE)) |
| Rule texts: 45 CFR § 164.514, Fed. R. Civ. P. 5.2, 26 CFR § 301.7216-1, 16 CFR § 314.2, Cal. Civ. Code § 1798.140, NIST SP 800-122, GDPR, PCI DSS v4.0.1, 5 U.S.C. § 552(b) | What each regulation lists | Public legal texts ([how they were checked](taxonomy/SOURCES.md)) |

### AI models and services

| | Role |
|---|---|
| **Firebase AI Logic** | The only path to both models |
| **Gemini Nano** (Chrome's built-in model, Prompt API) | On-device detection of names, places and sensitive facts |
| **Gemini** (`gemini-3.5-flash-lite` by default) | Optional cloud cleanup and answers, on scrubbed text only |
| **Firebase App Check** | Protects the cloud step |

### Research that shaped it

Ideas, not code. Confidence-routed cascades (LinkNER, arXiv 2402.10573; UCCI, arXiv
2605.18796) inspired the router that skips the AI model when the rules already explain
every possible name. Browser-side PII tools Casper (arXiv 2408.07004), Rescriber (arXiv
2410.11876) and RECAP (arXiv 2510.07551) informed the design. A small open tagger,
[masker-mini](https://huggingface.co/amsintelligence/masker-mini) (Apache-2.0), was
**tested but is not included**, so that all AI in the app runs on Firebase AI Logic.
Notes: [`evaluation/RESEARCH-FAST-PII-METHODS.md`](evaluation/RESEARCH-FAST-PII-METHODS.md),
[`evaluation/MASKER-EXPERIMENT.md`](evaluation/MASKER-EXPERIMENT.md).

### Everything else

- **Artwork.** The Redactobot logo is AI-generated (Google Gemini) and background-keyed for
  light and dark themes with `tools/key_logo.py`. The robot animation was supplied by the author.
- **Music.** "Waiting Room", the loop offered while the model starts, is an original piece written
  for this project and synthesised in the browser (`src/core/jazz.ts`). No recording is included.
- **Test data.** Every name, number and document in this repository is fictional.
- **Built with AI assistance.** Developed with AI coding assistants (OpenAI Codex and
  Anthropic's Claude Code), with all changes reviewed and tested by the author.
- **Sample documents.** The thirty built-in samples are original parody paperwork about fictional
  characters from popular films and series. They are not affiliated with or endorsed by the
  owners of those works.
- **Privacy and terms.** [redactobot.org/privacy](https://redactobot.org/privacy)
  ([source](public/privacy.html)): a technology demonstration,
  not a validated compliance tool. Do not enter real sensitive data.
- **Not legal advice.** Redactobot is a drafting aid. You remain responsible for what you share.

## `$ redactobot tree`

```text
src/core/         detection, replacement, routing, FOIA markings, file import,
                  sample documents, loading messages and the jazz loop
src/extension/    Chrome extension: paste guard, switch, background, on-device scanner
src/app.ts        the web app
public/           logo, icons, privacy policy and response headers for the site
taxonomy/         detectors, checksums, regulation lists and their sources
evaluation/       fictional test sets, scoring, accuracy and speed logs, research
bench/            in-browser benchmarks for Gemini Nano
tests/e2e/        end-to-end tests of the real extension
tools/            build scripts
extension/        manifest, settings and review pages, store listing and screenshots
wrangler.jsonc    hosting config for redactobot.org (Cloudflare, static files only)
```

```sh
npm test             # unit tests
npm run test:e2e     # the real extension in Chromium, with a stand-in model
npm run build        # web app → dist/
npm run lint         # Google-style lint (oxlint) and format check (Prettier)
npm run fix          # apply lint fixes and reformat
```

More: [change history](CHANGELOG.md) · [extension notes](extension/README.md) ·
[rule sources](taxonomy/SOURCES.md)

---

```text
user@redactobot:~$ exit
> mapping cleared from memory. nothing was saved. goodbye.
```

<div align="center">

[Apache 2.0](LICENSE) · Built for **#BuildHybridAI 2026**

</div>
