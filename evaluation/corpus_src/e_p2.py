from corpus_src.dsl import D, dt, amt, num

DOCS = []

# ---------------------------------------------------------------- 82 (LONG)
DOCS.append(D(82, "pdf", "court filing draft - motion", "legal", "US", length="long",
  title="Draft motion for partial summary judgment - unpaid commissions and leave interference",
  ents={"p1": "Delphine M. Okonkwo-Reyes", "p2": "Leonard P. Hargrove III", "p3": "Xiomara Bautista",
        "p4": "Raymond J. Feldkamp", "p5": "Calloway Jefferson-Ruiz", "p6": "Bartholomew Quigley IV",
        "p7": "Anjali Venkataraman", "p8": "Miriam J. Sandoval",
        "o1": "Brightwater Freight Systems, Inc.", "o2": "Kessler Agricultural Cooperative",
        "o3": "Tri-County Poultry Growers Ass'n", "o4": "Jefferson-Ruiz & Tan LLC",
        "o5": "Quigley Stanhope LLP", "o6": "Gateway Women's Surgical Associates",
        "o7": "Mississippi Valley Federal Credit Union"},
  distractors=["Fed. R. Civ. P. 56(a)", "Mo. Rev. Stat. § 407.913", "29 U.S.C. § 2615(a)(1)",
               "Celotex Corp. v. Catrett", "Count III", "CM/ECF", "Ford Explorer", "FreightLedger"],
  ok=["477 U.S. 317, 322-23 (1986)", "29 C.F.R. § 825.220(c)", "_001877", "47:2-10", "112:4-19"],
  body=r'''
**UNITED STATES DISTRICT COURT**
**EASTERN DISTRICT OF [[MISSOURI|place!:state in ALL CAPS]], EASTERN DIVISION**
[[DELPHINE M. OKONKWO-REYES|p1:caps]], Plaintiff,
v.
[[BRIGHTWATER FREIGHT SYSTEMS, INC.|o1:caps]], and [[LEONARD P. HARGROVE III|p2:caps]], Defendants.
Case No. [[4:25-cv-00871-MJS|rec:federal case number]]
Hearing requested before the [[Hon. Miriam J. Sandoval|p8:full:honorific + full name]]
# PLAINTIFF'S MOTION FOR PARTIAL SUMMARY JUDGMENT AND MEMORANDUM IN SUPPORT
**DRAFT v4 -- [[CJR|p5:initials]] edits [[10/19|date!:date without year]] -- do not file**
Plaintiff [[Delphine M. Okonkwo-Reyes|p1:full]] moves under Fed. R. Civ. P. 56(a) for partial summary judgment on Count I of her Amended Complaint (unpaid commissions, Mo. Rev. Stat. § 407.913) and on liability under Count III (interference with protected leave, 29 U.S.C. § 2615(a)(1)). In support she states as follows.
## I. INTRODUCTION
This is a case about a sales commission that was earned, booked, and then reassigned at 11:52 at night. [[Ms. Okonkwo-Reyes|p1:title-surname]] spent fourteen months landing the largest account in her employer's history. Nine days after she told the company she needed surgery, the account was moved to the company's president, her commission was zeroed out, and she was fired. None of this is disputed. Every material fact below comes from Defendants' own records or their own sworn testimony, and on those facts Plaintiff is entitled to judgment as a matter of law.
## II. STATEMENT OF UNCONTROVERTED MATERIAL FACTS
1. Defendant [[Brightwater Freight Systems, Inc.|o1:full]] ("[[Brightwater|o1:short!:short name without corporate suffix]]" or "[[BFS|o1:acronym]]") is a [[Missouri|place:state]] corporation with its principal office at [[7700 Hall Street|addr]], [[St. Louis|place:city]], Missouri [[63147|zip]]. Answer ¶ 4.
2. Defendant [[Leonard P. Hargrove III|p2:full:full name with suffix]] is Brightwater's president and majority shareholder. Inside the company he is known as "[[Len|p2:nickname]]." [[Hargrove|p2:surname]] Dep. 9:2-14.
3. Brightwater hired Plaintiff as an account executive on [[August 14, 2019|date:hire date]]. Her employee number was [[BFS-00417|rec:employee ID]]. Ex. 2 (offer letter). Throughout her employment she was [[the only Black woman among the company's fourteen account executives|attr!:race, also a unique role]]. [[Bautista|p3:surname]] Dep. 31:7-12.
4. Under the 2024 Sales Compensation Plan, Plaintiff received a base salary of [[$68,500|money]] plus a commission of 4.5% of net revenue on every account she originated, for the first 24 months of the account. Ex. 3 § 2.1. The Plan provides that a commission is "earned when the customer's first invoice is paid." Id. § 2.4.
5. Beginning in [[November 2023|date!:month and year only]], Plaintiff pursued the dedicated-haul business of [[Kessler Agricultural Cooperative|o2:full]] ("[[Kessler Ag|o2:short!:short name without corporate suffix]]"), a grain and feed cooperative in [[Sikeston|place:city]], Missouri. Ex. 5. She made eleven site visits over fourteen months; her approved expense reports for those trips total [[$6,212.40|money]]. Ex. 6.
6. On [[January 17, 2025|date:contract date]], Kessler Ag signed a three-year Master Transportation Agreement, Contract No. [[MTA-2025-0031|rec:contract number]], with projected annual net revenue to Brightwater of [[$3.9 million|money!:rounded in words]]. Ex. 7. It was, and remains, [[the largest single account in Brightwater's history|indirect!:distinctive transaction]]. Hargrove Dep. 22:15-23:1. Brightwater's customer database, FreightLedger, listed Plaintiff as the account owner. Ex. 8.
7. Kessler Ag paid its first invoice, No. [[INV-250214-006|rec:invoice number]], in the amount of [[$118,946.33|money]], on [[February 27, 2025|date:payment date]]. Ex. 9.
8. Brightwater's chief financial officer, [[R.J. Feldkamp|p4:short!:initials + surname]], calculated Plaintiff's first-quarter commission on the Kessler Ag account at [[$43,875.00|money]]. On [[March 3, 2025|date:email date]] he emailed her: "Nice work. [[Forty-three eight seventy-five|money!:amount spoken in words]] hits your [[3/28|date!:date without year]] check." Ex. 10 (BFS_001877).
9. [[Mr. Feldkamp|p4:title-surname]] testified that as of [[March 3|date!:date without year]] the commission was "booked and accrued" on Brightwater's ledger. [[Feldkamp|p4:surname]] Dep. 44:18-45:6.
10. A second account, [[Tri-County Poultry Growers Ass'n|o3:full]] ("[[Tri-County|o3:short!:short name without corporate suffix]]"), was also originated by Plaintiff. Commissions of [[$9,310.50|money]] on paid Tri-County invoices were accrued and never paid. Ex. 10 at 3; Feldkamp Dep. 47:2-10.
11. On [[March 5, 2025|date:leave request date]], Plaintiff emailed Brightwater's human resources director, [[Xiomara Bautista|p3:full]], at [[xbautista@brightwaterfreight.example|email]]. She wrote that she had been [[diagnosed with uterine fibroids|health!:diagnosis]], was [[scheduled for a hysterectomy|health!:surgical procedure]] on [[March 24, 2025|date:surgery date]] with [[Dr. Anjali Venkataraman|p7:full:title + full name]] of [[Gateway Women's Surgical Associates|o6:full]], and would need six weeks of leave. Ex. 11.
12. [[Ms. Bautista|p3:title-surname]] forwarded that email to Mr. Hargrove within the hour, adding: "FYI -- [[Delphine|p1:first-name]] out 6 wks starting the 24th. Right when [[Kessler|o2:short!:short name without corporate suffix]] ramps." Ex. 12.
13. At 11:52 p.m. on [[March 6, 2025|date:account reassignment date]], a user logged in to FreightLedger as "[[lhargrove3|cred:username]]" from IP address [[198.51.100.23|ip]] and changed the owner of the Kessler Ag account from Plaintiff to "House - [[LPH|p2:initials]]." Ex. 13 (audit log). Mr. Hargrove admits that lhargrove3 is his username and that the IP address is the internet connection at [[his home in Ladue|indirect!:home location of a named person]]. Hargrove Dep. 112:4-19.
14. The next morning Mr. Hargrove texted Mr. Feldkamp from [[(314) 555-0193|phone]]: "Tell Delphine her numbers are her numbers until I say they aren't. Kessler is a house account now." Ex. 14.
15. On [[March 14, 2025|date:termination date]], nine days after her leave request and ten days before her surgery, Brightwater terminated Plaintiff's employment. The letter, signed by Ms. Bautista, cites a "restructuring of the sales function." Ex. 15. No other employee was let go in the restructuring. Bautista Dep. 58:1-9.
16. Plaintiff's final paycheck was deposited on [[March 28, 2025|date:final pay date]] to her account ending in [[2274|acct!:last four only]] at [[Mississippi Valley Federal Credit Union|o7:full]]. It contained no commission. Ex. 16. The same day Brightwater sent a driver to retrieve her company vehicle, a 2023 Ford Explorer, VIN [[1FMSK8DH5PGA31907|veh:VIN]], Missouri plate [[RB7 K4D|veh:license plate]], from her home at [[3916 Juniata Street, Apt. 2W|addr]], St. Louis.
17. Plaintiff underwent surgery as scheduled. Because her group coverage ended with her employment, she paid continuation premiums of [[$1,842.17|money]] per month. [[Okonkwo-Reyes|p1:surname]] Decl. ¶ 19.
18. During calendar year 2025, Kessler Ag paid Brightwater net revenue of [[$3,412,008|money]]. Ex. 18. At 4.5%, the commission on that revenue is [[$153,540.36|money]]. Feldkamp Dep. 71:3-11 (agreeing with the arithmetic).
19. Brightwater has paid Plaintiff nothing on either account. Answer ¶ 38.
## III. ARGUMENT
**A. The summary judgment standard.** Summary judgment is proper where there is no genuine dispute of material fact and the movant is entitled to judgment as a matter of law. Fed. R. Civ. P. 56(a); Celotex Corp. v. Catrett, 477 U.S. 317, 322-23 (1986). A party opposing the motion may not rest on denials; it must point to evidence.
**B. Plaintiff's commissions were earned before she was terminated, and the statute required payment within thirty days.** Missouri law is direct on this point. When the relationship between a sales representative and a principal ends, commissions then due must be paid within thirty days, and a principal that fails to pay is liable for the commissions, an additional amount calculated under the statute, and attorney's fees. Mo. Rev. Stat. § 407.913. The only question under Count I is whether the commissions were "due."
They were. The Plan says a commission is earned when the customer's first invoice is paid. SUMF ¶ 4. Kessler Ag's first invoice was paid on February 27, 2025. SUMF ¶ 7. The CFO then calculated the commission, told Plaintiff the number, and booked it. SUMF ¶¶ 8-9. Defendants' only response is that Mr. Hargrove had "discretion to designate house accounts." But the Plan contains no such provision, and Mr. Hargrove could not identify one at his deposition. Hargrove Dep. 118:6-20. A principal cannot un-earn a commission by editing a database field at midnight.
The same analysis applies to the Tri-County commissions, which Defendants have never disputed. SUMF ¶ 10.
**C. Defendants interfered with Plaintiff's right to leave.** To prevail on an interference claim an employee must show she was eligible for leave, that she gave notice, and that the employer denied or interfered with a benefit to which she was entitled. Plaintiff had worked full time for Brightwater for more than five years. SUMF ¶ 3. She gave notice on [[March 5|date!:date without year]], in writing, nineteen days before her surgery. SUMF ¶ 11. She was fired nine days later. SUMF ¶ 15.
An employer may defend by showing it would have made the same decision regardless of the leave request. Brightwater cannot. Its own HR director connected the leave to the Kessler ramp-up in the same breath she reported it. SUMF ¶ 12. The account was reassigned the next night. SUMF ¶ 13. The "restructuring" eliminated exactly one position. SUMF ¶ 15. On this record no reasonable jury could find that the termination was unrelated to the leave request, and the regulations bar an employer from treating a request for leave as a negative factor in an employment decision. 29 C.F.R. § 825.220(c).
## IV. CONCLUSION
Plaintiff respectfully asks the Court to enter judgment in her favor on Count I in the principal amount of [[$162,850.86|money]] (the Kessler Ag and Tri-County commissions together), with the additional statutory amount and fees to be determined, and to enter judgment as to liability on Count III, reserving damages for trial.
Dated: [[October 23, 2026|date:filing date]]
Respectfully submitted,
**[[JEFFERSON-RUIZ & TAN LLC|o4:caps]]**
/s/ [[Calloway Jefferson-Ruiz|p5:full]] (draft)
Calloway Jefferson-Ruiz, #[[68214MO|govid:state bar number]]
[[211 North Broadway, Suite 2950|addr]]
St. Louis, [[MO|place:state abbreviation]] [[63102-2733|zip:ZIP+4]]
Tel. [[(314) 555-0126|phone]] | Fax [[(314) 555-0127|phone:fax]]
[[cjr@jrtlaw.example|email]]
Attorneys for Plaintiff
## CERTIFICATE OF SERVICE
I certify that on the date above a copy of the foregoing was served through the Court's CM/ECF system on [[Bartholomew Quigley IV|p6:full:full name with suffix]], [[Quigley Stanhope LLP|o5:full]], [[bquigley@quigleystanhope.example|email]], counsel for Defendants.
**Internal notes for [[Calloway|p5:first-name]] (strip before filing)**
- Local rule on redaction: Exs. 2 and 16 as received still show three things that must come out.
- Her SSN: [[462-63-8608|ssn]]
- Her DOB: [[05/19/1984|dob]]
- The full credit union account number: [[30051-882274|acct]]
- [[Bart|p6:nickname]] called [[Friday the 16th|date!:weekday and day only]]; they may offer [[90k|money!:k shorthand]] to make Count I go away. Delphine says no.
- [[Dr. Venkataraman|p7:title-surname]]'s office will not release the operative report without a new authorization. Not needed for this motion.
'''))

