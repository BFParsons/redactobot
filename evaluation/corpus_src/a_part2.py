"""Batch A, documents 5-8 (imported by batch_a.py)."""
from corpus_src.dsl import D, dt, amt, num

DOCS = []

# ---------------------------------------------------------------- doc 5
DOCS.append(D(5, "eml", "email thread", "legal", "US", enc="qp",
  title="Email thread - attorney and client, EEOC charge and retainer",
  ents={"p1": "Xiomara Fuentes", "p2": "Hunter Abernathy-Lowe", "p3": "Leon Brathwaite", "p4": "Dang Van Minh",
        "p5": "Brandi Kowalski", "p6": "Paula Okoye-Wright", "p7": "Terrence Lowe",
        "o1": "Fuentes Labor & Employment, PLLC", "o2": "Sweetgrass Bakery & Cafe LLC"},
  distractors=["Title VII", "Form I-9", "29 C.F.R. § 1601.12", "EEOC", "December", "Visa"],
  headers={
    "From": '"[[Fuentes, Xiomara|p1:last-first]]" <[[xfuentes@fuenteslabor.example|email]]>',
    "To": "[[Hunter Abernathy-Lowe|p2:full]] <[[hunter@sweetgrassbakery.example|email]]>",
    "Cc": "[[Leon Brathwaite|p3:full]] <[[lbrathwaite@fuenteslabor.example|email]]>",
    "Subject": "RE: Retainer + the [[Dang|p4:surname!:surname that is also a common word]] charge (EEOC No. [[846-2026-01193|rec:EEOC charge number]])",
    "Date": "Wed, [[04 Mar 2026|date:email header date]] 16:52:10 -0600"},
  body=r'''
[[Hunter|p2:first-name!:first name that is also a common word]],

Thanks -- received. Two housekeeping points before the substance:

1. Please don't send card numbers by email again. I have deleted your message from our mail server, and Leon ran the card ending [[4237|card!:last four only]] for the [[$3,500|money]] retainer this afternoon (receipt no. [[R-118204|rec:receipt number]]). Next time use the payment page inside the portal.

2. Change the portal password you mentioned today, and anywhere else you use it.

Now the charge. The charging party, [[Dang Van Minh|p4:full:family name first]] (you call him "[[Minh|p4:first-name!:given name only, Vietnamese name order]]"; the EEOC paperwork has him as "[[Mr. Dang|p4:title-surname]]"), alleges national-origin discrimination and retaliation under Title VII. He says he was fired eleven days after he complained that your shift lead told him to "speak English in my kitchen." He identifies as [[Vietnamese|attr:ethnicity / national origin]] and says he is the [[only Asian employee on the morning shift|indirect!:unique role within a small workplace]]. The timing is the problem, not the merits, and the comp claim makes the timing worse, not better. Do not talk to [[Brandi|p5:first-name]] or anyone else on staff about why he was let go.

Our position statement is due [[March 27, 2026|date:filing deadline]]. The investigator is [[Paula Okoye-Wright|p6:full]] in the [[Dallas|place:city]] District Office, [[(972) 555-0181|phone]]; all contact with her goes through me. See 29 C.F.R. § 1601.12 if you want to read what a charge has to contain.

What I need from you by Monday:
  - his complete personnel file, including the Form I-9 and any write-ups
  - timecards and schedules, October through his last day
  - the December no-show texts, as screenshots showing the date and his number
  - names of everyone who was in the kitchen on [[January 5|date!:month and day only]]

On your last question (the dishwashers): call me, don't write. [[214.555.0150|phone:dotted]] is my direct line.

[[Xiomara|p1:first-name]]

[[Xiomara Fuentes|p1:full]] | [[Fuentes Labor & Employment, PLLC|o1:full]]
[[500 N. Akard St., Ste. 1810|addr:street with suite]], Dallas, [[TX|place:state abbreviation]] [[75201|zip]]
State Bar of [[Texas|place:state]] No. [[24081177|govid:state bar number]]
CONFIDENTIAL ATTORNEY-CLIENT COMMUNICATION. If you received this in error, delete it.

> On Wed, [[Mar 4, 2026|date:abbreviated month]] at 11:07 AM Hunter Abernathy-Lowe <hunter@sweetgrassbakery.example> wrote:
>
> Xiomara - here's the card for the retainer. Visa [[4429 4695 1655 4237|card:card number with spaces]] exp [[08/28|exp]] cvv [[614|cvv]],
> billing zip [[75206|zip]]. Name on the card is my husband's, [[Terrence Lowe|p7:full]].
>
> I logged into the portal like Leon said (user [[hunter.al|cred:portal username]], password [[Sweetgrass#2019|cred!:password in an email]] - I know,
> I'll change it).
>
> Minh's last day was [[1/16|date!:month/day only]]. He'd been with us since [[Aug 2021|date!:month and year of hire]], most recently at [[$19.75|money:hourly rate]]/hr.
> Honestly the timing looks bad, but he no-showed three times in December and I have the texts.
> He also filed a comp claim for the [[oven burn on his forearm|health!:workplace injury]] (claim # [[WC-TX-25-338104|rec:workers' compensation claim number]]) back in
> November, and Brandi thinks that's what this is really about.
>
> Also - is it a problem that I pay two of the dishwashers in cash? One of them [[doesn't have papers|attr!:immigration status, colloquial]].
>
> Hunter
> [[Sweetgrass Bakery & Cafe LLC|o2:full]], [[2214 Greenville Ave|addr]], Dallas. [[469-555-0125|phone]]
>
>> On Tue, [[Mar 3, 2026|date:abbreviated month]] at 5:31 PM Xiomara Fuentes <xfuentes@fuenteslabor.example> wrote:
>>
>> Hunter, good talking today. The retainer is $3,500. [[Leon|p3:first-name]] (my paralegal, cc'd) will set you up
>> on the client portal: [[https://clients.fuenteslabor.example/login|url]]
>> [[XF|p1:initials]]
'''))

