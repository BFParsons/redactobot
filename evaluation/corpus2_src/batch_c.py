from corpus2_src.core import D, dt, amt, num

DOCS = []
BATCH_COMMON = ["inventory", "assets", "liabilities", "household", "law", "society", "real", "social", "full",
                "landlord", "administration", "authorization", "health", "school", "counted", "self", "half",
                "undivided", "barrister", "solicitor", "jewellery", "property", "estimated", "monthly", "annual",
                "vendor", "paid", "method", "routing", "status", "prepared", "street", "student", "grade", "room",
                "balances", "bankruptcy", "bought", "business", "cash", "collection", "food", "housing", "interview",
                "interviewer", "joint", "lawsuits", "limit", "loan", "login", "owes", "propose", "revisit", "security",
                "shop", "transfers", "trusts", "vehicle", "vehicles", "weekly", "worth", "identity", "living", "things",
                "owed", "asks", "never", "foreign", "investment", "estate", "application", "applicants", "besides",
                "bond", "guardians", "guardianship", "hearing", "paternity", "suitability", "survivor", "probate",
                "conference", "confirmation", "coordinator", "everything", "flights", "fare", "frequent", "front",
                "hotel", "known", "passport", "rate", "seat", "show", "travel", "traveler", "arrangement", "backup",
                "chart", "cleared", "crown", "dentist", "extraction", "financial", "findings", "medical", "pre",
                "procedure", "responsible", "root", "scaling", "staff", "treatment", "tooth", "compliance", "content",
                "custodian", "deposits", "device", "legal", "ordered", "produce", "process", "production", "subpoena",
                "subscriber", "tenant", "unit", "arranged", "collected", "fine", "gala", "gift", "gifts", "given",
                "instrument", "letters", "loose", "mail", "money", "source", "appraised", "basis", "careful",
                "citizenship", "donor", "extension", "lifetime", "points", "preparer", "present", "pro", "quitclaim",
                "securities", "taxable", "widower", "act", "road", "juvenile"]

# ---------------------------------------------------------------- 221
DOCS.append(D(221, "pdf", "probate inventory", "legal", "CA",
  title="Estate inventory of assets and liabilities - working draft",
  ents={"p1": "Agnes Rosalind Thackeray", "p2": "Callum J. Thackeray", "p3": "Fiona Gillespie",
        "p4": "Desmond Thackeray", "p5": "Margaux Lachance", "p6": "Jasbir K. Sidhu", "p7": "Odile Lachance", "p8": "Dr. Brandvold",
        "o1": "Saltspring Wills & Estates Law Corporation", "o2": "Arbutus Coast Credit Union",
        "o3": "Dominion Maritime Bank", "o4": "Shannonside Bank", "o5": "Larchwood Securities Inc.",
        "o6": "Lochside Manor", "o7": "Haywood & Stroud Funeral Chapel", "o8": "St. Columba's Anglican Church",
        "o9": "Peninsula Seniors' Hospice Society", "o10": "Garry Oak Appraisals Ltd."},
  distractors=["Form P10", "Wills, Estates and Succession Act", "Rule 25-3", "ICBC", "BC Assessment", "RRIF", "TFSA",
               "Supreme Court of"],
  ok=["2024", "2019", "1998", "2021", "2014", "T1", "50%", "25%", "17-ft", "I", "II", "III", "IV", "V", "Canada Revenue Agency",
      "Subaru Forester", "Ireland", "Deceased", "Estate", "Part", "Visa", "Registry", "Black", "OF", "PID"],
  body=r'''
# [[Saltspring Wills & Estates Law Corporation|o1:full]]
[[204 - 1127 Fort Street|addr:unit-first Canadian address]], [[Victoria|place:city]], [[BC|place:province abbreviation]] [[V8V 3K9|zip:Canadian postal code]] · Tel [[250-555-0116|phone]] · Fax [[250-555-0117|phone:fax]]
Our file: [[24-0388/JKS|rec:firm file number]] — PRIVILEGED AND CONFIDENTIAL — working draft, not yet sworn
## INVENTORY OF ASSETS AND LIABILITIES (to be exhibited to the Form P10 affidavit)
Estate of [[AGNES ROSALIND THACKERAY|p1:caps:name in caption]], also known as [[Nessa Thackeray|p1:nickname:also-known-as name]], late of [[Sidney|place:town]], [[British Columbia|place:province]] (the "Deceased")
Supreme Court of British Columbia, Victoria Registry, No. [[VIC-P-24-1187|rec:probate file number]]. Prepared under the Wills, Estates and Succession Act and Rule 25-3.
The Deceased was born on [[3 June 1929|dob:day month year]] in [[Leeds|place:city abroad]] and died at [[Lochside Manor|o6:full]] on [[11 February 2024|date:date of death]], aged [[94|age:bare age]]. Social insurance number [[599 329 059|taxid:SIN with spaces]]. Her last will is dated [[19 September 2011|date:will date]], with one codicil dated [[4 May 2019|date:codicil date]]. The executors are her nephew [[Callum J. Thackeray|p2:full]] of [[Nanaimo|place:city]] and [[Fiona Gillespie|p3:full]], [[the Deceased's next-door neighbour of thirty years|indirect:relationship to the deceased]].
## Part I — Real property
- [[2281 Amelia Avenue|addr]], Sidney, BC [[V8L 2H6|zip:Canadian postal code]]. PID [[004-918-227|rec:land title parcel identifier]]. 2024 BC Assessment value [[C$1,148,000|money:Canadian dollar prefix]]; appraised by [[Garry Oak Appraisals Ltd.|o10:full]] at [[$1,205,000|money]] as of the date of death.
- PID [[017-442-906|rec:land title parcel identifier]]: undivided one-half interest in a recreational lot on [[Mayne Island|place:island]], held with [[her late brother's estate|indirect:co-owner identified by relationship]]. Half interest: [[$212,500|money]].
## Part II — Accounts and investments
- [[Arbutus Coast Credit Union|o2:full]], Sidney branch (transit [[04810|rtn:Canadian transit number]], institution [[809|rtn:Canadian institution number]]): chequing [[1004-883-21|acct]], balance [[$18,342.17|money]]; term deposit [[TD-7702915|acct:term deposit number]], [[$85,000.00|money]], matures [[30 Nov 2024|date:maturity date]].
- [[Dominion Maritime Bank|o3:full]], routing [[00270-614|rtn:Canadian transit and institution number]], savings account [[5530 118 947|acct:account number with spaces]]: [[$46,910.55|money]].
- [[Shannonside Bank|o4:full]], [[Limerick|place:city abroad]], Ireland — an account left to her by her late husband [[Desmond Thackeray|p4:full]] (d. 1998) and never closed. IBAN [[IE86 AIBK 6006 4571 1882 84|iban:IBAN in groups of four]], BIC [[SHNNIE2LXXX|acct:BIC / SWIFT code]]. Balance [[€9,418.03|money:euro amount]], roughly [[C$13,850|money:Canadian dollar prefix]].
- RRIF with [[Larchwood Securities Inc.|o5:full]], account [[77-QK41-9|acct:brokerage account]]: [[$203,774.60|money]]. Callum is the designated beneficiary, so this passes outside the estate.
- TFSA with [[Larchwood|o5:short]], account [[77-QK42-6|acct:brokerage account]]: [[$61,208.11|money]]. No designation on file.
## Part III — Personal property
- 2014 Subaru Forester, VIN [[JF2SJADC5EH417726|veh:VIN]], BC plate [[KR4 82T|veh:licence plate with a space]], insured through ICBC. Black book value [[$9,800|money]].
- 17-ft aluminium boat "[[Sea Thrift|indirect:named boat]]", hull no. [[QBC41877K213|veh:hull identification number]], and trailer: [[$3,500|money]].
- Jewellery, including a sapphire ring appraised at [[$6,400|money]], and [[her late husband's RCAF service medals|indirect:distinctive personal property]].
- Household contents, estimated: [[$4,000|money]]. [[Mr. Thackeray|p2:title-surname]] says [[Aunt Nessa|p1:nickname:family nickname]] kept [[about four thousand dollars|money:amount in words]] in cash in a biscuit tin. Not yet located.
## Part IV — Liabilities
- Lochside Manor, final account, invoice [[LM-24-02219|rec:invoice number]]: [[$7,912.40|money]].
- [[Haywood & Stroud Funeral Chapel|o7:full]]: [[$11,280.00|money]], paid by Callum on his own Visa on [[Feb. 20|date:abbreviated date without year]]; to be reimbursed.
- Canada Revenue Agency, terminal T1 return, estimate only: [[$38,000|money]].
## Part V — Beneficiaries
- [[Callum Thackeray|p2:short:name without middle initial]] — 50% of residue.
- [[Margaux Lachance|p5:full]], [[the Deceased's great-niece|indirect:relationship to the deceased]], of [[Gatineau|place:city]], [[QC|place:province abbreviation]] — 25% of residue.
- [[Peninsula Seniors' Hospice Society|o9:full]] — 25% of residue.
- [[St. Columba's Anglican Church|o8:full]], Sidney — legacy of [[$25,000|money]]. The Deceased was [[a lifelong Anglican|attr:religion]] and sang in the choir there.
- [[Ms. Gillespie|p3:title-surname]] — the Mayne Island interest (specific gift under the codicil).
## Notes to file
The Deceased was diagnosed with [[vascular dementia|health:diagnosis]] in 2021 and moved to [[Lochside|o6:short]] that autumn. [[Margaux|p5:first-name]]'s mother, [[Odile Lachance|p7:full]], has hinted she may question capacity for the 2019 codicil. Ask [[Dr. Brandvold|p8:title-surname]]'s office for the chart before we swear anything.
- [[819-555-0138|phone]] is [[Odile|p7:first-name]]'s number; she phoned twice last week and wants a copy of the will.
Ms. Gillespie prefers email ([[fiona.gillespie@mailhaven.example|email]]) or her mobile, [[250 555 0171|phone:spaces only]]. [[Callum|p2:first-name]] is at sea until [[the 28th|date:day of month only]]; use [[cjthackeray@tidewrack.example|email]].
[[Jasbir K. Sidhu|p6:full]], Barrister & Solicitor (Law Society of BC no. [[512907|govid:law society number]]) — [[JKS|p6:initials]], [[March 6, 2024|date:draft date]]
'''))