# ---------------------------------------------------------------- 87
DOCS.append(D(87, "html", "case status report", "legal", "US",
  title="Weekly case status report - litigation group",
  ents={"p1": "Jordan Paris", "p2": "Aurelio Benedetti", "p3": "Thanh Huong Pham",
        "p4": "Winifred Achterberg", "p5": "Kwame Asante-Boateng", "p6": "Siobhan O'Brien",
        "p7": "Chase Montgomery", "p8": "Lucille Beaumont",
        "o1": "Paris & O'Brien, Attorneys at Law", "o2": "Benedetti Bros. Paving, Inc.",
        "o3": "Clackamas Valley Sand & Gravel Co.", "o4": "Rose City Mutual Insurance Company",
        "o5": "Estate of Lucille Beaumont", "o6": "Sellwood Animal Hospital, P.C."},
  distractors=["ORS 20.080", "UTCR 5.050", "ORCP 47", "Monday", "Dept. 14", "Rule 30(b)(6)"],
  body=r'''
# [[Paris & O'Brien, Attorneys at Law|o1:full]] - Case status report
Week of [[October 26, 2026|date:report week]]. Prepared by [[Chase Montgomery|p7:full]], paralegal, for the Monday docket meeting. Internal - do not forward to clients.
## Active matters
| Matter | Court no. | Atty | Next event |
| [[Benedetti Bros. Paving|o2:short!:short name without corporate suffix]] v. [[Clackamas Valley S&G|o3:short!:abbreviated organization name]] | [[23CV41877|rec:state court case number without separators]] | [[JP|p1:initials]] | MSJ hearing [[11/09/2026|date:hearing date]] |
| [[Pham|p3:surname]] v. [[Rose City Mutual|o4:short!:short name without corporate suffix]] | [[3:26-cv-00512-HZ|rec:federal case number]] | [[SOB|p6:initials]] | Rule 30(b)(6) depo [[11/12/2026|date:deposition date]] |
| In re [[Estate of Lucille Beaumont|o5:full]] | [[26PB03391|rec:probate case number]] | SOB | Inventory due [[12/01/2026|date:filing deadline]] |
| [[Asante-Boateng|p5:surname]] adv. [[Sellwood Animal Hosp.|o6:short!:abbreviated organization name]] | [[26CV18820|rec:state court case number without separators]] | JP | Answer due [[11/05/2026|date:answer deadline]] |
## Notes by matter
**[[Benedetti|o2:short!:matter nickname, also a surname]].** Client contact is [[Aurelio Benedetti|p2:full]] ([[503-555-0143|phone]]). [[Aurelio|p2:first-name]] wants to know why we have not moved under ORCP 47 already; [[Jordan Paris|p1:full!:name made of two common words]] explained the paving invoices ([[$214,600|money]] claimed, [[$61,250.75|money]] admitted) are the only part ripe for it. Defendant's full name for the caption is [[Clackamas Valley Sand & Gravel Co.|o3:full]] The hearing is in Dept. 14. Trial readiness under UTCR 5.050 is not yet set.
**Pham.** [[Thanh Huong Pham|p3:full]]'s homeowner claim, policy [[HO-3 8841207-02|rec:policy number]], claim no. [[RCM-2026-004417|rec:claim number]], for the [[January 13|date!:date without year]] ice-storm loss at [[6120 SE Tolman Street|addr]], [[Portland|place:city]], [[OR 97206|zip!:state abbreviation and ZIP written together]]. [[Rose City Mutual Insurance Company|o4:full]] has paid [[$18,400|money]] against our estimate of [[$96,000|money]]. [[Ms. Pham|p3:title-surname]] needs a Vietnamese interpreter for her deposition prep; she also asked that we not schedule anything on [[her dialysis days (Tues/Thurs)|health!:treatment schedule]]. The adjuster's claim portal is at [[https://claims.rosecitymutual.example/c/004417|url]].
**[[Beaumont|p8:surname]] estate.** Personal representative is [[Winifred Achterberg|p4:full]], [[the decedent's niece|indirect!:family relationship to a named person]]. [[Ms. Beaumont|p8:title-surname]] died [[August 30, 2026|date:date of death]] [[at 97|age!:age given as bare number]]. Assets so far: house in [[Sellwood|place:neighbourhood]], a 2011 Subaru Outback ([[Oregon|place:state]] plate [[417 KBD|veh:license plate]], VIN [[4S4BRBKC7B3398104|veh:VIN]]), and about [[$340k|money!:k shorthand]] at two banks. [[Winifred|p4:first-name]] found a second will in a kitchen drawer; [[Siobhan O'Brien|p6:full]] is reviewing.
**Asante-Boateng.** We defend [[Kwame Asante-Boateng|p5:full]], a former vet tech sued by [[Sellwood Animal Hospital, P.C.|o6:full]] on a non-compete. Amount in controversy is under [[$10,000|money]] so ORS 20.080 fees are in play. [[Kwame|p5:first-name]] is [[a shop steward with Local 88|attr!:union role]] at his new job and thinks the suit is payback for the organizing drive. [[Jordan|p1:first-name!:first name that is also a place]] says keep that theory in our pocket for now.
## Deadlines needing a decision
- Pham: expert disclosure. Retainer for the roofing expert is [[$3,500|money]]; client has not approved.
- Beaumont: bond waiver from the three heirs.
- Timekeeping: [[Chase|p7:first-name!:first name that is also a common word]] is out [[11/11|date!:date without year]]; send filings to the front desk.
'''))

