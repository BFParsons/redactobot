from corpus_src.dsl import D, dt, amt, num

DOCS = []

# ---------------------------------------------------------------- doc 1
DOCS.append(D(1, "txt", "client meeting notes", "legal", "US",
  title="Client meeting notes - divorce and custody consultation",
  ents={"p1": "Marisol Castellanos-Reyes", "p2": "Héctor Reyes Jr.", "p3": "Dana K. Liebowitz",
        "p4": "Ruth Tanaka", "p5": "Sofía Reyes", "p6": "Mateo Reyes", "p7": "Anand Krishnamurthy",
        "p8": "Grace Okonkwo-Bell", "p9": "Lucille P. Vandermeer", "p10": "Bartholomew Quigley III",
        "p11": "Guadalupe Castellanos", "p12": "Carmen Reyes",
        "o1": "Liebowitz & Marsh LLP", "o2": "Reyes Concrete & Paving, Inc.",
        "o3": "Lone Star Teachers Credit Union", "o4": "St. Brendan's Academy",
        "o5": "Quigley Family Law, P.C.", "o6": "The Rusty Spur", "o7": "Northside Elementary"},
  distractors=["Tex. Fam. Code § 153.002", "EpiPen", "Thursday", "Form 1040", "Honda Odyssey", "50/50", "288th District Court"],
  ok=["2022-2024"],
  body=r'''
PRIVILEGED & CONFIDENTIAL -- ATTORNEY WORK PRODUCT
[[Liebowitz & Marsh LLP|o1:full]] -- Family Law Group
Initial client mtg, file [[FL-2026-0318|rec:firm file number]]
[[2/10/26|date!:numeric date with two-digit year]], 10:30 am, conf rm B.  Present: [[DKL|p3:initials]], [[R. Tanaka|p4:short:initial + surname]] (paralegal), client.

CLIENT
[[Marisol Castellanos-Reyes|p1:full]] (goes by "[[Mari|p1:nickname]]"), DOB [[07/22/1984|dob]], SSN [[xxx-xx-4388|ssn!:masked SSN]].
Cell [[210.555.0164|phone:dotted]] (OK to text; do NOT leave voicemail on the
house line, [[(210) 555-0109|phone:parenthesized area code]]).
Email: [[mari.castellanos84@mailbox.example|email]] -- new account, husband doesn't know about it.
Staying w/ her sister [[Guadalupe|p11:first-name!:first name that is also a place]] at [[4417 Mesquite Hollow Dr., Apt. 12C|addr:street with apartment]],
[[San Antonio|place:city]], [[TX|place:state abbreviation]] [[78209|zip]].

SPOUSE
[[Héctor Reyes Jr.|p2:full]] ("[[Hector|p2:first-name!:first name written without accent]]" on the tax returns), born [[March 3, 1981|dob:written-out birth date]]. Owns 100% of
[[Reyes Concrete & Paving, Inc.|o2:full]] Married [[June 14, 2008|date:marriage date]] in [[Laredo|place:city]]. Separated since [[11/29/2025|date:separation date]],
when [[Mr. Reyes|p2:title-surname]] moved in with [[Grace Okonkwo-Bell|p8:full]], the company's office manager.

CHILDREN
[[Sofía|p5:first-name!:first name only, accented]] (DOB [[2011-09-02|dob:ISO format]], 8th grade at [[St. Brendan's Academy|o4:full]]) and [[Mateo|p6:first-name]] (born [[1/15/2016|dob]]).
Sofía was diagnosed with [[ADHD|health:diagnosis of a minor]] last spring and takes [[Adderall XR 10 mg|health:medication and dose]] on school days;
she sees [[Dr. Anand Krishnamurthy|p7:full:title + full name]] every other Thursday. Mateo has a [[peanut allergy|health:allergy]]
(EpiPen at school).

WHAT SHE TOLD US
1. Custody. Wants primary; husband wants 50/50. He had a [[DWI arrest in 2023|attr:criminal history]]
   ([[Bexar County|place:county]] cause no. [[CR-2023-118842|rec:criminal cause number]], pled to [[obstruction of a highway|attr!:criminal history, plea offence]],
   12 mo. deferred). He says he [[goes to AA|health!:substance-use treatment, colloquial]] but Mari found receipts from
   [[The Rusty Spur|o6:full:bar name]] in the truck. Best-interest factors under Tex. Fam. Code § 153.002
   look decent for her -- she has done all school/medical since birth.
2. Immigration. Mari [[became a U.S. citizen in 2019|attr:citizenship status]]. Hector has said he will "call
   ICE on her mother," who [[overstayed a visitor visa|attr!:immigration status of a relative]] and lives with Guadalupe.
   Told her we will document the threat; her mother needs separate counsel.
3. Money. He controls everything. [[Grace|p8:first-name!:first name that is also a common word]] has been signing company checks
   since December. Both families are [[devout Catholic|attr!:religion]]; her mother-in-law
   ("[[Doña Carmen|p12:nickname]]") is pressuring her not to file.

ASSETS / DEBTS (per client, unverified)
- House, [[218 Encino Ridge|addr]], [[Alamo Heights|place:neighbourhood]] -- bought 2014 for [[$389,000|money]]; she thinks it's
  worth "around [[six fifty|money!:amount in words without currency]]". Mortgage w/ [[Lone Star Teachers Credit Union|o3:full]],
  loan # [[0048-771203-9|rec:loan number]], bal. approx [[$214k|money!:abbreviated with k]].
- [[LSTCU|o3:acronym]] joint checking [[7730041928|acct!:unlabelled account number]]; her own savings (opened [[Jan. 5|date!:month and day only]]) acct
  ending [[6612|acct!:last four only]], about [[$3,200|money]].
- Condo in [[Port Aransas|place:town]] titled in the company's name -- the "[[Pelican unit|indirect!:distinctive asset]]".
- 2022 Ford F-250, VIN [[1FT7W2BT5NEC41873|veh:VIN]], plate [[TX KPL-4471|veh!:license plate with state prefix]], company-owned but
  his daily driver. Her 2019 Honda Odyssey is paid off.
- [[Reyes Concrete|o2:short!]] -- 2024 gross approx [[$2.1 million|money!:millions written out]]; she kept the books until 2022
  and says he runs personal expenses through the company AmEx ending [[2239|card!:last four only]].
- Her income: teacher's aide at [[Northside Elementary|o7:full]], [[$31,450|money]]/yr.

OTHER SIDE
He has retained [[Bartholomew Quigley III|p10:full]] of [[Quigley Family Law, P.C.|o5:full]]
([[bquigley@quigleyfamilylaw.example|email]], [[210-555-0177 x204|phone!:with x extension]]). [[Bart|p10:nickname]] will push mediation early.
Likely judge: [[Hon. Lucille P. Vandermeer|p9:full:honorific + full name]], 288th District Court. [[Judge Vandermeer|p9:title-surname]]
routinely orders a custody evaluation when ADHD meds are in the picture.

TO DO
- Retainer [[$5,000|money]] by cashier's check; fee agreement signed today.
- File petition + TRO request by [[Feb. 20, 2026|date:abbreviated month]].
- Get 2022-2024 joint returns (Form 1040) and company returns from the CPA.
- Send Mari the financial checklist via portal:
  [[https://portal.liebowitzmarsh.example/intake/FL-2026-0318|url:portal link containing the file number]]
- [[RT|p4:initials]] to run asset search on the Port Aransas condo.
'''))