# ---------------------------------------------------------------- 222
DOCS.append(D(222, "xlsx", "vendor W-9 and 1099 tracking sheet", "accounting", "US",
  title="Vendor W-9 and 1099 tracking workbook, tax year 2025",
  ents={"p1": "Dariusz Kozak", "p2": "Truong Lan Anh", "p3": "Marisela Trujillo", "p4": "Ibrahim Abdullah",
        "p5": "Eszter Molnar", "p6": "Noelle Hartigan", "p7": "Royce Pettigrew",
        "o1": "Bramblewood Cabinetry, Inc.", "o2": "Kozak Finish Carpentry", "o3": "Lan's Upholstery",
        "o4": "Greaves Mill Supply LLC", "o5": "Pettigrew & Nakashima, CPAs", "o6": "IA Delivery",
        "o7": "Sandpiper Logistics Group, Inc.", "o8": "Buckeye Commons Credit Union", "o9": "Dayton Mercantile Bank"},
  distractors=["1099-NEC", "1099-MISC", "Form 945", "Box 1", "CP2100A", "Form W-8BEN"],
  ok=["2025", "2024", "24%", "W-9", "ACH", "ST", "DBA", "TIN", "Individual", "Corp", "Rent", "Withheld", "Memo",
      "Payer", "Ref", "City", "$600", "C", "S", "Classification", "Partnership", "Goods", "Freight", "LLC",
      "1099", "Reportable", "Yes", "No", "TOTAL", "2nd", "B", "Dec", "Jun", "Nov", "ID", "LTL"],
  sheets=[
    ("Vendors", [
      ["Vendor ID", "Name on W-9", "DBA", "Classification", "TIN type", "TIN", "W-9 on file", "Street", "City", "ST", "ZIP",
       "Email", "Phone", "Method", "Bank", "Routing", "Account", "Notes"],
      ["[[V-0112|rec:vendor ID]]", "[[Kozak, Dariusz|p1:last-first]]", "[[Kozak Finish Carpentry|o2:full]]", "Individual", "SSN",
       "[[805-52-6199|ssn]]", dt("2023-01-09", "mm/dd/yyyy", "date:W-9 date"), "[[418 Larkmoor Lane|addr]]", "[[Dayton|place:city]]",
       "[[OH|place:state abbreviation]]", "[[45419|zip]]", "[[dariusz@kozakfinish.example|email]]", "[[(937) 555-0127|phone]]", "ACH",
       "[[Buckeye Commons Credit Union|o8:full]]", "[[040829982|rtn]]", "[[7781204456|acct]]",
       "CP2100A B-notice rec'd; backup withholding 24% from [[6/1|date:month/day only]] until new W-9"],
      ["[[V-0118|rec:vendor ID]]", "[[Truong Lan Anh|p2:full:family name first]]", "[[Lan's Upholstery|o3:full]]", "Individual", "ITIN",
       "[[947-78-3310|taxid:ITIN]]", dt("2024-05-20", "mm/dd/yyyy", "date:W-9 date"), "[[2206 Wayne Ave Apt 4C|addr:street with apartment]]", "Dayton",
       "OH", "[[45410|zip]]", "[[lan.upholstery@postbox.example|email]]", "[[937.555.0169|phone:dotted]]", "Check", "", "", "",
       "ITIN renewal letter seen. Asked about Form W-8BEN - not needed, [[resident alien for tax purposes|attr:immigration / tax residency status]]"],
      ["[[V-0121|rec:vendor ID]]", "[[Greaves Mill Supply LLC|o4:full]]", "", "LLC - S", "EIN",
       "[[31-2087745|taxid:EIN]]", dt("2022-08-02", "mm/dd/yyyy", "date:W-9 date"), "[[9100 Old Troy Pike|addr]]", "[[Huber Heights|place:city]]",
       "OH", "[[45424-3310|zip:ZIP+4]]", "[[ar@greavesmill.example|email]]", "[[937-555-0102 x6|phone:with extension]]", "ACH",
       "[[Dayton Mercantile Bank|o9:full]]", "[[066748801|rtn]]", "[[000419 77302|acct:account number with a space]]", "Goods only"],
      ["[[V-0125|rec:vendor ID]]", "[[Marisela Trujillo|p3:full]]", "", "Individual", "SSN",
       num(372051552, "ssn:SSN stored as a number"), dt("2025-03-31", "mm/dd/yyyy", "date:W-9 date"), "[[77 Shroyer Rd|addr]]", "[[Oakwood|place:city]]",
       "OH", num(45419, "zip:ZIP stored as a number"), "", "[[937 555 0190|phone:spaces only]]", "Check", "", "", "",
       "W-9 unsigned - redo. [[Marisela|p3:first-name]] is [[Noelle's sister-in-law|indirect:relationship to the bookkeeper]] (disclose?)"],
      ["[[V-0130|rec:vendor ID]]", "[[Pettigrew & Nakashima, CPAs|o5:full]]", "", "Partnership", "EIN",
       "[[34-1977302|taxid:EIN]]", dt("2021-11-15", "mm/dd/yyyy", "date:W-9 date"), "[[40 N. Ludlow St., Ste 900|addr:street with suite]]", "Dayton",
       "OH", "[[45402|zip]]", "[[royce@pettigrewnakashima.example|email]]", "[[937-555-0145|phone]]", "Check", "", "", "",
       "Contact [[Royce Pettigrew|p7:full]]"],
      ["[[V-0133|rec:vendor ID]]", "[[Ibrahim Abdullah|p4:full]]", "[[IA Delivery|o6:full]]", "Individual", "SSN",
       "[[XXX-XX-1856|ssn:masked SSN, capital X]]", dt("2025-06-18", "mm/dd/yyyy", "date:W-9 date"), "[[1530 Salem Avenue, Lot 22|addr:street with lot number]]", "Dayton",
       "OH", "[[45406|zip]]", "[[iadelivery@postbox.example|email]]", "[[9375550158|phone:no separators]]", "ACH",
       "Buckeye Commons Credit Union", "040829982", "[[...6037|acct:last four with ellipsis]]", "Full SSN in locked cabinet only"],
      ["[[V-0137|rec:vendor ID]]", "[[Sandpiper Logistics Group, Inc.|o7:full]]", "", "C Corp", "EIN",
       "[[82-0451193|taxid:EIN]]", dt("2024-01-04", "mm/dd/yyyy", "date:W-9 date"), "[[PO Box 5571|addr:PO Box]]", "[[Vandalia|place:city]]",
       "OH", "[[45377|zip]]", "[[billing@sandpiperlg.example|email]]", "[[800-555-0111|phone:toll-free]]", "ACH",
       "Dayton Mercantile Bank", "066748801", "[[2200915530|acct]]", "Freight - corp, no 1099"],
      ["[[V-0140|rec:vendor ID]]", "[[MOLNAR, ESZTER|p5:last-first:Last, First in ALL CAPS]]", "", "Individual", "SSN",
       "[[131 67 1769|ssn:SSN with spaces]]", dt("2024-12-02", "mm/dd/yyyy", "date:W-9 date"), "[[6 Peach Orchard Ct|addr]]", "[[Kettering|place:city]]",
       "OH", "[[45429|zip]]", "[[emolnar52@postbox.example|email]]", "", "Check", "", "", "Landlord, shop annex. Rent - 1099-MISC Box 1"],
    ]),
    ("2025 Payments", [
      ["Date", "Vendor", "Ref", "Amount", "Withheld", "Memo"],
      [dt("2025-01-17", "m/d/yy"), "[[Kozak|p1:surname]]", "ACH [[A-250117-03|rec:ACH trace reference]]", amt(4200.00), "", "trim install, [[Okeke|p8:surname]] kitchen"],
      [dt("2025-02-07", "m/d/yy"), "[[Lan|p2:first-name!:given name that is also a common word]]", "ck [[10482|rec!:check number]]", amt(1150.00), "", "banquette recover"],
      [dt("2025-02-21", "m/d/yy"), "[[Greaves Mill|o4:short]]", "ACH [[A-250221-01|rec:ACH trace reference]]", amt(12480.75), "", "inv [[GM-88213|rec:invoice number]] maple + ply"],
      [dt("2025-03-14", "m/d/yy"), "Kozak", "ACH [[A-250314-02|rec:ACH trace reference]]", amt(6850.00), "", ""],
      [dt("2025-03-28", "m/d/yy"), "[[P&N|o5:acronym]]", "ck [[10497|rec!:check number]]", amt(2400.00), "", "2024 return + payroll reports"],
      [dt("2025-04-04", "m/d/yy"), "[[M. Trujillo|p3:short:initial + surname]]", "ck [[10501|rec!:check number]]", amt(560.00), "", "showroom cleaning - under $600"],
      [dt("2025-05-09", "m/d/yy"), "Lan", "ck [[10519|rec!:check number]]", amt(780.00), "", ""],
      [dt("2025-06-20", "m/d/yy"), "Kozak", "ACH [[A-250620-01|rec:ACH trace reference]]", amt(3975.50), amt(954.12), "backup w/h - goes on Form 945"],
      [dt("2025-07-11", "m/d/yy"), "[[Ibrahim|p4:first-name]]", "ACH [[A-250711-04|rec:ACH trace reference]]", amt(925.00), "", "deliveries Jun"],
      [dt("2025-08-15", "m/d/yy"), "Greaves Mill", "ACH [[A-250815-01|rec:ACH trace reference]]", amt(9310.00), "", "inv [[GM-90177|rec:invoice number]]"],
      [dt("2025-09-05", "m/d/yy"), "Ibrahim", "ACH [[A-250905-02|rec:ACH trace reference]]", amt(1310.00), "", ""],
      [dt("2025-10-03", "m/d/yy"), "[[Sandpiper|o7:short]]", "ACH [[A-251003-01|rec:ACH trace reference]]", amt(3600.00), "", "LTL to [[Lexington|place:city]] job"],
      [dt("2025-11-14", "m/d/yy"), "[[E. Molnar|p5:short:initial + surname]]", "ck [[10566|rec!:check number]]", amt(2750.00), "", "annex rent Nov"],
      [dt("2025-12-12", "m/d/yy"), "E. Molnar", "ck [[10581|rec!:check number]]", amt(2750.00, "usd", None), "", "annex rent Dec; she asked us to mail to her daughter's in [[Xenia|place:city]]"],
    ]),
    ("Summary", [
      ["Payer", "[[Bramblewood Cabinetry, Inc.|o1:full]]", "EIN", "[[31-1544098|taxid:EIN]]", "Prepared", "[[Noelle Hartigan|p6:full]]", dt("2026-01-12", "mmmm d, yyyy", "date:preparation date")],
      ["Vendor", "Paid 2025", "Withheld", "Reportable", "Form", "Status"],
      ["[[Dariusz Kozak|p1:full]]", amt(15025.50, "acct"), amt(954.12, "acct", None), "Yes", "1099-NEC", "TIN mismatch - 2nd B-notice due [[1/31|date:month/day only]]"],
      ["Truong Lan Anh", amt(1930.00, "acct"), "", "Yes", "1099-NEC", "ok"],
      ["Greaves Mill Supply LLC", amt(21790.75, "acct"), "", "No", "", "goods"],
      ["Marisela Trujillo", amt(560.00, "acct", None), "", "No", "", "under $600"],
      ["Pettigrew & Nakashima, CPAs", amt(2400.00, "acct", None), "", "Yes", "1099-NEC", "ok"],
      ["Ibrahim Abdullah", amt(2235.00, "acct"), "", "Yes", "1099-NEC", "ok"],
      ["Sandpiper Logistics Group, Inc.", amt(3600.00, "acct", None), "", "No", "", "C Corp"],
      ["[[Eszter Molnar|p5:full]]", amt(5500.00, "acct"), "", "Yes", "1099-MISC", "ok"],
      ["TOTAL", amt(53041.25, "acct"), "", "", "", "e-file by [[Feb 2|date:abbreviated date without year]]; [[Noelle|p6:first-name]] to send copies to [[Mr. Okeke|p8:title-surname]]"],
    ]),
  ]))
