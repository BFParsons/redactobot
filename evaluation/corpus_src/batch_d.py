from corpus_src.dsl import D, dt, amt, num

DOCS = []

# ---------------------------------------------------------------- 61
DOCS.append(D(61, "txt", "trust administration notes", "legal", "US",
  title="Trust administration file notes - successor trustee calls",
  ents={"p1": "Renee Castellano", "p2": "Dmitri Volkov", "p3": "Ingrid Halvorsen-Pike",
        "p4": "Arvid T. Halvorsen", "p5": "Lars Halvorsen", "p6": "Soledad Marín",
        "p7": "Chase Whitlow", "p8": "Birgit Halvorsen", "p9": "Tammi (credit union representative)",
        "o1": "Halvorsen Family Revocable Trust", "o2": "Mercy Ridge Hospice",
        "o3": "Castellano & Bright LLP", "o4": "North Shore Federal Credit Union",
        "o5": "Pinecrest Wealth Partners", "o6": "Bethel Lutheran Church",
        "o7": "Gaelic Mutual Bank"},
  distractors=["Form 1041", "Form 706", "Minn. Stat. § 501C.0813", "Article VI", "Crummey", "Schedule K-1"],
  body=r'''
[[CASTELLANO & BRIGHT LLP|o3:caps]] -- TRUST ADMINISTRATION FILE NOTES
Matter: [[Halvorsen Family Revocable Trust|o1:full]] u/a/d [[June 3, 2009|date:trust date]]
File no. [[TR-2026-0318|rec:matter number]]      Atty: [[Renee Castellano|p1:full]]   Paralegal: [[Dmitri Volkov|p2:full]]

[[4/22/2026|date]] ([[RC|p1:initials]]) -- Intake call with successor trustee [[Ingrid Halvorsen-Pike|p3:full]],
the [[settlor's eldest daughter|indirect:family relationship to named person]]. Settlor [[Arvid T. Halvorsen|p4:full]] died
[[February 9, 2026|date:date of death]] at [[Mercy Ridge Hospice|o2:full]] in [[Duluth|place:city]]; he was [[age 94|age]].
His wife [[Birgit|p8:first-name]] predeceased him (d. [[11/30/2019|date:date of death]]). [[Ingrid|p3:first-name]] has the original
trust and the pour-over will. She does not have a death certificate yet; ordered six.
[[Mr. Halvorsen|p4:title-surname]]'s SSN per the old 1040 is [[250-96-2697|ssn]]. Trust has been using his
SSN; need a new EIN now that it is irrevocable. Explained the Form 1041 filing and
that a Form 706 is unlikely at this size, but we will confirm once values are in.

Assets she knows about:
  - Home at [[2207 Lakewood Terrace|addr]], [[Two Harbors|place:small town]], [[MN|place:state]] [[55616|zip]]. County
    estimated market value [[$412,300|money]]. No mortgage.
  - Cabin and 40 acres on [[Stewart Lake|place:lake / rural locality]], held in the trust since 2011. This is
    [[the only parcel with the old Halvorsen sawmill on it|indirect!:distinctive asset]]; [[Lars|p5:first-name]] wants it.
  - [[North Shore Federal Credit Union|o4:full]] checking, acct ending [[8841|acct!:last four only]], about
    [[$38,000|money]], and a share certificate, [[$75,000.00|money]], matures [[09/15/2026|date]].
    [[NSFCU|o4:acronym]] routing [[047096417|rtn]].
  - Brokerage at [[Pinecrest Wealth Partners|o5:full]], acct [[PWP-7730-22914|acct:brokerage account]], roughly
    [[$1.1 million|money!:amount with word scale]] at date of death. Adviser is [[Chase Whitlow|p7:full]]
    ([[cwhitlow@pinecrestwealth.example|email]], [[218.555.0116|phone:dotted]]). [[Chase|p7:first-name!:name that is also a common word]] says step-up
    statements will take two weeks.
  - An old account in [[Cork|place:city]] from when [[Arvid|p4:first-name]] worked there in the 1980s:
    [[Gaelic Mutual Bank|o7:full]], IBAN [[IE10 AIBK 0892 6394 9967 82|iban:spaced]], maybe [[EUR 9,400|money!:currency code before amount]].
    Nobody has touched it in years.
  - 2018 pickup, plate [[HLV 419|veh:license plate]], and a 19-ft aluminum boat, the "[[Birgit II|indirect!:named boat]]".

Beneficiaries under Article VI: Ingrid and her brother [[Lars Halvorsen|p5:full]], equal
shares, after specific gifts: [[$25,000|money]] to [[Bethel Lutheran Church|o6:full]] and
[[ten thousand dollars|money!:amount in words]] to his caregiver, [[Soledad Marín|p6:full]]. Ingrid mentioned that
Lars [[filed Chapter 13 in 2023|attr!:bankruptcy history]] and is [[in recovery from a gambling addiction|health:addiction]];
she asked whether his share can be held back. Told her the trust has a spendthrift
clause but no discretionary holdback; see Minn. Stat. § 501C.0813 on her duty to
inform. She is not to favor either beneficiary. The Crummey language is moot now.

[[4/24/2026|date]] ([[DV|p2:initials]]) -- Called NSFCU, spoke with "[[Tammi|p9:first-name!:first name only, in quotes]]" in member services
([[1-800-555-0177 x4402|phone!:toll-free with x extension]]). They need letters of trusteeship + death cert. to retitle.
Emailed Ingrid at [[ingrid.hp@lakemail.example|email]] the certification of trust for signature.
Her cell is [[(218) 555-0142|phone]]; she is in [[Grand Marais|place:small town]] Mon-Thu.

[[4/29/2026|date]] (RC) -- Lars called, upset. Says [[Ms. Marín|p6:title-surname]] "got Dad to change things" in
[[the last month at hospice|indirect:timing of event]] and that Dad had [[vascular dementia|health:diagnosis]] since at least 2024.
I told him we represent the trustee, not him, and that he may want his own lawyer.
He gave his number as [[218 555 0190|phone!:spaces only]] and said to stop emailing his sister
about "his" cabin. Note to file: the gift to Ms. Marín was added by the Third
Amendment dated [[January 12, 2026|date:amendment date]], four weeks before death. Need the
hospice chart and the notary's journal. Possible capacity issue; flag for [[Renee|p1:first-name]].

TO DO: EIN application; inventory within 60 days; Schedule K-1s at year end;
ask [[Whitlow|p7:surname!]] for date-of-death values; retainer [[$5,000|money]] received [[4/23/2026|date]], trust
acct ref. [[IOLTA-22-0457|rec:trust ledger reference]].
''',
))

# ---------------------------------------------------------------- 62
DOCS.append(D(62, "docx", "separation agreement draft", "legal", "US",
  title="Draft separation agreement and general release",
  ents={"p1": "Jordan A. Paris", "p2": "Maribel Ortiz-Vega", "p3": "Lucille Abernathy",
        "p4": "Desmond K. Oyelaran",
        "o1": "Brightwater Analytics, Inc.", "o2": "Feng & Abernathy, P.C.",
        "o3": "Oyelaran Employment Law, L.L.C.", "o4": "Front Range Mutual Health Plan"},
  distractors=["29 U.S.C. § 626(f)", "Section 409A", "Form W-2", "COBRA", "twenty-one (21) days",
               "Section 7", "Title VII", "seven (7) days"],
  body=r'''
# SEPARATION AGREEMENT AND GENERAL RELEASE
**DRAFT 3 - [[F&A|o2:acronym]] comments [[05/11/2026|date:draft date]] - PRIVILEGED AND CONFIDENTIAL - NOT FOR EXECUTION**
This Separation Agreement and General Release (the "Agreement") is entered into between [[Brightwater Analytics, Inc.|o1:full]], a [[Delaware|place:state of incorporation]] corporation with its principal office at [[3300 Arapahoe Parkway, Suite 410|addr]], [[Boulder|place:city]], [[Colorado|place:state]] [[80303|zip]] (the "Company"), and [[Jordan A. Paris|p1:full!:name made of ordinary words]] ("Employee"), residing at [[918 Juniper Court, Unit B|addr]], [[Longmont|place:city]], [[CO|place:state]] [[80501-4420|zip:ZIP+4]].
## 1. Separation
Employee's employment as Senior Data Engineer (Employee ID [[BW-004471|rec:employee ID]]) will end effective [[May 29, 2026|date:separation date]] (the "Separation Date"). Employee was hired on [[August 14, 2017|date:hire date]]. The Company will pay all wages earned through the Separation Date and accrued, unused paid time off in the gross amount of [[$3,912.44|money]], whether or not Employee signs this Agreement.
## 2. Severance
In exchange for the release in Section 4, the Company will pay Employee severance of [[$48,750.00|money]], equal to thirteen weeks of base salary, less applicable withholdings, reported on Form W-2. Payment will be made by direct deposit to the account on file ending in [[2205|acct!:last four only]] within ten business days after the Effective Date. The Company will also pay the employer share of COBRA premiums under the [[Front Range Mutual Health Plan|o4:full]] (member no. [[FRM-88204417-01|rec:health plan member ID]]) through [[November 30, 2026|date:benefits end date]], estimated at [[$1,187.20|money]] per month. The parties intend that payments be exempt from Section 409A.
## 3. Pending Charge
Employee filed Charge No. [[541-2026-01447|rec:agency charge number]] with the Equal Employment Opportunity Commission on [[March 3, 2026|date:filing date]], alleging that the Company denied his [[request for a reduced schedule|health!:disability accommodation request]] to accommodate [[multiple sclerosis|health:diagnosis]] and selected him for layoff because of his age. The Company denies these allegations. Employee agrees to request withdrawal of the charge within five days after the Effective Date. Nothing in this Agreement prevents Employee from communicating with any government agency or from exercising rights under Section 7 of the National Labor Relations Act.
## 4. General Release
Employee releases the Company and its officers, directors and affiliates from all claims arising through the date Employee signs, including claims under Title VII, the Americans with Disabilities Act, the Colorado Anti-Discrimination Act and the Age Discrimination in Employment Act. In compliance with 29 U.S.C. § 626(f), Employee acknowledges that he has been advised in writing to consult an attorney, has been given at least twenty-one (21) days to consider this Agreement, and may revoke it within seven (7) days after signing by written notice to [[Maribel Ortiz-Vega|p2:full]], Vice President, People, at [[mortizvega@brightwater-analytics.example|email]].
## 5. Return of Property
Employee will return by the Separation Date the Company laptop (serial no. [[C02ZK4QWMD6T|dev:laptop serial number]]), the security token (ID [[TKN-55-018822|dev:security token ID]]) and building badge no. [[40127|rec!:badge number, bare digits]]. Employee's network account ([[jparis|cred:username]]) will be disabled at 5:00 p.m. on the Separation Date. [[Ms. Ortiz-Vega|p2:title-surname]] has confirmed that Employee may keep the mobile phone ending [[0158|phone!:last four digits only]] after it is wiped.
## 6. References; Non-Disparagement
The Company will confirm dates of employment and last position held only. Inquiries are to be directed to [[M. Ortiz-Vega|p2:short:initial + surname]] at [[(720) 555-0103|phone]]. Neither party will disparage the other.
## 7. Attorneys' Fees
The Company will pay [[$6,500|money]] toward Employee's attorneys' fees directly to [[Oyelaran Employment Law, L.L.C.|o3:full]] (EIN [[84-3917720|taxid:EIN]]) upon receipt of a Form W-9.
## 8. Governing Law
This Agreement is governed by Colorado law. Venue lies in the District Court for [[Boulder County|place:county]].
## Drafting notes (delete before sending)
- [[LA|p3:initials]]: [[Jordan|p1:first-name!:name that is also a place]]'s counsel ([[Desmond K. Oyelaran|p4:full]], Colo. Atty. Reg. No. [[48817|govid!:attorney registration number, bare digits]], [[desmond@oyelaranlaw.example|email]]) wants 20 weeks, i.e. about [[75k|money!:shorthand k amount]]. Client authority is capped at [[$60,000|money]] all-in.
- [[Mr. Paris|p1:title-surname!:surname that is also a city]] turns 62 on [[July 8, 2026|dob!:birthday stated indirectly]]; check whether the pension bridge matters to him.
- Confirm with [[Brightwater|o1:short!]] payroll whether the last four of his SSN on the wage statement ([[xxx-xx-5807|ssn!:masked SSN]]) match the file. [[Oyelaran|p4:surname!]] says they do not.
- [[Lucille Abernathy|p3:full]], [[Feng & Abernathy, P.C.|o2:full]], direct [[303-555-0188|phone]].
''',
))

