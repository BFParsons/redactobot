from corpus2_src.core import D, dt, amt, num

DOCS = []
BATCH_COMMON = []

# ---------------------------------------------------------------- 231
DOCS.append(D(231, "html", "personal injury intake questionnaire", "legal", "US",
  title="New client intake questionnaire - motor vehicle collision with injured minor passenger",
  ents={"p1": "Delphine Marie Ruvalcaba", "p2": "Mateo Ruvalcaba", "p3": "Curtis Pettigrew",
        "p4": "Olusegun Bankole", "p5": "Lorna Tibbets", "p6": "Keisha Bellamy", "p7": "Farida Mirzaei",
        "p8": "Rex Standifer", "p9": "Yolanda Ruvalcaba",
        "o1": "Halloran & Mirzaei Injury Lawyers", "o2": "Wexford Mutual Auto Insurance Co.",
        "o3": "Pendragon Casualty Company", "o4": "Marrowbone Valley Children's Hospital",
        "o5": "Saltgrass Linen & Uniform Co.", "o6": "Tolland Street Elementary",
        "o7": "Scenic City Urgent Care", "o8": "Pettigrew Fence & Deck"},
  minors=["p2"],
  distractors=["Tenn. Code Ann. § 28-3-104", "Tenn. Code Ann. § 55-9-602", "Form HS-0114", "CPT 23500",
               "Honda Odyssey", "Ford F-150", "Chattanooga Police Department", "Glasgow Coma Scale"],
  ok=["Motor", "Vehicle", "New", "Intake", "Question", "Answer", "Full", "Goes", "Driver", "Cell", "Crash",
      "Location", "Police", "Citation", "Vehicles", "Our", "Other", "Plate", "Owner", "Damage", "Injured",
      "Persons", "Person", "Age", "Injuries", "Treated", "Insurance", "Carrier", "Policy", "Limits", "Adjuster",
      "Staff", "Fee", "Statute", "ER", "UM", "MedPay", "2019", "2021", "9", "4th", "15", "1", "2", "3", "4",
      "5", "6", "33", "TennCare", "Rule", "1.8", "OK", "Medical", "Lost", "Do", "Weather", "Dry", "Witness",
      "Photos", "Total", "1/3%", "25/50", "37", "ACV", "BPR", "Calendar", "Conflict", "HR", "ID", "Orthopaedic",
      "Responsible", "X"],
  body=r'''
# [[Halloran & Mirzaei Injury Lawyers|o1:full]] - New Client Intake (Motor Vehicle)
Intake no. [[HM-INT-26-0388|rec:intake number]]. Completed by [[Keisha Bellamy|p6:full]], paralegal, on [[06/17/2026|date:intake date]]. Conflict check cleared [[6/18|date:month/day only]]. Responsible attorney: [[Farida Mirzaei|p7:full]] (BPR No. [[031877|govid:state bar number]]).
## 1. Client
| Question | Answer |
| Full legal name | [[Delphine Marie Ruvalcaba|p1:full]] |
| Goes by | [[Del|p1:nickname]] |
| Date of birth | [[11/02/1988|dob]] |
| SSN (last 4 only) | [[5134|ssn:last four only]] |
| Driver license | TN [[104772968|govid!:driver's license number, digits only]] |
| Home address | [[2906 Dodson Avenue, Apt 4|addr:street with apartment]], [[Chattanooga|place:city]], [[TN|place:state abbreviation]] [[37406|zip]] |
| Cell | [[423-555-0171|phone]] (text OK) |
| Email | [[delruvalcaba88@inboxmail.example|email]] |
| Employer | [[Saltgrass Linen & Uniform Co.|o5:full]], route driver, [[$19.75/hr|money:hourly rate]] |
## 2. Crash
| Question | Answer |
| Date and time | [[Friday, June 5, 2026|date:date with weekday]], about 3:40 pm (school pickup) |
| Location | [[Brainerd Road|place!:road used as a location]] at [[Germantown Road|place!:road used as a location]], Chattanooga, [[Hamilton County|place:county]] |
| Police | Chattanooga Police Department, report no. [[26-058117|rec:police report number]], [[Ofc. R. Standifer|p8:short:rank, initial and surname]], badge [[1147|govid!:short badge number]] |
| Citation | Other driver cited, failure to yield, Tenn. Code Ann. § 55-9-602 (citation [[E4471902|rec:citation number]]) |
| Weather | Dry, clear |
| Witness | [[Yolanda Ruvalcaba|p9:full]] ([[client's sister-in-law|indirect:family relationship to client]]), following in her own car, [[(423) 555-0109|phone:parenthesized area code]] |
## 3. Vehicles
| | Our client | Other driver |
| Driver | [[Delphine Ruvalcaba|p1:short]] | [[Curtis Pettigrew|p3:full]], DOB [[3/9/71|dob:numeric, two-digit year]] |
| Year/make/model | 2019 Honda Odyssey | 2021 Ford F-150, lettered "[[Pettigrew Fence & Deck|o8:full]]" |
| Plate | TN [[7K4-2BN|veh:license plate]] | [[GA|place:state abbreviation]] [[CTP4418|veh!:license plate, no separator]] |
| VIN | [[5FNRL6H78KB041937|veh:VIN]] | [[1FTEW1EP4MFA62285|veh:VIN]] |
| Owner | client; lien with her credit union | [[Pettigrew|p3:surname]]'s business |
| Damage | Total loss per carrier, [[$17,850|money]] ACV offered | front end, drivable |
## 4. Injured Persons
| Person | Age / seat | Injuries | Treated at |
| [[Delphine|p1:first-name]] | 37, driver | [[cervical strain|health:injury]]; [[left wrist sprain|health:injury]]; headaches since | [[Scenic City Urgent Care|o7:full]] on [[6/6/26|date:numeric date with two-digit year]] |
| [[Mateo Ruvalcaba|p2:full]] | 9, rear passenger side | [[displaced fracture of the left clavicle|health:injury of a minor]]; [[mild concussion|health:injury of a minor]], Glasgow Coma Scale 15 on arrival | [[Marrowbone Valley Children's Hospital|o4:full]] ER, same day |
[[Mateo|p2:first-name]] was born [[August 30, 2016|dob:birth date of a minor]] and is in the 4th grade at [[Tolland Street Elementary|o6:full]]. He was belted in a booster. He [[has asthma|health:condition of a minor]] and uses [[albuterol as needed|health:medication]]. Orthopaedic follow-up is with [[Dr. Olusegun Bankole|p4:full:full name with title]] (NPI [[1730482296|govid:NPI]]); sling for 4 weeks, re-X-ray [[July 2|date:month and day only]]; closed treatment billed as CPT 23500. Hospital MRN [[MV-00648213|rec:medical record number]]. [[Dr. Bankole|p4:title-surname]] says no contact sports until cleared. Mateo missed the last 3 days of school and the whole swim season.
## 5. Insurance
| | Carrier | Policy / claim | Limits | Adjuster |
| Client | [[Wexford Mutual Auto Insurance Co.|o2:full]] | pol. [[WMA-TN-4418207-03|rec:policy number]]; claim [[26-TN-0077139|rec:claim number]] | 25/50 liability, UM 25/50, MedPay [[$5,000|money]] | not yet assigned |
| Other driver | [[Pendragon Casualty Company|o3:full]] | claim [[PCC-9920-481553|rec:claim number]] | unknown; commercial policy | [[Lorna Tibbets|p5:full]], [[615.555.0136|phone:dotted]], [[ltibbets@pendragoncasualty.example|email]] |
| Medical | TennCare (both) | member ID [[ZEC774190233|rec:health plan member ID]] (Delphine); [[ZEC774190241|rec:health plan member ID]] (Mateo) | | |
[[Ms. Tibbets|p5:title-surname]] called the client on [[June 9|date:month and day only]] asking for a recorded statement and offered [[$1,500|money]] "for the inconvenience." Client declined. Do NOT let [[Pendragon|o3:short]] contact her again; letter of representation goes out [[6/19/2026|date]].
## 6. Staff notes
- Lost wages: off work [[June 8|date:month and day only]] through [[June 19|date:month and day only]], 2 weeks at roughly [[$790|money]] gross per week. Get wage verification from [[Saltgrass|o5:short]] HR.
- Medical bills so far: ER [[$6,412.30|money]]; urgent care [[$385|money]]; ortho visit [[$298.00|money]]. Both are [[on TennCare|attr:public benefits status]], so expect a subrogation lien; send Form HS-0114 request.
- Client is [[a single parent|attr:family status]]; Mateo's father is not involved. Minor settlement will need court approval and a guardian ad litem if over the threshold.
- Statute: one year, Tenn. Code Ann. § 28-3-104, so calendar [[06/05/2027|date:limitations deadline]] for Delphine. Calendar it for Mateo too even though his claim is tolled.
- Fee: 33 1/3% explained and signed (Rule 1.8). Photos uploaded to [[https://files.halloranmirzaei.example/intake/HM-INT-26-0388|url:intake folder link containing the intake number]].
- [[KB|p6:initials]] to order the crash report and the body-cam footage.
'''))