DOCS[-1]["ents"]["p8"] = "Chidubem Okeke"

# ---------------------------------------------------------------- 223
DOCS.append(D(223, "docx", "school medication authorization", "health", "US",
  title="Authorization for medication administration at school",
  ents={"p1": "Mateo Espinoza-Kaur", "p2": "Gurpreet Kaur", "p3": "Rafael Espinoza", "p4": "Anjali Iyer",
        "p5": "Tamika Hinds", "p6": "Corinne Bellamy", "p7": "Anaya Espinoza-Kaur",
        "o1": "Fernhill Elementary School", "o2": "Quarry Creek Unified School District",
        "o3": "Thistledown Pediatric Group", "o4": "Kestrel Pharmacy", "o5": "Bluestem Health Plan",
        "o6": "Ridgeview Medical Center"},
  minors=["p1", "p7"],
  distractors=["Section 504", "Education Code § 49423", "Form HS-12", "EpiPen Jr", "ICD-10 J45.40", "Schedule II", "911"],
  ok=["2025-26", "1", "2", "4", "5", "12", "15", "20", "Route", "Dose", "Medication", "When",
      "Prescriber", "Nurse", "Storage", "Rx", "Lunch", "PE", "Emergency",
      "Give", "Do", "Call", "Teacher", "Inhaled", "Oral", "IM",
      "Lic", "Refill", "District", "Field", "Trip", "Benadryl", "AT", "DEA", "ID", "RN"],
  footer="[[Quarry Creek Unified School District|o2:full]] · Form HS-12 (rev. 2025-26) · Student ID [[60044817|rec:student ID]] · CONFIDENTIAL HEALTH RECORD",
  body=r'''
# AUTHORIZATION FOR MEDICATION ADMINISTRATION AT SCHOOL
School year 2025-26 · [[Fernhill Elementary School|o1:full]] · Health Office fax [[(530) 555-0193|phone:fax]]
Required by Education Code § 49423. A new form is needed each school year and whenever a dose changes.
## Student
Student: [[ESPINOZA-KAUR, Mateo|p1:last-first]] ("[[Teo|p1:nickname]]") · Date of birth: [[09/22/2016|dob]] · Grade 4 · Room 12 · Teacher: [[Ms. Bellamy|p6:title-surname]]
Home address: [[3317 Covey Run Court|addr]], [[Chico|place:city]], [[CA|place:state abbreviation]] [[95973|zip]]
Health plan: [[Bluestem Health Plan|o5:full]], member ID [[BHP-4471-20936-02|rec:health plan member ID]], group [[70318|rec!:group number]]
## Diagnoses and medications ordered
| Medication | Dose | Route | When |
| [[albuterol HFA 90 mcg|health:medication and dose]] | 2 puffs with spacer | Inhaled | 15 min before PE and recess; every 4 hrs as needed for wheeze |
| [[methylphenidate ER 18 mg|health:medication and dose]] | 1 tablet | Oral | 12:15 after Lunch |
| [[epinephrine auto-injector 0.15 mg|health:medication and dose]] | 1 injection | IM | At first sign of anaphylaxis, then Call 911 |
Diagnoses: [[moderate persistent asthma|health:diagnosis of a child]] (ICD-10 J45.40); [[ADHD, combined presentation|health:diagnosis of a child]]; [[peanut and tree-nut allergy|health:allergy]] with [[anaphylaxis in March 2024|health:medical event]]. No known drug allergies.
Self-carry: the student may carry and self-administer the inhaler. He may NOT carry the methylphenidate (Schedule II); it stays locked in the Health Office.
Storage and supply: the pharmacy label must match this order. Current fills are from [[Kestrel Pharmacy|o4:full]], [[East Avenue|place:street used as a location]] store: Rx [[7730418|rec!:prescription number]] (methylphenidate, filled [[8/11/25|date:numeric date with two-digit year]]) and Rx [[7730422|rec!:prescription number]] (EpiPen Jr two-pack, expires [[04/2026|date:month and year]]).
## Prescriber
[[Anjali Iyer, MD|p4:full:name with credential]] · [[Thistledown Pediatric Group|o3:full]] · [[1850 Bidwell Parkway, Suite 210|addr:street with suite]], Chico, CA [[95926|zip]]
Office [[530-555-0148|phone]] · after hours [[530-555-0149|phone]] · NPI [[1568204937|govid:NPI]] · DEA [[FI4482093|govid:DEA number]] · CA Lic. [[A 118562|govid:medical license number]]
Prescriber signature: /s/ [[A. Iyer|p4:short:initial + surname]] · Date: [[August 8, 2025|date:order date]]
## Parent/guardian
I ask that school staff give the medication above to my child as ordered and I allow the school nurse to talk with the prescriber and the pharmacy about it.
Mother: [[Gurpreet Kaur|p2:full]] · cell [[530.555.0162|phone:dotted]] · [[gkaur.rn@mailhaven.example|email]] · works nights at [[Ridgeview|o6:short]], so text first
Father: [[Rafael Espinoza|p3:full]] · cell [[(530) 555-0177|phone]] · work [[530-555-0105 ext. 31|phone:with extension]] · [[rafa.espinoza@quarrycreekfire.example|email]]
The parents are [[separated|attr:marital status]]; Teo is with his father on alternating weeks. Either parent may pick up medication. Sister [[Anaya|p7:first-name]] (Grade 1, Room 5) has no medications at school.
Signature: [[G. Kaur|p2:short:initial + surname]] · Date: [[8/12/2025|date:parent signature date]]
## Health Office use
Received and reviewed by [[Tamika Hinds, RN|p5:full:name with credential]], District Nurse (RN Lic. [[95088214|govid:nursing license number]]) on [[Aug. 14, 2025|date:abbreviated month]]. Section 504 plan updated the same day. Counted 20 tablets in; next Refill due about [[Sept. 9|date:abbreviated date without year]].
Emergency plan: Give epinephrine first. Do not give Benadryl instead. Call 911, then [[Mrs. Kaur|p2:title-surname]], then [[Mr. Espinoza|p3:title-surname]]. For a Field Trip, [[Corinne Bellamy|p6:full]] carries the red bag and has been trained ([[9/3/25|date:training date]]). Questions: [[thinds@qcusd.example|email]] or District Health Services, [[530-555-0100|phone]].
'''))

