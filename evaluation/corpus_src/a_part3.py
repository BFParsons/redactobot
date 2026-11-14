"""Batch A, documents 9-14 (imported by batch_a.py)."""
from corpus_src.dsl import D, dt, amt, num

DOCS = []

# ---------------------------------------------------------------- doc 9
_F = "mm/dd/yyyy"
DOCS.append(D(9, "xlsx", "bookkeeping ledger", "accounting", "US",
  title="General ledger detail and vendor list - veterinary clinic",
  ents={"p1": "Ingrid Solheim", "p2": "Karl Lindqvist", "p3": "Rahma Abdullahi", "p4": "Mai Yer Xiong",
        "p5": "Tyrell Washington", "p6": "Dale Hokanson", "p7": "Pete Kowalski", "p8": "Solveig Pedersen",
        "p9": "Freya Solheim", "p10": "Jenna Maki",
        "o1": "Tamarack Veterinary Clinic, PLLC", "o2": "Northwoods Veterinary Supply Co.",
        "o3": "Gopher State Payroll Services", "o4": "Borealis Reference Diagnostics", "o5": "Estate of Harold Bjornson",
        "o6": "Kowalski Snow & Lawn LLC", "o7": "Pedersen Family Trust", "o8": "Lake Country Community Bank",
        "o9": "Crow Wing Electric Cooperative", "o10": "Birchline Bookkeeping"},
  distractors=["Form 1099-NEC", "1010 Checking", "6100 Contract labor", "W-9 on file", "TPLO"],
  sheets=[
   ("GL Jan 2026", [
    ["Date", "Ref", "Payee / description", "Account", "Debit", "Credit"],
    [dt("2026-01-02", _F), "DEP", "Daily deposit - client payments", "1010 Checking", amt(4812.5, "num"), None],
    [dt("2026-01-02", _F), "ACH", "[[Northwoods Veterinary Supply Co.|o2:full]]", "5100 Medical supplies", None, amt(2317.84, "num")],
    [dt("2026-01-05", _F), "1047", "[[Dr. Ingrid Solheim|p1:full:title + full name]] - owner draw", "3200 Owner draws", None, amt(6000, "num")],
    [dt("2026-01-05", _F), "1048", "[[Lindqvist, Karl|p2:last-first]] - relief vet, week of [[Dec 22|date!:month and day only]]", "6100 Contract labor", None, amt(1850, "num")],
    [dt("2026-01-06", _F), "DEP", "Client pmt - [[R. Abdullahi|p3:short:initial + surname]] (Biscuit, TPLO deposit)", "1010 Checking", amt(1200, "num"), None],
    [dt("2026-01-09", _F), "EFT", "[[Gopher State Payroll Services|o3:full]] - payroll [[01/09|date!:month/day only]]", "6000 Wages", None, amt(9412.66, "num")],
    [dt("2026-01-09", _F), "EFT", "[[Gopher State|o3:short!:short name that reads like a nickname]] - service fee", "6050 Payroll fees", None, amt(87.5, "num")],
    [dt("2026-01-12", _F), "CC", "Card ending [[0004|card!:last four only]] - [[Borealis Reference Diagnostics|o4:full]]", "5200 Lab fees", None, amt(1436.2, "num")],
    [dt("2026-01-13", _F), "1049", "[[Estate of Harold Bjornson|o5:full]] - refund of prepaid boarding", "4900 Refunds", None, amt(315, "num")],
    [dt("2026-01-14", _F), "DEP", "Client pmt - [[Xiong, Mai Yer|p4:last-first]] - payment plan 3 of 6", "1010 Checking", amt(250, "num"), None],
    [dt("2026-01-15", _F), "ACH", "MN Dept of Revenue - sales tax, December", "2200 Sales tax payable", None, amt(1108, "num")],
    [dt("2026-01-15", _F), "1050", "[[Kowalski Snow & Lawn LLC|o6:full]] - plowing x4", "6400 Grounds", None, amt(520, "num")],
    [dt("2026-01-16", _F), "WIRE", "[[Pedersen Family Trust|o7:full]] - January rent, [[412 Birch Ave|addr]]", "6300 Rent", None, amt(4200, "num")],
    [dt("2026-01-20", _F), "ACH", "[[Lake Country Community Bank|o8:full]] - loan [[70-118834|rec:loan number]] P&I", "2500 Equipment loan", None, amt(1764.19, "num")],
    [dt("2026-01-21", _F), "1051", "[[Tyrell Washington|p5:full]] - reimbursement, CE conference", "6700 Education", None, amt(642.37, "num")],
    [dt("2026-01-22", _F), "EFT", "[[Crow Wing Electric Cooperative|o9:full]] - acct [[88-204417-02|rec:utility account number]]", "6500 Utilities", None, amt(731.08, "num")],
    [dt("2026-01-23", _F), "EFT", "Gopher State Payroll Services - payroll [[01/23|date!:month/day only]]", "6000 Wages", None, amt(9630.11, "num")],
    [dt("2026-01-26", _F), "DEP", "Insurance pmt - claim [[PET-2025-448102|rec:insurance claim number]] ([[Abdullahi|p3:surname!]])", "1010 Checking", amt(2875, "num"), None],
    [dt("2026-01-27", _F), "JE-03", "Reclass personal charge - orthodontist, [[owner's daughter Freya|indirect!:family relationship to a named person]]", "3200 Owner draws", amt(1950, "num"), None],
    [dt("2026-01-27", _F), "JE-03", "Reclass personal charge - contra", "6800 Misc", None, amt(1950, "num")],
    [dt("2026-01-29", _F), "1052", "[[K. Lindqvist|p2:short:initial + surname]] - relief vet, [[Jan 19-23|date!:date range, month and days only]]", "6100 Contract labor", None, amt(2220, "num")],
    [dt("2026-01-30", _F), "CHG", "NSF - returned check, [[M. Xiong|p4:short:initial + surname]]", "1010 Checking", None, amt(250, "num")],
    [dt("2026-01-30", _F), "FEE", "Bank service charge", "6900 Bank fees", None, amt(-35, "numacct")],
    [None, None, "Ending balance, acct [[2201 884 0731|acct!:account number with spaces]]", "1010 Checking", amt(38214.77, "usd"), None],
   ]),
   ("Vendors", [
    ["Vendor", "Contact", "Phone", "Email", "Tax ID", "Notes", "Address", "City", "ST", "ZIP", "Since"],
    ["Northwoods Veterinary Supply Co.", "[[Dale Hokanson|p6:full]]", "[[218-555-0121|phone]]", "[[ar@northwoodsvet.example|email]]", "[[41-1773025|taxid:EIN]]", "W-9 on file", "[[7200 Hwy 371 N|addr:highway address]]", "[[Brainerd|place:city]]", "[[MN|place:state abbreviation]]", num(56401, "zip!:ZIP stored as a number"), dt("2019-03-11", "m/d/yyyy", "date:vendor since")],
    ["[[Karl Lindqvist|p2:full]], DVM", "self", "[[(612) 555-0158|phone]]", "[[karl.lindqvist@vetrelief.example|email]]", num(291943244, "ssn!:SSN stored as a number"), "Form 1099-NEC", "[[3318 Emerson Ave S, Apt 2|addr:street with apartment]]", "[[Minneapolis|place:city]]", "MN", "[[55408|zip]]", dt("2024-06-03", "m/d/yyyy", "date:vendor since")],
    ["Kowalski Snow & Lawn LLC", "[[Pete Kowalski|p7:full]]", "[[218.555.0176|phone:dotted]]", "[[pete@kowalskisnow.example|email]]", "[[84-2290417|taxid:EIN]]", "W-9 on file", "[[RR 2 Box 114|addr!:rural route address]]", "[[Pequot Lakes|place:town]]", "MN", "[[56472|zip]]", dt("2021-11-01", "m/d/yyyy", "date:vendor since")],
    ["Pedersen Family Trust", "[[Solveig Pedersen|p8:full]], trustee", "[[218-555-0103|phone]]", "none - mail only", "[[41-6620883|taxid:EIN of a trust]]", "landlord", "[[PO Box 77|addr:PO Box]]", "[[Nisswa|place:town]]", "MN", "[[56468|zip]]", dt("2016-08-15", "m/d/yyyy", "date:vendor since")],
    ["Borealis Reference Diagnostics", "accounts dept", "[[1-888-555-0144|phone:toll-free]]", "[[billing@borealisdx.example|email]]", "[[39-2044718|taxid:EIN]]", "pay by card", "[[4100 Enterprise Dr, Ste 300|addr:street with suite]]", "[[Eau Claire|place:city]]", "[[WI|place:state abbreviation]]", "[[54703|zip]]", dt("2022-02-07", "m/d/yyyy", "date:vendor since")],
    ["Tyrell Washington", "employee [[E-0417|rec:employee ID]]", "[[218-555-0190|phone]]", "[[twashington@tamarackvet.example|email]]", None, "reimbursements only", None, None, None, None, dt("2023-09-18", "m/d/yyyy", "date:hire date")],
    [None],
    ["Prepared for [[Tamarack Veterinary Clinic, PLLC|o1:full]] by [[Birchline Bookkeeping|o10:full]] ([[J. Maki|p10:short:initial + surname]])"],
   ]),
  ]))

