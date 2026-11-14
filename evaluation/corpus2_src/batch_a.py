from corpus2_src.core import D, dt, amt, num

DOCS = []
BATCH_COMMON = [
    "review", "draft", "prepare", "invoice", "rates", "costs", "service", "filing", "trust",
    "applied", "less", "prefer", "questions", "enclosed", "based", "very", "direct", "items", "sex",
    "collected", "received", "reported", "fasting", "clinical", "comment", "called", "billing",
    "electronically", "end", "prepared", "landlord", "tenant", "guarantors", "guarantor", "lease",
    "premises", "commencement", "rent", "expiration", "percentage", "late", "use", "four", "loading",
    "notices", "member", "group", "prescriber", "drug", "requested", "dispensing", "denial",
    "attestation", "reviewer", "decision", "approved", "denied", "mother", "father", "child",
    "children", "parties", "exchanges", "holidays", "school",
    "neither", "both", "either", "each", "when", "during", "unless", "until", "absent", "nothing",
    "communication", "travel", "expenses", "medical", "education", "religion", "relocation",
    "disputes", "signatures", "addr", "spouse", "kids", "claim", "health", "fee", "do", "works",
    "consult", "atty", "referred", "add", "ask", "bring", "also", "sorry", "okay",
    "emp", "preferred", "street", "salary", "emergency", "relationship", "routing", "split",
    "serial", "asset", "tag", "issued", "value", "username", "temp", "password", "badge", "door",
    "issuer", "expires", "verified", "make", "model", "bank", "voided", "personal", "cell",
    "laptop", "monitor", "phone", "headset", "remainder", "savings", "checking", "balance",
    "ordering", "provider", "analyzer", "copy", "patient", "test", "flag", "lab", "director",
    "result", "units", "age", "accession", "summary", "state", "portal", "estimated", "capital",
    "partner", "tel", "fed", "fees", "cardholder", "authorized", "amount", "client", "charge",
    "card", "signed", "name", "diagnosis", "contact", "urgent", "plan", "policy", "step", "request",
    "start", "notes", "list", "doc", "equipment", "accounts", "work", "new", "hires", "prayer",
    "legal", "custody", "decision-making", "regular", "week", "weekend", "transportation",
    "thanksgiving", "passover", "christmas", "halloween", "hanukkah", "easter", "day",
    "labor", "memorial", "break", "birthdays", "passports", "insurance", "activities", "taxes",
    "college", "electronics", "safety", "third", "right", "refusal", "mediation", "miscellaneous",
    "definitions", "background", "draft", "v", "re", "district", "petitioner", "respondent",
    "co-petitioner", "proposed", "parenting", "allocation", "parental", "responsibilities",
    "exhibit", "counsel", "mom", "dad", "grandparents", "comments", "term", "use", "base",
    "security", "parking", "abstractor's", "tax", "two", "percentage", "fast-casual",
]
# reminder: nothing in BATCH_COMMON is a month, a personal name, a bank or a place.

# ---------------------------------------------------------------- 201
DOCS.append(D(201, "pdf", "retainer invoice", "legal", "US",
  title="Law firm invoice and client trust (IOLTA) statement with card on file",
  ents={"p1": "Marisela Quiroga-Bentz", "p2": "Oluwaseun Adeleke", "p3": "Kirsten Maddox",
        "p4": "Wade Tannehill", "p5": "Dietrich A. Bentz", "p6": "Renata Szymborska", "p7": "Gil Farkas",
        "o1": "Halloran Vukovic & Tsang LLP", "o2": "Tannehill Roofing Supply, Inc.",
        "o3": "Yolo Delta Community Bank", "o4": "Tule Fog Reporting Services",
        "o5": "Szymborska & Pell", "o6": "Folsom Lake Glass & Mirror", "o7": "Capitol Corridor Attorney Service"},
  cardholders=["p5"],
  distractors=["CCP § 998", "IOLTA", "Visa", "Rule 1.15", "Superior Court", "§ 4"],
  ok=["1.4", "2.1", "3.6", "0.5", "0.8", "1.2", "Site", "Bill", "MSC", "ABA", "NOT", "BALANCE", "DUE", "INVOICE",
      "STATEMENT", "TRUST", "ID", "Attorneys", "Law", "Professional", "February", "Evergreen", "Tel", "Total",
      "Unless", "Rates", "Applied", "Ending", "Replenishment", "Email", "Also", "Authorized", "Fees", "Service",
      "Less", "Costs", "Cardholder", "Questions"],
  body=r'''
# [[HALLORAN VUKOVIC & TSANG LLP|o1:caps]]
Attorneys at Law · [[980 Ninth Street, Suite 1450|addr:street with suite]], [[Sacramento|place:city]], [[CA|place:state abbreviation]] [[95814|zip]]
Tel [[916-555-0117|phone]] · Fed. Tax ID [[68-0417729|taxid:EIN]]
## INVOICE / TRUST STATEMENT
Invoice no. [[HVT-26-03318|rec:invoice number]]. Invoice date: [[April 3, 2026|date:invoice date]]. Billing period: [[03/01/26|date:two-digit year]] to [[03/31/26|date:two-digit year]].
Bill to: [[Marisela Quiroga-Bentz|p1:full]], [[4417 Larkmoor Way|addr]], [[Elk Grove|place!:city name made of common words]], CA [[95758-2204|zip:ZIP+4]]
Client no. [[20417|rec!:client number, bare digits]]. Matter no. [[20417.003|rec:matter number]]. Re: [[Quiroga-Bentz|p1:surname]] v. [[Tannehill Roofing Supply, Inc.|o2:full]], [[Sacramento County|place:county]] Superior Court No. [[34-2025-00381176|rec:court case number]]
## Professional services
[[03/02/26|date:two-digit year]] [[OA|p2:initials]] 1.4 hrs. Review [[Tannehill|o2:short]] production ([[TRS000412|rec:Bates number]] to [[TRS000987|rec:Bates number]]); call w/ client re missing change orders. [[$574.00|money]]
[[03/05/26|date:two-digit year]] [[KM|p3:initials]] 2.1 hrs. Draft subpoena to [[Yolo Delta Community Bank|o3:full]] for records of acct ending [[-7731|acct:last four with leading dash]]; calendar depo of [[Wade Tannehill|p4:full]]. [[$399.00|money]]
[[03/11/26|date:two-digit year]] OA 3.6 hrs. Prepare for and take deposition of [[W. Tannehill|p4:short:initial + surname]] (half day), incl. travel to [[Rancho Cordova|place:city]]. [[$1,476.00|money]]
[[03/12/26|date:two-digit year]] KM 0.5 hrs. Email to [[Ms. Quiroga-Bentz|p1:title-surname]] w/ depo summary; she reports [[Dietrich|p5:first-name]] is recovering from [[rotator cuff surgery|health:surgical procedure]] and cannot attend the [[4/14|date:month/day only]] MSC. [[$95.00|money]]
[[03/19/26|date:two-digit year]] OA 0.8 hrs. Tel. conf. w/ opposing counsel [[Renata Szymborska|p6:full]] ([[Szymborska & Pell|o5:full]]) re CCP § 998 offer of [[$41,500|money]]. [[$328.00|money]]
[[03/27/26|date:two-digit year]] OA 1.2 hrs. Draft mediation brief; review roof inspection report by [[G. Farkas|p7:short:initial + surname]]. [[$492.00|money]]
Rates: [[Oluwaseun Adeleke|p2:full]] (partner) [[$410/hr|money:hourly rate]]; [[Kirsten Maddox|p3:full]] (paralegal) [[$190/hr|money:hourly rate]]. Total fees: [[$3,364.00|money]]
## Costs advanced
03/11/26 [[Tule Fog Reporting Services|o4:full]], Tannehill transcript, inv. [[TF-88213|rec:vendor invoice number]]: [[$712.35|money]]
[[03/06/26|date:two-digit year]] Service of bank subpoena, [[Capitol Corridor Attorney Service|o7:full]]: [[$85.00|money]]
[[03/20/26|date:two-digit year]] Filing fee, stipulation and order: [[$60.00|money]]
[[03/24/26|date:two-digit year]] Site inspection fee, [[Gil Farkas|p7:full]] (roofing consultant), paid by firm check [[#10418|rec:check number]]: [[$600.00|money]]
Total costs: [[$1,457.35|money]]
## Client trust account activity
Trust funds are held per Rule 1.15 in our pooled IOLTA account at Yolo Delta Community Bank, ABA [[121863605|rtn]], acct [[004-417-20933|acct:account number with dashes]]; client ledger [[20417-T|rec:trust ledger number]].
[[02/28/26|date:two-digit year]] Balance forward: [[$2,150.00|money]]
[[03/09/26|date:two-digit year]] Replenishment, Visa ending [[3448|card:last four only]] ([[D. Bentz|p5:short:initial + surname]]), auth code [[09417B|rec!:card authorization code]]: [[$2,500.00|money]]
03/31/26 Applied to invoice [[HVT-26-02901|rec:invoice number]] (February): [[($1,988.40)|money:parenthesized negative]]
03/31/26 Ending trust balance: [[$2,661.60|money]]
## Amount due
Fees and costs this invoice: [[$4,821.35|money]]. Less trust applied: $2,661.60. BALANCE DUE [[$2,159.75|money]] by [[April 24, 2026|date:due date]].
Evergreen retainer: per § 4 of the fee agreement the trust balance must then be restored to [[$2,500|money]]. Unless we hear otherwise by [[4/10/26|date:numeric date with two-digit year]] we will charge the card on file.
Cardholder: [[DIETRICH A BENTZ|p5:caps:name as embossed on card]]. Visa [[4168 9645 2135 3448|card:card number with spaces]], exp [[08/28|exp]], billing ZIP [[95758|zip]]. Authorized amount: [[$4,659.75|money]] (balance plus retainer).
Prefer to wire? Yolo Delta Community Bank, routing 121863605, operating acct [[0044170388|acct!:account number with leading zeros]], NOT the trust account. Or pay online at [[https://pay.hvtlaw.example/inv/HVT-26-03318|url:payment link containing invoice number]].
Questions: [[kmaddox@hvtlaw.example|email]] or [[(916) 555-0117 ext. 204|phone:with extension]].
Note from [[Seun|p2:nickname]]: [[Marisela|p1:first-name]], the [[$41.5k|money!:abbreviated amount]] offer expires [[April 18|date:month and day only]]. Please call my cell, [[916.555.0162|phone:dotted]], before then. Also, [[Dieter|p5:nickname]] asked that statements stop going to his work address at [[Folsom Lake Glass & Mirror|o6:full]]; done.
'''))

