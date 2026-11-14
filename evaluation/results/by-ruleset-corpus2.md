# Catch rate by rule set

Each rule set was run on its own (only its checks switched on) over the 100 fictional documents, and scored
against the kinds of information that rule covers. Names are replayed from the final live model run.
"Caught" means every character of the value was covered. See RESULTS.md for method and limits.

"Counting flags" also counts a health or other sensitive detail as found when any part of it is underlined for review.

| Rank | Rule set | Caught | Of | Rate | Counting flags | Held-out part |
|---|---|---|---|---|---|---|
| 1 | Customer financial information (16 CFR 314.2) | 2536 | 2711 | 93.5% | 93.5% | 93.9% |
| 2 | Tax return information (26 CFR 301.7216-1) | 3368 | 3639 | 92.6% | 92.6% | 93.2% |
| 3 | Health information (18 identifiers) (45 CFR 164.514(b)(2)) | 3444 | 3768 | 91.4% | 91.9% | 90.2% |
| 4 | Payment card data (PCI DSS v4.0.1) | 216 | 238 | 90.8% | 90.8% | 95.5% |
| 5 | Federal court filings (Fed. R. Civ. P. 5.2(a)) | 402 | 454 | 88.5% | 88.5% | 86.1% |
| 6 | US federal PII guidance (NIST SP 800-122) | 2871 | 3443 | 83.4% | 87.6% | 81.7% |
| 7 | EU personal data (GDPR Art. 4, 9, 10) | 2731 | 3328 | 82.1% | 86.4% | 79.2% |
| 8 | California sensitive personal information (Cal. Civ. Code 1798.140(ae)) | 322 | 693 | 46.5% | 63.2% | 41.1% |

## Customer financial information

Consumer report details have no detector and no answer-key category.

| Kind of information | Caught | Of | Rate |
|---|---|---|---|
| email | 133 | 133 | 100.0% |
| iban | 12 | 12 | 100.0% |
| phone | 213 | 218 | 97.7% |
| routing number | 45 | 47 | 95.7% |
| person name | 1038 | 1095 | 94.8% |
| money amount | 653 | 689 | 94.8% |
| postal code | 113 | 123 | 91.9% |
| tax id | 50 | 58 | 86.2% |
| ssn | 41 | 48 | 85.4% |
| street address | 116 | 138 | 84.1% |
| bank account | 81 | 98 | 82.7% |
| payment card | 41 | 52 | 78.8% |

## Tax return information

| Kind of information | Caught | Of | Rate |
|---|---|---|---|
| email | 133 | 133 | 100.0% |
| iban | 12 | 12 | 100.0% |
| phone | 213 | 218 | 97.7% |
| routing number | 45 | 47 | 95.7% |
| organization name | 430 | 453 | 94.9% |
| person name | 1038 | 1095 | 94.8% |
| money amount | 653 | 689 | 94.8% |
| postal code | 113 | 123 | 91.9% |
| tax id | 50 | 58 | 86.2% |
| ssn | 41 | 48 | 85.4% |
| place | 402 | 475 | 84.6% |
| street address | 116 | 138 | 84.1% |
| bank account | 81 | 98 | 82.7% |
| payment card | 41 | 52 | 78.8% |

## Health information (18 identifiers)

Biometrics and photographs do not apply to text. A state or province on its own is not scored: this rule lets it stay.

| Kind of information | Caught | Of | Rate |
|---|---|---|---|
| email | 133 | 133 | 100.0% |
| ip address | 25 | 25 | 100.0% |
| iban | 12 | 12 | 100.0% |
| date of birth | 73 | 74 | 98.6% |
| phone | 213 | 218 | 97.7% |
| routing number | 45 | 47 | 95.7% |
| person name | 1038 | 1095 | 94.8% |
| record number | 377 | 404 | 93.3% |
| tax id | 54 | 58 | 93.1% |
| postal code | 113 | 123 | 91.9% |
| date | 594 | 651 | 91.2% |
| place | 261 | 287 | 90.9% |
| government id | 85 | 94 | 90.4% |
| device id | 62 | 69 | 89.9% |
| bank account | 87 | 98 | 88.8% |
| url | 23 | 26 | 88.5% |
| ssn | 41 | 48 | 85.4% |
| payment card | 43 | 52 | 82.7% |
| street address | 112 | 138 | 81.2% |
| vehicle id | 46 | 57 | 80.7% |
| age over 89 | 6 | 11 | 54.5% |
| indirect identifier | 1 | 48 | 2.1% |

