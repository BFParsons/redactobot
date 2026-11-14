from corpus3_src.core import D, dt, amt, num

DOCS = []

# ---------------------------------------------------------------- 341
DOCS.append(D(341, "pdf", "independent medical examination report", "health", "US",
  title="Independent medical examination summary in a longshore injury claim",
  ents={"p1": "Jacinta Olmedo-Varela", "p2": "Harlan B. Eichelberger", "p3": "Dr. Thuy-Vi Lam", "p4": "Reginald Fauntleroy",
        "o1": "Bulwark Casualty Insurance", "o2": "Pascagoula Shipfitters, Inc.", "o3": "Singing River Spine & Pain",
        "o4": "Eichelberger Orthopedic Evaluations, PLLC"},
  distractors=["AMA Guides, Sixth Edition", "33 U.S.C. § 907", "CPT 99456", "L4-L5", "Form LS-1", "Waddell signs"],
  body=r'''
# [[Eichelberger Orthopedic Evaluations, PLLC|o4:full]]
[[1200 Hardy Street, Suite 2B|addr:street with suite]], [[Hattiesburg|place:city]], [[Mississippi|place:state]] [[39401|zip]] · Tel. [[601-555-0125|phone]] · Fax [[601-555-0126|phone:fax]]
## INDEPENDENT MEDICAL EXAMINATION
- Examinee: [[Jacinta Olmedo-Varela|p1:full]] · Date of birth: [[07/22/1976|dob]] · Last four of SSN: [[5625|ssn:last four digits only]]
- Date of examination: [[November 4, 2025|date:examination date]] · Date of injury: [[January 16, 2025|date:date of injury]]
- Employer: [[Pascagoula Shipfitters, Inc.|o2:full]] · Carrier: [[Bulwark Casualty Insurance|o1:full]] · Claim no. [[BCI-LS-2025-004418|rec:insurance claim number]]
- Requested by: [[Reginald Fauntleroy|p4:full]], claims examiner, [[rfauntleroy@bulwarkcasualty.example|email]]
- Interpreter: none needed. The examinee was told that no doctor-patient relationship exists and that this report goes to the carrier.
## History given by the examinee
[[Ms. Olmedo-Varela|p1:title-surname]] is a 49-year-old pipefitter. She states that on [[January 16|date:month and day]] she was pulling a chain fall in a ship's engine room when she felt a "pop" in her low back. She finished the shift, reported it the next morning and was seen at the yard clinic. She has not worked since [[February 3|date:last day worked]]. She describes [[constant low back pain radiating down the left leg to the foot, with numbness in the great toe|health:symptoms]]. She rates it 7 out of 10.
She denies any earlier back injury. When I asked specifically about 2018, she agreed that she had [[a lumbar microdiscectomy at L5-S1 in 2018|health:prior surgery]] after a car accident, and said she "did not think that counted because it was the other side."
## Records reviewed
- [[Singing River Spine & Pain|o3:full]], [[Dr. Thuy-Vi Lam|p3:full]], notes of [[2/11/25|date:short numeric date]] through [[10/02/25|date:short numeric date]]; chart no. [[SR-118204|rec:chart number]]. Three epidural steroid injections (March, May and August).
- MRI lumbar spine, [[02/20/2025|date:imaging date]]: [[left paracentral disc extrusion at L4-L5 contacting the L5 nerve root|health:imaging finding]]; post-surgical change at L5-S1.
- Pharmacy printout: [[hydrocodone 10/325 four times daily since March, gabapentin 600 mg three times daily, duloxetine 60 mg|health:medications]].
- Form LS-1 authorizations and the employer's accident report.
## Examination
Height 5 ft 4 in, weight 171 lb. Gait antalgic on the left. Lumbar flexion limited to 40 degrees with pain. Straight leg raise positive on the left at 35 degrees, negative on the right. [[Weakness of left great-toe extension (4/5) and reduced sensation over the dorsum of the left foot|health:examination findings]]. Reflexes symmetric. Waddell signs: 1 of 5.
She became tearful when discussing work. She volunteered that she [[has been treated for depression since her divorce|health:mental health history]] and that [[she has been in recovery from alcohol for four years|health:addiction recovery]]. I note this because of the current opioid dose.
## Opinions
- 1. Diagnosis: [[left L5 radiculopathy due to L4-L5 disc extrusion|health:diagnosis]]. The findings are consistent with the mechanism described and are at a different level and side from the 2018 surgery.
- 2. Causation: more likely than not related to the January 16 work incident.
- 3. Maximum medical improvement: not reached. A surgical consultation is reasonable under 33 U.S.C. § 907.
- 4. Work status: sedentary duty only; no lifting over 10 lb.
- 5. If no surgery is performed, impairment under the AMA Guides, Sixth Edition would be [[12% of the whole person|health:impairment rating]].
- 6. I recommend that [[Dr. Lam|p3:title-surname]] taper the hydrocodone; [[the examinee has run out early twice according to the pharmacy record|health:medication use pattern]].
## Certification
I examined the examinee personally for 45 minutes. Fee for examination and report (CPT 99456): [[$1,850.00|money]]; no-show fee, had it applied, [[$600|money]].
[[Harlan B. Eichelberger|p2:full]], M.D., Board-certified orthopedic surgeon · Mississippi license no. [[18844|govid!:medical license number]] · NPI [[1447182209|govid:NPI]]
Dictated [[11/04/2025|date:dictation date]]; signed electronically [[11/07/2025|date:signature date]] · [[HBE|p2:initials]]:tm
'''))

