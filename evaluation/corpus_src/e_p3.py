from corpus_src.dsl import D, dt, amt, num

DOCS = []

# ---------------------------------------------------------------- 91
DOCS.append(D(91, "rtf", "bank reconciliation notes", "accounting", "US",
  title="Bank reconciliation notes - dental practice, September",
  ents={"p1": "Thaddeus Okoro-Lindgren", "p2": "Yolanda Fontenot-Park", "p3": "Candace Thibodeaux",
        "o1": "Magnolia Street Dental Studio, PLLC", "o2": "Bayou Teche State Bank",
        "o3": "Crescent Ledger Bookkeeping Co.", "o4": "Acadiana Dental Supply, Inc.",
        "o5": "Van der Meer Dentaal B.V.", "o6": "Bayou Belle Casino", "o7": "Teche Ridge Properties",
        "o8": "Pelican Lab Works"},
  distractors=["Form 941", "ACH", "Q3", "ATM", "September"],
  body=r'''
# Bank reconciliation notes - September 2026
**Client:** [[Magnolia Street Dental Studio, PLLC|o1:full]] ([[Dr. Thaddeus Okoro-Lindgren|p1:full:title + full name]], DDS)
**Account:** [[Bayou Teche State Bank|o2:full]] operating checking [[0113-20-88417|acct]], routing [[046209881|rtn]]
**Prepared by:** [[Yolanda Fontenot-Park|p2:full]], [[Crescent Ledger Bookkeeping Co.|o3:full]], [[10/08/2026|date:prepared date]]
## Summary
Balance per bank statement at [[9/30/2026|date:statement date]] was [[$48,217.63|money]]. Deposits in transit are [[$3,905.00|money]] (merchant batch of 9/30, cleared 10/1). Outstanding checks total [[$7,494.15|money]], listed below. Adjusted bank balance is [[$44,628.48|money]]. Balance per books is [[$45,888.48|money]]. That leaves [[$1,260.00|money]] unexplained, and I think I know what it is (item 2).
## Outstanding checks
| Check | Payee | Date | Amount |
| [[10582|rec:check number]] | [[Acadiana Dental Supply, Inc.|o4:full]] | [[09/24/2026|date:check date]] | [[$2,318.40|money]] |
| [[10585|rec:check number]] | [[Teche Ridge Properties|o7:full]] (rent) | [[09/28/2026|date:check date]] | [[$4,350.00|money]] |
| [[10586|rec:check number]] | [[Pelican Lab Works|o8:full]] | [[09/29/2026|date:check date]] | [[$825.75|money]] |
## Items to discuss with the doctor
- **1. Wire in, 9/11.** Credit of [[$3,402.00|money]] is a refund from [[Van der Meer Dentaal B.V.|o5:full]] for the returned handpiece ([[EUR 3,150.00|money!:currency code prefix]] at the bank's rate). Sender account IBAN [[NL14 RABO 7479 6435 16|iban]], BIC [[RABONL2U|acct!:SWIFT code]]. I booked it against equipment, not income.
- **2. ATM withdrawals.** Five cash withdrawals between [[9/4|date!:date without year]] and [[9/26|date!:date without year]], [[$200|money]] to [[$300|money]] each, all at the machine inside [[Bayou Belle Casino|o6:full]] in [[Breaux Bridge|place:city]], on the practice debit card ending [[8553|card!:last four only]]. That card is the one issued to the office manager, [[Candace Thibodeaux|p3:full]]. They add up to exactly $1,260.00. Nothing in the books for any of them.
- I asked [[Candy|p3:nickname]] about it on the phone. She said she "borrowed against her paycheck" and will pay it back, and that things have been hard at home since [[her husband's gambling got bad|health!:family member's addiction]]. I did not press. [[Dr. O-L|p1:short!:title + surname initials]] needs to hear this from me, not from the bank.
- **3. Payroll.** The [[9/15|date!:date without year]] payroll ACH ([[$11,204.37|money]]) posted twice and the duplicate was reversed [[9/17|date!:date without year]]. No action. Q3 Form 941 deposits tie.
- **4. Card processing.** September merchant fees were [[$612.90|money]]; statement rate crept up again.
## Next steps
- Call [[Dr. Okoro-Lindgren|p1:title-surname]] on his cell, [[337-555-0148|phone]], before Friday. Not the office line.
- Recommend he pull the debit card and move Candy off bank access until this is sorted. She has online banking login [[cthibodeaux_msds|cred:username]].
- Send him the recon and this memo at his personal address, [[thad.ol@okorolindgren.example|email]], not the shared office inbox.
[[YFP|p2:initials]]
'''))

