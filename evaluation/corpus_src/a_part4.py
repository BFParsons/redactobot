"""Batch A, documents 15-20 (imported by batch_a.py)."""
from corpus_src.dsl import D, dt, amt, num

DOCS = []

# ---------------------------------------------------------------- doc 15
DOCS.append(D(15, "md", "board minutes", "general", "US",
  title="Board minutes - outdoor retailer",
  ents={"p1": "Marguerite Calder", "p2": "Tobias Finch", "p3": "Anjali Deshpande-Hall", "p4": "Curtis Whitehorse",
        "p5": "Yuki Tanabe", "p6": "April Sorensen", "p7": "Jesse Reyes",
        "o1": "Calder & Finch Outfitters, Inc.", "o2": "High Desert Community Bank", "o3": "Cascade Fleet Sales",
        "o4": "Summit Ridge Mutual", "o5": "Three Creeks Trail Alliance", "o6": "Sorensen Lyle LLP"},
  distractors=["ORS 60.337", "Robert's Rules", "Q4", "Ram ProMaster", "MFA", "Sprinter", "BOLI"],
  body=r'''
# [[Calder & Finch Outfitters, Inc.|o1:full]]

## Minutes of the Regular Meeting of the Board of Directors

**Date:** [[Tuesday, January 20, 2026|date!:date with weekday]], 4:00 p.m.
**Place:** Company office, [[1045 NW Bond Street, 2nd floor|addr:street with floor]], [[Bend|place!:city name that is also a common word]], [[Oregon|place:state]], and by video

**Directors present:** [[Marguerite Calder|p1:full]] (Chair), [[Dr. Anjali Deshpande-Hall|p3:full:title + full name]], [[Rev. Curtis Whitehorse|p4:full:title + full name]], [[Yuki Tanabe|p5:full]] (CFO and Secretary)
**Absent:** [[Tobias Finch|p2:full]] (CEO), excused
**Also present:** [[April Sorensen|p6:full]], [[Sorensen Lyle LLP|o6:full]], outside counsel

### 1. Call to order

[[Ms. Calder|p1:title-surname]] called the meeting to order at 4:04 p.m. and confirmed a quorum under ORS 60.337. The minutes of the November meeting were approved without changes. The meeting followed Robert's Rules informally, as usual.

### 2. CEO leave of absence

The Chair reported that [[Tobias|p2:first-name]] began [[chemotherapy|health:treatment]] on [[January 6|date!:month and day only]] for [[non-Hodgkin lymphoma|health:diagnosis]] and expects to be away from day-to-day work for at least four months. He asked that staff be told only that he is on medical leave.

**RESOLVED:** [[Ms. Tanabe|p5:title-surname]] is appointed Acting Chief Executive Officer, effective immediately, with an additional stipend of [[$4,000|money]] per month. Carried 3-0, Ms. Tanabe abstaining.

### 3. Financial report

Ms. Tanabe presented the Q4 results. Revenue was [[$1.82 million|money!:millions written out]], up 6% on the prior year; the [[Redmond|place:city]] store again lost money ([[$41k|money!:abbreviated with k]] for the quarter). The line of credit with [[High Desert Community Bank|o2:full]] (loan no. [[4410-776-02|rec:loan number]]) stands at [[$310,000|money]] drawn against a [[$500,000|money]] limit. The company is in compliance with its covenants.

### 4. Delivery van

**RESOLVED:** The company may buy a used 2023 Ram ProMaster cargo van from [[Cascade Fleet Sales|o3:full]] for [[$38,450|money]] (VIN [[3C6LRVDG5PE518204|veh:VIN]]). It replaces the Sprinter, Oregon plate [[482 KVM|veh!:license plate with a space]], which will be sold. Carried unanimously.

### 5. Payroll fraud incident

On [[December 11, 2025|date]], a payroll clerk responded to a phishing email. The attacker then signed in to the payroll portal from IP address [[203.0.113.57|ip:IPv4]] using the Redmond store manager's account ([[jreyes.redmond|cred:username]]) and redirected the direct deposits of two employees. [[$14,280|money]] was diverted; [[$9,100|money]] has been recovered. The loss was reported to [[Summit Ridge Mutual|o4:full]] (claim no. [[CY-25-00817|rec:insurance claim number]]) and to the Bend police (case [[2025-00071934|rec:police case number]]). All portal passwords were reset and MFA is now required.

### 6. Executive session: personnel

[[Ms. Sorensen|p6:title-surname]] briefed the Board on the BOLI complaint (no. [[STEMDP251022-41877|rec:agency complaint number]]) filed by [[Jesse Reyes|p7:full]], the former Redmond store manager, who alleges he was dismissed in October shortly after telling Tobias he is [[HIV-positive|health:diagnosis]]. Management's position is that [[Mr. Reyes|p7:title-surname]] was dismissed over the cash-handling audit. [[April|p6:first-name!:first name that is also a month]] recommended settling.

**RESOLVED:** Counsel is authorized to settle the [[Reyes|p7:surname!]] matter for up to [[$22,500|money]] plus a neutral reference, on confidential terms. Carried 3-1, [[Rev. Whitehorse|p4:title-surname]] opposed.

### 7. Other business

- Donation of [[$2,500|money]] to the [[Three Creeks Trail Alliance|o5:full]] approved.
- Bank signers: Tobias is removed temporarily and [[Dr. Deshpande-Hall|p3:title-surname]] is added as second signer on the operating account ending [[3382|acct!:last four only]].

### 8. Adjournment

The next regular meeting is set for [[March 17, 2026|date]]. The meeting adjourned at 5:35 p.m.

*Submitted by Yuki Tanabe, Secretary. Draft; not yet approved.*
'''))

