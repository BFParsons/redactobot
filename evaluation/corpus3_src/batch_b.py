from corpus3_src.core import D, dt, amt, num

DOCS = []

# ---------------------------------------------------------------- 311
DOCS.append(D(311, "txt", "tax organizer call notes", "accounting", "US", minors=["p3", "p4"],
  title="Preparer's hurried notes from a tax organizer phone call",
  ents={"p1": "Dwayne E. Broadnax", "p2": "Tamika R. Broadnax", "p3": "Jaylen Broadnax", "p4": "Amara Broadnax",
        "p5": "Gloria Whitted",
        "o1": "Ardmore Mechanical", "o2": "Pikeview Dental", "o3": "Acorn Hollow Childcare",
        "o4": "Schuylkill Valley FCU", "o5": "Penn Crest Mortgage"},
  distractors=["1099-G", "1099-K", "form 1098", "PA-40", "sched C", "form 2441", "8332"],
  body=r'''
organizer call w/ [[tamika|p2:first-name!:lower case]] [[2/6|date:month/day only]] - TY2025 - mfj - notes not cleaned up

tp: [[dwayne e broadnax|p1:full!:lower case, no punctuation]]  ss [[811-12-4570|ssn]]  dob [[9/14/79|dob:short numeric]]  hvac tech @ [[ardmore mechanical|o1:full!:lower case]] (1 w2)
sp: [[tamika r. broadnax|p2:full!:lower case]]  ss ending [[1861|ssn:last four digits only]] - get full # off last yr  dob [[3-3-81|dob:hyphenated short date]]
    hygienist, 2 w2s - [[pikeview dental|o2:full!:lower case]] til june then the new place in [[media|place!:town name that is a common word, lower case]], she'll send
kids:
  [[jaylen|p3:first-name!:lower case]] - [[11/02/2012|dob]] - ss [[821-99-1511|ssn]] - [[has an IEP, adhd meds|health:child's condition and medication]], copays abt [[$1,340|money]]
  [[amara|p4:first-name!:lower case]] - born [[aug 2019|dob:month and year, lower case]] - ss [[512 96 4302|ssn:SSN with spaces]]
  daycare for amara = [[acorn hollow childcare|o3:full!:lower case]] ein [[23-4471906|taxid:EIN]] pd [[6,240|money!:no currency sign]] (form 2441)
  jaylen is [[dwaynes|p1:first-name!:lower case possessive without apostrophe]] from before - [[his ex claimed him in 2024|indirect:family relationship and prior-year dispute]]??? [[T|p2:initials:single initial]] says they have the 8332 now. GET COPY
[[tamikas|p2:first-name!:lower case possessive without apostrophe]] mom [[gloria whitted|p5:full!:lower case]] moved in w them in nov, [[on SSI|attr:benefits status]], [[had a stroke|health:condition]] - not a dependant this yr, maybe 2026

moved [[aug 15|date:month and day, lower case]]. old adress [[2218 w tioga st|addr:lower case]] [[phila|place!:city abbreviation, lower case]] [[19140|zip]]
new: [[61 Larchmere Ln|addr]], [[Upper Darby|place:town]] [[PA|place:state abbreviation]] [[19082|zip]]
form 1098 from [[penn crest mortgage|o5:full!:lower case]] loan [[0044718820|rec:mortgage loan number]] - int [[9,881.14|money!:no currency sign]], pts pd at closing [[2,150|money!:no currency sign]]

other income
- [[dwayne|p1:first-name!:lower case]] laid off jan-feb, [[collected unemployment|attr:benefits status]], 1099-G shows [[$4,212|money]], no w/h (ugh)
- he also drives rideshare wknds - 1099-K [[3,870.50|money!:no currency sign]] - sched C. 2,140 mi, no log. told her he needs a log
- sold the old truck to his cousin for [[four grand|money:amount in slang words]], no gain

id theft: dwayne recieved IP PIN letter again - pin is [[418207|cred:IRS identity protection PIN]]. T doesnt have one
last yr AGI [[118,402|money!:no currency sign]] (need for efile)
refund -> dd [[schuylkill valley fcu|o4:full!:lower case]]  rtg [[031479969|rtn]]  acct [[4400187725|acct]]  (checking, joint)
PA-40 + local. she thinks they owe local from the move

contact: T cell [[267-555-0126|phone]], dont call [[D|p1:initials:single initial]] at work. email [[tamikab81@quakermail.example|email]]
fee quoted [[425|money!:no currency sign]], she'll zelle it. docs due by [[the 20th|date:day of month only]], appt [[sat 2/28|date:weekday and month/day, lower case]] 9am
'''))

