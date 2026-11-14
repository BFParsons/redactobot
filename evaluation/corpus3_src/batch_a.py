from corpus3_src.core import D, dt, amt, num

DOCS = []

# ---------------------------------------------------------------- 301
DOCS.append(D(301, "txt", "deposition transcript excerpt", "legal", "US", length="long",
  title="Deposition of the plaintiff in a premises liability case (excerpt)",
  ents={"p1": "Leocadia Maria Wawrzyniak", "p2": "Rashida N. Holcombe", "p3": "Garrett T. Ulbricht",
        "p4": "Zbigniew Wawrzyniak", "p5": "Paulette Dzialo", "p6": "Ignacio Barrientos", "p7": "Dr. Sunita Kelkar",
        "p8": "Marisol Tsinajinnie",
        "o1": "Greenmantle Grocers, Inc.", "o2": "Holcombe & Ilves, PLLC", "o3": "Dunmow Pryce LLP",
        "o4": "Tortolita Family Dental", "o5": "Rincon Vista Medical Center"},
  distractors=["JOHN DOES 1-5", "Rule 30(e)", "Exhibit 4", "Exhibit 7", "Chapter 13"],
  body=r'''
IN THE SUPERIOR COURT OF THE STATE OF ARIZONA
IN AND FOR THE COUNTY OF [[PIMA|place:county in caps]]

[[LEOCADIA M. WAWRZYNIAK|p1:caps:name in caption]], a married woman,
            Plaintiff,
vs.                                             No. [[C20254417|rec:case number]]
[[GREENMANTLE GROCERS, INC.|o1:caps:name in caption]], an Arizona corporation; JOHN DOES 1-5,
            Defendants.

DEPOSITION OF [[LEOCADIA WAWRZYNIAK|p1:caps]]
[[Tucson|place:city]], [[Arizona|place:state]]
[[October 9, 2025|date:deposition date]], 9:32 a.m.

APPEARANCES
For the Plaintiff:   [[Rashida N. Holcombe|p2:full]], Esq., [[Holcombe & Ilves, PLLC|o2:full]]
                     [[2210 E. Speedway Blvd., Suite 140|addr:street with suite]], Tucson, [[AZ|place:state abbreviation]] [[85719|zip]]
                     [[rholcombe@holcombeilves.example|email]]
For the Defendant:   [[Garrett T. Ulbricht|p3:full]], Esq., [[Dunmow Pryce LLP|o3:full]]
                     [[One South Church Avenue, 18th Floor|addr:address with floor, number in words]], Tucson, AZ [[85701|zip]]
Also present:        [[Zbigniew Wawrzyniak|p4:full]]
Reported by:         [[Paulette Dzialo|p5:full]], RPR, Certified Reporter No. [[50844|govid:court reporter certificate number]]

                                                                 Page 6
EXAMINATION BY [[MR. ULBRICHT|p3:caps:title + surname in caps]]:
 Q.  Good morning, ma'am. Would you state your full name for the record?
 A.  [[Leocadia Maria Wawrzyniak|p1:full]]. Everybody calls me [[Lottie|p1:nickname]].
 Q.  Have you ever gone by any other name?
 A.  My maiden name was [[Stachura|p1:surname:maiden name]].
 Q.  And your date of birth?
 A.  [[March 3rd, 1958|dob:month, ordinal day, year]].
 Q.  Where do you live currently?
 A.  [[3391 North Calle Zaragoza|addr]], here in Tucson. We've been there since about two thousand eleven.
 Q.  Who lives there with you?
 A.  Just my husband, [[Ziggy|p4:nickname]]. [[Zbigniew|p4:first-name]]. He's sitting right there.
 Q.  I don't want your whole Social Security number on the record, just the last four digits.
     [[MS. HOLCOMBE|p2:caps:title + surname in caps]]:  Last four only, [[Lottie|p1:nickname]].
 A.  [[4570|ssn:last four digits only]].
 Q.  Is there a phone number where you can be reached if we need to reschedule anything?
 A.  My cell is [[five two zero, five five five, zero one four seven|phone:spoken digit by digit]]. Or email, it's [[lottie.w58@sonoramail.example|email]].

                                                                 Page 9
 Q.  Where were you working in the spring of this year?
 A.  I worked the front desk at [[Tortolita Family Dental|o4:full]]. I'd been there six years.
 Q.  What were you earning?
 A.  [[Nineteen dollars an hour|money:hourly rate in words]], thirty-two hours a week most weeks.
 Q.  Let's talk about the day of the incident. What day was it?
 A.  It was the Saturday before Easter. [[April 19th|date:month and ordinal day]].
 Q.  And which store were you in?
 A.  The [[Greenmantle|o1:short]] on [[Oracle Road|addr!:street name only, no number]], the one by the car wash. I shop there every week.
 Q.  What time did you arrive?
 A.  A little after ten in the morning. I remember because I had just dropped Ziggy at the union hall.
 Q.  Which union hall is that?
 A.  He's [[with the Sheet Metal Workers, Local 359|attr:union membership of the husband]]. Our health insurance comes through them.
 Q.  Tell me what happened once you were inside.
 A.  I got a cart, I went to produce first like I always do. I wanted grapes. There is a display on the end, and when
     I came around it my right foot just went out from under me. I went down on my left side, hard.
 Q.  Did you see anything on the floor before you fell?
 A.  No. After, when I was lying there, I could see water and some crushed grapes, and a long skid mark from my shoe.
 Q.  Was there a cone or a wet floor sign anywhere in that aisle?
 A.  Not that I saw. Not until afterwards, when a boy in an apron brought one over.
 Q.  What kind of shoes were you wearing?
 A.  Sneakers. The white ones I wear to work. They were maybe three months old.
 Q.  Did anyone come to help you?
 A.  A young woman with a toddler in her cart. She stayed with me the whole time and she called 911. She told me her name
     was [[Marisol Tsinajinnie|p8:full]]. She said she [[works at the university bookstore|indirect:workplace of a witness]]. I wrote her number on my hand.
 Q.  Did you speak with anyone from the store?
 A.  The manager came. [[Nacho|p6:nickname]]. I think his real name is [[Ignacio|p6:first-name]]. [[Barrientos|p6:surname]].
 Q.  What did [[Mr. Barrientos|p6:title-surname]] say to you?
 A.  He said, "I told them twice already this morning to mop that up." Those were his words. Then he asked me to sign
     a paper, and I said I can't sign anything, look at my hand.
 Q.  I'm showing you what has been marked Exhibit 4. Is that the paper?
 A.  I think so. It says incident report [[IR-114-0419-02|rec:store incident report number]] at the top. That is not my signature at the bottom.

                                                                 Page 14
 Q.  How did you leave the store?
 A.  By ambulance. They took me to [[Rincon Vista Medical Center|o5:full]].
 Q.  What were you told about your injuries?
 A.  That I had [[a broken left wrist|health:injury]] and [[a hairline fracture in my hip|health:injury]].
 Q.  Did you have surgery?
 A.  [[Dr. Kelkar|p7:title-surname]] [[put a plate and screws in the wrist|health:surgical procedure]] on [[the 22nd|date:day of month only]]. The hip they left alone, but I was on a walker
     for seven weeks.
 Q.  Before this fall, had you ever injured that wrist or that hip?
 A.  No.
 Q.  Do you have any ongoing medical conditions?
 A.  I've had [[type 2 diabetes|health:chronic condition]] since my forties. I take [[metformin|health:medication]] for that. And they told me in 2019 I have [[osteoporosis|health:chronic condition]].
 Q.  Who told you that?
 A.  My regular doctor, after a bone scan.
     MS. HOLCOMBE:  Objection to the extent this calls for a medical opinion. You can answer what you know.
 Q.  Have you ever been a party to a lawsuit before this one?
 A.  No. Well. [[We filed a bankruptcy, a Chapter 13, back in 2012|attr:past bankruptcy]]. I don't know if that counts.
 Q.  Was that discharged?
 A.  Yes. We paid for five years.
 Q.  When did you go back to work?
 A.  [[June 30|date:month and day]]. Part time at first. I still can't type the way I used to.
 Q.  Let me show you Exhibit 7. Do you recognize it?
 A.  It's the hospital bill. [[Forty-one thousand|money:amount in words]] and change.
 Q.  The total shown is [[$41,286.90|money]]. Has any part of that been paid, to your knowledge?
 A.  The union plan paid some. We got a letter that they want it back out of the case.
     MR. ULBRICHT:  Let's take ten minutes.
     (Recess taken from 10:51 a.m. to 11:04 a.m.)

                                                                 Page 31
     (Deposition concluded at 12:17 p.m. Signature reserved under Rule 30(e).)

REPORTER'S CERTIFICATE
I, Paulette Dzialo, certify that the foregoing pages are a true record of the testimony given.
Dated [[October 21, 2025|date:certificate date]].  Job No. [[25-10-0933|rec:court reporting job number]]
'''))

