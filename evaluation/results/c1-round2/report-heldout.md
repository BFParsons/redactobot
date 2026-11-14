# Evaluation: run `c1-round2`, split `heldout`

30 documents, 2458 occurrences of sensitive values in the answer keys.

| Measure | Caught | Of | Rate |
|---|---|---|---|
| Everything in the answer keys | 2114 | 2458 |  86.0% |
| Core categories (23 with a detector at baseline) | 1874 | 2006 |  93.4% |
| Same, with the on-device model switched off (code only) | 1754 | 2006 |  87.4% |
| Places, passwords, device IDs (simple detector added after baseline) | 186 | 216 |  86.1% |
| Health details, sensitive attributes, indirect identifiers: fully covered | 54 | 236 |  22.9% |
| Same three, flagged for review (any part highlighted) | 137 | 236 |  58.1% |

Within core categories: 49 partly caught, 81 missed, 2 lost in import.
Model: 57 chunks, 0 failed after one retry, 0.0 minutes of model time.

## By category

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| person_name | 502 | 14 | 13 | 0 | 529 |  94.9% |
| money_amount | 289 | 2 | 13 | 2 | 306 |  94.4% |
| date | 246 | 4 | 7 | 0 | 257 |  95.7% |
| organization_name | 228 | 17 | 1 | 0 | 246 |  92.7% |
| place (added after baseline) | 160 | 2 | 17 | 0 | 179 |  89.4% |
| record_number | 155 | 3 | 9 | 0 | 167 |  92.8% |
| health_info (flag only) | 40 | 56 | 51 | 0 | 147 |  27.2% |
| phone | 81 | 0 | 0 | 0 | 81 | 100.0% |
| sensitive_attribute (flag only) | 12 | 20 | 27 | 0 | 59 |  20.3% |
| postal_code | 49 | 2 | 2 | 0 | 53 |  92.5% |
| street_address | 37 | 5 | 5 | 0 | 47 |  78.7% |
| email | 44 | 0 | 0 | 0 | 44 | 100.0% |
| payment_card | 38 | 0 | 1 | 0 | 39 |  97.4% |
| tax_id | 37 | 0 | 1 | 0 | 38 |  97.4% |
| bank_account | 29 | 1 | 7 | 0 | 37 |  78.4% |
| date_of_birth | 34 | 0 | 1 | 0 | 35 |  97.1% |
| government_id | 25 | 0 | 8 | 0 | 33 |  75.8% |
| indirect_identifier (flag only) | 2 | 7 | 21 | 0 | 30 |   6.7% |
| device_id (added after baseline) | 21 | 0 | 2 | 0 | 23 |  91.3% |
| ssn | 20 | 0 | 1 | 0 | 21 |  95.2% |
| vehicle_id | 16 | 1 | 4 | 0 | 21 |  76.2% |
| routing_number | 16 | 0 | 0 | 0 | 16 | 100.0% |
| credential (added after baseline) | 5 | 1 | 8 | 0 | 14 |  35.7% |
| ip_address | 9 | 0 | 0 | 0 | 9 | 100.0% |
| age_over_89 | 3 | 0 | 4 | 0 | 7 |  42.9% |
| card_expiry | 6 | 0 | 0 | 0 | 6 | 100.0% |
| card_security_code | 2 | 0 | 4 | 0 | 6 |  33.3% |
| url | 5 | 0 | 0 | 0 | 5 | 100.0% |
| iban | 3 | 0 | 0 | 0 | 3 | 100.0% |

## By difficulty (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| standard | 1387 | 27 | 15 | 2 | 1431 |  96.9% |
| hard | 487 | 22 | 66 | 0 | 575 |  84.7% |

## Names by written form

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| full | 322 | 19 | 0 | 0 | 341 |  94.4% |
| first-name | 97 | 0 | 2 | 0 | 99 |  98.0% |
| short | 79 | 2 | 0 | 0 | 81 |  97.5% |
| title-surname | 71 | 1 | 0 | 0 | 72 |  98.6% |
| last-first | 45 | 6 | 0 | 0 | 51 |  88.2% |
| nickname | 36 | 0 | 3 | 0 | 39 |  92.3% |
| surname | 37 | 0 | 1 | 0 | 38 |  97.4% |
| caps | 18 | 3 | 2 | 0 | 23 |  78.3% |
| initials | 15 | 0 | 6 | 0 | 21 |  71.4% |
| acronym | 10 | 0 | 0 | 0 | 10 | 100.0% |

## By file format (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| txt | 675 | 20 | 48 | 0 | 743 |  90.8% |
| xlsx | 662 | 6 | 14 | 2 | 684 |  96.8% |
| pdf | 223 | 10 | 6 | 0 | 239 |  93.3% |
| eml | 115 | 6 | 4 | 0 | 125 |  92.0% |
| docx | 106 | 3 | 7 | 0 | 116 |  91.4% |
| html | 50 | 3 | 2 | 0 | 55 |  90.9% |
| md | 43 | 1 | 0 | 0 | 44 |  97.7% |

## By audience (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| accounting | 919 | 18 | 37 | 2 | 976 |  94.2% |
| legal | 684 | 21 | 31 | 0 | 736 |  92.9% |
| health | 228 | 9 | 13 | 0 | 250 |  91.2% |
| general | 43 | 1 | 0 | 0 | 44 |  97.7% |

## Over-redaction

171 of 2319 replacements (7.4%) touched nothing in the answer key. These would be replaced unnecessarily (the user can untick them, and the value is restored afterwards).

Separately, 68 of 194 sensitive-topic flags (35.1%) touched nothing in the answer key. Flags only underline text; nothing is replaced.

| Detector | Extra detections |
|---|---|
| person | 60 |
| company | 41 |
| record | 26 |
| account | 18 |
| date | 11 |
| places | 7 |
| money | 5 |
| region | 2 |
| passport_dl | 1 |

