from corpus2_src.core import D, dt, amt, num

DOCS = []
BATCH_COMMON = []

# ---------------------------------------------------------------- 211
DOCS.append(D(211, "xlsx", "privilege log", "legal", "US",
  title="Defendant's privilege log with custodian and counsel sheets",
  ents={"p1": "Siobhan Halloran", "p2": "Marcus Trevino", "p3": "Anneliese Ekström", "p4": "Rajiv Chowdhury",
        "p5": "Dolores Zamora", "p6": "Kenji Yamamoto", "p7": "Bettina Wozniak", "p8": "Femi Okereke",
        "p9": "Curtis Underhill", "p10": "Odalys Mendoza",
        "o1": "Dovetail Biologics, Inc.", "o2": "Ekström Pritchard LLP", "o3": "Marlowe Forensic Data LLC",
        "o4": "Sundial Occupational Medicine", "o5": "Mendoza Rosenthal Employment Law PLLC"},
  distractors=["21 U.S.C. § 399d", "Fed. R. Civ. P. 26(b)(5)(A)", "Dell Latitude 5440", "iPhone 14", "iPhone 15 Pro",
               "Lenovo ThinkPad T14", "FDA"],
  ok=["CC", "LOG", "PRIVILEGE", "AC", "WP", "PIP", "COBRA", "SOW", "QA", "CEO", "HR", "IT", "IMEI", "Bates", "Ctrl", "Doc", "Basis", "Author",
      "Recipient", "Custodian", "Title", "Device", "Serial", "Collected", "Role", "Bar", "Firm", "Street", "City", "ST",
      "Legal", "Reply", "Memo", "Handwritten", "Texts", "Letter", "Fitness", "Draft", "Preservation",
      "Engagement", "Board", "Comparator", "Voicemail", "Spreadsheet", "Text", "Lead", "Director", "General", "Counsel",
      "Administrator", "Not", "Defendant", "Plaintiff", "Gmail", "N.C", "Email", "EEOC", "Charge"],
  sheets=[
    ("Priv Log", [
      ["PRIVILEGE LOG - [[Halloran|p1:surname]] v. [[Dovetail Biologics, Inc.|o1:full]], No. [[5:25-cv-00384-FL|rec:federal docket number]] ([[E.D.N.C.|place!:court district abbreviation]]) - served [[September 12, 2025|date:service date]] per Fed. R. Civ. P. 26(b)(5)(A)"],
      ["Ctrl No.", "Bates begin", "Bates end", "Doc date", "Doc type", "Author / From", "Recipient(s)", "CC", "Basis", "Description"],
      ["[[PRIV-0001|rec:privilege log control number]]", "[[DOVE-0004417|rec:Bates number]]", "[[DOVE-0004419|rec:Bates number]]", dt("2025-02-11"), "Email",
       "[[Marcus Trevino|p2:full]] <[[mtrevino@dovetailbio.example|email]]>", "[[Rajiv Chowdhury|p4:full]]", "[[Dolores Zamora|p5:full]]", "AC",
       "Legal advice re Halloran request for intermittent leave ([[chemotherapy schedule|health:treatment]])"],
      ["[[PRIV-0002|rec:privilege log control number]]", "[[DOVE-0004420|rec:Bates number]]", "DOVE-0004420", dt("2025-02-13"), "Email chain",
       "[[R. Chowdhury|p4:short:initial + surname]]", "[[Trevino, M.|p2:last-first]]", "", "AC",
       "Reply asking whether [[Siobhan|p1:first-name]] can be moved off the [[Raleigh|place:city]] line before the FDA inspection"],
      ["[[PRIV-0003|rec:privilege log control number]]", "[[DOVE-0004502|rec:Bates number]]", "[[DOVE-0004511|rec:Bates number]]", dt("2025-03-04"), "Memo",
       "[[Anneliese Ekström|p3:full]], [[Ekström Pritchard LLP|o2:full]]", "[[M. Trevino|p2:short:initial + surname]]", "", "AC; WP",
       "Memo analyzing retaliation exposure under 21 U.S.C. § 399d; reserve est. [[$240,000|money]] to [[$310,000|money]]"],
      ["[[PRIV-0004|rec:privilege log control number]]", "[[DOVE-0004630|rec:Bates number]]", "[[DOVE-0004633|rec:Bates number]]", dt("2025-03-19"), "Handwritten notes",
       "[[ZAMORA, DOLORES|p5:caps:ALL CAPS, Last, First order]]", "file", "", "AC",
       "Notes of call w/ counsel re [[S. Halloran|p1:short:initial + surname]] PIP and her [[ADA accommodation request|health:disability accommodation]]"],
      ["[[PRIV-0005|rec:privilege log control number]]", "[[DOVE-0004702|rec:Bates number]]", "[[DOVE-0004706|rec:Bates number]]", dt("2025-04-02"), "Text messages",
       "[[Raj|p4:nickname]]", "[[MT|p2:initials]]", "", "AC",
       "Texts from [[919-555-0176|phone]] seeking advice on timing of termination; refers to her [[union organizing at a prior employer|attr:union activity]]"],
      ["[[PRIV-0006|rec:privilege log control number]]", "[[DOVE-0004811|rec:Bates number]]", "[[DOVE-0004812|rec:Bates number]]", dt("2025-04-09"), "Letter",
       "[[Dr. Femi Okereke|p8:full:full name with title]], [[Sundial Occupational Medicine|o4:full]]", "[[D. Zamora|p5:short:initial + surname]] (HR)", "M. Trevino", "AC (attachment to request for advice)",
       "Fitness-for-duty letter: [[stage II invasive ductal carcinoma|health:diagnosis]], cleared with restrictions; forwarded to counsel same day"],
      ["[[PRIV-0007|rec:privilege log control number]]", "[[DOVE-0004903|rec:Bates number]]", "[[DOVE-0004915|rec:Bates number]]", dt("2025-04-22"), "Draft",
       "[[K. Yamamoto|p6:short:initial + surname]]", "[[A. Ekström, Esq.|p3:short:initial + surname with Esq.]]", "", "AC; WP",
       "Draft separation agreement for Halloran; severance [[$46,500.00|money]]; never sent"],
      ["[[PRIV-0008|rec:privilege log control number]]", "[[DOVE-0005020|rec:Bates number]]", "[[DOVE-0005021|rec:Bates number]]", dt("2025-05-06"), "Email",
       "[[Curtis Underhill|p9:full]]", "M. Trevino; [[Kenji Yamamoto|p6:full]]", "", "WP",
       "Preservation steps for laptop [[DBL-LT-0388|dev:asset tag]] at counsel's direction; mailbox [[shalloran@dovetailbio.example|email]] exported"],
      ["[[PRIV-0009|rec:privilege log control number]]", "[[DOVE-0005144|rec:Bates number]]", "[[DOVE-0005150|rec:Bates number]]", dt("2025-05-30"), "Email w/ attachment",
       "[[Bettina Wozniak|p7:full]]", "[[Marlowe Forensic Data LLC|o3:full]]", "K. Yamamoto", "WP",
       "Engagement of vendor, SOW [[MFD-2025-0619|rec:vendor statement of work number]], search term list; rate [[$285/hr|money:hourly rate]]"],
      ["[[PRIV-0010|rec:privilege log control number]]", "[[DOVE-0005233|rec:Bates number]]", "[[DOVE-0005235|rec:Bates number]]", dt("2025-06-17"), "Email",
       "[[Chowdhury, Rajiv|p4:last-first]]", "[[aekstrom@ekstrompritchard.example|email]]", "MT", "AC",
       "Board update draft re EEOC Charge [[433-2025-02817|rec:EEOC charge number]]; settlement authority up to [[175k|money!:shorthand k amount without currency sign]]"],
      ["[[PRIV-0011|rec:privilege log control number]]", "[[DOVE-0005301|rec:Bates number]]", "[[DOVE-0005304|rec:Bates number]]", dt("2025-07-08"), "Spreadsheet",
       "D. Zamora", "[[Ekström|p3:surname]]", "", "WP",
       "Comparator chart prepared for counsel; identifies Halloran as [[the only QA lead over 55|indirect:unique role and age group]]"],
      ["[[PRIV-0012|rec:privilege log control number]]", "[[DOVE-0005388|rec:Bates number]]", "DOVE-0005388", dt("2025-08-01"), "Voicemail transcript",
       "[[Siobhan Halloran|p1:full]]", "[[Dolores|p5:first-name]]", "", "Not privileged - withheld in error; produced [[08/22/2025|date:production date]]",
       "Voicemail from her cell [[(919) 555-0103|phone]] about COBRA and [[her husband's dialysis|health:family medical information]]"],
    ]),
    ("Custodians", [
      ["Custodian", "Title", "Email", "Device", "Serial / IMEI", "Collected", "Collected by", "Notes"],
      ["[[Halloran, Siobhan A.|p1:last-first]]", "QA Lead (former)", "shalloran@dovetailbio.example", "Dell Latitude 5440", "[[7HX2LQ3|dev:laptop service tag]]",
       dt("2025-05-08", "d-mmm-yy"), "[[C. Underhill|p9:short:initial + surname]]",
       "pw reset to [[Dove!Hold2025|cred:temporary password]] for imaging; personal Gmail [[siobhan.halloran58@mail.example|email]] not collected"],
      ["[[Trevino, Marcus|p2:last-first]]", "General Counsel", "mtrevino@dovetailbio.example", "iPhone 14", "IMEI [[35 990039 779215 9|dev:IMEI with spaces]]",
       dt("2025-05-21", "d-mmm-yy"), "[[Marlowe|o3:short]]", "cell 919-555-0176; texts only, no photos"],
      ["[[Chowdhury, R.|p4:last-first]]", "CEO", "[[raj@dovetailbio.example|email]]", "iPhone 15 Pro", "[[357558782717330|dev!:IMEI, unlabelled digits]]",
       dt("2025-05-21", "d-mmm-yy"), "Marlowe", "passcode given verbally: [[281193|cred:six-digit phone passcode]]"],
      ["[[Zamora, Dolores|p5:last-first]]", "HR Director", "[[dzamora@dovetailbio.example|email]]", "Lenovo ThinkPad T14", "[[PF-3KW81Z|dev:laptop serial number]]",
       dt("2025-05-09", "d-mmm-yy"), "C. Underhill", "works from home in [[Cary|place!:town that is also a first name]]; [[919.555.0129|phone:dotted]]"],
      ["[[Underhill, Curtis|p9:last-first]]", "IT Administrator", "[[cunderhill@dovetailbio.example|email]]", "admin workstation", "[[DBL-WS-ADM02|dev:workstation hostname]]",
       dt("2025-05-09", "d-mmm-yy"), "self", "admin login [[dbl\\cunderhill-adm|cred:domain username with backslash]]"],
    ]),
    ("Counsel", [
      ["Role", "Name", "Firm", "Bar No.", "Phone", "Email", "Street", "City", "ST", "ZIP"],
      ["Defendant - lead", "Anneliese Ekström", "Ekström Pritchard LLP", "N.C. Bar [[41877|govid:state bar number]]", "[[919-555-0150 ext. 204|phone:with extension]]",
       "aekstrom@ekstrompritchard.example", "[[4208 Six Forks Road, Suite 1100|addr:street with suite]]", "Raleigh", "[[NC|place:state abbreviation]]", "[[27609|zip]]"],
      ["Defendant - associate", "Kenji Yamamoto", "Ekström Pritchard LLP", "[[52310|govid!:state bar number, bare digits]]", "[[919-555-0150|phone]]",
       "[[kyamamoto@ekstrompritchard.example|email]]", "4208 Six Forks Road, Suite 1100", "Raleigh", "NC", "27609"],
      ["Defendant - paralegal", "[[B. Wozniak|p7:short:initial + surname]]", "Ekström Pritchard LLP", "", "", "[[bwozniak@ekstrompritchard.example|email]]", "", "", "", ""],
      ["Plaintiff", "[[Odalys Mendoza|p10:full]]", "[[Mendoza Rosenthal Employment Law PLLC|o5:full]]", "N.C. Bar [[38842|govid:state bar number]]", "[[(984) 555-0117|phone]]",
       "[[omendoza@mrlaw.example|email]]", "[[112 W. Main Street, 3rd Floor|addr:street with floor]]", "[[Durham|place:city]]", "NC", "[[27701|zip]]"],
    ]),
  ]))

