# Copyright 2026 The Redactobot Authors
# SPDX-License-Identifier: Apache-2.0

"""How the answer keys' free-text subtype labels are grouped into sub-categories."""

import re

# category -> ordered list of (pattern on the subtype text, sub-category). First match wins.
RULES = {
    "money_amount": [
        (r"word|spelled|spoken", "Written in words"),
        (r"space instead", "Space instead of a decimal point"),
        (r"european|french", "European number format (€ 18.020,00)"),
        (
            r"shorthand|abbreviat|\bk\b|\bmm\b|million|word scale|rounded",
            "Abbreviated (75k, $1.9 million)",
        ),
        (r"parenthes|negative", "Negative in parentheses"),
        (
            r"currency code|euro amount|canadian dollar|pounds",
            "Other currencies and currency codes",
        ),
        (
            r"no currency|without currency|bare number",
            "No currency sign (ledger figures)",
        ),
        (r"hourly|monthly|rate|rent|wage", "Rates ($19.75/hr)"),
        (r"", "Standard ($1,250.00)"),
    ],
    "date": [
        (
            r"without year|no year|month and day|month/day|birthday without",
            "No year (06/26, 30 June)",
        ),
        (r"month and year", "Month and year only"),
        (r"two-digit year", "Two-digit year"),
        (r"spaces as separators", "Spaces as separators (08 29 2026)"),
        (r"weekday", "With weekday"),
        (r"", "Full date"),
    ],
    "date_of_birth": [
        (r"without year|indirect|words|written-out", "Indirect or in words"),
        (r"", "Full birth date"),
    ],
    "age_over_89": [
        (r"spelled", "Spelled out"),
        (r"bare|abbreviat", "Bare number"),
        (r"", 'With "age" or "years old"'),
    ],
    "phone": [
        (r"extension", "With extension"),
        (r"uk|irish|dutch|international", "International and UK"),
        (r"words|spoken|spelled", "In words"),
        (r"last four|seven digits|no dash|mixed", "Partial or unusual"),
        (r"fax", "Fax"),
        (r"", "Standard US formats"),
    ],
    "email": [
        (r"words|spelled|written out", "Spelled out in words"),
        (r"", "Standard"),
    ],
    "street_address": [
        (r"all caps", "ALL CAPS"),
        (r"po box", "PO box"),
        (r"rural", "Rural route"),
        (r"dutch|abroad|bilingual|canadian", "Non-US style"),
        (
            r"suite|floor|unit|apartment|building|apt|room",
            "With suite, floor or unit",
        ),
        (r"", "Standard street address"),
    ],
    "postal_code": [
        (r"zip\+4", "ZIP+4"),
        (r"canadian", "Canadian postal code"),
        (r"uk|irish|dutch", "UK, Irish and Dutch"),
        (r"written together", "State and ZIP together"),
        (r"", "ZIP code"),
    ],
    "place": [
        (
            r"state abbreviation|province abbreviation",
            "State or province code (TX)",
        ),
        (r"state|province", "State or province name"),
        (r"county", "County"),
        (r"city|town|village", "City or town"),
        (r"", "Neighbourhood, facility or other"),
    ],
    "ssn": [
        (r"masked", "Masked (xxx-xx-1234)"),
        (r"last four", "Last four only"),
        (r"without", "No separators"),
        (r"spaces", "With spaces"),
        (r"", "Standard (123-45-6789)"),
    ],
    "tax_id": [
        (r"\bein\b", "EIN"),
        (r"\bsin\b", "Canadian SIN"),
        (r"business number", "Canadian business number"),
        (r"itin", "ITIN"),
        (r"vat|chamber", "VAT and other foreign"),
        (r"", "State and other IDs"),
    ],
    "government_id": [
        (r"bar|attorney|law society", "Bar numbers"),
        (
            r"npi|dea|medical|medicare|health card",
            "Medical IDs (NPI, DEA, Medicare)",
        ),
        (r"passport", "Passport"),
        (r"driver|driving", "Driver's license"),
        (r"alien|uscis", "Immigration numbers"),
        (r"national insurance", "UK National Insurance"),
        (r"", "Other licences and IRS IDs"),
    ],
    "bank_account": [
        (r"last four|masked", "Masked or last four"),
        (r"swift|bic", "SWIFT/BIC code"),
        (
            r"brokerage|plan|trust|certificate|member",
            "Brokerage, plan and trust accounts",
        ),
        (r"institution|transit", "Institution and transit numbers"),
        (r"", "Bank account number"),
    ],
    "routing_number": [
        (r"uk", "UK sort code"),
        (r"canadian", "Canadian transit number"),
        (r"", "US routing number"),
    ],
    "iban": [(r"", "IBAN")],
    "payment_card": [
        (r"last f", "Last four or five digits"),
        (r"", "Full card number"),
    ],
    "card_expiry": [(r"", "Card expiry")],
    "card_security_code": [(r"", "Card security code")],
    "record_number": [
        (
            r"invoice|receipt|purchase order|check|confirmation|contract|engagement|order",
            "Invoice, check and order numbers",
        ),
        (
            r"case|docket|cause|charge|incident|police|eeoc|probate|citation|court",
            "Case, docket and incident numbers",
        ),
        (r"employee|payroll|group|badge", "Employee and group IDs"),
        (
            r"claim|policy|member|medical record|prescription|loan|mrn",
            "Claim, policy, loan and medical record numbers",
        ),
        (r"matter|file|client", "Matter, file and client numbers"),
        (r"", "Other reference numbers"),
    ],
    "url": [
        (r"containing|token|specific", "Link containing an identifier"),
        (r"", "Web address"),
    ],
    "ip_address": [(r"ipv6", "IPv6"), (r"", "IPv4")],
    "vehicle_id": [
        (r"vin", "VIN"),
        (r"plate", "License plate"),
        (r"", "Hull and ship numbers"),
    ],
    "device_id": [
        (r"mac", "MAC address"),
        (r"imei", "IMEI"),
        (r"", "Serial numbers and asset tags"),
    ],
    "credential": [
        (r"username|network name", "User names"),
        (r"password|passphrase", "Passwords"),
        (r"", "PINs, passcodes and codes"),
    ],
    "health_info": [
        (
            r"mental|substance|addiction|recovery|alcohol|drug test",
            "Mental health and substance use",
        ),
        (r"medication", "Medication"),
        (r"pregnan", "Pregnancy"),
        (
            r"lab|test|result|procedure|treatment|surg|device|care",
            "Tests, procedures and treatment",
        ),
        (
            r"diagnos|condition|allergy|injury|symptom|complaint|finding|history|health detail",
            "Diagnoses and conditions",
        ),
        (r"", "Other health details"),
    ],
    "sensitive_attribute": [
        (
            r"immigration|citizenship|nationality|national origin|residency|detention",
            "Immigration, citizenship and nationality",
        ),
        (r"criminal|juvenile|arrest", "Criminal history"),
        (r"relig", "Religion"),
        (r"union", "Union membership"),
        (r"politic", "Political views and donations"),
        (r"ethnic|language|tribal|race", "Race and ethnicity"),
        (r"sexual|gender", "Sexual orientation and gender identity"),
        (r"genetic|gene", "Genetic information"),
        (r"", "Bankruptcy and court obligations"),
    ],
    "indirect_identifier": [
        (
            r"relationship|family|spouse|household|marital",
            "Family relationships",
        ),
        (r"role|occupation", "Unique roles"),
        (r"", "Distinctive assets, events and whereabouts"),
    ],
}
NAME_VARIANT = {
    "full": "Full name",
    "first-name": "First name only",
    "surname": "Surname only",
    "title-surname": "Title and surname (Ms. Whitfield)",
    "initials": "Initials (DKL, R. Tanaka)",
    "nickname": "Nickname",
    "last-first": '"Last, First" order',
    "caps": "ALL CAPS",
    "short": "Short name",
    "acronym": "Acronym",
}
LABEL = {
    "person_name": "Person names",
    "organization_name": "Organization names",
    "money_amount": "Money amounts",
    "date": "Dates",
    "date_of_birth": "Dates of birth",
    "age_over_89": "Ages over 89",
    "phone": "Phone numbers",
    "email": "Email addresses",
    "street_address": "Street addresses",
    "postal_code": "Postal codes",
    "place": "Places",
    "ssn": "Social Security numbers",
    "tax_id": "Tax IDs",
    "government_id": "Government IDs",
    "bank_account": "Bank accounts",
    "routing_number": "Routing numbers",
    "iban": "IBANs",
    "payment_card": "Payment cards",
    "card_expiry": "Card expiry dates",
    "card_security_code": "Card security codes",
    "record_number": "Record numbers",
    "url": "Web addresses",
    "ip_address": "IP addresses",
    "vehicle_id": "Vehicle IDs",
    "device_id": "Device IDs",
    "credential": "Passwords and user names",
    "health_info": "Health details (flag only)",
    "sensitive_attribute": "Other sensitive attributes (flag only)",
    "indirect_identifier": "Indirect identifiers (not detected)",
}


def sub(it):
    cat, text = it["category"], (it.get("subtype") or "").lower()
    if cat in ("person_name", "organization_name"):
        if cat == "person_name" and re.search(
            r"also a|common word|is a common word", text
        ):
            return "Name that is also a word or place (Grace, Jordan)"
        return NAME_VARIANT.get(it.get("variant"), "Other forms")
    for pattern, name in RULES.get(cat, [("", "All")]):
        if re.search(pattern, text):
            return name
    return "Other"