# ---------------------------------------------------------------- 63
DOCS.append(D(63, "pdf", "bankruptcy intake summary", "legal", "US",
  title="Chapter 7 intake summary - consumer debtor",
  ents={"p1": "Latoya R. Baptiste-Greene", "p2": "Marcus Greene", "p3": "Everett Pohl",
        "p4": "Nadia Rahimi", "p5": "Evelyn L. Marchetti",
        "o1": "Pohl Consumer Law Group", "o2": "Tallgrass Bank", "o3": "Meridian Auto Finance Co.",
        "o4": "St. Brendan Regional Medical Center", "o5": "Flint Hills Unified School District 383",
        "o6": "Sunflower Recovery Services LLC", "o7": "Konza Federal Credit Union"},
  distractors=["11 U.S.C. § 341", "Form 122A-1", "Schedule I", "Schedule J", "11 U.S.C. § 523(a)(8)",
               "Chapter 13"],
  body=r'''
# [[Pohl Consumer Law Group|o1:full]] - Bankruptcy Intake Summary
Prepared by [[Nadia Rahimi|p4:full]], paralegal, for [[Everett Pohl|p3:full]]. Intake interview [[06/02/2026|date:intake date]]. Internal file [[BK-26-0291|rec:matter number]].
## Debtor
[[BAPTISTE-GREENE, LATOYA R.|p1:last-first]] (goes by "[[Toya|p1:nickname]]"). Born [[17 Nov 1984|dob]]. SSN [[445 89 7758|ssn!:SSN with spaces]]. [[Kansas|place:state]] driver's license [[K04-71-9938|govid:driver's license]]. Lives at [[1146 Poyntz Circle, Apt 3C|addr]], [[Manhattan|place:city]], [[KS|place:state]] [[66502|zip]]; renting since [[March 2024|date!:month and year only]]. Phone [[785-555-0129|phone]], email [[toya.bg84@inboxmail.example|email]]. Married, [[separated from her husband|indirect:family status]] [[Marcus Greene|p2:full]], who is not filing. Two dependents, ages 9 and 13.
## Employment and income
Paraprofessional at [[Flint Hills Unified School District 383|o5:full]] since [[08/12/2019|date:hire date]]; employee no. [[E-20714|rec:employee ID]]. Gross pay [[$2,684.00|money]] per month over ten months. Receives child support of [[$450|money]] a month, irregularly. [[Mr. Greene|p2:title-surname]] is [[currently incarcerated|attr:criminal justice status]] at the [[Riley County|place:county]] Jail, so do not count his income on Form 122A-1. She is below median for a household of three; no presumption of abuse.
## Why she is filing
Wage garnishment by [[Sunflower Recovery Services LLC|o6:full]] started [[May 15, 2026|date]] on a judgment of [[$7,912.36|money]] ([[Riley County|place:county]] District Court, Case No. [[2025-LM-000847|rec:court case number]]). Most of the unsecured debt is medical, from treatment for [[stage II breast cancer|health:diagnosis]] in 2024 at [[St. Brendan Regional Medical Center|o4:full]], when she had no coverage for four months.
## Debts
| Creditor | Account | Balance |
| [[Tallgrass Bank|o2:full]] | [[...4417|card!:card, last four with dots]] | [[$18,204.11|money]] |
| [[Meridian Auto|o3:short!]] | [[MAF-2291077|rec:loan number]] | [[$11,860.00|money]] |
| [[St. Brendan|o4:short!]] | [[SB-00918824|rec:patient account number]] | [[$23,447.90|money]] |
| [[Sunflower|o6:short!]] | judgment | [[$7,912.36|money]] |
| Student loans | 4 loans | [[$31,250|money]] |
Student loans are federal and will not be discharged; see 11 U.S.C. § 523(a)(8).
## Assets
Vehicle financed through [[Meridian Auto Finance Co.|o3:full]]: 2019 compact SUV, VIN [[5NMS33AD7KH041926|veh:VIN]], Kansas plate [[417 MTK|veh:license plate]], value about [[$9,500|money]]. She wants to reaffirm; payment is [[$318.74|money]] a month. Checking and savings at [[Konza Federal Credit Union|o7:full]], member no. [[0061-22804|acct:credit union member number]], combined balance [[$612.09|money]] on the intake date. Expects a tax refund of roughly [[1,900 dollars|money!:amount with the word dollars]]. No real estate. Household goods under exemption limits. Her grandmother's ring, appraised at [[$2,200|money]], is exempt.
## Prior filings and other flags
- Prior Chapter 13 filed jointly with [[Marcus|p2:first-name]], Case No. [[18-40662|rec:bankruptcy case number]], dismissed [[10/04/2019|date]] for missed plan payments. More than eight years is not required here because the earlier case ended without a discharge.
- She transferred a 2011 pickup to [[her brother|indirect:family relationship]] in [[Junction City|place:city]] in [[January 2026|date!:month and year only]] for [[$1,000|money]]. Disclose on the statement of financial affairs.
- Credit counseling certificate no. [[01356-KS-CC-039114477|rec:certificate number]], completed [[06/01/2026|date]].
## Next steps
File the petition, Schedule I and Schedule J by [[June 19, 2026|date:target filing date]] to stop the garnishment before the next pay date. Expect assignment to [[Judge Marchetti|p5:title-surname]] ([[Hon. Evelyn L. Marchetti|p5:full]]) and a meeting of creditors under 11 U.S.C. § 341 about five weeks later. Fee: [[$1,450|money]] plus the [[$338|money]] filing fee; she paid [[$400|money]] today by debit card ending [[9192|card!:last four only]]. [[Mr. Pohl|p3:title-surname]], Kan. S. Ct. No. [[22715|govid!:bar number, bare digits]], to sign.
''',
))

# ---------------------------------------------------------------- 64
DOCS.append(D(64, "txt", "criminal defense case notes", "legal", "US",
  title="DUI defense case notes",
  ents={"p1": "Hunter Brannigan", "p2": "Dale Yazzie", "p3": "Georgia Tsosie", "p4": "Colleen Abernethy-Ruiz",
        "p5": "Wendell Begaye", "p6": "Raúl Quintero",
        "o1": "Ponderosa Aggregate Hauling LLC", "o2": "Abernethy-Ruiz Defense, PLLC",
        "o3": "High Country Towing & Recovery", "o4": "SafeStart Interlock of Northern Arizona"},
  distractors=["A.R.S. § 28-1381(A)(1)", "A.R.S. § 28-1382", "Rule 15.1", "HGN", "Intoxilyzer 9000", "Miranda",
               "MVD", "Form 40-5807"],
  ok=["28-1381", "28-1382"],
  body=r'''
[[ABERNETHY-RUIZ DEFENSE, PLLC|o2:caps]]
CASE NOTES -- PRIVILEGED / WORK PRODUCT

Client:   [[Hunter Brannigan|p1:full!:first name is a common word]]   DOB [[09/27/1991|dob]]
Court:    [[Flagstaff|place:city]] Justice Court, [[Coconino County|place:county]], No. [[CR-2026-004417|rec:criminal case number]]
Citation: [[AZ0301-7781245|rec:citation number]]
Charges:  A.R.S. § 28-1381(A)(1) (impaired to slightest degree), A.R.S. § 28-1382 (extreme)
Atty:     [[Colleen Abernethy-Ruiz|p4:full]] ([[CAR|p4:initials]]), State Bar No. [[031774|govid:state bar number]]

6/8/26 -- initial consult ([[CAR|p4:initials]])
[[Hunter|p1:first-name!:name that is also a common word]] was stopped Saturday [[May 30, 2026|date:arrest date]] around 11:40 pm on
[[Route 66 near Fanning Drive|place:road location]] by DPS Trooper [[Dale Yazzie|p2:full]], badge [[#6193|govid!:badge number]], for
drifting over the fog line. He was driving his own truck, a 2017 three-quarter-ton
pickup, AZ plate [[CKD7R42|veh:license plate]], VIN [[1FT7W2BT4HEC30918|veh:VIN]]. Passenger was [[his girlfriend|indirect:relationship to named person]],
[[Georgia Tsosie|p3:full!:first name is also a place]]. [[Yazzie|p2:surname!]] says odor of alcohol, bloodshot eyes, six of six
clues on HGN. Hunter says he had "three beers at [[Georgia|p3:first-name!:name that is also a place]]'s cousin's
graduation" and that the field tests were done on a gravel shoulder in the wind.

Breath test on the Intoxilyzer 9000 at the [[Coconino County|place:county]] jail: [[0.158|health!:breath alcohol result]] and
[[0.151|health!:breath alcohol result]], 12:52 and 12:59 am. That is extreme by a hair. Need the
maintenance and calibration logs and the 15-minute deprivation video.

Priors: [[one prior DUI in 2019 in Mohave County|attr:criminal history]] (pled to regular DUI, completed
classes). That is within 84 months, so this is charged as a second offense.
Exposure is real jail. Also on file: [[a 2012 juvenile adjudication for shoplifting|attr!:juvenile record]],
not usable.

Health: Hunter is [[a Type 1 diabetic on an insulin pump|health:diagnosis and device]]. He says his
sugar was low that night ([[he read 58 on his meter|health!:glucose reading]] at the jail) and nobody
would let him eat. Hypoglycemia can mimic impairment and ketones can affect some
breath machines; ask [[Dr. Quintero|p6:title-surname]] ([[Raúl Quintero|p6:full]], endocrinology) for
records and whether he will testify. Pump serial no. [[NG2187443H|dev:medical device serial]] in case we
need the data download.

Work: he holds a CDL (AZ license [[D08841276|govid:driver's license]]) and drives belly dumps for
[[Ponderosa Aggregate Hauling LLC|o1:full]]. A conviction means a one-year CDL
disqualification even though he was in his personal vehicle. His dispatcher,
[[Wendell Begaye|p5:full]], does not know yet. Hunter is [[an enrolled member of the Navajo Nation|attr:tribal membership / ethnicity]]
and asked about treatment options through tribal services; will check.

Truck was towed to [[High Country Towing & Recovery|o3:full]], [[4410 E. Huntington Dr.|addr]], lot
ticket [[HC-118834|rec:tow ticket number]]. Storage is running [[$45|money]] a day. 30-day impound unless
we get an early release hearing.

MVD: admin per se suspension. He was handed the pink Form 40-5807 on [[5/31/26|date!:two-digit year]]; the 15-day
window to request a hearing ends [[June 15|date!:no year]]. FILE THE HEARING REQUEST MONDAY.

[[6/9/26|date!:two-digit year]] -- [[CAR|p4:initials]]
Discovery request under Rule 15.1 sent. Body-cam is on the state portal:
[[https://evidence.azdps.example/share/7f3a91c2|url:evidence share link]]   login [[car_defense|cred:username]] / pw [[Monsoon#2291|cred!:password in notes]]
Watched the first 20 min. No Miranda before the "how much have you had" questions
at the tailgate, but he was not in custody yet. Yazzie tells Hunter to "quit
fidgeting with that thing on your belt" -- that is the pump. Good for us.

[[Ms. Tsosie|p3:title-surname]] called ([[nine two eight, 555-0164|phone!:area code spelled out]]). She will say he seemed fine but
shaky. She does not want to testify if [[her ex|indirect:relationship]] finds out where she was.

Fees: flat [[$6,000|money]] through trial in justice court, [[2,500|money!:bare number, no currency sign]] paid on [[6/8/26|date!:two-digit year]]
(Visa ending [[8203|card!:last four only]]), balance in three payments. Bond was [[$1,500|money]] cash,
posted by [[his mother|indirect:family relationship]].

If convicted he will need an interlock for 12 months. [[SafeStart Interlock of Northern Arizona|o4:full]]
quoted [[$89/mo|money!:monthly rate with slash]]. Client contact: [[hbrannigan91@postbox.example|email]], cell [[928.555.0137|phone:dotted]].
Mail to [[PO Box 2204|addr:PO Box]], [[Bellemont|place:small town]], [[AZ|place:state]] [[86015|zip]].
''',
))

# ---------------------------------------------------------------- 65
DOCS.append(D(65, "eml", "email thread", "legal", "CA", enc="multipart",
  title="Email thread - residential purchase closing (Manitoba)",
  ents={"p1": "Anneliese Friesen", "p2": "Gurpreet Dhaliwal", "p3": "Harjit Kaur Dhaliwal",
        "p4": "Tyler Kowalchuk", "p5": "Odette Lavallée", "p6": "Stefan (realtor, surname not given)",
        "o1": "Friesen Tkachuk Law Office", "o2": "Assiniboine Prairie Credit Union",
        "o3": "Red River Realty Group Inc.", "o4": "Lavallée & Partners LLP"},
  distractors=["The Real Property Act", "Land Transfer Tax", "Schedule A", "FINTRAC"],
  ok=["3:00"],
  headers={
    "From": "[[Anneliese Friesen|p1:full]] <[[afriesen@friesentkachuk.example|email]]>",
    "To": '"[[Dhaliwal, Gurpreet|p2:last-first]]" <[[gurpreet.dhaliwal@prairiemail.example|email]]>',
    "Cc": "[[harjit.k.dhaliwal@prairiemail.example|email]], [[closings@friesentkachuk.example|email:shared mailbox]]",
    "Subject": "RE: [[418 Lanark Street|addr]] - closing [[June 26|date!:no year]] - funds and ID (our file [[26-1187 RE|rec:file number]])",
    "Date": "Wed, [[17 Jun 2026|date]] 16:42:09 -0500",
  },
  body=r'''
Hi [[Gurpreet|p2:first-name]] and [[Harjit|p3:first-name]],

Thanks for sending the IDs. A few things before closing on Friday, [[June 26, 2026|date:closing date]].

1. BALANCE TO CLOSE. Purchase price is [[$489,900.00|money]]. Your deposit of [[$20,000|money]] is held
by [[Red River Realty Group Inc.|o3:full]] in trust. The mortgage advance from
[[Assiniboine Prairie Credit Union|o2:full]] is [[$391,920.00|money]] (mortgage no. [[APCU-M-0077418|rec:mortgage number]]). After Land Transfer
Tax of [[$7,726.00|money]], our fees and disbursements of [[$1,684.35|money]], and adjustments for
property taxes, the amount we need from you is [[C$88,310.72|money:Canadian dollar prefix]].

2. HOW TO SEND IT. Bank draft payable to "[[Friesen Tkachuk Law Office|o1:full]], in trust",
or wire to our trust account:
     Institution [[879|acct!:institution number]]   Transit [[00417|acct!:transit number]]   Account [[1004-882-6|acct:trust account number]]
     SWIFT (only if your bank asks): [[APCUCAW1|acct:SWIFT code]]
PLEASE phone me at [[204-555-0119|phone]] to confirm these numbers before you send anything.
We will never change wire instructions by email. Last month a client of another
firm received a fake "updated instructions" message that our IT person traced to
[[203.0.113.57|ip:IPv4]]; if you get anything like that, call.

3. ID / FINTRAC. I have your licences. Harjit, the passport scan you sent
([[Z4471902|govid:passport number]]) is cut off at the bottom; can you resend? Also please confirm
dates of birth as I have them: Gurpreet [[1988-02-19|dob:ISO format]], Harjit [[1990-11-03|dob:ISO format]], and
your SINs for the lender's forms. Gurpreet's I have as [[548 275 650|taxid:SIN with spaces]]; I do not
have Harjit's. Do NOT email it; call [[Tyler|p4:first-name]] at ext. 204.

4. TITLE. Title no. [[3304417/1|rec:land title number]], [[Winnipeg|place:city]] Land Titles District. There is a
caveat from 1962 for a utility easement along the lane, which is normal. Roll no.
[[12-0-044718-0|rec:property tax roll number]]. The sellers' lawyer, [[Odette Lavallée|p5:full]] at [[Lavallée & Partners LLP|o4:full]],
confirms vacant possession at 3:00 p.m.

5. Since Harjit is [[here on a work permit and not yet a permanent resident|attr:immigration status]], the lender
wants a copy of the permit as part of Schedule A. That is their rule and has
nothing to do with The Real Property Act.

Signing appointment: Tuesday [[June 23|date!:no year]] at 4:15, our office, [[1210-363 Broadway|addr:suite-first Canadian style]],
[[Winnipeg|place:city]] [[MB|place:province]]  [[R3C 3N9|zip:Canadian postal code]]. Parking is off [[Carlton Street|place:street]].

[[Anneliese|p1:first-name]]

[[Anneliese Friesen|p1:full]] | Partner
[[Friesen Tkachuk Law Office|o1:full]]
T [[204-555-0119|phone]]  F [[204-555-0120|phone:fax]]
Law Society of [[Manitoba|place:province]] no. [[20071148|govid:law society number]]
Assistant: [[Tyler Kowalchuk|p4:full]], [[tkowalchuk@friesentkachuk.example|email]]

> On Tue, [[Jun 16, 2026|date]] at 9:03 PM [[Gurpreet Dhaliwal|p2:full]] wrote:
>
> Hi [[Ms. Friesen|p1:title-surname]],
> Attached are both drivers licences. Mine is [[DH-AL-IW-G512KD|govid:driver's licence]]. [[Harjit Kaur|p3:short:given names without surname]]'s is
> under her maiden name still, hope thats ok. Our realtor [[Stefan|p6:first-name]] said the
> sellers want to move closing up a day?? We cant, the movers are booked and
> [[my mother is flying in from Amritsar|indirect!:family event]] on the 25th. Also can you tell me the
> exact amount, the bank says they need 2 days for a draft over [[50k|money!:shorthand k amount]].
> My cell is [[204 555 0173|phone!:spaces only]] if easier. We are still at [[55 Nassau St N apt 1407|addr:lower-case apt]]
> until the 27th.
> thx
> Gurpreet
>
> Sent from my phone
''',
))