# ---------------------------------------------------------------- 312
DOCS.append(D(312, "xlsx", "payroll register", "accounting", "US",
  title="Biweekly payroll register with deductions, direct deposit and employee master tabs",
  ents={"p1": "Brandon T. Kowalewski", "p2": "Patrice Nguema", "p3": "Maria Elena Delacruz", "p4": "Stig Haugland",
        "p5": "Lila Running Crane", "p6": "Declan O'Shaughnessy",
        "o1": "Tannery Row Fabrication, Inc.", "o2": "Thornapple Community Credit Union", "o3": "Coldbrook Savings Bank",
        "o4": "Payworks Midwest"},
  distractors=["Form 668-W", "FICA", "I-9"],
  sheets=[
    ("Register", [
      ["[[Tannery Row Fabrication, Inc.|o1:full]]", "FEIN", "[[38-4471209|taxid:EIN]]", "Period", dt("2025-10-19", "mm/dd/yy", "date:period start"),
       dt("2025-11-01", "mm/dd/yy", "date:period end"), "Check date", dt("2025-11-07", "mm/dd/yy", "date:check date"), "Processor: [[Payworks Midwest|o4:full]] batch [[PW-881204|rec:payroll batch number]]"],
      ["Emp #", "Employee", "SSN", "Dept", "Rate", "Reg hrs", "OT hrs", "Gross", "Fed W/H", "FICA", "Other ded", "Net", "Method"],
      [num(1042, "rec!:employee number"), "[[Kowalewski, Brandon T.|p1:last-first]]", "[[XXX-XX-8151|ssn:masked SSN]]", "Shop", amt(31.50), 80, 6.5, amt(2827.13), amt(311.20), amt(216.27), amt(184.62), amt(2115.04), "DD"],
      [num(1057, "rec!:employee number"), "[[Nguema, Patrice|p2:last-first]]", "[[XXX-XX-8564|ssn:masked SSN]]", "Shop", amt(29.75), 80, 0, amt(2380.00), amt(238.00), amt(182.07), amt(46.00), amt(1913.93), "DD"],
      [num(1061, "rec!:employee number"), "[[DELACRUZ, MARIA ELENA|p3:last-first:Last, First in ALL CAPS]]", "[[XXX-XX-1967|ssn:masked SSN]]", "Office", amt(26.00), 72, 0, amt(1872.00), amt(149.76), amt(143.21), "", amt(1579.03), "DD"],
      [num(1068, "rec!:employee number"), "[[Haugland, Stig|p4:last-first]]", "[[XXX-XX-4801|ssn:masked SSN]]", "Install", amt(34.10), 80, 12, amt(3341.80), amt(401.02), amt(255.65), "", amt(2685.13), "Check [[20418|rec!:check number]]"],
      [num(1073, "rec!:employee number"), "[[Running Crane, Lila|p5:last-first:Last, First with a two-word surname]]", "[[XXX-XX-3604|ssn:masked SSN]]", "Install", amt(27.40), 64, 0, amt(1753.60), amt(140.29), amt(134.15), amt(310.00), amt(1169.16), "DD"],
      [num(1080, "rec!:employee number"), "[[O'Shaughnessy, Declan|p6:last-first]]", "[[XXX-XX-4335|ssn:masked SSN]]", "Shop", amt(30.25), 80, 4, amt(2601.50), amt(286.17), amt(199.01), amt(425.00), amt(1691.32), "DD"],
      ["TOTAL", "", "", "", "", 456, 22.5, amt(14776.03), amt(1526.44), amt(1130.36), amt(965.62), amt(11153.61), ""],
    ]),
    ("Deductions", [
      ["Emp #", "Employee", "Type", "Order / ref", "Per period", "Payee / note"],
      [1042, "[[B. Kowalewski|p1:short:initial + surname]]", "Child support", "[[2019-DR-004418|rec:support order case number]]", amt(184.62, "usd", None), "[[income withholding order for child support|attr:court-ordered obligation]]; remit to MiSDU"],
      [1057, "[[Patrice|p2:first-name]]", "Union dues", "", amt(46.00, "usd", None), "[[SMART Local 7 member|attr:union membership]]; dues remitted monthly"],
      [1073, "[[Lila R.C.|p5:short:first name + surname initials]]", "Tax levy", "Form 668-W", amt(310.00, "usd", None), "[[IRS wage levy|attr:tax debt]] rec'd [[9/22/25|date:short numeric date]]; exempt amt per her statement"],
      [1080, "[[Declan|p6:first-name]]", "Ch. 13 trustee", "[[25-41187-swd|rec:bankruptcy case number]]", amt(425.00, "usd", None), "[[Chapter 13 wage order|attr:bankruptcy]] eff. [[10/05/2025|date:effective date]]"],
    ]),
    ("Direct deposit", [
      ["Employee", "Bank", "Routing", "Account", "Type", "Split"],
      ["[[Brandon Kowalewski|p1:short:no middle initial]]", "[[Thornapple Community Credit Union|o2:full]]", "[[075474315|rtn]]", "[[7700418852|acct]]", "Chk", "100%"],
      ["[[Patrice Nguema|p2:full]]", "[[Coldbrook Savings Bank|o3:full]]", "[[071157526|rtn]]", "[[30-441-9072|acct:account number with hyphens]]", "Chk", "100%"],
      ["[[Maria Elena Delacruz|p3:full]]", "[[Thornapple CCU|o2:short]]", "075474315", "[[7700526610|acct]]", "Sav", "[[$200.00|money]] flat"],
      ["[[Maria Elena|p3:first-name:two-word given name]]", "Coldbrook Savings Bank", "071157526", "[[30-118-4425|acct:account number with hyphens]]", "Chk", "remainder"],
      ["[[Lila Running Crane|p5:full]]", "[[Coldbrook|o3:short]]", "071157526", "[[****3391|acct:masked account number]]", "Chk", "100%"],
      ["[[D. O'Shaughnessy|p6:short:initial + surname]]", "Thornapple Community Credit Union", "075474315", num(7700631184, "acct:account number stored as a number"), "Chk", "100%"],
    ]),
    ("Master", [
      ["Employee", "SSN", "DOB", "Hire date", "Street", "City", "ST", "ZIP", "Phone", "Notes"],
      ["[[Brandon T. Kowalewski|p1:full]]", "[[894-59-8151|ssn]]", dt("1988-02-17", "mm/dd/yyyy", "dob"), dt("2016-05-02", "mm/dd/yyyy", "date:hire date"), "[[3318 Byron Center Ave SW|addr]]", "[[Wyoming|place!:city that shares its name with a state]]", "[[MI|place:state abbreviation]]", "[[49519|zip]]", "[[616-555-0171|phone]]", ""],
      ["Patrice Nguema", "[[034-79-8564|ssn]]", dt("1979-09-30", "mm/dd/yyyy", "dob"), dt("2021-01-11", "mm/dd/yyyy", "date:hire date"), "[[44 Griggs St SE, Apt 3|addr:street with apartment]]", "[[Grand Rapids|place:city]]", "MI", "[[49507|zip]]", "[[(616) 555-0108|phone]]", "[[green card renewed 2024|attr:immigration status]]; I-9 reverified"],
      ["Maria Elena Delacruz", num(755421967, "ssn:SSN stored as a number"), dt("1994-12-04", "mm/dd/yyyy", "dob"), dt("2023-08-21", "mm/dd/yyyy", "date:hire date"), "[[905 Paris Ave|addr]]", "[[Holland|place!:city that shares its name with a country]]", "MI", "[[49423|zip]]", "[[616.555.0155|phone:dotted]]", "[[maternity leave planned from Jan|health:pregnancy]]"],
      ["[[Stig Haugland|p4:full]]", "[[269-89-4801|ssn]]", dt("1966-06-23", "mm/dd/yyyy", "dob"), dt("2009-03-16", "mm/dd/yyyy", "date:hire date"), "[[7120 Kenowa Ave|addr]]", "[[Walker|place!:city that is also a surname]]", "MI", "[[49534|zip]]", "[[6165550190|phone:no separators]]", "paper check by request"],
      ["Lila Running Crane", "[[451-99-3604|ssn]]", dt("1991-04-08", "mm/dd/yyyy", "dob"), dt("2024-06-03", "mm/dd/yyyy", "date:hire date"), "[[PO Box 418|addr:PO Box]]", "[[Zeeland|place:city]]", "MI", "[[49464|zip]]", "[[616-555-0139|phone]]", "[[enrolled member, Blackfeet Nation|attr:tribal enrollment / ethnicity]]"],
      ["[[Declan O'Shaughnessy|p6:full]]", "[[430-48-4335|ssn]]", dt("1983-11-19", "mm/dd/yyyy", "dob"), dt("2018-10-01", "mm/dd/yyyy", "date:hire date"), "[[2260 Kalamazoo Ave SE|addr]]", "[[Kentwood|place:city]]", "MI", "[[49508|zip]]", "[[616 555 0162|phone:spaces only]]", ""],
    ]),
  ]))