# ---------------------------------------------------------------- 232
DOCS.append(D(232, "html", "paid preparer due diligence checklist", "accounting", "US", raw_html=True,
  title="Paid preparer due diligence checklist and notes (Form 8867) - EITC, CTC, HOH",
  ents={"p1": "Adaeze N. Nkemelu", "p2": "Chidera Nkemelu", "p3": "Kelechi Nkemelu", "p4": "Obinna Nkemelu",
        "p5": "Ines Quaresma-Lott", "p6": "Patience Eze",
        "o1": "Calumet Avenue Tax Service", "o2": "Mulberry Lane Child Development Center",
        "o3": "Ribault Bend Elementary", "o4": "Sabal Coast Community Credit Union",
        "o5": "Arlington Shores Pediatrics", "o6": "Dunes Edge Home Care, LLC"},
  minors=["p2", "p3"],
  distractors=["Form 8867", "Form 8862", "Form W-7", "Form 2441", "Schedule EIC", "Form W-2", "Pub. 4687",
               "IRC § 6695(g)", "Treas. Reg. § 1.6695-2", "Form 1040", "Notice CP09"],
  ok=["Paid", "Preparer", "Due", "Diligence", "Checklist", "Tax", "2025", "Head", "Household", "Taxpayer",
      "Filing", "Qualifying", "Children", "Relationship", "Months", "Proof", "Residency", "Knowledge",
      "Credits", "Claimed", "EITC", "CTC", "ACTC", "HOH", "IP", "Refund", "Direct", "Routing", "Savings",
      "Documents", "Retained", "Preparer's", "Q1", "Q2", "Q3", "Q4", "Q5", "12", "Child", "Dependent", "Care",
      "Credit", "Born", "Grade", "Income", "Married", "Jan", "No", "Explained", "Box", "Federal", "MFS", "1",
      "2", "2023", "4th", "AGI", "Aug", "August", "June", "Considered", "EA", "Interview", "Kindergarten",
      "Marital", "PTIN", "SSNs", "Self"],
  body=r'''<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>8867 worksheet</title>
<style>body{font:14px/1.4 Arial,sans-serif;margin:24px} .lbl{color:#555} table{border-collapse:collapse} td,th{border:1px solid #bbb;padding:3px 6px}</style>
</head>
<body>
<div class="letterhead"><b>[[Calumet Avenue Tax Service|o1:full]]</b><br>
[[5512 Merrill Road, Suite B|addr:street with suite]] &middot; [[Jacksonville|place:city]], [[FL|place:state abbreviation]] [[32277|zip]] &middot; [[(904) 555-0118|phone]]</div>
<h1>Paid Preparer Due Diligence Checklist &mdash; Tax Year 2025</h1>
<p><span class="lbl">Preparer:</span> [[Ines Quaresma-Lott|p5:full]], EA &nbsp;|&nbsp; <span class="lbl">PTIN:</span> [[P01844720|taxid:PTIN]] &nbsp;|&nbsp; <span class="lbl">Client file:</span> [[CA-25-0611|rec:client file number]] &nbsp;|&nbsp; <span class="lbl">Interview:</span> [[02/11/2026|date:interview date]]</p>
<h2>Taxpayer</h2>
<dl>
<dt>Name</dt><dd>[[Adaeze N. Nkemelu|p1:full]] (return will show [[NKEMELU, ADAEZE N|p1:caps:Last, First in ALL CAPS]])</dd>
<dt>SSN</dt><dd>[[353-98-2165|ssn]]</dd>
<dt>Date of birth</dt><dd>[[14 Oct 1991|dob:day month year, abbreviated]]</dd>
<dt>Address</dt><dd>[[7741 Lone Star Rd, Unit 208|addr:street with unit]], Jacksonville, FL [[32211-4406|zip:ZIP+4]]</dd>
<dt>Phone / email</dt><dd>[[904 555 0163|phone!:spaces only]] / [[adaeze.nkemelu@postbox.example|email]]</dd>
<dt>Filing status</dt><dd>Head of Household (see Q3 notes &mdash; spouse lived apart all of 2025)</dd>
<dt>IP PIN</dt><dd>[[407715|cred:IRS identity protection PIN]] (Notice CP09 not relevant; PIN letter seen and copied)</dd>
</dl>
<h2>Qualifying Children</h2>
<table>
<tr><th>Name</th><th>SSN</th><th>Born</th><th>Relationship</th><th>Months lived with taxpayer</th><th>Grade / care</th></tr>
<tr><td>[[Chidera Nkemelu|p2:full]]</td><td>[[797-11-1006|ssn]]</td><td>[[05/22/2016|dob:birth date of a minor]]</td><td>daughter</td><td>12</td><td>4th grade, [[Ribault Bend Elementary|o3:full]]</td></tr>
<tr><td>[[Kelechi Nkemelu|p3:full]]</td><td>[[763 96 8188|ssn!:SSN with spaces]]</td><td>[[2019-09-03|dob:ISO date of a minor]]</td><td>son</td><td>12</td><td>Kindergarten since [[Aug. 11|date:abbreviated month, no year]]; before that [[Mulberry Lane Child Development Center|o2:full]]</td></tr>
</table>
<h2>Knowledge questions and answers</h2>
<p><b>Q1. Income.</b> One Form W-2 from [[Dunes Edge Home Care, LLC|o6:full]] (EIN [[59-3317746|taxid:EIN]]): Box 1 wages [[$27,914.62|money]], federal withholding [[$1,106.00|money]]. No self-employment. She confirmed she did not braid hair for pay in 2025 (she did in 2023; that return was Self-prepared).</p>
<p><b>Q2. Residency of children.</b> Both children lived with her all 12 months at the [[Lone Star Rd|addr!:street name only]] apartment. Proof retained: lease naming all three ([[Jan 1|date:abbreviated month and day]] &ndash; [[Dec 31, 2025|date]]); [[Ribault Bend|o3:short]] enrollment letter dated [[1/29/2026|date:letter date]] signed by the registrar; [[Arlington Shores Pediatrics|o5:full]] immunization record for [[Kelechi|p3:first-name]] showing the same address.</p>
<p><b>Q3. Marital status / HOH.</b> Married to [[Obinna Nkemelu|p4:full]]; he moved out [[November 2024|date:month and year only]] and lives with a cousin in [[Orange Park|place!:city name made of common words]]. No joint return. [[Obinna|p4:first-name]] [[has no SSN and is not authorized to work|attr:immigration status of a relative]]; his ITIN is [[9XX-78-4416|taxid:masked ITIN]] (expired, Form W-7 renewal not filed). He paid nothing toward rent. She paid rent of [[$1,385/mo|money:monthly rent]] and all utilities; I added it up and she paid more than half the cost of the home. Considered-unmarried test met, so HOH not MFS.</p>
<p><b>Q4. Could anyone else claim the children?</b> Her mother, [[Patience Eze|p6:full]], stayed with them June&ndash;August on a visitor visa and is not a taxpayer. [[Mrs. Eze|p6:title-surname]] is not claiming anyone. Obinna will not file.</p>
<p><b>Q5. Prior disallowance.</b> None. Form 8862 not required.</p>
<h2>Credits Claimed</h2>
<table>
<tr><th>Credit</th><th>Amount</th><th>Notes</th></tr>
<tr><td>EITC (Schedule EIC, 2 children)</td><td>[[$6,418|money]]</td><td>earned income and AGI both $27,914.62 rounded</td></tr>
<tr><td>CTC / ACTC</td><td>[[$4,000.00|money]]</td><td>both children have SSNs valid for work</td></tr>
<tr><td>Child and Dependent Care Credit (Form 2441)</td><td>[[$600|money]]</td><td>paid [[Mulberry Lane|o2:short]] [[$3,150|money]] Jan&ndash;Aug for Kelechi; provider EIN [[47-2095513|taxid:EIN]]</td></tr>
</table>
<h2>Refund</h2>
<p>Federal refund [[$10,912|money]]. Direct deposit to [[Sabal Coast Community Credit Union|o4:full]], Savings, Routing [[063855302|rtn]], account [[70044182265|acct]]. Fee of [[$240.00|money]] paid by debit card at pickup; no refund transfer product.</p>
<h2>Preparer's notes</h2>
<p>Client [[receives SNAP|attr:public benefits status]] and asked whether the refund counts against it; told her to ask her caseworker and gave her Pub. 4687 only as my own reference list. [[Chidera|p2:first-name]] [[has an IEP for a speech delay|health:condition of a minor]] &mdash; not relevant to any credit but [[Ms. Nkemelu|p1:title-surname]] mentioned it when explaining the school letter. Explained the penalty rules to her in plain words (IRC &sect; 6695(g); Treas. Reg. &sect; 1.6695-2). Documents Retained: copies in the portal folder <span>[[https://portal.calumettax.example/clients/CA-25-0611/8867|url:client portal link containing file number]]</span>. Form 8867 completed and attached to Form 1040. &mdash; [[IQL|p5:initials]], [[2/12/26|date:numeric date with two-digit year]]</p>
</body>
</html>
'''))