# ---------------------------------------------------------------- 66
DOCS.append(D(66, "txt", "deposition summary", "legal", "US", length="long",
  title="Deposition summary - defendant surgeon, medical malpractice / wrongful death",
  ents={"p1": "Anand Krishnamurthy", "p2": "Clarence J. Thibodeaux Jr.", "p3": "Earline Thibodeaux",
        "p4": "Monique Thibodeaux-Arceneaux", "p5": "Beau Landry", "p6": "Patricia Nwosu-Hebert",
        "p7": "Simone Fontenot-Reyes", "p8": "Kim-Ly Tran", "p9": "Gerald Broussard",
        "p10": "Janelle Guidry", "p11": "Howard Weiss", "p12": "Odile Thibodeaux", "p13": "Theo Castille",
        "o1": "Bayou Teche Surgical Associates, APMC", "o2": "Our Lady of the Bayou Medical Center",
        "o3": "Landry & Castille, L.L.C.", "o4": "Dugas Nwosu-Hebert LLP",
        "o5": "Pelican Physicians Mutual Insurance Co.", "o6": "Atchafalaya Pipe & Supply Co.",
        "o7": "Acadiana Court Reporters, Inc.", "o8": "Estate of Clarence J. Thibodeaux Jr.",
        "o9": "St. Landry Parish Kingdom Hall"},
  distractors=["La. R.S. 40:1231.8", "La. C.C.P. art. 1443", "Calot's triangle", "Exhibit 7", "ERCP",
               "CPT 47562", "Rule 30(b)(6)", "Strasberg", "HIDA scan", "POD 2"],
  body=r'''
[[LANDRY & CASTILLE, L.L.C.|o3:caps]]
ATTORNEY WORK PRODUCT -- DEPOSITION SUMMARY

Case:       [[ESTATE OF CLARENCE J. THIBODEAUX JR.|o8:caps]], through its administratrix
            [[EARLINE THIBODEAUX|p3:caps]], et al. v. [[BAYOU TECHE SURGICAL ASSOCIATES, APMC|o1:caps]], et al.
Court:      15th Judicial District Court, [[Lafayette Parish|place:parish]], [[Louisiana|place:state]]
Docket:     No. [[C-2025-4471, Div. K|rec:docket number with division]]
Our file:   [[LC-24-0933|rec:matter number]]
Deponent:   [[Anand Krishnamurthy|p1:full]], M.D. (defendant)
Taken:      Thursday, [[July 9, 2026|date:deposition date]], 9:38 a.m. to 4:52 p.m.
Place:      [[Acadiana Court Reporters, Inc.|o7:full]], [[600 Jefferson Street, Suite 1150|addr]], [[Lafayette|place:city]], [[LA|place:state]] [[70501|zip]]
Reporter:   [[Janelle Guidry|p10:full]], CCR No. [[2011-0447|govid:court reporter certificate number]]
Appearing:  [[Beau Landry|p5:full]] and [[Theo Castille|p13:full]] for plaintiffs;
            [[Patricia Nwosu-Hebert|p6:full]], [[Dugas Nwosu-Hebert LLP|o4:full]], for Dr. Krishnamurthy and [[BTSA|o1:acronym]]
Transcript: 241 pages. Summary prepared [[7/16/2026|date]] by [[TC|p13:initials]].

BOTTOM LINE
[[Dr. Krishnamurthy|p1:title-surname]] concedes he did not obtain a critical view of safety before
clipping, did not convert to open, and did not personally see the patient on
POD 2 despite two calls from nursing. He blames the delay on the hospitalist
and on the family's refusal of blood. He was a poor witness after lunch. The
alcohol-treatment history came in over objection and he was visibly rattled.

1. BACKGROUND AND CREDENTIALS (pp. 6-41)

Born in [[Chennai|place:city of birth]]; came to the United States in 1998; [[naturalized U.S. citizen since 2009|attr:citizenship status]]
(11:4-12). Medical school abroad, residency at a university program in
[[Shreveport|place:city]]. Louisiana license no. [[MD.204417|govid:medical license number]]; NPI [[1740388215|govid:NPI]]; DEA registration
[[FK4471826|govid:DEA number]] (14:2-15:9). Board certified in general surgery, recertified 2019.
Joined [[Bayou Teche Surgical Associates, APMC|o1:full]] in [[August 2012|date!:month and year only]]; became a shareholder in
2016. Senior partner is Dr. [[Gerald Broussard|p9:full]], whom everyone calls "[[Gerry|p9:nickname]]" (22:1).

He performs "roughly 150 to 180" laparoscopic cholecystectomies a year (CPT 47562).
He admitted one prior bile duct injury, in 2018, which was "recognized on the
table and repaired" (27:14-29:3). That claim, he agreed, was settled by his
carrier in 2019 for [[$350,000|money]] without a panel opinion (30:6-22). [[Ms. Nwosu-Hebert|p6:title-surname]]
objected; instruction not to answer was withdrawn after we cited La. C.C.P. art. 1443.

Insurance: [[Pelican Physicians Mutual Insurance Co.|o5:full]], policy no. [[PPM-LA-0092817|rec:insurance policy number]], limits
[[$1 million|money!:amount with word scale]] per claim. He is a qualified provider under La. R.S. 40:1231.8, so
the cap applies. He does not know whether [[Pelican|o5:short!]] has reserved the claim (33:1-9).

Health and fitness for duty (34:12-41:20). Over a continuing objection he
testified that he [[completed a 90-day residential program for alcohol dependence|health:substance use treatment]] in
early 2021 under a monitoring agreement with the state physicians' health program,
that the agreement ran five years, and that it was still in force on the date
of surgery. He denies any relapse. He agreed that his privileges at
[[Our Lady of the Bayou Medical Center|o2:full]] were "voluntarily restricted" for eleven weeks in 2021.
He takes [[naltrexone 50 mg daily|health:medication and dose]] (39:7). He said random screens were all negative; we
have not seen them. FOLLOW UP: subpoena the monitoring file.

2. THE PATIENT (pp. 42-67)

[[Clarence J. Thibodeaux Jr.|p2:full]], known as "[[Boo|p2:nickname]]," DOB [[04/02/1958|dob]], hospital MRN [[OLB-00381127|rec:medical record number]],
of [[1187 Bayou Tortue Road|addr]], [[Youngsville|place:town]], LA [[70518|zip]]. Retired after 31 years as a
machinist at [[Atchafalaya Pipe & Supply Co.|o6:full]]; Army veteran. History of [[type 2 diabetes|health:diagnosis]],
[[atrial fibrillation on apixaban|health:diagnosis and medication]], and [[BMI of 37|health!:body mass index]] (Exhibit 7, H&P). The witness first
saw [[Mr. Thibodeaux|p2:title-surname]] in clinic on [[January 6, 2025|date:clinic visit]] for [[symptomatic gallstones|health:diagnosis]] on referral
from his PCP.

The witness knew from the intake sheet that Mr. Thibodeaux and his wife are
[[Jehovah's Witnesses|attr:religion]] and that he carried a signed refusal of blood products
(48:3-49:17). He agreed the refusal covered whole blood and red cells but not
albumin or cell salvage, and that he "did not get into those details" at the
consent visit. He did not call the liaison committee at the [[St. Landry Parish Kingdom Hall|o9:full]]
although the family asked him to (51:2).

Consent was signed [[January 20, 2025|date]]. Apixaban was held 48 hours. He does not recall
discussing conversion to open or bile duct injury specifically; the form lists
both (53:10-56:1).

3. THE OPERATION -- [[JANUARY 23, 2025|date!:date in capitals]] (pp. 68-121)

Surgery at [[OLB|o2:acronym]] main OR, room 6, in-room 7:42 a.m., incision 8:09, close 9:31.
Assisted by a first-year PA whose name he could not recall. No cholangiogram:
"I do them selectively" (74:8). He described "a fair amount of inflammation" in
Calot's triangle and agreed that his operative note does not use the words
"critical view" (79:1-81:15). He placed two clips on what he believed was the
cystic duct and divided it. Shown the still images ([[Landry|p5:surname!]] Exhibits 11-14), he
agreed that the structure "could be" the common duct and that its diameter on
image 13 "looks larger than I remembered" (88:20-90:6).

He agreed with Dr. [[Howard Weiss|p11:full]]'s report that the injury is a Strasberg class E2
transection, but not that it was below the standard of care: "it is a known
complication" (97:3). Asked why he did not convert or call [[Dr. Broussard|p9:title-surname]], who
was operating next door: "In hindsight I would have" (101:12).

EHR audit log (Exhibit 19). The operative note was created at 9:58 a.m. under
user ID [[akrishnamurthy2|cred:EHR username]] from workstation [[OR6-WS02|dev:workstation name]], IP [[10.44.6.112|ip:private IPv4]], and was amended
at 6:14 a.m. on [[1/26/2025|date]], after the transfer, from a remote session at
[[198.51.100.23|ip:IPv4]]. The amendment added the sentence "anatomy clearly identified."
He says he was "cleaning up dictation" from home (112:5-118:22). This is the
best material in the transcript.

4. POST-OPERATIVE COURSE (pp. 122-198)

Discharged home same day at 1:15 p.m. Returned to the ED the next evening,
[[January 24|date!:no year]], with pain and vomiting; admitted to the hospitalist service under
Dr. [[Simone Fontenot-Reyes|p7:full]]. Labs that night: [[WBC 19.4|health:lab result]], [[total bilirubin 4.8|health:lab result]],
[[lactate 3.1|health:lab result]] (Exhibit 22).

[[Nurse Tran|p8:title-surname]] ([[Kim-Ly Tran|p8:full]], RN) charted calls to the witness's cell, [[337-555-0181|phone]], at
10:52 p.m. and 2:17 a.m. He remembers one call, not two, and says he ordered a
HIDA scan "for the morning" (131:4-134:9). His phone records (Exhibit 24) show
both calls connected, 3 min and 1 min. He was not on call; Gerry was. He did
not come in. He first examined the patient at about 11:30 a.m. on [[January 25|date!:no year]],
some 26 hours after readmission (140:2).

By then the patient was [[septic|health:condition]], with a [[hemoglobin of 6.9|health:lab result]]. The family, through
[[Mrs. Thibodeaux|p3:title-surname]] and [[their daughter|indirect:family relationship]] [[Monique Thibodeaux-Arceneaux|p4:full]], declined transfusion. The
witness testified that "if they had let us give blood he would be alive"
(152:11). On cross by [[Mr. Landry|p5:title-surname]] he agreed that the bleeding followed the
bile leak, that the leak followed the transection, and that no one offered
cell salvage or erythropoietin (155:1-158:16). He conceded [[Dr. Fontenot-Reyes|p7:title-surname]]
asked him twice for a surgical decision before ERCP was arranged.

Transfer to a tertiary center in [[New Orleans|place:city]] was requested at 4:40 p.m. on
the 25th and accepted at 9:05 p.m.; the patient left by ground at 1:20 a.m.
He died on [[January 29, 2025|date:date of death]] of [[biliary sepsis and multi-organ failure|health:cause of death]] (death
certificate, Exhibit 31). He was 66.

The witness did not attend the funeral and has not spoken with the family.
He learned from [[Earline|p3:first-name]]'s pastor -- he corrected himself, "her elder" -- that
[[the decedent's mother|indirect:family relationship to named person]], [[Odile Thibodeaux|p12:full]], who is [[92|age!:bare age]], had been living with the
couple and depended on [[Clarence|p2:first-name]]'s pension (171:9). [[Monique|p4:first-name]] now cares for her.

5. DAMAGES-RELATED TESTIMONY (pp. 199-214)

He agreed the hospital bill at OLB was [[$84,219.57|money]] and that the tertiary
center billed [[$212,400|money]] (Exhibits 33-34). He does not dispute funeral
expenses of [[$11,875.00|money]]. He has no opinion on lost pension income, which our
economist puts at about [[19k|money!:shorthand k amount]] a year.

6. MISCELLANEOUS (pp. 215-241)

- He reviewed his own notes, the [[Weiss|p11:surname!]] report and "some texts" before testifying.
  The texts are with [[Broussard|p9:surname!]] on the night of the 24th. Not produced. We
  demanded them on the record (217:3); [[Patricia|p6:first-name]] agreed to "look into it."
- BTSA's tax ID appears on Exhibit 33 as [[72-1408856|taxid:EIN]]; the billing address is
  [[P.O. Box 53310|addr:PO Box]], Lafayette, LA [[70505-3310|zip:ZIP+4]].
- He has never been deposed under Rule 30(b)(6) and does not know who BTSA's
  records custodian is.
- Read and sign reserved. Errata due 30 days after receipt.

TO DO ([[BL|p5:initials]] / TC)
1. Motion to compel the Broussard texts and the monitoring file.
2. Forensic image of the home computer; subpoena the ISP for 198.51.100.23.
3. Depose Dr. Fontenot-Reyes and [[Ms. Tran|p8:title-surname]] before the panel submission deadline,
   [[September 30, 2026|date:deadline]].
4. Ask [[Dr. Weiss|p11:title-surname]] to address cell salvage and the blood-refusal liaison issue.
5. Send [[Mrs. T|p3:short!:title + initial]] a short update; she prefers calls to [[(337) 555-0126|phone]] after 5.
''',
))

