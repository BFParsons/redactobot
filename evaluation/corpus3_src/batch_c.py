from corpus3_src.core import D, dt, amt, num

DOCS = []

# ---------------------------------------------------------------- 321
DOCS.append(D(321, "txt", "workplace investigation interview notes", "general", "US", length="long",
  title="Outside HR consultant's interview notes in a harassment investigation",
  ents={"p1": "Loretta Hsieh", "p2": "Imani Braxton-Reid", "p3": "Douglas Krantz", "p4": "Feliciano Manalastas",
        "p5": "Bree Tolbert", "p6": "Ansel Corrigan", "p7": "Zoran Milićević",
        "o1": "Plainspoken HR Consulting", "o2": "Cobblestone Brewing Supply Co."},
  distractors=["Title VII", "Policy 4.2", "Upjohn", "OSHA"],
  body=r'''
[[Plainspoken HR Consulting|o1:full]] - INVESTIGATION WORKING NOTES - PRIVILEGED AT DIRECTION OF COUNSEL
Client: [[Cobblestone Brewing Supply Co.|o2:full]], [[Asheville|place:city]] warehouse      Matter no. [[PHR-25-031|rec:investigation matter number]]
Investigator: [[Loretta Hsieh|p1:full]], SPHR       Notes typed same day from handwritten; quotes are as close as I could get them.

COMPLAINT RECEIVED [[10/27/25|date:short numeric date]] via the ethics line (ticket [[EL-00418|rec:ethics hotline ticket]]). Complainant [[Imani Braxton-Reid|p2:full]], inventory lead, emp. ID [[20771|rec!:employee ID]], hired [[March 2021|date:month and year]].
Respondent [[Douglas Krantz|p3:full]] ("[[Dougie|p3:nickname]]"), second-shift warehouse supervisor, emp. ID [[10388|rec!:employee ID]], with the company 14 yrs.
Policy at issue: Policy 4.2 (harassment), Title VII categories religion / sex / sexual orientation.

--- INTERVIEW 1: [[I. Braxton-Reid|p2:short:initial + surname]], [[Mon. Nov 3|date:weekday and abbreviated month/day]], 9:05-10:20, conf. room B. Gave Upjohn-style notice; she declined to have anyone with her.

- [[Imani|p2:first-name]] says it started in August after she began wearing a hijab to work. She [[converted to Islam last spring|attr:religion]]. Before that, she says, [[Krantz|p3:surname]] "was fine with me."
- First incident she can date: [[Aug. 19|date:abbreviated month and day]], shift huddle. Krantz allegedly said "is that thing OSHA approved?" and tugged at the back of the scarf. Others laughed. She told him not to touch her.
- [[9/11|date:month/day only]]: he said over the radio, "somebody keep an eye on [[Imani|p2:first-name]] today." She says at least six people were on channel 2.
- Since then he calls her "[[Sister Mary|p2:nickname:mocking nickname used by the respondent]]" in front of the crew. She has asked him to stop twice.
- [[10/24|date:month/day only]] (the Friday before she called the line): she asked for the small office for five minutes to pray. He said, "You can pray on your own time, this isn't a mosque," and wrote her up for an unauthorized break the same afternoon. I have the write-up (form dated 10/24, signed [[D. Krantz|p3:short:initial + surname]]).
- She also raised, without my asking, how he treats [[Feliciano Manalastas|p4:full]] on the dock. She says Krantz calls him "princess" and once said he "didn't want [[Chano|p4:nickname]] in the locker room with the guys." She says [[Chano|p4:nickname]] [[is gay and not out to most people at work|attr:sexual orientation]], and she is worried she has now outed him to me. I told her I would handle that carefully.
- Effect on her: not sleeping; [[her doctor put her on sertraline in October|health:medication for anxiety]]; she has used four sick days. She is looking at other jobs.
- Wants: for it to stop, the write-up removed, and not to be moved off second shift ([[she shares custody and the schedule is built around it|indirect:family circumstances]]).
- Personal cell for follow-up, NOT work email: [[828-555-0173|phone]], [[imani.breid@blueridgemail.example|email]].

--- INTERVIEW 2: [[Bree Tolbert|p5:full]], picker, [[11/3|date:month/day only]], 10:40-11:05

- Was at the Aug. 19 huddle. Confirms the "OSHA approved" remark and that he "kind of flicked" the scarf. "Everybody laughed because it's [[Dougie|p3:nickname]], that's how he is."
- Has heard "Sister Mary" "a bunch." Did not hear the radio comment.
- Asked whether she has seen him treat others differently: long pause. "He rides Chano pretty hard. I don't want to say why."
- [[Bree|p5:first-name]] is nervous. [[She is Krantz's niece by marriage|indirect:family relationship to the respondent]] and asked me three times who would see these notes.

--- INTERVIEW 3: [[F. Manalastas|p4:short:initial + surname]], [[Tues. 11/4|date:weekday and month/day]], 14:00-14:35, by phone at his request ([[828.555.0109|phone:dotted]])

- Did not want to be interviewed. Says he "has no complaint." Confirms "princess." Says it "doesn't bother him."
- On the locker room remark: "Who told you that?" then, after a while, "Yeah. He said it. In July."
- Volunteered that [[he is here on a green card through his husband|attr:immigration status and same-sex marriage]] and "cannot afford trouble." I told him retaliation is prohibited and gave him my direct line.
- He overheard the radio comment on 9/11 and says [[Zoran Milićević|p7:full]] (maintenance) said on the channel, "Not cool, [[Doug|p3:nickname]]."

--- INTERVIEW 4: [[Douglas Krantz|p3:full]], [[Wed. Nov. 5|date:weekday and abbreviated month/day]], 15:30-16:50. [[Ansel Corrigan|p6:full]] (HR manager) sat in.

- Denies touching the scarf. "I pointed at it." Says the OSHA comment was a real question about loose clothing near the conveyor.
- "Sister Mary": admits it. "It's a joke. She used to laugh." Could not say when she last laughed.
- Radio comment: "I say that about everybody." Could not name another person he has said it about.
- The 10/24 write-up: says she had already had both breaks. Time-clock report shows one break that day, not two. He had no answer.
- "Princess": "That's just dock talk." Locker room remark: denies it flatly.
- Raised his own issues: says he has been under strain, [[his wife is in chemo|health:spouse's cancer treatment]], and he is "[[six years sober|health:addiction recovery]] and not about to lose this job over a nickname."
- File check with [[Mr. Corrigan|p6:title-surname]] afterwards: Krantz has [[a written warning from 2022 for a comment about a Hispanic temp's accent|attr:prior disciplinary record]]. He did not mention it when I asked about prior discipline.

PRELIMINARY VIEW (for counsel only): the complainant is credible and largely corroborated. Recommend removing the 10/24 write-up now, separating reporting lines pending findings, and no contact between Krantz and either witness. Draft report to [[Ansel|p6:first-name]] by [[November 14|date:deadline]]. Fee to date [[$4,275|money]] (22.5 hrs at [[$190|money:hourly rate]]).
[[LH|p1:initials]]
'''))

