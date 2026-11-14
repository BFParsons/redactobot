# Evaluation: run `work`, split `all`

100 documents, 6997 occurrences of sensitive values in the answer keys.

| Measure | Caught | Of | Rate |
|---|---|---|---|
| Everything in the answer keys | 6656 | 6997 |  95.1% |
| Core categories (23 with a detector at baseline) | 5772 | 5772 | 100.0% |
| Same, with the on-device model switched off (code only) | 5543 | 5772 |  96.0% |
| Places, passwords, device IDs (simple detector added after baseline) | 654 | 654 | 100.0% |
| Health details, sensitive attributes, indirect identifiers: fully covered | 230 | 571 |  40.3% |
| Same three, flagged for review (any part highlighted) | 540 | 571 |  94.6% |

Within core categories: 0 partly caught, 0 missed, 0 lost in import.
Model: 182 chunks, 0 failed after one retry, 0.0 minutes of model time.

## By category

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| person_name | 1571 | 0 | 0 | 0 | 1571 | 100.0% |
| money_amount | 899 | 0 | 0 | 0 | 899 | 100.0% |
| organization_name | 758 | 0 | 0 | 0 | 758 | 100.0% |
| date | 708 | 0 | 0 | 0 | 708 | 100.0% |
| place (added after baseline) | 527 | 0 | 0 | 0 | 527 | 100.0% |
| record_number | 384 | 0 | 0 | 0 | 384 | 100.0% |
| health_info (flag only) | 144 | 159 | 14 | 0 | 317 |  45.4% |
| phone | 243 | 0 | 0 | 0 | 243 | 100.0% |
| email | 152 | 0 | 0 | 0 | 152 | 100.0% |
| street_address | 150 | 0 | 0 | 0 | 150 | 100.0% |
| sensitive_attribute (flag only) | 36 | 104 | 7 | 0 | 147 |  24.5% |
| postal_code | 136 | 0 | 0 | 0 | 136 | 100.0% |
| bank_account | 119 | 0 | 0 | 0 | 119 | 100.0% |
| indirect_identifier (flag only) | 50 | 47 | 10 | 0 | 107 |  46.7% |
| government_id | 99 | 0 | 0 | 0 | 99 | 100.0% |
| date_of_birth | 91 | 0 | 0 | 0 | 91 | 100.0% |
| tax_id | 84 | 0 | 0 | 0 | 84 | 100.0% |
| credential (added after baseline) | 72 | 0 | 0 | 0 | 72 | 100.0% |
| payment_card | 70 | 0 | 0 | 0 | 70 | 100.0% |
| ssn | 62 | 0 | 0 | 0 | 62 | 100.0% |
| vehicle_id | 60 | 0 | 0 | 0 | 60 | 100.0% |
| device_id (added after baseline) | 55 | 0 | 0 | 0 | 55 | 100.0% |
| routing_number | 45 | 0 | 0 | 0 | 45 | 100.0% |
| ip_address | 33 | 0 | 0 | 0 | 33 | 100.0% |
| url | 31 | 0 | 0 | 0 | 31 | 100.0% |
| card_expiry | 21 | 0 | 0 | 0 | 21 | 100.0% |
| age_over_89 | 20 | 0 | 0 | 0 | 20 | 100.0% |
| iban | 20 | 0 | 0 | 0 | 20 | 100.0% |
| card_security_code | 16 | 0 | 0 | 0 | 16 | 100.0% |

## By difficulty (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| standard | 4208 | 0 | 0 | 0 | 4208 | 100.0% |
| hard | 1564 | 0 | 0 | 0 | 1564 | 100.0% |

## Names by written form

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| full | 999 | 0 | 0 | 0 | 999 | 100.0% |
| first-name | 365 | 0 | 0 | 0 | 365 | 100.0% |
| short | 254 | 0 | 0 | 0 | 254 | 100.0% |
| title-surname | 205 | 0 | 0 | 0 | 205 | 100.0% |
| nickname | 139 | 0 | 0 | 0 | 139 | 100.0% |
| surname | 111 | 0 | 0 | 0 | 111 | 100.0% |
| initials | 83 | 0 | 0 | 0 | 83 | 100.0% |
| last-first | 75 | 0 | 0 | 0 | 75 | 100.0% |
| caps | 51 | 0 | 0 | 0 | 51 | 100.0% |
| acronym | 47 | 0 | 0 | 0 | 47 | 100.0% |

## By file format (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| txt | 2224 | 0 | 0 | 0 | 2224 | 100.0% |
| xlsx | 790 | 0 | 0 | 0 | 790 | 100.0% |
| pdf | 789 | 0 | 0 | 0 | 789 | 100.0% |
| docx | 590 | 0 | 0 | 0 | 590 | 100.0% |
| eml | 502 | 0 | 0 | 0 | 502 | 100.0% |
| html | 362 | 0 | 0 | 0 | 362 | 100.0% |
| rtf | 177 | 0 | 0 | 0 | 177 | 100.0% |
| md | 170 | 0 | 0 | 0 | 170 | 100.0% |
| pptx | 168 | 0 | 0 | 0 | 168 | 100.0% |

## By audience (core categories)

| | Caught | Partly | Missed | Lost in import | Total | Rate |
|---|---|---|---|---|---|---|
| accounting | 2483 | 0 | 0 | 0 | 2483 | 100.0% |
| legal | 2270 | 0 | 0 | 0 | 2270 | 100.0% |
| health | 573 | 0 | 0 | 0 | 573 | 100.0% |
| general | 446 | 0 | 0 | 0 | 446 | 100.0% |

## Over-redaction

436 of 6928 replacements (6.3%) touched nothing in the answer key. These would be replaced unnecessarily (the user can untick them, and the value is restored afterwards).

Separately, 650 of 1243 sensitive-topic flags (52.3%) touched nothing in the answer key. Flags only underline text; nothing is replaced.

| Detector | Extra detections |
|---|---|
| company | 110 |
| person | 95 |
| date | 70 |
| record | 54 |
| places | 32 |
| account | 30 |
| money | 30 |
| region | 7 |
| passport_dl | 2 |
| card_partial | 1 |
| credential | 1 |
| ip | 1 |

