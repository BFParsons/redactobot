# Evaluation: run `c2-round4`, split `all`

60 documents, 5502 occurrences of sensitive values in the answer keys.

| Measure | Caught | Of | Rate |
|---|---|---|---|
| Everything in the answer keys | 5056 | 5502 |  91.9% |
| Core categories (23 with a detector at baseline) | 4390 | 4527 |  97.0% |
| Same, with the on-device model switched off (code only) | 4270 | 4527 |  94.3% |
| Places, passwords, device IDs (simple detector added after baseline) | 557 | 621 |  89.7% |
| Health details, sensitive attributes, indirect identifiers: fully covered | 109 | 354 |  30.8% |
| Same three, flagged for review (any part highlighted) | 302 | 354 |  85.3% |

Within core categories: 61 partly caught, 76 missed, 0 lost in import.
Model: 128 chunks, 0 failed after one retry, 0.0 minutes of model time.

## By category

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| person_name | 1070 | 11 | 14 | 0 | 1095 |  97.7% |
| money_amount | 678 | 9 | 2 | 0 | 689 |  98.4% |
| date | 632 | 5 | 14 | 0 | 651 |  97.1% |
| place (added after baseline) | 442 | 2 | 31 | 0 | 475 |  93.1% |
| organization_name | 438 | 10 | 5 | 0 | 453 |  96.7% |
| record_number | 386 | 9 | 9 | 0 | 404 |  95.5% |
| phone | 216 | 2 | 0 | 0 | 218 |  99.1% |
| health_info (flag only) | 91 | 96 | 30 | 0 | 217 |  41.9% |
| street_address | 121 | 12 | 5 | 0 | 138 |  87.7% |
| email | 133 | 0 | 0 | 0 | 133 | 100.0% |
| postal_code | 122 | 0 | 1 | 0 | 123 |  99.2% |
| bank_account | 95 | 0 | 3 | 0 | 98 |  96.9% |
| government_id | 92 | 0 | 2 | 0 | 94 |  97.9% |
| sensitive_attribute (flag only) | 13 | 64 | 12 | 0 | 89 |  14.6% |
| credential (added after baseline) | 54 | 1 | 22 | 0 | 77 |  70.1% |
| date_of_birth | 74 | 0 | 0 | 0 | 74 | 100.0% |
| device_id (added after baseline) | 61 | 2 | 6 | 0 | 69 |  88.4% |
| tax_id | 57 | 1 | 0 | 0 | 58 |  98.3% |
| vehicle_id | 47 | 1 | 9 | 0 | 57 |  82.5% |
| payment_card | 46 | 0 | 6 | 0 | 52 |  88.5% |
| indirect_identifier (flag only) | 5 | 33 | 10 | 0 | 48 |  10.4% |
| ssn | 46 | 0 | 2 | 0 | 48 |  95.8% |
| routing_number | 47 | 0 | 0 | 0 | 47 | 100.0% |
| url | 26 | 0 | 0 | 0 | 26 | 100.0% |
| ip_address | 25 | 0 | 0 | 0 | 25 | 100.0% |
| card_expiry | 15 | 0 | 0 | 0 | 15 | 100.0% |
| iban | 12 | 0 | 0 | 0 | 12 | 100.0% |
| age_over_89 | 6 | 1 | 4 | 0 | 11 |  54.5% |
| card_security_code | 6 | 0 | 0 | 0 | 6 | 100.0% |

## By difficulty (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| standard | 3959 | 46 | 35 | 0 | 4040 |  98.0% |
| hard | 431 | 15 | 41 | 0 | 487 |  88.5% |

## Names by written form

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| full | 688 | 11 | 2 | 0 | 701 |  98.1% |
| first-name | 302 | 0 | 0 | 0 | 302 | 100.0% |
| short | 165 | 2 | 3 | 0 | 170 |  97.1% |
| title-surname | 119 | 1 | 0 | 0 | 120 |  99.2% |
| nickname | 74 | 0 | 3 | 0 | 77 |  96.1% |
| initials | 48 | 0 | 8 | 0 | 56 |  85.7% |
| caps | 44 | 6 | 1 | 0 | 51 |  86.3% |
| surname | 34 | 0 | 2 | 0 | 36 |  94.4% |
| last-first | 29 | 1 | 0 | 0 | 30 |  96.7% |
| acronym | 5 | 0 | 0 | 0 | 5 | 100.0% |

## By file format (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| txt | 1638 | 28 | 30 | 0 | 1696 |  96.6% |
| docx | 610 | 9 | 7 | 0 | 626 |  97.4% |
| xlsx | 554 | 3 | 12 | 0 | 569 |  97.4% |
| pdf | 504 | 8 | 8 | 0 | 520 |  96.9% |
| eml | 325 | 6 | 3 | 0 | 334 |  97.3% |
| html | 308 | 2 | 5 | 0 | 315 |  97.8% |
| rtf | 163 | 2 | 1 | 0 | 166 |  98.2% |
| pptx | 153 | 0 | 5 | 0 | 158 |  96.8% |
| md | 135 | 3 | 5 | 0 | 143 |  94.4% |

## By audience (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| legal | 1652 | 30 | 29 | 0 | 1711 |  96.6% |
| accounting | 1639 | 17 | 23 | 0 | 1679 |  97.6% |
| health | 640 | 9 | 6 | 0 | 655 |  97.7% |
| general | 459 | 5 | 18 | 0 | 482 |  95.2% |

## Over-redaction

336 of 5390 replacements (6.2%) touched nothing in the answer key. These would be replaced unnecessarily (the user can untick them, and the value is restored afterwards).

Separately, 487 of 824 sensitive-topic flags (59.1%) touched nothing in the answer key. Flags only underline text; nothing is replaced.

| Detector | Extra detections |
|---|---|
| person | 125 |
| company | 82 |
| places | 41 |
| date | 36 |
| money | 21 |
| region | 12 |
| record | 11 |
| zip | 4 |
| passport_dl | 1 |
| street | 1 |
| account | 1 |
| credential | 1 |

