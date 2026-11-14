# Benchmark results

## 2026-11-13 - Configurable paste categories and automatic PID removal

Checked the installed extension using Chrome's native Paste command in blank
Claude tabs. Fixed fictional sample: Avery Bennett, Seattle, diabetes, $1,250,
avery@example.com and record number 42. No chat messages were submitted.

| Selected checks | Automatic insertion observed | Result |
|---|---:|---|
| Contact details only | 0.08 s | Email removed; all other text unchanged |
| Names only, after boundary fix | 0.76 s | Full name removed; all other text unchanged |
| Common identifiers preset | 1.08 s | Name, place, email and record number removed; health and money left unchanged |

The contact-only run completed while a separate diagnostic was preparing Nano.
The name and Common identifiers runs used a warm model. All three completed without
a review dialogue or cloud cleanup. Timings include UI polling overhead; these are
individual checks, not a latency guarantee. Synthetic drafts were cleared and the
clipboard restored. Original full-category and cloud preferences were restored.

The first names-only implementation timed out in live paste tests. The extraction
format now retains its two-field JSON shape, with category-specific uncertainty
kinds. A subsequent fixed-sample diagnostic exposed Seattle as an uncertain person
and name-alias matching inside an unchecked email. Local category boundaries now
prevent these findings from reopening review. A generic doubt about a full person
name can also be resolved when local and model evidence independently agree; short
names and genuine category conflicts still require review. After the fixes, the
same names-only diagnostic took 0.88 s (838 ms AI, 44 ms local), with one finding and
automatic insertion selected.

Startup remains variable: the first all-category diagnostic after extension reload
took 97.39 s, including 96.65 s preparing Nano and 0.69 s inference. Pattern-only
selections avoid that startup and the model queue. This work does not establish a
fix for cold model loading. All 633 automated checks and both builds pass.

## 2026-11-12 - Desktop TESTFILES partial evaluation

All 500 files were imported for local evaluation against 3,587 answer-key entries.
Nano was stopped at 241 files at the user's request; 259 remained unscanned by the
model. The run remains stopped. Raw imports, answer keys, per-file outputs and
local harness authorization URLs are not published.

After investigating misses, a development replay of the 241 saved Nano outputs
removed **1,704 of 1,744 annotated values fully (97.7%)**, with 29 partial removals
and 11 misses. **202 of 241 documents** had no residual annotated identifier; all
241 were held for review. Category agreement was only **730 of 1,744**. Complete
removal, correct labels and a review hold are distinct measures. Extra removed
characters were also recorded, but the answer key does not establish every false
positive. These results do not justify a claim of complete protection.

The last local-only development replay covered all 500 files:

| Target | Fully removed annotated values |
|---|---:|
| Medical record numbers | 60 / 60 |
| Health IDs | 70 / 70 |
| Payment-card numbers | 64 / 64 |
| Whole addresses | 358 / 358 |

Full-value scoring excludes generic printed field labels; strict whole-phrase
coverage is tracked separately. The key has no independent city/place category,
so address results do not establish standalone place recall. Names, some account
and national IDs, and license plates still had misses in this local-only run.

The saved model-run median was **7.24 s**, with **11.19 s** p95. Its earlier prompt
and pipeline differ from the later compact paste scanner. These replays reused
evidence and data already inspected during development; they are not fresh,
independent tests of the current model prompt or configurable paste guard.