# ---------------------------------------------------------------- doc 16
DOCS.append(D(16, "txt", "clinical visit note", "health", "US",
  title="Office visit note (SOAP) - diabetes follow-up",
  ents={"p1": "Loretta M. Begaye", "p2": "Chidi Okwuosa", "p3": "Leonard Begaye", "p4": "Yvonne Tsosie",
        "o1": "Sagebrush Family Medicine", "o2": "Four Corners Health Alliance", "o3": "Red Mesa Behavioral Health",
        "o4": "Chaco Trail Pharmacy"},
  distractors=["ICD-10", "ADA guidelines", "BID", "CGM", "HEENT", "PHQ-9"],
  body=r'''
[[SAGEBRUSH FAMILY MEDICINE|o1:caps]]                                        OFFICE VISIT
Patient: [[BEGAYE, LORETTA M.|p1:last-first]]      MRN: [[SFM-0088213|rec:medical record number]]      DOB: [[11/08/1967|dob]] (58 y/o F)
DOS: [[02/12/2026|date:date of service]]    Provider: [[Dr. Okwuosa|p2:title-surname]]    Visit type: established, 30 min
Insurance: [[Four Corners Health Alliance|o2:full]], ID [[FCH-771-204-881|rec:health plan member ID]]

S:  [[Mrs. Begaye|p1:title-surname]] returns for follow-up of [[type 2 diabetes|health:diagnosis]], on insulin pump since 2022
    (pump serial [[NG2308841PX|dev:insulin pump serial number]]). Says she has been "forgetting" meal boluses most days since
    her husband [[Leonard|p3:first-name]] [[died in October|indirect!:family event tied to a named person]]. Sleeping 4-5 hrs. Appetite poor, then snacks late.
    Admits to [[3-4 beers most nights|health!:alcohol use]], up from "almost never." Denies thoughts of
    self-harm. PHQ-9 today: [[14|health!:depression screening score, bare number]]. No chest pain, no vision change, feet OK.
    She is [[Diné|attr:ethnicity / tribal affiliation]] and drives in from [[Shiprock|place:town]], about 40 minutes each way; missed
    the December visit because of the roads. Reminded me again that she is [[one of Jehovah's Witnesses|attr:religion]]
    and will not accept blood products; advance directive is on file.

O:  BP 148/92, HR 84, Wt 187 lb, BMI 32.1. Alert, tearful when discussing husband.
    HEENT unremarkable. Lungs clear. Feet: monofilament intact bilaterally.
    Labs [[2/5/2026|date:lab date]]: [[A1c 8.9%|health:lab result]] (was 7.6% in August), [[eGFR 61|health:lab result]], [[LDL 118|health:lab result]],
    urine microalbumin mildly elevated. CGM download: time in range 41%.

A:  1. Type 2 diabetes, uncontrolled, with missed boluses (ICD-10 code in chart)
    2. [[Moderate depression|health:mental health diagnosis]], likely [[bereavement-related|health!:mental health detail]]
    3. [[Hypertension|health:diagnosis]], above goal
    4. [[Risky alcohol use|health:substance-use assessment]], new

P:  - Pump: bolus reminders turned on at 7, 12 and 6. Continue [[metformin 1000 mg|health:medication and dose]] BID.
    - Increase [[lisinopril to 40 mg|health:medication and dose]] daily. Recheck BP in 4 wks per ADA guidelines.
    - Start [[sertraline 50 mg|health:medication and dose]] daily. Rx [[6620417|rec!:prescription number, digits only]] sent to [[Chaco Trail Pharmacy|o4:full]], [[505-555-0127|phone]].
    - Brief alcohol counseling done. She agrees to cut back; declines medication for it.
    - Referral to [[Yvonne Tsosie|p4:full]], LCSW, at [[Red Mesa Behavioral Health|o3:full]] for grief counseling.
      [[Loretta|p1:first-name]] prefers a counselor who speaks [[Navajo|attr!:language that implies ethnicity]]; [[Ms. Tsosie|p4:title-surname]] does.
    - OK to call her at [[(505) 555-0191|phone]]; do not leave details with her son.
    - RTC [[3/12/2026|date:follow-up date]].

Electronically signed: [[Chidi Okwuosa|p2:full]], MD   NPI [[1730284416|govid:NPI]]   02/12/2026 17:41
'''))