# ---------------------------------------------------------------- 88
DOCS.append(D(88, "txt", "tax organizer worksheet", "accounting", "US",
  title="Tax organizer worksheet - rental properties",
  ents={"p1": "Rafael Santos de Oliveira", "p2": "Mei-Ling Santos", "p3": "Darnell Whitlock",
        "p4": "Bernadette Kowalczyk", "p5": "Ignatius Farrow",
        "o1": "Kowalczyk & Farrow CPAs, LLC", "o2": "Santos Family Rentals LLC",
        "o3": "Palmetto Coastal Property Management", "o4": "Lowcountry Federal Savings Bank",
        "o5": "Sea Island Roofing & Sheet Metal"},
  distractors=["Schedule E", "Form 1098", "Form 4562", "Form 8582", "W-9", "27.5 yrs", "Zelle"],
  ok=["2025"],
  body=r'''
[[Kowalczyk & Farrow CPAs, LLC|o1:full]]                     2025 TAX ORGANIZER -- RENTAL REAL ESTATE (Schedule E)
Client no. [[C-10447|rec:client number]]                              Preparer: [[B. Kowalczyk|p4:short:initial + surname]]   Reviewer: [[IF|p5:initials]]

TAXPAYER    [[Santos de Oliveira, Rafael|p1:last-first]]      SSN [[502-39-8615|ssn]]     DOB [[11/02/1971|dob]]
SPOUSE      [[Santos, Mei-Ling|p2:last-first]]                SSN [[461261522|ssn!:SSN without dashes]]       DOB [[2 Feb 1974|dob:day month year]]
Home        [[18 Wappoo Creek Place|addr]], [[Charleston|place:city]], [[SC|place:state abbreviation]] [[29412|zip]]
Phone       [[843 555 0177|phone:spaces]] (R)   [[843-555-0102|phone]] ([[M-L|p2:initials]])      Email [[rafa.santos@santosrentals.example|email]]

Properties are held in [[Santos Family Rentals LLC|o2:full]] (disregarded; EIN [[47-2290618|taxid:EIN]]) unless noted.

PROPERTY A -- [[212-B Ashley Avenue|addr]], Charleston 29403? (client wrote 29403, deed says [[29401|zip]])
  Type: duplex, both units long-term        Placed in service: [[06/15/2014|date:placed-in-service date]]      Basis (bldg): [[$418,000|money]]
  Rents received ........................ [[52,800|money!:no currency symbol]]
  Mgmt fees ([[Palmetto Coastal Property Management|o3:full]]) ........ [[5,280|money!:no currency symbol]]
  Mortgage int. (Form 1098, [[Lowcountry Federal Savings Bank|o4:full]], loan [[#0091-447820|rec:loan number]]) ... [[9,611.48|money!:no currency symbol]]
  Property tax .......................... [[6,940|money!:no currency symbol]]
  Insurance ............................. [[4,125|money!:no currency symbol]]
  Repairs -- see note 1 ................. [[23,750|money!:no currency symbol]]
  Depreciation (27.5 yrs, Form 4562) .... computed by firm

PROPERTY B -- [[9 Egret Landing Ct, Unit 304|addr]], [[Folly Beach|place:city]], SC [[29439|zip]]   (held personally, NOT in the LLC)
  Type: condo, short-term (avg stay 4 nights)    Personal use days: 19     Rented days: 141
  Gross bookings ........................ [[71,366.20|money!:no currency symbol]]
  Platform fees ......................... [[10,704.93|money!:no currency symbol]]
  Cleaning ([[Darnell Whitlock|p3:full]], paid by Zelle -- 1099? see note 2) .... [[8,460|money!:no currency symbol]]
  HOA ................................... [[7,200|money!:no currency symbol]]

NOTES FROM CLIENT CALL [[1/29/26|date!:two-digit year]]
1. Roof on A replaced after the storm. [[Sea Island Roofing & Sheet Metal|o5:full]] inv. [[#SI-8821|rec:invoice number]] dated
   [[Sept. 9, 2025|date:invoice date]], [[$23,750.00|money]]. Insurance paid [[$15,000|money]] of it in [[January 2026|date!:month and year only]]. Repair vs improvement?
   Whole roof = improvement in my view. Ask Ignatius.
2. [[Rafael|p1:first-name]] paid [[Whitlock|p3:surname]] more than the threshold and has no W-9. [[Mr. Whitlock|p3:title-surname]] "doesn't do paperwork."
   Told Rafael to get it or we back-up withhold going forward. Whitlock cell per Rafael: [[(843) 555-0190|phone]].
3. [[Mei-Ling|p2:first-name]] qualifies as a real estate professional? She says 900+ hrs but also works 30 hrs/wk
   as a dental hygienist. Not on these facts. Passive loss limits apply (Form 8582).
4. Refund direct deposit: [[Lowcountry Federal|o4:short!:short name without corporate suffix]] checking, routing [[053255064|rtn]], account [[20 4471 08836|acct!:account number with spaces]].
5. Our fee ([[$1,650|money]]) to the card on file: Mastercard [[5577-4144-8335-0067|card:card with dashes]], exp. [[04/27|exp]], code [[339|cvv]].
   (Moved to the vault [[2/3|date!:date without year]]; shred this line.)
6. Estimated payments made: [[4/15|date!:date without year]] [[$3,000|money]]; [[6/16|date!:date without year]] $3,000; [[9/15|date!:date without year]] $3,000; [[1/15/26|date!:two-digit year]] [[$4,500|money]].
'''))