# ---------------------------------------------------------------- 212
DOCS.append(D(212, "xlsx", "bank statement summary", "accounting", "US",
  title="March bank statement summary for a tile contractor",
  ents={"p1": "Lucia Ferrante", "p2": "Paolo Ferrante", "p3": "Dwayne Bellamy", "p4": "Inés Salazar",
        "p5": "Greta Lindahl", "p6": "Corinne Ashworth",
        "o1": "Ferrante Tile & Stone, Inc.", "o2": "Osprey National Bank", "o3": "Hawthorn Ledger Services",
        "o4": "Azulejos Tavares, Lda", "o5": "Kestrel Equipment Leasing", "o6": "Quarry Lane Supply Co.",
        "o7": "Thackeray Insurance Agency"},
  cardholders=["p1", "p2", "p3"],
  distractors=["Form 1120-S", "Visa", "Mastercard", "Amex"],
  ok=["Operating", "Payroll", "Money", "Business", "LOC", "DEP", "POS", "XFER", "NSF", "FEE", "PMT", "WIRE", "OUT", "GL",
      "Q1", "7", "1.0873", "50%", "Mar", "Opened", "Signers", "Shown", "Routing", "Acct", "Payee", "Network", "Holder",
      "Limit", "Exp", "Full", "Company", "Foreman", "Returned", "Transfer", "Analysis", "Client", "Prepared", "Bank",
      "Customer", "Debit", "Credit", "Line", "Tax", "TOTALS", "Card", "Type", "Account", "Date", "Ref", "Memo", "Last",
      "Notes", "4", "ABA", "BIC", "IBAN", "EIN", "SSN"],
  sheets=[
    ("Accounts", [
      ["Account", "Type", "Bank", "Routing (ABA)", "Account no.", "Shown on stmt as", "Opened", "Signers", "[[3/31/2026|date:statement date]] balance"],
      ["Operating", "Business checking", "[[Osprey National Bank|o2:full]]", "[[117300004|rtn]]", num(4400718256, "acct:account number stored as a number"),
       "[[xxxxxx8256|acct:masked account number]]", dt("2014-06-02"), "[[Lucia Ferrante|p1:full]]; [[Paolo Ferrante|p2:full]]", amt(84312.77)],
      ["Payroll", "Business checking", "Osprey National Bank", "117300004", "[[4400-719-031|acct:account number with dashes]]",
       "[[...9031|acct:last four with ellipsis]]", dt("2014-06-02"), "Lucia Ferrante", amt(12050.00)],
      ["Tax savings", "Money market", "[[Osprey|o2:short]]", "", "[[88-204417-6|acct:account number with dashes]]", "ends [[4176|acct:last four only]]",
       dt("2019-01-15"), "[[L. Ferrante|p1:short:initial + surname]]", amt(40000.00)],
      ["Line of credit", "LOC", "Osprey", "", "loan [[LOC-0093381|rec:loan number]]", "", dt("2022-09-30"),
       "Lucia Ferrante (guarantor, SSN [[xxx-xx-6716|ssn:masked SSN]])", amt(-27500.00, "acct")],
      ["Client: [[Ferrante Tile & Stone, Inc.|o1:full]], EIN [[77-0418823|taxid:EIN]], [[2291 E. Belmont Avenue|addr]], [[Fresno|place:city]], [[CA|place:state abbreviation]] [[93721|zip]]"],
      ["Bank contact: [[Inés Salazar|p4:full]], [[Shaw Avenue|place!:branch location by street]] branch, [[559-555-0111|phone]], [[isalazar@ospreynb.example|email]]"],
      ["Prepared by [[Greta Lindahl|p5:full]], [[Hawthorn Ledger Services|o3:full]], [[4/6/2026|date:preparation date]]"],
    ]),
    ("Transactions", [
      ["Date", "Acct", "Ref / check #", "Payee / description", "Debit", "Credit", "Memo"],
      [dt("2026-03-02", "m/d/yy"), "Operating", "ACH [[20260302-7718|rec:ACH trace number]]", "[[Kestrel Equipment Leasing|o5:full]] - wet saw lease", amt(1140.00, "num"), "",
       "contract [[KEL-55102|rec:lease contract number]]"],
      [dt("2026-03-03", "m/d/yy"), "Operating", "chk [[10482|rec:check number]]", "[[Quarry Lane Supply Co.|o6:full]]", amt(6212.40, "num"), "",
       "inv [[QL-88213|rec:invoice number]] - [[Ashworth|p6:surname]] kitchen job"],
      [dt("2026-03-05", "m/d/yy"), "Operating", "DEP", "Customer deposit - [[Corinne Ashworth|p6:full]]", "", amt(9500.00, "num"),
       "50% down; her chk [[#2217|rec:customer check number]]"],
      [dt("2026-03-06", "m/d/yy"), "Payroll", "[[PR-0306|rec!:payroll batch reference]]", "Payroll - 7 employees", amt(11840.16, "num"), "",
       "incl. [[D. Bellamy|p3:short:initial + surname]] [[child support w/h|attr:court-ordered support withholding]] [[$212.50|money]]"],
      [dt("2026-03-09", "m/d/yy"), "Operating", "WIRE OUT [[W260309-0041|rec:wire reference]]", "[[Azulejos Tavares, Lda|o4:full]] - [[Porto|place:city abroad]]", amt(18430.00, "num"), "",
       "[[EUR 16,950|money:currency code before amount]] at 1.0873; IBAN [[PT75 3324 3302 5058 5355 2552 1|iban:IBAN in groups of four]]; BIC [[TAVAPTPL|acct:SWIFT/BIC code]]; wire fee [[$45|money]]"],
      [dt("2026-03-11", "m/d/yy"), "Operating", "POS", "Debit card [[x4471|card:masked card, last four]] - fuel", amt(96.14, "num"), "", "[[Paolo|p2:first-name]], on the way to the [[Clovis|place!:city that is also a first name]] job"],
      [dt("2026-03-12", "m/d/yy"), "Operating", "chk [[10483|rec:check number]]", "[[Thackeray Insurance Agency|o7:full]]", amt(3318.00, "num"), "",
       "GL policy [[TIA-GL-0077154|rec:policy number]] renewal"],
      [dt("2026-03-16", "m/d/yy"), "Tax savings", "XFER", "Transfer from Operating", "", amt(5000.00, "num"), "Q1 estimate, Form 1120-S"],
      [dt("2026-03-18", "m/d/yy"), "Operating", "NSF", "Returned item - [[C. Ashworth|p6:short:initial + surname]] chk #2217", amt(9500.00, "num"), "",
       "bank fee [[$35.00|money]]; [[Lucia|p1:first-name]] called her at [[559-555-0164|phone]] - says the money is tied up in [[her mother's estate|indirect:family circumstance]]"],
      [dt("2026-03-20", "m/d/yy"), "Operating", "DEP", "Ashworth - replacement cashier's check [[0091144672|rec!:cashier's check number, bare digits]]", "", amt(9500.00, "num"), ""],
      [dt("2026-03-24", "m/d/yy"), "Operating", "chk [[10484|rec:check number]]", "[[Dwayne Bellamy|p3:full]] - tool reimbursement", amt(418.33, "num"), "", ""],
      [dt("2026-03-27", "m/d/yy"), "Line of credit", "PMT", "LOC interest", amt(171.88, "num"), "", ""],
      [dt("2026-03-31", "m/d/yy"), "Operating", "FEE", "Analysis fee", amt(22.00, "num"), "", ""],
      ["", "", "", "TOTALS", amt(51148.91, "num"), amt(24000.00, "num"), ""],
    ]),
    ("Cards", [
      ["Card", "Network", "Last 4", "Full no. (from client email)", "Exp", "Holder", "Limit", "Mar spend", "Notes"],
      ["Company debit", "Visa", "[[4471|card:last four only]]", "", "", "[[Ferrante, Paolo|p2:last-first]]", "", amt(96.14), "tied to Operating"],
      ["Company credit", "Mastercard", "[[7449|card:last four only]]", "[[5191 6675 0615 7449|card:card number with spaces]]", "[[09/28|exp]]",
       "[[LUCIA M FERRANTE|p1:caps:name as embossed on card]]", amt(25000, "usd0"), amt(7204.59), "autopay from acct ending [[8256|acct:last four only]]"],
      ["Foreman card", "Mastercard", "[[2471|card:last four only]]", "", "[[9/27|exp:expiry without leading zero]]", "Dwayne Bellamy", amt(5000, "usd0"), amt(1933.02),
       "[[Dwayne|p3:first-name]] lost the card [[3/14|date:month/day only]]; replaced, old number ended [[0338|card:last four of cancelled card]]"],
      ["Personal Amex", "Amex", "[[86131|card:last five of an Amex]]", "", "", "L. Ferrante", "", amt(642.00), "personal card used for stone samples; coded to shareholder loan"],
    ]),
  ]))

