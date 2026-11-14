# Evaluation: run `baseline`, split `dev`

70 documents, 4539 occurrences of sensitive values in the answer keys.

| Measure | Caught | Of | Rate |
|---|---|---|---|
| Everything in the answer keys | 2703 | 4539 |  59.6% |
| Core categories (23 with a detector at baseline) | 2649 | 3766 |  70.3% |
| Same, with the on-device model switched off (code only) | 1494 | 3766 |  39.7% |
| Places, passwords, device IDs (simple detector added after baseline) | 54 | 438 |  12.3% |
| Health details, sensitive attributes, indirect identifiers (no detector) | 0 | 335 |   0.0% |

Within core categories: 281 partly caught, 806 missed, 30 lost in import.
Model: 125 chunks, 0 failed after one retry, 31.8 minutes of model time.

## By category

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| person_name | 773 | 50 | 219 | 0 | 1042 |  74.2% |
| money_amount | 426 | 23 | 114 | 30 | 593 |  71.8% |
| organization_name | 382 | 59 | 71 | 0 | 512 |  74.6% |
| date | 358 | 30 | 63 | 0 | 451 |  79.4% |
| place (new detector) | 50 | 0 | 298 | 0 | 348 |  14.4% |
| record_number | 77 | 48 | 92 | 0 | 217 |  35.5% |
| health_info (no detector) | 0 | 5 | 165 | 0 | 170 |   0.0% |
| phone | 145 | 15 | 2 | 0 | 162 |  89.5% |
| email | 105 | 0 | 3 | 0 | 108 |  97.2% |
| street_address | 42 | 26 | 35 | 0 | 103 |  40.8% |
| sensitive_attribute (no detector) | 0 | 10 | 78 | 0 | 88 |   0.0% |
| postal_code | 65 | 2 | 16 | 0 | 83 |  78.3% |
| bank_account | 29 | 10 | 43 | 0 | 82 |  35.4% |
| indirect_identifier (no detector) | 0 | 17 | 60 | 0 | 77 |   0.0% |
| government_id | 11 | 8 | 47 | 0 | 66 |  16.7% |
| credential (new detector) | 2 | 5 | 51 | 0 | 58 |   3.4% |
| date_of_birth | 51 | 2 | 3 | 0 | 56 |  91.1% |
| tax_id | 38 | 1 | 7 | 0 | 46 |  82.6% |
| ssn | 14 | 0 | 27 | 0 | 41 |  34.1% |
| vehicle_id | 15 | 0 | 24 | 0 | 39 |  38.5% |
| device_id (new detector) | 2 | 2 | 28 | 0 | 32 |   6.2% |
| payment_card | 12 | 1 | 18 | 0 | 31 |  38.7% |
| routing_number | 23 | 0 | 6 | 0 | 29 |  79.3% |
| url | 25 | 1 | 0 | 0 | 26 |  96.2% |
| ip_address | 20 | 0 | 4 | 0 | 24 |  83.3% |
| iban | 17 | 0 | 0 | 0 | 17 | 100.0% |
| card_expiry | 15 | 0 | 0 | 0 | 15 | 100.0% |
| age_over_89 | 0 | 5 | 8 | 0 | 13 |   0.0% |
| card_security_code | 6 | 0 | 4 | 0 | 10 |  60.0% |

## By difficulty (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| standard | 2232 | 192 | 324 | 29 | 2777 |  80.4% |
| hard | 417 | 89 | 482 | 1 | 989 |  42.2% |

## Names by written form

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| full | 534 | 57 | 67 | 0 | 658 |  81.2% |
| first-name | 237 | 0 | 29 | 0 | 266 |  89.1% |
| short | 109 | 25 | 39 | 0 | 173 |  63.0% |
| title-surname | 117 | 4 | 12 | 0 | 133 |  88.0% |
| nickname | 57 | 2 | 41 | 0 | 100 |  57.0% |
| surname | 49 | 0 | 24 | 0 | 73 |  67.1% |
| initials | 7 | 0 | 55 | 0 | 62 |  11.3% |
| acronym | 28 | 0 | 9 | 0 | 37 |  75.7% |
| caps | 15 | 2 | 11 | 0 | 28 |  53.6% |
| last-first | 2 | 19 | 3 | 0 | 24 |   8.3% |

## By file format (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| txt | 1056 | 96 | 329 | 0 | 1481 |  71.3% |
| pdf | 365 | 43 | 142 | 0 | 550 |  66.4% |
| docx | 338 | 38 | 98 | 0 | 474 |  71.3% |
| eml | 268 | 29 | 80 | 0 | 377 |  71.1% |
| html | 223 | 25 | 59 | 0 | 307 |  72.6% |
| rtf | 130 | 10 | 37 | 0 | 177 |  73.4% |
| pptx | 120 | 21 | 27 | 0 | 168 |  71.4% |
| md | 97 | 6 | 23 | 0 | 126 |  77.0% |
| xlsx | 52 | 13 | 11 | 30 | 106 |  49.1% |

## By audience (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| legal | 1079 | 105 | 350 | 0 | 1534 |  70.3% |
| accounting | 1045 | 118 | 314 | 30 | 1507 |  69.3% |
| general | 298 | 32 | 72 | 0 | 402 |  74.1% |
| health | 227 | 26 | 70 | 0 | 323 |  70.3% |

## Over-redaction

124 of 3136 detections (4.0%) touched nothing in the answer key. These would be replaced unnecessarily (the user can untick them, and the value is restored afterwards).

| Detector | Extra detections |
|---|---|
| company | 46 |
| money | 31 |
| person | 28 |
| date | 11 |
| account | 7 |
| ip | 1 |

