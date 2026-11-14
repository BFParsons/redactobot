# Evaluation: run `c2-final`, split `all`

60 documents, 5502 occurrences of sensitive values in the answer keys.

| Measure | Caught | Of | Rate |
|---|---|---|---|
| Everything in the answer keys | 4780 | 5502 |  86.9% |
| Core categories (23 with a detector at baseline) | 4224 | 4527 |  93.3% |
| Same, with the on-device model switched off (code only) | 4022 | 4527 |  88.8% |
| Places, passwords, device IDs (simple detector added after baseline) | 494 | 621 |  79.5% |
| Health details, sensitive attributes, indirect identifiers: fully covered | 62 | 354 |  17.5% |
| Same three, flagged for review (any part highlighted) | 212 | 354 |  59.9% |

Within core categories: 135 partly caught, 168 missed, 0 lost in import.
Model: 128 chunks, 0 failed after one retry, 0.0 minutes of model time.

## By category

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| person_name | 1038 | 29 | 28 | 0 | 1095 |  94.8% |
| money_amount | 653 | 32 | 4 | 0 | 689 |  94.8% |
| date | 597 | 16 | 38 | 0 | 651 |  91.7% |
| place (added after baseline) | 406 | 9 | 60 | 0 | 475 |  85.5% |
| organization_name | 432 | 11 | 10 | 0 | 453 |  95.4% |
| record_number | 371 | 18 | 15 | 0 | 404 |  91.8% |
| phone | 213 | 2 | 3 | 0 | 218 |  97.7% |
| health_info (flag only) | 54 | 93 | 70 | 0 | 217 |  24.9% |
| street_address | 112 | 19 | 7 | 0 | 138 |  81.2% |
| email | 133 | 0 | 0 | 0 | 133 | 100.0% |
| postal_code | 113 | 0 | 10 | 0 | 123 |  91.9% |
| bank_account | 87 | 2 | 9 | 0 | 98 |  88.8% |
| government_id | 84 | 1 | 9 | 0 | 94 |  89.4% |
| sensitive_attribute (flag only) | 7 | 37 | 45 | 0 | 89 |   7.9% |
| credential (added after baseline) | 26 | 2 | 49 | 0 | 77 |  33.8% |
| date_of_birth | 73 | 1 | 0 | 0 | 74 |  98.6% |
| device_id (added after baseline) | 62 | 1 | 6 | 0 | 69 |  89.9% |
| tax_id | 57 | 1 | 0 | 0 | 58 |  98.3% |
| vehicle_id | 46 | 1 | 10 | 0 | 57 |  80.7% |
| payment_card | 43 | 1 | 8 | 0 | 52 |  82.7% |
| indirect_identifier (flag only) | 1 | 20 | 27 | 0 | 48 |   2.1% |
| ssn | 41 | 0 | 7 | 0 | 48 |  85.4% |
| routing_number | 45 | 0 | 2 | 0 | 47 |  95.7% |
| url | 23 | 1 | 2 | 0 | 26 |  88.5% |
| ip_address | 25 | 0 | 0 | 0 | 25 | 100.0% |
| card_expiry | 15 | 0 | 0 | 0 | 15 | 100.0% |
| iban | 12 | 0 | 0 | 0 | 12 | 100.0% |
| age_over_89 | 6 | 0 | 5 | 0 | 11 |  54.5% |
| card_security_code | 5 | 0 | 1 | 0 | 6 |  83.3% |

## By difficulty (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| standard | 3824 | 120 | 96 | 0 | 4040 |  94.7% |
| hard | 400 | 15 | 72 | 0 | 487 |  82.1% |

## Names by written form

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| full | 668 | 28 | 5 | 0 | 701 |  95.3% |
| first-name | 302 | 0 | 0 | 0 | 302 | 100.0% |
| short | 162 | 4 | 4 | 0 | 170 |  95.3% |
| title-surname | 117 | 2 | 1 | 0 | 120 |  97.5% |
| nickname | 74 | 0 | 3 | 0 | 77 |  96.1% |
| initials | 41 | 0 | 15 | 0 | 56 |  73.2% |
| caps | 42 | 5 | 4 | 0 | 51 |  82.4% |
| surname | 31 | 0 | 5 | 0 | 36 |  86.1% |
| last-first | 29 | 1 | 0 | 0 | 30 |  96.7% |
| acronym | 4 | 0 | 1 | 0 | 5 |  80.0% |

## By file format (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| txt | 1551 | 76 | 69 | 0 | 1696 |  91.5% |
| docx | 600 | 12 | 14 | 0 | 626 |  95.8% |
| xlsx | 541 | 7 | 21 | 0 | 569 |  95.1% |
| pdf | 490 | 13 | 17 | 0 | 520 |  94.2% |
| eml | 313 | 9 | 12 | 0 | 334 |  93.7% |
| html | 297 | 10 | 8 | 0 | 315 |  94.3% |
| rtf | 156 | 4 | 6 | 0 | 166 |  94.0% |
| pptx | 150 | 0 | 8 | 0 | 158 |  94.9% |
| md | 126 | 4 | 13 | 0 | 143 |  88.1% |

## By audience (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| legal | 1595 | 54 | 62 | 0 | 1711 |  93.2% |
| accounting | 1582 | 36 | 61 | 0 | 1679 |  94.2% |
| health | 609 | 32 | 14 | 0 | 655 |  93.0% |
| general | 438 | 13 | 31 | 0 | 482 |  90.9% |

## Over-redaction

402 of 5318 replacements (7.6%) touched nothing in the answer key. These would be replaced unnecessarily (the user can untick them, and the value is restored afterwards).

Separately, 119 of 307 sensitive-topic flags (38.8%) touched nothing in the answer key. Flags only underline text; nothing is replaced.

| Detector | Extra detections |
|---|---|
| person | 191 |
| company | 121 |
| money | 25 |
| date | 20 |
| places | 17 |
| record | 16 |
| account | 5 |
| region | 4 |
| passport_dl | 1 |
| street | 1 |
| credential | 1 |