# ---------------------------------------------------------------- 213
DOCS.append(D(213, "html", "explanation of benefits", "health", "US", raw_html=True,
  title="Explanation of benefits for a dependent child's surgery",
  ents={"p1": "Gareth T. Duquette", "p2": "Elodie Duquette", "p3": "Naveen Iyer", "p4": "Marguerite Duquette",
        "o1": "Thistledown Health Plan", "o2": "Wexford Children's ENT Associates", "o3": "Saltmarsh Anesthesia Partners",
        "o4": "Pennywhistle Brewing Cooperative", "o5": "Quartzite Surgery Center of Bend"},
  minors=["p2"], cardholders=["p4"],
  distractors=["CPT 42820", "CPT 00170", "CPT 99213", "ERISA § 502(a)", "TTY 711", "THIS IS NOT A BILL", "Visa"],
  ok=["12", "ID", "Write", "Explanation", "Benefits", "Keep", "Member", "Services", "Statement", "Subscriber", "Group", "Patient", "Claim",
      "Provider", "Facility", "Billed", "Plan", "You", "Service", "Totals", "Family", "How", "Your", "Appeals", "Messages",
      "Fraud", "Receipt", "Office", "Anesthesia", "Remark", "PR-1", "CO-45", "180", "02", "Hi", "Questions"],
  body='''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Explanation of Benefits</title>
<style>
body{font-family:Arial,Helvetica,sans-serif;font-size:14px;margin:24px}
.banner{background:#234;color:#fff;padding:8px}
table{border-collapse:collapse;width:100%}
td,th{border:1px solid #bbb;padding:4px 6px}
.small{font-size:11px;color:#555}
</style>
</head>
<body>
<div class="banner"><strong>[[Thistledown Health Plan|o1:full]]</strong> &middot; Member Services [[1-800-555-0139|phone:toll-free]] (TTY 711) &middot; <span class="lnk">[[members.thistledownhp.example/eob|url:member portal address]]</span></div>
<h1>Explanation of Benefits</h1>
<p><b>THIS IS NOT A BILL.</b> Keep this statement for your records.</p>
<div class="mailto">[[GARETH T DUQUETTE|p1:caps:name in mailing block]]<br>[[618 Larkmoor Lane|addr]]<br>[[BEND|place!:city in ALL CAPS that is also a common word]] [[OR|place!:state abbreviation that is also a word]] [[97702-1184|zip:ZIP+4]]</div>
<dl>
<dt>Statement date</dt><dd>[[01/22/2026|date:statement date]]</dd>
<dt>Subscriber</dt><dd>[[Gareth T. Duquette|p1:full]]</dd>
<dt>Member ID</dt><dd>[[THP 884 201 557 01|rec:member ID with spaces]]</dd>
<dt>Group</dt><dd>[[0G7741-B|rec:group number]] ([[Pennywhistle Brewing Cooperative|o4:full]])</dd>
<dt>Patient</dt><dd>[[Elodie Duquette|p2:full]] (dependent 02, [[daughter of the subscriber|indirect:family relationship to a named person]])&nbsp;&nbsp;DOB&nbsp;[[06/19/2017|dob]]</dd>
</dl>

<h2>Claim [[2026-0114-77302-A|rec:claim number]]</h2>
<p>Provider: <a href="#prov">[[Naveen Iyer, MD|p3:full:full name with credential]]</a>, [[Wexford Children's ENT Associates|o2:full]] (NPI&nbsp;[[1730458821|govid:NPI]]) &mdash; in network.<br>
Facility: [[Quartzite Surgery Center of Bend|o5:full]]. Diagnosis on claim: [[J35.3|health:diagnosis code]], [[enlarged tonsils and adenoids with obstructive sleep apnea|health:diagnosis of a child]].</p>
<table>
<thead><tr><th>Date of service</th><th>Service</th><th>Billed</th><th>Plan discount</th><th>Plan paid</th><th>You owe</th><th>Remark</th></tr></thead>
<tbody>
<tr><td>[[12/18/2025|date:date of service]]</td><td>Office visit, pre-op (CPT 99213)</td><td>[[$212.00|money]]</td><td>[[$71.85|money]]</td><td>[[$0.00|money]]</td><td>[[$140.15|money]]</td><td>PR-1</td></tr>
<tr><td>[[01/06/2026|date:date of service]]</td><td>[[Tonsillectomy and adenoidectomy|health:procedure]], under age 12 (CPT 42820)</td><td>[[$3,870.00|money]]</td><td>[[$1,596.00|money]]</td><td>[[$1,819.20|money]]</td><td>[[$454.80|money]]</td><td>CO-45</td></tr>
<tr><td>01/06/2026</td><td>Facility fee</td><td>[[$5,140.00|money]]</td><td>[[$2,313.00|money]]</td><td>[[$2,737.80|money]]</td><td>[[$89.20|money]]</td><td>CO-45</td></tr>
<tr><td colspan="2"><b>Totals</b></td><td>[[$9,222.00|money]]</td><td>[[$3,980.85|money]]</td><td>[[$4,557.00|money]]</td><td><b>[[$684.15|money]]</b></td><td></td></tr>
</tbody>
</table>

<h2>Claim [[2026-0114-77302-B|rec:claim number]]</h2>
<p>Provider: [[Saltmarsh Anesthesia Partners|o3:full]] (out of network; processed at the in-network level because [[Dr. Iyer|p3:title-surname]] chose the facility).</p>
<table>
<tr><th>Date of service</th><th>Service</th><th>Billed</th><th>Plan paid</th><th>You owe</th></tr>
<tr><td>01/06/2026</td><td>Anesthesia, tonsil procedure, child under 12 (CPT 00170); claim attachment notes [[allergy to amoxicillin|health:allergy]]</td><td>[[$1,460.00|money]]</td><td>[[$1,168.00|money]]</td><td>[[$292.00|money]]</td></tr>
</table>

<h2>How your family deductible is tracking</h2>
<p>Family deductible [[$3,000.00|money]]; met so far this plan year [[$1,412.60|money]]. Out-of-pocket maximum [[$7,900|money]].</p>

<h2>Your payment</h2>
<p>Your $684.15 balance to [[Wexford|o2:short]] was paid on [[Jan. 20|date:abbreviated month, no year]] from the card on file, Visa ending in [[6352|card:last four only]] ([[Marguerite Duquette|p4:full]], exp. [[11/27|exp]]). Receipt no. [[RCP-5530921|rec:receipt number]] was sent to <span>[[m.duquette@mailhost.example|email]]</span>. The [[Saltmarsh|o3:short]] balance of $292.00 has not been paid.</p>

<h2>Messages</h2>
<p>Hi [[Gareth|p1:first-name]] &mdash; [[Elodie|p2:first-name]]&rsquo;s follow-up visit on [[2/3/26|date:numeric date with two-digit year]] needs referral [[REF-00918834|rec:referral number]]. Questions? Call the number above or [[(541) 555-0162|phone]] and ask for a pediatric case manager.</p>

<h2>Appeals</h2>
<p class="small">If you disagree with a decision you may appeal within 180 days of this statement. Write to [[Thistledown|o1:short]] Appeals, [[P.O. Box 4410|addr:PO Box]], [[Salem|place!:city that is also a first name]], OR [[97308|zip]]. You may have the right to bring a civil action under ERISA § 502(a). Fraud hotline [[(503) 555-0177|phone]].</p>
</body>
</html>
'''))