# ---------------------------------------------------------------- 202
DOCS.append(D(202, "pdf", "K-1 cover letter", "accounting", "US",
  title="Schedule K-1 transmittal letter to a limited partner (grantor trust)",
  ents={"p1": "Leilani Kapule-Stroud", "p2": "Noriko Oyama", "p3": "Dev Rangarajan", "p4": "Burkhard Stoll",
        "p5": "Gordon Stroud",
        "o1": "Brennecke & Oyama, CPAs", "o2": "Wapato Flats Hop Growers, LP", "o3": "Hop Hollow Management LLC",
        "o4": "Kapule-Stroud Living Trust", "o5": "Mount Defiance Credit Union"},
  distractors=["Schedule K-1 (Form 1065)", "Schedule K-1", "Form 1040-ES", "Section 199A", "§ 754",
               "Social Security number", "Box 19A", "Box 20Z", "Statement A", "Statement B"],
  ok=["2025", "2026", "4.25%", "0.75%", "1", "5", "14", "2", "3", "VIA", "SECURE", "PORTAL", "CLASS", "MAIL", "ACH",
      "K-1", "PTE", "E", "BIN", "ID", "PO", "PTIN", "Trustee", "Trust's", "Partnership", "Box", "Enclosed", "Summary",
      "State", "Capital", "Portal", "Items", "Estimated", "Based", "Very", "Direct", "Sign", "Wire", "Your", "Our"],
  body=r'''
[[Brennecke & Oyama, CPAs|o1:full]]
[[2140 NE Halsey Street, Suite 300|addr:street with suite]] · [[Portland|place:city]], [[Oregon|place:state]] [[97232|zip]]
[[March 9, 2026|date:letter date]]
VIA SECURE PORTAL AND FIRST-CLASS MAIL
[[Leilani Kapule-Stroud|p1:full]], Trustee
[[Kapule-Stroud Living Trust|o4:full]] u/a/d [[6/14/2011|date:trust date]]
[[PO Box 2291|addr:PO Box]]
[[Hood River|place:city]], [[OR|place!:state abbreviation that is also a word]] [[97031|zip]]
Re: 2025 Schedule K-1 (Form 1065), [[Wapato Flats Hop Growers, LP|o2:full]]
Partnership EIN [[93-1284406|taxid:EIN]]; partner no. [[017|rec!:partner number, three digits]]
Dear [[Ms. Kapule-Stroud|p1:title-surname]]:
Enclosed is the Trust's 2025 Schedule K-1 from [[Wapato Flats|o2:short]] (the "Partnership"). The K-1 was issued under the Trust's taxpayer identification number, which for a grantor trust is your Social Security number, shown on the form as [[XXX-XX-6538|ssn:masked SSN, capital X]]. Please confirm that the last four digits ([[6538|ssn:last four only]]) match your records; the prior-year K-1 was issued in error under the Trust's old EIN, [[93-6019954|taxid:EIN of a trust]].
Summary of your share (limited partner, 4.25% of profit, loss and capital):
- Box 1, ordinary business income: [[$38,412|money]]
- Box 5, interest income: [[$207|money]]
- Box 19A, cash distributions: [[$22,000|money]], paid [[07/15/2025|date]] and [[12/19/2025|date]] by ACH to the account ending [[...4471|acct:last four with ellipsis]] at [[Mount Defiance Credit Union|o5:full]]
- Box 20Z, Section 199A information: see Statement A
- Capital account (tax basis): beginning [[$311,906|money]]; ending [[$328,525|money]]
State matters. The Partnership operates in Oregon and [[Washington|place!:state name that is also a surname and a city]] ([[Yakima County|place:county]]). Your Washington-source share is [[$9,880|money]]; no Washington income tax return is required. The Partnership paid Oregon elective pass-through entity tax (PTE-E) of [[$3,457|money]] on your behalf under OR BIN [[1847729-5|taxid:state business identification number]], which you may claim as a credit on your Oregon individual return.
Portal access. Your K-1 package is posted here:
[[https://portal.brennecke-oyama.example/k1/WFHG-017|url:portal link containing partner number]]
Sign in with user ID [[lkapulestroud|cred:portal username]]; your one-time passcode is [[Hops-7731-Kiln|cred:temporary password]] and expires in 14 days. If you are locked out, call [[Dev Rangarajan|p3:full]] at [[503-555-0139|phone]]. Please do not email the passcode.
Items needing your attention:
1. The general partner, [[Hop Hollow Management LLC|o3:full]], still shows your address of record as the [[Odell|place!:town name that is also a surname]] farmhouse ([[3390 Straight Hill Road|addr]]). We gave them the PO box.
2. [[Burkhard Stoll|p4:full]] of [[Hop Hollow|o3:short]] advised that the [[$15,000|money]] capital call noticed [[January 30|date:month and day only]] is due [[April 1, 2026|date:due date]]. Wire to Mount Defiance Credit Union, routing [[028784395|rtn]], acct [[70044180226|acct]], reference [[WFHG-CC-2026-017|rec:capital call reference]].
3. The 0.75% interest formerly held by [[your late husband|indirect:family relationship to a named person]], [[Gordon Stroud|p5:full]] (d. [[11/02/2024|date:date of death]]), was combined with the Trust's interest. [[Mr. Stoll|p4:title-surname]] confirms that the § 754 basis step-up of [[$46,300|money]] is reflected on Statement B. [[Gordon|p5:first-name]]'s final K-1 was sent to the estate's attorney.
Estimated tax (Form 1040-ES). Based on the K-1 alone we project additional 2025 federal tax of about [[$8,900|money]] and recommend a first-quarter 2026 estimate of [[$2,300|money]] by [[April 15|date:month and day only]]. Our fee for the K-1 review is [[$450.00|money]], invoice [[BO-26-1187|rec:invoice number]].
Very truly yours,
[[Noriko Oyama|p2:full]], CPA (OR lic. [[11482|govid!:CPA license number, bare digits]]) · PTIN [[P01847720|taxid:PTIN]]
Direct [[(503) 555-0171|phone]] · [[noyama@brennecke-oyama.example|email]]
cc: [[B. Stoll|p4:short:initial + surname]], Hop Hollow; file [[KAPULE-STROUD, L.|p1:caps:caps surname with initial]] / [[2025-K1-0417|rec:file number]]
'''))

# ---------------------------------------------------------------- 203
DOCS.append(D(203, "pdf", "lab report", "health", "US",
  title="Final chemistry and haematology report for a 91-year-old resident",
  ents={"p1": "Eudora M. Fenwick", "p2": "Anselm Okereke", "p3": "Priyanka Vaidya", "p4": "Tyrell Guillory",
        "p5": "Corinne Baptista", "p6": "Marguerite Fenwick-Dahl",
        "o1": "Saltgrass Clinical Laboratories", "o2": "Seawall Geriatric Associates",
        "o3": "The Moorings at Offatts Bayou", "o4": "Seabreeze Retiree Health Plan"},
  distractors=["CLIA", "ICD-10", "CKD-EPI 2021", "Medicare Part B", "HIPAA", "136-145", "3.5-5.1", "0.50-1.10",
               "70-99", "11.7-15.5", "150-400", "0.40-4.50", "Page 1 of 1"],
  ok=["F", "H", "L", "MA", "SN", "FINAL", "REPORT", "07:42", "10:15", "06:03", "06:20", "06:01", "59", "5.7",
      "Sodium", "Potassium", "Creatinine", "Glucose", "Hemoglobin", "A1c", "Platelets", "TSH",
      "Chemistry", "Hematology", "Reference", "Critical", "ID", "K", "MBI", "Lab", "Director", "Sex", "Age", "Accession", "Ordering", "Collected", "Received", "Reported",
      "Fasting", "Clinical", "Comment", "Called", "Billing", "Electronically", "End", "Copy", "Result", "Flag",
      "Units", "Test", "Patient"],
  body=r'''
# [[Saltgrass Clinical Laboratories|o1:full]]
[[6100 Stewart Road, Bldg C|addr:street with building]], [[Galveston|place:city]], [[TX|place:state abbreviation]] [[77551|zip]] · CLIA [[45D2088417|govid:CLIA number]] · Lab Director: [[Priyanka Vaidya, MD|p3:full:full name with credential]]
## FINAL REPORT
Patient: [[FENWICK, EUDORA M|p1:caps:caps, Last, First order]]. DOB: [[02/11/1935|dob]]. Age: [[91 Y|age:abbreviated age]]. Sex: F
MRN: [[SG-00418872|rec:medical record number]]. Accession: [[26-098-04417|rec:accession number]]. Patient phone: [[409-555-0126|phone]]
Ordering provider: [[Anselm Okereke, DO|p2:full:full name with credential]] (NPI [[1730594826|govid:NPI]]), [[Seawall Geriatric Associates|o2:full]], fax [[(409) 555-0190|phone:fax]]
Collected: [[04/08/2026|date:collection date]] 07:42 by [[T. Guillory|p4:short:initial + surname]] at the resident's apartment, [[The Moorings at Offatts Bayou|o3:full]], [[8801 Teichman Road, Apt 214|addr:street with apartment]]
Received: 04/08/2026 10:15. Reported: [[04/09/2026|date:report date]] 06:03. Fasting: yes (per caregiver)
Clinical indication: [[CKD stage 3b|health:diagnosis in shorthand]]; [[type 2 diabetes|health:diagnosis]]; monitoring on [[apixaban 2.5 mg BID|health:medication and dose]]. ICD-10 [[N18.32|health:diagnosis code]], [[E11.22|health:diagnosis code]].
| Test | Result | Flag | Reference | Units |
| Sodium | [[133|health:lab value in a table cell]] | L | 136-145 | mmol/L |
| Potassium | [[5.4|health:lab value in a table cell]] | H | 3.5-5.1 | mmol/L |
| Creatinine | [[1.62|health:lab value in a table cell]] | H | 0.50-1.10 | mg/dL |
| eGFR | [[31|health:lab value in a table cell]] | L | >59 | mL/min |
| Glucose | [[148|health:lab value in a table cell]] | H | 70-99 | mg/dL |
| Hemoglobin A1c | [[7.9|health:lab value in a table cell]] | H | <5.7 | % |
| Hemoglobin | [[10.2|health:lab value in a table cell]] | L | 11.7-15.5 | g/dL |
| Platelets | [[212|health:lab value in a table cell]] | | 150-400 | K/uL |
| TSH | [[2.31|health:lab value in a table cell]] | | 0.40-4.50 | uIU/mL |
Comment: Potassium rechecked on a second aliquot (5.4 confirmed); specimen not hemolyzed. Critical-value policy not triggered. eGFR by CKD-EPI 2021; down from [[38|health:prior lab value]] on [[01/14/2026|date:prior test date]]. Chemistry analyzer SN [[CX5-2209-1187|dev:analyzer serial number]]; Hematology analyzer SN [[XN-44071|dev:analyzer serial number]].
Called to [[Dr. Okereke|p2:title-surname]]'s MA, [[Corinne|p5:first-name]], at 06:20 on [[4/9|date:month/day only]]; read back. Copy to daughter and health care agent [[Marguerite Fenwick-Dahl|p6:full]] (HIPAA release on file), [[mfdahl@postbox.example|email]]. Results online: [[https://results.saltgrasslabs.example/r/26-098-04417|url:results link containing accession number]]
Billing: Medicare Part B, MBI [[4TK8-WE2-RM61|govid:Medicare beneficiary identifier]]; secondary [[Seabreeze Retiree Health Plan|o4:full]], ID [[SBR 771 204 663|rec:member ID with spaces]]. Patient responsibility: [[$0.00|money]].
[[Mrs. Fenwick|p1:title-surname]] asked that results not be left with front-desk staff at [[The Moorings|o3:short]]. She has [[significant hearing loss|health:condition]]; call the daughter first at [[409.555.0158|phone:dotted]].
Electronically signed: [[P. Vaidya|p3:short:initial + surname]], 04/09/2026 06:01. Page 1 of 1. End of report.
'''))