# ---------------------------------------------------------------- 322
DOCS.append(D(322, "docx", "termination letter", "general", "US",
  title="Termination letter with final pay, benefits and return of company property",
  ents={"p1": "Rosendo Villalpando", "p2": "Kimberly Stang", "p3": "Marvin Oglesby",
        "o1": "Halberd Aerospace Fasteners, Inc.", "o2": "Wheatland Benefit Administrators", "o3": "Chisholm Trail 401(k) Trust"},
  distractors=["COBRA", "49 CFR Part 40", "K.S.A. 44-315", "Form W-2", "Section 6.3"],
  header="[[Halberd Aerospace Fasteners, Inc.|o1:full]] — Human Resources — CONFIDENTIAL PERSONNEL RECORD",
  body=r'''
# [[Halberd Aerospace Fasteners, Inc.|o1:full]]
[[4400 South Hydraulic Avenue|addr]], [[Wichita|place:city]], [[Kansas|place:state]] [[67216|zip]]
[[November 7, 2025|date:letter date]]
**Hand-delivered and by certified mail**
[[Rosendo Villalpando|p1:full]]
[[1729 N. Minneola St.|addr]]
Wichita, [[KS|place:state abbreviation]] [[67203|zip]]
Employee no. [[HAF-06617|rec:employee number]]
Dear [[Mr. Villalpando|p1:title-surname]]:
This letter confirms that your employment with [[Halberd|o1:short]] as a Route Driver ends effective today, [[11/07/2025|date:termination date]].
## Reason
On [[October 29|date:month and day]] you were involved in a collision in the company yard while driving truck no. 14. Under Section 6.3 of the handbook and 49 CFR Part 40 you were sent for post-accident testing. The medical review officer reported [[a verified positive result for amphetamines|health:drug test result]] on [[November 4|date:month and day]]. You told [[Marvin Oglesby|p3:full]], your supervisor, that [[you take a prescription for ADHD|health:condition and medication]]; the MRO did not receive documentation of a valid prescription within the time allowed. A positive result is a terminable offense for safety-sensitive positions.
## Final pay
- Wages through today: [[$1,286.40|money]] gross, paid on the regular payday, [[November 14|date:pay date]], as required by K.S.A. 44-315.
- Accrued vacation, 46.5 hours at [[$26.80|money:hourly rate]]: [[$1,246.20|money]].
- Less the balance of your uniform account: [[($88.00)|money:negative amount in parentheses]].
- Direct deposit will go to the account on file ending [[8852|acct:last four of account]]. Your Form W-2 will be mailed in January to the address above.
## Benefits
Medical and dental coverage ends [[11/30/25|date:coverage end date]]. [[Wheatland Benefit Administrators|o2:full]] will send your COBRA notice; your member ID is [[FH-774120-01|rec:health plan member ID]]. Your account with the [[Chisholm Trail 401(k) Trust|o3:full]] (participant no. [[P-0044187|rec:retirement plan participant number]]) is fully vested; the outstanding loan balance of [[$3,412.77|money]] becomes due.
## Company property to return by [[November 12|date:deadline]]
| Item | Identifier |
| Laptop, Dell Latitude | Service tag [[7HK2QW3|dev:laptop service tag]] |
| Phone, iPhone 13 | IMEI [[356979695221510|dev:IMEI]] |
| Access badge | No. [[00418-B|dev:access badge number]] |
| Fuel card | ending [[4417|card:last four of fuel card]] |
| Truck no. 14 keys | 2022 Ford F-250, VIN [[1FT7W2BT4NEC41877|veh:VIN]], tag [[KS 447 PLM|veh:license plate with state prefix]] |
Your network account ([[rvillalpando|cred:network user name]]) was disabled at 8:00 this morning.
## Other
You remain bound by the confidentiality agreement you signed on [[June 3, 2019|date:agreement date]]. We will confirm only dates of employment and job title to prospective employers. We will not contest a claim for unemployment benefits, but we will report the reason for separation truthfully if asked.
Questions may be directed to me at [[316-555-0128|phone]] or [[kstang@halberdfasteners.example|email]].
Sincerely,
[[Kimberly Stang|p2:full]], Director of Human Resources
cc: personnel file; [[M. Oglesby|p3:short:initial + surname]]
'''))

