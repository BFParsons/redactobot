from corpus_src.dsl import D, dt, amt, num

DOCS = []

# ---------------------------------------------------------------- 81
DOCS.append(D(81, "txt", "client meeting notes", "legal", "US",
  title="Client meeting notes - sale of a family millwork business",
  ents={"p1": "Hunter Abernathy-Sloane", "p2": "Georgia Sloane", "p3": "Soledad Ibarra",
        "p4": "William Tran", "p5": "Wade R. Abernathy", "p6": "Marisol Abernathy",
        "p7": "Preston Achebe", "p8": "Dmitri Vasquez-Koval",
        "o1": "Ibarra Kettleman LLP", "o2": "Three Forks Millwork & Cabinet Co.",
        "o3": "Ridgeline Building Products Holdings, Inc.", "o4": "Lowell & Achebe PLLC",
        "o5": "H&G Sloane Properties, L.L.C.", "o6": "First Gallatin Bank & Trust",
        "o7": "Estate of Wade R. Abernathy"},
  distractors=["Section 338(h)(10)", "Form 8594", "IRC § 1060", "S corp", "LOI", "Tues."],
  ok=["2023-2025"],
  body=r'''
MEETING NOTES -- PRIVILEGED & CONFIDENTIAL / ATTORNEY WORK PRODUCT
[[Ibarra Kettleman LLP|o1:full]]                      Matter No. [[2026-0417-CORP|rec:matter number]]
Date: [[9/22/2026|date:meeting date]] (Tues.), 10:00-11:35 a.m., our [[Bozeman|place:city]] office
Present: [[Hunter Abernathy-Sloane|p1:full]] (client); [[Georgia Sloane|p2:full]] (spouse, by phone,
first 20 min only); [[Soledad Ibarra|p3:full]] ([[SI|p3:initials]]); [[Billy Tran|p4:nickname:nickname + surname]], paralegal (notes)

1. Background
[[Hunter|p1:first-name!:first name that is also a common word]] owns 70% of [[Three Forks Millwork & Cabinet Co.|o2:full]] ("[[Three Forks|o2:short!:short name that is also a town]]" or "[[TFM|o2:acronym]]"), a
[[Montana|place:state]] S corp, EIN [[81-4472093|taxid:EIN]]. The other 30% sits in the [[Estate of Wade R. Abernathy|o7:full]] --
[[Hunter's older brother|indirect!:family relationship to a named person]], who died [[02/11/2025|date:date of death]]. [[Wade|p5:first-name]]'s widow, [[Marisol Abernathy|p6:full]], is
personal rep ([[Gallatin County|place:county]] probate, Cause No. [[DP-25-0193|rec:probate cause number]]). Hunter says
[[Marisol|p6:first-name]] "will sign anything if the check clears." SI wants her separately represented
and told him so twice.

Reason for selling, per Hunter (NOT to be shared with buyer): he [[had a stent placed in June|health!:cardiac procedure]]
and his cardiologist wants him off the shop floor. [[Georgia|p2:first-name!:first name that is also a place]] confirmed; she keeps the
books and is ready to be done.

2. The offer
Buyer is [[Ridgeline Building Products Holdings, Inc.|o3:full]] ("[[Ridgeline|o3:short!:short name without corporate suffix]]"), [[Boise|place:city]]. LOI dated
[[August 28, 2026|date:LOI date]]. Headline price [[$6.4 million|money!:rounded in words]]:
   - [[$5,150,000|money]] cash at close
   - [[$750k|money!:k shorthand]] seller note, 6%, five years, subordinated to Ridgeline's senior lender
   - earn-out up to [[$500,000|money]] on 2027 EBITDA
   - working capital peg [[$1.1MM|money!:MM shorthand]]; 10% escrow ([[$640,000|money]]) for 18 months
Structure: stock sale with a Section 338(h)(10) election. Buyer wants a Form 8594-style
allocation schedule anyway (IRC § 1060 by analogy). Target close [[Nov. 30, 2026|date:target closing]].
Code name on all buyer paper is "[[Project Larch|indirect!:deal code name]]".

Buyer's counsel: [[Preston Achebe|p7:full]], Esq., [[Lowell & Achebe PLLC|o4:full]], [[pachebe@lowellachebe.example|email]],
[[208.555.0164|phone:dotted]]. [[Mr. Achebe|p7:title-surname]] has already asked for three years of returns.

3. Real estate
Shop and yard at [[4410 Frontage Road|addr]], [[Belgrade|place:city]], [[MT|place:state abbreviation]] [[59714|zip]] are NOT in the company. Title
is in [[H&G Sloane Properties, L.L.C.|o5:full]] (Hunter and Georgia, 50/50). Ridgeline wants a 10-year
lease at [[$14,500|money]]/mo with an option to buy. Hunter would rather sell the dirt outright.

4. Debt / guaranty
[[First Gallatin Bank & Trust|o6:full]] line of credit, Loan No. [[7700-218845|rec:loan number]], balance about
[[$412,000|money]]. Hunter signed a personal guaranty; Wade did too, so the estate is on the hook.
[[First Gallatin|o6:short!:short name without corporate suffix]] needs for the release: Hunter DOB [[7/4/1963|dob]], SSN [[xxx-xx-5222|ssn!:masked SSN]], MT driver's
license [[0704196341207|govid:driver's license number]]. Payoff wire goes to ABA [[119762284|rtn]], acct [[0048-771-9023|acct]].

5. People issues
[[Dmitri Vasquez-Koval|p8:full]] is [[the only CNC programmer they have|indirect!:unique role]]. Ridgeline will want a
retention agreement. Hunter mentioned, quietly, that [[Dmitri|p8:first-name]] is [[on a TPS work permit|attr!:immigration status]]
that runs out [[3/2027|date!:month/year only]]. SI: do not volunteer, do not conceal; goes in the disclosure
schedule if asked. Hunter wants Dmitri to get [[$38,000|money]] out of proceeds as a thank-you.

6. Data room
Ridgeline opened one at [[https://dataroom.ridgelinebp.example/project-larch|url]]. Hunter's login is
[[hsloane_tfm|cred:username]], temp password [[Larch!2026#mw|cred!:password in notes]] (told him to change it today).

To do
- SI: engagement letter + conflict waiver re estate; call Mr. Achebe re exclusivity (45 days?)
- [[Billy|p4:nickname]]: order UCC and lien searches; calendar LOI expiry
- Hunter: send 2023-2025 returns and the equipment list. Cell [[(406) 555-0119|phone]],
  [[hunter@threeforksmillwork.example|email]]
'''))

