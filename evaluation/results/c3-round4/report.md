# Evaluation: run `work3`, split `all`

60 documents, 3663 occurrences of sensitive values in the answer keys.

| Measure | Caught | Of | Rate |
|---|---|---|---|
| Everything in the answer keys | 3344 | 3663 |  91.3% |
| Core categories (23 with a detector at baseline) | 2981 | 3047 |  97.8% |
| Same, with the on-device model switched off (code only) | 2873 | 3047 |  94.3% |
| Places, passwords, device IDs (simple detector added after baseline) | 314 | 332 |  94.6% |
| Health details, sensitive attributes, indirect identifiers: fully covered | 49 | 284 |  17.3% |
| Same three, flagged for review (any part highlighted) | 263 | 284 |  92.6% |

Within core categories: 18 partly caught, 42 missed, 6 lost in import.
Model: 107 chunks, 0 failed after one retry, 0.0 minutes of model time.

## By category

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| person_name | 728 | 5 | 26 | 0 | 759 |  95.9% |
| money_amount | 472 | 2 | 2 | 0 | 476 |  99.2% |
| date | 420 | 3 | 0 | 6 | 429 |  97.9% |
| place (added after baseline) | 260 | 4 | 12 | 0 | 276 |  94.2% |
| record_number | 266 | 2 | 2 | 0 | 270 |  98.5% |
| organization_name | 249 | 4 | 5 | 0 | 258 |  96.5% |
| health_info (flag only) | 30 | 104 | 9 | 0 | 143 |  21.0% |
| phone | 125 | 0 | 0 | 0 | 125 | 100.0% |
| street_address | 115 | 0 | 1 | 0 | 116 |  99.1% |
| postal_code | 94 | 0 | 2 | 0 | 96 |  97.9% |
| sensitive_attribute (flag only) | 13 | 70 | 6 | 0 | 89 |  14.6% |
| email | 85 | 0 | 0 | 0 | 85 | 100.0% |
| date_of_birth | 74 | 1 | 0 | 0 | 75 |  98.7% |
| government_id | 57 | 0 | 0 | 0 | 57 | 100.0% |
| bank_account | 53 | 0 | 0 | 0 | 53 | 100.0% |
| indirect_identifier (flag only) | 6 | 40 | 6 | 0 | 52 |  11.5% |
| ssn | 50 | 0 | 2 | 0 | 52 |  96.2% |
| tax_id | 47 | 1 | 1 | 0 | 49 |  95.9% |
| credential (added after baseline) | 32 | 0 | 1 | 0 | 33 |  97.0% |
| payment_card | 31 | 0 | 0 | 0 | 31 | 100.0% |
| routing_number | 25 | 0 | 0 | 0 | 25 | 100.0% |
| vehicle_id | 24 | 0 | 0 | 0 | 24 | 100.0% |
| device_id (added after baseline) | 22 | 0 | 1 | 0 | 23 |  95.7% |
| ip_address | 16 | 0 | 0 | 0 | 16 | 100.0% |
| age_over_89 | 13 | 0 | 0 | 0 | 13 | 100.0% |
| card_expiry | 10 | 0 | 1 | 0 | 11 |  90.9% |
| url | 11 | 0 | 0 | 0 | 11 | 100.0% |
| iban | 9 | 0 | 0 | 0 | 9 | 100.0% |
| card_security_code | 7 | 0 | 0 | 0 | 7 | 100.0% |

## By difficulty (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| standard | 2654 | 11 | 5 | 6 | 2676 |  99.2% |
| hard | 327 | 7 | 37 | 0 | 371 |  88.1% |

## Names by written form

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| full | 466 | 8 | 8 | 0 | 482 |  96.7% |
| first-name | 200 | 0 | 5 | 0 | 205 |  97.6% |
| short | 73 | 0 | 0 | 0 | 73 | 100.0% |
| title-surname | 71 | 0 | 1 | 0 | 72 |  98.6% |
| nickname | 48 | 0 | 9 | 0 | 57 |  84.2% |
| initials | 41 | 0 | 8 | 0 | 49 |  83.7% |
| caps | 36 | 1 | 0 | 0 | 37 |  97.3% |
| surname | 22 | 0 | 0 | 0 | 22 | 100.0% |
| last-first | 20 | 0 | 0 | 0 | 20 | 100.0% |

## By file format (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| txt | 937 | 14 | 32 | 0 | 983 |  95.3% |
| xlsx | 628 | 1 | 0 | 6 | 635 |  98.9% |
| eml | 304 | 1 | 4 | 0 | 309 |  98.4% |
| docx | 291 | 0 | 0 | 0 | 291 | 100.0% |
| pdf | 283 | 1 | 4 | 0 | 288 |  98.3% |
| md | 206 | 0 | 0 | 0 | 206 | 100.0% |
| html | 156 | 1 | 2 | 0 | 159 |  98.1% |
| rtf | 90 | 0 | 0 | 0 | 90 | 100.0% |
| pptx | 86 | 0 | 0 | 0 | 86 | 100.0% |

## By audience (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| legal | 1113 | 6 | 19 | 0 | 1138 |  97.8% |
| accounting | 1000 | 8 | 17 | 6 | 1031 |  97.0% |
| general | 530 | 3 | 6 | 0 | 539 |  98.3% |
| health | 338 | 1 | 0 | 0 | 339 |  99.7% |

## Over-redaction

173 of 3538 replacements (4.9%) touched nothing in the answer key. These would be replaced unnecessarily (the user can untick them, and the value is restored afterwards).

Separately, 360 of 705 sensitive-topic flags (51.1%) touched nothing in the answer key. Flags only underline text; nothing is replaced.

| Detector | Extra detections |
|---|---|
| person | 53 |
| date | 30 |
| company | 22 |
| region | 17 |
| record | 14 |
| places | 14 |
| money | 10 |
| zip | 7 |
| passport_dl | 3 |
| account | 1 |
| credential | 1 |
| phone | 1 |

