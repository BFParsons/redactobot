# Evaluation: run `c2-before`, split `all`

60 documents, 5502 occurrences of sensitive values in the answer keys.

| Measure | Caught | Of | Rate |
|---|---|---|---|
| Everything in the answer keys | 4471 | 5502 |  81.3% |
| Core categories (23 with a detector at baseline) | 4133 | 4527 |  91.3% |
| Same, with the on-device model switched off (code only) | 3854 | 4527 |  85.1% |
| Places, passwords, device IDs (simple detector added after baseline) | 331 | 621 |  53.3% |
| Health details, sensitive attributes, indirect identifiers: fully covered | 7 | 354 |   2.0% |
| Same three, flagged for review (any part highlighted) | 44 | 354 |  12.4% |

Within core categories: 150 partly caught, 244 missed, 0 lost in import.
Model: 128 chunks, 0 failed after one retry, 36.9 minutes of model time.

## By category

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| person_name | 997 | 33 | 65 | 0 | 1095 |  91.1% |
| money_amount | 652 | 32 | 5 | 0 | 689 |  94.6% |
| date | 590 | 18 | 43 | 0 | 651 |  90.6% |
| place (added after baseline) | 249 | 9 | 217 | 0 | 475 |  52.4% |
| organization_name | 427 | 13 | 13 | 0 | 453 |  94.3% |
| record_number | 354 | 24 | 26 | 0 | 404 |  87.6% |
| phone | 210 | 1 | 7 | 0 | 218 |  96.3% |
| health_info (flag only) | 5 | 8 | 204 | 0 | 217 |   2.3% |
| street_address | 100 | 20 | 18 | 0 | 138 |  72.5% |
| email | 133 | 0 | 0 | 0 | 133 | 100.0% |
| postal_code | 113 | 0 | 10 | 0 | 123 |  91.9% |
| bank_account | 87 | 2 | 9 | 0 | 98 |  88.8% |
| government_id | 81 | 2 | 11 | 0 | 94 |  86.2% |
| sensitive_attribute (flag only) | 1 | 15 | 73 | 0 | 89 |   1.1% |
| credential (added after baseline) | 25 | 0 | 52 | 0 | 77 |  32.5% |
| date_of_birth | 73 | 1 | 0 | 0 | 74 |  98.6% |
| device_id (added after baseline) | 57 | 1 | 11 | 0 | 69 |  82.6% |
| tax_id | 57 | 1 | 0 | 0 | 58 |  98.3% |
| vehicle_id | 45 | 1 | 11 | 0 | 57 |  78.9% |
| payment_card | 42 | 1 | 9 | 0 | 52 |  80.8% |
| indirect_identifier (flag only) | 1 | 14 | 33 | 0 | 48 |   2.1% |
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
| standard | 3764 | 135 | 141 | 0 | 4040 |  93.2% |
| hard | 369 | 15 | 103 | 0 | 487 |  75.8% |

## Names by written form

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| full | 658 | 34 | 9 | 0 | 701 |  93.9% |
| first-name | 286 | 0 | 16 | 0 | 302 |  94.7% |
| short | 162 | 4 | 4 | 0 | 170 |  95.3% |
| title-surname | 117 | 1 | 2 | 0 | 120 |  97.5% |
| nickname | 61 | 0 | 16 | 0 | 77 |  79.2% |
| initials | 41 | 0 | 15 | 0 | 56 |  73.2% |
| caps | 42 | 5 | 4 | 0 | 51 |  82.4% |
| surname | 25 | 0 | 11 | 0 | 36 |  69.4% |
| last-first | 28 | 2 | 0 | 0 | 30 |  93.3% |
| acronym | 4 | 0 | 1 | 0 | 5 |  80.0% |

## By file format (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| txt | 1527 | 78 | 91 | 0 | 1696 |  90.0% |
| docx | 592 | 15 | 19 | 0 | 626 |  94.6% |
| xlsx | 497 | 14 | 58 | 0 | 569 |  87.3% |
| pdf | 489 | 14 | 17 | 0 | 520 |  94.0% |
| eml | 311 | 9 | 14 | 0 | 334 |  93.1% |
| html | 296 | 10 | 9 | 0 | 315 |  94.0% |
| rtf | 156 | 3 | 7 | 0 | 166 |  94.0% |
| pptx | 143 | 3 | 12 | 0 | 158 |  90.5% |
| md | 122 | 4 | 17 | 0 | 143 |  85.3% |

## By audience (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| legal | 1567 | 59 | 85 | 0 | 1711 |  91.6% |
| accounting | 1552 | 44 | 83 | 0 | 1679 |  92.4% |
| health | 605 | 31 | 19 | 0 | 655 |  92.4% |
| general | 409 | 16 | 57 | 0 | 482 |  84.9% |

## Over-redaction

442 of 5063 replacements (8.7%) touched nothing in the answer key. These would be replaced unnecessarily (the user can untick them, and the value is restored afterwards).

| Detector | Extra detections |
|---|---|
| person | 207 |
| company | 171 |
| money | 28 |
| record | 14 |
| date | 10 |
| account | 5 |
| places | 4 |
| passport_dl | 1 |
| street | 1 |
| credential | 1 |