# ---------------------------------------------------------------- 302
DOCS.append(D(302, "docx", "demand letter", "legal", "US", minors=["p2"],
  title="Pre-suit demand letter to a homeowner's insurer (dog bite, child claimant)",
  ents={"p1": "Tobias Q. Lindenmuth", "p2": "Mateo Covarrubias", "p3": "Yesenia Covarrubias", "p4": "Harlan Stubblefield",
        "p5": "Corinne Maddock", "p6": "Dr. Imogen Vasbinder", "p7": "Lucero Pineda",
        "o1": "Lindenmuth Trial Lawyers, P.C.", "o2": "Plumbline Mutual Insurance Company",
        "o3": "Smoky Ridge Children's Hospital", "o4": "Pellissippi Trace Elementary", "o5": "Vasbinder Facial Plastics"},
  distractors=["Tenn. Code Ann. § 44-8-413", "Rule 408", "CPT 12013", "TennCare"],
  header="[[Lindenmuth Trial Lawyers, P.C.|o1:full]] | Privileged settlement communication",
  footer="Claim [[PLM-HO-2025-0061847|rec:insurance claim number]] | Demand of [[November 3, 2025|date:letter date]]",
  body=r'''
# [[Lindenmuth Trial Lawyers, P.C.|o1:full]]
[[900 S. Gay Street, Suite 1150|addr:street with suite]] · [[Knoxville|place:city]], [[Tennessee|place:state]] [[37902|zip]] · [[(865) 555-0134|phone]] · [[tql@lindenmuthtrial.example|email]]
[[November 3, 2025|date:letter date]]
**VIA EMAIL AND CERTIFIED MAIL** ([[corinne.maddock@plumblinemutual.example|email]])
[[Corinne Maddock|p5:full]], Senior Claims Specialist
[[Plumbline Mutual Insurance Company|o2:full]]
[[P.O. Box 30418|addr:PO Box]], [[Nashville|place:city]], [[TN|place:state abbreviation]] [[37241-0418|zip:ZIP+4]]
**Re:** Your insured: [[Harlan Stubblefield|p4:full]] · Claim No. [[PLM-HO-2025-0061847|rec:insurance claim number]] · Policy [[HO3-7745120-02|rec:policy number]] · Date of loss: [[07/26/2025|date:date of loss]] · Our client: [[M.C.|p2:initials:minor identified by initials]], a minor, by his mother and next friend [[Yesenia Covarrubias|p3:full]]
**FOR SETTLEMENT PURPOSES ONLY — Rule 408**
Dear [[Ms. Maddock|p5:title-surname]]:
This firm represents [[Mateo Covarrubias|p2:full]], who is [[seven years old|indirect:age of a child claimant]], and his mother. [[Mateo|p2:first-name]] was born [[August 14, 2018|dob]] and is [[a second grader|indirect:school grade of a child]] at [[Pellissippi Trace Elementary|o4:full]]. Please treat this letter as our time-limited demand under the policy issued to [[Mr. Stubblefield|p4:title-surname]].
## Facts
On the evening of [[Saturday, July 26|date:weekday, month and day]], Mateo was riding his scooter on the sidewalk in front of your insured's home at [[4127 Tooles Bend Court|addr]] in [[Farragut|place:town]]. Your insured's dog, a 90-pound Rottweiler mix that was not on a leash and not behind a fence, knocked Mateo down and bit him in the face. A neighbor, [[Lucero Pineda|p7:full]], pulled the dog off. Animal control report no. [[AC-25-03391|rec:animal control report number]] records that the same dog bit a delivery driver in 2023. Liability under Tenn. Code Ann. § 44-8-413 is not in serious question.
## Injuries and treatment
- [[Smoky Ridge Children's Hospital|o3:full]] emergency department, [[7/26/25|date:short numeric date]], MRN [[SR-4471209|rec:medical record number]]: [[three puncture wounds to the right cheek|health:injury]] and [[a 4 cm laceration through the upper lip|health:injury]], [[closed with 14 sutures under sedation|health:procedure]] (billed as CPT 12013 and related codes).
- [[Dr. Imogen Vasbinder|p6:full]] of [[Vasbinder Facial Plastics|o5:full]] saw Mateo on [[Aug. 12|date:abbreviated month and day]] and [[September 30|date:month and day]]. She expects [[a permanent, visible scar|health:prognosis]] and recommends [[scar revision surgery at about age twelve|health:planned procedure]], estimated at [[$14,800|money]].
- Since the attack Mateo has [[nightmares and will not go near dogs|health:psychological symptoms]]; his pediatrician has diagnosed [[an adjustment disorder with anxiety|health:diagnosis]] and referred him for counseling.
## Special damages to date
| Provider | Dates | Charges |
| Smoky Ridge Children's Hospital | 7/26/25 | [[$9,412.37|money]] |
| [[Dr. Vasbinder|p6:title-surname]] | [[8/12|date:month/day only]] – [[9/30|date:month/day only]] | [[$1,150.00|money]] |
| Counseling (6 visits) | Sept – Oct | [[$780.00|money]] |
| Future scar revision (estimate) | — | [[$14,800.00|money]] |
| **Total** | | [[$26,142.37|money]] |
Mateo is covered by TennCare (member ID [[ZTN 4409 2218 7|govid:Medicaid member ID]]), which has paid [[$3,906.11|money]] and will assert a subrogation interest.
## Demand
In light of permanent facial scarring to a seven-year-old, we demand [[$185,000.00|money]] (**[[one hundred eighty-five thousand dollars|money:amount in words]]**) in full settlement. This offer remains open until 5:00 p.m. Eastern on [[December 5, 2025|date:deadline]]. Any settlement will require court approval because the claimant is a minor. [[Ms. Covarrubias|p3:title-surname]] can be reached only through this office; please do not contact her at [[865-555-0177|phone]] again.
Very truly yours,
[[Tobias Q. Lindenmuth|p1:full]] (BPR No. [[031877|govid:state bar number]])
[[TQL|p1:initials]]/lp
'''))

