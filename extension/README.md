# Redactobot: Chrome paste guard

Checks text pasted into recognized ChatGPT, Claude and Gemini message editors. It holds
the original paste while local pattern checks and Gemini Nano scan it. A complete scan
with clear findings inserts the scrubbed text automatically. Ambiguous findings or an
incomplete scan open a review with removals checked by default. Nothing is submitted.
Ordinary request words such as "I", "my", "only" and "unique" do not trigger paragraph
removal. Actual identifying context is checked at sentence level, while direct
identifiers stay protected. General educational questions keep their topic words.
Uniqueness rules require explicit human-role or distinctive-possession context;
word endings such as those in "water", "filter" and "sensor" do not establish identity.

## Build and install

1. From the repository root, run `npm install` and `npm run build:extension`.
2. Open `chrome://extensions`, enable **Developer mode**, choose **Load unpacked**, and
   select `extension/build`. The parent `extension` directory contains templates, not a
   loadable build.
3. Open the extension's settings and click **Prepare on-device AI**. Chrome may need an
   initial model download and warmup. **Test a fictional paste** runs the actual local
   scanner and shows its elapsed time and scrubbed output. **Test a general paragraph**
   checks a fixed public economics paragraph and separates startup from scan time.
   **Test a 500-word paste** measures a longer fixed sample with fictional identifiers
   at the end. These local diagnostics do not call cloud cleanup.
4. Reload your AI chat tabs so the paste handler is present from the start. If the older
   0.1 launcher is installed from another directory, disable it to remove its old button.
5. After rebuilding, click **Reload** on this extension in `chrome://extensions`, then
   reload the chat tabs. Keep unsent drafts elsewhere before reloading a tab.

Requires desktop Chrome 148+ and a device eligible for Chrome's on-device model.

## End-to-end tests

`npm run test:e2e` loads a **test build** of the extension into Playwright's Chromium
(run `npx playwright install chromium` once). ChatGPT, Claude and Gemini are served from
local mock pages at their real URLs, so the content script attaches as in production;
no real chat site is contacted. The test build (`tests/e2e/.build`, git-ignored) replaces
Gemini Nano in the scanner with a deterministic fake (`tests/e2e/fake-nano.js`); never
load it for real use. Pastes use real Ctrl+V and mouse drags. Each mock records what the
site itself receives, and every test asserts that no raw identifier reached the site and
nothing was sent. Covered: all four composer types, clean text, Excel/Word-style
text-plus-image pastes, drag-and-drop, review and approval, model failure and Scan again,
pattern-only and unchecked categories, cloud failure fallback, queued pastes, oversized
pastes, typing during a scan and the per-site switch. `HEADED=1` shows the browser.

Once the model is installed, the extension preloads it when Chrome starts or the
extension updates. Enabled chat pages also request preparation immediately, before
focus or paste. One text-free session stays in the offscreen document to keep Nano
ready. Firebase uses an isolated clone for each request; document text never enters
the retained base. This uses memory but does not continuously scan pages. If all three site switches
are off, Chrome startup does not preload it. Chrome can still discard the model or
restart the extension, so an immediate first paste may have to wait for preparation.
The settings Prepare button warms this same scanner instead of creating another
session when the model is already installed. Setup shows elapsed time, bounds a
silent availability check at ten seconds, and reports startup errors without
overwriting them with an older status response. A temporary settings session is used
only for initial download and released after setup.

Each chunk uses one compact extraction request for names, places and sensitive facts.
It does not skip the full input based on a quick negative verdict. Raw-text inference
still uses Firebase AI Logic in local-only mode. The optional cloud pass adds its own time.

## Appearance and review

**Data types**, beside the chat-box switch, opens **What to check** in settings.
Choose any of 12 categories, or use **Common identifiers** / **All categories**.
Existing installations retain all checks until changed. The selection applies to
the next paste on all three sites; a pending paste keeps the choices it started with.
Turning off a category disables its redaction checks, model extraction and broad
review warnings. Local classification can still recognize email/URL boundaries
and places so they do not become spurious name matches. Health, other sensitive
facts and indirect identity clues are separate.
With no categories selected, text is inserted without screening.

Selections containing only structured checks (such as contact details, payment
cards or record numbers) skip Nano and do not wait for the model queue. Local
diagnostic buttons use your selection. Cloud cleanup is paused unless **All
categories** are enabled; this preserves the full local identity check and avoids
removing categories you turned off. The fixed fictional cloud connection test
always uses all categories. Only preferences, never paste text, are saved.

