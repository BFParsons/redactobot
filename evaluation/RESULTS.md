# Detection evaluation, 2026-11-11

> Round 2, with a second unseen test set and later numbers, is in [RESULTS-ROUND2.md](RESULTS-ROUND2.md).

How much of the sensitive information in a set of realistic documents does the app catch?

**Result: 92.7% of sensitive values in the app's core categories are fully caught, up from
68.7% before the fixes in this round. On the 30 documents never looked at while fixing, the
figure is 90.1% (up from 65.7%).** Health details, other sensitive attributes and indirect
identifiers have no detector and are essentially not caught (under 1%).

Everything here is fictional. Nothing in the corpus is real client data.

## What was tested

- **100 documents** written to look like real legal, accounting, health and general business
  paperwork: 40 `.txt`, 12 `.docx`, 12 `.pdf`, 10 `.eml`, 8 `.html`, 6 `.xlsx`, 4 `.rtf`,
  4 `.md`, 4 `.pptx`. 84 US, 12 Canadian, 2 UK, 2 EU. In `corpus/docs/`.
- **An answer key for each** (`corpus/keys/doc-NNN.json`, with a readable `doc-NNN.md`): every
  sensitive value as written, its category, and how many times it appears. 6,120 key items,
  about 7,000 occurrences, 26% marked hard (masked numbers, initials, ALL CAPS, and so on).
- **The app's real pipeline**, in Chrome 157 on this machine: import the file, apply all eight
  rule sets, ask the on-device model (Gemini Nano through Firebase AI Logic) for names, then
  run the detection code. `tools/evaluation/run_eval.py`.

### Keeping the test honest

- The documents and keys were written by a separate agent that was told not to read the
  detection code, so the documents are not shaped to fit the detectors.
- The keys are checked by `verify_corpus.py`, which uses its own file readers (not the app):
  100 documents, 6,120 items, 0 mismatches.
- Documents are split 70/30. Fixes were guided only by misses in the 70 development documents.
  The 30 held-out documents (numbers ending in 3, 6 or 9) were never inspected; only their
  totals were read.
- "Caught" is strict: every character of the value must be inside a detection. A value the
  importer failed to extract counts as missed.

## Results

| | Baseline | After fixes |
|---|---|---|
| **Core categories, all 100 documents** | 68.7% (3,971 of 5,777) | **92.7%** (5,350 of 5,772) |
| Core categories, 70 development documents | 70.3% | 94.1% |
| Core categories, 30 held-out documents | 65.7% | 90.1% |
| Core categories with the on-device model switched off (code only) | 38.3% | 83.9% |
| Places, passwords, device IDs (no detector at baseline, simple one added) | 10.4% | 59.2% |
| Health details, sensitive attributes, indirect identifiers (no detector) | 0.2% | 0.9% |
| Everything in the answer keys | 57.7% | 82.1% |
| Detections that matched nothing in the key (over-redaction) | 4.6% | 6.9% |

"Core categories" are the 23 that had a detector when the baseline ran; the list is fixed so
the two columns compare like with like. The totals differ by five because the spreadsheet
importer now extracts some values it previously lost.

The on-device model ran 182 chunks in each live run with no failures. Model time was about
46 minutes for the 100 documents on this machine (rated "Very Low" by Chrome).

### After fixes, by category (all 100 documents)

| Category | Caught | Of | Rate |
|---|---|---|---|
| Email | 152 | 152 | 100% |
| IBAN | 20 | 20 | 100% |
| Routing number | 45 | 45 | 100% |
| IP address | 33 | 33 | 100% |
| Card expiry | 21 | 21 | 100% |
| Phone | 239 | 243 | 98.4% |
| Date of birth | 89 | 91 | 97.8% |
| Web address | 30 | 31 | 96.8% |
| Other dates | 680 | 708 | 96.0% |
| Money amounts | 859 | 899 | 95.6% |
| SSN | 59 | 62 | 95.2% |
| Tax ID | 80 | 84 | 95.2% |
| Organization names | 710 | 758 | 93.7% |
| Device IDs (new) | 51 | 55 | 92.7% |
| Person names | 1,451 | 1,571 | 92.4% |
| Postal codes | 124 | 136 | 91.2% |
| Vehicle IDs | 54 | 60 | 90.0% |
| Bank accounts | 106 | 119 | 89.1% |
| Record numbers | 334 | 384 | 87.0% |
| Government IDs | 82 | 99 | 82.8% |
| Street addresses | 120 | 150 | 80.0% |
| Card security codes | 10 | 16 | 62.5% |
| Payment cards | 43 | 70 | 61.4% |
| Places (new) | 302 | 527 | 57.3% |
| Passwords and user names (new) | 34 | 72 | 47.2% |
| Ages over 89 | 9 | 20 | 45.0% |
| Indirect identifiers (no detector) | 3 | 107 | 2.8% |
| Sensitive attributes (no detector) | 1 | 147 | 0.7% |
| Health details (no detector) | 1 | 317 | 0.3% |

Standard items: 96.2%. Hard items: 83.4%. By file type the range is 89.4% (email) to 95.3%
(Markdown); no format stands out as broken.

### Names by how they are written

| Form | Baseline | After |
|---|---|---|
| Full name | 83.4% | 95.4% |
| Title and surname ("Ms. Whitfield") | 86.8% | 99.5% |
| Short company name | 65.7% | 95.3% |
| Acronym | 72.3% | 95.7% |
| First name only | 89.6% | 91.2% |
| Surname only | 73.9% | 91.9% |
| "Last, First" | 22.7% | 86.7% |
| ALL CAPS | 49.0% | 82.4% |
| Nickname | 59.7% | 80.6% |
| Initials | 13.3% | 75.9% |