# ---------------------------------------------------------------- 204
ST = "[[OH|place!:state abbreviation that is also a word]]"
DOCS.append(D(204, "xlsx", "HR onboarding checklist", "general", "US",
  title="New-hire onboarding workbook: people, direct deposit, equipment, accounts, I-9",
  ents={"p1": "Zubair Hakimi", "p2": "Lourdes Santamaría", "p3": "Thaddeus Okonedo", "p4": "Siobhan Kettering",
        "p5": "Nasreen Hakimi", "p6": "Hector Santamaría", "p7": "Emmanuel Okonedo", "p8": "Rory Kettering",
        "p9": "Annika Vuong",
        "o1": "Thimbleberry Print Works, Inc.", "o2": "Olentangy Savings Bank", "o3": "Scioto Mile Credit Union",
        "o4": "Darby Creek Federal Credit Union"},
  distractors=["Latitude 7450", "MacBook Pro 14", "ThinkPad T14s", "Form I-551", "Form I-9", "List A", "List B",
               "List C", "U.S. Department of State", "Social Security Administration", "Ohio BMV", "USCIS",
               "YubiKey 5C", "iPhone 15"],
  ok=["HR", "MFA", "VPN", "MAC", "ST", "100%", "Rest", "Dell", "Apple", "Lenovo", "PT", "2019", "30", "4", "IP",
      "Mother", "Husband", "Father", "Spouse", "Laptop", "Phone", "Security", "Checking", "Savings",
      "Prepared", "Item", "Issued", "Value", "Notes", "Bank", "Routing", "Type", "Split", "Voided", "Serial",
      "Asset", "Username", "Temp", "Badge", "Door", "Issuer", "Expires", "Verified", "Emp", "Preferred",
      "Start", "Street", "Salary", "Emergency", "Relationship", "Personal", "Cell", "City", "Make", "Document",
      "U.S", "Passport", "Card", "Driver's", "License", "Social", "Last", "First", "Work", "IMEI", "ID",
      "Doc", "Name", "Date"],
  sheets=[
    ("New hires", [
      ["Emp ID", "Name (Last, First)", "Preferred", "Start date", "SSN", "DOB", "Personal email", "Cell", "Street", "City", "ST", "ZIP", "Salary", "Emergency contact", "Relationship", "Emergency phone", "Notes"],
      ["[[E-3051|rec:employee ID]]", "[[Hakimi, Zubair|p1:last-first]]", "[[Zub|p1:nickname]]", dt("2026-04-20", "mm/dd/yyyy", "date:start date"), "[[466-19-3214|ssn]]", dt("1994-08-23", "mm/dd/yyyy", "dob"),
       "[[zubair.hakimi94@inbox.example|email]]", "[[614-555-0126|phone]]", "[[2284 Indianola Avenue, Apt 3|addr:street with apartment]]", "[[Columbus|place:city]]", ST, "[[43201|zip]]", amt(68500, "usd0"),
       "[[Nasreen Hakimi|p5:full]]", "Mother", "[[(614) 555-0171|phone]]", "[[prayer room access requested for Fridays|attr:implies religious practice]]"],
      ["[[E-3052|rec:employee ID]]", "[[Santamaría, Lourdes|p2:last-first]]", "[[Lola|p2:nickname]]", dt("2026-04-20", "mm/dd/yyyy", "date:start date"), num(162316538, "ssn:SSN stored as a number, no separators"), dt("1987-01-09", "mm/dd/yyyy", "dob"),
       "[[lola.santamaria@inbox.example|email]]", "[[614.555.0148|phone:dotted]]", "[[61 Shamrock Court|addr]]", "[[Dublin|place!:city name that is also a foreign capital]]", ST, "[[43017|zip]]", amt(74250, "usd0"),
       "[[Hector Santamaría|p6:full]]", "Husband", "[[614-555-0102|phone]]", "sit/stand desk; [[lumbar fusion in 2024|health:surgical history]]"],
      ["[[E-3053|rec:employee ID]]", "[[Okonedo, Thaddeus|p3:last-first]]", "[[Thad|p3:nickname]]", dt("2026-05-04", "mm/dd/yyyy", "date:start date"), "[[457 37 5488|ssn:SSN with spaces]]", dt("2001-11-30", "mm/dd/yyyy", "dob"),
       "[[thadokonedo@inbox.example|email]]", "[[380 555 0119|phone!:spaces only]]", "[[905 Granville Street, Unit 12B|addr:street with unit]]", "[[Gahanna|place:city]]", ST, "[[43230|zip]]", amt(52000, "usd0"),
       "[[Emmanuel Okonedo|p7:full]]", "Father", "[[+1 614 555 0183|phone:international format]]", "PT (30 hrs) until graduation on [[5/9|date:month/day only]]"],
      ["[[E-3054|rec:employee ID]]", "[[Kettering, Siobhan|p4:last-first:Last, First; surname is also an Ohio city]]", "", dt("2026-05-04", "mm/dd/yyyy", "date:start date"), "[[***-**-9605|ssn:masked SSN]]", dt("1979-06-17", "mm/dd/yyyy", "dob"),
       "[[s.kettering@inbox.example|email]]", "[[6145550164|phone:no separators]]", "[[PO Box 418|addr:PO Box]]", "[[Westerville|place:city]]", ST, "[[43081|zip]]", amt(91800, "usd0"),
       "[[Rory Kettering|p8:full!:surname is also an Ohio city]]", "Spouse", "[[614-555-0190|phone]]", "full SSN given by phone to [[Annika|p9:first-name]]; [[rehire, left in 2019 after a layoff|indirect:employment history that singles out the person]]"],
      ["Prepared by", "[[Annika Vuong|p9:full]], HR", "[[Thimbleberry Print Works, Inc.|o1:full]]", dt("2026-04-13", "mm/dd/yyyy", "date:prepared date")],
    ]),
    ("Direct deposit", [
      ["Emp ID", "Bank", "Routing", "Account", "Type", "Split", "Voided check #"],
      ["E-3051", "[[Olentangy Savings Bank|o2:full]]", "[[020933490|rtn]]", "[[4471008823|acct]]", "Checking", "100%", "[[1042|rec!:check number that looks like a form number]]"],
      ["E-3052", "[[Scioto Mile Credit Union|o3:full]]", "[[017183839|rtn]]", num(880231774, "acct:account number stored as a number"), "Checking", "Rest", ""],
      ["E-3052", "Scioto Mile Credit Union", "017183839", "[[880231774-S1|acct:savings sub-account suffix]]", "Savings", amt(250, "usd"), ""],
      ["E-3053", "[[Darby Creek Federal Credit Union|o4:full]]", "[[030228331|rtn]]", "[[00-4417-229031|acct:account number with dashes]]", "Checking", "100%", "[[0217|rec!:check number with leading zero]]"],
      ["E-3054", "Olentangy Savings Bank", "020933490", "[[xxxxxx5512|acct:masked account, last four]]", "Checking", "100%", "form on file from 2019"],
    ]),
    ("Equipment", [
      ["Emp ID", "Item", "Make / model", "Serial", "Asset tag", "MAC", "Issued", "Value"],
      ["E-3051", "Laptop", "Dell Latitude 7450", "[[7HX2K94|dev:laptop serial number]]", "[[TPW-LT-0412|dev:asset tag]]", "[[3C:52:82:1A:9F:07|dev:MAC address]]", dt("2026-04-17", "d-mmm-yy", "date:issue date shown as d-mmm-yy"), amt(1389.00)],
      ["E-3052", "Laptop", "Apple MacBook Pro 14", "[[C02ZQ1V8MD6T|dev:laptop serial number]]", "[[TPW-LT-0413|dev:asset tag]]", "[[A4-83-E7-2B-66-10|dev:MAC address with dashes]]", dt("2026-04-17", "d-mmm-yy", "date:issue date shown as d-mmm-yy"), amt(2199.00)],
      ["E-3052", "Phone", "Apple iPhone 15", "IMEI [[35 626309 055542 0|dev:IMEI with spaces]]", "[[TPW-PH-0088|dev:asset tag]]", "", dt("2026-04-17", "d-mmm-yy", "date:issue date shown as d-mmm-yy"), amt(799.00)],
      ["E-3053", "Laptop", "Lenovo ThinkPad T14s", "[[PF-4T9K2L|dev:laptop serial number]]", "[[TPW-LT-0414|dev:asset tag]]", "[[84a9.3e11.c0d2|dev!:MAC address in dotted form]]", dt("2026-05-01", "d-mmm-yy", "date:issue date shown as d-mmm-yy"), amt(1254.50)],
      ["E-3054", "Security key", "YubiKey 5C", "[[18840217|dev!:security key serial, bare digits]]", "", "", dt("2026-05-01", "d-mmm-yy", "date:issue date shown as d-mmm-yy"), amt(55.00)],
    ]),
    ("Accounts", [
      ["Emp ID", "Username", "Work email", "Temp password", "MFA phone (last 4)", "VPN IP", "Badge #", "Door code"],
      ["E-3051", "[[zhakimi|cred:username]]", "[[zhakimi@thimbleberryprint.example|email]]", "[[Welcome!Tpw-0423|cred:temporary password]]", "[[0126|phone:last four digits only]]", "[[10.44.7.31|ip:private IPv4]]", "[[B-20417|rec:badge number]]", "[[4471#|cred:door code]]"],
      ["E-3052", "[[lsantamaria|cred:username]]", "[[lsantamaria@thimbleberryprint.example|email]]", "[[Maple#Harbor22|cred:temporary password]]", "[[0148|phone:last four digits only]]", "[[10.44.7.32|ip:private IPv4]]", "[[B-20418|rec:badge number]]", "[[9026#|cred:door code]]"],
      ["E-3053", "[[tokonedo|cred:username]]", "[[tokonedo@thimbleberryprint.example|email]]", "[[tpw.Start-9914|cred:temporary password]]", "[[0119|phone:last four digits only]]", "[[10.44.7.33|ip:private IPv4]]", "[[B-20419|rec:badge number]]", "[[3358#|cred:door code]]"],
      ["E-3054", "[[skettering|cred:username]]", "[[skettering@thimbleberryprint.example|email]]", "[[Ch@ngeMe-Kett1|cred:temporary password]]", "[[0164|phone:last four digits only]]", "[[10.44.7.34|ip:private IPv4]]", "[[B-20420|rec:badge number]]", "[[7714#|cred:door code]]"],
    ]),
    ("I-9", [
      ["Emp ID", "Document (Form I-9)", "Doc number", "Issuer", "Expires", "Verified by", "Date"],
      ["E-3051", "List A: [[Permanent Resident Card|attr:immigration status shown by the document type]] (Form I-551)", "[[MSC2190448715|govid:permanent resident card number]]; A-number [[219-044-871|govid:alien registration number]]", "USCIS", dt("2031-02-28", "mm/dd/yyyy", "date:document expiry"), "[[A. Vuong|p9:short:initial + surname]]", dt("2026-04-20", "mm/dd/yyyy", "date:start date")],
      ["E-3052", "List A: U.S. Passport", "[[A04417729|govid:passport number]]", "U.S. Department of State", dt("2033-09-14", "mm/dd/yyyy", "date:document expiry"), "A. Vuong", dt("2026-04-20", "mm/dd/yyyy", "date:start date")],
      ["E-3053", "List B: Driver's License", "[[UK441872|govid:driver's license number]]", "Ohio BMV", dt("2029-11-30", "mm/dd/yyyy", "date:document expiry"), "[[AV|p9:initials]]", dt("2026-05-04", "mm/dd/yyyy", "date:start date")],
      ["E-3053", "List C: Social Security Card", "[[457375488|ssn:SSN without separators]]", "Social Security Administration", "", "AV", dt("2026-05-04", "mm/dd/yyyy", "date:start date")],
      ["E-3054", "List A: U.S. Passport Card", "[[C12044871|govid:passport card number]]", "U.S. Department of State", dt("2027-03-02", "mm/dd/yyyy", "date:document expiry"), "AV", dt("2026-05-05", "mm/dd/yyyy", "date:verification date")],
    ]),
  ]))