A compact **Paste check On/Off** switch sits inside each chat box's layout, outside
the editable text. It uses the site's font and color tokens, follows light/dark changes,
and remembers each site's preference in Chrome sync storage. Changes also update open
tabs and the settings page's site preferences. Turning it off cancels pending and queued
checks; it never inserts the held original. Subsequent pastes pass through unchecked until
the switch is turned back on. The control is keyboard accessible and cannot submit a chat.

The scanning status appears inside the active input, following its font family, size,
weight, line height, letter spacing and service color tokens. It has no floating card,
border, shadow or product tag. Existing drafts get a temporary extra row so the status
does not cover their text; that spacing is restored afterward. The status is outside the
editable DOM and cannot become part of a submitted message. Successful insertion clears
the status immediately. The review follows the site's colors and light/dark mode.
Each provider has light and dark fallback palettes. The guard
observes site theme changes and OS theme changes; the site's actual surface takes
precedence over the OS. Review choices and edited preview text survive theme changes.
The guard removes the retired launcher's persistent page badge, including a stale copy
left on an open page after that older extension was disabled. The extension remains
identifiable in Chrome's toolbar and settings.

The scanning notice appears after 180 ms, avoiding a flash for quick scans. Local
matches can update it early; automatic insertion waits for the full scan. Health,
and sensitive-topic matches are removed automatically after a complete scan. Uncertain
names or identifying context ask for review. Identifying details cannot be unchecked;
eligible sensitive facts can be removed locally or left for the optional cloud pass.
Editing the preview requires another local scan before insertion or submission.

If you edit the draft or navigate while scanning, the result cannot overwrite that
changed draft. If the site blocks the embedded review, a **Review** button opens the
same extension page in a separate window. A failed or unavailable model does not release
unscanned text automatically.

## Scope and data handling

- Handles plain text pasted into recognized message editors. Typing, file uploads,
  images and unsupported editors are outside this version's coverage.
- Site redesigns can change editor behavior or selectors; confirm the guard on each
  site before relying on it. Detection can miss details even after a successful scan.
- Captures paste events at document start in Chrome's isolated content-script world.
  Raw excerpts are shown in an extension-origin review frame, not the site's DOM.
- Runs deterministic detection in an extension worker and Nano inference through Firebase
  AI Logic's verified `ONLY_ON_DEVICE` adapter. No raw-text cloud fallback is allowed.
  The scanner, review and settings documents have `connect-src 'none'`; the background
  worker allows only Firebase AI Logic and App Check hosts. Preferences alone are synced.
- Pending jobs expire after ten minutes. Short local scans, including 500 words,
  have a 30-second deadline that includes queueing, startup and final checks. Larger
  scans get a word-count-based budget capped at three minutes; crossing 4,000 characters
  no longer jumps to three minutes. A separate background deadline catches a silent scanner.
  A failed paste stays held with Retry, but a new paste replaces the failed attempt and
  its queued text. Late results cannot insert old text. Background model preparation may continue.
  Real pastes interrupt diagnostic tests; a diagnostic cannot start while a paste is
  running. Cancellation frees the queue even if a native operation never returns.
  **Check scanner status** shows the active stage, elapsed time, waiting count and
  the blocker recorded at the last timeout. It does not expose document text or findings.
  Text is released from active extension job state on completion/cancellation. An open
  review window can retain its displayed preview until it is closed.
- Requests `storage` for site preferences and `offscreen` for the document owning the
  local detection worker. Content scripts run only on `chatgpt.com`, `chat.openai.com`,
  `claude.ai` and `gemini.google.com`. It has no clipboard-read or browsing-history access.

## Verify

Version 0.3.0 adds mandatory local identity removal plus optional cloud cleanup. Configure
Firebase using the root README, rebuild, and enable the cloud setting explicitly. It
defaults off and is unavailable without project/App Check configuration. Clear completed
scans can proceed automatically; uncertain identifying context requires review first.
The cloud receives only the identity-scrubbed text, which may still contain medical or
other sensitive facts. Identity mappings, filenames and chat history are excluded.
Do not publish a development build containing an App Check debug token. Use `npm run package:extension` for the published build: it has no Firebase
project, no debug token, no host permissions and no network access. See
[STORE-LISTING.md](STORE-LISTING.md) for the Chrome Web Store text and screenshots.