# ---------------------------------------------------------------- 303
DOCS.append(D(303, "eml", "client care and engagement email", "legal", "UK", enc="qp",
  title="Solicitor's engagement email on a house purchase, with the client's quoted reply",
  ents={"p1": "Fenella Ogilvie", "p2": "Dafydd Llewellyn-Price", "p3": "Anjali Raghunathan", "p4": "Kieran Musgrove",
        "o1": "Thwaite & Pendlebury Solicitors LLP", "o2": "Ravenglass Building Society", "o3": "Fellside Estates"},
  distractors=["Form TA6", "SDLT", "Law Society Conveyancing Protocol", "SRA", "Help to Buy ISA"],
  headers={"From": "[[Fenella Ogilvie|p1:full]] <[[f.ogilvie@thwaitependlebury.example|email]]>",
           "To": "[[Dafydd Llewellyn-Price|p2:full]] <[[dafydd.lp@fellmail.example|email]]>",
           "Cc": "[[anjali.raghunathan@fellmail.example|email]]",
           "Subject": "RE: [[14 Tanner's Yard|addr:house number and street]] - engagement, ID and money on account (our ref [[FO/LLE0412/1|rec:solicitor file reference]])",
           "Date": "Thu, [[6 Nov 2025|date:email header date]] 16:48:09 +0000"},
  body=r'''
Dear [[Dafydd|p2:first-name]] and [[Anjali|p3:first-name]],

Thank you for instructing [[Thwaite & Pendlebury Solicitors LLP|o1:full]] on your purchase of [[14 Tanner's Yard|addr:house number and street]], [[Kendal|place:town]], [[Cumbria|place:county]] [[LA9 4HT|zip:UK postcode]] at [[£284,950|money:pounds]]. Our client care letter is attached; the key points are below.

1. Fees. Our fixed fee is [[£1,150|money:pounds]] plus VAT ([[£1,380.00|money:pounds]] in all). Searches will be about [[£312.40|money:pounds]] and the Land Registry fee [[£150|money:pounds]]. On the figures you gave, no SDLT is payable as first-time buyers.

2. Money on account. Please send [[£500.00|money:pounds]] before we order searches, to our client account only:
     Sort code [[97-26-60|rtn:UK sort code]]   Account [[02659322|acct:UK account number]]
     IBAN [[GB15 NWBK 9726 6002 6593 22|iban]] (only needed if paying from abroad)
     Reference [[LLE0412|rec:payment reference]]
   We will NEVER change these details by email. If you receive anything saying otherwise, ring me on [[01632 960147|phone:UK landline]] before sending a penny.

3. ID. Thank you for the scans. For our records: [[Dafydd|p2:first-name]]'s passport no. [[533402917|govid:UK passport number]] (expires [[14/08/2031|date:day-first numeric]]), driving licence [[LLEWE801124D99XK|govid:UK driving licence number]]; Anjali's passport no. [[Z4418830|govid:Indian passport number]] and biometric residence permit [[ZU9041127|govid:residence permit number]]. Anjali, as you hold [[a Skilled Worker visa|attr:immigration status]], the lender will want to see at least 12 months left on it. Yours runs to [[2 March 2028|date:visa expiry]], so that is fine.

4. Mortgage. [[Ravenglass Building Society|o2:full]] have issued the offer (roll no. [[RBS/7741209-3|rec:mortgage roll number]]) for [[£256,455|money:pounds]]. The balance of the deposit from you will be [[£28,495|money:pounds]], part of it from Dafydd's Help to Buy ISA.

5. Timing. The sellers' agent, [[Kieran Musgrove|p4:full]] at [[Fellside Estates|o3:full]], is pressing for exchange by [[Friday 28 November|date:weekday, day and month]] and completion on [[12 December 2025|date:completion date]]. We have the Form TA6 and are following the Law Society Conveyancing Protocol.

We are authorised and regulated by the SRA. I am in the office Monday to Thursday; my mobile is [[07700 900152|phone:UK mobile]].

Kind regards,
[[Fenella|p1:first-name]]

[[Fenella Ogilvie|p1:full]] | Associate Solicitor, Residential Property
[[Thwaite & Pendlebury|o1:short]] | [[3 Finkle Street|addr]], Kendal [[LA9 4AB|zip:UK postcode]] | [[www.thwaitependlebury.example|url:firm website]]

> On [[5 Nov 2025|date:quoted reply date]], at 21:14, Dafydd Llewellyn-Price wrote:
> hi [[fenella|p1:first-name!:lower case]], passports + my licence attached. [[anjalis|p3:first-name!:lower case possessive without apostrophe]] BRP is the pink card, both sides.
> NI numbers if you need them - mine [[PB 41 72 09 C|taxid:UK National Insurance number]], hers [[SK 60 31 88 A|taxid:UK National Insurance number]]
> dobs: me [[24.11.1980|dob:dotted day-first]], anj [[9 Jan 87|dob:two-digit year]]
> we're still at [[Flat 3, 27 Stricklandgate|addr:flat and street]] til the move. can we pay the [[500|money!:bare number, no currency sign]] by card? [[kieran|p4:first-name!:lower case]] says the sellers want [[the 28th|date:day of month only]]
> cheers, [[D|p2:initials:single initial sign-off]]
'''))