# ---------------------------------------------------------------- 83
DOCS.append(D(83, "txt", "conflict check note", "legal", "US", length="short",
  title="Conflict check request - prospective elder client",
  ents={"p1": "Yusuf Al-Rashid", "p2": "Cheryl Dunphy", "p3": "Omar Al-Rashid",
        "p4": "Joanne M. Kessler", "o1": "Lakeshore Senior Living LLC"},
  distractors=["3pm", "POA"],
  body=r'''
Conflicts - pls run before 3pm today.

PNC: [[Yusuf Al-Rashid|p1:full]], [[age 91|age]], [[Dearborn|place:city]].
Adverse: [[Lakeshore Senior Living LLC|o1:full]] + its administrator, [[Cheryl Dunphy|p2:full]].
Also run [[grandson|indirect!:family relationship to a named person]] [[Omar Al-Rashid|p3:full]] (holds POA).

We repped [[Lakeshore|o1:short!:short name without corporate suffix]] in 2019, file [[19-0332|rec:file number]]. Screen needed?
[[Yusuf|p1:first-name]]'s daughter can be reached at [[313-555-0188|phone]].

- [[JMK|p4:initials]]
'''))

# ---------------------------------------------------------------- 84
DOCS.append(D(84, "docx", "will draft", "legal", "US",
  title="Last will and testament - working draft with drafter notes",
  ents={"p1": "Eugenia Rose Vantongeren", "p2": "Pieter J. Vantongeren Sr.",
        "p3": "Pieter J. Vantongeren Jr.", "p4": "Grace Vantongeren-Liu",
        "p5": "Hendrik de Groot", "p6": "Tyler Vantongeren", "p7": "Annelise Liu",
        "p8": "Marguerite Oyelaran",
        "o1": "Oyelaran & Brink, P.L.C.", "o2": "Third Reformed Church of Holland",
        "o3": "Macatawa Shores Credit Union", "o4": "Tulip City Wealth Advisors",
        "o5": "Annelise Liu Supplemental Needs Trust"},
  distractors=["MCL 700.2502", "Article III", "Form SS-4", "Personal Representative", "Buick"],
  body=r'''
# LAST WILL AND TESTAMENT OF [[EUGENIA ROSE VANTONGEREN|p1:caps]]
**DRAFT 3 - for client review. Not for execution.** File no. [[EP-2026-0288|rec:file number]]
I, [[Eugenia Rose Vantongeren|p1:full]], of [[2284 Lakeshore Drive|addr]], [[Saugatuck|place:city]], [[Allegan County|place:county]], [[Michigan|place:state]], [[being ninety-one (91) years of age|age!:age spelled out]] and of sound mind, declare this to be my Last Will and revoke all earlier wills and codicils.
## Article I - Family
I am the widow of [[Pieter J. Vantongeren Sr.|p2:full]], who died on [[January 9, 2018|date:date of death]]. I have two children: my son, [[Pieter J. Vantongeren Jr.|p3:full]] ("[[Piet|p3:nickname]]"), and my daughter, [[Grace Vantongeren-Liu|p4:full]]. References to "my children" mean Piet and [[Grace|p4:first-name!:first name that is also a common word]] only.
## Article II - Specific gifts
- To Piet: my 2019 Buick Enclave, VIN [[5GAEVAKW3KJ104482|veh:VIN]], Michigan plate [[DWK 4471|veh:license plate]], and his father's tools.
- To Grace: the cottage known as "[[Zeewind|indirect!:named property]]" at 2284 Lakeshore Drive, together with its furnishings, and the sloop [[Tulip Time|indirect!:named boat]] (hull no. [[MSQ41877H596|veh:hull identification number]]).
- To [[Third Reformed Church of Holland|o2:full|reveals religious affiliation]], [[of which I have been a member for sixty years|attr!:religious affiliation]], the sum of [[twenty-five thousand dollars|money!:amount in words]] ([[$25,000|money]]).
- To my nephew, [[Hendrik de Groot|p5:full]] ("[[Henk|p5:nickname]]"), [[$10,000|money]].
## Article III - Residue
I give the rest of my estate in equal shares to Piet and Grace. If either does not survive me by 120 hours (see MCL 700.2502 as to formalities; survivorship per statute), that share passes to his or her descendants, except as stated in Article IV.
## Article IV - Exclusion and special provision
I intentionally make no provision for my grandson [[Tyler Vantongeren|p6:full]], for reasons known to him, including [[his 2021 conviction for embezzlement|attr!:criminal history]]. Any share that would pass to [[Tyler|p6:first-name]] passes instead as if he had predeceased me.
Any share passing to [[my great-granddaughter|indirect!:family relationship to a named person]] [[Annelise Liu|p7:full]], [[who has Down syndrome|health!:diagnosis]], shall be held in the [[Annelise Liu Supplemental Needs Trust|o5:full]] so that it does not affect her eligibility for public benefits. Grace is trustee.
## Article V - Personal Representative
I nominate Grace as Personal Representative, to serve without bond. If she cannot serve, I nominate [[Mr. de Groot|p5:title-surname]].
**DRAFTER NOTES (delete before signing)**
- Client DOB [[the 3rd day of October, 1934|dob!:birth date in words]]. SSN for the trust's Form SS-4: [[108 49 6520|ssn!:SSN with spaces]].
- Accounts to retitle: [[Macatawa Shores Credit Union|o3:full]] savings ending [[4418|acct!:last four only]] (about [[$212,400|money]]); [[Tulip City Wealth Advisors|o4:full]] account no. [[TCW-883-20417|acct:brokerage account number]] (about [[$1.3 million|money!:rounded in words]]).
- Capacity: [[Mrs. Vantongeren|p1:title-surname]] was sharp at the [[10/14/2026|date:meeting date]] meeting; [[mild hearing loss|health!:condition]] only. Get the physician letter anyway given the Tyler exclusion.
- Signing set for [[November 6, 2026|date:signing date]] at our office. Two disinterested witnesses; not [[Henk|p5:nickname]].
Prepared by [[Marguerite Oyelaran|p8:full]] ([[P71443|govid:state bar number]]), [[Oyelaran & Brink, P.L.C.|o1:full]], [[88 West 9th Street, Suite 3B|addr]], [[Holland|place:city]], [[MI|place:state abbreviation]] [[49423|zip]]. Tel. [[616 555 0131|phone:spaces]]. [[moyelaran@oyelaranbrink.example|email]]
'''))

