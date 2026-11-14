# Evaluation: run `c2-round3`, split `all`

60 documents, 5502 occurrences of sensitive values in the answer keys.

| Measure | Caught | Of | Rate |
|---|---|---|---|
| Everything in the answer keys | 5017 | 5502 |  91.2% |
| Core categories (23 with a detector at baseline) | 4364 | 4527 |  96.4% |
| Same, with the on-device model switched off (code only) | 4215 | 4527 |  93.1% |
| Places, passwords, device IDs (simple detector added after baseline) | 549 | 621 |  88.4% |
| Health details, sensitive attributes, indirect identifiers: fully covered | 104 | 354 |  29.4% |
| Same three, flagged for review (any part highlighted) | 299 | 354 |  84.5% |

Within core categories: 65 partly caught, 98 missed, 0 lost in import.
Model: 128 chunks, 0 failed after one retry, 0.0 minutes of model time.

## By category

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| person_name | 1062 | 15 | 18 | 0 | 1095 |  97.0% |
| money_amount | 677 | 9 | 3 | 0 | 689 |  98.3% |
| date | 622 | 8 | 21 | 0 | 651 |  95.5% |
| place (added after baseline) | 436 | 7 | 32 | 0 | 475 |  91.8% |
| organization_name | 437 | 10 | 6 | 0 | 453 |  96.5% |
| record_number | 388 | 8 | 8 | 0 | 404 |  96.0% |
| phone | 214 | 2 | 2 | 0 | 218 |  98.2% |
| health_info (flag only) | 91 | 96 | 30 | 0 | 217 |  41.9% |
| street_address | 121 | 11 | 6 | 0 | 138 |  87.7% |
| email | 133 | 0 | 0 | 0 | 133 | 100.0% |
| postal_code | 120 | 0 | 3 | 0 | 123 |  97.6% |
| bank_account | 95 | 0 | 3 | 0 | 98 |  96.9% |
| government_id | 89 | 0 | 5 | 0 | 94 |  94.7% |
| sensitive_attribute (flag only) | 9 | 66 | 14 | 0 | 89 |  10.1% |
| credential (added after baseline) | 52 | 1 | 24 | 0 | 77 |  67.5% |
| date_of_birth | 74 | 0 | 0 | 0 | 74 | 100.0% |
| device_id (added after baseline) | 61 | 2 | 6 | 0 | 69 |  88.4% |
| tax_id | 58 | 0 | 0 | 0 | 58 | 100.0% |
| vehicle_id | 47 | 1 | 9 | 0 | 57 |  82.5% |
| payment_card | 45 | 1 | 6 | 0 | 52 |  86.5% |
| indirect_identifier (flag only) | 4 | 33 | 11 | 0 | 48 |   8.3% |
| ssn | 45 | 0 | 3 | 0 | 48 |  93.8% |
| routing_number | 46 | 0 | 1 | 0 | 47 |  97.9% |
| url | 26 | 0 | 0 | 0 | 26 | 100.0% |
| ip_address | 25 | 0 | 0 | 0 | 25 | 100.0% |
| card_expiry | 15 | 0 | 0 | 0 | 15 | 100.0% |
| iban | 12 | 0 | 0 | 0 | 12 | 100.0% |
| age_over_89 | 7 | 0 | 4 | 0 | 11 |  63.6% |
| card_security_code | 6 | 0 | 0 | 0 | 6 | 100.0% |

## By difficulty (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| standard | 3939 | 48 | 53 | 0 | 4040 |  97.5% |
| hard | 425 | 17 | 45 | 0 | 487 |  87.3% |

## Names by written form

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| full | 686 | 12 | 3 | 0 | 701 |  97.9% |
| first-name | 302 | 0 | 0 | 0 | 302 | 100.0% |
| short | 164 | 3 | 3 | 0 | 170 |  96.5% |
| title-surname | 118 | 2 | 0 | 0 | 120 |  98.3% |
| nickname | 74 | 0 | 3 | 0 | 77 |  96.1% |
| initials | 45 | 0 | 11 | 0 | 56 |  80.4% |
| caps | 43 | 7 | 1 | 0 | 51 |  84.3% |
| surname | 33 | 0 | 3 | 0 | 36 |  91.7% |
| last-first | 29 | 1 | 0 | 0 | 30 |  96.7% |
| acronym | 5 | 0 | 0 | 0 | 5 | 100.0% |

## By file format (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| txt | 1621 | 35 | 40 | 0 | 1696 |  95.6% |
| docx | 609 | 7 | 10 | 0 | 626 |  97.3% |
| xlsx | 554 | 3 | 12 | 0 | 569 |  97.4% |
| pdf | 504 | 6 | 10 | 0 | 520 |  96.9% |
| eml | 320 | 6 | 8 | 0 | 334 |  95.8% |
| html | 306 | 4 | 5 | 0 | 315 |  97.1% |
| rtf | 162 | 1 | 3 | 0 | 166 |  97.6% |
| pptx | 154 | 0 | 4 | 0 | 158 |  97.5% |
| md | 134 | 3 | 6 | 0 | 143 |  93.7% |

## By audience (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| legal | 1639 | 33 | 39 | 0 | 1711 |  95.8% |
| accounting | 1630 | 17 | 32 | 0 | 1679 |  97.1% |
| health | 636 | 10 | 9 | 0 | 655 |  97.1% |
| general | 459 | 5 | 18 | 0 | 482 |  95.2% |

## Over-redaction

427 of 5465 replacements (7.8%) touched nothing in the answer key. These would be replaced unnecessarily (the user can untick them, and the value is restored afterwards).

Separately, 475 of 809 sensitive-topic flags (58.7%) touched nothing in the answer key. Flags only underline text; nothing is replaced.

| Detector | Extra detections |
|---|---|
| person | 193 |
| company | 99 |
| places | 37 |
| date | 36 |
| money | 29 |
| record | 16 |
| region | 5 |
| account | 5 |
| zip | 4 |
| passport_dl | 1 |
| street | 1 |
| credential | 1 |