# ---------------------------------------------------------------- doc 6
DOCS.append(D(6, "txt", "demand letter", "legal", "CA",
  title="Demand letter - unpaid millwork invoices (Ontario)",
  ents={"p1": "Harpreet K. Sandhu", "p2": "Giancarlo De Luca", "p3": "Mei-Ling Cho", "p4": "Étienne Beaulieu",
        "p5": "Wojciech Nowakowski",
        "o1": "Beaulieu Sandhu LLP", "o2": "Trillium Millwork & Cabinetry Ltd.", "o3": "Lakeshore Custom Homes Inc.",
        "o4": "Halton Community Credit Union"},
  distractors=["Construction Act, R.S.O. 1990, c. C.30", "section 31", "Rule 49", "HST", "Courts of Justice Act", "Superior Court of Justice"],
  body=r'''
[[BEAULIEU SANDHU LLP|o1:caps]]
Barristers & Solicitors
[[150 King Street West, Suite 2710|addr:street with suite]]
[[Toronto|place:city]], [[ON|place!:province abbreviation]]  [[M5H 1J9|zip:Canadian postal code]]
T [[416-555-0138|phone]]   F [[416-555-0139|phone:fax]]

[[Harpreet K. Sandhu|p1:full]]
Direct: [[416-555-0141|phone]]
[[hsandhu@beaulieusandhu.example|email]]

[[March 2, 2026|date:letter date]]

WITHOUT PREJUDICE
DELIVERED BY COURIER AND EMAIL ([[gdeluca@lakeshorecustomhomes.example|email]])

[[Lakeshore Custom Homes Inc.|o3:full]]
Attention: [[Mr. Giancarlo De Luca|p2:full:title + full name]], President
[[2380 Speers Road, Unit 14|addr:street with unit]]
[[Oakville|place:city]], [[Ontario|place:province]]  [[L6L 5M2|zip:Canadian postal code]]

Dear [[Mr. De Luca|p2:title-surname]]:

Re:  [[Trillium Millwork & Cabinetry Ltd.|o2:full]] -- unpaid invoices
     [[48 Birchview Crescent|addr]], Oakville (the "[[Cho|p3:surname!]] residence")
     Our file no. [[26-0193/HKS|rec!:file number with lawyer initials]]

We are the lawyers for Trillium Millwork & Cabinetry Ltd. ("[[Trillium|o2:short!:one-word short name]]").

Under a subcontract dated [[2025-06-18|date:ISO format]], Trillium supplied and installed custom
kitchen, pantry and library millwork at the home of [[Dr. Mei-Ling Cho|p3:full:title + full name]], for which
[[Lakeshore|o3:short!:one-word short name that reads like a place]] is the general contractor. Trillium's last day on site was
[[January 23, 2026|date:last supply date]]. [[Dr. Cho|p3:title-surname]] moved in the following week and, so far as we are aware,
has raised no deficiencies.

The following invoices remain unpaid:

    Invoice     Date            Amount (incl. HST)
    [[TM-4471|rec:invoice number]]     [[Nov. 28, 2025|date:abbreviated month]]   [[$41,810.00|money]]
    [[TM-4502|rec:invoice number]]     [[Dec. 19, 2025|date:abbreviated month]]   [[$27,345.50|money]]
    [[TM-4533|rec:invoice number]]     [[Jan. 30, 2026|date:abbreviated month]]   [[$18,960.75|money]]
                                Total     [[C$88,116.25|money!:Canadian dollar prefix]]

Trillium's HST registration number, [[84127 9036 RT0001|taxid:Canadian business number with program account]], appears on each invoice. You have
not disputed any of them. On [[February 9|date!:month and day only]] you told Trillium's controller, [[Wojciech Nowakowski|p5:full]],
that payment was "waiting on the last draw." On [[February 20|date!:month and day only]] your cheque no. 01187 for
[[$25,000|money]] was returned NSF. [[Mr. Nowakowski|p5:title-surname]]'s messages since then have gone unanswered.

DEMAND

Trillium requires payment of C$88,116.25, plus interest at the contract rate of 18% per
year from each due date ([[$2,291.44|money]] to today) and [[$45.00|money]] in NSF charges, for a total of
[[$90,452.69|money]], by 5:00 p.m. on [[Thursday, March 12, 2026|date!:date with weekday]].

Payment may be made by certified cheque payable to "[[Beaulieu Sandhu LLP|o1:full]], in trust", or by
wire to our trust account:

    [[Halton Community Credit Union|o4:full]]
    Transit / institution: [[00412-828|rtn!:Canadian transit and institution number]]
    Account: [[1047882|acct:trust account number]]
    Reference: 26-0193/HKS

If payment is not received by that time, our instructions are to preserve and perfect
Trillium's lien against the Cho residence under section 31 of the Construction Act,
R.S.O. 1990, c. C.30, and to start an action in the Superior Court of Justice against
Lakeshore and against you personally on the guarantee you signed on [[June 18, 2025|date]]. In
that case Trillium will also seek its costs and prejudgment interest under the Courts of
Justice Act. Please note that a lien will name Dr. Cho as owner; we expect you would
prefer to avoid that conversation with your client.

This letter is an offer to settle within the meaning of Rule 49. It is not a waiver of
any of Trillium's rights, all of which are reserved.

Govern yourself accordingly.

Yours very truly,
BEAULIEU SANDHU LLP

Harpreet K. Sandhu
LSO No. [[71842P|govid:law society number]]

c.  client ([[W. Nowakowski|p5:short:initial + surname]], [[wojciech@trilliummillwork.example|email]])
    [[É. Beaulieu|p4:short!:initial + surname, accented]]
'''))

