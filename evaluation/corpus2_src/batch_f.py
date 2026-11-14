from corpus2_src.core import D, dt, amt, num

DOCS = []
BATCH_COMMON = ["unit", "room", "bed", "resident", "tenant", "landlord", "auditor", "petitioner", "camper",
                "campers", "guarantor", "nanny", "bookkeeper", "loan", "loans", "collateral", "timeline",
                "admission", "pickup", "session", "sessions", "per", "incident", "incidents", "screenshots",
                "exhibit", "declaration", "affidavit", "authorized", "emergency", "medical", "financial",
                "religious", "advance", "directives", "equipment", "devices", "valuables", "inventory"]

# ---------------------------------------------------------------- 251
DOCS.append(D(251, "md", "text message exhibit", "legal", "CA",
  title="Exhibit C - text messages between tenant and landlord",
  ents={"p1": "Summer Doucette", "p2": "Gurpreet Mangat", "p3": "Rakesh Mangat", "p4": "Delphine Achieng",
        "p5": "Olive Doucette", "p6": "Tyrell Bundy", "p7": "Joy Mangat",
        "o1": "Mangat Family Rentals Ltd.", "o2": "Loomis Achieng Legal Services",
        "o3": "Wexford Savings Credit Union"},
  distractors=["Residential Tenancies Act, 2006", "Form T2", "Form T6", "Interac e-Transfer", "s. 20(1)", "N4"],
  ok=["C", "EXHIBIT", "Tenant's", "LSO", "Tenant", "Landlord", "Messages", "Transcribed", "Board", "2", "3rd",
      "14", "LOL", "U", "Oct", "ODSP", "Sept", "Im", "Rental", "Prepared", "Legend", "Paralegal's", "D", "Rent",
      "Spelling"],
  body=r'''# EXHIBIT "C" to the Affidavit of [[Summer Doucette|p1:full!:first name is a common word]]

Landlord and Tenant Board file **[[LTB-T-048812-25|rec:tribunal file number]]** (Form T2 and Form T6 applications, heard together)
Rental unit: [[Unit 2, 318 Barton Lane|addr:unit-first address]], [[Hamilton|place:city]] [[ON|place:province abbreviation]] [[L8H 2V6|zip:Canadian postal code]]
Prepared by [[Delphine Achieng|p4:full]], licensed paralegal (LSO # [[P14772|govid:law society number]]), [[Loomis Achieng Legal Services|o2:full]], [[905-555-0164|phone]], [[dachieng@loomisachieng.example|email]]

## Legend

Screenshots exported from the Tenant's phone ([[289-555-0117|phone]]) on [[January 9, 2026|date:export date]]. The contact saved as "[[Gary landlord|p2:nickname:contact label]]" is the Landlord, [[Gurpreet Mangat|p2:full]] of [[Mangat Family Rentals Ltd.|o1:full]], texting from [[(905) 555-0139|phone]]. "[[Rocky|p3:nickname:nickname that is a common word]]" is his son [[Rakesh Mangat|p3:full]], who does the repairs and texts from [[9055550181|phone:no separators]]. "[[Ty|p6:nickname]]" is the Tenant's partner, [[Tyrell Bundy|p6:full]]. Spelling is as sent. Transcribed by [[D.A.|p4:initials]]

## Messages

**[[Nov 3|date:abbreviated, no year]], 8:14 pm — [[Summer|p1:first-name!:first name is a common word]]:** Hi [[Gary|p2:nickname]] its Summer in unit 2. furnace is out AGAIN, 3rd time since [[Oct 20|date:abbreviated, no year]]. its 14 degrees in here

**8:31 pm — Gary:** ok will send Rocky tmrw morning. he has the key

**[[Nov 4|date:abbreviated, no year]], 7:02 am — Summer:** pls have him knock first. Ty works nights and my mom [[Olive|p5:first-name!:first name is a common word]] is staying w me after her [[hip replacement|health:surgery of a relative]]

**7:40 am — Rocky:** this is Rocky, new number. side door code still [[4471#|cred:door code]] ? im in [[Brampton|place:city]] till noon

**7:41 am — Summer:** yes. and the [[mould in the bathroom is making my asthma worse|health:condition aggravated by housing]], I told your dad in Sept

**[[Nov 6|date:abbreviated, no year]], 5:55 pm — Gary:** Rocky says furnace needs a part, [[$640|money]]. U still owe [[275|money:no currency sign]] for Oct hydro. and rent was short

**5:58 pm — Summer:** rent was not short!! I sent [[$1,450|money]] by Interac e-Transfer on [[the 1st|date:day of month only]] to [[gmangat.rentals@mailbox.example|email]], password was [[barton318|cred:e-transfer password sent by text]] like always. The other [[$497|money]] comes straight from ODSP, you know [[I'm on disability|attr:benefits status]]

**6:10 pm — Gary:** it went to the old account. new one is [[Wexford Savings|o3:short]] transit [[01882|rtn:Canadian transit number]] acct [[5507731|acct]]. my wife [[Joy|p7:first-name!:first name is a common word]] does the books now, send to [[joy.mangat@mailbox.example|email]]

**[[Nov 19|date:abbreviated, no year]], 9:20 pm — Gary:** i hear your boyfriend is [[on probation|attr:criminal justice status of a third person]]. i dont want police at my building. maybe time u find another place

**9:26 pm — Summer:** thats not your business and its not grounds under the Residential Tenancies Act, 2006. Im keeping these texts

**[[Dec 1|date:abbreviated, no year]], 8:03 am — Gary:** N4 is on your door. [[$1,725|money]] by [[Dec 15|date:abbreviated, no year]] or I file

**8:30 am — Summer:** I owe you nothing. s. 20(1) says YOU fix the heat. My paralegal [[Ms. Achieng|p4:title-surname]] will be in touch

**[[12/19|date:month/day only]], 4:12 pm — Rocky:** dad says drop the hydro cheque at the house, [[77 Gladstone Ave|addr]] in [[Stoney Creek|place:neighbourhood]], mailbox by the garage

**[[Boxing Day|date:holiday used as a date]], 11:47 am — Summer:** heat is off again. [[2nd|date:day of month only, ordinal]] is the earliest Rocky can come?? my mom is [[77 with a new hip|health:age and surgery of a relative]]. [[Mrs. Mangat|p7:title-surname]] isnt answering either

**11:52 am — Gary:** call [[Rakesh|p3:first-name]] not me. LOL happy holidays

## Paralegal's note

Rent ledger from [[Wexford Savings Credit Union|o3:full]] is Exhibit "D". [[Mr. Mangat|p2:title-surname]] has not disputed that the [[Nov 6|date]] and [[Dec 1|date]] messages are his. [[Ms. Doucette|p1:title-surname]] and [[Mr. Bundy|p6:title-surname]] will both attend; [[Olive Doucette|p5:full!:first name is a common word]] by phone at [[519-555-0172|phone]].
'''))