# ---------------------------------------------------------------- 89
DOCS.append(D(89, "xlsx", "fixed asset ledger", "accounting", "US",
  title="Fixed asset ledger with vehicle and vendor sheets",
  ents={"p1": "Earl T. Kowalski Jr.", "p2": "Rosa Delgado-Finch", "p3": "Abdirahman Warsame",
        "p4": "Paulette Nakamura", "p5": "Gus Papadakis", "p6": "LaTonya Briggs",
        "o1": "Kowalski & Sons Excavating, Inc.", "o2": "Twin Ports Equipment Finance LLC",
        "o3": "Iron Range Tractor & Implement Co.", "o4": "Superior Shores Insurance Agency",
        "o5": "North Country Diesel Repair", "o6": "Arrowhead Aggregate Supply Corp.",
        "o7": "Papadakis Welding", "o8": "Duluth Harbor Fuel Co-op"},
  distractors=["MACRS 5-yr", "Sec. 179", "MACRS 7-yr", "Net 30", "Net 15"],
  sheets=[
   ("Assets", [
     ["[[Kowalski & Sons Excavating, Inc.|o1:full]] - Fixed asset register FY2025", None, None, None, None, None, None, None],
     ["Asset tag", "Description", "Serial / PIN", "In service", "Cost", "Method", "Accum. depr.", "Financed by / loan no."],
     ["[[FA-0101|rec:asset tag]]", "Excavator, 20-ton", "[[KHCX210ETN0A04417|dev:equipment serial number]]", dt("2019-04-22"), amt(187500, "acct"), "MACRS 5-yr", amt(-187500, "acct", "money!:parenthesized negative"), "paid off"],
     ["[[FA-0102|rec:asset tag]]", "Excavator, mini 5-ton", "[[JKUB0U55P01H11872|dev:equipment serial number]]", dt("2021-06-07"), amt(68240, "acct"), "MACRS 5-yr", amt(-60385.92, "acct", "money!:parenthesized negative"), "[[Twin Ports Equipment Finance LLC|o2:full]] [[#TP-44-019283|rec:loan number]]"],
     ["[[FA-0103|rec:asset tag]]", "Dozer, 105 hp", "[[CAT00D5KCWWW02231|dev:equipment serial number]]", dt("2022-03-15"), amt(214900, "acct"), "MACRS 5-yr", amt(-152922.84, "acct", "money!:parenthesized negative"), "[[Twin Ports|o2:short!:short name without corporate suffix]] [[#TP-44-020771|rec:loan number]]"],
     ["[[FA-0104|rec:asset tag]]", "Skid steer", "[[B4CV11447|dev:equipment serial number]]", dt("2023-05-01"), amt(54300, "acct"), "Sec. 179", amt(-54300, "acct", "money!:parenthesized negative"), "cash"],
     ["[[FA-0105|rec:asset tag]]", "Laser grade control kit", "[[TPS-GX60-771204|dev:equipment serial number]]", dt("2023-05-19"), amt(31875.5, "acct"), "Sec. 179", amt(-31875.5, "acct", "money!:parenthesized negative"), "cash"],
     ["[[FA-0106|rec:asset tag]]", "Shop air compressor", "[[IR2475N-90771|dev:equipment serial number]]", dt("2024-01-11"), amt(4212.99, "acct"), "MACRS 7-yr", amt(-1633.8, "acct", "money!:parenthesized negative"), "cash"],
     ["[[FA-0107|rec:asset tag]]", "Office laptops (3)", "[[5CG4127XKQ|dev:laptop serial number]]; [[5CG4127XLM|dev:laptop serial number]]; [[5CG4127XMD|dev:laptop serial number]]", dt("2024-09-03"), amt(4047, "acct"), "MACRS 5-yr", amt(-2104.44, "acct", "money!:parenthesized negative"), "company card ending [[0274|card!:last four only]]"],
     ["[[FA-0108|rec:asset tag]]", "Trench box set", "n/a", dt("2025-02-27"), amt(12980, "acct"), "MACRS 7-yr", amt(-1854.84, "acct", "money!:parenthesized negative"), "cash"],
     ["[[FA-0109|rec:asset tag]]", "Plate compactor (stolen 8/2025 - police rpt [[25-118403|rec:police report number]])", "[[WP1550AW-20184471|dev:equipment serial number]]", dt("2024-04-30"), amt(2689, "acct"), "MACRS 7-yr", amt(-2689, "acct", "money!:parenthesized negative"), "written off"],
     ["Total", None, None, None, amt(580744.49, "acct"), None, amt(-495266.34, "acct", "money!:parenthesized negative"), None],
     [None],
     ["Prepared by [[R. Delgado-Finch|p2:short:initial + surname]], bookkeeper. Reviewed w/ [[Earl Jr.|p1:nickname!:first name + suffix]] [[01/22/2026|date:review date]]. EIN [[41-1882047|taxid:EIN]]."],
   ]),
   ("Vehicles", [
     ["Unit", "Year / make / model", "VIN", "Plate", "Assigned driver", "Purchased", "Cost", "Insurance policy"],
     ["T-1", "2022 Ford F-350", "[[1FT8W3BT4NEC40718|veh:VIN]]", "[[MN YBR-4471|veh!:license plate with state prefix]]", "[[Earl T. Kowalski Jr.|p1:full]]", dt("2022-01-14", "m/d/yyyy"), amt(71240, "usd"), "[[SSA-CA-7714205|rec:policy number]]"],
     ["T-2", "2020 Ram 2500", "[[3C6UR5DL8LG211094|veh:VIN]]", "[[MN 218-KTP|veh!:license plate with state prefix]]", "[[Warsame, Abdirahman|p3:last-first]]", dt("2020-08-03", "m/d/yyyy"), amt(48915.25, "usd"), "SSA-CA-7714205"],
     ["T-3", "2018 Chevrolet Silverado 3500", "[[1GC4KYEY5JF187302|veh:VIN]]", "[[MN 904-HLW|veh!:license plate with state prefix]]", "pool", dt("2018-11-19", "m/d/yyyy"), amt(39800, "usd"), "SSA-CA-7714205"],
     ["D-1", "2017 Kenworth T880 dump", "[[1NKZX4TX6HJ155263|veh:VIN]]", "[[MN PAK 3382|veh!:license plate with state prefix]]", "[[Gus Papadakis|p5:full]] (CDL [[P-204-771-339-018|govid:driver's license number]])", dt("2019-03-08", "m/d/yyyy"), amt(118000, "usd"), "[[SSA-CA-7714206|rec:policy number]]"],
     ["TR-1", "2021 Towmaster T-50 trailer", "[[4KNFT5038ML160427|veh:VIN]]", "[[MN TRL 8840|veh!:license plate with state prefix]]", "n/a", dt("2021-06-07", "m/d/yyyy"), amt(27350, "usd"), "SSA-CA-7714206"],
     [None],
     ["Note: T-2 personal-use log missing for Q3. [[Abdi|p3:nickname]] took the truck home to [[Cloquet|place:city]] nightly from [[7/7/2025|date:start of personal use]]; fringe benefit to be added to his W-2."],
     ["Agent: [[Paulette Nakamura|p4:full]], [[Superior Shores Insurance Agency|o4:full]], [[218-555-0114|phone]], [[pnakamura@superiorshores.example|email]]"],
   ]),
   ("Vendors", [
     ["Vendor", "Contact", "Phone", "Address", "City/State/ZIP", "Tax ID", "1099?", "Terms", "YTD paid", "Remit to"],
     ["[[Iron Range Tractor & Implement Co.|o3:full]]", "parts desk", "[[(218) 555-0161|phone]]", "[[4402 Highway 53|addr]]", "[[Virginia|place!:city that is also a state name]], [[MN|place:state abbreviation]] [[55792|zip]]", "[[41-0773921|taxid:EIN]]", "N", "Net 30", amt(41882.17, "usd"), "ACH [[074375460|rtn]] / [[1004477821|acct]]"],
     ["[[North Country Diesel Repair|o5:full]]", "[[LaTonya Briggs|p6:full]]", "[[218.555.0138|phone:dotted]]", "[[RR 2 Box 114|addr:rural route]]", "[[Hermantown|place:city]], MN [[55811|zip]]", "[[XXX-XX-7421|ssn!:masked SSN used as tax ID]]", "Y", "Due on receipt", amt(18406.5, "usd"), "check"],
     ["[[Arrowhead Aggregate Supply Corp.|o6:full]]", "dispatch", "[[1-800-555-0199|phone:toll-free]]", "[[PO Box 3381|addr:PO Box]]", "[[Duluth|place:city]], MN [[55803-3381|zip:ZIP+4]]", "[[41-1620884|taxid:EIN]]", "N", "Net 30", amt(96210, "usd"), "ACH [[027304349|rtn]] / [[88-20417-3|acct]]"],
     ["[[Papadakis Welding|o7:full]]", "[[Gus|p5:first-name]] (also our dump truck driver - related party? ask CPA)", "[[218-555-0170|phone]]", "[[1917 W 4th St|addr]]", "Duluth, MN [[55806|zip]]", "[[317-76-0261|ssn:SSN used as tax ID]]", "Y", "Due on receipt", amt(7350, "usd"), "check"],
     ["[[Duluth Harbor Fuel Co-op|o8:full]]", "accounts", "[[218 555 0125|phone:spaces]]", "[[600 Garfield Ave|addr]]", "Duluth, MN [[55802|zip]]", "[[41-0294417|taxid:EIN]]", "N", "Net 15", amt(63927.84, "usd"), "card ending 0274"],
     ["Twin Ports Equipment Finance LLC", "loan servicing", "[[888-555-0133|phone:toll-free]]", "[[PO Box 90220|addr:PO Box]]", "[[Superior|place!:city that is also a common word]], [[WI|place:state abbreviation]] [[54880|zip]]", "n/a", "N", "monthly", amt(58114.2, "usd"), "autopay"],
   ]),
  ]))

