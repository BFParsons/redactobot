from corpus_src.dsl import D, dt, amt, num

DOCS = []

# ---------------------------------------------------------------- 21
DOCS.append(D(21, "txt", "settlement term sheet", "legal", "US",
  title="Mediated settlement term sheet - wage and accommodation claims",
  ents={"p1": "Rosalind M. Achterberg", "p2": "Desmond Okonkwo-Hale", "p3": "Lucille Baptiste-Moreau",
        "p4": "Tamsin Pruitt", "p5": "J. Everett Lindqvist III", "p6": "Kwame Asante",
        "o1": "Tidewater Cold Storage, LLC", "o2": "Pruitt & Vandermeer, PLLC",
        "o3": "Harborview Dispute Resolution Group", "o4": "Old Dominion Mutual Casualty Co.",
        "o5": "Chesapeake Tidal Bank", "o6": "Lindqvist Shaw & Abernathy LLP"},
  distractors=["FRE 408", "Form W-2", "Form 1099-MISC", "29 U.S.C. § 216(b)", "21 days"],
  body=r'''CONFIDENTIAL SETTLEMENT COMMUNICATION -- SUBJECT TO FRE 408 AND LOCAL RULE 83.6

                    MEDIATED SETTLEMENT TERM SHEET

Matter:    [[Achterberg|p1:surname]] v. [[Tidewater Cold Storage, LLC|o1:full]], et al.
Court:     U.S. District Court, Eastern District of [[Virginia|place:state]] ([[Norfolk|place:city]] Division)
Case No.:  [[2:25-cv-00417-RBS-LRL|rec:federal docket number]]
Mediator:  [[Hon. Lucille Baptiste-Moreau|p3:full:full name with honorific]] (Ret.), [[Harborview Dispute Resolution Group|o3:full]]
Date:      [[October 9, 2026|date:mediation date]]

1. PARTIES. Plaintiff [[Rosalind M. Achterberg|p1:full]] ("Plaintiff" or "[[Ms. Achterberg|p1:title-surname]]").
Defendants Tidewater Cold Storage, LLC ("[[Tidewater|o1:short]]") and its managing member,
[[Desmond Okonkwo-Hale|p2:full]] ("[[Okonkwo-Hale|p2:surname]]").

2. PAYMENT. Tidewater will pay a gross sum of [[$185,000.00|money]]
([[one hundred eighty-five thousand dollars|money!:amount in words]]), allocated as follows:
   (a) [[$52,400.00|money]] as back overtime wages, less withholding, reported on Form W-2;
   (b) $52,400.00 as liquidated damages, reported on Form 1099-MISC (box 3);
   (c) [[$6,200|money]] in settlement of the accommodation claim (EEOC Charge No.
       [[437-2025-01186|rec:agency charge number]]) arising from her [[high-risk pregnancy|health:pregnancy detail]];
   (d) [[$74,000.00|money]] in fees and costs to [[Pruitt & Vandermeer, PLLC|o2:full]] (EIN [[54-1830927|taxid:EIN]]).

3. TIMING AND DELIVERY. Payments (a)-(c) within 21 days of court approval and in no
event later than [[November 20, 2026|date:payment deadline]]. Checks to Plaintiff go to
[[2217 Colley Avenue, Apt. 3B|addr:street with apartment]], Norfolk, [[VA|place:state abbreviation]] [[23517|zip]]. For the W-2, payroll will use the SSN on file
ending [[xxx-xx-0681|ssn!:masked SSN]]; Plaintiff gives her W-9 to counsel only.
Payment (d) by wire to the firm's IOLTA account: [[Chesapeake Tidal Bank|o5:full]], ABA [[052476475|rtn]],
acct [[0004 1882 7731|acct!:account number with spaces]], reference [[PV-25-0417|rec!:firm matter number]].

4. INSURANCE. Tidewater's EPLI carrier, [[Old Dominion Mutual Casualty Co.|o4:full]] ("[[ODMC|o4:acronym]]"),
claim no. [[EPL-2025-0093317|rec:claim number]] under policy [[ODM-EPL-7704512|rec:policy number]], funds [[$110K|money!:abbreviated amount]] of the gross
sum. Tidewater funds the [[$75,000|money]] balance from its retention. Adjuster with authority:
[[Kwame Asante|p6:full]], [[(757) 555-0163 x214|phone:with extension]], [[kasante@odmc-claims.example|email]].

5. NON-MONETARY TERMS. Neutral reference limited to dates of employment ([[06/03/2019|date:hire date]]
to [[01/17/2025|date:termination date]]) and last position held. Separation re-coded as voluntary; no
contest of unemployment benefits. Mutual non-disparagement. No rehire.

6. RELEASE. General release of wage claims under 29 U.S.C. § 216(b) and state law.
Carve-out: her pending workers' compensation claim (JCN [[VA02000394417|rec!:claim number without separators]]) for
[[a lumbar disc herniation|health!:injury]] is NOT released.

7. APPROVAL. Joint motion for approval to be filed by [[10/23/2026|date:filing deadline]]. Counsel:
[[Tamsin Pruitt|p4:full]] (VSB No. [[48213|govid:state bar number]]) for Plaintiff; [[J. Everett Lindqvist III|p5:full:name with initial and suffix]],
[[Lindqvist Shaw & Abernathy LLP|o6:full]], for Defendants.

Initialed:  [[RMA|p1:initials]] ____   [[DOH|p2:initials]] ____   [[TP|p4:initials]] ____   [[JEL|p5:initials]] ____

Mediator's note: [[Judge Baptiste-Moreau|p3:title-surname]] holds the signed sheet. [[Rosalind|p1:first-name]] asked
that nothing be mailed to the [[Ghent|place!:neighbourhood that is also a foreign city name]] apartment after [[Dec. 1|date!:abbreviated date without year]], when her lease ends;
use [[r.achterberg77@mailbox.example|email]] or her cell, [[757.555.0128|phone:dotted]], after that.
'''))

