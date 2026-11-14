# Offline model-evidence experiments

Frozen saved text and model answers; no fresh inference or import. Baseline is rerun from the current code.

Recall below counts **enabled replacements only**. Whole-document counts refer only to annotated core values, not a privacy guarantee.

| Corpus | Variant | Core caught | Core recall | Whole core docs | Whole core + added | Extra replacements | Excess alphanumeric chars | Recovered / regressed |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | baseline | 5770/5772 | 99.965% | 98/100 | 98/100 | 276 (4.08%) | 3184 | 0 / 0 |
| 1 | trust-model | 5770/5772 | 99.965% | 98/100 | 98/100 | 353 (5.16%) | 3755 | 0 / 0 |
| 1 | guarded-exact | 5770/5772 | 99.965% | 98/100 | 98/100 | 280 (4.14%) | 3249 | 0 / 0 |
| 1 | guarded-normalized | 5770/5772 | 99.965% | 98/100 | 98/100 | 280 (4.14%) | 3249 | 0 / 0 |
| 1 | complete-spans | 5770/5772 | 99.965% | 98/100 | 98/100 | 276 (4.08%) | 3191 | 0 / 0 |
| 1 | combined | 5770/5772 | 99.965% | 98/100 | 98/100 | 280 (4.14%) | 3256 | 0 / 0 |
| 1 | identifier-memory | 5770/5772 | 99.965% | 98/100 | 98/100 | 276 (4.08%) | 3184 | 0 / 0 |
| 1 | combined-memory | 5770/5772 | 99.965% | 98/100 | 98/100 | 280 (4.14%) | 3256 | 0 / 0 |
| 2 | baseline | 4390/4527 | 96.974% | 12/60 | 6/60 | 336 (6.23%) | 4292 | 0 / 0 |
| 2 | trust-model | 4390/4527 | 96.974% | 12/60 | 7/60 | 397 (7.26%) | 4781 | 0 / 0 |
| 2 | guarded-exact | 4390/4527 | 96.974% | 12/60 | 6/60 | 340 (6.30%) | 4348 | 0 / 0 |
| 2 | guarded-normalized | 4390/4527 | 96.974% | 12/60 | 6/60 | 341 (6.32%) | 4355 | 0 / 0 |
| 2 | complete-spans | 4390/4527 | 96.974% | 12/60 | 6/60 | 336 (6.23%) | 4292 | 0 / 0 |
| 2 | combined | 4390/4527 | 96.974% | 12/60 | 6/60 | 341 (6.32%) | 4355 | 0 / 0 |
| 2 | identifier-memory | 4390/4527 | 96.974% | 12/60 | 6/60 | 336 (6.23%) | 4292 | 0 / 0 |
| 2 | combined-memory | 4390/4527 | 96.974% | 12/60 | 6/60 | 341 (6.32%) | 4355 | 0 / 0 |
| 3 | baseline | 2981/3047 | 97.834% | 38/60 | 33/60 | 173 (4.89%) | 2113 | 0 / 0 |
| 3 | trust-model | 2990/3047 | 98.129% | 38/60 | 34/60 | 209 (5.82%) | 2331 | 9 / 0 |
| 3 | guarded-exact | 2986/3047 | 97.998% | 38/60 | 33/60 | 175 (4.93%) | 2140 | 5 / 0 |
| 3 | guarded-normalized | 2989/3047 | 98.096% | 38/60 | 33/60 | 176 (4.96%) | 2152 | 8 / 0 |
| 3 | complete-spans | 2984/3047 | 97.932% | 38/60 | 33/60 | 173 (4.89%) | 2113 | 3 / 0 |
| 3 | combined | 2994/3047 | 98.261% | 38/60 | 33/60 | 176 (4.96%) | 2152 | 13 / 0 |
| 3 | identifier-memory | 2981/3047 | 97.834% | 38/60 | 33/60 | 173 (4.89%) | 2113 | 0 / 0 |
| 3 | combined-memory | 2994/3047 | 98.261% | 38/60 | 33/60 | 176 (4.96%) | 2152 | 13 / 0 |

The extra-replacement and excess-character counts are answer-key proxies, not audited precision. Titles and incomplete keys can contribute.
Corpus 1 and corpus 3 are development/regression sets. Corpus 2 is aggregate-only; repeated measurement still makes it an imperfect holdout.

## Selected combination: validation and uncertainty

`combined` was selected on corpora 1 and 3 before corpus 2 ran; its source hash and success checks are frozen in `protocol.json`.

| Corpus | Core recall gain (percentage points) | Paired document bootstrap 95% interval | Documents with a core gain | Extra-replacement rate change |
|---|---:|---:|---:|---:|
| 1 | 0.000 | [0.000, 0.000] | 0 | +0.057 pp |
| 2 | 0.000 | [0.000, 0.000] | 0 | +0.086 pp |
| 3 | 0.427 | [0.000, 1.068] | 3 | +0.068 pp |

Prespecified validation checks: recall_gain=FAIL, no_regression=PASS, extra_rate_budget=PASS.