# ---------------------------------------------------------------- 92
DOCS.append(D(92, "txt", "tax authority correspondence summary", "accounting", "CA",
  title="Summary of CRA correspondence - GST/HST audit",
  ents={"p1": "Jean-Luc Gagnon-Tremblay", "p2": "Sukanya Bhattacharya", "p3": "Moira MacGillivray",
        "p4": "Sylvie Gagnon-Tremblay",
        "o1": "Gagnon-Tremblay Forestry Services Inc.", "o2": "Boreal Ledger Chartered Professional Accountants",
        "o3": "Abitibi Trail Equipment Rentals Ltd.", "o4": "Caisse populaire de Timmins"},
  distractors=["GST/HST", "ETA s. 169(4)", "Form RC59", "CRA", "ITC", "T2"],
  body=r'''
[[Boreal Ledger Chartered Professional Accountants|o2:full]]
CORRESPONDENCE SUMMARY -- for file and for the partner

Client:   [[Gagnon-Tremblay Forestry Services Inc.|o1:full]] ("[[GTFS|o1:acronym]]")
          BN [[74418 2093 RT0001|taxid:Canadian business number with program account]]
          [[1184 chemin Kamiskotia Road|addr:bilingual street name]], [[Timmins|place:city]] [[ON|place:province abbreviation]]  [[P4N 7C3|zip:Canadian postal code]]
Owner:    [[Jean-Luc Gagnon-Tremblay|p1:full]] (SIN [[517-596-169|taxid:SIN with dashes]]), cell [[705-555-0183|phone]]
Our file: [[BL-2210-GST|rec:file number]]          Summary by: [[M. MacGillivray|p3:short:initial + surname]], [[2026-10-09|date:summary date]]

WHAT CAME IN
1. CRA letter dated [[September 3, 2026|date:letter date]], received here [[Sept. 11|date!:date without year]]. GST/HST audit, reporting periods
   [[2024-01-01|date:audit period start]] to [[2025-12-31|date:audit period end]]. Auditor: [[S. Bhattacharya|p2:short:initial + surname]], Audit Division,
   [[Sudbury|place:city]] Tax Services Office. Tel [[705-555-0127, ext. 4418|phone!:with extension]]. Fax [[705-555-0101|phone:fax]].
   Case ref. [[GH-2026-118-4471|rec:audit case reference]].
2. Proposal letter dated [[October 1, 2026|date:letter date]]: proposed adjustments of [[$41,280.16|money]] plus
   interest. French copy shows it as [[41 280,16 $|money!:French-Canadian number format]]. Thirty days to respond.

WHAT THEY ARE PROPOSING
(a) Deny ITCs of [[$27,930.00|money]] on invoices from [[Abitibi Trail Equipment Rentals Ltd.|o3:full]] -- auditor says
    supplier's registration number on the invoices is invalid (ETA s. 169(4) documentary
    requirements). [[Abitibi Trail|o3:short!:short name without corporate suffix]] is real and we rented from them all of 2024; their BN was
    printed with two digits transposed. Fixable with corrected invoices.
(b) Assess GST/HST of [[$9,412.50|money]] on the sale of the old skidder to [[Jean-Luc's sister-in-law|indirect!:family relationship to a named person]],
    [[Sylvie Gagnon-Tremblay|p4:full]], for [[CAD 72,500|money!:currency code prefix]] in [[March 2025|date!:month and year only]]. No tax was charged. She is not
    a registrant. He treated it as a "family thing." Assessment is probably right.
(c) Deny [[$3,937.66|money]] ITCs on meals/fuel -- no receipts. Partly right.

WHAT I DID
- Called [[Ms. Bhattacharya|p2:title-surname]] [[Oct 6|date!:date without year]]. Reasonable. She will accept corrected supplier invoices on
  (a) if received by [[October 30, 2026|date:response deadline]]. Extension to [[Nov 13|date!:date without year]] available on written request.
- Confirmed our authorization (Form RC59) is on file; rep ID [[RM7K2Q4|rec:CRA representative identifier]].
- Emailed [[Jean-Luc|p1:first-name]] at [[jlgt@gtforestry.example|email]] asking for the Abitibi Trail contact and the
  skidder bill of sale. No answer yet. His wife says [[he is in camp until the 20th|indirect!:whereabouts of a named person]] with no signal.

EXPOSURE
Best case about [[$11,000|money]] incl. interest; worst case the full proposal, roughly [[$46k|money!:k shorthand]]
with interest. The operating account at [[Caisse populaire de Timmins|o4:full]] (transit [[00417|rtn!:Canadian transit number]], acct
[[0884-217|acct]]) had [[$18,204.11|money]] at month end, so worst case needs a payment arrangement.

NOTE FOR PARTNER
[[Mr. Gagnon-Tremblay|p1:title-surname]] also asked whether the audit "has anything to do with"
[[his 2019 consumer proposal|attr!:insolvency history]]. I said no, but T2 arrears from that period still show.
'''))