# ---------------------------------------------------------------- 22
DOCS.append(D(22, "pdf", "court filing draft - declaration", "legal", "US",
  title="Declaration in support of motion to reopen removal proceedings",
  ents={"p1": "Yohannes Tesfaye Gebremariam", "p2": "Gerald P. Whitcombe", "p3": "Selamawit Gebremariam",
        "p4": "Amina Warsame-Lindgren", "p5": "Liya Gebremariam", "p6": "Mulugeta Hailu",
        "p7": "Ingrid Sondergaard-Pham",
        "o1": "Whitcombe Immigration Law Office, P.A.", "o2": "Northstar Halal Meats, Inc.",
        "o3": "Cedar-Riverside Community Health Center", "o4": "North Loop Immigrant Justice Clinic"},
  distractors=["28 U.S.C. § 1746", "8 C.F.R. § 1003.23(b)(4)(ii)", "Form I-589", "Form EOIR-33", "Matter of Lozada", "Immigration Court"],
  body=r'''
DRAFT v3 -- attorney work product -- do not file
# UNITED STATES DEPARTMENT OF JUSTICE, EXECUTIVE OFFICE FOR IMMIGRATION REVIEW
Immigration Court, [[Fort Snelling|place!:named facility]], [[Minnesota|place:state]]
In the Matter of: [[YOHANNES TESFAYE GEBREMARIAM|p1:caps:name in caption]], Respondent
File No. [[A 216-554-908|govid!:alien registration number]]
In removal proceedings
## DECLARATION OF RESPONDENT IN SUPPORT OF MOTION TO REOPEN AND RESCIND IN ABSENTIA ORDER
I, [[Yohannes Tesfaye Gebremariam|p1:full]], declare as follows:
1. I was born on [[19 January 1987|dob:day month year]] in [[Adigrat|place:town]]. I am [[an Ethiopian national of Tigrayan ethnicity|attr:nationality and ethnicity]] and I belong to [[the Ethiopian Orthodox church|attr:religion]]. My first language is [[Tigrinya|attr!:language indicating ethnicity]]. This declaration was read back to me in Tigrinya before I signed it.
2. I entered the United States at [[San Ysidro|place:port of entry]] on [[03/02/2022|date:entry date]] and asked for asylum the same day. I travelled on [[Ethiopian|attr!:nationality adjective]] passport no. [[EP5530917|govid:passport number]]. My Form I-589 was filed within one year.
3. I live at [[1904 South 6th Street, Unit 12|addr:street with unit]], [[Minneapolis|place:city]], [[MN|place:state abbreviation]] [[55454|zip]]. Since [[May 2023|date!:month and year of hire]] I have worked as a meat cutter at [[Northstar Halal Meats, Inc.|o2:full]] under my employment authorization, receipt number [[MSC2290417788|govid!:USCIS receipt number]].
4. My former lawyer was [[Gerald P. Whitcombe|p2:full]] of [[Whitcombe Immigration Law Office, P.A.|o1:full]] I paid [[Mr. Whitcombe|p2:title-surname]] [[$4,500|money]] in cash over six visits. He gave me receipts for only [[$3,000|money]].
5. Mr. Whitcombe never told me that my hearing had been moved up to [[August 14, 2025|date:hearing date]]. He did not file Form EOIR-33 when I moved, although I gave his office my new address in writing. I was ordered removed in my absence. I first learned of the order on [[Sept. 3, 2025|date:abbreviated month]], when [[my wife, Selamawit|indirect!:spouse of respondent]], opened a letter that had been forwarded from our old apartment in [[St. Paul|place:city]].
6. In my country I [[organized for an opposition student union|attr!:political activity]] and in 2021 I was [[held for eleven days by federal police in Mekelle|attr!:detention history abroad]]. I still have [[scars on both wrists|health!:physical finding]] from that time.
7. I have been diagnosed with [[post-traumatic stress disorder|health:mental health diagnosis]]. Since [[11/18/2024|date:start of treatment]] I have been treated by [[Dr. Amina Warsame-Lindgren|p4:full:full name with title]] at [[Cedar-Riverside Community Health Center|o3:full]] and I take [[sertraline 100 mg|health:medication and dose]] each morning. [[Dr. Warsame-Lindgren|p4:title-surname]] has written a letter, attached as Exhibit C.
8. My daughter [[Liya|p5:first-name!:child referred to by first name only]] was born in Minneapolis on [[2023-06-11|dob:ISO date]] and is [[a United States citizen|attr:citizenship status]]. She has [[a congenital heart defect|health:diagnosis of a child]] and is followed by cardiology every three months. [[Selamawit|p3:first-name]] does not drive, and I take Liya to every appointment.
9. On [[September 22, 2025|date:complaint date]] I filed a complaint against Mr. Whitcombe with the Minnesota Office of Lawyers Professional Responsibility, file no. [[OLPR-25-1147|rec:disciplinary file number]], and I mailed him a copy, as Matter of Lozada requires. He has not answered.
10. I ask the Court to reopen my case under 8 C.F.R. § 1003.23(b)(4)(ii). I did not receive notice, and I would never have missed my hearing on purpose.
I declare under penalty of perjury under 28 U.S.C. § 1746 that the foregoing is true and correct. Executed at Minneapolis, Minnesota, on [[October 2, 2025|date:execution date]].
/s/ [[Y. T. Gebremariam|p1:short!:initials + surname]]
## CERTIFICATE OF INTERPRETATION
I, [[Mulugeta Hailu|p6:full]], am fluent in Tigrinya and English and read this declaration to the Respondent in Tigrinya. [[Hailu|p6:surname]] can be reached at [[612 555 0119|phone!:spaces only]].
## COUNSEL
[[Ingrid Sondergaard-Pham|p7:full]] (Atty. ID [[MN 0398112|govid:state bar number]])
[[North Loop Immigrant Justice Clinic|o4:full]]
[[410 North 3rd Avenue, Suite 250|addr:street with suite]], Minneapolis, MN [[55401|zip]]
Tel. [[(612) 555-0184|phone]]
[[isp@northloopijc.example|email]]
'''))
# ---------------------------------------------------------------- 23
DOCS.append(D(23, "txt", "estate planning notes", "legal", "US", length="long",
  title="Estate planning conference notes to file",
  ents={"p1": "Evelyn R. Castellanos-Brandt", "p2": "Winifred Hollis", "p3": "Dong-hyun Park",
        "p4": "Marisol Brandt-Okafor", "p5": "Bernadette Kowalczyk", "p6": "Farrukh Siddiqui",
        "p7": "Rafael Castellanos", "p8": "Dieter Brandt", "p9": "Rafael Castellanos Jr.",
        "p10": "Annelise Brandt", "p11": "Jonah Brandt-Whitehorse", "p12": "Klaus Brandt",
        "p13": "Guadalupe Castellanos", "p14": "Thaddeus Nwosu",
        "o1": "Hollis, Marchetti & Thibodeaux, P.C.", "o2": "Wauwatosa Senior Health Partners",
        "o3": "Prairie Oak Supported Living, Inc.", "o4": "Lakeshore Community Credit Union",
        "o5": "Halvorsen Whitlock Securities", "o6": "Midwest Fraternal Life",
        "o7": "St. Hedwig's Catholic Parish", "o8": "Menomonee Valley Animal Rescue",
        "o9": "Great Lakes Fiduciary Trust Co.", "o10": "Comfort Hearth Home Care LLC",
        "o11": "Castellanos-Brandt Revocable Trust", "o12": "Kinnickinnic Valley Hospital"},
  distractors=["Form 709", "Wis. Stat. § 853.03", "Chapter 7", "SSI", "Medicaid", "MoCA", "Section 14", "HIPAA", "27/30"],
  body=r'''PRIVILEGED & CONFIDENTIAL -- ATTORNEY NOTES TO FILE
[[Hollis, Marchetti & Thibodeaux, P.C.|o1:full]]                         File No. [[EP-2026-0388|rec:firm file number]]

ESTATE PLANNING CONFERENCE -- dictated by [[Winifred Hollis|p2:full]] ([[WH|p2:initials]]), typed [[dhp|p3:initials:typist initials in lower case]]

Client:      [[CASTELLANOS-BRANDT, EVELYN R.|p1:last-first:Last, First in caps]]  (goes by "[[Evie|p1:nickname]]")
DOB:         [[April 2, 1935|dob]]  ([[age 91|age]])
SSN:         [[336 56 2821|ssn!:SSN with spaces]]
Home:        [[88 Larkspur Lane|addr]], [[Wauwatosa|place:city]], [[WI|place:state abbreviation]] [[53213|zip]]
Phone:       [[414 555 0106|phone!:spaces only]] (landline only; she does not carry a cell)
Conference:  Thursday, [[September 17, 2026|date:conference date]], at the client's home, 1:30 to 3:45 pm

Also present: her daughter [[Marisol Brandt-Okafor|p4:full]] (by video from [[Tucson|place:city]]) for the first half hour;
caregiver [[Bernadette|p5:first-name]] "[[Bernie|p5:nickname]]" [[Kowalczyk|p5:surname]], who let me in and then left the room at my request.
[[Dong-hyun Park|p3:full]] from our office attended to take the asset list and act as second observer.

1. CAPACITY AND HEALTH

[[Mrs. Castellanos-Brandt|p1:title-surname]] was alert, funny, and entirely clear about who her family is and what she
owns. She corrected me twice on dates. Her primary care doctor, [[Dr. Farrukh Siddiqui|p6:full:full name with title]] of
[[Wauwatosa Senior Health Partners|o2:full]], saw her on [[Aug. 28, 2026|date:abbreviated month]] and scored her 27/30 on the MoCA; his letter
is in the file. No diagnosis of dementia. She does have [[macular degeneration|health:diagnosis]] (we will print
everything in 16-point type), wears hearing aids, and has [[atrial fibrillation|health:diagnosis]] for which she takes
[[apixaban 2.5 mg twice daily|health:medication and dose]]. A [[pacemaker was implanted in 2021|health!:procedure described in a sentence]]. She told me she wants
[[no feeding tube|health!:end-of-life treatment preference]] and no "machines" if there is no reasonable hope of recovery.
I am satisfied she meets the standard in Wis. Stat. § 853.03, and I saw no sign that anyone
was steering her. [[Marisol|p4:first-name]] spoke only when asked.

2. FAMILY

First husband [[Rafael Castellanos|p7:full]], died [[11/04/1978|date:date of death]]. Second husband [[Dieter Brandt|p8:full]], died
[[February 9, 2019|date:date of death]]. No surviving spouse. Children and descendants:

  (a) [[Rafael Castellanos Jr.|p9:full:full name with suffix]] ("[[Rafe|p9:nickname]]"), born in [[the summer of 1959|dob!:season and year only]], single, no children.
      Lives rent-free in the client's lake cabin (see below).
  (b) Marisol Brandt-Okafor, born [[7/22/1964|dob:numeric without leading zero]], married, two adult children, lives at
      [[6140 E. Calle Ojos Verdes|addr]], Tucson, [[AZ|place:state abbreviation]] [[85750|zip]]. Cell [[(520) 555-0171|phone]];
      [[marisol.bo@desertmail.example|email]].
  (c) [[Annelise Brandt|p10:full]], who [[died of ovarian cancer in 2011|health:cause of death]]. [[Annelise|p10:first-name]] is survived by one son,
      [[Jonah Brandt-Whitehorse|p11:full]], now 24. [[Jonah|p11:first-name]] has [[autism spectrum disorder|health:diagnosis]] and [[receives SSI|attr!:public benefits status]].
      He lives in a group home run by [[Prairie Oak Supported Living, Inc.|o3:full]] in [[Waukesha|place:city]]. His father
      is [[an enrolled member of the Ho-Chunk Nation|attr:tribal membership]] and is not involved.

Stepson: [[Klaus Brandt|p12:full]], Dieter's son from his first marriage, [[a German citizen living in Stuttgart|attr:citizenship and residence]].
Evie is fond of [[Klaus|p12:first-name]] but says "he has plenty."

3. THE PROBLEM WITH RAFE (client asked that this stay out of any letter mailed to the cabin)

Rafe has [[two OWI convictions|attr:criminal history]], the last in 2019, and [[completed inpatient alcohol treatment|health:substance use treatment]] in 2020.
Evie believes he is drinking again. He [[filed Chapter 7 in 2016|attr!:bankruptcy history]] (Bankr. E.D. Wis.,
No. [[16-24817-gmh|rec:bankruptcy case number]]). Since then she has lent him money "whenever he asked" -- she
thinks about [[thirty-eight thousand five hundred dollars|money!:amount in words]], none of it documented; her check
register supports roughly [[$36,900|money]]. She does not want him cut out. She wants his share
held in trust with someone other than family deciding distributions. He does not know
she is meeting with a lawyer, and she asked that we not call him. (His number, for the
file only: [[920-555-0139|phone]].)

4. ASSETS (from her handwritten list and the statements [[Marisol|p4:first-name]] scanned)

  Residence, 88 Larkspur Lane. Assessed at [[$412,000|money]]. No mortgage. Titled in her name alone.
  Lake cabin, [[N7714 Loon Hollow Road|addr:rural fire-number address]], [[Elkhart Lake|place:village]], WI [[53020|zip]] ([[Sheboygan County|place:county]]). She
    guesses [[365k|money!:abbreviated amount without currency sign]]. In the family since 1966. Property tax parcel [[59016-204471|rec:tax parcel number]].
  Pontoon boat kept at the cabin, [[the "Second Wind"|indirect!:named boat]], registration [[WS 4471 KC|veh:boat registration number]].
  2020 Buick Enclave, VIN [[5GAEVAKW7LX662444|veh:VIN]], plate [[ALK-2291|veh:licence plate]]. She stopped driving in March;
    Bernie drives it for errands.
  [[Lakeshore Community Credit Union|o4:full]] ("[[LCCU|o4:acronym]]"), routing [[064705723|rtn]]:
    checking [[0071-4436612|acct]], balance [[$23,418.77|money]]; savings ending [[-8840|acct!:last four with leading dash]], balance [[$61,050|money]].
    Safe deposit box [[#214|rec!:safe deposit box number]] at the [[Mayfair|place:branch location]] branch. The key is in the blue teapot.
  [[Halvorsen Whitlock Securities|o5:full]], brokerage account [[HW-338-221904|acct:brokerage account number]], about [[$1.14 million|money:amount in millions]]. This
    account was retitled JOINT with Marisol in 2022 "so she could help pay bills."
  IRA at [[Halvorsen Whitlock|o5:short]], account [[7Q4-118835|acct:IRA account number]], about [[$286,000|money]]. The beneficiary on file is
    still [[Dieter|p8:first-name]].
  [[Midwest Fraternal Life|o6:full]] policy [[MFL-0092-55431|rec:life insurance policy number]], face amount [[$50,000|money]]; beneficiary is
    [[St. Hedwig's Catholic Parish|o7:full]].
  Dieter's watch collection, appraised in 2019 at [[$27,300|money]].
  Digital: e-mail [[evie.cb1935@mailbox.example|email]], password written on an index card taped inside
    the desk drawer ([[Dieter1961!|cred:password]]). iPad, serial [[DMPXK2Q7HG5F|dev:device serial number]]; passcode [[0402|cred!:four-digit passcode]].

  Rough total [[$2.25 million|money:amount in millions]], well under the federal exemption. No Form 709 has ever been filed.

5. WHAT SHE WANTS

  Specific gifts: [[$25,000|money]] to [[St. Hedwig's|o7:short]] (she is [[a lifelong Catholic|attr:religion]] and still tithes); [[$10,000|money]] to
  [[Menomonee Valley Animal Rescue|o8:full]]; [[$5,000|money]] to Bernie "if she is still with me"; the watch
  collection to Klaus. She mentioned she is [[a longtime donor to the county Democratic Party|attr:political donations]] but
  wants nothing political in the will.

  Residue in three equal shares: one to Marisol outright; one for Rafe in a discretionary
  trust; one for Jonah in a supplemental needs trust drafted so that he keeps SSI and
  Medicaid. Trustee of both trusts: [[Great Lakes Fiduciary Trust Co.|o9:full]], with Marisol holding the
  power to remove and replace.

  The cabin: Rafe may stay up to five years if he pays the taxes and insurance; then it is
  sold and the proceeds fall into the residue. The boat goes with the cabin.

  Health care agent: Marisol. Alternate: her niece [[Dr. Guadalupe Castellanos|p13:full:full name with title]] ("[[Lupe|p13:nickname]]"),
  [[the only hospice physician in Door County|indirect!:unique professional role]]. Financial agent: Marisol; alternate: the trust company.

  She also wants a HIPAA release naming Marisol and Lupe, so that the doctors will actually talk
  to them. Last winter, when Evie was [[admitted for pneumonia|health:hospital admission]] at [[Kinnickinnic Valley Hospital|o12:full]] for six days
  (in on [[Jan 9|date!:abbreviated date without year]], home on the 15th), nobody there would tell Marisol anything for the first two
  days, and "[[Evelyn|p1:first-name]] was not about to let that happen twice," as she put it.

  Burial beside Dieter at [[Holy Cross Cemetery|place:named cemetery]], Section 14, lot [[203-B|rec!:cemetery lot number]]. Funeral Mass at St. Hedwig's.

6. ISSUES I RAISED

  - The joint brokerage account defeats the three-way split: at death it passes to Marisol
    alone. Marisol volunteered, before I said anything, that it should be undone. Plan:
    create the [[Castellanos-Brandt Revocable Trust|o11:full]] and retitle the account to it. Call the adviser,
    [[Thaddeus Nwosu|p14:full]] ("[[Tad|p14:nickname]]"), direct [[414.555.0155|phone:dotted]], [[tad.nwosu@hwsecurities.example|email]].
  - IRA beneficiary form must be redone now; do not wait for signing.
  - Gift to a paid caregiver. Bernie is employed through [[Comfort Hearth Home Care LLC|o10:full]] at
    [[$31|money]] an hour. Check the agency's policy on gifts. I will see Evie alone again before signing and
    document that the gift is her own idea. [[Kowalczyk|p5:surname]] has worked for her since [[January 2023|date!:month and year of hire]].
  - Loans to Rafe: treat as advancements, or forgive? She wants them forgiven. Put it in writing.
  - She and Dieter signed a marital property agreement on [[June 30, 1994|date:agreement date]]. Neither she nor
    Marisol can find it. Ask [[Prairie Oak|o3:short]] nothing about this; ask the credit union to list the
    contents of the box.
  - Jonah: confirm with his case manager that a third-party trust will not count as his resource.

7. FEES AND NEXT STEPS

  Quoted a flat fee of [[$4,800|money]] for the trust, pour-over will, two powers of attorney, and
  the supplemental needs trust. Retainer of [[$1,500|money]] received, her check no. [[3318|rec!:check number]].
  Drafts to client (large print) and to Marisol by [[10/02/2026|date:draft deadline]]. Signing at the house on
  Tuesday [[the 13th of October|date!:date in words without year]] at 10:30; [[Park|p3:surname!:surname that is also a common word]] and I will witness. [[Dr. Siddiqui|p6:title-surname]]'s office will
  fax an updated capacity note the week before: fax [[(414) 555-0190|phone:fax number]].

[[WH|p2:initials]]/dhp
'''))

# ---------------------------------------------------------------- 24
DOCS.append(D(24, "docx", "court filing draft - motion", "legal", "US",
  title="Draft motion to compel discovery responses",
  ents={"p1": "Paris Delacroix-Mbeki", "p2": "Hunter J. Stavros", "p3": "Oluwaseun Adeyemi-Clark",
        "p4": "Marguerite T. Vance", "p5": "Bartholomew Quigley", "p6": "Irene Castaneda",
        "p7": "Leland Forsythe",
        "o1": "Stavros Precision Hydraulics, Inc.", "o2": "Adeyemi-Clark & Rooney LLP",
        "o3": "Quigley Forsythe Denham, P.C.", "o4": "Ironbridge Managed IT, LLC"},
  distractors=["Fed. R. Civ. P. 37(a)(3)(B)", "Rule 26(b)(1)", "Local Civil Rule 7.1", "Interrogatory No. 9", "Request for Production No. 14", "Exhibit D", "30 days"],
  body=r'''
DRAFT 2 -- OAC edits in bold -- not for filing
# IN THE UNITED STATES DISTRICT COURT FOR THE NORTHERN DISTRICT OF [[OHIO|place!:state in ALL CAPS]], EASTERN DIVISION
[[PARIS DELACROIX-MBEKI|p1:caps:plaintiff name in caption]], Plaintiff,
v.
[[STAVROS PRECISION HYDRAULICS, INC.|o1:caps:defendant company in caption]], and [[HUNTER J. STAVROS|p2:caps:defendant name in caption]], Defendants.
Case No. [[1:26-cv-00832-PAB|rec:federal docket number]]
Judge [[Marguerite T. Vance|p4:full]]
# PLAINTIFF'S MOTION TO COMPEL DISCOVERY RESPONSES AND FOR FEES
Plaintiff [[Paris Delacroix-Mbeki|p1:full:first name that is also a city]] moves under Fed. R. Civ. P. 37(a)(3)(B) and Local Civil Rule 7.1 for an order compelling Defendants [[Stavros Precision Hydraulics, Inc.|o1:full]] ("[[SPH|o1:acronym]]") and [[Hunter J. Stavros|p2:full:first name that is also a common word]] to answer Interrogatory No. 9 and to produce the documents called for by Request for Production No. 14.
## Background
[[Ms. Delacroix-Mbeki|p1:title-surname]] was SPH's controller from [[March 4, 2019|date:hire date]] until she was fired on [[November 21, 2025|date:termination date]], nine days after she reported to the board that [[Mr. Stavros|p2:title-surname]] had charged roughly [[$212,000|money]] in personal expenses to the company's corporate card. She alleges retaliation and unpaid bonus compensation of [[$48,750.00|money]]. Defendants answered that she resigned and that she deleted company files on her last day.
Whether she deleted anything turns on SPH's own access logs. SPH's outside IT vendor, [[Ironbridge Managed IT, LLC|o4:full]] ("[[Ironbridge|o4:short]]"), has admitted in a letter (Exhibit D) that the logs exist. According to that letter the finance share was accessed at 11:52 p.m. on the night of [[11/21/2025|date:numeric date]] from IP address [[203.0.113.47|ip:IPv4]], using the administrator account [[hstavros_adm|cred:username]], and not from the address assigned to Plaintiff's home connection, [[198.51.100.212|ip:IPv4]]. The same letter identifies the machine as a laptop with serial number [[PF-3XK8W21|dev:laptop serial number]] issued to Mr. Stavros, not the laptop Plaintiff returned (serial [[PF-2RM4T90|dev:laptop serial number]]).
## The requests and the responses
Plaintiff served her first set of requests on [[June 12, 2026|date:service date]]. Request for Production No. 14 asks for "all access, VPN and authentication logs for the finance file share for November 2025." Interrogatory No. 9 asks Defendants to identify every person who used the hstavros_adm account that month. Responses were due 30 days later. Defendants served objections only, on [[July 20, 2026|date:response date]], calling the requests "overbroad" and "not proportional."
Counsel conferred by telephone on [[August 6, 2026|date:meet and confer date]] and again by video on [[Aug. 19|date!:abbreviated date without year]]. Defense counsel, [[Bartholomew Quigley|p5:full]] of [[Quigley Forsythe Denham, P.C.|o3:full]], said the logs would be produced "once the client finds them." On [[September 1, 2026|date:letter date]] his partner [[Leland Forsythe|p7:full]] wrote that SPH now believes the logs were overwritten. Ironbridge's letter says otherwise. Declaration of [[Irene Castaneda|p6:full]] (Ironbridge's service manager) is being requested; [[Castaneda|p6:surname]] says she will sign only under subpoena.
## Argument
The logs are relevant under Rule 26(b)(1) because they go to the only defense pleaded. They are proportional because they cover one share for one month and already sit on a vendor portal, **[[https://portal.ironbridge-it.example/tickets/88214|url:vendor ticket link]]**, under ticket [[#88214|rec!:support ticket number]]. Defendants have never said what the burden would be. An unexplained boilerplate objection is no objection at all.
**[[Seun|p3:nickname]] -- add the cases from the [[Hartwell|rec!:earlier matter referred to by name only]] brief here. Also decide whether we mention that [[Hunter|p2:first-name!:first name that is also a common word]] told the board [[Paris|p1:first-name!:first name that is also a city]] was "unstable" because she had taken [[leave for a depressive episode|health:mental health leave]] in 2024. I would leave it out of this motion. -- [[OAC|p3:initials]]**
## Relief requested
Plaintiff asks the Court to (1) compel complete responses within 14 days; (2) order SPH to instruct Ironbridge to preserve and produce the logs; and (3) award fees of [[$6,340|money]] (15.1 hours) under Rule 37(a)(5)(A).
Respectfully submitted,
/s/ [[Oluwaseun Adeyemi-Clark|p3:full]]
Oluwaseun Adeyemi-Clark (Ohio Bar No. [[0091764|govid:state bar number]])
[[Adeyemi-Clark & Rooney LLP|o2:full]]
[[1375 East Ninth Street, 21st Floor|addr:street with floor]]
[[Cleveland|place:city]], [[Ohio|place:state]] [[44114-1724|zip:ZIP+4]]
[[216.555.0177|phone:dotted]] | fax [[216.555.0178|phone:fax number]]
[[oac@acr-law.example|email]]
## Certificate of service
I certify that on [[September 14, 2026|date:service date]] a copy of this motion was served by e-mail on Bartholomew Quigley, [[bquigley@qfdlaw.example|email]], and Leland Forsythe, [[lforsythe@qfdlaw.example|email]], counsel for Defendants.
'''))