# ---------------------------------------------------------------- 342
DOCS.append(D(342, "txt", "medical chronology", "health", "US", length="long",
  title="Nurse consultant's medical chronology in a delayed stroke diagnosis case",
  ents={"p1": "Vernon L. Applewhite", "p2": "Deborah Applewhite", "p3": "Dr. Cyrus Tehrani", "p4": "Kristof Nagy",
        "p5": "Dr. Folasade Akintola", "p6": "Dr. Marguerite Duchesne", "p7": "Gwendolyn Spratt", "p8": "Tucker Royce",
        "o1": "Saint Agnes Community Hospital", "o2": "Wabash Valley Neurology Group", "o3": "Sugar Creek Rehabilitation Hospital",
        "o4": "Spratt Legal Nurse Consulting", "o5": "Royce & Maldonado-Byrd, LLP"},
  distractors=["NIHSS", "CT head", "ICD-10 I63.9", "t-PA window"],
  body=r'''
MEDICAL CHRONOLOGY - ATTORNEY WORK PRODUCT
Prepared for: [[Tucker Royce|p8:full]], [[Royce & Maldonado-Byrd, LLP|o5:full]]            Firm file: [[RMB-24-0612|rec:firm file number]]
Prepared by: [[Gwendolyn Spratt|p7:full]], RN, BSN, LNCC, [[Spratt Legal Nurse Consulting|o4:full]]     Draft 2, [[11/09/2025|date:draft date]]
Patient: [[APPLEWHITE, Vernon L.|p1:last-first:surname in caps first]]     DOB: [[4/18/1967|dob]]     MRN ([[Saint Agnes|o1:short]]): [[SA-00771209|rec:medical record number]]
Records reviewed: Saint Agnes ED and inpatient (Bates [[APP-SA-000001|rec:Bates number]] to [[APP-SA-000412|rec:Bates number]]); EMS run report; [[Wabash Valley Neurology Group|o2:full]]; [[Sugar Creek Rehabilitation Hospital|o3:full]]; pharmacy; employer file.

BACKGROUND
[[Mr. Applewhite|p1:title-surname]], 57 at the time, a long-haul driver. Known history per primary care: [[hypertension, poorly controlled|health:chronic condition]]; [[atrial fibrillation diagnosed 2022, prescribed apixaban|health:diagnosis and medication]]; [[type 2 diabetes|health:chronic condition]]; [[smoker, one pack a day|health:tobacco use]]. Pharmacy fill history shows [[no apixaban refill after November 2023|health:medication non-adherence]] (he told his wife it cost too much after he lost insurance).

DATE / TIME        SOURCE (BATES)        EVENT                                                    COMMENT
-----------------------------------------------------------------------------------------------------------------
[[03/09/2024|date:first ED visit]]  21:47   EMS run report        Wife, [[Deborah Applewhite|p2:full]], calls 911 from home,              Onset time documented by EMS
                   ([[APP-EMS-0003|rec:Bates number]])        [[1127 Vigo Street|addr]], [[Terre Haute|place:city]] [[IN|place:state abbreviation]]. "Dizzy, can't walk               as "approx 21:15." This is
                                         straight, threw up twice." [[BP 198/112|health:vital sign]]. [[Glucose 164|health:lab value]].                the only clear onset time.
03/09/2024  22:31   ED triage             Triage RN [[Kristof Nagy|p4:full]]. Chief complaint entered as              No stroke scale done at
                   ([[APP-SA-000014|rec:Bates number]])       "vertigo / N&V." Triage level 3. No NIHSS recorded.                triage. Policy requires one.
03/09/2024  23:40   ED physician note     [[Dr. Cyrus Tehrani|p3:full]]. Exam: "[[nystagmus, unsteady gait|health:examination findings]], no             Did not document finger-to-
                   ([[APP-SA-000019-22|rec:Bates number]])    focal weakness." Impression: [[peripheral vertigo|health:working diagnosis]].                   nose, speech, or visual
                                         Orders: meclizine, ondansetron, IV fluids. CT head ordered.        fields. A-fib not mentioned.
[[3/10/24|date:short numeric date]]     00:52   Radiology             CT head without contrast: "no acute intracranial                   CT is insensitive for
                   ([[APP-SA-000031|rec:Bates number]])       abnormality." No CTA or MRI ordered.                               posterior strokes.
3/10/24     02:15   ED nursing note       "Pt states room still spinning, [[c/o double vision|health:symptom]]."                 NEW SYMPTOM. Not relayed to
                   ([[APP-SA-000027|rec:Bates number]])       [[RN Nagy|p4:title-surname:professional title + surname]]. No physician notified per the record.                the physician per the chart.
3/10/24     03:05   Discharge             Discharged home with meclizine. Dx: vertigo (not coded as          Discharged 5 h 50 min after
                   ([[APP-SA-000033|rec:Bates number]])       stroke). Instructions: follow up with PCP in 3 days.               onset; inside any extended
                                         [[Mrs. Applewhite|p2:title-surname]] signed; pt "too dizzy to sign."                  window for evaluation.
[[March 10, 2024|date:second ED visit]]  11:20   EMS / ED (second visit)   Found on bathroom floor by wife. [[Slurred speech, left facial droop, cannot swallow|health:symptoms]].
                   ([[APP-SA-000040|rec:Bates number]])       [[NIHSS 14|health:stroke scale score]] on arrival. 17 hours after first triage.
3/10/24     12:02   MRI brain             [[Acute infarct, left cerebellum and lateral medulla; basilar artery thrombus|health:imaging finding]].
                   ([[APP-SA-000058|rec:Bates number]])       Posterior circulation stroke. ICD-10 I63.9 used.
3/10/24     12:40   Neurology consult     [[Dr. Folasade Akintola|p5:full]] ([[Wabash Valley Neurology|o2:short]]). "Outside            Her note is the key
                   ([[APP-SA-000061-64|rec:Bates number]])    t-PA window.         causation document.
                                         [[Presentation last night was, in retrospect, a posterior circulation event|health:retrospective diagnosis]]." Transferred to ICU.
[[3/10|date:month/day only]] - [[3/29/24|date:short numeric date]]      Inpatient             ICU 6 days. [[PEG tube placed 3/14|health:procedure]]. [[Aspiration pneumonia 3/17|health:complication]].      19-day admission. Charges
                   ([[APP-SA-000070-398|rec:Bates number]])   Speech, PT, OT daily.                                              [[$214,880.16|money]].
[[29 Mar 2024|date:day, abbreviated month, year]] -       [[Sugar Creek Rehab|o3:short]]   Inpatient rehabilitation under [[Dr. Marguerite Duchesne|p6:full]].              Rehab charges [[$96,412.00|money]].
[[May 17, 2024|date:rehab discharge date]]       ([[APP-SC-0001-0220|rec:Bates number]])    Discharge status: 
                                         [[wheelchair for distance, walker in home, pureed diet, persistent double vision, left-sided ataxia|health:functional status]].
[[Sept. 2024|date:abbreviated month and year]]          Neurology follow-up   [[Dr. Akintola|p5:title-surname]]: "plateaued." [[Depression, started sertraline|health:diagnosis and medication]].          Permanent restrictions.
                   ([[APP-WV-0012|rec:Bates number]])         Cannot return to commercial driving; CDL medical card
                                         surrendered.
[[10/2024|date:month/year]]            Employer file         Terminated after exhausting leave. Last gross annual pay           Lost earnings base.
                                         [[$71,340|money]]. Applied for SSDI; [[awarded effective September 2024|attr:disability benefit status]],
                                         [[$2,214|money]] per month.

NURSE CONSULTANT'S OBSERVATIONS (not opinions on the standard of care)
1. No stroke scale at either triage or physician evaluation on the first visit, despite vomiting, gait instability, severe hypertension and a charted history of atrial fibrillation in the hospital's own prior records (visit of [[8/2/2022|date:earlier visit date]], [[APP-SA-000405|rec:Bates number]]).
2. The 02:15 nursing note of new double vision was not escalated. [[Mr. Nagy|p4:title-surname]] was a travel nurse on his third shift at the facility; ask for his orientation file.
3. [[Dr. Tehrani|p3:title-surname]] was covering the ED alone with 31 patients on the board at 23:00 per the tracking log ([[APP-SA-000409|rec:Bates number]]).
4. Defense will raise the stopped apixaban and the smoking. Note also one prior ED visit ([[12/31/2023|date:earlier visit date]]) where the chart records "[[ETOH on breath|health:alcohol use noted in chart]]"; nothing similar on [[3/9|date:month/day only]].
5. Missing: audit trail for the triage record; I count two edits on 3/10 after the second arrival. Request metadata.

Client contact for questions on home care: [[Deborah|p2:first-name]], [[812-555-0146|phone]] (she works nights at the candle factory; call before 2 pm).
Invoice for this draft: 14.5 hours at [[$165|money:hourly rate]] = [[$2,392.50|money]].   [[G. Spratt|p7:short:initial + surname]]
'''))