# ---------------------------------------------------------------- doc 10
DOCS.append(D(10, "docx", "IRS correspondence summary", "accounting", "US",
  title="IRS correspondence summary - underreporter notice",
  ents={"p1": "Gwendolyn P. Farnsworth-Ito", "p2": "Hiroshi Ito", "p3": "Renee Calloway", "p4": "Naomi Ito-Reyes",
        "p5": "Hadley",
        "o1": "Calloway Tax & Advisory", "o2": "Pinnacle Ridge Brokerage", "o3": "Pacific Cannery Workers Pension Trust",
        "o4": "Cedar Glen Memory Care"},
  distractors=["CP2000", "Form 2848", "Form 1099-B", "Form 1099-R", "Form 8949", "tax year 2023", "IRC § 6662"],
  body=r'''
# IRS Correspondence Summary
**[[Calloway Tax & Advisory|o1:full]]** - client file memo
| Item | Detail |
| Client | [[Gwendolyn P. Farnsworth-Ito|p1:full]] |
| Client no. | [[2019-0338|rec!:client number that looks like a year range]] |
| SSN | [[XXX-XX-3244|ssn!:masked SSN]] |
| Notice | CP2000, tax year 2023 |
| Notice date | [[December 8, 2025|date:notice date]] |
| AUR control no. | [[71003-4418-2|rec:IRS control number]] |
| Prepared by | [[Renee Calloway|p3:full]], EA |
| Memo date | [[1/6/2026|date:numeric date]] |
## What the notice says
The IRS matched third-party forms against the 2023 joint return filed by [[Mrs. Farnsworth-Ito|p1:title-surname]] and her late husband, [[Hiroshi Ito|p2:full]] (died [[July 3, 2024|date:date of death]]; his SSN ends in [[7914|ssn!:last four only]]). It proposes additional tax of [[$6,418|money]], a 20% accuracy penalty under IRC § 6662 of [[$1,284|money]], and interest of [[$512.33|money]], for a total of [[$8,214.33|money]].
Two items drive the change. First, Form 1099-B from [[Pinnacle Ridge Brokerage|o2:full]] (account [[811-40297|acct:brokerage account number]]) reported proceeds of [[$58,900|money]] with no basis shown, and the return left the sale off entirely. Second, a Form 1099-R from the [[Pacific Cannery Workers Pension Trust|o3:full]] showed a [[$4,100|money]] distribution to [[Mr. Ito|p2:title-surname]] that was not reported.
## Our assessment
The pension item is correct and we will agree to it. The brokerage item is mostly wrong: the shares were inherited from [[Gwen|p1:nickname]]'s mother in 2021 and the stepped-up basis was [[$51,220|money]], so the real gain is [[$7,680|money]], long-term. We estimate the corrected balance at roughly [[$1,900|money]] before interest and will ask for the penalty to be waived, since the omission happened during the months [[Hiroshi|p2:first-name]] was in [[hospice care|health!:end-of-life care]].
## Contact with the IRS
I called the number on the notice on [[1/5/26|date!:numeric date with two-digit year]] and spoke with [[Mr. Hadley|p5:title-surname]] (ID [[1004471892|govid:IRS employee ID number]]). He granted a 30-day extension; our response is now due [[February 6, 2026|date:response deadline]]. The response goes by fax to [[855-555-0118|phone:fax]]. My CAF number is [[0312-44871-R|govid:IRS CAF number]].
## Authority to act
[[Mrs. Ito|p1:title-surname!:shortened married surname]] has been living at [[Cedar Glen Memory Care|o4:full]] in [[Astoria|place:city]] since October and was diagnosed with [[Alzheimer's disease|health:diagnosis]] last year. Her daughter, [[Naomi Ito-Reyes|p4:full]], holds a durable power of attorney and signed Form 2848 on her behalf. All calls and mail go to [[Naomi|p4:first-name]]: [[503-555-0156|phone]], [[naomi.itoreyes@inboxmail.example|email]], [[1915 SE Clinton St|addr]], [[Portland|place:city]], [[Oregon|place:state]] [[97202|zip]]. Do not phone [[Cedar Glen|o4:short!]].
## Next steps
- Prepare Form 8949 with the inherited basis; attach the estate's date-of-death valuation.
- Draft the response and penalty waiver request for Naomi's signature by [[January 23|date!:month and day only]].
- If a balance remains, Naomi wants it debited from the estate checking account ending [[5590|acct!:last four only]].
'''))