Tests cover forged/reused/expired approvals, full document-and-question scanning,
mandatory identity removal, new scans after edits, stale results, cloud failures,
App Check failure, malformed cloud output and cancellation. The real Firebase browser
SDK is exercised with native inference mocked and JavaScript network APIs blocked.
The app and extension production builds pass, with 633 automated checks passing across
the taxonomy, core, app and extension suites. Version 0.3.0 was reloaded in Chrome and
tested with the real offscreen Nano scanner and Firebase background service worker on
2026-11-12. The fixed fictional contact/medical sample passed App Check and cloud cleanup:
4.66 seconds locally, 1.80 seconds for cleanup, with contact details absent from the
cloud preview and the medical facts removed from the result. The local-only contact
fixture also passed in 3.68 seconds and selected automatic insertion without review.
These individual runs are smoke tests, not accuracy or latency benchmarks.

Settings now includes **Test cloud cleanup with fictional text**. This runs a fixed
sample through the actual local and cloud stages without enabling automatic cloud
cleanup or reading any clipboard, document or chat history. It reports timing, the
identity-scrubbed cloud preview and the final cleaned result. This diagnostic is available
only to the extension's settings page. Cloud cleanup remains off by default.

Version 0.2.4 adds the composer switch. Tests cover all three editor structures, site
tokens and theme changes, replacement editors, failed preference saves, cancellation
of pending/queued jobs, late results, and resuming protection when turned back on.
The six-theme demo at `bench/paste/inline.html` includes the interactive switches.
Chrome checks confirmed the control in each live provider's composer and successful
On/Off changes without sending a message. Gemini's hidden Quill clipboard buffer is
excluded so it gets only one switch. Its changed preference survived a reload; all
preexisting site settings were restored afterward. Final validation: 53 extension
tests passed and the extension production build passed. All six preview themes were
inspected; the live-site checks used their current themes, not every theme combination.

Version 0.2.3 fixes redundant review of clear email/phone matches. Nano sometimes
called the already-covered contact details "potentially sensitive" and triggered
review (4 of 5 local runs of the contact fixture). Such uncertainty now proceeds with
automatic redaction only when fully inside an existing, unambiguous email/phone match.
Wider ambiguous spans, other categories and incomplete scans still require review.
After the fix, 5 of 5 local Nano runs selected automatic insertion, removing both
contacts in 0.85–2.53 seconds. This small smoke test is not an accuracy benchmark.

Version 0.2.2 adds inline scanning status and removes page branding. The six-theme visual
demo at `bench/paste/inline.html` uses the real status component with simulated scan
messages, and checks rendered font parity against each demo editor. It does not call a
model. Tests cover in-input positioning, preserving drafts, restoring spacing on cancel
and review, respecting site style updates, and removing the old launcher badge.

Version 0.2.1 recognizes ChatGPT's current ID-less ProseMirror editor by its
`role="textbox"` and `aria-label="Ask ChatGPT"`, while retaining the older composer
selectors. On the live ChatGPT page, the previous guard was loaded but missed this
editor, allowing the fictional test paste through unchanged. Regression tests now cover
the observed markup, nested paragraph paste targets, the labeled textarea variant,
and exclusion of unrelated rich-text fields. Claude and Gemini selectors are unchanged.

`npm test` includes extension policy, editor, paste interception, review and theme tests.
These cover all six provider/theme combinations, live theme changes, stale drafts,
queued pastes, blocked raw paste propagation, ambiguous spans, and incomplete scans.
They use simulated editors; they do not certify compatibility with live provider UIs.

Local validation on 2026-11-12: 199 tests passed (25 specific to this extension), and both
app and extension production builds passed. The unpacked build loaded in Chrome 157;
the offscreen scanner initialized successfully. Its fictional name/email/city self-test
completed in 3.58 seconds using Gemini Nano plus the detection worker, removed all three
details, labeled Seattle as a place, and requested review for model uncertainty. This
single smoke test is not an accuracy or latency benchmark.

For a visual preview, run `node tools/paste_benchmark.mjs` and open
`http://127.0.0.1:5175/bench/paste/themes.html`. This renders the actual review component
with fictional data. It does not run the model or send chat messages.

For each live provider, test light and dark modes, toggle the theme during a review,
paste a fictional email, paste a first name with ambiguous context, edit the draft while
scanning, and cancel a review. Confirm typing and file uploads retain their ordinary
behavior. Never press Send merely to test the paste guard.