# ---------------------------------------------------------------- doc 17
DOCS.append(D(17, "html", "patient intake form", "health", "US",
  title="New patient registration form - dermatology practice",
  ents={"p1": "Paris J. Okonkwo-Hayes", "p2": "Imani Hayes", "p3": "Lionel Achampong", "p4": "Kavita Banerjee",
        "o1": "Lakemont Dermatology & Skin Surgery", "o2": "Meridian Street Coffee Roasters", "o3": "Piedmont Shield Health"},
  distractors=["HIPAA", "45 C.F.R. § 164.520", "Notice of Privacy Practices", "SPF 30", "Section 4"],
  body=r'''
# [[Lakemont Dermatology & Skin Surgery|o1:full]]
**New Patient Registration** (submitted online [[02/17/2026|date:submission date]] at 9:12 PM)
Please complete every section. Your answers are part of your medical record and are protected under HIPAA; see our Notice of Privacy Practices (45 C.F.R. § 164.520).
## Section 1. About you
| Question | Your answer |
| Legal name | [[Okonkwo-Hayes, Paris J.|p1:last-first]] |
| Name you go by | [[Paris|p1:first-name!:first name that is also a place]] or [[PJ|p1:initials]] |
| Date of birth | [[March 22, 1994|dob:written-out birth date]] |
| Social Security no. | [[710-47-6423|ssn:SSN with dashes]] |
| Gender identity | [[nonbinary (they/them)|attr!:gender identity]] |
| Sexual orientation | [[bisexual|attr:sexual orientation]] |
| Street address | [[3300 Peachtree Battle Ave NW, Unit 4D|addr:street with unit]] |
| City, state, ZIP | [[Atlanta|place:city]], [[GA|place:state abbreviation]] [[30305|zip]] |
| Mobile phone | [[+1 404 555 0155|phone!:international format with spaces]] |
| Email | [[pj.okonkwohayes@webmail.example|email]] |
| Employer | [[Meridian Street Coffee Roasters|o2:full]] |
| Driver's license | [[GA 058812447|govid:driver's license number with state]] |
## Section 2. Emergency contact
| Question | Your answer |
| Name | [[Imani Hayes|p2:full]] |
| Relationship to you | [[wife|indirect!:family relationship]] |
| Phone | [[404.555.0129|phone:dotted]] |
## Section 3. Insurance
| Question | Your answer |
| Insurance company | [[Piedmont Shield Health|o3:full]] |
| Member ID | [[PSH220471889-01|rec:health plan member ID]] |
| Group number | [[0077154|rec:insurance group number]] |
| Policy holder | Imani Hayes |
| Policy holder date of birth | [[1992-07-30|dob:ISO format]] |
## Section 4. Health history
| Question | Your answer |
| Reason for visit | [[mole on left shoulder that has changed colour|health:presenting complaint]] |
| Skin conditions | [[psoriasis|health:diagnosis]] since high school |
| Family history | [[father had melanoma at 52|health!:family medical history]] |
| Current medications | [[Truvada for PrEP|health!:medication that implies HIV prevention]]; [[escitalopram 10 mg|health:medication and dose]] |
| Allergies | [[sulfa drugs|health:allergy]] (hives) |
| Sunscreen use | SPF 30, most days |
## Section 5. Card on file for copays
| Question | Your answer |
| Card number | [[5515-6122-7388-0483|card:card number with dashes]] |
| Expiry | [[04/29|exp]] |
| Security code | [[881|cvv]] |
| Billing ZIP | same as above |
## Section 6. Patient portal
Your portal user name is [[pj.okhayes|cred:portal username]]. Activate your account within 7 days: [[https://my.lakemontderm.example/activate?t=8f3a1c77|url:activation link with token]]
## Signature
I certify that the information above is correct. /s/ [[Paris J. Okonkwo-Hayes|p1:full]]
## Office use only
MRN [[LD-104772|rec:medical record number]]. Insurance verified by [[K. Banerjee|p4:short:initial + surname]] on [[2/18/26|date!:numeric date with two-digit year]]; copay [[$40|money]]. Referred by [[Dr. Lionel Achampong|p3:full:title + full name]], NPI [[1548839201|govid:NPI]], fax [[(404) 555-0102|phone:fax]]. Section 4 reviewed; flag family history for the provider.
'''))