# ---------------------------------------------------------------- 313
DOCS.append(D(313, "pdf", "bank reconciliation memo", "accounting", "US",
  title="Month-end bank reconciliation memo flagging cheques an office manager wrote to herself",
  ents={"p1": "Dr. Annika Ruud", "p2": "Kayleigh Dombek", "p3": "Winston Pell", "p4": "Jolene Marrs",
        "o1": "Quillfeather Animal Hospital, P.C.", "o2": "Mackinaw Straits Bank", "o3": "Pell Bookkeeping Services",
        "o4": "Tamarind Wellness LLC", "o5": "Vetline Supply Co."},
  distractors=["QuickBooks Online", "Positive Pay"],
  body=r'''
# [[Pell Bookkeeping Services|o3:full]]
[[1407 Front Street, Unit B|addr:street with unit]], [[Traverse City|place:city]], [[Michigan|place:state]] [[49686|zip]] · [[231-555-0118|phone]]
**MEMO — PRIVATE. Please do not leave this on the front desk.**
To: [[Dr. Annika Ruud|p1:full]], owner, [[Quillfeather Animal Hospital, P.C.|o1:full]]
From: [[Winston Pell|p3:full]]
Date: [[November 5, 2025|date:memo date]]
Re: [[October 2025|date:month and year]] reconciliation, operating account at [[Mackinaw Straits Bank|o2:full]] ending [[4471|acct:last four of account]] (full no. [[0218 5530 4471|acct:account number with spaces]])
## 1. Summary
- Balance per bank statement at [[10/31/2025|date:statement date]]: [[$48,216.09|money]]
- Add deposits in transit (card batches of [[10/30|date:month/day only]] and [[10/31|date:month/day only]]): [[$3,904.55|money]]
- Less outstanding checks: [[($6,118.40)|money:negative amount in parentheses]]
- Adjusted bank balance: [[$46,002.24|money]]
- Balance per QuickBooks Online: [[$50,327.24|money]]
- **Unreconciled difference: [[$4,325.00|money]]**
## 2. What the difference is
The difference is two checks that cleared the bank but were never entered in the books. I pulled the images.
- Check no. [[5518|rec!:check number]], dated [[Oct. 3|date:abbreviated month and day]], [[$2,350.00|money]], payable to [[Kayleigh Dombek|p2:full]], memo line "reimb. supplies".
- Check no. [[5524|rec!:check number]], dated [[Oct. 17|date:abbreviated month and day]], [[$1,975.00|money]], payable to [[K. Dombek|p2:short:initial + surname]], memo line blank.
Both carry your signature stamp, not a pen signature. There are no receipts in the supplies folder that come close to either amount. As you know, [[Kayleigh|p2:first-name]] is the only person besides you with access to the stamp and the check stock.
I also went back through the year. Checks [[5391|rec!:check number]] ([[$1,200|money]], [[June 6|date:month and day]]) and [[5447|rec!:check number]] ([[$1,640|money]], [[Aug. 22|date:abbreviated month and day]]) follow the same pattern and were coded to "Medical supplies — [[Vetline|o5:short]]" although [[Vetline Supply Co.|o5:full]] has no matching invoices. Total of the four: [[$7,165.00|money]].
## 3. Other items
- ACH debit of [[$1,200.00|money]] on the 15th of each month to [[Tamarind Wellness LLC|o4:full]]. I understand from our call that [[this is your own therapy practice bill|health:owner's therapy]] and should be coded to owner draw, not to the clinic. I have reclassified ten months.
- Outstanding more than 90 days: check [[5302|rec!:check number]] to [[Jolene Marrs|p4:full]] ([[former kennel assistant|indirect:former role at a small employer]]), final pay of [[$412.18|money]]. Her last address on file is [[609 Wadsworth St|addr]], Traverse City. Michigan unclaimed property rules will apply next year.
- Merchant deposits tie to the processor reports. Company debit card ending [[9958|card:last four of card]] is in your name only.
## 4. What I suggest
Please do not confront [[Ms. Dombek|p2:title-surname]] yet. Lock the signature stamp away today, ask the bank about Positive Pay, and call me on my cell, [[231.555.0164|phone:dotted]], before Friday. If you want to involve the police or your insurer I can prepare a schedule with check images. [[She has worked for you for nine years and I know her husband is ill|indirect:personal circumstances of the suspected employee]], so I am keeping this between the two of us and writing to your personal address, [[annika.ruud@northportmail.example|email]], not the clinic inbox.
[[W.P.|p3:initials]]
'''))

