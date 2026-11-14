# Paste gate speed log

Started 13 November 2026. Goal: make the Chrome extension's paste check faster without
losing names. Each round: theory, experiment, evaluation, decision.

## Method

- **Live bench** (`bench/speed.html` + `src/speed-bench.ts`, served by
  `npx vite -c tools/evaluation/vite.speed.config.ts` on :5183): runs the paste gate's real
  code in desktop Chrome with Gemini Nano (RTX 4070) on 59 samples: the 17 chat fixtures,
  40 paste-sized (~150-word) pieces and 3 whole documents from corpus 3 (the working set;
  corpus 2 stays unseen). Each variant reports wall time per sample (model + local rules)
  and **name recall**: answer-key person/organization names fully covered by the paste
  gate's findings. Model warm before every run.
- **Overhead bench** (`tests/e2e/latency.mjs`): the real extension in Playwright Chromium with
  the fake model, timing Ctrl+V to inserted text.

## Baseline

| | median | p90 | mean | name recall |
|---|---|---|---|---|
| production `extract()` | 2.76 s | 6.10 s | 3.20 s | 84.6% (368/435) |

Short chat fixtures took 0.25-0.6 s; 200/500/2,000-word fixtures 2.0-2.7 s. Dense
150-word corpus pieces took 3-8.7 s: the input is small, so output generation (many found
items) dominates.

Cold start (Chrome had unloaded the model): 115 s and 167 s in two measurements today.

## Round 0: extension overhead (theory 4)

Theory: messaging hops (content script, background worker, offscreen scanner, rules worker)
and Firebase setup add noticeable time.
Experiment: `tests/e2e/latency.mjs`, 6-8 timed pastes per case, fake model.
Result: **15 ms median** paste-to-insert (first paste ~30 ms), scrubbed text verified.
Decision: **rejected**. Essentially all latency is Gemini Nano; optimize the model step.

## Round 1: gate, grouped output, sentence filter (theories 1-3)

Theories: (1) skip Nano when no word could be a name (`src/core/name-trigger.ts`); (2) the
model spends its time writing output, and `[{"text":..,"kind":..}]` repeats keys for every
item, so one array per kind should be shorter; (3) send Nano only sentences that could name
someone (plus neighbours).
Experiment: live bench, all variants on the same 59 samples, plus a second production run
to measure noise.

| variant | median | p90 | mean | chat fixtures median / mean | name recall |
|---|---|---|---|---|---|
| production (run 1 / run 2) | 2.76 / 2.51 s | 6.10 / 5.37 s | 3.20 / 2.94 s | 468 / 783 ms (run 2) | 84.6 / 85.3% |
| gated | 2.73 s | 6.39 s | 3.05 s | **38** / 611 ms | 85.3% |
| grouped (all keys required) | **2.30 s** | 5.52 s | 2.75 s | 1,034 / 1,316 ms | 87.4% |
| sentence-filtered (includes gate) | 2.45 s | 5.78 s | 2.78 s | 11 / 432 ms | 86.2% |

Evaluation: run-to-run noise is about 10%. Recall differences (84.6-87.4%) are within noise.
- Gate: 10 of 17 chat fixtures skip Nano and drop from 250-600 ms to 1-40 ms; no effect on
  name-dense corpus pieces (they all fire). **Keep.**
- Grouped: ~13% faster on dense text, but 2x slower on short pastes: seven required keys
  cost more than `[]` when nothing is found. **Revise** (round 2: optional keys).
- Sentence filter: small gain over the gate alone and it hides non-name sentences from the
  model's health/sensitive/context checks. **Rejected.**

## Round 2: optional-key grouped output, combined with the gate

Theory: grouped output is slow on short pastes because all seven keys are required; making
them optional lets "nothing found" be `{}`. Combined with the gate, short name-free pastes
skip the model anyway.
Experiment: live bench, clean rerun (a first attempt was contaminated by unit/e2e tests
running at the same time; discarded).

| variant | median | p90 | mean | chat fixtures median / mean | name recall |
|---|---|---|---|---|---|
| production | 2.74 s | 6.63 s | 3.21 s | 551 / 896 ms | 85.7% |
| grouped, optional keys | **2.16 s** | 5.09 s | 2.55 s | 959 / 1,100 ms | 86.7% |
| gate + optional keys | 2.35 s | **4.53 s** | **2.47 s** | **25** / 609 ms | 86.7% |
| gate + grouped (required keys) | 2.20 s | 5.37 s | 2.54 s | 26 / 612 ms | 86.9% |

Evaluation: grouped output is ~20% faster on dense text with equal or better recall. Optional
keys did not remove the short-paste penalty (959 vs 551 ms on fixtures), so the model likely
still writes every key. With the gate, that penalty only affects short pastes that do name
someone. Gate + optional keys: mean -23%, p90 -32% vs production. **Promising; refine.**
Next: a flat list of tagged strings ("person: Name") keeps `[]` cheap and costs ~3 tokens of
overhead per item instead of ~15.

## Round 3: tagged strings

Diagnosis first: with one name found, optional-key grouped output still wrote all seven keys
(`{"person": ["Mira Calder"], "company": [], ...}`, 926 ms); tagged strings wrote
`["person: Mira Calder"]` (344 ms; production 484 ms).
Theory: a flat array of `"kind: excerpt"` strings keeps the cheap `[]` and costs ~3 tokens of
overhead per item instead of ~15.