# ---------------------------------------------------------------- doc 11
DOCS.append(D(11, "txt", "bank reconciliation notes", "accounting", "US",
  title="Bank reconciliation notes - seafood wholesaler",
  ents={"p1": "Manuel Ferreira", "p2": "Luz Andrade", "p3": "Teresa Ferreira-Costa", "p4": "Brian Whitlock",
        "o1": "Ferreira & Daughters Seafood Wholesale, Inc.", "o2": "Buzzards Bay Savings Bank",
        "o3": "Nordsee Fischhandel GmbH", "o4": "Acushnet Ice & Cold Storage", "o5": "Whaling City Diesel"},
  distractors=["GL 1010", "JANUARY 2026", "Form 941", "ACH", "QuickBooks"],
  body=r'''
BANK REC NOTES -- JANUARY 2026
[[Ferreira & Daughters Seafood Wholesale, Inc.|o1:full]]  ([[F&D|o1:acronym]])
Operating acct, [[Buzzards Bay Savings Bank|o2:full]], [[0081-447-2209|acct:account number with dashes]]   (GL 1010)
Done by [[Luz|p2:first-name!:first name that is also a word in another language]], [[2/6/26|date!:numeric date with two-digit year]]. Reviewed: not yet.

Balance per bank stmt [[1/31/26|date!:numeric date with two-digit year]]              [[$142,907.36|money]]
Add deposits in transit ([[1/30|date!:month/day only]], [[1/31|date!:month/day only]])           [[18,440.00|money!:amount without currency sign]]
Less outstanding checks (list below)              [[(27,315.88)|money!:parenthesized negative]]
Adjusted bank balance                              [[134,031.48|money!:amount without currency sign]]
Balance per books (QuickBooks)                     [[152,476.48|money!:amount without currency sign]]
UNRECONCILED DIFFERENCE                            [[(18,445.00)|money!:parenthesized negative]]

Outstanding checks
  #20418   [[Acushnet Ice & Cold Storage|o4:full]]      [[$9,600.00|money]]
  #20422   [[Whaling City Diesel|o5:full]]               [[$4,115.88|money]]
  #20425   [[Brian Whitlock|p4:full]] (truck lease)       [[$13,600.00|money]]

What I think the difference is
1. Wire out [[1/22|date!:month/day only]] for [[$18,400.00|money]] plus [[$45.00|money]] fee -- not in the books at all. Bank detail
   says beneficiary [[Nordsee Fischhandel GmbH|o3:full]], [[Bremerhaven|place:city]], IBAN
   [[DE32 3550 3921 3458 5519 11|iban:IBAN with spaces]], BIC [[NOSFDEHHXXX|acct:SWIFT code]]. No invoice in the folder. [[Manny|p1:nickname]] says it
   is a deposit on the spring halibut order and "[[Teresa|p3:first-name]] has the paperwork." She is
   out until the 16th.
2. That leaves zero. Good. But see 3.

Other things I noticed
3. Three debit card charges on the card ending [[0483|card!:last four only]] (Manny's) at a casino in
   [[Uncasville|place:town]]: [[$400|money]], [[$400|money]], [[$800|money]] on [[1/17|date!:month/day only]]. Booked to "Travel." I moved them
   to shareholder loan pending his OK. This is the third month in a row.
4. Payroll acct (ending [[2217|acct!:last four only]]) was short on [[1/16|date!:month/day only]]; bank auto-swept [[$6,250|money]] from
   operating. Transfer not recorded. Fixed.
5. ACH debit [[1/20|date!:month/day only]], [[$3,871.14|money]], "IRS USATAXPYMT" -- that is the Q4 Form 941 balance.
   OK, but it was coded to officer salary. Fixed.
6. Bank still shows [[Manuel Ferreira|p1:full]] as the only signer. [[Teresa Ferreira-Costa|p3:full]] was
   supposed to be added in November. The branch says the signature card was never returned. Their number is
   [[508-555-0131|phone]]; routing for the new ACH setup is [[016117880|rtn]].

For Teresa when she is back: need the [[Nordsee|o3:short!:one-word short name]] invoice and the wire authorization,
and someone other than [[Mr. Ferreira|p1:title-surname]] should be approving wires over [[10k|money!:abbreviated with k, no currency sign]].
                                                        -- [[L. Andrade|p2:short:initial + surname]]
'''))