# ---------------------------------------------------------------- 224
DOCS.append(D(224, "txt", "collection information statement notes", "accounting", "US", length="long",
  title="Interview notes for Form 433-A collection information statement",
  ents={"p1": "Wendell T. Mackenzie", "p2": "Soledad Mercado-Mackenzie", "p3": "Itzel Mackenzie", "p4": "Dolores Mackenzie",
        "p5": "Katarzyna Novotny", "p6": "Tyler Mackenzie", "p7": "Darla (Wendell's cousin)", "p8": "R. Buchanan",
        "p9": "Brianna Brannock-Sayles",
        "o1": "Dovetail Tax Resolution Group", "o2": "Mackenzie Climate Services LLC", "o3": "Osprey Dental Arts, PC",
        "o4": "Ozark Heritage Bank", "o5": "Banco Olivar de Jaén", "o6": "Kingfisher Mechanical",
        "o7": "Lantern Mutual Life", "o8": "Show-Me Auto Credit", "o9": "Lamplight Home Loans",
        "o10": "Iglesia Nueva Esperanza", "o11": "Wilder Elementary", "o12": "Breathe Easy Medical Supply"},
  minors=["p3", "p6"], cardholders=["p1", "p2"],
  distractors=["Form 433-A", "Form 2848", "Form 9465", "Form 433-D", "Form 12153", "FinCEN Form 114", "Schedule C",
               "Notice LT11", "Chapter 13", "MOST 529", "IRC § 6330", "Zillow", "ResMed AirSense 10", "Form 1040-ES",
               "National Standards"],
  ok=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "14", "16", "30", "87", "1040s", "2004", "2016", "2019", "2020",
      "2021", "2022", "2023", "2024", "401(k)", "4th", "90%", "CAF", "CPAP", "DOR", "EA", "F-250", "Ford", "Grandma",
      "Green", "HELOC", "HVAC", "Honda", "ID", "IS", "Odyssey", "POA", "Q3", "RO"],
  body=r'''
[[DOVETAIL TAX RESOLUTION GROUP|o1:caps]]
Interview notes for Form 433-A (Collection Information Statement) -- these are NOT the form
Client file: [[DTR-2025-0719|rec:client file number]]        Interviewer: [[K. Novotny|p5:short:initial + surname]], EA (enrolled agent no. [[00118274-EA|govid:enrolled agent number]])
Interview: Tues [[10/14/25|date:numeric date with two-digit year]] at the clients' kitchen table, about 2 hrs. Follow-up call [[10/16|date:month/day only]].
POA: Form 2848 signed [[10/14|date:month/day only]], CAF no. [[0309-55718-R|govid:IRS CAF number]]

1. WHO
Taxpayer:  [[Wendell T. Mackenzie|p1:full]] (goes by "[[Wen|p1:nickname]]"), SSN [[303-67-7048|ssn]], DOB [[4/2/1978|dob:numeric without leading zeros]], cell [[417-555-0133|phone]]
Spouse:    [[Soledad Mercado-Mackenzie|p2:full]], SSN [[394-98-2113|ssn]], DOB [[11-19-1981|dob:dashes]], cell [[417.555.0156|phone:dotted]],
           [[soledad.mm@mailhaven.example|email]] (she handles all the paperwork; email her, not him)
Home:      [[1846 E. Catalpa Street|addr]], [[Springfield|place:city]], [[MO|place:state abbreviation]] [[65804|zip]] ([[Greene County|place:county]]). They own it, see 7.
Household of four. Daughter [[Itzel|p3:first-name]], 9, born [[7/30/2016|dob:numeric without leading zeros]], 4th grade at [[Wilder Elementary|o11:full]].
[[Wendell|p1:first-name]]'s mother, [[Dolores Mackenzie|p4:full]], 87, moved in during [[March 2024|date:month and year]] after [[a stroke|health:medical event]]. They claim her
as a dependent; her SSN ends [[6494|ssn:last four only]]. She gets Social Security of [[$1,388|money]] a month and puts [[$400|money]] of it toward groceries.

2. WHAT IS OWED
Balances per account transcripts I pulled [[10/10|date:month/day only]] (joint 1040s, all filed, none under audit):
   2021   [[$18,406.22|money]]
   2022   [[$27,913.80|money]]
   2023    [[$9,150.47|money]]     total [[$55,470.49|money]] with penalties and interest to date
[[Missouri|place:state]] DOR also wants [[$4,312|money]] for 2022. Not dealing with that yet; the state has not sent anything
since a billing notice in the spring and Soledad would rather keep the two apart.
Notice LT11 is dated [[Sept. 22, 2025|date:abbreviated month]]. The hearing request under IRC § 6330 has to be postmarked by [[Oct 22|date:abbreviated date without year]].
The case is already with a Revenue Officer: [[Ms. Buchanan|p8:title-surname]] ([[R. Buchanan|p8:full:initial + surname]] on the letter), employee ID [[1000482233|govid:IRS employee ID number]],
Springfield field office, [[417-555-0181|phone]], fax [[417-555-0182|phone:fax]]. She left a card in their door on [[9/30|date:month/day only]].
Identity protection PIN: Wendell's for this year is [[604237|cred:IRS identity protection PIN]]. [[Soledad|p2:first-name]] has never been issued one.
How it happened, in his words: the business took off in 2021 and he never raised his estimates. Then
[[his cousin Darla, who kept his books until last year|indirect:relationship and role]], "borrowed" [[about thirty-one thousand|money:amount in words]] out of the business
account over 14 months. He filed a police report ([[SPD 24-061187|rec:police report number]]) but will not press it because she is family.
[[Darla|p7:first-name]] has paid back [[$2,000|money]]. In early 2023 he was in hospital 9 days with [[pneumonia|health:diagnosis]] and lost most of a quarter.

3. WORK AND INCOME
Wendell is the sole member of [[Mackenzie Climate Services LLC|o2:full]] (EIN [[81-4470926|taxid:EIN]]), HVAC install and repair, disregarded,
reported on Schedule C. Shop: [[2750 W. Kearney St, Unit C|addr:street with unit]], Springfield [[65803|zip]]. Two employees, payroll deposits current.
   2024 gross receipts [[$412,880|money]]; net profit [[$96,300|money]]. Year to date through 9/30: [[71.4k|money!:shorthand k amount without currency sign]] net.
Soledad is a dental hygienist at [[Osprey Dental Arts, PC|o3:full]] ([[Dr. Brannock-Sayles|p9:title-surname]]'s office), there since [[Aug 2017|date:month and year of hire]],
[[$41.50|money:hourly rate]] an hour, about 30 hours a week. Employee no. [[ODA-0457|rec:employee ID]]. Gross [[$5,395|money]] a month, net [[$4,180.66|money]] direct-deposited
to the joint checking. No other income. No rental, no side work, no crypto.

4. BANK AND INVESTMENT ACCOUNTS
a) Joint checking, [[Ozark Heritage Bank|o4:full]], acct ending [[7719|acct:last four only]], average balance [[$2,140|money]].
b) Joint savings, same bank, [[xxxx-3302|acct:masked account, last four]]: [[$6,025.18|money]]. This is the property-tax money.
c) Business checking, [[Ozark Heritage|o4:short]], routing [[089044443|rtn]], acct [[4410 0287 615|acct:account number with spaces]]: [[$14,870|money]] on the day, but
   payroll of [[$9,200|money]] clears Friday.
d) FOREIGN ACCOUNT. Soledad inherited an account in [[Spain|place:country where an account is held]] from her father, who died in 2022.
   She did not think of it as hers and said so twice. Statements go to her aunt's address there.
   [[Banco Olivar de Jaén|o5:full]], IBAN [[ES97 4538 4530 5794 0918 9421|iban:IBAN in groups of four]], SWIFT [[BOJAESMMXXX|acct:BIC / SWIFT code]].
   Balance on the last statement: [[11.260,00 EUR|money:European number format with currency code]], call it [[$12,200|money]]. It has NEVER been reported.
   No FinCEN Form 114 for 2022, 2023 or 2024. Flag for [[Katarzyna|p5:first-name]]: fix this before anything goes to the RO.
e) Wen's 401(k) from his old job at [[Kingfisher Mechanical|o6:full]], plan acct [[KM-401-228841|acct:retirement plan account number]]: [[$38,700|money]] vested, with
   a [[$6,000|money]] loan against it.
f) Itzel's college account, MOST 529, acct [[6120045583|acct!:unlabelled-style account number without separators]]: [[$4,890|money]]. Grandma [[Dolores|p4:first-name]] put in most of it.
g) Term life on Wendell, [[Lantern Mutual Life|o7:full]], policy [[LML-T-20984417|rec:insurance policy number]]. No cash value.
h) Cash on hand: about [[$300|money]]. No safe deposit box.

5. CREDIT CARDS
   Visa (Ozark Heritage), in Wendell's name, ending [[4082|card:last four only]]. Limit [[$12,000|money]], owes [[$11,612.40|money]], minimum [[$290|money]].
   Mastercard in the name [[SOLEDAD MERCADO|p2:caps:maiden name as embossed on a card]] (never updated after the wedding). She read me the
      whole number before I could stop her: [[5599 9859 2200 1381|card:card number with spaces]], exp [[03/27|exp]]. Limit [[$8,500|money]],
      owes [[$7,944.09|money]], minimum [[$199|money]].
   Amex business card, embossed [[WENDELL T MACKENZIE|p1:caps:name as embossed on a card]], last five [[32853|card!:last five digits of an Amex]]. Owes [[$4,310|money]]; he pays it in full
      most months.
   A home-improvement store card was closed in 2024 with nothing owing.

6. VEHICLES
   2019 Ford F-250, VIN [[1FT7W2BT5KEC41907|veh:VIN]], MO plate [[7HK R42|veh:license plate with a space]]. 90% business. Loan with [[Show-Me Auto Credit|o8:full]],
      no. [[30-88127-4|rec:loan number]], balance [[$21,350|money]], payment [[$612|money]]. Worth maybe [[$34,000|money]].
   2016 Honda Odyssey, VIN [[5FNRL5H64GB072218|veh:VIN]], vanity plate [[ITZLMOM|veh!:vanity plate that hints at a family name]]. Paid off. Worth about [[$9,500|money]].
   2004 utility trailer, plate [[43T-9KD|veh:trailer plate]]. [[$1,200|money]] at most.

7. REAL ESTATE
   The [[Catalpa|place!:street name used as a location]] house. Bought [[June 2015|date:month and year]] for [[$189,000|money]]. Zillow says [[$262,000|money]]; I would use [[$250k|money:shorthand k amount]].
   County parcel no. [[88-12-27-304-019|rec:parcel number]].
   First mortgage: [[Lamplight Home Loans|o9:full]], loan [[0077418265|rec!:loan number without separators]], balance [[$141,772.63|money]], payment [[$1,318.44|money]] with escrow.
   HELOC with Ozark Heritage opened in 2022 to cover a payroll: [[$18,000|money]] drawn, interest-only [[$131|money]] a month.

8. MONTHLY LIVING EXPENSES (actual; compare to the National Standards later)
   Food, clothing, misc.            [[$1,950|money]]
   Housing and utilities            [[$2,285|money]]
   Vehicle operating                  [[$640|money]]
   Health insurance (marketplace)   [[$1,104|money]]
   Out-of-pocket health               [[$870|money]]   <- this is the number the RO will push on. Detail:
      - Itzel has [[juvenile idiopathic arthritis|health:diagnosis of a child]]. Weekly [[etanercept 25 mg|health:medication and dose]] injections, copay [[$350|money]] a month,
        plus a rheumatology visit in [[Kansas City|place:city]] every 8 weeks (gas and a motel, not counted above).
      - Dolores: [[post-stroke outpatient rehab|health:treatment]] and a home aide three mornings a week, [[$780|money]] a month. Her
        Social Security does not cover it. They pay the difference.
      - Wendell: [[severe obstructive sleep apnea|health:diagnosis]]. CPAP (ResMed AirSense 10, serial [[23192847715|dev:CPAP serial number]]) on a
        payment plan with [[Breathe Easy Medical Supply|o12:full]], [[$46|money]] a month, 11 payments left.
   Court-ordered child support        [[$525|money]]   Wendell's son [[Tyler|p6:first-name]], 16, from a relationship before the marriage.
        Tyler lives in [[Joplin|place:city]] with his mother. Case [[18GR-DR00412|rec:family court case number]]. Paid through the state, never late.
   Estimated tax payments             [[$500|money]]   ([[$1,500|money]] a quarter on Form 1040-ES, started with Q3)
   Not allowable but real: they [[tithe|attr:religious practice]] $400 a month to [[Iglesia Nueva Esperanza|o10:full]], [[Soledad's church|indirect:affiliation of a named person]].
        Wendell says that one is not up for discussion, with us or with the IRS.

9. OTHER THINGS THE FORM ASKS
   - Soledad is [[a Spanish citizen and a lawful permanent resident|attr:citizenship and immigration status]]. Green card renewed 2023, A-number
     [[A 208 771 465|govid:alien registration number with spaces]]. She is nervous about anything that goes to the government with her name on it.
   - Bankruptcy: Wendell filed [[a Chapter 13 in 2012, discharged in 2017|attr:bankruptcy history]], case no. [[12-60884|rec:bankruptcy case number]]. Before the marriage
     was two years old. Soledad was not a debtor.
   - Lawsuits: none. Trusts: none. Transfers in the last ten years: gave his old truck to [[Darla's boy|indirect:relationship to a named person]] in 2020.
   - He owns three hunting rifles, maybe [[fifteen hundred dollars|money:amount in words]] together. Left off unless asked.

10. PLAN
   File the hearing request (Form 12153) by fax on [[10/17|date:month/day only]]. Propose an installment agreement at [[$450|money]] a month
   (Form 9465 with a Form 433-D direct debit from the joint checking). Revisit an offer after the foreign
   account is cleaned up.
   Our fee: [[$2,500|money]] retainer, charged to Soledad's Mastercard at the table, approval code [[08812Z|rec!:card authorization code]].
   Documents go to [[https://vault.dovetailtax.example/u/mackenzie-0719|url:client upload link containing surname and file number]]. Login [[wmackenzie78|cred:username]], temporary password
   [[Catalpa!1846|cred:temporary password]] -- told him to change it tonight. He will not; ask Soledad.
   Next call: Mon [[Oct. 20|date:abbreviated date without year]], 4:30, with [[Mrs. Mackenzie|p2:title-surname]] only. -- [[KN|p5:initials]]
'''))