# ---------------------------------------------------------------- 343
DOCS.append(D(343, "docx", "property insurance claim file notes", "legal", "US", cardholders=["p2"],
  title="Public adjuster's file notes on a residential burglary claim",
  ents={"p1": "Ignatius Okwuchukwu", "p2": "Marisol Okwuchukwu", "p3": "Desmond Tarleton", "p4": "Det. Aubrey Stiles",
        "p5": "Shelby Rae Linton", "p6": "Terrell Okwuchukwu",
        "o1": "Linton Public Adjusters, Inc.", "o2": "Hearthstone Mutual Insurance Co.", "o3": "Wexler Pawn & Loan"},
  distractors=["HO-3", "Coverage C", "Mo. Rev. Stat. § 375.1007", "examination under oath", "Xactimate"],
  header="[[Linton Public Adjusters, Inc.|o1:full]] — claim file [[LPA-25-0418|rec:adjuster file number]]",
  body=r'''
# Claim file notes — [[Okwuchukwu|p1:surname]] burglary
Insureds: [[Ignatius Okwuchukwu|p1:full]] and [[Marisol Okwuchukwu|p2:full]] · Loss location: [[7218 Pershing Avenue|addr]], [[University City|place:city]], [[MO|place:state abbreviation]] [[63130|zip]]
Carrier: [[Hearthstone Mutual Insurance Co.|o2:full]] · HO-3 policy [[HM-MO-7720418-03|rec:policy number]] · Claim [[25-HM-0091844|rec:insurance claim number]] · Carrier adjuster: [[Desmond Tarleton|p3:full]], [[314-555-0152|phone]]
Date of loss: between [[Oct. 17|date:abbreviated month and day]] and [[Oct. 19, 2025|date:abbreviated month, day and year]] (family was away at a wedding in [[Kansas City|place:city]])
Police: [[University City|place:city]] PD report no. [[25-044187|rec:police report number]], [[Det. Aubrey Stiles|p4:full:with rank]]
## Summary
Back door forced. Electronics, jewelry and a car taken from the detached garage. Claim was reported online by [[Mrs. Okwuchukwu|p2:title-surname]] on [[10/20/2025|date:report date]] at 7:14 a.m.; the carrier's portal log shows the submission came from IP [[198.51.100.203|ip]], which is the house's own connection. [[Mr. Tarleton|p3:title-surname]] seems to think that is suspicious. It is not; they were home by then.
## Contents schedule (Coverage C) — serial numbers supplied by the insureds
| Item | Identifier | Claimed |
| MacBook Pro 16-inch (2023) | Serial [[C02GK4418MD6|dev:laptop serial number]] | [[$2,899|money]] |
| iPad Air | Serial [[DMPZ7720Q1GC|dev:tablet serial number]] | [[$749|money]] |
| Sony a7 IV camera body | Serial [[4418827|dev!:camera serial number, digits only]] | [[$2,498|money]] |
| Samsung phone (old, in a drawer) | IMEI [[355178095580069|dev:IMEI]] | [[$350|money]] |
| Engagement ring, appraised 2021 | Appraisal no. [[GIA-2204418772|rec:gem grading report number]] | [[$11,400|money]] |
| Cash in a desk drawer | — | [[$1,200|money]] (policy limit is [[$200|money]]) |
## Vehicle (reported to the auto carrier separately)
2022 Kia Telluride, VIN [[5XYP5DHC4NG204418|veh:VIN]], [[Missouri|place:state]] plate [[RM4 K7T|veh:license plate]]. Keys were on a hook by the back door. Recovered [[10/26|date:month/day only]] in [[East St. Louis|place:city]] with the catalytic converter cut off.
## Card fraud after the burglary
A wallet was in the kitchen. [[Marisol|p2:first-name]]'s Visa ending [[2996|card:last four of card]] was used three times on [[10/18|date:month/day only]] ([[$412.77|money]] total) before the bank froze it; her debit card [[4769 15•• •••• 2996|card:partly masked card number]] was not used. Expiry on both was [[08/27|exp]]. Not part of this claim, but it helps fix the time of the break-in.
## Problems
- The carrier has asked for an examination under oath of both insureds on [[December 3|date:examination date]]. Their letter cites "financial motive": [[the mortgage is three months in arrears and a foreclosure notice was sent in September|attr:financial distress]]. [[Ignatius|p1:first-name]] says [[he lost his job at the brewery in June|indirect:job loss at an identifiable employer]] and they are catching up.
- A pawn ticket: [[Det. Stiles|p4:title-surname:rank + surname]] found the camera at [[Wexler Pawn & Loan|o3:full]] on [[Natural Bridge Road|addr!:street name only, no number]], pawned [[10/19|date:month/day only]] under ticket [[WX-118204|rec:pawn ticket number]] by a man who gave the name [[Terrell Okwuchukwu|p6:full]]. That is [[the insureds' 19-year-old nephew, who has a key|indirect:relative with access to the home]]. They have not told the carrier. I advised them they must, and that I cannot continue if they do not.
- Prior claims: water damage 2019 ([[$8,300|money]] paid), nothing else.
## Fee and next steps
Contract signed [[10/22/2025|date:contract date]]: 10% of recovery, capped per Mo. Rev. Stat. § 375.1007. Estimate being rebuilt in Xactimate for the door and frame. Call both insureds [[Thursday the 13th|date:weekday and day of month]] — his cell [[314.555.0191|phone:dotted]], hers [[(314) 555-0107|phone]], or [[marisol.okw@gatewaymail.example|email]].
[[Shelby Rae Linton|p5:full]], licensed public adjuster, Mo. license [[PA-8844172|govid:public adjuster license number]] — [[SRL|p5:initials]]
'''))