# ---------------------------------------------------------------- doc 18
DOCS.append(D(18, "rtf", "referral letter", "health", "US",
  title="Referral letter - internal medicine to cardiac electrophysiology",
  ents={"p1": "Cornelius van Wyk", "p2": "Evangeline Papadakis-Stone", "p3": "Rajesh Venkatesan",
        "p4": "Annika van Wyk-Bauer",
        "o1": "Blue Heron Internal Medicine", "o2": "Tidewater Heart Rhythm Associates", "o3": "Windward Commons"},
  distractors=["CHA2DS2-VASc", "Medicare", "ECG", "Part B", "February"],
  body=r'''
# [[Blue Heron Internal Medicine|o1:full]]
[[77 Wharf Street, Suite 3|addr:street with suite]], [[Beaufort|place:town]], [[NC|place:state abbreviation]] [[28516|zip]]
Phone [[252-555-0136|phone]] / Fax [[252-555-0137|phone:fax]]
[[10 Feb 2026|date:day-month-year]]
[[Rajesh Venkatesan|p3:full]], MD
[[Tidewater Heart Rhythm Associates|o2:full]]
[[2100 Stantonsburg Road|addr]], [[Greenville|place:city]], NC [[27834|zip]]
**Re: [[Cornelius van Wyk|p1:full]] ("[[Neil|p1:nickname]]"), DOB [[6 Jun 1931|dob:day-month-year]], Medicare no. [[7RK2-WD4-XN61|govid:Medicare beneficiary identifier]], our chart [[BH-20417|rec:medical record number]]**
Dear [[Raj|p3:nickname]],
Thank you for seeing [[Mr. van Wyk|p1:title-surname]], a [[94-year-old|age:age in years]] man who is well known along the waterfront here as the [[last surviving Morehead City harbor pilot of his generation|indirect!:unique role in a small community]]. He lives at [[Windward Commons|o3:full]] assisted living and remains sharp and independent.
He has a dual-chamber pacemaker placed in 2017 for [[complete heart block|health:diagnosis]] (generator serial [[PJK418873H|dev:pacemaker serial number]]). On [[February 1|date!:month and day only]] he had a [[brief syncopal episode|health:medical event]] at breakfast. Staff found him pale but alert within a minute; he refused transport. I saw him two days later. ECG showed a paced rhythm at 60. Our in-office device check suggests the battery is near elective replacement, and it logged eleven episodes of [[atrial fibrillation|health:diagnosis]] since October, the longest about six hours.
Other history: [[chronic kidney disease, stage 3|health:diagnosis]]; [[prostate cancer treated with radiation in 2009|health:medical history]]; an echocardiogram last spring showed an [[ejection fraction of 45%|health:test result]]. Medications: [[apixaban 2.5 mg twice daily|health:medication and dose]] (started by me on the 3rd; CHA2DS2-VASc of 4), [[metoprolol succinate 25 mg|health:medication and dose]], tamsulosin, vitamin D. No known drug allergies.
I would be grateful for your opinion on generator replacement, and on whether the syncope is device-related. Neil has told me plainly that he [[does not want resuscitation|health!:end-of-life preference]] but does want the pacemaker kept working. His daughter and health care agent, [[Annika van Wyk-Bauer|p4:full]], will bring him; please arrange the visit through her at [[(919) 555-0178|phone]] or [[annika.vwb@mailhaven.example|email]]. He has Medicare Part B and a supplement, so no authorization is needed.
With thanks and kind regards,
[[Evangeline Papadakis-Stone|p2:full]], MD
NPI [[1205938847|govid:NPI]] / DEA [[BP4418827|govid:DEA registration number]]
'''))