# ---------------------------------------------------------------- 214
DOCS.append(D(214, "docx", "severance agreement", "legal", "US", length="long",
  title="Confidential separation agreement and general release (executive)",
  header="CONFIDENTIAL SEPARATION AGREEMENT - [[T. Brzozowski|p1:short:initial + surname]] - Draft 4 (matter [[NGS 0417-0093|rec:law firm matter number]])",
  footer="Employee initials: ____   Company initials: ____",
  ents={"p1": "Thaddeus J. Brzozowski", "p2": "Imogen Rautio", "p3": "Latisha Kimathi", "p4": "Sandor Szabo",
        "p5": "Priscilla Nasser", "p6": "Carolyn Brzozowski", "p7": "Desmond Quach", "p8": "Yusuf Kaplan",
        "o1": "Hartsfield Cold Chain Logistics, Inc.", "o2": "Szabo Holloway LLC", "o3": "Nasser Giroux & Stern LLP",
        "o4": "Linden Career Transitions", "o5": "Ashgrove Federal Credit Union", "o6": "Orchard Retirement Services",
        "o7": "Verity Mutual Health", "o8": "Hartsfield Reefer Leasing LLC", "o9": "Peachleaf Bank & Trust",
        "o10": "Frostline Distribution Partners", "o11": "Glacier Gate Logistics", "o12": "Sweetbay Grocers"},
  cardholders=["p1"],
  distractors=["Form 1099-MISC", "Form W-2", "29 U.S.C. § 621 et seq.", "O.C.G.A. § 13-8-50 et seq.", "Section 409A",
               "Title VII", "Lenovo ThinkPad X1 Carbon", "iPhone 14 Pro", "2024 Ford Explorer", "Older Workers Benefit Protection Act",
               "Exhibit A", "Exhibit B", "Exhibit C"],
  ok=["Social Security", "1.1", "1.2", "1.3", "10", "11", "11.1", "11.2", "11.3", "2(c)", "3.1", "3.2", "3.3", "3.4", "4", "4.1", "4.2", "4.3", "4.4", "6", "6.1", "6.2", "6.3", "7.1", "7.2", "7.3", "7.4", "8", "8.1", "8.2", "8.3", "9", "9.1", "9.2", "9.3", "9.4", "Agreed", "Contributions", "Employee's", "Fed", "Group", "ID", "N", "Nothing", "RELEASE", "S", "SEPARATION", "Unvested", "Whether", "Agreement", "Separation", "Company", "Employee", "Vice", "Network", "Operations", "Chief", "Operating", "Officer",
      "Pay", "Severance", "Effective", "Release", "Releasees", "People", "Asset", "Coordinator", "Counties", "County",
      "IOLTA", "COBRA", "ERISA", "EEOC", "WMS", "VPN", "HQ", "PTO", "HRIS", "HR", "IT", "DL",
      "VIN", "IMEI", "CEO", "Item", "Identifier", "Grant", "Options", "Strike", "Vested", "Installment",
      "Gross", "Field", "Value", "Legal", "Home", "Emergency", "W-4", "Married", "Last", "Laptop", "Building",
      "Fuel", "Corporate", "Amex", "Restrictive", "Covenants", "Accrued", "Equity", "Benefits", "Property",
      "Miscellaneous", "Notices", "Signatures", "EMPLOYEE", "By", "Approved", "Counsel", "General", "Attn", "Ga", "Bar",
      "Friday", "Medicare", "Age", "Discrimination", "Employment", "Act",
      "Americans", "Disabilities", "Family", "Medical", "Leave", "Civil", "Rights", "Tax", "Review", "Revocation",
      "Spousal", "Acknowledgment", "Payroll", "Notes", "401(k)", "137.5", "39", "19", "18%", "21", "12",
      "3-18", "14", "12,000", "8,000", "6,000", "3,500", "1,750", "6:00", "40", "2", "2025", "1", "5", "7", "3",
      "Draft", "Not", "Mutual", "Disparagement", "Non", "Confidential", "Information",
      "Governing", "Law", "Entire", "President", "Director"],
  body='''
# CONFIDENTIAL SEPARATION AGREEMENT AND GENERAL RELEASE
This Confidential Separation Agreement and General Release (the "Agreement") is made between [[Hartsfield Cold Chain Logistics, Inc.|o1:full]], a Georgia corporation with its principal office at [[2750 Fulton Industrial Boulevard SW|addr]], [[Atlanta|place:city]], [[Georgia|place:state]] [[30336|zip]] ("[[Hartsfield|o1:short]]" or the "Company"), and [[Thaddeus J. Brzozowski|p1:full]] of [[418 Wieuca Trace NE|addr]], Atlanta, [[GA|place:state abbreviation]] [[30342|zip]] ("Employee" or "[[Mr. Brzozowski|p1:title-surname]]"), Employee No. [[HCC-004418|rec:employee ID]]. The Company and Employee are together the "Parties."
## 1. Separation
1.1 Employee's employment as Vice President, Network Operations began on [[August 14, 2006|date:hire date]] and will end on [[February 27, 2026|date:separation date]] (the "Separation Date"). Employee has been on approved medical leave since [[11/03/2025|date:leave start date]] following [[coronary artery bypass surgery|health:surgical procedure]] and the Parties agree that he will not return to active duty before the Separation Date.
1.2 The Company will describe the separation, internally and externally, as a position elimination resulting from the consolidation of its [[Savannah|place!:city that is also a first name]] and [[Macon|place:city]] hubs. [[Desmond Quach|p7:full]], Chief Operating Officer, will send the announcement in the form attached as Exhibit C and no other announcement will be made without Employee's written approval, which he will not unreasonably withhold.
1.3 Effective on the Separation Date Employee resigns as an officer of the Company and as a manager of [[Hartsfield Reefer Leasing LLC|o8:full]] (EIN [[58-2204417|taxid:EIN]]), and agrees to sign any further document reasonably needed to record those resignations.
## 2. Accrued Amounts
Whether or not Employee signs this Agreement, on the first regular payday after the Separation Date, [[March 6, 2026|date:payday]], the Company will pay: (a) base salary earned through the Separation Date at the annual rate of [[$214,000|money:annual salary]]; (b) 137.5 hours of accrued, unused PTO, being [[$14,146.63|money]]; and (c) expense report [[ER-25-1187|rec:expense report number]] in the amount of [[$1,904.18|money]], less the personal charges identified in Section 6.1.
## 3. Severance
3.1 In exchange for the release in Section 7, and provided Employee does not revoke under Section 8, the Company will pay severance equal to 39 weeks of base salary, [[$160,500.00|money]] gross (the "Severance Pay"), in 19 bi-weekly installments, less applicable withholdings, on the following schedule:
| Installment | Pay date | Gross |
| 1 | [[03/20/2026|date:pay date]] | [[$8,447.37|money]] |
| 2 | [[04/03/2026|date:pay date]] | $8,447.37 |
| 3-18 | every second Friday | $8,447.37 each |
| 19 (final) | [[11/27/2026|date:pay date]] | [[$8,447.34|money]] |
3.2 The Company will pay Employee's 2025 annual bonus at 18% of base salary, [[$38,520|money]], in a lump sum on or before [[March 13, 2026|date:bonus payment deadline]].
3.3 The Company will pay an additional lump sum of [[twenty-five thousand dollars|money:amount in words]] ([[$25,000.00|money]]) in resolution of the matters described in Section 7.2. This amount will be reported on Form 1099-MISC. All other payments will be reported on Form W-2 under the Social Security number on file ending [[-5708|ssn:last four with leading dash]].
3.4 Payments will be made by direct deposit to Employee's account at [[Ashgrove Federal Credit Union|o5:full]], routing no. [[113493384|rtn]], account ending [[40977|acct:last five digits]]. Any change must be requested in writing to [[Latisha Kimathi|p3:full]], Director of People Operations, at [[lkimathi@hartsfieldcc.example|email]].
## 4. Benefits
4.1 Group health coverage through [[Verity Mutual Health|o7:full]] (group [[VMH-G-20771|rec:group number]], subscriber ID [[W7 3391 0048|rec:subscriber ID with spaces]]) ends on [[February 28, 2026|date:coverage end date]]. If Employee timely elects COBRA continuation for himself and his spouse, [[Carolyn Brzozowski|p6:full]], the Company will pay the employer share of the premium, [[$1,318.44|money]] per month, through [[November 30, 2026|date:end of subsidy]] or, if earlier, the date Employee becomes eligible under another group plan. The Parties acknowledge that [[Mrs. Brzozowski|p6:title-surname]] is [[in active treatment for multiple sclerosis|health:spouse's diagnosis]] and that uninterrupted coverage is a material term.
4.2 Contributions to the 401(k) plan stop on the Separation Date. Employee's account with [[Orchard Retirement Services|o6:full]], participant no. [[0044-718-2260|rec:plan participant number]], is fully vested. The outstanding plan loan balance of [[$11,260.09|money]] is repayable under the plan's terms and is not forgiven by this Agreement.
4.3 The Company will pay for up to six months of outplacement services with [[Linden Career Transitions|o4:full]], not to exceed [[$7,500|money]], on invoices sent directly to the Company.
4.4 Nothing in this Agreement affects Employee's pending short-term disability claim [[STD-2025-118834|rec:disability claim number]] or the vested pension he earned in his earlier service as [[a union dock steward|attr:union role]].
## 5. Equity
| Grant | Grant date | Options | Strike | Vested at Separation Date |
| [[NQ-0611|rec:option grant number]] | [[06/01/2019|date:grant date]] | 12,000 | [[$4.10|money]] | 12,000 |
| [[NQ-0902|rec:option grant number]] | [[03/15/2022|date:grant date]] | 8,000 | [[$7.85|money]] | 6,000 |
| [[RSU-0147|rec:option grant number]] | [[01/10/2024|date:grant date]] | 3,500 | N/A | 1,750 (accelerated) |
The post-termination exercise period for vested options is extended to [[August 26, 2026|date:option exercise deadline]]. Unvested awards are forfeited on the Separation Date.
## 6. Company Property
6.1 On or before [[March 4, 2026|date:property return deadline]] Employee will return the following to [[Yusuf Kaplan|p8:full]], IT Asset Coordinator ([[404-555-0188|phone]]):
| Item | Identifier | Notes |
| Laptop, Lenovo ThinkPad X1 Carbon | S/N [[PW-08KR3T|dev:laptop serial number]]; tag [[HCC-A-20931|dev:asset tag]] | with dock and charger |
| iPhone 14 Pro | IMEI [[357828169645374|dev:IMEI]] | the number [[(404) 555-0126|phone]] may be ported to Employee |
| Building badge | [[0027714|rec!:badge number, bare digits]] | Atlanta HQ and Savannah hub |
| Fuel card | ending [[3068|card:fleet fuel card, last four]], embossed [[THADDEUS BRZOZOWSKI|p1:caps:name as embossed on card]] | cancel on receipt |
| Corporate Amex | [[XXXX-XXXXXX-83734|card:masked Amex number]] | personal charges of [[$2,318.70|money]] to be deducted under Section 2(c) |
| Company vehicle | 2024 Ford Explorer, VIN [[1FMSK8DH4RGA51207|veh:VIN]], tag [[TXR 4471|veh:license plate]] | see Section 6.2 |
6.2 Employee may purchase the vehicle for [[$31,200|money]] by notice given on or before [[March 31, 2026|date:vehicle purchase deadline]]. Otherwise he will return it to the Macon motor pool with both keys and the toll transponder, no. [[0094 5521 873|dev:toll transponder number]].
6.3 Employee's network account [[tbrzozowski|cred:network username]], his VPN profile and his WMS login [[TJB_OPS01|cred:application username]] will be disabled at 6:00 p.m. on the Separation Date. Employee confirms that he has not kept Company data on any personal device or in his personal mail account [[tadbrz61@mailbox.example|email]], and he will give the iPhone passcode ([[440816|cred:six-digit phone passcode]]) to [[Mr. Kaplan|p8:title-surname]] when the phone is returned.
## 7. Release
7.1 Employee, for himself and his heirs, releases the Company, its affiliates and their officers, directors, employees and agents (the "Releasees") from all claims of any kind arising on or before the date he signs this Agreement, including claims under Title VII of the Civil Rights Act, the Americans with Disabilities Act, the Family and Medical Leave Act, ERISA, the Age Discrimination in Employment Act (29 U.S.C. § 621 et seq.) and the common law of any state.
7.2 The release specifically includes the matters raised in the [[December 9, 2025|date:demand letter date]] letter from Employee's counsel, which alleged that he was selected for elimination because of [[his heart condition|health:condition]] and his age, and EEOC Charge No. [[410-2026-00733|rec:EEOC charge number]], which Employee will ask the agency to withdraw within 5 business days after the Effective Date. The Company denies those allegations.
7.3 Not released: Employee's workers' compensation claim [[WC-GA-2021-448120|rec:workers' compensation claim number]] (the [[2021 forklift injury to his left knee|health:injury]]), vested benefits, rights to indemnification as a former officer, and any claim that cannot lawfully be waived.
7.4 Employee represents that he is not a Medicare beneficiary and is not a debtor in any pending bankruptcy case. He has disclosed that [[a Chapter 13 plan confirmed in 2017|attr:bankruptcy history]] was completed and discharged.
## 8. Review and Revocation
8.1 Employee acknowledges, as required by the Older Workers Benefit Protection Act, that he is over 40; that he was first given this Agreement on [[February 6, 2026|date:date agreement first provided]]; that he has at least 21 days to consider it; that he has been advised in writing to consult a lawyer and has consulted [[Sandor Szabo|p4:full]] of [[Szabo Holloway LLC|o2:full]]; and that he signs voluntarily.
8.2 Employee may revoke within 7 days after signing by written notice to [[Priscilla Nasser|p5:full]], [[Nasser Giroux & Stern LLP|o3:full]], at [[pnasser@ngslaw.example|email]]. The eighth day after signing, if there is no revocation, is the "Effective Date."
8.3 Within ten days after the Effective Date the Company will pay [[$9,750.00|money]] toward Employee's legal fees by wire to the IOLTA account of Szabo Holloway LLC at [[Peachleaf Bank & Trust|o9:full]], ABA [[116816670|rtn]], account [[2200 4471 9035|acct:account number with spaces]], reference "[[Brzozowski|p1:surname]] / [[SH-26-0112|rec:firm matter number]]".
## 9. Restrictive Covenants
9.1 For 12 months after the Separation Date Employee will not provide refrigerated-warehousing or reefer-fleet management services, in a role similar to the one he held with the Company, within [[Fulton|place:county]], [[Chatham|place:county]], [[Bibb|place:county]] or [[Clayton|place!:county that is also a first name]] Counties for [[Frostline Distribution Partners|o10:full]] or [[Glacier Gate Logistics|o11:full]]. The Parties intend this covenant to comply with O.C.G.A. § 13-8-50 et seq.
9.2 For the same period Employee will not solicit any Company employee who reported to him, directly or through one other person, during his last two years of employment.
9.3 Confidential Information includes the pricing, volumes and service levels for the [[Sweetbay Grocers|o12:full]] account, which the Parties agree is worth approximately [[$18.4 million|money:amount in millions]] a year to the Company, and Employee will not use or disclose it.
9.4 Mutual Non-Disparagement. Employee will not disparage the Company. The Company will instruct [[Imogen Rautio|p2:full]], [[Mr. Quach|p7:title-surname]] and [[Ms. Kimathi|p3:title-surname]] not to disparage Employee. Reference inquiries will be directed to Ms. Kimathi at [[404.555.0102|phone:dotted]], who will confirm dates of employment and last title only.
## 10. Tax
The Parties intend all payments to be exempt from or to comply with Section 409A. The Company makes no representation about the tax treatment of any payment and Employee is responsible for his own taxes other than amounts the Company withholds.
## 11. Miscellaneous
11.1 Governing Law. This Agreement is governed by Georgia law. Any action will be brought in the state or federal courts sitting in Fulton County.
11.2 Entire Agreement. This Agreement, with Exhibit A and Exhibit C, is the entire agreement of the Parties on its subject and replaces the offer letter dated [[July 21, 2006|date:offer letter date]]. Exhibit B is an internal note and is not part of the Agreement.
11.3 Notices will be sent by email and overnight courier as follows:
| To | Address | Email |
| Company | Attn: General Counsel, 2750 Fulton Industrial Boulevard SW, Atlanta, GA 30336 | [[legal@hartsfieldcc.example|email]] |
| Employee | 418 Wieuca Trace NE, Atlanta, GA 30342; after [[June 1, 2026|date:move date]]: [[77 Marsh Wren Court|addr]], [[St. Simons Island|place:town]], GA [[31522|zip]] | tadbrz61@mailbox.example |
| Employee's counsel | Sandor Szabo, [[1180 Peachtree Street NE, Suite 2450|addr:street with suite]], Atlanta, GA [[30309|zip]]; tel. [[404-555-0159|phone]] | [[sszabo@szaboholloway.example|email]] |
## Signatures
EMPLOYEE: ______________________ Thaddeus J. Brzozowski ("[[Tad|p1:nickname]]") Date: __________
Spousal Acknowledgment (COBRA election and vehicle purchase only): ______________________ [[Carolyn M. Brzozowski|p6:full:full name with middle initial]] Date: __________
[[HARTSFIELD COLD CHAIN LOGISTICS, INC.|o1:caps]] By: ______________________ Imogen Rautio, President and CEO Date: February 6, 2026
Approved as to form: [[P. Nasser|p5:short:initial + surname]] (Ga. Bar No. [[538827|govid:state bar number]]) for the Company; [[S. Szabo|p4:short:initial + surname]] (Ga. Bar No. [[694410|govid:state bar number]]) for Employee.
---
## Exhibit A - Payroll data sheet (HR use only)
| Field | Value |
| Legal name | [[BRZOZOWSKI, THADDEUS JOSEF|p1:caps:ALL CAPS, Last, First order]] |
| DOB | [[09/22/1964|dob]] |
| SSN | [[XXX-XX-5708|ssn:masked SSN, capital X]] |
| Home phone | [[770 555 0143|phone!:spaces only]] |
| Emergency contact | [[Carolyn|p6:first-name]] (spouse), [[678-555-0170|phone]] |
| Georgia DL | [[058817342|govid!:driver's license number, bare digits]] |
| Fed/State W-4 | Married filing jointly; 2 allowances (state) |
| Last day worked | [[October 31, 2025|date:last day worked]] |
| HRIS termination code | 14 - position elimination |
## Exhibit B - Notes for HR file (not part of the Agreement)
- Tad asked on [[2/4|date:month/day only]] that the announcement not mention the surgery or [[his cardiac rehab|health:treatment]]. Agreed.
- [[Latisha|p3:first-name]] to confirm with [[Verity|o7:short]] that Carolyn's [[Ocrevus infusions|health:medication]] stay in network under COBRA.
- [[DQ|p7:initials]] approved the vehicle price by email [[1/29/26|date:numeric date with two-digit year]]. [[Yusuf|p8:first-name]] has the spare key.
- [[Nasser|p5:surname]] wants signed originals couriered to [[3344 Peachtree Road NE, Suite 1600|addr:street with suite]], Atlanta [[30326|zip]].
'''))

