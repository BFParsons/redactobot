# Change history

## Unreleased

### Without the on-device model, and a cloud answer fix

- **Notice for visitors without the on-device model.** The first screen now says when on-device AI is
  not available and why (another browser, a phone or tablet, an old Chrome, the feature switched off,
  hardware that cannot run it, or a model not yet downloaded), what still works (the pattern rules)
  and what to check by hand. **How to get on-device AI** opens steps for that visitor's situation.
  The review screen's "Names were not checked" warning links to the same steps
  (`src/core/model-help.ts`).
- **Fix: the cloud model refused to answer.** Asked a question about cleaned text, it replied that the
  document "contains only placeholders". Its instructions said never to guess placeholder values and
  to explain when information was removed, which it read as a reason to decline. The new instructions
  tell it to treat each placeholder as the real value, use placeholders in its answer exactly as
  written (the device restores the real values) and never refuse because details were replaced.
  Checked against the live model: it now summarises and lists the people involved, with names
  restored locally.

### Web app: the logo reloads the page

- Clicking the Redactobot logo (top left) reloads the page for a fresh start, clearing the text and
  any results. It is a real link to the home page, so it works from the keyboard, and a middle-click
  or Ctrl/Cmd-click opens a new tab instead.

### Twenty more sample documents

- **Use a sample document** now cycles through thirty fictional, comical documents. The twenty new
  ones are parody paperwork about The Lord of the Rings, Jaws, The Terminator, Alien, The Godfather,
  Home Alone, Die Hard, The Wizard of Oz, Titanic, Top Gun, Shrek, Toy Story, Finding Nemo, Mad Max,
  Rocky, Ferris Bueller's Day Off, The Princess Bride, Monty Python and the Holy Grail, The Big
  Lebowski and Groundhog Day. Original wording throughout; contact details use reserved test ranges.

### Extension: a build for publication

- `npm run package:extension` builds the extension for the Chrome Web Store and GitHub releases and
  zips it. The published build has no Firebase project and no App Check debug token, asks for no
  host permissions and cannot connect to any server (`connect-src 'none'`): it checks pastes on the
  device only. The packaging step refuses to zip a build that contains a Firebase key.
- In an extension without cloud access, settings now say "Cloud cleanup is not part of the extension
  … use redactobot.org" instead of asking for a debug token.
- `E2E_PUBLIC=1 npm run test:e2e` runs the end-to-end tests against the published variant.
- Store listing text, permission justifications, data-use answers and reviewer notes are in
  `extension/STORE-LISTING.md`; five 1280 × 800 screenshots and two promo images are in
  `extension/store/`.
- The web app links to the extension download, and has a GitHub icon in its header that opens the
  latest release (the extension zip and the source code).

### Names: fewer false alarms, surname particles, and a startup fix