# ---------------------------------------------------------------- 314
DOCS.append(D(314, "xlsx", "accounts receivable ageing sheet", "accounting", "CA",
  title="Bilingual aged receivables listing for a Montréal wholesaler",
  ents={"p1": "Jean-Sébastien Bissonnette", "p2": "Thi Mai Huynh", "p3": "Rosalie Ouellet-Gervais", "p4": "Hamza El Idrissi",
        "p5": "Geneviève Courtemanche",
        "o1": "Distribution Mont-Rouleau inc.", "o2": "Boulangerie du Plateau Bissonnette", "o3": "Resto Saïgon Mai",
        "o4": "Épicerie Gervais & Filles", "o5": "Café Atlas Jean-Talon", "o6": "Traiteur Courtemanche"},
  distractors=["TPS/TVQ", "Net 30", "NSF", "Loi sur la faillite", "31-60", "61-90"],
  sheets=[
    ("Âgé - Aged AR", [
      ["[[Distribution Mont-Rouleau inc.|o1:full]]", "Comptes clients âgés / Aged receivables", "au / as at", dt("2025-10-31", "yyyy-mm-dd", "date:as-at date")],
      ["No client", "Client / Customer", "Courant / Current", "31-60", "61-90", "90+", "Total", "Dernier paiement / Last payment", "Notes"],
      ["[[C-1042|rec:customer number]]", "[[Boulangerie du Plateau Bissonnette|o2:full]]", amt(1840.25, "num"), amt(2212.10, "num"), "", "", amt(4052.35, "num"), dt("2025-09-12", "yyyy-mm-dd", "date:last payment date"), "[[M. Bissonnette|p1:title-surname:French honorific]] promet un chèque [[le 14 nov.|date:French day and abbreviated month]]"],
      ["[[C-1077|rec:customer number]]", "[[Resto Saïgon Mai|o3:full]]", "", amt(960.00, "num"), amt(1415.75, "num"), amt(3380.40, "num"), amt(5756.15, "num"), dt("2025-06-27", "yyyy-mm-dd", "date:last payment date"), "Chèque NSF le [[3 oct.|date:French day and abbreviated month]] ([[1 200 $|money:French format, space thousands and trailing dollar sign]]). [[Mme Huynh|p2:title-surname:French honorific]] says [[her husband is in hospital|health:family member hospitalised]]; payment plan [[400 $|money:trailing dollar sign]] / sem."],
      ["[[C-1103|rec:customer number]]", "[[Épicerie Gervais & Filles|o4:full]]", amt(3120.90, "num"), "", "", "", amt(3120.90, "num", None), dt("2025-10-20", "yyyy-mm-dd", "date:last payment date"), "OK"],
      ["[[C-1118|rec:customer number]]", "[[Café Atlas Jean-Talon|o5:full]]", "", "", "", amt(7904.66, "num"), amt(7904.66, "num", None), dt("2025-04-02", "yyyy-mm-dd", "date:last payment date"), "Fermé. [[Proposition de consommateur déposée|attr:insolvency filing]] (Loi sur la faillite) - syndic file [[41-3027715|rec:insolvency estate number]]. Write off?"],
      ["[[C-1126|rec:customer number]]", "[[Traiteur Courtemanche|o6:full]]", amt(540.00, "num"), amt(540.00, "num", None), "", "", amt(1080.00, "num"), dt("2025-10-03", "yyyy-mm-dd", "date:last payment date"), "Paie par carte - Visa finissant par [[5762|card:last four of card]]"],
      ["Total", "", amt(5501.15, "num"), amt(3712.10, "num"), amt(1415.75, "num", None), amt(11285.06, "num"), amt(21914.06, "num"), "", ""],
    ]),
    ("Contacts", [
      ["No client", "Personne-ressource / Contact", "Téléphone", "Courriel / Email", "Adresse", "Ville", "Code postal", "No TPS / GST no.", "No TVQ / QST no."],
      ["C-1042", "[[Jean-Sébastien Bissonnette|p1:full]]", "[[514 555-0147|phone:Quebec style, space after area code]]", "[[js@boulangeriebissonnette.example|email]]", "[[4418, avenue du Mont-Royal Est|addr:French-Canadian address, comma after number]]", "[[Montréal|place:city]]", "[[H2J 1Y6|zip:Canadian postal code]]", "[[81447 2209 RT0001|taxid:GST/HST registration number]]", "[[1224418870 TQ0001|taxid:QST registration number]]"],
      ["C-1077", "[[Huynh, Thi Mai|p2:last-first]]", "[[514-555-0183|phone]]", "[[saigonmai@courrielqc.example|email]]", "[[7052, rue Saint-Denis|addr:French-Canadian address, comma after number]]", "Montréal", "[[H2S 2S4|zip:Canadian postal code]]", "[[74412 0937 RT0001|taxid:GST/HST registration number]]", "[[1219930442 TQ0001|taxid:QST registration number]]"],
      ["C-1103", "[[Rosalie Ouellet-Gervais|p3:full]]", "[[(450) 555-0112|phone]]", "[[rosalie@epiceriegervais.example|email]]", "[[212, boul. Curé-Labelle|addr:French-Canadian address with abbreviated boulevard]]", "[[Laval|place:city]]", "[[H7L 2Z9|zip:Canadian postal code]]", "[[89903 4471 RT0001|taxid:GST/HST registration number]]", "[[1230077415 TQ0001|taxid:QST registration number]]"],
      ["C-1118", "[[Hamza El Idrissi|p4:full]] (personal guarantee signed [[2023-02-14|date:ISO date]])", "[[438 555 0166|phone:spaces only]]", "[[hamza.elidrissi@courrielqc.example|email]]", "[[301-6690, rue Jean-Talon Est|addr:unit-first French-Canadian address]] (dom.: [[88, 12e Avenue|addr:French-Canadian ordinal street]], [[Saint-Léonard|place:borough]])", "Montréal", "[[H1S 1N2|zip:Canadian postal code]]", "[[70218 5536 RT0001|taxid:GST/HST registration number]]", ""],
      ["C-1126", "[[Geneviève Courtemanche|p5:full]] - [[Gen|p5:nickname]]", "[[514.555.0129|phone:dotted]]", "[[gen@traiteurcourtemanche.example|email]]", "[[1955, rue Beaubien Est|addr:French-Canadian address, comma after number]]", "Montréal", "[[H2G 1M1|zip:Canadian postal code]]", "", ""],
      ["Notes", "TPS/TVQ charged on all invoices. Terms Net 30. [[Hamza|p4:first-name]] also owes [[2 500,00 $|money:French format with decimal comma]] on a personal loan from the owner - not in this ledger.", "", "", "", "", "", "", ""],
    ]),
  ]))

