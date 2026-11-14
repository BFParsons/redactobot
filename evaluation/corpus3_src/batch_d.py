from corpus3_src.core import D, dt, amt, num

DOCS = []

# ---------------------------------------------------------------- 331
DOCS.append(D(331, "txt", "bilingual immigration document checklist", "legal", "US", minors=["p3"],
  title="English/Spanish document checklist for a family-based adjustment of status",
  ents={"p1": "Yorleny Patricia Zelaya Murillo", "p2": "Brandon Keith Sattler", "p3": "Dariel Zelaya",
        "p4": "Mirna Carbajal", "p5": "Lic. Osvaldo Requena",
        "o1": "Requena Immigration Law, PLLC", "o2": "Clínica Buen Samaritano"},
  distractors=["I-130", "I-601A", "I-693", "I-864", "TPS"],
  body=r'''
[[Requena Immigration Law, PLLC|o1:full]]  -  [[6200 Savoy Dr., Ste. 410|addr:street with suite]], [[Houston|place:city]], [[TX|place:state abbreviation]] [[77036|zip]]  -  [[(713) 555-0162|phone]]
LISTA DE DOCUMENTOS / DOCUMENT CHECKLIST            Expediente / File: [[RIL-24-0933|rec:firm file number]]
Preparado por / Prepared by: [[Mirna Carbajal|p4:full]], paralegal        Fecha: [[5 de noviembre de 2025|date:Spanish long date]]

CLIENTE / CLIENT:   [[ZELAYA MURILLO, Yorleny Patricia|p1:last-first:surnames in caps, then given names]]     A# [[A209 771 448|govid:alien registration number]]
   Nacida / born [[23/08/1991|dob:day-first numeric]] en [[San Pedro Sula|place:city abroad]], [[Honduras|attr:country of birth / national origin]]
PETICIONARIO / PETITIONER:   [[Brandon Keith Sattler|p2:full]] (esposo, ciudadano / U.S. citizen), born [[02/14/1988|dob]], [[Beaumont|place:city]], [[Texas|place:state]]
HIJO / CHILD:   [[Dariel Zelaya|p3:full]], [[9 años|indirect:age of a child, in Spanish]], A# [[A209 771 449|govid:alien registration number]]

CASOS / CASES PENDING
  I-130 (esposa)   receipt [[IOE0931447182|rec:immigration receipt number]]   filed [[03/11/2025|date:filing date]]
  I-130 (hijastro) receipt [[IOE0931447190|rec:immigration receipt number]]
  I-601A provisional waiver - NOT yet filed. Needed because [[she entered without inspection near Hidalgo in June 2016|attr:manner of entry / immigration history]].
  TPS: [[registered since 2018, currently valid|attr:immigration status]]. EAD card no. [[SRC2190441877|govid:employment authorization card number]], vence / expires [[07/05/2026|date:card expiry date]].

LO QUE YA TENEMOS / WHAT WE HAVE                                          OK
  [x] Pasaporte hondureño de [[Yorleny|p1:first-name]], no. [[F418820|govid:Honduran passport number]]
  [x] Acta de matrimonio, [[Harris County|place:county]], [[19 de octubre de 2024|date:Spanish long date]]
  [x] Partida de nacimiento de [[Dariel|p3:first-name]] con traducción
  [x] [[Brandon|p2:first-name]]'s birth certificate and 2022-2024 tax transcripts (I-864). Income [[$54,300|money]]. SSN [[678-33-3479|ssn]].

LO QUE FALTA / STILL MISSING                                              Para cuándo
  [ ] Examen médico I-693 con la [[Clínica Buen Samaritano|o2:full]] - cita [[martes 18 de noviembre|date:Spanish weekday, day and month]], 8:30. Costo [[$380|money]] por persona, efectivo.
      Nota: en 2019 le salió [[positiva la prueba de tuberculina; radiografía normal|health:test result, in Spanish]]. Traer la radiografía.
  [ ] Récord policial. Yorleny says she was [[arrested in 2019 for driving without a license; case dismissed|attr:criminal history]] ([[Fort Bend County|place:county]], no. [[19-CCR-204418|rec:criminal case number]]). We need the certified disposition.
  [ ] Carta de dificultad extrema (hardship) from Brandon: mention that [[he has epilepsy and cannot drive|health:condition]], and that Yorleny takes him to work.
  [ ] Proof Dariel is in school: he is [[in fourth grade at Sutton Elementary|indirect:school and grade of a child]].
  [ ] 2 fotos tipo pasaporte c/u

HONORARIOS / FEES
  Filing fees I-601A [[$795|money]] + biometrics. Honorarios del abogado [[$3,500.00|money]]; pagado [[$1,200|money]] el [[10/02|date:month/day only]]; saldo [[$2,300|money]] en pagos de [[$250|money]] cada quincena.

CONTACTO
  Yorleny cel. [[832-555-0147|phone]] (WhatsApp; no dejar mensaje de voz, comparte el teléfono con su cuñada)
  Dirección: [[9100 Bissonnet St., Apt. 2207|addr:street with apartment]], Houston, TX [[77074|zip]]
  Brandon: [[bsattler88@gulfmail.example|email]], trabajo [[281.555.0190|phone:dotted]]

Revisado por / Reviewed: [[Lic. Osvaldo Requena|p5:full:Spanish professional title]] (Texas Bar No. [[24091877|govid:state bar number]])   [[MC|p4:initials]]
'''))