# ---------------------------------------------------------------- 93
DOCS.append(D(93, "pdf", "payroll summary", "accounting", "US",
  title="Semi-monthly payroll summary - bakery and cafe",
  ents={"p1": "Bao Nguyen", "p2": "April Windsong", "p3": "Tomasz Wisniewski", "p4": "Deja Robinson",
        "p5": "Guadalupe Hernandez Ortiz", "p6": "Ingrid Solberg", "p7": "Malik Robinson",
        "o1": "Prairie Rose Bakery & Cafe LLC", "o2": "Red River Payroll Partners",
        "o3": "Dakota Plains Credit Union", "o4": "UFCW Local 1161"},
  distractors=["Form 941", "Form W-4", "FICA", "401(k)", "FUTA", "Pay period 20"],
  ok=["0.00"],
  body=r'''
# PAYROLL SUMMARY
**[[Prairie Rose Bakery & Cafe LLC|o1:full]]** | EIN [[45-3381072|taxid:EIN]] | [[ND|place:state abbreviation]] withholding acct [[WTH-2209417|taxid:state withholding account number]]
Pay period 20: [[10/16/2026|date:pay period start]] to [[10/31/2026|date:pay period end]]. Check date [[11/05/2026|date:check date]]. Processed by [[Red River Payroll Partners|o2:full]], batch [[RR-118820|rec:payroll batch number]].
## Employee totals
| Employee | ID | Gross | Net |
| [[Nguyen, Bao|p1:last-first]] | [[E-1003|rec:employee ID]] | [[$2,480.00|money]] | [[$1,902.44|money]] |
| [[Windsong, April|p2:last-first]] | [[E-1007|rec:employee ID]] | [[$1,612.50|money]] | [[$1,288.07|money]] |
| [[Wisniewski, T.|p3:last-first]] | [[E-1011|rec:employee ID]] | [[$1,944.00|money]] | [[$1,067.91|money]] |
| [[Robinson, Deja|p4:last-first]] | [[E-1015|rec:employee ID]] | [[$386.25|money]] | [[$342.18|money]] |
| [[Hernandez, G.|p5:last-first]] | [[E-1016|rec:employee ID]] | [[$1,530.00|money]] | [[$1,241.60|money]] |
| Total | | [[$7,952.75|money]] | [[$5,842.20|money]] |
## Notes for the owner
[[Ingrid Solberg|p6:full]] asked for plain-language notes this cycle, so here they are.
[[Bao Nguyen|p1:full]] (head baker) had 6.5 hours of overtime. His direct deposit changed this period to [[Dakota Plains Credit Union|o3:full]], routing [[022797346|rtn]], account [[7002 118 4460|acct!:account number with spaces]]. He brought the form in himself.
[[April|p2:first-name!:first name that is also a common word]] is back from [[maternity leave|health!:leave reason]] as of the 19th, part time. Her Form W-4 changed; she now has [[two dependents|indirect!:family detail]].
[[Tomasz Wisniewski|p3:full]]'s net is low. There is a [[child support order|attr!:family court order]] that takes [[$412.00|money]] per period (the case number is [[08-2023-DM-00417|rec:family court case number]]), plus [[UFCW Local 1161|o4:full|reveals union membership]] dues of [[$18.50|money]] ([[he is the only union member on staff|attr!:union membership]], carried over from his grocery job under the transfer card). The state unit asked us to confirm his SSN, which is [[433622202|ssn!:SSN without dashes]] in our records.
[[Deja Robinson|p4:full]] is a minor (DOB [[06/30/2010|dob]]), hours capped on school days. Her work permit is on file. Her father, [[Malik Robinson|p7:full]], asked that her pay go to a custodial account; we need a voided check first.
[[Guadalupe Hernandez Ortiz|p5:full]] started [[10/19/2026|date:hire date]]. Her I-9 was completed with a [[permanent resident card|attr!:immigration status]], number [[A-208-417-339|govid:alien registration number]]. Please keep the copy out of the general personnel folder.
## Employer taxes this period
FICA match [[$608.39|money]]. FUTA [[$11.20|money]]. State unemployment [[$87.48|money]]. The 401(k) match is 0.00 because nobody is enrolled yet. The Form 941 deposit of [[$1,811.06|money]] drafts on the check date.
Questions to [[payroll@redriverpayroll.example|email]] or [[701-555-0166|phone]].
'''))

# ---------------------------------------------------------------- 94
DOCS.append(D(94, "eml", "internal email", "accounting", "US", enc="plain",
  title="Internal email - new client setup with contact details spelled out",
  ents={"p1": "Cornelius Abara", "p2": "Stephanie Lund", "p3": "Deborah Fairweather",
        "p4": "Robert Kessinger", "p5": "Paris Delacroix",
        "o1": "Abara Lund & Co., CPAs", "o2": "Fairweather Orchards & Cider Mill, Inc.",
        "o3": "Wenatchee Valley Bank"},
  distractors=["Form 8821", "Q3", "QuickBooks", "Friday", "W-2"],
  headers={
    "From": "[[Cornelius Abara|p1:full]] <[[cabara@abaralund.example|email]]>",
    "To": "[[Stephanie Lund|p2:full]] <[[slund@abaralund.example|email]]>",
    "Subject": "new client - [[Fairweather Orchards|o2:short!:short name without corporate suffix]] - setup list (sent from my phone, sorry)",
    "Date": "Wed, [[4 Nov 2026|date:email date]] 21:17:40 -0800"},
  body=r'''
[[Steph|p2:nickname]],

Dictating this from the car so forgive the format. Signed [[Fairweather Orchards & Cider Mill, Inc.|o2:full]] today.
Family outfit outside [[Cashmere|place!:city that is also a common word]], about [[2.8 million|money!:no currency symbol, in words]] in revenue, books are a mess. Monthly
bookkeeping plus the corporate return, [[eighteen hundred a month|money!:amount in words]].

Contacts, since their email addresses never come through right when I type them:
- [[Deborah Fairweather|p3:full]], president. [[deb dot fairweather at fairweather-orchards dot example|email!:email spelled out in words]]. Cell
  [[five oh nine, 555, oh one three four|phone!:phone number spoken in words]]. She wants everything to go to her, not to her brother.
- [[Robert Kessinger|p4:full]], the outside bookkeeper they are letting go. He does not know yet so do NOT
  contact him before Friday. When you do: [[bob underscore k at mail dot example dot com|email!:email spelled out in words]].
  [[Deb|p3:nickname]] says [[Bob|p4:nickname]] has the only admin login to QuickBooks. User is [[rkessinger|cred:username]] and she thinks the
  password is [[Honeycrisp#1987|cred!:password in email]] but would not swear to it.

Things I need from you this week:
1. Engagement letter and Form 8821 (not 2848 yet) out to Deb by Friday.
2. Bank feeds. Operating account is at [[Wenatchee Valley Bank|o3:full]], routing [[124921793|rtn]], account
   [[4400187726|acct!:unlabelled-style account number without separators]]. Payroll account ends in [[3091|acct!:last four only]]. Deb will add you as a view-only user.
3. Their EIN is [[91-1840276|taxid:EIN]]. State UBI [[604 118 227|taxid:state business identifier]].
4. Put the software subscription on the firm card for now and bill it through. Amex,
   [[3714 788330 86605|card:Amex grouping]], expires [[08/29|exp]], four digit code on the front is [[4026|cvv!:four-digit Amex code]]. Please do not
   leave that in the client folder.
5. Deb mentioned in passing that her brother [[Paris Delacroix|p5:full]] (half-brother, different last
   name) took a "loan" of about [[60k|money!:k shorthand]] out of the company in [[May|date!:month only, tied to a transaction]] and that he is
   [[in rehab in Spokane|health!:substance-use treatment]] right now. She does not want it discussed with staff there.
   Book it to a shareholder receivable until we know more. [[Paris|p5:first-name!:first name that is also a place]] owns 20 percent.

Q3 payroll returns were filed late, there will be notices. W-2 season is going to be fun.

Thanks
[[Cornelius|p1:first-name]]

[[Abara Lund & Co., CPAs|o1:full]] | [[320 Orondo Avenue, 2nd Floor|addr]] | [[Wenatchee|place:city]], [[WA|place:state abbreviation]] [[98801|zip]]
'''))