# ---------------------------------------------------------------- 67
DOCS.append(D(67, "rtf", "court filing draft - declaration", "legal", "US",
  title="Draft declaration in support of petition for domestic violence protection order",
  ents={"p1": "Marisol Echevarría-Lund", "p2": "Trevor J. Lund", "p3": "Paloma Lund",
        "p4": "Ines Echevarría", "p5": "Dawn Okimoto", "p6": "Reggie Tate",
        "o1": "Cascade Family Dental", "o2": "Eastside Legal Aid Clinic", "o3": "Harborview Urgent Care - Renton",
        "o4": "Little Cedars Montessori"},
  distractors=["RCW 7.105.100", "RCW 9A.72.085", "Exhibit A", "Exhibit B", "GR 22"],
  body=r'''
SUPERIOR COURT OF [[WASHINGTON|place:state in capitals]] FOR [[KING COUNTY|place:county in capitals]]
**In re: [[MARISOL ECHEVARRÍA-LUND|p1:caps]], Petitioner, and [[TREVOR J. LUND|p2:caps]], Respondent.**
No. [[26-2-11847-3 KNT|rec:court case number]]
# DECLARATION OF PETITIONER IN SUPPORT OF PETITION FOR PROTECTION ORDER (RCW 7.105.100)
**DRAFT - prepared with [[Eastside Legal Aid Clinic|o2:full]], advocate [[Dawn Okimoto|p5:full]], [[6/22/2026|date:draft date]]. Petitioner's residential address is confidential under GR 22 and must not appear in the filed version.**
I, [[Marisol Echevarría-Lund|p1:full]], declare as follows:
1. I am the Petitioner. I am 34 years old. My date of birth is [[October 5, 1991|dob]]. Respondent, [[Trevor J. Lund|p2:full]], is [[my husband|indirect:relationship to named person]]. His date of birth is [[2/11/1987|dob]]. We married in 2018 and separated on [[May 2, 2026|date:separation date]]. We have one child together, [[Paloma|p3:first-name]], who is [[six years old and in kindergarten|indirect!:child's age and grade]] at [[Little Cedars Montessori|o4:full]].
2. I am asking for protection for myself and for Paloma. Since [[May 2|date!:no year]] I have been staying with [[my sister|indirect:family relationship]], [[Ines Echevarría|p4:full]], in [[Kent|place:city]]. Before that we lived together at [[23418 114th Place SE|addr]], [[Renton|place:city]], [[WA|place:state]] [[98031|zip]]. [[Trevor|p2:first-name]] still lives there.
3. **Most recent incident.** On the night of Friday, [[June 12, 2026|date:incident date]], Trevor came to [[Ines|p4:first-name]]'s apartment at about 11:15 p.m. He pounded on the door and yelled that he would "burn the place down" if I did not bring Paloma out. He was driving his gray pickup, Washington plate [[C81 447K|veh:license plate with space]]. Ines's neighbor, [[Reggie Tate|p6:full]], saw him and called 911. [[Kent|place:city]] Police responded (incident no. [[26-0041877|rec:police incident number]]) but Trevor had left.
4. **Text messages.** Between [[June 12|date!:no year]] and [[June 19, 2026|date]] Trevor sent me 141 text messages from his number, [[(425) 555-0155|phone]], and from a second number I did not recognize, [[206.555.0108|phone:dotted]]. Screenshots are attached as Exhibit A. They include: "you cant hide at [[ines|p4:first-name!:lower-case name in quoted text]] place forever," "I know what time you get off," and a photo of the front door of my work.
5. **Physical violence.** On [[April 18, 2026|date:incident date]], during an argument about money, Trevor grabbed my left arm and twisted it behind my back. I was treated the next morning at [[Harborview Urgent Care - Renton|o3:full]] for [[a fractured left wrist|health:injury]] (visit no. [[UC-3391047|rec:clinic visit number]]). I told the provider I had fallen. That was not true. I was afraid of what he would do if he was arrested. Records are attached as Exhibit B. I was [[eleven weeks pregnant|health!:pregnancy]] at the time; I [[miscarried|health!:pregnancy loss]] on [[April 30|date!:no year]].
6. **Firearms.** Trevor owns at least two firearms: a 9mm handgun, serial number [[BFKR447|dev!:firearm serial number]], which he keeps in the truck console, and a hunting rifle. In March he placed the handgun on the kitchen table during an argument and said, "This is how it ends."
7. **Substance use and history.** Trevor [[has used methamphetamine|health:substance use]] on and off since 2023. He has [[a 2021 conviction for assault in the fourth degree|attr:criminal history]] involving a former girlfriend in [[Pierce County|place:county]]. He lost his job as a longshoreman in January and blames me.
8. **Surveillance.** On [[June 15|date!:no year]] I found a tracking device taped under the rear bumper of my car, a blue 2015 hatchback, plate [[BXT9920|veh:license plate]]. The device ID printed on it is [[TG-88-41C7-0093|dev:tracker device ID]]. Trevor also knows the passcode to my phone ([[0513|cred!:phone passcode]], Paloma's birthday) and my email password. I have since changed both.
9. **My work.** I am a dental hygienist at [[Cascade Family Dental|o1:full]], [[410 Rainier Avenue South, Suite B|addr]], Renton. Trevor has come to the parking lot twice since we separated. I ask that he be ordered to stay 1,000 feet away from my work, from Ines's home, and from Paloma's school.
10. **Immigration.** Trevor has told me many times that he will "call immigration" on me and on my mother. I am [[a lawful permanent resident|attr:immigration status]]; my card number is [[A-204-417-883|govid:alien registration number]]. My mother [[has a pending asylum case|attr:immigration status of relative]]. I am afraid for her.
11. I can be reached through my advocate, [[Ms. Okimoto|p5:title-surname]], at [[206-555-0170 ext. 12|phone:with extension]] or [[dokimoto@eastsidelegalaid.example|email]]. Please do not send mail to the [[Renton|place:city]] house.
I declare under penalty of perjury under the laws of the State of [[Washington|place:state]] (RCW 9A.72.085) that the foregoing is true and correct.
Signed at [[Kent|place:city]], Washington on ____________, 2026.
______________________________
[[Marisol Echevarría-Lund|p1:full]], Petitioner
''',
))

# ---------------------------------------------------------------- 68
DOCS.append(D(68, "html", "IRS correspondence summary", "accounting", "US",
  title="IRS correspondence summary - examination and innocent spouse claim",
  ents={"p1": "Yolanda Prescott-Adeyemi", "p2": "Babatunde Adeyemi", "p3": "Winston Achebe",
        "p4": "Kowalczyk (IRS examiner)", "p5": "Lorraine Sato",
        "o1": "Larkspur Tax & Advisory, LLC", "o2": "Adeyemi Freight Brokers Inc.",
        "o3": "Great Miami Savings Bank", "o4": "Sycamore Counseling Associates"},
  distractors=["Form 8857", "Form 4549", "Letter 566", "IRC § 6015(c)", "Form 2848", "Schedule C", "IRC § 6662(a)",
               "Publication 971", "Form 1099-K", "CP2000"],
  body=r'''
# IRS correspondence summary
**Client:** [[Yolanda Prescott-Adeyemi|p1:full]] (file [[LTA-2231|rec:client file number]]) · **Prepared by:** [[Winston Achebe|p3:full]], EA · **Updated:** [[08/03/2026|date]]
[[Larkspur Tax & Advisory, LLC|o1:full]] · [[77 Wyoming Street, 2nd Floor|addr]] · [[Dayton|place:city]], [[OH|place:state]] [[45409|zip]] · [[(937) 555-0114|phone]]
## Who is who
- Taxpayer: [[Yolanda|p1:first-name]], SSN [[XXX-XX-1157|ssn!:masked SSN, capital X]], DOB [[12/09/1979|dob]]. Middle-school counselor, W-2 income only.
- Former spouse: [[Babatunde Adeyemi|p2:full]] ("[[Tunde|p2:nickname]]"), SSN ending [[0530|ssn!:last four only]]. Sole owner of [[Adeyemi Freight Brokers Inc.|o2:full]], EIN [[31-4420917|taxid:EIN]], reported on Schedule C before he incorporated.
- Divorce final [[November 14, 2025|date:divorce date]], [[Montgomery County|place:county]] Domestic Relations Court, Case No. [[2024 DR 00871|rec:court case number with spaces]].
- IRS examiner: [[Ms. Kowalczyk|p4:title-surname]], employee ID [[1000448217|govid!:IRS employee ID, bare digits]], phone [[866-555-0162 ext. 3307|phone:toll-free with extension]], fax [[855-555-0141|phone:fax]].
- Our authority: Form 2848 on file, CAF no. [[0314-77182-R|govid:CAF number]]; [[Winston|p3:first-name]]'s PTIN [[P01447823|govid:PTIN]].
## Notices received
| Notice | Tax year | Notice date | Amount | Respond by |
| Letter 566 | 2022 | [[03/16/2026|date]] | n/a | [[04/15/2026|date]] |
| Form 4549 | 2022 | [[05/28/2026|date]] | [[$23,418|money]] | [[06/27/2026|date]] |
| Form 4549 | 2023 | [[05/28/2026|date]] | [[$9,766|money]] | [[06/27/2026|date]] |
| CP2000 | 2023 | [[07/06/2026|date]] | [[$1,204.00|money]] | [[08/05/2026|date]] |
The proposed deficiencies arise almost entirely from unreported gross receipts of the freight business ([[$71,300|money]] for 2022 per Form 1099-K matching) and disallowed vehicle expenses. An accuracy penalty under IRC § 6662(a) of [[$4,683.60|money]] is included in the 2022 figure. Interest continues to accrue. Control number on the report: [[AUR-0226-447819|rec:IRS control number]].
## What we have told the IRS
[[Achebe|p3:surname!]] spoke with the examiner on [[June 4|date!:no year]] and [[June 18, 2026|date]]. Position: the returns were joint, but Yolanda had no role in the business, no signature authority on the business account at [[Great Miami Savings Bank|o3:full]] (acct [[000447120938|acct!:unlabelled-style account with leading zeros]]), and did not know receipts were being left off. She signed the returns electronically after being shown only the first page. We filed Form 8857 on [[June 24, 2026|date:filing date]] requesting separation of liability under IRC § 6015(c). The examiner agreed to suspend collection against Yolanda while the request is pending. [[Mr. Adeyemi|p2:title-surname]] will be notified and may participate; she has been warned about that.
## Facts that matter for relief (keep confidential)
- Yolanda reports a history of [[financial control and intimidation by her former spouse|indirect!:abuse history]]. A civil protection order was issued in [[February 2025|date!:month and year only]].
- She was [[treated for major depression|health:mental health treatment]] at [[Sycamore Counseling Associates|o4:full]] during 2023 and missed eleven weeks of work. Her therapist, [[Lorraine Sato|p5:full]], LISW, will provide a letter. See Publication 971 on abuse and duress.
- [[Tunde|p2:nickname]] moved to [[Houston|place:city]] in 2025 and is believed to be [[applying for naturalization|attr!:immigration status, hedged]]; he may be motivated to settle his side.
- The 2023 refund of [[$2,911|money]] was direct-deposited to a joint account she could not access (routing [[049626814|rtn]], account ending [[6603|acct!:last four only]]).
## Money
- Retainer received [[$1,500.00|money]]; billed to date [[$2,362.50|money]]; she is on a payment plan of [[$150|money]] a month drawn from her checking, routing [[012304383|rtn]], account [[7741 0029 558|acct:account number with spaces]].
- If relief is denied in full, her exposure for both years is roughly [[thirty-four thousand dollars|money!:amount in words]] plus interest.
## Next steps
- Send the therapist's letter and the protection order by [[August 21, 2026|date:deadline]].
- Calendar the CP2000 response; it double-counts the 2023 adjustment.
- Call client at [[937.555.0193|phone:dotted]] (do not leave detailed voicemail) or use the portal, [[https://portal.larkspurtax.example/c/LTA-2231|url:client portal link]]. Do not use her school address; personal email is [[ypa.counselor@quietmail.example|email]].
''',
))

# ---------------------------------------------------------------- 69
_T69 = [
    ("2026-04-01", "1791", "[[Okafor, Chidi|p1:last-first]]", "[[Kettle Moraine Lumber Co.|o2:full]]", "Materials", 2841.17, "Job 2611 - [[Hartung|p5:surname!:client surname in a memo]] residence, framing pkg"),
    ("2026-04-01", "1791", "Okafor, Chidi", "[[Badger State Fasteners|o3:full]]", "Materials", 318.4, "Job 2611"),
    ("2026-04-02", "3459", "[[Lindqvist, Maja|p2:last-first]]", "[[Cream City Coffee Roasters|o4:full]]", "Meals", 23.75, "site mtg w/ [[Dr. Feld|p6:title-surname]] (client)"),
    ("2026-04-03", "6976", "[[DeShawn Whitaker|p3:full]]", "[[Northwoods Fuel Stop #114|o5:full]]", "Fuel", 96.02, "truck 7, plate [[RT-48817|veh:license plate]]"),
    ("2026-04-03", "6495", "[[R. Villanueva|p4:short:initial + surname]]", "[[Driftless Software GmbH|o6:full]]", "Software", 189.0, "estimating seats x3, inv [[DS-2026-04417|rec:invoice number]]"),
    ("2026-04-06", "1791", "Okafor, Chidi", "[[Lakeshore Tool Rental LLC|o7:full]]", "Equipment rental", 412.5, "skid steer 2 days, contract [[LTR-88120|rec:rental contract number]]"),
    ("2026-04-06", "3459", "Lindqvist, Maja", "[[Third Coast Print & Sign|o8:full]]", "Marketing", 640.0, "yard signs"),
    ("2026-04-07", "6976", "DeShawn Whitaker", "[[Fox Valley Safety Supply|o9:full]]", "Safety", 152.88, "harness + lanyards"),
    ("2026-04-08", "6976", "DeShawn Whitaker", "[[Riverwest Wine & Spirits|o10:full]]", "PERSONAL", 61.43, "PERSONAL - payroll deduct per [[Maja|p2:first-name]]"),
    ("2026-04-09", "1791", "Okafor, Chidi", "[[Sheboygan Stone & Tile|o11:full]]", "Materials", 5120.0, "Job 2598 - [[Feld|p6:surname!:client surname in a memo]] kitchen, deposit"),
    ("2026-04-10", "6495", "R. Villanueva", "[[Hotel Pfister-Lange Madison|o12:full]]", "Travel", 428.66, "builders show, conf # [[HPL7741902|rec:hotel confirmation number]]"),
    ("2026-04-10", "6495", "R. Villanueva", "[[Parkade Capitol Square|o13:full]]", "Travel", 36.0, ""),
    ("2026-04-13", "1791", "Okafor, Chidi", "Kettle Moraine Lumber Co.", "Materials", -318.4, "return, credit memo [[CM-10447|rec:credit memo number]]"),
    ("2026-04-14", "3459", "Lindqvist, Maja", "[[Blue Mound Catering|o14:full]]", "Meals", 386.2, "crew lunch, Hartung topping-out"),
    ("2026-04-15", "6976", "DeShawn Whitaker", "Northwoods Fuel Stop #114", "Fuel", 104.77, "truck 7"),
    ("2026-04-16", "6976", "DeShawn Whitaker", "[[Wauwatosa Urgent Care|o15:full]]", "Medical", 175.0, "[[stitches, left hand|health!:injury treatment in a memo]] - work comp claim [[WC-26-003381|rec:claim number]]"),
    ("2026-04-17", "1791", "Okafor, Chidi", "Badger State Fasteners", "Materials", 77.19, "Job 2598"),
    ("2026-04-20", "6495", "R. Villanueva", "Driftless Software GmbH", "Software", -63.0, "refund 1 seat"),
    ("2026-04-21", "3459", "Lindqvist, Maja", "[[Lake Country Title & Escrow|o16:full]]", "Fees", 250.0, "lien waiver recording, [[Waukesha County|place:county]]"),
    ("2026-04-22", "1791", "Okafor, Chidi", "Sheboygan Stone & Tile", "Materials", 5120.0, "Job 2598 balance"),
    ("2026-04-23", "6976", "DeShawn Whitaker", "Lakeshore Tool Rental LLC", "Equipment rental", 88.0, "plate compactor"),
    ("2026-04-24", "3459", "Lindqvist, Maja", "Cream City Coffee Roasters", "Meals", 19.5, "interview - [[A. Brzezinski|p7:short:initial + surname]]"),
    ("2026-04-27", "6495", "R. Villanueva", "[[Milwaukee Area Carpenters Local 344|o17:full]]", "Dues", 1260.0, "[[union dues remit, 6 members|attr!:union membership]]"),
    ("2026-04-28", "1791", "Okafor, Chidi", "Kettle Moraine Lumber Co.", "Materials", 1934.6, "Job 2611 trim pkg"),
    ("2026-04-29", "6976", "DeShawn Whitaker", "Northwoods Fuel Stop #114", "Fuel", 99.31, "truck 7"),
    ("2026-04-30", "3459", "Lindqvist, Maja", "[[Friends of Rosalind Achterberg for Assembly|o18:full]]", "Contributions", 500.0, "[[campaign donation - NOT deductible|attr!:political donation]], reclass to owner draw"),
]

_TOT69 = round(sum(r[5] for r in _T69), 2)

