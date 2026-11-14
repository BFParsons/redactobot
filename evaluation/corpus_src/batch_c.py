from corpus_src.dsl import D, dt, amt, num

DOCS = []

# ---------------------------------------------------------------- 41
DOCS.append(D(41, "txt", "client intake notes", "legal", "US",
  title="Intake notes - new personal injury matter (rear-end collision)",
  ents={"p1": "Guadalupe Villanueva Ortiz", "p2": "Renee Abernathy-Cole", "p3": "J. Luis Montemayor",
        "p4": "Dwayne T. Hutchins Jr.", "p5": "Marisol Villanueva", "p6": "Ifeoma Okonkwo-Reyes",
        "p7": "Patrice Lemoine",
        "o1": "Alamo Ridge Linen Service, Inc.", "o2": "Brazos Valley Produce Co.",
        "o3": "Santa Rosa Westside Hospital", "o4": "Mission Trail Physical Therapy, PLLC",
        "o5": "Lone Prairie Mutual", "o6": "Granite Shield Commercial"},
  distractors=["Tex. Civ. Prac. & Rem. Code § 16.003", "HIPAA", "33 1/3%", "PIP", "Friday", "Toyota Corolla"],
  body=r'''
INTAKE NOTES -- NEW PI MATTER
Taken by: [[Renee Abernathy-Cole|p2:full!:hyphenated, multi-part or accented name]] (paralegal)     Date: [[4/22/2026|date:intake date]]
Resp. atty: [[JLM|p3:initials]]          File no. [[PI-2026-0418|rec:matter number]]

CLIENT: [[Guadalupe Villanueva Ortiz|p1:full]] (goes by "[[Lupe|p1:nickname]]")
DOB [[11/02/1987|dob]]   SSN [[688-32-4099|ssn]]   [[TX|place:state]] DL# [[31874425|govid:driver's license number]]
Addr: [[2219 Calle Naranjo, Apt 4C|addr]], [[San Antonio|place:city]], TX [[78207|zip]]
Cell [[210-555-0163|phone]] (texts ok); work [[(210) 555-0118 x204|phone!:phone with extension]];
[[lupe.vortiz87@mail.example|email]]
Employer: [[Alamo Ridge Linen Service, Inc.|o1:full]] -- route driver, [[$19.75|money:hourly wage]]/hr,
about 45 hrs/wk.

WHAT HAPPENED
On Friday [[3/13/2026|date:date of accident]] around 6:40 am Lupe was stopped at the light at
[[Culebra Rd and N. Zarzamora St|place!:street intersection]] in her 2019 Toyota Corolla (plate
[[TX LKR-4471|veh:license plate]], VIN [[5YFBURHE7KP912345|veh:VIN]]) when she was rear-ended by a
white box truck owned by [[Brazos Valley Produce Co.|o2:full]] Driver was
[[Dwayne T. Hutchins Jr.|p4:full]] [[Hutchins|p4:surname]] told the officer he "looked down at
the tablet." SAPD crash report no. [[2026-0313-00872|rec:police report number]]. [[Her sister|indirect!:family relationship to client]]
[[Marisol|p5:first-name]] was in the passenger seat, not hurt.

INJURIES / TREATMENT
Taken by ambulance to [[Santa Rosa Westside Hospital|o3:full]]. ER dx: [[cervical strain|health:diagnosis]],
[[L wrist fracture (distal radius)|health!:abbreviated diagnosis]]. Cast 6 weeks. Now in PT twice a week at
[[Mission Trail Physical Therapy, PLLC|o4:full]] w/ [[Dr. Okonkwo-Reyes|p6:title-surname!:title + hyphenated or multi-part surname]]. Taking
[[naproxen 500 mg|health:medication and dose]] and [[cyclobenzaprine|health:medication]] at night. She is
[[14 weeks pregnant|health:pregnancy]] -- OB is monitoring, no complications so far. Prior
history: none to neck; had [[carpal tunnel release|health:prior procedure]] on R wrist in 2021 (other wrist).
ER bill so far [[$8,412.60|money]]; ambulance [[$1,150|money]]; PT approx [[$2,300|money]] to date.
Missed 5 weeks of work = roughly [[4.4k|money!:abbreviated amount without currency sign]] in lost wages.

INSURANCE
Hers: [[Lone Prairie Mutual|o5:full]], policy [[LPM-TX-00728841|rec:policy number]], PIP limit [[$2,500|money]]
(already paid out).
Theirs: [[Granite Shield Commercial|o6:full]], claim no. [[GSC-26-118204|rec:claim number]], adjuster
[[Patrice Lemoine|p7:full]], [[1-800-555-0199 ext. 3317|phone!:toll-free with extension]],
[[plemoine@claims.graniteshield.example|email:subdomain]]. [[Lemoine|p7:surname]] offered
[[seven thousand five hundred dollars|money!:amount spelled out]] on the phone last week "to close
it out." Lupe did not accept.

OTHER
- Lupe is a [[lawful permanent resident|attr:immigration status]] (green card since 2015); worried
  the claim could affect her [[citizenship application|attr!:immigration status, indirect]]. Told her JLM will address.
- [[Brazos Valley|o2:short!:abbreviated organization nickname]] is [[the only produce wholesaler at the Zarzamora terminal market|indirect!:unique role]],
  so the truck is easy to ID on the market's camera.
- No prior claims or lawsuits. No criminal history.
- Fee: 33 1/3% pre-suit per standard agreement; statute of limitations 2 yrs
  (Tex. Civ. Prac. & Rem. Code § 16.003).

TO DO: send rep letter to [[Granite Shield|o6:short!:abbreviated organization nickname]]; order SAPD report + [[Santa Rosa|o3:short!:short form that is also a place name]]
records (HIPAA release signed); calendar SOL [[3/13/2028|date:limitations deadline]].
[[J. Luis Montemayor|p3:full]] to call client Thursday.
'''))

# ---------------------------------------------------------------- 42
DOCS.append(D(42, "pdf", "demand letter", "legal", "US",
  title="Demand letter - commercial lease, deposit and rent abatement",
  ents={"p1": "Kerem Basaran", "p2": "Saoirse Ní Dhomhnaill-Parker", "p3": "Theodore R. Pruitt IV",
        "p4": "Marguerite Odom",
        "o1": "Hargrove Ellison & Pruitt LLP", "o2": "Cumberland Yards Property Group, L.L.C.",
        "o3": "Wren & Thistle Bakehouse, LLC", "o4": "Volunteer State Bank & Trust",
        "o5": "Dixon Restoration Services"},
  distractors=["Tenn. Code Ann. § 66-28-301", "Section 14.2", "Section 9.1", "Commercial Lease", "IOLTA", "Rule 408"],
  body=r'''
# [[Hargrove Ellison & Pruitt LLP|o1:full]]
[[418 Commerce Street, 9th Floor|addr]]
[[Nashville|place:city]], [[TN|place:state]] [[37219|zip]]
Tel. [[615.555.0127|phone:dotted]] | Fax [[615.555.0128|phone:fax, dotted]]
[[May 6, 2026|date:letter date]]
**VIA CERTIFIED MAIL AND EMAIL ([[kbasaran@cumberlandyards.example|email]])**
Mr. [[Kerem Basaran|p1:full]], Managing Member
[[Cumberland Yards Property Group, L.L.C.|o2:full]]
[[PO Box 40117|addr:PO Box]]
[[Franklin|place:city]], TN [[37065|zip]]
**Re: Demand for return of security deposit and rent abatement — [[Suite 210, 1700 Riverfront Parkway|addr!:premises address, suite first]] (the "Premises"); Our File No. [[26-0393-L|rec:file number]]**
Dear [[Mr. Basaran|p1:title-surname]]:
This firm represents [[Wren & Thistle Bakehouse, LLC|o3:full]] ("[[Wren & Thistle|o3:short!:abbreviated organization nickname]]") and its owner, Ms. [[Saoirse Ní Dhomhnaill-Parker|p2:full!:hyphenated, multi-part or accented name]], in connection with the Commercial Lease dated [[August 1, 2022|date:lease date]] (the "Lease") between Wren & Thistle and Cumberland Yards Property Group, L.L.C. ("[[Cumberland Yards|o2:short!:abbreviated organization nickname]]"). Please direct all further communication about this matter to me and not to our client.
As you know, on [[January 19, 2026|date:date of loss]] a sprinkler main failed in the ceiling above the Premises and flooded the kitchen and retail floor. Your own contractor, [[Dixon Restoration Services|o5:full]], confirmed in its report of [[January 27, 2026|date]] that the failure was caused by a corroded fitting in the building's common fire-suppression system, which is the Landlord's responsibility under Section 9.1 of the Lease. The Premises were unusable from January 19 until [[April 17, 2026|date]], a period of nearly three months. Throughout that period Cumberland Yards continued to draw base rent of [[$6,240|money:monthly rent]] per month from our client's account by ACH.
Section 14.2 of the Lease provides that rent abates in full for any period in which the Premises are untenantable through no fault of the Tenant. Our client vacated on [[April 30, 2026|date:surrender date]] after giving proper notice and returned the keys to your property manager, [[Marguerite Odom|p4:full]], who signed the walk-through checklist without exception. [[Ms. Odom|p4:title-surname]] then told [[Ms. Ní Dhomhnaill-Parker|p2:title-surname!:title + hyphenated or multi-part surname]] by text message that the deposit was being "held pending review." There is nothing to review.
Accordingly, Wren & Thistle demands payment of the following:
- Return of the security deposit: [[$18,500.00|money]]
- Refund of rent collected during the abatement period (three months): [[$18,720.00|money]]
- Spoiled inventory and lost equipment, per the schedule already sent to you: approximately [[$11,000|money]]
- Total: [[$48,220.00|money]]
Payment must be received no later than [[May 20, 2026|date:payment deadline]]. Funds may be wired to our IOLTA trust account at [[Volunteer State Bank & Trust|o4:full]], routing no. [[087321579|rtn]], account no. [[0044-718-3392|acct!:trust account number]], referencing our file number above.
If payment is not received by that date, we are instructed to file suit in the Chancery Court for [[Davidson County|place:county]] without further notice, and to seek the bad-faith damages and attorney's fees available under Tenn. Code Ann. § 66-28-301 and the Lease. This letter is sent for settlement purposes under Rule 408 and is without prejudice to any of our client's rights, all of which are reserved.
Very truly yours,
[[Theodore R. Pruitt IV|p3:full:full name with suffix]]
TN BPR No. [[029914|govid:state bar number]]
Direct: [[(615) 555-0131|phone]] | [[trpruitt@hep-law.example|email]]
cc: [[S. Ní Dhomhnaill-Parker|p2:short!:initial + surname]] (by email)
'''))

# ---------------------------------------------------------------- 44
DOCS.append(D(44, "txt", "probate inventory notes", "legal", "US",
  title="Probate inventory working notes - Estate of B. L. Kowalczyk",
  ents={"p1": "Bernadette Louise Kowalczyk", "p2": "Casimir Kowalczyk", "p3": "Stanislaw Kowalczyk",
        "p4": "Hunter Dombrowski", "p5": "Faith Abdullahi", "p6": "Georgia Kowalczyk-Reed",
        "o1": "Rouge River Community Credit Union", "o2": "Penhallow & Strand Securities",
        "o3": "St. Hedwig Parish", "o4": "Estate of Bernadette L. Kowalczyk",
        "o5": "Lakeshore Marine Storage Co.", "o6": "Dombrowski Law, P.C.", "o7": "Beaumont Hills Hospice"},
  distractors=["MCL 700.3706", "Form PC 577", "Form 706", "1099-R", "Chris-Craft", "Buick Lucerne", "Letters of Authority"],
  body=r'''
ESTATE OF [[BERNADETTE LOUISE KOWALCZYK|p1:caps]], DECEASED
[[Wayne County|place:county]] Probate Court, File No. [[2026-871442-DE|rec:probate case number]]
Inventory working notes (for Form PC 577) -- prepared by [[FA|p5:initials]], [[3/30/2026|date]]

Decedent: [[Bernadette Louise Kowalczyk|p1:full]], d. [[February 3, 2026|date:date of death]] at
[[age 94|age]]. Born [[9 June 1931|dob!:day month year]] in [[Hamtramck|place:city]]. SSN on death cert:
[[xxx-xx-7388|ssn!:masked SSN]]. Widow of [[Stanislaw Kowalczyk|p3:full]] (d. 2009). No children.
Personal rep: [[her nephew|indirect!:family relationship to decedent]] [[Casimir Kowalczyk|p2:full]] ("[[Caz|p2:nickname]]"),
Letters of Authority issued [[3/12/2026|date]]. Caz's cell: [[313 555 0176|phone!:spaces only]].
Estate EIN (applied online [[3/16/2026|date]]): [[92-3310847|taxid:EIN]].

REAL PROPERTY
1. House at [[88 Lindenwood Terrace|addr]], [[Dearborn|place:city]], [[MI|place:state]] [[48124|zip]].
   Tax ID parcel [[82-09-214-031|rec!:parcel number]]. SEV x2 suggests about [[$212,000|money]];
   Caz got a realtor opinion of [[$235k|money!:abbreviated amount]]. No mortgage. Appraisal
   ordered.

BANK / INVESTMENT
2. [[Rouge River Community Credit Union|o1:full]] -- share draft acct ending [[4409|acct!:last four only]],
   date-of-death balance [[$14,882.19|money]].
3. [[RRCCU|o1:acronym]] 18-month certificate no. [[70041882|acct:certificate account number]] -- [[$50,000.00|money]] plus
   accrued int. [[$611.42|money]]. POD beneficiary named: [[Georgia Kowalczyk-Reed|p6:full!:hyphenated, multi-part or accented name]]
   ([[grand-niece|indirect!:family relationship]]). NON-PROBATE, list for info only.
4. [[Penhallow & Strand Securities|o2:full]] brokerage acct [[PSS-448-207716|acct:brokerage account number]], DOD value
   [[$386,240.77|money]]. Statement shows routing [[043993190|rtn]] for the sweep acct.
   [[Penhallow|o2:short!:abbreviated organization nickname]] needs a medallion signature + certified Letters to retitle to
   "[[Estate of Bernadette L. Kowalczyk|o4:full]]".

VEHICLES / OTHER TITLED
5. 2008 Buick Lucerne, VIN [[1G4HD57258U164229|veh:VIN]], MI plate [[DWK 3391|veh:license plate]]. KBB approx [[$3,100|money]].
6. 1987 Chris-Craft 26' cabin cruiser "[[Polish Princess|indirect!:named boat]]", hull ID [[CCHEV187M87A|veh!:hull identification number]],
   kept at [[Lakeshore Marine Storage Co.|o5:full]], [[St. Clair Shores|place:city]]. Storage arrears
   [[$1,940|money]] -- [[Lakeshore|o5:short!:abbreviated organization nickname]] is asserting a lien.

HOUSEHOLD / PERSONAL
7. Furnishings, est. [[$4,000|money]]. Jewelry in safe deposit box [[#217|rec!:safe deposit box number]] at RRCCU
   [[Michigan Ave|place!:branch location by street]] branch -- not yet opened, need Caz + credit union officer.
8. Uncashed pension check, [[$1,206.00|money]].

DEBTS / CLAIMS SO FAR
- [[Beaumont Hills Hospice|o7:full]] final invoice [[$2,317.50|money]] (decedent had [[advanced dementia|health:diagnosis]]
  and [[congestive heart failure|health:diagnosis]]; on hospice from Nov.)
- Funeral, paid by Caz personally: [[$9,480|money]] -- reimburse as priority claim (MCL 700.3706? check).

WILL (dated [[10/14/2014|date:date of will]], drafted by [[Hunter Dombrowski|p4:full:name that is also a common word]] of
[[Dombrowski Law, P.C.|o6:full]], bar no. [[P48113|govid:state bar number]]):
- [[$25,000|money]] to [[St. Hedwig Parish|o3:full]] "[[for Masses for my soul and Stan's|attr!:religious practice]]"
- [[$10,000|money]] to Georgia
- residue to Caz.
Caz says [[Hunter|p4:first-name!:first name that is also a common word]] retired; original will was in the firm's vault and
has been filed. [[Georgia|p6:first-name!:first name that is also a state]] lives out of state and has asked for a copy --
ok to send per [[Ms. Abdullahi|p5:title-surname]].

Open items: Form 706 not required (well under exemption). Confirm whether the 1099-R
pension payer needs the estate EIN. Next review with [[Faith Abdullahi|p5:full]] on [[4/9/2026|date]].
'''))