# ---------------------------------------------------------------- 252
DOCS.append(D(252, "txt", "declaration for protective order", "legal", "US",
  title="Declaration of petitioner in support of protection order",
  ents={"p1": "Imogen Haverford", "p2": "Curtis Wren Maddox", "p3": "Posy Haverford", "p4": "Lakshmi Iyer",
        "p5": "Brandon Stojanovic", "p6": "Renee Winslow",
        "o1": "Saltgrass Veterinary Clinic", "o2": "Larchmont Elementary", "o3": "Iyer Family Law PLLC"},
  minors=["p3"],
  distractors=["RCW 7.105.100", "RCW 9A.46.110", "GR 17", "AirTag", "chapter 7.105 RCW", "RCW 9A.72.085"],
  ok=["SUPERIOR", "COURT", "OF", "FOR", "DECLARATION", "PETITIONER", "IN", "SUPPORT", "PETITION", "PROTECTION",
      "ORDER", "No", "Respondent", "Honda", "Toyota", "Tundra", "Glock", "August", "Apple", "Officer",
      "Instagram", "WSBA", "2", "3", "4", "5", "6", "7", "8", "9", "1", "19", "2019", "43", "Civic", "Signed",
      "Counsel", "1,000", "911", "IP", "Mail", "Several"],
  body=r'''SUPERIOR COURT OF [[WASHINGTON|place:state in a caps court heading]] FOR [[PIERCE COUNTY|place:county in a caps court heading]]

[[IMOGEN HAVERFORD|p1:caps:name in caption]], Petitioner,          No. [[25-2-04418-6|rec:civil case number]]
        v.
[[CURTIS WREN MADDOX|p2:caps:name in caption]], Respondent.        DECLARATION OF PETITIONER IN SUPPORT
                                           OF PETITION FOR PROTECTION ORDER
                                           (chapter 7.105 RCW)

I, [[Imogen Haverford|p1:full]], declare:

1. I am the Petitioner. I was born [[06/14/1991|dob]]. Respondent [[Curtis Maddox|p2:short]] (DOB [[2/27/88|dob:two-digit year, no leading zero]]) and I
   lived together from 2019 until [[March 2023|date:month and year]]. We have one child, [[Posy|p3:first-name!:child's first name, also a common word]], age 7, [[a second grader|indirect:child's grade at a named school]]
   at [[Larchmont Elementary|o2:full]]. Our parenting plan is under [[23-3-01187-2|rec!:unlabelled family case number]].

2. My home address is confidential under GR 17. Mail goes to [[PO Box 4418|addr:PO Box]], [[Tacoma|place:city]], [[WA|place:state abbreviation]] [[98402|zip]].
   I work as a vet tech at [[Saltgrass Veterinary Clinic|o1:full]], [[6120 Pearl Street North|addr]], Tacoma.
   [[Curtis|p2:first-name]] lives at [[1907 S. Yakima Ave., Apt. C|addr:street with apartment]], Tacoma [[98405|zip]].

3. On [[September 12, 2025|date]] I found an Apple AirTag taped inside the rear bumper of my car, a gray Honda
   Civic, plate [[BXK2284|veh:license plate]]. The serial printed inside the battery cover is [[HGXT42LMP0QW|dev:tracker serial number]]. Officer
   [[Brandon Stojanovic|p5:full]] (badge [[#3317|govid:badge number]]) took it under incident no. [[2525501472|rec!:police incident number, no separators]].

4. Between [[Sept. 14|date:abbreviated, no year]] and [[October 3, 2025|date]] I got 43 emails from [[posys.real.dad@inbox.example|email]], an account I
   do not know. Several described what I wore that day. My lawyer's office pulled the headers: most came
   from IP [[203.0.113.58|ip:IPv4]] and two from [[2001:db8:4c2:11::7a|ip:IPv6]]. The same person runs the Instagram handle
   [[@curt_maddox_253|cred:social media handle]], which posted a photo of the clinic parking lot on [[10/01/25|date:two-digit year]].

5. On [[October 3|date:no year]] Curtis waited by Posy's school in his black Toyota Tundra (WA plate [[C81 447K|veh:license plate with a space]]). The
   office manager, [[Renee Winslow|p6:full]], walked [[Posy Haverford|p3:full]] back inside and called 911. [[Ms. Winslow|p6:title-surname]] will
   testify. Incident no. [[25-276-0931|rec:police incident number]].

6. Curtis told me in August that he had [[stopped taking his lithium|health:medication non-adherence]]. He has a
   [[2016 conviction for fourth-degree assault|attr:criminal history]] and he owns a Glock 19, serial [[BKRT918|dev:firearm serial number]], which he kept in the truck.

7. Since this started I have had [[panic attacks|health:symptom]] and my doctor put me on [[sertraline 50 mg|health:medication and dose]]. Posy has
   [[started wetting the bed again|health:symptom of a child]]. I changed my number to [[(253) 555-0126|phone]]; the old one, [[253.555.0190|phone:dotted]],
   still gets his voicemails.

8. He has also called the clinic line, [[253-555-0103|phone]], hanging up when anyone but me answers, and on [[the 9th|date:day of month only]]
   he left a note on my windshield signed "[[C.W.M.|p2:initials]]" that said he "knows the Spanaway place" -- that is
   [[my mother's house|indirect:relative's home]] in [[Spanaway|place:town]], where Posy and I have been sleeping.

9. I ask for an order under RCW 7.105.100 restraining [[Mr. Maddox|p2:title-surname]] from contacting me or Posy, from coming
   within 1,000 feet of my work, Posy's school or my mother's house, and requiring surrender of firearms. His
   conduct is stalking as defined in RCW 9A.46.110.

I declare under penalty of perjury under the laws of the State of [[Washington|place:state]] (RCW 9A.72.085) that the
foregoing is true. Signed at Tacoma, Washington, on [[October 6, 2025|date:signing date]].

/s/ Imogen Haverford

Counsel: [[Lakshmi Iyer|p4:full]], WSBA No. [[51903|govid:state bar number]], [[Iyer Family Law PLLC|o3:full]]
[[lakshmi@iyerfamilylaw.example|email]]  |  [[253-555-0158|phone]]  |  file [[IFL-2025-0388|rec:firm file number]]
'''))

# ---------------------------------------------------------------- 253
DOCS.append(D(253, "txt", "household employee payroll setup notes", "accounting", "US",
  title="Household employer setup notes - nanny payroll",
  ents={"p1": "Rohan Mistry", "p2": "Katrin Falk", "p3": "Marisela Quispe", "p4": "Juno Mistry-Falk",
        "p5": "Emil Mistry-Falk", "p6": "Ifeoma Balogun", "p7": "Wendell Thackeray",
        "o1": "Balogun & Thackeray CPAs", "o2": "Quince Household Payroll LLC",
        "o3": "Juneberry Community Bank"},
  minors=["p4", "p5"],
  distractors=["Schedule H", "Form W-4", "Form I-9", "Form W-2", "Form SS-4", "Form UI-HA", "Publication 926",
               "Form 1040-ES", "Form 2441", "List A", "IL-W-4", "FUTA", "FICA"],
  ok=["IDES", "EAD", "TVDL", "FSA", "OT", "Q4", "2026", "45", "40", "1.5", "2", "3", "1", "6", "Employer",
      "Employee", "Household", "Kids", "Wage", "Direct", "I-9", "W-4", "Fridays", "E", "Verify", "January",
      "Login", "RE", "Registrations", "Workers"],
  body=r'''[[BALOGUN & THACKERAY CPAs|o1:caps:letterhead]] -- workpaper note
Client: [[Mistry|p1:surname]] / [[Falk|p2:surname]] household        Client no. [[HH-2291|rec:client number]]
Prepared: [[IB|p6:initials]], [[11/18/2025|date]]        Reviewed: [[WT|p7:initials]] [[11/20|date:month/day only]]

RE: Household employer setup -- nanny starting [[December 1, 2025|date:start date]]

Employer of record will be [[Rohan Mistry|p1:full]] (SSN [[528-18-2569|ssn]]); his wife [[Katrin Falk|p2:full]] signs the checks.
Home: [[2214 Asbury Avenue|addr]], [[Evanston|place:city]], [[IL|place:state abbreviation]] [[60201|zip]]. [[Rohan|p1:first-name]]'s cell [[847-555-0119|phone]], [[Katrin|p2:first-name]]
[[(847) 555-0162|phone]], [[katrin.falk@mailbox.example|email]].

Kids: [[Juno|p4:first-name]] (6, born [[4/9/2019|dob:no leading zeros]]) and [[Emil|p5:first-name]] (3, born [[2022-08-30|dob:ISO format]]). [[Juno Mistry-Falk|p4:full]] has
[[type 1 diabetes|health:diagnosis of a child]] so the nanny does glucose checks -- Katrin wants that written into the work agreement.
[[Emil Mistry-Falk|p5:full]] is in half-day preschool; dependent care FSA election for 2026 is [[$5,000|money]] (Form 2441).

Employee: [[Marisela Quispe|p3:full]], SSN [[516-97-2499|ssn]], DOB [[March 3, 1998|dob]].
  [[1630 W. Lunt Ave., #3B|addr:street with unit]], [[Chicago|place:city]], IL [[60626|zip]]     cell [[773 555 0144|phone:spaces only]]
  Form I-9 completed [[11/17/2025|date]]. List A document: EAD card no. [[SRC2190451177|govid:employment authorization card number]], expires [[09/14/2027|date:expiry date]].
  She is a [[DACA recipient, EAD category C33|attr:immigration status]] -- calendar the reverification. [[Illinois|place:state]] TVDL
  [[Q212-5549-8071|govid:driver's license number]] seen for the car-insurance rider only, not for the I-9.
  Form W-4: single, no adjustments. IL-W-4: 1 allowance.
  [[Marisela|p3:first-name]] told Katrin she is [[expecting, due in late March|health:pregnancy]]. Not our business for payroll but Katrin
  asked about leave; told her to talk to an employment lawyer, not us.

Wage: [[$24.00/hr|money:hourly rate]], 45 hrs/wk guaranteed, OT at 1.5 over 40 = [[$36.00|money]]. Gross per week
[[$1,140.00|money]]. Paid biweekly on Fridays, first check [[12/12/25|date:two-digit year]]. Year-end bonus of [[five hundred dollars|money:amount in words]]
promised in the offer email -- taxable, run through payroll.

Registrations
  - Household EIN applied online (Form SS-4) [[11/18/2025|date]]: [[39-4417205|taxid:EIN]]
  - IDES household account (Form UI-HA) [[5512889-0|taxid:state unemployment account number]], rate letter pending
  - Illinois withholding: registered under the EIN, seq. [[39-4417205-001|taxid:state withholding account number]]
  - Workers' comp rider on the homeowner's policy [[HO-7720418-03|rec:policy number]] -- Rohan to confirm with agent

Payroll service: [[Quince Household Payroll LLC|o2:full]] ([[Quince|o2:short]]), plan [[$49|money]]/mo. Login created for Katrin:
[[kfalk.household|cred:username]]. They file Schedule H figures to us in January and issue the Form W-2.

Direct deposit (voided check on file): [[Juneberry Community Bank|o3:full]], routing [[073809607|rtn]], checking
[[004418207755|acct]]. Employer debit account is the joint checking ending [[-6021|acct:last four with leading dash]] at the same bank.

To-do
  1. Q4 Form 1040-ES voucher for Rohan needs to go up by about [[$1,900|money]] to cover employer FICA and FUTA.
  2. Send [[Ms. Quispe|p3:title-surname]] Publication 926 excerpt and the pay schedule.
  3. E-Verify not required for household employers -- told [[Mr. Mistry|p1:title-surname]] to stop asking her for more documents.

[[Ifeoma Balogun|p6:full]], CPA  |  [[ifeoma@balogunthackeray.example|email]]  |  [[312-555-0170 x12|phone:with extension]]
cc: [[Wendell Thackeray|p7:full]]
'''))