# ---------------------------------------------------------------- 95
DOCS.append(D(95, "txt", "insurance claim appeal letter", "health", "US",
  title="Appeal of denied skilled nursing claim, written by the patient's daughter",
  ents={"p1": "Florence Abernethy-Hsu", "p2": "Constance Hsu-Navarro", "p3": "Babajide Olatunji",
        "p4": "Reginald Hsu",
        "o1": "Evergreen Senior Health Plan", "o2": "Willamette Bend Rehabilitation & Care Center",
        "o3": "Santiam Valley Medical Center"},
  distractors=["42 C.F.R. § 422.582", "Notice of Denial of Medical Coverage",
               "Explanation of Benefits", "Level 1", "Appeals Department"],
  body=r'''
[[Constance Hsu-Navarro|p2:full]]
[[2750 NW Arbor Crest Lane|addr]]
[[Corvallis|place:city]], [[Oregon|place:state]] [[97330|zip]]
[[(541) 555-0158|phone]]  |  [[connie.hsunavarro@familymail.example|email]]

[[November 2, 2026|date:letter date]]

[[Evergreen Senior Health Plan|o1:full]]
Appeals Department
[[P.O. Box 44170|addr:PO Box]]
[[Salem|place:city]], [[OR|place:state abbreviation]] [[97308-4170|zip:ZIP+4]]
Sent by fax to [[1-866-555-0121|phone:toll-free fax]] and by certified mail

RE:  Request for reconsideration (Level 1 appeal)
     Member: [[Florence Abernethy-Hsu|p1:full]]
     Member ID: [[ESH 0044 71920 01|rec:health plan member ID]]        Medicare no.: [[4TK9-RW2-YH58|govid:Medicare beneficiary identifier]]
     Date of birth: [[February 8, 1934|dob]]
     Claim no.: [[2026-SNF-0098214|rec:claim number]]
     Dates of service denied: [[09/21/2026|date:service start]] through [[10/09/2026|date:service end]]

To whom it may concern:

I am Mrs. Abernethy-Hsu's daughter and I hold her health care power of attorney (copy
enclosed). I am writing to appeal your Notice of Denial of Medical Coverage dated
[[October 12, 2026|date:denial date]], which refuses payment for nineteen days of skilled nursing care at
[[Willamette Bend Rehabilitation & Care Center|o2:full]] on the ground that the care was "custodial."

It was not custodial. [[My mother|indirect!:family relationship to a named person]] is [[92 years old|age]]. On [[September 14|date!:date without year]] she fell in her kitchen
and [[broke her left hip|health!:injury]]. She had [[a partial hip replacement|health!:surgical procedure]] at [[Santiam Valley Medical Center|o3:full]]
on [[September 15|date!:date without year]] and was discharged to [[Willamette Bend|o2:short!:short name without corporate suffix]] six days later on her surgeon's order.
Her surgeon, [[Dr. Babajide Olatunji|p3:full:title + full name]] (NPI [[1881746203|govid:NPI]]), wrote the order for daily physical and
occupational therapy and for skilled nursing to manage her [[warfarin|health!:medication]] and a
[[stage 2 pressure wound on her heel|health!:wound]]. The therapy notes show she went from needing two people to stand to
walking sixty feet with a walker. That is the definition of skilled rehabilitation.

Your denial says she "plateaued" on [[September 21|date!:date without year]]. That is the day she arrived. I would
like to know who reviewed the file. Your letter also says she has [[advanced dementia|health!:diagnosis]]. She
does not. She has [[mild memory loss|health!:condition]] and does the crossword in pen.

The facility has billed us [[$11,343.00|money]] ([[$597|money]] a day for nineteen days). My mother lives on
Social Security and my late father's pension, about [[$2,900|money]] a month. [[My brother|indirect!:family relationship to a named person]] [[Reginald Hsu|p4:full]]
and I have paid [[$4,000|money]] of it so the facility would not send her to collections; I paid
with my own card ([[Visa ending 3637|card!:last four only]]) and I expect that to be refunded when this is overturned.

I am requesting an expedited reconsideration under 42 C.F.R. § 422.582 and a copy of
the complete case file, including the name and credentials of the reviewer.

Enclosed: power of attorney; [[Dr. Olatunji|p3:title-surname]]'s letter of [[October 20, 2026|date:letter date]]; therapy notes;
facility statement no. [[WB-77120-A|rec:statement number]]; your denial; the Explanation of Benefits.

If you need her Social Security number to locate the file, the last four are [[9427|ssn!:last four only]]. Please
call me, not her. [[She is hard of hearing|health!:condition]] and the calls frighten her.

Sincerely,

Constance Hsu-Navarro ([[Connie|p2:nickname]])
Daughter and health care representative for [[Mrs. Abernethy-Hsu|p1:title-surname]]

cc: [[Reggie Hsu|p4:nickname:nickname + surname]]; Oregon Senior Health Insurance Benefits Assistance
'''))

