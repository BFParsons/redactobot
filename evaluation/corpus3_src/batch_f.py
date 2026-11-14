from corpus3_src.core import D, dt, amt, num

DOCS = []

# ---------------------------------------------------------------- 351
DOCS.append(D(351, "txt", "bookkeeper handoff note", "accounting", "US", cardholders=["p1"],
  title="Departing bookkeeper's handoff note with logins, accounts and devices",
  ents={"p1": "Corwin Skaggs", "p2": "Trudy Vandermolen", "p3": "Keisha Rountree", "p4": "Lupe Arredondo", "p5": "R. Skaggs",
        "o1": "Mossback Outfitters, LLC", "o2": "Paradise Valley State Bank", "o3": "Hardy Reel Werkstatt GmbH",
        "o4": "Bitterbrush Payroll Co."},
  distractors=["QuickBooks Desktop 2024", "Form 941", "Synology DS220+", "1099", "W-2"],
  body=r'''
HANDOFF NOTES for [[Keisha|p3:first-name]] - [[Mossback Outfitters, LLC|o1:full]] books
from [[Trudy Vandermolen|p2:full]], last day [[Friday 11/14|date:weekday and month/day]]. Sorry this is a brain dump. Shred or lock up when you've moved everything into the password manager!!

OWNER: [[Corwin Skaggs|p1:full]], cell [[406-555-0119|phone]], [[corwin@mossbackoutfitters.example|email]]. He answers texts, not email. Shop is [[26 East Callender Street|addr:street with number in digits and direction]], [[Livingston|place:town]] [[MT|place:state abbreviation]] [[59047|zip]].
EIN [[81-4420871|taxid:EIN]]. MT withholding acct [[4418772-001-WTH|taxid:state withholding account number]].

BANK - [[Paradise Valley State Bank|o2:full]]
  operating  [[1104418772|acct]]   routing [[092662045|rtn]]
  payroll    [[1104418780|acct]]
  online banking: [[https://online.pvsb.example/business|url:online banking login page]]  user [[mossback_books|cred:online banking user name]]  pw [[Stonefly!Hatch26|cred:online banking password]]
  the token fob is in the top desk drawer. security question (first rod): [[Sage XP|cred:security question answer]]
  branch contact is [[Lupe Arredondo|p4:full]], direct [[406-555-0184|phone]] - she knows [[Corwin|p1:first-name]] and will call HIM, not you, to verify wires

COMPANY CARD (in Corwin's name, I keep a copy for online orders)
  Visa [[4304 2404 8340 0526|card]]  exp [[10/27|exp]]  cvv [[339|cvv]]  billing zip 59047
  statement closes the 22nd, autopay from operating

PAYROLL - [[Bitterbrush Payroll Co.|o4:full]]  client ID [[BB-20441|rec:payroll client ID]]
  login [[tvandermolen@mossbackoutfitters.example|email]] / [[Elk$Hair#Caddis|cred:payroll portal password]]  -> they need to re-issue under your email
  4 employees + 3 seasonal guides. Guides are 1099 except [[the one who is on a J-1 visa|indirect:worker identifiable by visa type]] (ask Corwin, paperwork in the blue folder)
  Form 941 filed through Q3. Q4 is yours.

QUICKBOOKS
  QuickBooks Desktop 2024 lives on the back-office PC, hostname [[MOSSBACK-BO1|dev:computer hostname]], serial on the sticker [[MXL4418K7Z|dev:computer serial number]]
  admin pw [[Rainbow2Brown|cred:accounting software password]]. Backups go nightly to the NAS (Synology DS220+, serial [[2140QRN441877|dev:NAS serial number]]) at [[192.168.10.40|ip:private LAN address]]
  remote in through the shop's static IP [[203.0.113.212|ip]] port 3390 - yes I know. tell him to get a VPN.

VENDORS THAT NEED CARE
  - [[Hardy Reel Werkstatt GmbH|o3:full]] (the German reel parts). They invoice in euros, usually [[EUR 3.200,00|money:European format with currency code]] or so a quarter. Wire only:
    IBAN [[DE19 0289 9499 5185 0830 84|iban]]   BIC [[HRWKDEFFXXX|acct:BIC / SWIFT code]]. Last one sent [[10/06|date:month/day only]], [[$3,512.44|money]] incl fee.
  - rent to the landlord is [[$2,850|money]] on the 1st by check, he will not take ACH

THINGS ONLY I KNOW (sorry)
  - Corwin takes [[$4,000|money]] owner draw twice a month. In August he took [[$22,000|money]] extra - that was [[his divorce settlement payment|indirect:owner's personal circumstances]], code it to draws not legal fees
  - the [[$600|money]]/mo to "[[R. Skaggs|p5:short:initial + surname]]" is [[his brother, who is in a rehab facility in Billings|indirect:family member in treatment]]. Personal. Draws.
  - sales tax: none ([[Montana|place:state]]) but the resort tax in [[West Yellowstone|place:town]] applies to the pop-up, permit [[WY-RT-0418|rec:resort tax permit number]]
  - my own W-2 will need mailing: [[311 South H Street|addr]], Livingston. SSN is in the payroll system, ends [[8297|ssn:last four digits only]]

call me if stuck, [[406.555.0102|phone:dotted]], until the end of the month. good luck - [[T.|p2:initials:single initial sign-off]]
'''))