- **Not names any more:** everyday phrases in capitals ("this Past Weekend", "Game Seven", "Happy New
  Year") and countries and continents ("America", "South America", "Team America"). "America" is on
  the public baby-name list, and two capitalized words in mid-sentence were assumed to be a person.
  New lists of everyday words and large places (`src/core/common-words.ts`) veto guesses that rest
  only on capital letters, in the rules, in the "Worth a look" list and for names the on-device model
  reports. Countries and continents are also no longer treated as places smaller than a state.
- **Now found:** names with a lower-case surname particle, anywhere in a sentence: "Nik van der
  Giesen", "Ludwig von Hartmann", "Pieter van den Berg", "Anna de la Cruz", "Sofia di Marco".
  "Tour de France" and "the van der Waals force" are left alone.
- People whose names are also places or everyday words are still found ("India Wilson", "Kenya
  Moore", "Jordan Smith", "Sarah Green"), as are unfamiliar company names ("Payworks Midwest").
- Measured on both test sets, with and without the model: recall is unchanged on every category;
  text removed that was not in the answer key fell (unseen set, whole documents: 7.2% to 6.6%).
- **Fix (extension):** the first paste after startup could stop with "The local scanner could not
  start." Switching on and pasting both asked for the scanner; the second saw none yet and failed to
  create a duplicate. Callers now share one attempt, and the first message is retried briefly if the
  new scanner is not listening yet. This was the cause of an intermittent end-to-end test failure.

### Cold start: the bar no longer restarts; loading messages

- **Fix (extension):** during a long cold start the progress bar under the chat box stopped and
  began again from zero. The once-a-minute keep-alive cancelled the load request that was still
  running and sent a new one, and a 155-second timeout did the same. A running load is now left
  alone; if it times out or the background worker restarts, the extension asks again without
  resetting the bar. Progress only moves forward.
- Fifty light-hearted loading messages ("Calculating the square root of infinity…") rotate above the
  bar every few seconds, in a fresh random order each time, in the extension and the web app. The
  first line still says plainly what is happening, and screen readers hear the plain status once.
- The estimate now eases towards 95% over about three minutes instead of stalling after one.

### Smooth jazz while the model starts

- The cold-start card now reads "Your local AI is getting set up. It will take a moment. In the
  meantime, why not listen to smooth jazz?" with a **Play smooth jazz** button. The music stops by
  itself when the model is ready, or when paused.
- The music is "Waiting Room", an original eight-bar loop written as data in `src/core/jazz.ts` and
  synthesised with the Web Audio API (electric piano, bass, a reed lead, brushes). There is no audio
  file and no third-party recording or arrangement.
- While it plays, notes sit in the robot's eyes in the logo and fainter notes drift up and fade.
  Reduced motion keeps the notes still.

### Copyright, privacy law and contact

- Licence headers now read `Copyright 2026 B Parsons`.
- The privacy policy names the operator, adds a section on Canadian privacy law (PIPEDA: accountability,
  consent, processing outside Canada, access and correction, complaints to the Privacy Commissioner)
  and gives a contact email. The address is assembled by a small script so it does not appear in the
  page source.

### Hosting

- The web app is hosted at https://redactobot.org (Cloudflare static hosting, `wrangler.jsonc`;
  response headers from `public/_headers`). The extension's card links to the privacy policy there.

### Web app: browser features blocked by default

- The web app now sends a `Permissions-Policy` header (hosted site via `firebase.json`, local server
  via `vite.config.ts`, one shared value) that switches off 26 browser features it never uses:
  camera, microphone, location, Bluetooth, USB, payment, screen capture, clipboard reading and more.
  Only clipboard writing (the Copy buttons) and muted autoplay (the robot animation) stay allowed.

### Fixes from the code review

- **Extension scanner:** the offscreen scanner now accepts commands only from the extension's own
  contexts (background worker, extension pages). Content scripts share the extension's id and run
  inside the chat sites, so they must go through the background worker's checks
  (`fromExtensionContext` in `src/extension/protocol.ts`).
- **FOIA boxes:** a redaction box is now exactly as long as the text it hides, with no cap, on screen,
  in print and in "Copy as text". Long boxes wrap where the text did. Before, the on-screen box
  stopped at 48 characters and the copied text at 40, while the comments said the length matched.
- **Zip size limits:** confirmed with a crafted archive that an entry can never unpack to more than
  the size it declares (the unzip library stops there), so the limits hold even if an archive lies.
  Documented and covered by tests; no behaviour change.
- **Dependencies:** `npm audit` reported four high-severity advisories in `@grpc/grpc-js`, pulled in
  by Firebase's Firestore package (which Redactobot does not use). An npm override pins it to the
  patched 1.14.7; `npm audit` now reports none.

### Samples, icons, wording and privacy policy

- **Use a sample document** now cycles through ten funny, fictional documents (`src/core/samples.ts`):
  parody paperwork about characters from Dune, Star Wars, Star Trek: TNG, Hackers, Blade Runner,
  Back to the Future, Indiana Jones, The Matrix, Ghostbusters and Jurassic Park. Each gives the
  rules at least 15 things to find; contact details use reserved test ranges.
- Robot-head icon for the web app (favicon, 192 px, Apple touch icon) and the Chrome extension.
- Web app wording: new intro with a technology-demonstration notice, text box label "Paste here",
  and "Select which information you want scanned and redacted" under What to replace.
- **Privacy policy and terms of use** (`public/privacy.html`), linked from the intro, the How this
  works dialog and the extension's settings (the extension build bundles a copy).

### Code style: Google style guides, lint and format scripts

- No behaviour change. The code is formatted and linted to the Google TypeScript, JavaScript,
  HTML/CSS and Python style guides: 80-column lines, one statement per line, braces on multi-line
  control flow, one variable per declaration, JSDoc on exported symbols, licence headers.
- `npm run lint` checks it (oxlint and Prettier, both pinned dev dependencies); `npm run fix`
  applies it. Python scripts use Black at 80 columns (`pyproject.toml`).

### What to replace: reliable tick boxes, FOIA under Regulatory

- Regulatory boxes are now simply ticked or blank (no dash) and always untick. Before, a regulation
  stayed ticked when another ticked regulation needed the same data types, and showed a dash when
  only some were on. Unticking removes only the data types that ticking it switched on; switching
  off a data type a ticked regulation needs unticks that regulation.
- **FOIA release (US)** is listed under Regulatory. Ticking it checks every data type and switches
  the output to the FOIA release; it stays in step with the Output switch on the review screen.
- Removed the audience shortcuts (Law practice, Accounting and tax, Health records ...).

### Extension: off by default, stop loading at once, optional startup load

- The Redactobot switch now starts **off** every time ChatGPT, Claude or Gemini loads, and applies to
  that tab only (it is no longer saved). Nothing loads the on-device model until you switch it on.
  Settings' site checkboxes now choose where the switch is shown.
- Switching off while the model is starting stops at once: the bar disappears, any held paste is
  canceled, and the model start is aborted when no other tab or paste is waiting for it (a late
  session is destroyed). Switching back on starts fresh.
- New setting, off by default: **Load on-device AI when Chrome starts**. It only warms the model in the
  background; the switch on each chat site still starts off. A tab switching off does not cancel it.

### Extension: Redactobot branding and cold-start bar

- The switch under the ChatGPT, Claude and Gemini chat boxes is now labelled **Redactobot** (was
  "Paste check"), and the in-box status reads "Redactobot is checking your paste…".
- When Chrome has to reload the on-device model (a cold start, 1-3 minutes after idle), a progress bar
  appears in the same row, right below the chat box: "Starting on-device AI…", elapsed time, and an
  estimated bar with a moving sheen, drawn with the site's own accent, border, text colour and font.
  It fills and says "On-device AI is ready" when the model answers, then disappears. A warm model
  (answers within 0.7 s) shows nothing. A paste that has to wait for a cold model shows the same bar.
  Screen readers get a progressbar with value text; reduced motion stops the sheen.

### FOIA release (US)

- New **Output** switch on the review screen: "For an AI chat" (placeholders, as before) or
  **"FOIA release (US)"**. The release marks each withholding the way a FOIA officer does, as 5 U.S.C.
  § 552(b) requires: a black box at the place of the deletion, as long as the withheld text, labelled
  with the exemption, e.g. `(b)(6)`. A "Released in part" stamp lists the exemptions used, and an
  explanation of exemptions closes the record. Shown on paper in any theme.
- Defaults (`src/core/foia.ts`): personal details (b)(6); business names, business numbers and money
  (b)(4). A "Law enforcement record" option cites `(b)(6), (b)(7)(C)` for personal details and
  (b)(7)(E) for credentials, IP addresses and device IDs. The FOIA exemptions card changes the
  exemption per data type (all of (b)(1)–(b)(9)), or releases that type. Choices are saved in this
  browser; no document text is stored.
- Print or save as PDF prints only the release, with boxes kept black; flagged details that were not
  withheld print as ordinary text. "Copy as text" uses █ runs plus the exemption. Cloud cleanup is
  off in FOIA mode: a release stays on the device.

### Display, accessibility and mobile

- Cold start: an animated progress card at the top of the page while Chrome loads the on-device model
  (striped, moving bar; estimated percent and elapsed time, since Chrome reports no load progress;
  fills to 100% and shows "ready" when the model answers).
- New logo artwork (solid pixel-art robot), keyed by `tools/key_logo.py`: the robot keeps its dark sprite
  outline as a solid silhouette, the wordmark loses all black (letter counters too). The light theme
  uses `redactobot-logo-light.webp`, the same art with an outlined wordmark so it reads on white.
- New **Display** menu (contrast icon in the header): theme (match the computer, light, dark), colours
  (standard, or colour-blind friendly Okabe-Ito blue/orange/purple) and motion (full or reduced).
  Saved in this browser only and applied before first paint (`public/display-prefs.js`).
- The logo (WebP) and robot video (WebM with alpha, MP4 fallback) now have transparent backgrounds, so
  they blend with both the light and dark themes.
- Accessibility: skip link; flagged details work from the keyboard (Enter/Space) with a focus ring;
  sensitive details carry a dashed underline as well as colour; `aria-busy` while text types out;
  pause button on the robot video (WCAG 2.2.2); Windows high-contrast (forced-colors) support; all
  semantic colour pairs measure at least 8.2:1 contrast.
- Mobile: smaller logo, compact verdict, 44 px touch targets, full-width buttons. The robot video is
  hidden and not played below 840 px wide; the progress bar shows the work instead.

### New name: Redactobot

- The project is now called **Redactobot** ("Client-safe AI" was taken): app title, extension name,
  settings and review pages, docs and internal identifiers. Saved app settings carry over. The
  evaluation ledger keeps the old name where it records commands as they were run; the scorers
  still accept the old `CSA_CORPUS` / `CSA_HARNESS_URL` variables.

### Faster paste checks

Measured in desktop Chrome with Gemini Nano; method and all rounds in
[evaluation/SPEED-LOG.md](evaluation/SPEED-LOG.md).

- Pastes with no word that could be a name or place, and no health, sensitive or identity
  vocabulary, skip Gemini Nano and are decided by rules in milliseconds (250-600 ms before).
  Rules already match the model on every structured identifier.
- Nano now answers with tagged strings (`"person: Name"`) constrained by a schema pattern
  instead of `{"text","kind"}` objects. Median check on unseen documents: 2.99 s to about
  1.3-1.4 s; p90 5.6 s to about 3 s; name recall unchanged.
- Rejected after measurement: grouped output, hiding rule findings from the model, sentence
  filtering, removing the duplicate rules pass and bypassing Firebase (no gain or within noise).

### Review dialog

- **Copy** is replaced by **Use this text**: it pastes the box exactly as shown,
  including your edits, without another check. **Ignore** pastes the original text
  unchanged. Neither result is checked again.
- The main button appears only when it adds something: **Clean up this preview in
  cloud** (cloud cleanup on), **Scan again** (incomplete scan) or **Check edited text**.
  Otherwise **Use this text** is the main action.
- If the draft changed during review, Use this text and Ignore add the text at the end
  of the draft. If it cannot be placed, the text is selected for manual copying.
- The action buttons stay pinned to the bottom of the panel; before, they could fall
  below the fold with three or more findings.

### Cold-start timeouts (live sites)

- Live pastes on ChatGPT and Gemini failed with "The local check timed out". Cause:
  Chrome shuts down its on-device model process when idle, even while the extension
  holds a session. The next request waits for a full reload (measured about 3.3 minutes
  on an RTX 4070: 62 s to create a session after the process started, 18 s for the
  first answer), well past the 30-second scan budget. Warm requests take about 0.6 s.
  With a session held open, a prompt after 5 minutes idle took 0.28 s; after 8 minutes
  Chrome had restarted the model process and the same prompt took 167 s.
- While a chat tab is visible with Paste check on, the extension now sends a text-free
  prepare request every minute and when the tab becomes visible again; the scanner
  touches the model with a one-word prompt only if it has been idle for 90 seconds.
  Focusing the chat box also wakes it, before the paste.
- Waking an unloaded model is reported as startup ("Starting on-device AI. After a
  break this can take a minute or two…") with a 5-minute budget. The scan budget
  restarts once the model answers.
- The document app keeps the model loaded while its tab is visible and wakes it under
  the loading state before scanning.

### Testing

- Added `npm run test:e2e`: 17 browser tests that drive the real extension with real
  keyboard pastes and mouse drags on mock ChatGPT, Claude and Gemini composers. Run
  against the 0.3.0 paste handler, they catch the Excel-paste, drag-and-drop and
  oversized-paste bugs fixed below.

### Speed

- Document app: each on-device prompt now clones one warm, text-free session instead
  of building a new one. A 1,010-word scan (names + topics, 4 chunks) went from
  12.0-14.1 s to 9.6-11.3 s in Chrome with Gemini Nano (about 20% faster).
- Document app: an already-downloaded model starts loading when the page opens
  (cold start measured at 50 s), and the cloud preview's local session loads while
  the user reviews. Downloads still need a click.
- Document app: detections are cached between renders. Selecting text or typing a
  question no longer re-runs detection (about 350 ms per render on 60 pages).
- Paste guard: skips the token-count round trip when a prompt provably fits.

### Privacy fixes from code review

- Paste guard: text copied from Excel, Word or PowerPoint, which arrives with an
  image of the selection, was passed through unscrubbed. It is now held and checked;
  the attached image is dropped. File-only pastes still go to the site.
- Paste guard: text dragged into the chat box is now checked like a paste.
- Document app: the cloud preview keeps every name the review scan found, so a
  name shown as replaced cannot reappear raw if the second local pass misses it.
- Cloud excerpts that span a placeholder (`[PERSON_…]'s diabetes`) now redact only
  the surrounding text, so the name is still restored in the answer.
- The hosted web build refuses to compile an App Check debug token into public JS.
- OpenDocument import caps space-run counts so a crafted file cannot exhaust memory.

### Reliability

- An oversized paste or a full queue shows a short notice instead of blocking later
  pastes or replacing an open review.
- An incomplete scan offers **Scan again**; editing the text enables a fresh check.
- If cloud cleanup fails, the review offers local removal only (sensitive details
  removed locally by default) instead of retrying the cloud on every approve.
- Opening a second review window closes the first and revokes its approval; review
  popups close when the paste finishes.
- Oversized paragraphs (spreadsheet sheets, dense PDF pages) are split at line
  breaks, then words, so each on-device prompt stays within budget.

## 0.3.0 — 2026-11-13

The app now combines local identity removal with optional cloud cleanup. The
Chrome extension checks pasted text directly in ChatGPT, Claude and Gemini, with
automatic insertion for clear matches and review for unresolved ambiguity.
This is a development release installed through Chrome's Developer mode.

### Choose what the paste guard checks

- Added **Data types** beside the composer **Paste check** switch. Settings offer
  12 categories: names, contact details, places, government/record IDs, payments,
  passwords, web/device/vehicle identifiers, dates, money, health, other personal
  facts and indirect identity clues.
- Added **Common identifiers** and **All categories** presets. Existing users keep
  all checks until they change them. Preferences apply to the next paste across
  all three sites; pending scans keep their original selection.
- Selected categories control local redaction, model extraction and review
  warnings. Pattern-only selections skip Nano and its queue entirely. An empty
  selection inserts text without screening.
- Narrower selections pause cloud cleanup. It requires all categories so that
  unchecked identifiers cannot enter the cloud and disabled categories are not
  removed by the second pass. The saved cloud preference is retained.
- Clear selected details are removed and pasted automatically. A full name agreed
  on by local checks and Nano no longer opens review for a generic model doubt.
  Short ambiguous names, conflicting evidence and incomplete scans still need attention.
- Fixed uncertain name output reintroducing an unchecked place such as Seattle,
  and name aliases being redacted inside unchecked email addresses or URLs.

### Chat integrations and appearance

- Replaced the original extension launcher with an actual text-paste gate, built
  from TypeScript. The extension captures the paste before it reaches the editor,
  scans locally, and inserts the cleaned text. It never sends a chat message.
- Added recognition of ChatGPT's newer ProseMirror editor and excluded Gemini's
  hidden Quill clipboard editor. Nested editor targets are covered by tests.
- Moved scanning status inside the composer layout. Controls and reviews follow
  each service's fonts, colors, light/dark appearance and theme changes.
- Added a per-site On/Off switch, removed the floating product badge, and preserved
  existing drafts. Turning protection off cancels held and queued pastes.
- Added an extension-origin review with a separate-window fallback. Changing the
  draft or navigating during a scan prevents the result from overwriting it;
  editing a review requires a fresh local scan.

### Local and cloud privacy

- Production detection uses Firebase AI Logic in locked `ONLY_ON_DEVICE` mode.
  Unexpected inference sources are rejected; raw-text detection has no cloud fallback.
- Added two privacy buckets: identifiers and identifying context must be removed
  locally; decontextualized medical and other sensitive facts can enter the
  optional cloud cleanup stage. Removing direct identifiers is not proof of anonymity.
- Added completed-scan and review checks, a final local check of the outgoing
  text, and single-use, expiring approvals for cloud requests. Edits invalidate
  earlier approvals. In the document app, the question is checked along with the document.
- Cloud cleanup uses Firebase AI Logic in `ONLY_IN_CLOUD` mode with App Check.
  It returns exact excerpts to remove rather than rewriting the document. Missing
  local findings are retained; malformed output, errors and cancellation hold the request.
- Identity mappings, original filenames and chat history are excluded from cloud
  payloads. The mapping remains in memory for local restoration of app answers.
- Added Firebase/App Check configuration examples and a fixed fictional cloud
  connection test. Cloud cleanup defaults off and requires configuration. Local
  credentials and generated debug builds are excluded from Git.

### Detection and false positives

- Corrected place/person, organization/person and clinical phrase/name labels,
  while preserving removal of overlapping identifiers.
- Expanded record-number detection for short values, labelled and table-based
  IDs, fragmented values and formats learned within the current document.
- Added Unicode/invisible-character normalization with offsets back to the original
  text, stronger payment-card detection, and preservation of complete overlapping spans.
- Added an offline GeoNames dictionary for cities and capitals, address context,
  and review of suspected place typos. Attribution and data scope ship with builds.
- Replaced broad occupation-suffix and uniqueness guesses that flagged ordinary
  phrases such as “only cold water.” Identifying context is scoped to relevant sentences.
- Added contextual handling of generic industry descriptions and quoted appliance
  controls such as “Pots & Pans,” without broadly exempting actual names or organizations.
- Resolved redundant uncertainty fully covered by clear local contact matches.
  Educational questions and ordinary request wording have regression coverage.

### Startup, speed and recovery

- Preloads a text-free Nano session at Chrome startup, extension update and enabled
  chat-page entry when the selection needs AI. Firebase uses an isolated clone for
  each request; pasted text never enters the retained base session.
- Replaced several model passes with compact extraction per overlapping chunk.
  The full input is still checked; a quick negative does not skip the remaining text.
- Settings warms the real scanner instead of creating a duplicate installed-model
  session. Initial downloads retain the visible setup flow and temporary sessions
  are released afterward.
- Added bounded availability/startup checks, elapsed setup status, word-based scan
  deadlines, an independent background watchdog, and cancellation of stale work.
- Added an explicit scan queue. Real pastes preempt diagnostics, cancelled work
  releases its slot even if a native promise hangs, and late results cannot insert text.
  A new paste can replace a failed attempt without leaving the editor blocked.
- Added scanner status, fixed-sample tests and separate startup/AI/local timings.
  Status diagnostics record job stages and queue counts, never document excerpts.

### Evaluation and documentation

- Added synthetic paste speed experiments, first-warning measurements, six-theme
  UI previews, category comparisons and deterministic identity benchmarks.
- Added Desktop TESTFILES import, answer-key scoring and saved-evidence replay
  tools. The key is used only by the scorer. Source/input hashes detect changes;
  imports, raw corpus results and local authorization URLs remain in ignored storage.
- The 500-file run was stopped at 241 Nano scans at the user's request. Its partial
  results and later development replays are documented separately from fresh tests.
  It has not been resumed or presented as a completed independent evaluation.
- Rewrote the README in plain language with the redaction robot, updated extension
  setup, and documented privacy boundaries, results and remaining limitations.

### Validation and remaining work

`npm test` passes **633 checks**: 33 taxonomy checks and 600 Vitest tests across
27 files. App and extension production builds pass, along with five additional
Python scorer contract tests. Live checks exercised all three chat integrations and the
Firebase/App Check pipeline; the latest category tests used Claude.

The latest fixed mixed-category sample pasted automatically in **0.08 s** with
contact checks only, **0.76 s** with names only, and **1.08 s** with Common identifiers.
The latter two used a warm model. The first all-category diagnostic after a reload
took **97.39 s**, almost entirely model preparation. Cold startup remains variable.
These are individual development measurements, not speed or accuracy guarantees.

The paste guard covers text pastes, not typing, chat-site file uploads or images.
The document app supports text-based PDF, Office/OpenDocument, RTF, email, HTML,
CSV and plain-text imports; OCR is not implemented. Detection still has misses and
false positives. The extension is not yet distributed through the Chrome Web Store,
and a public release needs production App Check setup instead of a debug token.

See [extension behavior and setup](extension/README.md) and
[measurements and partial corpus results](bench/RESULTS.md).