# ---------------------------------------------------------------- 215
DOCS.append(D(215, "txt", "credit card reconciliation memo", "accounting", "US",
  title="March purchasing-card reconciliation memo",
  ents={"p1": "Renata Vukovic", "p2": "Alasdair McKendrick", "p3": "Bo-ra Seong", "p4": "Terrence Eastman",
        "p5": "Guadalupe Valdez", "p6": "Hank Fitzgerald", "p7": "Ilse Brandtner",
        "o1": "Kingfisher Architectural Glass, LLC", "o2": "Stonebridge Commercial Card Services",
        "o3": "Vetro Tempering Supply", "o4": "Mirabelle Resort Scottsdale", "o5": "Roadrunner Crating Co.",
        "o6": "Copperfield Bank of Arizona"},
  cardholders=["p2", "p3", "p4", "p5", "p6"],
  distractors=["GL 2150", "Expensify", "NetSuite", "Amex", "P-card"],
  ok=["CC", "Fraud", "I've", "OK", "RE", "TO", "MC", "AP", "AR", "CFO", "HR", "FYI", "Controller", "Recon", "Program", "INTERNAL", "MEMO", "ACCOUNTING", "CARDS",
      "IN", "PROGRAM", "Holder", "Card", "Limit", "Receipts", "ACTION", "Me", "Three", "Charges", "Sent", "Dispute",
      "Need", "Autopay", "Disputed", "New", "March", "6", "2", "3", "1", "4", "5", "#2", "Over",
      "Terminated"],
  body=r'''[[KINGFISHER ARCHITECTURAL GLASS, LLC|o1:caps]]
INTERNAL MEMO - ACCOUNTING

TO:      [[Alasdair McKendrick|p2:full]], CFO
FROM:    [[Renata Vukovic|p1:full]], Controller
CC:      [[Bo-ra Seong|p3:full]] (AP)
DATE:    [[April 9, 2026|date:memo date]]
RE:      March P-card reconciliation - [[Stonebridge|o2:short]] program, stmt closing [[3/28|date:month/day only]]

[[Al|p2:nickname]] -

Recon for the March cycle is done except for the items below. Program acct w/ [[Stonebridge Commercial Card Services|o2:full]]
is [[5512-88-004417|acct:card program account number]]; statement total [[$48,216.09|money]], tied to GL 2150 after two reclass entries
([[JE-0326-14|rec:journal entry number]] and [[JE-0326-15|rec:journal entry number]]).

CARDS IN THE PROGRAM
  Holder               Card          Limit     March        Receipts in Expensify?
  [[A. McKendrick|p2:short:initial + surname]]        MC [[...5348|card:masked card, last four]]    [[25,000|money:no currency sign]]    [[6,114.20|money:no currency sign]]     all
  [[T. Eastman|p4:short:initial + surname]]           MC [[...6981|card:masked card, last four]]    [[10,000|money:no currency sign]]    [[11,902.77|money:no currency sign]]    missing 3
  [[Guadalupe Valdez|p5:full]]     MC [[...5194|card:masked card, last four]]    [[7,500|money:no currency sign]]     [[4,280.00|money:no currency sign]]     all
  [[H. Fitzgerald|p6:short:initial + surname]]        MC [[...7290|card:masked card, last four]]    7,500     [[2,871.46|money:no currency sign]]     none - see #2
  (ghost card - AP)    MC [[...0031|card:masked card, last four]]    [[50,000|money:no currency sign]]    [[23,047.66|money:no currency sign]]    n/a, vendor pays only

1. Over limit. [[Terrence Eastman|p4:full]] went [[$1,902.77|money]] over on the [[Scottsdale|place:city]] install. [[Mirabelle Resort Scottsdale|o4:full]]
   folio [[HM-448120|rec:hotel folio number]], 6 nights [[3/8|date:month/day only]] to [[3/14|date:month/day only]], [[$2,346.18|money]] incl. [[$312|money]] minibar/spa
   that I've coded to employee receivable. [[Terry|p4:nickname]] doesn't dispute it.

2. Terminated holder. [[Hank Fitzgerald|p6:full]] was let go [[March 6|date:month and day only]] (HR tells me it was [[a failed post-accident drug screen|health:drug test result]]
   - please keep that between us). Card ...7290 was not shut off until [[3/19|date:month/day only]].
   Charges after his last day: [[$640.12|money]] at a [[Tucson|place:city]] tire shop [[3/10|date:month/day only]]; [[$1,188.00|money]] to
   [[Roadrunner Crating Co.|o5:full]] on [[3/12|date:month/day only]] (legit - crates for job [[KAG-2611|rec:job number]]); and [[$203.34|money]] gas and food.
   Sent a demand letter [[4/2|date:month/day only]] to his last address, [[9142 N. Camino del Fierro|addr]], Tucson [[AZ|place:state abbreviation]] [[85742|zip]].
   He called back from [[520-555-0198|phone]] and says take the [[843.46|money:no currency sign]] out of his final commission check.

3. Disputed charge. [[$4,875.00|money]] from [[Vetro Tempering Supply|o3:full]] posted twice ([[03/17|date:month/day only]] and [[03/18|date:month/day only]]) on
   [[Lupe|p5:nickname]]'s card. Dispute filed, case [[SCC-DSP-7730291|rec:dispute case number]]; provisional credit expected by [[April 24|date:month and day only]].
   [[Vetro|o3:short]]'s AR contact, [[Ilse Brandtner|p7:full]], confirms the duplicate on their side (inv [[VT-20318|rec:invoice number]]).

4. Card-not-present fraud - your card. Three charges on [[3/22|date:month/day only]] from an online electronics seller totalling
   [[$1,611.93|money]]. Stonebridge closed [[5348|card:last four only]] and is reissuing. FYI when I called they read the whole old number
   back to me to confirm - [[5512 6579 8878 5348|card:card number with spaces]], exp [[04/27|exp]] - and I wrote it on the call sheet, which
   I have since shredded. New card ends [[8545|card:last four only]], exp [[04/29|exp]]. Fraud claim [[FR-26-0098812|rec:fraud claim number]].

5. Amex. The old corporate Amex ([[x-09827|card:masked Amex, last five]]) in [[Bo-ra|p3:first-name]]'s name still gets a [[$95|money]] annual fee
   every March. OK to close? Need your signature, since you are [[the only remaining officer on the account|indirect:unique role]].

ACTION
- [[Alasdair|p2:first-name]]: sign the dispute affidavit by [[Friday 4/17|date:date with weekday]].
- Me: reclass the [[Eastman|p4:surname]] receivable; payroll deduction of [[$156.00|money]] x 2 starting [[4/24|date:month/day only]].
- [[Seong|p3:surname]]: pull NetSuite vendor history on [[Roadrunner|o5:short]].

Autopay drafts on [[4/22|date:month/day only]] from the operating acct [[...2206|acct:last four with ellipsis]] at [[Copperfield Bank of Arizona|o6:full]].

- [[RV|p1:initials]]
[[rvukovic@kingfisherglass.example|email]] | direct [[480-555-0115|phone]]
'''))