# ---------------------------------------------------------------- doc 7
DOCS.append(D(7, "html", "solicitor attendance note", "legal", "UK",
  title="Attendance note - employment tribunal client (England)",
  ents={"p1": "Folasade Adeyemi-Clarke", "p2": "Rupert Pemberton", "p3": "Gareth Whitcombe", "p4": "Imran Qureshi",
        "p5": "Niamh Gallagher", "p6": "Desmond Clarke",
        "o1": "Pemberton Ashby Solicitors LLP", "o2": "Northgate Logistics (UK) Ltd", "o3": "Aire Valley Legal Protection plc",
        "o4": "Yorkshire Dales Building Society"},
  distractors=["Equality Act 2010", "section 20", "ACAS", "ET1", "Employment Rights Act 1996", "VAT", "Friday"],
  body=r'''
# [[Pemberton Ashby Solicitors LLP|o1:full]]
**ATTENDANCE NOTE** (privileged)
| Field | Detail |
| Client | [[Mrs Folasade Adeyemi-Clarke|p1:full:title + full name, UK style without full stop]] |
| Matter | [[ADE0417/0002|rec:client-matter number]] |
| Fee earner | [[RJP|p2:initials]] |
| Date | [[3 February 2026|date:UK day-month-year]] |
| Attendance | In person, 55 minutes |
| Opponent | [[Northgate Logistics (UK) Ltd|o2:full]] |
## Identity and contact (AML check completed)
| Item | Value |
| Known as | [[Sade|p1:nickname]] |
| Date of birth | [[14 March 1979|dob:UK day-month-year]] |
| NI number | [[JK 47 21 09 C|govid:UK National Insurance number]] |
| Passport | [[533184726|govid!:passport number, digits only]] |
| Driving licence | [[ADEYE753149FA9KL|govid:UK driving licence number]] |
| Address | [[27 Cardigan Lane|addr]] |
| Area | [[Headingley|place:neighbourhood]], [[Leeds|place:city]] |
| Postcode | [[LS6 3BJ|zip:UK postcode]] |
| Mobile | [[07700 900143|phone:UK mobile]] |
| Email | [[sade.ac@postbox.example|email]] |
## Background
[[Mrs Adeyemi-Clarke|p1:title-surname]] worked for [[Northgate|o2:short!:one-word short name]] as a transport planner at its [[Stourton|place:district]] depot from [[1 September 2017|date:employment start]] until she was dismissed on [[19 December 2025|date:dismissal date]]. Her salary was [[£31,200|money:pounds]] a year. She was diagnosed with [[relapsing-remitting multiple sclerosis|health:diagnosis]] in 2023 and told her line manager, [[Gareth Whitcombe|p3:full]], at the time. Occupational health recommended a later start and two home-working days; these were in place until [[Mr Whitcombe|p3:title-surname]] withdrew them in September "for operational reasons".
She raised a grievance on [[06/10/2025|date!:UK numeric date, day first]]. It was heard by the depot manager, [[Imran Qureshi|p4:full]], and rejected. She was then put on a performance plan and dismissed for capability eleven weeks later. She is a [[union member|attr:union membership]] and her [[branch rep|indirect!:role that identifies a third person]] attended both meetings; [[Sade|p1:nickname]] says the rep's notes record [[Whitcombe|p3:surname!]] saying "we can't carry people". She also mentioned, hesitantly, that she had asked to swap her Friday late shift so she could [[attend Jumu'ah prayers|attr!:implies religion]] and was refused; I do not think that is a separate claim, but it is relevant background.
She had [[two relapses|health!:health detail]] in the autumn and is currently on [[ocrelizumab infusions|health:medication]] every six months. She has been [[signed off with anxiety|health!:mental health detail]] since January. Her husband, [[Desmond|p6:first-name]], is the only earner at present.
## Advice given
- Claims: unfair dismissal (Employment Rights Act 1996), failure to make reasonable adjustments (section 20, Equality Act 2010) and discrimination arising from disability.
- Time limit: ACAS early conciliation must start by [[18 March 2026|date:limitation date]]. Certificate ref will be needed for the ET1.
- Prospects: reasonable to good on adjustments; I put overall prospects at about 60%.
- Likely value: basic award about [[£5,400|money]]; compensatory award and injury to feelings together in the range [[£18,000|money]] to [[£27,000|money]].
## Funding
She has legal expenses cover with her home insurance through [[Aire Valley Legal Protection plc|o3:full]], policy [[HH/7741093/LP|rec:insurance policy number]]. I will ask [[Aire Valley|o3:short!:short name that reads like a place]] to confirm cover and my appointment. Until then we act on a fixed fee of [[£450|money]] plus VAT for the ACAS stage, which she paid today by debit card ending [[9130|card!:last four only]].
Any refund or damages to be paid to her joint account at [[Yorkshire Dales Building Society|o4:full]]: sort code [[40-47-21|rtn!:UK sort code]], account [[41906532|acct]], IBAN [[GB39 NWBK 3875 8627 1563 32|iban:IBAN with spaces]].
## Actions
- [[RJP|p2:initials]] to send client care letter and notify ACAS this week.
- [[Niamh Gallagher|p5:full]] (trainee) to request the personnel file and occupational health reports by subject access request.
- Client to send payslips, the dismissal letter and her diary of the autumn meetings.
- Diary: review [[17/02/2026|date!:UK numeric date, day first]].
Time recorded: 9 units. [[Rupert Pemberton|p2:full]], Partner. Direct line [[0113 496 0127|phone:UK landline]].
'''))