# ---------------------------------------------------------------- 43
DOCS.append(D(43, "docx", "court filing draft - complaint", "legal", "US", length="long",
  title="Draft federal complaint - employment discrimination and retaliation",
  ents={"p1": "Adaeze N. Okpara-Lindqvist", "p2": "Bradley J. Vanderhoef", "p3": "Jordan Paris",
        "p4": "Hye-jin Park", "p5": "Tyler Brandt", "p6": "Darnell Whitlock-Pierce",
        "p7": "Rosalind Achterberg-Tran", "p8": "Kwame Mensah-Boateng", "p9": "Lars Lindqvist",
        "o1": "Meridian Lakes Logistics Corp.", "o2": "Great Plains Freightways, Inc.",
        "o3": "Fox Valley Neurology Associates, S.C.", "o4": "Prairie Path Infusion Center",
        "o5": "Tallgrass Health Plan", "o6": "Achterberg Mensah Employment Law Group LLC"},
  distractors=["42 U.S.C. § 2000e", "29 U.S.C. § 621", "42 U.S.C. § 1981", "Title VII", "28 U.S.C. § 1331",
               "Rule 38(b)", "COUNT III", "Civil Rights Act of 1964"],
  body=r'''
# IN THE UNITED STATES DISTRICT COURT FOR THE NORTHERN DISTRICT OF [[ILLINOIS|place!:state in caps within court name]], EASTERN DIVISION
[[ADAEZE N. OKPARA-LINDQVIST|p1:caps]], Plaintiff,
v.
[[MERIDIAN LAKES LOGISTICS CORP.|o1:caps]] and [[BRADLEY J. VANDERHOEF|p2:caps]], Defendants.
Case No. [[1:26-cv-04417|rec:federal docket number]]
**COMPLAINT AND JURY DEMAND**
DRAFT [[5/11/2026|date:draft date]] — PRIVILEGED AND CONFIDENTIAL — ATTORNEY WORK PRODUCT
([[KMB|p8:initials]] note to [[RAT|p7:initials]]: client confirmed all dates below by phone on [[5/8/2026|date]] (her cell, [[630-555-0190|phone]]). Her husband [[Lars|p9:first-name]] found the old offer letter. Still need the bonus plan document.)
## NATURE OF THE ACTION
1. This is an action for discrimination and retaliation under Title VII of the Civil Rights Act of 1964, 42 U.S.C. § 2000e et seq., the Americans with Disabilities Act, 42 U.S.C. § 12101 et seq. (the "ADA"), the Age Discrimination in Employment Act, 29 U.S.C. § 621 et seq. (the "ADEA"), and 42 U.S.C. § 1981. Plaintiff seeks back pay, front pay, compensatory and punitive damages, and her attorneys' fees and costs.
## PARTIES
2. Plaintiff [[Adaeze N. Okpara-Lindqvist|p1:full!:hyphenated, multi-part or accented name]] ("[[Ms. Okpara-Lindqvist|p1:title-surname!:title + hyphenated or multi-part surname]]" or "Plaintiff") is a 52-year-old [[Black woman|attr:race]] of [[Nigerian national origin|attr:national origin]] who resides at [[1108 Thornapple Court|addr]], [[Naperville|place:city]], [[Illinois|place:state]] [[60565|zip]]. She became a [[naturalized U.S. citizen|attr:citizenship status]] in 2009.
3. Defendant [[Meridian Lakes Logistics Corp.|o1:full]] ("[[Meridian Lakes|o1:short!:abbreviated organization nickname]]" or the "Company") is a [[Delaware|place:state of incorporation]] corporation with its principal place of business at [[2500 Diehl Road, Building C|addr]], [[Aurora|place!:city name that is also a common word]], Illinois [[60502|zip]]. At all relevant times the Company employed more than 500 people and was an employer within the meaning of Title VII, the ADA and the ADEA.
4. Defendant [[Bradley J. Vanderhoef|p2:full]], known inside the Company as "[[Chip|p2:nickname]]," is the Company's Senior Vice President of Network Operations. He was Plaintiff's direct supervisor from March 2024 until her termination. On information and belief he resides in [[DuPage County|place:county]], Illinois.
## JURISDICTION, VENUE AND ADMINISTRATIVE EXHAUSTION
5. This Court has subject-matter jurisdiction under 28 U.S.C. § 1331. Venue is proper in this District because the unlawful employment practices alleged below were committed here and the Company maintains its records here.
6. Plaintiff filed a timely charge of discrimination with the Equal Employment Opportunity Commission on [[September 8, 2025|date:EEOC charge date]], Charge No. [[440-2025-08812|rec:EEOC charge number]]. The Commission issued a Notice of Right to Sue dated [[February 24, 2026|date]], which Plaintiff received on [[February 27, 2026|date]]. This action is filed within ninety days of receipt.
## FACTS
7. The Company hired Plaintiff on [[June 14, 2016|date:hire date]] as a Transportation Analyst (Employee ID [[ML-104476|rec:employee ID]]). She was promoted three times and in January 2022 became Director of Carrier Procurement, with a base salary of [[$118,400|money:salary]] and a target bonus of 15 percent.
8. Plaintiff's annual reviews rated her "exceeds expectations" in every year from 2016 through 2023. In 2023 she renegotiated the Company's contract with its largest less-than-truckload carrier, [[Great Plains Freightways, Inc.|o2:full]], saving the Company approximately [[$2.3 million|money!:amount in words and figures]] a year, for which she received the Chief Executive's award.
9. In March 2024 [[Mr. Vanderhoef|p2:title-surname]] became Plaintiff's supervisor. At their first one-on-one meeting, on [[March 19, 2024|date]], he asked her "where the accent is from," said he "could never pronounce names like that," and announced that he would call her "[[Addie|p1:nickname]]." Plaintiff told him that she preferred to be called [[Adaeze|p1:first-name]]. He continued to call her Addie in meetings and in writing for the next thirteen months.
10. At staff meetings Mr. Vanderhoef repeatedly referred to Plaintiff's team, most of whom are people of color, as "the United Nations." In or about June 2024 he told [[Darnell Whitlock-Pierce|p6:full!:hyphenated, multi-part or accented name]], a [[Black analyst|attr:race]] on Plaintiff's team, that the group needed "fewer accents on the phone with carriers." [[Mr. Whitlock-Pierce|p6:title-surname!:title + hyphenated or multi-part surname]] reported the remark to Plaintiff the same day.
11. In August 2024 Plaintiff was diagnosed with [[relapsing-remitting multiple sclerosis|health:diagnosis]] by her neurologist, [[Dr. Hye-jin Park|p4:full!:full name with title]] of [[Fox Valley Neurology Associates, S.C.|o3:full]] She began [[ocrelizumab infusions every six months|health:medication and schedule]] at [[Prairie Path Infusion Center|o4:full]].
12. On [[September 3, 2024|date:accommodation request date]] Plaintiff submitted a written request for reasonable accommodation to the Company's Director of Human Resources, [[Jordan Paris|p3:full!:both names are also place names]]. She asked for two remote work days per week, [[a parking space near the building entrance|health!:disability accommodation]], and unpaid time off on infusion days. The request was supported by a letter from [[Dr. Park|p4:title-surname]].
13. [[Ms. Paris|p3:title-surname!:surname that is also a city]] approved the request on [[September 12, 2024|date]]. The next morning Mr. Vanderhoef sent Ms. Paris an email from [[bvanderhoef@meridianlakes.example|email]] that read, in part: "We need people who are here and who have some runway left. She's what, mid-fifties and sick? Find me a way to restructure."
14. Over the following four months Mr. Vanderhoef removed Plaintiff from the [[Great Plains|o2:short!:abbreviated organization nickname]] account, reassigned two of her direct reports to [[Tyler Brandt|p5:full]], a 31-year-old [[white manager|attr:race]] with no procurement experience, and stopped inviting her to the weekly carrier council that she had founded.
15. On [[January 9, 2025|date:internal complaint date]] Plaintiff complained in writing to Ms. Paris and to the Company's ethics hotline (report no. [[EH-2025-0037|rec:hotline report number]]) that she was being discriminated against because of her race, national origin, age and disability.
16. Eleven days later, on [[January 20, 2025|date]], Mr. Vanderhoef placed Plaintiff on a sixty-day performance improvement plan, the first adverse performance document of her career. The plan cited "availability" and "executive presence."
17. On [[March 4, 2025|date]], at Mr. Vanderhoef's direction, the Company's IT department pulled the VPN logs for Plaintiff's laptop (serial no. [[5CG2187KQZ|dev:laptop serial number]]) and flagged eleven logins from the IP address [[198.51.100.44|ip]] as coming from an "unauthorized location." That address belongs to the guest network at Prairie Path Infusion Center, where Plaintiff worked from a treatment chair on her approved infusion days.
18. On [[April 11, 2025|date:termination date]] Mr. Vanderhoef and Ms. Paris terminated Plaintiff's employment in a nine-minute video call. The stated reason was "performance and violation of the remote access policy." The Company refused to pay Plaintiff's earned 2024 bonus of [[$17,760|money]] and cancelled unvested restricted stock units worth approximately [[$64,000|money]].
19. The Company replaced Plaintiff with [[Mr. Brandt|p5:title-surname]], at a base salary of [[$131,000|money]].
20. As a result of her termination Plaintiff lost coverage under the Company's group plan with [[Tallgrass Health Plan|o5:full]] (member ID [[XGH883120457|rec:health plan member ID]]). She has paid COBRA premiums of [[$2,114.38|money]] per month to continue her infusions. Since April 2025 she has been treated for [[major depressive disorder|health:mental health diagnosis]] and has been prescribed [[sertraline 100 mg|health:medication and dose]].
21. Plaintiff has applied for more than sixty comparable positions. She remained unemployed until [[February 2, 2026|date]], when she accepted a contract role paying roughly [[sixty percent of her former salary|money!:relative amount]].
## COUNT I — RACE AND NATIONAL ORIGIN DISCRIMINATION (TITLE VII AND § 1981) — AGAINST BOTH DEFENDANTS AS APPLICABLE
22. Plaintiff restates paragraphs 1 through 21. Defendants subjected Plaintiff to disparate treatment in the terms and conditions of her employment, and terminated her, because of her race and national origin. Mr. Vanderhoef's own statements are direct evidence of that motive. He is individually liable under § 1981.
## COUNT II — DISABILITY DISCRIMINATION AND FAILURE TO ACCOMMODATE (ADA) — AGAINST THE COMPANY
23. Plaintiff restates paragraphs 1 through 21. Plaintiff is a qualified individual with a disability. The Company granted her an accommodation and then punished her for using it, treating her presence at an infusion center as a policy violation.
## COUNT III — AGE DISCRIMINATION (ADEA) — AGAINST THE COMPANY
24. Plaintiff restates paragraphs 1 through 21. Plaintiff was over forty, was performing to the Company's legitimate expectations, and was replaced by a substantially younger and less qualified employee at a higher salary.
## COUNT IV — RETALIATION (TITLE VII, ADA, ADEA AND § 1981) — AGAINST BOTH DEFENDANTS AS APPLICABLE
25. Plaintiff restates paragraphs 1 through 21. Plaintiff engaged in protected activity when she requested accommodation and when she complained on January 9, 2025. The performance plan followed eleven days later and the termination ninety-two days later. The stated reasons are pretext.
## PRAYER FOR RELIEF
Plaintiff respectfully requests that the Court enter judgment in her favor and award: (a) back pay and lost benefits, presently estimated at [[$171,300|money]]; (b) reinstatement or, in the alternative, front pay; (c) compensatory and punitive damages in an amount to be proved at trial; (d) liquidated damages under the ADEA; (e) pre- and post-judgment interest; (f) reasonable attorneys' fees and costs; and (g) such other relief as the Court deems just.
## JURY DEMAND
Under Rule 38(b) of the Federal Rules of Civil Procedure, Plaintiff demands trial by jury on all issues so triable.
Dated: May ___, 2026
Respectfully submitted,
[[ADAEZE OKPARA-LINDQVIST|p1:caps]]
By: /s/ DRAFT — NOT FILED
[[Rosalind Achterberg-Tran|p7:full!:hyphenated, multi-part or accented name]] (ARDC No. [[6298841|govid:attorney registration number]])
[[Kwame Mensah-Boateng|p8:full!:hyphenated, multi-part or accented name]] (ARDC No. [[6331207|govid:attorney registration number]])
[[Achterberg Mensah Employment Law Group LLC|o6:full]]
[[77 West Wacker Place, Suite 1850|addr]]
[[Chicago|place:city]], Illinois [[60601|zip]]
[[(312) 555-0144|phone]]
[[rat@amelg.example|email]] / [[kmb@amelg.example|email]]
'''))