# ---------------------------------------------------------------- 332
DOCS.append(D(332, "docx", "immigration consultant client file summary", "legal", "CA", minors=["p3"],
  title="Regulated immigration consultant's Express Entry file summary",
  ents={"p1": "Thiago Nascimento Barbosa", "p2": "Camila Rezende Barbosa", "p3": "Lívia Barbosa", "p4": "Parveen Sahota",
        "o1": "Sahota Immigration Consulting Inc.", "o2": "Bedford Basin Software Inc.", "o3": "Cabot Strait Credit Union",
        "o4": "Mineiro Sul Banco"},
  distractors=["NOC 21232", "IRCC", "CLB 9", "Express Entry", "IMM 5476", "GCKey", "TEER 1"],
  header="[[Sahota Immigration Consulting Inc.|o1:full]] — client file [[SIC-2025-118|rec:consultant file number]] — confidential",
  body=r'''
# File summary — [[BARBOSA, Thiago Nascimento|p1:last-first:surname in caps first]]
Prepared by [[Parveen Sahota|p4:full]], RCIC (licence no. [[R518204|govid:immigration consultant licence number]]) · [[parveen@sahotaimmigration.example|email]] · [[902-555-0114|phone]]
Office: [[1505 Barrington Street, Suite 1210|addr:street with suite]], [[Halifax|place:city]], [[NS|place:province abbreviation]] [[B3J 3K5|zip:Canadian postal code]]
Last updated [[2025-11-06|date:ISO date]]
## 1. Who is on the application
| Person | Role | Date of birth | Passport | UCI |
| [[Thiago Nascimento Barbosa|p1:full]] | Principal applicant | [[11 May 1989|dob:day month year]] | [[Brazil|attr:citizenship / national origin]] [[GB447182|govid:Brazilian passport number]] | [[11-0441-8772|govid:IRCC unique client identifier]] |
| [[Camila Rezende Barbosa|p2:full]] | Spouse | [[30 Jan 1991|dob:abbreviated month]] | Brazil [[GC209317|govid:Brazilian passport number]] | [[11-0441-8780|govid:IRCC unique client identifier]] |
| [[Lívia Barbosa|p3:full]] | Dependent child | [[2019-09-02|dob:ISO date]] | Brazil [[GD118824|govid:Brazilian passport number]] | — |
## 2. Status and history
- [[Thiago|p1:first-name]] is in Canada [[on an employer-specific work permit valid to 14 August 2026|attr:immigration status]], permit no. [[U441877209|govid:work permit number]]. [[Camila|p2:first-name]] holds an open spousal permit; [[Lívia|p3:first-name]] has a visitor record and is [[in Grade 1 at a French immersion school in Bedford|indirect:school and grade of a child]].
- Employer: [[Bedford Basin Software Inc.|o2:full]], senior developer (NOC 21232, TEER 1), [[C$104,000|money:Canadian dollar prefix]] per year, since [[4 March 2024|date:employment start date]].
- Express Entry profile no. [[E004418772|rec:Express Entry profile number]], created [[Sept. 12, 2025|date:abbreviated month]]. Language: CLB 9. Invitation to apply received [[October 22, 2025|date:invitation date]]; the application must be submitted by [[December 21, 2025|date:deadline]].
- [[One refused US visitor visa in 2017|attr:immigration history]] (Thiago). It must be declared. Nothing else adverse; no criminal record in Brazil or Canada.
## 3. Documents outstanding
- Police certificate from Brazil for Camila (requested [[3/11|date:day/month only, day first]]).
- Medical exams booked [[Nov. 19|date:abbreviated month and day]]. Camila mentioned [[she is being treated for hypothyroidism|health:condition]]; not an admissibility concern, but bring the prescription.
- Proof of funds letters. Required for a family of three: [[$22,483|money]]. They have [[C$28,450.17|money:Canadian dollar prefix]] at [[Cabot Strait Credit Union|o3:full]] (transit [[60283|rtn:Canadian transit number]], account [[1104418-7|acct]]) and about [[R$ 61.000|money:Brazilian reais, dot as thousands separator]] at [[Mineiro Sul Banco|o4:full]], which needs a certified translation.
- Use of representative form IMM 5476, signed by both adults.
## 4. Portal access (client-supplied — delete after submission)
- IRCC secure account (GCKey) user name: [[tnbarbosa89|cred:government portal user name]]
- Password: [[Pao-de-Queijo#21|cred:government portal password]]
- Recovery question answer ("first pet"): [[Bolinha|cred:security question answer]]
- Our client portal: [[https://clients.sahotaimmigration.example/file/SIC-2025-118|url:client portal link]]
## 5. Fees
Retainer agreement signed [[2025-09-05|date:ISO date]]. Professional fee [[$3,500|money]] plus HST; government fees [[$3,315.00|money]] (two adults and a child, with right of permanent residence fees). Received to date [[$2,000.00|money]] by e-transfer from [[thiago.barbosa@correiomail.example|email]]. Home address for the receipt: [[77 Nelsons Landing Blvd., Unit 508|addr:street with unit]], [[Bedford|place:town]], NS [[B4A 3X1|zip:Canadian postal code]]. Cell [[782 555 0166|phone:spaces only]].
'''))

