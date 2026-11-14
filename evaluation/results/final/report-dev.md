# Evaluation: run `final`, split `dev`

70 documents, 4539 occurrences of sensitive values in the answer keys.

| Measure | Caught | Of | Rate |
|---|---|---|---|
| Everything in the answer keys | 3820 | 4539 |  84.2% |
| Core categories (23 with a detector at baseline) | 3542 | 3766 |  94.1% |
| Same, with the on-device model switched off (code only) | 3245 | 3766 |  86.2% |
| Places, passwords, device IDs (simple detector added after baseline) | 273 | 438 |  62.3% |
| Health details, sensitive attributes, indirect identifiers (no detector) | 5 | 335 |   1.5% |

Within core categories: 75 partly caught, 149 missed, 0 lost in import.
Model: 125 chunks, 0 failed after one retry, 0.0 minutes of model time.

## By category

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| person_name | 963 | 13 | 66 | 0 | 1042 |  92.4% |
| money_amount | 575 | 5 | 13 | 0 | 593 |  97.0% |
| organization_name | 484 | 23 | 5 | 0 | 512 |  94.5% |
| date | 443 | 2 | 6 | 0 | 451 |  98.2% |
| place (new detector) | 213 | 5 | 130 | 0 | 348 |  61.2% |
| record_number | 182 | 16 | 19 | 0 | 217 |  83.9% |
| health_info (no detector) | 1 | 12 | 157 | 0 | 170 |   0.6% |
| phone | 158 | 1 | 3 | 0 | 162 |  97.5% |
| email | 108 | 0 | 0 | 0 | 108 | 100.0% |
| street_address | 85 | 7 | 11 | 0 | 103 |  82.5% |
| sensitive_attribute (no detector) | 1 | 19 | 68 | 0 | 88 |   1.1% |
| postal_code | 79 | 1 | 3 | 0 | 83 |  95.2% |
| bank_account | 79 | 1 | 2 | 0 | 82 |  96.3% |
| indirect_identifier (no detector) | 3 | 17 | 57 | 0 | 77 |   3.9% |
| government_id | 57 | 1 | 8 | 0 | 66 |  86.4% |
| credential (new detector) | 29 | 3 | 26 | 0 | 58 |  50.0% |
| date_of_birth | 55 | 1 | 0 | 0 | 56 |  98.2% |
| tax_id | 43 | 1 | 2 | 0 | 46 |  93.5% |
| ssn | 39 | 0 | 2 | 0 | 41 |  95.1% |
| vehicle_id | 38 | 0 | 1 | 0 | 39 |  97.4% |
| device_id (new detector) | 31 | 0 | 1 | 0 | 32 |  96.9% |
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
| standard | 2682 | 45 | 50 | 0 | 2777 |  96.6% |
| hard | 860 | 30 | 99 | 0 | 989 |  87.0% |

## Names by written form

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| full | 631 | 25 | 2 | 0 | 658 |  95.9% |
| first-name | 242 | 0 | 24 | 0 | 266 |  91.0% |
| short | 165 | 5 | 3 | 0 | 173 |  95.4% |
| title-surname | 133 | 0 | 0 | 0 | 133 | 100.0% |
| nickname | 80 | 1 | 19 | 0 | 100 |  80.0% |
| surname | 67 | 0 | 6 | 0 | 73 |  91.8% |
| initials | 49 | 0 | 13 | 0 | 62 |  79.0% |
| acronym | 35 | 0 | 2 | 0 | 37 |  94.6% |
| caps | 25 | 1 | 2 | 0 | 28 |  89.3% |
| last-first | 20 | 4 | 0 | 0 | 24 |  83.3% |

## By file format (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| txt | 1399 | 23 | 59 | 0 | 1481 |  94.5% |
| pdf | 521 | 8 | 21 | 0 | 550 |  94.7% |
| docx | 441 | 19 | 14 | 0 | 474 |  93.0% |
| eml | 339 | 6 | 32 | 0 | 377 |  89.9% |
| html | 293 | 5 | 9 | 0 | 307 |  95.4% |
| rtf | 168 | 4 | 5 | 0 | 177 |  94.9% |
| pptx | 159 | 4 | 5 | 0 | 168 |  94.6% |
| md | 121 | 3 | 2 | 0 | 126 |  96.0% |
| xlsx | 101 | 3 | 2 | 0 | 106 |  95.3% |

## By audience (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| legal | 1455 | 29 | 50 | 0 | 1534 |  94.9% |
| accounting | 1412 | 26 | 69 | 0 | 1507 |  93.7% |
| general | 380 | 6 | 16 | 0 | 402 |  94.5% |
| health | 295 | 14 | 14 | 0 | 323 |  91.3% |

## Over-redaction

266 of 4162 detections (6.4%) touched nothing in the answer key. These would be replaced unnecessarily (the user can untick them, and the value is restored afterwards).

| Detector | Extra detections |
|---|---|
| person | 96 |
| company | 95 |
| money | 22 |
| date | 21 |
| record | 20 |
| account | 7 |
| passport_dl | 1 |
| places | 1 |
| ip | 1 |
| routing | 1 |
| ein | 1 |