# ---------------------------------------------------------------- 352
DOCS.append(D(352, "eml", "IT support ticket thread", "accounting", "US", enc="plain",
  title="Managed IT provider's ticket thread about remote access at a CPA firm",
  ents={"p1": "Nikhil Jagannathan", "p2": "Marguerite Tollefsen", "p3": "Stanley Ruffin", "p4": "Hatfield-Combs",
        "o1": "Greenbrier Managed IT", "o2": "Tollefsen Ruffin & Associates, CPAs"},
  distractors=["Windows Server 2022", "Lacerte", "RDP", "WISP", "IRS Publication 4557", "FortiGate 60F"],
  headers={"From": "[[Nikhil Jagannathan|p1:full]] <[[support@greenbriermit.example|email]]>",
           "To": "[[Marguerite Tollefsen|p2:full]] <[[mtollefsen@tollefsenruffin.example|email]]>",
           "Subject": "[Ticket [[#GB-204418|rec:support ticket number]]] RE: Stan can't get into Lacerte from home",
           "Date": "Tue, [[11 Nov 2025|date:email header date]] 15:37:52 -0500"},
  body=r'''
Hi [[Marguerite|p2:first-name]],

Summary of what we found and did today on ticket [[#GB-204418|rec:support ticket number]]. Please keep this email out of the shared mailbox since it has credentials in it.

1) Why [[Stan|p3:nickname]] was locked out
His VPN account ([[sruffin|cred:VPN user name]]) was locked after 14 failed sign-ins between 02:10 and 02:31 this morning. They were not him. The attempts came from [[198.51.100.19|ip]] and [[198.51.100.23|ip]], which are not addresses he has ever used. His normal home address is [[203.0.113.77|ip]].

2) What I changed
- Unlocked the account and set a temporary password: [[Maple-Tax-7741!|cred:temporary password]] (he must change it at first sign-in).
- Turned on the authenticator app requirement for all three partners. Enrollment link: [[https://vpn.tollefsenruffin.example/enroll|url:VPN enrollment link]]
- Closed RDP on the firewall (FortiGate 60F, serial [[FGT60FTK2204418|dev:firewall serial number]]). It had been open to the internet on the office address, [[203.0.113.30|ip]], since the old provider set it up.
- The tax server, [[TR-TAX01|dev:server hostname]] ([[10.20.0.5|ip:private LAN address]], Windows Server 2022), now only accepts connections from the VPN range.

3) Things I need from you
- Stan's laptop is not in our inventory. Ask him for the serial, or the MAC address from the sticker. The one that connected last night from his house showed as [[A4:5E:60:C1:44:18|dev:MAC address]], host name [[STANS-MACBOOK|dev:computer hostname]]. Is that a personal machine? Client returns should not be on it.
- Your written security plan (WISP) under IRS Publication 4557 still lists [[Stanley Ruffin|p3:full]] as the security coordinator. He told me on the phone he "doesn't do computers." Someone else should be named.
- Approval for the quote to replace the server backup drive: [[$1,140.00|money]] plus two hours at [[$145|money:hourly rate]].

4) Did they get in?
I do not think so. No successful sign-in from the unknown addresses, and the Lacerte audit log shows no activity overnight. But the password he was using, [[Ruffin1958|cred:reused password]], is his surname and what I assume is his birth year, and he confirmed he uses it for his email as well. Treat it as burned everywhere. If client data had been reached you would have reporting duties; right now you do not.

Call me on [[304-555-0147|phone]] if anything looks odd.

[[Nikhil|p1:first-name]]
[[Greenbrier Managed IT|o1:full]]

---- [[Marguerite Tollefsen|p2:full]] wrote on [[11/11/2025|date:numeric date]] 8:02 AM ----
[[Nikhil|p1:first-name]] - [[Stan|p3:nickname]] called me at 7 this morning, he can't get into the tax software from home and he has the [[Hatfield-Combs|p4:surname:client family name]] return due. He says it "just says locked." He's at [[304.555.0163|phone:dotted]]. Can you look first thing? Our office is [[1018 Kanawha Blvd E, Suite 300|addr:street with suite]], [[Charleston|place:city]], [[WV|place:state abbreviation]] [[25301|zip]] if you need to come by. - [[MT|p2:initials]]
[[Tollefsen Ruffin & Associates, CPAs|o2:full]]
'''))