# ---------------------------------------------------------------- doc 8
DOCS.append(D(8, "txt", "tax organizer worksheet", "accounting", "US",
  title="Individual tax organizer worksheet",
  ents={"p1": "Adebayo T. Oyelaran", "p2": "Chiamaka Oyelaran", "p3": "Soo-Ah Yoo", "p4": "Tobi Oyelaran",
        "p5": "Folake Oyelaran", "p6": "Abiodun Oyelaran", "p7": "Marguerite Dunleavy",
        "o1": "Pellegrino & Yoo, CPAs", "o2": "Lakeview Compounding Pharmacy, Inc.", "o3": "Fox Prairie School District 88",
        "o4": "Prairie State Bank & Trust", "o5": "Harborstone Securities", "o6": "Midland Prairie Mortgage Co.",
        "o7": "Redeemed Life Assembly", "o8": "Little Sprouts Montessori", "o9": "Naperville Central Band Boosters"},
  distractors=["Form W-2", "Form 1099-INT", "Schedule A", "Form 8889", "Letter 5071C", "Form 1098", "Form 2441", "Box 1", "April 15"],
  ok=["2024 2025"],
  body=r'''
2025 INDIVIDUAL TAX ORGANIZER                         [[Pellegrino & Yoo, CPAs|o1:full]]
Client no. [[10-4418|rec:client number]]                                    Preparer: [[S. Yoo|p3:short:initial + surname]]
Returned by client [[2/21/2026|date:numeric date]] (handwritten answers typed up by front desk)

PART 1 -- TAXPAYER INFORMATION
Taxpayer:  [[OYELARAN, Adebayo T.|p1:last-first]]      SSN [[239-62-4388|ssn:SSN with dashes]]     DOB [[05/09/1978|dob]]
           Occupation: pharmacist
Spouse:    [[Chiamaka Oyelaran|p2:full]] ("[[Amy|p2:nickname]]")    SSN [[376 39 1788|ssn!:SSN with spaces]]     DOB [[12/30/1980|dob]]
           Occupation: school counselor
Address:   [[9 Quail Hollow Ct|addr]], [[Naperville|place:city]], [[IL|place:state abbreviation]] [[60564-4410|zip:ZIP+4]]     (same as last year: yes)
Phone:     T - [[630-555-0112|phone]]   S - [[630 555 0167|phone!:spaces only]]
Email:     [[bayo.oyelaran@fastmail.example|email]]  (send the e-file forms to [[Amy|p2:nickname]] instead: [[c.oyelaran+taxes@fastmail.example|email:plus addressing]])
IL driver's license (T): [[O460-1257-8132|govid:driver's license number]], issued [[05/09/2022|date:license issue date]], exp. [[05/09/2026|date:license expiry]]
Identity Protection PIN (T): [[418207|cred!:IRS identity protection PIN]]       Spouse: none issued

PART 2 -- DEPENDENTS
Name                    DOB           SSN / ITIN       Relationship    Months in home
[[Tobi Oyelaran|p4:full]]           [[03/14/2012|dob]]    [[146-36-0891|ssn]]      son             12
[[Folake Oyelaran|p5:full]]         [[8/2/2015|dob]]      [[453685862|ssn!:SSN without dashes]]        daughter        12
[[Abiodun Oyelaran|p6:full]]        [[1/4/1935|dob]]      [[947-78-3301|taxid:ITIN]]      [[T's mother|indirect!:family relationship]]      12
  Note from client: "My mother moved in with us in 2024, she is [[91|age!:bare age number]] now and has
  no income. She is [[not a citizen|attr!:citizenship status]] (visiting on a long-stay basis, we pay everything).
  Can we claim her? Last year's preparer said no."

PART 3 -- REFUND / PAYMENT
Direct deposit:  [[Prairie State Bank & Trust|o4:full]]    RTN [[071499792|rtn]]    Acct [[0029 4471 8830|acct!:account number with spaces]]  (checking)
If balance due:  debit same account on April 15.

PART 4 -- INCOME
Form W-2 (T)   [[Lakeview Compounding Pharmacy, Inc.|o2:full]]   EIN [[36-4471902|taxid:EIN]]   Box 1 [[$148,212.40|money]]   Fed w/h [[$27,904.11|money]]
Form W-2 (S)   [[Fox Prairie School District 88|o3:full]]        EIN [[36-6009114|taxid:EIN]]   Box 1 [[$71,338.00|money]]    Fed w/h [[$8,116.52|money]]
Form 1099-INT  Prairie State Bank & Trust                                    [[$412.77|money]]
1099-B / DIV   [[Harborstone Securities|o5:full]], acct [[5XT-208814|acct:brokerage account number]]   dividends [[$2,960.15|money]]; net short-term loss [[(1,844.00)|money!:parenthesized negative, no currency sign]]
Other:         Amy sold handmade jewelry online, "about [[$3k|money!:abbreviated with k]]" gross, no 1099 received. Receipts in shoebox.

PART 5 -- DEDUCTIONS (Schedule A items)
Mortgage interest (Form 1098): [[Midland Prairie Mortgage Co.|o6:full]], loan [[7700218834|rec:loan number]]             [[$14,208.39|money]]
Real estate tax, [[DuPage County|place:county]], PIN [[07-22-304-019|rec:property index number]]                         [[$11,940.22|money]]
Charity:  [[Redeemed Life Assembly|o7:full]] (weekly giving statement attached)               [[$6,240.00|money]]
          [[Naperville Central Band Boosters|o9:full]]                                     [[$350|money]]
Medical:  [[Tobi|p4:first-name]]'s [[insulin pump and CGM supplies|health:medical device and supplies]] -- he has [[type 1 diabetes|health:diagnosis of a minor]], dx 2021.
          Out of pocket after insurance approx. [[$7,150|money]]. Paid from HSA? "Some." (need Form 8889 detail)

PART 6 -- CHILD CARE (Form 2441)
Provider:  [[Little Sprouts Montessori|o8:full]], [[1550 W. Ogden Ave.|addr]], Naperville    EIN [[84-3317206|taxid:EIN]]    Paid [[$4,875|money]] ([[Folake|p5:first-name]], after-school)
Sitter:    [[Marguerite Dunleavy|p7:full]], SSN "she won't give it to us" -- paid [[$2,400|money]] by Zelle to [[630.555.0149|phone:dotted]]

PART 7 -- ESTIMATED PAYMENTS
None federal. [[Illinois|place:state]]: [[$600|money]] on [[6/16/25|date!:numeric date with two-digit year]], [[$600|money]] on [[9/15/25|date!:numeric date with two-digit year]].

PART 8 -- QUESTIONS FOR YOUR PREPARER
- "[[Bayo|p1:nickname]] got an IRS Letter 5071C in January asking him to verify his identity. Do we
  ignore it? He did not file anything yet."
- "We paid [[Mrs. Dunleavy|p7:title-surname]] more than last year. Do we need to give her a form?"
- "Compare 2024 2025 withholding -- why was our refund so much smaller?"

OFFICE USE: organizer complete? N -- missing HSA statement, 1099-B pages 3-6, mother's passport copy.
Assigned: [[SY|p3:initials]].   Target date: [[3/20/2026|date:internal target date]].
'''))
