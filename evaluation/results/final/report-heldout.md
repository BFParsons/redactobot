# Evaluation: run `final`, split `heldout`

30 documents, 2458 occurrences of sensitive values in the answer keys.

| Measure | Caught | Of | Rate |
|---|---|---|---|
| Everything in the answer keys | 1922 | 2458 |  78.2% |
| Core categories (23 with a detector at baseline) | 1808 | 2006 |  90.1% |
| Same, with the on-device model switched off (code only) | 1600 | 2006 |  79.8% |
| Places, passwords, device IDs (simple detector added after baseline) | 114 | 216 |  52.8% |
| Health details, sensitive attributes, indirect identifiers (no detector) | 0 | 236 |   0.0% |

Within core categories: 53 partly caught, 143 missed, 2 lost in import.
Model: 57 chunks, 0 failed after one retry, 0.0 minutes of model time.

## By category

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| person_name | 488 | 11 | 30 | 0 | 529 |  92.2% |
| money_amount | 284 | 2 | 18 | 2 | 306 |  92.8% |
| date | 237 | 4 | 16 | 0 | 257 |  92.2% |
| organization_name | 226 | 19 | 1 | 0 | 246 |  91.9% |
| place (new detector) | 89 | 1 | 89 | 0 | 179 |  49.7% |
| record_number | 152 | 6 | 9 | 0 | 167 |  91.0% |
| health_info (no detector) | 0 | 5 | 142 | 0 | 147 |   0.0% |
| phone | 81 | 0 | 0 | 0 | 81 | 100.0% |
| sensitive_attribute (no detector) | 0 | 11 | 48 | 0 | 59 |   0.0% |
| postal_code | 45 | 2 | 6 | 0 | 53 |  84.9% |
| street_address | 35 | 5 | 7 | 0 | 47 |  74.5% |
| email | 44 | 0 | 0 | 0 | 44 | 100.0% |
| payment_card | 13 | 0 | 26 | 0 | 39 |  33.3% |
| tax_id | 37 | 0 | 1 | 0 | 38 |  97.4% |
| bank_account | 27 | 3 | 7 | 0 | 37 |  73.0% |
| date_of_birth | 34 | 0 | 1 | 0 | 35 |  97.1% |
| government_id | 25 | 0 | 8 | 0 | 33 |  75.8% |
| indirect_identifier (no detector) | 0 | 4 | 26 | 0 | 30 |   0.0% |
| device_id (new detector) | 20 | 0 | 3 | 0 | 23 |  87.0% |
| ssn | 20 | 0 | 1 | 0 | 21 |  95.2% |
| vehicle_id | 16 | 1 | 4 | 0 | 21 |  76.2% |
| routing_number | 16 | 0 | 0 | 0 | 16 | 100.0% |
| credential (new detector) | 5 | 1 | 8 | 0 | 14 |  35.7% |
| ip_address | 9 | 0 | 0 | 0 | 9 | 100.0% |
| age_over_89 | 3 | 0 | 4 | 0 | 7 |  42.9% |
| card_expiry | 6 | 0 | 0 | 0 | 6 | 100.0% |
| card_security_code | 2 | 0 | 4 | 0 | 6 |  33.3% |
| url | 5 | 0 | 0 | 0 | 5 | 100.0% |
| iban | 3 | 0 | 0 | 0 | 3 | 100.0% |

## By difficulty (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| standard | 1364 | 31 | 34 | 2 | 1431 |  95.3% |
| hard | 444 | 22 | 109 | 0 | 575 |  77.2% |

## Names by written form

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| full | 322 | 16 | 3 | 0 | 341 |  94.4% |
| first-name | 91 | 0 | 8 | 0 | 99 |  91.9% |
| short | 77 | 4 | 0 | 0 | 81 |  95.1% |
| title-surname | 71 | 1 | 0 | 0 | 72 |  98.6% |
| last-first | 45 | 6 | 0 | 0 | 51 |  88.2% |
| nickname | 32 | 0 | 7 | 0 | 39 |  82.1% |
| surname | 35 | 0 | 3 | 0 | 38 |  92.1% |
| caps | 17 | 3 | 3 | 0 | 23 |  73.9% |
| initials | 14 | 0 | 7 | 0 | 21 |  66.7% |
| acronym | 10 | 0 | 0 | 0 | 10 | 100.0% |

## By file format (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| txt | 668 | 20 | 55 | 0 | 743 |  89.9% |
| xlsx | 610 | 13 | 59 | 2 | 684 |  89.2% |
| pdf | 223 | 9 | 7 | 0 | 239 |  93.3% |
| eml | 110 | 5 | 10 | 0 | 125 |  88.0% |
| docx | 106 | 3 | 7 | 0 | 116 |  91.4% |
| html | 50 | 3 | 2 | 0 | 55 |  90.9% |
| md | 41 | 0 | 3 | 0 | 44 |  93.2% |

## By audience (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| accounting | 862 | 23 | 89 | 2 | 976 |  88.3% |
| legal | 681 | 21 | 34 | 0 | 736 |  92.5% |
| health | 224 | 9 | 17 | 0 | 250 |  89.6% |
| general | 41 | 0 | 3 | 0 | 44 |  93.2% |

## Over-redaction

172 of 2156 detections (8.0%) touched nothing in the answer key. These would be replaced unnecessarily (the user can untick them, and the value is restored afterwards).

| Detector | Extra detections |
|---|---|
| person | 91 |
| company | 56 |
| record | 9 |
| date | 9 |
| money | 4 |
| passport_dl | 3 |