# ---------------------------------------------------------------- 96
DOCS.append(D(96, "html", "clinical visit note", "health", "US",
  title="Pediatric clinic visit note - diabetes and asthma follow-up",
  ents={"p1": "Mateo Okafor-Jimenez", "p2": "Adaeze Okafor", "p3": "Hannah Goldfarb-Reyes",
        "p4": "Luis Jimenez", "p5": "Tamsin Whitehorse",
        "o1": "Canyon Rim Pediatrics, P.A.", "o2": "Juniper Ridge Elementary",
        "o3": "Mesa Vista Pharmacy", "o4": "Sandia Peaks Health Cooperative"},
  distractors=["CPT 99214", "ICD-10", "Type 1", "A1c", "504 plan", "CGM"],
  ok=["E10.65", "J45.30"],
  body=r'''
# [[Canyon Rim Pediatrics, P.A.|o1:full]] - Office visit
| Patient | DOB | MRN | Visit date |
| [[OKAFOR-JIMENEZ, MATEO|p1:last-first]] | [[04/17/2019|dob]] | [[CRP-0088214|rec:medical record number]] | [[10/27/2026|date:visit date]] |
**Provider:** [[Hannah Goldfarb-Reyes|p3:full]], MD (NPI [[1629407715|govid:NPI]]). **Accompanied by:** mother, [[Adaeze Okafor|p2:full]]. **Insurance:** [[Sandia Peaks Health Cooperative|o4:full]], member ID [[SPH-771-204-88-02|rec:health plan member ID]].
## Subjective
[[Mateo|p1:first-name]] is a 7-year-old boy with [[type 1 diabetes|health!:diagnosis]] (diagnosed [[March 2024|date!:month and year only]]) and [[mild persistent asthma|health!:diagnosis]], here for a three-month follow-up. Mom reports [[two overnight lows in the 50s|health!:glucose readings]] in the past month, both after soccer. No ketones, no ER visits. He used his rescue inhaler about twice a week during the smoke days in September.
School: second grade at [[Juniper Ridge Elementary|o2:full]]. The school nurse, [[Tamsin Whitehorse|p5:full]], has asked for an updated diabetes plan; his 504 plan is due for review. Mom says [[Ms. Whitehorse|p5:title-surname]] is only on site Mondays and Wednesdays.
Social: [[Parents separated in the spring|indirect!:family circumstances]]. Mateo is with his father, [[Luis Jimenez|p4:full]], on alternate weekends. Mom is worried that [[dad does not count carbs|indirect!:family circumstances]] and that weekend numbers run high. She asked that the pump reports not be mailed to the old address. [[Family speaks Igbo and Spanish at home|attr!:ethnicity and language]]; Mateo answers me in English.
## Objective
| Measure | Today | Last visit |
| Weight | 24.1 kg | 23.2 kg |
| Height | 124 cm | 122.5 cm |
| A1c | [[7.9%|health!:lab result]] | [[7.4%|health!:lab result]] |
| Time in range | [[58%|health!:glucose time in range]] | [[66%|health!:glucose time in range]] |
Exam: well appearing, lungs clear, [[mild lipohypertrophy at the left abdomen infusion sites|health!:exam finding]]. Insulin pump serial [[PAA-3381-20417|dev:insulin pump serial number]]; CGM transmitter [[8HX2K7|dev:CGM transmitter ID]], paired to mom's phone.
## Assessment and plan
- Type 1 diabetes, above goal (ICD-10 E10.65). Change overnight basal from [[0.35 units/hr|health!:insulin dose]] to [[0.30 units/hr|health!:insulin dose]] on activity days. Rotate sites; avoid left abdomen for a month.
- Asthma, controlled (J45.30). Continue [[fluticasone 44 mcg, 2 puffs twice daily|health!:medication and dose]]. Flu vaccine given today, lot [[UJ417AB|rec:vaccine lot number]].
- Refills sent to [[Mesa Vista Pharmacy|o3:full]], [[505-555-0112|phone]]: [[insulin lispro|health!:medication]], Rx [[#7740291|rec:prescription number]]; test strips.
- New school orders faxed to the nurse at [[505-555-0191|phone:fax]]. Copy to mom through the portal, [[https://portal.canyonrimpeds.example/chart/0088214|url]].
- Offered a visit with our social worker about the two-household routine. Mom will think about it. With her consent I will send [[Mr. Jimenez|p4:title-surname]] the same carb-counting handout; his email on file is [[luis.jimenez77@inbox.example|email]].
Billing: CPT 99214. Return in 3 months, sooner for lows under 54.
Signed electronically, [[H. Goldfarb-Reyes MD|p3:short:initial + surname + credential]], [[10/27/2026 4:52 PM|date!:date with time stamp]]
'''))