# ---------------------------------------------------------------- 344
DOCS.append(D(344, "eml", "medical records request email", "health", "US", enc="qp",
  title="Daughter's records request for her 94-year-old mother, copied to counsel",
  ents={"p1": "Evangeline Rasmussen", "p2": "Astrid Rasmussen-Kehoe", "p3": "Lionel Stenberg", "p4": "Dr. Pinto",
        "o1": "Lakewood Shores Skilled Nursing", "o2": "Gitchi Gami Regional Medical Center"},
  distractors=["45 CFR 164.524", "HIPAA", "Minn. Stat. § 144.292"],
  headers={"From": "[[Astrid Rasmussen-Kehoe|p2:full]] <[[astrid.rk@northshoremail.example|email]]>",
           "To": "Release of Information <[[roi@gitchigamirmc.example|email]]>",
           "Cc": "[[lstenberg@stenberglaw.example|email]]",
           "Subject": "Records request - patient [[Evangeline Rasmussen|p1:full]], MRN [[4418-77-209|rec:medical record number]]",
           "Date": "Sat, [[8 Nov 2025|date:email header date]] 10:05:31 -0600"},
  body=r'''
To the Release of Information office at [[Gitchi Gami Regional Medical Center|o2:full]]:

I am the daughter and health care agent of your patient [[Evangeline Rasmussen|p1:full]] (maiden name [[Solheim-Berge|p1:surname:maiden name]]). My mother is [[94 years old|age:age with unit]] and cannot make this request herself. The signed authorization and my health care directive are attached. I am asking under HIPAA, 45 CFR 164.524, and Minn. Stat. § 144.292.

Patient: [[Evangeline M. Rasmussen|p1:full:with middle initial]]
Date of birth: [[May 2, 1931|dob]]
MRN: [[4418-77-209|rec:medical record number]]
Medicare no.: [[2KM9-WD4-TX18|govid:Medicare beneficiary identifier]]
Home before the nursing home: [[4406 London Road|addr]], [[Duluth|place:city]], [[MN|place:state abbreviation]] [[55804|zip]]

Please send, in electronic form:
1. The complete chart for the admission of [[September 22|date:admission date]] to [[October 9, 2025|date:discharge date]], when she came to you by ambulance from [[Lakewood Shores Skilled Nursing|o1:full]] with [[a stage 4 pressure wound on her tailbone and sepsis|health:condition on admission]].
2. The wound care photographs and the nursing skin assessments.
3. [[Dr. Pinto|p4:title-surname]]'s surgical notes from the [[debridement on September 24|health:procedure]].
4. The billing record. We received a statement for [[$48,216.40|money]] and do not understand it.

I'd also like the emergency department record from [[July 30|date:earlier visit date]], when she was seen after [[a fall at the nursing home|health:earlier injury]] and sent back the same night.

Please email the records to me and to our attorney, [[Lionel Stenberg|p3:full]] (copied). If there is a charge above the [[$6.50|money]] flat fee, call me first: [[218-555-0138|phone]]. Do not mail anything to [[Lakewood Shores|o1:short]]; my mother is no longer there and [[we have filed a complaint against them with the state|indirect:pending complaint against a named facility]].

She is now with me at [[212 Arrowhead Trail|addr]], [[Two Harbors|place:town]], MN [[55616|zip]], [[on hospice care|health:hospice status]], so time matters.

Thank you,
[[Astrid|p2:first-name]]
'''))

# ---------------------------------------------------------------- 345
DOCS.append(D(345, "html", "walk-in clinic patient registration", "health", "CA", raw_html=True, minors=["p1"], cardholders=["p2"],
  title="Walk-in clinic registration for a child, with an uninsured-service payment",
  ents={"p1": "Zainab Olawale-Fitzpatrick", "p2": "Nuala Fitzpatrick", "p3": "Babatunde Olawale", "p4": "Dr. Henrik Sandahl",
        "o1": "Glebe Walk-In & Family Clinic", "o2": "Bank Street Pharmasave", "o3": "Hopewell Avenue Public School"},
  distractors=["OHIP", "MedFlow Kiosk v3.8", "A007"],
  body=r'''<!DOCTYPE html>
<html lang="en-CA"><head><meta charset="utf-8"><title>Registration summary</title>
<style>dl{display:grid;grid-template-columns:14em auto} dt{font-weight:bold} .warn{color:#a00}</style></head>
<body>
<h1>[[Glebe Walk-In & Family Clinic|o1:full]]</h1>
<p>[[788 Bank Street|addr]], [[Ottawa|place:city]], [[Ontario|place:province]] [[K1S 3V8|zip:Canadian postal code]] &middot; [[613-555-0150|phone]] &middot; MedFlow Kiosk v3.8 &middot; printed [[2025-11-08|date:ISO date]] 09:42</p>
<h2>Patient</h2>
<dl>
<dt>Name</dt><dd>[[Zainab Olawale-Fitzpatrick|p1:full]] (goes by &ldquo;[[Zee|p1:nickname]]&rdquo;)</dd>
<dt>Date of birth</dt><dd>[[2014-03-27|dob:ISO date]] (age 11)</dd>
<dt>Health card (OHIP)</dt><dd>[[2204-418-772-ZK|govid:Ontario health card number with version code]], expires [[2027-03-27|date:health card expiry]]</dd>
<dt>Address</dt><dd>[[41 Monkland Avenue|addr]], Ottawa [[ON|place:province abbreviation]] [[K1S 1Y8|zip:Canadian postal code]]</dd>
<dt>School</dt><dd>[[Hopewell Avenue Public School|o3:full]], [[Grade 6|indirect:school grade of a child]]</dd>
<dt>Family doctor</dt><dd>[[Dr. Henrik Sandahl|p4:full]] (not accepting same-day visits)</dd>
<dt>Pharmacy</dt><dd>[[Bank Street Pharmasave|o2:full]], fax [[613-555-0151|phone:fax]]</dd>
</dl>
<h2>Parent / guardian completing this form</h2>
<dl>
<dt>Name</dt><dd>[[Nuala Fitzpatrick|p2:full]] (mother)</dd>
<dt>Cell</dt><dd>[[613 555 0177|phone:spaces only]]</dd>
<dt>Email</dt><dd>[[nuala.fitz@rideaumail.example|email]]</dd>
<dt>Other parent</dt><dd>[[Babatunde Olawale|p3:full]], [[343-555-0108|phone]]. <span class="warn">[[Custody order: father may attend appointments but may not pick up the child from the clinic|attr:court order concerning a child]].</span></dd>
</dl>
<h2>Reason for visit and history</h2>
<p>[[Sore throat and fever for three days; rash on chest since last night|health:presenting symptoms]].</p>
<ul>
<li>Allergies: [[penicillin (hives)|health:drug allergy]]; [[peanuts, carries an EpiPen|health:allergy and device]]</li>
<li>Regular medications: [[methylphenidate 18 mg every morning|health:medication]]</li>
<li>Conditions: [[ADHD|health:diagnosis]]; [[asthma, last hospital visit two winters ago|health:condition]]</li>
<li>Immunizations up to date: yes (yellow card seen)</li>
</ul>
<h2>Uninsured service</h2>
<p>A school sports form was also requested. This is not covered by OHIP. Fee [[$40.00|money]], paid at the kiosk:</p>
<table>
<tr><td>Cardholder</td><td>[[NUALA M FITZPATRICK|p2:caps:name as embossed on a card]]</td></tr>
<tr><td>Card</td><td>Mastercard [[5171 0247 6506 2270|card]]</td></tr>
<tr><td>Expiry</td><td>[[06/29|exp]]</td></tr>
<tr><td>CVC entered</td><td>[[614|cvv]]</td></tr>
<tr><td>Authorization</td><td>[[A-771209|rec:card authorization code]], receipt no. [[GW-0044187|rec:receipt number]]</td></tr>
</table>
<p class="warn">Kiosk fault: full card details were printed on this summary. Shred after billing code A007 is submitted. &mdash; front desk</p>
<p>Seen by the nurse at 10:05. Rapid strep: [[positive|health!:strep test result]]. Prescription sent to the pharmacy above (not a penicillin). [[Zainab|p1:first-name]] to stay home from school until [[Tuesday, Nov. 11|date:weekday, abbreviated month and day]].</p>
</body></html>
'''))