# ---------------------------------------------------------------- doc 2
DOCS.append(D(2, "docx", "engagement letter", "legal", "US",
  title="Engagement letter - trustee representation",
  ents={"p1": "Ngozi A. Okafor", "p2": "Emeka Okafor", "p3": "Chukwuma Okafor", "p4": "Ingrid M. Halvorsen",
        "p5": "Thomas J. Achebe", "p6": "Wendy Pruitt-Sato",
        "o1": "Halvorsen Pruitt & Achebe LLP", "o2": "The Okafor Family Trust", "o3": "Okafor Pediatrics, P.C.",
        "o4": "Brindle & Vasquez CPAs", "o5": "Three Rivers Bank & Trust", "o6": "Sewickley Valley Savings Bank"},
  distractors=["Form 1041", "Rule 1.15", "IOLTA", "Standard Terms", "January", "Orphans' Court Division"],
  body=r'''
# [[Halvorsen Pruitt & Achebe LLP|o1:full]]
Attorneys at Law
[[600 Grant Street, 41st Floor|addr:street with floor]]
[[Pittsburgh|place:city]], [[Pennsylvania|place:state]] [[15219-2702|zip:ZIP+4]]
Tel. [[412-555-0118|phone]] / Fax [[412-555-0119|phone:fax]]

[[January 22, 2026|date:letter date]]
**VIA EMAIL ([[ngozi.okafor@okafortrust.example|email]]) AND FIRST-CLASS MAIL**
[[Ms. Ngozi A. Okafor|p1:full:title + full name]], Trustee
[[The Okafor Family Trust|o2:full]]
[[P.O. Box 8842|addr:PO Box]]
[[Sewickley|place:town]], [[PA|place:state abbreviation]] [[15143|zip]]
**Re: Engagement for representation; [[Okafor Family Trust|o2:short!:trust name without article]] adv. [[Emeka Okafor|p2:full]]; our matter no. [[20260114.0003|rec!:matter number that looks like a date]]**
Dear [[Ms. Okafor|p1:title-surname]]:
Thank you for selecting Halvorsen Pruitt & Achebe LLP (the "Firm") to represent you in your capacity as successor trustee of the Okafor Family Trust, u/a/d [[April 9, 2003|date:trust instrument date]] (the "Trust"), in connection with the petition filed by [[your brother|indirect!:family relationship to a named person]], Emeka Okafor, in the Orphans' Court Division of the Court of Common Pleas of [[Allegheny County|place:county]] at No. [[02-25-06617|rec:court docket number]]. This letter and the enclosed Standard Terms describe the basis on which we will provide legal services. Please read both carefully.
**1. Scope.** We will represent you, as trustee only, in defending the petition for an accounting and for your removal, and in the related dispute over the proposed sale of the late [[Dr. Chukwuma Okafor|p3:full:title + full name]]'s former medical office at [[1187 Beaver Street|addr]] in Sewickley (the "[[Beaver Street property|indirect!:distinctive asset]]"). We do not represent you individually, the Trust's other beneficiaries, or [[Okafor Pediatrics, P.C.|o3:full]] Tax advice and preparation of the Trust's Form 1041 remain with your accountants at [[Brindle & Vasquez CPAs|o4:full]]. If you later ask us to take on additional work, we will confirm that in writing.
**2. Staffing and rates.** I will have primary responsibility for the matter. My 2026 rate is [[$525|money]] per hour. [[Thomas J. Achebe|p5:full]] (associate, [[$340|money]] per hour) and paralegal [[Wendy Pruitt-Sato|p6:full]] ([[$185|money]] per hour) will assist where that is more economical. Rates are adjusted each January. We bill in tenths of an hour and send statements monthly.
**3. Retainer.** We ask for an advance of [[$7,500|money]], which will be held in our IOLTA account and applied to our final invoice. You may pay by check or by wire to [[Three Rivers Bank & Trust|o5:full]], ABA [[102560066|rtn]], account no. [[4000 7731 8852|acct!:account number with spaces]], reference 20260114.0003. You may also pay online at [[https://pay.hpa-law.example/retainer|url]]. Under Rule 1.15 we must keep these funds separate from the Firm's own money until they are earned.
**4. Conflicts.** As we discussed on [[January 14|date!:month and day only]], the Firm represented [[Sewickley Valley Savings Bank|o6:full]] ("[[SVSB|o6:acronym]]"), the Trust's lender, in unrelated matters that concluded in 2022. We do not believe this creates a conflict, and you have agreed to waive any conflict that may exist. SVSB has given its consent as well.
**5. Communication.** You have asked that we not call your office line. We will use your mobile, [[(412) 555-0171|phone]], and the email address above. Documents will be shared through our client portal; your username is [[nokafor-trustee|cred:portal username]] and a temporary password will be sent to you separately.
**6. Document retention.** We keep closed files for seven years and then destroy them unless you ask us in writing to return them.
If these terms are acceptable, please sign below and return a copy with the retainer by [[February 6, 2026|date:deadline]]. You may end our engagement at any time.
Very truly yours,
[[Ingrid M. Halvorsen|p4:full]]
PA Attorney ID No. [[87214|govid!:short bar number]]
[[imh@hpa-law.example|email]] / direct [[412.555.0122|phone:dotted]]
cc: [[T. Achebe|p5:short:initial + surname]]
**ACKNOWLEDGED AND AGREED:**
______________________ [[NGOZI A. OKAFOR|p1:caps]], as Trustee and not individually. Date: __________
'''))