DOCS.append(D(69, "xlsx", "expense ledger", "accounting", "US",
  title="Corporate card expense ledger and reconciliation - April",
  ents={"p1": "Chidi Okafor", "p2": "Maja Lindqvist", "p3": "DeShawn Whitaker", "p4": "Rosa Villanueva",
        "p5": "Hartung (client)", "p6": "Dr. Feld (client)", "p7": "A. Brzezinski (job applicant)", "p8": "Noor Haddad",
        "o1": "Tamarack Design-Build, Inc.", "o2": "Kettle Moraine Lumber Co.", "o3": "Badger State Fasteners",
        "o4": "Cream City Coffee Roasters", "o5": "Northwoods Fuel Stop #114", "o6": "Driftless Software GmbH",
        "o7": "Lakeshore Tool Rental LLC", "o8": "Third Coast Print & Sign", "o9": "Fox Valley Safety Supply",
        "o10": "Riverwest Wine & Spirits", "o11": "Sheboygan Stone & Tile", "o12": "Hotel Pfister-Lange Madison",
        "o13": "Parkade Capitol Square", "o14": "Blue Mound Catering", "o15": "Wauwatosa Urgent Care",
        "o16": "Lake Country Title & Escrow", "o17": "Milwaukee Area Carpenters Local 344",
        "o18": "Friends of Rosalind Achterberg for Assembly", "o19": "Marquette Commerce Bank"},
  distractors=["Job 2611", "Job 2598", "truck 7", "GL 6120", "Form 1099-NEC"],
  sheets=[
    ("Transactions",
     [["Post date", "Card (last 4)", "Cardholder", "Merchant", "Category", "Amount", "Memo"]] +
     [[dt(d, "mm/dd/yyyy"), "[[%s|card!:last four only]]" % c, h, m, cat, amt(a, "acct"), memo]
      for (d, c, h, m, cat, a, memo) in _T69] +
     [["", "", "", "", "TOTAL", amt(_TOT69, "acct"), ""]]),
    ("Cards",
     [["Cardholder", "Emp ID", "Card number", "Exp", "CVV", "Limit", "Billing ZIP", "Notes"],
      ["[[Chidi Okafor|p1:full]]", "[[TDB-0007|rec:employee ID]]", "[[4908 5838 1563 1791|card:spaced]]", "[[09/28|exp]]", "[[352|cvv]]", amt(15000, "usd0"), "[[53186|zip]]", "owner"],
      ["[[Maja Lindqvist|p2:full]]", "[[TDB-0012|rec:employee ID]]", "[[5116-9710-9144-3459|card:dashed]]", "[[11/27|exp]]", "[[046|cvv!:security code with leading zero]]", amt(7500, "usd0"), "53186", "office mgr; PIN for cash advance [[7714|cred!:card PIN]]"],
      ["DeShawn Whitaker", "[[TDB-0031|rec:employee ID]]", num(374587270046976, "card!:card number stored as a number"), "[[2/29|exp!:expiry without leading zero]]", num(8104, "cvv!:four-digit code stored as a number"), amt(2500, "usd0"), "[[53213|zip]]", "field super"],
      ["[[Rosa Villanueva|p4:full]]", "[[TDB-0019|rec:employee ID]]", "[[6011040043406495|card!:no separators]]", "[[Jan 2029|exp!:expiry as month name and year]]", "[[907|cvv]]", amt(5000, "usd0"), "53186", "estimator. old card [[6011-1993-1080-1349|card:dashed]] CANCELLED [[3/2/26|date!:two-digit year]]"]]),
    ("Recon",
     [["Item", "Value", "Notes"],
      ["Entity", "[[Tamarack Design-Build, Inc.|o1:full]]", "EIN [[39-2044781|taxid:EIN]]"],
      ["Issuer", "[[Marquette Commerce Bank|o19:full]]", "program acct [[4418-220-0091|acct:card program account]]"],
      ["Statement closing date", dt("2026-04-30", "mmmm d, yyyy"), ""],
      ["Statement balance", amt(_TOT69, "usd"), ""],
      ["GL 2150 balance", amt(round(_TOT69 - 185, 2), "usd"), "before adj."],
      ["Difference", amt(185.0, "usd"), "= urgent care [[$175|money]] not yet coded + [[$10|money]] late fee"],
      ["Personal charges to recover", amt(61.43, "usd"), "[[Whitaker|p3:surname!]], deduct [[5/8/2026|date]] payroll"],
      ["Reclass to owner draw", amt(500.0, "usd"), "GL 6120 to 3050"],
      ["Autopay account", "[[****2218|acct!:masked account]]", "routing [[081204265|rtn]]"],
      ["Prepared by", "[[Noor Haddad|p8:full]]", dt("2026-05-06", "m/d/yyyy")],
      ["Reviewed by", "[[C. Okafor|p1:short:initial + surname]]", dt("2026-05-07", "m/d/yyyy")],
      ["Open items", "Form 1099-NEC check for Third Coast Print & Sign", "ask [[Noor|p8:first-name]]"]]),
  ]))

# ---------------------------------------------------------------- 70
DOCS.append(D(70, "docx", "loan application", "accounting", "US",
  title="SBA loan application package memo - bakery expansion",
  ents={"p1": "Aroha Ngata-Williams", "p2": "Mei-Ling Zhou", "p3": "Fatima al-Sayed", "p4": "Graham Petrakis",
        "p5": "Bernard Ostrowski III",
        "o1": "Three Sisters Bakehouse LLC", "o2": "Columbia Gorge Community Bank", "o3": "Petrakis & Yoon CPAs, LLP",
        "o4": "Ostrowski Family Properties LP", "o5": "Wy'east Federal Credit Union"},
  distractors=["SBA Form 1919", "SBA Form 413", "NAICS 311811", "Form 1065", "7(a)", "Form 4506-C", "DSCR"],
  body=r'''
# [[Petrakis & Yoon CPAs, LLP|o3:full]]
**MEMO TO FILE - LOAN APPLICATION PACKAGE**
Client: [[Three Sisters Bakehouse LLC|o1:full]] (client no. [[30418|rec!:client number, bare digits]]) | Prepared by [[Graham Petrakis|p4:full]], CPA | [[September 14, 2026|date:memo date]]
## Purpose
The client is applying to [[Columbia Gorge Community Bank|o2:full]] for an SBA 7(a) term loan of [[$285,000|money]] to build out a second production kitchen. The bank's reference is application no. [[CGCB-7A-2026-0418|rec:loan application number]]. We compiled the financial package and helped the members complete SBA Form 1919 and SBA Form 413. This memo records what was submitted and the open points.
## Borrower
[[Three Sisters|o1:short!:shortened trade name]] is an [[Oregon|place:state]] limited liability company formed [[March 9, 2019|date:formation date]], EIN [[93-4471208|taxid:EIN]], NAICS 311811. It operates a retail bakery at [[212 Oak Street|addr]], [[Hood River|place:city]], [[OR|place!:two-letter state abbreviation that is also a word]] [[97031|zip]], under a lease with [[Ostrowski Family Properties LP|o4:full]] (landlord contact [[Bernard Ostrowski III|p5:full:name with suffix]], [[541-555-0122|phone]]). Rent is [[$4,150|money]] a month through 2031. It files Form 1065.
## Members and guarantors
| Name | Ownership | SSN | Date of birth | ID |
| [[Aroha Ngata-Williams|p1:full]] | 40% | [[048-36-1142|ssn]] | [[14 Feb 1985|dob]] | OR DL [[4471902|govid!:driver's license, bare digits]] |
| [[Mei-Ling Zhou|p2:full]] | 30% | [[186824355|ssn!:SSN without dashes]] | [[1988-07-30|dob]] | OR DL [[A882047|govid:driver's license]] |
| [[Fatima al-Sayed|p3:full]] | 30% | ITIN [[9XX-XX-4471|taxid!:masked ITIN]] applied for SSN | [[06/21/1990|dob]] | Passport [[N01447729|govid:passport number]] |
All three will guarantee personally. [[Ms. Ngata-Williams|p1:title-surname]] is [[a New Zealand citizen and a lawful permanent resident|attr:citizenship and immigration status]] (USCIS no. [[A-088-204-417|govid:alien registration number]]). [[Ms. al-Sayed|p3:title-surname]]'s [[adjustment of status is pending|attr:immigration status]]; the bank has said this does not disqualify her as a guarantor of a minority interest but wants her work authorization card, which expires [[01/31/2027|date:document expiry]]. [[Mei-Ling|p2:first-name]] disclosed [[a Chapter 7 discharge in 2014|attr:bankruptcy history]] on Form 1919, question 7; a letter of explanation is in the package.
## Financial summary
- 2025 gross receipts [[$1,184,300|money]]; net income before guaranteed payments [[$142,760|money]].
- Year-to-date through [[August 31, 2026|date:period end]]: receipts [[$861,900|money]], up eleven percent.
- Existing debt: equipment note with [[Wy'east Federal Credit Union|o5:full]], loan no. [[70-0044187-L2|rec:loan number]], balance [[$38,412.66|money]], payment [[$1,022|money]] monthly.
- Projected DSCR after the new loan is 1.41.
- Personal financial statements: [[Aroha|p1:first-name]]'s net worth [[$212,000|money]]; Mei-Ling's [[$96,500|money]]; [[Fatima|p3:first-name]]'s under [[20k|money!:shorthand k amount]], mostly her vehicle.
## Collateral offered
- First lien on all business assets, including the deck oven (serial [[RV-DO4-2291-0087|dev:equipment serial number]]) and the spiral mixer (serial [[SM80-114477|dev:equipment serial number]]).
- 2022 refrigerated delivery van, VIN [[1FTBW3XG5NKA40917|veh:VIN]], Oregon plate [[817 MKT|veh:license plate]].
- Second deed of trust on Aroha's home at [[1640 Belmont Avenue|addr]], [[Hood River|place:city]] (tax lot [[03N10E35CB 04400|rec!:tax lot number]]); estimated equity [[$150,000|money]].
## Banking
Operating account at [[CGCB|o2:acronym]]: routing [[057426080|rtn]], account [[20044718830|acct]]. Payroll account at [[Wy'east|o5:short!:shortened credit union name]]: account [[881-0047-2|acct:account number with dashes]]. Loan proceeds and payments will run through the operating account.
## Open points
- The bank's underwriter asked for Form 4506-C transcripts for each guarantor. Mei-Ling's 2024 return was filed late; expect a question.
- [[Mr. Ostrowski|p5:title-surname]] has not yet signed the landlord consent. He told [[Fatima|p3:first-name]] he wants a personal guarantee on the lease extension first.
- Fee for this engagement: [[$3,200|money]] fixed, invoice [[PY-11872|rec:invoice number]] sent [[9/14/26|date!:two-digit year]]. Questions to [[gpetrakis@petrakisyoon.example|email]] or [[(541) 555-0148|phone]].
''',
))

# ---------------------------------------------------------------- 71
DOCS.append(D(71, "txt", "donor contribution notes", "accounting", "US",
  title="Nonprofit donor contribution notes - spring appeal",
  ents={"p1": "Constance Abernathy-Wolfe", "p2": "Grace Olufemi", "p3": "Hyun-woo Park", "p4": "Leonard Feinstein",
        "p5": "Miriam Feinstein", "p6": "Paz Villaseñor", "p7": "Walter Dumbrowski", "p8": "Teddy Kalani",
        "o1": "Riverbend Community Food Pantry", "o2": "Temple Beth Shalom of Riverbend",
        "o3": "Olufemi Family Charitable Fund", "o4": "Keystone Heritage Securities",
        "o5": "Susquehanna Valley Democratic Committee", "o6": "Allegheny Ridge Tool & Die, Inc.",
        "o7": "Laborers' Local 1180", "o8": "Riverbend Islamic Center"},
  distractors=["Form 990", "Schedule B", "IRC § 170(f)(8)", "Form 8283", "501(c)(3)", "Pub. 1771", "Giving Tuesday"],
  body=r'''
[[RIVERBEND COMMUNITY FOOD PANTRY|o1:caps]] -- DONOR NOTES, SPRING APPEAL
kept by [[Paz Villaseñor|p6:full]], bookkeeper (part-time)      EIN [[23-7741980|taxid:EIN]]
for the Form 990 / Schedule B file and year-end acknowledgment letters

[[May 4, 2026|date]]
* [[Constance Abernathy-Wolfe|p1:full]] -- mailed check #[[3318|rec!:check number]] for [[$5,000.00|money]], dated [[4/30/2026|date]].
  Same as last year. She is [[97|age!:bare age]] now and her daughter handles the checkbook; the
  thank-you goes to [[Mrs. Abernathy-Wolfe|p1:title-surname]] at [[Willow Glen Retirement Residence|place:named facility]], [[Rm 214|addr!:room number only]],
  [[88 Front Street|addr]], [[Lewisburg|place:town]], [[PA|place:state]] [[17837|zip]]. NO phone calls (hard of hearing).
  Needs written acknowledgment per IRC § 170(f)(8) since it is over the threshold.

* [[Olufemi Family Charitable Fund|o3:full]] (donor-advised, at [[Keystone Heritage Securities|o4:full]]) --
  grant [[$12,500|money]] recommended by [[Grace Olufemi|p2:full!:first name is a common word]]. Grant ID [[KHS-DAF-0092741|rec:grant ID]].
  No tax letter to [[Grace|p2:first-name!:name that is also a common word]] personally -- the fund is the donor. She asked that
  it be listed as anonymous in the annual report.

[[May 6, 2026|date]]
* [[Hyun-woo Park|p3:full]] -- phoned in a card gift, [[$250|money]] monthly starting now.
  Card [[4985 5081 6529 6933|card:spaced]]  exp [[08/29|exp]]  code [[611|cvv]]  billing zip [[17801|zip]]
  ([[PAZ|p6:caps]] -- SHRED THIS PAGE after entering in the processor. We are not supposed
  to keep the code.)  His email [[hwpark@susqmail.example|email]]. Employer match through
  [[Allegheny Ridge Tool & Die, Inc.|o6:full]] -- he will send their form.

* Stock gift: [[Leonard|p4:first-name]] and [[Miriam Feinstein|p5:full]], 140 shares of an index fund,
  transferred [[05/01/2026|date]] from their account [[KH-4471-88203|acct:brokerage account]] at [[Keystone Heritage|o4:short!]]
  to ours ([[KH-9020-11467|acct:brokerage account]]). Mean of high/low that day x 140 = [[$19,362.00|money]].
  Letter must describe the shares and NOT state a value. They will need
  Form 8283. The gift is in honor of their grandson's bar mitzvah at
  [[Temple Beth Shalom of Riverbend|o2:full]]; [[Mr. Feinstein|p4:title-surname]] wants the temple's
  social action committee copied. ([[Leonard Feinstein|p4:full]], [[570-555-0131|phone]].)

[[May 11, 2026|date]]
* Cash, [[$1,840|money]], Friday collection from [[Riverbend Islamic Center|o8:full]], dropped off by
  the imam's assistant. Receipt no. [[R-2026-0417|rec:receipt number]] issued to the Center, not
  to individuals.
* [[Laborers' Local 1180|o7:full]] -- check [[$750.00|money]] from the members' relief fund,
  delivered by [[Walter Dumbrowski|p7:full]], [[the local's business agent|indirect:unique role]]. [[Walt|p7:nickname]] also
  dropped off a personal [[$100|money]] in cash. Receipt in his name, home address
  [[R.R. 2 Box 118|addr:rural route]], [[Mifflinburg|place:town]] PA [[17844|zip]].
* [[Teddy Kalani|p8:full]] -- online, [[$40|money]]. Came in through the Giving Tuesday page that
  is somehow still live: [[https://give.riverbendpantry.example/donate?c=gt25|url:donation page]]
  Ask the web volunteer to take it down. Processor shows donor IP [[192.0.2.146|ip:IPv4]]
  and flagged it as possible card testing; it was a real gift, he called.

[[May 13, 2026|date]] -- PROBLEMS / QUESTIONS FOR THE TREASURER
1. [[Mrs. Feinstein|p5:title-surname]] asked whether we could "pass along" [[$500|money]] of their
   gift to the [[Susquehanna Valley Democratic Committee|o5:full]] dinner. NO. We are a
   501(c)(3); we cannot touch that. I told her politely. Please back me up.
2. [[Mr. Park|p3:title-surname]] wrote on his pledge card that he is giving "in thanks,
   [[5 years sober this month|health!:recovery status]]." Lovely, but it should not go in the newsletter. I
   blacked it out on the scanned copy.
3. A walk-in donor who would only give her first name ([[Dolores|p9:first-name]]) left a
   cashier's check for [[ten thousand dollars|money!:amount in words]] even. No address. Pub. 1771
   says we cannot force it; I logged it as anonymous. Bank deposit slip
   shows our account [[0044-718-2260|acct]] at the credit union, deposited [[5/12/26|date!:two-digit year]].
4. Board member asked for "the list of who gave what." Schedule B names are
   not public. I will give totals only: [[$40,142.00|money]] for the appeal so far.

[[Paz|p6:first-name]] -- [[pantry.books@riverbendpantry.example|email]] -- Tues/Thurs only -- [[570 555 0109|phone!:spaces only]]
''',
))
DOCS[-1]["ents"]["p9"] = "Dolores (walk-in donor, surname not given)"

