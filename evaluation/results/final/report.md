# Evaluation: run `final`, split `all`

100 documents, 6997 occurrences of sensitive values in the answer keys.

| Measure | Caught | Of | Rate |
|---|---|---|---|
| Everything in the answer keys | 5742 | 6997 |  82.1% |
| Core categories (23 with a detector at baseline) | 5350 | 5772 |  92.7% |
| Same, with the on-device model switched off (code only) | 4845 | 5772 |  83.9% |
| Places, passwords, device IDs (simple detector added after baseline) | 387 | 654 |  59.2% |
| Health details, sensitive attributes, indirect identifiers (no detector) | 5 | 571 |   0.9% |

Within core categories: 128 partly caught, 292 missed, 2 lost in import.
Model: 182 chunks, 0 failed after one retry, 0.0 minutes of model time.

## By category

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| person_name | 1451 | 24 | 96 | 0 | 1571 |  92.4% |
| money_amount | 859 | 7 | 31 | 2 | 899 |  95.6% |
| organization_name | 710 | 42 | 6 | 0 | 758 |  93.7% |
| date | 680 | 6 | 22 | 0 | 708 |  96.0% |
| place (new detector) | 302 | 6 | 219 | 0 | 527 |  57.3% |
| record_number | 334 | 22 | 28 | 0 | 384 |  87.0% |
| health_info (no detector) | 1 | 17 | 299 | 0 | 317 |   0.3% |
| phone | 239 | 1 | 3 | 0 | 243 |  98.4% |
| email | 152 | 0 | 0 | 0 | 152 | 100.0% |
| street_address | 120 | 12 | 18 | 0 | 150 |  80.0% |
| sensitive_attribute (no detector) | 1 | 30 | 116 | 0 | 147 |   0.7% |
| postal_code | 124 | 3 | 9 | 0 | 136 |  91.2% |
| bank_account | 106 | 4 | 9 | 0 | 119 |  89.1% |
| indirect_identifier (no detector) | 3 | 21 | 83 | 0 | 107 |   2.8% |
| government_id | 82 | 1 | 16 | 0 | 99 |  82.8% |
| date_of_birth | 89 | 1 | 1 | 0 | 91 |  97.8% |
| tax_id | 80 | 1 | 3 | 0 | 84 |  95.2% |
| credential (new detector) | 34 | 4 | 34 | 0 | 72 |  47.2% |
| payment_card | 43 | 1 | 26 | 0 | 70 |  61.4% |
| ssn | 59 | 0 | 3 | 0 | 62 |  95.2% |
| vehicle_id | 54 | 1 | 5 | 0 | 60 |  90.0% |
| device_id (new detector) | 51 | 0 | 4 | 0 | 55 |  92.7% |
| routing_number | 45 | 0 | 0 | 0 | 45 | 100.0% |
| ip_address | 33 | 0 | 0 | 0 | 33 | 100.0% |
| url | 30 | 1 | 0 | 0 | 31 |  96.8% |
| card_expiry | 21 | 0 | 0 | 0 | 21 | 100.0% |
| age_over_89 | 9 | 1 | 10 | 0 | 20 |  45.0% |
| iban | 20 | 0 | 0 | 0 | 20 | 100.0% |
| card_security_code | 10 | 0 | 6 | 0 | 16 |  62.5% |

## By difficulty (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| standard | 4046 | 76 | 84 | 2 | 4208 |  96.2% |
| hard | 1304 | 52 | 208 | 0 | 1564 |  83.4% |

## Names by written form

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| full | 953 | 41 | 5 | 0 | 999 |  95.4% |
| first-name | 333 | 0 | 32 | 0 | 365 |  91.2% |
| short | 242 | 9 | 3 | 0 | 254 |  95.3% |
| title-surname | 204 | 1 | 0 | 0 | 205 |  99.5% |
| nickname | 112 | 1 | 26 | 0 | 139 |  80.6% |
| surname | 102 | 0 | 9 | 0 | 111 |  91.9% |
| initials | 63 | 0 | 20 | 0 | 83 |  75.9% |
| last-first | 65 | 10 | 0 | 0 | 75 |  86.7% |
| caps | 42 | 4 | 5 | 0 | 51 |  82.4% |
| acronym | 45 | 0 | 2 | 0 | 47 |  95.7% |

## By file format (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| txt | 2067 | 43 | 114 | 0 | 2224 |  92.9% |
| xlsx | 711 | 16 | 61 | 2 | 790 |  90.0% |
| pdf | 744 | 17 | 28 | 0 | 789 |  94.3% |
| docx | 547 | 22 | 21 | 0 | 590 |  92.7% |
| eml | 449 | 11 | 42 | 0 | 502 |  89.4% |
| html | 343 | 8 | 11 | 0 | 362 |  94.8% |
| rtf | 168 | 4 | 5 | 0 | 177 |  94.9% |
| md | 162 | 3 | 5 | 0 | 170 |  95.3% |
| pptx | 159 | 4 | 5 | 0 | 168 |  94.6% |

## By audience (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| accounting | 2274 | 49 | 158 | 2 | 2483 |  91.6% |
| legal | 2136 | 50 | 84 | 0 | 2270 |  94.1% |
| health | 519 | 23 | 31 | 0 | 573 |  90.6% |
| general | 421 | 6 | 19 | 0 | 446 |  94.4% |

## Over-redaction

438 of 6318 detections (6.9%) touched nothing in the answer key. These would be replaced unnecessarily (the user can untick them, and the value is restored afterwards).

| Detector | Extra detections |
|---|---|
| person | 187 |
| company | 151 |
| date | 30 |
| record | 29 |
| money | 26 |
| account | 7 |
| passport_dl | 4 |
| places | 1 |
| ip | 1 |
| routing | 1 |
| ein | 1 |