# ---------------------------------------------------------------- 45
DOCS.append(D(45, "eml", "email thread", "legal", "UK", enc="plain",
  title="Email thread - residential conveyancing, completion funds",
  ents={"p1": "Imogen Farquharson-Lee", "p2": "Rhys ap Gwilym", "p3": "Oluwaseun Adeyemi",
        "p4": "Priyanka Chaudhary", "p5": "Malcolm Tetley", "p6": "Eluned ap Gwilym",
        "o1": "Castlegate Conveyancing LLP", "o2": "Pennine & Wharfe Building Society",
        "o3": "Tetley Marsh Solicitors", "o4": "Aire Valley Removals Ltd"},
  distractors=["SDLT", "TR1", "CHAPS", "Friday", "VAT", "Solicitors Regulation Authority", "Land Registry"],
  ok=["2023.) 3"],
  headers={"From": "[[Imogen Farquharson-Lee|p1:full!:hyphenated, multi-part or accented name]] <[[i.farquharson-lee@castlegate-conveyancing.example|email]]>",
           "To": "[[Rhys ap Gwilym|p2:full!:hyphenated, multi-part or accented name]] <[[rhys.apgwilym@mail.example|email]]>, [[Seun Adeyemi|p3:short:nickname first name + surname]] <[[seun.a+house@mail.example|email!:plus addressing]]>",
           "Cc": "[[p.chaudhary@castlegate-conveyancing.example|email]]",
           "Subject": "RE: [[14 Bishopthorpe Mews|addr]] - completion statement and funds (our ref [[IFL/26/01187|rec:solicitor reference]])",
           "Date": "Wed, [[10 Jun 2026|date!:day-first date with month name]] 16:42:07 +0100"},
  body=r'''
Dear [[Rhys|p2:first-name]] and [[Seun|p3:nickname]],

Thank you both - signed contract and TR1 received this morning. To answer
your questions in turn:

1. Completion is fixed for Friday [[19 June 2026|date!:completion date]]. The sellers' solicitors
([[Tetley Marsh Solicitors|o3:full]], [[Malcolm Tetley|p5:full]] acting) confirmed by phone today.

2. The balance we need from you is [[£41,862.50|money]], made up as follows:
     Purchase price                          [[£385,000.00|money]]
     Less deposit paid on exchange           [[£38,500.00|money]]
     Less mortgage advance ([[Pennine & Wharfe|o2:short!:abbreviated organization nickname]])  [[£308,000.00|money]]
     SDLT                                    [[£1,750.00|money]]
     Land Registry fee                       [[£330.00|money]]
     Our fees and disbursements incl. VAT    [[£1,282.50|money]]
(I know [[Mr Adeyemi|p3:title-surname]] queried the SDLT figure - it reflects first-time
buyer relief for Rhys only, as Seun owned the flat in [[Headingley|place:neighbourhood]] until 2023.)

3. Please send cleared funds by CHAPS or Faster Payment no later than
[[Wednesday 17 June|date!:date without year]] to our client account:
     [[Castlegate Conveyancing LLP|o1:full]] Client Account
     Sort code [[40-47-31|rtn!:UK sort code]]   Account no. [[61094422|acct]]
     IBAN [[GB90 HBUK 1941 5563 0721 37|iban:IBAN with spaces]]   BIC [[HBUKGB4B|acct!:SWIFT code]]
     Reference: [[APGWILYM 01187|rec!:payment reference containing surname]]
WE WILL NEVER CHANGE OUR BANK DETAILS BY EMAIL. If you receive anything
saying otherwise, ring [[Priyanka|p4:first-name]] or me on [[0113 496 0152|phone:UK landline]] before sending money.

4. ID: thank you for the passports. For our file, Rhys's is no. [[533209871|govid:passport number]]
(expires [[03/2031|date!:month and year only]]) and Seun's [[Nigerian passport|attr:nationality]] is no. [[A09417726|govid:passport number]],
with his [[indefinite leave to remain|attr:immigration status]] vignette. The lender has asked for Seun's
National Insurance number again as the one on the mortgage offer has a
typo - I have [[QQ 12 34 56 C|govid!:National Insurance number]] on file; please confirm.

5. [[Aire Valley Removals Ltd|o4:full]] can collect keys from the agent from 1pm.

Kind regards,
[[Imogen|p1:first-name]]

Imogen Farquharson-Lee | Senior Associate
Castlegate Conveyancing LLP, [[3 Toft Green|addr]], [[York|place:city]] [[YO1 6JT|zip:UK postcode]]
DDI [[01904 555 0117|phone:UK direct dial]] | Mob [[07700 900413|phone:UK mobile]]
SRA no. [[648213|govid:regulator number]]. Authorised and regulated by the Solicitors Regulation Authority.

> -----Original Message-----
> From: Rhys ap Gwilym
> Sent: [[09 June 2026|date!:day-first date with month name]] 21:15
> To: Imogen Farquharson-Lee
> Subject: 14 Bishopthorpe Mews - completion statement and funds
>
> Hi Imogen
>
> Signed docs are in the post (recorded, tracking no. [[KQ 4471 8802 3GB|rec:postal tracking number]]).
> Two things. Seun thinks the stamp duty looks wrong - can you check? And
> my mum, [[Mrs Eluned ap Gwilym|p6:title-surname!:title + full name]], is gifting us [[twenty thousand pounds|money!:amount spelled out]] towards
> the balance. Do you need anything from her? She's [[91|age!:bare age]] and doesn't
> do email, but you can ring her on [[01632 960884|phone]].
>
> Also our new joint account for the direct debits is with [[P&W|o2:acronym]],
> a/c [[20817763|acct!:unlabelled account number]] if you need it for the mortgage form.
>
> Cheers
> [[R.|p2:initials!:single initial sign-off]]
'''))

# ---------------------------------------------------------------- 46
DOCS.append(D(46, "txt", "immigration case notes", "legal", "US",
  title="Immigration case notes - marriage-based adjustment of status",
  ents={"p1": "Trần Minh Khôi", "p2": "Chase Abernethy", "p3": "Soledad Ibarra-Whitcomb",
        "p4": "Anand Krishnamurthy", "p5": "Trần Văn Hùng",
        "o1": "Sierra Vista Immigration Law Group, P.C.", "o2": "South Bay Federal Credit Union",
        "o3": "De Anza Community College", "o4": "Willow Glen Urgent & Occupational Care",
        "o5": "Pho Hoa Binh Restaurant Group LLC"},
  distractors=["I-485", "I-130", "I-693", "INA § 245(a)", "F-1", "USCIS", "Form I-864", "SEVIS"],
  body=r'''
[[SIERRA VISTA IMMIGRATION LAW GROUP, P.C.|o1:caps]] -- CASE NOTES
Matter: [[26-IMM-0291|rec:matter number]]   Atty: [[S. Ibarra-Whitcomb|p3:short!:initial + surname]]   Portal:
[[https://portal.sierravistalaw.example/c/26-IMM-0291|url:client portal link containing matter number]]

BENEFICIARY: [[TRAN, Minh Khoi|p1:last-first:Last, First without diacritics]] (passport spelling) / [[Trần Minh Khôi|p1:full!:full name with diacritics, family name first]]
   goes by "[[Khoi|p1:first-name!:given name without diacritics]]"
   DOB: [[22 Feb 1994|dob!:day month year]], [[Đà Nẵng|place!:city with diacritics]], [[Vietnam|attr!:country of birth and nationality]]
   A-number: [[A 216 448 907|govid!:alien registration number with spaces]]
   Passport: [[C4471882|govid:passport number]] (Vietnam), exp. [[11 Aug 2029|date!:day-first date with month name]]
   I-94 no.: [[73018845521|govid!:admission record number, digits only]]
   ITIN: [[953-78-4410|taxid:ITIN]] (no SSN yet)
PETITIONER / SPOUSE: [[Chase Abernethy|p2:full!:first name that is also a common word]], [[U.S. citizen by birth|attr:citizenship status]]
   DOB [[1991-07-30|dob!:ISO format]], SSN [[667 37 3167|ssn!:SSN with spaces]]
Home (both): [[745 Lincoln Ave, Unit 12|addr]], [[San Jose|place:city]], [[CA|place:state]] [[95126|zip]]
Khoi cell [[408.555.0171|phone:dotted]]   Chase cell [[+1 408 555 0109|phone!:international format]]
Email: [[khoi.tran94@mail.example|email]]; [[c.abernethy@southbayfab.example|email]] (Chase's work, AVOID)

[[1/14/2026|date]] - INITIAL CONSULT ([[SIW|p3:initials]])
Khoi entered at [[SFO|place!:airport code]] on [[08/17/2018|date:date of entry]] in F-1 status to attend [[De Anza Community College|o3:full]].
Stopped attending spring 2020 when [[his father|indirect!:family relationship]] ([[Trần Văn Hùng|p5:full!:name with diacritics]]) became ill and money
ran out; SEVIS terminated [[06/02/2020|date]]. So: [[out of status since June 2020|attr:immigration status]], but
inspected and admitted -> eligible to adjust under INA § 245(a) as immediate
relative. [[Unauthorized employment|attr!:immigration violation]] forgiven for IRs. He has been working the line at a
restaurant owned by [[Pho Hoa Binh Restaurant Group LLC|o5:full]], paid by check, files with the ITIN.
Married [[Chase|p2:first-name!:first name that is also a common word]] [[October 4, 2025|date:date of marriage]] at the [[Santa Clara County|place:county]] Clerk-Recorder; reception
at his parents' place in [[Los Gatos|place:city]]. This is a [[same-sex marriage|attr:sexual orientation]]; Khoi says
his family in Vietnam does not know and asked that nothing be mailed there.
ISSUE: one arrest. [[3/9/2021|date:date of arrest]], [[petty theft (Cal. Penal Code § 484)|attr:criminal history]], Santa Clara
County Superior Court docket [[C2104417|rec:criminal docket number]]. [[Completed diversion, dismissed|attr!:criminal history disposition]] [[9/21/2021|date]]. Need
certified disposition. Not a CIMT problem w/ petty offense exception but must disclose.
Quoted flat fee [[$4,800|money]] + filing fees ([[$1,440|money]] I-485, [[$675|money]] I-130). Chase paid
retainer [[$2,400|money]] by card ending [[8493|card!:last four only]].

[[2/3/2026|date]] - DOCS RECEIVED
Joint lease; joint acct at [[South Bay Federal Credit Union|o2:full]] (acct [[0098314472|acct]], opened [[11/12/2025|date]]);
wedding photos; Chase's 2024 return (AGI [[$96,410|money]]) for Form I-864.
Missing: Khoi's birth cert translation; school transcripts.

[[2/19/2026|date]] - MEDICAL
I-693 done by civil surgeon [[Dr. Anand Krishnamurthy|p4:full:full name with title]], [[Willow Glen Urgent & Occupational Care|o4:full]].
[[IGRA positive|health!:lab result, abbreviated]], chest x-ray clear -> [[latent TB|health:diagnosis]]. Started [[rifampin 600 mg daily x 4 months|health:medication and dose]].
[[Dr. K|p4:nickname:title + initial]] says this is Class B, not a bar. Vaccines complete.

[[3/2/2026|date]] - FILED concurrent I-130 / I-485 / I-765. Receipts:
   I-130  [[IOE0926114478|rec:USCIS receipt number]]
   I-485  [[IOE0926114479|rec:USCIS receipt number]]
   I-765  [[IOE0926114480|rec:USCIS receipt number]]
Client set up his own USCIS online account -- login [[khoitran_sj|cred:username]] / pw [[Banhmi#2018!|cred:password]] (he
emailed it to us; told him to change it and NOT to send passwords by email).

[[4/27/2026|date]] - Biometrics done at ASC, [[122 Charcot Ave|addr:government office address]]. Interview notice came:
[[July 16, 2026|date:interview date]], 8:15 am, USCIS San Jose Field Office. Prep session w/ both
spouses set for [[7/9/2026|date]]. Remind [[Mr. Abernethy|p2:title-surname]] to bring original birth
certificate. [[Soledad Ibarra-Whitcomb|p3:full!:hyphenated, multi-part or accented name]] to attend.
'''))

# ---------------------------------------------------------------- 47
DOCS.append(D(47, "pptx", "case status presentation", "legal", "US",
  title="Litigation status deck for client members",
  ents={"p1": "Mercy Abiodun-Clark", "p2": "Gunnar Halvorsen", "p3": "Delphine Roux",
        "p4": "Wesley Tanaka-Brooks", "p5": "Ezekiel Stoltzfus", "p6": "Ingrid Halvorsen",
        "o1": "Halvorsen Family Farms LLC", "o2": "AgriNova Seed Co.",
        "o3": "Roux Tanaka Litigation Partners", "o4": "Corn Belt Mutual Insurance Group",
        "o5": "Cedar Valley Agronomy Consultants, Inc."},
  distractors=["Rule 26(f)", "Rule 30(b)(6)", "Daubert", "Q3", "UCC § 2-315"],
  body=r'''
# [[Halvorsen Family Farms LLC|o1:full]] v. [[AgriNova Seed Co.|o2:full]]
Litigation status report to the members
Prepared by [[Roux Tanaka Litigation Partners|o3:full]] — [[June 2, 2026|date:presentation date]]
PRIVILEGED AND CONFIDENTIAL — ATTORNEY-CLIENT COMMUNICATION
# Where the case stands
- Filed [[November 21, 2025|date:filing date]], U.S. District Court, N.D. [[Iowa|place:state]] — No. [[6:25-cv-02088-MAC|rec:federal docket number with judge initials]]
- Assigned to [[Hon. Mercy Abiodun-Clark|p1:full!:full name with judicial title]]; [[Judge Abiodun-Clark|p1:title-surname!:title + hyphenated or multi-part surname]] denied [[AgriNova|o2:short!:abbreviated organization nickname]]'s motion to dismiss on [[March 30, 2026|date]]
- Claims surviving: breach of implied warranty (UCC § 2-315), negligent misrepresentation
- Lead counsel: [[Delphine Roux|p3:full]] ([[droux@rouxtanaka.example|email]], [[319-555-0148|phone]]) and [[Wesley Tanaka-Brooks|p4:full!:hyphenated, multi-part or accented name]]
# Key dates
| Event | Date |
| Rule 26(f) report filed | [[04/20/2026|date]] |
| Fact discovery closes | [[10/30/2026|date]] |
| Expert reports due | [[12/15/2026|date]] |
| Mediation ([[E. Stoltzfus|p5:short:initial + surname]]) | [[09/09/2026|date]] |
| Trial-ready date | [[05/03/2027|date]] |
# Discovery status
- We produced 14,200 pages, including planting records for the [[Black Hawk County|place:county]] and [[Butler County|place:county]] fields
- AgriNova has produced lot records for seed lot [[AN-24-77193|rec:product lot number]] only; motion to compel being drafted
- Rule 30(b)(6) deposition of AgriNova noticed for [[July 22, 2026|date]] in [[Des Moines|place:city]]
- [[Gunnar|p2:first-name]] and [[Ingrid|p6:first-name]] will each be deposed in August; prep sessions to be scheduled with [[Wes|p4:nickname]]
# Damages model
| Item | Amount |
| Lost yield, 2,340 acres | [[$1,872,000|money]] |
| Replant and inputs | [[$214,650|money]] |
| Lost premium contracts | [[$388,000|money]] |
| Total claimed | [[$2,474,650|money]] |
- Expert: [[Cedar Valley Agronomy Consultants, Inc.|o5:full]] — preliminary report supports the yield figure; expect a Daubert challenge
- [[Corn Belt Mutual Insurance Group|o4:full]] paid [[$310,000|money]] on crop policy [[MPCI-19-0044817|rec:policy number]] and holds a subrogation interest
# Settlement posture
- AgriNova's opening number at the March call: [[$350k|money!:abbreviated amount]] plus seed credits — rejected
- Our recommendation: do not go below [[$1.4 million|money!:amount in words and figures]] before the 30(b)(6) deposition
- [[Mr. Stoltzfus|p5:title-surname]] ([[Ezekiel Stoltzfus|p5:full]], retired magistrate) mediated the 2023 [[Corn Belt|o4:short!:abbreviated organization nickname]] hail cases and knows the carriers
# Budget and next steps
- Fees billed to date: [[$186,412.75|money]]; estimate through trial: [[$520,000|money]] to [[$610,000|money]]
- Matter no. [[HFF-0031|rec:matter number]]; invoices go to [[Gunnar Halvorsen|p2:full]], managing member
- Decision needed from the members in Q3: authority range for the September mediation
- Questions: call [[Delphine|p3:first-name]] direct at [[(319) 555-0102|phone]]
'''))