# ---------------------------------------------------------------- 216
DOCS.append(D(216, "rtf", "collections letter", "legal", "US",
  title="Debt collection validation letter on a charged-off credit card",
  ents={"p1": "Deshawn R. Oduya", "p2": "Ingrid Stellan", "p3": "Marisela Papazian",
        "o1": "Haverford & Stellan, Attorneys at Law", "o2": "Corvid Receivables Fund IV, LLC",
        "o3": "Marigold Bank, N.A.", "o4": "Gantry Row Pallet Works, Inc."},
  cardholders=["p1"],
  distractors=["15 U.S.C. § 1692g", "12 CFR § 1006.34", "Regulation F", "ORC § 1319.12", "Mastercard",
               "Consumer Financial Protection Bureau"],
  ok=["Social Security", "S.D", "Toll", "Fax", "Our", "Current", "Original", "Total", "As", "Between", "How", "What", "Offer", "Mail",
      "Rewards", "Attorney", "Law", "Sup", "Ct", "Reg", "Client", "Trust", "Account", "Name", "File", "Go", "Pay", "Thu", "Fri", "ET", "8", "8-5", "Sincerely", "Detach", "To", "Your", "We", "If", "This", "24", "Se", "Hours", "Option", "A", "B"],
  body='''
# [[Haverford & Stellan, Attorneys at Law|o1:full]]
[[9300 Wickham Parkway, Suite 410|addr:street with suite]], [[Columbus|place:city]], [[Ohio|place:state]] [[43240|zip]]
Toll-free [[(866) 555-0147|phone:toll-free]] - Fax [[614-555-0190|phone:fax]] - Hours Mon-Thu 8 a.m. to 8 p.m., Fri 8-5 ET - [[www.haverfordstellan.example/pay|url]]
[[April 14, 2026|date:letter date]]
[[Deshawn R. Oduya|p1:full]]
[[1127 Sycamore Run Drive, Apt. 6C|addr:street with apartment]]
[[Dayton|place:city]], [[OH|place:state abbreviation]] [[45417|zip]]
Our file: [[HS-2026-044871|rec:collection file number]]
Current creditor: [[Corvid Receivables Fund IV, LLC|o2:full]]
Original creditor: [[Marigold Bank, N.A.|o3:full]]
Account: Marigold Rewards Mastercard [[XXXX-XXXX-XXXX-5339|card:masked card number]]
**Total due as of April 14, 2026: [[$6,418.27|money]]**
Dear [[Mr. Oduya|p1:title-surname]]:
[[Haverford & Stellan|o1:short]] is a debt collector. We are trying to collect a debt that you owe to Corvid Receivables Fund IV, LLC ("[[Corvid|o2:short]]"). We will use any information you give us to help collect the debt. At this time no attorney with this firm has personally reviewed the particular circumstances of your account.
## How much you owe
| As of [[September 30, 2024|date:charge-off date]], you owed: | [[$5,302.66|money]] |
| Between September 30, 2024 and today, you were charged this amount in interest: | + [[$1,290.61|money]] |
| Between September 30, 2024 and today, you were charged this amount in fees: | + [[$75.00|money]] |
| Between September 30, 2024 and today, you paid or were credited this amount: | - [[$250.00|money]] |
| Total amount of the debt now: | $6,418.27 |
Our records show the card was opened in [[06/2019|date:month and year, numeric]] in the name [[DESHAWN ROMELL ODUYA|p1:caps]]. The last payment before charge-off, [[$125.00|money]], was received on [[July 8, 2024|date:last payment date]]. [[Marigold|o3:short]] charged the account off and sold it to Corvid on [[11/21/2024|date:sale date]] (Corvid reference [[CRF4-00918827-M|rec:creditor reference number]]). To protect your privacy we show only part of the card number; the full sixteen digits begin [[4118 04|card!:first six digits only]].
## Your rights
You have until [[May 19, 2026|date:dispute deadline]] to dispute all or part of the debt. If you write to us by then to dispute it, we must stop collection on the amount you dispute until we send you information that shows you owe it (15 U.S.C. § 1692g; Regulation F, 12 CFR § 1006.34). You may use the form at the bottom of this letter or write to us without it. You may also write to ask for the name and address of the original creditor, if different from the current creditor. We are licensed where Ohio law requires it (ORC § 1319.12).
## What else you can do
Go to the Consumer Financial Protection Bureau's website for more information about your rights. Contact us about your payment options. Se habla español: [[(866) 555-0152|phone:toll-free]].
## Offer
If you cannot pay the total now, either of these will resolve the account. Option A: one payment of [[$3,850.00|money]] received by [[May 29, 2026|date:offer deadline]]. Option B: 24 monthly payments of [[$275.00|money]] starting [[06/05/26|date:numeric date with two-digit year]]. Pay online at [[https://pay.haverfordstellan.example/a/HS-2026-044871|url:payment link containing the file number]] with PIN [[77302|cred:online payment PIN]], or call [[866-555-0147 ext. 3306|phone:toll-free with extension]] and ask for [[Marisela Papazian|p3:full]]. To confirm your identity [[Ms. Papazian|p3:title-surname]] will ask for your date of birth (we have [[08/30/1991|dob]]) and the last four digits of your Social Security number (we have [[xxx-xx-4556|ssn:masked SSN]]).
Our file lists [[Gantry Row Pallet Works, Inc.|o4:full]] as your employer. We have not contacted your employer. Our records also show [[a Chapter 13 case dismissed in 2023|attr:bankruptcy history]] (S.D. Ohio No. [[3:22-bk-31187|rec:bankruptcy case number]]). If you are now in bankruptcy, this letter is for information only and is not a demand for payment.
Sincerely,
[[Ingrid Stellan|p2:full]], Attorney at Law (Ohio Sup. Ct. Reg. No. [[0088214|govid:attorney registration number]])
[[istellan@haverfordstellan.example|email]]
This communication is from a debt collector.
---
Detach and return. Mail to [[P.O. Box 18077|addr:PO Box]], Columbus, OH [[43218-0077|zip:ZIP+4]].
Name: [[Oduya, Deshawn R.|p1:last-first]] - File: HS-2026-044871 - [[D. Oduya|p1:short:initial + surname]] signature: __________
- I dispute this debt because I think: __________
- I enclose this amount: $________. Make checks payable to Haverford & Stellan Client Trust Account.
'''))