**Decision:** keep the changes as research prototypes. The selected combination did not meet the prespecified validation criteria, so these results do not justify presenting it as a general accuracy upgrade.

These intervals are descriptive: this is reused synthetic data, gains can be concentrated in very few documents, and multiple variants were explored. They do not establish accuracy on future real documents.

## Changed categories and subtypes

Only aggregate changes are shown, including for corpus 2. No individual corpus 2 misses were inspected.

| Corpus | Category | Baseline | Combined | Additional fully replaced |
|---|---|---:|---:|---:|
| 2 | place | 92.84% (441/475) | 93.05% (442/475) | 1 |
| 3 | indirect_identifier | 1.92% (1/52) | 3.85% (2/52) | 1 |
| 3 | organization_name | 96.51% (249/258) | 98.45% (254/258) | 5 |
| 3 | person_name | 95.92% (728/759) | 96.97% (736/759) | 8 |
| 3 | place | 94.20% (260/276) | 94.57% (261/276) | 1 |

| Corpus | Subtype with baseline ≥90% | Baseline caught | Combined caught | Total |
|---|---|---:|---:|---:|

No detailed subtype already at ≥90% gained full occurrences with the selected combination. The improvements above occur within broader categories that already exceed 90%, concentrated in their weaker written forms.


## What each experiment changes

- `trust-model`: add any exact model-proposed span that is free. A deliberately permissive comparison; it does not overwrite earlier spans.
- `guarded-exact`: add exact grounded spans after generic-word, region, and occurrence-context checks.
- `guarded-normalized`: the same with case, canonical Unicode, apostrophe, hyphen, and whitespace normalization mapped back to original offsets. It preserves accents.
- `complete-spans`: only complete an existing, contained, same-kind partial span using guarded exact model evidence. Manual and disabled detections are protected.
- `combined`: guarded normalization plus complete-span reconciliation; no extra model requests.
- `identifier-memory`: infer an ID family from two different explicitly detected values with the same prefix, separators, digit widths, and type. No new inference calls.
- `combined-memory`: the combination plus identifier memory. The narrow memory rule did not add value in these corpora.

## Behavioral controls and chunk bounds

| Variant | Controlled positives fully covered | Negative controls hit |
|---|---:|---:|
| baseline | 54/68 | 4/13 |
| trust-model | 62/68 | 12/13 |
| guarded-exact | 62/68 | 4/13 |
| guarded-normalized | 66/68 | 4/13 |
| complete-spans | 54/68 | 4/13 |
| combined | 68/68 | 4/13 |
| identifier-memory | 54/68 | 4/13 |
| combined-memory | 68/68 | 4/13 |

These controls were authored for the mechanisms and are not an independent accuracy estimate. The four negative hits already present in the baseline remain unresolved. Offset mapping, manual/disabled choices, selected categories, restoration, identifier-family boundaries, and chunk coverage checks passed.

| Corpus | Old maximum words/chunk | Old chunks over 350 words | Bounded maximum | Old → bounded chunk count |
|---|---:|---:|---:|---:|
| 1 | 1416 | 12 | 350 | 182 → 192 |
| 2 | 798 | 4 | 350 | 128 → 124 |
| 3 | 437 | 5 | 350 | 107 → 105 |

A separate 2,000-word paragraph is currently one chunk; the bounded prototype makes seven overlapping chunks of at most 350 words. This establishes a bound and coverage, not a model recall gain. Context-carrying model prompts, targeted repair inference, and learned table schemas remain untested.

## Reproduce

From the repository root, after installing the locked dependencies:

```bash
node tools/evaluation/run_evidence_experiments.mjs --corpora 1,3
node tools/evaluation/check_evidence_experiments.mjs
# Freeze the experiment before consulting corpus 2 totals.
node tools/evaluation/run_evidence_experiments.mjs --corpora 2
python3 -P tools/evaluation/score_evidence_experiments.py
node_modules/.bin/tsc --ignoreConfig --noEmit --target ES2022 --module ESNext --moduleResolution bundler --lib ES2023,DOM,DOM.Iterable --allowJs --skipLibCheck --types node tools/evaluation/evidence-experiments.ts
npm test
npm run build
```

The `.json.gz` files retain per-document variant detections for reproducibility. Corpus 2 is consumed only by aggregate scoring. Each run records its source hash, base commit, and timing. Baselines reproduced the saved round-4 spans and kinds exactly on all documents. JS UTF-16 offsets are converted to Python code-point offsets before scoring.

The only post-validation source edit was a TypeScript non-null assertion after an existing nonempty-array guard. It has no runtime effect; both source hashes are recorded in `protocol.json`, and all corpora were replayed after that type-check fix.

Timing is local CPU postprocessing only, excludes import/model/UI latency, and is affected by warmup and variant order. It is not an end-to-end latency benchmark. Production detector code and published accuracy figures are unchanged.

Historical core scoring counted highlighted-only spans too. This experiment also retains `legacy_core` for comparison but requires enabled replacements for its headline; corpus 1 therefore starts at 5,770 rather than the previously reported 5,771.