## By rule set

Each rule set run on its own, scored against what that rule covers. Detail:
[results/by-ruleset.md](results/by-ruleset.md).

| Rank | Rule set | Rate | On the 30 unseen documents |
|---|---|---|---|
| 1 | Customer financial information (GLBA) | 93.0% | 90.4% |
| 2 | Health information (HIPAA, 18 identifiers) | 86.2% | 83.8% |
| 3 | Tax return information (IRC § 7216) | 85.3% | 82.9% |
| 4 | Federal court filings (FRCP 5.2) | 81.2% | 66.5% |
| 5 | US federal PII guidance (NIST) | 76.0% | 70.7% |
| 6 | EU personal data (GDPR) | 73.6% | 69.6% |
| 7 | Payment card data (PCI DSS) | 43.0% | 21.6% |
| 8 | California sensitive personal information (CCPA) | 37.2% | 25.6% |

A rule set run alone switches on only its own checks, so some values that are caught when all
rules are on are missed here: birth dates with no "born" or "DOB" label (court filings), card
numbers written as last-four or masked (payment cards), and city names (tax returns).

## What was wrong, and what was fixed

1. **Spreadsheets lost values on import.** Dates and amounts were shown differently from how
   Excel displays them (166 values lost). The importer now applies the cell's number format,
   including custom currency such as `C$`. Two values are still lost.
2. **Two patterns stole fragments.** The account-number pattern took pieces of dates and times
   ("2026 16"), and the card-expiry pattern took "05/09" out of "05/09/2026".
3. **Numbers were not labelled the way the patterns assumed.** Invoice, case, policy, employee,
   bar, NPI and passport numbers often sit in a table column or after different wording.
   Added general rules for "looks like an ID code" and "long number", with exclusions for tax
   form numbers and statute citations.
4. **Money, dates, phones and addresses come in more shapes.** Pounds and euros, `USD 4,500`,
   `75k`, `$1.9 million`, amounts in words, ledger figures with no currency sign; dates with
   weekdays, without years, day-first; phone extensions and international numbers; PO boxes,
   suites, floors, ALL CAPS addresses.
5. **Masked and last-four forms** of SSNs, cards and accounts were not caught.
6. **The model returns full names only, and misses some.** Code now reads names from reliable
   cues (a title, a role, a form field, an email display name, a court caption, a company
   ending such as "LLC" or "Credit Union") and derives the other written forms: initials,
   "Last, First", ALL CAPS, without the middle name, without accents, short company names,
   acronyms, and short names a document defines, such as `("Brightwater")`.
7. **New simple detectors:** places written with a state, province or county; labelled
   passwords, PINs and user names; device serial numbers and hardware addresses.

Code is in `taxonomy/detectors.js`, `src/core/names.ts`, `src/core/redact.ts` and
`src/core/import/numfmt.ts`, with unit tests for each.

## What is still missed

- **Health details, sensitive attributes, indirect identifiers: under 1%.** These need the
  model to read for meaning. They are 571 of the 6,997 occurrences.
- **Places with no state or county next to them** ("lives in Wenatchee"): 57% caught.
- **Payment cards: 61%.** The misses are in the held-out documents, so the cause has not been
  looked at. On the development documents the rate is 90%.
- **Passwords and user names with no label**, and ages over 89 written as a bare number.
- **Names with no cue** that the model also misses: mostly first names and nicknames of people
  whose full name never appears.
- **Short unlabelled numbers** in tables (four-digit employee IDs, five-digit check numbers).
- **Addresses outside the US pattern** ("3 Toft Green", "Keizersgracht 418-II").

## Limits of this evaluation

- The documents were written by an AI agent, not collected from real practices. Real files
  will have layouts and habits these do not.
- The answer keys are verified for presence, not completeness: every listed value is in its
  document, but a sensitive value the author forgot to list would not be counted. The author
  reported a handful of known omissions (two defined terms, a pet's name, some check numbers).
- The held-out figure is a fair estimate for documents like these. It is lower than the
  development figure by four points, which is the size of the fitting effect.
- The "after" figure uses the names the model returned in the final live run, re-scored with
  the committed code (two small rules were added after that run; re-scoring takes seconds and
  changes nothing about the model's part).
- Over-redaction rose from 4.6% to 6.9%. Most extra detections are defined terms such as
  "Plaintiff" and "Employee" being linked to the party they stand for, which is deliberate,
  and product names the model returned as companies.
- One independent check of the spreadsheet importer against LibreOffice found that the only
  differences are date separators (LibreOffice prints dashes on this machine; US Excel shows
  slashes, which the importer produces).
- Speed was not a target of this round.

## Reproducing

```bash
python3 -P evaluation/verify_corpus.py                      # answer keys match the documents
npm run dev                                                 # dev server, port 5173
python3 -P tools/evaluation/run_eval.py myrun               # all 100 documents, live model (~45 min)
python3 -P tools/evaluation/run_eval.py myrun2 --replay myrun   # re-score code changes in seconds
python3 -P tools/evaluation/score.py myrun --split heldout  # all | dev | heldout
python3 -P tools/evaluation/score.py myrun --split dev --misses # what was missed (dev only)
```

Stored runs: `results/baseline` (before fixes), `results/after` (final live run),
`results/final` (the live run's names with the committed code). Each has a `report.md`.