# ---------------------------------------------------------------- 323
DOCS.append(D(323, "eml", "accommodation request email thread", "general", "CA", enc="multipart",
  title="Bilingual workplace accommodation thread at a Quebec employer",
  ents={"p1": "Marie-Ève Dandurand", "p2": "Olumide Fasanya", "p3": "Réjean Thériault", "p4": "Dre Anouk Villemure",
        "o1": "Textiles Beauharnois ltée", "o2": "Syndicat des travailleuses et travailleurs de Textiles Beauharnois"},
  distractors=["Charte des droits et libertés de la personne", "article 10"],
  headers={"From": "[[Olumide Fasanya|p2:full]] <[[ofasanya@textilesbeauharnois.example|email]]>",
           "To": "[[Marie-Eve Dandurand|p1:full:without the accent]] <[[medandurand@textilesbeauharnois.example|email]]>",
           "Cc": "[[Rejean Theriault|p3:full:without accents]] <[[rtheriault@sttb.example|email]]>",
           "Subject": "RE: Demande d'accommodement / Accommodation request - dossier [[RH-2025-0612|rec:HR file number]]",
           "Date": "Fri, [[7 Nov 2025|date:email header date]] 14:22:10 -0500"},
  body=r'''
Bonjour [[Marie-Ève|p1:first-name]],

(English follows, since [[Réjean|p3:first-name]] asked that the union's file be bilingual.)

Merci pour le certificat de la [[Dre Villemure|p4:title-surname:French honorific for a female doctor]] daté du [[30 octobre 2025|date:French long date]]. Nous acceptons les limitations suivantes à compter du [[lundi 17 novembre|date:French weekday, day and month]] :
- quart de jour seulement (7 h à 15 h), pas de rotation;
- pas plus de 4 heures debout par quart;
- deux jours de télétravail par semaine pour les tâches de planification.

In English: we accept the restrictions in [[Dr. Villemure|p4:title-surname]]'s note. You move to the planning desk on days, with two remote days a week. Your rate stays at [[31,85 $|money:French-Canadian format, decimal comma]] an hour. We will review on [[2026-02-16|date:ISO date]].

Two things I still need:
1. The insurer's form for the short-term disability top-up. Your certificate number is [[TB-004418-07|rec:group insurance certificate number]].
2. Confirmation of the address for the ergonomic chair delivery: is it still [[218, rue Ellice|addr:French-Canadian address, comma after number]], [[Salaberry-de-Valleyfield|place:city]] ([[Québec|place:province]]) [[J6T 1E9|zip:Canadian postal code]]?

I have not shared your diagnosis with your supervisor, only the restrictions.

[[Olumide Fasanya|p2:full]]
Conseiller, ressources humaines / HR Advisor
[[Textiles Beauharnois ltée|o1:full]] | [[450 555-0136|phone:Quebec style, space after area code]], poste 214

-----Message d'origine-----
De : Marie-Ève Dandurand
Envoyé : [[4 novembre 2025|date:French long date]] 20:51
À : Olumide Fasanya
Cc : [[Réjean Thériault|p3:full]] ([[Syndicat des travailleuses et travailleurs de Textiles Beauharnois|o2:full]])
Objet : Demande d'accommodement

Bonjour [[M. Fasanya|p2:title-surname:French honorific]],

Comme discuté avec [[Réjean|p3:first-name]], mon [[délégué syndical|attr:union representation]], je demande un accommodement en vertu de l'article 10 de la Charte des droits et libertés de la personne. [[J'ai reçu un diagnostic de sclérose en plaques|health:diagnosis, in French]] en septembre. [[La fatigue et les engourdissements dans les jambes|health:symptoms, in French]] rendent le quart de nuit impossible pour le moment. Ma neurologue est la [[Dre Anouk Villemure|p4:full]] (clinique de [[Châteauguay|place:city]], [[450-555-0190|phone]]); elle peut vous parler si je signe le consentement.

Pour le formulaire : matricule [[04417|rec!:employee number]], date de naissance [[1988-05-21|dob:ISO date]], numéro d'assurance maladie [[DANM 8855 2114|govid:Quebec health insurance number]]. Mon cell : [[450 555-0177|phone:Quebec style, space after area code]].

Je préfère que mes collègues ne soient pas mis au courant.

Merci,
[[Marie-Ève Dandurand|p1:full]]
Opératrice, atelier de tissage
'''))

# ---------------------------------------------------------------- 324
DOCS.append(D(324, "txt", "disciplinary hearing minutes", "general", "UK",
  title="Minutes of a disciplinary hearing at a UK coach operator",
  ents={"p1": "Gareth Moxon", "p2": "Shabnam Akhtar", "p3": "Lorna Peat", "p4": "Derek Ainscough",
        "o1": "Wharfedale Coachlines Ltd", "o2": "Unite the Union"},
  distractors=["ACAS Code of Practice", "DVLA", "D4 medical", "Driver CPC", "Rehabilitation of Offenders Act 1974"],
  body=r'''
[[WHARFEDALE COACHLINES LTD|o1:caps]]
MINUTES OF DISCIPLINARY HEARING - STRICTLY CONFIDENTIAL

Held at the depot, [[Unit 6, Snaygill Industrial Estate|addr:unit and estate]], [[Skipton|place:town]] [[BD23 2QR|zip:UK postcode]], on [[Thursday 6th November 2025|date:weekday, ordinal day, month, year]] at 10.00am.

Present:  [[Shabnam Akhtar|p2:full]], Operations Manager (chair)
          [[Gareth Moxon|p1:full]], PCV driver, payroll no. [[W0417|rec:payroll number]]
          [[Derek Ainscough|p4:full]], [[Unite the Union|o2:full]] branch rep (companion)
          [[Lorna Peat|p3:full]], HR Administrator (notes)

1. [[SA|p2:initials]] opened the hearing and confirmed [[GM|p1:initials]] had received the invite letter of [[29/10/25|date:day-first short date]] and the investigation pack. The hearing follows the ACAS Code of Practice.

2. Allegations
(a) That GM failed to tell the company about [[a conviction for drink-driving at Bradford Magistrates' Court in March 2019|attr:criminal conviction]] when he applied in 2022, and answered "No" to the convictions question on the application form.
(b) That on [[14 October 2025|date:incident date]] he drove vehicle [[YX19 KLO|veh:UK registration plate]] on the [[Ilkley|place:town]] school contract for 40 minutes beyond his permitted driving time (tachograph card [[DB04417712300010|dev:tachograph driver card number]]).

3. GM's response
(a) GM said the ban was 12 months, ended in 2020, and he believed it was "spent". [[DA|p4:initials]] referred to the Rehabilitation of Offenders Act 1974. SA said the form asks about any endorsement in the last five years and that the insurer must be told regardless. GM accepted he should have asked. His licence, no. [[MOXON710153G99LD|govid:UK driving licence number]], now shows no points.
(b) GM said the relief driver did not turn up at [[Addingham|place:village]] and he could not leave 31 children on the roadside. He rang the depot on [[01632 960122|phone:UK landline]] twice and nobody picked up. SA confirmed the call log shows two missed calls from [[07700 900164|phone:UK mobile]] at 15.52 and 15.58.

4. Mitigation
[[Mr Ainscough|p4:title-surname]] said GM has three years' clean service. He asked the company to take into account that GM was [[diagnosed with sleep apnoea in the summer and now uses a CPAP machine|health:diagnosis and treatment]]; DVLA were notified and his D4 medical was passed on [[2 September|date:day and month]]. GM added that [[his wife left in August and he has the two boys on his own|indirect:family circumstances]], which is why he had been swapping shifts.

5. Adjournment 10.48 to 11.20.

6. Decision
(a) Upheld. Final written warning, live for 12 months from today. GM to complete a new declaration; the insurer will be informed and any extra premium is the company's cost.
(b) Not upheld as misconduct. Depot phone cover to be reviewed.
GM's pay is unaffected ([[£15.90|money:hourly rate in pounds]] per hour). The [[£250|money:pounds]] Driver CPC training deduction agreed in July stands.

7. Appeal: in writing to the Managing Director within five working days, i.e. by [[13/11/2025|date:day-first numeric]]. Outcome letter to GM's home address, [[41 Gargrave Road|addr]], Skipton [[BD23 1PJ|zip:UK postcode]], and by email to [[gaz.moxon71@dalesmail.example|email]].

Notes taken by [[L. Peat|p3:short:initial + surname]]. [[Gareth|p1:first-name]]'s date of birth for the insurer's form: [[15.01.1971|dob:dotted day-first]]. NI no. [[NH 44 71 82 D|taxid:UK National Insurance number]].
'''))

