# Evaluation, round 3: one sub-category at a time

11 November 2026. Follows [RESULTS.md](RESULTS.md) (round 1) and
[RESULTS-ROUND2.md](RESULTS-ROUND2.md) (round 2).

## What was done

The 126 sub-categories of sensitive data in the first test set were taken in order, highest
hit rate first. For each one, every miss was read, a general rule was written, and the work
moved on when the sub-category reached 100%. No rule names a document, a person or a value from
the test sets.

## Results

| | Start of round 3 | End of round 3 |
|---|---|---|
| Sub-categories at 100%, first set | 38 of 126 | **116 of 126** |
| Core categories fully caught, first set (100 documents) | 94.8% | **100.0%** (5,772 of 5,772) |
| Core categories fully caught, second set (60 unseen documents) | 93.3% | **96.4%** (4,364 of 4,527) |
| Places, passwords, device IDs, second set | about 80% | 88.4% |
| Sensitive facts flagged for review, first set | 57% | 94.6% |
| Sensitive facts flagged for review, second set | 60% | 84.5% |
| Core categories with the on-device model switched off, first / second set | not measured | 96.0% / 93.1% |
| Replacements that touch nothing in the answer key, first / second set | 6.1% / 7.9% | 6.3% / 7.8% |

Per-sub-category table for the first set: [results/by-subcategory.md](results/by-subcategory.md).

## How to read these numbers

- **The second set is the honest figure.** Nobody has looked at its misses; only its totals are
  ever printed. The first set reached 100% because its misses were read and fixed one by one.
  The gap between the two (100% against 96.4%) is the measure of how much of the late work is
  specific to the forms that happen to occur in the first set. Expect a new document to behave
  like the second set, not the first.
- **The first set no longer has a held-out part.** Rounds 1 and 2 kept 30 of its documents
  unread. Getting each sub-category to 100% meant reading those too, so from this round on the
  second set is the only unseen data.
- **No new model runs.** All scores replay the model output recorded in round 2 through the
  current code. The on-device prompts did not change.
- **The scorer became slightly more lenient**, in four stated ways: only letters and digits have
  to be covered (a hyphen or full stop between two covered parts does not count as a leak); a
  label word in front of a number ("Room 214B", "#20841") need not be covered; nor does a
  possessive ending on a name; nor does a joining word between two covered places ("Culebra Rd
  and N. Zarzamora St"). These apply to both sets.
- **Flag-only groups are judged by "flagged".** Health details, special-category facts and
  indirect identifiers are underlined for the user to review, not replaced, because the
  question may depend on the fact. For these, a sub-category counts as done when every item has
  some part underlined. Fully covered is much lower (40% on the first set, 29% on the second).
- **More underlines.** The word lists add flags that match nothing in the answer keys: about
  half of all flags (52% on the first set, 59% on the second). Nothing is replaced by a flag,
  but it is more for the user to look at.

## What changed in the app

- Street addresses are read before dates and reference numbers, stay on one line and in one
  table cell, and cover unit-first, grid, rural-route, lettered county road and French-Canadian
  forms. A street named without a number is a place.
- Organization names grow over the words that finish them ("Blue Shield" + "PPO"), drop a role
  word in front ("Defendant ..."), and are found in capitals when the whole run of capitals is
  the name. "Estate of ..." is a party of its own.
- People: surnames from case names and "the Hartung residence"; "Last, First" when only the
  first name is known; initials in brackets, before a colon and in table cells; lower-case
  typist initials; one-letter sign-offs; a model misspelling no longer hides the real surname;
  role words ("Defendants") and street words ("Drive") are never a person.
- Tables: headings may hold "401(k)" or a year; Markdown tables are read; new column kinds
  (plate, card security code, expiry, user name).
- Numbers: court numbers after a case name, short labelled numbers ("lot 203-B"), bar and
  regulator numbers, SSN and account endings, card security codes, PINs and door codes, state
  business IDs, small figures in a row of amounts, amounts in words and spoken digits, rates
  ("$89/mo"), European and French-Canadian formats, ages given as a bare number.
- Passwords are recognized by shape (capital, small letter, digit and symbol in one word); user
  names by the word before them or by being built from a known person's name.
- New file `src/core/sensitive-terms.ts`: general word lists for health details, the special
  categories (immigration, criminal history, religion, race, court obligations, union, politics,
  orientation, genetics) and identifying circumstances (relatives, one-of-a-kind roles, vehicles).

## What is left, and why it stops here

Ten sub-categories are below 100%, all in the flag-only groups, with 31 items between them that
get no underline at all. They are bare numbers with no word beside them (a screening score of
"14", a breath reading of "0.158", "58%"), one-off phrasings ("shoved her into the kitchen
counter", "being acquired by a private equity roll-up") and unlabelled proper names ("Pelican
unit", a boat called "Polish Princess"). A rule for any of these would be a rule for one
document. The route to these is the on-device model: a better topics prompt, or a faster
machine that can afford a second pass.

## Reproduce

```
npx vite --host 127.0.0.1 --port 5173 --strictPort          # dev server, in another terminal
python3 -P tools/evaluation/progress.py --guard             # both sets, replayed with the current code
python3 -P tools/evaluation/misses.py work CATEGORY "Sub-category"   # first set only
```

Kept result folders: `results/c1-round3`, `results/c2-round3`.