# ---------------------------------------------------------------- 72
DOCS.append(D(72, "pdf", "invoice", "accounting", "EU",
  title="Invoice - marine engineering services (Netherlands to Ireland)",
  ents={"p1": "Joost van der Meulen", "p2": "Siobhán Ní Bhraonáin", "p3": "Anouk de Vries-Bakker",
        "o1": "Van der Meulen Scheepstechniek B.V.", "o2": "Claddagh Coastal Ferries DAC",
        "o3": "Noordzee Handelsbank N.V."},
  distractors=["Article 44", "VAT Directive 2006/112/EC", "0%", "Incoterms", "ISO 9001", "30 days"],
  body=r'''
# INVOICE / FACTUUR
**[[Van der Meulen Scheepstechniek B.V.|o1:full]]**
[[Havenkade 41-43|addr:Dutch street address]], [[3011 XK|zip:Dutch postal code]] [[Rotterdam|place:city]], The Netherlands
KvK [[24477180|taxid:Dutch chamber of commerce number]] · BTW/VAT [[NL004471882B01|taxid:VAT number]] · T [[+31 10 555 0147|phone:international format]] · [[administratie@vdmscheepstechniek.example|email]]
**Invoice no.:** [[2026-0418|rec:invoice number]]
**Invoice date:** [[12-05-2026|date!:day-month-year with dashes]]
**Due date:** [[11-06-2026|date!:day-month-year with dashes]]
**Your PO:** [[CCF/PO/7741|rec:purchase order number]]
**Our project:** [[P-2611|rec:project number]]
## Bill to
[[Claddagh Coastal Ferries DAC|o2:full]]
Attn. [[Siobhán Ní Bhraonáin|p2:full]], Technical Superintendent
[[Unit 6, Docks Enterprise Park|addr]], [[Galway|place:city]], [[H91 X4T2|zip:Irish Eircode]], Ireland
VAT no. [[IE3344718TH|taxid:VAT number]]
## Description
Dry-dock overhaul of the port-side main engine gearbox and replacement of the stern tube seals on the passenger ferry "[[Aisling na Mara|indirect!:named vessel]]", IMO [[9044718|veh!:ship IMO number]], carried out at our yard between [[20 April|date!:no year]] and [[7 May 2026|date]].
| Item | Qty | Amount (EUR) |
| Labour, fitters | 212 h | [[€ 18.020,00|money!:European number format]] |
| Gearbox bearings | 1 set | [[€ 9.460,00|money!:European number format]] |
| Stern tube seals | 2 | [[€ 4.250,00|money!:European number format]] |
| Dock hire, 9 days | 9 | [[€ 6.750,00|money!:European number format]] |
| Class surveyor | 1 | [[€ 1.180,50|money!:European number format]] |
| **Total excl. VAT** | | [[€ 39.660,50|money!:European number format]] |
| VAT 0% | | [[€ 0,00|money!:European number format]] |
| **Total due** | | [[€ 39.660,50|money!:European number format]] |
VAT reverse-charged to the customer under Article 44 of VAT Directive 2006/112/EC. An advance of [[EUR 15,000|money!:currency code before amount]] was received on [[17 April 2026|date]] against pro-forma [[PF-2026-0092|rec:pro-forma invoice number]] and is NOT deducted above; balance now payable is [[€ 24.660,50|money!:European number format]].
## Payment
Please pay within 30 days to [[Noordzee Handelsbank N.V.|o3:full]], Rotterdam.
IBAN: [[NL48 RABO 0447 1882 03|iban:spaced]]
BIC: [[NZHBNL2R|acct:BIC / SWIFT code]]
Quote the invoice number. Late payment interest runs at the statutory commercial rate.
## Notes
The seal housings showed scoring consistent with the grounding off [[Inis Oírr|place:island]] in February that [[Ms. Ní Bhraonáin|p2:title-surname]] mentioned; we recommend a shaft alignment check at the next docking. Warranty on parts is twelve months. Our work is certified to ISO 9001; delivery terms per Incoterms do not apply to services.
Questions about this invoice: [[Anouk de Vries-Bakker|p3:full]], accounts receivable, direct [[010-555 01 62|phone!:Dutch national format]], [[a.devries@vdmscheepstechniek.example|email]].
Signed for the company: [[J. van der Meulen|p1:short:initial + surname with particles]], director
''',
))

# ---------------------------------------------------------------- 73
DOCS.append(D(73, "txt", "payroll summary", "accounting", "CA",
  title="Payroll summary - pay period 11 (Saskatchewan greenhouse)",
  ents={"p1": "Marguerite Lafrenière", "p2": "Dwayne Pelletier", "p3": "Rosario Macaraeg",
        "p4": "Sukhmani Brar", "p5": "Erik Thorvaldson", "p6": "Kateri Ahenakew", "p7": "Jun Macaraeg",
        "o1": "Qu'Appelle Valley Greenhouses Ltd.", "o2": "Prairie Sky Bookkeeping Inc.",
        "o3": "Conexus Plains Credit Union", "o4": "UFCW Local 1400-G",
        "o5": "Maintenance Enforcement Office"},
  distractors=["T4", "TD1", "PD7A", "ROE", "CPP", "EI", "s. 2-60", "WCB"],
  body=r'''
[[PRAIRIE SKY BOOKKEEPING INC.|o2:caps]]
PAYROLL SUMMARY -- client: [[Qu'Appelle Valley Greenhouses Ltd.|o1:full]] ("[[QVG|o1:acronym]]")
CRA payroll account [[81447 2209 RP0001|taxid:Canadian business number, payroll account]]
Pay period 11: [[May 17|date!:no year]] to [[May 30, 2026|date]]    Pay date: [[June 5, 2026|date:pay date]]
Prepared by [[Marguerite Lafrenière|p1:full]], [[2026-06-03|date:ISO format]]

EMPLOYEE              SIN            GROSS      CPP     EI     TAX     OTHER     NET
[[Pelletier, Dwayne|p2:last-first]]     [[491 385 274|taxid:SIN with spaces]]   [[2,480.00|money!:no currency sign]]   [[139.56|money!:no currency sign]]  [[40.67|money!:no currency sign]]  [[381.20|money!:no currency sign]]   [[412.00|money!:no currency sign]]   [[1,506.57|money!:no currency sign]]
[[Macaraeg, Rosario|p3:last-first]]     [[528-301-708|taxid:SIN with dashes]]   [[1,920.00|money!:no currency sign]]   [[106.23|money!:no currency sign]]  [[31.49|money!:no currency sign]]  [[214.85|money!:no currency sign]]    [[28.50|money!:no currency sign]]   [[1,538.93|money!:no currency sign]]
[[Brar, Sukhmani|p4:last-first]]        [[226021244|taxid!:SIN without separators]]     [[1,760.00|money!:no currency sign]]    [[96.71|money!:no currency sign]]  [[28.86|money!:no currency sign]]  [[176.40|money!:no currency sign]]    [[28.50|money!:no currency sign]]   [[1,429.53|money!:no currency sign]]
[[Thorvaldson, Erik|p5:last-first]]     [[626 503 841|taxid:SIN with spaces]]   [[3,076.92|money!:no currency sign]]   [[175.08|money!:no currency sign]]  [[50.46|money!:no currency sign]]  [[598.11|money!:no currency sign]]     0.00   [[2,253.27|money!:no currency sign]]
[[Ahenakew, Kateri|p6:last-first]]      [[364-493-569|taxid:SIN with dashes]]   [[1,584.00|money!:no currency sign]]    [[86.24|money!:no currency sign]]  [[25.98|money!:no currency sign]]    0.00    [[28.50|money!:no currency sign]]   [[1,443.28|money!:no currency sign]]
                                     ---------
TOTAL GROSS                          [[10,820.92|money!:no currency sign]]

NOTES ON "OTHER"
- [[Dwayne|p2:first-name]]: union dues [[28.50|money!:no currency sign]] plus garnishment [[383.50|money!:no currency sign]] to the [[Maintenance Enforcement Office|o5:full]],
  file [[MEO-0044718|rec:enforcement file number]] ([[child support order|indirect!:family court obligation]]). Remit by the 15th. He asked [[Erik|p5:first-name]] to
  keep this quiet on the floor.
- Dues of 28.50 for [[Rosario|p3:first-name]], [[Sukhmani|p4:first-name]] and [[Kateri|p6:first-name]] go to [[UFCW Local 1400-G|o4:full]]; all four are
  [[members of the bargaining unit|attr:union membership]]. Erik is management, no dues.
- Kateri: no income tax withheld. She filed a TD1 claiming the exemption as a
  [[Status Indian working on reserve|attr!:Indigenous status]]; QVG's main site is on leased land of
  [[Muscowpetung First Nation|place:First Nation community]]. Letter on file. Do not "correct" this again.

CHANGES THIS PERIOD
- [[Rosario Macaraeg|p3:full]] -- [[closed work permit, employer-specific (TFW program)|attr!:immigration status]], permit no.
  [[U771204418|govid:work permit number]], expires [[2027-02-28|date:permit expiry]]. SIN begins with 9 on the old record
  ([[9XX XXX 118|taxid!:masked temporary SIN]]); she now has the one above -- update T4 master. [[Her husband|indirect:family relationship]]
  [[Jun|p7:first-name]] starts [[June 8|date!:no year]] on the same permit type; need his SIN and void cheque.
- [[Sukhmani Brar|p4:full]] -- last day [[May 29, 2026|date:last day worked]], [[maternity leave|health:pregnancy-related leave]]. ROE issued, serial
  [[W40447182|rec:ROE serial number]], code F. Vacation pay of [[$211.20|money]] included in gross above. Expected
  return [[June 2027|date!:month and year only]].
- [[Erik Thorvaldson|p5:full]] -- salary increase to [[$80,000|money]] per year effective [[May 17, 2026|date:effective date]]
  (was [[76k|money!:shorthand k amount]]). Signed letter from the owner on file.
- [[Dwayne Pelletier|p2:full]] -- off [[May 21|date!:no year]] to [[May 26|date!:no year]], WCB claim no. [[26-118447|rec:workers' compensation claim number]]
  ([[lower back strain|health:injury]], lifting). Paid day of injury only per s. 2-60.

DIRECT DEPOSIT FILE -- [[Conexus Plains Credit Union|o3:full]], originator ID [[0044718829|rec!:originator ID, bare digits]]
  [[Pelletier|p2:surname!]]     transit [[40418|acct!:transit number]]  inst [[889|acct!:institution number]]  acct [[2204471|acct]]
  [[Macaraeg|p3:surname!]]      transit [[40418|acct!:transit number]]  inst 889  acct [[2209983|acct]]
  [[Brar|p4:surname!]]          transit [[00378|acct!:transit number]]  inst [[010|acct!:institution number with leading zero]]  acct [[77-41802|acct:account number with dash]]
  [[Thorvaldson|p5:surname!]]   transit 40418  inst 889  acct [[1180026|acct]]
  [[Ahenakew|p6:surname!]]      paid by cheque no. [[004417|rec!:cheque number]] (no account on file)

REMITTANCE (PD7A): CPP [[1,207.64|money!:no currency sign]], EI [[425.90|money!:no currency sign]], tax [[1,370.56|money!:no currency sign]]; total [[$3,004.10|money]] due
[[June 15, 2026|date:remittance deadline]]. Pay from QVG operating acct ending [[-3317|acct!:last four with leading dash]].

Questions: [[Marguerite|p1:first-name]], [[306-555-0115|phone]], [[marguerite@prairieskybooks.example|email]]
[[Box 418|addr:rural box number]], [[Fort Qu'Appelle|place:town]], [[SK|place:province]]  [[S0G 1S0|zip:Canadian postal code]]
''',
))

