# Catch rate by rule set

Each rule set was run on its own (only its checks switched on) over the 100 fictional documents, and scored
against the kinds of information that rule covers. Names are replayed from the final live model run.
"Caught" means every character of the value was covered. See RESULTS.md for method and limits.

"Counting flags" also counts a health or other sensitive detail as found when any part of it is underlined for review.

| Rank | Rule set | Caught | Of | Rate | Counting flags | Held-out part |
|---|---|---|---|---|---|---|
| 1 | Customer financial information (16 CFR 314.2) | 3402 | 3551 | 95.8% | 95.8% | 94.2% |
| 2 | Tax return information (26 CFR 301.7216-1) | 4573 | 4836 | 94.6% | 94.6% | 93.3% |
| 3 | Federal court filings (Fed. R. Civ. P. 5.2(a)) | 416 | 446 | 93.3% | 93.3% | 91.3% |
| 4 | Health information (18 identifiers) (45 CFR 164.514(b)(2)) | 4216 | 4568 | 92.3% | 92.9% | 91.7% |
| 5 | Payment card data (PCI DSS v4.0.1) | 95 | 107 | 88.8% | 88.8% | 82.4% |
| 6 | US federal PII guidance (NIST SP 800-122) | 3846 | 4551 | 84.5% | 89.2% | 82.4% |
| 7 | EU personal data (GDPR Art. 4, 9, 10) | 3445 | 4181 | 82.4% | 87.4% | 81.2% |
| 8 | California sensitive personal information (Cal. Civ. Code 1798.140(ae)) | 465 | 922 | 50.4% | 67.7% | 46.0% |

## Customer financial information

Consumer report details have no detector and no answer-key category.

| Kind of information | Caught | Of | Rate |
|---|---|---|---|
| email | 152 | 152 | 100.0% |
| routing number | 45 | 45 | 100.0% |
| iban | 20 | 20 | 100.0% |
| payment card | 69 | 70 | 98.6% |
| phone | 238 | 243 | 97.9% |
| person name | 1510 | 1571 | 96.1% |
| money amount | 864 | 899 | 96.1% |
| postal code | 130 | 136 | 95.6% |
| ssn | 59 | 62 | 95.2% |
| tax id | 78 | 84 | 92.9% |
| bank account | 106 | 119 | 89.1% |
| street address | 131 | 150 | 87.3% |

## Tax return information

| Kind of information | Caught | Of | Rate |
|---|---|---|---|
| email | 152 | 152 | 100.0% |
| routing number | 45 | 45 | 100.0% |
| iban | 20 | 20 | 100.0% |
| payment card | 69 | 70 | 98.6% |
| phone | 238 | 243 | 97.9% |
| person name | 1510 | 1571 | 96.1% |
| money amount | 864 | 899 | 96.1% |
| postal code | 130 | 136 | 95.6% |
| ssn | 59 | 62 | 95.2% |
| organization name | 711 | 758 | 93.8% |
| tax id | 78 | 84 | 92.9% |
| bank account | 106 | 119 | 89.1% |
| street address | 131 | 150 | 87.3% |
| place | 460 | 527 | 87.3% |

## Federal court filings

Names of minors are also covered by the rule, but the answer keys do not say who is a minor, so names are not scored here.

| Kind of information | Caught | Of | Rate |
|---|---|---|---|
| iban | 20 | 20 | 100.0% |
| payment card | 68 | 70 | 97.1% |
| ssn | 59 | 62 | 95.2% |
| date of birth | 85 | 91 | 93.4% |
| tax id | 78 | 84 | 92.9% |
| bank account | 106 | 119 | 89.1% |

## Health information (18 identifiers)

Biometrics and photographs do not apply to text. A state or province on its own is not scored: this rule lets it stay.