# ---------------------------------------------------------------- 315
DOCS.append(D(315, "eml", "expense claim query thread", "accounting", "UK", enc="plain", cardholders=["p2"],
  title="Finance team's query on an expense claim, with quoted replies",
  ents={"p1": "Imogen Ashby-Voce", "p2": "Callum Rutherglen", "p3": "Priyanka Venn",
        "o1": "Harcastle Surveying Ltd", "o2": "The Mill Race Hotel", "o3": "Moorgate Plant Hire"},
  distractors=["HMRC", "P11D", "VAT receipt", "Concur", "45p per mile"],
  headers={"From": "[[Imogen Ashby-Voce|p1:full]] <[[accounts@harcastlesurveying.example|email]]>",
           "To": "[[Callum Rutherglen|p2:full]] <[[c.rutherglen@harcastlesurveying.example|email]]>",
           "Cc": "[[Priyanka Venn|p3:full]] <[[p.venn@harcastlesurveying.example|email]]>",
           "Subject": "RE: RE: Expenses claim [[EXP-2025-1147|rec:expense claim number]] - 3 things outstanding",
           "Date": "Mon, [[10 Nov 2025|date:email header date]] 09:12:44 +0000"},
  body=r'''
Hi [[Callum|p2:first-name]],

Thanks. Please don't send card details by email again - I've deleted your message from the shared inbox and so should you. I've set the refund up from what you sent, so no need to resend.

Where we are on claim [[EXP-2025-1147|rec:expense claim number]] (employee no. [[HS0388|rec:employee number]]):

1. [[The Mill Race Hotel|o2:full]], [[Leeds|place:city]], 2 nights from [[21/10/2025|date:day-first numeric]], [[£238.00|money:pounds]]. This went on the company Amex ending [[51947|card:last five of card]], not your own card, so I've taken it off the claim. I still need the VAT receipt (their VAT no. is [[GB 418 7729 06|taxid:UK VAT registration number]] if you need to ring them).
2. Mileage [[Sheffield|place:city]] - [[Hebden Bridge|place:town]] - Sheffield, 3 trips, 212 miles at 45p per mile = [[£95.40|money:pounds]]. HMRC wants the vehicle on the claim: I have your Octavia as [[YK21 HXT|veh:UK registration plate]] - still right?
3. [[Moorgate Plant Hire|o3:full]] deposit [[£400|money:pounds]] paid on your personal Visa on [[23 Oct|date:day and abbreviated month]]. Approved by [[Priyanka|p3:first-name]]. We'll reimburse with payroll on [[the 28th|date:day of month only]] to the account we hold for you (sort code [[40-51-62|rtn:UK sort code]], account ending [[6819|acct:last four of account]]).

Total now payable to you: [[£495.40|money:pounds]].

[[Imogen|p1:first-name]]
[[Harcastle Surveying Ltd|o1:full]] | Finance | [[0114 496 0133|phone:UK landline]]

-----Original Message-----
From: Callum Rutherglen
Sent: [[07 November 2025|date:day month year]] 18:03
To: Accounts
Subject: RE: Expenses claim EXP-2025-1147 - 3 things outstanding

[[Imogen|p1:first-name]] - the plant hire lot charged me twice (2 x [[400|money!:bare number, no currency sign]]). They say they can only refund to the card but their machine was down, can you sort it with them direct? Card is my Visa [[4189 9264 4982 6610|card]], exp [[04/27|exp]], security code [[380|cvv]], name on it is [[MR C J RUTHERGLEN|p2:caps:name as embossed on a card]]. Billing postcode [[S11 8TP|zip:UK postcode]].
Also I'm off from [[Weds 12th|date:weekday and day of month]] for [[the op on my knee|health:planned surgery]] so anything else ring me on [[07700 900118|phone:UK mobile]] before then.
[[Cal|p2:nickname]]

-----Original Message-----
From: Accounts
Sent: [[06 November 2025|date:day month year]] 11:40
To: Callum Rutherglen
Subject: Expenses claim EXP-2025-1147 - 3 things outstanding

Hi Callum, three items on your October claim can't go through Concur as submitted - hotel, mileage and a [[£400|money:pounds]] deposit with no receipt. Can you send what you have? Anything not sorted by month end goes on your P11D. Thanks, [[I.A-V.|p1:initials]]
'''))

# ---------------------------------------------------------------- 316
DOCS.append(D(316, "txt", "sole trader bookkeeping notes", "accounting", "AU",
  title="Australian bookkeeper's client notes for a sole-trader electrician",
  ents={"p1": "Lachlan Petherbridge", "p2": "Mele Taufahema", "p3": "Bronwyn Kiddle",
        "o1": "Petherbridge Electrical", "o2": "Kiddle & Co Bookkeeping", "o3": "Illawarra Mutual Bank",
        "o4": "SunCoast Tradies Super"},
  distractors=["BAS", "GST", "ATO", "PAYG instalment", "Single Touch Payroll", "Xero"],
  body=r'''
[[Kiddle & Co Bookkeeping|o2:full]] - client file note
Client: [[Lachlan Petherbridge|p1:full]] t/as [[Petherbridge Electrical|o1:full]]     Client code [[PETH01|rec:client code]]
Note by [[Bronwyn Kiddle|p3:full]] (BAS agent no. [[24718803|govid:BAS agent registration number]]) after meeting at his place, [[Tues 4/11/25|date:weekday and day-first short date]]

DETAILS
ABN [[51 824 753 556|taxid:Australian Business Number]]   TFN [[481 207 339|taxid:Australian tax file number]]   DOB [[17/03/1986|dob:day-first numeric]]
Home / business address: [[Unit 4, 18 Wattle Grove Road|addr:unit and street]], [[Marrickville|place:suburb]] [[NSW|place:state abbreviation]] [[2204|zip:Australian postcode]]
Mob [[0491 570 156|phone:Australian mobile]]   [[lachie@petherbridgeelectrical.example|email]]
Electrical contractor licence [[348817C|govid:contractor licence number]], NSW driver licence [[19044712|govid:driver licence number]]
Business account: [[Illawarra Mutual Bank|o3:full]], BSB [[641-800|rtn:Australian BSB]], acct [[10447 2218|acct:account number with a space]]
Work ute: 2021 HiLux, rego [[CX41TZ|veh:NSW registration plate]] - logbook kept from [[1 July|date:day and month]], 78% business so far

SEPT QUARTER BAS (due [[25 Nov|date:day and abbreviated month]] through us)
- Sales incl GST [[$68,442.00|money]], GST collected [[$6,222|money]]
- Purchases incl GST [[$21,907.50|money]], GST credits [[$1,991.59|money]]
- PAYG instalment [[$3,150|money]]. Net payable about [[$7,380|money]]. He hasn't got it. Wants a payment plan; ATO debt from last year is still [[$11,260.45|money]] on the running balance account.
- One apprentice, [[Mele Taufahema|p2:full]], started [[11/08/2025|date:day-first numeric]], [[$24.80|money:hourly rate]]/hr. Single Touch Payroll not lodged for 3 pays. Super goes to [[SunCoast Tradies Super|o4:full]], member no. [[STS-4471209|rec:super fund member number]]. [[Mele|p2:first-name]]'s TFN declaration is on file: [[602 118 457|taxid:Australian tax file number]], DOB [[9 Feb 2006|dob:day, abbreviated month, year]].

THINGS HE TOLD ME (not for the accountant's letter)
- [[Lachie|p1:nickname]] and his partner split in June. [[He pays child support for two kids through Services Australia|attr:child support obligation]], [[$412|money]] a fortnight, comes out of the business account - recode to drawings.
- [[He's been off the tools since the shoulder reconstruction in September|health:surgery and incapacity]]; income protection claim no. [[IP-22087341|rec:insurance claim number]] pays [[$1,150|money]] a week, taxable.
- His Medicare card for the claim forms: [[2951 84417 3|govid:Medicare card number]], ref 1.
- Xero login is his email; he wrote the password on the whiteboard, [[Sparky#2204|cred:accounting software password]]. Told him to change it and turn on two-step.
- Second phone for jobs only: [[(02) 5550 0142|phone:Australian landline with area code]]

TO DO: lodge STP, draft payment plan ([[$600|money]]/mth?), ring him [[Fri 14th|date:weekday and day of month]].   [[BK|p3:initials]]
'''))