# ---------------------------------------------------------------- 333
DOCS.append(D(333, "pdf", "lasting power of attorney attendance note", "legal", "UK",
  title="Solicitor's attendance note on a lasting power of attorney for a 92-year-old client",
  ents={"p1": "Winifred Mary Arkwright", "p2": "Julian Arkwright", "p3": "Tamsin Pargeter", "p4": "Dr Rohan Seneviratne",
        "p5": "Honor Wilmot",
        "o1": "Garside Wilmot LLP", "o2": "Nidderdale Building Society", "o3": "The Arkwright Will Trust"},
  distractors=["Mental Capacity Act 2005", "Form LP1F", "Office of the Public Guardian", "Premium Bonds"],
  body=r'''
# [[Garside Wilmot LLP|o1:full]] — ATTENDANCE NOTE
Client: [[Mrs Winifred Mary Arkwright|p1:full:with honorific]] · Matter: [[ARK/0412/LPA|rec:solicitor matter reference]] · Fee earner: [[Honor Wilmot|p5:full]] ([[HW|p5:initials]]) · Date: [[11 November 2025|date:attendance date]] · Time: 1 hr 20 mins · Home visit
## Attendance
HW attending [[Mrs Arkwright|p1:title-surname]] at her home, [[The Old Forge, 9 Church Lane|addr:house name, number and street]], [[Pateley Bridge|place:town]], [[Harrogate|place:town]] [[HG3 5LB|zip:UK postcode]]. Her son [[Julian Arkwright|p2:full]] let me in and then, at my request, left for the whole of the meeting.
Mrs Arkwright is [[92|age:bare age]] (born [[3 April 1933|dob:day month year]]). She was a schoolteacher and is very clear about what she wants. She is [[registered partially sighted|health:condition]], so I read each section of Form LP1F aloud. She told me her GP said in the summer that she has [[mild cognitive impairment|health:diagnosis]]; she [[scored 26 out of 30 on the MMSE|health:cognitive test score]] in August. I asked the usual open questions under the Mental Capacity Act 2005. She explained in her own words what an attorney can and cannot do, and why she does not want the bank "deciding for her." I have no concerns about capacity or pressure.
## Instructions
- Both types of LPA: property and financial affairs, and health and welfare.
- Attorneys: [[Julian|p2:first-name]] (son, born [[19.07.1961|dob:dotted day-first]], of [[14 Ripon Road|addr]], Harrogate [[HG1 2JB|zip:UK postcode]]) and her granddaughter [[Tamsin Pargeter|p3:full]] (born [[2 Feb 1992|dob:abbreviated month]], of [[Flat 2, 61 Otley Road|addr:flat and street]], [[Leeds|place:city]] [[LS6 3AB|zip:UK postcode]]), to act jointly and severally.
- She does NOT want her younger son to be notified. She said only that [[he "has had his troubles with money and with drink"|indirect:family member's financial and alcohol problems]] and has not visited since 2021.
- Life-sustaining treatment: attorneys to decide. She [[is a Quaker|attr:religion]] and wants a simple funeral at the meeting house; noted, though not for the LPA itself.
- Certificate provider: her GP, [[Dr Rohan Seneviratne|p4:full]], who has known her for eleven years. [[Dr Seneviratne|p4:title-surname]] will call on [[Friday 14th|date:weekday and day of month]].
## Assets (for the Will Trust file as well)
- The house, unencumbered, about [[£465,000|money:pounds]]. Title number [[NYK204418|rec:Land Registry title number]].
- [[Nidderdale Building Society|o2:full]] instant access account: sort code [[60-83-71|rtn:UK sort code]], account [[44187209|acct:UK account number]], about [[£38,600|money:pounds]].
- Premium Bonds, holder's number [[104418772|rec!:Premium Bonds holder's number]]: [[£50,000|money:pounds]].
- Teachers' pension, [[£1,412.50|money:pounds]] a month; state pension. NI number [[ZT 41 87 20 B|taxid:UK National Insurance number]].
- Life interest under [[The Arkwright Will Trust|o3:full]] (her late husband's will, 1998): one half of the house is held in the trust.
## Costs and next steps
Fixed fee [[£850|money:pounds]] plus VAT for both LPAs, plus the Office of the Public Guardian registration fees of [[£82|money:pounds]] each. She does not qualify for a fee remission. She paid [[£200|money:pounds]] on account by cheque no. [[000318|rec:cheque number]].
Engrossments to be posted, large print. Any queries: she prefers the landline, [[01632 960188|phone:UK landline]], after 10am. [[Julian|p2:first-name]]'s mobile [[07700 900131|phone:UK mobile]]; [[Tamsin|p3:first-name]]'s email [[tamsin.pargeter@ridingsmail.example|email]].
'''))

# ---------------------------------------------------------------- 334
DOCS.append(D(334, "eml", "estate planning email thread", "legal", "US", enc="base64", minors=["p3", "p4"],
  title="Estate planner's email on beneficiary designations and a special needs trust, with the client's reply quoted",
  ents={"p1": "Whitney Tolleson", "p2": "Marcus Tolleson", "p3": "Eli Tolleson", "p4": "Harper Tolleson",
        "p5": "Paige Dunaway", "p6": "Annabeth Crowder",
        "o1": "Crowder Estate Planning, PLLC", "o2": "Catawba Trust Bank", "o3": "Yadkin Fidelity Life",
        "o4": "Uwharrie Furniture Group"},
  distractors=["401(k)", "401k", "IRA"],
  headers={"From": "[[Annabeth Crowder|p6:full]] <[[annabeth@crowderestate.example|email]]>",
           "To": "[[Whitney Tolleson|p1:full]] <[[whitney.tolleson@piedmontmail.example|email]]>, [[Marcus Tolleson|p2:full]] <[[mtolleson@uwharriefurniture.example|email]]>",
           "Subject": "RE: beneficiary forms - please do NOT name Eli directly",
           "Date": "Wed, [[5 Nov 2025|date:email header date]] 08:41:27 -0500"},
  body=r'''
[[Whitney|p1:first-name]], [[Marcus|p2:first-name]],

Good questions. Short answers first, then the list.

Please do not name [[Eli|p3:first-name]] as a direct beneficiary of anything. Because [[he receives SSI and Medicaid|attr:benefits status]], an inheritance in his own name of more than [[$2,000|money]] would cut off his benefits. Everything meant for him should name "the trustee of the [[Eli Tolleson|p3:full]] Supplemental Needs Trust dated [[October 30, 2025|date:trust date]]." The trust's EIN is [[39-4418772|taxid:EIN]]. [[Harper|p4:first-name]]'s share can go to her outright through a custodian until she is 25.

What to change, account by account:

1. Marcus's 401(k) at [[Uwharrie Furniture Group|o4:full]] (plan participant ID [[UFG-204418|rec:retirement plan participant ID]], balance about [[$312,000|money]]): primary Whitney 100%; contingent 50% the trust, 50% Harper.
2. Whitney's rollover IRA at [[Catawba Trust Bank|o2:full]], account [[CTB-7700418|acct:IRA account number]]: same pattern.
3. [[Yadkin Fidelity Life|o3:full]] term policy no. [[YF-0044187-T|rec:life insurance policy number]], face amount [[$750,000|money]], insured Marcus (the application shows SSN ending [[6049|ssn:last four digits only]] - please confirm that is right, I have [[6094|ssn:last four digits only]] in my notes).
4. Joint checking and savings at [[Catawba|o2:short]]: leave as they are; the wills cover them.

Guardian. You named Whitney's sister, [[Paige Dunaway|p5:full]], of [[Greensboro|place:city]]. I need her date of birth and a phone number for the nomination, and she should know that Eli's guardianship continues after he turns 18; we would file for adult guardianship [[the year before his 18th birthday, i.e. in 2027|indirect:timing that reveals a child's age]].

Fee: the flat fee of [[$4,800|money]] covers all of this. Balance due at signing is [[$2,400|money]]. Signing is [[Thursday, November 20|date:weekday, month and day]] at 2:00 at our office, [[301 N. Elm Street, Suite 600|addr:street with suite]], Greensboro, [[NC|place:state abbreviation]] [[27401|zip]]. Bring driver's licenses.

[[Annabeth|p6:first-name]]

[[Annabeth Crowder|p6:full]] | [[Crowder Estate Planning, PLLC|o1:full]] | [[336-555-0155|phone]]

On Tue, [[Nov 4, 2025|date:quoted reply date]] at 9:58 PM Whitney Tolleson wrote:
> Annabeth - Marcus's HR sent the 401k beneficiary form and it wants names + SSNs + birthdates for the kids. I was going to put:
> [[Eli James Tolleson|p3:full:with middle name]], [[06/17/2010|dob]], [[117-88-5665|ssn]]
> [[Harper Tolleson|p4:full]], [[01/09/2013|dob]], [[734-02-3590|ssn]]
> Is that wrong for [[Eli|p3:first-name]] because of the trust? His SSI is [[$967|money]] a month and we can't lose the Medicaid waiver, [[his ABA therapy and the autism day program|health:child's diagnosis and therapy]] run through it.
> Also [[Paige|p5:first-name]] said yes to being guardian. Her cell is [[336.555.0121|phone:dotted]]. She asked if [[her DUI from college|attr:criminal history]] is a problem??
> W.
'''))