# ---------------------------------------------------------------- 25
DOCS.append(D(25, "eml", "internal email", "legal", "US", enc="multipart",
  title="Internal conflict-check email for a new matter",
  ents={"p1": "Graciela Montenegro", "p2": "Stuart Abimbola", "p3": "Chase Wetherington",
        "p4": "Jordan Wetherington", "p5": "Lorraine Zhou", "p6": "Hye-jin Bae",
        "p7": "Anton Marchetti",
        "o1": "Montenegro Abimbola Lowe LLP", "o2": "Wetherington Family Orchards, Inc.",
        "o3": "Blue Heron Agricultural Lending, FLCA", "o4": "Cascade Ridge Packing Co.",
        "o5": "The Wetherington 2009 Irrevocable Trust"},
  distractors=["RPC 1.7", "RPC 1.9", "Schedule K-1", "New Business Intake", "Chapter 12"],
  headers={
    "From": "[[Graciela Montenegro|p1:full]] <[[gmontenegro@mal-law.example|email]]>",
    "To": "Conflicts <[[conflicts@mal-law.example|email]]>",
    "Cc": '"[[Abimbola, Stuart|p2:last-first]]" <[[sabimbola@mal-law.example|email]]>, [[Hye-jin Bae|p6:full]] <[[hbae@mal-law.example|email]]>',
    "Subject": "CONFLICT CHECK - new matter - [[Wetherington|p3:surname]] / orchard partition - need by Thursday",
    "Date": "Mon, [[05 Oct 2026|date:email date]] 16:42:07 -0700"},
  body=r'''Team,

New Business Intake form is in the system but I want a manual check on this one because of the family overlap. Please run all of the following and reply-all.

PROSPECTIVE CLIENT
[[Chase Wetherington|p3:full:first name that is also a common word]] (goes by his middle name; legal name on the deed is [[Franklin C. Wetherington|p3:full!:legal name differing from the name used]])
DOB [[10/30/1978|dob]]. Driver's license [[WDL7K29QF41B|govid!:driver's license number without separators]].
[[4410 Naches Heights Road|addr]], [[Yakima|place:city]], [[WA|place:state abbreviation]] [[98908|zip]]
Cell [[509-555-0133|phone]], [[chase@wetheringtonorchards.example|email]]

ADVERSE / RELATED
1. [[Jordan Wetherington|p4:full:first name that is also a place]] -- [[Chase's younger sister|indirect!:family relationship to named person]], co-owner of the home ranch. Lives in [[Wenatchee|place:city]]. [[Jordan|p4:first-name!:first name that is also a place]] is represented by [[Anton Marchetti|p7:full]] (solo, [[Ellensburg|place:city]]).
2. [[Wetherington Family Orchards, Inc.|o2:full]] ("[[WFO|o2:acronym]]"), UBI [[602 771 348|taxid!:state business identifier with spaces]], EIN [[91-1740226|taxid:EIN]]. [[Chase|p3:first-name!:first name that is also a common word]] and Jordan each hold 50%.
3. [[The Wetherington 2009 Irrevocable Trust|o5:full]] -- holds the 80 acres on [[Tieton Drive|place!:road used as a location]]. Trustee is their mother, [[Lorraine Zhou|p5:full]] (remarried; formerly Lorraine Wetherington -- check both names).
4. [[Blue Heron Agricultural Lending, FLCA|o3:full]] -- operating line, loan no. [[4471-209-88|rec:loan number]], about [[$1.9 million|money:amount in millions]] outstanding; in default since the [[August 1|date!:date without year]] payment. [[Blue Heron|o3:short]] has threatened a receiver.
5. [[Cascade Ridge Packing Co.|o4:full]] -- packer, claims a crop lien of [[$214,600|money]].

WHY I'M WORRIED
- [[Stuart|p2:first-name]], I believe you did the mother's estate plan around 2019 when she was still [[Mrs. Wetherington|p5:title-surname!:former married name]]. If [[Lorraine|p5:first-name]] is a former client and the trust is adverse, that is an RPC 1.9 problem at least.
- [[Hye-jin|p6:first-name]], didn't your group represent [[Cascade Ridge|o4:short]] in a labor matter last year? If they are a current client it is RPC 1.7 and we need waivers or we pass.
- Chase says Jordan [[has been in treatment for an eating disorder|health:mental health treatment]] and "isn't in a state to run anything." I told him we would not be using that. Flagging so nobody is surprised if it shows up in his emails.
- He also mentioned a possible Chapter 12 for WFO. Different engagement; do not open it yet.

He wired a [[$7,500|money]] advance deposit this morning without being asked (trust account ending [[...2204|acct!:last four with ellipsis]]). I have not accepted the engagement. If we can't clear this by Thursday I'm sending it back.

His Schedule K-1 forms and the loan file are at [[https://files.mal-law.example/intake/wetherington-26-1183|url:intake folder link]] (proposed matter no. [[26-1183|rec:matter number]]).

Thanks,
[[Graciela|p1:first-name]]

[[Graciela Montenegro|p1:full]] | Partner
[[Montenegro Abimbola Lowe LLP|o1:full]]
[[32 North 3rd Street, Suite 400|addr:street with suite]], Yakima, WA [[98901|zip]]
d [[509.555.0102|phone:dotted]] | f [[509.555.0103|phone:fax number]]

This message may contain privileged information. If you received it in error, delete it and tell the sender.
'''))
# ---------------------------------------------------------------- 26
DOCS.append(D(26, "txt", "client intake notes", "legal", "CA",
  title="Family law intake notes - separation and protection order",
  ents={"p1": "Thi Mai Nguyen-Fraser", "p2": "Callum Fraser", "p3": "Kiran Sandhu", "p4": "Owen Fraser",
        "p5": "Linh Fraser", "p6": "Thi Lan Nguyen", "p7": "Daljit K. Grewal",
        "o1": "Pattullo Marine Fabricators Ltd.", "o2": "Fraser Valley Savings Credit Union",
        "o3": "Guildford Family Dental", "o4": "Coastline Bank of Canada", "o5": "Bear Creek Elementary"},
  distractors=["Form F3", "Form F8", "Family Law Act s. 183", "IEP", "RRSP", "Labour Day"],
  body=r'''INTAKE - FAMILY                file # [[F-26-0219|rec:firm file number]]             taken by: [[KS|p3:initials]] ([[Kiran Sandhu|p3:full]], articled student)
Thurs [[8 Oct 2026|date:day month year]], 2:10 pm, in person, [[Surrey|place:city]] office. Interpreter not needed.

CLIENT:  [[Nguyen-Fraser, Thi Mai|p1:last-first]]   -- goes by "[[Mai|p1:nickname]]"
DOB [[1988-11-03|dob:ISO date]]     SIN [[683 248 363|taxid:SIN with spaces]]  (need it for the Form F8)
Addr: [[#1204 - 13618 100 Avenue|addr:unit number before street number]], Surrey [[BC|place:province abbreviation]]  [[V3T 0A8|zip:Canadian postal code]]
   *** DO NOT MAIL ANYTHING HERE. husband opens the mailbox. ***
Safe phone [[604-555-0191|phone]] -- TEXT ONLY, never after 9 pm
Email [[mai.nf.safe@inbox.example|email]] (new acct, he doesn't know about it)
Client portal set up today: user [[mnguyenfraser|cred:username]] / temp pw [[Maple!4471|cred:password]]

OTHER SIDE:  [[Callum Fraser|p2:full]], dob [[14 Feb 1985|dob:day month year]]. Foreman at [[Pattullo Marine Fabricators Ltd.|o1:full]]
([[Pattullo Marine|o1:short]]), she thinks about [[118k|money!:abbreviated salary without currency sign]] plus overtime. No lawyer yet as far as she knows.

Married [[2015-08-22|date:marriage date]] in [[Kelowna|place:city]]. Still under one roof. She moved into the spare room
[[July 1, 2026|date:separation date]] -- use that as separation date unless [[DKG|p7:initials]] says otherwise.

KIDS:  [[Owen|p4:first-name]], 9 (b. [[2017-05-19|dob:ISO date]]) and [[Linh|p5:first-name]], 6. Owen has [[ADHD|health:diagnosis of a child]], on an IEP at
[[Bear Creek Elementary|o5:full]]. Both kids with her most of the time; [[callum|p2:first-name!:first name in lower case]] works 6 days.

WHAT HAPPENED: on the Labour Day weekend he [[shoved her into the kitchen counter|indirect!:incident of family violence]] in front of
Owen. [[Bruised ribs|health:injury]], went to walk-in next day, has the visit record. RCMP attended;
file [[2026-118834|rec:police file number]]. No charges "yet". She says he has [[an assault conviction from 2012 in Alberta|attr:criminal history]]
(bar fight). He controls the online banking and changed the password last month.

IMMIGRATION: she is [[a permanent resident, not a citizen|attr:immigration status]] -- he sponsored her in 2014 and tells her he can
"send her back". Told her that is not how it works but DKG to confirm. Parents are in
[[Ho Chi Minh City|place:city abroad]]. Family is [[Buddhist|attr:religion]]; she wants the kids to keep going to temple.

HEALTH: [[seeing a counsellor for anxiety|health:mental health treatment]] since June. Also [[14 weeks pregnant|health:pregnancy]]. He does not know.

MONEY / PROPERTY
 - condo (joint). mortgage w/ [[Fraser Valley Savings Credit Union|o2:full]], approx [[$512,000|money]] owing, worth maybe [[780k|money!:abbreviated amount without currency sign]]
 - joint chequing at the credit union, acct [[100-448-2217|acct]]
 - her own acct opened last month at [[Coastline Bank of Canada|o4:full]], ends [[9920|acct!:last four digits only]]. About [[$1,850|money]] in it.
 - his pension (union plan -- he is [[a member of the Boilermakers local|attr:union membership]]); her RRSP about [[C$41,000|money:Canadian dollar prefix]]
 - 2022 F-150, his name, BC plate [[RK4 81T|veh:licence plate]]
 - her job: reception at [[Guildford Family Dental|o3:full]], [[$24.50|money]]/hr, 22 hrs a week

WANTS: protection order (Family Law Act s. 183), kids primarily with her, child support,
to stay in the condo until the baby comes.

RETAINER: [[her sister Thi Lan|indirect!:family relationship to named person]] ([[Thi Lan Nguyen|p6:full]], [[Burnaby|place:city]], cell [[778 555 0164|phone!:spaces only]]) will
e-transfer [[$3,000|money]] by Friday. Receipt goes to the sister NOT the client.

NEXT: [[Daljit K. Grewal|p7:full]] to call her Tues between 10 and 2. Draft Form F3 for the
[[New Westminster|place:court registry location]] registry. Ask [[Ms. Nguyen-Fraser|p1:title-surname]] to bring walk-in record + photos.
'''))

