# Evaluation: run `baseline`, split `all`

100 documents, 7002 occurrences of sensitive values in the answer keys.

| Measure | Caught | Of | Rate |
|---|---|---|---|
| Everything in the answer keys | 4040 | 7002 |  57.7% |
| Core categories (23 with a detector at baseline) | 3971 | 5777 |  68.7% |
| Same, with the on-device model switched off (code only) | 2214 | 5777 |  38.3% |
| Places, passwords, device IDs (simple detector added after baseline) | 68 | 654 |  10.4% |
| Health details, sensitive attributes, indirect identifiers (no detector) | 1 | 571 |   0.2% |

Within core categories: 419 partly caught, 1221 missed, 166 lost in import.
Model: 182 chunks, 0 failed after one retry, 47.3 minutes of model time.

## By category

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| person_name | 1174 | 89 | 308 | 0 | 1571 |  74.7% |
| money_amount | 645 | 31 | 163 | 65 | 904 |  71.3% |
| organization_name | 583 | 79 | 96 | 0 | 758 |  76.9% |
| date | 480 | 48 | 92 | 88 | 708 |  67.8% |
| place (new detector) | 62 | 1 | 464 | 0 | 527 |  11.8% |
| record_number | 120 | 68 | 196 | 0 | 384 |  31.2% |
| health_info (no detector) | 0 | 5 | 312 | 0 | 317 |   0.0% |
| phone | 220 | 21 | 2 | 0 | 243 |  90.5% |
| email | 149 | 0 | 3 | 0 | 152 |  98.0% |
| street_address | 63 | 36 | 51 | 0 | 150 |  42.0% |
| sensitive_attribute (no detector) | 1 | 13 | 133 | 0 | 147 |   0.7% |
| postal_code | 106 | 4 | 26 | 0 | 136 |  77.9% |
| bank_account | 46 | 13 | 60 | 0 | 119 |  38.7% |
| indirect_identifier (no detector) | 0 | 19 | 88 | 0 | 107 |   0.0% |
| government_id | 17 | 13 | 69 | 0 | 99 |  17.2% |
| date_of_birth | 71 | 2 | 5 | 13 | 91 |  78.0% |
| tax_id | 69 | 1 | 14 | 0 | 84 |  82.1% |
| credential (new detector) | 3 | 6 | 63 | 0 | 72 |   4.2% |
| payment_card | 43 | 1 | 26 | 0 | 70 |  61.4% |
| ssn | 30 | 2 | 30 | 0 | 62 |  48.4% |
| vehicle_id | 19 | 1 | 40 | 0 | 60 |  31.7% |
| device_id (new detector) | 3 | 6 | 46 | 0 | 55 |   5.5% |
| routing_number | 33 | 0 | 12 | 0 | 45 |  73.3% |
| ip_address | 28 | 0 | 5 | 0 | 33 |  84.8% |
| url | 30 | 1 | 0 | 0 | 31 |  96.8% |
| card_expiry | 17 | 1 | 3 | 0 | 21 |  81.0% |
| age_over_89 | 0 | 8 | 12 | 0 | 20 |   0.0% |
| iban | 20 | 0 | 0 | 0 | 20 | 100.0% |
| card_security_code | 8 | 0 | 8 | 0 | 16 |  50.0% |

## By difficulty (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| standard | 3273 | 267 | 533 | 140 | 4213 |  77.7% |
| hard | 698 | 152 | 688 | 26 | 1564 |  44.6% |

## Names by written form

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| full | 833 | 72 | 94 | 0 | 999 |  83.4% |
| first-name | 327 | 0 | 38 | 0 | 365 |  89.6% |
| short | 167 | 36 | 51 | 0 | 254 |  65.7% |
| title-surname | 178 | 6 | 21 | 0 | 205 |  86.8% |
| nickname | 83 | 2 | 54 | 0 | 139 |  59.7% |
| surname | 82 | 0 | 29 | 0 | 111 |  73.9% |
| initials | 11 | 0 | 72 | 0 | 83 |  13.3% |
| last-first | 17 | 49 | 9 | 0 | 75 |  22.7% |
| caps | 25 | 3 | 23 | 0 | 51 |  49.0% |
| acronym | 34 | 0 | 13 | 0 | 47 |  72.3% |

## By file format (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| txt | 1572 | 146 | 506 | 0 | 2224 |  70.7% |
| xlsx | 436 | 58 | 135 | 166 | 795 |  54.8% |
| pdf | 550 | 56 | 183 | 0 | 789 |  69.7% |
| docx | 420 | 45 | 125 | 0 | 590 |  71.2% |
| eml | 361 | 42 | 99 | 0 | 502 |  71.9% |
| html | 256 | 32 | 74 | 0 | 362 |  70.7% |
| rtf | 130 | 10 | 37 | 0 | 177 |  73.4% |
| md | 126 | 9 | 35 | 0 | 170 |  74.1% |
| pptx | 120 | 21 | 27 | 0 | 168 |  71.4% |

## By audience (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| accounting | 1608 | 185 | 529 | 166 | 2488 |  64.6% |
| legal | 1654 | 148 | 468 | 0 | 2270 |  72.9% |
| health | 382 | 51 | 140 | 0 | 573 |  66.7% |
| general | 327 | 35 | 84 | 0 | 446 |  73.3% |

## Over-redaction

218 of 4727 detections (4.6%) touched nothing in the answer key. These would be replaced unnecessarily (the user can untick them, and the value is restored afterwards).

| Detector | Extra detections |
|---|---|
| company | 66 |
| date | 58 |
| money | 39 |
| person | 28 |
| account | 26 |
| ip | 1 |