# ---------------------------------------------------------------- 317
DOCS.append(D(317, "docx", "tax engagement letter with card authorization", "accounting", "US", cardholders=["p2"],
  title="CPA engagement letter to a couple, with a card-on-file authorization block",
  ents={"p1": "Everett J. Sundquist", "p2": "Noor Sundquist", "p3": "Delphine Marchbanks",
        "o1": "Marchbanks & Yoder, CPAs", "o2": "Sundquist Field Geology LLC"},
  distractors=["Form 1040", "Schedule C", "Form 8879", "Circular 230", "IRC § 7216", "Form 2848"],
  header="[[Marchbanks & Yoder, CPAs|o1:full]]",
  footer="Client no. [[20417|rec!:client number]] — engagement letter, tax year 2025",
  body=r'''
# [[Marchbanks & Yoder, CPAs|o1:full]]
[[212 West Main Street, Suite 3|addr:street with suite]] · [[Bozeman|place:city]], [[Montana|place:state]] [[59715|zip]] · [[406-555-0137|phone]] · [[www.marchbanksyoder.example|url:firm website]]
[[December 1, 2025|date:letter date]]
[[Everett J. Sundquist|p1:full]] and [[Noor Sundquist|p2:full]]
[[1885 Sourdough Ridge Road|addr]]
Bozeman, [[MT|place:state abbreviation]] [[59715-8802|zip:ZIP+4]]
Dear [[Everett|p1:first-name]] and [[Noor|p2:first-name]]:
Thank you for choosing us again. This letter confirms the terms of our engagement to prepare your 2025 federal and Montana individual income tax returns (Form 1040 with Schedule C for [[Sundquist Field Geology LLC|o2:full]], EIN [[81-4471906|taxid:EIN]]).
## What we will do
We will prepare the returns from the information you give us. We will not audit or verify it. You are responsible for the accuracy of the returns and should review them before signing Form 8879. Our work is governed by Circular 230, and we will not disclose your information except as allowed by IRC § 7216.
## What we need from you
Please upload your documents to the portal at [[https://portal.marchbanksyoder.example/sundquist|url:client portal link]] by [[March 2, 2026|date:deadline]]. Your portal user name is [[esundquist59715|cred:portal user name]]; if the password we set last year ([[Bridger!Bowl88|cred:portal password]]) no longer works, call the office. We have you on file as SSNs ending [[4983|ssn:last four digits only]] ([[Everett|p1:first-name]]) and [[8373|ssn:last four digits only]] ([[Noor|p2:first-name]]); tell us if either is wrong.
## Fees
Our fee for the returns described above is [[$1,450|money]]. Bookkeeping clean-up for the LLC, if needed, is billed at [[$95|money:hourly rate]] per hour. A deposit of [[$400.00|money]] is due on signing. Last year's balance of [[$212.50|money]] remains unpaid and will be added.
## Card on file (optional)
I authorize [[Marchbanks & Yoder|o1:short]] to charge the card below for the deposit now and for the balance when the returns are ready.
| Name on card | [[Noor A. Sundquist|p2:full:with middle initial]] |
| Card number | [[4196 6112 9293 7588|card]] |
| Expires | [[11/2028|exp:four-digit year]] |
| Security code | [[902|cvv]] |
| Billing ZIP | 59715 |
| Cell for receipts | [[(406) 555-0181|phone]] |
## Signatures
[[Delphine Marchbanks|p3:full]], CPA (Montana license no. [[CPA-007418|govid:CPA license number]]) — [[delphine@marchbanksyoder.example|email]]
Accepted: ______________________ [[E. J. Sundquist|p1:short:initials + surname]] Date ________
Accepted: ______________________ [[N. Sundquist|p2:short:initial + surname]] Date ________
**P.S.** [[Noor|p2:first-name]], you mentioned that [[your naturalization interview is in February|attr:immigration status]]. If USCIS asks for tax transcripts we can pull them with a Form 2848; there is no charge for that.
'''))