# ---------------------------------------------------------------- 325
DOCS.append(D(325, "xlsx", "benefits enrollment census", "general", "US",
  minors=["p7", "p8", "p10"],
  title="Group health enrollment census with dependents and retirees",
  ents={"p1": "Marcus Oyelaja", "p2": "Siobhan Kilgallen", "p3": "Hyun-woo Baik", "p4": "Teresa Montalvo-Ruelas",
        "p5": "Wendell Purifoy", "p6": "Adunni Oyelaja", "p7": "Tobi Oyelaja", "p8": "Fiadh Kilgallen",
        "p9": "Jonas Kilgallen-Weir", "p10": "Mateo Ruelas", "p11": "Ottoline Purifoy",
        "o1": "Greenhow Printing & Packaging Co.", "o2": "Unison Benefit Brokers", "o3": "Calibrate Health PPO"},
  distractors=["HDHP 3200", "PPO 500", "Section 125"],
  sheets=[
    ("Census", [
      ["Group", "[[Greenhow Printing & Packaging Co.|o1:full]]", "Group no.", "[[G-0044187|rec:group number]]", "Carrier", "[[Calibrate Health PPO|o3:full]]", "Broker", "[[Unison Benefit Brokers|o2:full]]", "Renewal", dt("2026-01-01", "m/d/yyyy", "date:renewal date")],
      ["Emp ID", "Last", "First", "SSN", "DOB", "Sex", "Hire date", "Annual salary", "Plan", "Tier", "ZIP", "Home email"],
      ["[[GP-1004|rec:employee ID]]", "[[Oyelaja|p1:surname]]", "[[Marcus|p1:first-name]]", "[[175-63-5647|ssn]]", dt("1981-07-19", "mm/dd/yyyy", "dob"), "M", dt("2014-09-08", "mm/dd/yyyy", "date:hire date"), amt(84500, "usd0"), "PPO 500", "EE+Family", "[[30310|zip]]", "[[marcus.oyelaja@peachmail.example|email]]"],
      ["[[GP-1019|rec:employee ID]]", "[[Kilgallen|p2:surname]]", "[[Siobhan|p2:first-name]]", "[[594-02-0219|ssn]]", dt("1976-03-02", "mm/dd/yyyy", "dob"), "F", dt("2008-02-11", "mm/dd/yyyy", "date:hire date"), amt(97250, "usd0"), "PPO 500", "EE+Family", "[[30030|zip]]", "[[skilgallen76@peachmail.example|email]]"],
      ["[[GP-1033|rec:employee ID]]", "[[Baik|p3:surname]]", "[[Hyun-woo|p3:first-name:hyphenated Korean given name]]", "[[857 48 6718|ssn:SSN with spaces]]", dt("1992-11-27", "mm/dd/yyyy", "dob"), "M", dt("2022-06-20", "mm/dd/yyyy", "date:hire date"), amt(61000, "usd0"), "HDHP 3200", "EE only", "[[30318|zip]]", "[[hwbaik@peachmail.example|email]]"],
      ["[[GP-1041|rec:employee ID]]", "[[Montalvo-Ruelas|p4:surname:hyphenated surname]]", "[[Teresa|p4:first-name]]", "[[507-15-9974|ssn]]", dt("1987-01-14", "mm/dd/yyyy", "dob"), "F", dt("2019-04-01", "mm/dd/yyyy", "date:hire date"), amt(58300, "usd0"), "HDHP 3200", "EE+Child", "[[30344|zip]]", "[[teresa.mr@peachmail.example|email]]"],
    ]),
    ("Dependents", [
      ["Emp ID", "Dependent", "Relationship", "DOB", "SSN", "Notes"],
      ["GP-1004", "[[Adunni Oyelaja|p6:full]]", "Spouse", dt("1983-10-05", "mm/dd/yyyy", "dob"), "[[742-30-0334|ssn]]", "[[32 weeks pregnant, due Jan|health:pregnancy]]; add newborn within 30 days"],
      ["GP-1004", "[[Tobi Oyelaja|p7:full]]", "Child", dt("2016-04-22", "mm/dd/yyyy", "dob"), "[[797-05-0886|ssn]]", "[[sickle cell disease|health:diagnosis]], sees hematology monthly - PPO only"],
      ["GP-1019", "[[Jonas Kilgallen-Weir|p9:full]]", "[[Domestic partner (same-sex)|attr:sexual orientation / partnership status]]", dt("1978-12-30", "mm/dd/yyyy", "dob"), "[[359-91-7795|ssn]]", "imputed income applies; affidavit signed [[10/21/2025|date:affidavit date]]"],
      ["GP-1019", "[[Fiadh Kilgallen|p8:full]]", "Child", dt("2011-08-09", "mm/dd/yyyy", "dob"), "[[029-16-6547|ssn]]", "[[adopted 2013; legal name change from the birth name on the SS card pending|indirect:adoption and name history]]"],
      ["GP-1041", "[[Mateo Ruelas|p10:full]]", "Child", dt("2019-02-15", "mm/dd/yyyy", "dob"), "applied for", "[[father under a support order, must provide coverage|attr:court-ordered obligation]] - medical support notice rec'd [[9/3/25|date:short numeric date]]"],
    ]),
    ("Retirees-COBRA", [
      ["Name", "Status", "DOB", "Age", "Medicare no.", "Monthly premium", "Bill to", "Phone", "Notes"],
      ["[[Wendell Purifoy|p5:full]]", "Retiree (pre-1998 plan)", dt("1934-05-06", "mm/dd/yyyy", "dob"), num(91, "age:age stored as a number"), "[[6QH4-TF7-KW22|govid:Medicare beneficiary identifier]]", amt(212.40), "daughter, [[Ottoline Purifoy|p11:full]] (POA), [[2218 Cascade Rd SW|addr]], [[Atlanta|place:city]] [[GA|place:state abbreviation]]", "[[404-555-0149|phone]]", "[[in memory care since March|health:dementia care placement]]; do not phone him, call [[Ottoline|p11:first-name]]"],
      ["[[H. Baik|p3:short:initial + surname]]", "COBRA elect (prior employer overlap)", "", "", "", amt(688.15), "self", "[[(470) 555-0116|phone]]", "ends [[12/31/25|date:coverage end date]]"],
      ["Prepared by broker for open enrollment; return to [[census@unisonbrokers.example|email]] by [[11/21|date:month/day only]]. Section 125 elections on separate form."],
    ]),
  ]))