| variant | median | p90 | mean | chat fixtures median / mean | name recall |
|---|---|---|---|---|---|
| production (gate now built in) | 2.78 s | 5.91 s | 3.08 s | 244 / 589 ms | 85.7% |
| **gate + tagged strings** | **1.59 s** | **2.92 s** | **1.60 s** | **11 / 349 ms** | 85.3% |
| gate + optional keys | 2.37 s | 5.08 s | 2.46 s | 11 / 563 ms | 86.4% |

Evaluation: median -43%, p90 -51%, mean -48% at equal recall. **Adopted** in production
`extract()` (keeps per-category scoping and `uncertain_<kind>` tags; unknown tags, empty
excerpts and untagged strings are rejected as incomplete, as before).

Gate refinement found while porting: a capitalized word at the start of a sentence never
fired, so "Quillon will call." would have skipped the model. Now any sentence-initial
capitalized word fires unless it is a common sentence starter. Corpus recall stays 472/472;
the 8 name-free chat fixtures still skip.

## Round 4: unseen-corpus check of tagged output

Experiment: production (tagged) vs the previous object format (rebuilt in the harness, gate
included) on corpus 2 (unseen) and corpus 3.

| corpus | format | median | p90 | mean | name recall | model errors |
|---|---|---|---|---|---|---|
| 2 (unseen) | tagged | **1.29 s** | **2.80 s** | **1.41 s** | 89.2% | 2 |
| 2 (unseen) | objects | 2.99 s | 5.64 s | 2.81 s | 89.6% | 0 |
| 3 | tagged | **1.57 s** | 2.74 s | 1.60 s | 84.6% | 1 |
| 3 | objects | 2.53 s | 6.67 s | 3.00 s | 86.9% | 0 |

Evaluation: ~50% faster on unseen documents, recall within noise. But 3 samples failed after
retries: Nano invented a tag (`"email: mira.calder@example.com"`), which the parser rejects
as incomplete. The object schema had prevented this with an enum.

## Round 5: constrain tags with a schema pattern

Theory: Chrome's response constraint may honour JSON-schema `pattern`, restoring the enum's
guarantee. Probe: a system prompt inviting "any kind you like, e.g. email" still produced only
allowed tags under `pattern: ^(person|company|...): .+$`. Production now builds the pattern
from the active categories (also restoring per-category scoping).

| corpus | median | p90 | mean | name recall | model errors |
|---|---|---|---|---|---|
| 2 (unseen) | 1.43 s | 3.24 s | 1.55 s | 88.5% | **0** |
| 3 | 1.57 s | 3.09 s | 1.60 s | 84.6% | **0** |

Decision: **adopted**.

## Round 6: hide rule findings from the model

Theory: on dense text Nano spends output repeating emails, phones and numbers the rules
already remove; replacing them with placeholders first should shorten output and input.
Result (corpus 3): median 1.51 vs 1.57 s, p90 2.45 vs 2.65 s, mean 1.46 vs 1.61 s, recall
85.3 vs 86.0%. A 4-9% gain is inside the ~10% noise and adds a text-rewriting step to a
privacy-critical path. **Rejected.**

## Round 7: greedy decoding; duplicate rules pass

- Greedy decoding (topK 1, temperature 0) might shorten output, but web pages no longer expose
  sampling parameters (`LanguageModel.params` absent, `topK` ignored), and the bench cannot
  load the extension into the user's Chrome. **Untested**; worth a try in the extension's
  offscreen document.
- The scanner runs the rules twice (a "local" pass for the progress label, then the report).
  Overhead bench: a 2,000-word name-free paste, which now skips the model, takes **67 ms**
  Ctrl+V to insert in total, so removing one pass saves ~25 ms. **Rejected** (not noticeable).

## Round 8: Firebase AI Logic per-call overhead

Theory: `firebaseLocalPrompt` rebuilds the Firebase model object and checks availability on
every call. Experiment: the same tagged request through Firebase vs the native session,
6 times each. Result: 322-325 ms vs 323-428 ms: **no measurable overhead. Rejected.**
Timings fall in ~100 ms steps (217/303/406 ms), suggesting the model service delivers output
in ~100 ms ticks; ~0.2-0.3 s is the floor for any model call.

## Where it ended

| | before (baseline) | after |
|---|---|---|
| name-free chat paste (gate skips model) | 250-600 ms | **1-40 ms** (plus ~15 ms extension overhead) |
| short chat paste that names someone | ~480 ms | ~340 ms |
| dense 150-word piece, median (corpus 2, unseen) | 2.99 s | **1.29-1.43 s** |
| p90 (corpus 2, unseen) | 5.64 s | **2.80-3.24 s** |
| model errors | 0 | 0 |
| name recall (corpus 2, unseen) | 89.6% | 88.5-89.2% (within noise) |
| cold start after an idle break | 115-167 s, scan timed out at 30 s | kept warm while a chat tab is visible; otherwise a labelled wake with a 5-minute budget |

Not verified here: the real extension in desktop Chrome (the bench runs the same code in a
page). Load `extension/build` and paste on a live site to confirm.