# ---------------------------------------------------------------- 27
DOCS.append(D(27, "docx", "criminal defense intake memo", "legal", "US",
  title="Criminal defense intake memo - new felony client",
  ents={"p1": "Mateo Ibarra-Lund", "p2": "Rhiannon Castellano", "p3": "Cole Brannigan", "p4": "Kaylee Voss",
        "p5": "Travis Oyelaran", "p6": "Egon Pruett", "p7": "Lucia Ibarra", "p8": "Benedikt Reyes",
        "o1": "Castellano & Reyes Criminal Defense, Ltd.", "o2": "Sierra Crest Roofing & Gutter LLC",
        "o3": "High Desert Bail Bonds"},
  distractors=["NRS 453.337", "NRS 202.360", "Miranda", "Category B felony", "Department 4", "Padilla"],
  body=r'''
# [[Castellano & Reyes Criminal Defense, Ltd.|o1:full]]
PRIVILEGED AND CONFIDENTIAL -- ATTORNEY-CLIENT COMMUNICATION / WORK PRODUCT
**To:** [[Benedikt Reyes|p8:full]]
**From:** [[Rhiannon Castellano|p2:full]]
**Date:** [[September 29, 2026|date:memo date]]
**Re:** New client intake -- State v. [[Ibarra-Lund|p1:surname]], Case No. [[CR26-1447|rec:criminal case number]]
## Client
| Field | Detail |
| Name | [[IBARRA-LUND, MATEO|p1:last-first]] |
| Also known as | "[[Teo|p1:nickname]]" |
| Date of birth | [[06/27/1996|dob]] |
| SSN | [[493211306|ssn!:SSN without dashes]] |
| [[Nevada|place:state]] DL | [[1702884415|govid!:driver's license number, unlabelled digits]] |
| Booking no. | [[26-0091873|rec:jail booking number]] |
| Status | [[lawful permanent resident|attr:immigration status]] |
| Home | [[2290 Wedekind Road, Apt. 14|addr:street with apartment]] |
| City | [[Sparks|place:city]], [[NV|place:state abbreviation]] [[89431|zip]] |
| Phone | [[775-555-0148|phone]] (phone seized) |
| Mother | [[Lucia Ibarra|p7:full]], [[775-555-0115|phone]] |
## Charges and custody
[[Mateo Ibarra-Lund|p1:full]] was arrested on [[Sept. 24, 2026|date:arrest date]] after a traffic stop on [[Pyramid Way|place!:road used as a location]]. He is charged with possession of a controlled substance for sale (NRS 453.337, a Category B felony) and possession of a firearm by a prohibited person (NRS 202.360). Bail was set at [[$25,000|money]] by [[Judge Egon Pruett|p6:full:full name with title]] in Department 4. His mother posted through [[High Desert Bail Bonds|o3:full]] and paid a premium of [[$3,750|money]]; she put up the title to her car. He was released the evening of [[9/26/26|date!:two-digit year]]. Arraignment is set for [[October 14, 2026|date:arraignment date]].
## What he says happened
He was driving his girlfriend's car, a 2019 Honda Accord, VIN [[1HGCV1F32KU724601|veh:VIN]], Nevada plate [[448-LRT|veh:licence plate]]. The girlfriend is [[Kaylee Voss|p4:full]]. Detective [[Cole Brannigan|p3:full]] says he smelled marijuana and searched the trunk, where he found a backpack with about 61 grams of methamphetamine and a 9 mm pistol, serial number [[BKRT417|dev:firearm serial number]]. [[Teo|p1:nickname]] says the backpack belongs to [[Kaylee's cousin|indirect!:family relationship to named person]], [[Travis Oyelaran|p5:full]] ("[[Tre|p5:nickname]]"), who had borrowed the car that weekend. He did not consent to the search. He says he asked for a lawyer twice before [[Brannigan|p3:surname]] kept questioning him; if that holds up we have a Miranda issue.
Police also seized his phone, IMEI [[356938112047755|dev:IMEI]], and have applied for a warrant. He gave them the passcode ([[271996|cred!:six-digit phone passcode]]) at the roadside. He thinks there are messages with [[Tre|p5:nickname]] on a marketplace account under the username [[teo_lund96|cred:username]].
## Record and exposure
He has [[a 2017 felony conviction for burglary|attr:criminal history]] in [[Washoe County|place:county]], case [[CR17-0832|rec:prior criminal case number]], for which he served 14 months. That prior is what makes the gun charge possible. Because he is [[not a U.S. citizen|attr!:citizenship status stated in the negative]], a drug-sale conviction almost certainly means removal. He was brought from [[Sinaloa|place:region abroad]] at age four and has no family there. We need a Padilla advisal in writing before any plea discussion.
## Personal circumstances
He has worked for [[Sierra Crest Roofing & Gutter LLC|o2:full]] since 2022 at [[$27|money]] an hour; his foreman will write a letter. He reports [[daily methamphetamine use until last spring|health:substance use]] and [[six months sober|health!:recovery status]] since entering an outpatient program. He takes [[buprenorphine|health:medication]] and is worried about missing doses if he is taken back into custody. [[Ms. Voss|p4:title-surname]] is [[five months pregnant|health:pregnancy]].
## Fee
Flat fee through preliminary hearing: [[$8,500|money]]. His mother paid [[$2,000|money]] by card today (Visa ending [[8293|card!:last four digits only]], exp. [[04/29|exp]]). The balance is due in four payments.
## To do
- [[Ben|p8:nickname]]: request body-camera video and the dispatch log today.
- Subpoena [[Sierra Crest|o2:short]] time sheets for the weekend before the arrest.
- Interview Ms. Voss separately; she may need her own lawyer.
-- [[RC|p2:initials]]
'''))

# ---------------------------------------------------------------- 28
DOCS.append(D(28, "txt", "loan application", "accounting", "US",
  title="Small business loan application summary prepared by the borrower's accountant",
  ents={"p1": "Ingrid Solveig Haugen", "p2": "Babajide Akinwande", "p3": "Florence Whitlock-Tan",
        "p4": "Marcus Delgado",
        "o1": "Tamarack Ridge Brewing Co., LLC", "o2": "Whitlock-Tan & Associates, CPAs",
        "o3": "First Bitterroot Bank", "o4": "Clark Fork Federal Credit Union",
        "o5": "Northern Rockies Equipment Finance, Inc."},
  distractors=["SBA Form 1919", "Form 413", "Form 1065", "7(a)", "10-barrel", "1.41x"],
  body=r'''SBA 7(a) LOAN APPLICATION -- BORROWER INFORMATION SUMMARY
Prepared by [[Whitlock-Tan & Associates, CPAs|o2:full]] for submission to [[First Bitterroot Bank|o3:full]]
Lender contact: [[Marcus Delgado|p4:full]], VP Commercial Lending, [[mdelgado@firstbitterroot.example|email]], [[406-555-0170|phone]]
Date prepared: [[08/31/2026|date:preparation date]]                      Lender ref: [[FBB-SBA-26-00419|rec:loan application number]]

A. APPLICANT BUSINESS
Legal name:      [[Tamarack Ridge Brewing Co., LLC|o1:full]]  (d/b/a "[[Tamarack Ridge|o1:short]]")
EIN:             [[81-4092275|taxid:EIN]]
Address:         [[1180 Railyard Spur, Unit C|addr:street with unit]], [[Missoula|place:city]], [[MT|place:state abbreviation]] [[59802|zip]]
Formed:          [[March 11, 2019|date:formation date]] ([[Montana|place:state]] LLC, taxed as a partnership -- files Form 1065)
Employees:       14 (9 full-time)
Web:             [[www.tamarackridgebrewing.example|url]]

B. LOAN REQUEST
Amount:          [[$640,000|money]], 10-year term
Use of proceeds: 10-barrel brewhouse expansion ([[$410,000|money]]); refinance equipment note with
                 [[Northern Rockies Equipment Finance, Inc.|o5:full]], loan no. [[NRE-0077-31854|rec:loan number]], payoff [[$148,220.16|money]];
                 working capital ([[$81,779.84|money]]).

C. OWNERS (20% or more) -- from SBA Form 1919 and Form 413
1. [[HAUGEN, INGRID SOLVEIG|p1:last-first]] -- 60%, managing member
   DOB [[Nov. 8, 1984|dob:abbreviated month]]   SSN [[115-14-4666|ssn]]   MT driver's license [[0811198441208|govid!:driver's license number, digits only]]
   Home: [[742 Cherry Blossom Court|addr]], Missoula, MT [[59801|zip]]. Cell [[(406) 555-0124|phone]].
   U.S. citizen: yes. Criminal history question: YES -- [[misdemeanor DUI, 2011, disclosed|attr:criminal history]].
   Personal net worth per Form 413: [[$386,400|money]].
2. [[Babajide Akinwande|p2:full]] ("[[Jide|p2:nickname]]") -- 40%, head brewer
   DOB [[1990-02-17|dob:ISO date]]   SSN [[168964978|ssn!:SSN without dashes]]
   Home: [[PO Box 317|addr:PO Box]], [[Lolo|place:small town]], MT [[59847|zip]]. Cell [[406.555.0186|phone:dotted]]. [[jide@tamarackridgebrewing.example|email]]
   U.S. citizen: no -- [[lawful permanent resident, card no. A-208-661-573|attr!:immigration status with card number]].
   Personal net worth per Form 413: [[$71,950|money]]. Student loans of [[$38K|money!:abbreviated amount]] outstanding.

D. BANKING
Operating account: First Bitterroot Bank, routing [[102296990|rtn]], account [[2000417738|acct]]
Payroll account:   [[Clark Fork Federal Credit Union|o4:full]], routing [[124493946|rtn]], account [[77-104-5529|acct]]
Average collected balance, last 12 months: [[$58,300|money]]

E. COLLATERAL OFFERED
 - Brewhouse and fermentation tanks (to be purchased); existing glycol chiller, serial [[GC-2291-0457A|dev:equipment serial number]]
 - 2021 Ford Transit delivery van, VIN [[1FTFW1E53NC506833|veh:VIN]], MT plate [[4-71802B|veh:licence plate]]
 - Second lien on [[Ms. Haugen|p1:title-surname]]'s residence (first mortgage balance [[$214,000|money]])

F. FINANCIAL HIGHLIGHTS (from the reviewed statements)
                       FY2024        FY2025        YTD (7 mos.)
 Revenue             1,412,880     1,688,415       1,104,270
 Net income             61,340        97,125          72,060
 Owner draws            84,000        96,000          56,000
Debt service coverage on the proposed loan: 1.41x on 2025 results.

G. PREPARER'S NOTES (not for the lender package)
[[Ingrid|p1:first-name]] wants the taproom lease assigned before closing; landlord has not answered.
[[Jide|p2:nickname]]'s green card expires next June -- lender will ask; he has the renewal receipt.
The 2025 owner draws include [[twelve thousand dollars|money!:amount in words]] that went to Ingrid's brother and should be
reclassified as a loan. [[FWT|p3:initials]] to discuss before we sign the compilation letter.

[[Florence Whitlock-Tan|p3:full]], CPA (MT license [[PAC-CPAP-LIC-004417|govid:CPA license number]])
[[florence@whitlocktancpa.example|email]]   office [[406 555 0111|phone!:spaces only]]
''',
  ok=["1,412,880", "1,688,415", "1,104,270"]))