| Kind of information | Caught | Of | Rate |
|---|---|---|---|
| email | 152 | 152 | 100.0% |
| routing number | 45 | 45 | 100.0% |
| ip address | 33 | 33 | 100.0% |
| iban | 20 | 20 | 100.0% |
| phone | 238 | 243 | 97.9% |
| date of birth | 89 | 91 | 97.8% |
| payment card | 68 | 70 | 97.1% |
| date | 687 | 708 | 97.0% |
| url | 30 | 31 | 96.8% |
| person name | 1509 | 1571 | 96.1% |
| ssn | 59 | 62 | 95.2% |
| device id | 52 | 55 | 94.5% |
| postal code | 128 | 136 | 94.1% |
| tax id | 78 | 84 | 92.9% |
| place | 298 | 328 | 90.9% |
| bank account | 108 | 119 | 90.8% |
| vehicle id | 54 | 60 | 90.0% |
| record number | 343 | 384 | 89.3% |
| street address | 128 | 150 | 85.3% |
| government id | 83 | 99 | 83.8% |
| age over 89 | 9 | 20 | 45.0% |
| indirect identifier | 5 | 107 | 4.7% |

## Payment card data

Cardholder names are covered by the standard, but the answer keys do not say which names are cardholders.

| Kind of information | Caught | Of | Rate |
|---|---|---|---|
| payment card | 68 | 70 | 97.1% |
| card expiry | 17 | 21 | 81.0% |
| card security code | 10 | 16 | 62.5% |

## US federal PII guidance

| Kind of information | Caught | Of | Rate |
|---|---|---|---|
| email | 152 | 152 | 100.0% |
| iban | 20 | 20 | 100.0% |
| payment card | 69 | 70 | 98.6% |
| postal code | 132 | 136 | 97.1% |
| person name | 1512 | 1571 | 96.2% |
| money amount | 864 | 899 | 96.1% |
| ssn | 59 | 62 | 95.2% |
| date of birth | 85 | 91 | 93.4% |
| tax id | 78 | 84 | 92.9% |
| bank account | 106 | 119 | 89.1% |
| street address | 131 | 150 | 87.3% |
| place | 460 | 527 | 87.3% |
| government id | 75 | 99 | 75.8% |
| health info | 78 | 317 | 24.6% |
| sensitive attribute | 18 | 147 | 12.2% |
| indirect identifier | 7 | 107 | 6.5% |

## EU personal data

| Kind of information | Caught | Of | Rate |
|---|---|---|---|
| email | 152 | 152 | 100.0% |
| routing number | 45 | 45 | 100.0% |
| ip address | 33 | 33 | 100.0% |
| iban | 20 | 20 | 100.0% |
| payment card | 69 | 70 | 98.6% |
| postal code | 132 | 136 | 97.1% |
| url | 30 | 31 | 96.8% |
| person name | 1512 | 1571 | 96.2% |
| tax id | 80 | 84 | 95.2% |
| ssn | 59 | 62 | 95.2% |
| device id | 52 | 55 | 94.5% |
| bank account | 108 | 119 | 90.8% |
| record number | 339 | 384 | 88.3% |
| place | 462 | 527 | 87.7% |
| street address | 131 | 150 | 87.3% |
| government id | 82 | 99 | 82.8% |
| credential | 34 | 72 | 47.2% |
| health info | 80 | 317 | 25.2% |
| sensitive attribute | 18 | 147 | 12.2% |
| indirect identifier | 7 | 107 | 6.5% |

## California sensitive personal information

Health and other sensitive attributes are in the rule but have no detector.

| Kind of information | Caught | Of | Rate |
|---|---|---|---|
| iban | 20 | 20 | 100.0% |
| payment card | 68 | 70 | 97.1% |
| ssn | 59 | 62 | 95.2% |
| bank account | 106 | 119 | 89.1% |
| government id | 75 | 99 | 75.8% |
| card security code | 10 | 16 | 62.5% |
| credential | 31 | 72 | 43.1% |
| health info | 79 | 317 | 24.9% |
| sensitive attribute | 17 | 147 | 11.6% |