To evaluate a new local corpus, use `tools/evaluation/desktop-corpus.mjs` and
`tools/evaluation/score_desktop.py` as described in the
[extension evaluation notes](../extension/README.md#verify). Starting another
evaluation is a separate action; documenting these results did not restart one.

## 2026-11-12 - Real Claude paste flow and queue recovery

The live Claude error was `Another local check did not finish`, meaning the new
paste timed out before it acquired the scanner. The previous implementation did
not record the earlier job's type, so the precise blocker is unknown. The queue now
tracks its owner and stage, gives pastes priority over diagnostics, and releases a
task's slot on cancellation even if native work never settles. Regression tests
cover a hung diagnostic, paste preemption, late replies and queued cancellation.

Verified in a separate blank Claude tab using Chrome's native Paste command, with
the site's actual content script, offscreen scanner and optional cloud cleanup:

| Fictional sample | Cloud stage first observed | Scrubbed insertion observed |
|---|---:|---:|
| Short contact, email and record ID | 1.05 s | 6.30 s |
| 500 words: repeated public prose plus those identifiers | 2.93 s | 3.96 s |
| Same 500 words, settings and extension details tabs closed | 2.96 s | 9.26 s |

All three identifier values were replaced in the composer in each run. No message
was submitted, the synthetic drafts were cleared, and the clipboard was restored.
These are UI-observed timings with polling overhead. Cloud latency is included and
varied between runs; the repeated public-prose fixture is not a general accuracy
benchmark. Chrome was already running. This does not reproduce the original unknown
blocking job or measure startup after restarting Chrome.

## 2026-11-12 - Startup recovery checked in the installed extension

Chrome 157.0.8103.40, real offscreen Nano scanner through Firebase, local diagnostics
only. Chrome itself was already running; this is not a measurement after restarting
Chrome or the machine.

After reloading the updated extension, the settings Prepare button reached Ready in
**2.13 s** as observed through UI automation. The fixed 500-word diagnostic then ran in
**1.72 s** (0 ms startup wait, 1562 ms AI, 157 ms local checks). A repeat took **1.58 s**
(0 ms startup, 1433 ms AI, 150 ms local). The public economics paragraph took **0.39 s**
(386 ms AI, 5 ms local), with zero findings and automatic insertion selected.

The 500-word fixture detected its fictional contact identifiers but also marked
ordinary appliance headings as people, producing eight spans and requiring review.
Those runs validate timing and completion, not clean-text precision. These settings
diagnostics do not include live chat insertion or optional cloud cleanup.

The settings button now prepares the real scanner without creating another session
when the model is installed. Availability checks have a ten-second timeout; native
initialization has its existing 150-second limit. Settings show elapsed wait time and
preserve the actual startup error. A cold engine can still take longer than these runs.

## 2026-11-12 - Chrome startup preload and compact paste extraction

The extension now retains one text-free model base in its offscreen document, starts
preparation on Chrome startup/update, and requests preparation when an enabled chat
page loads. It uses one compact Firebase local-only extraction request per chunk,
without generating explanations. It still checks every chunk, including the last.

A public economics paragraph about artificial intelligence companies took **0.70 s**
in the installed extension: 0 ms startup wait, 646 ms AI, 57 ms local checks/worker.
Three warm browser-harness runs took **0.65-0.69 s**, all unchanged with no review.
A preceding diagnostic measured 73.2 s waiting for initial model preparation; preloading
moves that cost before paste when possible, rather than eliminating cold loading.

Sixteen small development controls covered ordinary requests, the public paragraph,
email, a personal medical statement, record/place/card fields, names, a company, a
secret and a first name at the end of about 1,000 words. Early versions missed the
trailing first name and a small town, and over-expanded some names; the final prompt
fixed the name cases and a local meeting-location rule fixed the town case. The saved
final model evidence was replayed through that local rule; all seven annotated ID
values were covered. The other cases were checked for intended unchanged/redacted
output. These are development regressions, not an independent accuracy estimate.
The original 500-file corpus remains stopped at 241 Nano scans and was not rerun.

Measurements exclude optional cloud cleanup and live-site insertion. Existing cloud
preferences are preserved. Raw evaluation artifacts stay under ignored
`evaluation/results/work/desktop-2026-11-13T00-44-22-981Z`.

## 2026-11-12 - record numbers, places and payment cards

The new local pass uses a normalized detection copy with offsets back to the original
text. It combines explicit fields, document-local record formats, offline GeoNames
lookup and payment-card fragments. It preserves complete overlapping identifiers and
holds uncertain formats for review. No additional model request is needed.

The 20 synthetic examples used to investigate these gaps now have complete coverage.
Broader regression checks include Unicode digit scripts, invisible characters, short
and letters-only IDs, addresses, short place names and category conflicts. These are
development examples, not an independent accuracy estimate.

`node tools/evaluation/identity-benchmark.mjs` measures the deterministic part only.
On this Windows machine, the three categories took a median 11-17 ms on approximately
2,000 words after warmup. All local checks took 50-90 ms. First-use initialization was
slower; these Node measurements exclude Nano, browser startup and paste insertion.

The Desktop TESTFILES corpus is evaluated separately with
`node tools/evaluation/desktop-corpus.mjs --corpus <folder>` and
`python tools/evaluation/score_desktop.py <run-folder>`.
Original imports, source hashes, answer-key hashes and results stay under ignored
`evaluation/results/work`. The answer key never enters detection or model prompts.
Full removal, category agreement, review holds, import losses and latency are scored
separately. Replays after inspecting failures are development results.

GeoNames covers larger cities and capitals; it is not a complete list of places.
See [the attribution and data scope](../taxonomy/places-data.NOTICE).

## 2026-11-12 — time to the first paste warning

Follow-up on the same Windows machine: stop as soon as a match is found. The first-warning
demo is `http://127.0.0.1:5176/bench/paste/strategies.html?record=1` in the current session.
To start a fresh instance, run `node tools/paste_benchmark.mjs --port 5176`.
Raw results: [paste/first-warning-windows-results.json](paste/first-warning-windows-results.json).

For the original 2,000-word sample with a name and email at the end, **local checks produced
the first warning in 20.9 ms (median; three runs: 22.5, 20.9, 20.5 ms)**. No model request was
needed. This measures detection, not rendering an extension popup or completing redaction.

When local checks found no match, a single request over the full 2,000-word text produced
a warning in approximately **1.5 seconds**, including the token-budget check. The inputs
used about 2,200 tokens plus a 142-token system prompt, comfortably inside this session's
9,216-token window. The prototype checks the budget and falls back to overlapping chunks
when necessary; it does not truncate text to fit.

The four approaches were 500-word chunks, 1,000-word chunks, a full-text request, and local
checks followed by a full-text request only when needed. All stop at the first positive
result. A no-match result still requires processing the entire input. Eight fictional cases
were run three times in rotating method order, including names at the start, middle and
end of long passages. There were no model-call errors. The tab was hidden for part of this
run, and the long passages use repeated neutral filler; these are approximate diagnostic
timings rather than a general performance guarantee.

The clean long control still caused false warnings. In particular, the 1,000-word approach
warned on the first chunk even when the actual sensitive detail was at the end. Those early
results cannot be credited as finding that detail. Local-first produced false warnings on
three of four clean controls (already replaced text, a general health question, and the long
clean passage). The prompt needs accuracy work before release.

The useful change is to show a warning immediately on a local match and do detailed
redaction after the user asks for it. The earlier 2.75-second figure measured the complete
five-request Nano check; it is not a necessary delay before showing this warning.

## 2026-11-12 — Windows paste sensitivity experiment

Intel Core i7-13700K (16 cores / 24 logical processors), about 32 GB RAM,
Chrome 157. The model was already downloaded. The tab stayed visible throughout the run.
Raw timings: [paste/windows-results.json](paste/windows-results.json).
Run again with `node tools/paste_benchmark.mjs`, then open
`http://127.0.0.1:5175/bench/paste/?record=1`.

The fast model experiment asks only whether the text contains sensitive details. It uses
a persistent native Chrome Prompt API base session, a fresh clone per chunk and a boolean
JSON response. It visits every 500-word chunk with 50 words of overlap. First-warning time
and full-check time are separate, so an early false positive cannot masquerade as a complete
scan of a long paste. The comparison uses the app's existing Firebase on-device name and
topic extraction plus its normal detection pass.

| Input | Local checks, median | Nano sensitivity check, median | Full app scan, median |
|---|---:|---:|---:|
| Short messages (9–18 words) | 0.2–0.5 ms | 0.28–0.29 s | not measured |
| 200 words, sensitive ending | 2.25 ms | 0.56 s | 2.17 s |
| 500 words, sensitive ending | 4.35 ms | 0.57 s | 2.42 s |
| 500 words, clean | 3.75 ms | 0.57 s | 1.97 s |
| 2,000 words, sensitive ending | 13.6 ms | 2.75 s | 4.12 s |
| 2,000 words, clean | 13.2 ms | 2.74 s | not measured |

Initial session creation took **50.25 seconds**, separate from inference. Creating a new
session on a repeat run took **0.20 seconds**. Protection should prepare a model session
before the first paste; a downloaded model is not necessarily loaded and ready to answer.

Method: 17 fixed fictional samples, 10 local passes per sample and 3 Nano runs per sample.
The full app comparison ran twice on each of four samples. All ready local detectors were
enabled, and a flagged health detail counted as a warning even if not selected for replacement.
The long samples repeat neutral editing instructions to control length; caching, different
writing styles, other applications and real extension integration may change these timings.
Page loading, rendering the warning and extension messaging are not included.

Results on this small diagnostic set:

- Nano warned on all 11 sensitive samples in all three runs, including the final chunk of
  the long sample. There were no model-call errors. This is not a general recall estimate.
- Local checks missed the first-name-only sample; Nano caught it.
- Nano unnecessarily warned on already replaced text, the clean 2,000-word sample, and
  one of three runs of the clean 500-word sample.
- Local checks also warned on a general educational health question. Combining the two
  with an "either can warn" rule produced a false warning on 4 of the 6 clean controls
  in at least one run. The warning logic needs refinement before release.

The results support an immediate local warning and a roughly half-second warm model check
for these short-to-medium pastes. Long pastes need a continuing-check state. A negative
result means no match was found, not proof that the text contains no sensitive information.
This remains a benchmark and local paste demo; the extension does not intercept pastes yet.

## 2026-11-11 — minipc (Linux, Chrome 157.0.8103.50)

Hardware: 12-core AMD (Barcelo integrated GPU), 15 GiB usable RAM. Chrome's
`chrome://on-device-internals` rates it performance class **Very Low**.
Sample document: 202 words.

| | Cold (first load) | Warm |
|---|---|---|
| Model download | ~1.5 min | — |
| Base session create | 101.6 s | 1.4 s |
| Per run (mean of 2 successful) | 13.7 s | 13.1 s |
| Seconds per 500-word page | ~34 | ~32 |
| Context window | 9,216 tokens | 9,216 tokens |
| System prompt | 129 tokens | 129 tokens |
| System prompt + sample + schema | 381 tokens | 381 tokens |

Pattern matching: 0.014 ms per pass; all 10 structured items found
(5 amounts, 2 accounts, phone, email, business number), no false positives.

### Accuracy (4 successful runs)

- Full names: **8/8 in every run.** No person or company missed.
- Short forms: `D. Okafor` and `Northgate` alone were caught in **0 of 4** runs;
  `Harbourline` alone was caught in 1 of 4.
- Trap words: `Tofino` returned once as a company. `Victoria` and `May` never.
- Made-up names: `Whitfield Holdings` (it isn't in the text; the model took it from the email
  domain) in 3 of 4 runs.
- Not verbatim: `Cascadia Credit Union` every time, because the source breaks it
  across a line (`Cascadia Credit\nUnion`).

### Reliability

The second prompt in each 3-run batch failed with `UnknownError: kErrorUnknown`.
Same position both batches (clone → prompt → destroy, then clone again).
Runs 1 and 3 succeeded.

## What this means for the app

1. **The model finds full names; code must find the short forms.** After the model
   returns `Daniel Okafor`, code should also search for `D. Okafor`, `Okafor`,
   `Mr. Okafor`, and for company short names like `Harbourline` from
   `Harbourline Marine Supply`. Show these as suggestions in the review step.
2. **Match with flexible whitespace.** Replacement must treat any run of spaces or
   line breaks as one space, or line-wrapped names will slip through unredacted.
3. **Drop names that aren't in the text.** Discard model output that doesn't appear
   in the document (after whitespace normalization) so that invented names like
   `Whitfield Holdings` don't end up in the review list.
4. **Retry on `kErrorUnknown`.** One retry per chunk before falling back to
   pattern-only for that chunk.
5. **Chunk size is not context-bound.** ~250 tokens per 200 words means a
   500-word page is ~650 tokens, well under 9,216. Speed is the limit: on
   Very Low hardware a 10-page document takes ~5 minutes. Page-by-page results are
   essential, and the UI should start review on page 1 while later pages run.

## Harness note

Playwright's default Chrome switches (`--disable-component-update`,
`--disable-background-networking`) make Gemini Nano report `unavailable` and
the on-device service never start. Launch Chrome normally and attach over CDP.
The old `#optimization-guide-on-device-model` and
`#prompt-api-for-gemini-nano-multimodal-input` flags no longer exist in Chrome 157;
the Prompt API works on the web without flags.