# ---------------------------------------------------------------- 254
DOCS.append(D(254, "txt", "GST/HST audit notes", "accounting", "CA",
  title="HST audit - meeting notes and open items",
  ents={"p1": "Lucien Arsenault", "p2": "Odette Arsenault", "p3": "Priyanka Venugopal", "p4": "Maeve Tierney",
        "p5": "Dougal Fitzroy",
        "o1": "Saltfleet Marine Canvas & Upholstery Ltd.", "o2": "Kittering Tierney Chartered Professional Accountants",
        "o3": "Fundy Tidal Credit Union", "o4": "Eastern Passage Yacht Club", "o5": "Zephyr Sailcloth Imports Inc."},
  cardholders=["p1", "p2"],
  distractors=["Excise Tax Act", "subsection 169(1)", "subsection 15(2)", "Form RC59",
               "section 285", "T2", "Income Tax Act"],
  ok=["HST", "ITCs", "CRA", "Visa", "Ford", "F-150", "2021", "3", "4", "1", "2", "38", "Costco", "Audit",
      "Attendees", "Vehicle", "Personal", "Proposed", "Next", "Bank", "Q3", "Halifax", "Tax", "Centre", "100%",
      "15/115", "50%", "62%", "BN", "Commodore", "Imports", "Meeting", "Owner", "RC0001", "RP0001", "SIN",
      "Supplier's", "Unreported"],
  body=r'''[[Kittering Tierney Chartered Professional Accountants|o2:full]]
File note -- HST audit, [[Saltfleet Marine Canvas & Upholstery Ltd.|o1:full]] ("[[Saltfleet|o1:short]]")
Our file [[KT-0937|rec:firm file number]]        BN [[84417 2290 RT0001|taxid:Canadian business number with program account]]        CRA case [[GA-2511-4470-9|rec:audit case number]]

Meeting [[14 November 2025|date:day month year]], 10:00, at the shop, [[41 Wharf Road, Bay 3|addr:street with bay number]], [[Dartmouth|place:city]] [[NS|place:province abbreviation]] [[B2Y 3Z8|zip:Canadian postal code]]
Attendees: [[Lucien Arsenault|p1:full]] (owner), [[Maeve Tierney|p4:full]] CPA ([[MT|p4:initials]]), CRA auditor [[Priyanka Venugopal|p3:full]]
(Halifax Tax Centre, [[902-555-0148 ext. 4417|phone:with extension]], [[priyanka.venugopal@taxcentre.example|email]]).

Audit period: [[2023-01-01|date:ISO format]] to [[2024-12-31|date:ISO format]], quarterly filer. Payroll (RP0001) and corporate (RC0001) accounts
under the same BN are not in scope, although she asked for the T2 schedules.

1. Vehicle. 2021 Ford F-150, plate [[GXK 418|veh:licence plate with a space]], VIN [[1FTFW1E87MKD40193|veh:VIN]]. 100% of fuel and repair ITCs were
   claimed. No logbook. [[Lucien|p1:first-name]] estimates 62% business. Auditor will allow 62% if he reconstructs a log from
   the job calendar; otherwise she proposes 50%. ITCs at risk about [[$3,180|money]].

2. Personal charges on the company Visa. Two cards on the account: the one ending [[3360|card:last four only]] is Lucien's and
   the one ending [[2060|card!:last four that looks like a year]] is carried by his wife, [[Odette Arsenault|p2:full]], who is not an employee. Auditor
   pulled 38 charges on [[Odette|p2:first-name]]'s card (Costco, a [[Florida|place:state where a personal trip was taken]] condo rental [[Feb 2024|date:month and year]], [[her physiotherapy|health:treatment]])
   totalling [[C$11,942.17|money:Canadian dollar prefix]] on which HST of [[1,557.67|money:no currency sign]] was claimed. Denied under subsection 169(1) of
   the Excise Tax Act. MT conceded. These also need to go through the shareholder loan -- subsection 15(2)
   of the Income Tax Act exposure if not repaid by [[Dec. 31, 2025|date:abbreviated month]].

3. Imports. [[Zephyr Sailcloth Imports Inc.|o5:full]] invoices [[ZS-20418|rec:invoice number]] and [[ZS-20455|rec:invoice number]] ([[C$8,400.00|money]] and [[C$6,115.50|money]])
   show no HST number. Supplier's BN per Lucien is [[70219 5548 RT0001|taxid:Canadian business number]]; auditor will verify on the registry.

4. Unreported sale. Deposit of [[$23,000.00|money]] on [[June 6, 2024|date]] from [[Eastern Passage Yacht Club|o4:full]] ([[EPYC|o4:acronym]]) for the
   clubhouse awnings was booked to shareholder loan. Commodore [[Dougal Fitzroy|p5:full]] confirmed by email it was
   a progress payment. HST collectible [[$3,000.00|money]] -- included in the price, so it is 15/115. Auditor is
   considering a section 285 gross negligence penalty; MT argued bookkeeping error, the
   [[former bookkeeper was Lucien's sister-in-law|indirect:family relationship to owner]] and left in Q3.

Bank: [[Fundy Tidal Credit Union|o3:full]], transit [[00417|rtn:Canadian transit number]], institution [[839|rtn:Canadian institution number]], chequing [[2204418|acct]]. Auditor wants
statements for [[Dec 2024|date:month and year]] and written confirmation that there is no second account.

Owner details she took for the file: Lucien Arsenault, SIN [[499 743 706|taxid:SIN with spaces]], home [[9 Shore Drive|addr]],
[[Eastern Passage|place:community]], NS [[B3G 1M4|zip:Canadian postal code]], cell [[902 555 0117|phone:spaces only]].

Proposed assessment (auditor's draft, before interest): [[$7,737.67|money]] plus penalty to be decided.
Next: logbook and Form RC59 to [[Ms. Venugopal|p3:title-surname]] by [[28 Nov|date:day month, no year]]. MT to draft representation letter.
[[Mrs. Arsenault|p2:title-surname]] to return her card. Fee estimate to client [[$2,400|money]] plus HST.
'''))