# ---------------------------------------------------------------- doc 12
DOCS.append(D(12, "pdf", "invoice", "accounting", "US",
  title="Invoice - design studio to dental practice",
  ents={"p1": "Samuel Osei-Bonsu", "p2": "Priscilla Achterberg", "p3": "Lucía Montoya",
        "o1": "Brightwater Design Studio LLC", "o2": "Osei Family Dentistry, P.A.", "o3": "Gulf Coast Commerce Bank"},
  distractors=["Net 30", "1.5% per month", "Form W-9", "Qty", "Phase 2"],
  body=r'''
# INVOICE
**[[Brightwater Design Studio LLC|o1:full]]**
[[418 Magnolia Court, Studio B|addr:street with unit]]
[[St. Petersburg|place:city]], [[FL|place:state abbreviation]] [[33701|zip]]
[[(727) 555-0114|phone]] / [[billing@brightwaterdesign.example|email]]
EIN [[59-3310847|taxid:EIN]] (Form W-9 available on request)
| Invoice no. | [[BW-2026-0142|rec:invoice number]] |
| Invoice date | [[Feb 3, 2026|date:abbreviated month]] |
| Due date | [[Mar 5, 2026|date:abbreviated month]] |
| Terms | Net 30 |
| Your PO | [[4471-B|rec:purchase order number]] |
**Bill to:**
[[Osei Family Dentistry, P.A.|o2:full]]
Attn: [[Dr. Samuel Osei-Bonsu|p1:full:title + full name]]
[[2750 Fourth Street North, Suite 110|addr:street with suite]]
St. Petersburg, FL [[33704|zip]]
## Services, January 2026 (Phase 2: website and patient forms)
| Description | Qty | Rate | Amount |
| Web design | 22 h | [[$135.00|money]] | [[$2,970.00|money]] |
| Copywriting | 9 h | [[$95.00|money]] | [[$855.00|money]] |
| Photo session | 1 | [[$650.00|money]] | $650.00 |
| Stock images | 6 | [[$12.50|money]] | [[$75.00|money]] |
| Subtotal | | | [[$4,550.00|money]] |
| Sales tax | | | [[$5.25|money]] |
| Deposit paid | | | [[($1,500.00)|money!:parenthesized negative]] |
| **Balance due** | | | [[$3,055.25|money]] |
## How to pay
Online: [[https://pay.brightwaterdesign.example/i/BW-2026-0142|url:payment link containing the invoice number]]
ACH: [[Gulf Coast Commerce Bank|o3:full]], routing [[072842966|rtn]], account [[000123886041|acct]].
International wire: IBAN [[IE60AIBK90660631872110|iban!:IBAN without spaces]], reference the invoice number.
Card on file: the Visa ending [[9031|card!:last four only]] (exp. [[11/27|exp]]) will be charged on the due date unless [[Priscilla|p2:first-name]] in your office tells us otherwise.
## Notes
[[Dr. Osei-Bonsu|p1:title-surname]], the photo session on [[January 17|date!:month and day only]] covered you and the two hygienists only; [[Dr. Achterberg|p2:title-surname]] was out. We can add her portrait at no charge when she is back from [[maternity leave|health!:pregnancy-related leave]]. Past-due balances accrue a late charge of 1.5% per month.
Questions: [[Lucía Montoya|p3:full]], studio manager, [[lucia@brightwaterdesign.example|email]], [[727.555.0162|phone:dotted]].
Thank you for your business.
'''))