# ---------------------------------------------------------------- doc 3
DOCS.append(D(3, "pdf", "court filing draft - complaint", "legal", "US", length="long",
  title="Complaint for damages - trucking collision (draft)",
  ents={"p1": "Annelise van der Berg", "p2": "Jordan van der Berg", "p3": "Dwayne T. Pruett, Jr.",
        "p5": "Marcus E. Delacroix", "p6": "Lamar Okonjo", "p7": "Rhonda Castellano", "p8": "Kenji Watanabe",
        "p9": "Miriam Abelson", "p10": "Paul Yoon",
        "o1": "Cascade Ridge Freight Lines, Inc.", "o2": "Northwest Registered Agents of Olympia LLC",
        "o3": "Delacroix Injury Law, PLLC", "o4": "Padilla Bay Medical Center", "o5": "Treasure Valley Hauling Co.",
        "o6": "Harbor Heights Trauma Center", "o7": "Evergreen Mutual Health Plan", "o8": "van der Berg Marine Joinery",
        "o9": "Cascadia Northwest Insurance Co.", "o10": "Great Basin Commercial Casualty"},
  distractors=["28 U.S.C. § 1332(a)", "28 U.S.C. § 1391(b)(2)", "RCW 46.61.145", "49 C.F.R. § 395.3",
               "$75,000", "Fed. R. Civ. P. 38(b)", "Interstate 5", "DOES 1-10", "Freightliner Cascadia"],
  body=r'''
[[Marcus E. Delacroix|p5:full]], WSBA No. [[48213|govid!:short bar number]]
[[Delacroix Injury Law, PLLC|o3:full]]
[[1201 Third Avenue, Suite 2950|addr:street with suite]]
[[Seattle|place:city]], [[WA|place:state abbreviation]] [[98101|zip]]
Telephone: [[(206) 555-0133|phone]]
Facsimile: [[(206) 555-0134|phone:fax]]
[[marcus@delacroixinjury.example|email]]
Attorney for Plaintiffs
# UNITED STATES DISTRICT COURT
# WESTERN DISTRICT OF [[WASHINGTON|place!:state in a caps court heading]] AT [[SEATTLE|place!:city in caps]]
[[ANNELISE VAN DER BERG|p1:caps]] and [[JORDAN VAN DER BERG|p2:caps]], a married couple,
Plaintiffs,
v.
[[CASCADE RIDGE FREIGHT LINES, INC.|o1:caps]], a [[Delaware|place!:state of incorporation]] corporation; [[DWAYNE T. PRUETT, JR.|p3:caps]], an individual; and DOES 1-10,
Defendants.
Case No. [[2:26-cv-00417-RSM|rec:federal case number]]
**COMPLAINT FOR DAMAGES (Negligence; Negligent Hiring, Retention and Entrustment; Loss of Consortium)**
**JURY DEMAND**
Plaintiffs allege as follows:
## I. PARTIES
1. Plaintiff [[Annelise van der Berg|p1:full]] ("[[Ms. van der Berg|p1:title-surname]]") is a [[lawful permanent resident|attr:immigration status]] of the United States and a [[citizen of the Netherlands|attr:citizenship]] who resides in [[Bellingham|place:city]], [[Whatcom County|place:county]], [[Washington|place:state]].
2. Plaintiff [[Jordan van der Berg|p2:full]] is Ms. van der Berg's husband. He resides with her in Bellingham and is a citizen of Washington.
3. Defendant [[Cascade Ridge Freight Lines, Inc.|o1:full]] ("[[Cascade Ridge|o1:short!:short name that reads like a place]]") is a Delaware corporation with its principal place of business at [[8800 Industrial Parkway|addr]], [[Boise|place:city]], [[Idaho|place:state]] [[83716|zip]]. It operates as an interstate motor carrier under USDOT No. [[3184472|rec!:USDOT carrier number]]. Its registered agent in Washington is [[Northwest Registered Agents of Olympia LLC|o2:full]].
4. Defendant [[Dwayne T. Pruett, Jr.|p3:full]] ("[[Pruett|p3:surname!]]") is a resident of [[Nampa|place:city]], Idaho, who at all relevant times held Idaho commercial driver's license no. [[TB184406K|govid:commercial driver's license number]]. At all relevant times Pruett was employed by Cascade Ridge as a long-haul driver (employee no. [[CR-20871|rec:employee ID]]) and was acting within the course and scope of that employment.
5. Plaintiffs do not know the true names of the defendants sued as DOES 1-10 and will amend this complaint when their identities are learned.
## II. JURISDICTION AND VENUE
6. This Court has subject-matter jurisdiction under 28 U.S.C. § 1332(a) because the parties are citizens of different states or of a foreign state and the amount in controversy exceeds $75,000, exclusive of interest and costs.
7. Venue is proper in this district under 28 U.S.C. § 1391(b)(2) because a substantial part of the events giving rise to the claims occurred in [[Skagit County|place:county]], Washington.
## III. FACTS
8. On [[Thursday, October 9, 2025|date!:date with weekday]], at approximately 6:40 a.m., Ms. van der Berg was driving her 2021 Subaru Outback (VIN [[4S4BTANC8M3172905|veh:VIN]], Washington plate [[BXR4192|veh:license plate]]) southbound on Interstate 5 near milepost 227 in [[Mount Vernon|place:city]]. She was on her way to her job as a surgical nurse at [[Padilla Bay Medical Center|o4:full]]. Traffic ahead had slowed for a disabled vehicle, and Ms. van der Berg slowed with it.
9. Pruett was driving directly behind her in a 2019 Freightliner Cascadia tractor (VIN [[3AKJHHDR7KSKF4418|veh:VIN]], Idaho plate [[A47 2291T|veh!:license plate with a space]]) pulling a loaded 53-foot trailer owned by Cascade Ridge and identified as unit [[T5512|rec!:fleet unit number]].
10. Pruett did not slow. The tractor struck the rear of the Subaru at highway speed, drove it into the concrete median barrier, and pushed it roughly 140 feet before both vehicles came to rest.
11. Washington State Patrol Trooper [[L. Okonjo|p6:short:initial + surname]] (badge no. [[1147|govid!:short badge number]]) responded and prepared Collision Report No. [[E1298845|rec:police report number]]. Trooper [[Okonjo|p6:surname!]] cited Pruett under RCW 46.61.145 for following too closely.
12. Data from the tractor's electronic logging device (serial no. [[ELD7C20093318|dev:ELD serial number]]) show that Pruett had been on duty for more than fifteen hours when the collision occurred, in violation of 49 C.F.R. § 395.3, and that the tractor was traveling 71 miles per hour four seconds before impact.
13. Records for the cell phone Pruett carried that morning, number [[208-555-0186|phone]], show that he sent or received six text messages in the two minutes before the collision.
14. Before it hired Pruett in [[March 2024|date!:month and year of hire]], Cascade Ridge knew or should have known that he had a [[2019 conviction for reckless driving|attr:criminal history]] in [[Canyon County|place:county]], Idaho (Case No. [[CR14-19-08832|rec:criminal case number]]), two earlier preventable collisions, and a [[license suspension in 2021|attr!:driving and criminal history]], and that he had [[failed a DOT drug screen|health!:substance-use detail]] while working for a previous employer, [[Treasure Valley Hauling Co.|o5:full]]
15. Cascade Ridge's safety director, [[Rhonda Castellano|p7:full]], nonetheless approved Pruett's application. In an email dated [[3/18/2024|date:numeric date]], [[Ms. Castellano|p7:title-surname]] wrote that the company "needs drivers" and directed that Pruett be cleared without the road test required by the company's own written policy.
16. Cascade Ridge dispatched Pruett on the morning of the collision knowing that he could not lawfully complete the assigned run within his available hours of service.
## IV. INJURIES AND DAMAGES
17. Ms. van der Berg was taken by ambulance to the emergency department at [[Padilla Bay|o4:short!:short name that reads like a place]] and was then airlifted to [[Harbor Heights Trauma Center|o6:full]] in Seattle, where she remained an inpatient from [[October 9|date!:month and day only]] until [[October 27, 2025|date:discharge date]] (medical record no. [[HH00672914|rec:medical record number]]).
18. She sustained a [[burst fracture of the L1 vertebra|health:diagnosis]], a [[traumatic brain injury|health:diagnosis]], a [[fractured left femur|health:diagnosis]] and a [[splenic laceration|health:diagnosis]]. She underwent a [[spinal fusion|health:procedure]] performed by [[Dr. Kenji Watanabe|p8:full:title + full name]] and a second surgery to repair the femur.
19. Ms. van der Berg was [[fourteen weeks pregnant|health!:pregnancy]] at the time of the collision. She [[lost the pregnancy|health!:pregnancy loss]] three days later.
20. She continues to suffer from chronic back pain, memory and concentration deficits, and [[post-traumatic stress disorder|health:mental health diagnosis]], for which she is treated by psychologist [[Dr. Miriam Abelson|p9:full:title + full name]]. She has been prescribed [[sertraline 100 mg|health:medication and dose]] daily and [[oxycodone 5 mg|health:medication and dose]] as needed.
21. Her medical expenses to date exceed [[$612,480.17|money]], including [[$48,900|money]] for air transport. Her health insurer, [[Evergreen Mutual Health Plan|o7:full]] (member ID [[EMH884201773|rec:health plan member ID]]; claim no. [[2025CL0099417|rec:claim number]]), asserts a subrogation interest of [[$377,204.66|money]].
22. Before the collision Ms. van der Berg earned approximately [[$118,300|money]] per year. She has not been able to return to work. Her future lost earnings are estimated at not less than [[$1.4 million|money!:millions written out]].
23. [[Jordan|p2:first-name!:first name that is also a place name]] is a self-employed boat builder who operates [[van der Berg Marine Joinery|o8:full]] He closed his shop for four months to care for his wife and as a result lost a contract, worth [[$86,000|money]], to restore the [[schooner Marguerite|indirect!:distinctive asset, named vessel]]. He has been deprived of his wife's companionship, society and support.
24. The Subaru was a total loss valued at [[$31,750|money]]. Plaintiffs' automobile carrier, [[Cascadia Northwest Insurance Co.|o9:full]] (policy no. [[PA7731440218|rec:policy number]]), paid that amount less a [[$500|money]] deductible.
## V. PRE-SUIT DEMAND
25. On [[January 12, 2026|date]], Plaintiffs' counsel sent a written demand to Cascade Ridge's liability insurer, [[Great Basin Commercial Casualty|o10:full]] (claim no. [[GBTRK25104482|rec:claim number]]), to the attention of adjuster [[Paul Yoon|p10:full]] ([[paul.yoon@greatbasincc.example|email]]; [[1-800-555-0199 ext. 4471|phone!:toll-free with extension]]), for the policy limits of [[$1,000,000|money]].
26. On [[February 2, 2026|date]], [[Mr. Yoon|p10:title-surname]] responded with an offer of [[$225,000|money]], which Plaintiffs rejected.
## VI. FIRST CLAIM: NEGLIGENCE (against Pruett)
27. Plaintiffs reallege the paragraphs above.
28. Pruett owed Ms. van der Berg a duty to operate the tractor-trailer with reasonable care, to keep a proper lookout, to maintain a safe following distance, and to comply with state law and federal motor carrier safety regulations.
29. Pruett breached those duties by following too closely, driving at an unsafe speed, driving while fatigued and beyond his lawful hours of service, and using a handheld phone while driving.
30. Pruett's negligence was a proximate cause of the injuries and damages described above.
## VII. SECOND CLAIM: VICARIOUS LIABILITY (against Cascade Ridge)
31. Plaintiffs reallege the paragraphs above.
32. Pruett was acting within the course and scope of his employment when the collision occurred. Cascade Ridge is liable for his negligence under the doctrine of respondeat superior.
## VIII. THIRD CLAIM: NEGLIGENT HIRING, RETENTION, SUPERVISION AND ENTRUSTMENT (against Cascade Ridge)
33. Plaintiffs reallege the paragraphs above.
34. Cascade Ridge owed the motoring public a duty to use reasonable care in hiring, training, supervising and retaining its drivers and in entrusting commercial vehicles to them.
35. Cascade Ridge breached that duty by hiring and retaining Pruett despite his record, by waiving its own road test, by failing to monitor his hours of service, and by dispatching him on a run he could not lawfully complete.
36. Cascade Ridge's negligence was a proximate cause of the injuries and damages described above.
## IX. FOURTH CLAIM: LOSS OF CONSORTIUM (against all Defendants)
37. Plaintiffs reallege the paragraphs above.
38. As a direct result of Defendants' negligence, Jordan van der Berg has lost the love, care, companionship and services of his wife, and will continue to suffer that loss.
## X. PRAYER FOR RELIEF
Plaintiffs ask for judgment against Defendants, jointly and severally, as follows:
- special damages for past and future medical expenses, lost earnings and lost earning capacity, in amounts to be proved at trial;
- general damages for pain, suffering, disability, disfigurement and loss of enjoyment of life;
- damages for loss of consortium;
- property damage, prejudgment interest on liquidated sums, and taxable costs; and
- such other relief as the Court finds just.
## XI. JURY DEMAND
Under Fed. R. Civ. P. 38(b), Plaintiffs demand a trial by jury on all issues so triable.
DATED this [[19th day of February, 2026|date!:date in legal long form]].
[[DELACROIX INJURY LAW, PLLC|o3:caps]]
By: s/ Marcus E. Delacroix
Marcus E. Delacroix, WSBA No. 48213
Attorney for Plaintiffs
## VERIFICATION
I, Annelise van der Berg, declare under penalty of perjury under the laws of the United States that I have read this complaint and that the facts stated in it are true to the best of my knowledge. Executed at Bellingham, Washington on [[February 18, 2026|date]].
______________________________
Annelise van der Berg
'''))