# ---------------------------------------------------------------- 74
DOCS.append(D(74, "eml", "internal email", "general", "US", enc="plain",
  title="Internal email - vendor payments and IT handover before leave",
  ents={"p1": "Bronwyn Castellanos", "p2": "Ravi Subramanian", "p3": "Mike O'Dell",
        "p4": "Ingeborg Maier", "p5": "Tasha Greenleaf",
        "o1": "Copperline Outfitters Co.", "o2": "Sawtooth Freight Lines, Inc.",
        "o3": "Maier Textil GmbH & Co. KG", "o4": "First Teton Bank & Trust", "o5": "O'Dell Networks"},
  distractors=["Net 30", "QuickBooks", "Form W-9", "2FA", "ACH", "PTO"],
  headers={
    "From": "[[Bronwyn Castellanos|p1:full]] <[[bronwyn@copperlineoutfitters.example|email]]>",
    "To": "[[Ravi Subramanian|p2:full]] <[[ravi@copperlineoutfitters.example|email]]>",
    "Subject": "everything you need while I'm out ([[7/20|date!:month/day only]]-[[8/7|date!:month/day only]]) - PLEASE DELETE AFTER READING",
    "Date": "Fri, [[17 Jul 2026|date]] 18:07:44 -0600",
  },
  body=r'''
[[Ravi|p2:first-name]],

I know, I know, I shouldn't put all this in one email. But you asked for one
place to look, so here it is. Delete it when I'm back.

PAYMENTS DUE WHILE I'M GONE

1) [[Sawtooth Freight Lines, Inc.|o2:full]] -- invoice [[SFL-208841|rec:invoice number]], [[$4,318.90|money]], due [[July 24|date!:no year]], Net 30.
   Pay by ACH from the bank portal. They are already set up as a payee but if
   it asks again: routing [[064808675|rtn]], account [[3300447182|acct]]. Their Form W-9 is in
   the vendor folder.

2) [[Maier Textil GmbH & Co. KG|o3:full]] -- the wool order. [[EUR 11,240.00|money!:currency code before amount]] by international
   wire, must arrive by [[July 31|date!:no year]] or [[Ingeborg|p4:first-name]] will not ship before the fall
   catalog. Details exactly as on her pro-forma:
       Beneficiary: Maier Textil GmbH & Co. KG
       IBAN: [[DE12 9249 1078 0589 9210 51|iban:spaced]]
       BIC: [[MAIEDEM1XXX|acct:BIC / SWIFT code]]
       Reference: [[PF-7741|rec:pro-forma number]]
   The bank charges [[$45|money]] per wire. If the portal balks at the amount, call
   [[Tasha Greenleaf|p5:full]] at [[First Teton Bank & Trust|o4:full]], [[(208) 555-0166|phone]]. She knows us. She will
   ask for the callback PIN, which is [[4471|cred!:bank callback PIN]].

3) The software subscriptions bill to the company card, the one ending [[2830|card!:last four only]].
   If anything declines, the full number is [[6011 2427 4797 0830|card:spaced]], exp [[03/28|exp]], CVV [[529|cvv]].
   Do NOT give that to anyone over the phone.

BANK PORTAL
   [[https://business.firstteton.example/login|url:bank portal login]]
   user: [[copperline_ap|cred:username]]
   pass: [[Huckleberry!Trail88|cred!:password in an email]]
   2FA codes go to my cell, so text me ([[208-555-0134|phone]]) BEFORE you log in and I
   will send the code. I'll have service most days.

QuickBooks runs on the back-office PC. Windows login is [[coadmin|cred:username]] / [[Winter2026$|cred!:password in an email]].
(Yes, [[Mike|p3:first-name]] keeps telling me to change it.)

IT STUFF, since [[Mike O'Dell|p3:full]] of [[O'Dell Networks|o5:full]] is also away the week of the 27th:
   - If the internet drops, power-cycle the router in the stock room. Its admin
     page is [[192.168.10.1|ip:private IPv4]]. Static IP from the ISP is [[203.0.113.88|ip:IPv4]] -- Mike says
     the card terminal needs that.
   - Label printer by the packing bench keeps falling off the network. It is
     the one with MAC [[00:1B:44:11:3A:B7|dev:MAC address]], serial [[ZT41-2291-00817|dev:printer serial number]]. Turn it off and on.
   - Remote support, only if desperate: [[mike@odellnetworks.example|email]] or [[208.555.0191|phone!:dotted]].

PEOPLE THINGS (between us)
   - [[Tasha|p5:first-name]] is not just our banker, she is [[my sister-in-law|indirect!:family relationship to named person]], so be nice.
   - If [[Mr. Subramanian senior|p6:title-surname!:title + surname + senior]] calls about the lease, tell [[your dad|indirect!:family relationship]] I will
     ring him the week I'm back. The deposit he fronted us, [[$18,000|money]], is on
     the books as a loan, not equity. We agreed that at Christmas.
   - I'm out for [[my knee replacement|health:surgery]], not a vacation, whatever the PTO
     calendar says. Please keep that to yourself.

Thank you thank you.
[[B.|p1:initials!:single initial sign-off]]

--
[[Bronwyn Castellanos|p1:full]]
Operations, [[Copperline Outfitters Co.|o1:full]]
[[118 N. Main St.|addr]], [[Driggs|place:small town]], [[ID|place:state]] [[83422|zip]]
''',
))
DOCS[-1]["ents"]["p6"] = "Mr. Subramanian senior (Ravi's father)"

# ---------------------------------------------------------------- 75
DOCS.append(D(75, "txt", "phone message", "accounting", "US", length="short",
  title="While-you-were-out phone message",
  ents={"p1": "Dolores Featherstone", "p2": "Kenji (staff accountant, first name only)",
        "o1": "Featherstone Orchards"},
  distractors=["Form 1310", "K-1"],
  body=r'''
WHILE YOU WERE OUT        Tues [[3/10|date!:month/day only]]  2:40 pm
For: [[Kenji|p2:first-name]]
Caller: [[Dolores Featherstone|p1:full]] ([[Featherstone Orchards|o1:full]])
Phone: [[509 555-0118|phone!:mixed separators]], before 6

Her husband passed [[Feb. 27|date!:abbreviated month, no year]]. Needs to know if she signs the joint
return alone and whether Form 1310 applies. IRS letter says they owe
[[$6,214|money]]; she can pay half now. His SSN ends [[-7758|ssn!:last four with dash]]. K-1 from
the orchard not in yet. Call back, she's upset. -- [[jm|p4:initials!:lower-case initials]]
''',
))
DOCS[-1]["ents"]["p4"] = "JM (receptionist, initials only)"

# ---------------------------------------------------------------- 76
DOCS.append(D(76, "txt", "clinical visit note", "health", "US",
  title="Office-based opioid treatment follow-up visit note",
  ents={"p1": "Dakota R. Lemieux", "p2": "Efua Mensah-Boateng", "p3": "Curtis Yellowhorse",
        "p4": "April Lemieux", "p5": "Sandoval (pharmacist)",
        "o1": "Three Rivers Recovery & Primary Care", "o2": "Mesa Verde Community Pharmacy",
        "o3": "San Juan Basin Health Plan", "o4": "Animas Sober Living"},
  distractors=["42 CFR Part 2", "COWS", "CPT 99214", "PDMP", "ICD-10 F11.20", "q4wk"],
  body=r'''
[[THREE RIVERS RECOVERY & PRIMARY CARE|o1:caps]]                 42 CFR Part 2 PROTECTED RECORD
OBOT FOLLOW-UP                                          DOS: [[11/03/2026|date:date of service]]

PT: [[LEMIEUX, DAKOTA R.|p1:last-first]]     DOB: [[6-19-1994|dob!:dashes, no leading zero]]     MRN: [[TRR-0091447|rec:medical record number]]
Ins: [[San Juan Basin Health Plan|o3:full]] (Medicaid MCO), ID# [[SJB 4471 882 06|rec!:member ID with spaces]]
Provider: [[Efua Mensah-Boateng|p2:full]], FNP-BC   NPI [[1881447203|govid:NPI]]   DEA [[MM2204718|govid:DEA number]]

S: 32 y/o here for monthly f/u, [[OUD, severe, in early remission|health!:diagnosis in clinical shorthand]] (ICD-10 F11.20).
On [[bup/nx 8-2 mg SL BID|health!:medication and dose in shorthand]] x 7 mos. Denies cravings most days. One slip:
[[used fentanyl pills x1|health!:substance use in shorthand]] on [[10/17|date!:month/day only]] after an argument w/ [[sister|indirect:family relationship]] [[April|p4:first-name!:name that is also a month]]; no OD,
told his sponsor next day. No IV use since March. Sleeping 5-6 hrs. Mood
"flat but OK." Working 30 hrs/wk at a tire shop. Living at [[Animas Sober Living|o4:full]]
([[Farmington|place:city]]) since [[8/1/26|date!:two-digit year]]; house manager does random UDS too.
[[Tobacco 1/2 ppd|health!:tobacco use in shorthand]]. EtOH: denies. [[Cannabis: "a couple times a month."|health!:substance use, quoted]]
[[Hep C Ab+ (dx 2023), RNA pending|health!:infection status in shorthand]]. [[HIV neg 5/2026|health!:test result in shorthand]].
Legal: [[on probation through 2027|attr:criminal justice status]], [[San Juan County|place:county]], [[poss. of controlled substance|attr!:criminal history in shorthand]]. PO is
[[Curtis Yellowhorse|p3:full]], [[505-555-0127|phone]]; pt signed release for attendance + UDS
results only, NOT the note.

O: [[BP 122/78, HR 74, wt 168|health!:vital signs]]. COWS 2. Alert, well groomed, no track marks.
[[PHQ-9 = 11|health!:depression screening score]] (was 16 in Aug). No SI/HI.
UDS today (cup, lot 4471B): [[bup +, norbup +, fentanyl NEG, THC +, all else neg|health!:drug screen result]].
PDMP checked: no other controlled Rx.

A/P:
1. [[OUD|health!:diagnosis acronym]] -- continue [[buprenorphine-naloxone 8/2 mg|health:medication and dose]] film, 1 BID, #56, 0 RF.
   eRx to [[Mesa Verde Community Pharmacy|o2:full]], [[2101 E. 20th St|addr]], [[Farmington|place:city]] [[NM|place:state]] [[87401|zip]],
   Rx # [[7044718|rec:prescription number]]. Pharmacist ([[Sandoval|p5:surname!:surname only]]) had questions last month about
   early fill; ok to fill [[11/3|date!:month/day only]].
2. [[MDD, moderate|health!:diagnosis in shorthand]] -- start [[sertraline 50 mg qAM|health:medication and dose]]. Declines counseling referral
   again; will revisit.
3. [[Hep C|health!:diagnosis in shorthand]] -- RNA + genotype drawn today. If viremic, treat here.
4. [[Narcan 4 mg nasal x2|health:medication]] dispensed; [[April|p4:first-name!:name that is also a month]] trained on use.
5. Housing: sober-living fee [[$140/wk|money!:weekly rate with slash]]; he is behind [[$280|money]]. Referred to
   peer navigator for the county voucher.
6. RTC q4wk. Next: [[12/1/2026|date:next appointment]] 10:20.

Contact: pt cell [[(505) 555-0183|phone]] -- OK to leave msg w/ first name only.
Emergency contact: sister, [[April Lemieux|p4:full]], [[505.555.0159|phone!:dotted]]. Do NOT contact
[[his father|indirect:family relationship]] (pt request).
Billing: CPT 99214. No copay.

Electronically signed: [[E. Mensah-Boateng|p2:short!:initial + surname]] FNP-BC  [[11/03/2026|date]] 16:52
''',
))

# ---------------------------------------------------------------- 77
DOCS.append(D(77, "docx", "referral letter", "health", "US",
  title="Referral letter to cancer genetics clinic",
  ents={"p1": "Rivka Goldfarb-Stein", "p2": "Naveen Chaudhry", "p3": "Helen Abiodun",
        "p4": "Shira Goldfarb", "p5": "Esther Goldfarb", "p6": "Katarzyna Wiśniewska-Hall",
        "o1": "Lakeside Women's Health Associates, S.C.", "o2": "Northshore University Cancer Genetics Program",
        "o3": "Prairie State Blue Shield PPO"},
  distractors=["NCCN", "ICD-10 Z80.41", "CLIA", "CA-125", "HIPAA", "GINA", "FACOG"],
  body=r'''
# [[Lakeside Women's Health Associates, S.C.|o1:full]]
[[1500 Sheridan Road, Suite 310|addr]] · [[Wilmette|place:city]], [[Illinois|place:state]] [[60091|zip]] · Tel [[847-555-0105|phone]] · Fax [[847-555-0106|phone:fax]]
[[October 21, 2026|date:letter date]]
[[Naveen Chaudhry|p2:full]], MD, MS
[[Northshore University Cancer Genetics Program|o2:full]]
VIA FAX: [[(847) 555-0199|phone:fax]]
**RE: [[GOLDFARB-STEIN, Rivka|p1:last-first]] · DOB [[05/28/1987|dob]] · our MRN [[LW-204471|rec:medical record number]]**
**Insurance: [[Prairie State Blue Shield PPO|o3:full]], member ID [[XPS884471205|rec:health plan member ID]], group [[0077418|rec!:group number, bare digits]]**
Dear [[Dr. Chaudhry|p2:title-surname]]:
I am referring [[Ms. Goldfarb-Stein|p1:title-surname]], a 39-year-old [[G2P2|health!:obstetric history in shorthand]] woman, for genetic counseling and management recommendations following a positive result on a multigene panel that I ordered on [[September 29, 2026|date:test order date]].
## Result
The laboratory (CLIA-certified; accession no. [[GX-26-0447182|rec:lab accession number]]) reported [[a pathogenic variant in BRCA1|attr:genetic test result|genetic information]], [[c.68_69delAG|attr!:specific gene variant notation|genetic information]], heterozygous. No other reportable variants were identified in the remaining 46 genes. A copy of the report is enclosed.
## Family history
Ms. Goldfarb-Stein is of [[Ashkenazi Jewish ancestry|attr:ethnicity and religion]] on both sides. [[Her mother|indirect:family relationship]], [[Esther Goldfarb|p5:full]], [[died of ovarian cancer at age 52|health:family medical history]]. [[Her sister|indirect:family relationship]], [[Shira|p4:first-name]], was [[diagnosed with triple-negative breast cancer at 36|health:family medical history]] and is in treatment at your institution; I understand she has not had germline testing. [[A maternal aunt had breast cancer|health:family medical history]] in her sixties. Her father is alive and well at 71. She has two daughters, ages 4 and 7.
## Personal history
Menarche at 12; two term deliveries; [[currently 14 weeks pregnant|health:pregnancy]] with an unplanned third pregnancy, which she has not yet disclosed to her employer. No prior breast biopsies. Clinical breast exam on [[10/14/2026|date:exam date]] was normal. Baseline CA-125 was not drawn because of the pregnancy. She takes [[levothyroxine 75 mcg daily|health:medication and dose]] for [[Hashimoto's thyroiditis|health:diagnosis]] and a prenatal vitamin. She reports [[significant anxiety|health:mental health]] since receiving the result and has started [[seeing a therapist|health!:mental health treatment]].
## Questions for you
- Timing of breast MRI surveillance during and after pregnancy, per NCCN.
- Counseling about risk-reducing salpingo-oophorectomy after childbearing.
- Cascade testing for her sister, her father and, eventually, her daughters.
- Her concerns about insurance. I explained GINA in general terms; she is worried about life insurance, which GINA does not cover, and asked that the result not be released to anyone, including her husband's employer plan, without her written consent under HIPAA.
Please use ICD-10 Z80.41 and the test result for authorization. [[Rivka|p1:first-name]] prefers to be reached on her personal mobile, [[224.555.0167|phone!:dotted]], or at [[rivka.gs@mailhaven.example|email]], not at work. She [[observes the Sabbath|attr!:religious observance]] and cannot take appointments on Friday afternoons or Saturdays.
My nurse, [[Helen Abiodun|p3:full]], RN, can send records: [[habiodun@lakesidewomens.example|email]], direct line 847-555-0105, extension 4.
Thank you for seeing her.
Sincerely,
[[Katarzyna Wiśniewska-Hall|p6:full]], MD, FACOG
NPI [[1447188203|govid:NPI]] · Illinois license [[036.144718|govid:medical license number]]
cc: patient portal
''',
))

