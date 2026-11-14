# Deterministic name rules for the paste gate

14 November 2026. Goal: raise accuracy of the rules-only step (no Gemini Nano) on paste-sized
text, where it caught about three names in four.

## Method

`npx vite-node tools/evaluation/paste_gate_compare.ts c3-round4 c3` (and `c2-round4 c2`) runs the
paste gate's `makeReport` on every document, whole and as ~150-word pieces; then
`PYTHONUTF8=1 python -P tools/evaluation/paste_gate_report.py det-paste det-doc` scores both
corpora with the standard scorer. Misses were read on corpus 3 only (working set). Corpus 2 is the
unseen check: totals and aggregate breakdowns only. `tools/evaluation/try_gate.ts FILE` shows what
the gate removes from probe texts. Over-redaction (detections not in the keys) is tracked with recall.

## Results (rules only)

| | person, paste-sized | critical, paste-sized | person, whole doc | over-redaction |
|---|---|---|---|---|
| corpus 3, before | 74.3% | 85.8% | 84.8% | 5.8% |
| corpus 3, after | **87.6%** | **92.7%** | **92.9%** | 6.0% |
| corpus 2 (unseen), before | 76.6% | 86.0% | 89.8% | 5.4% |
| corpus 2 (unseen), after | **82.3%** | **88.9%** | **92.8%** | 6.1% |

For reference, rules + Nano on corpus 2: 93.5% person (paste-sized).

## Iterations

1. Cue rules (`discoverNames`): full names at the start of a line, cell or label with a role,
   bracket or next cell; names after sign-offs incl. French/Spanish/German; possessives with
   personal attributes; addressing cues ("ask Shirin", "approved by Priyanka"); person-only
   verbs; greetings to two people. Corpus 2: 76.6 -> 79.5%.
2. Ages/births ("Wren, born 2014"), a name labelling a phone/email line, general possessives
   ("Harper's share"), more person verbs, other-language greetings, names starting with any
   capital (Íñigo, Élodie), more field labels and roles. Corpus 2: 82.5%; false positives from
   heading labels ("Fee:", "Debts:") then removed by requiring contact details: 82.0%, over-
   redaction 6.4 -> 6.0%.
3. Names after any label, in brackets, after a sentence end with a role, before a dash, phone
   or quoted nickname. Corpus 3 +2.3, corpus 2 unchanged.
4. Initials (sign-offs, "GM said", "(HW)"), names in capitals after labels and between
   parties, "Surname, First". Corpus 3 +3.1, corpus 2 +0.3.

Iterations 3-4 moved corpus 3 far more than corpus 2: further hand-written cues risk fitting
corpus 3's layouts. Remaining corpus 2 misses (aggregate): lone first names 71/302, full names
47/701, initials 38/56, "Surname, First" 15/30.

## Larger given-name list (SSA)

`src/core/given-names-ssa.ts` (21,866 names, 155 KB; public-domain US Social Security baby-name data,
built by `tools/build_given_names.py`) is used only for capitalized words in mid-sentence, skipping
known places and a list of common English words that are also names ("Case", "Honor", "Manual").

| rules only | person, paste-sized | critical, paste-sized | person, whole doc | over-redaction |
|---|---|---|---|---|
| corpus 2 (unseen), before | 82.3% | 88.9% | 92.8% | 6.1% |
| corpus 2 (unseen), after | **86.1%** | **90.9%** | **94.8%** | 6.4% |
| corpus 3, after | 88.8% | 93.3% | 93.5% | 6.1% |

Rules alone now beat the rules + Nano path on whole documents of the unseen set (94.8% vs 93.5%
from the earlier saved model run). Bundle: document app +65 KB gzip; the chat-page content script
is unchanged (23 KB).

## Earlier note: next lever

Lone first names depend on `GIVEN_NAMES` (1,250 names). A larger public-domain list (US Social
Security baby-name data) plus an English-word filter for names that are also words would
target the largest remaining gap without corpus-specific rules. Needs a data download.