# ---------------------------------------------------------------- doc 13
DOCS.append(D(13, "eml", "internal email", "accounting", "CA", enc="plain",
  title="Email - T4 preparation problems (Manitoba contractor)",
  ents={"p1": "Nathalie Tremblay-Singh", "p2": "Bohdan Kravchuk", "p3": "Oleksandr Petrenko", "p4": "Jean-Luc Fontaine",
        "p5": "Destiny Moose-Flett", "p6": "Halyna Kravchuk",
        "o1": "Prairie Ledger Bookkeeping Inc.", "o2": "Kravchuk Electric Ltd.", "o3": "Assiniboine Credit Co-operative"},
  distractors=["PD7A", "box 14", "box 71", "section 87", "CRA", "T4s", "end of February"],
  headers={
    "From": "[[Nathalie Tremblay-Singh|p1:full]] <[[nathalie@prairieledger.example|email]]>",
    "To": "[[Bohdan Kravchuk|p2:full]] <[[bohdan@kravchukelectric.example|email]]>",
    "Cc": "[[halyna.k@kravchukelectric.example|email]]",
    "Subject": "T4s for 2025 - three problems before I can file",
    "Date": "Mon, [[16 Feb 2026|date:email header date]] 08:47:03 -0600"},
  body=r'''
Hi [[Bohdan|p2:first-name]],

I'm ready to file the 2025 T4s for [[Kravchuk Electric Ltd.|o2:full]] (payroll account [[72114 8830 RP0001|taxid:Canadian payroll program account number]]) but three things are stopping me. They are due at the end of February, so I need answers this week please.

1. [[Sasha|p3:nickname]]. The SIN I have for [[Oleksandr Petrenko|p3:full]] is [[935 589 010|taxid!:SIN beginning with 9, with spaces]]. A SIN that starts with 9 is temporary and has an expiry date. His file says the [[work permit expires June 30, 2026|attr!:immigration status]], but I have no copy of the permit and nothing showing the SIN is still valid. Can you get a photo of both from him? Gross for the year was [[$58,214.60|money]], so this is not a small slip.

2. [[Jean-Luc Fontaine|p4:full]]. He started [[2025-09-08|date:hire date, ISO format]] and I was never given a SIN at all, just "will bring it Monday" on the TD1. I cannot file his slip without one. He was paid [[C$19,877.25|money!:Canadian dollar prefix]]. His cell is [[204-555-0148|phone]] if [[Halyna|p6:first-name]] wants to chase him.

3. [[Destiny Moose-Flett|p5:full]]. She gave you a letter in October saying she is a [[registered Status Indian|attr:Indigenous status]] and that part of her work was on reserve at [[Peguis|place:community]]. If that is right, some of her pay is exempt under section 87 and goes in box 71 instead of box 14, and we over-deducted tax from about [[$11,400|money]] of it. I need the dates and the job site address to split it properly. Please do not guess. [[Destiny|p5:first-name!:first name that is also a common word]] knows which weeks they were.

Also, for the record, the SINs I do have on file and will use: [[Halyna Kravchuk|p6:full]] [[652-040-619|taxid:SIN with dashes]], you [[273682658|taxid!:SIN without separators]].

Last thing. I tried to log in to CRA My Business Account to check the PD7A balance and the password you gave me no longer works (user ID [[kravchukelec1|cred:username]], password [[Volts&Amps2024|cred!:password in an email]]). If you changed it, please do NOT email me the new one. Phone me at [[204.555.0113|phone:dotted]] or come by: [[887 Pembina Hwy, Unit 6|addr:street with unit]], [[Winnipeg|place:city]], [[MB|place!:province abbreviation]] [[R3M 2M3|zip:Canadian postal code]].

December's remittance of [[$4,318.09|money]] did go through from the [[Assiniboine Credit Co-operative|o3:full]] account on [[Jan 15|date!:month and day only]], so at least that part is fine.

Thanks,
[[Nathalie|p1:first-name]]

[[Prairie Ledger Bookkeeping Inc.|o1:full]]
'''))