# ---------------------------------------------------------------- 97
DOCS.append(D(97, "txt", "pharmacy note", "health", "US", length="short",
  title="Pharmacy counter note - early refill",
  ents={"p1": "Edith Kowalczuk", "p2": "Marlene Kowalczuk", "p3": "Vikram Patel"},
  distractors=["INR", "OK'd"],
  body=r'''
Rx [[6620417-03|rec:prescription number]] [[warfarin 2.5 mg|health!:medication and dose]] - [[E. Kowalczuk|p1:short:initial + surname]], [[93 y/o|age!:abbreviated age]], DOB [[4/9/33|dob!:two-digit year]]
[[Dr. Patel|p3:title-surname]]'s office ([[555-0115|phone!:seven digits, no area code]]) OK'd early refill.
[[INR 3.4|health!:lab result]] on [[10/28|date!:date without year]] - told daughter [[Marlene|p2:first-name]] to hold tonight's dose.
Copay [[$11.40|money]], card ending [[6379|card!:last four only]]. Do not leave msg on home phone - [[pt lives alone|indirect!:living situation]].
'''))

# ---------------------------------------------------------------- 98
DOCS.append(D(98, "docx", "psychiatric evaluation", "health", "US",
  title="Initial psychiatric evaluation",
  ents={"p1": "Jonah R. Castellanos-Meyer", "p2": "Priyanka Subramaniam", "p3": "Marcus Tolliver",
        "p4": "Ruth Meyer", "p5": "Owen Blackfeather",
        "o1": "Three Rivers Behavioral Health Associates", "o2": "Allegheny Steel City Transit Authority",
        "o3": "Monongahela Valley Hospital", "o4": "Keystone Unified Health Plan"},
  distractors=["DSM-5-TR", "PHQ-9", "AUDIT-C", "CPT 90792", "FMLA", "Mental status examination"],
  ok=["F31.81", "F10.20"],
  body=r'''
# Initial Psychiatric Evaluation
**[[Three Rivers Behavioral Health Associates|o1:full]]** - [[4100 Penn Avenue, Suite 6|addr]], [[Pittsburgh|place:city]], [[PA|place:state abbreviation]] [[15224|zip]]
| Patient | [[Jonah R. Castellanos-Meyer|p1:full]] |
| Date of birth | [[12 Jan 1992|dob:day month year]] |
| MRN | [[TRB-204417|rec:medical record number]] |
| SSN | [[xxx-xx-9960|ssn!:masked SSN]] |
| Insurance | [[Keystone Unified Health Plan|o4:full]], ID [[KUH88120447|rec:health plan member ID]] |
| Date of evaluation | [[October 21, 2026|date:evaluation date]] |
| Evaluator | [[Priyanka Subramaniam|p2:full]], MD |
## Reason for referral
[[Mr. Castellanos-Meyer|p1:title-surname]] is a 34-year-old bus operator for the [[Allegheny Steel City Transit Authority|o2:full]] referred by his primary care physician, [[Dr. Owen Blackfeather|p5:full:title + full name]], after two weeks of [[sleeping three hours a night|health!:symptom]] followed by a period in which he "could not get off the couch." He is on leave and asks for FMLA paperwork.
## History of present illness
He describes at least four episodes since his early twenties of elevated mood, little need for sleep, rapid speech and overspending lasting four to six days. In the most recent, in early September, he [[put $9,200 on a credit card in one weekend|health!:symptom with financial detail]], mostly on camera equipment. These are followed by weeks of low mood. Current PHQ-9 is 17. He [[denies suicidal intent but has had passive thoughts|health!:suicidality screen]] ("it would be easier not to wake up"). No psychosis.
## Past psychiatric history
One hospitalization, [[Monongahela Valley Hospital|o3:full]], [[March 3-9, 2019|date:hospitalization dates]], after [[an overdose of sleeping pills|health!:suicide attempt]]. Discharged on [[sertraline|health!:medication]], which he says "made everything faster." No outpatient follow-up since 2020.
## Substance use
Drinks most evenings, four to six beers, more on days off. AUDIT-C is 9. He was [[arrested for DUI in August 2022|attr!:criminal history]] (off duty, personal vehicle; license suspended 60 days; [[the Authority|o2:short!:generic-looking short name]] was notified). [[Uses cannabis edibles to sleep|health!:substance use]]. Denies other drugs.
## Family and social history
[[Mother, Ruth Meyer, has Huntington's disease|attr!:genetic information about a named relative]]; he has [[declined predictive genetic testing|attr!:genetic testing decision]] and says that not knowing is "the only way I can drive a bus." Father's side: an uncle with "manic depression." [[Raised Jehovah's Witness, no longer practicing|attr!:religion]], and estranged from most of his mother's family over it.
He [[lives with his partner of six years|indirect!:household and relationship]], [[Marcus Tolliver|p3:full]], in [[Bloomfield|place:neighbourhood]]. He [[identifies as gay|attr!:sexual orientation]]; out at home, not at work. [[Marcus|p3:first-name]] is the emergency contact ([[412.555.0139|phone:dotted]]) and came to the first half of the visit with the patient's consent. He is [[a steward in ATU Local 85|attr!:union role]] and worries a diagnosis will be used against him in a pending grievance.
## Mental status examination
Casually dressed, cooperative, good eye contact. Speech normal rate today. Mood "flat." Affect constricted. Thought process linear. Insight fair. Judgment fair.
## Assessment
- [[Bipolar II disorder, current episode depressed, moderate|health!:diagnosis]] (DSM-5-TR; F31.81)
- [[Alcohol use disorder, moderate|health!:diagnosis]] (F10.20)
- [[Family history of Huntington's disease|attr!:genetic information]]; neurologic exam unremarkable today
## Plan
- Start [[lamotrigine 25 mg daily|health!:medication and dose]], titrate per schedule; rash precautions reviewed. Taper sertraline over two weeks.
- No driving for work until re-evaluated. Leave certified through [[November 30, 2026|date:leave end date]]; form sent to the Authority's leave office, attention [[file LV-2026-0733|rec:leave file number]], with diagnosis withheld.
- Referral to intensive outpatient program for alcohol use. He agreed to remove the [[9 mm handgun|indirect!:firearm in the home]] from the home; Marcus will take it to his brother's.
- Safety plan completed. Return [[11/04/2026|date:follow-up date]]. Crisis line reviewed.
[[P. Subramaniam, MD|p2:short:initial + surname + credential]] - DEA [[FS4471900|govid:DEA number]] - License [[MD-448120|govid:state medical license number]] - CPT 90792
'''))