# ---------------------------------------------------------------- 29
DOCS.append(D(29, "xlsx", "payroll register", "accounting", "US",
  title="Payroll register with employee master and garnishments",
  ents={"p1": "Dolores Ybarra", "p2": "Winston Achebe", "p3": "Siobhan O'Malley", "p4": "Grace Tanaka",
        "p5": "Ruben van der Merwe", "p6": "April Kowalski-Reed", "p7": "Efraim Goldfarb",
        "o1": "Copperline Dental Laboratory, Inc.", "o2": "Saguaro Federal Credit Union",
        "o3": "Pinnacle West Community Bank"},
  distractors=["Form 941", "PP19", "FICA", "Biweekly"],
  ok=["86.25", "2026"],
  sheets=[
    ("Register PP19", [
      ["[[Copperline Dental Laboratory, Inc.|o1:full]] -- Payroll Register", None, None, None, None, None, None],
      ["Biweekly pay period PP19", "Check date:", dt("2026-09-18", "mm/dd/yyyy", "date:check date"), "EIN", "[[86-0714493|taxid:EIN]]", None, None],
      ["Emp ID", "Employee", "Hours", "Gross", "Fed W/H", "FICA", "Net"],
      ["[[E-1004|rec:employee ID]]", "[[Ybarra, Dolores|p1:last-first]]", 80, amt(2884.62, "usd", "money!:currency cell (stored as a bare number)"), amt(346.15, "usd", "money!:currency cell (stored as a bare number)"), amt(220.67, "usd", "money!:currency cell (stored as a bare number)"), amt(2317.80, "usd", "money!:currency cell (stored as a bare number)")],
      ["[[E-1011|rec:employee ID]]", "[[Achebe, Winston|p2:last-first]]", 80, amt(2400.00, "usd", "money!:currency cell (stored as a bare number)"), amt(264.00, "usd", "money!:currency cell (stored as a bare number)"), amt(183.60, "usd", "money!:currency cell (stored as a bare number)"), amt(1952.40, "usd", "money!:currency cell (stored as a bare number)")],
      ["[[E-1019|rec:employee ID]]", "[[O'Malley, Siobhan|p3:last-first]]", 72.5, amt(1921.25, "usd", "money!:currency cell (stored as a bare number)"), amt(192.13, "usd", "money!:currency cell (stored as a bare number)"), amt(146.98, "usd", "money!:currency cell (stored as a bare number)"), amt(1582.14, "usd", "money!:currency cell (stored as a bare number)")],
      ["[[E-1023|rec:employee ID]]", "[[Tanaka, Grace|p4:last-first]]", 80, amt(3461.54, "usd", "money!:currency cell (stored as a bare number)"), amt(484.62, "usd", "money!:currency cell (stored as a bare number)"), amt(264.81, "usd", "money!:currency cell (stored as a bare number)"), amt(2712.11, "usd", "money!:currency cell (stored as a bare number)")],
      ["[[E-1030|rec:employee ID]]", "[[van der Merwe, Ruben|p5:last-first]]", 86.25, amt(2156.25, "usd", "money!:currency cell (stored as a bare number)"), amt(215.63, "usd", "money!:currency cell (stored as a bare number)"), amt(164.95, "usd", "money!:currency cell (stored as a bare number)"), amt(1375.67, "usd", "money!:currency cell (stored as a bare number)")],
      ["[[E-1034|rec:employee ID]]", "[[Kowalski-Reed, April|p6:last-first]]", 40, amt(880.00, "usd", "money!:currency cell (stored as a bare number)"), amt(52.80, "usd", "money!:currency cell (stored as a bare number)"), amt(67.32, "usd", "money!:currency cell (stored as a bare number)"), amt(759.88, "usd", "money!:currency cell (stored as a bare number)")],
      ["TOTAL", None, 438.75, amt(13703.66, "usd", "money!:currency cell (stored as a bare number)"), amt(1555.33, "usd", "money!:currency cell (stored as a bare number)"), amt(1048.33, "usd", "money!:currency cell (stored as a bare number)"), amt(10700.00, "usd", "money!:currency cell (stored as a bare number)")],
      ["Form 941 liability this period", None, None, None, None, None, amt(3651.99, "usd", "money!:currency cell (stored as a bare number)")],
      ["Approved by [[E. Goldfarb|p7:short:initial + surname]], controller", None, None, None, None, None, None],
    ]),
    ("Employee Master", [
      ["Emp ID", "Name", "SSN", "DOB", "Hire date", "City", "DD routing", "DD account", "Rate", "Notes"],
      ["E-1004", "[[Dolores Ybarra|p1:full]]", "[[518-56-8386|ssn]]", dt("1971-12-05", "mm/dd/yyyy", "dob!:birth date in a real date cell (stored as a serial number)"), dt("2008-04-14", "mm/dd/yyyy", "date:hire date"), "[[Tucson|place:city]]", "[[127400981|rtn]]", "[[4410098127|acct]]", amt(36.06, "usd", "money!:currency cell (stored as a bare number)"), "lab manager"],
      ["E-1011", "[[Winston Achebe|p2:full]]", "[[663 36 5675|ssn!:SSN with spaces]]", dt("1989-07-30", "mm/dd/yyyy", "dob!:birth date in a real date cell (stored as a serial number)"), dt("2017-10-02", "mm/dd/yyyy", "date:hire date"), "[[Marana|place:town]]", "127400981", "[[4410233906|acct]]", amt(30.00, "usd", "money!:currency cell (stored as a bare number)"), "[[H-1B, expires 03/2027|attr:immigration status]]"],
      ["E-1019", "[[Siobhan O'Malley|p3:full]]", num(170071459, "ssn!:SSN stored as a number, no dashes"), dt("1995-03-22", "mm/dd/yyyy", "dob!:birth date in a real date cell (stored as a serial number)"), dt("2021-06-07", "mm/dd/yyyy", "date:hire date"), "Tucson", "[[115028595|rtn]]", "[[00-55-1873042|acct]]", amt(26.50, "usd", "money!:currency cell (stored as a bare number)"), "[[intermittent FMLA - migraines|health:leave reason]]"],
      ["E-1023", "[[Grace Tanaka|p4:full:first name that is also a common word]]", "[[271-17-5505|ssn]]", dt("1982-09-09", "mm/dd/yyyy", "dob!:birth date in a real date cell (stored as a serial number)"), dt("2012-01-16", "mm/dd/yyyy", "date:hire date"), "[[Oro Valley|place:town]]", "127400981", "[[4410771265|acct]]", amt(43.27, "usd", "money!:currency cell (stored as a bare number)"), "CDT, ceramics lead"],
      ["E-1030", "[[Ruben van der Merwe|p5:full]]", "[[xxx-xx-3900|ssn!:masked SSN]]", dt("1978-01-27", "mm/dd/yyyy", "dob!:birth date in a real date cell (stored as a serial number)"), dt("2019-08-19", "mm/dd/yyyy", "date:hire date"), "[[Sahuarita|place:town]]", "115028595", "[[00-55-2290118|acct]]", amt(25.00, "usd", "money!:currency cell (stored as a bare number)"), "garnishment - see tab 3"],
      ["E-1034", "[[April Kowalski-Reed|p6:full:first name that is also a month]]", "[[576-79-0681|ssn]]", dt("2003-11-14", "mm/dd/yyyy", "dob!:birth date in a real date cell (stored as a serial number)"), dt("2026-05-26", "mm/dd/yyyy", "date:hire date"), "Tucson", "paper check", None, amt(22.00, "usd", "money!:currency cell (stored as a bare number)"), "part-time; [[student at Pima Tech|indirect!:school attended]]"],
      [None],
      ["DD banks:", "127400981 = [[Saguaro Federal Credit Union|o2:full]]", None, "115028595 = [[Pinnacle West Community Bank|o3:full]]"],
    ]),
    ("Garnishments", [
      ["Emp ID", "Employee", "Type", "Case / order no.", "Payee", "Per period", "Balance", "Start"],
      ["E-1030", "[[R. van der Merwe|p5:short:initial + surname]]", "Child support", "[[DR-2021-004418|rec:family court case number]]", "State disbursement unit", amt(412.00, "usd", "money!:currency cell (stored as a bare number)"), None, dt("2021-11-05", "d-mmm-yy", "date!:date cell shown as d-mmm-yy (stored as a serial number)")],
      ["E-1030", "R. van der Merwe", "Creditor", "[[CV2024-09177|rec:civil case number]]", "[[Pinnacle West|o3:short]]", amt(188.00, "usd", "money!:currency cell (stored as a bare number)"), amt(3902.14, "acct", "money!:currency cell (stored as a bare number)"), dt("2024-06-21", "d-mmm-yy", "date!:date cell shown as d-mmm-yy (stored as a serial number)")],
      ["E-1011", "[[W. Achebe|p2:short:initial + surname]]", "Student loan", "[[AWG-88-2291045|rec:wage garnishment order number]]", "U.S. Dept. of Education", amt(240.00, "usd", "money!:currency cell (stored as a bare number)"), amt(11480.50, "acct", "money!:currency cell (stored as a bare number)"), dt("2025-02-14", "d-mmm-yy", "date!:date cell shown as d-mmm-yy (stored as a serial number)")],
    ]),
  ]))

# ---------------------------------------------------------------- 31
DOCS.append(D(31, "txt", "expense report", "general", "US",
  title="Employee travel expense report with approver comments",
  ents={"p1": "Anneliese Okoro-Baptiste", "p2": "Reginald Fontaine", "p3": "Mei-Ling Castillo",
        "o1": "Brightwater Analytics Group", "o2": "Halcyon Mutual Insurance Company",
        "o3": "The Wexley Riverside", "o4": "Peachtree Fleet Rentals"},
  distractors=["Policy T-4", "GL 6420", "per diem", "Economy Plus", "RFP"],
  body=r'''[[BRIGHTWATER ANALYTICS GROUP|o1:caps]] -- EXPENSE REPORT                      Report # [[ER-2026-03318|rec:expense report number]]

Employee:    [[Anneliese Okoro-Baptiste|p1:full]]          Emp. ID: [[BW-00672|rec:employee ID]]
Dept:        Client Services (GL 6420)         Approver: [[Reginald Fontaine|p2:full]]
Purpose:     On-site kickoff, [[Halcyon Mutual Insurance Company|o2:full]] ([[Hartford|place:city]], [[CT|place:state abbreviation]])
Trip dates:  [[09/14/2026|date:trip start]] - [[09/17/2026|date:trip end]]
Paid with:   corporate Amex ending [[34224|card!:last five digits of an Amex]] unless marked (P) = personal

DATE     ITEM                                             AMOUNT
[[09/14|date!:month and day only]]    Airfare [[ATL-BDL|place!:airport codes showing origin and destination]] r/t, Economy Plus, conf. [[QK7M2X|rec!:airline confirmation code]]       [[$612.40|money]]
09/14    Rideshare, home to airport (P)                   [[$38.75|money]]
09/14    Dinner, self                                     [[$41.20|money]]
09/14    [[The Wexley Riverside|o3:full]], 3 nights, folio [[88104-2|rec:hotel folio number]]       [[$887.61|money]]
[[09/15|date!:month and day only]]    Client dinner, 6 people -- see note 1            [[$544.90|money]]
09/15    [[Peachtree Fleet Rentals|o4:full]], agreement [[RA 5571 0294|rec!:rental agreement number with spaces]], car plate
         CT [[AV-90217|veh:licence plate]]                                   [[$203.18|money]]
[[09/16|date!:month and day only]]    Parking, [[Halcyon|o2:short]] garage                          [[$24.00|money]]
[[09/17|date!:month and day only]]    Fuel (P)                                         [[$31.07|money]]
                                                TOTAL     [[$2,383.11|money]]
                                 Less corporate card     [[($2,313.29)|money!:negative amount in parentheses]]
                                 Due to employee            [[$69.82|money]]

Reimburse to checking on file: routing [[061980279|rtn]], acct ending [[x4419|acct!:masked account number]].

NOTES
1. Dinner attendees from Halcyon: [[M. Castillo|p3:short:initial + surname]] (VP Claims) and three of her staff, plus
   Reggie and me. Over the Policy T-4 limit of $75 a head by about [[fifteen dollars|money!:amount in words]] each;
   [[Reggie|p2:nickname]] approved at the table.
2. The hotel put the first night on my personal Visa by mistake ([[4697 7220 0063 3395|card:card number with spaces]],
   exp [[11/27|exp]]) and then re-billed the Amex. Refund of [[$295.87|money]] is pending; the front desk
   asked me to read them the CVV ([[406|cvv]]) over the phone to process it. Not claiming it.
3. I skipped per diem on the 16th because [[Mei-Ling|p3:first-name]] hosted lunch.

APPROVER COMMENTS ([[R. Fontaine|p2:short:initial + surname]], [[9/22|date!:month and day only]]): Approved. [[Anneliese|p1:first-name]] -- please don't put full card
numbers in these, finance scans them into the shared drive. Also flag the Halcyon dinner
to legal: [[Castillo|p3:surname]] is on their vendor selection committee and we are mid-RFP.
''',
  ok=["$75"]))