# ---------------------------------------------------------------- 205
DOCS.append(D(205, "txt", "immigration intake notes", "legal", "US",
  title="Asylum consultation intake notes for a family with two children",
  ents={"p1": "Dilnoza Yusupova", "p2": "Rustam Yusupov", "p3": "Kamila Yusupova", "p4": "Timur Yusupov",
        "p5": "Beatriz Aldama", "p6": "Sevara Tursunova", "p7": "Otabek Nazarov", "p8": "Lyudmila Korzun",
        "p9": "Maryam Jalali", "p10": "Jahongir Yusupov", "p11": "Lev Brodskiy",
        "o1": "Aldama Immigration Counsel PLLC", "o2": "Kensington Auto Upholstery",
        "o3": "Pennypack Creek Elementary", "o4": "Zarafshon Ovozi", "o5": "Tacony Family Wellness Collaborative"},
  minors=["p3", "p4"],
  distractors=["Form I-589", "Form I-765", "Form G-639", "8 CFR § 208.7", "INA § 208(a)(2)(B)", "(c)(8)", "B-2",
               "WhatsApp", "Telegram", "FOIA", "I-589", "I-94", "JFK", "ARD", "EAD"],
  ok=["PC", "DOB", "1", "2", "4th", "2022", "2024", "10:30am", "Thurs", "Uzbek",
      "Russian", "Uzbekistan", "Atty", "Consult", "Referred", "Addr", "Spouse", "Kids", "Claim",
      "Health", "Fee", "Works", "INTAKE", "NOTES", "TO", "DO", "She", "Paid", "Need",
      "Affirmative", "Other", "Interview", "Quoted", "Upload", "Calendar", "Get", "Bring",
      "Admitted", "Filed", "Interpreter", "Summoned", "Wrote"],
  body=r'''
[[ALDAMA IMMIGRATION COUNSEL PLLC|o1:caps]] -- INTAKE NOTES (atty-client privileged)

Consult: Thurs [[2/19/26|date:numeric date with two-digit year]], 10:30am, in person w/ Uzbek/Russian interpreter ([[Sevara|p6:first-name]], staff)
Atty: [[B. Aldama|p5:short:initial + surname]]        New matter #: [[26-0188|rec:matter number]]
Referred by: cousin [[Otabek Nazarov|p7:full]] (former client, file [[23-0611|rec:file number]])

PC: [[Dilnoza Yusupova|p1:full]]  (passport spells it "[[YUSUPOVA DILNOZA BAKHTIYOROVNA|p1:caps:passport order with patronymic]]")
DOB [[14 Sept 1988|dob:day-first with abbreviated month]], [[Samarkand|place:city abroad]]. [[Uzbek citizen|attr:citizenship]], [[ethnic Tajik|attr:ethnicity]]. [[Sunni Muslim, not practicing|attr:religion]].
Uzbekistan ppt [[FA2217409|govid:passport number]], exp [[03/2029|date:month and year only]].
A# [[220-417-883|govid:alien registration number]] (from biometrics notice).  I-94 # [[64418820733|govid!:I-94 admission number, bare digits]]
Admitted JFK [[08/03/2023|date:entry date]] as B-2, stay authorized to [[02/02/2024|date]]  -> [[out of status since Feb 2024|attr:immigration status]] except for the pending asylum app.
Addr: [[7214 Frankford Ave, 2nd Fl rear|addr:street with floor]], [[Philadelphia|place:city]] [[PA|place:state abbreviation]] [[19135|zip]]
Cell [[267-555-0148|phone]] (WhatsApp + Telegram same #, handle [[@dilnoza_writes|cred:messaging handle]]).  Email [[d.yusupova88@inbox.example|email]]
ITIN [[943-88-4417|taxid:ITIN]] (got it for the 2024 return)

Spouse: [[Rustam Yusupov|p2:full]], DOB [[3/9/1985|dob:numeric without leading zeros]], entered w/ her on same B-2. No A#.
Works for cash at [[Kensington Auto Upholstery|o2:full]] (owner "[[Mr. Lev|p11:title-surname!:title + first name]]") -- [[NO work authorization|attr:immigration status]].
[[Rustam|p2:first-name]]: [[retail theft citation 2025, Bucks County, ARD completed|attr:criminal history]]; docket [[MJ-07104-NT-0000417-2025|rec:criminal docket number]]. Need certified disposition.

Kids:
 1. [[Kamila|p3:first-name]], b. [[22.11.2016|dob:dotted day-first]] [[Tashkent|place:city abroad]], Uzbek ppt [[FA3380162|govid:passport number]], came w/ parents (rider on mom's I-589).
    4th grade, [[Pennypack Creek Elementary|o3:full]]. [[Asthma, albuterol inhaler|health:diagnosis of a child]].
 2. [[Timur|p4:first-name]], b. [[June 6 2024|dob:month day year without comma]], Philadelphia -> [[USC by birth|attr:citizenship status]]. PA birth cert state file no. [[136-24-0418872|govid:birth certificate number]]

Claim (her words, summarized):
 - Wrote for the independent Telegram channel "[[Zarafshon Ovozi|o4:full]]" about forced labor in the cotton harvest. She was [[the only reporter who covered the 2022 Jizzakh cotton story under her own name|indirect:unique role]].
 - [[Detained two days by security services in June 2022|attr:detention history abroad]]; phone and laptop seized. Summoned twice more before they left.
 - [[her brother-in-law Jahongir|indirect:family relationship to a named person]] ([[Jahongir Yusupov|p10:full]]) [[is still in pretrial detention in Samarkand|attr:criminal justice status of a relative]].
 - Affirmative Form I-589 filed pro se [[01/18/2024|date:filing date]] with help of a "notario", [[Lyudmila Korzun|p8:full]], paid [[$1,800|money]] cash. Receipt no. [[ZNK2450041877|govid:USCIS receipt number]].
   Filed inside one year of entry so INA § 208(a)(2)(B) is fine. [[Korzun|p8:surname]] kept the originals - demand letter.
 - Interview notice: asylum office, [[Lyndhurst|place:town]] [[NJ|place:state abbreviation]]? (she is not sure), [[04/22/2026|date:interview date]]. Calendar it. 8 CFR § 208.7 clock running; EAD (c)(8) expires [[July 30|date:month and day only]] -> renew now, Form I-765.

Health: [[PTSD and insomnia|health:mental health diagnosis]], sees [[Maryam Jalali, LCSW|p9:full:full name with credential]] at [[Tacony Family Wellness Collaborative|o5:full]] every other week. Get a letter from [[Ms. Jalali|p9:title-surname]]. [[Dilnoza|p1:first-name]] is [[14 weeks pregnant|health:pregnancy]] (due [[mid-August|date:approximate month]]).

Fee: Quoted [[$6,500|money]] flat for asylum representation through interview + [[$1,200|money]] for both EAD renewals. Paid [[$1,000|money]] cash today, receipt [[#4471|rec:receipt number]]. Balance [[$500/mo|money:monthly instalment]] starting [[3/15|date:month/day only]].

TO DO
 - FOIA (Form G-639) for her A-file and the I-94 history
 - Upload link sent: [[https://clients.aldama-immigration.example/upload/26-0188|url:client upload link containing matter number]]
 - Bring: both passports, Kamila's school records, Timur's birth cert, anything from [[Otabek|p7:first-name]] who can corroborate the 2022 detention
 - Other atty on file will be [[Beatriz Aldama|p5:full]] only. Interpreter for prep: [[Sevara Tursunova|p6:full]], [[215.555.0107|phone:dotted]]
'''))