# ---------------------------------------------------------------- 78
DOCS.append(D(78, "md", "case management notes", "health", "US",
  title="Home health case management notes",
  ents={"p1": "Adaeze Okonkwo-Bell", "p2": "Ngozi Bell-Hampton", "p3": "Luis Carrasquillo",
        "p4": "Imogen Faircloth", "p5": "Hank (neighbor)", "p6": "Tamsin Reyes",
        "o1": "Tidewater Home Health & Hospice", "o2": "Faircloth Internal Medicine",
        "o3": "Chesapeake Senior Meals", "o4": "AllHours Medical Alert"},
  distractors=["OASIS-E", "Medicare Part A", "PRN", "PT/OT", "Form CMS-485", "HHA", "MoCA"],
  body=r'''
# Case management notes — [[Tidewater Home Health & Hospice|o1:full]]

**Client:** [[Adaeze Okonkwo-Bell|p1:full]] ("[[Miss Addie|p1:nickname]]") · **DOB:** [[Jan. 4, 1930|dob!:abbreviated month]] · **Age:** [[96|age!:bare age in a form field]]
**Client ID:** [[THH-26-00418|rec:client ID]] · **MBI:** [[4EG7-TK5-MW93|rec:Medicare beneficiary identifier]] · **Cert period:** [[09/14/2026|date]] – [[11/12/2026|date]]
**RN case manager:** [[Tamsin Reyes|p6:full]], RN · **HHA:** [[Luis Carrasquillo|p3:full]]
**PCP:** Dr. [[Imogen Faircloth|p4:full]], [[Faircloth Internal Medicine|o2:full]], [[757-555-0112|phone]]

## Home & access

- [[614 Poplar Hall Lane|addr]], [[Norfolk|place:city]], [[VA|place:state]] [[23502|zip]]. Single-story brick; ramp at side door.
- Lockbox on side door, code **[[1930|cred!:lockbox code that is also a birth year]]**. Alarm panel code [[40418#|cred!:alarm code]]. Do **not** give either to vendors.
- Daughter and POA: [[Ngozi Bell-Hampton|p2:full]], lives in [[Raleigh|place:city]], cell [[919 555 0144|phone!:spaces only]], [[ngozi.bh@familymail.example|email]]. Calls every evening at 7.
- Neighbor "[[Hank|p5:first-name!:first name only, in quotes]]" at [[618|addr!:house number only]] has a key and checks the mail.
- Family care portal: [[https://family.tidewaterhh.example/c/THH-26-00418|url:care portal link]] — daughter's login is [[nbellhampton|cred:username]].

## Diagnoses / meds (from Form CMS-485)

| Problem | Notes |
|---|---|
| [[Alzheimer's dementia, moderate|health:diagnosis]] | MoCA [[14/30|health!:cognitive test score]] in August |
| [[CHF, EF 35%|health!:diagnosis in shorthand]] | [[furosemide 40 mg daily|health:medication and dose]]; daily weights |
| [[COPD on home O2 2 L|health!:diagnosis and oxygen therapy in shorthand]] | concentrator serial [[OC5-2291-447A|dev:oxygen concentrator serial number]] |
| [[Type 2 DM|health!:diagnosis in shorthand]] | [[glipizide 5 mg|health:medication and dose]] with breakfast |
| Recent fall | [[R hip contusion, no fx|health!:injury in shorthand]], ED visit [[10/02/2026|date:ED visit]] |

Also PRN [[lorazepam 0.5 mg|health:medication and dose]] at bedtime for [[sundowning|health:symptom]] — daughter keeps it locked up.

## Visit notes

**[[10/06/2026|date]] ([[TR|p6:initials]])** — Start-of-care reassessment after the fall, OASIS-E completed. [[Weight 131, up 4 lb in a week; ankles 2+|health!:clinical findings]]. Called [[Dr. Faircloth|p4:title-surname]]'s office, new order: [[furosemide 40 mg twice daily x 3 days|health:medication order]], then recheck. Client [[oriented to self only|health!:cognitive status]]. She asked several times for "[[Emeka|p7:first-name!:deceased spouse, first name only]]," [[her late husband|indirect:family relationship]]. PT/OT evals ordered. Medical alert pendant from [[AllHours Medical Alert|o4:full]] was in a drawer; device ID [[AH-PND-0091447|dev:medical alert device ID]]. Put it back on her and tested it.

**[[10/09/2026|date]] ([[LC|p3:initials]])** — Bath and breakfast. Ate about half. She would not let me in at first; thought I was "the man from the bank." Found three envelopes of cash in the bread box, about [[$2,300|money]] total. Told [[Ms. Bell-Hampton|p2:title-surname]] by phone, who says [[her brother|indirect:family relationship]] in [[Lagos|place:city abroad]] sometimes asks their mother to wire money and she wants that stopped.

**[[10/13/2026|date]] (TR)** — Weight 127. Lungs clearer. [[Sat 93% on 2 L|health!:oxygen saturation]]. [[Chesapeake Senior Meals|o3:full]] delivery restarted (5 lunches/wk, client pays [[$3.50|money]] a meal). Discussed with [[Ngozi|p2:first-name]] that Medicare Part A home health will not cover 24-hour care; she is pricing private aides at [[$31/hr|money!:hourly rate with slash]] and thinks the family can manage about [[4k|money!:shorthand k amount]] a month. Client is [[a retired Navy civilian nurse|indirect!:occupation history]]; daughter will look into survivor benefits. Hospice not appropriate yet but explained the benefit.

**[[10/16/2026|date]] (LC)** — [[Miss Addie|p1:nickname]] in good spirits, sang along to the radio. [[BP 138/70|health!:vital sign]]. No new bruises. Hank's truck (VA plate [[XKC-4471|veh:license plate]]) was blocking the ramp again; left a note.

## To do

- [ ] Recert visit due by [[11/10/2026|date]]
- [ ] Ask Dr. Faircloth about a palliative consult
- [ ] Wi-Fi for the telehealth tablet: network "[[BellHouse|cred!:Wi-Fi network name]]", password [[magnolia1930|cred!:Wi-Fi password]]; tablet serial [[TB8-X447-1182|dev:tablet serial number]]
- [ ] Advance directive on file ([[DNR signed 2024|health!:code status]]); copy to fridge folder
''',
))
DOCS[-1]["ents"]["p7"] = "Emeka (client's late husband)"

# ---------------------------------------------------------------- 79
DOCS.append(D(79, "txt", "patient intake form", "health", "CA",
  title="Walk-in clinic new patient registration (Ontario)",
  ents={"p1": "Maria Corazon Dimaculangan", "p2": "Rodel Dimaculangan", "p3": "A. Venkataraman (former family doctor)",
        "p4": "Bituin Dimaculangan",
        "o1": "Lakeshore West Walk-In & Family Clinic", "o2": "Mimico Guardian Drugs",
        "o3": "Sunnybrook Long-Term Care Staffing Ltd.", "o4": "Maple Shield Benefits"},
  distractors=["OHIP", "PHIPA", "SECTION A", "Tylenol", "Form 14", "CPSO"],
  body=r'''
[[LAKESHORE WEST WALK-IN & FAMILY CLINIC|o1:caps]]
[[2890 Lake Shore Blvd W, Unit 4|addr]], [[Etobicoke|place:district]] [[ON|place:province]] [[M8V 1J2|zip:Canadian postal code]]   tel [[416-555-0138|phone]]
NEW PATIENT REGISTRATION -- please print                     Date: [[2026/10/05|date!:year/month/day with slashes]]

SECTION A -- ABOUT YOU
Last name: [[DIMACULANGAN|p1:caps:surname in capitals]]       First: [[Maria Corazon|p1:short!:given names only]]     Goes by: [[Cora|p1:nickname]]
Date of birth (yyyy-mm-dd): [[1979-12-08|dob:ISO format]]            Sex: F
Health card (OHIP) no.: [[4471-882-031-KP|govid:provincial health card number with version code]]      Expiry: [[2029-12-08|date:card expiry]]
Address: [[77 Superior Ave., Apt. 1203|addr]]     City: [[Toronto|place:city]]     Postal code: [[m8v2m8|zip!:postal code, lower case, no space]]
Cell: [[647 555 0171|phone!:spaces only]]      Home: n/a      Email: [[cora_dimaculangan79@mailbox.example|email]]
Preferred language: [[Tagalog|attr!:language indicating ethnic origin]] / English         Interpreter needed?  no
Status in Canada (for billing): [[PR since 2019|attr!:immigration status, abbreviated]]
Occupation: PSW        Employer: [[Sunnybrook Long-Term Care Staffing Ltd.|o3:full]]
Extended benefits: [[Maple Shield Benefits|o4:full]]   plan [[088204|rec!:plan number, bare digits]]   cert [[00447182-01|rec:benefit certificate number]]

EMERGENCY CONTACT
Name: [[Rodel Dimaculangan|p2:full]]     Relationship: [[husband|indirect:family relationship]]     Phone: [[(647) 555-0102|phone]]

FAMILY DOCTOR:  none since moving / last one was Dr. [[A. Venkataraman|p3:short!:initial + surname]] in [[Scarborough|place:district]]
PHARMACY: [[Mimico Guardian Drugs|o2:full]], [[Royal York & Lake Shore|place!:intersection]]  fax [[416-555-0139|phone:fax]]

SECTION B -- HEALTH HISTORY
Reason for today's visit:  [[cough x 3 wks, night sweats, lost 10 lbs|health!:symptoms in patient's own shorthand]]
Allergies:  [[penicillin (hives)|health:allergy]]
Current medications:  [[metformin 500 bid|health!:medication and dose in shorthand]], [[losartan 50|health!:medication and dose in shorthand]], Tylenol as needed
Past medical:  [[diabetes 2018|health:diagnosis with year]], [[high blood pressure|health:diagnosis]], [[C-section 2008|health:surgical history]]
[[TB as a child|health!:past infection]] in [[Batangas|place!:place of origin abroad]] (treated)
Family history:  [[mother - stroke|health:family medical history]]; father - unknown
Smoke? no     Alcohol? occasional     Pregnant? no
Anyone at home unwell?  [[my daughter|indirect:family relationship]] [[Bituin|p4:first-name]] (b. [[2008-03-14|dob:ISO format]]) also coughing

SECTION C -- CONSENT (PHIPA)
I agree the clinic may collect and share my health information with my
other providers for my care. OK to leave detailed voicemail?  YES on cell
Signature: [[M. C. Dimaculangan|p1:short:initials + surname]]         Date: [[Oct 5/26|date!:handwritten style]]

---------------- OFFICE USE ----------------
Chart no. [[LW-118447|rec:chart number]]   HC validated [[Oct 5|date!:no year]] 09:12, response code 50 (valid)
Seen by: Dr. [[K. Oyelowo|p5:short!:initial + surname]], CPSO [[104471|govid!:physician registration number, bare digits]]
Triage note (RN [[SB|p6:initials]]): [[T 37.9, SpO2 96%|health!:vital signs]]. Masked. CXR + sputum x3 ordered; [[TB skin test placed|health!:test ordered]],
read [[Oct 7|date!:no year]]. Public health Form 14 if positive. Employer
is a nursing home agency -- advised [[off work until results|health!:work restriction]]; pt worried,
sends money home monthly and has no sick pay. Note for employer given,
no diagnosis stated.
Visit fee: OHIP billed. Sick note [[$20.00|money]] paid debit.
''',
))
DOCS[-1]["ents"]["p5"] = "K. Oyelowo (clinic physician)"
DOCS[-1]["ents"]["p6"] = "SB (triage nurse, initials only)"

# ---------------------------------------------------------------- 80
DOCS.append(D(80, "pptx", "sales pipeline presentation", "general", "US",
  title="Quarterly sales pipeline review deck",
  ents={"p1": "Tobias Lindgren", "p2": "Imani Okoro", "p3": "Paris Delacroix", "p4": "Vikram Seshadri",
        "p5": "Dr. Lucinda Marsh", "p6": "Hugo Brandt", "p7": "Carmen Ibáñez",
        "o1": "Fieldstone Scheduling Software, Inc.", "o2": "Blue Heron Dental Partners",
        "o3": "Marsh Veterinary Group, P.C.", "o4": "Brandt & Söhne Physiotherapie GmbH",
        "o5": "Cedar Hollow Pediatrics", "o6": "Summit Ortho Alliance"},
  distractors=["Q3", "ARR", "SOC 2", "MEDDIC", "Stage 4", "Net 45", "v4.2"],
  body=r'''
# Q3 Pipeline Review
[[Fieldstone Scheduling Software, Inc.|o1:full]] - Sales team - internal only
Presented by [[Tobias Lindgren|p1:full]], VP Sales - [[October 6, 2026|date:presentation date]]
# Where we landed
- Closed-won ARR: [[$412k|money!:shorthand k amount]] against a plan of [[$450k|money!:shorthand k amount]]
- Two slips into Q4 worth [[$1.3M|money!:shorthand M amount]] combined
- Churn: one logo, [[Cedar Hollow Pediatrics|o5:full]], [[$18,600|money]] ARR, moved to a competitor
- Pipeline coverage for Q4 is 2.8x
# Top open deals
| Account | Owner | Amount | Close |
| [[Blue Heron Dental Partners|o2:full]] | [[Imani|p2:first-name]] | [[$640,000|money]] | [[11/20/2026|date:expected close]] |
| [[Summit Ortho Alliance|o6:full]] | [[Paris|p3:first-name!:name that is also a city]] | [[$655,000|money]] | [[12/11/2026|date:expected close]] |
| [[Marsh Veterinary Group, P.C.|o3:full]] | [[Vikram|p4:first-name]] | [[$84,500|money]] | [[10/30/2026|date:expected close]] |
| [[Brandt & Söhne Physiotherapie GmbH|o4:full]] | [[Imani|p2:first-name]] | [[€120,000|money]] | [[1/15/2027|date:expected close]] |
# Blue Heron - deal notes
- 61 locations; economic buyer is the CFO, [[Carmen Ibáñez|p7:full]] ([[cibanez@blueherondental.example|email]], [[602-555-0177|phone]])
- Stage 4. Legal wants Net 45 and our SOC 2 report
- Risk: [[Blue Heron|o2:short!:shortened account name]] is [[being acquired by a private equity roll-up|indirect!:confidential transaction]], not public yet. Do not mention outside this room
- [[Imani Okoro|p2:full]] to send revised order form by [[10/9|date!:month/day only]]
# [[Marsh Vet|o3:short!:shortened account name]] - deal notes
- Owner-operator: [[Dr. Lucinda Marsh|p5:full:title + full name]], mobile [[(406) 555-0121|phone]]
- She is [[out for chemo|health!:medical treatment of a named contact]] through mid-November; her practice manager is covering. Be kind and do not push
- Paying by card on file ending [[5472|card!:last four only]] for the pilot, [[$1,200|money]] a month
# [[Brandt|o4:short!:one-word account nickname]] (first EU deal)
- Contact: [[Hugo Brandt|p6:full]], [[hugo@brandt-physio.example|email]], [[+49 30 555 0142|phone:international format]]
- Wants invoices in euros to IBAN [[DE89 3704 0044 0532 0130 00|iban:spaced]]? No - that is THEIR account for our refund of the pilot deposit, [[€2,500|money]]
- Needs data residency answer before signature
# Demo environment (v4.2)
- [[https://demo.fieldstone.example/q4-sandbox|url:demo environment link]]
- Login [[sales_demo|cred:username]] / [[Pipeline#Q4go|cred!:password on a slide]] - rotate after the offsite
- Allow-listed office IP: [[198.51.100.77|ip:IPv4]]; VPN gateway [[2001:db8:44:a1::17|ip!:IPv6]]
# Asks
- [[Paris Delacroix|p3:full!:first name is also a city]] needs a sales engineer for the [[Summit Ortho|o6:short!:shortened account name]] bake-off the week of [[November 9|date!:no year]]
- [[Vikram Seshadri|p4:full]]: approve a 12 percent discount for [[Marsh|o3:short!:one-word account nickname]], floor is [[76k|money!:shorthand k amount]]
- MEDDIC refresh for new hires - [[Tobias|p1:first-name]] to schedule
''',
))