# ---------------------------------------------------------------- 255
DOCS.append(D(255, "docx", "bank confirmation request", "accounting", "US",
  title="Audit confirmation request to financial institution",
  ents={"p1": "Selim Yilmaz", "p2": "Corinne Osgood", "p3": "Thaddeus Marlowe", "p4": "Bianca Trevino",
        "p5": "Nadia Petrov", "p6": "Hollis Marlowe",
        "o1": "Osgood Yilmaz & Partners LLP", "o2": "Tolland Valley Bank & Trust",
        "o3": "Ravenna Aggregate & Paving, Inc.", "o4": "Ravenna Aggregados, S.L."},
  distractors=["AU-C Section 505", "SOFR", "UCC-1", "Kenworth T880", "Caterpillar 320"],
  ok=["STANDARD", "CONFIRMATION", "REQUEST", "Balance", "Rate", "Maturity", "Collateral", "Operating", "Money",
      "Market", "Term", "Revolving", "Authorized", "Deposit", "Other", "Sincerely", "Bank", "Use", "Only",
      "Confirmations", "Department", "Client", "2022", "2023", "1", "2", "3", "4", "Customer", "Loan", "By",
      "Title", "CFO", "CPA", "Exceptions", "Payroll", "Borrowings", "Standby", "Engagement", "Principal", "1.85%",
      "2.10%", "6.25%", "BALANCES", "Confirm", "Confirmation", "Controller", "Portable", "Spanish",
      "Transportation"],
  header="[[Osgood Yilmaz & Partners LLP|o1:full]] - Confirmation [[CONF-25-1187|rec:confirmation request number]]",
  body=r'''# STANDARD CONFIRMATION REQUEST - DEPOSIT AND LOAN BALANCES
[[January 12, 2026|date:letter date]]
[[Tolland Valley Bank & Trust|o2:full]], Confirmations Department
[[400 Campbell Avenue SW, 6th Floor|addr:street with floor]], [[Roanoke|place:city]], [[VA|place:state abbreviation]] [[24011|zip]]
By fax [[540-555-0199|phone:fax]] and to [[confirmations@tollandvalley.example|email]]
Customer: **[[Ravenna Aggregate & Paving, Inc.|o3:full]]** (EIN [[54-2204417|taxid:EIN]]), [[2285 Quarry Spur Road|addr]], [[Salem|place:city]], VA [[24153|zip]]
In connection with our audit of the financial statements of [[Ravenna|o3:short]] as of [[December 31, 2025|date:balance date]], performed under AU-C Section 505, please confirm directly to us the information below as of the close of business on that date. If a balance is blank, please supply it.
## 1. Deposit accounts
| Account | Number | Rate | Balance |
| Operating | [[7720 0418 3306|acct:account number with spaces]] | none | [[$412,880.19|money]] |
| Payroll | [[7720 0418 3314|acct:account number with spaces]] | none | [[$38,204.66|money]] |
| Money Market | [[MM-90417726|acct:money market account number]] | 1.85% | [[$1,150,000.00|money]] |
All three carry routing number [[052559680|rtn]]. Per the client the payroll account was overdrawn by [[(2,114.09)|money:parenthesized negative, no currency sign]] on [[12/29/25|date:two-digit year]]; please note any overdraft fees.
## 2. Borrowings
| Loan | Number | Rate | Maturity | Principal |
| Term | [[TL-0044172|rec:loan number]] | 6.25% | [[03/15/2029|date:maturity date]] | [[$684,512.40|money]] |
| Revolving | [[RLOC-0044190|rec:loan number]] | SOFR + 2.10% | [[June 30, 2026|date:maturity date]] | [[$250,000.00|money]] |
Collateral for the term loan, per the UCC-1 on file:
- 2022 Kenworth T880 tractor, VIN [[1XKZD40X5NJ418827|veh:VIN]], [[Virginia|place:state]] plate [[TX-48817|veh:license plate]]
- 2023 Caterpillar 320 excavator, serial [[CAT0320XHYB02217|dev:equipment serial number]]
- Portable crushing plant, serial no. [[PCP-7-00931|dev:equipment serial number]] (title held by the Bank)
The revolving line is guaranteed personally by [[Thaddeus Marlowe|p3:full]] (President) and his brother [[Hollis Marlowe|p6:full]]. Please state the available commitment (we understand [[$750,000|money]]) and whether any covenant waiver was issued after [[Sept. 30, 2025|date:abbreviated month]].
## 3. Authorized signers
Please list all authorized signers. Our records show [[T. Marlowe|p3:short:initial + surname]], [[Bianca Trevino|p4:full]] (CFO) and, until her resignation on [[10/17/2025|date:resignation date]], [[Nadia Petrov|p5:full]] (Controller). Confirm the date [[Ms. Petrov|p5:title-surname]] was removed.
## 4. Other
- Standby letter of credit [[SB-25-00612|rec:letter of credit number]] for [[$125,000.00|money]] in favor of the Virginia Department of Transportation.
- Any accounts of the Spanish subsidiary, [[Ravenna Aggregados, S.L.|o4:full]] We are aware of a euro account, IBAN [[ES59 2487 9294 8163 9114 9968|iban:IBAN in groups of four]], SWIFT [[TVBTUS3RXXX|acct:SWIFT code]] used as correspondent, with a balance of about [[EUR 96,400|money:currency code before amount]].
- Company credit cards, safe deposit boxes, or interest rate swaps not listed above.
Please return this form directly to [[Selim Yilmaz|p1:full]], CPA, at [[syilmaz@osgoodyilmaz.example|email]] or [[1200 Jefferson Street, Suite 410|addr:street with suite]], [[Lynchburg|place:city]], VA [[24504|zip]]; questions to [[(434) 555-0127|phone]]. Do not send your reply to the client.
Sincerely,
[[Corinne Osgood|p2:full]], Engagement Partner
## Customer authorization
The Bank is authorized to release the requested information to [[Osgood Yilmaz|o1:short]].
By: [[Bianca Trevino|p4:full]], CFO, [[Ravenna Aggregate & Paving, Inc.|o3:full]] - [[btrevino@ravennapaving.example|email]] - [[540.555.0131|phone:dotted]] - signed [[1/9/2026|date:no leading zeros]]
## Bank Use Only
Exceptions: ____   By: ____   Title: ____   Date: ____''',
  footer="Client matter [[RAV-2025-AUD|rec:engagement code]] - reply to [[S. Yilmaz|p1:short:initial + surname]] only"))

# ---------------------------------------------------------------- 256
DOCS.append(D(256, "txt", "bookkeeping chat export", "accounting", "US",
  title="Chat export - bookkeeper and client, Q3 cleanup",
  ents={"p1": "Marcus Okeke", "p2": "Noelle Drozd", "p3": "Tasha Okeke", "p4": "Deshawn Vale",
        "p5": "Art Sinclair",
        "o1": "Okeke Mobile Detailing LLC", "o2": "Umber Ledger Co.", "o3": "Halloway First Bank",
        "o4": "Zephyr Car Care Supply", "o5": "Sinclair Auto Group"},
  cardholders=["p1"],
  distractors=["QuickBooks Online", "Form 941", "Form 1099-NEC", "Form W-9", "Schedule C", "Venmo", "Texas Comptroller",
               "Form 1099-K"],
  ok=["Export", "PM", "AM", "Q3", "QBO", "Visa", "Sept", "Aug", "600", "W9", "NEVER", "Ford", "Transit", "9",
      "I'll", "I'm", "PO", "W-2"],
  body=r'''Export -- workspace: [[umberledger|cred:workspace handle]]   channel: #okeke-detailing   exported [[2025-10-09|date:ISO format]] 16:02
Members: [[Noelle Drozd|p2:full]] ([[Umber Ledger Co.|o2:full]]), [[Marcus Okeke|p1:full]] ([[Okeke Mobile Detailing LLC|o1:full]])
-----------------------------------------------------------------------

[[Oct 6|date:abbreviated, no year]]
[9:12 AM] [[Noelle|p2:first-name]]: morning [[Marcus|p1:first-name]] -- starting the Q3 bank rec. [[Halloway First Bank|o3:full]] feed in QuickBooks Online
           dropped on [[8/22|date:month/day only]]. can you reconnect?
[9:40 AM] Marcus: I dont remember how. just log in as me. user [[mokeke_detail|cred:bank username]] pw [[Wax0n!Wax0ff22|cred:bank password pasted in chat]]
[9:41 AM] Marcus: itll text me a code hang on
[9:43 AM] Marcus: [[448120|cred:one-time 2FA code]]
[9:44 AM] Noelle: got in. pls don't paste passwords in here, I'm deleting those two. change it tonight.
[9:44 AM] Marcus: lol ok
[10:05 AM] Noelle: feed is back. checking ending [[8834|acct:last four only]] and the savings [[...0271|acct:last four with ellipsis]]. Q3 deposits total [[$61,480.25|money]],
           QBO shows [[58.9k|money:shorthand k amount, no currency sign]]. the gap is mostly Venmo.
[10:07 AM] Marcus: yeah [[Sinclair Auto Group|o5:full]] pays the fleet washes by venmo now. [[Art|p5:first-name!:first name is a common word]] said its easier. like [[2,600|money:no currency sign]] a month
[10:09 AM] Noelle: that's income, it has to go on the books. it'll show on a Form 1099-K anyway. is that [[Art Sinclair|p5:full!:first name is a common word]] the
           owner or the dealership? need a W9 name
[10:10 AM] Marcus: dealership. EIN is on their PO i think. [[74-2918840|taxid!:unlabelled-looking EIN]]

[1:30 PM] Noelle: next -- [[Zephyr Car Care Supply|o4:full]] autopay bounced [[9/15|date:month/day only]], they charged a [[$35|money]] fee. card on file
           expired?
[1:52 PM] Marcus: new card came in Aug. here
[1:52 PM] Marcus: [[4598 2375 1965 5177|card:card number with spaces]] exp [[08/29|exp]] cvv [[614|cvv]] name on it is [[MARCUS T OKEKE|p1:caps:name as embossed on card]]
[1:53 PM] Noelle: Marcus. NEVER the full number in chat!! I updated [[Zephyr|o4:short]] and I'm deleting that message too.
[1:53 PM] Noelle: for our notes it's the biz Visa ending [[5177|card:last four only]].
[1:55 PM] Marcus: sorry. also heads up theres personal stuff on that card. [[Tasha|p3:first-name]]'s [[chemo copays|health:treatment of a spouse]], like [[$312.87|money]] and
           [[$1,150|money]] in Sept
[1:57 PM] Noelle: ok. I'll book those to owner draw, not medical -- not a Schedule C expense. hope [[Tasha Okeke|p3:full]] is doing ok.

[[Oct 7|date:abbreviated, no year]]
[8:15 AM] Noelle: payroll q. [[Deshawn|p4:first-name]] -- is he W-2 or contractor? I see cash withdrawals every Friday, about [[eleven hundred|money:amount in words]] a week
[8:31 AM] Marcus: contractor. [[Deshawn Vale|p4:full]]. hes got his own van
[8:33 AM] Noelle: then I need a Form W-9 from him before I can do the Form 1099-NEC. anything over 600 for the year.
[8:34 AM] Marcus: his social is [[807-41-4568|ssn!:unlabelled SSN in chat]] he texted it to me. addr [[5118 Cullen Blvd Apt 12|addr:street with apartment]] [[Houston|place:city]] [[77004|zip]]
[8:35 AM] Noelle: ...ok, I still need the signed form. cell for him?
[8:35 AM] Marcus: [[7135550148|phone:no separators]]
[8:50 AM] Noelle: also the [[$4.2k|money:shorthand k amount]] to "[[H. County Child Support|indirect:payee that reveals a support order]]" on [[9/3|date:month/day only]] -- that's personal right?
[8:52 AM] Marcus: yeah [[my child support comes out of that account|attr:family court obligation]], always has. [[last Tues|date:relative weekday]] too
[8:53 AM] Noelle: owner draw then. please move that to your personal account.

[3:20 PM] Noelle: sales tax. Texas Comptroller taxpayer no. [[32071844190|taxid!:state taxpayer number, bare digits]], Q3 due [[10/20|date:month/day only]]. taxable sales [[$48,112.00|money]],
           tax [[$3,969.24|money]]. ok to file and draft from [[8834|acct]]?
[3:31 PM] Marcus: do it
[3:32 PM] Noelle: done, confirmation [[0482-7719-33|rec:filing confirmation number]]. Q3 package is here:
           [[https://share.umberledger.example/u/okeke-detail/2025-q3|url:client folder link containing client name]]
           Form 941 is next -- I'll need the EIN letter, I have [[87-3340921|taxid:EIN]] but want to confirm.
[3:40 PM] Marcus: thats right. call me if u need me [[832-555-0177|phone]], im at the Ford Transit job til 9
[3:41 PM] Noelle: reminder to change the bank password. -- [[ND|p2:initials]]
'''))