# ---------------------------------------------------------------- 233
DOCS.append(D(233, "txt", "home health nursing visit note", "health", "US",
  title="Skilled nursing home visit note",
  ents={"p1": "Eleanor J. Ashworth", "p2": "Rosalie Koenig", "p3": "Marisol Ospina", "p4": "Thandiwe Mwangi",
        "p5": "Lazlo Vukovic", "p6": "Gus Koenig",
        "o1": "Verity Bluffs Home Nursing", "o2": "Key City Heart Clinic", "o3": "Asbury Road Pharmacy",
        "o4": "Tri-State Oxygen & Medical Supply", "o5": "St. Columbkille Parish"},
  distractors=["OASIS-E", "Braden Scale", "Morse Fall Scale", "42 CFR § 484.60", "ICD-10 I50.32", "Medicare Part A",
               "Form CMS-485", "Lasix"],
  ok=["SN", "VISIT", "NOTE", "Visit", "Pt", "Episode", "Dx", "Vitals", "BP", "HR", "RR", "SpO2", "LPM", "Temp",
      "Wt", "Meds", "Devices", "Plan", "Caregiver", "BID", "RN", "MD", "DNR", "POLST", "A&Ox3", "Lungs", "Skin",
      "Pain", "Access", "Teaching", "Next", "RA", "NC", "L", "R", "Edema", "Instructed", "Daughter", "Called",
      "Entered", "Fingerstick", "Denies", "Reports", "Model", "Serial", "Front", "Key", "She", "Order",
      "Verbal", "Goal", "2", "3", "5", "6", "16", "18", "55", "2+", "1+", "3/10", "97.9", "x2", "88%", "95%",
      "2-3", "Electronically", "214", "2x/wk", "6.4", "8-12", "9", "Age", "BMP", "Chart", "EverFlo", "Filter",
      "Found", "Glucometer", "ID", "Oxygen", "Pacemaker", "Pendant", "Read", "Refill", "Remote", "Rx",
      "Sundays", "Wallet"],
  body=r'''
[[VERITY BLUFFS HOME NURSING|o1:caps]] -- SN VISIT NOTE
[[Verity Bluffs Home Nursing|o1:full]], [[3180 Asbury Rd|addr]], [[Dubuque|place:city]], [[IA|place:state abbreviation]] [[52001|zip]]   ph [[563-555-0127|phone]]   after hours [[563-555-0190|phone]]

Pt:        [[ASHWORTH, ELEANOR J|p1:caps:Last, First in ALL CAPS]]  ("[[Nell|p1:nickname]]")       DOB [[04/19/1933|dob]]   Age [[93|age:bare age]]
Chart #:   [[VB-204417|rec:home health chart number]]         Medicare no. [[4NK7-WT2-HD86|govid:Medicare beneficiary identifier]]
Address:   [[1466 Loras Blvd|addr]], Dubuque -- side door, 2 steps, no rail
Episode:   cert period [[5/28/26|date:numeric date with two-digit year]] - [[7/26/26|date:numeric date with two-digit year]] (Form CMS-485 signed by MD)
Visit:     [[Tues 6/23/26|date:weekday and numeric date]], in 10:05, out 10:55.  RN: [[Thandiwe Mwangi, RN|p4:full:full name with credential]] (lic. [[IA 148830|govid:nursing license number]])
MD:        [[Dr. Lazlo Vukovic|p5:full:full name with title]], [[Key City Heart Clinic|o2:full]], [[563.555.0144|phone:dotted]], fax [[563.555.0145|phone:fax, dotted]]

Access: Front door stays locked. Key in lockbox on the side railing, code [[1933|cred!:lockbox code that is also her birth year]] (daughter set it; told her
to change it). Entered with aide present.

Dx: [[chronic diastolic heart failure|health:diagnosis]] (ICD-10 I50.32), [[atrial fibrillation|health:diagnosis]], [[type 2 diabetes|health:diagnosis]],
[[stage 3 chronic kidney disease|health:diagnosis]], [[macular degeneration|health:diagnosis]], [[hard of hearing|health:condition]] (L worse than R).

Vitals: BP [[148/72|health:blood pressure reading]] sitting, HR [[78 irregular|health:heart rate finding]], RR 18, Temp 97.9, SpO2 [[92% on 2L|health:oxygen saturation]] NC (88% on RA
after walking to the bathroom, back to 95% in 3 minutes). Wt [[131.4 lb|health:weight]], up [[3.2 lb|health:weight change]] since Friday.
Fingerstick [[212 mg/dL|health:blood glucose reading]] at 10:20 (ate toast and jam at 9).

Reports: sleeping in the recliner x2 nights, "can't get my breath flat." Denies chest pain. Pain 3/10 both knees.
Lungs: crackles both bases. Edema 2+ both ankles (was 1+ on [[6/19|date:month/day only]]). A&Ox3, a little forgetful about
the day of the week. Skin intact; heels soft. Braden Scale 16. Morse Fall Scale 55 (high).

Meds reviewed against bottles. [[Furosemide 40 mg|health:medication and dose]] every morning (she calls it Lasix); [[apixaban 2.5 mg|health:medication and dose]] BID;
[[metoprolol succinate 25 mg|health:medication and dose]] daily; [[insulin glargine 14 units|health:medication and dose]] at bedtime. Found she skipped the water pill
Sat and Sun because of the church picnic at [[St. Columbkille Parish|o5:full]] ("didn't want to be running to the
bathroom"). She is [[a lifelong Catholic|attr:religion]] and wants Father to bring communion on weeks she can't go.
Refill due on apixaban: Rx [[6620417-02|rec:prescription number]] at [[Asbury Road Pharmacy|o3:full]], [[(563) 555-0102|phone]].

Devices:
  Oxygen concentrator, Model EverFlo-type 5 LPM, Serial [[HC5-2291847|dev:oxygen concentrator serial number]], from [[Tri-State Oxygen & Medical Supply|o4:full]]
    ([[1-800-555-0133|phone:toll-free]]). Filter dusty, cleaned. Hours meter 6 214.
  Pacemaker (dual chamber, implanted [[March 2019|date:month and year only]]): SN: [[PJN508812H|dev:pacemaker serial number]]. Wallet card checked. Remote
    monitor at bedside, transmitter ID [[TX-88014-6627|dev:remote monitor transmitter ID]], green light on.
  Glucometer: serial [[GM07K31190|dev!:glucometer serial number]], control solution not expired.
  Pendant alarm worn; did not test today.

Caregiver: Daughter [[Rosalie Koenig|p2:full]] lives next door at [[1470 Loras|addr!:house number and street name only]], cell [[563-555-0168|phone]], is health care
agent; POLST on fridge, DNR. [[Rosalie|p2:first-name]] works nights at the casino so mornings are covered by the aide,
[[Marisol Ospina|p3:full]], Mon/Wed/Fri 8-12 (private pay, [[$24/hr|money:hourly rate]]). Son-in-law [[Gus|p6:nickname!:short first name]] ([[Mr. Koenig|p6:title-surname]]) does the
pill box on Sundays -- he is [[the retired fire chief|indirect:distinctive former occupation]], everybody on the street knows him.
[[Marisol|p3:first-name]] says [[Mrs. Ashworth|p1:title-surname]] nearly fell Monday reaching for the phone.

Teaching: daily weights, call if up 2-3 lb overnight or 5 lb in a week; low-salt reminders (the picnic ham);
do not skip the water pill. Instructed Marisol to log weights on the fridge sheet.

Called MD office 10:40, spoke to nurse. Verbal Order per [[Dr. Vukovic|p5:title-surname]]: furosemide [[40 mg twice daily x 3 days|health:medication change]],
then back to daily; BMP [[Friday 6/26|date:weekday and month/day]]; office visit [[July 1|date:month and day only]] 2:15 pm. Read back and confirmed.
Rosalie texted re: new order and the ride on [[the 1st|date:day of month only]].

Plan: SN 2x/wk x 3 wks then reassess (42 CFR § 484.60 care plan updated; OASIS-E not due). Goal: no
hospitalization this episode (Medicare Part A). Next visit [[Fri 6/26|date:abbreviated weekday and month/day]], lab draw.

Electronically signed: [[T. Mwangi|p4:short:initial and surname]] RN  [[06/23/2026|date:signature date]] 11:32   visit ID [[V-0623-11873|rec:visit ID]]   mileage 6.4 mi
'''))

