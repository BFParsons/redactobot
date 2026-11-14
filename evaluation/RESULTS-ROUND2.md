# Detection evaluation, round 2 (2026-11-11)

Round 1 is in [RESULTS.md](RESULTS.md). This round built eight enhancements, added a second test
set that nobody has inspected, made state handling follow the rule sets exactly, and ran an
experiment on using the on-device model as a judge.

**Result: on the fresh test set, the app fully catches 93.3% of sensitive values in its core
categories (91.3% with the round-1 code), 80% of places, passwords and device IDs (53% before),
and flags 60% of health details and other sensitive topics (12% before).** Needless
replacements fell from 8.7% to 7.6%. The cost is time: the second on-device request roughly
doubles model time per page.

Everything in both test sets is fictional.

## Test sets

| | First set | Fresh set |
|---|---|---|
| Documents | 100 (`corpus/`) | 60 (`corpus2/`, numbered 201–260) |
| Answer-key items | 6,120 | 4,857 |
| Written by | a separate agent that had not seen the detection code | the same way, with new people, organizations and storylines |
| Key check | `verify_corpus.py`: 0 mismatches | `verify_corpus2.py`: 0 mismatches, 0 unreviewed leftovers |
| Used to guide fixes | 70 development documents | never; only totals have been read |
| Extra markings | none | names of minors (19 documents) and cardholders (23 documents) |

The first set's 30 held-out documents have now been used for several totals-based decisions, so
the fresh set is the cleaner measure.

## Results

| | First set, round 1 | First set, now | Fresh set, round-1 code | Fresh set, now |
|---|---|---|---|---|
| **Core categories** | 92.7% | **94.8%** | 91.3% | **93.3%** |
| Core, with the model switched off (code only) | 83.9% | 89.0% | 85.1% | 88.8% |
| Places, passwords, device IDs | 59.2% | 83.8% | 53.3% | 79.5% |
| Health and other sensitive topics, flagged for review | under 1% | 56.7% | 12.4% | 59.9% |
| Same, every character covered | 0.9% | 18.9% | 2.0% | 17.5% |
| Everything in the answer keys | 82.1% | 87.6% | 81.3% | 86.9% |
| Replacements that matched nothing in the key | 6.9% | 5.8% | 8.7% | 7.6% |
| Sensitive-topic flags that matched nothing in the key | n/a | 35% | n/a | 39% |

First set by split, now: development 95.5%, held-out 93.4% (round 1: 94.1% and 90.1%).

"Core categories" are the same 23 as in round 1. "Flagged" means some part of the phrase is
underlined for the user; sensitive topics are flagged, not replaced, because the question put to
the AI may depend on them. No model request failed in any run (492 chunks).

The fresh set's round-1 figure, 91.3%, matches the 90.1% reported in round 1 for documents never
looked at, which is evidence that figure was honest.

### Selected categories on the fresh set

| Category | Round-1 code | Now |
|---|---|---|
| Person names | 91.1% | 94.8% |
| Organization names | 94.3% | 95.4% |
| Places | 52.4% | 85.5% |
| Record numbers | 87.6% | 91.8% |
| Street addresses | 72.5% | 81.2% |
| Payment cards | 80.8% | 82.7% |
| Passwords and user names | 32.5% | 33.8% |
| Health details, flagged | about 12% | about 60% |

Still weak on the fresh set: passwords and user names (34%), ages over 89 (55%, 11 items),
vehicle IDs (81%), street addresses (81%), SSNs (85%).

## By rule set

Each rule set run on its own, scored against what that rule covers. Full tables:
[results/by-ruleset.md](results/by-ruleset.md) and
[results/by-ruleset-corpus2.md](results/by-ruleset-corpus2.md).

| Rule set | First set, round 1 | First set, now | Fresh set, now | Fresh set, counting flags |
|---|---|---|---|---|
| Customer financial information (GLBA) | 93.0% | 95.8% | 93.5% | 93.5% |
| Tax return information (IRC § 7216) | 85.3% | 94.6% | 92.6% | 92.6% |
| Health information (HIPAA) | 86.2% | 92.3% | 91.4% | 91.9% |
| Payment card data (PCI DSS) | 43.0% | 88.8% | 90.8% | 90.8% |
| Federal court filings (FRCP 5.2) | 81.2% | 93.3% | 88.5% | 88.5% |
| US federal PII guidance (NIST) | 76.0% | 84.5% | 83.4% | 87.6% |
| EU personal data (GDPR) | 73.6% | 82.4% | 82.1% | 86.4% |
| California sensitive personal information (CCPA) | 37.2% | 50.4% | 46.5% | 63.2% |

On the fresh set the answer keys mark who is a minor and who is a cardholder, so those names are
scored for the two rules that single them out: minors' names 99.1% (111 of 112), cardholders'
names 95.2% (157 of 165).

HIPAA is scored without bare states, because that rule lets a state stay (see below).

## What was built