# ---------------------------------------------------------------- 48
DOCS.append(D(48, "txt", "tax return preparation notes", "accounting", "US",
  title="Preparer notes - joint 1040 with Schedule C (rideshare driver)",
  ents={"p1": "Nikolai Petrosyan", "p2": "Anush Petrosyan", "p3": "Davit Petrosyan", "p4": "Lilit Petrosyan",
        "p5": "Marcy Oyelaran", "p6": "Gayane Sargsyan",
        "o1": "Oyelaran & Finch Tax Services", "o2": "RydeLoop Technologies, Inc.",
        "o3": "Verdugo Hills Unified School District", "o4": "Foothill Pacific Bank",
        "o5": "St. Sarkis Armenian Apostolic Church", "o6": "Covered California"},
  distractors=["Sched C", "Form 1099-K", "Form 1095-A", "Form 8962", "Form 8879", "W-2", "Toyota Camry Hybrid", "67 cents"],
  body=r'''
[[Oyelaran & Finch Tax Services|o1:full]] -- PREPARER NOTES (TY2025, MFJ)
Client #[[20417|rec!:short client number]]     Preparer: [[M. Oyelaran|p5:short:initial + surname]]     Interview [[2/26/2026|date]]

TAXPAYER   [[Petrosyan, Nikolai|p1:last-first]] ("[[Niko|p1:nickname]]")   SSN [[542177388|ssn!:SSN without separators]]   DOB [[05/09/1979|dob]]
SPOUSE     [[Petrosyan, Anush|p2:last-first]]             SSN [[396-41-9690|ssn]]  DOB [[12/01/1982|dob]]
DEPENDENTS [[Davit|p3:first-name]] (son, DOB [[3/3/2011|dob]], SSN [[710 34 3802|ssn!:SSN with spaces]])
           [[Lilit|p4:first-name]] (daughter, DOB [[8/19/2015|dob]], SSN ends [[6134|ssn!:last four only]])
           + Niko's mother [[Gayane Sargsyan|p6:full]], lives w/ them, [[no SSN -- ITIN applied for|attr!:immigration-related tax status]],
             [[green card pending|attr:immigration status]]. Check qualifying relative test (her income = [[$0|money]]).
Address    [[1630 Glenoaks Blvd #207|addr]], [[Glendale|place:city]], [[CA|place:state]] [[91201-2214|zip:ZIP+4]]
Phone      [[818-555-0156|phone]] (Niko)  [[818-555-0184|phone]] (Anush, prefers text)
Email      [[npetrosyan.driver@mail.example|email]]
IP PIN (taxpayer): [[402918|cred:IRS identity protection PIN]]     Prior-yr AGI: [[$71,266|money]]

INCOME
- [[Anush|p2:first-name]] W-2, [[Verdugo Hills Unified School District|o3:full]] (classified staff; [[CSEA member, dues in box 14|attr:union membership]]):
  wages [[$48,902.11|money]], fed w/h [[$3,871.00|money]].
- Niko Sched C, rideshare. Form 1099-K from [[RydeLoop Technologies, Inc.|o2:full]] (payer EIN
  [[84-2917730|taxid:EIN]]): gross [[$63,418.57|money]]. [[RydeLoop|o2:short!:abbreviated organization nickname]] annual summary shows fees/commissions
  [[$15,220.04|money]] and 31,870 "online miles." Cash tips per Niko's own log: about [[2,900|money!:bare number without currency sign]].
- Interest, [[Foothill Pacific Bank|o4:full]]: [[$38.12|money]].

VEHICLE (100% business use claimed LAST year by prior preparer -- not right)
2021 Toyota Camry Hybrid, VIN [[4T1C31AK5MU558201|veh:VIN]], plate [[8XKR274|veh!:license plate, no state given]]. Placed in
service [[06/15/2021|date]]. Mileage log (app export): 38,405 total, 31,870 business =
83%. Std mileage 67 cents? CONFIRM 2025 RATE before computing. Car loan interest
[[$1,104|money]] x 83%. TNC permit + airport placard [[$312|money]]. Phone [[$85|money]]/mo x 80%.

HEALTH COVERAGE
Niko + kids on a marketplace plan via [[Covered California|o6:full]] Jan-Aug (Form 1095-A, policy
[[CC-0094417726|rec:marketplace policy number]]); APTC [[$4,216|money]] -> Form 8962, likely repayment. All on Anush's
district plan from Sept. Niko mentioned out-of-pocket costs for [[Lilit's insulin pump|health:child's medical device, implies diabetes]]
([[$2,480|money]]) -- won't clear the floor, noted only.

OTHER
- Charity: [[$1,200|money]] to [[St. Sarkis Armenian Apostolic Church|o5:full]] (letter on file). Also gave
  [[$250|money]] to [[a city council campaign|attr!:political donation]] -- told him not deductible.
- Est. tax payments: NONE made. Expect SE tax + penalty. Set up 2026 vouchers.
- Balance due est. [[$3,950|money]] fed. Refund not expected; if state refund, direct
  deposit to [[Foothill Pacific|o4:short!:abbreviated organization nickname]], RTN [[123436959|rtn]], acct [[000447190233|acct]].
- Our fee [[$485.00|money]]. Niko paid by card over the phone: Visa
  [[4248 6362 7945 8223|card:card number with spaces]], exp [[09/28|exp]], CVV [[417|cvv]]. DO NOT KEEP THIS IN THE FILE AFTER
  POSTING -- shred. ([[MO|p5:initials]])
- Portal invite sent: [[https://clients.oyelaranfinch.example/u/npetrosyan|url:portal link containing client username]]; temp password
  [[Glendale-7731|cred:temporary password]].
- Form 8879 to both for e-signature once [[Marcy|p5:first-name]] finishes review. Target [[3/20/2026|date]].
'''))

# ---------------------------------------------------------------- 49
_E49 = {"p1": "Raymond J. Blackfeather", "p2": "Chidinma Nwosu-Bergstrom", "p3": "Seamus P. O'Rourke III",
        "p4": "Mai Kou Xiong", "p5": "April Grace", "p6": "Yusuf al-Masri", "p7": "Pieter van der Meer",
        "p8": "Loretta Blackfeather", "p9": "Erik Bergstrom", "p10": "Huda al-Masri",
        "p11": "Annelies van der Meer", "p12": "Tamsin Ridgeway",
        "o1": "Redbud Hollow Veterinary Clinic, PLLC", "o2": "Grace Floral & Gifts LLC",
        "o3": "Arkansas River Drilling Supply Co.", "o4": "Masri Brothers Auto Body, Inc.",
        "o5": "The Blackfeather Family Trust", "o6": "Osage Prairie Bank"}
DOCS.append(D(49, "xlsx", "client list", "accounting", "US",
  title="Tax practice client list (individuals, businesses, contact log)",
  ents=_E49,
  distractors=["CP2000", "Form 1041", "Form 941", "EFTPS", "W-9"],
  sheets=[
    ("Individuals", [
      ["Client ID", "Name (Last, First)", "SSN", "DOB", "Spouse", "Phone", "Email", "City", "ST", "ZIP", "2025 fee"],
      ["[[C-1001|rec:client ID]]", "[[Blackfeather, Raymond J.|p1:last-first]]", "[[248-72-6134|ssn]]", dt("1958-04-17", "mm/dd/yyyy", "dob"),
       "[[Loretta Blackfeather|p8:full]]", "[[(918) 555-0111|phone]]", "[[rjblackfeather@mail.example|email]]", "[[Tulsa|place:city]]", "[[OK|place!:state abbreviation that is also a word]]", "[[74104|zip]]", amt(425)],
      ["[[C-1002|rec:client ID]]", "[[Nwosu-Bergstrom, Chidinma|p2:last-first]]", "[[647-44-5874|ssn]]", dt("1984-11-30", "mm/dd/yyyy", "dob"),
       "[[Erik Bergstrom|p9:full]]", "[[918.555.0162|phone:dotted]]", "[[chidi.nb@mail.example|email]]", "[[Broken Arrow|place!:city name made of common words]]", "OK", "[[74012|zip]]", amt(610)],
      ["[[C-1003|rec:client ID]]", "[[O'Rourke, Seamus P., III|p3:last-first]]", "[[722-01-6161|ssn]]", dt("1971-02-08", "mm/dd/yyyy", "dob"),
       "", "[[539-555-0125|phone]]", "", "[[Sand Springs|place:city]]", "OK", "[[74063|zip]]", amt(425)],
      ["[[C-1004|rec:client ID]]", "[[Xiong, Mai Kou|p4:last-first]]", num(628435852, "ssn!:SSN stored as a number, no separators"), dt("1990-06-21", "mm/dd/yyyy", "dob"),
       "", "[[+1 918 555 0190|phone!:international format]]", "[[maikou.xiong@mail.example|email]]", "Tulsa", "OK", "[[74136|zip]]", amt(295)],
      ["[[C-1005|rec:client ID]]", "[[Grace, April|p5:last-first]]", "[[886-06-7741|ssn]]", dt("1966-09-12", "mm/dd/yyyy", "dob"),
       "", "[[918-555-0137 ext 22|phone!:phone with extension]]", "[[agrace@gracefloral.example|email]]", "[[Jenks|place:city]]", "OK", "[[74037|zip]]", amt(540)],
      ["[[C-1006|rec:client ID]]", "[[al-Masri, Yusuf|p6:last-first]]", "[[059-02-3282|ssn]]", dt("1979-01-03", "mm/dd/yyyy", "dob"),
       "[[Huda al-Masri|p10:full!:surname with lower-case particle]]", "[[918 555 0174|phone!:spaces only]]", "[[yusuf@masribros.example|email]]", "[[Owasso|place:city]]", "OK", "[[74055|zip]]", amt(610)],
      ["[[C-1007|rec:client ID]]", "[[van der Meer, Pieter|p7:last-first]]", "[[xxx-xx-8126|ssn!:masked SSN]]", dt("1934-03-29", "mm/dd/yyyy", "dob"),
       "", "", "", "[[Bixby|place:city]]", "OK", "[[74008|zip]]", amt(850)],
    ]),
    ("Businesses", [
      ["Client ID", "Legal name", "Short name", "EIN", "Contact", "Phone", "EFTPS bank", "Routing", "Account", "Monthly fee"],
      ["[[B-2001|rec:client ID]]", "[[Redbud Hollow Veterinary Clinic, PLLC|o1:full]]", "[[Redbud Vet|o1:short!:abbreviated organization nickname]]", "[[73-1418820|taxid:EIN]]",
       "[[Dr. Chidinma Nwosu-Bergstrom|p2:full!:full name with title]]", "[[918-555-0143|phone]]", "[[Osage Prairie Bank|o6:full]]", "[[104745384|rtn]]", "[[7700418823|acct]]", amt(650)],
      ["[[B-2002|rec:client ID]]", "[[Grace Floral & Gifts LLC|o2:full]]", "[[Grace Floral|o2:short!:abbreviated organization nickname]]", "[[82-4017395|taxid:EIN]]",
       "[[April Grace|p5:full!:both names are also common words]]", "918-555-0137 ext 22", "Osage Prairie Bank", "104745384", "[[7700502961|acct]]", amt(300)],
      ["[[B-2003|rec:client ID]]", "[[Arkansas River Drilling Supply Co.|o3:full]]", "[[ARDS|o3:acronym]]", "[[73-0992714|taxid:EIN]]",
       "[[Seamus O'Rourke|p3:short!:name without middle initial or suffix]]", "[[918-555-0108|phone]]", "", "", "", amt(1200)],
      ["[[B-2004|rec:client ID]]", "[[Masri Brothers Auto Body, Inc.|o4:full]]", "[[Masri Bros.|o4:short!:abbreviated organization nickname]]", "[[46-3381902|taxid:EIN]]",
       "[[Yusuf al-Masri|p6:full!:surname with lower-case particle]]", "[[918-555-0129|phone]]", "", "", "", amt(475)],
      ["[[B-2005|rec:client ID]]", "[[The Blackfeather Family Trust|o5:full]]", "", "[[88-6120447|taxid:EIN]]",
       "[[Raymond Blackfeather|p1:short:name without middle initial]], trustee", "(918) 555-0111", "", "", "", amt(0)],
    ]),
    ("Contact log", [
      ["Date", "Client", "By", "Note"],
      [dt("2026-01-12", "d-mmm-yy", "date!:day-first date with two-digit year"), "C-1004", "[[TR|p12:initials]]", "[[Mai Kou|p4:first-name]] called about IRS letter CP2000; proposed additional tax [[$1,912|money]]. She thinks it is the brokerage sale. Sending the notice by portal."],
      [dt("2026-01-20", "d-mmm-yy", "date!:day-first date with two-digit year"), "C-1007", "TR", "[[Pieter|p7:first-name]] died [[11/02/2025|date:date of death]] ([[age 91|age]]). [[His daughter|indirect!:family relationship]] [[Annelies van der Meer|p11:full!:surname with lower-case particles]] has power of attorney and is executor; cell [[720-555-0166|phone]]. Final return plus Form 1041 for the estate."],
      [dt("2026-02-03", "d-mmm-yy", "date!:day-first date with two-digit year"), "B-2002", "TR", "[[April|p5:first-name!:first name that is also a month]] wants the monthly fee charged to the card on file: Amex [[3481 076633 67294|card!:15-digit card with spaces]], exp [[11/27|exp]], code [[5521|cvv!:4-digit security code]]."],
      [dt("2026-02-17", "d-mmm-yy", "date!:day-first date with two-digit year"), "C-1003", "[[Tamsin Ridgeway|p12:full]]", "[[Wage garnishment for child support|attr!:court-ordered garnishment]] showed up on his W-2 detail. Do not discuss with the former spouse, who still calls the office."],
      [dt("2026-03-05", "d-mmm-yy", "date!:day-first date with two-digit year"), "B-2004", "TR", "[[Yusuf|p6:first-name]] asked for a W-9 for a new insurer. [[Huda|p10:first-name]] now signs Form 941; update the EFTPS enrollment."],
      [dt("2026-03-09", "d-mmm-yy", "date!:day-first date with two-digit year"), "C-1001", "TR", "[[Ray|p1:nickname]] and [[Loretta|p8:first-name]] moved to [[2207 S. Florence Pl.|addr]], same ZIP. Trust return due as usual."],
    ]),
  ]))