# ---------------------------------------------------------------- 234
DOCS.append(D(234, "eml", "expert witness retention email", "legal", "US", enc="qp",
  title="Email retaining an orthopaedic expert witness",
  ents={"p1": "Gwendolyn Faulk", "p2": "Anselm Imanishi", "p3": "Dragan Stojanovic", "p4": "Keanu Kealoha",
        "p5": "Meredith Oyelade", "p6": "Vesna Stojanovic",
        "o1": "Brassfield Faulk LLP", "o2": "Imanishi Orthopaedic Consulting, PLLC",
        "o3": "Pendleton Regional Logistics, Inc.", "o4": "Osprey Delta Bank", "o5": "Sutter Fork Spine Institute",
        "o6": "Hartsell Crane LLP"},
  distractors=["Fed. R. Civ. P. 26(a)(2)(B)", "W-9", "Rule 35", "Cal. Evid. Code § 720", "MRI"],
  ok=["Tue", "0700", "Retention", "Superior", "California", "Scope", "Rates", "Retainer", "Records", "Key",
      "Bates", "1", "2", "3", "4", "5", "6", "Thanks", "Password", "Your", "Expert", "ABA", "Acct",
      "Beneficiary", "Memo", "Trial", "Direct", "Partner", "Depo", "I'll", "2,100", "2024", "Defense", "Exam",
      "RE", "SBN", "Short", "Travel"],
  headers={"From": "[[Gwendolyn Faulk|p1:full]] <[[gfaulk@brassfieldfaulk.example|email]]>",
           "To": "\"[[Imanishi, Anselm|p2:last-first]]\" <[[dr.imanishi@imanishiortho.example|email]]>",
           "Cc": "[[Keanu Kealoha|p4:full]] <[[kkealoha@brassfieldfaulk.example|email]]>",
           "Subject": "RE: Retention - [[Stojanovic|p3:surname]] v. [[Pendleton Regional Logistics|o3:short]] (No. [[34-2025-00381764|rec:state court case number]]) - PRIVILEGED",
           "Date": "Tue, [[07 Jul 2026|date:email date]] 16:42:10 -0700"},
  body=r'''
[[Anselm|p2:first-name]],

Thank you for the call this morning. This confirms that [[Brassfield Faulk LLP|o1:full]] is retaining you, through
[[Imanishi Orthopaedic Consulting, PLLC|o2:full]], as a testifying expert for the plaintiff in
[[STOJANOVIC v. PENDLETON REGIONAL LOGISTICS, INC.|o3:caps:case caption in ALL CAPS]], Superior Court of California, [[County of Sacramento|place:county]],
Case No. 34-2025-00381764. Please treat everything below as attorney work product.

1. Scope. Review the records, examine [[Mr. Stojanovic|p3:title-surname]] once, and give opinions on causation, the
reasonableness of past treatment, and future care. Short version of the facts: on [[October 3, 2024|date:incident date]] a
[[Pendleton|o3:short]] tractor backed into the loading dock where our client, [[Dragan Stojanovic|p3:full]] (DOB [[2/27/1979|dob:numeric without leading zero]]), was
working. He had [[an L4-L5 disc herniation with left-sided radiculopathy|health:diagnosis]], failed conservative care, and
underwent [[a microdiscectomy|health:surgical procedure]] on [[March 11, 2025|date:surgery date]] at [[Sutter Fork Spine Institute|o5:full]]. He still has
[[foot drop on the left|health:symptom]] and takes [[gabapentin 600 mg three times a day|health:medication and dose]]. The defense will make a great
deal of [[a 2017 workers' comp claim for low back strain|health:prior medical claim]] and of the fact that he [[was treated for alcohol dependence in 2021|health:substance use treatment]].
You should know both before you see their Rule 35 report.

2. Rates. Per your fee schedule: [[$650/hour|money:hourly rate]] for review and conferences, [[$900 per hour|money:hourly rate]] for deposition and
trial testimony (four-hour minimum), exam flat fee [[$2,400|money]]. Travel at half rate.

3. Retainer. We will wire [[$7,500.00|money]] ([[seventy-five hundred dollars|money:amount in words]]) this week against your first invoice. Per your W-9
(EIN [[84-3920175|taxid:EIN]]) and the wire sheet [[Keanu|p4:first-name]] has:
      Beneficiary:  Imanishi Orthopaedic Consulting, PLLC
      Bank:         [[Osprey Delta Bank|o4:full]], [[Elk Grove|place:city]] branch
      ABA:          [[116959977|rtn]]
      Acct:         [[3300 7714 0926|acct:account number with spaces]]
      Memo:         [[BF-24-1193|rec:firm matter number]] / Stojanovic
Keanu will call your office manager at the number we have on file, [[916-555-0156|phone]], to read the account back
before anything is sent. We do not change wire details by email, ever.

4. Records. About 2,100 pages, Bates [[STOJ-000001|rec:Bates number]] through [[STOJ-002114|rec:Bates number]], plus the MRI discs. They are on our
share: [[https://share.brassfieldfaulk.example/x/stoj-expert-7Qm4T9|url:file share link with token]]
Password (I'll also text it to you): [[Tulip!Harbor-2291|cred:file share password]]
The link expires [[July 21|date:month and day only]]. Please do not forward it to staff; if your assistant [[Meredith Oyelade|p5:full]] needs
access, Keanu will set her up with her own login ([[moyelade-ext|cred:username]]).

5. Key dates. Expert disclosure [[9/14/26|date:numeric date with two-digit year]]. Your written report, if we decide we want one (think Fed. R.
Civ. P. 26(a)(2)(B) format even though we are in state court), by [[August 28th|date:month and ordinal day]]. Depo window the weeks of
[[Oct. 5|date:abbreviated month, no year]] and [[Oct. 12|date:abbreviated month, no year]]. Trial is set for [[January 11, 2027|date:trial date]]. Defense counsel is [[Hartsell Crane LLP|o6:full]].

6. Exam. Mr. Stojanovic lives in [[Rancho Cordova|place:city]] and does not drive since the surgery; his wife [[Vesna|p6:first-name]] will
bring him. He is more comfortable in [[Serbian|attr:language indicating national origin]]; tell us if you want an interpreter. He can do any
weekday after [[the 20th|date:day of month only]]. Her cell is [[(916) 555-0129|phone]].

Please countersign the attached engagement letter and send back the W-9 if the one we have (dated 2024) is stale.
You will be qualified under Cal. Evid. Code § 720 without any trouble.

Thanks,
[[Gwen|p1:nickname]]

[[Gwendolyn R. Faulk|p1:full:full name with middle initial]] | Partner | SBN [[218846|govid:state bar number]]
Brassfield Faulk LLP | [[980 9th Street, Suite 1450|addr:street with suite]], [[Sacramento|place:city]], [[CA|place:state abbreviation]] [[95814|zip]]
Direct [[916.555.0184|phone:dotted]] | [[gfaulk@brassfieldfaulk.example|email]]
'''))

# ---------------------------------------------------------------- 235
DOCS.append(D(235, "rtf", "wage garnishment processing memo", "accounting", "US",
  title="Payroll memo - processing an income withholding order and a creditor garnishment",
  ents={"p1": "Terrence D. Holloway", "p2": "Jaylen Holloway", "p3": "Brianna Sepulveda", "p4": "Noor Hadjiev",
        "p5": "Wendell Cray",
        "o1": "Thistledown Bakery Supply, Inc.", "o2": "Candlewood Credit Recovery LLC",
        "o3": "Scioto Commons Bank", "o4": "Hadjiev & Marlowe Payroll Accountants",
        "o5": "Olentangy Motor Credit"},
  minors=["p2"],
  distractors=["15 U.S.C. § 1673", "Form OMB 0970-0154", "Ohio Rev. Code § 3121.03", "Form W-4", "CCPA",
               "Ohio Child Support Payment Central", "Chapter 13", "Court of Common Pleas"],
  ok=["MEMO", "Prepared", "Employee", "Orders", "Income", "Withholding", "IWO", "Creditor", "Ohio", "Juvenile",
      "Domestic", "Relations", "Municipal", "Priority", "Gross", "Disposable", "Remittance", "Open", "Support",
      "Child", "Processing", "HR", "EFT", "Step", "1", "2", "3", "4", "55%", "25%", "7", "Do", "Federal",
      "FICA", "Current", "Amount", "Remaining", "Start", "Trustee", "Hold", "5", "80", "Judgment", "Obligee",
      "SETS", "TO"],
  body=r'''
# MEMO TO PAYROLL FILE
**Client:** [[Thistledown Bakery Supply, Inc.|o1:full]] (EIN [[31-1940662|taxid:EIN]])
**Prepared by:** [[Noor Hadjiev|p4:full]], [[Hadjiev & Marlowe Payroll Accountants|o4:full]], [[Columbus|place!:city that is also a surname and first name]], Ohio
**Date:** [[May 12, 2026|date:memo date]]
**Re:** Employee [[Terrence D. Holloway|p1:full]], emp. no. [[00417|rec:employee ID with leading zeros]] - two withholding orders received the same week
## 1. Employee
[[Holloway, Terrence D.|p1:last-first]]; SSN [[237-27-5134|ssn]]; DOB [[9/30/1990|dob]]; warehouse lead, hired [[08/14/2019|date:hire date]]; paid biweekly, [[$26.40|money:hourly rate without unit]] an hour. Home address on the orders is [[618 Sullivant Avenue|addr]], Columbus, [[OH|place:state abbreviation]] [[43223|zip]], which does not match our file ([[2240 Gantz Rd Lot 31|addr:street with lot number]], [[Grove City|place:city]]). [[Wendell Cray|p5:full]] in HR will ask him which is right; do not send anything to either address until then.
## 2. Orders received
- **Income Withholding for Support (IWO)**, Form OMB 0970-0154, issued [[April 29, 2026|date:order date]] by the [[Franklin County|place:county]] Court of Common Pleas, Domestic Relations and Juvenile, case no. [[24 JU 03 2291|rec:juvenile case number with spaces]], SETS case [[7049336118|rec!:child support case number, digits only]]. Obligee: [[Brianna Sepulveda|p3:full]]. Child: [[Jaylen Holloway|p2:full]], born [[03/17/2019|dob:birth date of a minor]]. Current child support [[$612.00|money]] per month; cash medical support [[$41.50|money]] per month; arrears payment [[$122.40|money]] per month on [[past-due support|attr:child-support arrears]] of [[$8,930.17|money]]. Total [[$775.90|money]] per month, which the order converts to [[$358.11|money]] biweekly.
- **Creditor garnishment**, Franklin County Municipal Court, case [[2026 CVF 011872|rec:civil case number]], served [[5/1/2026|date:service date]]. Judgment creditor [[Candlewood Credit Recovery LLC|o2:full]], assignee of [[Olentangy Motor Credit|o5:full]] (deficiency on [[a repossessed 2018 Chevrolet Malibu|attr:repossession]]). Judgment balance [[$6,204.88|money]] plus costs.
## 3. Priority and calculation (per pay period)
Child support comes first (Ohio Rev. Code § 3121.03). The CCPA limit for support is 55% of disposable earnings here because he supports no second family and [[is more than 12 weeks in arrears|attr:child-support arrears]]; see 15 U.S.C. § 1673.
| Step | Amount |
| Gross (80 hrs) | [[$2,112.00|money]] |
| Federal, FICA, state, city tax | [[(431.87)|money:parenthesized negative, no currency sign]] |
| Disposable earnings | [[$1,680.13|money]] |
| Support withheld (IWO) | [[358.11|money!:no currency sign]] |
| Processing fee kept by employer | [[$2.00|money]] |
| 25% cap for creditor garnishment | [[$420.03|money]] |
| Already taken by support | 358.11 |
| Remaining for [[Candlewood|o2:short]] | [[$61.92|money]] |
So each check: 358.11 to support, $61.92 to the creditor, until the judgment is paid or we are told to stop. Start with the pay date of [[May 22|date:month and day only]].
## 4. Remittance
Support goes by EFT to Ohio Child Support Payment Central within 7 days of each pay date, using the SETS case number and the employee's SSN. The EFT is drawn on the payroll account at [[Scioto Commons Bank|o3:full]], routing [[080391137|rtn]], account ending [[-8816|acct:last four with leading dash]]. The creditor's share goes by check to the clerk, memo "2026 CVF 011872 / [[T. Holloway|p1:short:initial and surname]]".
## 5. Open items
- [[Mr. Holloway|p1:title-surname]] told [[Wendell|p5:first-name]] he [[filed Chapter 13 in March|attr:bankruptcy]] (he gave case no. [[2:26-bk-51077|rec:bankruptcy case number]]). If that is right, the creditor garnishment must stop, but the support order does not. Hold the $61.92 in the liability account until we see the notice from the Trustee. Do not discuss the bankruptcy with his supervisor.
- He also asked that [[Jaylen|p2:first-name]] be added to his medical plan; that is an HR matter, not payroll, but the IWO has a medical support box checked. [[Ms. Sepulveda|p3:title-surname]]'s attorney called HR twice; refer any calls to me at [[614-555-0173|phone]] or [[noor@hadjievmarlowe.example|email]].
- New Form W-4 not needed.
[[NH|p4:initials]]
'''))