# ---------------------------------------------------------------- 257
DOCS.append(D(257, "pdf", "wire fraud incident memo", "accounting", "US",
  title="Incident memo - fraudulent change of vendor payment instructions",
  ents={"p1": "Dominika Szabo", "p2": "Howard Fennimore", "p3": "Renata Aguilar", "p4": "Kofi Adjei",
        "p5": "Trent Nilsson", "p6": "Wes Lindahl",
        "o1": "Fennimore Kaplan CPAs, PLLC", "o2": "Garnet Hollow Vineyards, LLC",
        "o3": "Vireo Bottling Solutions Inc.", "o4": "Ironwood IT Partners",
        "o5": "Pemberly National Bank", "o6": "Nettlebank Specialty Insurance Company"},
  distractors=["IC3", "IRS Publication 4557", "Gramm-Leach-Bliley Act", "FTC Safeguards Rule",
               "16 C.F.R. Part 314", "SPF", "DKIM"],
  ok=["PRIVILEGED", "AND", "CONFIDENTIAL", "MEMORANDUM", "Summary", "Timeline", "Technical", "Bank", "Losses",
      "Reporting", "MFA", "FBI", "PT", "UK", "September", "1", "2", "3", "4", "5", "6", "72", "30", "Legitimate",
      "Fraudulent", "Second", "Net", "Insurer", "Prepared", "Lagos", "Nigeria", "VPN", "Recalled", "Business",
      "Compromised", "Forensics", "MAC", "Mail", "Managing", "Password", "RSS", "Reset", "W-9s", "Cyber"],
  body=r'''# PRIVILEGED AND CONFIDENTIAL - INCIDENT MEMORANDUM
To: [[Howard Fennimore|p2:full]], Managing Partner
From: [[Kofi Adjei|p4:full]], [[Ironwood IT Partners|o4:full]] (ticket [[IW-88213|rec:IT ticket number]])
Date: [[November 14, 2025|date:memo date]]
Re: Business email compromise - payment diverted from [[Garnet Hollow Vineyards, LLC|o2:full]]
## 1. Summary
On [[Thursday, November 6|date:date with weekday, no year]], staff accountant [[Dominika Szabo|p1:full]], who runs outsourced accounts payable for [[Garnet Hollow|o2:short]] (client no. [[GHV-0417|rec:client number]]), released a wire of [[$84,310.00|money]] to an account controlled by a fraudster posing as [[Vireo Bottling Solutions Inc.|o3:full]] A second request for [[$41,950|money]] to a UK account was stopped. [[Fennimore Kaplan CPAs, PLLC|o1:full]] ("[[FK|o1:acronym]]") has recovered [[$52,000.00|money]] so far.
## 2. Timeline (all times PT)
- [[Oct. 28|date:abbreviated, no year]] 07:44 - [[Dominika|p1:first-name]] receives a "shared invoice" email and enters her password at [[https://login.micros0ft-365.example/auth?id=dszabo|url:phishing URL containing the username]]. No MFA prompt; MFA had been switched off for her mailbox during a phone migration in September.
- [[Oct. 28|date]] 07:51 - first foreign sign-in to her mailbox from [[203.0.113.142|ip:IPv4]] (VPN exit, Lagos, Nigeria). An inbox rule named ".." starts moving anything from [[Vireo|o3:short]] to the RSS folder.
- [[Nov. 4|date:abbreviated, no year]] - attacker replies in an existing thread from [[ar@vireo-bottIing.example|email:look-alike sender address (capital I for l)]] (the real address is [[ar@vireobottling.example|email]]) with "updated remittance details".
- [[Nov. 6|date:abbreviated, no year]] 10:22 - Dominika updates the vendor record and releases wire ref. [[20251106B6Q8021C004417|rec:wire reference number]] from the client's operating account.
- [[Nov. 10|date:abbreviated, no year]] - second email asks that the next payment go to the UK account. Client controller [[Renata Aguilar|p3:full]] calls the real vendor contact, [[Wes Lindahl|p6:full]] (cell [[503 555 0166|phone:spaces only]]); [[Mr. Lindahl|p6:title-surname]] says nothing has changed. [[Ms. Aguilar|p3:title-surname]] calls us at 14:10.
- [[Nov. 10|date]] 14:35 - recall request filed with [[Pemberly National Bank|o5:full]], fraud officer [[Trent Nilsson|p5:full]], case [[FR-2025-110932|rec:bank fraud case number]].
## 3. Technical findings
- Compromised account: [[dszabo@fennimorekaplan.example|email]], username [[FKCPA\dszabo|cred:domain username with backslash]]. Password at the time was [[Harvest#2024|cred:compromised password]], reused on her personal webmail. Reset [[Nov. 10|date]].
- Her laptop [[FK-LT-0417|dev:workstation hostname]] (serial [[PF3XK9T2|dev:laptop serial number]], MAC [[3C:52:82:9A:1F:E0|dev:MAC address]], office address [[10.20.4.31|ip:private IPv4]]) was imaged; no malware found.
- Other sign-ins came from [[198.51.100.77|ip:IPv4]] and [[2001:db8:a41c::22|ip:IPv6]]. Mail was read for nine days. About 72 messages with client W-9s and one payroll file were opened.
- The look-alike domain passed SPF and DKIM because the attacker registered and configured it properly.
## 4. Bank details
- Legitimate: [[Vireo Bottling|o3:short]] - routing [[127024118|rtn]], account [[4410 882 0193|acct:account number with spaces]].
- Fraudulent: routing [[026229124|rtn]], account [[9900417726|acct]], in the name "[[V B Solutions|o3:short:fraudulent look-alike payee name]]".
- Second request: IBAN [[GB62NWBK88495877963232|iban:IBAN without spaces]], [[London|place:city abroad]].
## 5. Losses and recovery
- Wire sent: $84,310.00. Recalled [[Nov. 12|date:abbreviated, no year]]: $52,000.00. Net exposure: [[$32,310.00|money]].
- Insurer: [[Nettlebank Specialty Insurance Company|o6:full]], retention [[$10,000|money]].
- Cyber policy [[NSI-CY-0091847|rec:policy number]]
- Claim [[CL-25-447190|rec:claim number]]
- Forensics and counsel to date: [[$7.5K|money:abbreviated amount]].
## 6. Reporting and next steps
- IC3 complaint filed [[11/10/2025|date]], no. [[I2511108834|rec:complaint number]]. [[Mr. Nilsson|p5:title-surname]] ([[trent.nilsson@pemberlynb.example|email]]) is the contact for the FBI.
- Client notified in writing [[Nov. 11|date:abbreviated, no year]]; [[Howard|p2:first-name]] to call Ms. Aguilar at [[(503) 555-0109|phone]] about reimbursing the net loss.
- Because client tax data was viewed, the FTC Safeguards Rule (16 C.F.R. Part 314) and IRS Publication 4557 apply; we must also consider notice under the Gramm-Leach-Bliley Act.
- MFA re-enabled for all 30 mailboxes. Call-back verification of any change to payee bank details, using a number already on file, is now mandatory.
Prepared by [[K. Adjei|p4:short:initial + surname]] - [[kofi@ironwoodit.example|email]] - [[503.555.0184|phone:dotted]]
'''))