# ---------------------------------------------------------------- 30
DOCS.append(D(30, "pdf", "audit workpaper", "accounting", "US", length="long",
  title="Audit workpaper C-1: cash, bank confirmations and reconciliation testing",
  ents={"p1": "Tomoko Nakagawa-Ruiz", "p2": "Priyanka Deshmukh", "p3": "Augustus Calloway",
        "p4": "Henrik Ostrander", "p5": "Delphine Ostrander", "p6": "Maribel Quintanilla",
        "p7": "Lindiwe Mabuza", "p8": "Cormac Brennan", "p9": "Jae-won Seo", "p10": "Niamh Gallagher",
        "p11": "Wendell Pike",
        "o1": "Ostrander Marine Hardware, Inc.", "o2": "Bellweather Stokes LLP",
        "o3": "Penobscot Harbor Trust Company", "o4": "Casco Mutual Savings Bank",
        "o5": "Liffey Commercial Bank DAC", "o6": "Skerries Rope & Rigging Ltd.",
        "o7": "Downeast Diesel Service LLC", "o8": "Ostrander Family Realty Trust"},
  distractors=["AU-C 505", "AU-C 240", "ASC 230", "Form 1099-NEC", "W/P C-1", "$5,000", "ECB"],
  body=r'''
# [[Bellweather Stokes LLP|o2:full]] -- AUDIT WORKPAPER
**Client:** [[Ostrander Marine Hardware, Inc.|o1:full]] ("[[OMH|o1:acronym]]")
**Engagement no.:** [[BS-2026-1147|rec:engagement number]]
**Period:** fiscal year ended [[June 30, 2026|date:fiscal year end]]
**W/P C-1:** Cash -- lead sheet, bank confirmations, reconciliation testing
**Prepared by:** [[T. Nakagawa-Ruiz|p1:short:initial + surname]] ([[TNR|p1:initials]]), [[08/19/2026|date:preparation date]]
**Reviewed by:** [[Priyanka Deshmukh|p2:full]] ([[PD|p2:initials]]), [[08/24/2026|date:review date]]
**Partner:** [[Augustus Calloway|p3:full]]
## 1. Objective
Obtain evidence that cash balances exist, are complete, are owned by the client and are stated at the right amount at year end, and respond to the fraud risks identified at planning (AU-C 240): management override, and transactions with the owner's family.
## 2. Accounts at year end
Per the general ledger and the client's listing, OMH had five cash accounts at [[6/30|date!:month and day only]]:
- Operating, [[Penobscot Harbor Trust Company|o3:full]], acct [[0118 4420 771|acct!:account number with spaces]]
- Payroll, Penobscot Harbor Trust Company, acct [[0118 4420 902|acct!:account number with spaces]]
- Money market, [[Casco Mutual Savings Bank|o4:full]], acct [[MM-70-338215|acct]]
- Euro account for supplier payments, [[Liffey Commercial Bank DAC|o5:full]]
- Petty cash, [[Rockland|place:city]] store, [[$600|money]] imprest
Routing number for both [[Penobscot Harbor|o3:short]] accounts: [[028549585|rtn]]
Routing number at [[Casco Mutual|o4:short]]: [[029439759|rtn]]
Euro account IBAN: [[IE47 BOFI 3661 6849 9049 22|iban:IBAN in groups of four]]
Euro account SWIFT: [[LIFCIE2DXXX|acct:SWIFT code]]
## 3. Lead sheet
| Account | Per G/L | Per bank | Ref |
| Operating | [[$412,906.13|money]] | [[$455,218.40|money]] | C-2 |
| Payroll | [[$18,440.00|money]] | [[$31,072.55|money]] | C-3 |
| Money market | [[$250,317.82|money]] | $250,317.82 | C-4 |
| Euro (USD equiv.) | [[$66,180.09|money]] | [[$67,004.90|money]] | C-5 |
| Petty cash | [[$600.00|money]] | n/a | C-6 |
| Total | [[$748,444.04|money]] | | |
Total agrees to the trial balance and to the statement of cash flows (ASC 230) without exception.
## 4. Confirmations (AU-C 505)
Confirmation requests were authorized by the controller, [[Maribel Quintanilla|p6:full]], on [[July 8, 2026|date:authorization date]] and sent by us directly to each bank. We kept control of the requests throughout.
- Penobscot Harbor: request ID [[CNF-4471-88213|rec:confirmation request ID]]; response received [[7/21/26|date!:two-digit year]] from [[Cormac Brennan|p8:full]], commercial services, [[207-555-0142|phone]].
- Casco Mutual: request ID [[CNF-4471-88214|rec:confirmation request ID]]; response received [[7/16/26|date!:two-digit year]]. No exceptions.
- [[Liffey Commercial|o5:short]]: paper confirmation mailed [[9 July 2026|date:day month year]] to [[14 Usher's Quay|addr:street address abroad]], [[Dublin 8|place:postal district]]. Reply signed by [[Niamh Gallagher|p10:full]] received [[4 August 2026|date:day month year]]. Balance confirmed at [[EUR 61,702.33|money:euro amount with currency code]].
The Penobscot Harbor response listed a THIRD account that is not on the client's listing or in the general ledger: a savings account ending [[...5518|acct!:last four with ellipsis]], opened [[March 3, 2026|date:account opening date]], titled "[[Ostrander Marine Hardware Inc.|o1:full!:company name written without its comma]] -- Special", with a 6/30 balance of [[$37,250.00|money]]. The only authorized signer is [[Delphine Ostrander|p5:full]]. See section 7.
## 5. Reconciliation testing -- operating account (C-2)
We obtained the June reconciliation prepared by [[Jae-won Seo|p9:full]] (staff accountant) and approved by [[Ms. Quintanilla|p6:title-surname]] on [[July 11|date!:date without year]]. We footed it, agreed the bank balance to the confirmation and the book balance to the general ledger, and tested reconciling items as follows.
Deposits in transit of [[$9,884.25|money]] (two items) cleared on [[July 1|date!:date without year]] and [[July 2|date!:date without year]]. No exception.
Outstanding checks total [[$52,196.52|money]] (23 items). We tested all items over $5,000 and a sample of five others to the July and August statements:
| Check | Date | Payee | Amount |
| [[20418|rec!:check number]] | [[06/26|date!:month and day only]] | [[Skerries Rope|o6:short]] | [[$18,406.00|money]] |
| [[20421|rec!:check number]] | [[06/29|date!:month and day only]] | [[Downeast Diesel|o7:short]] | [[$7,912.40|money]] |
| [[20423|rec!:check number]] | 06/29 | [[H. Ostrander|p4:short:initial + surname]] | [[$12,500.00|money]] |
| [[20377|rec!:check number]] | [[05/08|date!:month and day only]] | [[L. Mabuza|p7:short:initial + surname]] | [[$1,264.17|money]] |
| [[20425|rec!:check number]] | [[06/30|date!:month and day only]] | [[W. Pike|p11:short:initial + surname]] | [[$850.00|money]] |
Payees in full: [[Skerries Rope & Rigging Ltd.|o6:full]] (inventory; the same supplier is paid in euros from the [[Dublin|place:city abroad]] account) and [[Downeast Diesel Service LLC|o7:full]] (forklift repair).
Check 20423 to [[Henrik Ostrander|p4:full]], the president and 70% shareholder, is described in the check register as "expense reimb." There is no expense report. Ms. Quintanilla told us [[Henrik|p4:first-name]] "said he would bring the receipts in." Unsupported. Carried to the summary of misstatements.
Check 20377 is payable to [[Lindiwe Mabuza|p7:full]], a former warehouse employee, for final pay. It has been outstanding more than 90 days. Per [[Seo|p9:surname]], [[Ms. Mabuza|p7:title-surname]] moved back to [[Durban|place:city abroad]] after [[her work visa was not renewed|attr!:immigration status described indirectly]], and the check was mailed to an old address. Recommend the client reissue it or follow the state's unclaimed property rules.
Check 20425 to [[Wendell Pike|p11:full]] is for snow-plowing and yard work. [[Pike|p11:surname!:surname that is also a common word]] is [[the president's brother-in-law|indirect!:family relationship to a named person]] and is paid by check with no invoice. Total paid to him in the year: [[$11,300|money]]. No Form 1099-NEC was issued for the prior year. Related party; see W/P R-2.
Petty cash (C-6) was counted by TNR on [[July 9, 2026|date:count date]] at the Rockland store in the presence of the store manager. Cash and receipts on hand came to [[$583.15|money]]; the shortage of [[$16.85|money]] was written off by the client and is clearly trivial. The payroll account reconciliation (C-3) had three reconciling items, all of which cleared in the first week of July, and the money market account (C-4) had none.
## 6. Cutoff and unusual items
We scanned the June and July statements for round-dollar transfers, wires, and items of [[$10,000|money]] or more.
On [[June 29, 2026|date:wire date]] a wire of [[$48,200.00|money]] left the operating account for an account at Casco Mutual ending [[-0934|acct!:last four with leading dash]]. The bank's wire detail names the beneficiary as the [[Ostrander Family Realty Trust|o8:full]], the entity that owns the Rockland store building. The client recorded it as prepaid rent. The lease calls for rent of [[$6,500|money]] a month, so the payment equals more than seven months' rent paid in advance on the last business day before year end. [[Mr. Calloway|p3:title-surname]] to discuss with Henrik. Possible distribution rather than rent.
On [[July 2, 2026|date:transfer date]] the same amount, less [[$200|money]], came back into the operating account from the unrecorded "Special" savings account. We have not yet been able to trace how the funds moved from the trust's account to that savings account.
The euro account was translated at 1.0726, which agrees to the ECB reference rate for [[30 June|date!:date without year]]. A payment of [[EUR 9,150.00|money:euro amount with currency code]] to Skerries Rope dated 30 June was recorded by OMH on [[3 July|date!:date without year]]; proposed adjustment of [[$9,814|money]] passed as trivial.
## 7. Unrecorded account -- inquiry
PD and TNR met with Ms. Quintanilla on [[August 20, 2026|date:meeting date]]. She said she had never heard of the account. [[Delphine|p5:first-name]] is [[Henrik's wife|indirect!:family relationship to a named person]]; she is not an employee or officer but has kept a company credit card (Visa ending [[2024|card!:last four digits that look like a year]]) "for years." Statements for that card go to the [[Ostranders|p4:surname!:pluralised family surname]]' home at [[61 Beauchamp Point Road|addr]], [[Rockport|place:town]], [[ME 04856|zip!:state abbreviation and ZIP written together]], not to the office.
Ms. Quintanilla also told us, with some hesitation, that she and Seo share the online banking login because the bank charges per user. The user name is [[omh_controller|cred:username]] and the token is kept in her desk. This means the person who prepares the reconciliation can also release payments. Control deficiency; to be evaluated with the other findings.
She asked that we not put in writing that [[Henrik has been in treatment for a gambling problem|health!:addiction treatment disclosed in confidence]] since the winter. We told her we could not agree to leave relevant information out of our file but that workpapers are confidential.
## 8. Conclusion and open items
Cash is fairly stated at year end EXCEPT for the matters below, which remain open and prevent sign-off of this section:
- Unrecorded savings account ([[$37,250|money]]): obtain statements from opening; determine source of the opening deposit.
- Wire of [[48.2k|money!:abbreviated amount without currency sign]] to the realty trust: obtain lease, board approval if any, and the trust's bank statement.
- Unsupported check to H. Ostrander.
- Shared banking credentials: include in the management letter.
- Consider whether these matters require communication to those charged with governance before issuance. Target issuance was [[September 30, 2026|date:target issuance date]]; that date is now at risk.
Time on this section: TNR 14.5 hours, PD 3.0 hours.
[[PD|p2:initials]] review note, [[8/24|date!:month and day only]]: Agree. Do not send any of this to the client by e-mail. [[Gus|p3:nickname]] will call Henrik himself. Our contact at the bank going forward is [[Brennan|p8:surname]] only: [[cbrennan@penobscotharbortrust.example|email]]
''',
  ok=["1.0726"]))

# ---------------------------------------------------------------- 32
DOCS.append(D(32, "html", "client statement", "accounting", "US",
  title="Client account statement from an accounting firm's billing portal",
  ents={"p1": "Georgia Papadakis-Lowe", "p2": "Nikolai Lowe", "p3": "Arjun Venkataraman",
        "o1": "Venkataraman & Holt CPAs, PLLC", "o2": "Papadakis-Lowe Family Dentistry, P.L.L.C."},
  distractors=["Form 1040", "Form 1120-S", "Form 2848", "Net 30", "Schedule E", "tax year 2025"],
  body=r'''
# [[Venkataraman & Holt CPAs, PLLC|o1:full]]
[[9800 Research Boulevard, Bldg. 2, Suite 310|addr:street with building and suite]], [[Austin|place:city]], [[TX|place:state abbreviation]] [[78759-6418|zip:ZIP+4]]
Billing questions: [[512-555-0166|phone]] or [[billing@vhcpas.example|email]]
## Statement of account
| Field | Detail |
| Client | [[PAPADAKIS-LOWE, GEORGIA|p1:last-first]] and [[LOWE, NIKOLAI|p2:last-first]] |
| Client no. | [[20418-J|rec:client number]] |
| Statement date | [[October 1, 2026|date:statement date]] |
| Billing address | [[3307 Bee Caves Trail|addr]], [[West Lake Hills|place:town]], TX [[78746|zip]] |
| Portal login | [[gpapadakislowe|cred:username]] |
| Terms | Net 30 |
## Activity
| Date | Invoice | Description | Charges | Payments |
| [[07/15/2026|date:invoice date]] | [[INV-26-3391|rec:invoice number]] | Form 1040 preparation, tax year 2025 (extended), incl. Schedule E for the [[Port Aransas|place:town]] rental | [[$1,850.00|money]] | |
| [[07/15/2026|date:invoice date]] | [[INV-26-3392|rec:invoice number]] | Form 1120-S, [[Papadakis-Lowe Family Dentistry, P.L.L.C.|o2:full]] | [[$2,400.00|money]] | |
| [[08/02/2026|date:payment date]] | | Payment -- Visa ending [[5148|card!:last four digits only]] | | [[$2,000.00|money]] |
| [[08/28/2026|date:invoice date]] | [[INV-26-3718|rec:invoice number]] | IRS notice response; Form 2848 for [[Nikolai|p2:first-name]] | [[$675.00|money]] | |
| [[09/12/2026|date:payment date]] | | Payment -- ACH from account ending [[x7702|acct!:masked account number]] | | [[$1,250.00|money]] |
| [[09/30/2026|date:late fee date]] | | Late fee on INV-26-3392 | [[$36.00|money]] | |
**Balance due: [[$1,711.00|money]]**
## Payment method on file
Visa, cardholder [[Georgia Papadakis-Lowe|p1:full:first name that is also a place]], number [[4754 4783 9339 5148|card:card number with spaces]], expires [[09/28|exp]]. Autopay is off. To pay online go to [[https://pay.vhcpas.example/c/20418-J|url:payment link containing client number]].
## Notes from your accountant
[[Georgia|p1:first-name!:first name that is also a place]] -- thank you for the September payment. Two things. First, the IRS letter for Nikolai (notice [[CP2000|rec!:notice type used as an identifier]] dated [[August 10, 2026|date:notice date]]) proposes additional tax of [[$4,318|money]] because the brokerage reported the sale of his late mother's stock without basis. We answered on [[September 4|date!:date without year]]; expect ten to twelve weeks. Second, the practice's EIN on the state franchise filing was keyed as [[74-2981135|taxid:EIN]]; the correct number is [[74-2981153|taxid:EIN]]. We have corrected it at no charge.
If the balance is a hardship while [[Nikolai is out on medical leave|health!:medical leave mentioned in passing]], call me on my direct line, [[(512) 555-0109|phone]], and we will set up a plan.
[[Arjun Venkataraman|p3:full]], CPA
[[arjun@vhcpas.example|email]]
'''))

# ---------------------------------------------------------------- 33
DOCS.append(D(33, "eml", "email thread", "accounting", "EU", enc="qp",
  title="Email thread on a cross-border invoice, VAT treatment and wire details",
  ents={"p1": "Katharina Vogelsang", "p2": "Lorcan Ó Súilleabháin", "p3": "Fabrizio Conti",
        "p4": "Mareike Jansen",
        "o1": "Vogelsang Steuerberatung GmbH", "o2": "Brightloom Textiles Ltd.",
        "o3": "Atelier Conti S.r.l.", "o4": "Rheinufer Volksbank eG"},
  distractors=["Article 196", "reverse charge", "VIES", "MwSt", "19%", "22%"],
  headers={
    "From": "[[Katharina Vogelsang|p1:full]] <[[k.vogelsang@vogelsang-stb.example|email]]>",
    "To": "[[Lorcan O Suilleabhain|p2:full!:name with diacritics dropped]] <[[lorcan@brightloom.example|email]]>",
    "Cc": "[[m.jansen@vogelsang-stb.example|email]]",
    "Subject": "AW: Invoice 2026-0417 / VAT and bank details -- PLEASE READ before paying",
    "Date": "Wed, [[23 Sep 2026|date:email date]] 08:51:33 +0200"},
  body=r'''Dear Lorcan,

Short answers first, details below.

1. Do NOT pay to the account in the PDF you received on Monday. That PDF did not come from us. Our bank details have not changed since 2019:

   Account holder: [[Vogelsang Steuerberatung GmbH|o1:full]]
   Bank: [[Rheinufer Volksbank eG|o4:full]], [[Köln|place!:city in native spelling]]
   IBAN: [[DE65 0954 8966 5692 8370 88|iban:IBAN in groups of four]]
   BIC: [[GENODED1RVK|acct:SWIFT code]]

   The PDF shows an IBAN beginning NL75 -- that is not ours. [[Mareike|p4:first-name]] has reported it to the police here (reference [[K-2026/331-4478|rec:police reference number]]). Please check whether anyone at Brightloom opened the attachment, and tell your IT people that the message came from IP [[203.0.113.189|ip:IPv4]] according to the header.

2. VAT. Our invoice [[2026-0417|rec:invoice number]] for [[€3.850,00|money!:euro amount in continental format]] is correctly issued WITHOUT German MwSt. You are a business customer in Ireland with a valid VAT number ([[IE3491226TH|taxid:VAT number]], I checked it in VIES this morning), so the reverse charge under Article 196 applies and you account for Irish VAT yourself. Our number, for your records: [[DE318847209|taxid:VAT number]].

3. The Italian supplier. [[Atelier Conti S.r.l.|o3:full]] charged you 22% Italian VAT on the sample fabrics ([[EUR 1.240,00|money!:euro amount in continental format]] net). If the goods left Italy and you can prove transport to [[Kilkenny|place:city]], that is wrong and [[Signor Conti|p3:title-surname]] should issue a credit note. If you collected the goods yourself at the fair in [[Milano|place!:city in native spelling]], it is correct. Which was it?

Kind regards
[[Katharina|p1:first-name]]

Katharina Vogelsang, Steuerberaterin
Vogelsang Steuerberatung GmbH | [[Agrippinaufer 41|addr:German street address]] | [[50678|zip:German postal code]] Köln
Tel. [[+49 221 5550 142|phone:German number with country code]] | Fax [[+49 221 5550 143|phone:fax number]]
Assistant: [[Mareike Jansen|p4:full]]

> -----Original message-----
> From: [[Lorcan Ó Súilleabháin|p2:full!:name with diacritics]]
> Sent: Tuesday, [[22 September 2026|date:day month year]] 17:14
> To: Katharina Vogelsang
> Subject: Invoice 2026-0417 / VAT and bank details
>
> Hi Katharina,
>
> Two things on your invoice for the German payroll registration.
>
> (a) Our bookkeeper says there should be 19% VAT on it and that without it Revenue
> will query the deduction. Is she right? [[Brightloom Textiles Ltd.|o2:full]] is registered here,
> company no. [[648213|rec!:company registration number, unlabelled digits]], if that matters.
>
> (b) We got an email yesterday saying you'd moved banks, with a new IBAN
> ([[NL75 INGB 7240 6681 39|iban:IBAN in groups of four]]). I was about to send the [[3,850 euro|money!:amount with currency in words]] from our
> account ([[IE89AIBK69733626420599|iban!:IBAN without spaces]]) but it looked off -- the sender was
> [[k.vogelsang@vogelsang-stb.example.net|email!:spoofed look-alike sender address]], not your usual address. Can you confirm?
>
> Also, [[Fabrizio|p3:first-name]] from [[Atelier Conti|o3:short]] is chasing me for [[€1.512,80|money!:euro amount in continental format]]. I'd rather not pay
> Italian VAT if I don't have to. I'm in [[Lyon|place:city]] at a fair until Friday -- mobile
> [[+353 85 555 0147|phone:Irish mobile with country code]] is best.
>
> Thanks,
> [[Lorcan|p2:first-name]]
> Finance Director, [[Brightloom|o2:short]]
''',
  ok=["NL75"]))

