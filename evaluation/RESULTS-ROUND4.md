# Evaluation, round 4: fewer needless replacements, and a third test set

11 to 12 November 2026. Follows [RESULTS-ROUND3.md](RESULTS-ROUND3.md).

## What was done

1. **Cut needless replacements.** Everything the app replaced on the first set that the answer
   key does not list was read, and the general causes were removed.
2. **Wrote a third test set** (`evaluation/corpus3`, documents 301 to 360, 3,266 key items).
   A separate agent wrote it without access to the detectors, the scoring tools or earlier
   results, with new genres and more non-US material (UK, Ireland, Canada including Quebec,
   Australia, France, Germany, Spain, the Netherlands) and notes typed in a hurry.
3. **Used the third set as the working set.** Its misses were read and fixed with general
   rules. The second set stayed unread and is still the honest check.

## Results

| | Start of round 4 | End of round 4 |
|---|---|---|
| **Second set (unseen): core categories fully caught** | 96.4% | **97.0%** (4,390 of 4,527) |
| Second set: with the on-device model switched off | 93.1% | 94.3% |
| Second set: places, passwords, device IDs | 88.4% | 89.7% |
| Second set: sensitive facts flagged for review | 84.5% | 85.3% |
| **Second set: needless replacements** | 7.8% | **6.2%** |
| First set: core categories fully caught | 100% | 5,771 of 5,772 |
| First set: needless replacements | 6.3% | 4.1% |
| Third set (new): core, model switched off | 87.3% | 94.3% |
| Third set: core, with the model | 96.9% (first measurement) | 97.8% |
| Third set: places, passwords, device IDs | 90.4% | 94.6% |
| Third set: sensitive facts flagged for review | 71% (model off) | 92.6% |
| Third set: needless replacements | not measured | 4.9% |

## How to read these numbers

- **The second set is still the figure to expect on a new document: about 97% of core values
  fully caught, about 6% of replacements unnecessary.** Its misses have never been read.
- **The third set confirmed the second.** A corpus written independently, on first contact and
  with the model on, scored 96.9% core, next to the second set's 96.8% at that point. The two
  unseen measurements agree, which is the best evidence so far that the figure is real.
- **Without the model the app is at 94%.** Fixed rules alone now catch 94.3% of core values on
  both the second and the third set. The model adds about three points, mostly names of people
  and places that no rule can know.
- **Returns have flattened.** The last three rule patches of the night moved the second set by
  0.1 points or less each. What is left on the third set is mostly notes typed entirely in lower
  case (surnames, town names), nicknames, and single-letter initials: things a rule cannot tell
  from ordinary words and the on-device model has to supply.
- **Sensitive-fact underlining is near its ceiling for word lists.** Additions that lifted the
  third set from 71% to 92.6% moved the second set from 84.5% to 85.3%. About half of all
  underlines still match nothing in the answer keys; most of those are real sensitive words the
  key authors did not list ("lien", "custody", "surgery"), not noise.
- **Six date items in the third set cannot be scored** ("lost in import"): the generator wrote
  the answer key for a weekday date format wrongly. The app's reading of those cells is right.

## What changed in the app

Precision:
- A capitalized word that the same document also writes in lower case is treated as an ordinary
  word, not a name. This one idea removed most false people and organizations ("Signed ...",
  "Letters of Authority", "Regular Meeting").
- Job titles, heading words and makes of vehicle are not names; months and other first names
  that are also words ("June", "Miranda") need a personal context.
- Organization names from the model are dropped when they are a legal ending on its own, a bare
  run of capitals that is no known organization's initials, a phrase in lower case that is not a
  name elsewhere, a public body or a make of car. A bracketed acronym is a short name only if it
  matches the owner's initials.
- Statute citations, lab reference ranges, chart-of-accounts names, year ranges, counts
  ("31,870 miles") and fractions are no longer taken for sensitive values.

Coverage, from the third set:
- Dates in French, Spanish and Dutch; "Fri 14th", "the 22nd", "aug 15", "29/10/25", "30/10".
- Street addresses: French and French-Canadian (comma after the number, ordinal avenues),
  British (flat first, no street word), Spanish (number last), Australian (unit/number),
  lower-case, "One South Church Avenue". The town and state written right after an address;
  towns beside British, Irish, Australian and continental postcodes.
- Money with the sign after the number ("46 000 €", "1 200 $", "112.480,17 €"), reais, Swiss
  francs, "2 grand".
- Tax numbers outside the US (ABN, TFN, SIRET, NEQ, Steuer-IdNr.), BSB and sort codes, British
  plates, French, Spanish and Australian phone formats, host names.
- SSN endings asked on one line and answered on the next; masked cards; security codes; shape
  and context rules for passwords; handles; security answers.
- People: more titles (police ranks, French, Spanish, German), surnames in capitals, names
  embossed on cards, maiden names, "X family", names in notes typed in lower case after a label
  or a title, initials at the end of a note.
- Organizations: three-word names, capitals with a legal ending, Quebec endings ("inc.",
  "ltée"), "... of Canada", names that end the way organizations end.
- Tables: French and Spanish column headings, "Emp #", "Last" / "First" columns, an "Age" column.

Tooling:
- `tools/evaluation/extras.py` lists needless replacements in context.
- `tools/evaluation/progress3.py` re-scores the third set (model off, or `--replay c3-live`).
- Model-off runs now use the headless browser. Before, they attached to the same Chrome as a
  live model run and navigated its page away, which lost documents.

## Reproduce

```
npx vite --host 127.0.0.1 --port 5173 --strictPort            # dev server, in another terminal
python3 -P tools/evaluation/progress.py --guard               # first and second sets
python3 -P tools/evaluation/progress3.py --replay c3-live     # third set, with stored model output
```

Kept result folders: `results/c1-round4`, `results/c2-round4`, `results/c3-round4`, and
`results/c3-live` (the on-device model's output for the third set).