# ---------------------------------------------------------------- 217
DOCS.append(D(217, "txt", "adolescent telehealth intake", "health", "CA",
  title="Youth counselling telehealth intake note",
  ents={"p1": "Anjali K. Sidhu", "p2": "Harpreet Sidhu", "p3": "Gurinder Sidhu", "p4": "Louise Tremaine",
        "p5": "Noor Farahani", "p6": "Callum Sinclair", "p7": "Kiran Sidhu", "p8": "Odette Pellerin",
        "p9": "Manjit Gill",
        "o1": "Dunsmuir Heights Secondary", "o2": "Sparrowhawk Youth Wellness Clinic", "o3": "Fernbank Pharmacy"},
  minors=["p1", "p7"],
  distractors=["Infants Act s. 17", "MSP", "Kids Help Phone", "iPad", "Zoom"],
  ok=["September", "10", "4", "5-6", "Disclosed", "IP", "Letter", "OK", "Psychiatry", "Referred", "Sibling", "Wednesdays", "Weekly", "RCC", "PHN", "Gr", "Completed", "Visit", "Pronouns", "Chart", "School", "Lives", "TELEHEALTH", "INTAKE", "CLIENT",
      "FAMILY", "PRESENTING", "MEDS", "SAFETY", "TECH", "CONSENT", "PLAN", "Rx", "Session", "Portal", "Next", "Denies", "Sleep", "Mom", "Dad", "Parents", "Emergency", "Thu", "9th", "12-18", "15", "11", "72", "6", "3", "2",
      "1", "Name", "Lives", "Reviewed", "Declined", "Mature", "Aunt", "Fee", "No", "Family", "Hx"],
  body=r'''[[SPARROWHAWK YOUTH WELLNESS CLINIC|o2:caps]] - TELEHEALTH INTAKE (ages 12-18)
Completed by: [[Noor Farahani|p5:full]], RCC        Date: [[Jan 14/26|date:abbreviated month, day/two-digit year]], 4:10 pm        Visit type: video (parent joined first 15 min)

CLIENT
Name: [[Sidhu, Anjali K.|p1:last-first]] ("[[Anj|p1:nickname]]")        DOB: [[2010-11-03|dob:ISO format]] (15)        Pronouns: she/her
PHN: [[9698 658 215|govid:provincial health number with spaces]]                     Chart #: [[SYW-22-01874|rec:chart number]]
School: [[Dunsmuir Heights Secondary|o1:full]], Gr. 10 (counsellor there: [[Ms. Pellerin|p8:title-surname]], [[604-555-0121 x 4|phone:with extension]])
Lives: Mon-Thu w/ mom at [[14-6388 Hazelmere Crescent|addr:unit-first Canadian address]], [[Surrey|place:city]] [[BC|place:province abbreviation]] [[V3S 2K7|zip:Canadian postal code]];
       weekends w/ dad in [[Abbotsford|place:city]]. Parents separated since [[spring 2024|date:season and year]].

FAMILY
Mom: [[Harpreet Sidhu|p2:full]], cell [[778-555-0109|phone]], [[harpreet.sidhu@mailbox.example|email]] - joined start of session
Dad: [[Gurinder Sidhu|p3:full]], [[(604) 555-0186|phone]] - not aware of referral; [[Anjali|p1:first-name]] asks we not call him
Sibling: [[Kiran|p7:first-name]], 11, same school catchment ([[Hazelmere Elementary|place!:named school used as a location]])
Emergency contact if mom unreachable: Aunt [[Manjit Gill|p9:full!:surname that is also a common word]], [[604 555 0174|phone!:spaces only]]
Family Hx: [[mother treated for postpartum depression|health:family medical history]]; [[paternal uncle - alcohol use disorder|health:family medical history]].
[[Family attends the gurdwara weekly|attr:implies religion]]; Anj says faith is "mostly a mom thing."

PRESENTING
Referred by pediatrician [[Dr. Callum Sinclair|p6:full:full name with title]] ([[Dr. Sinclair|p6:title-surname]]'s office fax [[604-555-0140|phone:fax]]) for [[panic attacks at school|health:symptom]]
since September. [[GAD-7 score 15|health:screening score]]; [[PHQ-A score 11|health:screening score]]. Sleep 5-6 h. [[Skipped 9 school days this term|indirect:school attendance detail]].
Anj disclosed she [[identifies as bisexual|attr:sexual orientation]] and is [[not out to her father|attr:sexual orientation, disclosure status]]. Disclosed
[[superficial cutting, left forearm, last in November|health:self-harm history]]. Denies current suicidal thoughts.

MEDS
[[sertraline 50 mg daily|health:medication and dose]], started [[Dec. 2|date:abbreviated month, no year]] by Dr. Sinclair. Rx [[#7740-221867|rec:prescription number]] at [[Fernbank Pharmacy|o3:full]]
([[Fernbank|o3:short]] delivers to mom's address). [[salbutamol inhaler prn|health:medication]] for [[exercise-induced asthma|health:diagnosis]]. No known drug allergies.

SAFETY
Reviewed safety plan. Kids Help Phone number given. Mom agreed to lock up [[her zopiclone|health:parent's medication]].

TECH
Session via Zoom from client's iPad (9th gen), serial [[F9FXK2LMQ1|dev:tablet serial number]], on home wifi; clinic log shows join from
IP [[203.0.113.58|ip:IPv4]]. Portal: [[sparrowhawkyouth.example/portal|url]]  username [[anj.sidhu09|cred:portal username]]  temp password [[Maple-Otter-41|cred:temporary password]]
(expires in 72 h). Mom has a separate parent login ([[hsidhu_parent|cred:portal username]]).

CONSENT
Mature minor consent assessed and documented per Infants Act s. 17. Anj does NOT consent to parents reading session notes;
OK to share attendance and safety concerns. Declined consent to contact dad.

PLAN
1. Weekly video sessions x 6, Wednesdays 4 pm, starting [[Jan 21|date:abbreviated month, no year]]. Fee covered - sliding scale [[$20|money]]/session, not MSP.
2. Psychiatry consult request to [[Dr. Louise Tremaine|p4:full:full name with title]] ([[L. Tremaine|p4:short:initial + surname]], MSP billing no. [[62417|govid:practitioner billing number]]).
3. Letter to school counsellor [[Odette Pellerin|p8:full]] re quiet-room pass - with Anj's consent, signed [[14/01/2026|date:day-first numeric date]].
4. Next review [[2026-03-04|date:ISO format]].

[[NF|p5:initials]]
'''))

# ---------------------------------------------------------------- 218
DOCS.append(D(218, "eml", "self-assessment and payroll starter email", "accounting", "UK", enc="qp",
  title="Client email with new-starter and self-assessment details",
  ents={"p1": "Rhiannon Ashcombe", "p2": "Dev Malhotra", "p3": "Gethin Ashcombe", "p4": "Moira Tolhurst",
        "o1": "Fenwick Lowther Accountants Ltd", "o2": "Tolpuddle Print Works Ltd", "o3": "Severnside Building Society",
        "o4": "Ashcombe Ceramics", "o5": "Gower Makers' Collective"},
  distractors=["P45", "SA302s", "Plan 2", "Class 2", "Making Tax Digital", "Government Gateway", "1257L", "Etsy"],
  ok=["July", "+0000", "Everything", "I'll", "ID", "Ring", "Small", "Turnover", "User", "Hi", "Tue", "Starter", "HMRC", "NI", "UTR", "PAYE", "DOB", "IBAN", "New", "Self", "Bank", "Other", "Thanks", "Sorry", "Student",
      "Marriage", "Allowance", "VAT", "PS", "2024/25", "2023/24", "1", "2", "3", "4", "5", "Sort", "Acct"],
  headers={"From": "[[Rhiannon Ashcombe|p1:full]] <[[rhi@ashcombeceramics.example|email]]>",
           "To": "[[Dev Malhotra|p2:full]] <[[dev.malhotra@fenwicklowther.example|email]]>",
           "Cc": "[[gethin.ashcombe@mailbox.example|email]]",
           "Subject": "Starter details for [[Tolpuddle|o2:short]] + stuff for my 2024/25 return",
           "Date": "Tue, [[13 Jan 2026|date:email date]] 21:47:05 +0000"},
  body='''Hi [[Dev|p2:first-name!:first name that is also a common word]],

Sorry this is so late, I know the deadline is [[31/01/2026|date:filing deadline, day-first]]. Everything you asked for is below, I think.

1. New job
I started at [[Tolpuddle Print Works Ltd|o2:full]] on [[5 January 2026|date:start date]] (three days a week). Their payroll lady [[Moira Tolhurst|p4:full]] says she needs the starter checklist from you as you do their payroll?? Small world. [[Moira|p4:first-name]]'s number is [[01632 960471|phone:UK landline]].
- NI number: [[QQ 41 87 23 C|govid:National Insurance number]]
- DOB: [[14th of March 1988|dob:day-first with ordinal]]
- Their PAYE ref is [[120/TP45873|taxid:employer PAYE reference]]
- Salary [[£18,720|money]] a year pro rata, paid monthly, first pay [[30.01.26|date:dotted day-first, two-digit year]]
- P45 from my old job shows tax code 1257L, pay to date [[£14,203.50|money]], tax [[£1,112.20|money]], leaving date [[19/12/2025|date:leaving date, day-first]]
- Student loan: Plan 2, still about [[£21k|money:shorthand k amount]] left

2. Self-employed ([[Ashcombe Ceramics|o4:full]])
- UTR: [[61884 20755|taxid:Unique Taxpayer Reference with a space]]
- Turnover [[6 April 2024|date:tax year start, day-first]] to [[5 April 2025|date:tax year end, day-first]] was [[£23,418.76|money]], expenses [[£9,870|money]] (spreadsheet attached). About [[£4,100|money]] of the sales came through Etsy and the rest from the stall at [[Gower Makers' Collective|o5:full]] in [[Mumbles|place!:village with a common-word name]].
- I paid [[£1,264.40|money]] on account last July, reference [[6188420755K|rec!:payment reference built from the UTR]].
- Do I need to worry about VAT or Making Tax Digital yet?
- Class 2 - I can't remember if I paid.

3. Bank for the refund / wages
[[Severnside Building Society|o3:full]], account name [[R E ASHCOMBE|p1:caps:name on bank account]]
Sort [[57-87-59|rtn:UK sort code]]  Acct [[72152880|acct]]
IBAN if you need it for anything: [[GB95 HBUK 5787 5972 1528 80|iban:IBAN in groups of four]]
(The joint one ending [[4419|acct:last four only]] is for the mortgage, please don't use it.)

4. Government Gateway
User ID [[84 17 30 26 59 02|cred:Government Gateway user ID]], password is [[Kiln&Glaze!88|cred:password in an email]] - I'll change it once you've pulled the SA302s for 2023/24 and 2024/25. The access code goes to my mobile [[07700 900318|phone:UK mobile]].

5. Other
- [[Gethin|p3:first-name]] wants to know if we should claim Marriage Allowance - he earned about [[£11,900|money]] last year since [[he went part time after his back operation|health:surgery and work impact]]. His NI no. is [[QQ 60 22 91 A|govid:National Insurance number]] and he's copied in.
- We moved on [[1 Sept|date:day and abbreviated month, no year]]. New address: [[Flat 2, 17 Brynmill Terrace|addr:flat-first UK address]], [[Swansea|place:city]] [[SA2 0DP|zip:UK postcode]]. Old one was [[9 Heol Cennen|addr:Welsh street name]], [[Llanelli|place:town]], [[SA15 3QT|zip:UK postcode]] - HMRC still writes to that.
- Your invoice [[FL-10772|rec:invoice number]] for [[£385.00|money]] - paid today by bank transfer.

Thanks Dev. Ring me after 4 if anything's missing, landline [[(01632) 960 112|phone:UK landline with parentheses]].

[[Rhi|p1:nickname]]

PS [[Mr Malhotra|p2:title-surname]] is what [[Gethin Ashcombe|p3:full]] insists on calling you, sorry in advance. He says [[Fenwick Lowther|o1:short]] did his dad's probate.
--
[[Rhiannon Ashcombe|p1:full]] | Ashcombe Ceramics | [[www.ashcombeceramics.example|url]] | [[Fenwick Lowther Accountants Ltd|o1:full]] client ref [[ASH0412|rec:client reference]]
'''))

