from corpus2_src.core import D, dt, amt, num

DOCS = []
BATCH_COMMON = ["yes", "our", "your", "enclosed", "total", "see", "per", "re", "tab", "mr", "ms", "mrs", "dr",
                "answer", "interrogatory", "objection", "response", "slide", "source", "category", "device",
                "browser", "location", "driver", "unit", "vehicle", "vehicles", "drivers", "annual", "monthly",
                "household", "property", "debts", "assets", "vendor", "period", "audit", "auditor", "sales",
                "treatment", "goals", "findings", "subjective", "objective", "recommendations", "worker",
                "employment", "education", "residences", "lender", "loan", "union", "retention", "recipients",
                "purposes", "categories", "kind", "when", "what", "who", "why", "where", "how", "still", "her",
                "she", "he", "his", "they", "them", "did", "does", "had", "got", "wants", "says", "both",
                "nothing", "everything", "copies", "copy", "original", "wire", "bank", "thanks", "thx",
                "medications", "vitals", "today's", "reason", "upcoming", "recent", "sign-in", "activity",
                "questions", "exhibit", "sworn", "verification", "definitions", "claimed", "exempt", "taxable",
                "additional", "interest", "penalty", "premium", "coverage", "liability", "collision",
                "comprehensive", "deductible", "lienholder", "garaging", "radius", "use", "class", "abstract",
                "children", "income", "expenses", "support", "matrimonial", "valuation", "separation", "marriage",
                "action", "items", "opportunities", "estimates", "safe", "harbor", "harbour", "notes", "prepared",
                "steps", "taken", "to-do", "open", "background", "timeline", "documents", "issue", "position",
                "request", "attachments", "progress", "diagnosis", "mechanism", "discharge", "functional",
                "status", "attendance", "payment", "copay", "visit", "printed", "instructions", "problem",
                "list", "provider", "pharmacy", "preferred", "allergies", "immunizations", "none", "known"]

# ---------------------------------------------------------------- 241
DOCS.append(D(241, "txt", "data subject access request response", "legal", "EU",
  title="Response to a data subject access request (Article 15)",
  ents={"p1": "Annelies Terpstra", "p2": "Joris Hendrickx", "p3": "Fenna Zuidema", "p4": "Matthias Brückner",
        "o1": "Veldhoek Fietsen & Outdoor B.V.", "o2": "Kruisberg Advocaten N.V.", "o3": "Sparda-Genossenschaftsbank Rheinland eG",
        "o4": "Postillon Pakketdienst B.V.", "o5": "Brückner Zweiradtechnik"},
  cardholders=["p1"],
  distractors=["Article 15 GDPR", "Regulation (EU) 2016/679", "Art. 12(3)", "Article 17", "Art. 6(1)(b)",
               "Autoriteit Persoonsgegevens", "Article 16", "Mastercard", "Android 15"],
  ok=["1.240", "14", "2023", "31", "E", "Fi", "ID", "MAIL", "Outside", "SMS", "Technical", "Warranty", "Wi",
      "Nederland", "Functionaris", "Gegevensbescherming", "Privacy", "KvK", "BTW", "BY", "REGISTERED", "POST", "Frau",
      "Annex", "A", "B", "C", "1", "2", "3", "4", "5", "6", "24", "BIC", "IMEI", "MAC", "Google", "German",
      "Trekking", "Identity", "Orders", "Online", "Marketing", "Kind", "Data", "Protection", "Officer", "Pixel", "8a",
      "SEPA", "2019"],
  body=r'''[[Veldhoek Fietsen & Outdoor B.V.|o1:full]]
Privacy Office / Functionaris Gegevensbescherming
[[Croeselaan 318|addr:Dutch street address]], [[3521 CG|zip:Dutch postcode]] [[Utrecht|place:city]], Nederland
KvK [[70418829|taxid:Dutch chamber of commerce number]] - BTW [[NL861204733B01|taxid:Dutch VAT number]]

BY REGISTERED POST AND E-MAIL                                   Utrecht, [[7 April 2026|date:letter date, day first]]
Our ref: [[DSAR-2026-0193|rec:request reference]]            Your ref: your e-mail of [[11 March|date:day and month only]]

Frau [[Annelies Terpstra|p1:full]]
[[Lindenthalgürtel 48|addr:German street address, number after street]]
[[50935|zip:German postal code]] [[Köln|place:city in native spelling]]
[[Deutschland|place:country in native spelling, locates the data subject abroad]]
[[a.terpstra84@postfach.example|email]]

Subject: Your request for access under Article 15 GDPR

Dear [[Ms Terpstra|p1:title-surname]],

You asked us on 11 March for a copy of the personal data we hold about you. We
confirmed your identity by telephone on [[18.03.2026|date:dotted day-first date]] (call taken by [[Fenna Zuidema|p3:full]] of
customer service, who rang you back on [[+49 221 5550 187|phone:German number with country code]]). This letter is our
response under Regulation (EU) 2016/679. It is sent within the one-month period of
Art. 12(3); we did not need the extension.

1. Who we are. [[Veldhoek|o1:short]] is the controller. Our Data Protection Officer is
[[Joris Hendrickx|p2:full]] ([[fg@veldhoek-fietsen.example|email:shared mailbox]], [[030 555 0142|phone:Dutch national format]]). Outside counsel,
[[Kruisberg Advocaten N.V.|o2:full]], reviewed the annexes; [[mr. Hendrickx|p2:title-surname:Dutch lawyer's title + surname]] signs for us.

2. What we hold (full export in Annex A, 24 pages).

   Identity and contact   customer no. [[K-4471902|rec:customer number]]; name; date of birth [[23-09-1984|dob:day-first with dashes]];
                          the Köln address above and your previous address,
                          [[Oudegracht 211 bis|addr:Dutch address with house-number suffix]], [[3511 NH|zip:Dutch postcode]] Utrecht (until [[August 2023|date:month and year]]);
                          mobile [[0049 171 5550 163|phone:German mobile with 00 prefix]]; German tax ID you gave us for the
                          lease-bike invoice, [[48 205 916 374|taxid:German tax identification number with spaces]].
   Online account         username [[annelies_t84|cred:username]], created [[2 June 2019|date]]. We store only a
                          salted hash of your password, not the password itself.
   Orders                 14 orders between 2019 and [[26 February 2026|date]], most recently order
                          [[VF-2026-118834|rec:order number]] (Trekking E-bike, [[€ 3.249,00|money:euro amount in continental format]]) and the return of
                          [[RMA-55120|rec:return number]], refunded [[EUR 189,95|money:euro amount with currency code]] on [[03.03.2026|date:dotted day-first date]].
   Payment                SEPA mandate [[VFM-000482771|rec:mandate reference]] on IBAN [[DE71 0539 3195 1175 4199 10|iban:IBAN in groups of four]]
                          (BIC [[GENODED1SPR|acct:BIC code]], [[Sparda-Genossenschaftsbank Rheinland eG|o3:full]]); a Mastercard stored as
                          [[5553 18** **** 0072|card:masked card number]], expiry [[11/27|exp]]. We never hold the security code.
   Customer-service notes 6 entries. One, dated [[9 January 2026|date]], records that you returned the
                          saddle because of [[a knee replacement last autumn|health:surgical history mentioned in a service note]]. See point 5.
   Marketing              newsletter consent given 2 June 2019, withdrawn [[14-01-2026|date:day-first with dashes]]; loyalty
                          card [[6340 0091 7725 4418|rec:loyalty card number that looks like a payment card]] with 1.240 points.

3. Technical data (Annex B). Our web shop and app logged:
   - sign-ins from [[203.0.113.47|ip:IPv4]] (Köln, 31 times), [[198.51.100.212|ip:IPv4]] (Utrecht, until 2023)
     and once from [[2001:db8:4c1a:9e::2f|ip:IPv6]] on [[22 December 2025|date]];
   - app installation ID [[7f3c1a9e-52b0-4d1e-9a6f-0c2e81d4b7a3|dev:app installation identifier (UUID)]] on a Google Pixel 8a
     (Android 15), advertising ID [[c41d77e0-9b2a-4f6e-8d35-1a60b2f9e4c8|dev:mobile advertising identifier]], and an older
     phone with IMEI [[35 738055 554584 2|dev:IMEI with spaces]] that we recorded for the theft-insurance add-on;
   - the frame number of your bike, [[WVF24T0381176|dev:bicycle frame serial number]], and the serial of its
     battery, [[BT-E8036-22K4417|dev:battery serial number]];
   - Wi-Fi MAC [[9c:2e:a1:4f:07:d3|dev:MAC address]] seen by the in-store network in our Utrecht shop.

4. Recipients. Delivery data went to [[Postillon Pakketdienst B.V.|o4:full]] (tracking
[[3SPOST881204417|rec:parcel tracking code]]). Warranty work was passed to our German service partner
[[Brückner Zweiradtechnik|o5:full]], [[Aachener Straße 1120|addr:German street address]], Köln ([[Matthias Brückner|p4:full]],
[[m.brueckner@brueckner-zweirad.example|email]]). [[Herr Brückner|p4:title-surname:German title + surname]] holds only your name, phone and frame number.

5. The health remark. The service note about your knee should not have been
written down. It was not needed for the return (Art. 6(1)(b)) and we had no
basis to keep health data. We erased the sentence on [[1 April 2026|date]]; the
unredacted note is shown to you once, in Annex C, so you can see what was held.
No other record mentions your health, and the profile label "[[lives alone, 40-45, no car|indirect:marketing profile label]]"
has been deleted from our marketing system as well.

6. Your rights. You may ask for rectification (Article 16) or erasure (Article 17),
and you may complain to the Autoriteit Persoonsgegevens or to the authority in
[[Nordrhein-Westfalen|place:German state in native spelling]].

A secure copy of the annexes is at
[[https://privacy.veldhoek-fietsen.example/dsar/DSAR-2026-0193|url:portal link containing the request reference]] ; the one-time
access code [[VH-7Q2M-K9XD|cred:one-time access code]] was sent by SMS to the number ending [[0163|phone!:last four digits only]].

Kind regards,

[[J. Hendrickx|p2:short:initial + surname]]
Data Protection Officer
'''))