# ---------------------------------------------------------------- 335
DOCS.append(D(335, "txt", "prenuptial financial disclosure schedule", "legal", "US", cardholders=["p1", "p2"],
  title="Financial disclosure schedules exchanged before a premarital agreement",
  ents={"p1": "Soraya Mansouri", "p2": "Preston Ellery Caldecott III", "p3": "Beatriz Aldrete", "p4": "Lyle Fenstermacher",
        "p5": "Preston Ellery Caldecott Jr.",
        "o1": "Mansouri Dermatology, P.A.", "o2": "Caldecott Marine Holdings, LLC", "o3": "Biscayne Keys Private Bank",
        "o4": "Tamiami Federal Credit Union", "o5": "Aldrete Family Law"},
  distractors=["Fla. Stat. § 61.079", "SCHEDULE A", "SCHEDULE B", "Form 1040", "K-1"],
  body=r'''
EXHIBITS TO PREMARITAL AGREEMENT - FINANCIAL DISCLOSURE (Fla. Stat. § 61.079)
Parties: [[SORAYA MANSOURI|p1:caps]], M.D. ("[[Soraya|p1:first-name]]") and [[PRESTON ELLERY CALDECOTT III|p2:caps:name with suffix in caps]] ("[[Preston|p2:first-name]]")
Wedding date: [[January 17, 2026|date:wedding date]], [[Coral Gables|place:city]], [[Florida|place:state]]
Counsel: [[Beatriz Aldrete|p3:full]], [[Aldrete Family Law|o5:full]], for Soraya (file [[AFL-25-0271|rec:firm file number]]); [[Lyle Fenstermacher|p4:full]], Esq., for Preston
All values as of [[10/31/2025|date:valuation date]] unless noted. Each party has seen the other's last three Form 1040 returns.

SCHEDULE A - [[SORAYA|p1:caps:first name in caps]]                                                        approx. value
 1. Residence, [[3418 Alhambra Circle|addr]], Coral Gables [[FL|place:state abbreviation]] [[33134|zip]] (sole name)        [[$1,640,000|money]]
      mortgage, loan no. [[0091-447182|rec:mortgage loan number]]                                 [[($702,115)|money:negative amount in parentheses]]
 2. 100% of [[Mansouri Dermatology, P.A.|o1:full]], EIN [[65-4418720|taxid:EIN]] (valuation attached)       [[$2,100,000|money]]
 3. [[Biscayne Keys Private Bank|o3:full]] - checking [[x4471|acct:masked account ending]], brokerage [[BKP-7720418|acct:brokerage account number]]       [[$884,300|money]]
 4. 401(k), practice plan                                                  [[$512,000|money]]
 5. 2024 Porsche Macan, VIN [[WP1AA2A58RLB04418|veh:VIN]], tag [[SMD 77K|veh:license plate]]            [[$58,000|money]]
 6. Jewelry and art (schedule with insurer)                                [[$95,000|money]]
 Debts: medical school loans, servicer acct [[9-4418-7720-1|rec:student loan account number]]                    [[($148,600)|money:negative amount in parentheses]]
        Amex Platinum ending [[09204|card:last five of card]], paid monthly (cardholder: Soraya)       [[($11,240)|money:negative amount in parentheses]]
 2024 income per return: [[$742,880|money]]
 Other: Soraya expects [[an inheritance from her father's estate in Shiraz|indirect:expected inheritance abroad]]; amount unknown, not included.
        [[Dual U.S. and Iranian citizen|attr:citizenship / national origin]]; no accounts held outside the U.S.

SCHEDULE B - [[PRESTON|p2:caps:first name in caps]]                                                       approx. value
 1. 40% membership interest, [[Caldecott Marine Holdings, LLC|o2:full]] (family company; K-1 income)   [[$3,400,000|money]] est.
 2. Beneficial interest in the [[P.E. Caldecott Jr.|p5:short:initials, surname and suffix]] 2009 Irrevocable Trust - income only   not valued
 3. Condo, [[900 Brickell Key Blvd., Unit 2104|addr:street with unit]], [[Miami|place:city]] FL [[33131|zip]]                [[$1,150,000|money]]
 4. [[Tamiami Federal Credit Union|o4:full]] savings [[20441877-01|acct]]                              [[$41,907.63|money]]
 5. 38-ft sportfisher "[[Third Reef|indirect:named boat]]", hull no. [[SERF4418K920|veh:hull identification number]], FL reg. [[FL 4418 TK|veh:boat registration number]]   [[$210,000|money]]
 6. 2021 Ford Bronco, tag [[CALD3|veh:vanity license plate]]                                                 [[$39,500|money]]
 Debts: marine loan on item 5                                              [[($96,400)|money:negative amount in parentheses]]
        Visa ending [[7412|card:last four of card]] (cardholder: Preston), balance carried               [[($27,318.44)|money:negative amount in parentheses]]
        [[IRS installment agreement for 2021-2022, $1,850 a month|attr:tax debt]]                  [[($61,200)|money:negative amount in parentheses]]
 2024 income per return: [[$188,412|money]]
 Other: Preston [[pays $2,600 a month in child support for a daughter from a prior relationship|attr:court-ordered support obligation]]
        (case no. [[2019-DR-018842-FC-04|rec:family court case number]]). [[One DUI, 2018, adjudication withheld|attr:criminal history]] - disclosed at his counsel's request.

Acknowledged: ________________ [[S. Mansouri|p1:short:initial + surname]]   ________________ [[P. E. Caldecott III|p2:short:initials, surname and suffix]]
Questions to [[baldrete@aldretefamilylaw.example|email]] or [[305-555-0148|phone]].
'''))