# ---------------------------------------------------------------- 85
DOCS.append(D(85, "eml", "email to opposing counsel", "legal", "US", enc="qp",
  title="Meet-and-confer email on discovery deficiencies",
  ents={"p1": "Tobias Lindqvist", "p2": "Renata Castellanos-Webb", "p3": "Ifeoma Okafor",
        "p4": "Gordon Pruitt", "p5": "Nadia Haddad",
        "o1": "Okafor Family Trust", "o2": "Meridian Coastal Title & Escrow Co.",
        "o3": "Lindqvist Marsh LLP", "o4": "Castellanos-Webb & Stern, P.C.",
        "o5": "Seabright Community Bank"},
  distractors=["Code Civ. Proc. § 2031.310", "RFP No. 14", "Rule 3.1345", "Bates"],
  ok=["030 through 2", "MCT-000412 through MCT-000498"],
  headers={
    "From": "[[Tobias Lindqvist|p1:full]] <[[tlindqvist@lindqvistmarsh.example|email]]>",
    "To": '"[[Castellanos-Webb, Renata|p2:last-first]]" <[[rcw@cwstern-law.example|email]]>',
    "Cc": "[[Nadia Haddad|p5:full]] <[[nhaddad@lindqvistmarsh.example|email]]>",
    "Subject": "[[Okafor Family Trust|o1:full]] v. [[Meridian Coastal Title|o2:short!:short name without corporate suffix]] - No. [[24-CV-018832|rec:case number]] - meet and confer re RFP Set Two",
    "Date": "Thu, [[15 Oct 2026|date:email date]] 16:42:07 -0700"},
  body=r'''
[[Renata|p2:first-name]],

Following up on our call Tuesday. I am writing under Code Civ. Proc. § 2031.310 before we
file anything, and I'd much rather not file anything.

Your client's responses to the Trust's second set of document requests, served [[September 18, 2026|date:service date]],
are deficient in three respects:

1. RFP No. 14 (wire authorization records). [[Meridian Coastal Title & Escrow Co.|o2:full]] produced the
outgoing wire confirmation for the [[$487,250.00|money]] disbursement on [[June 3, 2025|date:wire date]] but not the
authorization log. We know from [[Seabright Community Bank|o5:full]]'s subpoena response that the wire went to
an account ending in [[7617|acct!:last four only]] at a bank in Ireland (IBAN [[IE08 AIBK 3848 4972 3876 17|iban]]) that
has nothing to do with my client. Somebody at [[Meridian|o2:short!:short name without corporate suffix]] approved the changed instructions. We are
entitled to know who and from where.

2. RFP No. 17 (login records). The escrow platform logs you produced (Bates MCT-000412 through
MCT-000498) stop on [[May 30|date!:date without year]]. The changed wire instructions were uploaded [[June 2|date!:date without year]]. Please produce the
logs for [[June 1-4, 2025|date:date range]], including source IPs. For what it's worth, [[Seabright|o5:short!:short name without corporate suffix]]'s records show
the confirming email was opened from [[203.0.113.47|ip]] and again from [[2001:db8:4c2::1f|ip:IPv6]], neither of
which is a Meridian office as far as we can tell. Your escrow officer [[Gordon Pruitt|p4:full]] testified he
was "working from home that week"; [[Mr. Pruitt|p4:title-surname]]'s home connection should be easy to rule in or out.

3. Privilege log. There isn't one. Forty-one documents were withheld.

On your side: you asked for the trustee's deposition. [[Ifeoma Okafor|p3:full]] is available [[November 10|date!:date without year]] or
[[12|date!:bare day of month continuing a date]], at our office. Please note [[Ms. Okafor|p3:title-surname]] [[observes Friday prayers|attr!:religious practice]] and cannot do the 13th.
She will need breaks; [[she is recovering from chemotherapy|health!:cancer treatment]] and I will hold you to
seven hours over two days if needed.

If I don't have supplemental responses and a log by [[October 29, 2026|date:response deadline]], I will file the motion
with a separate statement under Rule 3.1345 and ask for [[$2,850|money]] in sanctions, which is what
this has cost the Trust so far. I have also uploaded our own supplemental production to
[[https://share.lindqvistmarsh.example/s/okafor-meridian-prod04|url]] (password by separate email).

Call me. I'm in tomorrow until 3.

[[Tobias|p1:first-name]]

Tobias Lindqvist | [[Lindqvist Marsh LLP|o3:full]]
State Bar No. [[284471|govid:state bar number]]
[[1900 Soquel Avenue, Suite 410|addr]], [[Santa Cruz|place:city]], [[CA|place:state abbreviation]] [[95062|zip]]
Direct [[(831) 555-0172 ext. 214|phone!:with extension]] | Fax [[831-555-0109|phone:fax]]

This message may contain privileged information. If you received it in error, delete it
and let me know.

> On [[Oct 13, 2026|date:quoted message date]], at 9:05 AM, [[Renata Castellanos-Webb|p2:full]] wrote:
> [[Toby|p1:nickname]] - can we talk at 2? [[Castellanos-Webb & Stern, P.C.|o4:full]] is closed Monday so I am buried.
> I'll have [[Pruitt|p4:surname]]'s calendar by then. - [[RCW|p2:initials]]
'''))