# ---------------------------------------------------------------- 225
DOCS.append(D(225, "pdf", "guardianship petition", "legal", "US",
  title="Application for appointment of guardians of a minor",
  ents={"p1": "Jaylen Amari Sorrell", "p2": "Bernice Sorrell", "p3": "Otis L. Sorrell", "p4": "Danielle Sorrell",
        "p5": "Marcus D. Tavares", "p6": "Leila Chowdhury", "p7": "Naoko Yamamoto", "p8": "Dr. Feinberg-Addo",
        "o1": "Marlowe Middle School", "o2": "Scioto Valley Savings Bank", "o3": "Chowdhury & Rosenthal Co., LPA",
        "o4": "Olentangy Children's Neurology", "o5": "Mount Calvary AME Church"},
  minors=["p1"],
  distractors=["R.C. 2111.02", "Form 16.0", "Sup.R. 66", "Social Security Administration",
               "Ohio Transfers to Minors Act", "Children's Health Insurance Program"],
  ok=["1", "2", "3", "4", "5", "6", "7", "8", "9", "2019", "EEG", "IN", "OF", "Reg", "Sup"],
  body=r'''
# PROBATE COURT OF [[FRANKLIN COUNTY|place:county in a caps court heading]], [[OHIO|place:state in a caps court heading]]
IN THE MATTER OF THE GUARDIANSHIP OF [[JAYLEN AMARI SORRELL|p1:caps:name in caption]], A MINOR
Case No. [[25-GM-004471|rec:probate case number]] · Judge: unassigned
## APPLICATION FOR APPOINTMENT OF GUARDIANS OF MINOR (Form 16.0) — DRAFT 2, for client review
1. Applicants. [[Bernice Sorrell|p2:full]] and [[Otis L. Sorrell|p3:full]], husband and wife, of [[1422 Bryden Road|addr]], [[Columbus|place:city]], [[Ohio|place:state]] [[43205|zip]], apply under R.C. 2111.02 to be appointed co-guardians of the person and estate of their grandson. [[Mrs. Sorrell|p2:title-surname]] is a retired school cook. [[Mr. Sorrell|p3:title-surname]] drives for the transit authority and is [[a steward in his union local|attr:union role]]. Telephone [[(614) 555-0152|phone]]; [[bernice.sorrell@postbox.example|email]].
2. The minor. [[Jaylen Amari Sorrell|p1:full]] was born on [[February 9, 2014|dob]] and is eleven years old. The last four digits of his Social Security number are [[9148|ssn:last four only]]. He has lived with the applicants at the [[Bryden Road|place!:street used as a location]] address since [[July 2023|date:month and year]]. He is in the sixth grade at [[Marlowe Middle School|o1:full]], where his counselor is [[Naoko Yamamoto|p7:full]].
3. The mother. [[Danielle Sorrell|p4:full]], the applicants' daughter, died on [[June 27, 2023|date:date of death]] in Columbus. The death certificate lists [[accidental fentanyl toxicity|health:cause of death]]. A certified copy is attached as Exhibit A.
4. The father. [[Marcus D. Tavares|p5:full]] is [[serving a sentence at the Lebanon Correctional Institution|attr:incarceration]], inmate no. [[A784-512|govid:inmate number]], with an earliest release date of [[10/2031|date:month and year]]. Paternity was established in [[Franklin County|place:county]] Juvenile Court case [[14-JU-09-11846|rec:juvenile court case number]]. [[Mr. Tavares|p5:title-surname]] has been served and has signed a waiver and consent dated [[3/18/2025|date:consent date]]. He has not paid support since 2019; arrears stand at [[$23,611.40|money]].
5. Why a guardianship is needed. The applicants cannot enrol [[Jaylen|p1:first-name]] in the Children's Health Insurance Program, consent to his treatment or manage his money without letters of guardianship. Jaylen has [[childhood absence epilepsy|health:diagnosis of a child]] and takes [[ethosuximide 250 mg twice a day|health:medication and dose]]. He is followed by [[Dr. Feinberg-Addo|p8:title-surname]] at [[Olentangy Children's Neurology|o4:full]], which now refuses to schedule his EEG without a legal guardian's signature. Since his mother's death he has also seen a [[grief counselor weekly|health:mental health treatment]].
6. The minor's estate. (a) Survivor benefits from the Social Security Administration of [[$1,046.00|money]] a month, paid to Mrs. Sorrell as representative payee. (b) A custodial account under the Ohio Transfers to Minors Act at [[Scioto Valley Savings Bank|o2:full]], account [[30-4471-88206|acct]], holding [[$17,340.92|money]] from his mother's life insurance. (c) An expected share, not more than [[$40,000|money]], of a wrongful-death settlement now being negotiated. Total personal property: about [[$57,300|money]]. No real estate.
7. Next of kin. Besides the father: paternal grandmother [[Rosa Tavares|p9:full]], [[Dayton|place:city]], address unknown. No siblings.
8. Suitability. Neither applicant has been convicted of any offense. Background checks under Sup.R. 66 were run on [[April 2, 2025|date:background check date]]. The family attends [[Mount Calvary AME Church|o5:full]], and [[the pastor|indirect:unique role]] has offered a letter.
9. Bond. The applicants ask that bond be set at [[$35,000|money]] or dispensed with while the funds stay in the restricted account.
Respectfully submitted,
[[Leila Chowdhury|p6:full]] (Sup. Ct. Reg. No. [[0098417|govid:attorney registration number]])
[[Chowdhury & Rosenthal Co., LPA|o3:full]]
[[88 East Gay Street, 11th Floor|addr:street with floor]], Columbus, [[OH|place:state abbreviation]] [[43215-3107|zip:ZIP+4]]
Tel. [[614-555-0119|phone]] · [[lchowdhury@chowdhuryrosenthal.example|email]]
Our ref. [[SOR-G-25-031|rec:firm matter number]]
Note to [[Bernice|p2:first-name]]: please check paragraph 4. [[Otis|p3:first-name]] told me the consent was signed "[[the 18th|date:day of month only]]" but the notary stamp is hard to read. Hearing will likely be set for [[the week of May 12|date:approximate date]]. — [[LC|p6:initials]]
'''))
DOCS[-1]["ents"]["p9"] = "Rosa Tavares"