# ---------------------------------------------------------------- 34
DOCS.append(D(34, "txt", "bookkeeper note", "accounting", "CA", length="short",
  title="Bookkeeper's handover note left for a colleague",
  ents={"p1": "Francine Beaulieu-Roy", "p2": "Dmitri Sokolov", "o1": "Sokolov Auto Glass Inc."},
  distractors=["GST34", "Q3"],
  body=r'''[[francine|p1:first-name!:first name in lower case]] -- before you file the Q3 GST34 for [[sokolov auto glass|o1:short!:company name in lower case]]:
- BN is [[84417 2290 RT0001|taxid:Canadian business number]], CRA My Business login [[dsokolov_bn|cred:username]] / [[Windshield#88|cred:password]]
- [[dmitri|p2:first-name!:first name in lower case]] paid the [[$4,212.60|money]] instalment [[Oct 6|date!:abbreviated date without year]] on his own Visa
  [[4671 8642 8966 2024|card:card number with spaces]] exp [[03/28|exp]] cvv [[517|cvv]] (he read it to me, pls shred this)
- his SIN for the T4: [[214-930-521|taxid:SIN with dashes]]
call him [[(204) 555-0158|phone]] if short, he's in [[Brandon|place!:city name that is also a first name]] til fri
'''))

# ---------------------------------------------------------------- 35
DOCS.append(D(35, "rtf", "engagement letter", "accounting", "US",
  title="Tax preparation engagement letter for a married couple",
  ents={"p1": "Cordelia Featherstonehaugh", "p2": "Tevita Fonoti", "p3": "Mele Fonoti-Greer",
        "p4": "Sione Fonoti",
        "o1": "Featherstonehaugh Tax & Advisory, Inc.", "o2": "Fonoti Landscape & Stone, LLC",
        "o3": "Wasatch Peaks Credit Union"},
  distractors=["26 U.S.C. § 7216", "Circular 230", "Form 8879", "Form 1040", "Schedule C", "Form 8332", "April 15"],
  body=r'''
# [[Featherstonehaugh Tax & Advisory, Inc.|o1:full]]
[[2150 South 1300 East, Suite 500|addr:grid-style street address with suite]], [[Salt Lake City|place:city]], [[Utah|place:state]] [[84106|zip]]
Tel. [[801.555.0131|phone:dotted]]    Fax [[801.555.0132|phone:fax number]]    [[www.featherstonehaugh-tax.example|url]]
[[January 12, 2026|date:letter date]]
[[Tevita Fonoti|p2:full]] and [[Mele Fonoti-Greer|p3:full]]
[[874 West Pacific Avenue|addr]]
[[Taylorsville|place:city]], [[UT|place:state abbreviation]] [[84123|zip]]
**Re: 2025 individual income tax return -- client file [[FTA-11872|rec:client file number]]**
Dear [[Mr. Fonoti|p2:title-surname]] and [[Ms. Fonoti-Greer|p3:title-surname]]:
Thank you for choosing us again. This letter confirms what we will and will not do for you this year. Please read it, sign the last page, and return it with your organizer.
## What we will do
We will prepare your 2025 federal Form 1040 and your Utah resident return from the information you give us, including Schedule C for [[Fonoti Landscape & Stone, LLC|o2:full]] (EIN [[87-3340918|taxid:EIN]]). We will not audit or verify your records. We may ask you to explain items that look incomplete or inconsistent.
You told us that [[Mele|p3:first-name]]'s son from her first marriage, [[Sione|p4:first-name]] (born [[August 3, 2011|dob]]), lived with you all year and that his father has agreed in writing not to claim him. Please send us the signed Form 8332. Without it we cannot claim the child tax credit for him.
## Your responsibilities
You are responsible for the completeness and accuracy of what you give us, and for keeping the records that support it. The return is yours; review it before you sign Form 8879. Returns are due April 15. If we do not have all of your documents by [[March 13, 2026|date:document deadline]] we will file an extension, which extends the time to file but not the time to pay.
## Identity and bank details we have on file
So that you can check them, here is what we carried forward from last year. Tell us at once if anything is wrong.
| Item | [[Tevita|p2:first-name]] | Mele |
| SSN / ITIN | [[XXX-XX-7907|ssn!:masked SSN]] | [[9XX-7X-4410|taxid!:masked ITIN]] |
| Date of birth | [[02/19/1980|dob]] | [[11/30/1983|dob]] |
| Occupation | Landscape contractor | Dental hygienist |
| Mobile | [[801-555-0175|phone]] | [[801-555-0199|phone]] |
Refund or payment account: [[Wasatch Peaks Credit Union|o3:full]], routing [[034481750|rtn]], checking [[0091 7745 30|acct!:account number with spaces]]. Identity Protection PIN issued to Tevita by the IRS for this season: [[604417|cred:IRS identity protection PIN]].
Mele has told us that her ITIN is being replaced by a Social Security number now that [[her adjustment of status was approved|attr!:immigration status described indirectly]]. Bring the new card when you have it; we will need to notify the IRS so that her earlier returns are linked.
## Fees
Our fee for the returns described above is [[$1,150|money]], plus [[$225|money]] if we prepare the city business license renewal. Last year's balance of [[$310.00|money]] remains unpaid and is due before we begin. Work outside this letter, such as answering a notice, is billed at [[$190|money]] an hour.
## Privacy
Under 26 U.S.C. § 7216 and Circular 230 we may not disclose your tax return information to anyone outside this firm, or use it for anything other than preparing your return, without your written consent. We use an encrypted portal, not e-mail, for documents: [[https://portal.featherstonehaugh-tax.example/fonoti|url:client portal link containing surname]]
If this letter matches your understanding, please sign below.
Sincerely,
[[Cordelia Featherstonehaugh|p1:full]], EA
Enrolled agent no. [[00118264-EA|govid:enrolled agent number]]
[[cordelia@featherstonehaugh-tax.example|email]]
Accepted: ______________________ ([[T. Fonoti|p2:short:initial + surname]])     ______________________ ([[M. Fonoti-Greer|p3:short:initial + surname]])     Date: __________
'''))
# ---------------------------------------------------------------- 36
DOCS.append(D(36, "txt", "discharge summary", "health", "US",
  title="Hospital discharge summary - heart failure admission",
  ents={"p1": "Harold T. Abernathy-Nakamura", "p2": "Folasade Adeyinka", "p3": "Leonard Brzezinski",
        "p4": "Karen Nakamura-Ellis", "p5": "Ignacio Villalobos",
        "o1": "St. Brendan's Regional Medical Center", "o2": "Cornerstone Senior Health Plan",
        "o3": "Harborlight Home Health, Inc.", "o4": "Coos Bay Heart & Vascular Associates"},
  distractors=["NYHA class III", "2 g sodium", "IV furosemide", "Medicare", "BMP", "1.5 L"],
  body=r'''[[ST. BRENDAN'S REGIONAL MEDICAL CENTER|o1:caps]]                       DISCHARGE SUMMARY
[[1775 Thompson Road|addr]], [[Coos Bay|place:city]], [[Oregon|place:state]] [[97420|zip]]

PATIENT:   [[ABERNATHY-NAKAMURA, HAROLD T.|p1:last-first:Last, First in caps]]       MRN: [[00-447-1182|rec:medical record number]]
DOB:       [[02/11/1933|dob]]  ([[93 y/o|age!:abbreviated age]] M)             ACCT: [[V0093317745|rec:hospital account number]]
ADMITTED:  [[10/02/2026|date:admission date]]                        DISCHARGED: [[10/07/2026|date:discharge date]]
ATTENDING: [[Folasade Adeyinka|p2:full]], MD (NPI [[1669704218|govid:NPI]])
PCP:       [[Dr. Leonard Brzezinski|p3:full:full name with title]]
COVERAGE:  Medicare [[4RK8-TN2-MH61|rec:Medicare beneficiary identifier]]; [[Cornerstone Senior Health Plan|o2:full]], member [[CSH 88104471 02|rec!:member ID with spaces]]

PRINCIPAL DIAGNOSIS: [[Acute on chronic systolic heart failure|health:diagnosis]], NYHA class III
SECONDARY: [[permanent atrial fibrillation|health:diagnosis]]; [[CKD stage 3b|health:diagnosis]]; [[type 2 diabetes|health:diagnosis]]; [[mild cognitive impairment|health:diagnosis]]
ALLERGIES: [[sulfa (rash)|health:allergy]]
CODE STATUS: [[DNR/DNI|health!:code status abbreviation]], confirmed with patient and daughter [[10/03|date!:month and day only]]

HOSPITAL COURSE
[[Mr. Abernathy-Nakamura|p1:title-surname]] is a [[retired tugboat captain|indirect!:distinctive former occupation]] who lives with his daughter. He came to the
ED with three days of worsening shortness of breath and [[a 9 lb weight gain|health:clinical finding]] after running
out of his diuretic. [[BNP 1,840|health:lab result]], [[creatinine 1.9|health:lab result]] (baseline 1.6). Echo on [[10/03/2026|date:procedure date]] showed
[[EF 30%|health:test result]], unchanged. He was diuresed with IV furosemide, net negative 5.2 L, and
returned to room air by day 4. Device interrogation of his dual-chamber pacemaker
(serial [[PJN448213H|dev:implanted device serial number]]) by [[Dr. Villalobos|p5:title-surname]] showed normal function, battery 4.1 years.
One episode of [[evening confusion|health:symptom]] on night 2 resolved without medication.

DISCHARGE MEDICATIONS
  [[furosemide 40 mg daily|health:medication and dose]] (was 20 mg)        [[metoprolol succinate 50 mg daily|health:medication and dose]]
  [[apixaban 2.5 mg BID|health:medication and dose]]                   [[insulin glargine 12 units nightly|health:medication and dose]]
  STOP: ibuprofen. No NSAIDs.

DISPOSITION: Home with [[Harborlight Home Health, Inc.|o3:full]] (RN visits 3x/week, daily weights).
Diet 2 g sodium, fluids 1.5 L. Daughter and health care agent: [[Karen Nakamura-Ellis|p4:full]],
[[541-555-0137|phone]], same address: [[63310 Shinglehouse Slough Road|addr:rural road address]], Coos Bay [[97420-8811|zip:ZIP+4]].
[[Karen|p4:first-name]] manages his pill box; [[harold|p1:first-name!:first name in lower case]] "forgets the evening ones" per her.

FOLLOW-UP
  Cardiology: [[Ignacio Villalobos|p5:full]], MD, [[Coos Bay Heart & Vascular Associates|o4:full]], [[Oct. 15, 2026|date:follow-up appointment]] 9:40 am
  PCP: [[Dr. Brzezinski|p3:title-surname]] within 7 days; BMP at that visit.

Dictated: [[F. Adeyinka|p2:short:initial + surname]] MD  10/07/2026 14:12      Transcription job [[#7781205|rec!:transcription job number]]
'''))

# ---------------------------------------------------------------- 37
DOCS.append(D(37, "pdf", "insurance claim form", "health", "US",
  title="Health insurance claim form (professional services) after an auto accident",
  ents={"p1": "Leslie K. Drummond-Achterhof", "p2": "Marcus D. Achterhof", "p3": "Soledad Ibanez-Roth",
        "p4": "Tyrone Washington-Bell",
        "o1": "Stones River Spine & Rehabilitation, PLLC", "o2": "Volunteer State Employees Health Plan",
        "o3": "Rutherford Logistics Corp.", "o4": "Cumberland Plateau Auto Insurance Co."},
  distractors=["CMS-1500", "CPT 99204", "CPT 97110", "CPT 72148", "ICD-10", "PLACE OF SERVICE 11", "BOX 24"],
  body=r'''
# HEALTH INSURANCE CLAIM FORM
Approved form CMS-1500 (02-12), professional services
## CARRIER
[[VOLUNTEER STATE EMPLOYEES HEALTH PLAN|o2:caps]]
[[PO BOX 440918|addr!:PO Box in ALL CAPS]]
[[NASHVILLE|place!:city in ALL CAPS]] [[TN|place:state abbreviation]] [[37244-0918|zip:ZIP+4]]
## PATIENT AND INSURED
1a. INSURED'S I.D. NUMBER: [[VSE 904471826 01|rec!:member ID with spaces]]
2. PATIENT'S NAME: [[DRUMMOND-ACHTERHOF, LESLIE K|p1:last-first:Last, First in caps]]
3. PATIENT'S BIRTH DATE: [[03 22 1969|dob!:birth date with spaces as separators]] SEX: F
4. INSURED'S NAME: [[ACHTERHOF, MARCUS D|p2:last-first:Last, First in caps]]
5. PATIENT'S ADDRESS: [[2218 SULPHUR SPRINGS RD|addr!:street address in ALL CAPS]]
CITY: [[MURFREESBORO|place!:city in ALL CAPS]] STATE: TN ZIP: [[37129|zip]]
TELEPHONE: [[(615) 555 0127|phone!:no dash between exchange and line]]
6. PATIENT RELATIONSHIP TO INSURED: [[SPOUSE|indirect!:relationship to the insured]]
7. INSURED'S ADDRESS: SAME
8. INSURED'S DATE OF BIRTH: [[11 05 1966|dob!:birth date with spaces as separators]] SEX: M
9. INSURED'S SSN: [[301417907|ssn!:SSN without dashes]]
11. INSURED'S POLICY GROUP NUMBER: [[GRP-0077214|rec:group number]]
11b. EMPLOYER: [[RUTHERFORD LOGISTICS CORP.|o3:caps]]
## CONDITION
10b. AUTO ACCIDENT? YES. PLACE (STATE): TN
14. DATE OF CURRENT INJURY: [[08 29 2026|date!:date with spaces as separators]]
10d. OTHER CLAIM: [[CUMBERLAND PLATEAU AUTO INSURANCE CO.|o4:caps]]
AUTO CLAIM NO. [[CPA-26-TN-0418837|rec:auto insurance claim number]]
AUTO POLICY NO. [[TNA 7720 4415 9|rec!:policy number with spaces]]
16. UNABLE TO WORK FROM [[08 29 2026|date]] TO [[09 28 2026|date!:date with spaces as separators]]
17. REFERRING PROVIDER: [[TYRONE WASHINGTON-BELL MD|p4:caps]]
17b. NPI: [[1528390476|govid:NPI]]
## DIAGNOSES (ICD-10)
A. [[S13.4XXA SPRAIN OF LIGAMENTS OF CERVICAL SPINE|health:diagnosis code and description]]
B. [[M54.16 RADICULOPATHY, LUMBAR REGION|health:diagnosis code and description]]
C. [[F43.10 POST-TRAUMATIC STRESS DISORDER|health:mental health diagnosis code and description]]
## SERVICES (BOX 24)
| DATE | CPT | DX | CHARGE |
| [[09 03 2026|date!:date with spaces as separators]] | 99204 | AB | [[385 00|money!:amount with a space instead of a decimal point]] |
| [[09 10 2026|date!:date with spaces as separators]] | 72148 | B | [[1,460 00|money!:amount with a space instead of a decimal point]] |
| [[09 17 2026|date!:date with spaces as separators]] | 97110 | AB | [[148 00|money!:amount with a space instead of a decimal point]] |
| [[09 24 2026|date!:date with spaces as separators]] | 97110 | AB | 148 00 |
PLACE OF SERVICE 11 for all lines. CPT 99204, CPT 72148, CPT 97110.
28. TOTAL CHARGE: [[$2,141.00|money]]
29. AMOUNT PAID: [[$40.00|money]]
30. BALANCE: [[$2,101.00|money]]
## PROVIDER
25. FEDERAL TAX I.D. NUMBER: [[62-1904483|taxid:EIN]] (EIN)
26. PATIENT'S ACCOUNT NO.: [[SRS-0031947|rec:patient account number]]
31. SIGNATURE OF PHYSICIAN: [[SOLEDAD IBANEZ-ROTH DO|p3:caps]]
DATE SIGNED: [[10 01 2026|date!:date with spaces as separators]]
33. BILLING PROVIDER: [[STONES RIVER SPINE & REHABILITATION, PLLC|o1:caps]]
[[745 MEDICAL CENTER PKWY STE 204|addr!:street address in ALL CAPS with suite]]
MURFREESBORO TN [[37129-2260|zip:ZIP+4]]
PHONE: [[615-555-0181|phone]]
33a. NPI: [[1841205597|govid:NPI]]
## OFFICE NOTE (not transmitted)
Pt asked that statements NOT go to the house; she and [[Marcus|p2:first-name]] are [[separating|indirect!:marital status change]]. Use her cell above and [[leslie.da@postbox.example|email]] only. Auto adjuster wants records for C; do not release the counseling notes without a specific authorization.
'''))

