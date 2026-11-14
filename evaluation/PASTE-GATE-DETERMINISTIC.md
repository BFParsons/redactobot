# Paste gate: rules only vs rules + Gemini Nano

13 November 2026. Question: can the chat paste gate skip the on-device model and rely on
deterministic rules for the initial paste?

## Method

`tools/evaluation/paste_gate_compare.ts` runs the paste gate's own `makeReport`
(`src/extension/policy.ts`) on every document of a corpus, four ways, and writes runs the
standard scorer reads (`tools/evaluation/score.py`):

- rules only, whole document, and rules only on each ~150-word piece checked on its own
  (a chat paste has far less context than a document);
- rules + saved Nano output (names, places, topics from the live `c2-round4` / `c3-round4`
  runs), whole document and per piece.

The saved model output comes from the document app's prompts, not the paste gate's
single-prompt `extract()`, so the "+ Nano" columns approximate that path. Corpus 2 is the
unseen set; only totals were read. Corpus 3 (working set) was used for the breakdown by name form.

## Results (corpus 2, unseen; share of occurrences fully caught)

| | Rules, paste-sized | + Nano, paste-sized | Rules, whole doc | + Nano, whole doc |
|---|---|---|---|---|
| Person names | **76.6%** | 93.3% | 89.8% | 97.7% |
| Organizations | 85.0% | 94.5% | 91.4% | 96.9% |
| Email, phone, SSN, government/tax IDs, bank, routing, IBAN, cards, DOB | identical in all four columns (88.5-100% per category) | | | |
| Critical identifiers overall | 86.0% | 94.8% | 92.9% | 97.2% |
| Secondary (records, postal codes, dates, money, URLs, IPs, vehicles) | 94.4% | 96.1% | 95.7% | 96.7% |
| Needless replacements | 5.4% | 6.3% | 6.0% | 7.1% |

Corpus 3 agrees (names 74.3% rules vs 92.2% with Nano, paste-sized). By name form (corpus 3,
paste-sized, rules vs Nano): full names 89% vs 96%, first name alone 61% vs 97%, nicknames
56% vs 77%, initials 27% vs 57%, title + surname 97% vs 99%.

Chat-style fixtures (`src/paste-fixtures.ts`, 17): rules alone handle 16 correctly in 2-85 ms.
The miss is a lone first name ("Could you tell Amity that her appointment has been moved?").

## A cheap trigger for when Nano is needed

`tools/evaluation/name_trigger.ts` flags text that might name someone: a capitalized or
all-caps word that does not start a sentence, initials, or a known given name. It fired on
every paste-sized piece that contained a key name (266/266 corpus 2, 206/206 corpus 3) and
would skip Nano on 8 of the 17 chat fixtures (ordinary requests, clean 500/2,000-word text,
email-only and health-only pastes).

## Conclusion

Rules alone are as good as Nano for every structured identifier, but miss about one name in
four in paste-sized text (mostly first names, nicknames and initials). Rules-only is not safe
as the whole gate. Running Nano only when the trigger fires would make many ordinary pastes
instant without missing any name in these corpora.