# ---------------------------------------------------------------- doc 19
DOCS.append(D(19, "txt", "phone message", "health", "US", length="short",
  title="Phone message - prescription refill request",
  ents={"p1": "Dolores Ibarra", "p2": "Sunil Mehta", "p3": "Rudy Ibarra", "p4": "Kay", "o1": "Corner Drug"},
  distractors=["90-day"],
  body=r'''
PHONE MSG  [[2/18|date!:month/day only]]  3:55p  taken by [[Kay|p4:first-name]]

Pt [[Dolores Ibarra|p1:full]] (DOB [[4/30/52|dob!:two-digit year]]), chart [[44-1907|rec!:chart number that looks like a year]]. Needs refill of
[[lorazepam 0.5 mg|health:medication and dose]], out since Sat. Rx # [[7741206|rec:prescription number]] at [[Corner Drug|o1:full]], [[915-555-0183|phone]].
Says [[Dr. Mehta|p2:title-surname]] promised a 90-day supply. Sounded [[shaky and tearful|health!:observed mental state]]; husband
[[Rudy|p3:first-name]] in background. Call back on cell [[915 555 0106|phone!:spaces only]], NOT the home number.
'''))

# ---------------------------------------------------------------- doc 20
DOCS.append(D(20, "docx", "HR incident report", "general", "US",
  title="HR incident report - yard collision and harassment complaint",
  ents={"p1": "Malik Abdi-Rahman", "p2": "Travis Boone", "p3": "Guadalupe Santos", "p4": "Charlotte Dubois-Kim",
        "p5": "Wade Pruitt",
        "o1": "Ridgeline Building Supply, Inc.", "o2": "Truckee Meadows Urgent Care", "o3": "Sierra Crest Risk Partners"},
  distractors=["Policy 4.2", "OSHA 300 log", "Title VII", "Toyota Corolla", "Monday", "Section 7"],
  body=r'''
# [[Ridgeline Building Supply, Inc.|o1:full]]
## Confidential HR Incident Report
| Field | Entry |
| Report no. | [[HR-2026-011|rec:HR report number]] |
| Location | [[Sparks|place!:city name that is also a common word]] yard, [[1890 Glendale Avenue|addr]] |
| Incident date | [[Monday, February 9, 2026|date!:date with weekday]] |
| Reported by | [[Malik Abdi-Rahman|p1:full]], ID [[20418|rec!:short employee ID]] |
| Respondent | [[Travis Boone|p2:full]], ID [[17733|rec!:short employee ID]] |
| Investigator | [[Charlotte Dubois-Kim|p4:full]], HR Manager |
| Report date | [[2026-02-13|date:ISO format]] |
## Summary of the complaint
[[Mr. Abdi-Rahman|p1:title-surname]], a yard associate hired in [[June 2024|date!:month and year of hire]], reports that since December [[Mr. Boone|p2:title-surname]] (known in the yard as "[[T.J.|p2:initials]]") has made repeated remarks about his religion and background. [[Malik|p1:first-name]] is [[Muslim|attr:religion]] and uses his breaks to pray in the tool crib; he was [[born in Somalia|attr:national origin]] and became a [[U.S. citizen last year|attr!:citizenship status]]. He says [[Boone|p2:surname!]] has called the tool crib "the mosque," asked whether he was "legal," and on [[February 6|date!:month and day only]] left a printed cartoon taped to his locker (no. 31).
## The vehicle incident
At about 7:15 a.m. on the incident date, Boone reversed the company flatbed (unit 14, [[Nevada|place:state]] plate [[81C 447|veh!:license plate with a space]], VIN [[1FDUF5GT4KEC90213|veh:VIN]]) into Mr. Abdi-Rahman's parked Toyota Corolla (plate [[392-LMK|veh:license plate]]) while Malik was sitting in it. Boone says it was an accident and that he did not see the car. Malik believes it was deliberate. Damage to the Corolla is estimated at [[$2,840|money]]. Malik was seen the same morning at [[Truckee Meadows Urgent Care|o2:full]] for [[neck strain|health:injury]] and released to light duty; workers' compensation claim [[WC-NV-0226-5531|rec:workers' compensation claim number]] has been opened with [[Sierra Crest Risk Partners|o3:full]] and the injury entered on the OSHA 300 log.
Under Policy 4.2 Boone took a post-accident drug screen, which came back [[positive for THC|health!:drug test result]].
## Evidence gathered
- Statement of [[Guadalupe Santos|p3:full]] ("[[Lupe|p3:nickname]]"), forklift operator and [[shop steward|attr!:union role]], who heard the "legal" remark and saw the cartoon. She asked that her statement be shared with the union under Section 7 of the contract.
- Yard camera footage, 7:09 to 7:21 a.m., exported from the recorder (serial [[DVR-88A41F207|dev:video recorder serial number]]).
- Print log showing the cartoon was printed on February 6 at 6:52 a.m. from the dispatch laptop (asset tag [[RBS-LT-0462|dev:asset tag]], serial [[5CG9413XQ7|dev:laptop serial number]], IP [[10.20.4.117|ip:private IPv4]]) while signed in as [[tboone|cred:username]].
- Text messages provided by Malik from the number [[775-555-0124|phone]], which Boone confirms is his.
## Interim actions
Boone is suspended without pay pending the outcome. Yard supervisor [[Wade Pruitt|p5:full]] has been told to keep the two on separate shifts if Boone returns. [[Mr. Pruitt|p5:title-surname]] admitted that Malik raised the comments with him in January and that he "told them both to knock it off." That is a reporting failure in its own right and will be addressed separately. The conduct described may also raise Title VII concerns; outside counsel has been notified.
## Contact
[[C. Dubois-Kim|p4:short:initial + surname]], [[cdubois-kim@ridgelinesupply.example|email]], [[775.555.0160|phone:dotted]], ext. 204. Malik prefers contact by personal email, [[malik.ar@postmail.example|email]], not through the yard office.
'''))