# ---------------------------------------------------------------- 226
DOCS.append(D(226, "eml", "travel booking and expense email", "general", "US", enc="qp",
  title="Travel booking details and expense follow-up for a conference trip",
  ents={"p1": "Renata Kovac", "p2": "Samuel Oduya", "p3": "Ifeoma Oduya", "p4": "Duarte Horvat",
        "o1": "Vantage Point Surveying, Inc.", "o2": "Alfama Miradouro Hotel", "o3": "Banco Ribeira do Tejo",
        "o4": "Wayfarer Corporate Travel"},
  cardholders=["p1"],
  distractors=["TSA PreCheck", "Global Entry", "Mastercard", "FIG Working Week", "Concur", "Per diem"],
  ok=["0600", "1", "2", "3", "5", "23C", "June", "2025"],
  headers={"From": "[[Renata Kovac|p1:full]] <[[rkovac@vantagepointsurvey.example|email]]>",
           "To": "[[Samuel Oduya|p2:full]] <[[soduya@vantagepointsurvey.example|email]]>",
           "Cc": "[[bookings@wayfarercorp.example|email:shared mailbox]]",
           "Subject": "Lisbon - your bookings, and the hotel refund (need 2 things from you)",
           "Date": "Thu, [[16 Apr 2026|date:email date]] 16:42:10 -0600"},
  body=r'''
[[Sam|p2:nickname]],

Everything for [[Lisbon|place:city abroad]] is ticketed. Details below so you have them in one place. Please don't forward this one, it has the card on it.

FLIGHTS (booked through [[Wayfarer Corporate Travel|o4:full]], agent [[Duarte Horvat|p4:full]], [[720-555-0114|phone]])
  Record locator [[QX7RLM|rec!:airline record locator]], e-ticket [[047 2218840963|rec:airline ticket number]]
  Sun [[10 May|date:day and month without year]]  [[DEN|place:airport code]]-[[EWR|place:airport code]]-[[LIS|place:airport code]], arrive Mon [[11 May|date:day and month without year]] 07:35. Seat 23C on the long leg.
  Sat [[16 May|date:day and month without year]]  LIS-EWR-DEN
  Fare [[$1,486.30|money]]. Name on the ticket is exactly as in your passport: [[ODUYA/SAMUEL CHUKWUEMEKA|p2:last-first:airline ticket format in ALL CAPS]].
  Passport [[A04418827|govid:passport number]], expires [[22 NOV 2031|date:passport expiry in caps]]. Date of birth on file [[14 AUG 1983|dob:day month year in caps]].
  Known Traveler Number [[TT9K41R7Z|govid:known traveler number]] is on the booking, so TSA PreCheck should print. Your Global Entry card number is not needed.
  Frequent flyer: I added [[MP-88 204 771|rec:frequent flyer number]].

HOTEL
  [[Alfama Miradouro Hotel|o2:full]], [[Rua das Escolas Gerais 41|addr:street address abroad]], [[1100-213|zip:Portuguese postal code]] Lisbon. 5 nights, in [[11 May 2026|date:check-in date]], out [[the 16th|date:day of month only]].
  Confirmation [[HAM-260511-7729|rec:hotel confirmation number]]. Rate [[€164,00|money:euro amount in continental format]] a night, city tax extra. Front desk [[+351 21 555 0164|phone:Portuguese number, international format]].

PAYMENT
  All of it is on the company Mastercard in my name:
     [[5122 3096 5238 7421|card:card number with spaces]]   exp [[09/28|exp]]   security code [[417|cvv]]
     billing ZIP [[80202|zip]]
  The hotel will ask to see the card at check-in. Show them this email and have them ring me on [[(303) 555-0186|phone]] if they refuse. Do NOT put the room on your own card again.

THE REFUND (this is what I need you for)
  Last year the [[Alfama|o2:short]] took the [[€492,00|money:euro amount in continental format]] deposit twice, once from the company card and once by transfer from your wife's account when the card was declined. They have finally agreed to send it back, but only to the account it came from. They need, in writing:
  1. Account holder: [[Ifeoma Oduya|p3:full]]
  2. IBAN: I have [[PT29 5473 7348 2822 1041 9695 4|iban:IBAN in groups of four]] at [[Banco Ribeira do Tejo|o3:full]] from the old receipt. Is that still open? [[Ifeoma|p3:first-name]] said she might have closed it when [[her mother's flat in Cascais was sold|indirect:family circumstances]].
  3. A signed line from her. Email is fine: [[reservas@alfamamiradouro.example|email]], quote the 2025 folio [[F-25-03318|rec:hotel folio number]].
  When it lands, tell me the amount in dollars so I can clear the open item (it was coded as [[$531.36|money]]).

EXPENSES
  Per diem is [[$92|money]] a day. Conference fee ([[$780.00|money]], FIG Working Week) is already paid. Receipts into Concur by [[May 29|date:deadline without year]], please, not June.

Also: [[Dr. Oduya|p2:title-surname]], the medical form you sent me by mistake ([[the one about the insulin pump|health:medical device use]]) is deleted. I did not open the attachment. You may want a doctor's letter for security at DEN.

[[Renata|p1:first-name]]

[[Renata Kovac|p1:full]] | Office & Travel Coordinator
[[Vantage Point Surveying, Inc.|o1:full]] | [[1701 Wynkoop Street, Suite 640|addr:street with suite]], [[Denver|place:city]], [[CO|place:state abbreviation]] 80202
direct [[303-555-0186|phone]] | [[https://travel.vantagepointsurvey.example/trips/LIS-0526-oduya|url:trip page link containing surname]]
'''))

# ---------------------------------------------------------------- 227
DOCS.append(D(227, "txt", "dental treatment plan and payment arrangement", "health", "US",
  title="Dental treatment plan with payment arrangement",
  ents={"p1": "Henrik Lindahl", "p2": "Annika Lindahl", "p3": "Mi-rae Cheung", "p4": "Jocelyn Ramos",
        "o1": "Greystone Family Dentistry", "o2": "Sterling Dental Benefit Plan", "o3": "Kittitas Farmers Bank"},
  cardholders=["p2"],
  distractors=["D2740", "D3330", "D4341", "D7140", "CareCredit", "Truth in Lending Act", "Visa"],
  ok=["#1", "#19", "#30", "1", "2", "3", "4", "2026", "5th", "ID", "LR", "UR", "x2"],
  body=r'''
[[GREYSTONE FAMILY DENTISTRY|o1:caps]]
[[612 N. Pearl St.|addr]], [[Ellensburg|place:city]], [[WA|place:state abbreviation]] [[98926|zip]]   ph [[509-555-0141|phone]]   [[frontdesk@greystonefamilydental.example|email]]

TREATMENT PLAN & FINANCIAL ARRANGEMENT                      printed [[01/22/2026|date:print date]]

Patient:  [[Lindahl, Henrik|p1:last-first]]     Chart # [[GF-11873|rec:patient chart number]]     DOB [[05/17/1957|dob]]
Responsible party:  [[Annika Lindahl|p2:full]] (spouse)     [[40 Thorp Prairie Rd|addr:rural road address]], [[Thorp|place:town]], WA [[98946|zip]]
Home [[509-555-0178|phone]]   her cell [[509 555 0123|phone:spaces only]]   [[annika.lindahl@mailhaven.example|email]]
Dentist:  [[Mi-rae Cheung, DDS|p3:full:name with credential]] (WA lic. [[DE60417733|govid:dental license number]])     Treatment coordinator: [[Jocelyn|p4:first-name]]

Medical alerts: [[type 2 diabetes, last A1c 8.1|health:diagnosis and lab value]]; [[on warfarin, INR needed within 72 hrs of any extraction|health:medication]];
[[penicillin allergy|health:allergy]]. Cleared with his physician by phone [[1/20|date:month/day only]].
Findings: [[generalized moderate periodontitis|health:dental diagnosis]], [[fractured cusp #19|health:dental finding]], [[irreversible pulpitis #30|health:dental diagnosis]],
[[night-time grinding|health:symptom]]. Third molar #1 non-restorable.

 Visit  Tooth  Code    Procedure                      Fee        Plan pays   Patient
 1      UR/LR  D4341   Scaling & root planing x2      [[$548.00|money]]    [[$438.40|money]]     [[$109.60|money]]
 2      #30    D3330   Root canal, molar            [[$1,385.00|money]]    [[$692.50|money]]     [[$692.50|money:patient portion]]
 3      #30    D2740   Crown, porcelain/ceramic     [[$1,490.00|money]]    [[$369.10|money]]   [[$1,120.90|money]]
 3      #19    D2740   Crown, porcelain/ceramic     [[$1,490.00|money]]        [[$0.00|money]]   [[$1,490.00|money:patient portion]]
 4      #1     D7140   Extraction                     [[$245.00|money]]        $0.00     [[$245.00|money:patient portion]]
                                             TOTAL  [[$5,158.00|money]]  [[$1,500.00|money]]   [[$3,658.00|money]]

Insurance: [[Sterling Dental Benefit Plan|o2:full]], subscriber Annika Lindahl through her employer, member ID [[SDB 300 771 42|rec:member ID with spaces]], group [[WA-06611|rec:group number]].
Annual maximum [[$1,500|money]]; [[$0|money]] used so far in 2026. The plan estimate is not a guarantee. Pre-determination sent [[1/21/26|date:numeric date with two-digit year]], ref [[PD-4471902|rec:pre-determination reference]].

PAYMENT ARRANGEMENT (no interest, so the Truth in Lending Act disclosures do not apply; we do not take CareCredit)
 - Down payment today: [[$658.00|money]] on card.
 - Balance [[$3,000.00|money]] in six payments of [[$500.00|money]] on the 5th of each month, [[March 5|date:first installment, no year]] through [[August 5, 2026|date:last installment]].
 - Card on file (Visa), holder [[ANNIKA LINDAHL|p2:caps:name as embossed on a card]]:  [[4540-0156-7938-9160|card:card number with dashes]]   exp [[11/27|exp]]   CVV [[608|cvv]]
   [[Mrs. Lindahl|p2:title-surname]] gave the card by phone; [[Henrik|p1:first-name]] is not an authorized user.
 - Backup if the card declines: bank draft from [[Kittitas Farmers Bank|o3:full]], routing [[059828822|rtn]], checking [[81 0044 6217|acct:account number with spaces]].
 - A missed payment adds [[$25|money]] and pauses lab work on the crowns.

Patient/responsible party signature: [[A. Lindahl|p2:short:initial + surname]]          Date: [[1-22-26|date:dashes, two-digit year]]
Staff: [[J. Ramos|p4:short:initial + surname]]   (note: [[Mr. Lindahl|p1:title-surname]] asked that statements NOT go to the Thorp address; [[the couple are in the middle of a divorce|attr:marital status]]. Email [[Annika|p2:first-name]] only.)
'''))