# ---------------------------------------------------------------- 258
DOCS.append(D(258, "eml", "patient billing statement email", "health", "US", enc="qp",
  title="Billing statement email to guarantor",
  ents={"p1": "Hye-jin Shin", "p2": "Daniel Shin", "p3": "Camille Beauchamp", "p4": "Babajide Fashanu",
        "o1": "Thistledown Pediatric Associates", "o2": "Alderney Health Plan"},
  minors=["p2"], cardholders=["p1"],
  distractors=["CPT 99214", "CPT 87880", "CPT 96127", "Mastercard", "No Surprises Act", "HSA"],
  ok=["Tue", "0600", "09:14:22", "Statement", "Billing", "Office", "Plan", "Questions", "This", "2", "8", "5",
      "Charges", "Copay", "Behavioral", "We", "Manager", "AUTO", "ID", "MD", "PAY", "RESPONSIBILITY", "Sick"],
  headers={"From": "[[Thistledown Pediatric Associates|o1:full]] Billing <[[billing@thistledownpeds.example|email]]>",
           "To": "[[Hye-jin Shin|p1:full]] <[[hjshin.dallas@mailbox.example|email]]>",
           "Subject": "Statement [[TPA-S-2291847|rec:statement number]] - balance due for [[Daniel|p2:first-name]]",
           "Date": "Tue, [[02 Dec 2025|date:email date]] 09:14:22 -0600"},
  body=r'''Dear [[Ms. Shin|p1:title-surname]],

This is your statement for services to your son, [[Daniel Shin|p2:full]] (date of birth [[05/19/2016|dob]], chart no. [[TPA-0088417|rec:medical record number]]).
You are listed as guarantor on account [[G-4417-220|rec:guarantor account number]].

VISIT SUMMARY
  [[10/21/2025|date:service date]]  Dr. [[Fashanu|p4:surname]]  Office visit (CPT 99214), [[ADHD medication follow-up|health:reason for visit]]             [[$215.00|money]]
              Behavioral screening (CPT 96127)                                              [[$18.00|money]]
  [[11/07/2025|date:service date]]  [[Babajide Fashanu|p4:full]], MD (NPI [[1730448291|govid:NPI]])  Sick visit, rapid strep (CPT 87880) -- [[strep throat, positive|health:test result]]   [[$164.00|money]]

  Charges                                   [[$397.00|money]]
  [[Alderney Health Plan|o2:full]] paid                 [[-$201.36|money:negative amount]]   (member ID [[AHP 884 207 119 02|rec:member ID with spaces]], group [[TX-55017|rec:group number]])
  Plan adjustment                           [[-$88.14|money:negative amount]]
  Copay paid at visit ([[11/07|date:month/day only]])                [[-$30.00|money:negative amount]]
  YOUR RESPONSIBILITY                       [[$77.50|money]]

The plan applied [[$47.50|money]] of this to Daniel's deductible; claim numbers [[25294-00417-A|rec:claim number]] and [[25311-00982-A|rec:claim number]].

AUTO-PAY
The Mastercard on file ending in [[1216|card:last four only]] (cardholder [[HYE JIN SHIN|p1:caps:name as it appears on the card, no hyphen]], expires [[11/27|exp]]) will be charged $77.50
on [[December 16, 2025|date:auto-pay date]]. Our last attempt to run the HSA card ending [[7752|card:last four only]] was declined on [[11/24|date:month/day only]], so we have
switched to the Mastercard. To use a different card or pay now:

  [[https://pay.thistledownpeds.example/s/TPA-S-2291847?t=9f3c1a7e|url:payment link containing statement number and token]]

We will never ask for your full card number or security code by email.

Questions? Call [[Camille|p3:first-name]] in billing at [[214-555-0136|phone]], option 2, Mon-Fri 8 to 5, or reply to this message.
If [[Daniel|p2:first-name]]'s coverage through [[Alderney|o2:short]] changes on [[Jan. 1|date:abbreviated, no year]], please send us the new card.

[[Camille Beauchamp|p3:full]]
Billing Manager, Thistledown Pediatric Associates
[[5900 Lovers Lane, Suite 204|addr:street with suite]], [[Dallas|place:city]], [[TX|place:state abbreviation]] [[75206-1104|zip:ZIP+4]]
fax [[214.555.0137|phone:fax, dotted]]

You have the right to a good-faith estimate under the No Surprises Act.
'''))