# ---------------------------------------------------------------- 346
DOCS.append(D(346, "txt", "recorded statement summary", "legal", "US", minors=["p2", "p3"],
  title="Auto claims adjuster's summary of an insured's recorded statement",
  ents={"p1": "Marguerite Yoshioka", "p2": "Clayton Deveraux", "p3": "Trinity Deveraux", "p4": "Anders Folkestad",
        "p5": "Ofc. Pruneau",
        "o1": "Slickrock Insurance Exchange", "o2": "Jordan Narrows Towing & Recovery", "o3": "Beehive State Farm Bureau Mutual"},
  distractors=["Utah Code § 31A-22-309", "PIP", "Form DI-9", "CCC ONE"],
  body=r'''
[[SLICKROCK INSURANCE EXCHANGE|o1:caps]] - CLAIM NOTES (recorded statement summary; audio on file 14 min 08 sec)
Claim #: [[CR-AU-25-1184207|rec:insurance claim number]]     Policy: [[UT-PA-004418772|rec:policy number]]     DOL: [[11/01/2025|date:date of loss]] approx 5:40 PM
Adjuster: [[Anders Folkestad|p4:full]], ext [[4418|phone!:internal extension only]]            Statement taken [[11/03/2025|date:statement date]] by phone

NAMED INSURED / DRIVER
[[Marguerite Yoshioka|p1:full]], DOB [[10-12-1959|dob:hyphenated numeric]], UT DL [[188441720|govid:driver license number]]
[[2931 South 2300 East|addr:Utah grid-style address]], [[Millcreek|place:city]], [[UT|place:state abbreviation]] [[84109|zip]]. Cell [[801-555-0165|phone]]. Prefers "[[Peggy|p1:nickname]]".
IV: 2020 Subaru Outback, VIN [[4S4BTACC8L3204418|veh:VIN]], plate [[F18 4KT|veh:license plate]]. Lienholder none.
Plug-in telematics device on this vehicle, serial [[CRX-7720-4418-B|dev:telematics device serial number]] (trip data requested).

OTHER PARTY
Driver [[Clayton Deveraux|p2:full]], age 17 per police report, permit/DL [[204418772|govid:driver license number]]. Passenger: his sister [[Trinity Deveraux|p3:full]], age 14.
CV: 2011 Chevy Silverado, plate [[9KT 418|veh:license plate]], VIN ending [[...G1187204|veh:partial VIN]], owned by the father. Carrier per exchange slip: [[Beehive State Farm Bureau Mutual|o3:full]], policy [[BFB-0091844-A|rec:policy number]].

INSURED'S VERSION
[[Peggy|p1:nickname]] was northbound on [[2300 East|addr!:street name only, grid style]] going home from a hair appointment. Light at [[3300 South|addr!:street name only, grid style]] was green for her. CV turned left across her lane from the southbound turn pocket. She braked, hit CV at the right rear wheel. Est. her speed 30 to 35. Dry, dusk, headlights on.
She says the other driver got out and said "I'm so sorry, I thought I could make it." His sister was crying and holding her arm.
Police: Unified PD, [[Ofc. Pruneau|p5:title-surname:abbreviated rank + surname]], case no. [[UP-25-204418|rec:police case number]]. Other driver cited for failure to yield (she saw the officer hand him the ticket). Form DI-9 exchange slip in file.
Witness: none she knows of. A man from the tire shop on the corner brought out a chair for her.

INJURIES
Insured: [[seat belt bruising across the chest, sore neck, left knee hit the dash|health:injuries]]. Went to urgent care that evening; x-rays negative. She mentioned she [[had a knee replacement on that side in 2021|health:prior surgery]] and is worried about it. [[On blood thinners|health:medication]], so the bruising is extensive. PIP opened under Utah Code § 31A-22-309; med pay limit [[$5,000|money]].
Other vehicle: she believes the girl was taken by ambulance. Nothing confirmed. Both are minors, so contact goes through the parents only.

VEHICLE
IV towed by [[Jordan Narrows Towing & Recovery|o2:full]] to their yard, [[1450 West 2100 South|addr:Utah grid-style address]], [[Salt Lake City|place:city]]. Tow invoice [[WF-118204|rec:tow invoice number]], [[$285|money]] plus [[$45|money]] a day storage. Move it by [[11/5|date:month/day only]]. CCC ONE estimate pending; likely total loss, ACV range [[$19,500|money]] to [[$21,000|money]]. Deductible [[$500|money]].
Rental authorized 30 days at [[$40|money]]/day.

OTHER
- Insured asked whether her rates go up. Told her that is underwriting's call; liability looks 100% adverse.
- She [[lives alone and does not drive at night since her cataract surgery|indirect:living situation and health-related habit]]; her son in [[Boise|place:city]] handles her email: [[yoshioka.kenji.r@treasurevalleymail.example|email]]. OK to copy him per her verbal consent on the recording at 11:20.
- Subro: put [[Beehive|o3:short]] on notice today.     [[AF|p4:initials]]
'''))

