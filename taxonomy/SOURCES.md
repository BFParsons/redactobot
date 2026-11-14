# Taxonomy sources and how they were verified

Checked 2026-11-11. "Primary" means the wording in `taxonomy.js` was compared against the
text of the rule itself. "Secondary" means the official page could not be loaded and the
wording was confirmed from other publications that quote it. Re-check secondary items
against the official text before quoting them in the app or the submission.

This is a product taxonomy, not legal advice. The app never claims a document meets any
of these rules; it shows what each rule lists and what was and was not caught.

| Rule | Citation | Used for | Verified | Checked against |
|---|---|---|---|---|
| HIPAA Safe Harbor | 45 CFR § 164.514(b)(2)(i)(A)–(R) | The 18 identifiers | Primary | Cornell LII copy of the CFR. hhs.gov and ecfr.gov refused automated access. |
| Federal court filing privacy | Fed. R. Civ. P. 5.2(a) | What must be cut down in filings, and what may remain | Primary | Cornell LII |
| Tax return information | 26 CFR § 301.7216-1(b)(3) | Definition of tax return information | Primary | Cornell LII |
| GLBA Safeguards Rule | 16 CFR § 314.2(l), (o), (h)(2)(viii) | Customer financial information; tax preparers are covered | Primary | Cornell LII |
| CCPA | Cal. Civ. Code § 1798.140(ae) | Sensitive personal information | Primary | California Privacy Protection Agency statute PDF, effective 2025-01-01 |
| NIST SP 800-122 | § 2.1, § 2.2, glossary | PII definition; linked and linkable information | Primary | NIST PDF (April 2010) |
| GDPR | Art. 4(1), 9(1), 10 | Personal data; special categories; criminal convictions | Primary | gdpr-info.eu, an unofficial copy of the regulation text |
| PCI DSS v4.0.1 | Account data definitions | Cardholder data; sensitive authentication data | Primary (partial) | PCI SSC self-assessment questionnaires, which reproduce the definitions. The main standard sits behind a click-through. |
| ABA Model Rule 1.6 | 1.6(a), (c) | Why lawyers review everything | Secondary | americanbar.org refused automated access. Wording confirmed from court and law-school publications quoting the rule. States adopt their own versions. |
| AICPA Code of Professional Conduct | ET § 1.700.001 | Why accountants review everything | Secondary | Journal of Accountancy and The Tax Adviser articles describing the rule. The exact current wording was not retrieved. |

## Number checks

| Check | Method | Verified |
|---|---|---|
| Payment card | Luhn checksum, 13–19 digits | Standard; tested with the public test number 4111 1111 1111 1111 |
| Canadian SIN | Luhn checksum, 9 digits, first digit not 0 or 8 | Secondary: python-stdnum and Django localflavor. No Service Canada page was found. |
| IBAN | Mod-97 check | Standard; tested with the public example GB82 WEST 1234 5698 7654 32 |
| US bank routing number | 3-7-1 weighted checksum | From memory, not re-checked against a source; tested with one known-valid number |
| US Social Security number | Format, plus never-issued ranges (area 000, 666, 900–999; group 00; serial 0000) | From memory, not re-checked against an SSA page |

## Corrections found during verification

- California's list also includes **neural data** and **citizenship or immigration status**,
  and covers account and card numbers only **in combination with** an access code or password.
- HIPAA's ZIP rule lets the first three digits stay only where that area has more than
  20,000 people. The app does not check population, so it should not keep them by default.
- A Canadian SIN starting with 0 is never issued, so the widely quoted example
  046 454 286 is rejected by the validator.

## Not used

Canadian sources (PIPEDA, the federal Privacy Commissioner's bulletin on sensitive
information, provincial law society and CPA rules) were checked earlier but left out,
because the contest is US-based. Canadian ID formats (SIN, business number, postal code)
stay as patterns because the sample document uses them.