# ---------------------------------------------------------------- 50
_E50 = {"p1": "Maëlle Tremblay-Fortin", "p2": "Harjit Singh Dhaliwal", "p3": "Brigid Ó Conaill",
        "p4": "Wayne Kaslo", "p5": "Shelagh MacEachern", "p6": "Jun-seo Baek",
        "o1": "Kootenay Ridge Millwork Ltd.", "o2": "Selkirk Summit Builders Inc.",
        "o3": "Dhaliwal Custom Homes", "o4": "Dunmore Joinery Teoranta",
        "o5": "Slocan Valley School District No. 8", "o6": "Baek & MacEachern Architecture Corp.",
        "o7": "Kaslo Lakefront Cabins"}
DOCS.append(D(50, "xlsx", "accounts receivable ledger", "accounting", "CA",
  title="Accounts receivable aging and customer master (BC millwork shop)",
  ents=_E50,
  distractors=["Net 30", "GST/BN", "2% 10 Net 30", "COD", "Days out"],
  sheets=[
    ("AR aging", [
      ["Invoice", "Invoice date", "Customer", "Amount", "Paid", "Balance", "Days out", "Comment"],
      ["[[KR-10418|rec:invoice number]]", dt("2025-11-14", "yyyy-mm-dd"), "[[Selkirk Summit Builders Inc.|o2:full]]", amt(18450.00, "cad"), amt(18450.00, "cad"), amt(0, "cad"), 0, "paid in full"],
      ["[[KR-10431|rec:invoice number]]", dt("2025-12-02", "yyyy-mm-dd"), "[[Dhaliwal Custom Homes|o3:full]]", amt(7312.50, "cad"), amt(3000.00, "cad"), amt(4312.50, "cad"), 149, "[[Harjit|p2:first-name]] promised the rest after the [[Fernie|place:city]] closing"],
      ["[[KR-10440|rec:invoice number]]", dt("2025-12-19", "yyyy-mm-dd"), "[[Kaslo Lakefront Cabins|o7:full]]", amt(2264.85, "cad"), amt(0, "cad"), amt(2264.85, "cad"), 132, "cheque [[#0417|rec!:cheque number]] returned NSF, fee [[C$45.00|money]] added"],
      ["[[KR-10452|rec:invoice number]]", dt("2026-01-15", "yyyy-mm-dd"), "[[Dunmore Joinery Teoranta|o4:full]]", amt(12980.00, "cad"), amt(13480.00, "cad"), amt(-500.00, "numacct", "money!:negative in parentheses, no currency sign"), 105, "overpaid by wire; refund to IBAN [[IE58 AIBK 0478 4413 2806 93|iban:IBAN with spaces]], BIC [[AIBKIE2D|acct!:SWIFT code]]"],
      ["[[KR-10467|rec:invoice number]]", dt("2026-02-06", "yyyy-mm-dd"), "[[Slocan Valley School District No. 8|o5:full]]", amt(31075.20, "cad"), amt(0, "cad"), amt(31075.20, "cad"), 83, "PO [[SD8-26-00319|rec:purchase order number]]; waiting on board approval"],
      ["[[KR-10471|rec:invoice number]]", dt("2026-02-20", "yyyy-mm-dd"), "Selkirk Summit Builders Inc.", amt(9940.00, "cad"), amt(0, "cad"), amt(9940.00, "cad"), 69, ""],
      ["[[KR-10480|rec:invoice number]]", dt("2026-03-11", "yyyy-mm-dd"), "[[Baek & MacEachern Architecture Corp.|o6:full]]", amt(4200.00, "cad"), amt(4200.00, "cad"), amt(0, "cad"), 0, "paid by Visa ending [[0095|card!:last four only]]"],
      ["[[KR-10488|rec:invoice number]]", dt("2026-03-27", "yyyy-mm-dd"), "Dhaliwal Custom Homes", amt(15620.00, "cad"), amt(0, "cad"), amt(15620.00, "cad"), 34, "stairs for the [[Dhaliwal|p2:surname]] spec house on [[Granite Road|place!:street used as a location]]"],
      ["[[KR-10493|rec:invoice number]]", dt("2026-04-09", "yyyy-mm-dd"), "Kaslo Lakefront Cabins", amt(1188.60, "cad"), amt(0, "cad"), amt(1188.60, "cad"), 21, "COD from now on per [[Maëlle|p1:first-name!:first name with diacritic]]"],
      ["", "", "TOTAL", amt(103031.15, "cad"), amt(39130.00, "cad"), amt(63901.15, "cad"), "", "as at [[April 30, 2026|date:aging date]]"],
    ]),
    ("Customers", [
      ["Customer", "Contact", "Phone", "Email", "Street", "City", "Prov", "Postal", "GST/BN or SIN", "Terms"],
      ["Selkirk Summit Builders Inc.", "[[Shelagh MacEachern|p5:full]]", "[[250-555-0119|phone]]", "[[ap@selkirksummit.example|email]]", "[[1402 Lakeside Drive, Unit 3|addr]]", "[[Nelson|place!:city name that is also a personal name]]", "[[BC|place:province]]", "[[V1L 6B9|zip:Canadian postal code]]", "[[70412 6689 RT0001|taxid!:Canadian business number]]", "Net 30"],
      ["Dhaliwal Custom Homes", "[[Harjit Singh Dhaliwal|p2:full]] (sole proprietor)", "[[(250) 555-0183|phone]]", "[[harjit@dhaliwalhomes.example|email]]", "[[RR 2, Site 14, Comp 9|addr!:rural route address]]", "[[Castlegar|place:city]]", "BC", "[[V1N 4T5|zip:Canadian postal code]]", "SIN [[764 614 665|taxid!:Canadian SIN with spaces]]", "Net 30"],
      ["Kaslo Lakefront Cabins", "[[Wayne Kaslo|p4:full!:surname that is also the town name]]", "[[250 555 0147|phone!:spaces only]]", "[[wayne at kaslocabins dot example|email!:email written out in words]]", "[[PO Box 88|addr:PO Box]]", "[[Kaslo|place:village]]", "BC", "[[V0G 1M0|zip:Canadian postal code]]", "not registered", "COD"],
      ["Dunmore Joinery Teoranta", "[[Brigid Ó Conaill|p3:full!:surname with diacritic]]", "[[+353 91 555 0123|phone!:Irish number, international format]]", "[[brigid@dunmorejoinery.example|email]]", "[[Unit 6, Ballybrit Business Park|addr]]", "[[Galway|place:city]]", "", "[[H91 X4K7|zip!:Irish Eircode]]", "VAT [[IE6388047V|taxid!:Irish VAT number]]", "Prepaid wire"],
      ["Baek & MacEachern Architecture Corp.", "[[Jun-seo Baek|p6:full!:hyphenated, multi-part or accented name]]", "[[604-555-0158 x 31|phone!:phone with extension]]", "[[jbaek@bmarch.example|email]]", "[[300-1090 Homer Street|addr!:unit-first Canadian address]]", "[[Vancouver|place:city]]", "BC", "[[V6B 2W9|zip:Canadian postal code]]", "[[81977 0234 RT0001|taxid!:Canadian business number]]", "2% 10 Net 30"],
      ["Slocan Valley School District No. 8", "accounts payable", "[[250-555-0101|phone]]", "[[payables@sd8.example|email]]", "[[811 Stanley Street|addr]]", "Nelson", "BC", "[[V1L 1N8|zip:Canadian postal code]]", "", "Net 30"],
    ]),
  ]))

# ---------------------------------------------------------------- 51
DOCS.append(D(51, "pdf", "penalty abatement request letter", "accounting", "US",
  title="Request for first-time and reasonable-cause penalty abatement (Form 941)",
  ents={"p1": "María José Fernández de Córdoba", "p2": "Desmond Achebe-Whitlow", "p3": "Luz Fernández",
        "o1": "Three Sisters Tamales LLC", "o2": "Achebe-Whitlow & Sato, CPAs, P.A.",
        "o3": "Presbyterian Rio Grande Medical Center", "o4": "Sandia Crest Payroll Co."},
  distractors=["Form 941", "IRC § 6656", "IRM 20.1.1.3.2", "Form 2848", "Ogden, UT 84201-0038", "CP276B", "Internal Revenue Service"],
  body=r'''
# [[Achebe-Whitlow & Sato, CPAs, P.A.|o2:full]]
[[6100 Uptown Blvd NE, Suite 420|addr]], [[Albuquerque|place:city]], [[NM|place:state]] [[87110|zip]]
Phone [[505-555-0136|phone]] · Fax [[505-555-0137|phone:fax]] · [[www.awscpa.example|url!:firm website]]
[[March 18, 2026|date:letter date]]
Internal Revenue Service
Ogden, UT 84201-0038
**Re: Request for abatement of failure-to-deposit penalty**
Taxpayer: [[Three Sisters Tamales LLC|o1:full]]
EIN: [[85-1440927|taxid:EIN]]
Tax form and period: Form 941, quarter ended [[March 31, 2025|date:tax period end]]
Notice: CP276B dated [[February 9, 2026|date:notice date]]
Penalty assessed: [[$4,317.82|money]]
To whom it may concern:
We represent the taxpayer named above under the enclosed Form 2848 (CAF no. [[0314-88271-R|govid:IRS CAF number]]). On the taxpayer's behalf we respectfully request abatement of the failure-to-deposit penalty assessed under IRC § 6656 for the first quarter of 2025, on the grounds of reasonable cause and, in the alternative, under the first-time abatement policy in IRM 20.1.1.3.2.
**Facts.** [[Three Sisters|o1:short!:abbreviated organization nickname]] is a family restaurant and wholesale kitchen with eleven employees. Its sole managing member, [[María José Fernández de Córdoba|p1:full!:multi-part name with diacritics]] (SSN ending [[4099|ssn!:last four only]]), personally handled every payroll tax deposit from the company's formation in 2019 through January 2025, and every deposit in that period was made on time and in full.
On [[February 11, 2025|date:hospital admission date]] [[Ms. Fernández de Córdoba|p1:title-surname!:title + hyphenated or multi-part surname]] suffered an [[ischemic stroke|health:diagnosis]] at work and was admitted to [[Presbyterian Rio Grande Medical Center|o3:full]]. She remained an inpatient until [[March 6, 2025|date:discharge date]] and was then in [[inpatient rehabilitation for aphasia|health:treatment]] until [[April 22, 2025|date]]. During that period she could not speak on the telephone, read numbers reliably, or use a computer. A letter from her treating neurologist is enclosed.
No one else at the company had access to the electronic deposit system. [[Her daughter|indirect!:family relationship]], [[Luz Fernández|p3:full!:hyphenated, multi-part or accented name]], kept the kitchen open and paid the employees by handwritten check, but did not know that deposits were due. The semiweekly deposits for the pay dates between February 14 and March 28, totalling [[$31,609.44|money]], were therefore not made when due.
**Correction.** As soon as Ms. Fernández de Córdoba was able to review the mail, the company deposited the full amount on [[April 29, 2025|date:deposit date]], filed the return on time, and engaged [[Sandia Crest Payroll Co.|o4:full]] to make all future deposits. Every deposit since has been timely. The company has no penalties in the prior three years.
**Request.** The taxpayer exercised ordinary business care and prudence and was prevented from complying by the sudden, serious illness of the only person responsible. We ask that the penalty of $4,317.82 and the related interest be abated in full. My direct line is [[(505) 555-0139|phone]] and my email address is [[dachebe@awscpa.example|email]] if you need anything further.
Respectfully,
[[Desmond Achebe-Whitlow|p2:full!:hyphenated, multi-part or accented name]], CPA
[[New Mexico|place:state]] license no. [[CPA-7714|govid:CPA license number]] · PTIN [[P01847733|govid:preparer tax identification number]]
Enclosures: Form 2848; physician letter; deposit confirmations
cc: [[M. J. Fernández de Córdoba|p1:short!:initials + surname]], [[412 Atrisco Vista Rd SW|addr]], Albuquerque, NM [[87121|zip]]
'''))