# ---------------------------------------------------------------- 304
DOCS.append(D(304, "txt", "voicemail transcription log", "legal", "US", length="short", cardholders=["p1"],
  title="Auto-transcribed voicemails on a law office line",
  ents={"p1": "Ronnie Latiolais", "p2": "Ms. Quennell", "p3": "Dr. Anand Bhagwat"},
  distractors=["VM-to-text beta"],
  body=r'''
VM-to-text beta - main line [[412-555-0100|phone]] - transcripts not proofread

[[[11/4|date:month/day only]] 8:02a, 1m12s, from [[4125550163|phone:no separators]]]
hi this is uh [[ronnie latiolais|p1:full!:lower case, auto-transcribed]] calling for [[miss quennell|p2:title-surname!:lower case, title spelled out]]. my court date got moved to [[the nineteenth|date:day of month in words]], case is [[cr 2025 08812|rec:criminal case number as spoken]]. you can run my visa for [[the fifteen hundred|money:amount in words]], its [[4708 0349 9544 0084|card]] expires [[oh three twenty eight|exp:expiry as spoken]] code on the back [[771|cvv]]. im staying at my sisters in [[mckeesport|place!:city in lower case]] so call the cell not the house

[11/4 11:40a, 0m31s, from [[(412) 555-0119|phone]]]
[[Dr. Bhagwat|p3:title-surname]]'s office, records for [[Ronald Latiolais|p1:full:formal first name]] date of birth [[6/2/71|dob:short numeric]] are ready, copy fee is [[$45|money]]
'''))

# ---------------------------------------------------------------- 305
DOCS.append(D(305, "pdf", "last will and testament with client data sheet", "legal", "US", minors=["p5", "p6"],
  title="Will of a 91-year-old widower with the attorney's client data sheet",
  ents={"p1": "Cornelius Augustin Vandiver", "p2": "Henrietta Vandiver", "p3": "Lucinda Vandiver Peebles",
        "p4": "Augustin Vandiver Jr.", "p5": "Wren Peebles", "p6": "Amos Peebles", "p7": "Odessa Gathers",
        "p8": "Philippa Ravenel-Sims", "p9": "Marcus Tindall",
        "o1": "Tidelands Trust Company", "o2": "Mt. Carmel A.M.E. Church", "o3": "Ravenel-Sims Law Firm, LLC",
        "o4": "Port Royal Sound Bank"},
  distractors=["S.C. Code Ann. § 62-2-502", "South Carolina Uniform Transfers to Minors Act", "ARTICLE III", "Schedule A",
               ],
  body=r'''
# LAST WILL AND TESTAMENT OF [[CORNELIUS AUGUSTIN VANDIVER|p1:caps:name in title]]
I, [[Cornelius Augustin Vandiver|p1:full]], also known as [[C.A. Vandiver|p1:short:initials + surname]], a resident of [[Beaufort County|place:county]], [[South Carolina|place:state]], being [[ninety-one (91)|age:age in words and digits]] years of age and of sound mind, declare this to be my Last Will and revoke all earlier wills and codicils.
## ARTICLE I — Family
My wife, [[Henrietta Vandiver|p2:full]], died on [[February 2, 2019|date:date of death]]. I have two children, [[Lucinda Vandiver Peebles|p3:full]] and [[Augustin Vandiver Jr.|p4:full]], and two grandchildren, [[Wren Peebles|p5:full]] and [[Amos Peebles|p6:full]].
## ARTICLE II — Specific gifts
- To [[Mt. Carmel A.M.E. Church|o2:full]], where I have served [[as a deacon for forty years|attr:religious office]], the sum of [[Ten Thousand Dollars ($10,000.00)|money:amount in words and digits]].
- To [[Odessa Gathers|p7:full]], [[who has kept my house and cared for me since my wife's death|indirect:caregiver identified by role]], the sum of [[$25,000|money]] and my 2017 Buick, if she survives me.
- To my son [[Gus|p4:nickname]], my late wife's interest in [[the shrimp boat "Miss Henrietta"|indirect:named boat]] and all of my tools.
## ARTICLE III — Residue
I give the rest of my estate in equal shares to my two children. The share of any grandchild under the age of twenty-five shall be held by my Executor as custodian under the South Carolina Uniform Transfers to Minors Act.
## ARTICLE IV — Executor
I name my daughter [[Lucinda|p3:first-name]] as Executor. If she cannot serve, I name [[Tidelands Trust Company|o1:full]]. No bond shall be required.
Signed on [[the 17th day of October, 2025|date:formal long date]], at [[Bluffton|place:town]], South Carolina. Because [[my eyesight has failed|health:condition]], this Will was read aloud to me before I signed it.
[[Cornelius A. Vandiver|p1:short:middle initial]], Testator
Witnesses, under S.C. Code Ann. § 62-2-502: [[Marcus Tindall|p9:full]], of [[Hardeeville|place:town]]; [[Philippa Ravenel-Sims|p8:full]], of Bluffton.
---
# CLIENT DATA SHEET — not part of the Will
[[Ravenel-Sims Law Firm, LLC|o3:full]] · File [[25-EP-0417|rec:firm file number]] · Prepared by [[P. Ravenel-Sims|p8:short:initial + surname]]
- Client: [[Vandiver, Cornelius A.|p1:last-first]] · born [[06/11/1934|dob]] · SSN [[084-35-7507|ssn]] · widowed
- Home: [[118 Egret Landing Road|addr]], Bluffton, [[SC|place:state abbreviation]] [[29910|zip]] · landline [[843-555-0121|phone]] (no email; [[hard of hearing|health:condition]], call after 10)
- Daughter: Lucinda Vandiver Peebles, [[77 Gadsden Street|addr]], [[Charleston|place:city]], SC [[29401|zip]] · [[843.555.0188|phone:dotted]] · [[lucinda.peebles@lowtidemail.example|email]]
- Son: [[Augustin Jr.|p4:short:first name with suffix]] ("Gus"), [[lives on the boat at the Port Royal landing|indirect:unusual residence]]. [[In recovery; two DUI convictions (2011, 2016)|attr:criminal history and addiction recovery]]. Client does not want this mentioned in the Will.
- Grandchildren: [[Wren|p5:first-name!:given name that is also a common word]], born [[2014|dob!:birth year only]]; [[Amos|p6:first-name]], [[age 9|indirect:age of a grandchild]]. Wren has [[cystic fibrosis|health:diagnosis]]; discuss a supplemental needs trust with [[Mrs. Peebles|p3:title-surname]].
- Diagnoses the client reports: [[macular degeneration|health:diagnosis]], [[atrial fibrillation|health:diagnosis]], on [[warfarin|health:medication]]. Dr.'s capacity letter requested [[10/09/25|date:short numeric date]].
## Schedule A — assets (client's own figures)
- Home, [[Egret Landing Road|addr!:street name only, no number]], tax map no. [[R610 039 000 0218 0000|rec:county tax map number]]: about [[$640,000|money]].
- [[Port Royal Sound Bank|o4:full]] checking [[0077-41852|acct]] and CD [[0077-90031|acct:certificate of deposit number]]: [[$38,200|money]] and [[$150,000|money]].
- Tidelands Trust Company agency account [[TT-204417|acct:trust agency account]]: [[$412,775.18|money]] at [[9/30/2025|date:statement date]].
- Burial policy no. [[BP-0091873|rec:policy number]], face amount [[$7,500|money]].
Fee quoted: flat [[$1,800|money]], paid by check no. [[2291|rec!:check number]].
'''))