# ---------------------------------------------------------------- 228
DOCS.append(D(228, "txt", "subpoena duces tecum", "legal", "US",
  title="Subpoena to produce records (phone carrier and bank)",
  ents={"p1": "Rosalva Zubiri", "p2": "Devon Petrov", "p3": "Thandiwe Dlamini", "p4": "Gareth Sinclair",
        "o1": "Hartwell Ridge Property Management, LLC", "o2": "Sagelark Wireless, Inc.", "o3": "Aspen Gold Bank",
        "o4": "Dlamini Kapoor LLC", "o5": "Mile High Legal Couriers"},
  distractors=["C.R.C.P. 45", "C.R.C.P. 26(c)", "C.R.S. § 13-25-126", "Stored Communications Act", "18 U.S.C. § 2702",
               "DISTRICT COURT", "Exhibit A", "Exhibit B", "EXHIBIT A", "EXHIBIT B", "Colorado Rules of Evidence 902(11)"],
  ok=["1", "2", "3", "4", "9", "204", "Atty", "ICCID", "IMEI", "IP", "OF", "Plaintiff's", "Reg", "SIM", "TO"],
  body=r'''
DISTRICT COURT, [[ARAPAHOE COUNTY|place:county in a caps court heading]], [[COLORADO|place:state in a caps court heading]]
Case Number: [[2025CV031447|rec!:state court case number without separators]]          Division: 204

Plaintiff:   [[ROSALVA ZUBIRI|p1:caps:name in caption]]
v.
Defendants:  [[HARTWELL RIDGE PROPERTY MANAGEMENT, LLC|o1:caps:name in caption]], and [[DEVON PETROV|p2:caps:name in caption]], individually

Attorney for Plaintiff:
[[Thandiwe Dlamini|p3:full]], Atty. Reg. # [[48817|govid:attorney registration number]]
[[Dlamini Kapoor LLC|o4:full]], [[5350 S. Roslyn St., Ste. 310|addr:street with suite]], [[Greenwood Village|place:city]], [[CO|place:state abbreviation]] [[80111|zip]]
Phone [[720-555-0137|phone]]   Fax [[720-555-0138|phone:fax]]   [[tdlamini@dlaminikapoor.example|email]]

                    SUBPOENA TO PRODUCE (C.R.C.P. 45)

TO:  (1) Custodian of Records, [[Sagelark Wireless, Inc.|o2:full]], Subpoena Compliance, fax [[866-555-0109|phone:toll-free fax]]
     (2) Custodian of Records, [[Aspen Gold Bank|o3:full]], Legal Process Unit, [[PO Box 17730|addr:PO Box]], [[Denver|place:city]], CO [[80217|zip]]

YOU ARE ORDERED to produce the records described in Exhibit A (to [[Sagelark|o2:short]]) and Exhibit B (to the Bank) at the
office of Plaintiff's counsel above on or before [[December 5, 2025|date:production deadline]] at 10:00 a.m. Production by
secure upload with a records affidavit under Colorado Rules of Evidence 902(11) is accepted in place of appearance.

EXHIBIT A -- [[Sagelark Wireless|o2:short]]
For the period [[March 1, 2025|date:start of records period]] through [[July 31, 2025|date:end of records period]], for the account of subscriber
[[Devon Petrov|p2:full]], account no. [[SW-9920-417736|rec:carrier account number]], and each line on it, including:
   [[(303) 555-0172|phone]]   (believed to be [[Mr. Petrov|p2:title-surname]]'s personal line)
   [[303-555-0198|phone]]     (believed to be the on-call maintenance line for [[Hartwell Ridge|o1:short]])
1. Subscriber and billing records, including the name, address and payment method on file.
2. Call and text detail records (date, time, duration, numbers). Content of messages is NOT requested; see the
   Stored Communications Act, 18 U.S.C. § 2702.
3. Device history for each line, including the device with IMEI [[35 364581 477864 8|dev:IMEI with spaces]] and any SIM
   change (ICCID [[8901260882317764051|dev!:SIM card number]]).
4. IP session logs showing the addresses assigned to those lines on [[June 14, 2025|date:incident date]] between 9 p.m. and
   midnight, and the subscriber to whom [[198.51.100.77|ip:IPv4]] and [[2001:db8:4c0:1a2::9f|ip:IPv6]] were assigned at 10:42 p.m.
   that night.

EXHIBIT B -- Aspen Gold Bank
For the period [[01/01/2024|date:start of records period]] to [[09/30/2025|date:end of records period]]:
1. Statements, signature cards and deposit items for the Hartwell Ridge "Tenant Security Deposits" account
   no. [[4400 7718 2093|acct:account number with spaces]] (routing [[117139563|rtn]]) and operating account ending [[-5561|acct:last four with leading dash]].
2. Records of every transfer from either account to any account held by Devon Petrov, including the
   personal checking account ending in [[0339|acct:last four only]].
3. The deposit record and both sides of cashier's check no. [[7002214|rec!:cashier's check number]] for [[$2,850.00|money]], which Plaintiff
   paid as a security deposit for [[9841 E. Girard Ave., Unit 12B|addr:street with unit]], [[Aurora|place!:city that is also a first name]], on [[11/02/2023|date:deposit date]].

Plaintiff alleges that her deposit was diverted and that, after she complained, Mr. Petrov sent her
[[threatening messages that referred to her immigration case|attr:immigration status described indirectly]]. A protective order under C.R.C.P. 26(c) covers
anything produced. Witness fee of [[$15.00|money]] per C.R.S. § 13-25-126 is tendered with service.

Date: [[November 12, 2025|date:issue date]]                 /s/ [[T. Dlamini|p3:short:initial + surname]]

RETURN OF SERVICE: served on Sagelark by fax and on the Bank by hand, [[11/13/25|date:service date, two-digit year]], by [[Gareth Sinclair|p4:full]],
[[Mile High Legal Couriers|o5:full]]. Fee [[$95|money]]. Questions about scope: [[Ms. Dlamini|p3:title-surname]]'s paralegal, ext. [[214|phone!:extension only]].
'''))