1. **Checks attached to the rule sets that need them.** Partial card and account numbers ("ending
   3637", "x4410") became their own check and are part of the payment-card rules. Places are part
   of tax return information. Under the court-filing rule, a full date at least 16 years older
   than the newest date in the document is treated as a birth date.
2. **Sensitive topics.** A second on-device request per chunk returns places, health details,
   other sensitive details, and first names used on their own. Topics are underlined and left as
   written unless the user selects them.
3. **Places without a state beside them,** from location cues ("lives in Wenatchee", "the
   Stourton depot") and from the model.
4. **Names:** a bundled list of about 1,500 given names and nicknames, with names that are also
   ordinary words ("Grace", "Hunter", "May") accepted only when the sentence treats them as a
   person; initials written with full stops; forms such as "RUNNING BEAR, WENDELL K." linked to
   their person.
5. **Tables read by their headings.** A column headed "Emp ID", "Check #" or "Amount", or a form
   label such as "Passport", says what the value is.
6. **Smaller gaps:** unlabelled passwords and user names, more ways of writing an age, card
   security codes near a card, British, Irish, Dutch and German street forms.
7. **Fewer needless replacements:** role words such as "Plaintiff" and well-known software and
   public bodies are no longer treated as names.
8. **The fresh test set** described above.

Also in this round:

- **States follow the rule sets.** HIPAA lists "geographic subdivisions smaller than a State", so
  under HIPAA alone a state or province is left as written. Tax return information, GLBA, GDPR
  and NIST cover the address or location with no such exception, so under any of those it is
  replaced. When rule sets are combined, the stricter one wins.
- **A bug the research pass found:** in "Dallas, TX 75201", if "Dallas" had already been taken as
  a name or a model place, the state code was left bare. Fixed; places on the first set went
  from 70.8% to 85.4% from this alone.

## Experiment: the on-device model as a judge

The idea: skip the request that asks the model to write out every name. Let code find names
first, then show the model each leftover capitalized phrase and have it pick one of four labels
(person, organization, place, other), with the answer format restricted to those words. This is
the question-and-answer shape used by Jev and the Gemini Decisions API, run on Gemini Nano.
Code: `src/core/decide.ts`; it is used only by the test harness.

On 24 development documents (42 chunks):

| Approach | Person names | Organization names | Places | All core | Needless name or place replacements | Model time per chunk |
|---|---|---|---|---|---|---|
| Code only, no model | 87.8% | 80.2% | 72.1% | 91.9% | 33 of 648 | 0 s |
| Today: model writes out the names | 97.3% | 96.6% | 76.0% | 96.8% | 47 of 694 | 13 s |
| Judge: code first, model labels leftovers | 91.6% | 83.6% | 87.6% | 93.5% | 198 of 902 | 20 s |

**As built, the judge is slower and less accurate, and is not adopted.**

- **It is not faster.** The judge's answers are short, yet it took 20 s per chunk against 13 s.
  That settles a question open since the first benchmark: on this machine the time goes mostly
  into reading the page, not writing the answer. Shorter answers do not buy speed; fewer or
  shorter requests would.
- **It over-labels.** Of 299 candidate phrases it called only 97 "other", so needless
  replacements rose from 7% to 22%.
- **It misses what it is never shown.** Candidates were limited to capitalized phrases in the
  middle of a sentence, so names at the start of a line or in capitals were never judged.
- **It did help places** (76% to 88%), which is the part worth keeping in mind.

What this suggests instead: since reading dominates, the two requests the app now makes per
chunk (names, then places and topics) each pay to read the same page. Combining them into one
request, or having the document read once and questioned twice, is the more promising route to
speed. Neither has been tried.

## Limits

- **Time.** Names take about 13–17 s per chunk and the topic request about 18–20 s, so a page
  now costs roughly twice the model time it did in round 1, on a machine Chrome rates "Very Low".
- **Sensitive-topic keys are incomplete.** Many flags that "matched nothing" are real health
  details the answer keys did not list ("pacemaker", "panic attacks"). The 35–39% figure
  overstates the noise, and the flagged rate understates what was found. Neither can be fixed
  without re-annotating.
- **"Flagged" is a lenient measure:** any overlap counts. The strict figure is given beside it.
- **Indirect identifiers** (family relationships, unique roles, distinctive assets) are still
  essentially uncaught: 2–7% fully covered.
- **Both test sets were written by an AI agent.** They contain no typing errors, no scans and no
  real-world layouts. The research notes recommend a test set with errors added.
- **Development-set fitting.** Round-2 rules were tuned on the first set's 70 development
  documents. The fresh set is the check: its gain (91.3% to 93.3%) is the same size as the first
  set's (92.7% to 94.8%).
- **Scores are from re-scoring stored model output with the committed code,** as in round 1.
  The model output itself comes from live runs: names from `after` and `c2-before`, topics from
  `c1-topics` and `c2-topics`.
- **The cloud step is still untested;** no Firebase project is connected.

## Reproducing

```bash
python3 -P evaluation/verify_corpus2.py --quiet
# Re-score stored model output with the current code (seconds, no model needed):
python3 -P tools/evaluation/run_eval.py my1 --replay c1-topics
python3 -P tools/evaluation/score.py my1 --split heldout
CSA_CORPUS=evaluation/corpus2 python3 -P tools/evaluation/run_eval.py my2 --replay c2-topics
CSA_CORPUS=evaluation/corpus2 python3 -P tools/evaluation/score.py my2
# Per rule set:
CSA_CORPUS=evaluation/corpus2 python3 -P tools/evaluation/by_ruleset.py c2-topics --prefix r2 --out by-ruleset-corpus2.md
# A live run (needs Chrome with Gemini Nano; about 20 s per chunk per request):
python3 -P tools/evaluation/run_eval.py live1                 # names
python3 -P tools/evaluation/run_eval.py live1t --replay live1 --live-topics
```

Stored runs under `results/`: `c1-topics` and `c2-topics` (live model output), `c1-round2` and
`c2-final` (re-scored with the committed code), `c2-before` (fresh set, round-1 code),
`jexp-judge` and `jexp-names` (the judge experiment). Never read the fresh set's misses when
changing code; use totals only.