# ---------------------------------------------------------------- 86
DOCS.append(D(86, "txt", "immigration consultation notes", "legal", "CA",
  title="Immigration consultation notes - permanent residence options",
  ents={"p1": "Oluwaseun Adebayo-Clarke", "p2": "Harpreet Dhillon-Marchetti",
        "p3": "Chidinma Adebayo-Clarke", "p4": "Lorne Pasternak",
        "o1": "Prairie Sky Agri-Tech Ltd.", "o2": "Northern Lights Immigration Consulting Inc.",
        "o3": "University of Regina"},
  distractors=["IMM 5669", "NOC 21232", "CLB 9", "Express Entry", "IRPA s. 40", "CRS 471", "SINP"],
  ok=["471"],
  body=r'''
[[Northern Lights Immigration Consulting Inc.|o2:full]]
CONSULTATION NOTES (paid initial, 60 min)                 File: [[NL-26-1187|rec:file number]]

Consultant: [[Harpreet Dhillon-Marchetti|p2:full]], RCIC [[R712904|govid:RCIC licence number]]
Date: [[2026-10-07|date:consultation date]]     In person, [[Saskatoon|place:city]] office

CLIENT
Name:      [[ADEBAYO-CLARKE, Oluwaseun|p1:last-first]]  (goes by "[[Seun|p1:nickname]]")
DOB:       [[1994-06-02|dob:ISO format]]
Status:    [[Nigerian citizen|attr!:citizenship]]; [[post-graduation work permit|attr!:immigration status]], expires [[2027-01-18|date:permit expiry]]
Passport:  [[A09471126|govid:passport number]] (exp. [[14 FEB 2029|date:passport expiry]])
UCI:       [[11-0447-2913|govid:immigration client identifier]]
SIN:       [[326 357 266|taxid:SIN with spaces]]
Address:   [[Unit 12 - 815 Kristjanson Road|addr:unit-prefixed address]], Saskatoon [[SK|place:province abbreviation]]  [[S7S 1M9|zip:Canadian postal code]]
Phone:     [[306.555.0156|phone:dotted]]      Email: [[seun.adebayoclarke@mailbox.example|email]]
Spouse:    [[Chidinma Adebayo-Clarke|p3:full]], open work permit, [[expecting their first child in February|health!:pregnancy]]

WORK / EDUCATION
M.Sc. Computer Science, [[University of Regina|o3:full]], conferred [[June 2024|date!:month and year only]]. Since [[August 12, 2024|date:hire date]]
full-time software developer (NOC 21232) at [[Prairie Sky Agri-Tech Ltd.|o1:full]], salary [[$84,000|money]].
Supervisor [[Lorne Pasternak|p4:full]] will sign the reference letter. [[Prairie Sky|o1:short!:short name without corporate suffix]] has about 30 staff
and has never supported a PR application before.

ISSUES RAISED
1. Express Entry profile: he self-calculated CRS 471. I get the same with CLB 9 across the
   board. Recent CEC draws have been higher, so we also look at SINP.
2. Prior refusal. [[Seun|p1:nickname]] [[was refused a US visitor visa in 2019|attr!:prior visa refusal]] and did not list it on his
   study permit application. I explained IRPA s. 40 (misrepresentation) plainly. We disclose
   now, with an explanation letter, on IMM 5669 and everywhere else.
3. He asked whether it matters that [[his brother claimed asylum in the UK|attr!:relative's asylum claim]]. Told him it
   is not his claim, but he must answer family questions truthfully.
4. [[Chidinma|p3:first-name]]'s permit is tied to his; both expire the same day.

FEES
Consult fee [[$250.00|money]] + GST paid by Visa [[4379 7518 8853 5872|card:card with spaces]], exp [[09/28|exp]], CVV [[614|cvv]] (taken by
phone at booking -- front desk please do NOT leave this on the file copy).
Quoted flat fee for full PR application: [[C$4,800|money!:Canadian dollar prefix]] in three instalments.

NEXT
- [[Mr. Adebayo-Clarke|p1:title-surname]] to send pay stubs, T4, passport scans (all pages)
- I draft the explanation letter by the 21st
- Retainer agreement out by e-sign

[[H. Dhillon-Marchetti|p2:short:initial + surname]]
'''))

from corpus_src.e_p2 import DOCS as _P2
DOCS += _P2
from corpus_src.e_p3 import DOCS as _P3
DOCS += _P3