# ---------------------------------------------------------------- 242
DOCS.append(D(242, "pdf", "family law financial statement notes", "legal", "CA",
  title="Notes for Form 13.1 financial statement (property and support claims)",
  ents={"p1": "Mireille Desrochers", "p2": "Thanh Kelvin Banh", "p3": "Élodie Banh", "p4": "Marc-Antoine Banh",
        "p5": "Sunita Ramcharan", "p6": "Gordon Wojcik", "p7": "Huguette Desrochers", "p8": "Tavish Imrie",
        "o1": "Ramcharan Petit Family Law Professional Corporation", "o2": "Wojcik & Oyelade LLP",
        "o3": "Kawartha Shores Credit Union", "o4": "Dominion Lakehead Bank", "o5": "Byward Smiles Dental Hygiene",
        "o6": "Kanata Photonics Inc.", "o7": "École élémentaire Sainte-Geneviève", "o8": "Imrie Appraisals Ltd."},
  minors=["p3", "p4"], cardholders=["p1", "p2"],
  distractors=["Form 13.1", "s. 7", "line 15000", "HOOPP", "Visa", "Mastercard", "Honda CR-V", "Mazda3", "RRSP", "TFSA", "RESP", "Notice of Assessment"],
  ok=["14", "28/72", "5-10", "6", "Appraised", "Competitive", "Gift", "January", "Joint", "Married", "Meeting",
      "Mortgage", "Notices", "Opposing", "RSUs", "SIN", "Spousal", "TO", "V", "T4", "2025", "2024", "2021", "2016",
      "2", "3", "4", "10", "CRA", "IEP", "Grade", "OT", "Superior", "Justice", "Family", "Branch", "FRO", "Part",
      "HELOC", "VIN"],
  body=r'''# [[Ramcharan Petit Family Law Professional Corporation|o1:full]]
NOTES TO FILE - financial disclosure, Form 13.1 - PRIVILEGED
File: [[Desrochers|p1:surname]] / [[Banh|p2:surname]] - our no. [[26-0417-SR|rec:firm file number]] - Court file [[FC-26-1184|rec:court file number]] (Superior Court of Justice, Family Branch, [[Ottawa|place:city]])
Meeting [[Thurs. 21 May 2026|date:date with abbreviated weekday]], [[Mireille Desrochers|p1:full]] with [[Sunita Ramcharan|p5:full]] ([[SR|p5:initials]]). Opposing counsel: [[Gordon Wojcik|p6:full]], [[Wojcik & Oyelade LLP|o2:full]], [[613-555-0171|phone]], [[gwojcik@wojcikoyelade.example|email]].
## Parties and children
[[Mireille|p1:first-name]], born [[4 Feb 1986|dob:abbreviated month, day first]], SIN [[359-185-956|taxid:SIN with dashes]]. Husband [[Thanh Kelvin Banh|p2:full]], goes by [[Kelvin|p2:nickname:middle name used as everyday name]], born [[1983-11-30|dob:ISO format]], SIN [[527 469 837|taxid:SIN with spaces]] (from the 2024 joint mortgage renewal, he has not produced it). Married [[16 Aug 2012|date:date of marriage]] in [[Gatineau|place:city]]; separated [[Jan 3/26|date:shorthand date]] (he says [[Feb. 14|date:abbreviated date without year]], when he moved to his brother's in [[Orléans|place!:neighbourhood that is also a foreign city name]]). V-day will be argued.
- [[Élodie Banh|p3:full]], born [[09/06/2014|dob:numeric day-first]], Grade 6 at [[École élémentaire Sainte-Geneviève|o7:full]]. Competitive swimming, [[$3,180|money]] a year.
- [[Marc-Antoine Banh|p4:full]] ("[[Marco|p4:nickname]]"), born [[22 March 2017|dob]]. [[ADHD, combined type, on Biphentin 20 mg|health:diagnosis and medication of a child]]; IEP at the same school; OT at [[$140|money:per-session fee]] a session, not covered. [[Élodie|p3:first-name]] and Marco are with Mireille 10 nights of 14 since January.
## Income (Part 2)
Mireille: dental hygienist, [[Byward Smiles Dental Hygiene|o5:full]], 4 days a week. 2025 T4 box 14 [[$71,460.12|money]]; CRA Notice of Assessment line 15000 [[$73,902|money]]. Kelvin: optical engineer, [[Kanata Photonics Inc.|o6:full]], employee no. [[KP-20418|rec:employee number]], base [[$148,500|money:salary]] plus bonus (2025: [[38,250|money:amount without currency sign]]). He also has RSUs he calls "worthless"; SR to demand the grant statements.
## Assets and debts on V-day (Part 4)
- Matrimonial home, [[62 Wigan Drive|addr]], [[Nepean|place:community]], [[ON|place!:province abbreviation that is also a common word]] [[K2J 3T8|zip:Canadian postal code]]. Joint. Appraised [[$912,000|money]] by [[Tavish Imrie|p8:full]] of [[Imrie Appraisals Ltd.|o8:full]], report [[IA-26-0338|rec:appraisal report number]]. Mortgage with [[Dominion Lakehead Bank|o4:full]], no. [[4410-778-203961|rec:mortgage number]], balance [[$388,214.67|money]]; HELOC [[$41,900|money]].
- Joint chequing, [[Kawartha Shores Credit Union|o3:full]], transit [[04512|rtn:Canadian transit number]], institution [[842|rtn:Canadian institution number]], account [[6017733|acct]]: [[$6,244.10|money]].
- Her savings at [[Kawartha Shores|o3:short]], acct ending [[-2290|acct:last four with leading dash]]: [[$18,700|money]]. Gift from her mother [[Huguette Desrochers|p7:full]] ([[$15,000|money]], [[Dec. 2024|date:abbreviated month and year]]) - excluded property if we can trace it. [[Huguette|p7:first-name]] will swear an affidavit.
- His RRSP at [[Dominion Lakehead|o4:short]], plan [[RSP 77-1204-5|acct:registered plan number]]: [[$203,118|money]]. Her RRSP [[$54,300|money]]; TFSA [[$11,025.40|money]]. RESP for both kids, [[$46,880|money]], joint subscribers.
- 2021 Honda CR-V, plate [[CKRT 482|veh:Ontario licence plate]], VIN [[2HKRW2H84MH614273|veh:VIN]], hers, worth about [[$27,500|money]]. 2016 Mazda3, plate [[BXMJ917|veh!:Ontario licence plate written without a space]], his, [[$9,000|money]].
- Debts: joint Visa ending [[7042|card:last four only]] ([[$4,812.33|money]], both are cardholders); Kelvin's Mastercard [[5532 6879 7315 9320|card:card number with spaces]] - Mireille found the statement, [[$22,406.90|money]], mostly [[online sports betting|attr:gambling debts]], he denies it. Loan from his brother, "[[twenty thousand|money:amount in words without currency]]", undocumented.
## Support
Table child support on his 2025 income approx. [[$2,610/mo|money:monthly amount]]; s. 7 expenses shared 28/72. He has paid [[$1,500|money]] by e-transfer twice ([[Feb 27|date:abbreviated date without year]] and [[April 1|date:month and day only]]) to [[mireille.desrochers@courriel.example|email]]. Spousal: mid-range about [[$1,150|money]] monthly, 5-10 yrs. If he stops paying we register with FRO.
## To do
- SR: serve Form 13.1 and Request for Information by [[June 12, 2026|date:service deadline]]; case conference [[2026-07-08|date:ISO format]].
- Mireille: 3 years of Notices of Assessment, [[Kawartha|o3:short!:one-word short form that is also a region]] statements, pension statement (HOOPP member no. [[0048-221-907|rec:pension member number]]). She can be reached on [[(613) 555-0138|phone]] after 4, not at work.
- Do not email her at the shared family address; Kelvin still has the tablet.
'''))