# ---------------------------------------------------------------- 90
DOCS.append(D(90, "txt", "audit workpaper", "accounting", "US",
  title="Audit workpaper - related party transactions",
  ents={"p1": "Anselm Varga", "p2": "Katalin Varga-Thorne", "p3": "Desmond Thorne",
        "p4": "Imani Castellano", "p5": "Hye-jin Kwon", "p6": "Felix Baumgartner-Ruiz",
        "o1": "Varga Precision Castings, Inc.", "o2": "Thorne Logistics Group, LLC",
        "o3": "VPC Hungary Kft.", "o4": "Kwon Castellano & Associates, P.C.",
        "o5": "Blue Juniata Lake House LLC", "o6": "Susquehanna Heritage Bank",
        "o7": "Friends of Varga for County Commissioner"},
  distractors=["ASC 850", "AU-C 550", "Form 5472", "W/P ref. R-2", "PBC", "FYE"],
  ok=["12/31/2025"],
  body=r'''
[[Kwon Castellano & Associates, P.C.|o4:full]]                                       W/P ref. R-2
Client: [[Varga Precision Castings, Inc.|o1:full]] ("[[VPC|o1:acronym]]")                 FYE 12/31/2025
Subject: Related party transactions (AU-C 550 / ASC 850)
Prepared: [[I. Castellano|p4:short:initial + surname]] [[02/18/2026|date:prepared date]]        Reviewed: [[HJK|p5:initials]] [[02/24/2026|date:review date]]

OBJECTIVE
Identify related parties, test completeness of management's list (PBC item 41), and
evaluate whether transactions are disclosed and at terms we can describe.

RELATED PARTIES IDENTIFIED
(a) [[Anselm Varga|p1:full]] -- founder, CEO, 62% shareholder.
(b) [[Katalin Varga-Thorne|p2:full]] -- [[his daughter|indirect!:family relationship to a named person]], VP Operations, 19% shareholder.
(c) [[Desmond Thorne|p3:full]] -- [[Katalin's husband|indirect!:family relationship to a named person]]. Sole member of [[Thorne Logistics Group, LLC|o2:full]] ("[[TLG|o2:acronym]]").
    NOT on management's list. Found via vendor master: TLG's remit address is
    [[77 Quarry Hollow Road|addr]], [[Lewisburg|place:city]], [[PA|place:state abbreviation]] [[17837|zip]] -- same as [[Katalin|p2:first-name]]'s home address in HR file.
(d) [[VPC Hungary Kft.|o3:full]] -- 100% sub, [[Gyor|place:city]]. Managing director [[Felix Baumgartner-Ruiz|p6:full]].
(e) [[Blue Juniata Lake House LLC|o5:full]] -- owned by [[Mr. Varga|p1:title-surname]] personally. See item 4.

TRANSACTIONS TESTED
1. Freight paid to TLG: [[$1,284,300|money]] (2024: [[$402,150|money]]). Tripled. No bids obtained. Traced
   12 invoices; rates run 18-22% above the two carriers VPC used before. Controller says
   "[[Des|p3:nickname]] is reliable." Proposed: disclose; discuss with audit committee.
2. Intercompany: VPC wired [[EUR 640,000|money!:currency code prefix]] to the sub on [[14 March 2025|date:wire date]]. Booked as loan, no
   note on file. Beneficiary account IBAN [[FR58 5640 7655 8395 8814 5082 902|iban]] -- that is a FRENCH
   IBAN, not Hungarian. [[Baumgartner-Ruiz|p6:surname]] says the sub banks in [[Lyon|place:city]] "for convenience."
   Requested bank confirmation direct. Form 5472 n/a (VPC is the US parent) but confirm w/ tax.
3. Shareholder loan to Mr. Varga: opening balance [[$350,000|money]]; advances [[$125,000|money]] on [[6/2/2025|date:advance date]] and
   [[$90,000|money]] on [[10/20/2025|date:advance date]]; no repayments; closing [[$565,000|money]]. Interest accrued at 4%,
   not paid. Advances went by wire from the [[Susquehanna Heritage Bank|o6:full]] operating account
   ([[xxxxxx4093|acct!:masked account number]]) to his personal account [[7782-0-116459|acct]].
4. Lake house: VPC paid [[$48,600|money]] of "customer entertainment facility" costs to Blue Juniata
   Lake House LLC, incl. dock repair and a pontoon ([[the "Molten Lady"|indirect!:named boat]]). Usage log shows
   3 customer events and 41 family days. Personal use >> business. Proposed AJE to
   reclass to shareholder loan; tax to consider constructive dividend.
5. Political: [[$10,000|money]] check [[#20417|rec:check number]] dated [[9/30/2025|date:check date]] to [[Friends of Varga for County Commissioner|o7:full]],
   coded to "dues & subscriptions." [[Mr. Varga is the candidate|attr!:political candidacy]]. Corporate contribution; non-
   deductible; legal exposure -- refer to counsel. Controller unaware it was an issue.

OTHER
- [[Ms. Varga-Thorne|p2:title-surname]] signed the management rep letter draft for related parties. Given (c),
  [[Hye-jin Kwon|p5:full]] wants the CEO and the board chair to sign instead.
- Per HR, [[Mr. Thorne|p3:title-surname]] was a VPC employee until 2022; [[terminated after a positive drug test|health!:substance use, employment record]].
  Not relevant to the financial statements; do not carry forward.

CONCLUSION
Management's list incomplete. Items 1, 3, 4 require disclosure. Item 5 communicated to
those charged with governance [[2/26/2026|date:communication date]]. Passed adjustment schedule updated.
'''))