# ---------------------------------------------------------------- 236
DOCS.append(D(236, "txt", "real estate closing statement", "legal", "US",
  title="Residential purchase closing statement and disbursement notes",
  ents={"p1": "Soren A. Lindholm", "p2": "Mei-Ling Lindholm", "p3": "Bartholomew Trzebiatowski",
        "p4": "Joanna Ekwueme", "p5": "Silas Whitfield-Boyce", "p6": "Darnell Uzun",
        "o1": "Anchorpoint Title & Settlement, LLC", "o2": "Longleaf Home Lending, Inc.",
        "o3": "Neuse Basin Bank & Trust", "o4": "Oakwood Crest Homeowners Association, Inc.",
        "o5": "Carolina Wren Home Inspections", "o6": "Ekwueme Law Office, PLLC", "o7": "Dogwood Realty Partners"},
  cardholders=["p2"],
  distractors=["Form 1099-S", "ALTA Settlement Statement", "N.C. Gen. Stat. § 47H", "Closing Disclosure",
               "TRID", "Form W-9", "4506-C", "Fannie Mae"],
  ok=["BUYER", "SELLER", "BUYERS", "PROPERTY", "LENDER", "SETTLEMENT", "STATEMENT", "Seller", "Buyers",
      "Borrower", "Sale", "Price", "Earnest", "Money", "Loan", "Origination", "Appraisal", "County", "Taxes",
      "HOA", "Dues", "Owner's", "Lender's", "Title", "Recording", "Commission", "Payoff", "Proceeds",
      "Settlement", "Closing", "Disbursement", "Notary", "Public", "Deed", "Trust", "PIN", "REID", "Inspection",
      "Home", "Warranty", "Survey", "Excise", "Revenue", "Stamps", "Listing", "Selling", "Existing", "Mortgage",
      "DEBIT", "CREDIT", "TOTALS", "POC", "My", "Expires", "ABA", "Further", "Beneficiary", "Attorney", "1",
      "2", "3", "4", "12", "6.375%", "2.5%", "365", "183", "0.5", "Insurance", "Premium", "Homeowner's",
      "Prepaid", "Interest", "Escrow", "Initial", "Reissue", "Rate", "Items", "Due", "Paid", "Outside", "Visa",
      "30-year", "5", "AT", "TO", "April", "Bar", "CASH", "CLOSING", "DISBURSEMENT", "PROCEEDS", "Combined",
      "Fed", "Matches", "OK", "POA"],
  body=r'''
                 [[ANCHORPOINT TITLE & SETTLEMENT, LLC|o1:caps]]
        [[4208 Six Forks Road, Suite 910|addr:street with suite]], [[Raleigh|place:city]], [[NC|place:state abbreviation]] [[27609|zip]]
              tel [[919-555-0115|phone]]    wires: call to verify, always

                SETTLEMENT STATEMENT (ALTA Settlement Statement - Combined)

File No.:        [[APT-26-04417|rec:title file number]]                 Settlement date:   [[June 30, 2026|date:closing date]]
Settlement agent: [[Joanna Ekwueme|p4:full]], [[Ekwueme Law Office, PLLC|o6:full]]     Disbursement date: [[07/01/2026|date:disbursement date]]
                 (NC Bar No. [[40217|govid:state bar number]])

BUYERS:    [[Soren A. Lindholm|p1:full]] and [[Mei-Ling Lindholm|p2:full]], husband and wife
           currently of [[311 Hillsborough Street, Apt 6C|addr:street with apartment]], Raleigh, NC [[27603|zip]]
SELLER:    [[Bartholomew Trzebiatowski|p3:full]], unmarried (widower), forwarding address
           [[c/o Sunrise Villa, 88 Kildaire Farm Rd, Rm 114|addr:care-of address with room number]], [[Cary|place!:town that is also a first name]], NC [[27511|zip]]
PROPERTY:  [[1027 Thistle Brook Court|addr]], [[Wake Forest|place!:town name made of common words]], NC [[27587|zip]]
           [[Lot 14, Block 2, Oakwood Crest Phase II|addr!:legal description of the lot]], [[Map Book 2004, Page 1183|rec:plat recording reference]], [[Wake County|place:county]]
           PIN [[1840-67-2291|rec:parcel identification number]]      REID [[0318472|rec!:real estate ID, digits only]]
LENDER:    [[Longleaf Home Lending, Inc.|o2:full]], loan no. [[4400918273|rec!:loan number, digits only]], 30-year fixed at 6.375%

                                                   BUYER DEBIT      BUYER CREDIT     SELLER DEBIT    SELLER CREDIT
Sale Price                                         [[$468,500.00|money]]                                       [[468,500.00|money!:no currency sign]]
Earnest Money (held by [[Dogwood Realty Partners|o7:full]])                      [[$7,500.00|money]]
Due diligence fee paid to Seller [[5/2/26|date:numeric date with two-digit year]]                         [[2,000.00|money!:no currency sign]]         2,000.00
Loan Amount                                                         [[$374,800.00|money]]
Origination (0.5 pt)                                   [[1,874.00|money!:no currency sign]]
Appraisal (POC by Borrower, [[$625|money]])
Prepaid Interest [[7/1|date:month/day only]] - [[8/1|date:month/day only]]                             [[$2,029.17|money]]
Homeowner's Insurance Premium, 12 mo.                  [[$1,611.00|money]]
Initial Escrow deposit                                 [[$1,947.36|money]]
County Taxes [[1/1|date:month/day only]] - [[6/30|date:month/day only]] (183 of 365 days)                               [[$1,742.08|money]]      [[1,742.08|money!:no currency sign]]
HOA Dues proration, [[Oakwood Crest Homeowners Association, Inc.|o4:full]]     [[$46.00|money]]                                                [[46.00|money!:no currency sign]]
Owner's Title Insurance (Reissue Rate)                                                    [[$1,032.50|money]]
Lender's Title Insurance                                 [[$118.00|money]]
Settlement / Attorney fee                              [[$1,150.00|money]]                         [[$350.00|money]]
Recording: Deed and Deed of Trust                        [[$90.00|money]]
Excise Tax (Revenue Stamps)                                                               [[$937.00|money]]
Commission, Listing 2.5% + Selling 2.5%                                                [[$23,425.00|money]]
Payoff of Existing Mortgage, [[Neuse Basin Bank & Trust|o3:full]],
   acct [[xxxxxx5530|acct:masked account, last four]], good through 7/1                                        [[$141,206.44|money]]
Home Warranty                                                                             [[$575.00|money]]
                                                   -----------      -----------      -----------     -----------
TOTALS                                             [[$477,865.53|money]]     [[$386,042.08|money]]     [[$171,268.02|money]]     [[$468,546.00|money]]

CASH DUE FROM BUYERS AT CLOSING:   [[$91,823.45|money]]
NET PROCEEDS TO SELLER:           [[$297,277.98|money]]

Items Paid Outside Closing: Home Inspection, [[Carolina Wren Home Inspections|o5:full]], [[$485.00|money]], paid [[May 6|date:month and day only]] by
[[Mrs. Lindholm|p2:title-surname]] on her Visa ending [[2171|card:last four only]] (receipt in file; she asked about a refund of the radon
add-on, [[$150|money]] - not ours to refund). Survey waived.

DISBURSEMENT NOTES ([[JE|p4:initials]] / closer [[Darnell Uzun|p6:full]])
1. Buyers' funds: wire of $91,823.45 received [[6/29/2026|date]] 2:14 pm from the [[Lindholms|p1:surname!:plural surname for the couple]]' joint account at
   their credit union, Fed ref [[20260629MMQFMP9N004417|rec!:Fedwire reference, unlabelled format]]. Matches Closing Disclosure (TRID three-day timing OK).
2. Seller proceeds: [[Mr. Trzebiatowski|p3:title-surname]] is in assisted living and signed by attorney-in-fact, his nephew
   [[Silas Whitfield-Boyce|p5:full]] (POA recorded [[Deed Book 19644, Page 0871|rec:recording reference]]). Proceeds by wire per instructions
   signed in person:
        Beneficiary   Bartholomew Trzebiatowski
        Bank          Neuse Basin Bank & Trust
        ABA           [[053744106|rtn]]
        Account       [[000418827730|acct!:account number with leading zeros]]
   [[Darnell|p6:first-name]] called [[Silas|p5:first-name]] back at [[919.555.0177|phone:dotted]] (number from the POA, not from the email) and read the
   account to him before release. Do NOT accept changed instructions by email.
3. Form 1099-S: gross proceeds $468,500.00 to seller, TIN [[104-59-4081|ssn:SSN used as TIN]] per Form W-9. [[Bart|p3:nickname]] turned
   [[91|age:bare age]] in April; [[Silas|p5:first-name]] says the sale is paying for memory care, so expect questions from the
   family about the tax.
4. [[Soren|p1:first-name]]'s name on the loan docs was typed "[[Soren A Lindolm|p1:short!:misspelled name]]" on the first set; corrected set signed.
   His SSN on the 4506-C ends [[9285|ssn:last four only]]; hers ends [[1824|ssn!:last four that looks like a year]].
5. Fannie Mae condo questionnaire not applicable. N.C. Gen. Stat. § 47H does not apply (no option contract).

Notary: [[Darnell Uzun|p6:full]], Notary Public, Wake County, NC. Commission no. [[20211740062|govid!:notary commission number, digits only]]. My commission
Expires [[March 9, 2027|date:commission expiry date]].
Further questions: [[closings@anchorpointtitle.example|email]]
'''))