# ---------------------------------------------------------------- 52
DOCS.append(D(52, "txt", "year-end close memo", "accounting", "US", length="long",
  title="Controller's year-end close memo to outside accountants",
  ents={"p1": "Rosalyn Tsosie-Baker", "p2": "Hank Dellaria", "p3": "Grant Hollingsworth", "p4": "Reid Hollingsworth",
        "p5": "Jordan Yazzie", "p6": "Paloma Guerrero-Stein", "p7": "DeShawn Carter", "p8": "Brittany Kowalski",
        "p9": "Lucinda Whitcombe", "p10": "Winona Hollingsworth", "p11": "Aurelio Benavidez",
        "o1": "Juniper Mesa Outfitters, Inc.", "o2": "Whitcombe Dellaria LLP", "o3": "Ponderosa National Bank",
        "o4": "Kaibab Credit Union", "o5": "Four Peaks Commercial Finance", "o6": "Bergkamm Zelte GmbH",
        "o7": "Hollingsworth Peak Properties, LLC", "o8": "Tallyho Payments", "o9": "Coconino Trail Runners Association",
        "o10": "Red Rock Guide Service L.L.C.", "o11": "Benavidez Employment Law, PLC"},
  distractors=["ASC 842", "ASC 450", "Form 1120-S", "Form W-2", "FIFO", "Section 179", "A.R.S. § 23-1501", "Q4", "Ford Transit", "December"],
  ok=["12 x 2"],
  body=r'''
[[JUNIPER MESA OUTFITTERS, INC.|o1:caps]]
MEMORANDUM

TO:      [[Hank Dellaria|p2:full]], CPA, and [[Lucinda Whitcombe|p9:full]], CPA -- [[Whitcombe Dellaria LLP|o2:full]]
FROM:    [[Rosalyn Tsosie-Baker|p1:full!:hyphenated, multi-part or accented name]], Controller ([[rtsosiebaker@junipermesa.example|email]], [[928-555-0115|phone]])
DATE:    [[January 23, 2026|date:memo date]]
RE:      FY2025 year-end close -- open items before you start fieldwork [[Feb. 9|date!:abbreviated date without year]]

[[Hank|p2:first-name]] -- here is everything I know of that is unusual in the [[12/31/2025|date:balance sheet date]] close,
in trial balance order. The TB, bank recs and subledgers are in the shared
folder. Call my cell ([[928.555.0170|phone:dotted]]) rather than the store line; I am only in
[[Flagstaff|place:city]] Tuesday through Thursday.

1. CASH
Operating account at [[Ponderosa National Bank|o3:full]] (acct ending [[3318|acct!:last four only]]): book balance
[[$214,907.33|money]], reconciled. Four checks over 90 days outstanding, total
[[$3,412.00|money]]; the largest is ck [[#20841|rec!:check number]] for [[$1,950.00|money]] to the
[[Coconino Trail Runners Association|o9:full]] (race sponsorship) -- they say they never
got it. I will void and reissue in January.
Payroll account ([[Ponderosa|o3:short!:abbreviated organization nickname]], ending [[3326|acct!:last four only]]): [[$18,220.14|money]]. Reconciled to zero
after the [[1/2/2026|date]] payroll cleared.
Money market at [[Kaibab Credit Union|o4:full]], member no. [[0061-4472|acct:credit union member number]]: [[$402,655.80|money]]
including [[$1,318.44|money]] December dividend that I accrued.
[[Tallyho Payments|o8:full]] (card processor) had [[$27,364.19|money]] in transit at year end; it
settled [[1/3/2026|date]] and [[1/5/2026|date]]. One chargeback of [[$1,286.00|money]] is still in dispute
(customer card ending [[4609|card!:last four only]], a guided-trip deposit).
FYI the online banking user ID is [[jmo_controller|cred:username]] and the token PIN is
[[7731|cred!:PIN]] -- [[Lucinda|p9:first-name]] asked for read-only access last year; please ask
Ponderosa for your own login this time rather than using mine.

2. ACCOUNTS RECEIVABLE
Total AR [[$61,480.25|money]]. Almost all is wholesale/guide accounts. The one
problem is [[Red Rock Guide Service L.L.C.|o10:full]], [[$14,300.00|money]], now 140 days. The
owner told [[Grant|p3:first-name]] in November that he is [[filing Chapter 7|attr!:bankruptcy filing]]. I reserved
100%. Allowance otherwise unchanged at [[$2,500|money]].

3. INVENTORY
Physical count was [[January 4, 2026|date:count date]] at all three stores ([[Flagstaff|place:city]], [[Sedona|place:city]],
[[Prescott|place:city]]). Count sheets signed by store managers; [[Jordan Yazzie|p5:full!:first name that is also a country]] ran [[Sedona|place:city]].
Book-to-physical shrink was [[$11,902|money]] ([[$7,640|money]] of it in Sedona -- see item 9).
Ending inventory at FIFO cost [[$1,184,266|money]]. In-transit: one container of
tents from [[Bergkamm Zelte GmbH|o6:full]], invoice [[BZ-2025-11873|rec:invoice number]], EUR terms, title passed
at [[Hamburg|place:city]] [[12/18/2025|date]], so it is in inventory at [[$88,415|money]] ([[81,200 EUR|money!:currency code after amount]] at the
spot rate). We paid [[Bergkamm|o6:short!:abbreviated organization nickname]] on [[1/14/2026|date]] by wire to IBAN
[[DE22 4140 0286 5096 1416 77|iban:IBAN with spaces]], so it is in AP at year end.

4. FIXED ASSETS
Additions, all in the fixed asset schedule:
 - 2022 Ford Transit 250 cargo van bought used [[8/19/2025|date]] for [[$34,750|money]],
   VIN [[1FTBR1C82NKA40917|veh:VIN]], [[AZ|place:state]] plate [[CKH7R42|veh:license plate]]. Financed -- see item 6.
 - Electric pallet stacker for the warehouse, serial [[CRW-ES4000-2291847|dev:equipment serial number]],
   [[$9,180|money]].
 - Point-of-sale terminals for [[Prescott|place:city]] (6 units), [[$7,494|money]]. Serial numbers
   are on the invoice; the one that was stolen in the October break-in is
   S/N [[TLY8840217735|dev:device serial number]] (police report [[PPD 25-081144|rec:police report number]], insurance paid
   [[$1,049|money]] less deductible).
Grant wants Section 179 on everything that qualifies. Your call.

5. PREPAIDS AND LEASES
Store leases unchanged except Flagstaff, which is owned by [[Hollingsworth Peak Properties, LLC|o7:full]]
-- that is [[Grant's brother|indirect!:family relationship to owner]] [[Reid Hollingsworth|p4:full]]. Rent went from [[$11,500|money]] to
[[$13,000|money]] a month on [[July 1, 2025|date]] with no written amendment. I have an email
from [[Reid|p4:first-name]] only. You will want this for the related-party note and for ASC 842.
Related: the company still carries a [[$60,000|money]] note receivable from Grant
personally (the [[2023 loan for the Lake Powell houseboat|indirect!:distinctive asset]]). No payments
in 2025; interest accrued at 5%, [[$3,000|money]].

6. DEBT
[[Four Peaks Commercial Finance|o5:full]]:
 - Term loan no. [[4410-229817|rec:loan number]], balance [[$318,744.02|money]], matures [[3/1/2029|date:loan maturity date]].
 - Van loan no. [[4410-231005|rec:loan number]], balance [[$29,880.61|money]].
 - Line of credit, limit [[$500,000|money]], drawn [[$125,000|money]] at year end.
Covenant: debt service coverage 1.25x, tested annually. My calc is 1.31x
before your adjustments, so there is not much room. [[Four Peaks|o5:short!:abbreviated organization nickname]] needs
reviewed statements by [[April 30, 2026|date:reporting deadline]]. Their contact changed -- details
are in the confirmation folder.

7. PAYROLL AND ACCRUALS
Accrued wages 5 days, [[$41,277|money]]. Accrued bonuses [[$52,000|money]]: Grant [[$25,000|money]],
me [[$12,000|money]], three store managers [[$5,000|money]] each. Paid [[2/13/2026|date]].
Two things HR asked me to keep out of the general ledger descriptions:
 - [[Paloma Guerrero-Stein|p6:full!:hyphenated, multi-part or accented name]] (Sedona assistant manager, employee no. [[E-0217|rec:employee ID]]) has
   been on [[FMLA leave since October 6 for chemotherapy|health:medical leave and treatment]]. We are continuing
   her health premium, [[$843.17|money]] a month, and she owes her share, [[$212|money]] a
   month, which I have as a receivable of [[$636|money]]. Grant says forgive it.
 - [[DeShawn Carter|p7:full]] (warehouse, [[E-0164|rec:employee ID]]) has a [[child support withholding order|attr!:court-ordered garnishment]]
   from [[Maricopa County|place:county]], case [[FC2019-052288|rec:family court case number]], [[$388.50|money]] per pay period.
   December's second remittance went out late ([[1/6/2026|date]]).
Form W-2 totals tie to the 941s. Company EIN is [[86-0718834|taxid:EIN]]; state TPT
license [[21-448817|govid:state tax license number]] if you need it for the sales tax recon.

8. CREDIT CARD
Company Amex ending [[57838|card!:last five of an Amex]], December statement [[$19,206.77|money]], coded and
accrued. [[$2,140|money]] of it is Grant's family trip to [[Telluride|place:city]] -- booked to
shareholder distributions, not T&E. [[Winona Hollingsworth|p10:full]] ([[Grant's wife|indirect!:family relationship to owner]], 10%
shareholder) has a card on the same account; hers was clean.

9. CONTINGENCIES -- PLEASE READ
(a) [[Brittany Kowalski|p8:full]], the former Sedona store manager, was terminated
[[9/26/2025|date:termination date]] after the cycle counts showed the shrink in item 3. She filed
an EEOC charge ([[540-2026-00412|rec:EEOC charge number]]) on [[12/11/2025|date]] alleging [[pregnancy discrimination|health!:pregnancy, stated in a legal claim]]
and retaliation; she also cites A.R.S. § 23-1501. Our employment lawyer is
[[Aurelio Benavidez|p11:full]] of [[Benavidez Employment Law, PLC|o11:full]] ([[602-555-0122|phone]]). He says
exposure is "possible, not probable," range [[$40,000|money]] to [[$90,000|money]], insurance
retention [[$25,000|money]]. Nothing accrued. He will answer your legal letter.
[[Ms. Kowalski|p8:title-surname]] has not been charged with anything and Grant does not
want the theft suspicion written anywhere it does not need to be.
(b) Sales tax: Sedona city rate change was missed for six weeks. Under-
collected about [[$2,900|money]]. Accrued; amended return goes in with January.

10. EQUITY / OTHER
S-corp distributions [[$240,000|money]] (Grant [[$216,000|money]], [[Winona|p10:first-name]] [[$24,000|money]]) plus the
Telluride item. No new shareholders. Form 1120-S extension is fine with us
if you need it.

11. THINGS I THINK ARE FINE (so you do not spend time on them)
 - Gift cards: liability rolled forward by month, breakage recognized on the
   same 24-month pattern as last year. No change in policy.
 - Loyalty points: accrued at the redemption value times the historical
   redemption rate. The rate moved less than a point, so no true-up.
 - Returns reserve: Q4 sales were up, returns in the first three weeks of
   January ran at the usual percentage, and I left the reserve formula alone.
 - Depreciation: ran all twelve months, agreed the schedule to the ledger,
   and removed the stolen terminal and two fully depreciated display racks.
 - Prepaid insurance: the package policy renewed on the first of October and
   is amortized straight-line over twelve months, nine remaining.
 - Sales tax payable other than item 9(b): agrees to the December returns as
   filed for the state and all three cities.
 - Deferred revenue for guided trips: every booking with a trip date after
   year end is deferred at the full deposit; the schedule is by trip.
 - Vacation accrual: recalculated from the timekeeping export at current
   pay rates, capped at 80 hours per person as the handbook says.

12. WHAT I NEED FROM YOU
 - A view on whether the legal matter in item 9(a) needs disclosure under
   ASC 450 even though nothing is accrued. Grant will push back on any
   wording that names a store.
 - The lease entry for the Flagstaff rent change. I can book it once you
   tell me whether the email counts as a modification.
 - Whether the shareholder note in item 5 has to be reclassified out of
   current assets, since nobody expects it to be repaid this year.
 - Your PBC list as early as possible. Last year it arrived the Friday
   before fieldwork and we lost two days finding fixed asset invoices.
 - A draft of the covenant calculation in the lender's format before the
   statements are issued, so there are no surprises.

That is the list. I am out [[February 2|date!:date without year]] for a [[minor procedure|health!:vague medical reference]]; [[Jordan|p5:first-name!:first name that is also a country]] can pull
documents that day.

[[Roz|p1:nickname]]
'''))

# ---------------------------------------------------------------- 53
DOCS.append(D(53, "eml", "email thread", "accounting", "US", enc="base64",
  title="Email thread - missing W-9s and 1099-NEC filing",
  ents={"p1": "Constance Okafor-Bell", "p2": "Mateus Carvalho dos Santos", "p3": "Hunter Lindgren",
        "p4": "Xiomara Quiñones", "p5": "Bao Vang",
        "o1": "Okafor-Bell Bookkeeping & Tax, LLC", "o2": "Driftless Roasters Cooperative",
        "o3": "Lindgren Mechanical", "o4": "Coulee Region Design Studio LLC",
        "o5": "Mississippi Bluffs Credit Union"},
  distractors=["Form 1099-NEC", "W-9", "backup withholding", "Venmo", "January 31", "24%", "Box 1"],
  headers={"From": "[[Constance Okafor-Bell|p1:full!:hyphenated, multi-part or accented name]] <[[connie@okaforbell-books.example|email]]>",
           "To": "[[Mateus Carvalho dos Santos|p2:full!:multi-part surname]] <[[mateus@driftlessroasters.example|email]]>",
           "Subject": "Re: 1099s - still missing W-9s (3 vendors)",
           "Date": "Thu, [[15 Jan 2026|date!:day-first date with month name]] 08:52:40 -0600"},
  body=r'''
[[Mateus|p2:first-name]],

Thanks, that helps. Where we are for [[Driftless Roasters Cooperative|o2:full]] (EIN [[39-2284176|taxid:EIN]]):

DONE - I have good W-9s and totals for these two:
  * [[Lindgren Mechanical|o3:full]] ([[Hunter Lindgren|p3:full!:first name that is also a common word]], sole prop). He gave his
    SSN, [[622-58-8948|ssn]], not an EIN. 2025 payments [[$8,640.00|money]] (roaster
    repairs). Address [[N3172 County Road K|addr!:rural fire-number address]], [[Viroqua|place:city]], [[WI|place:state]] [[54665|zip]].
  * [[Coulee Region Design Studio LLC|o4:full]], EIN [[87-1930442|taxid:EIN]], [[$3,200.00|money]].
    Single-member LLC, so it still gets a Form 1099-NEC.

STILL MISSING:
  * [[Xiomara Quiñones|p4:full!:surname with diacritic]] (the farmers market staffing). You paid her
    [[$5,475|money]] by Venmo and check. The W-9 she sent has a 9-digit number
    with no dashes, [[948735521|taxid!:ITIN without separators]], which starts with a 9 - that is an
    ITIN, not an SSN. That is fine for the 1099, but please do not ask
    her about [[her immigration status|attr!:immigration status, implied]]; it is not our business and we do
    not need it. I only need her to confirm the mailing address:
    [[418 1/2 Cass St, Upper|addr!:fractional house number]], [[La Crosse|place:city]], WI [[54601|zip]]?
  * [[Bao Vang|p5:full]] (delivery driver, Jan-May). No W-9 at all. Last known
    cell [[608 555 0191|phone!:spaces only]]. If we cannot get one by the deadline we
    file with what we have and you start backup withholding at 24% on
    anything further. Paid [[$2,210.00|money]].

Totals go in Box 1. Filing deadline is January 31 so I need
answers by [[Friday the 23rd|date!:date in words without month]]. My fee for the five forms is [[$125|money]] flat,
same as last year - you can pay the invoice ([[INV-2026-0042|rec:invoice number]]) at
[[https://pay.okaforbell-books.example/i/INV-2026-0042|url:payment link containing invoice number]].

[[Connie|p1:nickname]]

--
Constance Okafor-Bell, EA
[[Okafor-Bell Bookkeeping & Tax, LLC|o1:full]]
[[211 Pearl Street, Ste B|addr]], La Crosse, WI 54601
[[(608) 555-0149|phone]]  |  fax [[(608) 555-0150|phone:fax]]

On Wed, Jan 14, 2026 at 4:17 PM Mateus Carvalho dos Santos wrote:
> Hi Connie - sorry for the delay. [[Hunter|p3:first-name!:first name that is also a common word]] dropped his form off, photo
> attached. I texted [[Xiomara|p4:first-name]] and she sent hers too. I don't have
> anything for [[Bao|p5:first-name]], he moved to [[St. Paul|place:city]] I think. Do we really
> need one from the design studio? They're an LLC.
>
> Also for your records the co-op's new checking account for your
> autopay is at [[Mississippi Bluffs Credit Union|o5:full]], routing [[067965120|rtn]],
> account [[4471002286|acct]]. Old one closes at month end.
>
> [[M.|p2:initials!:single initial sign-off]]
'''))