# ---------------------------------------------------------------- 326
DOCS.append(D(326, "html", "employment background check report", "general", "US", raw_html=True,
  title="Pre-employment background screening report",
  ents={"p1": "Katarzyna Elżbieta Nowicka-Hobbs", "p2": "Renard Thibeaux", "p3": "Odalys Carballo",
        "o1": "ClearLedger Screening Services", "o2": "Brightmoor Senior Living", "o3": "Golden Triangle Home Health Agency",
        "o4": "Monroeville Community College"},
  distractors=["Fair Credit Reporting Act", "15 U.S.C. § 1681", "Form I-9", "E-Verify", "Summary of Rights"],
  body=r'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>Background report</title>
<style>body{font-family:Arial,sans-serif} th{text-align:left;background:#eee} td,th{padding:4px 8px;border:1px solid #ccc}</style></head>
<body>
<header><h1>[[ClearLedger Screening Services|o1:full]]</h1>
<p>Consumer report prepared under the Fair Credit Reporting Act, 15 U.S.C. &sect; 1681 et seq. A copy of the Summary of Rights is attached.</p></header>
<section>
<p>Report no. [[CL-2025-11-0044187|rec:report number]] &middot; Ordered [[11/03/2025|date:order date]] &middot; Completed [[11/06/2025|date:completion date]]<br>
Client: [[Brightmoor Senior Living|o2:full]] (acct [[BSL-PA-0291|rec:client account code]]) &middot; Requested by: [[Odalys Carballo|p3:full]], HR Generalist, [[ocarballo@brightmoorsl.example|email]]<br>
Position applied for: Certified Nursing Assistant, night shift</p>
</section>
<h2>Subject</h2>
<table>
<tr><th>Name</th><td>[[NOWICKA-HOBBS, KATARZYNA ELZBIETA|p1:last-first:Last, First in ALL CAPS without diacritics]]</td></tr>
<tr><th>Also known as</th><td>[[Kasia Hobbs|p1:nickname:nickname with married surname]]; [[Katarzyna Nowicka|p1:short:maiden name]]</td></tr>
<tr><th>SSN</th><td>[[XXX-XX-7167|ssn:masked SSN]] (validated; issued 2009&ndash;2010)</td></tr>
<tr><th>Date of birth</th><td>[[02/08/1990|dob]]</td></tr>
<tr><th>Current address</th><td>[[315 Haymaker Road, Apt 14|addr:street with apartment]], [[Monroeville|place:town]], [[PA|place:state abbreviation]] [[15146|zip]]</td></tr>
<tr><th>Prior addresses (7 yrs)</th><td>[[2260 Brownsville Rd|addr]], [[Pittsburgh|place:city]], PA [[15210|zip]] (2018&ndash;2022); [[88 Chestnut St, Fl 2|addr:street with floor]], [[Passaic|place:city]], [[NJ|place:state abbreviation]] [[07055|zip]] (2014&ndash;2018)</td></tr>
<tr><th>Driver's license</th><td>PA [[31 447 209|govid:driver's license number with spaces]], Class C, valid</td></tr>
</table>
<h2>Criminal record search</h2>
<table>
<tr><th>Jurisdiction</th><th>Result</th><th>Detail</th></tr>
<tr><td>[[Allegheny County|place:county]], PA</td><td>RECORD FOUND</td><td>Docket [[CP-02-CR-0004418-2019|rec:criminal docket number]]. [[Retail theft, graded summary offense; guilty plea|attr:criminal history]] [[06/11/2019|date:plea date]]; fine and costs [[$418.25|money]] paid. No other cases.</td></tr>
<tr><td>[[Passaic County|place:county]], NJ</td><td>CLEAR</td><td>&mdash;</td></tr>
<tr><td>Federal (W.D. Pa., D.N.J.)</td><td>CLEAR</td><td>&mdash;</td></tr>
<tr><td>National sex offender registry</td><td>CLEAR</td><td>&mdash;</td></tr>
</table>
<h2>Employment and education</h2>
<table>
<tr><th>Source</th><th>Claimed</th><th>Verified</th></tr>
<tr><td>[[Golden Triangle Home Health Agency|o3:full]]</td><td>Home health aide, [[03/2020|date:month/year]] &ndash; [[08/2025|date:month/year]]</td><td>Dates confirmed by [[Renard Thibeaux|p2:full]], office manager, [[412-555-0187|phone]]. Eligible for rehire: <b>No</b>. [[Mr. Thibeaux|p2:title-surname]] stated she [[was let go after a client's family complained about missing cash|indirect:reason for leaving a prior job]]; no police report was made.</td></tr>
<tr><td>[[Monroeville Community College|o4:full]]</td><td>Nurse aide certificate, 2019</td><td>Confirmed. Student ID [[M00441872|rec:student ID]]. PA nurse aide registry no. [[NA-0418827|govid:nurse aide registry number]], active, no findings.</td></tr>
</table>
<h2>Work authorization</h2>
<p>Form I-9 documents presented: [[Permanent Resident Card|attr:immigration status]], USCIS no. [[A-218-440-917|govid:alien registration number]], expires [[03/14/2031|date:card expiry date]]. E-Verify case [[2025310144187KP|rec:E-Verify case number]]: employment authorized.</p>
<footer><p>Report viewed [[11/06/2025|date:completion date]] 16:02 by user [[ocarballo|cred:screening portal user name]] from [[192.0.2.41|ip]]. Disputes: [[disputes@clearledger.example|email]] or [[1-800-555-0199|phone:toll-free with country code]]. Before taking adverse action the employer must send the subject this report and wait a reasonable period.</p></footer>
</body></html>
'''))

# ---------------------------------------------------------------- 327
DOCS.append(D(327, "txt", "text message transcript", "general", "US", length="short",
  title="Texts between a store manager and an injured employee",
  ents={"p1": "Renee Oxendine", "p2": "Tavita Leiataua", "o1": "Makai Surf & Sundry"},
  distractors=["TDI-45"],
  body=r'''
Screenshots typed up for the TDI-45 file - thread between [[Renee Oxendine|p1:full]] (mgr, [[Makai Surf & Sundry|o1:full]]) and [[Tavita Leiataua|p2:full]] - [[Nov 8-9|date:date range, month and days]]

[[Tavi|p2:nickname]] ([[808-555-0143|phone]]) 6:12 PM: hey [[renee|p1:first-name!:lower case]] its [[tavi|p2:nickname!:lower case]]. slipped in the stockroom at the [[kapolei|place!:town in lower case]] store, wrist is huge
[[Renee|p1:first-name]] 6:15 PM: omg. go to urgent care NOW, co pays. who saw it
Tavi 6:16 PM: [[uncle junior|indirect:coworker known only by a family-style nickname]] was there
Tavi 9:40 PM: xray says [[hairline fracture, splint 4 wks|health:injury and treatment]]. no lifting
Renee 9:44 PM: ok ur off [[tmrw the 9th|date:informal next-day reference]]. still paying u the 6 hrs, [[$16.25|money:hourly rate]]/hr. need ur last 4 for the form
Tavi 9:45 PM: [[1511|ssn:last four digits only]]. can u send my check to cashapp instead [[$tavi_L|cred:payment app handle]]
Renee 9:47 PM: cant, payroll only. rest up
'''))

# ---------------------------------------------------------------- 328
DOCS.append(D(328, "pdf", "workers' compensation first report and adjuster notes", "general", "US",
  title="Employer's first report of injury with the adjuster's file notes",
  ents={"p1": "Efraín Mondragón-Solís", "p2": "Latrice Uzoma", "p3": "Hank Brubaker", "p4": "Dr. Parisa Nouri",
        "p5": "Guadalupe Solís",
        "o1": "Cascabel Cold Storage, LLC", "o2": "Chaparral Employers Mutual", "o3": "Organ Mountain Regional Hospital"},
  distractors=["Form E-1.2", "NMSA 1978, § 52-1-25", "OSHA 300", "New Mexico Workers' Compensation Administration", "ICD-10 S92.3"],
  body=r'''
# EMPLOYER'S FIRST REPORT OF INJURY OR ILLNESS (Form E-1.2)
Filed with the New Mexico Workers' Compensation Administration. Carrier: [[Chaparral Employers Mutual|o2:full]]. Claim no. [[CEM-WC-25-0077412|rec:workers' compensation claim number]].
## Employer
[[Cascabel Cold Storage, LLC|o1:full]], [[2800 West Amador Avenue|addr]], [[Las Cruces|place:city]], [[NM|place:state abbreviation]] [[88005|zip]]. FEIN [[85-4418720|taxid:EIN]]. Policy [[WC-NM-0044187-25|rec:policy number]]. Contact: [[Hank Brubaker|p3:full]], warehouse manager, [[575-555-0151|phone]].
## Worker
- Name: [[Efraín Mondragón-Solís|p1:full]] (payroll shows [[Efrain Mondragon|p1:short:without diacritics or second surname]])
- SSN: [[672-78-6049|ssn]] · Date of birth: [[12/09/1979|dob]] · Hired: [[04/15/2021|date:hire date]]
- Home: [[1455 Calle de Alvarez, Space 22|addr:street with mobile-home space number]], [[Mesilla|place:town]], NM [[88046|zip]] · Phone: [[575.555.0106|phone:dotted]] (wife, [[Guadalupe Solís|p5:full]], answers; [[he speaks Spanish only|attr:language indicating national origin]])
- Job: forklift operator, freezer dock · Average weekly wage: [[$842.60|money]]
## Injury
- Date and time: [[11/04/2025|date:date of injury]], 2:40 a.m. · Reported to employer: same shift
- What happened: A stand-up reach truck (Raymond 7500, serial no. [[RY7500BA44187|dev:forklift serial number]], fleet tag [[FL-09|dev!:fleet asset tag]]) driven by a co-worker backed over the worker's left foot at dock door 6.
- Injury: [[crush injury to the left foot with fractures of the second and third metatarsals|health:injury]] (ICD-10 S92.3)
- Treated at: [[Organ Mountain Regional Hospital|o3:full]], emergency department; admitted. MRN [[OM-20441877|rec:medical record number]]. Surgeon: [[Dr. Parisa Nouri|p4:full]].
- Post-accident drug and alcohol screen: [[negative|health!:drug screen result]].
Prepared by [[H. Brubaker|p3:short:initial + surname]] on [[11/5/25|date:short numeric date]].
---
# ADJUSTER FILE NOTES — [[Latrice Uzoma|p2:full]], [[Chaparral|o2:short]]
- [[Nov. 6|date:abbreviated month and day]]: Three-point contact done. Spoke with [[Mrs. Solís|p5:title-surname]] through the language line. Worker had [[open reduction and pinning on 11/5|health:surgery]]; non-weight-bearing 8 to 10 weeks. Compensable; no dispute from the employer.
- Nov. 6: TTD rate calculated at two-thirds of the average weekly wage: [[$561.73|money]] per week under NMSA 1978, § 52-1-25. First check to issue [[11/18/2025|date:first payment date]].
- [[Nov. 7|date:abbreviated month and day]]: [[Mr. Brubaker|p3:title-surname]] called. He says the worker's I-9 was completed with [[a Social Security card that the payroll service later flagged as a mismatch|attr:possible immigration / work authorization issue]]. I told him benefits do not depend on that and not to raise it with the family.
- Nov. 7: Telematics download requested for the reach truck, unit ID [[TMX44187720|dev:telematics unit ID]], to confirm speed and the backup alarm. Employer to add the case to its OSHA 300 log.
- [[Nov. 10|date:abbreviated month and day]]: Reserve set: medical [[$48,000|money]], indemnity [[$14,500|money]]. Hospital estimate received, [[$31,206.44|money]].
- Nov. 10: Wife asked whether checks can be direct-deposited. Bank details taken by phone: routing [[103824811|rtn!:routing number given by phone]], account [[2204417788|acct]]. [[Efraín|p1:first-name]]'s cousin in [[El Paso|place:city]] will drive him to follow-up visits; mileage to be reimbursed.
[[L. Uzoma|p2:short:initial + surname]] · [[luzoma@chaparralmutual.example|email]] · direct [[505-555-0139 ext. 4417|phone:with extension]]
'''))

# ---------------------------------------------------------------- 329
DOCS.append(D(329, "md", "international relocation checklist", "general", "EU", minors=["p3", "p4"],
  title="Relocation checklist for an employee moving from Bilbao to Eindhoven",
  ents={"p1": "Íñigo Zubeldia Aramburu", "p2": "Maite Larrañaga Otxoa", "p3": "Ane Zubeldia Larrañaga",
        "p4": "Unai Zubeldia Larrañaga", "p5": "Annelies van der Heijden",
        "o1": "Brabant Photonics B.V.", "o2": "Kutxa Nervión", "o3": "Internationale School Kempen",
        "o4": "Expat Landing Services"},
  distractors=["30%-regeling", "DigiD", "BRP", "Modelo 030", "A1 certificate"],
  body=r'''
# Relocation file: [[Zubeldia|p1:surname]] family — Bilbao → Eindhoven

**Case** [[ELS-2025-0718|rec:relocation case number]] · consultant [[Annelies van der Heijden|p5:full:Dutch name with particles]] ([[Expat Landing Services|o4:full]]) · [[a.vanderheijden@expatlanding.example|email]] · [[+31 40 555 0142|phone:Dutch number, international format]]
**Employer** [[Brabant Photonics B.V.|o1:full]], start date [[1 december 2025|date:Dutch-style date, lower-case month]], gross salary [[€ 78.400|money:Dutch format, dot as thousands separator]] per year, relocation allowance [[€ 7.500,00|money:Dutch format, decimal comma]]

## The family

| | Name | Born | Passport / DNI | Notes |
|---|---|---|---|---|
| Employee | [[Íñigo Zubeldia Aramburu|p1:full:Spanish name with two surnames]] | [[14-03-1983|dob:day-first with hyphens]] | DNI [[44718820-K|govid:Spanish national ID number]], passport [[PAK441872|govid:Spanish passport number]] | optical engineer |
| Spouse | [[Maite Larrañaga Otxoa|p2:full:Spanish name with two surnames]] | [[02-11-1985|dob:day-first with hyphens]] | DNI [[72093316-T|govid:Spanish national ID number]] | [[physiotherapist; Dutch BIG registration not started|indirect:spouse's profession and licensing status]] |
| Child | [[Ane|p3:first-name]] | [[2015|dob!:birth year only]] | passport [[PAL207719|govid:Spanish passport number]] | [[type 1 diabetes, insulin pump|health:child's diagnosis and device]] |
| Child | [[Unai|p4:first-name]] | [[2019|dob!:birth year only]] | on mother's Libro de Familia | — |

## Done

- [x] Rental signed [[2025-10-28|date:ISO date]]: [[Kruisstraat 118-B|addr:Dutch address, street then number]], [[5612 CL|zip:Dutch postcode]] [[Eindhoven|place:city]]. Rent [[€ 2.150|money:Dutch format]] p/m, deposit two months.
- [x] BRP registration appointment at the gemeente: [[woensdag 3 december|date:Dutch weekday, day and month]], 09:20. Bring apostilled birth certificates for [[Ane Zubeldia Larrañaga|p3:full]] and [[Unai Zubeldia Larrañaga|p4:full]].
- [x] BSN for [[Íñigo|p1:first-name]] issued on his earlier short stay: [[218440917|taxid:Dutch citizen service number (BSN)]].
- [x] School: [[Internationale School Kempen|o3:full]], places confirmed for both children; fees [[€ 6.900|money:Dutch format]] each, employer pays half.

## Still open

- [ ] 30%-regeling application. Needs the signed addendum and proof he lived more than 150 km from the border. Old address: [[Calle Licenciado Poza 44, 3º Izda.|addr:Spanish address with floor and door]], [[48011|zip:Spanish postal code]] [[Bilbao|place:city]], [[Bizkaia|place:province]].
- [ ] Dutch bank account. Until then salary goes to the Spanish account at [[Kutxa Nervión|o2:full]]: IBAN [[ES16 2191 2410 3273 1773 1932|iban]], BIC [[KUNEES2BXXX|acct:BIC / SWIFT code]].
- [ ] Spanish tax: file Modelo 030 for change of address; NIF is the DNI. Ask HR for the A1 certificate for November.
- [ ] Health insurance within four months of registration. [[Ane|p3:first-name]]'s endocrinologist in Bilbao will write a summary in English; ask the insurer about pump supplies. [[Maite|p2:first-name]] asked whether her [[treatment for postnatal depression|health:mental health treatment]] has to be declared: no, basic cover has no medical questions.
- [ ] DigiD. Applied [[12 nov|date:day and abbreviated month, lower case]]; activation letter goes to [[Kruisstraat|addr!:street name only, no number]]. He chose user name [[izubeldia83|cred:government portal user name]].
- [ ] Car: Spanish plates [[4418 LKM|veh:Spanish registration plate]] must be re-registered or exported within the exemption period.

## Contact

Íñigo: [[+34 655 550 147|phone:Spanish mobile, international format]], [[inigo.zubeldia@correovasco.example|email]]. Maite: [[655 55 01 82|phone:Spanish mobile, national format]] (WhatsApp). They [[speak Basque at home|attr:language indicating ethnicity]]; emails in English or Spanish are fine. *Eskerrik asko* to [[Annelies|p5:first-name]] from the family.
'''))

# ---------------------------------------------------------------- 330
DOCS.append(D(330, "txt", "family leave administration log", "general", "US",
  title="HR leave administrator's log for an intermittent family leave",
  ents={"p1": "Charlene Aguinaldo", "p2": "Bienvenido Aguinaldo", "p3": "Dr. Reuben Katzenberg", "p4": "Monique Fairbanks",
        "o1": "Presidio Title & Escrow Co.", "o2": "Sunset Geriatric Associates"},
  distractors=["WH-380-F", "29 CFR 825.305", "CFRA", "FMLA", "PFL"],
  body=r'''
LEAVE ADMIN LOG - [[Presidio Title & Escrow Co.|o1:full]] - kept by [[Monique Fairbanks|p4:full]], HR
Employee: [[Aguinaldo, Charlene|p1:last-first]]   Emp# [[004417|rec:employee number]]   Escrow officer, [[Daly City|place:city]] branch   Hired [[8/14/2017|date:hire date]]
Leave case: [[LV-2025-088|rec:leave case number]]   Type: FMLA/CFRA intermittent, care of parent

[[10/20/25|date:short numeric date]]  [[Charlene|p1:first-name]] came by. Her father, [[Bienvenido Aguinaldo|p2:full]], [[age 93|age:labelled age]], lives with her at [[72 Wellington Avenue|addr]], Daly City [[CA|place:state abbreviation]] [[94014|zip]]. He [[fell on 10/17 and broke his hip|health:injury]]; surgery at the county hospital on [[10/18|date:month/day only]]. She needs time for rehab visits and then to be home with him some afternoons. Gave her the WH-380-F and the 15-day deadline under 29 CFR 825.305. She has 1,250+ hours, eligible.

[[10/29/25|date:short numeric date]]  Certification received by fax from [[Sunset Geriatric Associates|o2:full]], signed by [[Dr. Reuben Katzenberg|p3:full]] (lic. [[G 44187|govid:medical license number]]), office [[415-555-0123|phone]]. Summary of what it says, for my own reference, original locked in the medical file:
   - patient born [[2/11/1932|dob]]; conditions: [[hip fracture status post hemiarthroplasty|health:condition]], [[moderate Alzheimer's dementia|health:diagnosis]], [[congestive heart failure|health:diagnosis]]
   - needs help with transfers, meals, medication; cannot be left alone more than 2 hours
   - leave needed: up to 3 half-days a week plus appointments, [[10/20/2025|date:leave start date]] through [[4/20/2026|date:leave end date]], then reassess
   Complete and sufficient. Approved. Designation notice emailed to [[caguinaldo@presidiotitle.example|email]] and mailed.

[[11/3|date:month/day only]]  Charlene asked about pay. Explained PFL through the state, up to 8 weeks; she applies herself. Her claim ID once filed: [[R1000-441-877-20|rec:state benefit claim ID]]. Our piece is only the wage info: [[$38.75|money:hourly rate]]/hr, 40 hrs.

[[11/6|date:month/day only]]  Her supervisor asked me "how old is the dad, [[ninety-something|age:approximate age in words]]? how long can this go on." Told him the reason for leave is not his business and not to ask her. Noted here in case it comes up again.

[[11/10|date:month/day only]]  Charlene called from her cell ([[650-555-0178|phone]]). Father readmitted overnight, [[pneumonia|health:condition]]. She will be out all week. Told her that is covered; just text me the days. She mentioned [[her brother in Manila can't get a visa to come help|indirect:family abroad]] so it is all on her. She was upset about money; told her about the hardship option in the 401(k) but did not push.

Usage to date: 31.5 hrs of 480.   Next recert: not before [[5/1/26|date:short numeric date]].   [[MF|p4:initials]]
'''))