# ---------------------------------------------------------------- 306
DOCS.append(D(306, "md", "undertakings and refusals chart", "legal", "CA",
  title="Undertakings chart after examination for discovery (Ontario disability claim)",
  ents={"p1": "Shirin Golzari", "p2": "Maeve Teskey", "p3": "Dev Raichura", "p4": "Dr. Lakshmi Ponnambalam",
        "p5": "Farhad Golzari",
        "o1": "Stonecutter Assurance Company of Canada", "o2": "Teskey Injury Law", "o3": "Kilbride Logistics Inc.",
        "o4": "Humberline Credit Union", "o5": "Raichura Baptiste-Cole LLP"},
  distractors=["Rule 31.07", "Rules of Civil Procedure", "OHIP", "Ontario Superior Court of Justice", "T4", "CPP-D", "Form 30C"],
  body=r'''
# Undertakings, under advisements and refusals

**Court file no.** [[CV-24-00718834-0000|rec:court file number]] (Ontario Superior Court of Justice, [[Toronto|place:city]])
**[[GOLZARI|p1:caps:surname in short style of cause]] v. [[STONECUTTER ASSURANCE|o1:caps:short name in caps]]**
Examination for discovery of the plaintiff, [[Shirin Golzari|p1:full]], held [[2025-09-18|date:ISO date]] by video.
Examined by [[Dev Raichura|p3:full]] ([[Raichura Baptiste-Cole LLP|o5:full]]) for the defendant, [[Stonecutter Assurance Company of Canada|o1:full]].
Chart prepared by [[Maeve Teskey|p2:full]], [[Teskey Injury Law|o2:full]], [[410-55 Eglinton Ave. E.|addr:unit-first Canadian address]], Toronto [[ON|place:province abbreviation]] [[M4P 1G8|zip:Canadian postal code]], [[mteskey@teskeyinjury.example|email]], [[416-555-0193|phone]]. LSO no. [[71884K|govid:law society number]].
Answers due [[November 17, 2025|date:deadline]] (60 days; Rule 31.07 of the Rules of Civil Procedure applies to anything not answered).

| # | Q. | Page | U / UA / R | Undertaking | Status as of [[Nov. 4/25|date:abbreviated date with slash year]] |
|---|----|------|-----------|-------------|--------|
| 1 | 44 | 12 | U | Produce decoded OHIP summary from [[1 Jan 2019|date]] to date. Health card [[4418 902 337 KP|govid:Ontario health card number with version code]]. | Requested [[Sept 22|date:abbreviated month and day]]; not yet received. |
| 2 | 51 | 14 | U | Clinical notes and records of the family doctor, [[Dr. Lakshmi Ponnambalam|p4:full]], [[2200 Danforth Ave.|addr]], from 2019. | Received 212 pp. To be served. |
| 3 | 63 | 17 | U | Complete employment file from [[Kilbride Logistics Inc.|o3:full]], employee no. [[KL-20771|rec:employee number]], incl. attendance for 2021-2022. | [[Kilbride|o3:short]] HR says 3 weeks. |
| 4 | 70 | 19 | UA | Income tax returns and notices of assessment 2020-2023. SIN [[546 636 465|taxid:SIN with spaces]] to be redacted before service. | 2020-2022 in hand; 2023 T4 missing. |
| 5 | 88 | 24 | U | Statements for the joint account with her husband, [[Farhad Golzari|p5:full]], at [[Humberline Credit Union|o4:full]], transit [[20412|rtn:Canadian transit number]], inst. [[828|rtn:Canadian institution number]], acct [[4411907|acct]], for [[March 2022|date:month and year]] to date. | Client to download. |
| 6 | 102 | 29 | R | Posts from her running account, [[@shirin.g.runs|cred:social media handle]], after the date of disability. | Refused: relevance, proportionality. |
| 7 | 117 | 33 | UA | Whether she has applied for CPP-D and, if so, the decision letter. | Applied [[06/02/2023|date:numeric date]]; [[denied, under reconsideration|attr:disability benefit application status]]. |
| 8 | 131 | 38 | U | Names of all treating psychologists and psychiatrists since 2019. | See note below. |

## Notes for [[Maeve|p2:first-name]] before we answer

- Date of disability pleaded: [[14 February 2022|date:date of disability]]. Policy [[GH-0044718|rec:group policy number]], certificate [[0020771|rec:certificate number]]. Monthly benefit claimed [[$3,412.50|money]]; arrears to date about [[$146,700|money]].
- Diagnoses in the file: [[fibromyalgia|health:diagnosis]] (2021) and [[major depressive disorder|health:diagnosis]]. She told [[Mr. Raichura|p3:title-surname]] on the record about [[a hospital admission in December 2022 after an overdose|health:psychiatric admission]]. That admission is NOT in [[Dr. Ponnambalam|p4:title-surname]]'s notes; ask [[Shirin|p1:first-name]] which hospital before we answer no. 8.
- [[Shirin|p1:first-name]]'s date of birth is [[1984-07-30|dob:ISO date]], not 1985 as in the Form 30C. Home: [[1806-88 Thorncliffe Park Dr.|addr:unit-first Canadian address]], [[East York|place:district]], [[M4H 1N5|zip:Canadian postal code]]. Cell [[647 555 0150|phone:spaces only]]. She [[prefers Farsi|attr:language indicating national origin]] for anything complicated; [[Farhad|p5:first-name]] interprets.
- Our file: [[TIL-2024-0388|rec:firm file number]].
'''))

