# Routing Gemini Nano by the rules' own confidence (hackathon-compliant cascade)

14 November 2026. The masker-mini cascade (MASKER-EXPERIMENT.md) needs a second, non-Firebase model,
which the contest overview discourages. This tests the same idea with only the rules: call Nano
only when the rules leave a possible name unexplained.

## Policy (shipped)

`modelNeeded(text, kinds, covered)` in src/extension/model.ts. The scanner passes the rules'
findings (`covered`). Nano runs when:
- names/places are checked and some possible name (`nameCandidates` in src/core/name-trigger.ts:
  capitalized words that do not start a sentence or are unfamiliar starters, initials, known given
  names; titles such as "Dr" excluded) is not inside a rules finding; or
- health/sensitive/context are checked and the text has that vocabulary or an identity context.

Otherwise the rules decide alone. All Nano calls still go through Firebase AI Logic.

## Results

Simulated with saved Nano output (`tools/evaluation/routing_compare.ts`), ~150-word pieces:

| | Nano calls | person | critical |
|---|---|---|---|
| corpus 2 (unseen), previous gate | 274/274 | 93.9% | 95.1% |
| corpus 2 (unseen), rules-coverage routing | 272/274 | 93.9% | 95.1% |
| corpus 3, previous gate | 215/215 | 94.3% | 96.4% |
| corpus 3, rules-coverage routing | 214/215 | 94.3% | 96.4% |
| chat fixtures (17), previous gate | 10 | all names caught | |
| chat fixtures (17), rules-coverage routing | **6** | all names caught | |

No recall lost. Dense client documents almost always contain some unexplained capitalized word
(headings, products, courts), so they still go to Nano; ordinary chat pastes whose names the rules
already caught ("I met with Mira Calder", "Larkspur Fabrication LLC is our client", "tell Amity")
now skip Nano and insert in milliseconds.

## Tried and rejected: ranking pieces for a fixed Nano budget

Ranking by the number of unexplained candidates (or only name-looking ones: given names, initials)
and sending the top 10/25/50% to Nano was no better than random on the unseen corpus
(e.g. 50%: 90.2% vs 89.9% person). Unlike masker-mini's token probabilities, the rules' coverage is
not a graded confidence signal for dense text.