# ---------------------------------------------------------------- 347
DOCS.append(D(347, "xlsx", "medical billing ledger and lien sheet", "health", "US", minors=["p2"], cardholders=["p3"],
  title="Chiropractic and physical therapy billing ledger for personal injury patients",
  ents={"p1": "Florentino Abarca-Luna", "p2": "Kaylee Stavropoulos", "p3": "Despina Stavropoulos", "p4": "Wilhelmina Oduro",
        "p5": "Dr. Garth Ollerenshaw",
        "o1": "Ollerenshaw Spine & Sport, P.C.", "o2": "Bascom & Teague Injury Lawyers", "o3": "Pinebluff Indemnity Company",
        "o4": "Ridgeback Auto Insurance"},
  distractors=["98941", "97110", "97140", "99203"],
  sheets=[
    ("Patients", [
      ["Acct", "Patient", "DOB", "DOI", "Attorney / payer", "Claim no.", "Adjuster / contact", "Notes"],
      ["[[OSS-20441|rec:patient account number]]", "[[Abarca-Luna, Florentino|p1:last-first]]", dt("1985-06-08", "mm/dd/yyyy", "dob"), dt("2025-08-14", "mm/dd/yyyy", "date:date of injury"), "[[Bascom & Teague Injury Lawyers|o2:full]] (lien signed)", "[[PIC-25-0077412|rec:insurance claim number]] ([[Pinebluff Indemnity Company|o3:full]])", "paralegal [[910-555-0113|phone]]", "[[whiplash, lumbar strain|health:diagnosis]]; [[needs Spanish interpreter|attr:language indicating national origin]]; [[no health insurance|attr:insurance / financial status]]"],
      ["[[OSS-20457|rec:patient account number]]", "[[Stavropoulos, Kaylee|p2:last-first]]", dt("2010-11-30", "mm/dd/yyyy", "dob"), dt("2025-09-02", "mm/dd/yyyy", "date:date of injury"), "Med-pay, [[Ridgeback Auto Insurance|o4:full]]", "[[RB-MP-204418|rec:insurance claim number]]", "mother, [[Despina Stavropoulos|p3:full]], [[910-555-0186|phone]]", "[[concussion follow-up, neck pain|health:diagnosis]]; cheer team; school note needed; mom pays copays by card"],
      ["[[OSS-20463|rec:patient account number]]", "[[Oduro, Wilhelmina|p4:last-first]]", dt("1948-02-19", "mm/dd/yyyy", "dob"), dt("2025-09-21", "mm/dd/yyyy", "date:date of injury"), "Medicare primary, [[Bascom & Teague|o2:short]] lien secondary", "Medicare no. [[8NV2-KF6-QH40|govid:Medicare beneficiary identifier]]", "self, [[9105550129|phone:no separators]]", "[[fall on bus; rotator cuff tear, osteoporosis|health:diagnosis]]; [[lives at the Azalea Court assisted living|indirect:residence in a named facility]]"],
    ]),
    ("Ledger", [
      ["DOS", "Acct", "Patient", "CPT", "Description", "Charge", "Ins paid", "Pt paid", "Adj", "Balance"],
      [dt("2025-08-18", "m/d/yy"), "OSS-20441", "[[F. Abarca-Luna|p1:short:initial + surname]]", "99203", "New patient exam", amt(245.00), "", "", "", amt(245.00, "usd", None)],
      [dt("2025-08-20", "m/d/yy"), "OSS-20441", "[[Florentino|p1:first-name]]", "98941", "Adjustment 3-4 regions", amt(85.00), "", "", "", amt(85.00, "usd", None)],
      [dt("2025-08-27", "m/d/yy"), "OSS-20441", "Florentino", "97110", "Therapeutic exercise x2", amt(120.00), "", "", "", amt(120.00, "usd", None)],
      [dt("2025-09-04", "m/d/yy"), "OSS-20457", "[[Kaylee S.|p2:short:first name + surname initial]]", "99203", "New patient exam (minor, parent present)", amt(245.00, "usd", None), amt(196.00), amt(40.00), amt(-9.00, "acct"), amt(0.00, "usd", None)],
      [dt("2025-09-11", "m/d/yy"), "OSS-20457", "[[Kaylee|p2:first-name]]", "97140", "Manual therapy", amt(95.00), amt(76.00), amt(19.00), "", amt(0.00, "usd", None)],
      [dt("2025-09-24", "m/d/yy"), "OSS-20463", "[[W. Oduro|p4:short:initial + surname]]", "99203", "New patient exam", amt(245.00, "usd", None), amt(118.42), "", amt(-96.98, "acct"), amt(29.60)],
      [dt("2025-10-01", "m/d/yy"), "OSS-20463", "[[Mrs. Oduro|p4:title-surname]]", "97110", "Therapeutic exercise x2", amt(120.00, "usd", None), amt(58.10), "", amt(-47.38, "acct"), amt(14.52)],
      ["", "", "", "", "TOTAL OPEN", "", "", "", "", amt(494.12)],
    ]),
    ("Payments", [
      ["Date", "Acct", "From", "Method", "Ref", "Amount", "Posted by"],
      [dt("2025-09-04", "m/d/yy"), "OSS-20457", "[[D. Stavropoulos|p3:short:initial + surname]]", "Visa ending [[5466|card:last four of card]], exp [[02/28|exp]]", "auth [[07741B|rec:card authorization code]]", amt(40.00, "usd", None), "front"],
      [dt("2025-09-11", "m/d/yy"), "OSS-20457", "[[Despina|p3:first-name]]", "card on file [[4693-6240-8778-5466|card:full number with hyphens]]", "auth [[09912C|rec:card authorization code]]", amt(19.00, "usd", None), "front"],
      [dt("2025-10-15", "m/d/yy"), "OSS-20457", "Ridgeback Auto Insurance", "check [[0044187|rec!:check number]]", "EOB [[RB-E-771209|rec:explanation of benefits number]]", amt(272.00), "billing"],
      [dt("2025-10-28", "m/d/yy"), "OSS-20463", "Medicare", "EFT", "trace [[881204417720|rec!:EFT trace number]]", amt(176.52), "billing"],
      ["Lien balance letter to Bascom & Teague for OSS-20441 due", dt("2025-11-14", "mmmm d, yyyy", "date:deadline"), "", "", "", amt(450.00), "[[Dr. Ollerenshaw|p5:title-surname]] to sign"],
      ["Practice", "[[Ollerenshaw Spine & Sport, P.C.|o1:full]]", "Tax ID", "[[56-4418720|taxid:EIN]]", "NPI", "[[1881204417|govid:NPI]]", "[[Dr. Garth Ollerenshaw|p5:full]]"],
    ]),
  ]))