# ---------------------------------------------------------------- 307
DOCS.append(D(307, "xlsx", "settlement distribution statement", "legal", "US",
  title="Personal injury settlement distribution workbook",
  ents={"p1": "Thaddeus Brightwell", "p2": "Renata Szczepanski", "p3": "Aurelio Fontanez", "p4": "Kendra Brightwell",
        "o1": "Corbel Freight Systems, LLC", "o2": "Fontanez & Drury, Attorneys", "o3": "Bluewillow Health Plan",
        "o4": "Calhoun Orthopaedic Associates", "o5": "Lodestar Legal Funding", "o6": "Chattahoochee Valley Bank",
        "o7": "Ocmulgee Imaging Center"},
  distractors=["O.C.G.A. § 51-12-1", "Form W-9", "Medicare"],
  sheets=[
    ("Statement", [
      ["SETTLEMENT STATEMENT - attorney/client privileged"],
      ["Client", "[[Brightwell, Thaddeus|p1:last-first]]", "aka", "[[Tad|p1:nickname]]", "File", "[[FD-23-1182|rec:firm file number]]"],
      ["Matter", "[[Brightwell|p1:surname]] v. [[Corbel Freight Systems, LLC|o1:full]]", "Civil action", "[[23-CV-04471-B|rec:civil action number]]", "DOL", dt("2023-03-09", "mm/dd/yyyy", "date:date of loss")],
      ["Prepared by", "[[Aurelio Fontanez|p3:full]]", "", "", "Date", dt("2025-10-28", "mmmm d, yyyy", "date:statement date")],
      [],
      ["Line", "Item", "Payee", "Amount", "Note"],
      [1, "Gross settlement", "[[Corbel Freight|o1:short]] / its carrier", amt(275000.00, "acct"), "Release signed [[10/14|date:month/day only]]"],
      [2, "Attorney fee 33 1/3%", "[[Fontanez & Drury, Attorneys|o2:full]]", amt(-91666.67, "acct"), "per contract"],
      [3, "Case costs advanced", "[[Fontanez & Drury|o2:short]]", amt(-12418.33, "acct"), "see Costs tab in file"],
      [4, "Health plan subrogation", "[[Bluewillow Health Plan|o3:full]]", amt(-18250.00, "acct"), "reduced from [[$31,906.44|money]]; O.C.G.A. § 51-12-1"],
      [5, "Medicare conditional payment", "Medicare", amt(-2114.09, "acct"), "final demand ltr [[9/30/25|date:short numeric date]]"],
      [6, "Balance - surgeon", "[[Calhoun Orthopaedic Associates|o4:full]]", amt(-9800.00, "acct"), "[[Dr. Szczepanski|p2:title-surname]], acct [[COA-558812|rec:patient account number]]"],
      [7, "Balance - MRI", "[[Ocmulgee Imaging Center|o7:full]]", amt(-1350.00, "acct"), ""],
      [8, "Pre-settlement advance payoff", "[[Lodestar Legal Funding|o5:full]]", amt(-14725.00, "acct"), "payoff good through [[11/15/2025|date:payoff date]]; contract [[LLF-0092217|rec:funding contract number]]"],
      [9, "Child support lien", "Georgia DHS", amt(-4210.55, "acct"), "[[arrears owed for a child of a prior relationship|attr:court-ordered support arrears]]"],
      [10, "NET TO CLIENT", "[[Thaddeus Brightwell|p1:full]]", amt(120465.36, "acct"), "wire - see Wire tab"],
    ]),
    ("Liens", [
      ["Lienholder", "Contact", "Phone", "Their ref", "Claimed", "Agreed", "Paid by check no."],
      ["Bluewillow Health Plan", "[[subro@bluewillowhp.example|email]]", "[[800-555-0142|phone:toll-free]]", "[[BW-SUB-7714920|rec:subrogation file number]]", amt(31906.44, "usd", None), amt(18250.00, "usd", "money"), "[[10418|rec!:check number]]"],
      ["[[Calhoun Orthopaedic|o4:short]]", "[[Renata Szczepanski|p2:full]], MD", "[[(478) 555-0166|phone]]", "COA-558812", amt(16240.00), amt(9800.00, "usd", "money"), "[[10419|rec!:check number]]"],
      ["[[Lodestar|o5:short]]", "[[payoffs@lodestarfunding.example|email]]", "[[4785550109|phone:no separators]]", "LLF-0092217", amt(14725.00), amt(14725.00, "usd", None), "wire"],
      ["Member ID on the [[Bluewillow|o3:short]] file", "[[BWH884120773|rec:health plan member ID]]", "", "", "", "", ""],
      ["Client's Medicare number", "[[4TK7-RG2-MH61|govid:Medicare beneficiary identifier]]", "", "", "", "", ""],
    ]),
    ("Wire", [
      ["Field", "Value"],
      ["Beneficiary", "[[Thaddeus R. Brightwell|p1:full:with middle initial]] and [[Kendra Brightwell|p4:full]] (joint)"],
      ["Beneficiary address", "[[2904 Rivoli Drive|addr]], [[Macon|place:city]], [[GA|place:state abbreviation]] [[31210|zip]]"],
      ["Bank", "[[Chattahoochee Valley Bank|o6:full]]"],
      ["ABA", "[[067740879|rtn:ABA routing number]]"],
      ["Account", num(48812277, "acct:account number stored as a number")],
      ["Amount", amt(120465.36, "usd", "money")],
      ["Callback verified", "Spoke to [[Tad|p1:nickname]] at [[478-555-0131|phone]], [[10/27|date:month/day only]] 3:10 pm; he read back the last four, [[2277|acct:last four of account]]"],
      ["Client SSN (for the Form W-9 on the interest portion)", "[[136-61-4006|ssn]]"],
      ["Client DOB", dt("1957-12-01", "m/d/yyyy", "dob")],
    ]),
  ]))

