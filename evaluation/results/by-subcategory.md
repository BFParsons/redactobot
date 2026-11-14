# Hit rate by sub-category (run `c1-round4`, 100 documents)

"Caught" means every character of the value was covered. For the flag-only categories, "Flagged" counts a
value when any part of it was underlined for review. Sub-categories with fewer than 10 occurrences are too small
to read much into.

## Person names: 100% of 1571

| Sub-category | Caught | Of | Rate |
|---|---|---|---|
| Full name | 475 | 475 | 100% |
| First name only | 299 | 299 | 100% |
| Title and surname (Ms. Whitfield) | 199 | 199 | 100% |
| Nickname | 139 | 139 | 100% |
| Surname only | 108 | 108 | 100% |
| Name that is also a word or place (Grace, Jordan) | 98 | 98 | 100% |
| Initials (DKL, R. Tanaka) | 83 | 83 | 100% |
| "Last, First" order | 75 | 75 | 100% |
| Short name | 73 | 73 | 100% |
| ALL CAPS | 22 | 22 | 100% |

## Money amounts: 100% of 899

| Sub-category | Caught | Of | Rate |
|---|---|---|---|
| Standard ($1,250.00) | 659 | 659 | 100% |
| No currency sign (ledger figures) | 113 | 113 | 100% |
| Abbreviated (75k, $1.9 million) | 40 | 40 | 100% |
| Written in words | 25 | 25 | 100% |
| Other currencies and currency codes | 21 | 21 | 100% |
| Negative in parentheses | 16 | 16 | 100% |
| Rates ($19.75/hr) | 11 | 11 | 100% |
| European number format (€ 18.020,00) | 10 | 10 | 100% |
| Space instead of a decimal point | 4 | 4 | 100% |

## Organization names: 100% of 758

| Sub-category | Caught | Of | Rate |
|---|---|---|---|
| Full name | 500 | 501 | 100% |
| Short name | 181 | 181 | 100% |
| Acronym | 47 | 47 | 100% |
| ALL CAPS | 29 | 29 | 100% |

## Dates: 100% of 708

| Sub-category | Caught | Of | Rate |
|---|---|---|---|
| Full date | 518 | 518 | 100% |
| No year (06/26, 30 June) | 132 | 132 | 100% |
| Two-digit year | 28 | 28 | 100% |
| Month and year only | 16 | 16 | 100% |
| Spaces as separators (08 29 2026) | 8 | 8 | 100% |
| With weekday | 6 | 6 | 100% |

## Places: 100% of 527

| Sub-category | Caught | Of | Rate |
|---|---|---|---|
| City or town | 253 | 253 | 100% |
| State or province name | 124 | 124 | 100% |
| State or province code (TX) | 83 | 83 | 100% |
| Neighbourhood, facility or other | 35 | 35 | 100% |
| County | 32 | 32 | 100% |

## Record numbers: 100% of 384

| Sub-category | Caught | Of | Rate |
|---|---|---|---|
| Claim, policy, loan and medical record numbers | 83 | 83 | 100% |
| Other reference numbers | 77 | 77 | 100% |
| Invoice, check and order numbers | 64 | 64 | 100% |
| Matter, file and client numbers | 57 | 57 | 100% |
| Case, docket and incident numbers | 52 | 52 | 100% |
| Employee and group IDs | 51 | 51 | 100% |

## Health details (flag only): 46% of 317 fully covered, 96% flagged

| Sub-category | Caught | Of | Rate | Flagged |
|---|---|---|---|---|
| Diagnoses and conditions | 61 | 104 | 59% | 102 (98%) |
| Medication | 39 | 58 | 67% | 58 (100%) |
| Tests, procedures and treatment | 21 | 54 | 39% | 49 (91%) |
| Other health details | 11 | 45 | 24% | 40 (89%) |
| Mental health and substance use | 8 | 43 | 19% | 41 (95%) |
| Pregnancy | 7 | 13 | 54% | 13 (100%) |

## Phone numbers: 100% of 243

| Sub-category | Caught | Of | Rate |
|---|---|---|---|
| Standard US formats | 183 | 183 | 100% |
| Fax | 26 | 26 | 100% |
| With extension | 14 | 14 | 100% |
| International and UK | 14 | 14 | 100% |
| Partial or unusual | 4 | 4 | 100% |
| In words | 2 | 2 | 100% |

## Email addresses: 100% of 152

| Sub-category | Caught | Of | Rate |
|---|---|---|---|
| Standard | 149 | 149 | 100% |
| Spelled out in words | 3 | 3 | 100% |

## Street addresses: 100% of 150

| Sub-category | Caught | Of | Rate |
|---|---|---|---|
| Standard street address | 93 | 93 | 100% |
| With suite, floor or unit | 30 | 30 | 100% |
| PO box | 10 | 10 | 100% |
| Rural route | 8 | 8 | 100% |
| Non-US style | 6 | 6 | 100% |
| ALL CAPS | 3 | 3 | 100% |

## Other sensitive attributes (flag only): 28% of 147 fully covered, 98% flagged

| Sub-category | Caught | Of | Rate | Flagged |
|---|---|---|---|---|
| Immigration, citizenship and nationality | 16 | 52 | 31% | 51 (98%) |
| Criminal history | 2 | 19 | 11% | 18 (95%) |
| Religion | 6 | 19 | 32% | 18 (95%) |
| Race and ethnicity | 8 | 16 | 50% | 16 (100%) |
| Bankruptcy and court obligations | 1 | 14 | 7% | 14 (100%) |
| Union membership | 4 | 11 | 36% | 11 (100%) |
| Political views and donations | 0 | 6 | 0% | 6 (100%) |
| Sexual orientation and gender identity | 2 | 5 | 40% | 5 (100%) |
| Genetic information | 2 | 5 | 40% | 5 (100%) |