# ---------------------------------------------------------------- 206
DOCS.append(D(206, "txt", "payment authorization form", "accounting", "US", length="short",
  title="One-time credit card authorization for tax preparation fees",
  ents={"p1": "Hyacinth Obuya", "p2": "Cornelius J. Obuya", "o1": "Pruneda & Lamb Tax Service"},
  cardholders=["p2"],
  distractors=["Form 1040", "PCI DSS 3.2", "Mastercard"],
  ok=["CARD", "AUTHORIZATION", "CVC", "Exp", "Ph", "2025", "Do", "Client", "Name", "Card", "Billing", "Charge", "Signed"],
  body=r'''
CARD AUTHORIZATION - [[Pruneda & Lamb Tax Service|o1:full]]
Client: [[Hyacinth Obuya|p1:full]] (file [[T-5582|rec:client file number]])
Name on card: [[CORNELIUS J OBUYA|p2:caps:name as embossed on card]]
Card: Mastercard [[5544 8942 4810 9413|card:card number with spaces]]   Exp [[11/27|exp]]   CVC [[306|cvv]]
Billing: [[618 Tamarind Ct|addr]], [[Yuma|place:city]], [[AZ|place:state abbreviation]] [[85364|zip]]
Charge [[$385.00|money]] for 2025 Form 1040 prep on [[4/2/26|date:numeric date with two-digit year]]; balance of [[$140|money]] at pickup.
Signed: [[C. Obuya|p2:short:initial + surname]]    Ph [[928-555-0173|phone]]
Do not store CVC after processing (PCI DSS 3.2).
'''))

# ---------------------------------------------------------------- 207
DOCS.append(D(207, "txt", "prior-authorization request", "health", "US",
  title="Expedited prior-authorization resubmission for a specialty cardiac drug",
  ents={"p1": "Casimir T. Wojtowicz", "p2": "Lakshmi Vemulapalli", "p3": "Stanislaw Wojtowicz", "p4": "Tessa Rourke",
        "p5": "Jolene Twofeathers",
        "o1": "Owyhee Senior Advantage HMO", "o2": "Boise Bench Heart Clinic", "o3": "Ridgecrest Specialty Pharmacy",
        "o4": "Bogus Basin Imaging"},
  distractors=["42 CFR § 422.572", "ICD-10", "NYHA", "Tc-99m PYP", "NCPDP", "Policy RX-CARD-014", "FACC", "6MWT", "H/CL"],
  ok=["PRIOR", "AUTHORIZATION", "REQUEST", "URGENT", "72", "FAX", "COVER", "FORM", "4", "pp", "UM", "Dept", "Ph", "MEMBER",
      "PRESCRIBER", "DRUG", "REQUESTED", "DIAGNOSIS", "CLINICAL", "JUSTIFICATION", "PLAN", "USE", "ONLY", "M", "Sex",
      "PO", "#30/30", "12", "II", "AFib", "HFpEF", "LVEF", "GLS", "NT-proBNP", "AL", "HF", "6", "90", "PA", "RN", "MD",
      "Pharmacy", "Cardiology", "Member", "Group", "Dispensing", "Denial", "Request", "Attestation", "Reviewer",
      "Rcvd", "Decision", "Approved", "Denied", "Auth", "Two", "Step", "Echo", "Serum/urine", "Plan", "Pt/family",
      "Ref/PA", "Contact", "1.8", "3", "52%", "17", "11%", "1/2026", "212", "14:10", "14:22", "Ste", "W", "N", "St",
      "DEA", "Manufacturer", "NT", "POA", "Serum"],
  body=r'''
PRIOR AUTHORIZATION REQUEST -- URGENT (72 hr)                 FAX COVER + FORM, 4 pp

To:    [[Owyhee Senior Advantage HMO|o1:full]], Pharmacy UM Dept          Fax [[208-555-0199|phone:fax]]
From:  [[Boise Bench Heart Clinic|o2:full]], [[1420 W Kootenai St Ste 210|addr:street with suite]], [[Boise|place:city]] [[ID|place!:state abbreviation that is also a word]] [[83705|zip]]
       Ph [[(208) 555-0112|phone]]   Fax [[208.555.0113|phone:fax, dotted]]
Sent:  [[05/06/2026|date:date sent]] 14:10       Ref/PA case #: [[PA-26-0558713|rec:prior authorization case number]]
       (resubmission after denial [[DN-26-0091442|rec:denial reference number]] dtd [[4/29/26|date:numeric date with two-digit year]])

MEMBER
Name: [[Wojtowicz, Casimir T.|p1:last-first]]        DOB: [[11/30/1933|dob]]  (age [[92|age:bare age]])     Sex: M
Member ID: [[OSA904417288-01|rec:health plan member ID]]      Group: [[MAPD-ID-007|rec:group number]]      Medicare #: [[7UF2-KD9-YT44|govid:Medicare beneficiary identifier]]
Address: [[2206 N 28th St|addr]], Boise, ID [[83703|zip]]         Ph: [[208 555 0146|phone!:spaces only]] (son answers; pt is [[hard of hearing|health:condition]])

PRESCRIBER
[[Lakshmi Vemulapalli, MD|p2:full:full name with credential]], FACC -- Cardiology       NPI [[1568204417|govid:NPI]]     DEA [[FV4418823|govid:DEA number]]     ID lic. [[M-11872|govid:state medical license number]]
Contact: [[Tessa|p4:first-name]] (PA coordinator) ext 6, [[tessa.r@boisebenchheart.example|email]]

DRUG REQUESTED
[[tafamidis 61 mg capsule, 1 cap PO daily|health:medication and dose]], #30/30 days, 12 refills
Dispensing pharmacy: [[Ridgecrest Specialty Pharmacy|o3:full]], NCPDP [[1344178|rec!:pharmacy identifier, bare digits]], ph [[800-555-0164|phone:toll-free]]

DIAGNOSIS: [[wild-type transthyretin amyloid cardiomyopathy|health:diagnosis]] ([[ATTR-CM|health:diagnosis in shorthand]]), ICD-10 [[E85.82|health:diagnosis code]]; HFpEF, [[NYHA class II|health:functional class]];
[[permanent AFib|health:diagnosis in shorthand]]; [[CKD 3a|health:diagnosis in shorthand]].

CLINICAL JUSTIFICATION ([[Dr. Vemulapalli|p2:title-surname]]):
[[Mr. Wojtowicz|p1:title-surname]] is a [[92-year-old|age:age as an adjective]] retired machinist who lives alone with daily help from his son.
Tc-99m PYP scan [[03/12/2026|date:scan date]] at [[Bogus Basin Imaging|o4:full]]: [[grade 3 myocardial uptake|health:imaging result]], H/CL ratio 1.8. Serum/urine
immunofixation negative [[3/3/26|date:numeric date with two-digit year]] (no monoclonal protein), which rules out AL. Echo [[02/20/26|date:two-digit year]]: LVEF 52%, septum 17 mm,
GLS -11% with apical sparing. NT-proBNP [[2,840 pg/mL|health:lab result]] ([[2/20|date:month/day only]]) -> [[3,310|health:lab result]] ([[4/24|date:month/day only]]). Two HF admissions in 6 months
([[Dec 9-13, 2025|date:date range]] and [[3/28-4/1/26|date:date range, two-digit year]]). Current: [[torsemide 40 mg BID|health:medication and dose]], [[apixaban 2.5 mg BID|health:medication and dose]]. 6MWT 212 m.

Denial stated "age > 90 and NYHA class not documented." Plan criteria (Policy RX-CARD-014, rev. 1/2026) contain no age
limit, and NYHA II was documented [[4/24/26|date:numeric date with two-digit year]]. Step therapy not applicable; there is no formulary alternative.
Request expedited review under 42 CFR § 422.572.

Pt/family: son and POA [[Stanislaw ("Stan") Wojtowicz|p3:full:full name with nickname in quotes]], [[208-555-0177|phone]], will handle the copay, est. [[$268/mo|money:monthly amount]].
Manufacturer assistance application pending, ref [[VC-4417720|rec:assistance application number]]. [[Stan|p3:nickname]] asks that the plan NOT call his father directly.

Attestation: I certify the above is accurate and supported by the chart.   /s/ [[L. Vemulapalli MD|p2:short:initial + surname + credential]]   [[05/06/26|date:two-digit year]]

PLAN USE ONLY: Reviewer [[J. Twofeathers RN|p5:short:initial + surname + credential]]   Rcvd [[5/6/26|date:numeric date with two-digit year]] 14:22   Decision due [[5/9/26|date:numeric date with two-digit year]]
[ ] Approved  [ ] Denied   Auth # ________
'''))

