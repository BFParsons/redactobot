# Evaluation: run `baseline`, split `heldout`

30 documents, 2463 occurrences of sensitive values in the answer keys.

| Measure | Caught | Of | Rate |
|---|---|---|---|
| Everything in the answer keys | 1337 | 2463 |  54.3% |
| Core categories (23 with a detector at baseline) | 1322 | 2011 |  65.7% |
| Same, with the on-device model switched off (code only) | 720 | 2011 |  35.8% |
| Places, passwords, device IDs (simple detector added after baseline) | 14 | 216 |   6.5% |
| Health details, sensitive attributes, indirect identifiers (no detector) | 1 | 236 |   0.4% |

Within core categories: 138 partly caught, 415 missed, 136 lost in import.
Model: 57 chunks, 0 failed after one retry, 15.5 minutes of model time.

## By category

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| person_name | 401 | 39 | 89 | 0 | 529 |  75.8% |
| money_amount | 219 | 8 | 49 | 35 | 311 |  70.4% |
| date | 122 | 18 | 29 | 88 | 257 |  47.5% |
| organization_name | 201 | 20 | 25 | 0 | 246 |  81.7% |
| place (new detector) | 12 | 1 | 166 | 0 | 179 |   6.7% |
| record_number | 43 | 20 | 104 | 0 | 167 |  25.7% |
| health_info (no detector) | 0 | 0 | 147 | 0 | 147 |   0.0% |
| phone | 75 | 6 | 0 | 0 | 81 |  92.6% |
| sensitive_attribute (no detector) | 1 | 3 | 55 | 0 | 59 |   1.7% |
| postal_code | 41 | 2 | 10 | 0 | 53 |  77.4% |
| street_address | 21 | 10 | 16 | 0 | 47 |  44.7% |
| email | 44 | 0 | 0 | 0 | 44 | 100.0% |
| payment_card | 31 | 0 | 8 | 0 | 39 |  79.5% |
| tax_id | 31 | 0 | 7 | 0 | 38 |  81.6% |
| bank_account | 17 | 3 | 17 | 0 | 37 |  45.9% |
| date_of_birth | 20 | 0 | 2 | 13 | 35 |  57.1% |
| government_id | 6 | 5 | 22 | 0 | 33 |  18.2% |
| indirect_identifier (no detector) | 0 | 2 | 28 | 0 | 30 |   0.0% |
| device_id (new detector) | 1 | 4 | 18 | 0 | 23 |   4.3% |
| ssn | 16 | 2 | 3 | 0 | 21 |  76.2% |
| vehicle_id | 4 | 1 | 16 | 0 | 21 |  19.0% |
| routing_number | 10 | 0 | 6 | 0 | 16 |  62.5% |
| credential (new detector) | 1 | 1 | 12 | 0 | 14 |   7.1% |
| ip_address | 8 | 0 | 1 | 0 | 9 |  88.9% |
| age_over_89 | 0 | 3 | 4 | 0 | 7 |   0.0% |
| card_expiry | 2 | 1 | 3 | 0 | 6 |  33.3% |
| card_security_code | 2 | 0 | 4 | 0 | 6 |  33.3% |
| url | 5 | 0 | 0 | 0 | 5 | 100.0% |
| iban | 3 | 0 | 0 | 0 | 3 | 100.0% |

## By difficulty (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| standard | 1041 | 75 | 209 | 111 | 1436 |  72.5% |
| hard | 281 | 63 | 206 | 25 | 575 |  48.9% |

## Names by written form

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| full | 299 | 15 | 27 | 0 | 341 |  87.7% |
| first-name | 90 | 0 | 9 | 0 | 99 |  90.9% |
| short | 58 | 11 | 12 | 0 | 81 |  71.6% |
| title-surname | 61 | 2 | 9 | 0 | 72 |  84.7% |
| last-first | 15 | 30 | 6 | 0 | 51 |  29.4% |
| nickname | 26 | 0 | 13 | 0 | 39 |  66.7% |
| surname | 33 | 0 | 5 | 0 | 38 |  86.8% |
| caps | 10 | 1 | 12 | 0 | 23 |  43.5% |
| initials | 4 | 0 | 17 | 0 | 21 |  19.0% |
| acronym | 6 | 0 | 4 | 0 | 10 |  60.0% |

## By file format (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| txt | 516 | 50 | 177 | 0 | 743 |  69.4% |
| xlsx | 384 | 45 | 124 | 136 | 689 |  55.7% |
| pdf | 185 | 13 | 41 | 0 | 239 |  77.4% |
| eml | 93 | 13 | 19 | 0 | 125 |  74.4% |
| docx | 82 | 7 | 27 | 0 | 116 |  70.7% |
| html | 33 | 7 | 15 | 0 | 55 |  60.0% |
| md | 29 | 3 | 12 | 0 | 44 |  65.9% |

## By audience (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| accounting | 563 | 67 | 215 | 136 | 981 |  57.4% |
| legal | 575 | 43 | 118 | 0 | 736 |  78.1% |
| health | 155 | 25 | 70 | 0 | 250 |  62.0% |
| general | 29 | 3 | 12 | 0 | 44 |  65.9% |

## Over-redaction

94 of 1591 detections (5.9%) touched nothing in the answer key. These would be replaced unnecessarily (the user can untick them, and the value is restored afterwards).

| Detector | Extra detections |
|---|---|
| date | 47 |
| company | 20 |
| account | 19 |
| money | 8 |