# ---------------------------------------------------------------- 336
DOCS.append(D(336, "html", "petition for change of name and sex designation", "legal", "US",
  title="Draft petition for a legal change of name and sex designation",
  ents={"p1": "Daniel Joseph Przybylski", "p2": "Dana Josephine Przybylski", "p3": "Dr. Ifeoma Chukwudi",
        "p4": "Noelani Kapaona",
        "o1": "Emerald Valley Legal Aid Clinic", "o2": "McKenzie River Gender Health"},
  distractors=["ORS 33.410", "ORS 33.460", "UTCR 2.130", "CIRCUIT COURT OF THE STATE OF OREGON", "Oregon Health Plan"],
  body=r'''
# IN THE CIRCUIT COURT OF THE STATE OF OREGON FOR THE COUNTY OF [[LANE|place!:county in caps, also a common word]]
## In the Matter of the Change of Name and Sex Designation of [[DANIEL JOSEPH PRZYBYLSKI|p1:caps:name in caption]], Petitioner
Case No. [[25PB04418|rec:court case number]] · PETITION (ORS 33.410, ORS 33.460) · DRAFT [[11/10/2025|date:draft date]] — not filed
Petitioner states:
- 1. My current legal name is [[Daniel Joseph Przybylski|p1:full]]. I ask the court to change my name to [[Dana Josephine Przybylski|p2:full]].
- 2. I was born on [[September 26, 1997|dob]] in [[Toledo|place:city of birth]], [[Ohio|place:state]]. My Ohio birth certificate is file number [[1997-134418|rec:birth certificate file number]].
- 3. I live at [[2255 Kincaid Street, Apt. 9|addr:street with apartment]], [[Eugene|place:city]], [[OR|place:state abbreviation]] [[97405|zip]], and have lived in [[Lane County|place:county]] for more than six years.
- 4. I ask the court to change my legal sex designation from male to female. [[I have undergone treatment appropriate for me for the purpose of affirming my gender identity|attr:gender identity]].
- 5. I am not asking for this change to avoid debts or for any fraudulent purpose. I am not required to register as a sex offender. I have no criminal convictions.
- 6. I ask that the record of this case be sealed and that no public notice be posted, because [[I was assaulted in 2023 after a co-worker shared my former name online|indirect:past assault linked to identity]].
## Information for the court (confidential information form, UTCR 2.130)
| Item | Detail |
| Oregon driver license | [[4418720|govid!:driver license number, digits only]] |
| Social Security number (last four) | [[1229|ssn:last four digits only]] |
| Phone | [[541-555-0133|phone]] |
| Email | [[dana.j.prz@emeraldmail.example|email]] |
| Fee waiver | Requested. [[Receives SNAP and is on the Oregon Health Plan|attr:benefits status]]; monthly income [[$1,480|money]]. Filing fee [[$124|money]]. |
## Clinic notes (not part of the petition)
- Client goes by [[Dana|p2:first-name]]; do not use the former first name when calling. Voicemail is fine on the number above.
- Supporting letter requested from [[Dr. Ifeoma Chukwudi|p3:full]] at [[McKenzie River Gender Health|o2:full]] confirming [[hormone therapy since 2022|health:gender-affirming treatment]]. Not required by the statute; the client wants it for the passport application later.
- After the judgment: Social Security first, then DMV, then Ohio vital statistics for the birth certificate. Ohio will want a certified copy and [[$40|money]].
- Student loan servicer and the credit union still have "[[Danny Przybylski|p1:nickname]]". Employer payroll already uses Dana.
- Prepared by [[Noelani Kapaona|p4:full]], law student, under supervision, [[Emerald Valley Legal Aid Clinic|o1:full]]. Intake no. [[LAC-25-1187|rec:legal aid intake number]]. Hearing, if the judge wants one, is likely the week of [[December 8|date:month and day]].
'''))