# ---------------------------------------------------------------- 208
DOCS.append(D(208, "docx", "lease abstract", "legal", "US",
  title="Abstract of a restaurant lease with personal guaranty",
  ents={"p1": "Quang Trinh", "p2": "Mai-Ly Trinh", "p3": "Delphine Castaing", "p4": "Imani Fairley",
        "p5": "Anselmo Rojas",
        "o1": "Ironworks Yard Holdings LLC", "o2": "Bao & Brine Dumpling House, Inc.",
        "o3": "Ferrous Property Services", "o4": "Shockoe Trust Bank", "o5": "Fairley Legal PLC",
        "o6": "Tredegar Mutual Insurance Co."},
  header="[[Ironworks Yard|o1:short]] - Unit B - CONFIDENTIAL",
  footer="Abstract ID [[LA-2026-031|rec:abstract ID]] · [[D. Castaing|p3:short:initial + surname]]",
  distractors=["Va. Code § 55.1-1200", "ABC", "CAM", "FMV", "Sienna", "Lot C", "Article 14", "Exhibit D"],
  ok=["LEASE", "ABSTRACT", "CONFIDENTIAL", "Unit", "B", "ID", "SCC", "FEIN", "ACH", "CGL", "L/C", "2,840", "310",
      "90-day", "5-year", "95%", "6%", "5%", "5th", "12%", "36", "60", "45", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
      "7–10", "1–2", "3–5", "6–10", "Not", "Lease", "Tenant", "Landlord", "Guarantors", "Guaranty", "Guarantor", "Premises",
      "Term", "Commencement", "Rent", "Expiration", "Base", "Annual", "Monthly", "Percentage", "Late", "Security",
      "Use", "Fast-casual", "Asian", "Yard", "Parking", "Four", "Loading", "Insurance", "Policy", "Notices",
      "Abstractor's", "Tax", "Two", "Parties", "Prepared", "January", "Abstract", "C", "Fast", "L", "Tenant's"],
  body=r'''
# LEASE ABSTRACT
Prepared [[10 March 2026|date:day month year]] by [[Delphine Castaing|p3:full]], [[Ferrous Property Services|o3:full]], for the owner's lender file. Not a substitute for the Lease.
## 1. Parties
Landlord: [[Ironworks Yard Holdings LLC|o1:full]], a [[Virginia|place:state]] limited liability company (SCC ID [[S7041882|rec:state entity number]]), c/o Ferrous Property Services, [[1700 Altamont Avenue, Suite 5|addr:street with suite]], [[Richmond|place:city]], [[VA|place:state abbreviation]] [[23230|zip]].
Tenant: [[Bao & Brine Dumpling House, Inc.|o2:full]] (d/b/a "[[Bao & Brine|o2:short]]"), FEIN [[84-3317204|taxid:EIN]].
Guarantors: [[Quang Trinh|p1:full]] and [[Mai-Ly Trinh|p2:full]], husband and wife, jointly and severally (Guaranty dated [[09/22/2023|date]], Exhibit D). Guarantor data per the credit application: [[Mr. Trinh|p1:title-surname]], DOB [[4/17/1979|dob:numeric without leading zero]], SSN ending [[8841|ssn:last four only]]; [[Mrs. Trinh|p2:title-surname]], DOB [[1981-12-02|dob:ISO format]], SSN [[xxx-xx-0416|ssn:masked SSN]]; residence [[9 Wythe Mews|addr]], [[Henrico|place:county]], VA [[23229|zip]].
## 2. Premises
[[3119 West Leigh Street, Unit B|addr:street with unit]], Richmond, VA 23230 (in [[Scott's Addition|place!:neighbourhood made of ordinary words]]), approx. 2,840 rentable sq. ft. on the ground floor plus a 310 sq. ft. patio licence. Tax parcel [[N000-1687/014|rec:tax parcel number]].
## 3. Term
Lease dated [[September 22, 2023|date]]. Commencement [[11/01/2023|date]]; Rent Commencement [[February 1, 2024|date]] (90-day abatement). Expiration [[10/31/2033|date]]. Two 5-year options at 95% of FMV; notice no later than [[Jan. 31, 2033|date:abbreviated month]]. The Lease is governed by Virginia law; Va. Code § 55.1-1200 et seq. does not apply to commercial premises.
## 4. Base rent
| Lease years | Annual | Monthly |
| 1–2 | [[$79,520.00|money]] | [[$6,626.67|money]] |
| 3–5 | [[$85,200.00|money]] | [[$7,100.00|money]] |
| 6–10 | [[$93,720.00|money]] | [[$7,810.00|money]] |
Percentage rent: 6% of gross sales over a natural breakpoint of [[$1,325,333|money]] (years 1–2). CAM, taxes and insurance estimated at [[$5.85 psf|money:rate per square foot]], or [[$1,384.50/mo|money:monthly amount]]. Late charge 5% after the 5th; default interest 12% (Article 14).
## 5. Security deposit
[[$19,880|money]] (three months), held in escrow account no. [[2204 7718 03|acct:account number with spaces]] at [[Shockoe Trust Bank|o4:full]] (ABA [[052646247|rtn]]), plus standby L/C no. [[SB-2023-00417|rec:letter of credit number]] for [[$40,000|money]], reducing to [[twenty thousand dollars|money:amount in words]] after month 36.
## 6. Use and exclusive
Fast-casual dumpling restaurant with beer and wine (ABC licence no. [[088-417205|govid:state alcohol licence number]]). Landlord may not lease to another "Asian dumpling or noodle concept" in the Yard.
## 7. Parking and loading
Four reserved permits in Lot C (permit nos. [[IY-0211|rec:parking permit number]] to [[IY-0214|rec:parking permit number]]), assigned to: VA plate [[UKR-4417|veh:license plate]] ([[Q. Trinh|p1:short:initial + surname]], grey Sienna); VA [[TZW 2291|veh:license plate with a space]] ([[M. Trinh|p2:short:initial + surname]]); [[VLD-8830|veh!:license plate, no state given]] ([[the head chef, Anselmo|indirect:unique role at a small business]]); and the delivery van, VIN [[1FTBR1C84PKA44172|veh:VIN]], plate pending. Loading dock 7–10 a.m. only.
## 8. Insurance and notices
CGL [[$1M|money!:abbreviated amount in millions]] per occurrence / [[$2M|money!:abbreviated amount in millions]] aggregate; liquor liability [[$1,000,000|money]]. Policy [[BOP-7718204-03|rec:policy number]], [[Tredegar Mutual Insurance Co.|o6:full]]. Notices to Tenant at the Premises, with a copy to [[Imani Fairley, Esq.|p4:full:full name with suffix]], [[Fairley Legal PLC|o5:full]], [[ifairley@fairleylegal.example|email]], [[804-555-0138|phone]].
## 9. Abstractor's flags
- The Guaranty burns off after month 60 if there has been no default. [[Quang|p1:first-name]] asked on [[3/3/26|date:numeric date with two-digit year]] that [[Mai-Ly|p2:first-name]] be released now because of [[their pending divorce|attr:marital status change]]. Referred to the owner.
- Tenant was [[45 days late on January rent|attr:financial distress]]; cured [[2/14/2026|date]] by cashier's check no. [[0098417|rec:check number]] for [[$7,455.00|money]] including the late charge.
- Rent is pulled by ACH from Tenant's operating account ending [[5530|acct:last four only]]. Mr. Trinh's cell is [[(804) 555-0177|phone]]; [[quang@baoandbrine.example|email]]. [[Anselmo Rojas|p5:full]] has the alarm code and opens most days.
'''))

# ---------------------------------------------------------------- 209
DOCS.append(D(209, "eml", "personal tax intake email", "accounting", "CA", enc="base64",
  title="Client email with T1 information for a Winnipeg family",
  ents={"p1": "Maricel A. Dumalagan", "p2": "Rodel Dumalagan", "p3": "Priscilla Hiebert", "p4": "Althea Dumalagan",
        "p5": "Joaquin Dumalagan", "p6": "Tyler Wolanski", "p7": "Achieng Otieno",
        "o1": "Hiebert & Wolanski Chartered Professional Accountants", "o2": "Voyageur Kids Child Care Co-op",
        "o3": "Kildonan Pines Personal Care Home", "o4": "Transcona Railcar Works Ltd.",
        "o5": "Keewatin Savings Credit Union", "o6": "Henderson Smiles Orthodontics", "o7": "Ecole Bonaventure School"},
  minors=["p4", "p5"],
  distractors=["T1", "T4", "T5", "T2201", "RRSP", "RESP", "NETFILE", "Canada Child Benefit", "GST credit", "Sign-In Partner",
               "box 14", "box 44", "CPAP", "Sienna", "GST"],
  ok=["0600", "2025", "2019", "2027", "1", "2", "3", "4", "5", "60", "9:02", "US", "KIDS", "SLIPS", "MEDICAL", "OTHER", "Me",
      "Same", "Here", "The", "Can", "We're", "Salamat", "Security", "PR", "CRA", "Sorry", "My", "I'm", "Our", "Hi",
      "AM", "BN", "ID", "SIN", "SINs"],
  headers={"From": "[[Maricel Dumalagan|p1:short:first and last name]] <[[maricel.dumalagan@prairiemail.example|email]]>",
           "To": "[[Priscilla Hiebert|p3:full]] <[[phiebert@hiebertwolanski.example|email]]>",
           "Cc": "[[rodel.d@prairiemail.example|email]]",
           "Subject": "Re: 2025 T1 checklist - [[Dumalagan|p1:surname:family surname]] family (client [[HW-4418|rec:client number]])",
           "Date": "Sat, [[28 Feb 2026|date:email date]] 21:47:12 -0600"},
  body=r'''
Hi [[Priscilla|p3:first-name]],

Sorry this is late, [[Rodel|p2:first-name]] was on nights all month. Here is everything on your checklist. The slips are in the portal folder, I'm just typing the numbers so you have them in one place.

1) US
Me: [[Maricel A. Dumalagan|p1:full]], SIN [[615-614-740|taxid:SIN with dashes]], born [[March 2 1988|dob:month day year without comma]]
[[Rodel Dumalagan|p2:full]], SIN [[107 431 645|taxid:SIN with spaces]], DOB [[1986-07-19|dob:ISO format]]
We moved on [[Aug 1, 2025|date:abbreviated month]] from [[7-1190 Henderson Hwy|addr:unit-first Canadian address]] to [[412 Larchdale Crescent|addr]], [[Winnipeg|place:city]] [[MB|place:province abbreviation]] [[R2K 1V7|zip:Canadian postal code]]. Same phone [[204-555-0155|phone]], Rodel's cell is [[431-555-0121|phone]].

2) KIDS
[[Althea|p4:first-name]] - [[May 9, 2015|dob]] - SIN [[627698780|taxid:SIN without separators]] (we got her one for the RESP)
[[Joaquin|p5:first-name]] ("[[Wakin|p5:nickname]]") - [[Oct. 27, 2019|dob:abbreviated month]] - no SIN yet
Joaquin is at [[Voyageur Kids Child Care Co-op|o2:full]] full days, receipts total [[$7,480.00|money]] (their BN is [[81442 7705 RR0001|taxid:Canadian business number]]). Althea is in the before-and-after program at [[Ecole Bonaventure School|o7:full]], [[$2,160|money]].

3) SLIPS
My T4 from [[Kildonan Pines Personal Care Home|o3:full]]: box 14 [[$52,318.44|money]], tax deducted [[8,104.27|money!:no currency sign]], union dues [[611.52|money!:no currency sign]] ([[I'm in the health care aides' local|attr:union membership]]).
Rodel's T4 from [[Transcona Railcar Works Ltd.|o4:full]]: [[$71,905.10|money]], box 44 dues [[$1,112.80|money]].
T5 from [[Keewatin Savings Credit Union|o5:full]], [[$38.11|money]].
RRSP: Rodel put [[$4,200|money]] in his RRSP at [[Keewatin|o5:short]], contract no. [[RSP-0041877|rec:RRSP contract number]]. Of that, [[$1,500|money]] was on [[Feb 20, 2026|date:abbreviated month]] (first 60 days).

4) MEDICAL
- Althea's [[braces|health:orthodontic treatment of a child]] at [[Henderson Smiles Orthodontics|o6:full]], [[$3,950|money]] (paid [[2,000|money!:no currency sign]] so far)
- Rodel's CPAP machine for his [[sleep apnea|health:diagnosis]], [[$1,289|money]]
- Joaquin's [[speech therapy|health:treatment of a child]], not covered, [[$1,640|money]]. You said last year we should do the T2201 for his [[autism diagnosis|health:diagnosis of a child]]. [[Dr. Achieng Otieno|p7:full:full name with title]] signed the form on [[Jan 14|date:month and day only]], it's in the folder.

5) OTHER
- I sent [[$6,000|money]] to [[my mother in Batangas|indirect:family relationship and location abroad]] over the year (tuition for my sister). I know it's probably not deductible but you asked.
- Canada Child Benefit and the GST credit should keep going to my account: Keewatin Savings Credit Union, transit [[04417|rtn:Canadian transit number]], institution [[879|rtn:Canadian institution number]], account [[1002288417|acct]]. Rodel's refund goes to the joint one, same transit, acct [[1002291056|acct]].
- CRA sign-in: user ID [[mdumalagan88|cred:username]], password [[Bahay-Kubo#2015|cred:password in an email]]. Security question (mother's birthplace) = [[Tagaytay|cred:security answer that is a place name]]. Rodel uses the Sign-In Partner through the credit union so there is no password, but his NETFILE access code from last year's notice is [[7K4T9B2Q|cred:NETFILE access code]].
- I [[became a Canadian citizen|attr:citizenship status]] on [[Sept 12, 2025|date:abbreviated month]]!! Rodel is [[still PR|attr:immigration status]], his card expires 2027.

Can you tell us roughly what we owe or get back before [[March 20|date:month and day only]]? We're trying to decide about the van (2019 Sienna).

Salamat,
[[Maricel|p1:first-name]]
204-555-0155

> On Tue, [[Feb 17, 2026|date:abbreviated month]] at 9:02 AM [[Tyler Wolanski|p6:full]] <[[admin@hiebertwolanski.example|email]]> wrote:
> Hi Maricel, Priscilla asked me to send the 2025 checklist (attached). Our fee this year is [[$420|money]] + GST for the couple, by e-transfer to [[payments@hiebertwolanski.example|email]]. Please don't email your SINs, use the portal: [[https://portal.hiebertwolanski.example/c/HW-4418|url:portal link containing client number]]
> [[Tyler|p6:first-name]]
> [[Hiebert & Wolanski Chartered Professional Accountants|o1:full]] | [[204-555-0109|phone]] | [[3-845 Corydon Avenue|addr:unit-first Canadian address]], Winnipeg, MB [[R3M 0W8|zip:Canadian postal code]]
'''))

