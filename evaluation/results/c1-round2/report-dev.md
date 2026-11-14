# Evaluation: run `c1-round2`, split `dev`

70 documents, 4539 occurrences of sensitive values in the answer keys.

| Measure | Caught | Of | Rate |
|---|---|---|---|
| Everything in the answer keys | 4013 | 4539 |  88.4% |
| Core categories (23 with a detector at baseline) | 3597 | 3766 |  95.5% |
| Same, with the on-device model switched off (code only) | 3381 | 3766 |  89.8% |
| Places, passwords, device IDs (simple detector added after baseline) | 362 | 438 |  82.6% |
| Health details, sensitive attributes, indirect identifiers: fully covered | 54 | 335 |  16.1% |
| Same three, flagged for review (any part highlighted) | 187 | 335 |  55.8% |

Within core categories: 72 partly caught, 97 missed, 0 lost in import.
Model: 125 chunks, 0 failed after one retry, 0.0 minutes of model time.

## By category

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| person_name | 1009 | 10 | 23 | 0 | 1042 |  96.8% |
| money_amount | 575 | 5 | 13 | 0 | 593 |  97.0% |
| organization_name | 484 | 23 | 5 | 0 | 512 |  94.5% |
| date | 442 | 3 | 6 | 0 | 451 |  98.0% |
| place (added after baseline) | 302 | 11 | 35 | 0 | 348 |  86.8% |
| record_number | 184 | 16 | 17 | 0 | 217 |  84.8% |
| health_info (flag only) | 43 | 72 | 55 | 0 | 170 |  25.3% |
| phone | 157 | 2 | 3 | 0 | 162 |  96.9% |
| email | 108 | 0 | 0 | 0 | 108 | 100.0% |
| street_address | 91 | 7 | 5 | 0 | 103 |  88.3% |
| sensitive_attribute (flag only) | 6 | 35 | 47 | 0 | 88 |   6.8% |
| postal_code | 81 | 0 | 2 | 0 | 83 |  97.6% |
| bank_account | 79 | 1 | 2 | 0 | 82 |  96.3% |
| indirect_identifier (flag only) | 5 | 26 | 46 | 0 | 77 |   6.5% |
| government_id | 58 | 0 | 8 | 0 | 66 |  87.9% |
| credential (added after baseline) | 29 | 3 | 26 | 0 | 58 |  50.0% |
| date_of_birth | 55 | 1 | 0 | 0 | 56 |  98.2% |
| tax_id | 43 | 1 | 2 | 0 | 46 |  93.5% |
| ssn | 39 | 0 | 2 | 0 | 41 |  95.1% |
| vehicle_id | 38 | 0 | 1 | 0 | 39 |  97.4% |
| device_id (added after baseline) | 31 | 0 | 1 | 0 | 32 |  96.9% |
| payment_card | 30 | 1 | 0 | 0 | 31 |  96.8% |
| routing_number | 29 | 0 | 0 | 0 | 29 | 100.0% |
| url | 25 | 1 | 0 | 0 | 26 |  96.2% |
| ip_address | 24 | 0 | 0 | 0 | 24 | 100.0% |
| iban | 17 | 0 | 0 | 0 | 17 | 100.0% |
| card_expiry | 15 | 0 | 0 | 0 | 15 | 100.0% |
| age_over_89 | 6 | 1 | 6 | 0 | 13 |  46.2% |
| card_security_code | 8 | 0 | 2 | 0 | 10 |  80.0% |

## By difficulty (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| standard | 2707 | 47 | 23 | 0 | 2777 |  97.5% |
| hard | 890 | 25 | 74 | 0 | 989 |  90.0% |

## Names by written form

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| full | 634 | 24 | 0 | 0 | 658 |  96.4% |
| first-name | 265 | 0 | 1 | 0 | 266 |  99.6% |
| short | 166 | 4 | 3 | 0 | 173 |  96.0% |
| title-surname | 133 | 0 | 0 | 0 | 133 | 100.0% |
| nickname | 95 | 1 | 4 | 0 | 100 |  95.0% |
| surname | 68 | 0 | 5 | 0 | 73 |  93.2% |
| initials | 51 | 0 | 11 | 0 | 62 |  82.3% |
| acronym | 35 | 0 | 2 | 0 | 37 |  94.6% |
| caps | 25 | 1 | 2 | 0 | 28 |  89.3% |
| last-first | 21 | 3 | 0 | 0 | 24 |  87.5% |

## By file format (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| txt | 1413 | 26 | 42 | 0 | 1481 |  95.4% |
| pdf | 525 | 7 | 18 | 0 | 550 |  95.5% |
| docx | 450 | 16 | 8 | 0 | 474 |  94.9% |
| eml | 353 | 6 | 18 | 0 | 377 |  93.6% |
| html | 300 | 4 | 3 | 0 | 307 |  97.7% |
| rtf | 171 | 4 | 2 | 0 | 177 |  96.6% |
| pptx | 160 | 5 | 3 | 0 | 168 |  95.2% |
| md | 120 | 4 | 2 | 0 | 126 |  95.2% |
| xlsx | 105 | 0 | 1 | 0 | 106 |  99.1% |

## By audience (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| legal | 1477 | 26 | 31 | 0 | 1534 |  96.3% |
| accounting | 1437 | 24 | 46 | 0 | 1507 |  95.4% |
| general | 386 | 8 | 8 | 0 | 402 |  96.0% |
| health | 297 | 14 | 12 | 0 | 323 |  92.0% |

## Over-redaction

214 of 4308 replacements (5.0%) touched nothing in the answer key. These would be replaced unnecessarily (the user can untick them, and the value is restored afterwards).

Separately, 81 of 227 sensitive-topic flags (35.7%) touched nothing in the answer key. Flags only underline text; nothing is replaced.

| Detector | Extra detections |
|---|---|
| company | 73 |
| person | 52 |
| money | 22 |
| record | 21 |
| date | 20 |
| region | 9 |
| account | 6 |
| places | 6 |
| card_partial | 1 |
| passport_dl | 1 |
| ip | 1 |
| routing | 1 |