# ---------------------------------------------------------------- 337
DOCS.append(D(337, "txt", "partner visa file note", "legal", "AU",
  title="Australian migration agent's file note on a partner visa application",
  ents={"p1": "Maricel Dimaunahan", "p2": "Bradley Cuthbertson", "p3": "Fiona Yeatman",
        "o1": "Yeatman Migration Services", "o2": "Moreton Bay Community Bank"},
  distractors=["subclass 820/801", "Form 888", "Form 80", "Home Affairs", "ImmiAccount", "MARA Code of Conduct"],
  body=r'''
[[Yeatman Migration Services|o1:full]] - FILE NOTE
Agent: [[Fiona Yeatman|p3:full]], MARN [[1844172|govid:migration agent registration number]]        File: [[YMS-25-0448|rec:agent file number]]
Matter: Partner visa (subclass 820/801), onshore        Note date: [[Thursday 6 November 2025|date:weekday, day, month, year]]

APPLICANT
[[Maricel Dimaunahan|p1:full]] ("[[Cel|p1:nickname]]"), DOB [[04/12/1993|dob:day-first numeric]], born [[Batangas City|place:city abroad]]. [[Philippine citizen|attr:citizenship]]. Passport [[P4418720B|govid:Philippine passport number]], exp [[11 Jan 2030|date:passport expiry]].
Currently [[on a Student visa (subclass 500) that ends 15 March 2026|attr:immigration status]]. Grant no. [[0044187720931|rec:visa grant number]].
SPONSOR
[[Bradley Cuthbertson|p2:full]] ("[[Brad|p2:nickname]]"), DOB [[22 June 1987|dob:day month year]], Australian citizen by birth. Diesel fitter, FIFO out of [[Mackay|place:city]].
Both at [[7/42 Vulture Street|addr:Australian unit/number format]], [[West End|place:suburb]] [[QLD|place:state abbreviation]] [[4101|zip:Australian postcode]] since [[1 Feb 2024|date:move-in date]] (joint lease).
[[Cel|p1:nickname]] mob [[0491 570 110|phone:Australian mobile]], [[maricel.dim93@baysidemail.example|email]]. [[Brad|p2:nickname]] mob [[0491 570 159|phone:Australian mobile]] (on site 2 weeks in 3, text first).

RELATIONSHIP EVIDENCE - where we are
- Met [[August 2022|date:month and year]] at her cousin's wedding in [[Cairns|place:city]]. Living together since the West End lease. Married [[20 September 2025|date:wedding date]] at the [[Brisbane|place:city]] registry, certificate no. [[B-2025-0441877|rec:marriage certificate number]].
- Joint account: [[Moreton Bay Community Bank|o2:full]], BSB [[124-081|rtn:Australian BSB]], acct [[2204 4187|acct:account number with a space]], opened [[March 2024|date:month and year]]. Rent [[$640|money]] a week goes from it.
- Form 888 declarations: his mum and one workmate done; need two from her side.
- Photos, travel to [[Batangas|place:province abroad]] together [[Dec 2024|date:abbreviated month and year]], shared car rego [[448 KT7|veh:Queensland registration plate]] in both names.

ISSUES TO HANDLE (discussed with both, they agree to disclose)
1. [[Cel's first marriage in the Philippines was annulled in 2021|attr:marital history]]. Need the annotated PSA marriage certificate and the court decision. This is the one Home Affairs will look at hardest.
2. Brad has [[a 2014 conviction for mid-range drink driving and a 2016 common assault (no conviction recorded)|attr:criminal history]]. Sponsor police check will show both. Not a bar, but it goes in his statement.
3. Health: Cel's medical is booked [[19/11/2025|date:day-first numeric]], HAP ID [[44187209|rec!:health examination ID]]. She is [[14 weeks pregnant|health:pregnancy]]; chest x-ray can be deferred or done with shielding. Her Medicare (interim card) no. [[6044 18772 1|govid:Medicare card number]].
4. Form 80 gaps: she [[worked cash-in-hand at a nail salon for 5 months in 2023|indirect:undeclared work history]]. Advised on the 48 hrs/fortnight condition. My advice recorded; MARA Code of Conduct obligations explained.

LODGEMENT
- ImmiAccount created under her email. Username [[mdimaunahan93|cred:government portal user name]], password [[Kalabaw!2025|cred:government portal password]] (she will change it after lodgement). TRN [[EGOX4418K7|rec:transaction reference number]].
- Draft application saved at [[https://online.immi.example/lusc/app/EGOX4418K7|url:link to the draft application]]. Last session from her home IP, [[203.0.113.9|ip]].
- Visa application charge [[$9,365|money]], to be paid on Brad's card. My fee [[$4,400|money]] incl GST: [[$2,200|money]] received [[30/10|date:day/month only]], balance on lodgement.
- Target lodgement [[by 28 Nov|date:deadline, day and abbreviated month]] so the bridging visa is in place well before the student visa ends.   [[FY|p3:initials]]
'''))

# ---------------------------------------------------------------- 338
DOCS.append(D(338, "rtf", "nonprofit board minutes", "legal", "US",
  title="Minutes of a small historical society's board meeting, including an executive session",
  ents={"p1": "Eudora Pennywell", "p2": "Lamar Whisenhunt", "p3": "Constance Abegunde", "p4": "Rev. Silas Trotter",
        "p5": "Joaquín Membreño", "p6": "Nettie Pennywell-Ross",
        "o1": "Tuckahoe Creek Historical Society, Inc.", "o2": "Choptank Farmers & Merchants Bank",
        "o3": "Delmarva Heritage Foundation"},
  distractors=["Form 990-EZ", "Article IV", "Maryland Historical Trust"],
  body=r'''
# [[Tuckahoe Creek Historical Society, Inc.|o1:full]]
## Minutes of the regular meeting of the Board of Directors — [[Tuesday, November 11, 2025|date:meeting date]]
Held at the [[Old Mill Schoolhouse|place:named building]], [[114 Gay Street|addr]], [[Denton|place:town]], [[Maryland|place:state]]. Called to order at 7:02 p.m. by the president, [[Lamar Whisenhunt|p2:full]].
**Present:** [[L. Whisenhunt|p2:short:initial + surname]]; [[Constance Abegunde|p3:full]], treasurer; [[Rev. Silas Trotter|p4:full]]; [[Joaquín Membreño|p5:full]], secretary; [[Miss Eudora Pennywell|p1:full:with honorific]], founding member. **Absent:** two directors (excused). A quorum was present under Article IV of the bylaws.
## 1. Recognition
The president noted that [[Miss Pennywell|p1:title-surname]], who founded the Society in 1971, [[turned one hundred and one|age:age in words]] on [[October 28|date:birthday, month and day]]. The board stood. She thanked everyone and said she intends to keep cataloguing "until the Lord or the mice stop me."
## 2. Minutes
Minutes of [[September 9|date:prior meeting date]] approved as circulated ([[Trotter|p4:surname]] / [[Abegunde|p3:surname]]).
## 3. Treasurer's report
- Operating account at [[Choptank Farmers & Merchants Bank|o2:full]] ending [[2218|acct:last four of account]]: [[$14,206.77|money]] at [[October 31|date:month-end date]].
- Building fund certificate of deposit no. [[40-0044187|acct:certificate of deposit number]]: [[$61,340.00|money]], matures [[2/15/2026|date:maturity date]].
- Grant from the [[Delmarva Heritage Foundation|o3:full]], [[$12,500|money]], received [[10/20|date:month/day only]] for the roof. A matching request to the Maryland Historical Trust is pending.
- Form 990-EZ for the fiscal year was filed on time. EIN [[52-4418720|taxid:EIN]].
- [[Ms. Abegunde|p3:title-surname]] reported that check no. [[1187|rec!:check number]] for [[$2,400|money]] to the roofer was signed by one officer only. Motion that all checks over [[$1,000|money]] carry two signatures from now on; carried unanimously.
## 4. Signers on the bank account
Resolved: remove the former treasurer as signer; add [[Constance Abegunde|p3:full]] and [[Joaquín Membreño|p5:full]]; keep Lamar Whisenhunt. The bank requires each signer's date of birth and Social Security number; the secretary will deliver these by hand rather than email. Online banking user name [[tchs_treasurer|cred:online banking user name]] to be reset by the bank.
## 5. Gift of the [[Pennywell|p1:surname]] papers
[[Nettie Pennywell-Ross|p6:full]], Miss Pennywell's great-niece and agent under her power of attorney, has offered the family papers and the house at [[309 Franklin Street|addr]] as a bequest. The board accepted with thanks. [[Mrs. Pennywell-Ross|p6:title-surname]] can be reached at [[410-555-0127|phone]] or [[nettie.pross@shoremail.example|email]]. Appraisal budget not to exceed [[$1,800|money]].
## 6. Executive session (7:48 to 8:15 p.m.; staff excused)
The board discussed a personnel matter. The part-time director has asked for unpaid leave from [[December 1|date:leave start]] through [[February 27, 2026|date:leave end]] [[for cancer treatment|health:reason for leave]]. Granted; her health insurance stipend of [[$350|money]] a month will continue. [[Rev. Trotter|p4:title-surname]] will tell the volunteers only that she is on leave. The board also heard that a volunteer docent [[is listed on the state sex offender registry|attr:criminal history]]; he will no longer lead school tours, and the president will speak with him privately.
## 7. Adjournment
Adjourned at 8:22 p.m. Next meeting [[January 13, 2026|date:next meeting date]].
Respectfully submitted, [[J. Membreño|p5:short:initial + surname]], Secretary
'''))