# ---------------------------------------------------------------- 237
DOCS.append(D(237, "txt", "foreign account reporting worksheet", "accounting", "US",
  title="FBAR / Form 8938 worksheet for tax year 2025",
  ents={"p1": "Beatriz S. Quaresma", "p2": "Declan Rafferty", "p3": "Hideo Oyama", "p4": "Amelia Quaresma",
        "p5": "Leonor Quaresma",
        "o1": "Ferncliff & Oyama CPAs", "o2": "Banco Minhoto de Aforro, S.A.", "o3": "Shannonside Savings Bank plc",
        "o4": "Volksbank Altmuehltal eG", "o5": "Banque Privee Leman-Rive SA", "o6": "Ironbound Biologics, Inc."},
  distractors=["FinCEN Form 114", "Form 8938", "31 U.S.C. § 5314", "Schedule B", "Form 3520", "Form 1116",
               "Treasury Reporting Rates of Exchange", "Form 8854", "BSA E-Filing"],
  ok=["FBAR", "FATCA", "WORKSHEET", "Tax", "2025", "2024", "Filer", "Spouse", "Joint", "Owner", "Accounts",
      "Max", "Opened", "Current", "Savings", "Time", "Custody", "Securities", "Signature", "Authority", "Only",
      "Financial", "Interest", "Portugal", "Ireland", "Germany", "Switzerland", "US", "EUR", "CHF", "USD",
      "Part", "I", "II", "III", "IV", "1", "2", "3", "4", "5", "10,000", "50,000", "0.923", "0.851",
      "Aggregate", "Threshold", "Questions", "Preparer", "Client", "Dec", "31", "Yes", "No", "Line", "7a", "7b",
      "April", "Oct", "15", "Automatic", "Extension", "Foreign", "Inherited", "Late", "Streamlined", "IBAN",
      "BIC", "NIF", "PPS", "She", "He", "Sister", "FinCEN", "2003", "2027", "3520", "Amend", "Dividends",
      "FBARs", "Filing", "Fixed", "Matured", "Penalty", "Portfolio", "QC", "Swiss", "January"],
  body=r'''
[[Ferncliff & Oyama CPAs|o1:full]]                                         FBAR / FATCA WORKSHEET - Tax Year 2025
[[60 Park Place, 11th Floor|addr:street with floor]], [[Newark|place:city]], [[NJ|place:state abbreviation]] [[07102|zip]]          Client no. [[Q-1182|rec:client number]]     Preparer: [[H. Oyama|p3:short:initial and surname]]

Part I - Filer
  Name:            [[Beatriz S. Quaresma|p1:full]] (passport shows [[QUARESMA, BEATRIZ SOFIA|p1:caps:Last, First in ALL CAPS]])
  SSN:             [[341-20-3668|ssn]]            DOB: [[23.08.1984|dob:day-first with dots]]
  Status:          [[Portuguese citizen; U.S. lawful permanent resident since 2017|attr:citizenship and immigration status]]. [[Green card renewal pending|attr:immigration status]].
  [[Portuguese|attr:nationality adjective]] passport no. [[CB482219|govid:passport number]], expires [[11 Mar 2029|date:day month year, abbreviated]].   Portuguese NIF [[248117903|taxid!:foreign tax number, digits only]]
  Home:            [[74 Ferry Street, Apt 3R|addr:street with apartment]], Newark, NJ [[07105|zip]] (the [[Ironbound|place:neighbourhood]])
  Employer:        [[Ironbound Biologics, Inc.|o6:full]], senior QC chemist
  Phone / email:   [[973-555-0148|phone]]   [[bquaresma@fastmail.example|email]]
  Spouse:          [[Declan Rafferty|p2:full]], [[Irish citizen on an H-1B|attr:citizenship and immigration status]], SSN [[118-65-2246|ssn]], [[Irish|attr:nationality adjective]] PPS no. [[4471902TA|taxid:Irish PPS number]].
                   Filing jointly. He files his own FinCEN Form 114 for account 3 (joint, both report).

Part II - Accounts (maximum value during 2025, in account currency, then USD at the Treasury Reporting Rates of
Exchange for Dec 31, 2025: EUR 0.923, CHF 0.851 per dollar)

 1. [[Banco Minhoto de Aforro, S.A.|o2:full]], [[Rua do Souto 114|addr:Portuguese street address]], [[4700-328|zip:Portuguese postal code]] [[Braga|place:city abroad]], Portugal
    Current account, Owner: [[Beatriz|p1:first-name]] only. Opened 2003.
    IBAN [[PT81 2183 7855 3254 1891 7151 4|iban:IBAN with spaces]]     BIC [[BMAFPTPL|acct:SWIFT code]]
    Max [[EUR 18.412,60|money:European number format with currency code]]  =  [[$19,948.65|money]]           Year-end [[€6.930,11|money:European number format]]
 2. Same bank, Time deposit (Fixed-term), account [[0033.0000.45518220.77|acct:Portuguese domestic account number]]
    Max [[€40.000,00|money:European number format]]  =  [[$43,336.94|money]].  Matured [[14/10/2025|date:day-first numeric]], rolled into account 1 then wired to NJ.
 3. [[Shannonside Savings Bank plc|o3:full]], [[12 O'Connell Street|addr:street address abroad]], [[Limerick|place:city abroad]], [[V94 T2X8|zip:Irish Eircode]], Ireland
    Joint with spouse. Savings.
    IBAN [[IE64BOFI86831682855568|iban:IBAN without spaces]]       BIC [[SHSBIE2L|acct:SWIFT code]]
    Max [[31 205.44 EUR|money:space as thousands separator, currency code after]]  =  [[$33,808.71|money]]
 4. [[Volksbank Altmuehltal eG|o4:full]], [[Marktplatz 9|addr:German street address]], [[91781|zip:German postal code]] [[Weissenburg|place:town abroad]], Germany
    Signature Authority Only - account of her late father's estate; she is co-executor with her sister.
    No Financial Interest. IBAN [[DE70 1151 0087 1059 8963 84|iban:IBAN with spaces]]
    Max [[112.870,00 €|money:European number format, symbol after]]  (report value; no income to her)
 5. [[Banque Privee Leman-Rive SA|o5:full]], [[Quai du Mont-Blanc 21|addr:Swiss street address]], [[1201|zip!:Swiss postal code, four digits]] [[Geneve|place:city abroad]], Switzerland
    Securities Custody account, Inherited from her mother [[May 2024|date:month and year only]]. Portfolio no. [[5.218.447-01|acct:portfolio number]]
    IBAN [[CH43 3948 2743 2366 2351 9|iban:IBAN with spaces]]
    Max [[CHF 204'650.00|money:Swiss number format with apostrophe]]  =  [[$240,481.79|money]]       Dividends 2025: [[CHF 3'118.25|money:Swiss number format with apostrophe]]

    Aggregate maximum: well over the 10,000 Threshold, so FinCEN Form 114 required (31 U.S.C. § 5314).
    Form 8938: joint filers living in the US, 50,000 year-end / Threshold met because of account 5.

Part III - Questions for client (call [[2/26/2026|date:call date]])
  - Was the 2024 FBAR filed? She says no: her mother [[Leonor Quaresma|p5:full]] died [[12 May 2024|date:date of death]] in [[Geneve|place:city abroad]] and nobody told
    her the custody account had been retitled until the bank wrote in January. Late 2024 FBAR needed with
    reasonable-cause statement; discuss Streamlined procedures only if the dividends were left off the 2024
    return (they were: about [[$2,900|money]]). Amend.
  - Sister [[Amelia Quaresma|p4:full]] lives in [[Porto|place:city abroad]] and holds the other half of the estate account (no. 4). [[Amelia|p4:first-name]] is
    [[not a U.S. person|attr:citizenship status stated in the negative]], no filing for her.
  - Did the inheritance exceed the Form 3520 amount? Yes - the Swiss securities alone were about [[$231k|money:abbreviated amount]]
    at date of death. Form 3520 for 2024 was NOT filed. Penalty exposure; raise with [[Hideo|p3:first-name]] before calling her back.
  - [[Declan|p2:first-name]] asks whether leaving the US in 2027 triggers anything (Form 8854 - no, he is not a long-term resident).
  - Schedule B, Part III, Line 7a Yes; 7b: Portugal, Ireland, Germany, Switzerland.

Part IV - Filing
  FBAR due April 15, Automatic Extension to Oct 15. File through BSA E-Filing; her FinCEN account login is
  [[bquaresma84|cred:username]] (she will type the password herself in the office). Foreign tax paid on Swiss dividends
  [[CHF 1'091.39|money:Swiss number format with apostrophe]] - Form 1116.
  Fee quote: [[$1,450|money]] for both FBARs and Form 8938; [[$900|money]] more for the late 3520.    [[HO|p3:initials]] [[3/2/26|date:numeric date with two-digit year]]
'''))