# ---------------------------------------------------------------- 348
DOCS.append(D(348, "txt", "medico-legal report letter", "health", "UK",
  title="UK consultant's medico-legal report letter to solicitors",
  ents={"p1": "Alasdair Kinnaird", "p2": "Mr Jonty Featherby", "p3": "Dr Meera Sivanesan", "p4": "Harriet Dowling",
        "o1": "Dowling Skerrett Solicitors", "o2": "Solway Aggregates Ltd", "o3": "Border City Orthopaedic Chambers",
        "o4": "Eden Vale Surgery"},
  distractors=["CPR Part 35", "Judicial College Guidelines", "GMC", "RIDDOR"],
  body=r'''
[[Border City Orthopaedic Chambers|o3:full]]
[[12 Portland Square|addr]], [[Carlisle|place:city]] [[CA1 1PT|zip:UK postcode]]
Tel [[01632 960175|phone:UK landline]]

PRIVATE AND CONFIDENTIAL - MEDICO-LEGAL REPORT
[[10th November 2025|date:ordinal day, month, year]]

[[Dowling Skerrett Solicitors|o1:full]]
For the attention of [[Ms Harriet Dowling|p4:full:with honorific]]
Your ref: [[HD/KIN/004418|rec:solicitor file reference]]          Our ref: [[JF/25/1187|rec:consultant file reference]]

Dear Sirs,

Re: [[Mr Alasdair Kinnaird|p1:full:with honorific]], d.o.b. [[14/06/1982|dob:day-first numeric]]
    [[23 Scotby Gardens|addr]], [[Wetheral|place:village]], Carlisle [[CA4 8HD|zip:UK postcode]]
    NHS no. [[441 877 2093|govid:NHS number]]
    Accident at work on [[19 February 2025|date:accident date]]

Thank you for your instructions. I examined [[Mr Kinnaird|p1:title-surname]] on [[4.11.25|date:dotted day-first short date]] for 50 minutes and have read his GP records from [[Eden Vale Surgery|o4:full]] ([[Dr Meera Sivanesan|p3:full]]), the hospital notes and the employer's RIDDOR report. This report is addressed to the Court and complies with CPR Part 35.

1. The accident. Mr Kinnaird, a quarry plant operator with [[Solway Aggregates Ltd|o2:full]] for nine years, was struck on the right shoulder and thrown from an access platform when a conveyor guard gave way. He fell about 2.5 metres.

2. Injuries. He sustained [[a displaced fracture of the right clavicle, treated by plate fixation on 21 February|health:injury and surgery]], [[fractures of the 6th to 8th right ribs|health:injury]] and [[a scaphoid fracture of the right wrist that was not identified until April|health:injury with delayed diagnosis]]. He is right-handed.

3. Progress. The clavicle has united. The scaphoid went on to non-union and he had [[a bone graft and screw fixation on 2 July 2025|health:surgery]]. He remains off work. He takes [[co-codamol 30/500 up to eight a day and amitriptyline 25 mg at night|health:medications]].

4. Past history. The GP records show [[an episode of low mood in 2019 following the death of his father, treated with citalopram for six months|health:mental health history]], and attendances for [[gout|health:condition]]. Nothing relevant to the right arm. He told me he drinks "four or five pints most nights since the accident"; his GP recorded [[alcohol intake of 50 units a week in September|health:alcohol use]] and has referred him to the community service. I mention this because it bears on the bone healing and on the prognosis.

5. Present complaints. Pain and stiffness at the wrist; cannot grip a spanner; wakes most nights. He is [[anxious about money, having moved onto Universal Credit in August|attr:benefits status]], and [[his partner is expecting their third child in January|indirect:family circumstances]].

6. Examination. Healed 11 cm scar over the clavicle. Shoulder movements full. Right wrist: flexion 30 degrees, extension 25 (left 70/70). Grip strength 14 kg right, 46 kg left.

7. Opinion and prognosis. On the balance of probabilities all three fractures were caused by the index accident. The delay in diagnosing the scaphoid fracture has, in my opinion, materially worsened the outcome; you may wish to take separate advice on that. I expect permanent loss of about half of wrist movement. He will not return to plant operation. There is a 20 to 25 per cent risk of wrist arthritis requiring fusion within 15 years, at a present-day private cost of about [[£9,500|money:pounds]].

8. I would place the wrist injury within the "significant permanent disability" bracket of the Judicial College Guidelines.

My fee for this report is [[£1,150.00|money:pounds]] plus VAT, invoice [[BC-25-0418|rec:invoice number]] enclosed; payment by BACS to sort code [[20-18-44|rtn:UK sort code]], account [[77204418|acct:UK account number]].

Yours faithfully,

[[Mr Jonty Featherby|p2:full:surgeon's honorific]] FRCS (Tr & Orth)
Consultant Orthopaedic and Hand Surgeon          GMC no. [[4418772|govid!:GMC registration number]]
[[j.featherby@bordercityortho.example|email]]
'''))

# ---------------------------------------------------------------- 349
DOCS.append(D(349, "pptx", "mediation brief deck", "legal", "US",
  title="Plaintiffs' mediation presentation in a nursing home wrongful death case, with speaker notes",
  ents={"p1": "Philomena Guarnieri", "p2": "Rosemarie Guarnieri-Platt", "p3": "Dominic Guarnieri", "p4": "Hon. Leland Mabry",
        "p5": "Dr. Shirin Vossoughi", "p6": "Odell Farrier",
        "o1": "Heron Pointe Care Center", "o2": "Farrier Nettles Trial Group", "o3": "Altamaha Senior Holdings, LLC",
        "o4": "Coastal Empire Assurance"},
  distractors=["42 CFR § 483.25", "F-tag 686", "Braden Scale", "O.C.G.A. § 51-4-2", "CMS Form 2567"],
  body=r'''
# Estate of [[Philomena Guarnieri|p1:full]] v. [[Heron Pointe Care Center|o1:full]]
- Mediation before [[Hon. Leland Mabry|p4:full:with judicial honorific]] (Ret.) — [[November 19, 2025|date:mediation date]]
- Civil Action No. [[STCV24-01187|rec:civil action number]], State Court of [[Chatham County|place:county]]
- [[Farrier Nettles Trial Group|o2:full]] for the plaintiffs — CONFIDENTIAL SETTLEMENT COMMUNICATION
> Open with the photograph of [[Mrs. Guarnieri|p1:title-surname]] at her [[95th birthday|age:age implied by a birthday]]. Do not show the wound photos until slide 4. [[Rosemarie|p2:first-name]] will step out for that slide.
# Who she was
- Born [[December 8, 1927|dob]] in [[Savannah|place:city]]; seamstress for 40 years; widow; two children
- Admitted to [[Heron Pointe|o1:short]] on [[March 3, 2023|date:admission date]], walking with a walker, [[mild dementia|health:diagnosis]], weight 131 lb
- Died [[January 22, 2024|date:date of death]], [[age 96|age:labelled age]]
> She [[attended Mass daily at the cathedral until she was 93|attr:religion]]. The defense will say she was [[96|age:bare age]] and frail. Our answer: she was 96 and walking when she arrived.
# Timeline of the wound
| Date | Record | Event |
| [[10/02/23|date:short numeric date]] | Braden Scale | Scored high risk; no care plan change |
| [[11/14/23|date:short numeric date]] | Nurse note | "[[Redness to sacrum|health:early skin finding]]" — no physician notified |
| [[12/19/23|date:short numeric date]] | Wound nurse | [[Stage 3 sacral pressure ulcer|health:diagnosis]], first measurement |
| [[1/9/24|date:short numeric date]] | Hospital ED | [[Stage 4 ulcer to bone, osteomyelitis, sepsis|health:diagnosis]]; weight 104 lb |
| [[1/22/24|date:short numeric date]] | Hospice | Death |
> Turning logs for December are blank on 41 of 93 shifts. Two aides will testify the unit ran one aide to 22 residents on nights. One of them, [[the night aide who was fired after she called the state hotline|indirect:whistleblower identifiable by circumstances]], is our best witness and is afraid of losing her new job.
# Liability
- State survey of [[2/6/2024|date:survey date]] (CMS Form 2567): deficiency under 42 CFR § 483.25, F-tag 686, "actual harm"
- [[Dr. Shirin Vossoughi|p5:full]], geriatrician: the ulcer was avoidable; [[27 lb weight loss in ten weeks|health:weight loss]] went unaddressed
- Corporate parent [[Altamaha Senior Holdings, LLC|o3:full]] cut the nursing budget [[$310,000|money]] in 2023
# Damages
- Medical expenses: [[$187,442.19|money]] (Medicare lien [[$61,208.33|money]])
- Funeral: [[$11,950|money]]
- Pain and suffering, ten weeks; full value of the life under O.C.G.A. § 51-4-2
- Opening demand: [[$2,750,000|money]]
> Authority from the clients: do not go below [[$900,000|money]] without calling them. [[Rosemarie Guarnieri-Platt|p2:full]] is the administrator and decides. Her brother [[Dominic Guarnieri|p3:full]] wants to try the case; [[he has not spoken to her since the funeral|indirect:family estrangement]] and will attend by video from [[Jacksonville|place:city]].
> Carrier is [[Coastal Empire Assurance|o4:full]], policy [[CEA-LTC-0044187|rec:policy number]], limits [[$1,000,000|money]] per claim, eroding. Defense costs to date are probably [[$140K|money:abbreviated thousands]], so real money available is about [[$860,000|money]].
# Logistics
- Plaintiffs' room: conference room B; [[Odell Farrier|p6:full]] lead, cell [[912-555-0141|phone]]
- Rosemarie: [[912.555.0189|phone:dotted]], [[rgplatt@moonrivermail.example|email]]
- Proposed payee if settled: the estate account ending [[4418|acct:last four of account]]; probate no. [[E-2024-0612|rec:probate case number]]
> [[Dominic|p3:first-name]] [[filed for Chapter 7 last year|attr:bankruptcy]]. His share may belong to his trustee. Raise it with the mediator privately, not in the joint session.
'''))