# ---------------------------------------------------------------- 259
DOCS.append(D(259, "docx", "long-term care admission packet", "health", "US", length="long",
  title="Long-term care admission packet - face sheet, history and inventory",
  ents={"p1": "Wilhelmina R. Vandenberg", "p2": "Lorraine Ochoa", "p3": "Gerrit Vandenberg", "p4": "Mirabel Ochoa",
        "p5": "Anselm Bjorklund", "p6": "Farida Haidari", "p7": "Cornelius Vandenberg", "p8": "Tamsin Hargreaves",
        "p9": "Dwight Pellerin", "p10": "Josefina Romero", "p11": "Pastor Elwood Kapoor", "p12": "Hazel Gupta", "p13": "Priscilla Wong",
        "p14": "Agnes Fitzgerald", "p15": "Raul Ochoa",
        "o1": "Yarrow Glen Health & Rehabilitation Center", "o2": "Underhill Regional Medical Center",
        "o3": "Sablewood Mutual Life Insurance Company", "o4": "Fourth Street Reformed Church",
        "o5": "Hendry & Sons Funeral Home", "o6": "Dubuque Bluffs Savings Bank",
        "o7": "Orchard Hill Long-Term Care Pharmacy", "o8": "Driftwood Audiology",
        "o9": "Sageville Consolidated School", "o10": "Tri-State Medical Transport"},
  distractors=["Form CMS-802", "MDS 3.0", "IPOST", "42 C.F.R. § 483.10", "PASRR", "Medicare Part D",
               "BIMS", "Iowa Code chapter 144D", "Section GG", "ICD-10", "Braden"],
  ok=["FACE", "SHEET", "ADMISSION", "PACKET", "Iowa", "POA", "VA", "English", "CNA", "RN", "LSW", "Part", "A",
      "B", "No", "Level", "II", "2", "3", "1", "6", "9", "10", "12", "15", "16", "18", "Resident's", "Section",
      "Responsible", "Code", "Diet", "Private", "Language", "Marital", "Widowed", "Religion", "Veteran",
      "Hearing", "Glasses", "Dentures", "Wheelchair", "Clothing", "Admissions", "Coordinator", "Director",
      "Nursing", "Social", "Worker", "Advance", "Durable", "Living", "Pharmacy", "Funeral", "Clergy", "Admitted",
      "Cardiology", "Audiology", "Supplement", "She", "Her", "Both", "Quantity", "Condition", "Phonak",
      "Medtronic", "Azure", "Bible", "Contact", "Relationship", "Physicians", "Mobility", "Weight", "Tuesdays",
      "Sundays", "Aid", "Attendance", "Model", "Medicaid's", "Witness", "2-person", "2-gram", "2.4", "132",
      "142/78", "64", "97.9", "Room", "Wing", "East", "Hospital", "100-day", "14", "94%", "Attending", "Cash",
      "Discharge", "Estimated", "Granddaughter", "ID", "Long", "MBI", "MR", "OK", "Pacemaker", "Security",
      "Serial", "Wedding", "2022", "31", "Alert", "Arrived", "Born", "Directions", "Family", "Incision", "Married", "Pain", "Rx"],
  header="[[Yarrow Glen Health & Rehabilitation Center|o1:full]] - Resident: [[VANDENBERG, WILHELMINA R.|p1:last-first:Last, First in ALL CAPS]] - MR# [[YG-104417|rec:medical record number]]",
  footer="Admission packet - contains protected health information - Room [[214-B|place:room number in a named facility]]",
  body=r'''# ADMISSION PACKET - FACE SHEET
| Section | Details |
| Resident | [[Wilhelmina R. Vandenberg|p1:full]] (goes by "[[Billie|p1:nickname]]") |
| Date of birth | [[August 2, 1928|dob]] (age [[97|age:bare age in a form field]]) |
| Admitted | [[11/03/2025|date:admission date]] at 14:20 from [[Underhill Regional Medical Center|o2:full]] |
| Room | 214-B, East Wing |
| SSN | [[362-21-8792|ssn]] |
| Medicare (MBI) | [[4TK8-YE2-MH61|govid:Medicare beneficiary identifier]], Part A and Part B effective [[08-01-1993|date:coverage effective date]] |
| Iowa Medicaid | State ID [[4418207C|govid:Medicaid state ID]] - application pending, filed [[10/29/2025|date]] |
| Supplement | [[Sablewood Mutual Life Insurance Company|o3:full]], policy [[SML-MS-7741902|rec:policy number]] |
| Long-term care policy | [[Sablewood|o3:short]] [[LTC-0092-55817|rec:policy number]], daily benefit [[$140|money]], 100-day elimination |
| Marital status | Widowed [[March 1998|date:month and year of spouse's death]]; husband [[Cornelius Vandenberg|p7:full]] |
| Religion | [[Christian Reformed|attr:religion]]; member of [[Fourth Street Reformed Church|o4:full]] |
| Language | English; [[Dutch was her first language|attr:language indicating national origin]] |
| Veteran status | [[Widow of a U.S. Army veteran of the Korean War|attr:veteran family status]]; VA Aid and Attendance claim [[C 24 417 882|rec:VA claim number with spaces]] |
| Code status | [[Do-not-resuscitate; IPOST on chart|health:code status]] signed [[10/31/2025|date]] |
## Responsible parties
| Contact | Relationship | Phone |
| [[Lorraine Ochoa|p2:full]] | Daughter; durable POA for finances and health care | [[563-555-0142|phone]] cell, [[(563) 555-0108|phone]] home |
| [[Gerrit Vandenberg|p3:full]] | Son, [[Tucson|place:city]], [[AZ|place:state abbreviation]] | [[520.555.0171|phone:dotted]] |
| [[Dr. Mirabel Ochoa|p4:full:full name with title]] | Granddaughter | [[mirabel.ochoa@mailbox.example|email]] |
[[Lorraine|p2:first-name]] lives at [[1182 Alpine Street|addr]], [[Dubuque|place:city]], [[IA|place:state abbreviation]] [[52001|zip]], email [[lorraine.ochoa52@mailbox.example|email]]. Statements go to her. [[Gerrit|p3:first-name]] asked for a copy of anything financial; Lorraine has not agreed, so do NOT send without her written OK. The granddaughter is [[the only physician in the family|indirect:unique role within the family]] and may call for clinical updates; [[Mrs. Ochoa|p2:title-surname]] signed the release for her on [[11/03|date:month/day only]].
## Physicians and pharmacy
- Attending: [[Dr. Anselm Bjorklund|p5:full:full name with title]], NPI [[1528830417|govid:NPI]], office [[563-555-0190|phone]], fax [[563-555-0191|phone:fax]]
- Cardiology: [[Farida Haidari, MD|p6:full:full name with credential]], NPI [[1902277184|govid:NPI]]. Pacemaker checks every 6 months; last [[9/16/25|date:two-digit year]].
- Audiology: [[Driftwood Audiology|o8:full]], [[563-555-0115|phone]]
- Pharmacy: [[Orchard Hill Long-Term Care Pharmacy|o7:full]], account [[OH-22-0871|rec:pharmacy account number]]; Medicare Part D ID [[PDP 7 0041 882 19|rec:drug plan member ID with spaces]]
## Hospital course and diagnoses
[[Mrs. Vandenberg|p1:title-surname]] was hospitalized [[10/22/2025|date:hospital admission date]] after a fall at home at [[640 Rhomberg Avenue|addr]] with a [[right intertrochanteric hip fracture|health:injury]], repaired on [[10/23|date:month/day only]]. Hospital MRN [[URMC 00-58-4417|rec:medical record number with separators]]. Discharge summary by the hospitalist lists (ICD-10 codes on the transfer form):
- [[Atrial fibrillation|health:diagnosis]], on [[apixaban 2.5 mg BID|health:medication and dose]]
- [[Heart failure with preserved ejection fraction|health:diagnosis]]; [[furosemide 20 mg daily|health:medication and dose]], [[potassium chloride 10 mEq|health:medication and dose]]
- [[Chronic kidney disease, stage 3b|health:diagnosis]]; last creatinine [[1.4 mg/dL|health:lab value]] on [[11/01|date:month/day only]]
- [[Moderate dementia, Alzheimer's type|health:diagnosis]]; BIMS 9 of 15 on admission; [[donepezil 10 mg QHS|health:medication and dose]]
- [[Macular degeneration, left eye worse|health:diagnosis]]
- [[Bilateral hearing loss|health:diagnosis]]
- [[Depression after her sister's death in 2023|health:mental health history]]; [[sertraline 25 mg|health:medication and dose]]
- [[Stage 2 pressure injury, sacrum|health:skin finding]], present on admission, 2.4 cm
Allergies: [[penicillin (hives)|health:allergy]]; [[sulfa|health:allergy]]; [[shellfish|health:food allergy]]. Diet: 2-gram sodium, mechanical soft. Weight 132 lb. Vitals on arrival 142/78, pulse 64, temp 97.9, sat 94% on room air. Braden score 15. Mobility: 2-person assist, non-weight-bearing right leg until ortho follow-up [[December 4|date:no year]]. PASRR Level II screening not required. MDS 3.0 admission assessment due by day 14; Section GG started by therapy.
## Medication reconciliation (pharmacy and transfer orders compared [[11/03/2025|date]])
| Medication | Directions | Rx / note |
| [[acetaminophen 650 mg|health:medication and dose]] | every 6 hours, scheduled | house stock |
| [[oxycodone 2.5 mg|health:medication and dose]] | every 6 hours as needed, 12 tablets sent | Rx [[7740182|rec:prescription number]] - count on arrival 12 |
| [[latanoprost, one drop left eye|health:medication and dose]] | nightly | Rx [[7740185|rec:prescription number]] |
| [[vitamin D3 2,000 units|health:medication and dose]] | daily | family supplied, sent home |
The hospital list also showed [[lorazepam 0.5 mg|health:medication and dose]] at bedtime. [[Dr. Bjorklund|p5:title-surname]] stopped it on admission because of the fall. [[QuantiFERON negative|health:test result]] on [[10/24|date:month/day only]]; influenza vaccine given [[10/02/2025|date]].
## Social history (from her daughter, [[November 5, 2025|date]])
Born in [[Pella|place:town]], [[IA|place:state abbreviation]], the youngest of seven; her parents [[came from Friesland in 1921|attr:family national origin]]. She taught fourth grade at [[Sageville Consolidated School|o9:full]] for 31 years and still corrects grammar. Married [[June 17, 1950|date:wedding date]]. Her husband farmed and later drove a county snowplow; she calls for "[[Cor|p7:nickname]]" in the late afternoon and it helps to say he is out checking the cattle. She quilted for the church sale every year and knows most of the hymnal by heart. She [[votes in every election and is a registered Republican|attr:political affiliation]]; [[Lorraine|p2:first-name]] will request the absentee ballot. She gave up driving in 2022; her Iowa ID card is [[417AB2206|govid:state ID card number]]. No tobacco, no alcohol.
Her roommate in [[214-A|place:room number in a named facility]], [[Mrs. Agnes Fitzgerald|p14:full:full name with title]], is [[her neighbor of forty years from Rhomberg Avenue|indirect:relationship to another resident]]; the family asked for this placement. [[Agnes|p14:first-name]]'s daughter has agreed.
## Nursing admission note
Arrived by stretcher with [[Tri-State Medical Transport|o10:full]], run [[TS-25-110377|rec:transport run number]]. Alert, oriented to self only, pleasant, repeating that she needs to get supper on. Pain 3 of 10 at the right hip. Incision clean and dry, staples intact, due out [[11/06|date:month/day only]]. High fall risk: bed in low position, alarm on, non-slip socks. Her flip phone ([[563-555-0184|phone]]) is kept at the nurses' station; the passcode is [[1928|cred:phone passcode that is also her birth year]]. Family was given the East Wing door keypad code, [[7731*|cred:door keypad code]]. After hours, if Lorraine cannot be reached, call her husband [[Raul Ochoa|p15:full]] at [[563-555-0133|phone]]. Long-term care claim opened with the insurer, no. [[LTC-CLM-250418|rec:claim number]]. Her daughter took the wedding photographs and the blue quilt home to sew name labels on and will bring them back Thursday. - [[Priscilla Wong|p13:full]], RN, [[11/03/2025|date]] 16:45
## Devices and equipment
| Item | Model | Serial |
| Pacemaker | Medtronic Azure | [[RNB418827H|dev:pacemaker serial number]], implanted [[May 2019|date:month and year]] |
| Hearing aid, left | Phonak | [[2241X0GK7|dev:hearing aid serial number]] |
| Hearing aid, right | Phonak | [[2241X0GK9|dev:hearing aid serial number]] |
| Wheelchair | 18 in. | facility tag [[YG-WC-0338|dev:asset tag]] |
Both hearing aids go in the locked med cart at night. [[Billie|p1:nickname]] will take them out and wrap them in tissue, which is how the last pair was lost.
## Financial
Private pay daily rate [[$312.00|money]] (semi-private) until Medicaid is approved; Lorraine paid the first month, [[$9,360.00|money]], by check [[#2291|rec:check number]] on [[11/03/2025|date]]. Estimated client participation once approved: [[$1,847|money]] a month from Social Security ([[$1,902.00|money]] gross) and the [[Sablewood|o3:short]] annuity ([[$211.40|money]]). Personal needs allowance [[$50|money]].
Resident trust fund: opened at [[Dubuque Bluffs Savings Bank|o6:full]], routing [[090419494|rtn]], pooled account [[0188-417-2206|acct:account number with dashes]], sub-account [[RTF-214B|acct:resident sub-account code]]; opening deposit [[$200.00|money]]. Her own checking there (ending [[4471|acct:last four only]]) stays open for the Medicaid look-back; balance about [[eighteen hundred dollars|money:amount in words]].
The farm ground in [[Jackson County|place:county]] was [[deeded to Gerrit in 2021|indirect:asset transfer to a named relative]] - flagged for Medicaid's five-year review.
## Advance directives and arrangements
Durable power of attorney for health care dated [[June 9, 2016|date]], prepared under Iowa Code chapter 144D; agent Lorraine Ochoa, alternate [[G. Vandenberg|p3:short:initial + surname]]. Living will on file. Funeral arrangements: [[Hendry & Sons Funeral Home|o5:full]], prepaid contract [[PN-0417-88|rec:prepaid funeral contract number]], [[563-555-0127|phone]]; burial next to [[Cornelius|p7:first-name]] at [[Linwood Cemetery|place:named cemetery]]. Clergy: [[Pastor Elwood Kapoor|p11:full:full name with title]], [[563-555-0153|phone]], visits Tuesdays; she wants to be taken to the chapel service Sundays and [[does not want care scheduled during it|attr:religious practice]].
## Valuables and personal inventory
| Item | Quantity | Condition / notes |
| Wedding band | 1 | [[gold band engraved "C.V. to W.R. 6-17-50"|indirect:distinctive personal property]] - stays on, cannot be removed |
| Glasses | 2 | bifocals, name taped inside |
| Dentures | upper | labeled [[W. VANDENBERG|p1:caps:name label, initial + surname]] |
| Bible | 1 | [[Dutch-language family Bible|indirect:distinctive personal property]] |
| Cash | - | [[$40.00|money]] placed in trust, receipt [[R-11884|rec:receipt number]] |
| Clothing | 16 pieces | marked [[WRV|p1:initials]] |
## Resident's rights and signatures
Resident rights under 42 C.F.R. § 483.10 were reviewed with the resident and her representative. Form CMS-802 roster updated.
Responsible party: [[Lorraine Ochoa|p2:full]], signed [[11/03/2025|date]]. Witness: [[Hazel Gupta|p12:full!:first name is a common word]], CNA.
Admissions Coordinator: [[Tamsin Hargreaves|p8:full]], [[thargreaves@yarrowglen.example|email]], [[563-555-0160 ext. 204|phone:with extension]]
Director of Nursing: [[Dwight Pellerin|p9:full]], RN (license [[IA-RN 118204|govid:nursing license number]])
Social Worker: [[Josefina Romero|p10:full]], LSW - notes that [[Mr. Vandenberg|p3:title-surname]] and his sister [[are not speaking|indirect:family conflict]]; calls about money go to [[Ms. Hargreaves|p8:title-surname]] or to [[Mr. Pellerin|p9:title-surname]], not the floor staff. [[J. Romero|p10:short:initial + surname]] will complete the social history with the family on [[Nov. 10|date:abbreviated, no year]].
[[Yarrow Glen|o1:short]], [[2750 Kerper Boulevard|addr]], Dubuque, IA [[52001-2210|zip:ZIP+4]] - main [[563-555-0100|phone]]'''))