# ---------------------------------------------------------------- 243
DOCS.append(D(243, "pptx", "year-end tax planning deck", "accounting", "US",
  title="2026 year-end tax planning meeting deck",
  ents={"p1": "Bartosz Skoczylas", "p2": "Noelani Kealoha-Skoczylas", "p3": "Kai Skoczylas", "p4": "Maile Skoczylas",
        "p5": "Dolores Marchand", "p6": "Ifeoma Nwachukwu", "p7": "Stanisława Skoczylas",
        "o1": "Skoczylas Orthodontics, PLLC", "o2": "NKS Rentals LLC", "o3": "Tidewell & Marchand CPAs",
        "o4": "Harrowgate Securities", "o5": "Boise Bench Community Bank", "o6": "Idaho Foodbank Alliance of Ada County"},
  minors=["p3", "p4"], cardholders=["p2"],
  distractors=["Form 1040-ES", "Form 2210", "Section 199A", "Schedule E", "IRS Direct Pay", "Form 8283", "IDeal 529",
               "EFTPS", "Roth IRA", "Form 709", "American Express"],
  ok=["100%", "110%", "150", "2019", "529", "Appreciated", "Born", "Cash", "Grandmother", "Meeting", "November",
      "POA", "Q1-Q3", "Recommend", "Recommended", "Roof", "S", "2026", "2025", "Q4", "Q3", "401(k)", "QBI", "PLLC",
      "AGI", "DAF", "K-1", "W-2", "3", "5", "Agenda", "Where", "Estimated", "Entities", "Kids", "Charitable",
      "Speaker", "Reasonable", "Projected", "Family", "Planning", "Balance"],
  body=r'''# 2026 Year-end Planning - [[Skoczylas|p1:surname]] Family
[[Tidewell & Marchand CPAs|o3:full]] - prepared for [[Bartosz Skoczylas|p1:full]] and [[Noelani Kealoha-Skoczylas|p2:full]]
Meeting [[Tuesday, November 17, 2026|date:date with weekday]] - [[Boise|place:city]] office
Client no. [[SKO-0412|rec:client number]] - confidential
> Speaker notes: [[Dolores|p5:first-name]] presents; [[Ifeoma Nwachukwu|p6:full]] takes notes. [[Bart|p1:nickname]] joins by phone from the clinic, [[208-555-0166|phone]]. Do not show slide 5 if his mother is in the room.
# Agenda
- Where 2026 stands vs. 2025
- Estimated tax: Q4 payment and safe harbor
- Entities: [[Skoczylas Orthodontics, PLLC|o1:full]] and [[NKS Rentals LLC|o2:full]]
- Kids: 529 plans and [[Kai|p3:first-name]]'s summer wages
- Charitable and family gifts
# Where 2026 stands
| Item | 2025 | 2026 projected |
| Bart W-2 from the PLLC | [[$240,000|money]] | [[$255,000|money]] |
| K-1 income, PLLC (EIN [[82-3391740|taxid:EIN]]) | [[$412,880|money]] | [[$467,000|money]] |
| [[Noelani|p2:first-name]] W-2 (school district) | [[$68,214|money]] | [[$70,950|money]] |
| [[NKS Rentals|o2:short]], Schedule E (EIN [[93-1847265|taxid:EIN]]) | [[(11,406)|money:parenthesized negative, no currency sign]] | [[$6,300|money]] |
| Projected AGI | [[$734k|money:abbreviated with k]] | [[$821k|money:abbreviated with k]] |
> Speaker notes: the rental turned positive because the [[Garden City|place!:city name made of common words]] duplex at [[4108 W. Adams St.|addr:abbreviated street address]] was fully let from [[March 1|date:month and day only]]. Roof replacement [[$38,400|money]] is capitalized, not expensed.
# Estimated tax
- Paid so far on Form 1040-ES: [[$52,000|money]] x 3 = [[$156,000|money]]
- 110% safe harbor needs [[$214,720|money]] in total, so Q4 is at least [[$58,720|money]] by [[January 15, 2027|date:payment deadline]]
- Recommended: pay [[$75,000|money]] to avoid a spring balance; Form 2210 penalty otherwise about [[$1,900|money]]
- [[Idaho|place:state]]: [[$9,500|money]] per quarter; Q3 was paid late ([[10/02/26|date:two-digit year]])
> Speaker notes: Q1-Q3 went on Noelani's American Express ending [[98823|card:last five of an Amex]] through the card processor (fee [[$962|money]] each time - she wants the points). Recommend IRS Direct Pay or EFTPS from the joint account at [[Boise Bench Community Bank|o5:full]] instead: routing [[123394127|rtn]], account [[0071 4482 09|acct:account number with spaces]]. PLLC payroll deposits already use EFTPS, PIN [[4471|cred:four-digit EFTPS PIN]] - [[Ifeoma|p6:first-name]] holds it, do not put it in the minutes.
# Entities
- PLLC: S-corp since 2019. Reasonable compensation review - Bart's W-2 raised to $255,000
- Section 199A: no QBI deduction above the threshold (specified service trade)
- 401(k) profit sharing: fund [[$46,000|money]] employer contribution by the return due date
- NKS Rentals: Noelani 100% member; second property under contract in [[Meridian|place!:city that is also a common word]], closing [[12/18/2026|date:expected closing]], price [[$489,900|money]]
# Kids
| Child | Born | 529 account | Balance |
| [[Kai Skoczylas|p3:full]] | [[05/19/2012|dob]] | [[ID-529-60441872|acct:529 plan account number]] | [[$61,240|money]] |
| [[Maile Skoczylas|p4:full]] | [[2015-08-02|dob:ISO format]] | [[ID-529-60441880|acct:529 plan account number]] | [[$44,915|money]] |
- IDeal 529 contributions: [[$12,000|money]] joint Idaho deduction, same as 2025
- Kai earned [[$2,140|money]] lifeguarding - Roth IRA at [[Harrowgate Securities|o4:full]], acct [[HG-7714-0926|acct:brokerage account number]], funded [[$2,000|money]]
- Grandmother [[Stanisława Skoczylas|p7:full]] wants to give each child [[$19,000|money]] - no Form 709 needed at that amount
> Speaker notes: [[Maile|p4:first-name]] has [[type 1 diabetes|health:diagnosis of a child]]; pump and supplies ran [[$7,800|money]] out of pocket, so check the medical floor. [[Mrs. Skoczylas|p7:title-surname]] is [[in memory care|health:care status of a relative]] and Bart holds her power of attorney - gifts must come from her own account and be within the POA.
# Charitable
- Appreciated stock to the DAF: 150 shares, basis [[$4,100|money]], value about [[$31,500|money]]
- Cash to [[Idaho Foodbank Alliance of Ada County|o6:full]]: [[$5,000|money]] pledged, receipt [[IFA-2026-00871|rec:donation receipt number]] for the first [[$2,500|money]]
- Form 8283 only if non-cash gifts other than securities exceed the limit
# Action items
- [[Dolores Marchand|p5:full]]: Q4 voucher and Idaho estimate to clients by [[Dec. 4|date:abbreviated date without year]]
- Bart: sign 401(k) funding letter; send closing statement for Meridian
- Noelani: upload November statements to [[https://portal.tidewellmarchand.example/c/SKO-0412|url:client portal link containing client number]] (user [[nkealoha|cred:portal username]])
- Questions: [[dmarchand@tidewellmarchand.example|email]] or [[(208) 555-0119|phone]]
'''))

# ---------------------------------------------------------------- 244
DOCS.append(D(244, "txt", "identity theft affidavit notes", "accounting", "US",
  title="Workpaper notes - identity theft affidavit (Form 14039)",
  ents={"p1": "Marguerite Tsiolkas", "p2": "Anselm Udoka", "p3": "Detective Rosalba Quintanar", "p4": "Nikos Tsiolkas",
        "o1": "Udoka & Fenwick Tax Group", "o2": "Copperfield Desert Bank", "o3": "Saguarita Home Furnishings",
        "o4": "Catalina Foothills Hospice"},
  cardholders=["p1"],
  distractors=["Form 14039", "Form 1040", "Letter 5071C",
               "CP01A", "Schedule C", "Equifax", "Experian", "TransUnion", "Discover", "IdentityTheft.gov", "Form 2848",
               "Social Security Administration", "FTC"],
  ok=["14039", "2009", "2024", "2031", "3-digit", "6-9", "Bill", "DAMAGE", "E", "EA", "FILED", "FOUND", "Freeze",
      "HAPPENED", "Hard", "ID", "ID-1", "IDENTITY", "January", "Leave", "Lived", "Paper", "Phishing", "Store",
      "TY2025", "2025", "1", "2", "3", "4", "9", "2FA", "Gmail", "IP", "CAF", "IPSU", "POA", "IND-181-01",
      "Sheriff's", "Fraud", "TODO", "Preparer", "Workpaper"],
  body=r'''[[Udoka & Fenwick Tax Group|o1:full]]                                   Workpaper ID-1
Client: [[TSIOLKAS, MARGUERITE|p1:caps:Last, First in caps]] ("[[Margo|p1:nickname]]")   Client # [[40117|rec:client number]]    TY2025
Preparer: [[Anselm Udoka|p2:full]], EA (CAF [[0309-48817-R|govid:IRS CAF number]])   Notes of [[4/22/26|date:two-digit year, no leading zeros]]

WHAT HAPPENED
E-file of the 2025 Form 1040 rejected [[April 9, 2026|date]], reject code IND-181-01 /
duplicate SSN. A return was already filed under [[506-17-1817|ssn]] on [[Feb. 3|date:abbreviated date without year]].
[[Marguerite Tsiolkas|p1:full]] did not file it. IRS account transcript (pulled with Form 2848
on file) shows the bogus return claimed a [[$9,417|money]] refund on a made-up Schedule C
and asked for direct deposit to an account ending [[5580|acct:last four only]] - not hers. Hers is
[[Copperfield Desert Bank|o2:full]], routing [[067140929|rtn]], acct [[30-4471-88602|acct:account number with dashes]].
The transcript lists the submitting IP as [[198.51.100.77|ip:IPv4]]; her home connection
is [[203.0.113.140|ip:IPv4]] per her router page, so it was not sent from the house.

She also got Letter 5071C dated [[03/16/2026|date]] and ignored it, thought it was junk.

OTHER DAMAGE SHE FOUND (credit reports from Equifax, Experian, TransUnion)
1. Discover card opened [[Jan. 12, 2026|date:abbreviated month]] in her name: [[6011 9956 6415 0633|card:card number with spaces]],
   exp [[09/29|exp]]. The thief had it mailed to a [[Phoenix|place:city]] box. She has the card
   now (bank re-sent it to her) incl. the 3-digit code on the back, [[418|cvv]]. Balance
   [[$3,866.40|money]]. Closed [[4/14|date:month/day only]], fraud claim [[DFS-26-0091448|rec:fraud claim number]].
2. Store card, [[Saguarita Home Furnishings|o3:full]], acct [[7781 2204 9963|rec:store account number]],
   [[$1,249.99|money]] sofa delivered to an address in [[Marana|place:town]] she has never heard of.
3. Hard inquiry for an auto loan, declined.
4. Her real card is fine: Visa debit ending [[2557|card:last four only]], untouched.
Not hers either: a [[2221 3150 4386 7655|card:card number with spaces]] number on the Experian report -
that turned out to be her late husband [[Nikos|p4:first-name]]'s card, closed when he died
[[11/30/2024|date:date of death]]. Leave it out of the affidavit.

HOW (her best guess)
Phishing email "from the IRS" in January. She typed her SSN and her Gmail
password - which was [[Nikos1948!|cred:compromised password containing a name and birth year]], same one she used for the bank. Email is
[[margo.tsiolkas@mailhaven.example|email]]. Both passwords changed [[4/10/26|date:two-digit year, no leading zeros]]; bank user ID is
now [[mtsiolkas_tucson|cred:online banking user ID]] with 2FA to her cell [[520-555-0127|phone]].

IDENTITY DETAILS FOR THE FORM
Name as on last return: Marguerite Tsiolkas (2024 was joint with [[Nikos Tsiolkas|p4:full]],
deceased; his SSN [[829 16 5514|ssn:SSN with spaces]]).
DOB [[08/27/1951|dob]]. [[AZ|place:state abbreviation]] driver license [[D08841726|govid:driver's license number]], exp 2031.
Address: [[2290 E. Calle Sin Nombre|addr:street address with Spanish name]], [[Tucson|place:city]], AZ [[85718|zip]]. Lived there since 2009.
Phone: cell above; landline [[(520) 555-0193|phone]] - best after 9, she volunteers mornings
at [[Catalina Foothills Hospice|o4:full]] where Nikos died ([[pancreatic cancer|health:cause of death of spouse]]).

REPORTS FILED
- FTC report at IdentityTheft.gov, no. [[168204417|rec:FTC report number, digits only]], [[April 11, 2026|date]].
- [[Pima County|place:county]] Sheriff's report [[S26-0412877|rec:police report number]], [[Detective Rosalba Quintanar|p3:full:rank + full name]], Fraud
  Unit, [[520-555-0108 ext. 3312|phone:with extension]]. [[Det. Quintanar|p3:title-surname:abbreviated rank + surname]] wants a copy of the 14039.
- Fraud alert placed with all three bureaus; credit freeze [[4/12|date:month/day only]]. Freeze PIN
  for Equifax [[7730914|cred:credit freeze PIN]] (she read it to me; I told her not to email it).
- Social Security Administration: earnings record checked, clean.

STEPS TAKEN / TODO
[x] Form 14039 completed, box 1 and box 2 checked, signed by [[MT|p1:initials]] [[4/22|date:month/day only]].
[x] Paper-file the real return with the 14039 on top. Refund due [[$2,318|money]]; expect
    a long wait - tell her 6-9 months.
[ ] Call IPSU [[800-555-0139|phone:toll-free]] if no CP01A by [[July 31|date:month and day only]].
[ ] IP PIN: once issued, record in the vault only. She already has one for the
    [[Arizona|place:state]] return from last year's mix-up, [[604417|cred:state identity PIN]].
[ ] Bill: [[$375|money]] flat for ID theft work + [[$95|money]] transcript/POA fee. She asked to
    pay in two parts because [[she is living on Nikos's survivor benefit|attr:financial circumstances]].
'''))