## Payment card data

Cardholder names are covered by the standard, but the answer keys do not say which names are cardholders.

| Kind of information | Caught | Of | Rate |
|---|---|---|---|
| cardholder name | 157 | 165 | 95.2% |
| card expiry | 13 | 15 | 86.7% |
| card security code | 5 | 6 | 83.3% |
| payment card | 41 | 52 | 78.8% |

## Federal court filings

Names of minors are also covered by the rule, but the answer keys do not say who is a minor, so names are not scored here.

| Kind of information | Caught | Of | Rate |
|---|---|---|---|
| iban | 12 | 12 | 100.0% |
| minor name | 111 | 112 | 99.1% |
| date of birth | 66 | 74 | 89.2% |
| tax id | 50 | 58 | 86.2% |
| ssn | 41 | 48 | 85.4% |
| bank account | 81 | 98 | 82.7% |
| payment card | 41 | 52 | 78.8% |

## US federal PII guidance

| Kind of information | Caught | Of | Rate |
|---|---|---|---|
| email | 133 | 133 | 100.0% |
| iban | 12 | 12 | 100.0% |
| person name | 1038 | 1095 | 94.8% |
| money amount | 653 | 689 | 94.8% |
| postal code | 113 | 123 | 91.9% |
| tax id | 53 | 58 | 91.4% |
| date of birth | 67 | 74 | 90.5% |
| ssn | 41 | 48 | 85.4% |
| place | 405 | 475 | 85.3% |
| street address | 115 | 138 | 83.3% |
| bank account | 81 | 98 | 82.7% |
| payment card | 42 | 52 | 80.8% |
| government id | 61 | 94 | 64.9% |
| health info | 49 | 217 | 22.6% |
| sensitive attribute | 7 | 89 | 7.9% |
| indirect identifier | 1 | 48 | 2.1% |

## EU personal data

| Kind of information | Caught | Of | Rate |
|---|---|---|---|
| email | 133 | 133 | 100.0% |
| ip address | 25 | 25 | 100.0% |
| iban | 12 | 12 | 100.0% |
| tax id | 57 | 58 | 98.3% |
| routing number | 45 | 47 | 95.7% |
| person name | 1038 | 1095 | 94.8% |
| postal code | 113 | 123 | 91.9% |
| record number | 371 | 404 | 91.8% |
| bank account | 87 | 98 | 88.8% |
| url | 23 | 26 | 88.5% |
| device id | 61 | 69 | 88.4% |
| ssn | 41 | 48 | 85.4% |
| place | 404 | 475 | 85.1% |
| street address | 115 | 138 | 83.3% |
| payment card | 43 | 52 | 82.7% |
| government id | 77 | 94 | 81.9% |
| credential | 26 | 77 | 33.8% |
| health info | 52 | 217 | 24.0% |
| sensitive attribute | 7 | 89 | 7.9% |
| indirect identifier | 1 | 48 | 2.1% |

## California sensitive personal information

Health and other sensitive attributes are in the rule but have no detector.

| Kind of information | Caught | Of | Rate |
|---|---|---|---|
| iban | 12 | 12 | 100.0% |
| ssn | 41 | 48 | 85.4% |
| card security code | 5 | 6 | 83.3% |
| bank account | 81 | 98 | 82.7% |
| payment card | 42 | 52 | 80.8% |
| government id | 62 | 94 | 66.0% |
| credential | 24 | 77 | 31.2% |
| health info | 49 | 217 | 22.6% |
| sensitive attribute | 6 | 89 | 6.7% |