# ---------------------------------------------------------------- 54
DOCS.append(D(54, "md", "IT onboarding notes", "general", "US",
  title="IT onboarding checklist notes for a new hire",
  ents={"p1": "Thandiwe Mokoena-Hart", "p2": "Gus Papadakis", "p3": "Leilani Kahananui",
        "o1": "Brightwater Benefits Group, Inc.", "o2": "Northloop Managed IT"},
  distractors=["Windows 11 Pro", "ThinkPad T14", "TCP 443", "SOC 2", "Monday", "RFC 1918", "802.1X", "MFA"],
  body=r'''
# New hire IT setup — [[Thandiwe Mokoena-Hart|p1:full!:hyphenated, multi-part or accented name]] (Claims Analyst)

**Start date:** [[2026-05-18|date:hire date]] · **Manager:** [[Leilani Kahananui|p3:full]] · **Employee ID:** [[BBG-00618|rec:employee ID]]
**Ticket:** [[NL-48213|rec:help desk ticket number]] · **Tech:** [[Gus Papadakis|p2:full]] ([[Northloop Managed IT|o2:full]], [[612-555-0177|phone]])

> Internal use only. Do not paste this page into chat tools. — [[GP|p2:initials]]

## 1. Accounts

| System | Username | Notes |
|---|---|---|
| Microsoft 365 | [[tmokoenahart@brightwaterbenefits.example|email]] | MFA enrolled Monday, authenticator app |
| Claims platform | [[tmokoena-hart|cred:username]] | role: analyst-L1 |
| VPN | [[bbg\tmokoenahart|cred!:domain username with backslash]] | cert expires [[2027-05-18|date]] |
| Payroll self-service | [[618THM|cred!:short username]] | she sets her own password at first login |

- Temporary password for all of the above: [[Welcome!Lake26|cred:temporary password]] — forced change at first sign-in.
- Door badge no. [[0047731|rec:badge number]]; alarm PIN [[5820|cred!:PIN]] (shared with the claims pod, yes I know).
- She asked us to use "[[Thandi|p1:nickname]]" as her display name. Legal name stays in HR.

## 2. Hardware

- Laptop: ThinkPad T14 Gen 4, serial **[[PF4XK2M9|dev:laptop serial number]]**, asset tag [[BBG-LT-0392|dev:asset tag]], Windows 11 Pro.
  - Wi-Fi MAC `[[3C:6A:A7:1B:90:4E|dev:MAC address]]`, dock Ethernet MAC `[[00-E0-4C-68-3A-17|dev!:MAC address with dashes]]`
  - BitLocker recovery key ID [[7F2C19A4|cred!:recovery key identifier]] escrowed to the tenant
- Phone: company iPhone, IMEI [[35 693803 564380 9|dev!:IMEI with spaces]], number [[(612) 555-0193|phone]]
- Monitor x2 from stock, no serials tracked.

## 3. Network

- Static DHCP reservation `[[10.40.12.57|ip:private IPv4]]` on VLAN 40 (claims). Printer is `[[10.40.12.9|ip:private IPv4]]`.
- VPN concentrator: `[[vpn.brightwaterbenefits.example|url!:hostname]]` → [[203.0.113.18|ip]] (TCP 443). IPv6 is `[[2001:db8:40:12::57|ip!:IPv6 address]]` if she ends up on the new stack.
- Home IP allow-listed for the first two weeks while her token ships: [[198.51.100.203|ip]]. Remove by [[June 1, 2026|date]].
- 802.1X on the wired ports; the private ranges are the usual RFC 1918 space.

## 4. HR / accommodation items passed to IT

- [[Leilani|p3:first-name]] forwarded an approved accommodation: [[screen reader (JAWS) and a 27-inch high-contrast display|health!:disability accommodation]] — Thandi has [[low vision|health:disability]]. Software licence key is in the vault, not here.
- She needs the laptop shipped, not picked up: [[5121 Xerxes Ave S, Apt 3|addr]], [[Minneapolis|place:city]], [[MN|place:state]] [[55410|zip]]. Signature required.
- Personal email for the shipping notice: [[thandi.mh@mail.example|email]]. Personal cell [[651.555.0128|phone:dotted]].

## 5. Open items

1. Claims platform vendor still has to approve the seat (SOC 2 access review) — [[Gus|p2:first-name]] chasing.
2. Add to the `claims-phi` group only after HIPAA training is logged.
3. Confirm with [[Brightwater Benefits Group, Inc.|o1:full]] HR whether her [[work authorization (H-1B transfer)|attr:immigration status]] start date changes anything for payroll access. Not an IT question but it came to us.
4. Intranet profile: [[https://intranet.brightwaterbenefits.example/people/tmokoenahart|url:profile link containing username]]
'''))

# ---------------------------------------------------------------- 55
DOCS.append(D(55, "txt", "estate tax return notes", "accounting", "CA",
  title="Working notes - final T1 and T3 estate return (Ontario)",
  ents={"p1": "Margaret-Anne Fairweather", "p2": "Alasdair Fairweather", "p3": "Catriona Fairweather-Menzies",
        "p4": "Gurpreet Bhullar", "p5": "Yvette Laframboise",
        "o1": "Rideau Lakes Credit Union", "o2": "Estate of Margaret-Anne Fairweather",
        "o3": "Lanark Highlands Hospice Society", "o4": "Laframboise Wills & Estates Professional Corporation",
        "o5": "Bhullar Chartered Professional Accountants"},
  distractors=["T3", "TX19", "Part XIII", "NR4", "subsection 70(5)", "RRIF", "TFSA", "CPP"],
  body=r'''
[[Bhullar Chartered Professional Accountants|o5:full]]
File: [[EST-25-077|rec:file number]] -- [[FAIRWEATHER ESTATE|o2:caps]]          notes by [[G. Bhullar|p4:short:initial + surname]], [[14-Apr-2026|date!:day-first date with month name]]

Deceased:  [[Margaret-Anne Fairweather|p1:full!:hyphenated, multi-part or accented name]] ("[[Peggy|p1:nickname]]"), SIN [[540 570 496|taxid!:Canadian SIN with spaces]]
           b. [[17 Nov 1928|dob!:day month year]], d. [[2 Aug 2025|date!:date of death]] ([[aged 96|age]]), widow, resident of
           [[Perth|place!:town name shared with larger cities]], [[Ontario|place:province]] all year.
Executor:  [[her son|indirect!:family relationship to deceased]] [[Alasdair Fairweather|p2:full]], [[61 Drummond St. E.|addr]], Perth [[ON|place!:province abbreviation that is also a word]] [[K7H 1G3|zip:Canadian postal code]]
           tel [[613-555-0138|phone]], [[alasdair.fairweather@mail.example|email]]
Lawyer:    [[Yvette Laframboise|p5:full]], [[Laframboise Wills & Estates Professional Corporation|o4:full]]
           (probate granted [[9 Jan 2026|date!:day-first date with month name]], court file [[CV-25-00412-ES|rec:court file number]])
Estate trust account no. (CRA): [[T 4418 7702|taxid!:trust account number with spaces]]

FINAL T1 (Jan 1 - Aug 2, 2025) -- due [[April 30, 2026|date:filing deadline]], balance owing likely
 - OAS/CPP/pension to date of death: [[$31,406|money]]
 - RRIF at [[Rideau Lakes Credit Union|o1:full]], plan no. [[RLF-0028841|acct!:registered plan number]]: FMV at death
   [[$188,930.12|money]], no qualifying survivor, so fully included in income. Ouch.
 - Deemed disposition, subsection 70(5): non-registered portfolio, ACB
   [[$96,000|money]] vs FMV [[$141,750|money]] -> gain [[$45,750|money]].
 - House, [[9 Mill Lane|addr]], Perth: principal residence, exempt. Sold [[11 Dec 2025|date!:sale date]]
   for [[$612,000|money]] -- gain since death ([[12k|money!:abbreviated amount without currency sign]]) belongs on the T3, not here.
 - Medical: [[$22,480|money]] to the retirement home, incl. the [[memory care wing|health!:implies dementia care]]
   surcharge from March. Attendant care certificate on file ([[Alzheimer's|health:diagnosis]]).
 - Donations by will: [[$20,000|money]] to [[Lanark Highlands Hospice Society|o3:full]]; [[$5,000|money]] to
   [[the Kirk session|attr!:religious affiliation, implied]] of her church. Claim on final T1 or T3 -- model both.

T3 FOR THE ESTATE (GRE, first year-end [[1 Aug 2026|date!:day-first date with month name]])
 - TFSA at [[RLCU|o1:acronym]], no. [[TF-7741093|acct!:registered plan number]], [[$74,215|money]] at death; growth after death
   [[$1,102|money]] is taxable to the estate.
 - CPP death benefit [[$2,500|money]].
 - 2014 Subaru Forester, plate [[CKLM 418|veh:license plate]], VIN [[JF2SJCDC5EH447120|veh:VIN]], sold to
   a neighbour for [[$6,000|money]]. Personal-use property, loss denied.
 - The [[1958 cedar-strip launch "Heather Belle"|indirect!:distinctive named boat]] kept at [[Otty Lake|place:lake]] -- appraised
   [[$18,500|money]], going in specie to Alasdair. Listed personal property? Check.

BENEFICIARIES
 - [[Alasdair|p2:first-name]], 50%. SIN [[364-364-513|taxid:Canadian SIN]].
 - [[Catriona Fairweather-Menzies|p3:full!:hyphenated, multi-part or accented name]] ([[daughter|indirect!:family relationship]]), 50%. Lives in [[Inverness|place:city]],
   [[non-resident of Canada since 1998|attr:tax residency status]] -> Part XIII withholding 25% on
   income distributions, NR4 slip. UK NI no. for her adviser: [[JG 10 37 59 A|govid!:National Insurance number]].
   Her share to be wired to IBAN [[GB90 HBUK 1941 5563 0721 37|iban:IBAN with spaces]] once clearance arrives.

TO DO
 - TX19 clearance certificate request after assessments. Hold back [[$40,000|money]].
 - Ask [[Mme Laframboise|p5:title-surname!:French title + surname]] for the passed accounts.
 - Fee estimate to [[Mr. Fairweather|p2:title-surname]]: [[$4,200|money]] plus HST. He wants to pay by
   e-transfer to [[payments@bhullarcpa.example|email]].
 - [[Peggy's|p1:nickname!:possessive nickname]] 2024 return was never filed (in hospital Feb-Apr 2025 with a
   [[broken hip|health:injury]]). File late with the final.
'''))

# ---------------------------------------------------------------- 56
DOCS.append(D(56, "txt", "care plan note", "health", "US",
  title="Nursing home quarterly care plan note",
  ents={"p1": "Eleanor Whitehorse-Dubois", "p2": "Renata Dubois-Kim", "p3": "Olumide Fashola",
        "p4": "Kristy Vandersloot", "p5": "Faith Morningstar",
        "o1": "Cedar Hollow Care & Rehabilitation Center", "o2": "Bitterroot Long-Term Care Pharmacy"},
  distractors=["MDS", "BIMS", "Braden", "PRN", "POLST", "IDT", "Tylenol"],
  body=r'''
[[CEDAR HOLLOW CARE & REHABILITATION CENTER|o1:caps]] -- QUARTERLY CARE PLAN NOTE
Resident: [[WHITEHORSE-DUBOIS, Eleanor|p1:last-first]] ("[[Nell|p1:nickname]]")        Room [[214-B|rec!:room and bed number]]
MRN [[CH-0038817|rec:medical record number]]   DOB [[01/26/1929|dob]] ([[97 y/o|age!:abbreviated age]])   Admit [[09/14/2023|date:admission date]]
Medicare no. [[1EG4-TE5-MK73|rec:Medicare beneficiary identifier]]    Medicaid ID [[MT00447318|rec:Medicaid ID]]
Attending: [[Olumide Fashola|p3:full]], MD (NPI [[1654581465|govid:NPI]])     IDT date: [[6/11/2026|date]]
Present: [[K. Vandersloot|p4:short:initial + surname]] RN (MDS coord.), [[Faith Morningstar|p5:full!:both names are also common words]] (social services),
dietary, activities; [[daughter/POA|indirect!:family relationship and legal role]] [[Renata Dubois-Kim|p2:full!:hyphenated, multi-part or accented name]] by phone ([[406-555-0121|phone]]).

DIAGNOSES: [[vascular dementia|health:diagnosis]] (BIMS 6, down from 8); [[CHF, EF 35%|health!:abbreviated diagnosis with lab value]];
[[stage 2 pressure injury, sacrum|health:diagnosis]] (noted [[5/29/2026|date]], 1.5 x 1 cm, improving);
[[hx of falls|health!:abbreviated history]] -- last fall [[4/2/2026|date:date of fall]], no injury. Pacemaker in place
(model/serial on wallet card: [[PJN 7204419|dev:implanted device serial number]]), last interrogation OK.

MEDS (filled by [[Bitterroot Long-Term Care Pharmacy|o2:full]]): [[furosemide 40 mg daily|health:medication and dose]] (Rx
[[#6621047|rec:prescription number]]), [[metoprolol succinate 25 mg|health:medication and dose]], [[donepezil 10 mg at bedtime|health:medication and dose]], Tylenol PRN.
[[Quetiapine was discontinued|health:medication change]] [[5/1/2026|date]] per gradual dose reduction; no increase in
behaviors per night staff.

CODE STATUS / PREFERENCES: DNR, POLST on chart signed [[10/02/2023|date]]. Resident is
[[one of Jehovah's Witnesses -- NO blood products|attr:religion with treatment implication]]; card in chart, [[Renata|p2:first-name]] confirms.
Elders from her congregation visit Thursdays; resident enjoys this.
[[Speaks Salish with visitors|attr!:ethnicity, implied by language]] and responds better to her nickname than to
"[[Mrs. Dubois|p1:title-surname!:title + partial surname]]" -- staff reminded.

NUTRITION: weight 104 lb, down 4 lb in 90 days. Mechanical soft diet,
fortified shakes twice daily. Braden score 14.

GOALS NEXT 90 DAYS
1. Sacral wound closed by next review; turn q2h, air mattress in place.
2. No falls with injury; bed alarm, non-skid socks, toileting schedule.
3. Weight stable within 2 lb.

FAMILY / FINANCIAL: [[Ms. Dubois-Kim|p2:title-surname!:title + hyphenated or multi-part surname]] asked about the private-pay balance
([[$3,912.40|money]] for March, before Medicaid approval) and whether the personal
needs allowance ([[$50|money]]/mo) can go to the beauty shop account. Social
services to follow up with the business office. Next review [[9/10/2026|date]].
She is [[the last surviving charter resident of the facility|indirect!:unique status]]; activities
would like to mark her 100th when the time comes.

Signed: [[Kristy Vandersloot|p4:full]], RN   [[06/11/2026|date]] 15:40
'''))