# ---------------------------------------------------------------- 260
DOCS.append(D(260, "txt", "summer camp registration", "general", "US",
  title="Camp registration confirmation and camper records",
  ents={"p1": "Beatriz Zamora", "p2": "Colm Cavanaugh", "p3": "Mateo Zamora-Cavanaugh", "p4": "Ines Zamora-Cavanaugh",
        "p5": "Laleh Farouk", "p6": "Rosario Zamora", "p7": "Stephen Dvorak", "p8": "Greta Esposito",
        "o1": "Camp Kestrel Ridge", "o2": "Wickford Health Cooperative", "o3": "Poudre Canyon Pediatrics",
        "o4": "Kestrel Ridge Outdoor Education, Inc."},
  minors=["p3", "p4"], cardholders=["p1"],
  distractors=["American Express", "EpiPen Jr", "Form CR-7", "C.R.S. § 13-22-107", "American Camp Association",
               "Subaru Outback", "Honda Odyssey", "Session 2"],
  ok=["REGISTRATION", "CONFIRMATION", "Medications", "Allergies", "Cabin", "Grade", "2026", "2", "3", "4", "6",
      "11", "8", "1", "YM", "YS", "CID", "Amex", "Tuition", "Sibling", "Deposit", "Remaining", "Owls", "Marmots",
      "Registrar", "Swim", "Family", "Household", "Vehicle", "NOT", "Bring", "Sunday", "Mom", "Dad", "Custody",
      "Dietary", "Returning", "Confirmation", "Person", "Thank", "1:00-3:00", "Carries", "Dad's", "ID", "PORTAL",
      "Physical", "Registered", "Relationship", "Rx", "Subaru", "T", "Upload"],
  body=r'''[[CAMP KESTREL RIDGE|o1:caps:letterhead]] -- 2026 REGISTRATION CONFIRMATION
operated by [[Kestrel Ridge Outdoor Education, Inc.|o4:full]]  |  [[4410 Fish Creek Road|addr]], [[Estes Park|place:town]], CO [[80517|zip]]
Confirmation [[KR26-004417|rec:registration confirmation number]]        Family ID [[F-22871|rec:family account number]]        Registered [[02/14/2026|date:registration date]]

PARENT/GUARDIAN
  [[Beatriz Zamora|p1:full]]  (Mom)      cell [[970-555-0148|phone]]   work [[970-555-0102 x318|phone:with extension]]   [[bea.zamora@mailbox.example|email]]
  [[Colm Cavanaugh|p2:full]]  (Dad)      cell [[(303) 555-0175|phone]]                          [[colm.cavanaugh@mailbox.example|email]]
  Household: [[1418 Remington Street|addr]], [[Fort Collins|place:city]], [[CO|place:state abbreviation]] [[80524|zip]]. Dad's address: [[2200 Blake St., Unit 507|addr:street with unit]], [[Denver|place:city]] [[80205|zip]].
  Custody: [[parents share custody, week on / week off|indirect:family circumstances]]. Either parent may pick up. See pickup list.

CAMPER 1   [[Mateo Zamora-Cavanaugh|p3:full]]   born [[07/30/2014|dob]] (11)   Grade 6 in the fall   Cabin: Owls   T-shirt YM
  Session 2: [[June 21|date:no year]] - [[July 3, 2026|date]]   Swim level 4   Returning camper (camper no. [[C-10338|rec:camper number]])
  Allergies: [[peanut and tree nut - anaphylaxis|health:allergy of a child]]. Carries EpiPen Jr; second pen to the nurse at check-in.
  Medications: [[methylphenidate ER 27 mg every morning|health:medication and dose of a child]] ([[ADHD|health:diagnosis of a child]]); Rx no. [[RX 4417-22906|rec:prescription number]]. Parent note: "[[Teo|p3:nickname]] will say he
  already took it. He didn't."

CAMPER 2   [[Ines Zamora-Cavanaugh|p4:full]]   born [[11/02/2017|dob]] (8)   Grade 3 in the fall   Cabin: Marmots   T-shirt YS
  Session 2 (same dates)   Swim level 2   First year
  Allergies: none known. Dietary: vegetarian. [[Wears a hearing aid in her right ear|health:condition of a child]] (serial [[HA-R-7Q20418|dev:hearing aid serial number]]) - remove for
  swimming, case goes to the cabin counselor. [[Bedwetting, occasional|health:condition of a child]] - mom has packed supplies; please be discreet.
  [[Ines|p4:first-name]] and [[Mateo|p3:first-name]] may NOT share canteen money; [[$40|money]] each on account.

INSURANCE / PHYSICIAN
  [[Wickford Health Cooperative|o2:full]], subscriber Beatriz Zamora, member ID [[WHC-770418-2206|rec:member ID]], group [[88140|rec:group number, bare digits]]
  Dr. [[Laleh Farouk|p5:full]], [[Poudre Canyon Pediatrics|o3:full]], [[970.555.0119|phone:dotted]]. Physical on file dated [[1/22/26|date:two-digit year, no leading zero]] (Form CR-7).

PICKUP LIST (photo ID required)
  Person                       Relationship            Vehicle / plate
  Beatriz Zamora               mother                  blue Subaru Outback, CO [[CQT-418|veh:license plate]]
  Colm Cavanaugh               father                  Honda Odyssey, CO [[BRN-J72|veh:license plate]]
  [[Rosario Zamora|p6:full]]               grandmother             same Subaru; her cell [[970 555 0163|phone:spaces only]]
  [[Stephen Dvorak|p7:full]] ("[[Skip|p7:nickname:nickname that is a common word]]")       neighbor                gray pickup, plate [[481-XPL|veh:license plate]]
  NOT authorized: [[Colm's girlfriend|indirect:relationship to a named person]], per [[Ms. Zamora|p1:title-surname]]. Call mom first if anyone else shows up.

PAYMENT
  Tuition, Session 2 x 2 campers      [[$2,360.00|money]]     ([[$1,180|money]] each)
  Sibling discount                      [[-$118.00|money:negative amount]]
  Deposit paid [[2/14|date:month/day only]]                    [[-$400.00|money:negative amount]]     American Express ending [[73767|card:last five of an Amex]]
  Remaining balance                    [[$1,842.00|money]]     auto-charge on [[May 1, 2026|date:auto-charge date]]
  Card on file: Amex [[3417 944421 73767|card:15-digit card with spaces]], exp [[05/28|exp]], CID [[8823|cvv:4-digit security code]], name on card [[BEATRIZ M ZAMORA|p1:caps:name as embossed on card]],
  billing ZIP 80524. [[Mr. Cavanaugh|p2:title-surname]] reimburses half directly; do not split the charge.

PORTAL
  [[https://families.kestrelridge.example/login|url:family portal login]]     username [[bzamora84|cred:portal username]]     temporary password [[Kestrel-7Owls|cred:temporary password]] (change at first sign-in)
  Upload the signed waiver (C.R.S. § 13-22-107) and photo release by [[April 15|date:no year]].

Check-in is Sunday 1:00-3:00 at the lodge. Bring the medication in its original pharmacy bottle.
We are accredited by the American Camp Association.

[[Greta Esposito|p8:full]], Registrar   [[registrar@kestrelridge.example|email]]   [[970-555-0190|phone]]
Thank you, [[Bea|p1:nickname]]!
'''))