# ---------------------------------------------------------------- 350
DOCS.append(D(350, "md", "long-term disability appeal notes", "health", "US",
  title="Attorney's working notes for a long-term disability appeal",
  ents={"p1": "Bronislava Havlicek", "p2": "Dr. Emeka Onwuachi", "p3": "Dr. Lorelei Stannard", "p4": "Cassius Whitby",
        "p5": "Tomas Havlicek",
        "o1": "Stalwart Life & Disability Insurance Co.", "o2": "Parallax Data Corp.", "o3": "Whitby Disability Law",
        "o4": "Longs Peak Autonomic Clinic"},
  distractors=["ERISA § 502(a)(1)(B)", "29 C.F.R. § 2560.503-1", "SSDI", "own occupation", "CPET", "Form SSA-831"],
  body=r'''
# LTD appeal — working notes

**Client:** [[Bronislava Havlicek|p1:full]] ("[[Brona|p1:nickname]]") · **Our file:** [[WDL-25-0933|rec:firm file number]] · **Atty:** [[Cassius Whitby|p4:full]], [[Whitby Disability Law|o3:full]]
**Insurer:** [[Stalwart Life & Disability Insurance Co.|o1:full]] · **Claim:** [[LTD-2024-0044187|rec:insurance claim number]] · **Group policy:** [[GLT-771209|rec:group policy number]] (employer [[Parallax Data Corp.|o2:full]])
**Denial letter dated** [[August 27, 2025|date:denial date]] → **appeal due** [[February 23, 2026|date:deadline]] (180 days, 29 C.F.R. § 2560.503-1). Calendar [[2/9/26|date:short numeric date]] as our internal deadline.

## Basics

- DOB [[1981-12-03|dob:ISO date]]; SSN [[684-78-5625|ssn]]; lives at [[1409 Remington St.|addr]], [[Fort Collins|place:city]], [[CO|place:state abbreviation]] [[80524|zip]]; cell [[970-555-0157|phone]]; [[brona.havlicek@poudremail.example|email]]
- Senior data engineer at [[Parallax|o2:short]], salary [[$148,000|money]]. Last day worked [[11/17/2023|date:last day worked]]. STD paid 26 weeks, then LTD at 60% = [[$7,400|money]]/month, less offsets.
- [[Stalwart|o1:short]] paid LTD from [[May 2024|date:month and year]] through [[8/31/2025|date:benefits end date]], then terminated: "no objective evidence of impairment precluding own occupation."
- SSDI: [[awarded on reconsideration|attr:disability benefit status]], notice dated [[July 14, 2025|date:award notice date]], [[$2,871|money]]/month, onset [[November 2023|date:month and year]]. The denial letter does not mention the award at all. Get the Form SSA-831.
- Back benefits owed if we win: roughly [[$4,529|money]] net per month from September.

## Medical picture

| Provider | What they say | Problem |
|---|---|---|
| [[Dr. Emeka Onwuachi|p2:full]], PCP | [[Long COVID since the January 2023 infection; ME/CFS criteria met|health:diagnosis]]; [[crashes for two to three days after any exertion|health:symptom pattern]] | Notes are short, mostly "no change" |
| [[Dr. Lorelei Stannard|p3:full]], [[Longs Peak Autonomic Clinic|o4:full]] | [[POTS confirmed on tilt table (heart rate rise of 48)|health:diagnosis and test result]]; on [[ivabradine and midodrine|health:medications]] | Stalwart's file reviewer never saw this test |
| Neuropsych testing, [[3/2025|date:month/year]] | [[Processing speed at the 9th percentile; working memory low average|health:test results]] | Examiner noted "[[possible mood contribution|health:mental health observation]]" |
| Therapist | [[Adjustment disorder with depressed mood; one passive suicidal ideation entry in June|health:mental health history]] | Policy has a 24-month mental/nervous cap. They will try to recharacterize everything as psychiatric. |

## Surveillance

Stalwart's investigator filmed her on [[April 11|date:month and day]] and [[April 12, 2025|date:month, day and year]]. Day one: 22 minutes at a grocery store, then nothing. Day two: no activity. Their letter calls this "inconsistent with reported limitations." It is the opposite. Also: he followed her to [[her son's elementary school|indirect:child's school]] and filmed the pickup line. Raise this.

## To do

1. Two-day CPET (the objective test they say is missing). About [[$2,400|money]], not covered. She cannot afford it; [[Tomas|p5:first-name]] ([[Tomas Havlicek|p5:full]], husband) says [[they have been living on credit cards since September and are behind on the mortgage|attr:financial distress]]. Advance the cost.
2. Narrative letters from [[Dr. Onwuachi|p2:title-surname]] and [[Dr. Stannard|p3:title-surname]] answering the own-occupation question directly.
3. Statements from Tomas and from her former manager.
4. Demand the full claim file and the reviewer's contract. ERISA § 502(a)(1)(B) suit only after exhaustion.
5. Overpayment: Stalwart will claim an SSDI offset of about [[$31,500|money]]. Benefits were direct-deposited to the joint account ending [[7209|acct:last four of account]]; tell her not to spend the SSDI back pay.

Fee: contingent, 33% of back benefits, capped; costs advanced. [[Brona|p1:nickname]] prefers email; phone calls [[wipe her out for the afternoon|health:symptom pattern]]. Keep calls under 15 minutes.
'''))
