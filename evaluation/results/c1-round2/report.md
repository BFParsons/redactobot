# Evaluation: run `c1-round2`, split `all`

100 documents, 6997 occurrences of sensitive values in the answer keys.

| Measure | Caught | Of | Rate |
|---|---|---|---|
| Everything in the answer keys | 6127 | 6997 |  87.6% |
| Core categories (23 with a detector at baseline) | 5471 | 5772 |  94.8% |
| Same, with the on-device model switched off (code only) | 5135 | 5772 |  89.0% |
| Places, passwords, device IDs (simple detector added after baseline) | 548 | 654 |  83.8% |
| Health details, sensitive attributes, indirect identifiers: fully covered | 108 | 571 |  18.9% |
| Same three, flagged for review (any part highlighted) | 324 | 571 |  56.7% |

Within core categories: 121 partly caught, 178 missed, 2 lost in import.
Model: 182 chunks, 0 failed after one retry, 0.0 minutes of model time.

## By category

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| person_name | 1511 | 24 | 36 | 0 | 1571 |  96.2% |
| money_amount | 864 | 7 | 26 | 2 | 899 |  96.1% |
| organization_name | 712 | 40 | 6 | 0 | 758 |  93.9% |
| date | 688 | 7 | 13 | 0 | 708 |  97.2% |
| place (added after baseline) | 462 | 13 | 52 | 0 | 527 |  87.7% |
| record_number | 339 | 19 | 26 | 0 | 384 |  88.3% |
| health_info (flag only) | 83 | 128 | 106 | 0 | 317 |  26.2% |
| phone | 238 | 2 | 3 | 0 | 243 |  97.9% |
| email | 152 | 0 | 0 | 0 | 152 | 100.0% |
| street_address | 128 | 12 | 10 | 0 | 150 |  85.3% |
| sensitive_attribute (flag only) | 18 | 55 | 74 | 0 | 147 |  12.2% |
| postal_code | 130 | 2 | 4 | 0 | 136 |  95.6% |
| bank_account | 108 | 2 | 9 | 0 | 119 |  90.8% |
| indirect_identifier (flag only) | 7 | 33 | 67 | 0 | 107 |   6.5% |
| government_id | 83 | 0 | 16 | 0 | 99 |  83.8% |
| date_of_birth | 89 | 1 | 1 | 0 | 91 |  97.8% |
| tax_id | 80 | 1 | 3 | 0 | 84 |  95.2% |
| credential (added after baseline) | 34 | 4 | 34 | 0 | 72 |  47.2% |
| payment_card | 68 | 1 | 1 | 0 | 70 |  97.1% |
| ssn | 59 | 0 | 3 | 0 | 62 |  95.2% |
| vehicle_id | 54 | 1 | 5 | 0 | 60 |  90.0% |
| device_id (added after baseline) | 52 | 0 | 3 | 0 | 55 |  94.5% |
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
| standard | 4094 | 74 | 38 | 2 | 4208 |  97.3% |
| hard | 1377 | 47 | 140 | 0 | 1564 |  88.0% |

## Names by written form

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| full | 956 | 43 | 0 | 0 | 999 |  95.7% |
| first-name | 362 | 0 | 3 | 0 | 365 |  99.2% |
| short | 245 | 6 | 3 | 0 | 254 |  96.5% |
| title-surname | 204 | 1 | 0 | 0 | 205 |  99.5% |
| nickname | 131 | 1 | 7 | 0 | 139 |  94.2% |
| surname | 105 | 0 | 6 | 0 | 111 |  94.6% |
| initials | 66 | 0 | 17 | 0 | 83 |  79.5% |
| last-first | 66 | 9 | 0 | 0 | 75 |  88.0% |
| caps | 43 | 4 | 4 | 0 | 51 |  84.3% |
| acronym | 45 | 0 | 2 | 0 | 47 |  95.7% |

## By file format (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| txt | 2088 | 46 | 90 | 0 | 2224 |  93.9% |
| xlsx | 767 | 6 | 15 | 2 | 790 |  97.1% |
| pdf | 748 | 17 | 24 | 0 | 789 |  94.8% |
| docx | 556 | 19 | 15 | 0 | 590 |  94.2% |
| eml | 468 | 12 | 22 | 0 | 502 |  93.2% |
| html | 350 | 7 | 5 | 0 | 362 |  96.7% |
| rtf | 171 | 4 | 2 | 0 | 177 |  96.6% |
| md | 163 | 5 | 2 | 0 | 170 |  95.9% |
| pptx | 160 | 5 | 3 | 0 | 168 |  95.2% |

## By audience (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| accounting | 2356 | 42 | 83 | 2 | 2483 |  94.9% |
| legal | 2161 | 47 | 62 | 0 | 2270 |  95.2% |
| health | 525 | 23 | 25 | 0 | 573 |  91.6% |
| general | 429 | 9 | 8 | 0 | 446 |  96.2% |

## Over-redaction

385 of 6627 replacements (5.8%) touched nothing in the answer key. These would be replaced unnecessarily (the user can untick them, and the value is restored afterwards).

Separately, 149 of 421 sensitive-topic flags (35.4%) touched nothing in the answer key. Flags only underline text; nothing is replaced.

| Detector | Extra detections |
|---|---|
| company | 114 |
| person | 112 |
| record | 47 |
| date | 31 |
| money | 27 |
| account | 24 |
| places | 13 |
| region | 11 |
| passport_dl | 2 |
| card_partial | 1 |
| ip | 1 |
| routing | 1 |