# ---------------------------------------------------------------- 57
DOCS.append(D(57, "pdf", "discharge summary", "health", "US",
  title="Hospital discharge summary - NSTEMI with stent placement",
  ents={"p1": "Wendell K. Running Bear", "p2": "Soraya Haddad-Ellis", "p3": "Tobias Lundquist",
        "p4": "Charlene Running Bear",
        "o1": "Black Hills Regional Heart & Vascular Hospital", "o2": "Pine Ridge Family Health Clinic"},
  distractors=["LAD", "EF", "LDL", "Echo", "troponin", "Indian Health Service"],
  body=r'''
# [[Black Hills Regional Heart & Vascular Hospital|o1:full]]
## DISCHARGE SUMMARY
**Patient:** [[RUNNING BEAR, WENDELL K.|p1:last-first]]
**MRN:** [[BH-20447193|rec:medical record number]]
**Encounter:** [[E-90031877|rec:encounter number]]
**DOB:** [[July 4, 1967|dob:month day year]]
**Admitted:** [[05/02/2026|date:admission date]]
**Discharged:** [[05/06/2026|date:discharge date]]
**Attending:** [[Soraya Haddad-Ellis|p2:full!:hyphenated, multi-part or accented name]], MD, Cardiology (NPI [[1555306962|govid:NPI]])
**Primary care:** [[Tobias Lundquist|p3:full]], PA-C, [[Pine Ridge Family Health Clinic|o2:full]]
**Clinic phone:** [[605-555-0126|phone]]
## Reason for admission
[[Mr. Running Bear|p1:title-surname!:two-word surname made of common words]] is a 58-year-old man, an [[enrolled member of the Oglala Sioux Tribe|attr:tribal membership]], who presented to the emergency department with two hours of substernal chest pressure radiating to the left arm while loading hay. Initial troponin was elevated and rose on repeat. ECG showed ST depression in the lateral leads.
## Hospital course
He was diagnosed with a [[non-ST-elevation myocardial infarction|health:diagnosis]]. Cardiac catheterization on [[05/03/2026|date:procedure date]] showed a 90 percent lesion of the mid LAD, treated with [[one drug-eluting stent|health:procedure]]. Echo showed EF 45 percent. He had no arrhythmia on telemetry. On hospital day two he developed tremor, sweating and agitation consistent with [[alcohol withdrawal|health:substance use]]; he reports [[drinking six to eight beers nightly|health!:substance use detail]] since [[his wife's death last winter|indirect!:family event]]. He was treated on the withdrawal protocol and seen by the addiction medicine team, and he agreed to an outpatient referral. He also has [[type 2 diabetes|health:diagnosis]], previously untreated, and [[smokes a pack a day|health!:tobacco use]].
## Results at discharge
| Test | Result |
| LDL | [[162 mg/dL|health!:lab result]] |
| HbA1c | [[9.4%|health!:lab result]] |
| Creatinine | [[1.1 mg/dL|health!:lab result]] |
## Discharge medications
- [[aspirin 81 mg daily|health:medication and dose]]
- [[ticagrelor 90 mg twice daily|health:medication and dose]] for twelve months; do not stop without calling cardiology
- [[atorvastatin 80 mg nightly|health:medication and dose]]
- [[metformin 500 mg twice daily|health:medication and dose]]
- [[naltrexone 50 mg daily|health:medication for alcohol use disorder]], started [[05/05/2026|date]]
- nicotine patch, 21 mg
## Follow-up
- Cardiology clinic, [[(605) 555-0180|phone]], with [[Dr. Haddad-Ellis|p2:title-surname!:title + hyphenated or multi-part surname]] on [[May 20, 2026|date:follow-up appointment]] at 10:30
- [[Mr. Lundquist|p3:title-surname]] within one week for diabetes teaching
- Cardiac rehabilitation referral sent; the nearest program is in [[Rapid City|place!:city name made of common words]], about ninety minutes from his home near [[Kyle|place!:town name that is also a personal name]], [[SD|place:state]]
- No driving for one week; no lifting over ten pounds for five days
## Contact and coverage
His sister, [[Charlene Running Bear|p4:full!:surname made of common words]], will stay with him for two weeks and can be reached at [[605 555 0162|phone!:spaces only]]. Coverage is through the Indian Health Service purchased/referred care program, authorization no. [[PRC-26-0041882|rec:authorization number]], with Medicaid secondary (ID [[SD-774019336|rec:Medicaid ID]]). Estimated patient balance: [[$0.00|money]].
Dictated by [[S. Haddad-Ellis|p2:short!:initial + surname]], MD, on [[05/06/2026|date]] at 14:12. Electronically signed.
'''))

# ---------------------------------------------------------------- 58
DOCS.append(D(58, "txt", "patient portal message", "health", "US", length="short",
  title="Patient portal message - new insurance and refill request",
  ents={"p1": "Dolores Etxeberria", "p2": "Nomvula Mbeki"},
  distractors=["Rx", "DOB"],
  body=r'''
From: [[Dolores Etxeberria|p1:full]]   Sent: [[6/3/2026|date]] 9:12 PM   To: [[Dr. Mbeki|p2:title-surname]]'s office

hi - new insurance card came. member ID [[HZK4471902|rec:health plan member ID]], group [[88213|rec!:group number]]. can you
resend my [[lexapro 20mg|health!:medication, lower case and no space]] (Rx [[#7714402|rec:prescription number]]) to the pharmacy on [[Alder St|place!:street used as a location]]? still
getting [[the panic attacks at night|health:mental health symptom]]. DOB [[4/4/1990|dob]] if you need it. portal
keeps locking me out, username is [[lola.etx90|cred:username]]. cell [[503-555-0164|phone]]
thanks [[lola|p1:nickname:lower-case nickname]]
'''))

# ---------------------------------------------------------------- 59
DOCS.append(D(59, "docx", "accommodation letter", "health", "US",
  title="Clinician letter supporting workplace accommodation and intermittent leave",
  ents={"p1": "Min-jun Seo", "p2": "Simone Okwuosa-Laurent", "p3": "Beatriz Almeida-Novak", "p4": "Grace Seo",
        "o1": "Cascade Behavioral & Occupational Health, PLLC", "o2": "Tidemark Aerospace Components Inc.",
        "o3": "Sound Mutual Life & Disability"},
  distractors=["Form WH-380-E", "29 C.F.R. § 825.306", "ADA", "DSM-5", "Monday"],
  body=r'''
# [[Cascade Behavioral & Occupational Health, PLLC|o1:full]]
[[2811 Colby Avenue, Suite 300|addr]] · [[Everett|place:city]], [[WA|place:state]] [[98201|zip]] · Tel [[425-555-0155|phone]] · Fax [[425-555-0156|phone:fax]]
[[April 28, 2026|date:letter date]]
[[Beatriz Almeida-Novak|p3:full!:hyphenated, multi-part or accented name]], HR Business Partner
[[Tidemark Aerospace Components Inc.|o2:full]]
[[9000 Airport Road, Bldg 4|addr]]
[[Mukilteo|place:city]], WA [[98275|zip]]
**Re: [[Min-jun Seo|p1:full!:hyphenated, multi-part or accented name]] (also known at work as "[[Daniel Seo|p1:nickname:Western name used at work]]"), Employee No. [[TAC-118824|rec:employee ID]], DOB [[11/23/1988|dob]]**
**Disability claim: [[Sound Mutual Life & Disability|o3:full]], claim no. [[STD-2026-0417733|rec:claim number]]**
Dear [[Ms. Almeida-Novak|p3:title-surname!:title + hyphenated or multi-part surname]]:
I am a licensed clinical psychologist and have treated [[Mr. Seo|p1:title-surname]] since [[January 12, 2026|date:start of treatment]]. He has signed a release allowing me to share the information below, and only this information, with his employer. This letter accompanies the completed Form WH-380-E and is intended to meet the certification requirements of 29 C.F.R. § 825.306 and to support his request for reasonable accommodation under the ADA.
## Condition
Mr. Seo has [[post-traumatic stress disorder|health:mental health diagnosis]] and [[attention-deficit/hyperactivity disorder, combined presentation|health:diagnosis]], each diagnosed under DSM-5 criteria. The first is related to [[his service as an Army combat medic|indirect!:distinctive personal history]] between 2009 and 2014. Both conditions are chronic. They substantially limit concentration and sleep and, during flare-ups, his ability to tolerate sudden loud noise. He currently takes [[prazosin 2 mg at bedtime|health:medication and dose]] and [[extended-release methylphenidate 36 mg each morning|health:medication and dose]], and attends therapy weekly.
## Functional limitations and requested accommodations
Mr. Seo can perform all essential functions of his position as a quality inspector with the following adjustments:
- Reassignment from the stamping bay to an inspection station away from the drop hammers, or [[active noise-cancelling hearing protection|health!:disability accommodation]] that still meets plant safety rules
- A fixed day shift; rotating to nights has repeatedly disrupted his sleep and triggered symptoms
- Permission to bring [[his trained service dog|health!:disability accommodation]] to the administrative building for meetings; the dog would not enter the production floor
- Written rather than verbal-only instructions for changes to inspection plans
## Leave
He will need intermittent leave for treatment and for flare-ups. I estimate one half-day per week for appointments, normally Monday afternoons, and one to two full days per month for episodes that cannot be predicted. He was fully unable to work from [[March 9, 2026|date:start of leave]] through [[March 27, 2026|date:end of leave]] and was [[admitted for three nights to a crisis stabilization unit|health:psychiatric admission]] during that period. I expect the need for intermittent leave to continue for at least twelve months, after which I will reassess.
## Other
Mr. Seo's spouse, [[Grace Seo|p4:full!:first name that is also a common word]], is his emergency contact and may be called at [[(425) 555-0198|phone]] if he becomes distressed at work. Please do not contact family members for any other purpose. Questions about this letter may be sent to me at [[dr.okwuosa-laurent@cascadeboh.example|email]]; I can discuss only what is written here.
Sincerely,
[[Simone Okwuosa-Laurent|p2:full!:hyphenated, multi-part or accented name]], PsyD
Licensed Psychologist, [[Washington|place:state]] license no. [[PY60448127|govid:state professional license number]]
NPI [[1913266569|govid:NPI]]
cc: patient, by secure message
'''))

# ---------------------------------------------------------------- 60
DOCS.append(D(60, "html", "vendor contract summary", "general", "US",
  title="Order form summary - analytics software subscription",
  ents={"p1": "Anneliese Vogt-Ramirez", "p2": "Kofi Darko", "p3": "Paris Whitlock", "p4": "Jeroen de Vries",
        "o1": "Lumenstack Analytics, Inc.", "o2": "Harborview Dental Partners, P.C.",
        "o3": "Lumenstack Europe B.V.", "o4": "First Chesapeake Commercial Bank"},
  distractors=["Net 45", "SOC 2 Type II", "Section 7.2", "HIPAA", "Business Associate Agreement", "99.9%", "UTC"],
  body=r'''
# Order Form Summary — Subscription Agreement
**Agreement no.:** [[LSA-MSA-2026-00731|rec:contract number]] · **Order no.:** [[Q-118204|rec:order number]] · **Effective date:** [[07/01/2026|date:effective date]]
Prepared by procurement for internal circulation. This is a summary; the signed Master Subscription Agreement controls.
## Parties
| Role | Legal name | Address | Tax ID |
| Vendor | [[Lumenstack Analytics, Inc.|o1:full]] | [[55 Fleet Wharf, 6th Floor|addr]], [[Baltimore|place:city]], [[MD|place:state]] [[21231|zip]] | [[47-2260918|taxid:EIN]] |
| Customer | [[Harborview Dental Partners, P.C.|o2:full]] | [[1200 Light Street, Suite 2A|addr]], Baltimore, MD [[21230-4410|zip:ZIP+4]] | [[52-1873346|taxid:EIN]] |
| Vendor affiliate (EU data hosting) | [[Lumenstack Europe B.V.|o3:full]] | [[Keizersgracht 418-II|addr!:Dutch street address]], [[1016 GC|zip!:Dutch postcode]] [[Amsterdam|place:city]] | [[NL861447203B01|taxid!:Dutch VAT number]] |
## Contacts
- Vendor account executive: [[Kofi Darko|p2:full]], [[kofi.darko@lumenstack.example|email]], [[+1 (410) 555-0114|phone!:international format with parentheses]]
- Customer business owner: [[Anneliese Vogt-Ramirez|p1:full!:hyphenated, multi-part or accented name]], Chief Operating Officer, [[avogtramirez@harborviewdental.example|email]], [[410.555.0167|phone:dotted]] ext. 5
- Customer technical contact: [[Paris Whitlock|p3:full!:first name that is also a city]], IT manager, [[443-555-0133|phone]]
- EU affiliate signatory: [[Jeroen de Vries|p4:full!:surname with lower-case particle]], Director
## Commercial terms
| Item | Term |
| Initial term | [[07/01/2026|date]] to [[06/30/2029|date:end of term]] |
| Annual subscription fee | [[$84,000|money]] |
| One-time implementation | [[$12,500.00|money]] |
| Overage per provider seat | [[$95|money]] per month |
| Price cap on renewal | 5% |
| Payment terms | Net 45 |
| Total contract value | [[$264,500|money]] |
- The first invoice ([[LS-INV-044817|rec:invoice number]]) is due [[August 15, 2026|date:payment due date]].
- Annual fees are paid by ACH to the vendor's account at [[First Chesapeake Commercial Bank|o4:full]]: routing [[016990476|rtn]], account [[3300917452|acct]].
- Overage is charged monthly to the corporate card on file: Mastercard [[5120-5473-2514-8074|card:card number with dashes]], expires [[03/29|exp]], security code [[608|cvv]], in the name of [[A. Vogt-Ramirez|p1:short!:initial + surname]].
- Fees for the EU-hosted reporting module, [[EUR 6,000|money!:currency code before amount]] a year, are invoiced by [[Lumenstack Europe|o3:short!:abbreviated organization nickname]] and paid to IBAN [[NL75 ABNA 4137 1832 64|iban:IBAN with spaces]].
## Technical and security terms
- Uptime commitment of 99.9% per calendar month, measured in UTC; service credits under Section 7.2.
- Single sign-on at [[https://harborview.lumenstack.example/sso|url:customer-specific login link]]; the first administrator account is [[pwhitlock-admin|cred:username]] with initial passphrase [[tidal-crab-velvet-88|cred!:passphrase]], to be rotated at go-live.
- Vendor will accept traffic only from the customer's office addresses [[192.0.2.64|ip]] and [[192.0.2.65|ip]], and from the on-premises data gateway appliance, serial number [[LSG-2X-00417729|dev:device serial number]], at [[10.20.0.14|ip:private IPv4]].
- Vendor holds a current SOC 2 Type II report. Because the data set includes patient scheduling and billing fields, a Business Associate Agreement under HIPAA was signed with the order.
## Notes from negotiation
- [[Kofi|p2:first-name]] agreed to waive the implementation fee if the customer serves as a reference; [[Anneliese|p1:first-name]] declined because the practice [[is in sale discussions with a regional dental group|indirect!:confidential one-off transaction]] and does not want its name in vendor marketing.
- [[Paris|p3:first-name!:first name that is also a city]] asked that de-identified exports exclude the two providers who are [[the only pediatric dentists in Federal Hill|indirect!:unique role]], since they would be identifiable from volume alone.
- Renewal notice must be given by [[April 1, 2029|date:renewal notice deadline]].
- Signed for the customer by [[Ms. Vogt-Ramirez|p1:title-surname!:title + hyphenated or multi-part surname]] on [[June 12, 2026|date:signature date]]; countersigned by [[Mr. Darko|p2:title-surname]] on [[June 15, 2026|date]].
'''))

# END