# ---------------------------------------------------------------- 219
DOCS.append(D(219, "html", "IT offboarding ticket", "general", "US",
  title="IT offboarding ticket export",
  ents={"p1": "Cassius Holloway", "p2": "Yevgenia Markova", "p3": "Obinna Nwachukwu", "p4": "Stacy-Ann Thackeray",
        "p5": "Lior Rosenthal",
        "o1": "Ravenmoor Analytics Group", "o2": "Bluff City Managed Systems", "o3": "Tessellate Data Labs"},
  distractors=["MacBook Pro 14", "YubiKey 5C NFC", "Okta", "GitLab", "Slack", "Jira", "AWS", "SOC 2 CC6.2", "macOS 15.2",
               "FileVault", "UPS"],
  ok=["COBRA", "Fi", "ID", "Logged", "N", "PSK", "S", "Shared", "Wi", "Ticket", "Priority", "Requester", "Assignee", "Opened", "Closed", "Summary", "Employee", "Asset", "Identifier", "Laptop", "Phone", "Hardware", "Monitor", "Badge", "Step", "Who", "When", "Result", "Disabled",
      "Revoked", "Rotated", "Removed", "Comments", "High", "Platform", "Engineering", "SSO", "VPN", "MAC",
      "IMEI", "IAM", "CI", "HR", "OK", "Offboarding", "Access", "Timeline", "Account",
      "Status", "Shipping", "Label", "Last", "Ethernet", "Reason",
      "Value", "2", "Notes", "Security", "Field", "Legal", "Central"],
  body='''
# Ticket [[ITSD-48213|rec:help desk ticket number]] - Offboarding: [[Cassius Holloway|p1:full]]
| Field | Value |
| Status | Closed |
| Priority | High |
| Requester | [[Stacy-Ann Thackeray|p4:full]] (HR), [[sthackeray@ravenmoor.example|email]] |
| Assignee | [[Obinna Nwachukwu|p3:full]], [[Bluff City Managed Systems|o2:full]] |
| Opened | [[2026-02-18|date:ISO format]] 09:02 Central |
| Closed | [[2026-02-27|date:ISO format]] 16:40 Central |
## Summary
Employee [[C. Holloway|p1:short:initial + surname]] (ID [[E-20417|rec:employee ID]], Platform Engineering, manager [[Yevgenia Markova|p2:full]]) resigned [[Feb 17|date:abbreviated month, no year]]. Last day [[Friday, February 20, 2026|date:date with weekday]]. Reason given to HR: he is joining [[Tessellate Data Labs|o3:full]], a direct competitor, so Legal asked for same-day access removal. HR note, not for the team channel: [[he had been on a PIP since January|attr:employment performance status]].
## Access
| Account | Identifier | Step | Who / When | Result |
| SSO (Okta) | [[cholloway|cred:username]] | Disabled | [[ON|p3:initials]], 2/20 17:05 | OK |
| VPN | cert [[rmg-vpn-cholloway-03|cred:VPN certificate name]] | Revoked | ON, 2/20 17:06 | last connected from [[198.51.100.77|ip:IPv4]] |
| GitLab ([[https://git.ravenmoor.example/cholloway|url:profile link containing username]]) | personal access token [[glpat-Xw4Tq9ZrL2mVb8Ns|cred:access token]] | Revoked | ON, 2/20 17:11 | 2 deploy keys also removed |
| AWS IAM | [[svc-etl-cassius|cred:service account name]] | Rotated | [[L. Rosenthal|p5:short:initial + surname]], [[2/23|date:month/day only]] | key was still active - see comments |
| Wi-Fi | guest PSK [[Raven-Guest-0226|cred:Wi-Fi password]] | Rotated | ON, 2/23 | |
| Shared mailbox | [[platform-alerts@ravenmoor.example|email:shared mailbox]] | Removed | ON, 2/20 | |
## Hardware
| Asset | Identifier | Notes |
| Laptop, MacBook Pro 14 | S/N [[C02ZK4QWMD6T|dev:laptop serial number]]; host [[RMG-MBP-0417|dev:hostname]] | Wi-Fi MAC [[3C:22:FB:9A:41:0E|dev:MAC address]]; Ethernet MAC [[3c-22-fb-9a-41-0f|dev:MAC address with dashes, lower case]] |
| Phone | IMEI [[356942523595919|dev:IMEI]] | company line [[(901) 555-0157|phone]], ported out at his request |
| YubiKey 5C NFC | serial [[19884207|dev!:security key serial, bare digits]] | returned |
| Badge | [[#004417|rec:badge number]] | disabled 2/20; last door event [[2/20|date:month/day only]] 16:52 |
| Monitor | tag [[RMG-MON-1188|dev:asset tag]] | stays at his home until the box arrives |
## Timeline
- [[2/18|date:month/day only]] - Shipping box and UPS label sent to his home, [[2208 Cooper Young Lane|addr]], [[Memphis|place:city]], [[TN|place:state abbreviation]] [[38104|zip]]. Label [[1Z 84W 07E 03 9921 4470|rec:shipment tracking number]].
- 2/20 - [[Cassius|p1:first-name]] signed out. Laptop on macOS 15.2 with FileVault; recovery key escrowed. Local account password he gave us to unlock it: [[tr0ub4dor&Grits|cred:password]].
- 2/23 - [[Lior Rosenthal|p5:full]] (Security) found the service key above used on [[Feb 21|date:abbreviated month, no year]] at 02:14 from [[2001:db8:41c:9::2f|ip:IPv6]] and again from [[10.40.12.186|ip:private IPv4]]. Second address is our own CI runner. First one is unexplained. Logged as [[SEC-2026-0031|rec:security incident number]] for the SOC 2 CC6.2 evidence folder.
- [[2/24|date:month/day only]] - [[Markova|p2:surname]] confirmed nothing in Slack or Jira needs to be reassigned. His personal address for the COBRA packet: [[cass.holloway@mailbox.example|email]], cell [[901.555.0122|phone:dotted]].
- [[2/27|date:month/day only]] - Laptop received and wiped by [[Obinna|p3:first-name]]. Monitor still pending.
## Comments
[[Yevgenia|p2:first-name]]: please do not delete his home directory until [[March 20|date:month and day only]], we need two notebooks out of it.
[[Stacy-Ann|p4:first-name]]: final paycheck goes out [[3/6|date:month/day only]]; [[Ravenmoor Analytics Group|o1:full]] ([[Ravenmoor|o1:short]]) will deduct [[$240.00|money]] if the monitor is not back by then.
'''))

# ---------------------------------------------------------------- 220
DOCS.append(D(220, "txt", "plea negotiation note", "legal", "US", length="short",
  title="Plea offer note to file",
  ents={"p1": "Brandon T. Zubiri", "p2": "Monique Giroux", "p3": "P. Jankowski"},
  distractors=["§28-1381(A)(1)", "F-150"],
  ok=["PLEA", "NOTE", "Cty", "Justice", "Ct", "Offer", "Fine", "DL", "Prior", "PTC", "DUI", "1", "12", "90"],
  body=r'''PLEA NOTE - [[Zubiri, Brandon T.|p1:last-first]] - [[CR-2026-001184|rec:criminal case number]] ([[Pima|place:county]] Cty Justice Ct)
[[3/9|date:month/day only]] call w/ [[ADA Giroux|p2:title-surname]]. Offer: plead to §28-1381(A)(1), dismiss extreme DUI ([[BAC .164|health:breath alcohol result]]).
Fine + assessments [[$1,582.50|money]], 1 day jail, interlock 12 mo on the F-150, plate [[AZ CKV7732|veh:license plate with state prefix]].
DL [[D08841207|govid:driver's license number]] suspended 90 days. Prior: [[2019 reckless driving|attr:prior conviction]].
Offer expires [[3/27|date:month/day only]]; PTC [[April 2|date:month and day only]] before [[Judge Jankowski|p3:title-surname]].
[[Brandon|p1:first-name]] wants it - call him [[520-555-0131|phone]].
'''))