# ---------------------------------------------------------------- 38
DOCS.append(D(38, "txt", "psychotherapy progress note", "health", "CA",
  title="Psychotherapy progress note - individual session",
  ents={"p1": "Ravinder Bhullar", "p2": "Catriona MacAskill", "p3": "Devon Fairweather",
        "p4": "Harpreet Bhullar",
        "o1": "Grand River Counselling Collective", "o2": "Laurentide Benefit Assurance",
        "o3": "Conestoga Precision Tooling"},
  distractors=["PHQ-9", "GAD-7", "CBT", "DSM-5", "EAP", "Session 7"],
  body=r'''[[Grand River Counselling Collective|o1:full]]
[[22 Frederick Street, Suite 6|addr:street with suite]], [[Kitchener|place:city]] [[ON|place:province abbreviation]]  [[N2H 6M6|zip:Canadian postal code]]

PROGRESS NOTE -- INDIVIDUAL PSYCHOTHERAPY                      Session 7 of 12 (EAP)

Client:      [[Ravinder Bhullar|p1:full]] ("[[Ravi|p1:nickname]]")         Chart: [[GRC-2026-0412|rec:chart number]]
DOB:         [[1994-04-18|dob:ISO date]]                       Health card: [[4532 281 947 KM|govid:provincial health card number]]
Date:        [[Tuesday, 6 October 2026|date:session date with weekday]], 5:00-5:50 pm, in person
Therapist:   [[Catriona MacAskill|p2:full]], RP (CRPO # [[009417|govid:professional registration number]])
Funder:      [[Laurentide Benefit Assurance|o2:full]], EAP file [[LBA-EAP-771820|rec:benefit file number]]; fee [[$165.00|money]] billed direct

PRESENTATION
[[R.B.|p1:initials]] arrived on time, tired, tearful once. PHQ-9 = 14 (was 17 at intake), GAD-7 = 11.
Sleep 5 hrs. Reports [[two panic attacks at work|health:mental health symptom]] since last session, both on the shop floor
at [[Conestoga Precision Tooling|o3:full]], where he is [[the only apprentice on the night shift|indirect!:unique role at a named employer]].

RISK
[[Passive suicidal ideation|health:suicide risk]] ("wouldn't mind not waking up") twice this week, no plan, no
intent, no access to means. Safety plan reviewed. Protective: partner, [[his sister Harpreet|indirect!:family relationship to a named person]].

CONTENT
- [[Came out to his parents as gay|attr:sexual orientation]] on Thanksgiving weekend. Father has not spoken to him
  since. Family is [[observant Sikh|attr:religion]]; [[Ravi|p1:nickname]] says the gurdwara community "will know by now".
- Partner [[Devon Fairweather|p3:full]] wants him to move in. R.B. fears this "makes it final" with his family.
  [[Devon|p3:first-name]] has offered to attend a session.
- [[Cannabis nightly|health:substance use]] to sleep, up from weekends only. Drinking unchanged (2-3/week).
- Started [[sertraline 50 mg|health:medication and dose]] via family doctor on [[Sept 21|date!:abbreviated date without year]]; nausea settling.
- Worried the plant will find out: his supervisor signs the EAP attendance slips. Explained
  that the slip shows dates only.

INTERVENTION: CBT thought record on "I have destroyed my family"; grounding for panic;
behavioural activation (gym 2x). Psychoeducation re cannabis and sleep.

ASSESSMENT: [[Major depressive episode, moderate|health:mental health diagnosis]] (DSM-5), with panic attacks. Improving
slowly; acute stressor.

PLAN
1. Next session [[13 Oct|date!:abbreviated date without year]], 5 pm. Ask funder for 6 more sessions.
2. With consent, short letter to family doctor re SI and medication.
3. Emergency contact on file: [[Harpreet Bhullar|p4:full]], [[519-555-0114|phone]]. Client's cell [[226 555 0172|phone!:spaces only]];
   OK to leave voicemail, NOT ok to email his work address. Personal: [[rav.b94@inbox.example|email]].

Signed electronically: [[C. MacAskill|p2:short:initial + surname]], RP    2026-10-06 18:22
''',
  ok=["2026-10-06 18:22"]))

# ---------------------------------------------------------------- 39
DOCS.append(D(39, "html", "lab results report", "health", "US",
  title="Clinical laboratory results report",
  ents={"p1": "Philippa Oyelowo-Grant", "p2": "Hyun-woo Lim", "p3": "Esperanza Maldonado",
        "o1": "Tri-County Reference Laboratories, LLC", "o2": "Magnolia Court Assisted Living",
        "o3": "Pecan Grove Internal Medicine"},
  distractors=["CLIA", "g/dL", "mIU/L", "eGFR", "Reference range", "13.5-17.5", "CBC"],
  body=r'''
# [[Tri-County Reference Laboratories, LLC|o1:full]]
[[4400 Industrial Loop East|addr]], [[Valdosta|place:city]], [[GA|place:state abbreviation]] [[31601|zip]] | CLIA no. [[11D2094417|rec:laboratory certification number]] | Client services [[1-800-555-0143|phone:toll-free]]
## Final report
| Field | Value |
| Patient | [[OYELOWO-GRANT, PHILIPPA M|p1:last-first:Last, First in caps]] |
| DOB / Age / Sex | [[07/04/1930|dob]] / [[96 Y|age!:abbreviated age]] / F |
| Patient ID | [[MC-00388|rec:facility resident number]] |
| Accession | [[T26-1004-07731|rec:lab accession number]] |
| Collected | [[10/04/2026|date:collection date]] 06:40 |
| Reported | [[10/05/2026|date:report date]] 14:05 |
| Ordering provider | [[Hyun-woo Lim|p2:full]], MD, NPI [[1356448820|govid:NPI]] |
| Practice | [[Pecan Grove Internal Medicine|o3:full]] |
| Collection site | [[Magnolia Court Assisted Living|o2:full]], [[Room 214B|place!:room number in a named facility]] |
| Collected by | [[E. Maldonado|p3:short:initial + surname]], phlebotomist ID [[PBT-5521|rec:staff ID]] |
## Results
| Test | Result | Flag | Reference range |
| Hemoglobin (CBC) | [[9.8 g/dL|health:lab value in a table cell]] | L | 12.0-15.5 |
| Ferritin | [[8 ng/mL|health:lab value in a table cell]] | L | 15-150 |
| Creatinine | [[1.6 mg/dL|health:lab value in a table cell]] | H | 0.6-1.1 |
| eGFR | [[31|health!:bare lab value in a table cell]] | L | 60 or more |
| TSH | [[11.2 mIU/L|health:lab value in a table cell]] | H | 0.4-4.5 |
| Hemoglobin A1c | [[7.9 %|health:lab value in a table cell]] | H | under 5.7 |
| Hepatitis C antibody | [[REACTIVE|health!:infectious disease result as a single word]] | A | Non-reactive |
| Digoxin level | [[2.6 ng/mL|health:drug level]] | CRITICAL | 0.5-2.0 |
## Comments
Findings are [[consistent with iron deficiency anemia|health:interpretive diagnosis]]. Reactive hepatitis C antibody: confirmatory RNA testing has been added to this accession. The men's hemoglobin range (13.5-17.5) does not apply.
CRITICAL VALUE called to and read back by [[Esperanza Maldonado|p3:full]] at the facility on 10/05/2026 at 14:11, and to [[Dr. Lim|p2:title-surname]]'s after-hours line, [[229.555.0168|phone:dotted]], at 14:20.
## Delivery
Faxed to Pecan Grove Internal Medicine at [[(229) 555-0169|phone:fax number]]. Posted to the provider portal: [[https://results.tricountylabs.example/r/T26-1004-07731|url:results link containing accession number]]
Bill to: Medicare [[7TY2-PD9-XK48|rec:Medicare beneficiary identifier]]. Responsible party: [[her grandson, the facility's listed contact|indirect!:family relationship and role]], [[229-555-0105|phone]].
''',
  ok=["12.0-15.5", "10/05/2026 at 14:11"]))

# ---------------------------------------------------------------- 40
DOCS.append(D(40, "pptx", "board presentation", "general", "US",
  title="Quarterly board of directors presentation",
  ents={"p1": "Rosemary Achterberg-Diaz", "p2": "Clifton Mbatha", "p3": "Yusuf Demirci",
        "p4": "Hunter Lindqvist", "p5": "Noor Al-Rashid",
        "o1": "Larkfield Home Services, Inc.", "o2": "Summit Ridge Property Management LLC",
        "o3": "Great Plains Agricultural Bank", "o4": "Brightway Senior Living Group",
        "o5": "Dunmore & Kessler LLP"},
  distractors=["Q3 2026", "EBITDA", "Rule 10b5-1", "SOC 2", "12 percent", "14%"],
  body=r'''
# [[Larkfield Home Services, Inc.|o1:full]] -- Board of Directors, Q3 2026
Prepared by [[Rosemary Achterberg-Diaz|p1:full]], CEO
[[October 20, 2026|date:meeting date]] | [[Omaha|place:city]], [[Nebraska|place:state]]
CONFIDENTIAL -- board members and counsel only
# Financial highlights
- Revenue [[$4.2M|money!:abbreviated amount in millions]], up 14% on last year
- EBITDA [[$310K|money!:abbreviated amount]]; cash at quarter end [[$1,180,400|money]]
- Credit line with [[Great Plains Agricultural Bank|o3:full]], loan no. [[GPA-CL-0044812|rec:loan number]]: [[$600,000|money]] drawn of [[$1.5 million|money:amount in millions]]
- Covenant test passed; next test [[12/31/2026|date:covenant test date]]
# Top customers
| Customer | Q3 revenue | Renewal |
| [[Summit Ridge Property Management LLC|o2:full]] | [[$1,020,000|money]] | [[3/1/2027|date:renewal date]] |
| [[Brightway Senior Living Group|o4:full]] | [[$655,500|money]] | at risk |
| All others | [[$2,524,500|money]] | |
- [[Brightway|o4:short]] has asked for a 12 percent price cut; decision needed today
# People
- CFO [[Clifton Mbatha|p2:full]] will step down [[November 30|date!:date without year]] [[for cancer treatment|health:reason for resignation]]; not yet announced
- Interim CFO: [[Yusuf Demirci|p3:full]], controller; offer at [[$185,000|money]] base
- [[Cliff|p2:nickname]] keeps his options under the Rule 10b5-1 plan
# Litigation
- [[Lindqvist|p4:surname]] v. [[Larkfield|o1:short]], No. [[CI 26-4471|rec:state court case number]], [[Douglas County|place:county]] District Court
- Former technician [[Hunter Lindqvist|p4:full:first name that is also a common word]] alleges he was fired [[after reporting a workplace injury|indirect!:event that identifies the plaintiff]]
- Counsel ([[Dunmore & Kessler LLP|o5:full]]) recommends settling at up to [[$90,000|money]]; insurer reserve [[$75K|money!:abbreviated amount]]
# Security incident
- [[September 9|date!:date without year]]: laptop stolen from a van, serial [[5CG1337KQZ|dev:laptop serial number]]; disk encrypted
- [[September 11|date!:date without year]]: logins to payroll from [[198.51.100.36|ip:IPv4]] using the account [[nalrashid|cred:username]]
- [[Noor Al-Rashid|p5:full]] (IT lead) reset all passwords; 412 employee records may have been viewed
- SOC 2 audit moved to next year
# Decisions requested
- Approve Brightway pricing response
- Approve settlement authority in the [[Lindqvist|p4:surname]] matter
- Approve interim CFO appointment and retention bonus of [[$40,000|money]] for [[Mr. Demirci|p3:title-surname]]
'''))