# ---------------------------------------------------------------- 238
DOCS.append(D(238, "pptx", "fleet incident review deck", "general", "US",
  title="Quarterly fleet incident review - Q2 2026",
  ents={"p1": "Leilani Kahale", "p2": "Viktor Malinowski", "p3": "Ruth Okonedo", "p4": "Barrett Yancey",
        "p5": "Consuelo Arrieta", "p6": "Dale Fitzhugh",
        "o1": "Quarry Road Beverage Distributors, Inc.", "o2": "Hawthorne Commercial Indemnity Co.",
        "o3": "Ocotillo Collision & Frame", "o4": "Camelback Occupational Health",
        "o5": "RoadLedger Telematics"},
  distractors=["49 CFR § 382.303", "Form MCS-150", "Freightliner M2", "Ram ProMaster", "Isuzu NPR",
               "FMCSA", "OSHA 300 log"],
  ok=["Q2", "2026", "Q1", "Fleet", "Incident", "Review", "Safety", "Committee", "Summary", "Unit", "Driver",
      "Plate", "Vehicle", "Claim", "Cost", "Repair", "Est", "Telematics", "Device", "Incidents", "Actions",
      "Owner", "Due", "Testing", "Negative", "I-10", "CDL", "Class", "B", "MVR", "HR", "DOT", "Speaker",
      "Total", "Subrogation", "Open", "Hard", "Braking", "Camera", "Backing", "Sideswipe", "2", "4", "5", "38",
      "52", "No", "Next", "Do", "Not", "Notes", "Result", "Tests", "Lic", "Cameras", "Three", "Loss", "Run",
      "Injury", "Injuries", "0.9", "10", "Coaching", "DC", "Decision", "Driver's", "OK", "Parked", "Portal",
      "Post", "Rear", "Risk", "Spotter", "Struck"],
  body=r'''
# Fleet Incident Review - Q2 2026
[[Quarry Road Beverage Distributors, Inc.|o1:full]]
Safety Committee, [[July 14, 2026|date:meeting date]]. Prepared by [[Consuelo Arrieta|p5:full]], Fleet & Risk Manager
CONFIDENTIAL - contains personnel and claim information. Do Not forward outside the committee.
> Speaker notes: remind everyone this deck is not to be saved to personal drives. Loss Run from [[Hawthorne Commercial Indemnity Co.|o2:full]] is as of [[6/30/26|date:numeric date with two-digit year]].
# Summary
- Three incidents this quarter (Q1: 5). Two preventable.
- Total incurred to date [[$41,930|money]]; our deductible is [[$2,500|money]] per claim on policy [[HCI-CA-7730418|rec:policy number]].
- No DOT-recordable crashes. One OSHA 300 log entry (shoulder).
- All three units carry [[RoadLedger Telematics|o5:full]] gateways and dash Cameras.
# Incidents
| Unit | Date | Driver | Vehicle / Plate | Type | Claim | Est. Cost |
| [[112|rec!:fleet unit number, unlabelled]] | [[4/9/26|date:numeric date with two-digit year]] | [[L. Kahale|p1:short:initial and surname]] | Freightliner M2 / [[AZ|place:state abbreviation]] [[AB4 7TK2|veh:license plate with a space]] | Backing, dock at [[Chandler|place!:city that is also a surname and first name]] DC | [[HCI-26-0041877|rec:claim number]] | [[$6,180|money]] |
| [[117|rec!:fleet unit number, unlabelled]] | [[5/21/26|date:numeric date with two-digit year]] | [[V. Malinowski|p2:short:initial and surname]] | Ram ProMaster / AZ [[CKR9041|veh!:license plate, no separator]] | Rear-end, I-10 at [[Baseline Rd|place!:road used as a location]] | [[HCI-26-0058102|rec:claim number]] | [[$31,400|money]] |
| [[204|rec!:fleet unit number, unlabelled]] | [[6/12/26|date:numeric date with two-digit year]] | [[R. Okonedo|p3:short:initial and surname]] | Isuzu NPR / AZ [[BXT 5520|veh:license plate with a space]] | Sideswipe, parked car, [[Tempe|place:city]] | [[HCI-26-0066390|rec:claim number]] | [[$4,350|money]] |
# Unit 112 - Backing (preventable)
- Driver: [[Leilani Kahale|p1:full]], CDL Class B, AZ Lic. [[D08841297|govid:driver's license number]], hired [[Feb 2022|date:abbreviated month and year]]
- VIN [[1FVACWFC5NHNK4418|veh:VIN]]; Telematics Device [[RL-GW-00A4F17C|dev:telematics gateway ID]]
- Struck a bollard while backing without a spotter. No Injuries.
- Repair at [[Ocotillo Collision & Frame|o3:full]], invoice [[OCF-11827|rec:invoice number]], [[$6,180.00|money]] paid [[5/4|date:month/day only]]
- Post-incident Tests at [[Camelback Occupational Health|o4:full]]: Negative
> Notes: [[Leilani|p1:first-name]] self-reported within 10 minutes. First incident in 4 years. Coaching only.
# Unit 117 - Rear-end (preventable)
- Driver: [[Viktor Malinowski|p2:full]], employee no. [[E-3381|rec:employee ID]], AZ Lic. [[D05570126|govid:driver's license number]]
- VIN [[3C6LRVDG7PE562290|veh:VIN]]; gateway [[RL-GW-00A51B03|dev:telematics gateway ID]]; camera serial [[DC4-7719-KQ|dev:dash camera serial number]]
- Telematics: 52 mph in a 38 mph work zone; Hard Braking 0.9 seconds before impact; phone handling flagged by camera
- Other party: 2 occupants, soft-tissue claims; Hawthorne adjuster [[Barrett Yancey|p4:full]], [[602-555-0137|phone]], reserve [[$25,000|money]] bodily Injury
- Driver's own Injury: [[right shoulder strain, 9 days restricted duty|health:work injury]] (workers' comp claim [[WC-AZ-26-118845|rec:workers' compensation claim number]])
- Post-incident Testing under 49 CFR § 382.303 not required (no CDL vehicle); company policy test done anyway. Result: [[non-negative for THC, confirmed by MRO|health:drug test result]]
> Speaker notes: [[Viktor|p2:first-name]] told HR he [[holds a state medical marijuana card for PTSD|health:condition and treatment disclosed to HR]] from [[his Army service|attr:veteran status]]. This is NOT for discussion in committee beyond "policy violation under review." [[Dale Fitzhugh|p6:full]] (HR) owns it. His MVR also shows [[a 2023 citation for texting while driving|attr:driving record]].
# Unit 204 - Sideswipe (non-preventable)
- Driver: [[Ruth Okonedo|p3:full]], AZ Lic. [[D11206483|govid:driver's license number]]
- VIN [[JALC4W167P7K01156|veh:VIN]]; gateway [[RL-GW-00A4D9E0|dev:telematics gateway ID]]
- Parked car door opened into the lane on [[Mill Avenue|place!:street used as a location]]. Camera clears our driver.
- Other vehicle: AZ plate [[HJL2R7|veh!:license plate of a third party, no separator]], owner's insurer has accepted liability. Subrogation Open, [[$4,350.00|money]] expected back.
- Post-incident Tests: Negative
> Notes: [[Ruth|p3:first-name!:first name that is also a common word]] is [[the shop steward for the drivers' local|attr:union role]]; she asked that the camera clip not be used in training without her OK.
# Actions
| Action | Owner | Due |
| Spotter rule retraining, all Class B drivers | [[C. Arrieta|p5:short:initial and surname]] | [[Aug 1|date:abbreviated month and day]] |
| Decision on Unit 117 driver | [[D. Fitzhugh|p6:short:initial and surname]] | [[7/24|date:month/day only]] |
| Update Form MCS-150 mileage (FMCSA) | Arrieta | [[August 31, 2026|date:deadline]] |
| Ask [[Hawthorne|o2:short]] about camera credit at renewal ([[10/1/2026|date:renewal date]]) | [[Yancey|p4:surname]] / [[Arrieta|p5:surname]] | Next meeting |
> Notes: questions to [[carrieta@quarryroadbev.example|email]] or ext. [[4417|phone!:internal extension only]]. Portal for clips: [[https://fleet.roadledger.example/qrbd/incidents|url:customer-specific portal link]], shared login [[qrbd_safety|cred:shared username]].
'''))