# ---------------------------------------------------------------- doc 14
DOCS.append(D(14, "txt", "payroll summary", "accounting", "US",
  title="Biweekly payroll summary - tool and die shop",
  ents={"p1": "Marisela Lopez", "p2": "Thanh Nguyen", "p3": "DeShawn Jefferson", "p4": "Earl Hargrove III",
        "p5": "Katarzyna Wisniewski", "p6": "Bill McAllister", "p7": "Rosa Delgado",
        "o1": "Hargrove Tool & Die Co.", "o2": "Machinists Lodge 2211", "o3": "Cuyahoga Valley Bank",
        "o4": "PayRight Processing"},
  distractors=["Form 668-W", "Form W-4", "FMLA", "401(k)", "FICA", "PP 03"],
  ok=["02/01/2026 - 02/14/2026"],
  body=r'''
[[HARGROVE TOOL & DIE CO.|o1:caps]] -- PAYROLL SUMMARY
Pay period PP 03: 02/01/2026 - 02/14/2026        Check date: [[02/20/2026|date:pay date]]
Prepared by: [[R. Delgado|p7:short:initial + surname]], office mgr.      Processor: [[PayRight Processing|o4:full]], client ID [[HTD-0932|rec:payroll client ID]]

EMP ID  NAME                    SSN          RATE     HRS    GROSS      DUES    401(k)   GARN     NET       DD ACCT
[[1004|rec!:short employee ID]]    [[HARGROVE, EARL III|p4:last-first]]      [[***-**-6631|ssn!:masked SSN]]  salary   --     [[4,807.69|money!:amount without currency sign]]   --      [[480.77|money!:amount without currency sign]]   --       [[3,102.14|money!:amount without currency sign]]  [[x4410|acct!:masked account, last four]]
[[1017|rec!:short employee ID]]    [[McALLISTER, BILL|p6:last-first]]        [[***-**-6423|ssn!:masked SSN]]  [[$34.10|money:hourly rate]]   88.0   [[3,137.20|money!:amount without currency sign]]   [[41.50|money!:amount without currency sign]]   [[156.86|money!:amount without currency sign]]   --       [[2,207.55|money!:amount without currency sign]]  [[x0927|acct!:masked account, last four]]
[[1022|rec!:short employee ID]]    [[NGUYEN, THANH|p2:last-first]]           [[***-**-2374|ssn!:masked SSN]]  [[$29.75|money:hourly rate]]   24.0   [[714.00|money!:amount without currency sign]]     41.50   --       --       [[548.31|money!:amount without currency sign]]    [[x7718|acct!:masked account, last four]]
[[1031|rec!:short employee ID]]    [[JEFFERSON, DeSHAWN|p3:last-first]]      [[***-**-3202|ssn!:masked SSN]]  [[$27.40|money:hourly rate]]   80.0   [[2,192.00|money!:amount without currency sign]]   41.50   [[65.76|money!:amount without currency sign]]    [[412.00|money!:amount without currency sign]]   [[1,201.92|money!:amount without currency sign]]  paper ck
[[1038|rec!:short employee ID]]    [[LOPEZ, MARISELA|p1:last-first]]         [[***-**-7914|ssn!:masked SSN]]  [[$22.00|money:hourly rate]]   80.0   [[1,760.00|money!:amount without currency sign]]   --      --       --       [[1,428.47|money!:amount without currency sign]]  [[x3355|acct!:masked account, last four]]
[[1040|rec!:short employee ID]]    [[WISNIEWSKI, KATARZYNA|p5:last-first]]   [[***-**-7802|ssn!:masked SSN]]  [[$24.50|money:hourly rate]]   76.5   [[1,874.25|money!:amount without currency sign]]   41.50   [[93.71|money!:amount without currency sign]]    --       [[1,397.08|money!:amount without currency sign]]  [[x6102|acct!:masked account, last four]]

TOTALS: gross [[$14,485.14|money]]; employer FICA [[$1,108.11|money]]; net pay [[$9,885.47|money]]
ACH file sent [[2/18|date!:month/day only]] to [[Cuyahoga Valley Bank|o3:full]], RTN [[098025107|rtn]], funding acct [[5500081729|acct]].

NOTES THIS PERIOD
- [[Nguyen|p2:surname!]]: out on FMLA since [[2/5|date!:month/day only]] ([[rotator cuff surgery|health:procedure]]). Three days worked, then
  short-term disability takes over. Expected back mid-April. Do not discuss on the floor.
- [[Jefferson|p3:surname!]]: garnishment is the [[child support order|attr!:family court obligation]], [[Summit County|place:county]] case no.
  [[DR-2019-04-1182|rec:domestic relations case number]], $412.00 per period. Separate IRS levy (Form 668-W) received [[2/11|date!:month/day only]]
  for [[$3,940.18|money]]; starts next period. He asked that [[Earl|p4:first-name]] not be told. Earl signs the
  levy acknowledgment, so that is not possible.
- [[Lopez|p1:surname!]]: new Form W-4 and name change. She was [[Marisela Pruitt|p1:full:former married name]] until the
  divorce was final in January. Update the bank record too; DD still shows [[Pruitt|p1:surname!:former surname]].
- Dues: $41.50 per period remitted to [[Machinists Lodge 2211|o2:full]] for the four [[union members|attr:union membership]].
  [[Wisniewski|p5:surname!]] joined [[1/26|date!:month/day only]]. Lopez and [[Hargrove|p4:surname!]] are not in the unit.
- [[McAllister|p6:surname!]]: turned 65 on [[February 9|dob!:birthday without year]]; wants to stop 401(k) deferrals next period.

Questions to [[Rosa|p7:first-name]], ext. 12, or [[rdelgado@hargrovetool.example|email]]. Shop line [[330-555-0170|phone]].
'''))