# ---------------------------------------------------------------- 210
DOCS.append(D(210, "txt", "parenting plan draft", "legal", "US", length="long",
  title="Draft parenting plan with attorney and client comments (two children)",
  ents={"p1": "Shoshana R. Lindenbaum", "p2": "Declan P. Rafferty", "p3": "Ezra Asher Rafferty",
        "p4": "Tovah Miriam Rafferty", "p5": "Nanami Fujikawa", "p6": "Garrett Zwick", "p7": "Odalys Menocal",
        "p8": "Farida Nazari", "p9": "Corbin Ellsworth", "p10": "Brielle Santoro", "p11": "Miriam Lindenbaum",
        "p12": "Saul Lindenbaum", "p13": "Colm Rafferty",
        "o1": "Fujikawa Family Law LLC", "o2": "Zwick & Brandvold, P.C.", "o3": "Poudre Bluffs Middle School",
        "o4": "Cottonwood Hollow Elementary", "o5": "Laporte Avenue Pediatric Group", "o6": "Horsetooth Ambulance Service",
        "o7": "Mulberry Street Dental Arts", "o8": "Congregation Ohr Hadash", "o9": "St. Brigid Parish",
        "o10": "NoCo Junior Eagles Hockey Club", "o11": "Horsetooth Employees Benefit Trust",
        "o12": "Cache la Poudre Bank & Trust"},
  minors=["p3", "p4"],
  distractors=["C.R.S. § 14-10-124", "C.R.S. § 14-10-129", "C.R.C.P. 121", "IRS Form 8332", "OurFamilyWizard",
               "Infinite Campus", "Life360", "CollegeInvest", "Family Support Registry", "Worksheet A", "Exhibit A",
               "Subaru Outback", "F-150", "Model Y", "Buick", "Venmo", "Google", "48/96", "Support Order"],
  ok=["Div", "4B", "NOT", "FOR", "FILING", "DRAFT", "v4", "CAPS", "THE", "CHILDREN", "DECISION", "REGULAR",
      "SCHEDULE", "EXCHANGES", "AND", "TRANSPORTATION", "HOLIDAYS", "COMMUNICATION", "INFORMATION", "HEALTH", "CARE",
      "CHILD", "SUPPORT", "EXPENSES", "TAXES", "DOCUMENTS", "RELOCATION", "DISPUTES", "OTHER", "OPEN", "ITEMS",
      "SIGNATURES", "PROPOSED", "PARENTING", "PLAN", "DISTRICT", "COURT", "TO", "BE", "CHANGED", "INCLUDED", "IN",
      "FILED", "VERSION", "EXCEPT", "CANNOT", "PRE", "GF", "FSR", "SSNs", "529", "Plan", "Mother", "Father", "Mother's",
      "Father's", "Petitioner", "Drafter's", "Open", "Joint", "Religion", "School", "Summer", "Right",
      "Default", "Vehicles", "Late", "Garage", "Thanksgiving", "Winter", "Christmas", "Eve", "Day", "Hanukkah",
      "Passover", "Easter", "Spring", "Birthdays", "Halloween", "All", "Shared", "Pediatrician", "Records",
      "Insurance", "Uninsured", "Extracurriculars", "Reimbursements", "College", "Passports", "IDs", "January", "MAKING",
      "Neither", "Mediation", "Approved", "Reg", "Wed", "Sun", "Wednesday", "Sundays", "Friday", "Saturday",
      "Tuesday", "Under", "Phones", "Because", "Case", "Marriage",
      "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11",
      "1.1", "1.2", "1.3", "2.1", "2.2", "2.3", "3.1", "3.2", "3.3", "4.1", "4.2", "4.3", "4.4", "4.5", "5.1", "5.2",
      "5.3", "5.4", "5.5", "5.6", "6.1", "6.2", "6.3", "6.4", "7.1", "7.2", "7.3", "7.4", "7.5", "8.1", "8.2", "8.3",
      "8.4", "9.1", "9.2", "9.3", "10.1", "10.2", "14", "58%", "42%", "58/42", "139", "2026", "2027", "2026-27", "2021",
      "2022", "2019", "20", "30", "6th", "2nd", "4'9"],
  body=r'''
DISTRICT COURT, [[LARIMER COUNTY|place!:county in ALL CAPS]], [[COLORADO|place!:state in ALL CAPS]]
Case No. [[2025DR30417|rec:domestic relations case number]]            Div. 4B

In re the Marriage of:
[[SHOSHANA R. LINDENBAUM|p1:caps:name in caption]], Petitioner,
and
[[DECLAN P. RAFFERTY|p2:caps:name in caption]], Co-Petitioner.

PROPOSED PARENTING PLAN  (C.R.S. § 14-10-124)
DRAFT v4 - [[03/27/2026|date:draft date]] - [[NF|p5:initials]] redline after [[3/24|date:month/day only]] mediation w/ [[G. Zwick|p6:short:initial + surname]] - NOT FOR FILING

[Drafter's note: [[Shoshana|p1:first-name]]'s comments are in brackets marked [[SRL|p1:initials]]; [[Declan|p2:first-name]]'s, relayed by [[Garrett|p6:first-name]], are marked [[DPR|p2:initials]]. Open items in CAPS.]

1. THE CHILDREN
1.1 This Plan concerns the parties' two minor children:
    [[Ezra Asher Rafferty|p3:full]], born [[May 3, 2014|dob]] (age 11), 6th grade at [[Poudre Bluffs Middle School|o3:full]]; and
    [[Tovah Miriam Rafferty|p4:full]] ("[[Tovi|p4:nickname]]"), born [[09/19/2018|dob]] (age 7), 2nd grade at [[Cottonwood Hollow Elementary|o4:full]].
1.2 Mother ("[[Ms. Lindenbaum|p1:title-surname]]") lives at [[2418 Stover Street|addr]], [[Fort Collins|place:city]], [[CO|place:state abbreviation]] [[80525|zip]]. Father ("[[Mr. Rafferty|p2:title-surname]]") lives at [[915 Sandbar Court, Unit 4|addr:street with unit]], [[Windsor|place!:town name that is also a surname and a royal house]], CO [[80550|zip]], with his partner, [[Brielle Santoro|p10:full]].
1.3 Mother works as a dental hygienist at [[Mulberry Street Dental Arts|o7:full]] (Mon–Thu). Father is a paramedic with [[Horsetooth Ambulance Service|o6:full]] on a 48/96 rotation; his 2026 shift calendar is Exhibit A.

2. DECISION-MAKING
2.1 Joint decision-making for education, non-emergency health care and extracurricular activities. Religion: see 2.3.
2.2 If the parents cannot agree within 14 days they will consult the PRE, [[Dr. Odalys Menocal|p7:full:full name with title]] (appointed [[11/06/2025|date:appointment date]]; report dated [[Feb. 9, 2026|date:abbreviated month]]), before filing any motion. Her fee ([[$225/hr|money:hourly rate]]) is split 58% Father / 42% Mother.
2.3 Religion. The children will continue [[Hebrew school|attr:implies religion of the children]] at [[Congregation Ohr Hadash|o8:full]], and [[Ezra|p3:first-name]] will [[become bar mitzvah|attr:implies religion of a child]] there on Saturday, [[March 13, 2027|date:ceremony date]]. Father may [[take the children to Mass|attr:implies religion of a parent]] at [[St. Brigid Parish|o9:full]] during his time. Neither parent will disparage the other's faith. [SRL: I want it in writing that he won't have them baptized. DPR: agreed.]

3. REGULAR SCHEDULE
3.1 School year. Because of Father's 48/96 rotation the parties adopt a shift-following schedule. The children are with Father on each of his four-day blocks that begins on a Friday or Saturday, from 5:30 p.m. the first day until school drop-off the last day, and every Wednesday overnight when he is off shift. All other time is with Mother. Under Exhibit A this gives Father 139 overnights in 2026.
3.2 Summer ([[June 1|date:month and day only]] to [[August 9, 2026|date]]): alternating weeks, exchanges Sundays at 6:00 p.m.
3.3 Right of first refusal for any absence over 6 hours. [[Ms. Santoro|p10:title-surname]] and [[the maternal grandparents|indirect:relationship to named persons]] ([[Miriam|p11:first-name]] and [[Saul Lindenbaum|p12:full]] of [[Boulder|place!:city name that is also a common word]]) are pre-approved caregivers and are not subject to this paragraph.

4. EXCHANGES AND TRANSPORTATION
4.1 The receiving parent drives. Default exchange point is the [[Harmony Road Park-n-Ride|place:named facility]], east lot; school-day exchanges happen at school.
4.2 Vehicles authorized for pick-up, on file with both school offices: Mother's 2021 Subaru Outback, CO plate [[CKT-L41|veh:license plate]]; Father's white F-150, plate [[BXR-P07|veh:license plate]]; Ms. Santoro's grey Model Y, [[DWN-K68|veh!:license plate, unlabelled]]; Saul Lindenbaum's Buick, plate [[418-ZTQ|veh:license plate]].
4.3 [[Tovah|p4:first-name]] rides in a high-back booster until she is 4'9".
4.4 Late more than 20 minutes without a text means forfeited time, unless Father is held over on a call (he will text from the station line, [[970-555-0170|phone]]).
4.5 Garage keypad at [[Stover Street|place!:street used as a location]] for backpack drop-offs: code [[0519#|cred:garage keypad code]]. Mother will change it if Father's household shares it. [DPR: fine.]

5. HOLIDAYS (these override the regular schedule)
5.1 Thanksgiving: Mother in even years, Father in odd. 2026 is Mother's, Wed. [[Nov. 25|date:abbreviated month and day]] at 5:30 p.m. to Sun. [[Nov. 29|date:abbreviated month and day]].
5.2 Winter break 2026-27 ([[Dec. 19, 2026|date:abbreviated month]] to [[Jan. 4, 2027|date:abbreviated month]]): first half Father, including Christmas Eve and Christmas Day until noon on [[12/26|date:month/day only]]; second half Mother. Hanukkah: Mother has the first night ([[December 4, 2026|date]]) regardless.
5.3 Passover: first two seders with Mother (2027: [[April 21-22|date:two-day range without year]]). Easter Sunday with Father ([[3/28/27|date:numeric date with two-digit year]]).
5.4 Spring break ([[March 13-21, 2027|date:date range]]) alternates; 2027 is Father's EXCEPT the bar mitzvah weekend, which the parties share.
5.5 Birthdays: the non-scheduled parent gets two hours on [[May 3|date:child's birthday without year]] and [[September 19|date:child's birthday without year]].
5.6 Halloween follows the regular schedule. Mother's Day and Father's Day are with the honoree.

6. COMMUNICATION AND INFORMATION
6.1 All non-emergency communication between the parents goes through OurFamilyWizard. Phones for emergencies: Mother [[(970) 555-0134|phone]]; Father [[970.555.0188|phone:dotted]].
6.2 Shared calendar: the Google account [[raffertylindenbaum.kids@mailbox.example|email:shared account address]] (password [[EzTov!2026|cred:shared account password]] - TO BE CHANGED AND NOT INCLUDED IN FILED VERSION) holds the children's calendar. School portal (Infinite Campus) logins: Mother [[srlindenbaum|cred:portal username]], Father [[drafferty915|cred:portal username]].
6.3 Ezra has a phone ([[970-555-0116|phone:child's number]]). It travels with him; the screen-time passcode, [[3141|cred!:four-digit passcode]], is known to both parents and not to Ezra. No tracking apps installed by either parent without notice. [SRL: [[Brielle|p10:first-name]] put Life360 on it in January. DPR: removed [[2/2|date:month/day only]].]
6.4 Each child may call the other parent nightly between 7:00 and 7:30 p.m.

7. HEALTH CARE
7.1 Pediatrician: [[Dr. Farida Nazari|p8:full:full name with title]], [[Laporte Avenue Pediatric Group|o5:full]], [[970-555-0152|phone]]. Records portal invitations to both parents.
7.2 Ezra: [[ADHD, combined type|health:diagnosis of a child]] (dx 2022), takes [[methylphenidate ER 27 mg|health:medication and dose]] each school morning; [[severe peanut allergy|health:allergy]] - an epinephrine auto-injector travels in his backpack and each home keeps a second. He sees [[Corbin Ellsworth, LPC|p9:full:full name with credential]], every other Tuesday; neither parent will ask [[Mr. Ellsworth|p9:title-surname]] to testify.
7.3 Tovah: [[amblyopia (left eye)|health:diagnosis of a child]], patching two hours daily per ophthalmology; [[celiac disease|health:diagnosis of a child]], strict gluten-free diet in both homes. [SRL: the [[Dec. 6|date:abbreviated month and day]] pizza incident CANNOT happen again. DPR: disputed, it was a GF crust.]
7.4 Insurance: Father carries both children on his employer plan through [[Horsetooth Employees Benefit Trust|o11:full]], member IDs [[HEB-4471902-03|rec:health plan member ID]] and [[HEB-4471902-04|rec:health plan member ID]], group [[00812|rec!:group number, bare digits]]. Mother carries dental through her employer, subscriber no. [[D-2209417|rec:dental subscriber number]].
7.5 Uninsured costs over [[$250|money]] per child per year are split 58/42. Ezra's orthodontia estimate is [[$5,600|money]]; first payment of [[$1,400|money]] is due [[April 15, 2026|date:payment due date]].

8. CHILD SUPPORT AND EXPENSES (summary only; see Support Order)
8.1 Father pays Mother [[$1,140|money]] per month through the Family Support Registry, FSR account [[14-0771-9052|rec:support registry account number]], beginning [[May 1, 2026|date]]. Worksheet A incomes: Father [[$8,917/mo|money:monthly income]]; Mother [[$6,450/mo|money:monthly income]].
8.2 Extracurriculars agreed in writing are split 58/42: Ezra's hockey with [[NoCo Junior Eagles Hockey Club|o10:full]] ([[$1,850|money]] for 2026-27, plus about [[six hundred dollars|money:amount in words]] in gear); Tovah's gymnastics ([[$95/month|money:monthly amount]]).
8.3 Reimbursements within 30 days by transfer to the requesting parent: Mother's account at [[Cache la Poudre Bank & Trust|o12:full]] ending [[2207|acct:last four only]] (routing [[080646633|rtn]]); Father by Venmo, [[@dec-rafferty-915|cred:payment app handle]].
8.4 College savings: each child has a CollegeInvest 529 account owned by Mother (Ezra [[CI-55081724|acct:529 plan account number]]; Tovah [[CI-55081730|acct:529 plan account number]]). Father contributes [[$100|money]] per month to each.

9. TAXES AND DOCUMENTS
9.1 Mother claims Tovah every year; Father claims Ezra in any year he is current on support (IRS Form 8332 as needed).
9.2 The children's SSNs are on file with counsel (Ezra [[xxx-xx-4417|ssn:masked SSN]]; Tovah [[xxx-xx-9082|ssn:masked SSN]]) and will not appear in any filed document, per C.R.C.P. 121.
9.3 Passports: Mother holds both (Ezra no. [[671204418|govid:passport number]], exp. [[08/2029|date:month and year only]]; Tovah no. [[A41820937|govid:passport number]]). Neither parent travels abroad with a child without 30 days' written notice and an itinerary. Father's trip to see [[his brother Colm|indirect:family relationship to a named person]] in [[Cork|place!:city abroad that is also a common word]] ([[July 11-25, 2026|date:date range]]) is approved.

10. RELOCATION AND DISPUTES
10.1 Neither parent moves the children's residence outside [[Larimer County|place:county]] or [[Weld County|place:county]] without written agreement or court order (C.R.S. § 14-10-129).
10.2 Mediation first: three hours with the mediator used on 3/24 before any motion, cost split equally, except in an emergency.

11. OTHER OPEN ITEMS
- Father's [[DUI from 2019|attr:criminal history]] (Weld County [[19T2204|rec!:traffic case number]], deferred, completed): Mother wants an ignition-interlock clause; Father refuses. [NF: PRE report p. 14 finds no current concern; suggest a no-alcohol-while-parenting clause both ways.]
- Mother's request that Brielle not administer Ezra's medication. PRE silent.
- Mother disclosed in mediation that she has been treated for [[postpartum-onset anxiety|health:mental health diagnosis]] since 2019 and takes [[sertraline|health:medication]]; Father agrees this is not to be raised in the Plan.
- [[Colm|p13:first-name]]'s address in Cork for the itinerary: still needed from [[Mr. Zwick|p6:title-surname]].

SIGNATURES
_______________ [[Shoshana R. Lindenbaum|p1:full]], Petitioner          _______________ [[Declan P. Rafferty|p2:full]], Co-Petitioner

Approved as to form:
[[Nanami Fujikawa|p5:full]], Reg. No. [[51877|govid!:attorney registration number, bare digits]], [[Fujikawa Family Law LLC|o1:full]], [[123 N College Ave Ste 310|addr:street with suite]], Fort Collins CO [[80524|zip]], [[nanami@fujikawafamilylaw.example|email]], [[970-555-0105|phone]]
[[Garrett Zwick|p6:full]], Reg. No. [[39046|govid!:attorney registration number, bare digits]], [[Zwick & Brandvold, P.C.|o2:full]], [[gzwick@zwickbrandvold.example|email]]
'''))