# ---------------------------------------------------------------- 239
DOCS.append(D(239, "txt", "pharmacy transfer note", "health", "US", length="short",
  title="Prescription transfer note",
  ents={"p1": "Wilhelmina Greenhalgh", "p2": "Ravi Seetharaman", "p3": "Dot Greenhalgh-Pace",
        "o1": "Stillwater Apothecary", "o2": "Orchard Hill Drug"},
  distractors=["Eliquis", "21 CFR § 1306.25"],
  ok=["RX", "TRANSFER", "IN", "Pt", "Rx", "BID", "Refills", "Prescriber", "From", "2", "Daughter", "Not", "#60",
      "C", "II", "DEA", "N"],
  body=r'''
RX TRANSFER IN - [[Orchard Hill Drug|o2:full]], [[6/3/26|date:numeric date with two-digit year]]
From: [[Stillwater Apothecary|o1:full]], [[405-555-0119|phone]]
Pt: [[GREENHALGH, WILHELMINA|p1:caps:Last, First in ALL CAPS]], DOB [[1/8/1930|dob]] ([[96 y/o|age:abbreviated age]])
Rx [[4471826|rec!:prescription number, digits only]]: [[apixaban 2.5 mg|health:medication and dose]] BID, #60, Refills 2 (Eliquis; Not C-II, 21 CFR § 1306.25 N/A)
Prescriber: [[Dr. R. Seetharaman|p2:short:title, initial and surname]], DEA [[FS4418260|govid:DEA number]]
Allergy: [[sulfa|health:allergy]]
Daughter [[Dot|p3:nickname]] picks up; call [[4055550164|phone]].
'''))

# ---------------------------------------------------------------- 240
DOCS.append(D(240, "docx", "stepparent adoption notes", "legal", "US",
  title="Attorney notes to file - stepparent adoption",
  header="[[Abebe Family Law, P.C.|o1:full]] - PRIVILEGED AND CONFIDENTIAL - File [[26-AD-0173|rec:firm file number]]",
  ents={"p1": "Nathaniel J. Vanterpool", "p2": "Jocelyn Vanterpool", "p3": "Elias Batista Rourke",
        "p4": "Shane Rourke", "p5": "Corinne Abebe", "p6": "Imelda Batista", "p7": "Priscilla Nyberg",
        "o1": "Abebe Family Law, P.C.", "o2": "Columbine Family Assessments, LLC",
        "o3": "Cherry Creek Trail Elementary", "o4": "Peakline Aerospace Fasteners, Inc.",
        "o5": "Aurora Meadows Pediatric Group"},
  minors=["p3"],
  distractors=["C.R.S. § 19-5-203(1)(d)(II)", "C.R.S. § 19-5-105.5", "Form JDF 501", "Form JDF 503", "ICWA",
               "Colorado Bureau of Investigation", "TRAILS", "Servicemembers Civil Relief Act"],
  ok=["Stepparent", "Adoption", "Notes", "File", "Conference", "Petitioner", "Mother", "Child", "Birth",
      "Grounds", "Background", "Checks", "Home", "Study", "Costs", "To", "Do", "Colorado", "District", "Court",
      "FBI", "Petition", "Consent", "Affidavit", "Diligent", "Search", "Decree", "Vital", "Records", "New",
      "Indian", "No", "He", "1", "2", "3", "4", "5", "6", "7", "8", "9", "12", "2019", "Publication",
      "Abandonment", "Failure", "Support", "Filing", "Flat", "Fee", "Ask", "Draft", "Calendar", "Married",
      "Not", "Fingerprints", "11", "5th", "6th", "70", "Atty", "Reg", "Dad", "Dental", "Family", "Never",
      "Pediatrician", "Tooling", "Explanation"],
  body=r'''
# Stepparent Adoption - Notes to File
**Attorney:** [[Corinne Abebe|p5:full]] (Atty. Reg. No. [[44718|govid:attorney registration number]]). **Conference:** [[Thursday, May 14, 2026|date:date with weekday]], both clients in the office, about 70 minutes.
## 1. Petitioner (stepfather)
[[Nathaniel J. Vanterpool|p1:full]] ("[[Nate|p1:nickname]]"), born [[July 6, 1986|dob]] in [[Wichita|place:city]], [[Kansas|place:state]]. SSN [[359-10-7624|ssn]]. Colorado driver license [[17-204-8831|govid:driver's license number]]. Tooling engineer at [[Peakline Aerospace Fasteners, Inc.|o4:full]] since 2019; salary [[$104,000|money]] plus bonus. Married the mother on [[09/18/2021|date:marriage date]]. Has lived with the child since [[June 2020|date:month and year only]].
## 2. Mother
[[Jocelyn Vanterpool|p2:full]], formerly [[Jocelyn Batista|p2:short:former (maiden) name]], DOB [[12/01/1989|dob]]. Dental hygienist, part time, about [[$38,500|money]] a year. Cell [[720-555-0142|phone]]; [[jocelyn.vanterpool@mailhaven.example|email]]. Family home: [[19044 East Girard Place|addr]], [[Aurora|place!:city that is also a first name]], [[CO|place:state abbreviation]] [[80013|zip]] ([[Arapahoe County|place:county]]).
## 3. Child
[[Elias Batista Rourke|p3:full]], goes by [[Eli|p3:nickname]], born [[February 2, 2015|dob:birth date of a minor]] in [[Amarillo|place:city]], [[Texas|place:state]]; he is 11 and in 5th grade at [[Cherry Creek Trail Elementary|o3:full]]. Texas birth certificate, state file no. [[142-15-018827|govid:birth certificate state file number]]. SSN ends [[-2246|ssn:last four with dash]]. Pediatrician: [[Aurora Meadows Pediatric Group|o5:full]]. [[Eli|p3:nickname]] [[has ADHD and takes methylphenidate ER 27 mg|health:diagnosis and medication of a minor]] on school days. He is 11, so his written consent is not required (it would be at 12), but the court will want to hear from him. He calls [[Nate|p1:nickname]] "Dad" and asked on his own whether his name can be [[Elias Batista Vanterpool|p3:full:proposed new name]]. Not an Indian child; ICWA inquiry made of both sides of the family, none claimed.
## 4. Birth father
[[Shane Rourke|p4:full]], DOB [[10/23/1987|dob]]. Never married to the mother; on the birth certificate. Last contact with [[Elias|p3:first-name]] was a phone call at [[Christmas 2022|date:holiday and year]]. Last-known address [[c/o 4417 SW 45th Avenue, Lot 12|addr:care-of address with lot number]], Amarillo, [[TX|place:state abbreviation]] [[79109|zip]]; his mother there says he "comes and goes." Child support order out of [[Potter County|place:county]], Texas, cause no. [[D-1-FM-16-004418|rec:family court cause number]]: [[$415 a month|money:monthly support amount]], nothing paid since [[March 2023|date:month and year only]], arrears about [[$16,600|money]]. [[Mr. Rourke|p4:title-surname]] [[served 14 months in a Texas state jail for possession of a controlled substance (released 2021)|attr:criminal history]]. [[Jocelyn|p2:first-name]] does not want his record "thrown at him" if he will simply sign.
## 5. Grounds
If [[Shane|p4:first-name]] signs Form JDF 503 (consent), we proceed on consent. If he cannot be found or refuses: C.R.S. § 19-5-203(1)(d)(II), Abandonment for a year or more or Failure to pay reasonable Support for a year or more without cause. Servicemembers Civil Relief Act Affidavit needed either way; [[Jocelyn|p2:first-name]] says he was never in the military.
## 6. Background Checks
Fingerprints submitted [[5/15|date:month/day only]]; Colorado Bureau of Investigation and FBI results come back to the court directly. TRAILS (child abuse registry) check requested for both adults. [[Nate|p1:nickname]] disclosed, before I asked, [[a 2011 misdemeanor DUI|attr:criminal history]] in [[Sedgwick County|place:county]], Kansas, deferred and dismissed. Explanation goes with the Petition (Form JDF 501); not disqualifying under C.R.S. § 19-5-105.5.
## 7. Home Study
If the court orders one: [[Columbine Family Assessments, LLC|o2:full]], evaluator [[Priscilla Nyberg|p7:full]], LCSW, [[303.555.0166|phone:dotted]], flat [[$850|money]]. [[Ms. Nyberg|p7:title-surname]] will want to meet the maternal grandmother, [[Imelda Batista|p6:full]], who lives in the basement apartment and does after-school care. [[Imelda|p6:first-name]] [[is a lawful permanent resident from Brazil|attr:immigration status and national origin]]; she worries about being fingerprinted. Told [[Jocelyn|p2:first-name]] the registry check is by name and date of birth only (hers: [[4 April 1962|dob:day month year]]).
## 8. Costs
Flat Fee [[$3,200.00|money]] ([[thirty-two hundred|money:amount in words without currency]]), half paid today by check no. [[2291|rec!:check number that looks like a year]]. Filing Fee [[$167|money]]. Publication, if needed, roughly [[$300|money]]. New birth certificate from Texas Vital Records [[$27.00|money]].
## 9. To Do
- Draft Petition and Consent; send Consent to Shane by certified mail and to [[shanerourke87@quickpost.example|email]], the last email [[Jocelyn|p2:first-name]] has for him.
- Diligent Search Affidavit if nothing back by [[June 15|date:month and day only]].
- Ask [[Arapahoe County|place:county]] District Court clerk for a hearing in [[late August|date:approximate date without year]] so the Decree is in hand before 6th grade registration. Case number once filed will be in the form [[2026JA000---|rec:placeholder juvenile case number]].
- Calendar: Eli turns 12 on [[2/2/2027|date:birthday of a minor, used as a deadline]]. File well before then.
[[CA|p5:initials]]
'''))