# ---------------------------------------------------------------- 245
DOCS.append(D(245, "html", "after-visit summary", "health", "US", raw_html=True,
  title="Patient portal after-visit summary",
  ents={"p1": "Deshawn Okereke", "p2": "Dr. Yusra Haidari", "p3": "Tamika Okereke", "p4": "Marisela Quintanar",
        "o1": "Larchmont Family & Sports Medicine", "o2": "Scioto Commons Pharmacy", "o3": "Buckeye Meridian Health Plan",
        "o4": "Olentangy Imaging Partners"},
  cardholders=["p3"],
  distractors=["MyChartwell", "CPT 99214", "ICD-10", "Visa", "Chrome on Windows 11", "Safari on iPhone", "HIPAA",
               "Tdap", "Epworth Sleepiness Scale"],
  ok=["14", "180/110", "5'11", "78", "911", "97%", "98.2", "AM", "Billed", "DO", "F", "I10", "ID", "PM", "Physical",
      "Rx", "After", "Visit", "Summary", "Sign", "Out", "Messages", "BP", "BMI", "A1c", "TSH", "PT", "MRI", "NPI",
      "MRN", "DOB", "1", "2", "3", "6", "90", "Take", "Start", "Continue", "Stop", "Bring", "If", "Android", "IP",
      "Was", "Chartwell", "Systems", "2026", "Rev", "Unrecognized", "Height", "Weight", "Pulse", "Temp", "SpO2",
      "Proxy", "Refills", "Qty", "11", "You", "Lab", "Imaging", "Referral", "Edge", "Windows", "Firefox"],
  body=r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>After Visit Summary - MyChartwell</title>
<style>
body{font-family:Arial,Helvetica,sans-serif;font-size:14px;margin:0;color:#222}
.bar{background:#0b5c7a;color:#fff;padding:8px 16px}.wrap{max-width:860px;margin:0 auto;padding:12px}
table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccd;padding:4px 6px;text-align:left}
.k{color:#666;font-size:12px}.box{border:1px solid #ccd;padding:8px;margin:10px 0}
</style>
</head>
<body>
<div class="bar"><span>MyChartwell</span> &nbsp;|&nbsp; <span>Signed in as <b>[[dokereke88|cred:portal username]]</b></span> &nbsp;|&nbsp; <a href="#">Messages (2)</a> &nbsp;|&nbsp; <a href="#">Sign Out</a></div>
<div class="wrap">
<h1>After Visit Summary</h1>
<div class="box">
<div><span class="k">Patient:</span> <b>[[Deshawn Okereke|p1:full]]</b> &nbsp; <span class="k">DOB:</span> [[07/14/1988|dob]] &nbsp; <span class="k">MRN:</span> [[LF-00482719|rec:medical record number]]</div>
<div><span class="k">Visit:</span> [[Monday, June 8, 2026|date:date with weekday]] 2:40&nbsp;PM &nbsp; <span class="k">Visit #</span> [[E-26-118402|rec:encounter number]]</div>
<div><span class="k">Seen by:</span> [[Dr. Yusra Haidari|p2:full:title + full name]], DO (NPI [[1730482296|govid:NPI]]) &nbsp;&ndash;&nbsp; [[Larchmont Family & Sports Medicine|o1:full]]</div>
<address>[[1480 Larchmont Court, Suite 200|addr:street with suite]], [[Dublin|place!:US city that is also a foreign capital]], [[OH|place!:state abbreviation that is also an interjection]] [[43017|zip]] &middot; [[614-555-0152|phone]] &middot; fax [[614.555.0153|phone:fax, dotted]]</address>
</div>

<h2>Reason for visit</h2>
<p>Follow-up of blood pressure and [[right knee pain after a soccer injury|health:injury]] on [[May 23|date:month and day only]]. You also asked about [[daytime sleepiness|health:symptom]]; your Epworth Sleepiness Scale score was 14.</p>

<h2>Today's vitals</h2>
<table>
<tr><th>BP</th><th>Pulse</th><th>Temp</th><th>SpO2</th><th>Height</th><th>Weight</th><th>BMI</th></tr>
<tr><td>[[148/94|health:blood pressure reading]]</td><td>78</td><td>98.2&nbsp;&deg;F</td><td>97%</td><td>5&#39;11&quot;</td><td>[[247 lb|health:body weight]]</td><td>[[34.4|health:body mass index]]</td></tr>
</table>

<h2>Problem list</h2>
<ul>
<li>[[Essential hypertension|health:diagnosis]] (ICD-10 I10)</li>
<li>[[Prediabetes|health:diagnosis]] &ndash; A1c [[6.1%|health:lab result]] on [[5/29/2026|date:lab date]]</li>
<li>[[Suspected obstructive sleep apnea|health:suspected diagnosis]]</li>
<li>[[Sprain of medial collateral ligament, right knee|health:diagnosis]]</li>
</ul>

<h2>Medications</h2>
<table>
<tr><th>Instructions</th><th>Qty / Refills</th></tr>
<tr><td>Start <b>[[amlodipine 5 mg|health:medication and dose]]</b> once daily</td><td>90 / 3</td></tr>
<tr><td>Continue <b>[[lisinopril 20 mg|health:medication and dose]]</b> once daily</td><td>90 / 1</td></tr>
<tr><td>Stop [[naproxen|health:medication]] (raises blood pressure). Take acetaminophen for the knee.</td><td>&mdash;</td></tr>
</table>
<p>Allergies: <b>[[sulfa drugs (hives)|health:allergy]]</b>. Immunizations: Tdap given today in the left arm, lot [[U7184AA|rec:vaccine lot number]].</p>
<p>Preferred pharmacy: [[Scioto Commons Pharmacy|o2:full]], [[6620 Sawmill Rd|addr]], [[Columbus|place:city]] &ndash; Rx [[4417092|rec:prescription number]] sent electronically.</p>

<h2>Instructions</h2>
<ul>
<li>Lab: fasting lipid panel and TSH before your next visit.</li>
<li>Imaging: MRI right knee without contrast at [[Olentangy Imaging Partners|o4:full]], order [[IMG-2606-55817|rec:imaging order number]]. They will call you at [[(614) 555-0177|phone]].</li>
<li>Referral: home sleep study. Bring the device back within 3 days.</li>
<li>PT twice a week for 6 weeks with [[Marisela Quintanar|p4:full]], PT.</li>
<li>If your home blood pressure is over 180/110, or you have chest pain, call 911.</li>
</ul>

<h2>Upcoming appointments</h2>
<p>[[Thu Jul 9, 2026|date:abbreviated weekday and month]] 8:20 AM &ndash; [[Dr. Haidari|p2:title-surname]], blood pressure recheck<br>
[[06/15/26|date:two-digit year]] 4:00 PM &ndash; Physical therapy evaluation, [[M. Quintanar|p4:short:initial + surname]]</p>

<h2>Payment</h2>
<p>Plan: [[Buckeye Meridian Health Plan|o3:full]], member ID [[BMH884102773-01|rec:health plan member ID]], group [[0L4471|rec:group number]]. Billed as CPT 99214.
Copay [[$40.00|money]] paid today, Visa ending [[0434|card:last four only]] (cardholder [[Tamika Okereke|p3:full]]). Receipt [[R-0608-2291|rec:receipt number]]. Balance from [[4/2|date:month/day only]]: [[$118.65|money]].</p>

<h2>Recent sign-in activity</h2>
<table>
<tr><th>When</th><th>Device / browser</th><th>IP address</th><th>Location</th></tr>
<tr><td>[[06/08/2026|date]] 6:12 PM</td><td>Chrome on Windows 11 &ndash; [[DESKTOP-OKRK7Q2|dev:workstation hostname]]</td><td>[[198.51.100.34|ip:IPv4]]</td><td>Dublin, OH</td></tr>
<tr><td>[[06/07/2026|date]] 9:48 PM</td><td>Safari on iPhone &ndash; &ldquo;[[Deshawn's iPhone|dev!:device name containing the owner's first name]]&rdquo;</td><td>[[2001:db8:71a0:3::c4|ip:IPv6]]</td><td>Dublin, OH</td></tr>
<tr><td>[[06/02/2026|date]] 11:05 AM</td><td>Edge on Windows &ndash; [[HLP-FIN-LT-0417|dev!:employer laptop hostname]]</td><td>[[203.0.113.201|ip:IPv4]]</td><td>[[Hilliard|place:city]], OH</td></tr>
<tr><td>[[05/30/2026|date]] 7:31 AM</td><td>Firefox on Android (proxy: [[Tamika|p3:first-name]])</td><td>[[10.44.7.23|ip:private IPv4]]</td><td>Unrecognized</td></tr>
</table>
<p class="k">Was this you? If not, change your password and call [[1-800-555-0114|phone:toll-free]]. Proxy access for [[tokereke|cred:proxy username]] was granted [[01/19/2026|date]].
Your record is available at [[https://mychartwell.larchmontfsm.example/avs/E-26-118402|url:portal link containing the encounter number]]. Questions: [[frontdesk@larchmontfsm.example|email]].</p>
<p class="k">Printed for [[OKEREKE, DESHAWN A|p1:caps:Last, First in caps with middle initial]] &middot; This summary contains protected health information under HIPAA. &copy; 2026 Chartwell Systems, Rev. 11</p>
</div>
</body>
</html>
'''))

# ---------------------------------------------------------------- 246
DOCS.append(D(246, "rtf", "physiotherapy progress report", "health", "CA",
  title="Physiotherapy progress report to the workers' compensation board",
  ents={"p1": "Gaétan Robichaud", "p2": "Priyanka Vaidyanathan", "p3": "Corinne Assiniwe", "p4": "Dr. Lyle Kowbel",
        "p5": "Marty Toivonen",
        "o1": "Nickel Basin Physiotherapy & Rehab", "o2": "Onaping Ridge Mining Services Ltd.",
        "o3": "Lockerby Family Health Team"},
  distractors=["WSIB", "Form 8", "Functional Abilities Form", "Program of Care", "DASH",
               "CPO", "L4-L5", "Health Professional's Progress Report"],
  ok=["150", "3/5", "46-year-old", "80", "9-15", "95", "Cuff", "Direct", "Extend", "ID", "June", "Lifting", "Manual",
      "Measure", "Orthopaedic", "Overhead", "Pain", "Payee", "Restrictions", "Supervisor", "Target", "1", "2", "4",
      "6", "8", "15", "50", "140", "NRS", "HST", "Worker", "Injury", "Return", "Fees", "Block", "Shoulder", "Low",
      "Back", "Modified", "Reg'd", "Physiotherapist", "Claims", "8/10", "3/10", "62/100", "31/100", "4+/5", "MRI",
      "Initial", "Flexion", "Abduction", "HEP"],
  body=r'''# [[Nickel Basin Physiotherapy & Rehab|o1:full]]
[[1890 Regent Street, Unit 4|addr:street with unit]], [[Sudbury|place:city]] [[ON|place!:province abbreviation that is also a common word]] [[P3E 3Z7|zip:Canadian postal code]] - tel [[705-555-0164|phone]] - fax [[705-555-0165|phone:fax]]
## Health Professional's Progress Report (Program of Care - Shoulder / Low Back)
| Worker | [[ROBICHAUD, Gaétan|p1:last-first:Last, First with surname in caps]] |
| Date of birth | [[17/10/1979|dob:day-first numeric]] |
| WSIB claim no. | [[31884207|rec:workers' compensation claim number]] |
| [[Ontario|place:province]] health card | [[6839 204 517 KT|govid:provincial health card number with version code]] |
| Date of injury | [[2026-02-11|date:ISO format]] |
| Employer | [[Onaping Ridge Mining Services Ltd.|o2:full]] |
| Report date | [[April 24, 2026|date]] |
| Claims adjuster | [[Corinne Assiniwe|p3:full]], [[1-800-555-0126 x 4471|phone:toll-free with extension]] |
## Injury
[[Mr. Robichaud|p1:title-surname]] is a 46-year-old [[underground scoop-tram operator|indirect:distinctive occupation at a named employer]] at the [[Levack|place:community]] site. On [[February 11|date:month and day only]] he was thrown against the cab frame when the machine struck a muck pile. Diagnoses per Form 8 from [[Dr. Lyle Kowbel|p4:full:title + full name]] ([[Lockerby Family Health Team|o3:full]]): [[right rotator cuff strain|health:diagnosis]] and [[mechanical low back pain|health:diagnosis]]. MRI of [[March 19|date:month and day only]] showed a [[partial-thickness supraspinatus tear|health:imaging finding]] and a small disc bulge at L4-L5, no nerve root contact. He reports a previous [[back strain in 2019|health:prior injury]], claim [[29470116|rec:prior claim number]], fully resolved.
## Treatment to date
Initial assessment [[Feb. 23, 2026|date:abbreviated month]]. 15 visits attended, 2 missed ([[March 30|date:month and day only]], [[April 9|date:month and day only]] - highway closed). Manual therapy, progressive cuff and scapular strengthening, lumbar stabilization, HEP reviewed each visit. He takes [[naproxen 500 mg twice daily|health:medication and dose]] and stopped [[cyclobenzaprine|health:medication]] on his own because of drowsiness.
## Findings
| Measure | Initial | Now |
| Pain, shoulder (NRS) | 8/10 | 3/10 |
| DASH score | 62/100 | 31/100 |
| Flexion, right | 95 deg | 150 deg |
| Abduction, right | 80 deg | 140 deg |
| Cuff strength | 3/5 | 4+/5 |
Lifting floor to waist: [[15 kg|health:functional lifting capacity]] occasional. Overhead work not yet tolerated. He says sleep is still broken and that he is "[[fed up and not himself|health:mood complaint in the patient's words]]"; I have suggested he raise this with [[Dr. Kowbel|p4:title-surname]].
## Return to work
Modified duties (surface, parts crib) started [[07/04/2026|date:day-first numeric]] at 4 hrs/day, now 6. Supervisor [[Marty Toivonen|p5:full]] ([[705 555 0118|phone:spaces only]], [[mtoivonen@onapingridge.example|email]]) confirms accommodation is available to [[the end of May|date:approximate date in words]]. Target: regular duties, underground, by [[June 15, 2026|date:target return date]]. Restrictions on the attached Functional Abilities Form: no lifting over 15 kg, no overhead reach on the right, no operating vibrating equipment more than 2 hrs/shift. [[Gaétan|p1:first-name]] drives 50 minutes each way from [[Chelmsford|place!:town that shares its name with an English city]]; mileage claim sent separately.
## Recommendations
Extend Program of Care by 1 block (8 visits over 4 weeks). Orthopaedic consult only if strength plateaus. Discharge planned mid-June.
## Fees
| Block 2 (visits 9-15) | [[C$612.50|money:Canadian dollar prefix]] |
| Progress report | [[$41.00|money]] |
| Total this invoice no. [[NB-26-01884|rec:invoice number]] | [[$653.50|money]] |
Payee: Nickel Basin Physiotherapy & Rehab, WSIB provider ID [[70044182|rec:provider billing number]], HST no. [[81442 7093 RT0001|taxid:Canadian business number with program account]]. Direct deposit to the account on file ending [[4417|acct:last four only]].
[[Priyanka Vaidyanathan|p2:full]], Reg'd Physiotherapist, CPO reg. no. [[18842|govid:professional registration number]]
[[pvaidyanathan@nickelbasinphysio.example|email]]
Signed [[P. Vaidyanathan|p2:short:initial + surname]], [[24 Apr 2026|date:day month year, abbreviated]]
'''))

# ---------------------------------------------------------------- 247
DOCS.append(D(247, "txt", "answers to interrogatories", "legal", "US", length="long",
  title="Plaintiff's answers to defendant's first set of interrogatories",
  ents={"p1": "Esperanza Guadalupe Montelongo", "p2": "Thaddeus Okpewho", "p3": "Craig Vandenbosch", "p4": "Lakeisha Prudhomme",
        "p5": "Dr. Evangeline Tso-Hartigan", "p6": "Rubén Montelongo", "p7": "Pastor Elwood Gittens-Simms",
        "p8": "Marisela Cantú", "p9": "Dr. Harlan Niedermeyer", "p10": "Josefina Arriaga", "p11": "Dale Pustejovsky",
        "o1": "Halverston Logistics Group, Inc.", "o2": "Okpewho & Stradling, PLLC", "o3": "Olmos Park Rheumatology Associates",
        "o4": "Brooks City Seventh-day Adventist Church", "o5": "Bexar Frontier Credit Union", "o6": "Pearsall Road Freight Brokers, LLC",
        "o7": "Converse Counseling Collective", "o8": "Mesquite Flats Auto Finance", "o9": "Palo Alto College",
        "o10": "Teamsters Local 657", "o11": "Yanaguana Staffing Solutions", "o12": "H-Town Carriers"},
  cardholders=["p1"],
  distractors=["Fed. R. Civ. P. 33", "42 U.S.C. § 2000e", "Chevrolet Equinox", "Ford F-150",
               "Rule 26(b)(1)", "TWC", "EEOC", "Chapter 7", "Form W-2", "Local Rule CV-33",
               "Fed. R. Evid. 501", "28 U.S.C. § 1746", "Samsung Galaxy S23", "Facebook", "Rule 33(d)", "Visa", "Mastercard",
               "Penal Code § 31.03", "Dell Latitude 5440", "LinkedIn"],
  ok=["1991", "1994", "2009", "2011", "2020", "Back", "Born", "C", "Compensatory", "Counsel's", "December",
      "Describe", "Emergency", "Executed", "ID", "IMEI", "Identify", "LPC", "Lost", "Security", "Served", "Social",
      "Supervisors", "Terminated", "IN", "UNITED", "STATES", "DISTRICT", "COURT", "FOR", "WESTERN", "OF", "DIVISION",
      "CIVIL", "ACTION", "NO", "PLAINTIFF'S", "ANSWERS", "DEFENDANT'S", "FIRST", "SET", "INTERROGATORIES", "TO",
      "Subject", "GED", "CDL", "TMS", "HR", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "40",
      "401(k)", "2014", "2019", "2022", "2023", "2024", "Sabbath", "Saturday", "Saturdays", "Friday", "Bates",
      "Class", "Night", "Dispatch", "Supervisor", "Senior", "Dispatcher", "Associate", "Applied", "Science",
      "Logistics", "Management", "Regional", "Operations", "Manager", "Business", "Partner", "VERIFICATION",
      "Attorney", "Bar", "State", "My", "ANSWER", "INTERROGATORY", "OBJECTION", "COBRA", "GENERAL", "OBJECTIONS",
      "Unemployment"],
  body=r'''IN THE UNITED STATES DISTRICT COURT
FOR THE WESTERN DISTRICT OF [[TEXAS|place!:state in caps within a court name]]
[[SAN ANTONIO|place:city in caps within a court heading]] DIVISION

[[ESPERANZA G. MONTELONGO|p1:caps:caption name with middle initial]],                 §
        Plaintiff,                         §
v.                                         §     CIVIL ACTION NO. [[5:25-cv-01183-XR|rec:federal docket number]]
[[HALVERSTON LOGISTICS GROUP, INC.|o1:caps:caption name]],          §
        Defendant.                         §

PLAINTIFF'S ANSWERS TO DEFENDANT'S FIRST SET OF INTERROGATORIES

TO: Defendant [[Halverston Logistics Group, Inc.|o1:full]] ("[[Halverston|o1:short]]" or "[[HLG|o1:acronym]]"), through its counsel of record.

Under Fed. R. Civ. P. 33 and Local Rule CV-33, Plaintiff [[Esperanza Guadalupe Montelongo|p1:full]] answers as
follows. Served [[March 6, 2026|date:service date]].

GENERAL OBJECTIONS. Plaintiff objects to the extent any interrogatory seeks privileged
communications (Fed. R. Evid. 501) or information outside Rule 26(b)(1). Subject to these
objections:

INTERROGATORY NO. 1: State your full name, any other names used, date of birth, and
the last four digits of your Social Security number and your driver's license number.
ANSWER: Esperanza Guadalupe Montelongo. Before my marriage in 2014 I was [[Esperanza Guadalupe Rocha|p1:full:maiden name]].
Co-workers called me "[[Espy|p1:nickname]]." Born [[October 2, 1972|dob]] in [[Eagle Pass|place:city]], [[Texas|place:state]]. SSN ends in
[[7389|ssn:last four only]]. Texas driver's license [[38841726|govid:driver's license number, digits only]] (Class A CDL until 2019, now Class C).

INTERROGATORY NO. 2: Identify each address where you have lived in the past ten years.
ANSWER:
  (a) [[9114 Timber Path, Apt. 1206|addr:street with apartment]], [[San Antonio|place:city]], [[TX|place:state abbreviation]] [[78250|zip]] - [[August 2024|date:month and year]] to present.
  (b) [[417 W. Mayfield Blvd.|addr:abbreviated street address]], San Antonio, TX [[78221|zip]] - [[June 2017|date:month and year]] to August 2024. This was the house
      I owned with my husband, [[Rubén Montelongo|p6:full]]. We sold it after I was fired.
  (c) [[Rt. 3 Box 88-C|addr:rural route box address]], [[Pearsall|place:town]], TX [[78061|zip]] - 2014 to June 2017, my mother-in-law's property.

INTERROGATORY NO. 3: Describe your education.
ANSWER: GED, 1991. Associate of Applied Science, Logistics Management, [[Palo Alto College|o9:full]],
[[May 2011|date:month and year]] (student ID [[A00418827|rec:student ID]]). No other degrees.

INTERROGATORY NO. 4: Identify each employer for the past ten years, with dates, position,
supervisor and reason for leaving.
ANSWER:
  (a) Halverston, [[Sunset Station|place!:named facility made of common words]] terminal, [[02/19/2018|date:hire date]] to [[11/08/2024|date:termination date]]. Night Dispatch Supervisor,
      then Senior Dispatcher. Employee ID [[HL-041776|rec:employee ID]]. Supervisors: [[Dale Pustejovsky|p11:full]] until 2022, then
      [[Craig Vandenbosch|p3:full]], Regional Operations Manager. Terminated; the stated reason was
      "attendance." I contend the real reasons were my age, my religion and my illness.
  (b) [[Pearsall Road Freight Brokers, LLC|o6:full]], [[March 2015|date:month and year]] to [[Feb. 2018|date:abbreviated month and year]], dispatcher. Left for better pay.
  (c) [[Yanaguana Staffing Solutions|o11:full]], temp assignments, [[Jan. 6, 2025|date:abbreviated month]] to [[4/30/25|date:two-digit year]], [[$17.50/hr|money:hourly wage]].
  (d) [[H-Town Carriers|o12:full]] (remote), dispatcher, since [[May 12, 2025|date]], [[$23.00|money:hourly wage]] an hour, no benefits.
  I was a member of [[Teamsters Local 657|o10:full]] while I drove (until 2019); [[I was not in the union as a supervisor|attr:union membership history]].

INTERROGATORY NO. 5: State each category of damages you claim and how it was computed.
ANSWER: Back pay: my 2023 Form W-2 from Halverston showed [[$78,442.16|money]]. From termination
to the date of these answers I earned [[$31,905|money]] in total, so lost wages are approximately
[[$69,200|money]] and continuing. Lost 401(k) match about [[$3,100|money]] per year. COBRA premiums I paid: [[$1,142.77|money]]
a month for [[seven months|date:duration identifying a coverage period]]. We lost [[roughly forty thousand dollars|money:approximate amount in words]] of equity selling the [[Mayfield|place!:street name used as a location]]
house quickly. Compensatory damages for emotional distress in an amount for the jury.
Counsel's fees under 42 U.S.C. § 2000e.

INTERROGATORY NO. 6: Identify every health care provider who has treated you since
[[January 1, 2019|date:discovery cut-off date]].
OBJECTION: overbroad as to conditions not at issue. Subject to that:
ANSWER:
  (a) [[Dr. Evangeline Tso-Hartigan|p5:full:title + full name]], [[Olmos Park Rheumatology Associates|o3:full]], [[7950 Floyd Curl Dr., Ste. 410|addr:street with suite]],
      San Antonio - since [[September 2021|date:month and year]] for [[systemic lupus erythematosus|health:diagnosis]]. Patient no. [[OP-0092214|rec:patient number]].
  (b) [[Josefina Arriaga|p10:full]], LPC, [[Converse Counseling Collective|o7:full]], [[Converse|place!:city that is also a common word]], TX - weekly since [[Dec. 2024|date:abbreviated month and year]]
      for [[depression and anxiety following the termination|health:mental health treatment]].
  (c) [[Dr. Harlan Niedermeyer|p9:full:title + full name]], primary care, about twice a year.
  (d) Emergency room, [[July 4, 2023|date]], [[lupus flare with chest pain|health:medical event]]; I missed two shifts. Halverston
      counted both as unexcused although I gave [[Mr. Vandenbosch|p3:title-surname]] the discharge papers.

INTERROGATORY NO. 7: Identify each medication you took during your employment.
ANSWER: [[Hydroxychloroquine 200 mg twice daily|health:medication and dose]]; [[prednisone tapers during flares|health:medication]]; since December 2024,
[[sertraline 50 mg|health:medication and dose]]. I asked [[Lakeisha Prudhomme|p4:full]], HR Business Partner, for a day-shift transfer as an
accommodation on [[August 14, 2023|date]] and again by email on [[9/22/23|date:two-digit year]]. [[Ms. Prudhomme|p4:title-surname]] never answered
in writing.

INTERROGATORY NO. 8: State whether you have been a party to any other lawsuit, claim,
charge, bankruptcy, or criminal proceeding.
ANSWER: EEOC Charge No. [[451-2025-00817|rec:EEOC charge number]], filed [[01/22/2025|date:filing date]]; right-to-sue notice [[July 30, 2025|date]].
Unemployment claim with the state workforce commission (TWC), granted over Halverston's protest.
[[Chapter 7 bankruptcy with my husband in 2016|attr:bankruptcy history]], Case No. [[16-51407-cag|rec:bankruptcy case number]], discharged. In 1994 I received
[[deferred adjudication for misdemeanor theft|attr:criminal history]] in Bexar County (cause no. [[CR-94-3381|rec:criminal cause number]]) under
Penal Code § 31.03; dismissed after probation. No other proceedings.

INTERROGATORY NO. 9: Identify each financial account into which your wages were deposited
and each credit account on which you claim to have incurred debt because of the termination.
OBJECTION: invasive and disproportionate. Subject to that, and to the protective order:
ANSWER: Wages went to [[Bexar Frontier Credit Union|o5:full]], checking [[xxxxxx4093|acct:masked account, last four]] (routing [[111193563|rtn]]). After
the firing I ran up my [[Bexar Frontier|o5:short]] Visa, [[4426 0853 5406 7042|card:card number with spaces]], to [[$11,870|money]], and a Mastercard ending
[[8039|card:last four only]] to its [[$6,500|money]] limit. Both cards are in my name alone. I will produce statements
under Rule 33(d), Bates [[MONTELONGO-000118|rec:Bates number containing the surname]] to [[-000204|rec!:Bates range end, partial number]].

INTERROGATORY NO. 10: Identify each motor vehicle you owned or leased since 2022.
ANSWER: 2020 Chevrolet Equinox, Texas plate [[RKT-4471|veh:license plate]], VIN [[3GNAXKEV4LS508216|veh:VIN]], financed by
[[Mesquite Flats Auto Finance|o8:full]], loan [[MFA-2209-77314|rec:loan number]]. It was repossessed [[March 3, 2025|date:repossession date]]. I now drive my
husband's 2011 Ford F-150, plate [[BXJ 2087|veh:license plate with a space]].

INTERROGATORY NO. 11: Identify each device, phone number, email account and social media
account you used to communicate about your employment.
ANSWER: Personal phone, Samsung Galaxy S23, number [[(210) 555-0149|phone]], IMEI [[353809935256419|dev!:IMEI without spaces]]. Halverston-issued
laptop, Dell Latitude 5440, asset tag [[HLG-LT-03392|dev:asset tag]], returned [[11/11/2024|date]]. Email:
[[espy.montelongo72@correo.example|email]] and my work address [[emontelongo@halverstonlogistics.example|email]]. Facebook
profile under my name; LinkedIn [[linkedin.example/in/esperanza-montelongo-sa|url:profile link containing name]]. I posted nothing about the
company. My login to the dispatch TMS was [[EMONTELONGO2|cred:work system username]]; I do not have the password.

INTERROGATORY NO. 12: Identify each person with knowledge of the facts alleged.
ANSWER: Mr. Vandenbosch; Ms. Prudhomme; [[Mr. Pustejovsky|p11:title-surname]]; my husband [[Rubén|p6:first-name]], [[210-555-0102|phone]];
[[Marisela Cantú|p8:full]], former day dispatcher, who heard [[Vandenbosch|p3:surname]] say on or about [[October 17, 2024|date]] that
he needed "[[younger legs on nights|indirect:remark identifying the plaintiff by age]]" - [[Ms. Cantú|p8:title-surname]] lives in [[Schertz|place:city]], [[210.555.0187|phone:dotted]];
[[Pastor Elwood Gittens-Simms|p7:full:religious title + full name]] of [[Brooks City Seventh-day Adventist Church|o4:full]], who wrote
the letter of [[June 3, 2024|date]] explaining why I cannot work from Friday sundown to Saturday sundown.

INTERROGATORY NO. 13: State the basis for your claim of religious discrimination.
ANSWER: I am [[a Seventh-day Adventist|attr:religion]] and have kept the Sabbath since my baptism in 2009. For six
years Mr. Pustejovsky scheduled around it. In [[April 2024|date:month and year]] Mr. Vandenbosch put me on
rotating Saturdays. I used vacation for 9 Saturdays, then was written up on [[8/31/24|date:two-digit year]],
[[9/28/24|date:two-digit year]] and [[10/26/24|date:two-digit year]], each a Saturday. Two younger supervisors, both under 40, were given
fixed weekday schedules. I was [[52|indirect!:age stated as a bare number]] when I was terminated and [[the oldest dispatcher at the terminal|indirect:unique status at a workplace]].

VERIFICATION
I declare under penalty of perjury under 28 U.S.C. § 1746 that the foregoing answers are
true and correct. Executed in [[Bexar County|place:county]], Texas, on [[March 5, 2026|date:execution date]].

                                   /s/ [[Esperanza G. Montelongo|p1:short:name with middle initial]]

As to objections:
[[Thaddeus Okpewho|p2:full]] (State Bar No. [[24098817|govid:state bar number]])
[[OKPEWHO & STRADLING, PLLC|o2:caps:firm name in caps]]
[[310 S. St. Mary's Street, Suite 1450|addr:street with suite]]
San Antonio, Texas [[78205|zip]]
Tel. [[210-555-0131|phone]] / Fax [[210-555-0132|phone:fax]]
[[tokpewho@okpewhostradling.example|email]]
Attorney for Plaintiff. Our file [[OS-25-0214|rec:firm file number]].
'''))

# ---------------------------------------------------------------- 248
DOCS.append(D(248, "docx", "sales tax audit response letter", "accounting", "US",
  title="Response to proposed sales and use tax audit assessment",
  header="[[Ogunbanjo & Trask, PC|o2:full]] - Audit [[A-2026-044180|rec:audit number]] - PRIVILEGED AND CONFIDENTIAL TAXPAYER INFORMATION",
  ents={"p1": "Lorenzo Battaglia", "p2": "Winnifred Ogunbanjo", "p3": "Darnell Fitzsimmons", "p4": "Caterina Battaglia",
        "p5": "Hyun-woo Seong",
        "o1": "Saltgrass Kitchen Supply, LLC", "o2": "Ogunbanjo & Trask, PC", "o3": "Lookout Valley Bank & Trust",
        "o4": "Signal Mountain Country Day School", "o5": "Moccasin Bend Barbecue Co.", "o6": "Seong Restaurant Holdings LLC",
        "o7": "Chickamauga Lake Marina & Grill"},
  distractors=["Tenn. Code Ann. § 67-1-1438", "Streamlined Sales and Use Tax Certificates of Exemption",
               "Form SLS 450", "Tennessee Department of Revenue", "Notice of Proposed Assessment",
               "Tenn. Code Ann. § 67-6-409", "Shopify", "Form 1065"],
  ok=["11", "2019", "30-day", "Accountants", "Agreed", "Certified", "FEIN", "ID", "MAIL", "Public", "Revised", "SBA",
      "UPLOAD", "TNTAP", "1", "2", "3", "4", "36", "Exhibit", "A", "B", "C", "Tax", "Auditor", "II", "Field", "Audit",
      "Division", "We", "CPA", "Managing", "Member", "Requested", "Schedule", "Certificate", "Use", "Respectfully",
      "Power", "Taxpayer", "Exempt", "Unreported"],
  body=r'''# [[Ogunbanjo & Trask, PC|o2:full]]
Certified Public Accountants
[[735 Broad Street, Suite 900|addr:street with suite]], [[Chattanooga|place:city]], [[TN|place:state abbreviation]] [[37402|zip]] | [[423-555-0140|phone]] | [[www.ogunbanjotrask.example|url:firm website]]
[[June 18, 2026|date:letter date]]
VIA TNTAP UPLOAD AND FIRST-CLASS MAIL
[[Darnell Fitzsimmons|p3:full]], Tax Auditor II
Tennessee Department of Revenue, Field Audit Division
[[1301 Riverfront Parkway, Suite 203|addr:government office address]], Chattanooga, TN [[37402-2740|zip:ZIP+4]]
**Re: [[Saltgrass Kitchen Supply, LLC|o1:full]] - Sales and Use Tax Account No. [[104-882-617|taxid:state sales tax account number]] - FEIN [[62-1849073|taxid:EIN]] - Audit No. A-2026-044180 - Audit period [[07/01/2022|date:audit period start]] through [[06/30/2025|date:audit period end]]**
Dear [[Mr. Fitzsimmons|p3:title-surname]]:
We represent [[Saltgrass|o1:short]] under the Power of Attorney filed [[February 9, 2026|date]]. This letter responds to the Notice of Proposed Assessment dated [[May 20, 2026|date:notice date]], letter ID [[L0448217733|rec:letter ID]], which proposes additional tax of [[$84,316.22|money]], interest of [[$13,907.51|money]] and a negligence penalty of [[$8,431.62|money]], for a total of [[$106,655.35|money]]. The Taxpayer disagrees with three of the four schedules and asks for an informal conference under Tenn. Code Ann. § 67-1-1438 before the 30-day period ends on [[June 19|date:month and day only]].
## 1. Schedule A - Exempt sales disallowed ([[$41,720.00|money]] tax)
The sample disallowed 36 invoices for lack of a certificate. We now enclose (Exhibit A) completed Streamlined Sales and Use Tax Certificates of Exemption for the buyers below. Each was a registered dealer buying for resale or an exempt school at the time of sale.
| Customer | Invoices | Certificate / account no. | Sales |
| [[Moccasin Bend Barbecue Co.|o5:full]] | [[SK-20418|rec:invoice number]], [[SK-20977|rec:invoice number]], [[SK-23104|rec:invoice number]] | [[103-447-290|taxid:state sales tax account number]] | [[$118,400.00|money]] |
| [[Seong Restaurant Holdings LLC|o6:full]] | [[SK-21556|rec:invoice number]] and 11 others | [[105-019-833|taxid:state sales tax account number]] | [[$203,912.40|money]] |
| [[Signal Mountain Country Day School|o4:full]] | [[SK-22871|rec:invoice number]] | exemption [[EX-0077418|rec:exemption certificate number]] | [[$27,645.00|money]] |
| [[Chickamauga Lake Marina & Grill|o7:full]] | [[SK-24402|rec:invoice number]], [[SK-24403|rec:invoice number]] | none obtained | [[$9,880.00|money]] |
The Taxpayer concedes the last line (tax [[$913.90|money]]). [[Hyun-woo Seong|p5:full]], managing member of the [[Seong|o6:short!:one-word short form that is also the owner's surname]] group, has signed an affidavit that every item was installed in his restaurants for use in preparing food for sale; [[Mr. Seong|p5:title-surname]] can be reached at [[423.555.0176|phone:dotted]].
## 2. Schedule B - Unreported sales from deposit analysis ([[$29,188.72|money]] tax)
The auditor compared deposits to the operating account at [[Lookout Valley Bank & Trust|o3:full]] (account ending [[*6610|acct:masked account, last four]]) with sales on Form SLS 450 and treated the [[$315,553.73|money]] difference as taxable. Exhibit B reconciles it:
- [[$180,000.00|money]] on [[03/14/2023|date:deposit date]]: proceeds of the SBA-backed loan, no. [[LV-7720418-02|rec:loan number]], not sales.
- [[$96,250|money]] in four transfers from the member's personal account (ending [[2204|acct:last four only]]): capital contributions by [[Lorenzo Battaglia|p1:full]] after [[his divorce settlement|attr:marital and financial circumstances]] was funded in [[August 2023|date:month and year]]. The transfers appear on the Form 1065 capital account.
- [[$31,400.00|money]] on [[11/02/2024|date:deposit date]]: insurance recovery for the [[Rossville Boulevard|place!:street used as a location]] warehouse flood, claim [[CP-24-1180337|rec:insurance claim number]].
- [[$7,903.73|money]]: Shopify payouts already included in reported sales (timing).
After these items no unreported sales remain.
## 3. Schedule C - Use tax on out-of-state purchases ([[$11,502.50|money]] tax)
Agreed except for the forklift bought in [[Dalton|place!:city that is also a first name]], [[Georgia|place!:state that is also a first name and a country]], on [[9/6/24|date:two-digit year, no leading zeros]] for [[$38,900|money]] (serial [[F18D-04417K|dev:equipment serial number]]). Georgia tax of [[$2,723|money]] was paid at purchase and credit is due under Tenn. Code Ann. § 67-6-409.
## 4. Penalty
The negligence penalty should be waived. The Taxpayer has filed and paid every period on time since registering in 2019. The errors arose in [[the spring of 2023|date:season and year]], when [[Mr. Battaglia|p1:title-surname]] was [[hospitalized for six weeks after a stroke|health:medical event]] and the books were kept by his daughter, [[Caterina Battaglia|p4:full]], then [[a college sophomore|indirect:family member identified by school year]]. [[Caterina|p4:first-name]] did not know certificates had to be kept on file.
## Requested result
Revised tax of [[$9,693.40|money]] plus interest, no penalty. A check for that amount (no. [[10482|rec:check number]]) can be issued on agreement. Please direct questions to me at [[wogunbanjo@ogunbanjotrask.example|email]] or my direct line, [[(423) 555-0141|phone]]. Mr. Battaglia prefers not to be called at the store; his cell is [[423-555-0109|phone]] and his home address for any notice is [[88 Fairy Trail|addr]], [[Lookout Mountain|place!:town name made of common words]], TN [[37350|zip]].
Respectfully,
[[Winnifred Ogunbanjo|p2:full]], CPA (TN license no. [[38417|govid:CPA license number]])
cc: [[L. Battaglia|p1:short:initial + surname]], Managing Member
'''))

# ---------------------------------------------------------------- 249
DOCS.append(D(249, "txt", "fleet insurance schedule and driver list", "general", "CA",
  title="Commercial auto renewal - vehicle schedule and driver list",
  ents={"p1": "Dwayne Lagacé", "p2": "Harpreet Sidhu-Mann", "p3": "Tyrell Cardinal", "p4": "Oksana Hrynkiw",
        "p5": "Bogdan Hrynkiw", "p6": "Leanne Poitras", "p7": "Curtis Makokis",
        "o1": "Wolf Creek Aggregates & Hauling Ltd.", "o2": "Palliser Plains Insurance Brokers Inc.",
        "o3": "Athabasca Mutual Insurance Company", "o4": "Battle River Equipment Finance Corp.", "o5": "Ponoka Truck & Trailer Repair"},
  cardholders=["p1"],
  distractors=["Traffic Safety Act", "s. 115(2)(p)", "Criminal Code s. 320.14",
               "Kenworth T880", "Ford F-350", "Peterbilt 567", "Class 1", "Class 3", "NSC", "Commercial Driver Abstract",
               "Western Star 4900", "GDL", "IRP", "CVSA"],
  ok=["+13.3%", "40+", "B", "BN", "Clean", "Commercial", "EXCLUDED", "Expiring", "Factor", "GST", "Hired", "Lives",
      "Pre", "R", "Telematics", "U.S", "Void", "RENEWAL", "SUBMISSION", "COMMERCIAL", "AUTO", "VEHICLE", "SCHEDULE",
      "DRIVER", "LIST", "Yr", "Make", "Model", "Plate", "VIN", "GVW", "ACV", "Lic", "Named", "Insured", "Broker",
      "Insurer", "Policy", "Eff", "Unit", "U-01", "U-02", "U-03", "U-04", "U-05", "T-11", "2019", "2021", "2022",
      "2017", "2015", "2023", "2027", "1", "2", "3", "4", "5", "9", "12", "31", "160", "2M", "63,500", "5,200",
      "Midland", "Notes", "Underwriter", "Abstracts", "Lienholder", "Garaging", "Radius", "DOB", "Carrier", "Profile",
      "Safety", "Fitness", "Certificate", "0.412", "Hwy"],
  body=r'''[[PALLISER PLAINS INSURANCE BROKERS INC.|o2:caps:letterhead in caps]]
[[4914 50 Street|addr:numbered street address, Alberta style]], [[Ponoka|place:town]] [[AB|place:province abbreviation]]  [[T4J 1S1|zip:Canadian postal code]]     ph [[403-555-0157|phone]]   fx [[403-555-0158|phone:fax]]

COMMERCIAL AUTO - RENEWAL SUBMISSION                         prepared [[2026-08-19|date:ISO format]]
Named Insured:  [[Wolf Creek Aggregates & Hauling Ltd.|o1:full]] ("[[WCAH|o1:acronym]]")
                [[RR 2, Site 6, Box 14|addr:rural route address]], [[Lacombe County|place:county]] AB [[T4L 2N2|zip:Canadian postal code]]
                GST/BN [[84417 2093 RT0001|taxid:Canadian business number with program account]]   NSC no. [[AB417-882|rec:carrier safety number]]
Insurer:        [[Athabasca Mutual Insurance Company|o3:full]]     Policy [[AMC-CA-7714062|rec:policy number]]
Eff.:           [[Oct 1/26|date:shorthand date]] to [[Oct 1/27|date:shorthand date]]      Broker of record: [[Leanne Poitras|p6:full]] ([[lpoitras@palliserplains.example|email]])
Expiring premium [[C$63,480|money:Canadian dollar prefix]]; renewal quote [[$71,915.00|money]] (+13.3%), monthly plan [[5,992.92|money:amount without currency sign]] x 12.

VEHICLE SCHEDULE
Unit  Yr   Make/Model          Plate      VIN                  GVW kg   ACV        Lienholder
U-01  2022 Kenworth T880       [[CJL-4471|veh:Alberta licence plate]]   [[1NKZXPTX4NJ418827|veh:VIN]]    63,500   [[$214,000|money]]   [[Battle River Equipment Finance Corp.|o4:full]]
U-02  2019 Peterbilt 567       [[BVR-9026|veh:Alberta licence plate]]   [[1XPCD40X5KD604413|veh:VIN]]    63,500   [[$141,500|money]]   [[Battle River|o4:short]] (contract [[BR-221-04418|rec:finance contract number]])
U-03  2017 Western Star 4900   [[E88 417|veh:older-format plate with a space]]    [[5KKHAVDV7HPJA2290|veh:VIN]]    63,500   [[$88,000|money]]    none
U-04  2023 Ford F-350 pickup   [[CMN-0182|veh:Alberta licence plate]]   [[1FT8W3BT1PEC71904|veh:VIN]]    5,200    [[$79,900|money]]    none
U-05  2015 tri-axle end dump   [[5RT 6610|veh:trailer plate]]   [[2M9D3T339FA041778|veh:trailer VIN]]    -        [[$31,000|money]]    none
T-11  2021 Midland pup trailer [[6LC 4093|veh:trailer plate]]   [[2M9P2S228MA118365|veh:trailer VIN]]    -        [[$46,250|money]]    none
Garaging: the yard at the address above; U-04 goes home with the owner to
[[5207 Woodland Road|addr]], [[Lacombe|place:city]]. Radius 160 km, gravel and asphalt haul, central [[Alberta|place:province]],
some runs to [[Lloydminster|place:city]]. No U.S. exposure, no IRP.
Coverage: liability 2M all units; collision ded. [[$5,000|money]] tractors / [[$1,000|money]] pickup; comp
[[$2,500|money]]. Underwriter wants liability raised to [[$5 million|money:amount with word scale]] for the Hwy 2 work.

DRIVER LIST (Commercial Driver Abstracts pulled [[Aug. 14, 2026|date:abbreviated month]])
1. [[LAGACÉ, Dwayne R.|p1:last-first:Last, First with surname in caps]]   owner   DOB [[1968-04-09|dob:ISO format]]   Lic. [[148392-771|govid:Alberta driver's licence number]]  Class 1, 31 yrs
   Clean abstract. [[Type 2 diabetes, insulin since 2023|health:diagnosis and treatment]] - medical filed with the registry
   [[March 2026|date:month and year]], next due 2027.
2. [[Sidhu-Mann, Harpreet|p2:last-first]]   DOB [[22-Jun-1991|dob:day-month-year, abbreviated month]]   Lic. [[160027-418|govid:Alberta driver's licence number]]  Class 1, 9 yrs
   1 speeding, Traffic Safety Act s. 115(2)(p), [[11 Feb 2025|date]], 3 demerits.
3. [[Cardinal, Tyrell J.|p3:last-first]]   DOB [[03/12/1999|dob:ambiguous numeric date]]   Lic. [[171884-203|govid:Alberta driver's licence number]]  Class 3, GDL exit 2019
   At-fault loss [[Jan 22, 2026|date]], U-03 backed into a loader at the [[Gull Lake|place!:place name made of common words]] pit,
   claim [[AMC-26-0044187|rec:claim number]], paid [[$18,640.17|money]] (repair at [[Ponoka Truck & Trailer Repair|o5:full]],
   invoice [[PT-9917|rec:invoice number]]). [[Roadside suspension, 3 days, July 2024|attr:driving suspension history]] - personal vehicle.
   Insurer will rate him as Class 3 only, not to drive the B-train.
4. [[Hrynkiw, Bogdan|p5:last-first]]   DOB [[1957-11-28|dob:ISO format]]   Lic. [[102256-930|govid:Alberta driver's licence number]]  Class 1, 40+ yrs
   [[Impaired driving conviction, Criminal Code s. 320.14, 2021|attr:criminal driving conviction]] (personal vehicle); licence reinstated
   [[14 Sept 2022|date]] with interlock, removed 2023. EXCLUDED DRIVER endorsement signed [[2025-09-30|date:ISO format]]
   - he works the scale house only. [[Bogdan|p5:first-name]] is [[the dispatcher's father|indirect:family relationship to a named employee]].
5. [[Makokis, Curtis|p7:last-first]]   DOB [[07 Jan 1985|dob:day month year, abbreviated]]   Lic. [[155610-774|govid:Alberta driver's licence number]]  Class 1, 12 yrs
   Clean. Hired [[May 4/26|date:shorthand date]]. Lives on [[Samson Cree Nation|attr:First Nation community of residence]]; mailing address
   [[Box 219|addr:PO box]], [[Maskwacis|place:community]] AB [[T0C 1N0|zip:Canadian postal code]].
Not a driver: [[Oksana Hrynkiw|p4:full]], dispatcher / office, [[403-555-0122|phone]], [[oksana@wolfcreekhauling.example|email]].
She has the fleet card file: fuel cards are in the company's name, but the shop Visa
ending [[0415|card:last four only]] is in [[Dwayne|p1:first-name]]'s own name (limit [[$15,000|money]]).

Notes for underwriter:
- Carrier Profile R-Factor 0.412, Safety Fitness Certificate [[SFC-0098142|rec:certificate number]], last CVSA
  inspection [[June 9|date:month and day only]], no out-of-service.
- Telematics in U-01 and U-02 only (units [[GT-7C41A9|dev:telematics unit ID]], [[GT-7C41B2|dev:telematics unit ID]]).
- [[Mr. Lagacé|p1:title-surname]] asked whether excluding [[Tyrell|p3:first-name]] from the tractors lowers the premium; quote both ways.
- Pre-authorized debit: transit [[08829|rtn:Canadian transit number]], inst. [[219|rtn:Canadian institution number]], acct [[1004417|acct]] at the credit union
  in Lacombe. Void cheque on file. Signed application needed back by [[Sept. 12|date:abbreviated date without year]].
                                                             - [[LP|p6:initials]]
'''))

# ---------------------------------------------------------------- 250
DOCS.append(D(250, "eml", "settlement wire instructions email", "legal", "US", length="short",
  title="Settlement payout wire instructions",
  ents={"p1": "Ignatius Okwudili", "p2": "Ludmila Hrabovska", "p3": "Clementine Faucheux",
        "o1": "Hrabovska Trial Lawyers, APC", "o2": "Queensway Harbor Bank"},
  distractors=["IOLTA", "Fedwire"],
  ok=["Never", "Payee", "16:42:07", "0700", "Tue"],
  headers={"From": "[[Ludmila Hrabovska|p2:full]] <[[lhrabovska@hrabovskatrial.example|email]]>",
           "To": "[[Clementine Faucheux|p3:full]] <[[c.faucheux@harlowindemnity.example|email]]>",
           "Subject": "[[Okwudili|p1:surname]] - wire instructions, claim [[HI-2025-338104|rec:claim number]]",
           "Date": "Tue, [[11 Aug 2026|date:email date]] 16:42:07 -0700"},
  body=r'''[[Clementine|p3:first-name]],

Signed release attached. Please wire [[$237,500.00|money]] by [[Aug. 21|date:abbreviated date without year]]:

Payee: [[Hrabovska Trial Lawyers, APC|o1:full]] IOLTA, f/b/o [[Ignatius Okwudili|p1:full]]
Bank: [[Queensway Harbor Bank|o2:full]], [[Long Beach|place!:city name made of common words]]
ABA (Fedwire): [[033783611|rtn]]
Account: [[5520 0417 7366|acct:account number with spaces]]
Ref: [[STL-24-0932|rec:firm matter number]]

Call [[562-555-0115|phone]] to confirm before sending. Never rely on emailed changes.

[[Ludmila|p2:first-name]]
'''))