# ---------------------------------------------------------------- doc 4
DOCS.append(D(4, "txt", "deposition summary", "legal", "US", length="long",
  title="Deposition summary - elder financial exploitation case",
  ents={"p1": "Walter J. Kowalczyk", "p2": "Tiffany-Rae Mullins", "p3": "Barbara Kowalczyk-Greene",
        "p4": "Dennis Greene", "p5": "Irene Kowalczyk", "p6": "Sanjay Venkataraman", "p7": "Colleen O'Brien",
        "p8": "Marlene Fitch", "p9": "Tomasz Zielinski", "p10": "Hye-Jin Park", "p11": "Chase Dombrowski",
        "p12": "Ray Santangelo", "p13": "Kyle Mullins", "p14": "Jerome D. Lask",
        "o1": "Brightpath Home Care, LLC", "o2": "Monongahela Valley Federal Credit Union",
        "o3": "O'Brien & Stanek, P.C.", "o4": "Venkataraman Lowe LLP", "o5": "St. Stanislaus Kostka Parish",
        "o6": "Steel & Tin Workers Local 1408", "o7": "Chestnut Ridge Medical Center",
        "o8": "Laurel Highlands Coin & Jewelry"},
  distractors=["Pa.R.C.P. 4007.1", "Exhibit 7", "Social Security", "Medicare", "Tuesdays", "Buick", "Form 1099-R", "18 Pa.C.S. § 3921"],
  body=r'''
DEPOSITION SUMMARY (PAGE:LINE)                         PRIVILEGED -- PREPARED FOR TRIAL COUNSEL

Case:        [[Kowalczyk|p1:surname!:surname in a case caption]] v. Brightpath Home Care, LLC, et al.
Court:       Court of Common Pleas, [[Westmoreland County|place:county]], [[Pa.|place!:state abbreviation with period]], No. [[2025-CV-03381|rec:civil docket number]]
Deponent:    [[WALTER J. KOWALCZYK|p1:caps]] (Plaintiff)
Taken:       [[February 24, 2026|date:deposition date]], 9:42 a.m. - 2:15 p.m., at the offices of [[O'Brien & Stanek, P.C.|o3:full]],
             [[35 West Pittsburgh Street, 2nd Fl.|addr:street with floor]], [[Greensburg|place:city]], [[PA|place:state abbreviation]] [[15601|zip]]
Noticed by:  Defendants, under Pa.R.C.P. 4007.1
Appearances: [[Colleen O'Brien|p7:full]], Esq. (for Plaintiff); [[Sanjay Venkataraman|p6:full]], Esq., [[Venkataraman Lowe LLP|o4:full]]
             (for [[Brightpath Home Care, LLC|o1:full]]); no appearance for Defendant [[Mullins|p2:surname!]] (pro se, served)
Reporter:    [[Marlene Fitch|p8:full]], RPR
Summarized by: [[jdl|p14:initials:lower-case initials]], [[3/2/26|date!:numeric date with two-digit year]]            Our file: [[OS-25-0447|rec:firm file number]]

NOTE FOR [[CO'B|p7:initials]]: witness tired noticeably after lunch (see 118:4 onward). He is a
good witness on the big points. Weak spots flagged with **.

-----------------------------------------------------------------------------------------
PAGE:LINE     SUMMARY
-----------------------------------------------------------------------------------------
5:1-7:20      Background. Deponent is [[ninety-one years old|age!:age spelled out]], born [[August 3, 1934|dob]] in [[Monessen|place:town]].
              Has lived alone at [[212 Sycamore St.|addr]], [[Latrobe|place:city]], since his wife [[Irene|p5:first-name]] died
              on [[11/2/2019|date:date of death]]. Everyone calls him "[[Buddy|p1:nickname]]." One child, [[Barbara Kowalczyk-Greene|p3:full]]
              ("[[Babs|p3:nickname]]"), who lives in [[Scottsdale|place:city]] with her husband [[Dennis Greene|p4:full]].

8:1-10:14     Work history. 38 years as a millwright; receives a [[union pension|attr!:implies union membership]] through
              [[Steel & Tin Workers Local 1408|o6:full]] of [[$1,412|money]] a month plus Social Security of
              [[$2,236|money]]. Both are direct-deposited to [[Monongahela Valley Federal Credit Union|o2:full]]
              ("[[Mon Valley FCU|o2:short!:abbreviated organization nickname]]"), where he has banked "since Eisenhower."

10:15-13:6    Health. Has [[macular degeneration|health:diagnosis]] (cannot read small print without a
              magnifier), wears hearing aids, takes [[warfarin|health:medication]] and a "water pill." PCP is
              [[Dr. Hye-Jin Park|p10:full:title + full name]] at [[Chestnut Ridge Medical Center|o7:full]]. Denies any memory
              problem. ** Admits [[Dr. Park|p10:title-surname]] gave him "the clock test" last fall and told
              him he had [[mild cognitive impairment|health:diagnosis, contested]]; he disagrees with that.

13:7-19:22    Hiring Brightpath. After a [[fall in March 2025|health!:medical event]] he spent four days at
              [[Chestnut Ridge|o7:short!:short name that reads like a place]]. Babs arranged home care by phone from [[Arizona|place:state]]. Contract
              signed [[April 1, 2025|date:contract date]] (Exhibit 3): three visits a week at [[$34.50|money]] an hour.
              [[Brightpath|o1:short!:one-word short name]] assigned [[Tiffany-Rae Mullins|p2:full]]. He liked her; "she was like a
              granddaughter." She started driving him to [[Mass|attr!:implies religious practice]] at [[St. Stanislaus|o5:short!:shortened parish name]] on Sundays
              in his Buick.

20:1-27:9     Access to finances. By June [[Ms. Mullins|p2:title-surname]] was picking up his mail and
              "helping with the bills." He gave her his debit card to buy groceries and
              told her the PIN, [[0834|cred!:PIN stated in testimony]] ("my birthday, so I don't forget it").
              Card number per Exhibit 5: [[4989 4186 6411 9402|card:card number with spaces]], exp. [[09/27|exp]]. He kept his
              online banking password on a sticky note on the refrigerator; he recited it
              as [[Polka1934!|cred!:password read into the record]] and his user name as [[buddyk34|cred:username]].
              ** Concedes he never told her NOT to use the card for herself.

27:10-41:3    The withdrawals. Shown Exhibit 7 (statements for share draft account
              [[00-4471-208816|acct:account number with dashes]]). Does not recognize:
                - 31 ATM withdrawals, [[May 29|date!:month and day only]] through [[Sept. 30, 2025|date:abbreviated month]], totaling [[$15,340|money]];
                - check no. 3318 for [[$9,800.00|money]] payable to "[[T. Mullins|p2:short:initial + surname]]", memo "loan";
                - check no. 3321 for [[$4,250|money]] to [[Laurel Highlands Coin & Jewelry|o8:full]];
                - an online transfer of [[$22,000|money]] on [[10/14/25|date!:numeric date with two-digit year]] to an account ending [[7706|acct!:last four only]].
              Signature on 3318 "looks like mine but I never wrote that." Denies ever
              lending money to [[Tiffany|p2:first-name]]. ** On cross-check with 34:11, he first said he
              "might have helped her with her car once," then said that was [[fifty dollars|money!:amount in words]]
              for gas.

41:4-48:16    The new phone. In August Ms. Mullins bought him a smartphone "so Babs could
              see me on the video." He does not know how to use it for banking. Exhibit 9
              (credit union device log) shows the mobile app was enrolled on [[8/19/2025|date:numeric date]] from
              a phone with IMEI [[35 693803 564380 9|dev!:IMEI with spaces]], and that later logins came from IP
              addresses [[198.51.100.23|ip:IPv4]] and [[2001:db8:4c2:91::1f|ip!:IPv6]]. He has no internet at the house.
              His own number is [[724-555-0142|phone]]; the app was registered to [[(724) 555-0190|phone]],
              which he does not recognize.

48:17-55:2    Discovery of the loss. On [[October 20, 2025|date]], teller [[Chase Dombrowski|p11:full]] at the
              Latrobe branch asked him about the $22,000 transfer when he came in for
              cash. "[[Chase|p11:first-name!:first name that is also a common word]] turned the screen around and I about fell over." Balance
              was [[$611.08|money]]; a year earlier it had been "over [[sixty thousand|money!:amount in words without currency]]."
              He called [[Barbara|p3:first-name]] from the branch.

55:3-63:18    Aftermath. Babs flew in on [[Oct. 22|date!:abbreviated month and day only]]. Police report made to Latrobe PD,
              [[Det. Ray Santangelo|p12:full:rank + full name]], incident no. [[25-LP-009214|rec:police incident number]]. Mon Valley FCU
              fraud claim no. [[FRD-2025-11873|rec:fraud claim number]] denied in part because the PIN was
              "voluntarily shared." Brightpath terminated Ms. Mullins [[10/24/2025|date:termination date]].
              He understands she has been charged (18 Pa.C.S. § 3921) and that she has
              [[a prior theft conviction|attr!:criminal history]] from [[Fayette County|place:county]] that the agency missed.

63:19-71:5    What Brightpath knew. He complained twice to the scheduler that Tiffany
              came on days she wasn't scheduled and brought [[her boyfriend, Kyle|indirect!:relationship to a named person]]. No one
              called back. ** Cannot give dates. Thinks one call was "around the
              Fourth of July." Brightpath's office number, which he dialed from memory:
              [[724 555 0117|phone!:spaces only]].

71:6-80:12    Church and giving. [[Father Zielinski|p9:title-surname]] of [[St. Stanislaus Kostka Parish|o5:full]] visited
              weekly. Deponent [[tithes|attr!:implies religious practice]] [[$40|money]] a week by envelope and denies
              authorizing the [[$1,500|money]] online gift to the parish roof fund on Exhibit 7
              ("I'd have done it by check"). [[Venkataraman|p6:surname!]] pressed on whether deponent
              gives money away freely; he also [[gave $200 to the county Democratic committee|attr!:political donation]]
              in 2024 "like every election year."

80:13-96:7    Damages. Total he believes was taken: [[$52,890|money]] (matches our schedule).
              Has had trouble sleeping, [[lost eleven pounds|health!:health detail in plain words]], stopped going to the
              Tuesdays card game at the union hall because he is "ashamed." Dr. Park
              started him on [[mirtazapine 15 mg|health:medication and dose]] in November. Babs now pays his
              bills remotely; he resents it.

96:8-117:20   Cross by [[Mr. Venkataraman|p6:title-surname]]. Established: (a) deponent signed the Brightpath
              service agreement without reading the "no financial assistance" clause,
              could not read it without his magnifier; (b) he gave Ms. Mullins a
              Christmas card with [[$100|money]] cash in 2024 -- before she was assigned to him,
              when she cared for a neighbor; (c) he told Babs in July everything was
              "fine"; (d) he could not name the current month without prompting
              (objection, [[O'Brien|p7:surname!:surname only, with apostrophe]]; he then answered correctly).

118:4-131:2   ** After lunch. Confused Exhibit 5 with Exhibit 7. Said the debit card
              "ends in 9402 or 4902." Said Irene "handles the checkbook," then corrected
              himself. [[Ms. O'Brien|p7:title-surname]] requested a break at 124:15.

              Asked about insurance: he has Medicare and a supplemental plan through
              the Local, member no. [[STW-1408-00771|rec:health plan member ID]]; neither covered the home care, which
              Babs paid from her own account ([[$1,656|money]] for the first month). He also said
              Ms. Mullins once drove him to [[Laurel Highlands|o8:short]] "to look at Irene's rings" and
              that he has not seen [[Irene's engagement ring|indirect!:distinctive personal property]] since. He does not know
              whether it was sold. (New fact; not in our complaint. Consider amending.)

131:3-140:9   Redirect. Reaffirmed he never authorized any withdrawal over "grocery
              money," never wrote check 3318, never used the app. Identified his own
              signature exemplar (Exhibit 12). Read and sign reserved.

-----------------------------------------------------------------------------------------
FOLLOW-UP
 1. Subpoena carrier records for (724) 555-0190 -- likely [[Kyle Mullins|p13:full]].
 2. Get Dr. Park's chart; expect defense IME request on capacity. Retain geriatric psych.
 3. Ask [[Dombrowski|p11:surname!]] for a statement before the credit union lawyers get to him.
 4. Form 1099-R for the pension shows the [[Local 1408|o6:short!:union local number only]] plan ID; redact before producing.
 5. Babs's contact for scheduling: [[babs.kg@desertmail.example|email]], [[480.555.0163|phone:dotted]].
 6. Errata sheet due 30 days after transcript; calendar for [[April 6, 2026|date:deadline]].
'''))

from corpus_src.a_part2 import DOCS as _P2
DOCS += _P2
from corpus_src.a_part3 import DOCS as _P3
DOCS += _P3
from corpus_src.a_part4 import DOCS as _P4
DOCS += _P4