# ---------------------------------------------------------------- 99
DOCS.append(D(99, "md", "security incident report", "general", "US",
  title="Security incident report - phishing and mailbox compromise",
  ents={"p1": "Rosalind Achterberg-Cole", "p2": "Tevita Fonoti", "p3": "Gwendolyn Marsh",
        "p4": "Arjun Bhatnagar", "p5": "Hunter Voss",
        "o1": "Larkspur Benefits Administrators, Inc.", "o2": "Granite Peak Managed IT, LLC",
        "o3": "Cedar Hollow School District", "o4": "Front Range Cyber Mutual"},
  distractors=["MFA", "HIPAA", "45 C.F.R. § 164.404", "Microsoft 365", "SSO", "P1", "RFC 1918"],
  ok=["02:14", "1,204"],
  body=r'''
# Incident Report IR-2026-017

**Company:** [[Larkspur Benefits Administrators, Inc.|o1:full]]
**Prepared by:** [[Tevita Fonoti|p2:full]], IT Manager, with [[Granite Peak Managed IT, LLC|o2:full]]
**Status:** Contained. **Severity:** P1. **Privileged draft: prepared at the direction of counsel.**
**Tracking no.:** [[IR-2026-017|rec:incident number]] / insurer claim [[FRC-CY-0044186|rec:insurance claim number]] ([[Front Range Cyber Mutual|o4:full]])

## Summary

On [[Monday, October 12, 2026|date:incident date]], a claims analyst entered her Microsoft 365 credentials into a fake
SSO page. The attacker used the mailbox for about 31 hours, set up a forwarding rule, and
downloaded one spreadsheet containing enrollment data for **1,204** members of a client plan
([[Cedar Hollow School District|o3:full]]), including names, dates of birth and Social Security numbers.

## Timeline (Mountain time)

| When | What |
|---|---|
| [[10/12|date!:date without year]] 08:47 | [[Gwendolyn Marsh|p3:full]] (`[[gmarsh|cred:username]]`) receives "Benefits portal re-verification" email from `[[it-helpdesk@larkspur-benefits-login.example.net|email:look-alike sender address]]` |
| 10/12 08:52 | She signs in at `[[http://larkspur-benefits-login.example.net/sso|url:phishing URL]]` from her workstation `[[LBA-WS-0417|dev:workstation hostname]]` ([[10.20.14.87|ip:private IPv4]], MAC [[3C:52:82:1A:9F:D4|dev:MAC address]]) and approves an MFA prompt |
| 10/12 08:55 | First foreign sign-in to her mailbox from [[203.0.113.201|ip]] |
| 10/12 09:10 | Inbox rule "RSS Feeds" created; forwards anything containing "invoice" or "ACH" to `[[acct.review.8841@mailbox.example.org|email]]` |
| [[10/13|date!:date without year]] 02:14 | `CHSD_enrollment_2027.xlsx` downloaded from SharePoint via session at [[2001:db8:a0b:12f0::7c|ip:IPv6]] |
| 10/13 15:40 | [[Arjun Bhatnagar|p4:full]] in Finance gets an email "from Gwen" asking to change a vendor's bank details; he calls her desk instead. She has no idea what he is talking about |
| 10/13 16:05 | Sessions revoked, password reset, rule removed by [[T. Fonoti|p2:short:initial + surname]] |
| [[10/14|date!:date without year]] | Laptop serial [[PF-3KX81W7|dev:laptop serial number]] re-imaged; [[Gwen|p3:nickname]]'s phone (IMEI [[35 693803 564380 9|dev!:IMEI with spaces]]) checked, clean |

## What we know

- [[Ms. Marsh|p3:title-surname]]'s password at the time was `[[Larkspur2026!|cred!:compromised password]]`, which she also used for the payroll portal. Both changed.
- The attacker never touched the claims system. VPN logs show nothing from her account outside
  the office range (RFC 1918 space behind [[198.51.100.14|ip:office egress address]]).
- No money moved. [[Arjun|p4:first-name]]'s phone call is the only reason.
- Ms. Marsh was back from [[medical leave|health!:leave reason]] for one week and had missed the September phishing
  training. This is context, not blame. Please keep it out of the all-staff summary.

## Notification

Counsel ([[Rosalind Achterberg-Cole|p1:full]], [[303-555-0144|phone]], [[rac@achterbergcole-law.example|email]]) advises this is a reportable
breach under HIPAA; individual notices are due within 60 days of discovery (45 C.F.R. § 164.404),
so no later than [[December 11, 2026|date:notification deadline]]. The District's benefits director was told by phone
on [[October 15|date!:date without year]]. Credit monitoring quote: [[$14,448|money]] ([[$12|money]] per member). Policy retention is [[$25,000|money]].

## Actions

1. Conditional access: block sign-ins from outside the US (done [[10/16|date!:date without year]]).
2. Number-matching MFA for all staff by [[11/15/2026|date:remediation deadline]]. Owner: [[Tevita|p2:first-name]].
3. Remove SSNs from enrollment exports. Owner: [[Hunter Voss|p5:full!:first name that is also a common word]], Client Services.
4. Shared admin account `[[lba-admin|cred:shared admin username]]` still has PIN [[4802|cred!:PIN in a report]] on the server room keypad. Change it.
'''))