# ---------------------------------------------------------------- 353
DOCS.append(D(353, "html", "online order receipt", "accounting", "US", raw_html=True, cardholders=["p1"],
  title="Emailed receipt for a payroll software subscription",
  ents={"p1": "Lucinda Aponte-Rhee", "o1": "Aponte Rhee Bookkeeping LLC", "o2": "Ledgerwing Payroll, Inc."},
  distractors=["Ledgerwing Plus", "Form W-9", "PCI DSS", "Terms of Service", "Order Summary"],
  body=r'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>Your receipt</title>
<style>body{font-family:Helvetica,Arial,sans-serif;color:#222} table{border-collapse:collapse} td{padding:4px 12px 4px 0} .muted{color:#777;font-size:12px}</style></head>
<body>
<div><b>[[Ledgerwing Payroll, Inc.|o2:full]]</b> &middot; Receipt</div>
<h2>Thanks, [[Lucinda|p1:first-name]]. Your payment went through.</h2>
<p>Order [[LW-ORD-7720441|rec:order number]] &middot; placed [[Nov 3, 2025|date:order date]] at 9:14 PM ET &middot; Invoice [[INV-00441877|rec:invoice number]]</p>
<h3>Order Summary</h3>
<table>
<tr><td>Ledgerwing Plus, annual plan (up to 25 client companies)</td><td>[[$1,188.00|money]]</td></tr>
<tr><td>Onboarding package</td><td>[[$250.00|money]]</td></tr>
<tr><td>Promo SMALLFIRM20</td><td>[[-$237.60|money:negative amount with leading minus]]</td></tr>
<tr><td>Sales tax (NJ 6.625%)</td><td>[[$79.53|money]]</td></tr>
<tr><td><b>Total charged</b></td><td><b>[[$1,279.93|money]]</b></td></tr>
</table>
<h3>Payment</h3>
<p>Visa ending in [[5958|card:last four of card]] (&bull;&bull;&bull;&bull; &bull;&bull;&bull;&bull; &bull;&bull;&bull;&bull; 5958), expires [[03/27|exp]]<br>
Name on card: [[LUCINDA M APONTE-RHEE|p1:caps:name as embossed on a card]]<br>
Authorization code [[08441K|rec:card authorization code]]. Your plan renews automatically on [[November 3, 2026|date:renewal date]] at the then-current price.</p>
<h3>Billed to</h3>
<p>[[Aponte Rhee Bookkeeping LLC|o1:full]]<br>
Attn: [[Lucinda Aponte-Rhee|p1:full]]<br>
[[77 Bloomfield Avenue, 2nd Floor|addr:street with floor]]<br>
[[Montclair|place:town]], [[NJ|place:state abbreviation]] [[07042|zip]]<br>
[[(973) 555-0124|phone]]</p>
<h3>Account</h3>
<table>
<tr><td>Account ID</td><td>[[ACC-441877|rec:customer account ID]]</td></tr>
<tr><td>Sign-in email</td><td>[[lucinda@aponterhee.example|email]]</td></tr>
<tr><td>Tax ID on file (Form W-9)</td><td>EIN ending [[0871|taxid:last four of EIN]]</td></tr>
<tr><td>Order placed from</td><td>IP [[203.0.113.164|ip]], Chrome on Windows</td></tr>
</table>
<p>View or download this invoice: [[https://billing.ledgerwing.example/invoices/INV-00441877?t=k7Zq41|url:invoice link with access token]]<br>
Manage your subscription: [[https://app.ledgerwing.example/account|url:account page]]</p>
<p class="muted">We never store your full card number (PCI DSS). Questions? Reply to this email or write to [[billing@ledgerwing.example|email]]. By purchasing you agree to the Terms of Service. If you did not make this purchase, call [[1-888-555-0190|phone:toll-free with country code]] right away.</p>
</body></html>
'''))

# ---------------------------------------------------------------- 354
DOCS.append(D(354, "txt", "fiduciary return workpaper memo", "accounting", "US", minors=["p4"],
  title="CPA workpaper memo on a trust's Form 1041 and beneficiary K-1s",
  ents={"p1": "Ottilie Hargesheimer", "p2": "Conrad Hargesheimer", "p3": "Brigid Hargesheimer-Abiola", "p4": "Felix Nwachi",
        "p5": "Raymond Sprague", "p6": "Marit Lindskog",
        "o1": "Ottilie Hargesheimer Revocable Trust", "o2": "Sprague & Lindskog, CPAs", "o3": "Loess Hills Trust Company",
        "o4": "Platte Meridian Securities"},
  distractors=["Form 1041", "Schedule K-1", "DNI", "65-day rule", "IRC § 663(b)", "Form 56"],
  body=r'''
[[Sprague & Lindskog, CPAs|o2:full]] - WORKPAPER MEMO                       Client no. [[4418-T|rec:client number]]
Re: [[Ottilie Hargesheimer Revocable Trust|o1:full]] u/a/d [[6/14/1996|date:trust agreement date]] - 2025 Form 1041
Prepared: [[ML|p6:initials]] ([[Marit Lindskog|p6:full]]) [[11/10/25|date:short numeric date]]      Reviewed: [[RS|p5:initials]] ________

1. STATUS OF THE TRUST
Grantor [[Ottilie Hargesheimer|p1:full]], born [[January 9, 1930|dob]], is living, [[age 95|age:labelled age]], and resides at [[the memory care unit at Prairie Commons|indirect:residence in a named care facility]] in [[Council Bluffs|place:city]]. The trust was a grantor trust reported under her SSN ([[096-76-6330|ssn]]) through 2024. On [[March 4, 2025|date:incapacity determination date]] two physicians certified [[incapacity (advanced Alzheimer's disease)|health:diagnosis]] under Article 7. Her son [[Conrad Hargesheimer|p2:full]] and [[Loess Hills Trust Company|o3:full]] became co-trustees. Counsel's view, which we follow: still a grantor trust for income tax while she lives, but the bank wants a separate EIN for its systems. EIN issued [[May 2025|date:month and year]]: [[42-4418720|taxid:EIN]]. So: file a 1041 as an information return with a grantor statement; all income to [[Ottilie|p1:first-name]]'s 1040.
   -> [[RS|p5:initials]]: agree? The bank's tax department prepared a draft treating it as a complex trust with K-1s. I think that is wrong but see section 3.

2. ASSETS AND INCOME (per the bank's statements through [[10/31/2025|date:statement date]])
   [[Platte Meridian Securities|o4:full]] acct [[PM-7720-4418|acct:brokerage account number]]     market value [[$2,318,440|money]]
        dividends [[$41,207.18|money]]; interest [[$22,910.44|money]]; LT gains [[$96,300|money]] (sale of the bank stock in April)
   Farmland, 240 acres, [[Pottawattamie County|place:county]], cash rent [[$74,400|money]] (tenant pays [[3/1|date:month/day only]] and [[12/1|date:month/day only]])
   [[Loess Hills|o3:short]] checking [[0044-18772|acct]]                    balance [[$58,206.91|money]]
   Trustee fees paid to the bank: [[$17,388|money]]. Our fee estimate: [[$2,600|money]].

3. DISTRIBUTIONS MADE IN 2025 - the problem
   The trust instrument lets the trustees make gifts "consistent with the grantor's pattern of giving." The co-trustees paid:
   - [[Brigid Hargesheimer-Abiola|p3:full]] (daughter), [[$19,000|money]] on [[6/2/25|date:short numeric date]]. SSN [[720-32-3072|ssn]]. Address [[4411 Underwood Avenue|addr]], [[Omaha|place:city]], [[NE|place:state abbreviation]] [[68132|zip]].
   - [[Felix Nwachi|p4:full]] (great-grandson, born [[2012|dob!:birth year only]]), [[$19,000|money]] into his 529 on 6/2/25, and tuition of [[$11,450|money]] paid directly to his school. SSN [[228-40-1229|ssn]]. [[Brigid|p3:first-name]] is custodian.
   - [[Conrad|p2:first-name]] himself, [[$60,000|money]] on [[8/15/25|date:short numeric date]], described in the trustee minutes as "advance on inheritance." SSN ending [[5625|ssn:last four digits only]].
   Under our reading these are gifts by Ottilie (grantor trust), not distributions carrying DNI, so no Schedule K-1 to anyone. [[Conrad|p2:first-name]]'s [[$60,000|money]] exceeds the annual exclusion: a gift tax return is needed for 2025, and frankly [[a co-trustee paying himself from an incapacitated parent's trust|indirect:possible self-dealing by a named trustee]] is something the bank's trust officer should have questioned. [[Brigid|p3:first-name]] phoned us about it on [[11/6|date:month/day only]], upset; [[she and Conrad are not speaking|indirect:family estrangement]].
   If instead the bank is right (complex trust): K-1s to [[Brigid|p3:first-name]], [[Felix|p4:first-name]] and Conrad; the 65-day rule under IRC § 663(b) would be available; and the kiddie tax hits Felix. I have run both ways in the software; difference in total family tax is about [[$9,800|money]].

4. OPEN ITEMS
   - Engagement letter is signed by Conrad only. Need the bank's signature.
   - Ottilie's long-term care costs, [[$11,900|money]] a month to the facility: medical deduction on her 1040; get the physician's chronic-illness certification.
   - Conrad's contact: [[712-555-0136|phone]], [[conrad.h@loessmail.example|email]]. He asked that statements NOT go to [[Brigid|p3:first-name]]. As a beneficiary she is entitled to them; raise with counsel.
   - Form 56 for the co-trustees not yet filed.
'''))

# ---------------------------------------------------------------- 355
DOCS.append(D(355, "docx", "bilingual notice of objection cover letter", "accounting", "CA",
  title="Accountant's bilingual cover letter for a Quebec restaurateur's tax objection",
  ents={"p1": "Sylvain Archambault-Gingras", "p2": "Khadija Benslimane", "p3": "Mme Isabelle Pronovost",
        "o1": "Bistro Le Cormoran inc.", "o2": "Benslimane CPA inc.", "o3": "Coopérative d'épargne de Limoilou"},
  distractors=["Loi sur l'administration fiscale", "article 93.1.1", "Revenu Québec", "formulaire MR-93.1.1",
               "Agence du revenu du Canada", "T400A"],
  header="[[Benslimane CPA inc.|o2:full]] — dossier [[BC-2025-0418|rec:accountant file number]]",
  body=r'''
# [[Benslimane CPA inc.|o2:full]]
[[1150, 3e Avenue, bureau 210|addr:French-Canadian address with ordinal street and office number]], [[Québec|place:city]] ([[Québec|place:city]]) [[G1L 2X8|zip:Canadian postal code]] · [[418 555-0126|phone:Quebec style, space after area code]] · [[kbenslimane@benslimanecpa.example|email]]
Québec, [[le 10 novembre 2025|date:French long date]]
**PAR COURRIER RECOMMANDÉ / BY REGISTERED MAIL**
Revenu Québec — Direction des oppositions
À l'attention de [[Mme Isabelle Pronovost|p3:full:French honorific]], agente d'opposition
**Objet / Re :** Avis d'opposition — [[Bistro Le Cormoran inc.|o1:full]] — NEQ [[1177204418|taxid:Quebec enterprise number]] — no d'identification [[1224418772 TQ0001|taxid:Quebec tax identification number]] — avis de cotisation [[L-2025-0044187|rec:notice of assessment number]] du [[14 août 2025|date:French day, month and year]]
Madame,
Nous représentons [[Bistro Le Cormoran inc.|o1:full]] et son actionnaire unique, [[M. Sylvain Archambault-Gingras|p1:full:French honorific]]. Vous trouverez ci-joint le formulaire MR-93.1.1 signé. L'opposition est produite dans le délai de 90 jours prévu à l'article 93.1.1 de la Loi sur l'administration fiscale.
## Résumé (English summary follows each point for the client's file)
- **1. Montants contestés / Amounts in dispute.** La cotisation ajoute des ventes non déclarées de [[184 300 $|money:French format, space thousands and trailing dollar sign]] pour 2022 et 2023, calculées par une méthode indirecte, soit [[18 384,93 $|money:French format with decimal comma]] de TVQ, [[9 215,00 $|money:French format with decimal comma]] de TPS, des intérêts de [[4 102,77 $|money:French format with decimal comma]] et une pénalité de [[13 800 $|money:French format]]. / The auditor projected unreported sales from napkin and beer purchases.
- **2. Notre position / Our position.** La méthode ne tient pas compte de la fermeture du restaurant du [[3 janvier|date:French day and month]] au [[28 février 2023|date:French day, month and year]] après le dégât d'eau (réclamation d'assurance no [[DA-23-004418|rec:insurance claim number]]), ni des repas offerts au personnel. / The restaurant was closed for eight weeks; the auditor counted those weeks as open.
- **3. Circonstances personnelles / Personal circumstances.** [[M. Archambault-Gingras|p1:title-surname:French honorific]] [[a été hospitalisé pour une dépression majeure|health:hospitalisation, in French]] du [[11 mars|date:French day and month]] au [[2 avril 2025|date:French day, month and year]] et n'a pu répondre aux demandes de la vérificatrice. Un billet médical est joint sous pli confidentiel. / He asks that this not be shared beyond the objections officer.
- **4. Demande / Request.** Annulation de la pénalité et recalcul des ventes; suspension des mesures de recouvrement pendant l'opposition.
## Renseignements / Details for your file
| Élément | Détail |
| Actionnaire | [[Sylvain Archambault-Gingras|p1:full]], né le [[1979-04-26|dob:ISO date]], NAS [[402 655 062|taxid:SIN with spaces]] |
| Adresse du bistro | [[742, 3e Avenue|addr:French-Canadian address with ordinal street]], [[Limoilou|place:neighbourhood]], Québec [[G1L 2W5|zip:Canadian postal code]] |
| Domicile | [[1288, rue de la Canardière, app. 4|addr:French-Canadian address with apartment]], Québec [[G1J 2C1|zip:Canadian postal code]] |
| Téléphone | [[418-555-0171|phone]] (cellulaire) |
| Numéro d'entreprise fédéral | [[81442 0871 RT0001|taxid:GST/HST registration number]] — une opposition parallèle (T400A) sera transmise à l'Agence du revenu du Canada |
| Compte pour remboursement | [[Coopérative d'épargne de Limoilou|o3:full]], transit [[20418|rtn:Canadian transit number]], institution [[815|rtn:Canadian institution number]], folio [[0441877|acct:caisse folio number]] |
Our fee for the objection is [[3 500 $|money:French format]] plus taxes; [[Sylvain|p1:first-name]] has paid a deposit of [[1 000 $|money:French format]] and asked to pay the rest in three instalments, as [[the bistro is behind on its rent and two suppliers have stopped credit|attr:financial distress]].
Veuillez agréer, Madame, l'expression de nos sentiments distingués.
[[Khadija Benslimane|p2:full]], CPA — permis no [[A118204|govid:CPA permit number]]
[[KB|p2:initials]]/sr
'''))

# ---------------------------------------------------------------- 356
DOCS.append(D(356, "xlsx", "employee expense report", "accounting", "US", cardholders=["p1", "p2"],
  title="Travel expense report workbook with mileage log and card statement extract",
  ents={"p1": "Octavia Rhinehart", "p2": "Ferdinand Koopmans", "p3": "Jalen Whitlatch",
        "o1": "Lanternfish Media Group", "o2": "The Driskell Arms Hotel", "o3": "Zephyrus Regional Airways", "o4": "Barton Creek BBQ"},
  distractors=["IRS Pub. 463", "6410", "6420"],
  sheets=[
    ("Report", [
      ["EXPENSE REPORT", "[[ER-2025-1187|rec:expense report number]]", "Employee", "[[Octavia Rhinehart|p1:full]]", "Emp ID", "[[LMG-0418|rec:employee ID]]", "Approver", "[[Ferdinand Koopmans|p2:full]]"],
      ["Company", "[[Lanternfish Media Group|o1:full]]", "Trip", "Client shoot, [[Austin|place:city]] [[TX|place:state abbreviation]]", "Dates", dt("2025-10-20", "m/d/yyyy", "date:trip start"), "to", dt("2025-10-24", "m/d/yyyy", "date:trip end")],
      ["Date", "Merchant", "Category", "GL", "Amount", "Paid with", "Receipt", "Notes"],
      [dt("2025-10-20", "ddd m/d", "date:weekday and month/day in a date cell"), "[[Zephyrus Regional Airways|o3:full]]", "Airfare", "6410", amt(418.60), "Corp Amex [[...43800|card:last five with ellipsis]]", "Y", "conf [[QK7TLM|rec:airline record locator]]; frequent flyer no. [[ZR 4418 7720|rec:frequent flyer number]]"],
      [dt("2025-10-20", "ddd m/d", "date:weekday and month/day in a date cell"), "Airport rideshare", "Ground", "6420", amt(38.17), "personal Visa [[x4541|card:masked card ending]]", "Y", ""],
      [dt("2025-10-24", "ddd m/d", "date:weekday and month/day in a date cell"), "[[The Driskell Arms Hotel|o2:full]]", "Lodging", "6410", amt(1147.52), "Corp Amex ...43800", "Y", "4 nights, folio [[DA-0044187|rec:hotel folio number]], room 612"],
      [dt("2025-10-22", "ddd m/d", "date:weekday and month/day in a date cell"), "Client dinner, 5 people", "Meals", "6420", amt(486.00), "personal Visa x4541", "Y", "attendees incl. [[Jalen Whitlatch|p3:full]] (client) - over the [[$75|money]] pp guideline, [[Ferdinand|p2:first-name]] pre-approved"],
      [dt("2025-10-23", "ddd m/d", "date:weekday and month/day in a date cell"), "Pharmacy", "Other", "6420", amt(27.40), "personal Visa x4541", "N", "[[migraine medication|health:medication]] - not reimbursable, remove"],
      [dt("2025-10-24", "ddd m/d", "date:weekday and month/day in a date cell"), "Mileage (see log)", "Ground", "6420", amt(61.60), "n/a", "", "88 mi at the IRS Pub. 463 rate"],
      ["", "", "", "TOTAL", amt(2179.29), "", "", ""],
      ["", "", "", "Due to employee", amt(585.77), "", "", "ACH to acct ending [[7720|acct:last four of account]] with payroll of [[11/14|date:month/day only]]"],
    ]),
    ("Mileage", [
      ["Date", "From", "To", "Miles", "Vehicle", "Purpose"],
      [dt("2025-10-20", "m/d/yy", "date:short date in a date cell"), "Home, [[1904 Fairmount Ave|addr]], [[Philadelphia|place:city]] [[PA|place:state abbreviation]] [[19130|zip]]", "PHL airport", 11, "personal 2019 Mazda CX-5, plate [[KZT-4418|veh:license plate]]", "outbound"],
      [dt("2025-10-24", "m/d/yy", "date:short date in a date cell"), "PHL airport", "Home", 11, "same", "return"],
      [dt("2025-10-21", "m/d/yy", "date:short date in a date cell"), "Hotel", "[[Whitlatch|p3:surname]] ranch, [[Dripping Springs|place:town]]", 33, "rental, agreement [[RA-88120441|rec:rental agreement number]], plate [[TX SJR-7720|veh:license plate with state prefix]]", "location scout"],
      [dt("2025-10-23", "m/d/yy", "date:short date in a date cell"), "Dripping Springs", "Hotel", 33, "rental", "return"],
    ]),
    ("Card extract", [
      ["Card", "Cardholder", "Post date", "Merchant", "Amount", "Matched to"],
      ["[[3712 240410 43800|card:American Express number in 4-6-5 groups]]", "[[O RHINEHART|p1:caps:name as embossed on a card]]", dt("2025-10-21", "mm/dd/yyyy", "date:posting date"), "[[ZEPHYRUS REG AIR|o3:caps:truncated card-statement descriptor]]", amt(418.60, "usd", None), "ER-2025-1187"],
      ["3712 240410 43800", "O RHINEHART", dt("2025-10-25", "mm/dd/yyyy", "date:posting date"), "[[DRISKELL ARMS HTL|o2:caps:truncated card-statement descriptor]] [[AUSTIN|place!:city in caps]]", amt(1147.52, "usd", None), "ER-2025-1187"],
      ["[[3420 843133 92376|card:American Express number in 4-6-5 groups]]", "[[F KOOPMANS|p2:caps:name as embossed on a card]]", dt("2025-10-22", "mm/dd/yyyy", "date:posting date"), "[[BARTON CREEK BBQ|o4:caps:card-statement descriptor]]", amt(212.08), "unmatched - whose is this?"],
      ["Program admin note", "[[Octavia|p1:first-name]]'s corporate card expires [[12/25|exp]]; replacement mailed to her home address. Card ending [[92376|card:last five of card]] limit raised to [[$15,000|money]] on [[10/30/2025|date:numeric date]].", "", "", "", ""],
    ]),
  ]))

# ---------------------------------------------------------------- 357
DOCS.append(D(357, "txt", "inheritance tax worksheet notes", "accounting", "UK",
  title="UK accountant's worksheet notes for an inheritance tax account",
  ents={"p1": "Edith Maud Ramsbottom", "p2": "Clive Ramsbottom", "p3": "Philippa Entwhistle-Shaw", "p4": "Nigel Tranter", "p5": "Harold Ramsbottom",
        "o1": "Tranter & Holroyd Chartered Accountants", "o2": "Calderbrook Building Society", "o3": "Caja Levantina del Mediterráneo",
        "o4": "Ribble & Hodder Solicitors"},
  distractors=["IHT400", "IHT403", "IHT408", "IHT417", "residence nil rate band", "HMRC", "NS&I"],
  body=r'''
[[Tranter & Holroyd Chartered Accountants|o1:full]] - IHT WORKSHEET - file [[RAM/E/0418|rec:accountant file reference]]
Deceased: [[Edith Maud Ramsbottom|p1:full]] ("[[Edie|p1:nickname]]")        Prepared [[NT|p4:initials]], [[7 Nov 2025|date:day, abbreviated month, year]]

Date of birth [[11 October 1928|dob:day month year]].  Date of death [[28 August 2025|date:date of death]], aged [[96|age:bare age]], at home.
Last address: [[17 Whalley Old Road|addr]], [[Clitheroe|place:town]], [[Lancashire|place:county]] [[BB7 1NB|zip:UK postcode]]
NI no. [[ZH 20 44 18 C|taxid:UK National Insurance number]]     UTR [[44187 72093|taxid:UK unique taxpayer reference]]     HMRC IHT ref (applied for [[3/10/25|date:day-first short date]]): [[A418772/25K|rec:inheritance tax reference]]
Widow of [[Harold|p5:first-name]] (d. 2009) - his unused nil rate band is available in full; grant and his will located.
Executors: son [[Clive Ramsbottom|p2:full]] ([[01632 960141|phone:UK landline]]) and granddaughter [[Philippa Entwhistle-Shaw|p3:full]] ([[07700 900177|phone:UK mobile]], [[pippa.es@pendlemail.example|email]]).
Solicitors on the grant: [[Ribble & Hodder Solicitors|o4:full]], ref [[RH/PRB/2204|rec:solicitor file reference]]. We do the IHT400 and schedules only.

ASSETS AT DATE OF DEATH                                                          £
 House, [[Whalley Old Road|addr!:street name only, no number]] (two valuations, mid-point)                       [[285,000|money!:no currency sign in a pounds column]]
 [[Calderbrook Building Society|o2:full]]  sort [[60-44-18|rtn:UK sort code]]  a/c [[20441877|acct:UK account number]]  (current)        [[14,206.31|money!:no currency sign in a pounds column]]
 [[Calderbrook|o2:short]] cash ISA  a/c [[70018442|acct:UK account number]]                                      [[62,480.00|money!:no currency sign in a pounds column]]
 NS&I Premium Bonds, holder no. [[2204418A|rec:Premium Bonds holder's number]]                                     [[30,000|money!:no currency sign in a pounds column]]
 Spanish account kept from the flat she sold in 2016:
   [[Caja Levantina del Mediterráneo|o3:full]], [[Torrevieja|place:town abroad]]  IBAN [[ES32 6635 7455 4445 2071 4812|iban]]
   [[EUR 18,442.10|money:euro amount with currency code]] at death = [[£15,871|money:pounds]] at the day's rate (IHT417 not needed; put on IHT400 box for foreign assets)
 Teachers' pension arrears to date of death                                    [[1,104.66|money!:no currency sign in a pounds column]]
 Car, 2014 Honda Jazz, reg [[PK14 XTD|veh:UK registration plate]] (sold to a neighbour)                       [[3,200|money!:no currency sign in a pounds column]]
 Contents / jewellery (probate valuation)                                      [[4,750|money!:no currency sign in a pounds column]]
LIABILITIES
 Funeral ([[Clive|p2:first-name]] paid on his own card, to be reimbursed)                            [[(4,312.00)|money:negative amount in parentheses, no currency sign]]
 Care agency final invoice [[CA-118204|rec:invoice number]]                                         [[(1,846.50)|money:negative amount in parentheses, no currency sign]]

LIFETIME GIFTS IN THE 7 YEARS (IHT403) - from her cheque stubs and what the family told us
 [[14 Feb 2020|date:day, abbreviated month, year]]    [[£40,000|money:pounds]] to Clive "for the extension"            -> more than 5 yrs, taper applies if tax were due
 [[Christmas 2022|date:holiday and year]]   [[£3,000|money:pounds]] each to four great-grandchildren -> annual exemptions 2022/23 + b/f
 [[2 May 2024|date:day, abbreviated month, year]]     [[£25,000|money:pounds]] to [[Pippa|p3:nickname]] for her house deposit          -> chargeable, within nil rate band
 Monthly [[£250|money:pounds]] standing order to [[her grandson Mark, who the family say has a gambling problem|indirect:relative identified by relationship and personal difficulty]]
   since [[June 2021|date:month and year]] -> claim as normal expenditure out of income; need 3 yrs of her income figures. [[Clive|p2:first-name]] would
   rather this was left off. Told him it cannot be.

POINTS
 - Estate about [[£410,000|money:pounds]] net before gifts; with both nil rate bands and residence nil rate band (house to direct descendants) no tax expected, but the full IHT400 is needed because of the foreign asset and the gifts.
 - Capacity: GP letter of [[March 2024|date:month and year]] says [[early vascular dementia|health:diagnosis]]. The [[£25,000|money:pounds]] gift was made two months later. If [[Clive|p2:first-name]] challenges it, that is for the solicitors, not us.
 - [[Edie|p1:nickname]] was [[a lifelong Methodist|attr:religion]]; will leaves [[£5,000|money:pounds]] to the chapel (charity exemption, IHT408 not required).
 - Our fee: [[£1,950|money:pounds]] + VAT, agreed with both executors [[31/10/2025|date:day-first numeric]].
'''))

# ---------------------------------------------------------------- 358
DOCS.append(D(358, "pdf", "tax adviser client master data sheet", "accounting", "EU", minors=["p3"],
  title="German tax adviser's client master data sheet, kept in English with German terms",
  ents={"p1": "Dr. Jürgen Weißmüller", "p2": "Aylin Weißmüller-Öztürk", "p3": "Lena Weißmüller", "p4": "Sabine Hölzl",
        "o1": "Steuerkanzlei Hölzl & Partner mbB", "o2": "Isartal Sparkasse", "o3": "Weißmüller Ingenieurbüro"},
  distractors=["Anlage V", "Anlage Kind", "ELSTER", "DATEV", "§ 33b EStG", "Finanzamt München", "Kirchensteuer"],
  body=r'''
# [[Steuerkanzlei Hölzl & Partner mbB|o1:full]]
[[Rumfordstraße 21|addr:German address, street then number]], [[80469|zip:German postal code]] [[München|place:city]] · Tel. [[+49 89 5550 142|phone:German number, international format]] · [[kanzlei@hoelzlpartner.example|email]]
## Mandantenstammblatt / Client master data — Mandant Nr. [[20441|rec!:client number]]
Stand: [[06.11.2025|date:German dotted date]] · Bearbeiterin: [[Sabine Hölzl|p4:full]], Steuerberaterin
## 1. Persons
- Taxpayer: [[Dr. Jürgen Weißmüller|p1:full]], geb. [[14.03.1975|dob:German dotted date]] in [[Regensburg|place:city of birth]] · Steuer-IdNr. [[44 187 720 931|taxid:German tax identification number]] · Konfession: [[rk|attr!:religion code for church tax]] (Kirchensteuer applies)
- Spouse: [[Aylin Weißmüller-Öztürk|p2:full]], geb. [[02.09.1979|dob:German dotted date]] in [[Izmir|place:city of birth abroad]] · Steuer-IdNr. [[61 204 418 772|taxid:German tax identification number]] · Konfession: [[none (formerly Muslim, left 2011)|attr:religion]] · [[German citizen since 2008, also holds a Turkish passport|attr:citizenship]]
- Child: [[Lena Weißmüller|p3:full]], geb. [[23.07.2014|dob:German dotted date]] · Steuer-IdNr. [[77 209 441 870|taxid:German tax identification number]] · Kindergeld-Nr. [[115FK441877|rec:child benefit number]] · [[Grad der Behinderung 50, Merkzeichen G|health:disability status]] (lump sum under § 33b EStG; notice of [[12.01.2023|date:German dotted date]] on file)
- Married [[19.05.2007|date:German dotted date]], joint assessment. Tax office: Finanzamt München, Steuernummer [[143/217/40418|taxid:German tax number]].
## 2. Addresses and contact
- Home: [[Lindwurmstraße 114a|addr:German address, street then number with letter]], [[80337|zip:German postal code]] München
- [[Jürgen|p1:first-name]]: [[0171 5550 188|phone:German mobile]], [[j.weissmueller@isarpost.example|email]] · [[Aylin|p2:first-name]]: [[aylin.wo@isarpost.example|email]]
- Rental flat (Anlage V): [[Pfarrgasse 7|addr:German address, street then number]], [[93047|zip:German postal code]] Regensburg, let since [[01.10.2019|date:German dotted date]] at [[980,00 €|money:German format, decimal comma, trailing euro sign]] per month
## 3. Income
- Jürgen: freelance engineer, [[Weißmüller Ingenieurbüro|o3:full]], USt-IdNr. [[DE441877209|taxid:German VAT identification number]]. Profit 2024: [[112.480,17 €|money:German format, dot thousands and decimal comma]]. Quarterly prepayments [[6.200 €|money:German format]].
- Aylin: employed part time as a pharmacist, gross [[38.900 €|money:German format]]; wage tax class V.
- Rental surplus 2024: [[4.310,55 €|money:German format, dot thousands and decimal comma]].
## 4. Bank details (SEPA mandate signed [[03.02.2022|date:German dotted date]])
- [[Isartal Sparkasse|o2:full]] · IBAN [[DE06 2223 1911 1267 0142 51|iban]] · BIC [[ISTLDEMMXXX|acct:BIC / SWIFT code]] · account holder: both spouses
- Refunds to the same account. Our fees are collected by direct debit; last invoice no. [[2025-0933|rec!:invoice number]], [[1.428,00 €|money:German format, dot thousands and decimal comma]].
## 5. Access
- ELSTER certificate file held by the Kanzlei. Client's own ELSTER user name: [[jweissmueller75|cred:tax portal user name]]. Activation code letter received [[28.10.2025|date:German dotted date]].
- DATEV client portal invitation sent to Aylin; she asked that tax matters about [[her inheritance from her father in Izmir|indirect:expected inheritance abroad]] be discussed with her alone.
## 6. Notes
- [[Lena|p3:first-name]]'s care costs and special-school transport: collect receipts for Anlage Kind. [[Frau Weißmüller-Öztürk|p2:title-surname:German honorific]] reduced her hours in [[September 2024|date:month and year]] because of this.
- [[Herr Dr. Weißmüller|p1:title-surname:German honorific with academic title]] received a letter from the tax office about undeclared interest on a Swiss account, IBAN [[CH90 4330 6913 7671 3015 3|iban]], balance about [[CHF 61'000|money:Swiss format with apostrophe]]. He says it was his late mother's. Voluntary disclosure to be discussed in person only — nothing by email.
'''))

# ---------------------------------------------------------------- 359
DOCS.append(D(359, "txt", "bilingual eviction notice and tenant ledger", "general", "US", minors=["p2", "p3"],
  title="Property manager's bilingual pay-or-quit notice with the tenant ledger",
  ents={"p1": "Reyna Isabel Cifuentes de León", "p2": "Ximena", "p3": "Josué", "p4": "Darnell Upchurch",
        "o1": "Sweetwater Crossing Apartments", "o2": "Upchurch Residential Management, LLC"},
  distractors=["Tenn. Code Ann. § 66-28-505", "General Sessions Court"],
  body=r'''
[[Upchurch Residential Management, LLC|o2:full]] - agent for [[Sweetwater Crossing Apartments|o1:full]]
[[1500 West Andrew Johnson Hwy, Office|addr:highway address with office]], [[Morristown|place:city]], [[TN|place:state abbreviation]] [[37814|zip]]  -  [[423-555-0111|phone]]

14-DAY NOTICE TO PAY RENT OR VACATE / AVISO DE 14 DÍAS PARA PAGAR LA RENTA O DESOCUPAR
(Tenn. Code Ann. § 66-28-505)

Date / Fecha: [[November 6, 2025|date:notice date]] ([[6 de noviembre de 2025|date:Spanish long date]])
To / Para: [[REYNA ISABEL CIFUENTES DE LEÓN|p1:caps:full Spanish name with particle, in caps]] and all other occupants
Unit / Unidad: [[1500 W. Andrew Johnson Hwy, Apt. C-12|addr:highway address with apartment]]      Lease no. [[SWC-C12-2023|rec:lease number]]      Resident ID [[t0044187|rec:resident ID]]

You owe / Usted debe:  [[$1,946.00|money]]  (see ledger below / vea el estado de cuenta abajo)
You must pay this amount in full by [[November 20, 2025|date:deadline]], or move out. If you do neither, we will file in General Sessions Court.
Usted debe pagar esta cantidad completa a más tardar el [[20 de noviembre de 2025|date:Spanish long date]], o desocupar la unidad. De lo contrario presentaremos una demanda de desalojo.
Payment by money order or cashier's check only / Solo giro postal o cheque de caja. No se acepta efectivo.

[[Darnell Upchurch|p4:full]], Property Manager          Delivered by: posting on door and first-class mail

------------------------------------------------------------------------------------------
RESIDENT LEDGER - [[Cifuentes de León|p1:surname:compound surname with particle]], [[Reyna|p1:first-name]] - [[C-12|addr!:unit number only]]              Contract rent [[$1,090|money]]  Tenant portion [[$412|money]]  HAP [[$678|money]]
Date        Description                                   Charge      Payment     Balance
[[08/01/25|date:short numeric date]]    Tenant rent Aug                               [[412.00|money!:no currency sign in a ledger column]]                   [[412.00|money!:no currency sign in a ledger column]]
[[08/04/25|date:short numeric date]]    Money order [[#77204418|rec:money order number]]                                     [[412.00|money!:no currency sign in a ledger column]]        [[0.00|money!:no currency sign in a ledger column]]
[[09/01/25|date:short numeric date]]    Tenant rent Sep                               [[412.00|money!:no currency sign in a ledger column]]                   [[412.00|money!:no currency sign in a ledger column]]
[[09/06/25|date:short numeric date]]    Late fee                                       [[50.00|money!:no currency sign in a ledger column]]                   [[462.00|money!:no currency sign in a ledger column]]
[[09/19/25|date:short numeric date]]    Partial payment, cash app receipt [[R-118204|rec:payment receipt number]]                 [[200.00|money!:no currency sign in a ledger column]]      [[262.00|money!:no currency sign in a ledger column]]
[[10/01/25|date:short numeric date]]    Rent Oct - FULL contract rent (HAP abated)  [[1,090.00|money!:no currency sign in a ledger column]]                 [[1,352.00|money!:no currency sign in a ledger column]]
[[10/06/25|date:short numeric date]]    Late fee                                       [[50.00|money!:no currency sign in a ledger column]]                 [[1,402.00|money!:no currency sign in a ledger column]]
[[11/01/25|date:short numeric date]]    Tenant rent Nov (HAP reinstated [[10/28|date:month/day only]])         [[412.00|money!:no currency sign in a ledger column]]                 [[1,814.00|money!:no currency sign in a ledger column]]
[[11/06/25|date:short numeric date]]    Late fee + notice fee                         [[132.00|money!:no currency sign in a ledger column]]                 [[1,946.00|money!:no currency sign in a ledger column]]

MANAGER'S FILE NOTES (do not mail with the notice)
- Household: [[Ms. Cifuentes|p1:title-surname:first surname only]] and two children, [[Ximena|p2:first-name]], [[age 9|indirect:child's age]], and [[Josué|p3:first-name]], [[age 6|indirect:child's age]]. [[Josué|p3:first-name]] [[uses a wheelchair|health:child's mobility impairment]]; ground-floor unit was a reasonable accommodation in 2023. Legal says be careful.
- [[Housing Choice Voucher (Section 8) through the Nolichucky Housing Authority|attr:housing benefit status]], caseworker ext. 214, voucher no. [[NHA-V-0044187|rec:housing voucher number]]. October HAP was abated because the unit failed inspection (OUR water heater), so the [[$678|money]] for October is arguably not hers to pay. Check before filing: if we take that out she owes [[$1,268|money]].
- She [[lost hours at the poultry plant in September|indirect:reduced work at an identifiable employer]]. Speaks Spanish; her English is limited. Her sister translates: [[423.555.0158|phone:dotted]]. Tenant's own cell [[(423) 555-0193|phone]].
- Parking: one space, silver Honda Odyssey, tag [[4T8 K71|veh:license plate]]. A second car with [[Georgia|place:state]] plates has been in visitor parking for three weeks; lease violation letter NOT sent yet.
- She asked [[D.U.|p4:initials]] on [[11/3|date:month/day only]] whether a notice goes "on her record with immigration." Told her we do not report to anyone. [[Did not ask her status|attr:possible immigration concern]] and will not.
'''))

# ---------------------------------------------------------------- 360
DOCS.append(D(360, "eml", "forwarded stolen laptop report", "general", "US", enc="qp", cardholders=["p2"],
  title="Forwarded email chain reporting a stolen laptop bag to the insurer",
  ents={"p1": "Bernadette Oyinkansola", "p2": "Rupert Kingsolver", "p3": "Mei-Ling Szeto", "p4": "Ofc. Dewitt", "p5": "Applegarth-Kwan",
        "o1": "Kingsolver Szeto Wealth Advisors", "o2": "Hartwick Specialty Underwriters", "o3": "Trailhead Coffee Roasters"},
  distractors=["BitLocker", "Reg S-P", "Microsoft 365"],
  headers={"From": "[[Bernadette Oyinkansola|p1:full]] <[[bernadette@kingsolverszeto.example|email]]>",
           "To": "[[claims@hartwickspecialty.example|email]]",
           "Cc": "[[Mei-Ling Szeto|p3:full]] <[[meiling@kingsolverszeto.example|email]]>",
           "Subject": "Fwd: laptop bag stolen - new claim under policy [[HSU-CYB-0044187|rec:insurance policy number]]",
           "Date": "Mon, [[10 Nov 2025|date:email header date]] 08:47:15 -0700"},
  body=r'''
To the claims team at [[Hartwick Specialty Underwriters|o2:full]]:

I am the office manager at [[Kingsolver Szeto Wealth Advisors|o1:full]], [[2440 Pearl Street, Suite 200|addr:street with suite]], [[Boulder|place:city]], [[CO|place:state abbreviation]] [[80302|zip]]. I am reporting a theft under our cyber and property policy [[HSU-CYB-0044187|rec:insurance policy number]]. Our partner's own account of it is forwarded below. Here is what I can add.

WHAT WAS TAKEN ([[Saturday, November 8|date:weekday, month and day]], about 10:30 a.m., from a chair at [[Trailhead Coffee Roasters|o3:full]] on [[Pearl Street|addr!:street name only, no number]])
- Laptop: Lenovo ThinkPad X1 Carbon, serial [[PF-4KT7720|dev:laptop serial number]], our asset tag [[KSW-L-014|dev:asset tag]], Wi-Fi MAC [[3C:6A:A7:44:18:77|dev:MAC address]]. BitLocker was on.
- Phone: company iPhone 15, IMEI [[357902572952105|dev:IMEI]], number [[720-555-0148|phone]]. Remote wipe sent 11:52 a.m. Saturday; confirmed.
- A paper folder with three client account applications (names, Social Security numbers, dates of birth). This is the part that worries us most.
- His wallet, with the firm's Visa.

WHAT WE HAVE DONE
- Police report filed with Boulder PD, case no. [[25-0118204|rec:police report number]], [[Ofc. Dewitt|p4:title-surname:abbreviated rank + surname]].
- Microsoft 365 password reset for [[Rupert|p2:first-name]] at 11:40 a.m.; all sessions signed out. The sign-in log shows one attempt at 1:15 p.m. from [[198.51.100.141|ip]] that failed at the second factor. The laptop last checked in from the cafe's network, [[203.0.113.88|ip]].
- Firm card cancelled: Visa [[4825 2101 9625 7562|card]], expiry [[01/28|exp]], security code [[226|cvv]], in the name of [[RUPERT KINGSOLVER|p2:caps:name as embossed on a card]]. Two charges had already posted, [[$312.40|money]] and [[$89.99|money]].
- Custodian notified; the three client accounts are on verbal-password-only status.
- Device tracking page, in case your forensic vendor wants it: [[https://assets.kingsolverszeto.example/track/KSW-L-014|url:device tracking page]] (sign in as [[ksw-admin|cred:admin user name]]; I will give the password by phone, not here).

We believe Reg S-P requires us to notify the three clients. Please tell us whether the policy's breach coach must approve the letter first. Replacement cost of the equipment is [[$3,460|money]]. My direct line is [[303-555-0122|phone]].

[[Bernadette Oyinkansola|p1:full]]

---------- Forwarded message ----------
From: [[Rupert Kingsolver|p2:full]] <[[rupert@kingsolverszeto.example|email]]>
Date: Sat, [[Nov 8, 2025|date:forwarded message date]] at 4:26 PM
Subject: laptop bag stolen
To: Bernadette Oyinkansola, Mei-Ling Szeto

[[Bernie|p1:nickname]], [[Mei|p3:nickname]] -

Bad news. My bag was lifted at [[Trailhead|o3:short]] this morning while I was at the counter. Laptop, work phone, wallet, and the folder with the [[Applegarth-Kwan|p5:surname:client family name]] paperwork plus the two new accounts from Thursday. I had the folder with me because I was going to drop it at their house in [[Niwot|place:town]] afterwards.

I know the laptop password was not great ([[Buffs2019!|cred:laptop password]]) and yes, it is the same one I use for the custodian site. I have changed that from my home computer.

Writing from my personal phone, [[720.555.0107|phone:dotted]]. I am sorry. [[I have not been sleeping since the diagnosis|health:undisclosed health issue]] and I was not paying attention. Please keep that between us.

[[R.|p2:initials:single initial sign-off]]
'''))
