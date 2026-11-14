// Written by tools/evaluation/class_accuracy.py. Do not edit by hand.
// Source: evaluation run `c2-round4` on the second test set (60 documents whose misses are never inspected).
// caught = every letter and digit of the value was replaced; of = values in the answer keys.
// `flagged` counts sensitive facts with any part underlined for review.
export const MEASURED_RUN = "c2-round4";
export const MEASURED = {
  "age_over_89": {
    "caught": 6,
    "of": 11,
    "partly": 1
  },
  "bank_account": {
    "caught": 95,
    "of": 98,
    "partly": 0
  },
  "card_expiry": {
    "caught": 15,
    "of": 15,
    "partly": 0
  },
  "card_security_code": {
    "caught": 6,
    "of": 6,
    "partly": 0
  },
  "credential": {
    "caught": 54,
    "of": 77,
    "partly": 1
  },
  "date": {
    "caught": 632,
    "of": 651,
    "partly": 5
  },
  "date_of_birth": {
    "caught": 74,
    "of": 74,
    "partly": 0
  },
  "device_id": {
    "caught": 61,
    "of": 69,
    "partly": 2
  },
  "email": {
    "caught": 133,
    "of": 133,
    "partly": 0
  },
  "flagged": {
    "caught": 302,
    "of": 354,
    "partly": 0
  },
  "government_id": {
    "caught": 92,
    "of": 94,
    "partly": 0
  },
  "health_info": {
    "caught": 91,
    "of": 217,
    "partly": 96
  },
  "iban": {
    "caught": 12,
    "of": 12,
    "partly": 0
  },
  "indirect_identifier": {
    "caught": 5,
    "of": 48,
    "partly": 33
  },
  "ip_address": {
    "caught": 25,
    "of": 25,
    "partly": 0
  },
  "money_amount": {
    "caught": 678,
    "of": 689,
    "partly": 9
  },
  "organization_name": {
    "caught": 438,
    "of": 453,
    "partly": 10
  },
  "payment_card": {
    "caught": 46,
    "of": 52,
    "partly": 0
  },
  "person_name": {
    "caught": 1070,
    "of": 1095,
    "partly": 11
  },
  "phone": {
    "caught": 216,
    "of": 218,
    "partly": 2
  },
  "place": {
    "caught": 442,
    "of": 475,
    "partly": 2
  },
  "postal_code": {
    "caught": 122,
    "of": 123,
    "partly": 0
  },
  "record_number": {
    "caught": 386,
    "of": 404,
    "partly": 9
  },
  "routing_number": {
    "caught": 47,
    "of": 47,
    "partly": 0
  },
  "sensitive_attribute": {
    "caught": 13,
    "of": 89,
    "partly": 64
  },
  "ssn": {
    "caught": 46,
    "of": 48,
    "partly": 0
  },
  "street_address": {
    "caught": 121,
    "of": 138,
    "partly": 12
  },
  "tax_id": {
    "caught": 57,
    "of": 58,
    "partly": 1
  },
  "url": {
    "caught": 26,
    "of": 26,
    "partly": 0
  },
  "vehicle_id": {
    "caught": 47,
    "of": 57,
    "partly": 1
  }
};