# ---------------------------------------------------------------- 100
DOCS.append(D(100, "pptx", "client onboarding presentation", "general", "US",
  title="Client onboarding deck - outsourced accounting",
  ents={"p1": "Marisela Quintanilla", "p2": "Desmond Calder", "p3": "Annika Voss",
        "p4": "Bettina Schrader",
        "o1": "Calder & Voss Advisory Group", "o2": "Bluebonnet Pediatric Dentistry, PA",
        "o3": "Hill Country National Bank", "o4": "Schrader Dentalwerk GmbH"},
  distractors=["Net 30", "Form W-9", "Week 1", "QuickBooks Online"],
  body=r'''
# Welcome, [[Bluebonnet Pediatric Dentistry, PA|o2:full]]
Onboarding kickoff with [[Calder & Voss Advisory Group|o1:full]]
[[November 9, 2026|date:kickoff date]] - [[Dr. Marisela Quintanilla|p1:full:title + full name]]'s office, [[New Braunfels|place:city]]
# Your team
| Role | Name | Direct line |
| Partner | [[Desmond Calder|p2:full]] | [[830-555-0117|phone]] |
| Controller | [[Annika Voss|p3:full]] | [[830-555-0118 x22|phone!:with extension]] |
- One inbox for everything: [[bluebonnet@caldervoss.example|email]]
- [[Annika|p3:first-name]] is your day-to-day contact; [[Desmond|p2:first-name]] joins the quarterly review
# What we agreed
- Monthly close by the 12th, bill pay weekly, payroll semi-monthly
- Fee: [[$2,450|money]] per month, first invoice [[12/01/2026|date:first invoice date]]
- Autopay from the practice Amex ending [[3221|card!:last four only]], exp [[11/28|exp]]
- Engagement no. [[CV-2026-0312|rec:engagement number]]
# Bank and payment setup
- Operating account: [[Hill Country National Bank|o3:full]], routing [[067680065|rtn]], account [[0052 7719 044|acct!:account number with spaces]]
- View-only access for Annika; [[Dr. Q|p1:short!:title + initial]] stays the only signer
- Overseas lab: [[Schrader Dentalwerk GmbH|o4:full]], IBAN [[IE95 AIBK 3577 8976 8483 90|iban]], contact [[Bettina Schrader|p4:full]]
- Lab invoices average [[EUR 4,200|money!:currency code prefix]] a month, terms Net 30
# Portal and devices
- Client portal: [[https://portal.caldervoss.example/bluebonnet|url]]
- Your login: [[mquintanilla|cred:username]] - temporary password [[Bluebonnet-Start-77|cred!:temporary password on a slide]]
- Receipt scanner at the front desk, serial [[FI-8170-A44271|dev:scanner serial number]]
- Practice EIN on file: [[74-3018852|taxid:EIN]]
# Week 1 checklist
- Signed Form W-9 and prior-year return
- QuickBooks Online accountant invite to the inbox above
- Payroll reports since [[January 1, 2026|date:start of period]]
- Loan statement for the equipment note, no. [[HCN-EQ-440187|rec:loan number]], balance about [[$186,000|money]]
'''))