# ---------------------------------------------------------------- 229
DOCS.append(D(229, "md", "donor acknowledgment notes", "accounting", "US",
  title="Year-end donor acknowledgment working notes",
  ents={"p1": "Eleanor Suzuki", "p2": "Vikram Rao", "p3": "Nandini Rao", "p4": "Imogen Ferguson", "p5": "Lyle Kaminski",
        "p6": "Douglas Kaminski", "p7": "Faith Okonedo", "p8": "Patrick Leclerc",
        "o1": "Sparrowhawk Youth Music Project", "o2": "Wexford Hale Securities", "o3": "Beacon Charitable Gift Fund",
        "o4": "Congregation Ohr Chadash", "o5": "Pipefitters Local 512", "o6": "Leclerc Honda of Asheville"},
  cardholders=["p2", "p5"],
  distractors=["IRC § 170(f)(8)", "Form 8283", "Form 990", "Schedule B", "Publication 1771", "Amex", "Visa", "QuickBooks",
               "Section A"],
  ok=["1", "2", "3", "150", "2025", "$250", "$5,000", "CRM", "DTC", "Grant"],
  body=r'''
# [[Sparrowhawk Youth Music Project|o1:full]] — 2025 gift acknowledgments (working notes)

*Prepared by [[Imogen Ferguson|p4:full]], development manager, for the bookkeeper. EIN [[56-2740118|taxid:EIN]]. Letters must go out by [[Jan 31|date:deadline without year]]. Do not share outside finance: this has donor names next to amounts, and Schedule B is not public.*

## Letters that need special wording

**1. [[Eleanor Suzuki|p1:full]]** ([[Mrs. Suzuki|p1:title-surname]], [[91|age:bare age]] this year, our oldest donor; large print, please)
- Gift of stock: 150 shares transferred [[12/18/2025|date:transfer date]] from her account at [[Wexford Hale Securities|o2:full]], acct [[8QR-204417|acct:brokerage account]], DTC confirmation [[WH25-1218-0093|rec:transfer confirmation number]].
- Value on the date of gift: [[$21,946.50|money]] (mean of high and low). **The letter describes the shares, not the value.** She needs Form 8283 because it is over $5,000? No, publicly traded, Section A only.
- Mail to [[14 Kimberly Knoll Rd|addr]], [[Asheville|place:city]], [[NC|place:state abbreviation]] [[28804|zip]]. Her daughter [[Faith Okonedo|p7:full]] opens the mail now ([[Eleanor has macular degeneration|health:diagnosis]]); copy [[faith.okonedo@postbox.example|email]].

**2. [[Vikram|p2:first-name]] and [[Nandini Rao|p3:full]]**
- Monthly gift of [[$275|money]] on Vikram's Amex ending [[2586|card:last four only]], twelve charges, [[$3,300.00|money]] total. One charge ([[Aug 3|date:abbreviated date without year]]) was refunded and re-run, so QuickBooks shows thirteen. It is twelve.
- Gala table, [[$2,000|money]], less goods and services of [[$640|money]] (eight dinners at [[$80|money]]). Deductible: [[$1,360|money]]. This is a quid pro quo letter under IRC § 170(f)(8).
- They asked to be listed as "[[The Rao Family|p2:short!:family name used as a donor listing]]". Address [[305 Sunset Summit|addr:street with no street type]], Asheville [[28804-1120|zip:ZIP+4]]. [[vik.rao@mailhaven.example|email]], [[828-555-0166|phone]].

**3. [[Lyle Kaminski|p5:full]]**
- [[$7,500|money]] by Visa, card number on the pledge form [[4660 7563 0004 2082|card:card number with spaces]] (shred the form after entry; do NOT type the number into the CRM, last four only).
- Given "[[in memory of my husband Doug|indirect:family relationship revealing a same-sex marriage]]" ([[Douglas Kaminski|p6:full]], our former board treasurer, d. [[April 2025|date:month and year of death]]). Use that wording exactly. [[Lyle|p5:first-name]] does not want the gift listed in the annual report.
- [[828.555.0143|phone:dotted]]; [[22B Chestnut Mews|addr:unit letter attached to house number]], Asheville, NC [[28801|zip]].

## Gifts through someone else (no tax letter from us, thank-you only)

| Source | Amount | Notes |
|---|---|---|
| [[Beacon Charitable Gift Fund|o3:full]] (donor-advised) | [[$10,000.00|money]] | Grant [[BCG-2025-118845|rec:grant number]], advised by the [[Raos|p2:nickname:plural family nickname]]. [[Beacon|o3:short]] is the donor of record. Check [[#0061877|rec:check number]]. |
| [[Congregation Ohr Chadash|o4:full]] sisterhood | [[$1,200|money]] | Collected at their [[Hanukkah|attr:religious observance]] concert. Mrs. Suzuki's daughter-in-law organised it; several of our parents [[are members there|attr:religious affiliation]]. Cheque [[#4418|rec:check number]]. |
| [[Pipefitters Local 512|o5:full]] | [[$750|money]] | Instrument fund. Arranged by [[Patrick Leclerc|p8:full]], [[a member of the local|attr:union membership]] and dad of one of our cellists. Money order [[19-447720613|rec:money order number]]. |

## In-kind

- [[Leclerc Honda of Asheville|o6:full]] ([[Patrick|p8:first-name]]'s brother's dealership) lent a van for the tour. No value stated in the letter. Their EIN, if the auditor asks: [[56-1193027|taxid:EIN]].

## Loose ends

- Publication 1771 says $250 and up needs a written acknowledgment. Everything above qualifies except nothing; the [[Local 512|o5:short]] gift is from an organisation, still send one.
- [[Mr. Rao|p2:title-surname]] wants a single year-end statement instead of twelve receipts. Fine.
- Form 990 Schedule B: [[Suzuki|p1:surname]], Beacon and [[Kaminski|p5:surname]] are over the threshold. — [[IF|p4:initials]], [[1/9/26|date:numeric date with two-digit year]]
'''))

# ---------------------------------------------------------------- 230
DOCS.append(D(230, "txt", "gift tax return notes", "accounting", "US",
  title="Preparer notes for a 2025 gift tax return (Form 709)",
  ents={"p1": "Cornelius R. Haverford", "p2": "Marjorie Haverford", "p3": "Preston Haverford",
        "p4": "Camille Haverford-Leung", "p5": "Theo Leung", "p6": "Wren Leung", "p7": "August Haverford",
        "p8": "Gwendolyn Aaltonen", "p9": "Bartholomew Stroud",
        "o1": "Haverford 2019 Irrevocable Family Trust", "o2": "Haverford Orchard Lands LLC",
        "o3": "Stroud Valuation Partners", "o4": "Aaltonen & Nyström, CPAs", "o5": "Yakima Basin Trust Company",
        "o6": "Cashmere Valley Brokerage"},
  minors=["p5", "p6", "p7"],
  distractors=["Form 709", "Schedule A", "Part 2", "IRC § 529(c)(2)(B)", "Form 706", "Rev. Rul. 59-60",
               "Treas. Reg. § 301.6501(c)-1(f)", "Crummey", "DSUE", "GST"],
  ok=["1", "2", "3", "4", "5", "8", "12", "15", "12%", "31%", "1040", "2019", "2021", "2023", "2025", "2025-2029", "3520",
      "529", "709s", "G-1", "IN", "PTIN", "September", "US"],
  body=r'''
[[AALTONEN & NYSTRÖM, CPAs|o4:caps]]                                             workpaper G-1
2025 Form 709 -- preparer notes                                          client no. [[20417|rec!:client number]]
Donor: [[Cornelius R. Haverford|p1:full]] ("[[Neil|p1:nickname]]")      SSN [[776-68-2859|ssn]]      b. [[1/26/1934|dob:numeric without leading zero]], so [[91|age:bare age]] at the date of every gift
       [[2204 Naches Heights Rd|addr]], [[Yakima|place:city]], [[WA|place:state abbreviation]] [[98908|zip]]     [[509-555-0120|phone]] (landline only, no email)
Widower. [[Marjorie Haverford|p2:full]] d. [[11/3/2020|date:date of death]]; Form 706 filed, DSUE of [[$4,180,000|money]] elected and available.
Citizenship: US. No gift-splitting (no spouse). Prior 709s: 2019, 2021, 2023.

GIFTS IN 2025
1. Cash to son [[Preston Haverford|p3:full]] (SSN [[240-44-2974|ssn]]), wire [[03/10/2025|date:wire date]], [[$60,000|money]]. Present interest.
   [[Preston|p3:first-name]] used it to pay off [[a tax lien on his restaurant|attr:financial distress]]. Annual exclusion [[$19,000|money]]; taxable [[$41,000|money]].
2. Quitclaim of the lake cabin to daughter [[Camille Haverford-Leung|p4:full]] (SSN [[649 25 6481|ssn:SSN with spaces]]), recorded [[June 2, 2025|date:recording date]],
   [[Chelan County|place:county]] parcel [[272215340050|rec!:parcel number without separators]], [[118 Wapato Point Lane|addr]], [[Manson|place!:town that is also a surname]]. Appraised [[$735,000|money]] by
   [[Bartholomew Stroud|p9:full]], [[Stroud Valuation Partners|o3:full]], report dated [[7/15/25|date:numeric date with two-digit year]]. Taxable [[$716,000|money]].
3. 529 plans, five-year election under IRC § 529(c)(2)(B), all funded [[9/4/2025|date:contribution date]], [[$95,000|money]] each:
      [[Theo Leung|p5:full]], 12            SSN [[746-60-5089|ssn]]     acct [[529-WA-00418827|acct:529 plan account number]]
      [[Wren Leung|p6:full!:first name that is also a common word]], 8             SSN [[242-70-5729|ssn]]     acct [[529-WA-00418835|acct:529 plan account number]]
      [[August Haverford|p7:full!:first name that is also a month]], 15      SSN [[802-01-0560|ssn]]     acct [[529-WA-00402291|acct:529 plan account number]]
   One-fifth ([[$19,000|money]]) reported each year 2025-2029. Check the box on Schedule A.
   Careful: "[[August|p7:first-name!:first name that is also a month]]" is the grandson, [[Preston's boy|indirect:family relationship to a named person]]; the contribution was in September. I mixed
   this up once already.
4. Transfer of a 12% non-voting interest in [[Haverford Orchard Lands LLC|o2:full]] (EIN [[91-2204417|taxid:EIN]]) to the
   [[Haverford 2019 Irrevocable Family Trust|o1:full]] (EIN [[92-6140337|taxid:EIN of a trust]]), [[Yakima Basin Trust Company|o5:full]], trustee, on [[12/22/2025|date:transfer date]].
   Pro rata value [[$1,152,000|money]]; after combined discounts of 31% (Rev. Rul. 59-60 analysis, [[Stroud|o3:short]] report no.
   [[SVP-25-0612|rec:appraisal report number]]) the gift is [[$794,880|money]]. Crummey notices went to Camille, Preston and the three grandchildren
   on [[12/23|date:month/day only]]; five exclusions less what item 3 already used. GST: allocate exemption, Part 2.
   Attach the full appraisal for adequate disclosure, Treas. Reg. § 301.6501(c)-1(f).
5. NOT a gift: tuition of [[$31,400|money]] paid straight to August's school, and [[$8,912.36|money]] to the hospital for
   [[Wren|p6:first-name!:first name that is also a common word]]'s [[tonsillectomy|health:surgical procedure]]. Both excluded under the direct-payment rule. Keep the receipts.

OPEN POINTS
- Securities sold to fund item 3 came from [[Cashmere Valley Brokerage|o6:full]] acct [[CV-7120-3398|acct:brokerage account]]. Basis report still missing.
- [[Mr. Haverford|p1:title-surname]] signs with difficulty since [[his hip fracture in October|health:injury]]. [[Camille|p4:first-name]] holds a durable power of attorney
  but the return must be signed by him if he is able. Her cell: [[(509) 555-0187|phone]]; [[camille.hl@postbox.example|email]].
- Lifetime exemption used through 2023: [[$2,306,500|money]]. After 2025 roughly [[$3.99 million|money:amount with word scale]]. No tax due.
- [[Theo|p5:first-name]] and Wren's father is [[a Canadian citizen|attr:citizenship of a relative]]; not relevant to the donor's return, noted for the 3520 question.
Due [[April 15, 2026|date:filing deadline]]. Extension rides with his 1040.
Preparer: [[Gwendolyn Aaltonen|p8:full]], CPA, PTIN [[P01448276|taxid:PTIN]]         reviewed [[GA|p8:initials]] [[2/19/26|date:review date]]
'''))