# ---------------------------------------------------------------- 339
DOCS.append(D(339, "xlsx", "estate accounting ledger", "legal", "US", cardholders=["p2", "p1"],
  title="Executor's estate accounting: receipts, disbursements and proposed distribution",
  ents={"p1": "Mabel Jean Stooksbury", "p2": "Carolyn Stooksbury Leach", "p3": "Dwight Stooksbury", "p4": "Ronnie Dale Stooksbury",
        "p5": "Faye Killebrew",
        "o1": "Clinch Valley Bank & Trust", "o2": "Killebrew Law Office", "o3": "Norris Lake Funeral Home",
        "o4": "Powell Valley Electric Cooperative", "o5": "Hiwassee Hospice Care"},
  distractors=["Tenn. Code Ann. § 30-2-601", "Form 1040", "Form 56", "TennCare Estate Recovery"],
  sheets=[
    ("Summary", [
      ["ESTATE OF [[MABEL JEAN STOOKSBURY|p1:caps:name in caption]], DECEASED"],
      ["Probate no.", "[[2025-PR-0418|rec:probate case number]]", "Court", "Chancery Court, [[Anderson County|place:county]], [[Tennessee|place:state]]"],
      ["Date of death", dt("2025-02-19", "mmmm d, yyyy", "date:date of death"), "Decedent's SSN", "[[527-25-0259|ssn]]"],
      ["Executor", "[[Carolyn Stooksbury Leach|p2:full]]", "Attorney", "[[Faye Killebrew|p5:full]], [[Killebrew Law Office|o2:full]], [[865-555-0115|phone]]"],
      ["Estate EIN", "[[92-4418720|taxid:EIN]]", "Estate account", "[[Clinch Valley Bank & Trust|o1:full]] [[0077204418|acct]]"],
      ["Accounting period", dt("2025-02-19", "m/d/yy", "date:period start"), "to", dt("2025-10-31", "m/d/yy", "date:period end")],
      ["Total receipts", amt(287412.66)],
      ["Total disbursements", amt(41906.18)],
      ["Balance for distribution", amt(245506.48)],
    ]),
    ("Receipts", [
      ["Date", "Source", "Description", "Amount"],
      [dt("2025-03-04", "m/d/yy"), "[[Clinch Valley|o1:short]] checking [[x3391|acct:masked account ending]]", "Decedent's account closed to estate", amt(18204.11)],
      [dt("2025-03-04", "m/d/yy"), "Clinch Valley CD [[55-20441|acct:certificate of deposit number]]", "Redeemed, incl. interest", amt(52318.40)],
      [dt("2025-04-22", "m/d/yy"), "Sale of 2015 Buick LaCrosse", "VIN [[1G4GB5G39FF204418|veh:VIN]], sold to [[Ronnie Dale|p4:first-name:double given name]] at book value", amt(8900.00)],
      [dt("2025-06-30", "m/d/yy"), "Sale of house, [[418 Sinking Springs Rd|addr]], [[Clinton|place!:town that is also a surname]] [[TN|place:state abbreviation]] [[37716|zip]]", "Net of closing costs; deed book ref [[1644/209|rec:deed book and page]]", amt(204750.00)],
      [dt("2025-07-15", "m/d/yy"), "[[Powell Valley Electric Cooperative|o4:full]]", "Capital credits refund, member no. [[441877|rec!:cooperative member number]]", amt(312.15)],
      [dt("2025-08-01", "m/d/yy"), "U.S. Treasury", "Final Form 1040 refund", amt(2928.00)],
    ]),
    ("Disbursements", [
      ["Date", "Payee", "Description", "Check / method", "Amount"],
      [dt("2025-02-27", "m/d/yy"), "[[Norris Lake Funeral Home|o3:full]]", "Funeral, contract [[NL-25-0188|rec:funeral contract number]]", "paid by [[Carolyn|p2:first-name]] on her own Visa ending [[8801|card:last four of card]]; reimbursed ck [[1001|rec!:check number]]", amt(9870.00)],
      [dt("2025-03-10", "m/d/yy"), "[[Hiwassee Hospice Care|o5:full]]", "Final bill, patient acct [[CGH-20441|rec:patient account number]]", "ck [[1002|rec!:check number]]", amt(1244.60)],
      [dt("2025-03-10", "m/d/yy"), "Card issuer", "Decedent's Mastercard ending [[1078|card:last four of card]], balance at death", "ck [[1003|rec!:check number]]", amt(3316.92)],
      [dt("2025-05-05", "m/d/yy"), "TennCare Estate Recovery", "Claim for [[nursing home care paid by Medicaid, 2023-2025|attr:benefits status of the decedent]], settled (Tenn. Code Ann. § 30-2-601)", "ck [[1006|rec!:check number]]", amt(14500.00)],
      [dt("2025-06-02", "m/d/yy"), "Killebrew Law Office", "Fees and costs to date, invoice [[KLO-2291|rec:invoice number]]", "ck [[1007|rec!:check number]]", amt(6850.00)],
      [dt("2025-09-12", "m/d/yy"), "[[Dwight Stooksbury|p3:full]]", "Repay loan he made to Mother in 2022 (note in file)", "ck [[1011|rec!:check number]]", amt(5000.00)],
      [dt("2025-10-20", "m/d/yy"), "Carolyn Stooksbury Leach", "Executor's mileage and postage", "ck [[1012|rec!:check number]]", amt(1124.66)],
    ]),
    ("Distribution", [
      ["Beneficiary", "Relationship", "Share", "Amount", "Address", "SSN", "Notes"],
      ["[[Leach, Carolyn S.|p2:last-first]]", "daughter", "1/3", amt(81835.50), "[[2204 Edgemoor Rd|addr]], [[Powell|place!:town that is also a surname]] TN [[37849|zip]]", "[[892-16-2710|ssn]]", "also executor"],
      ["[[Stooksbury, Dwight|p3:last-first]]", "son", "1/3", amt(81835.49), "[[77 Mariner Point Dr|addr]], Clinton TN", "[[023-91-7897|ssn]]", ""],
      ["[[Stooksbury, Ronnie Dale|p4:last-first]]", "son", "1/3", amt(81835.49), "c/o Carolyn", "[[xxx-xx-9764|ssn:masked, lower-case x]]", "[[currently incarcerated at the county detention facility; release expected March 2026|attr:incarceration]]. Share to be held, less the [[$8,900|money]] car purchase he has not paid."],
      ["Prepared for the hearing on", dt("2025-11-24", "mmmm d, yyyy", "date:hearing date"), "", "", "", "", "[[Ms. Killebrew|p5:title-surname]] to file Form 56 release"],
    ]),
  ]))