# ---------------------------------------------------------------- 318
DOCS.append(D(318, "md", "vendor master change log", "accounting", "US",
  title="Accounts-payable vendor master change log with callback verification",
  ents={"p1": "Roxanne Villegas-Stout", "p2": "Ikechukwu Nnamdi", "p3": "Gerald Pfeffer", "p4": "Suda Wongsakul",
        "p5": "Travis Hollenbeck",
        "o1": "Hollenbeck Property Management, Inc.", "o2": "Nnamdi HVAC Services", "o3": "Pfeffer & Sons Roofing LLC",
        "o4": "Suda's Cleaning Crew", "o5": "Brazoria Gulf Bank", "o6": "Cypress Bend Credit Union",
        "o7": "Trinity Bayou National Bank"},
  distractors=["Form W-9", "AP-07", "Yardi Voyager 8"],
  body=r'''
# Vendor master file — change log (Q4)

Owner: [[Roxanne Villegas-Stout|p1:full]], AP lead, [[Hollenbeck Property Management, Inc.|o1:full]]
Procedure AP-07: no bank change is made live until a callback to the number **already on file** is logged. System: Yardi Voyager 8.

| Date | Vendor no. | Vendor | Field | Old value | New value | Requested via | Callback / verified by |
|---|---|---|---|---|---|---|---|
| [[10/02/25|date:short numeric date]] | [[V00418|rec:vendor number]] | [[Nnamdi HVAC Services|o2:full]] ([[Ikechukwu Nnamdi|p2:full]], sole prop.) | Tax ID | SSN [[857-48-6718|ssn]] | EIN [[93-4471208|taxid:EIN]] | new Form W-9 by email | n/a — [[RVS|p1:initials]] |
| [[10/09/25|date:short numeric date]] | [[V00233|rec:vendor number]] | [[Pfeffer & Sons Roofing LLC|o3:full]] | Bank | [[Brazoria Gulf Bank|o5:full]], ABA [[118200886|rtn]], acct [[0044187725|acct]] | [[Cypress Bend Credit Union|o6:full]], ABA [[119830695|rtn]], acct [[77100492|acct]] | letter on letterhead | Called [[Gerald Pfeffer|p3:full]] at [[979-555-0144|phone]], [[10/10|date:month/day only]] 9:20. Confirmed. — RVS |
| [[10/21/25|date:short numeric date]] | [[V00507|rec:vendor number]] | [[Suda's Cleaning Crew|o4:full]] ([[Suda Wongsakul|p4:full]]) | Address | [[1420 Avenue H, Lot 6|addr:street with lot number]], [[Rosenberg|place!:city that is also a surname]] [[TX|place:state abbreviation]] [[77471|zip]] | [[88 Mulberry Field Ln|addr]], [[Richmond|place:city]] TX [[77406|zip]] | phone | Spoke with [[Suda|p4:first-name]] in person at the [[Lake Jackson|place:city]] office. — RVS |
| [[11/03/25|date:short numeric date]] | V00418 | Nnamdi HVAC Services | Bank | Cypress Bend Credit Union, acct ending [[3310|acct:last four of account]] | [[Trinity Bayou National Bank|o7:full]], ABA [[117568095|rtn]], acct [[5120044871|acct]] | vendor portal, user [[inamdi.hvac|cred:vendor portal user name]] | **REJECTED — see below** |
| [[11/05/25|date:short numeric date]] | V00418 | Nnamdi HVAC Services | Portal password | — | reset; temp password [[Tmp-7Qx!4418|cred:temporary password]] given by phone | phone | [[Ike|p2:nickname]] confirmed identity with last 4 of EIN. — RVS |

## [[11/03|date:month/day only]] rejected change — notes for [[Travis|p5:first-name]]

- The portal request came in at 02:14 from IP [[198.51.100.77|ip]]. Every earlier login for this vendor was from [[203.0.113.140|ip]] (his shop in [[Angleton|place:city]]).
- The portal user name is **inamdi.hvac**; the real one is [[innamdi.hvac|cred:vendor portal user name]]. Somebody registered a look-alike account on [[10/30|date:month/day only]] using [[ike@nnamdi-hvac-services.example|email]], not his real address, [[ike@nnamdihvac.example|email]].
- I called [[Mr. Nnamdi|p2:title-surname]] on the number on file, [[(979) 555-0171|phone]]. He has not changed banks. He says his email was hacked in October and that he had sent an invoice with his voided check to another customer.
- Our next ACH to him would have been [[$18,440.00|money]] on [[November 7|date:month and day]] (invoices [[NH-2291|rec:invoice number]] and [[NH-2304|rec:invoice number]]). Held and reissued to the old account.
- I have not told the bank yet. [[Travis Hollenbeck|p5:full]] to decide whether we report it; our cyber policy is no. [[CYB-0091844|rec:insurance policy number]].
- Side note: Ike mentioned he is [[waiting on his citizenship oath ceremony|attr:immigration status]] and is worried a fraud report with his name on it will cause him trouble. I told him he is the victim here.
'''))

# ---------------------------------------------------------------- 319
DOCS.append(D(319, "txt", "bilingual accountant's client note", "accounting", "EU",
  title="French accountant's bilingual note and fee summary for English-speaking clients",
  ents={"p1": "Élodie Vasseur-Lemaître", "p2": "Graham Entwistle", "p3": "Patricia Entwistle", "p4": "Maître Julien Cazenave",
        "o1": "Cabinet Vasseur Expertise Comptable", "o2": "Les Gîtes du Noyer", "o3": "Crédit Mutuel du Périgord Noir"},
  distractors=["formulaire 2042-C-PRO", "micro-BIC", "CFE", "impots.gouv.fr", "LMNP", "TVA non applicable, art. 293 B du CGI"],
  body=r'''
[[Cabinet Vasseur Expertise Comptable|o1:full]]
[[14 bis, rue de la République|addr:French address with bis]] - [[24200|zip:French postal code]] [[Sarlat-la-Canéda|place:town]] - Tél. [[05 55 55 01 42|phone:French format, pairs of digits]]
SIRET [[824 417 209 00031|taxid:French SIRET number]]

[[Sarlat|place:town, short form]], [[le 12 novembre 2025|date:French long date]]

M. et Mme [[ENTWISTLE|p2:caps:surname in caps, French style]]
[[Lieu-dit Les Noyers|addr:French rural address without number]]
[[24250|zip:French postal code]] [[Domme|place:village]]

Objet / Re: your 2025 file - [[Les Gîtes du Noyer|o2:full]] - dossier n° [[D-2023-0418|rec:client file number]]

Dear [[Graham|p2:first-name]], dear [[Patricia|p3:first-name]],

Voici le point sur votre dossier. I write in English below, with the French terms you will see on the forms.

1. Rental income (revenus locatifs). For the two gîtes you received [[38 640,00 €|money:French format, space thousands, decimal comma]] between [[1er janvier|date:French ordinal day and month]] and [[31 octobre 2025|date:French long date]]. You remain under the micro-BIC regime (LMNP). The amount to report on formulaire 2042-C-PRO will be about [[46 000 €|money:French format]] for the full year.

2. Numbers you asked for:
   - SIRET of the gîtes: [[901 447 182 00014|taxid:French SIRET number]]
   - Your numéro fiscal: [[30 24 418 772 091|taxid:French tax number]] ([[Graham|p2:first-name]]), [[30 24 418 772 106|taxid:French tax number]] ([[Patricia|p3:first-name]])
   - Your space on impots.gouv.fr: the identifiant is the numéro fiscal; the mot de passe you gave me by phone, [[Dordogne2019!|cred:tax portal password]], should be changed.

3. CFE. The avis for [[412 €|money:euro after the number]] is payable before [[15/12/2025|date:day-first numeric]]. It will be taken from your account at the [[Crédit Mutuel du Périgord Noir|o3:full]], IBAN [[FR34 2604 6402 3594 0889 4661 008|iban]], BIC [[CMPNFR2AXXX|acct:BIC / SWIFT code]].

4. Residence. Your cartes de séjour ([[titre de séjour "Article 50 TUE"|attr:immigration status]], n° [[9924041877|govid:French residence permit number]] and n° [[9924041878|govid:French residence permit number]]) expire on [[03/02/2026|date:day-first numeric]]. The préfecture asks for the last avis d'imposition; I enclose it. Your UK State Pensions ([[£11,502|money:pounds]] and [[£8,814|money:pounds]]) are declared here but taxed only in the UK.

5. The sale of the barn. [[Maître Julien Cazenave|p4:full:French notary's title]], notaire à [[Bergerac|place:town]], needs your dates and places of birth for the acte: I gave him [[4 July 1953|dob:day month year]], [[Rochdale|place:town abroad]] (Graham) and [[22 Sept. 1955|dob:abbreviated month]], [[Oldham|place:town abroad]] (Patricia). Signature is planned for [[mardi 9 décembre|date:French weekday, day and month]] at 14h30. Price [[92 000 €|money:French format]], of which [[4 600 €|money:French format]] deposit already held by [[Me Cazenave|p4:title-surname:abbreviated French notary's title]].

6. Patricia: because of [[your long-term illness (ALD, 100 % cover)|health:long-term illness status]], the home-help costs are not deductible twice; send me the attestation from the CPAM anyway.

NOTE D'HONORAIRES n° [[F-2025-1187|rec:invoice number]]
   Tenue et déclarations 2025 .............. [[1 250,00 €|money:French format, decimal comma]]
   Assistance vente (forfait) .................. [[300,00 €|money:French format, decimal comma]]
   Total (TVA non applicable, art. 293 B du CGI) .... [[1 550,00 €|money:French format, decimal comma]]
   Règlement par virement sous 30 jours : IBAN [[FR02 8684 2669 6264 6131 7870 487|iban]]

Bien cordialement,
[[Élodie Vasseur-Lemaître|p1:full]], expert-comptable
[[e.vasseur@cabinet-vasseur.example|email]] - portable [[06 55 55 01 87|phone:French mobile]]
'''))