## Postal codes: 100% of 136

| Sub-category | Caught | Of | Rate |
|---|---|---|---|
| ZIP code | 98 | 98 | 100% |
| Canadian postal code | 16 | 16 | 100% |
| ZIP+4 | 14 | 14 | 100% |
| UK, Irish and Dutch | 6 | 6 | 100% |
| State and ZIP together | 2 | 2 | 100% |

## Bank accounts: 100% of 119

| Sub-category | Caught | Of | Rate |
|---|---|---|---|
| Bank account number | 54 | 54 | 100% |
| Masked or last four | 30 | 30 | 100% |
| Brokerage, plan and trust accounts | 16 | 16 | 100% |
| Institution and transit numbers | 10 | 10 | 100% |
| SWIFT/BIC code | 9 | 9 | 100% |

## Indirect identifiers (not detected): 47% of 107 fully covered, 91% flagged

| Sub-category | Caught | Of | Rate | Flagged |
|---|---|---|---|---|
| Family relationships | 42 | 67 | 63% | 64 (96%) |
| Distinctive assets, events and whereabouts | 5 | 29 | 17% | 22 (76%) |
| Unique roles | 3 | 11 | 27% | 11 (100%) |

## Government IDs: 100% of 99

| Sub-category | Caught | Of | Rate |
|---|---|---|---|
| Medical IDs (NPI, DEA, Medicare) | 26 | 26 | 100% |
| Bar numbers | 22 | 22 | 100% |
| Other licences and IRS IDs | 20 | 20 | 100% |
| Driver's license | 14 | 14 | 100% |
| Passport | 8 | 8 | 100% |
| Immigration numbers | 6 | 6 | 100% |
| UK National Insurance | 3 | 3 | 100% |

## Dates of birth: 100% of 91

| Sub-category | Caught | Of | Rate |
|---|---|---|---|
| Full birth date | 86 | 86 | 100% |
| Indirect or in words | 5 | 5 | 100% |

## Tax IDs: 100% of 84

| Sub-category | Caught | Of | Rate |
|---|---|---|---|
| EIN | 44 | 44 | 100% |
| Canadian SIN | 17 | 17 | 100% |
| VAT and other foreign | 7 | 7 | 100% |
| Canadian business number | 6 | 6 | 100% |
| ITIN | 5 | 5 | 100% |
| State and other IDs | 5 | 5 | 100% |

## Passwords and user names: 100% of 72

| Sub-category | Caught | Of | Rate |
|---|---|---|---|
| User names | 38 | 38 | 100% |
| Passwords | 19 | 19 | 100% |
| PINs, passcodes and codes | 15 | 15 | 100% |

## Payment cards: 100% of 70

| Sub-category | Caught | Of | Rate |
|---|---|---|---|
| Last four or five digits | 51 | 51 | 100% |
| Full card number | 19 | 19 | 100% |

## Social Security numbers: 100% of 62

| Sub-category | Caught | Of | Rate |
|---|---|---|---|
| Standard (123-45-6789) | 23 | 23 | 100% |
| Masked (xxx-xx-1234) | 18 | 18 | 100% |
| No separators | 8 | 8 | 100% |
| With spaces | 7 | 7 | 100% |
| Last four only | 6 | 6 | 100% |

## Vehicle IDs: 100% of 60

| Sub-category | Caught | Of | Rate |
|---|---|---|---|
| License plate | 32 | 32 | 100% |
| VIN | 24 | 24 | 100% |
| Hull and ship numbers | 4 | 4 | 100% |

## Device IDs: 100% of 55

| Sub-category | Caught | Of | Rate |
|---|---|---|---|
| Serial numbers and asset tags | 47 | 47 | 100% |
| IMEI | 4 | 4 | 100% |
| MAC address | 4 | 4 | 100% |

## Routing numbers: 100% of 45

| Sub-category | Caught | Of | Rate |
|---|---|---|---|
| US routing number | 41 | 41 | 100% |
| Canadian transit number | 2 | 2 | 100% |
| UK sort code | 2 | 2 | 100% |

## IP addresses: 100% of 33

| Sub-category | Caught | Of | Rate |
|---|---|---|---|
| IPv4 | 28 | 28 | 100% |
| IPv6 | 5 | 5 | 100% |

## Web addresses: 100% of 31

| Sub-category | Caught | Of | Rate |
|---|---|---|---|
| Web address | 20 | 20 | 100% |
| Link containing an identifier | 11 | 11 | 100% |

## Card expiry dates: 100% of 21

| Sub-category | Caught | Of | Rate |
|---|---|---|---|
| Card expiry | 21 | 21 | 100% |

## Ages over 89: 100% of 20

| Sub-category | Caught | Of | Rate |
|---|---|---|---|
| Bare number | 10 | 10 | 100% |
| With "age" or "years old" | 8 | 8 | 100% |
| Spelled out | 2 | 2 | 100% |

## IBANs: 100% of 20

| Sub-category | Caught | Of | Rate |
|---|---|---|---|
| IBAN | 20 | 20 | 100% |

## Card security codes: 100% of 16

| Sub-category | Caught | Of | Rate |
|---|---|---|---|
| Card security code | 16 | 16 | 100% |