# ---------------------------------------------------------------- 308
DOCS.append(D(308, "txt", "administrative hearing transcript excerpt", "legal", "US",
  title="Unemployment insurance appeal hearing by telephone (excerpt)",
  ents={"p1": "Tsehay Woldemichael", "p2": "Bernadine Fosse", "p3": "Trevor Lunsford", "p4": "Kalkidan",
        "o1": "Quayside Valet & Parking, Inc.", "o2": "Unemployment Law Clinic of Puget Sound"},
  distractors=["RCW 50.20.066", "WAC 192-150-205", "OFFICE OF ADMINISTRATIVE HEARINGS", "Employment Security Department",
               "Exhibit 3"],
  body=r'''
OFFICE OF ADMINISTRATIVE HEARINGS - for the Employment Security Department
Docket [[04-2025-UI-118204|rec:hearing docket number]]     Claimant ID [[7700418823|rec:claimant ID]]     SSN [[xxx-xx-8373|ssn:masked, lower-case x]]
Claimant: [[TSEHAY WOLDEMICHAEL|p1:caps]]          Employer: [[QUAYSIDE VALET & PARKING, INC.|o1:caps]]
Telephone hearing, [[November 6, 2025|date:hearing date]], 1:15 p.m. Recording begins.

JUDGE [[FOSSE|p2:caps:surname in caps after title]]: This is Administrative Law Judge [[Bernadine Fosse|p2:full]]. The issue is whether the claimant was discharged for misconduct under RCW 50.20.066. On the line I have the claimant, her representative from the [[Unemployment Law Clinic of Puget Sound|o2:full]], and for the employer, [[Mr. Lunsford|p3:title-surname]]. [[Ms. Woldemichael|p1:title-surname]], I'm calling you at [[206-555-0114|phone]], is that a good number if we're disconnected?

CLAIMANT: Yes. That is my daughter's phone. [[Kalkidan|p4:first-name]]. Mine is broken.

JUDGE: And your mailing address is still [[8815 Renton Avenue South, Apartment 204|addr:street with apartment]], [[Seattle|place:city]], [[98118|zip]]?

CLAIMANT: Yes. [[Rainier Beach|place:neighbourhood]].

JUDGE: [[Mr. Lunsford|p3:title-surname]], your full name and position.

[[MR. LUNSFORD|p3:caps:title + surname in caps]]: [[Trevor Lunsford|p3:full]], regional operations manager, [[Quayside Valet|o1:short]]. We let her go on [[September 12th|date:month and ordinal day]] for a third no-call, no-show. It's in Exhibit 3, the points sheet. She was at seven and a half points.

JUDGE: Ms. Woldemichael, what was your job and rate of pay?

CLAIMANT: Cashier at the garage on [[Pike Street|addr!:street name only, no number]], four years. [[$21.40|money:hourly rate]] an hour.

JUDGE: Tell me about [[September 11|date:month and day]].

CLAIMANT: That day is our New Year. [[Enkutatash|attr:holiday revealing ethnic and religious background]]. [[I am Ethiopian Orthodox|attr:religion]]. Every year I ask for this day and I get it. This year in August I asked the new supervisor and he said "put it in the app." I put it in the app. I have the picture, it says "pending." Nobody answered me.

MR. LUNSFORD: Pending isn't approved, Your Honor. The handbook is clear.

JUDGE: You'll have your turn. Go on, ma'am.

CLAIMANT: The other two times, in July, I was at the hospital. [[I was pregnant and I lost the baby|health:pregnancy loss]]. I brought the paper from the doctor on [[July 22|date:month and day]]. He did not take the points away.

JUDGE: Mr. Lunsford, did the employer receive medical documentation in July?

MR. LUNSFORD: I'd have to check with HR. I will say, when she was hired her work permit was a temporary one, and there was a gap when it expired, so there's history of paperwork being late.

CLAIMANT: [[I am an asylee|attr:immigration status]]. My card was renewed. USCIS was late, not me. I never worked one day without permission.

JUDGE: That isn't the issue before me and I'm not going to consider it. Under WAC 192-150-205 the employer has the burden. Mr. Lunsford, does the company have anything in writing showing the September 11 request was denied before the shift?

MR. LUNSFORD: Not in front of me.

JUDGE: All right. I'll leave the record open until [[November 13|date:deadline]] for the app screenshot and the July doctor's note. Send them to the fax on the notice. Ms. Woldemichael, your weekly benefit amount if you prevail is [[$612|money:weekly benefit amount]], going back to the week of [[9/14/2025|date:numeric date]]. A written order will be mailed. We're off the record at 1:52.
'''))