# ---------------------------------------------------------------- 340
DOCS.append(D(340, "txt", "jail visit notes", "legal", "US",
  title="Defender investigator's hurried notes from a jail visit",
  ents={"p1": "Tyrese M. Goodwine", "p2": "Shanice Albury", "p3": "Deandre Polite", "p4": "Ofc. Mulvaney-Luz",
        "p5": "Ms. Hyacinth",
        "o1": "Ashley River Tire & Lube"},
  distractors=["rule 5", "form 4.01", "ROR"],
  ok=[],
  body=r'''
jail visit [[11/8|date:month/day only]] 2:10pm - pod C - abt 35 min. notes rough, will clean up monday

client: [[tyrese m. goodwine|p1:full!:lower case]], goes by [[reese|p1:nickname!:lower case]]. dob [[5/30/01|dob:short numeric]]. booking # [[2025-0044187|rec:jail booking number]]
arrested [[thurs 11/6|date:weekday and month/day, lower case]] abt 11pm, traffic stop on [[rivers ave|addr!:street name only, lower case]] near the walmart. arresting [[ofc mulvaney-luz|p4:title-surname!:lower case, abbreviated rank]] badge [[4418|rec!:badge number]]
charges: poss w/ intent (cocaine, "28 grams" per warrant), unlawful carry. warrants [[2025A1010204418|rec:arrest warrant number]] and [[...419|rec:partial warrant number]]
bond set at [[$75,000|money]] surety at the hearing fri am. family cant make it. mom has maybe [[2 grand|money:amount in slang]]. ask abt ROR / bond reduction motion - rule 5 wasnt read to him he says

his version:
- car isnt his. its [[shanices|p2:first-name!:lower case possessive without apostrophe]] - girlfriend - [[shanice albury|p2:full!:lower case]] - silver altima tag [[TKR 418|veh:license plate]] ([[SC|place:state abbreviation]]). he borrowed it to get to work
- works at [[ashley river tire & lube|o1:full!:lower case]] on [[dorchester rd|addr!:street name only, lower case]], 2nd shift, clocked out 10:30. boss is "[[mr. ray|indirect:supervisor known only by first name with title]]". GET TIMECARD
- bag was under pass. seat. says its [[deandre|p3:first-name!:lower case]]'s - [[deandre polite|p3:full!:lower case]] aka "[[dre|p3:nickname!:lower case]]" - shanices cousin - who had the car all day weds. [[dre|p3:nickname!:lower case]] is [[on federal probation|attr:criminal supervision status of a third party]] so nobody wants to say it
- gun: says he never saw it. glovebox was locked, shanice has the only key??
- cops searched w/o asking. bodycam should show. no consent form 4.01 signed

priors (he says): [[juvie adjudication 2017 (joyriding)|attr:juvenile record]], [[simple possession 2021 - PTI completed|attr:criminal history]]. nothing violent. CHECK NCIC

health: [[type 1 diabetic|health:condition]]. [[jail hasnt given him insulin since booking|health:medication need]] - nurse said "tomorrow" twice. he looked bad. CALL MEDICAL TODAY. also [[takes lexapro|health:medication]]
family: lives w/ his grandmother, [[ms. hyacinth|p5:title-surname!:lower case, title with first name]], [[2204 ranger dr apt b|addr:lower case, with apartment]] [[n. charleston|place!:city abbreviated, lower case]] [[29405|zip]]. [[she's 90 and he does her shopping|indirect:elderly relative who depends on the client]] - use for bond motion
phones: [[shanice|p2:first-name!:lower case]] [[843-555-0170|phone]]. grandmother landline [[843 555 0104|phone:spaces only]]. his phone was seized - passcode is [[053001|cred:phone passcode]] IF we decide to consent to a dump (dont yet)
his cashapp shows he got paid [[$412|money]] thurs - explains the cash on him ([[$388|money]])

next: prelim [[12/4|date:month/day only]] 9am courtroom 2B. bond motion asap. subpoena tire shop cameras before they overwrite (7 days!!)
'''))