# ---------------------------------------------------------------- 320
DOCS.append(D(320, "pptx", "board finance and cap table deck", "accounting", "US",
  title="Start-up board deck: cap table, bridge note and founder matters, with speaker notes",
  ents={"p1": "Ksenia Abramovich", "p2": "Teodoro Balderas", "p3": "Hollis Grimsby", "p4": "Wanjiru Kamande",
        "p5": "Sandeep Ahluwalia",
        "o1": "Quillon Robotics, Inc.", "o2": "Grimsby Family Office LP", "o3": "Tessera Seed Partners",
        "o4": "Monadnock Commerce Bank", "o5": "Ahluwalia Valuation Advisors"},
  distractors=["409A", "Section 83(b)", "ASC 718"],
  body=r'''
# [[Quillon Robotics, Inc.|o1:full]] — Board finance update
- Prepared by [[Wanjiru Kamande|p4:full]], fractional CFO
- Board meeting of [[November 18, 2025|date:meeting date]] — CONFIDENTIAL
> Deck goes only to the three directors. [[Hollis|p3:first-name]] dials in from [[Nantucket|place:island]]; send to [[hollis@grimsbyfo.example|email]], not his assistant.
# Cap table (fully diluted) at [[10/31/2025|date:as-at date]]
| Holder | Class | Shares | % |
| [[Ksenia Abramovich|p1:full]] (CEO) | Common | 3,600,000 | 36.0% |
| [[Teodoro Balderas|p2:full]] (CTO) | Common | 2,900,000 | 29.0% |
| [[Tessera Seed Partners|o3:full]] | Seed Pref. | 1,500,000 | 15.0% |
| [[Grimsby Family Office LP|o2:full]] | Seed Pref. | 1,000,000 | 10.0% |
| Option pool | Common | 1,000,000 | 10.0% |
> [[Teo|p2:nickname]] never filed his Section 83(b) election in 2022. Counsel says the exposure is his personally, roughly [[$310,000|money]] of ordinary income at the last 409A price. He does not know we know.
# Bridge financing
- Convertible note from [[Grimsby Family Office|o2:short]]: [[$750,000|money]], 8%, matures [[May 31, 2026|date:maturity date]]
- [[Tessera|o3:short]] will match up to [[$500K|money:abbreviated thousands]] if the pilot signs by [[12/15|date:month/day only]]
- Wire received [[11/04/25|date:short numeric date]], ref [[FT25308-004417|rec:wire reference]]
> [[Hollis Grimsby|p3:full]] asked for a personal guarantee from [[Ksenia|p1:first-name]]. She refused. He then asked for a board seat for his son-in-law. Not on the agenda; expect it under other business.
# Cash and runway
- Operating account, [[Monadnock Commerce Bank|o4:full]], ending [[7714|acct:last four of account]]: [[$1,184,220|money]]
- Monthly net burn: [[$162,000|money]] — runway about seven months with the note
- Payroll: 11 people, [[$118,400|money]] per month fully loaded
- Company card (Amex ending [[9204|card:last four of card]]): [[$14,870|money]] in October, mostly cloud compute
> Online banking is still under Ksenia's login only ([[kabramovich_qr|cred:online banking user name]]). I need my own credentials before year end.
# 409A and option grants
- New 409A from [[Ahluwalia Valuation Advisors|o5:full]] ([[Sandeep Ahluwalia|p5:full]]) dated [[October 20, 2025|date:valuation date]]: [[$0.41|money:per-share price]] per common share
- Fee: [[$4,500|money]]. Grants to four engineers to be approved today.
> ASC 718 expense for the new grants is immaterial this year.
# Founder matters (closed session)
- [[K. Abramovich|p1:short:initial + surname]]: work authorization
- [[T. Balderas|p2:short:initial + surname]]: leave of absence request
> Ksenia is [[on an O-1 visa that expires in March|attr:immigration status]]; the green card petition (receipt [[IOE0924418820|rec:immigration receipt number]]) is pending. If it is denied she cannot remain CEO in the US. Budget [[$18,000|money]] for premium processing and counsel.
> Teo has asked for eight weeks off from January. He told me in confidence [[he is starting treatment for alcohol dependence|health:addiction treatment]] and [[his divorce is being finalized|indirect:marital status change]]; his wife's lawyer has already written asking about his 2,900,000 shares. Nothing in writing to the full board, please.
'''))