# ---------------------------------------------------------------- 309
DOCS.append(D(309, "html", "web intake form submission", "legal", "US", raw_html=True, cardholders=["p2"],
  title="Expungement intake form as received from a law firm's website",
  ents={"p1": "DeShawn Marcellus Pettway", "p2": "Lorraine Pettway", "p3": "Adaeze Oyinlola",
        "o1": "Gravois & Oyinlola, Attorneys at Law", "o2": "Halsted Street Bakehouse"},
  distractors=["20 ILCS 2630/5.2", "FormRelay 4.2", "Illinois State Police", "Class A misdemeanor"],
  body=r'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>New intake submission</title>
<style>td{padding:3px 10px;vertical-align:top} .k{color:#555}</style></head>
<body>
<p>FormRelay 4.2 notification &mdash; do not reply</p>
<h2>New submission: Record sealing / expungement intake</h2>
<p>Submission [[S-8F31C2|rec:form submission ID]] received [[11/07/2025|date:submission date]] 22:41 from IP [[203.0.113.58|ip]]. Assigned to: [[Adaeze Oyinlola|p3:full]]. View in portal: [[https://intake.gravoislaw.example/s/8f31c2|url:link to the submission]]</p>
<table>
<tr><td class="k">Legal name</td><td>[[DeShawn Marcellus Pettway|p1:full]]</td></tr>
<tr><td class="k">Other names used</td><td>[[Shawn Pettway|p1:short:shortened first name]]; "[[D-Money|p1:nickname:street nickname]]" (appears on one arrest report)</td></tr>
<tr><td class="k">Date of birth</td><td>[[04/17/1994|dob]]</td></tr>
<tr><td class="k">SSN (last 4)</td><td>[[2543|ssn:last four digits only]]</td></tr>
<tr><td class="k">Driver's license / state ID</td><td>[[P300-1764-8291|govid:driver's license number]] (IL)</td></tr>
<tr><td class="k">Address</td><td>[[6120 S. Vernon Ave., Apt 2R|addr:street with apartment]], [[Chicago|place:city]], [[IL|place:state abbreviation]] [[60637|zip]]</td></tr>
<tr><td class="k">Phone</td><td>[[773-555-0158|phone]] (text is better)</td></tr>
<tr><td class="k">Email</td><td>[[dpettway94@lakemail.example|email]]</td></tr>
<tr><td class="k">Current employer</td><td>[[Halsted Street Bakehouse|o2:full]] &mdash; they do NOT know about my record, please don't call there</td></tr>
<tr><td class="k">Arrests / cases (as best you remember)</td><td>
 1. 2016, [[Cook County|place:county]], [[retail theft, pled guilty, 12 months supervision|attr:criminal history]], case [[16 CR 0448120|rec:criminal case number]].<br>
 2. [[March 2019|date:month and year]], [[arrested for DUI in Evanston, case dismissed|attr:criminal history]]. Don't have the number. I think it started with [[19 DT|rec!:partial case number]].<br>
 3. 2021, [[possession of cannabis ticket|attr:criminal history]], paid a [[$200|money]] fine.</td></tr>
<tr><td class="k">Fingerprinted by</td><td>Illinois State Police; IR number on my rap sheet is [[IR 2204187|rec:police identification record number]]</td></tr>
<tr><td class="k">Why are you seeking sealing now?</td><td>I was turned down for an apartment in [[Oak Park|place:town]] on [[10/30|date:month/day only]] after a background check. Also I want to apply for a CDL. My mom is helping me pay for this.</td></tr>
<tr><td class="k">Anything else?</td><td>[[I am on the kidney transplant list|health:condition]] so some days I am at dialysis and can't answer.</td></tr>
</table>
<h3>Consultation fee &mdash; entered by front desk</h3>
<table>
<tr><td class="k">Amount</td><td>[[$150.00|money]]</td></tr>
<tr><td class="k">Cardholder</td><td>[[Lorraine Pettway|p2:full]] (mother) &mdash; [[773.555.0102|phone:dotted]]</td></tr>
<tr><td class="k">Card</td><td>Mastercard [[5112 7137 5139 2756|card]]</td></tr>
<tr><td class="k">Exp / CVC</td><td>[[09/27|exp]] / [[418|cvv]]</td></tr>
<tr><td class="k">Billing ZIP</td><td>[[60619|zip]]</td></tr>
<tr><td class="k">Receipt</td><td>[[R-110725-0093|rec:receipt number]], emailed to [[lorraine.pettway@lakemail.example|email]]</td></tr>
</table>
<p>Staff note ([[AO|p3:initials]], [[11/8|date:month/day only]]): Case 1 is a Class A misdemeanor with supervision completed, so it is eligible under 20 ILCS 2630/5.2. Pull the [[Evanston|place:city]] file. Consult booked [[Nov. 14|date:abbreviated month and day]] at 10:30 with [[Ms. Oyinlola|p3:title-surname]]. Conflict check for [[Gravois & Oyinlola, Attorneys at Law|o1:full]]: clear.</p>
</body></html>
'''))

# ---------------------------------------------------------------- 310
DOCS.append(D(310, "rtf", "residential tenancy abstract", "legal", "EU",
  title="Abstract of a residential letting in Galway",
  ents={"p1": "Sorcha Ní Fhlannagáin", "p2": "Tomasz Wieczorek", "p3": "Ana-Luísa Figueiredo", "p4": "Declan Heffernan",
        "o1": "Corrib Lettings Ltd", "o2": "Lough Atalia Credit Union"},
  distractors=["Residential Tenancies Act 2004", "RTB", "Part 4 tenancy", "BER C2", "Rent Pressure Zone"],
  body=r'''
# Tenancy abstract — [[Apt 12, The Maltings, Bridge Street|addr:apartment, building and street]]
Prepared by [[Declan Heffernan|p4:full]], [[Corrib Lettings Ltd|o1:full]], for the landlord's solicitor. Our ref [[CL/GAL/0338|rec:agent file reference]]. Dated [[04/11/2025|date:day-first numeric]].
## Parties
| Role | Name | Contact | PPSN |
| Landlord | [[Sorcha Ní Fhlannagáin|p1:full:Irish-language name with particle]] | [[sorcha.nif@iarthar.example|email]], [[087 555 0144|phone:Irish mobile]] | [[7284519TA|taxid:Irish PPS number]] |
| Tenant 1 | [[Tomasz Wieczorek|p2:full]] | [[t.wieczorek@postoffice.example|email]], [[+353 85 555 0190|phone:international format]] | [[3391057LW|taxid:Irish PPS number]] |
| Tenant 2 | [[Ana-Luísa Figueiredo|p3:full]] | [[085 555 0161|phone:Irish mobile]] | [[4410882F|taxid:Irish PPS number]] |
| Agent | [[Corrib Lettings|o1:short]] | [[091 555 0120|phone:Irish landline]] | — |
## Premises
[[Apt 12, The Maltings, Bridge Street|addr:apartment, building and street]], [[Galway|place:city]], [[H91 XK2P|zip:Eircode]]. Two-bed, second floor, BER C2. The landlord's own address for notices is [[Teach na Mara|addr:house name only]], [[An Spidéal|place:village, Irish-language name]], [[Co. na Gaillimhe|place:county, Irish-language form]], [[H91 F6W3|zip:Eircode]].
## Key terms
- Tenancy began [[1 September 2023|date:commencement]]; fixed term to [[31 August 2024|date:end of fixed term]], now a Part 4 tenancy under the Residential Tenancies Act 2004.
- RTB registration no. [[RT-0923-118703|rec:tenancy registration number]]. The property is in a Rent Pressure Zone.
- Rent [[€1,850|money:euro]] per month, reviewed to [[€1,887.00|money:euro]] from [[01/09/2025|date:day-first numeric]] (2% cap). Deposit held: [[€1,850|money:euro]].
- Rent is paid by standing order on the 1st to the landlord's account at [[Lough Atalia Credit Union|o2:full]]: IBAN [[IE23 AIBK 3657 8015 7702 51|iban]], BIC [[LACUIE2GXXX|acct:BIC / SWIFT code]].
- Of the monthly rent, [[€1,100|money:euro]] comes direct from the council because [[the tenants receive HAP|attr:housing benefit status]] (HAP ref. [[GCC-HAP-0044172|rec:housing assistance reference]]); the tenants pay the remaining [[€787|money:euro]] themselves.
## Current position
- [[Ms Ní Fhlannagáin|p1:title-surname]] wishes to sell and has asked whether a notice of termination can be served. Length of tenancy is over two years, so the notice period is 180 days at least.
- Arrears: the tenants' top-up was missed for August and [[October 2025|date:month and year]]; balance owing [[€1,574.00|money:euro]]. [[Mr Wieczorek|p2:title-surname]] says [[he was laid off from the medical device plant in Parkmore in July|indirect:job loss at an identifiable employer]] and has asked for a payment plan of [[€150|money:euro]] a month.
- [[Ana-Luísa|p3:first-name]] is [[expecting a baby in January|health:pregnancy]]; [[Sorcha|p1:first-name]] knows this and does not want it referred to in any notice.
- Inspection of [[22 October|date:day and month]]: no damage; smoke alarm in hall replaced.
'''))
