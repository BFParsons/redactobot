/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Sample documents for the "Use a sample document" button:
 * parody paperwork about fictional characters from popular films and series.
 * Every person, number, address and account is invented. Phone numbers use the
 * 555-01xx range, email addresses use the reserved .example domain, and the
 * card and IBAN are the public test values. Never put real data here.
 */

/** One sample document. */
export interface Sample {
  /** Short name of the document, for tests and tooling. */
  title: string;
  /** The document text loaded into the app. */
  text: string;
}

/** The sample documents, shown one after another. */
export const SAMPLES: Sample[] = [
  {
    title: 'House Atreides relocation claim',
    text: `EXPENSE CLAIM - CONFIDENTIAL
Filed March 3, 2026 by Thufir Hawat, Head of Finance, Atreides Holdings Ltd.

Claimant: Paul Atreides, date of birth June 12, 2005. Employee file HR-10191.
Reason for travel: permanent family relocation from Caladan to Arrakeen. The claimant
describes the move as "not my idea".

Items claimed:
- Moving costs, one ancestral household: $84,500.00
- Stillsuit, custom fitted, non-refundable: $3,200.00
- Sand damage to formal boots: $410.75
- "Emotional support water", 40 litres: $1,975.00 (rejected, see policy 7.2)

Medical note from Dr. Wellington Yueh: the claimant reports vivid recurring dreams and
mild heat exhaustion. Dr. Yueh also says he has nothing to hide and asks that we stop asking.

Reimburse to account 4471-889-2203 at Caladan Credit Union. Lady Jessica has asked to be
copied on everything: jessica@atreides-holdings.example or 604-555-0142.

Home address on file: 12 Palace Road, Arrakeen. Please do not send mail by worm.`,
  },
  {
    title: 'Death Star workplace incident report',
    text: `WORKPLACE INCIDENT REPORT - PERSONNEL IN CONFIDENCE
Galactic Empire Human Resources, Battle Station Division. Case number IR-2187-0042.
Reported April 9, 2026 by Admiral Conan Motti.

Summary: During a budget meeting, Admiral Motti questioned a colleague's management
style. The colleague, Darth Vader, responded with what the admiral calls "a remote and
unwelcome neck adjustment". Grand Moff Wilhuff Tarkin ended the meeting.

Medical: Admiral Motti was treated for a bruised windpipe and anxiety. Mr. Vader's own
file notes chronic breathing problems and severe burns; he declined a wellness check.

Witnesses: Wilhuff Tarkin, Cassio Tagge.

Separately, facilities reports an uncovered exhaust port on level 3. Contractor Galen Erso
quoted $18,000 to cover it. The request was denied as "not a priority".

Admiral Motti's contact: conan.motti@empire-hr.example, 415-555-0187.
Settlement of $25,000 to be paid to account 5520-114-9087. He has asked for a desk on a
different moon.`,
  },
  {
    title: 'Starfleet Medical: annual physicals',
    text: `STARFLEET MEDICAL - PATIENT CONFIDENTIAL
Annual physical summaries, prepared May 20, 2026 by Dr. Beverly Crusher.

Patient: Jean-Luc Picard, born July 13, 1965. Medical record number MRN-1701-D.
History: artificial heart, fitted after a bar fight he calls "a youthful misjudgement".
Blood pressure rises sharply when children are on the bridge. Prescribed: fewer cups of Earl Grey
tea, and a holiday he will not take.

Patient: William Riker. Lower back strain. Cause: he will not sit down on a chair in the
normal way. Referred to physiotherapy. He has also asked whether the beard is covered by
his health plan. It is not; the $1,200.00 grooming claim is denied.

Patient: Geordi La Forge. Recurring headaches linked to his visor. Follow-up in two weeks.

Patient: Worf. Declined the examination. Says he is fine. Has a visible fracture.

Counselling referrals go to Deanna Troi: deanna.troi@starfleet-medical.example,
628-555-0133. Billing questions: 1701 Galaxy Way, San Francisco, CA 94129.
Insurance policy number POL-47-ALPHA-83.`,
  },
  {
    title: 'Legal intake: the Gibson incident',
    text: `PRIVILEGED AND CONFIDENTIAL - ATTORNEY WORK PRODUCT
Client intake notes, June 2, 2026. Prepared by Margo Wallace, Wallace & Plague LLP.

New client: Dade Murphy, age 18, of 221 West 4th Street, New York, NY 10014.
Social Security number 219-09-9999. Phone 212-555-0164. Email dade@crashoverride.example.

Mr. Murphy is under investigation after a supercomputer at Ellingson Mineral Company
began playing a cartoon. He says he was "just looking around". He has a prior juvenile
record from 1988 and was barred from using a telephone until his 18th birthday.

Also named in the complaint: Kate Libby, Emmanuel Goldstein and Ramon Sanchez.

The complainant, Eugene Belford, head of security at Ellingson, claims losses of
$25,000,000. Our forensic review suggests Mr. Belford moved that money himself, to
account 7781-204-5566.

Evidence we should not have on paper: the server login was user name: admin,
password: Tr0ub4dor-99. IP address 192.0.2.44.

Agent Richard Gill of the Secret Service has called four times. Do not call him back
before Friday.`,
  },
  {
    title: 'Tyrell Corporation expense audit',
    text: `INTERNAL AUDIT - RESTRICTED
Tyrell Corporation, Finance Department. Audit reference AUD-2019-1107.
Prepared November 8, 2026 by Rachael Rosen for Eldon Tyrell.

Subject: expenses claimed by contractor Rick Deckard, badge number B-263-54.

Mr. Deckard was hired to "retire" four former employees: Roy Batty, Pris Stratton,
Leon Kowalski and Zhora Salome. He has billed us for:
- Noodles, one portion (he ordered four, received two): $14.50
- Whisky, described as "research": $380.00
- One trench coat, torn on a rooftop: $1,150.00
- Therapy, 12 sessions, reason given as "unicorn dreams": $2,400.00

Medical note: Mr. Deckard's empathy test results were inconclusive. He was upset by the
question and asked to stop. Dr. Hannibal Chew advises we not tell him.

Mr. Kowalski's file records a short temper when asked about his mother.

Pay the balance to card 4111 1111 1111 1111, or by transfer to
IBAN GB82 WEST 1234 5698 7654 32. Contact: deckard@tyrell-contractors.example,
213-555-0119, 9732 Hauser Tower, Los Angeles, CA 90013.`,
  },
  {
    title: 'Hill Valley auto insurance claim',
    text: `AUTO INSURANCE CLAIM - PERSONAL INFORMATION
Hill Valley Mutual Insurance. Claim number CLM-1985-1026. Filed October 27, 2026.

Policyholder: Dr. Emmett Brown, 1640 Riverside Drive, Hill Valley, CA 95420.
Date of birth: August 3, 1955. Phone 530-555-0121. Email doc@brown-enterprises.example.
Driver's license number D4428817.

Vehicle: 1981 DeLorean, licence plate 3KLM992, VIN SCEDT26T8BD005261.
Declared modifications: "a few". Declared top speed: 88 miles per hour, "precisely".

Description of loss: the vehicle was struck by lightning at 10:04 p.m. outside the
courthouse and then, in the policyholder's words, "went somewhere else for a while".
It returned covered in ice. A second claim reports that a train hit it.

Other driver: Martin McFly, age 17, of 9303 Lyon Drive. Not on the policy.
Witness: Jennifer Parker.

Third-party claim: Biff Tannen seeks $3,000 for a car filled with manure. This is his
third such claim.

Amount claimed: $62,000. Pay to account 8834-551-7702. Adjuster's note: the policyholder
asked whether the policy covers events that have not happened yet.`,
  },
  {
    title: 'Marshall College expense review',
    text: `FACULTY EXPENSE REVIEW - CONFIDENTIAL
Marshall College, Office of the Bursar. File number EXP-1936-0077.
Reviewed September 14, 2026 by Dean Marcus Brody.

Faculty member: Dr. Henry Jones Jr., Department of Archaeology.
Passport number 548832917. Home: 38 Adler Avenue, Fairfield, CT 06824.
Phone 203-555-0176. Email h.jones@marshall-college.example.

Dr. Jones has taught 3 of his 41 scheduled classes this term. His travel claims:
- Flights to Cairo, Kathmandu and Venice: $9,840.00
- One hat, replaced: $45.00
- One hat, recovered at personal risk (no charge)
- Damage to a market, a truck, a tank and a zeppelin: $212,600.00
- Snake bite treatment (he was not bitten, he "wanted to be sure"): $130.00

Health note: Dr. Jones has a diagnosed fear of snakes and has asked that this not be
shared with students.

Items acquired "for the museum" have not arrived. Dr. Jones says a rival,
Rene Belloq, took them. His companion Marion Ravenwood confirms this and also says he
owes her $5,000.

Reimbursement on hold. Account on file: 2290-663-4418.`,
  },
  {
    title: 'Tax audit notice: Thomas Anderson',
    text: `NOTICE OF AUDIT - TAXPAYER CONFIDENTIAL
Department of Revenue, Compliance Division. Case number TX-1999-0331.
Issued February 18, 2026.

Taxpayer: Thomas Anderson, 101 Lake Street, Apartment 101, Chicago, IL 60601.
Social Security number 123-45-6789. Date of birth March 11, 1962.
Employer: Metacortex Software Inc., employer ID number 12-3456789.
Phone 312-555-0101. Email t.anderson@metacortex.example.

Our records show two sets of income. By day, Mr. Anderson reports a salary of $74,200 as
a programmer. By night, he appears to sell software under another name and reports
nothing. He has told our agent, Mr. Smith, that the income is imaginary. That is not a
recognised deduction.

Also disallowed:
- Sunglasses, 14 pairs: $2,660.00
- One leather coat, floor length: $1,400.00
- "Training programs", including kung fu: $18,000.00

Mr. Anderson's manager notes he is often late and has a problem with authority.

Amount owing: $31,455.20. Pay within 30 days. Questions may go to his adviser,
Morpheus Reyes, at 312-555-0147. Mr. Reyes will offer you a choice. Please just take
the form.`,
  },
  {
    title: 'Ghostbusters small business loan file',
    text: `SMALL BUSINESS LOAN FILE - BANK CONFIDENTIAL
Manhattan Trust Bank, Commercial Lending. Loan number LN-1984-0608.
Reviewed June 8, 2026 by loan officer Janine Melnitz.

Applicants: Dr. Peter Venkman, Dr. Raymond Stantz and Dr. Egon Spengler, trading as
Ghostbusters Inc., 14 North Moore Street, New York, NY 10013.
Business phone 212-555-0122. Email billing@ghostbusters-inc.example.

Purpose of loan: "professional paranormal investigation and elimination". Amount: $95,000.
Security offered: Dr. Stantz's family home, 55 Central Park West, already carrying a third
mortgage at 19 percent.

Assets: one former fire station, one 1959 ambulance (the mechanic's list of repairs runs to
two pages), and equipment the applicants prefer not to
describe to a bank.

Risk notes:
- Dr. Venkman lost his university post. The dean's letter questions his research methods
  and his motives.
- Dr. Spengler lists his only hobby as growing things in jars.
- Environmental inspector Walter Peck has filed a complaint, file number EPA-0042-NY.

First client: Dana Barrett, who reports a problem in her refrigerator. Deposit of $5,000
paid to account 6612-908-3345.`,
  },
  {
    title: 'InGen payroll and security review',
    text: `PAYROLL AND SECURITY REVIEW - STRICTLY CONFIDENTIAL
InGen Corporation, Isla Nublar office. Review number SEC-1993-0611.
Prepared June 11, 2026 by Ray Arnold for John Hammond.

Employee: Dennis Nedry, Systems. Date of birth April 22, 1971.
Home address: 2714 Harbor View Road, San Jose, CA 95134. Phone 408-555-0158.
Email dnedry@ingen-systems.example. Salary: $68,000, which he describes as an insult.

Concerns:
- Mr. Nedry has $1,500,000 arriving from a Lewis Dodgson into account 3345-770-1126.
  When asked, he laughed and said the name loudly in a restaurant.
- He has locked every door in the park with a password only he knows. The login screen
  now shows a cartoon of him. User name: dnedry, password: MagicW0rd-93.
- He was last seen carrying a can of shaving cream towards the east dock in a storm.

Health and safety: game warden Robert Muldoon reports the fences are off. Dr. Ian Malcolm
has a broken leg and several opinions. Dr. Ellie Sattler and Dr. Alan Grant are unpaid
visitors and are not covered by our insurance, policy number POL-65-MYA-002.

Mr. Hammond's note says cost was never a concern. Finance's note: we have the receipts.
That is the problem.`,
  },
  {
    title: 'Bag End courier insurance claim',
    text: `COURIER INSURANCE CLAIM - POLICYHOLDER COPY
Shire Mutual Assurance. Claim number CLM-3019-0922. Filed September 22, 2026.

Policyholder: Frodo Baggins, 1 Bagshot Row, Hobbiton, WA 98101. Date of birth September 22, 1968.
Phone 206-555-0113. Email frodo@bagend-courier.example. Policy POL-33-BAG-117.

Item delivered: one small gold ring, described as "ordinary". Declared value: $40.00. Insured value, after a
long chat with the agent: $4,000,000.00.

Journey costs claimed:
- Walking boots, six pairs: $1,140.00
- Travel companions, five, meals and second breakfasts: $9,860.50
- Cloak, elven, one, "shows up as grey": $620.00
- Mountain damage to a trip planner: $260.00

Medical note: the claimant reports a recurring shoulder ache and sleeplessness. Dr. Samwise Gamgee
confirms he carried the claimant up a hill, and asks that it stay off the record.

Third party: Mr. Gollum, a former tenant of a cave, disputes ownership and has bitten a finger.

Reimburse account 6624-118-0970. Adjuster Bilbo Baggins asks that the claim be settled before his
111th birthday party.`,
  },
  {
    title: 'Amity Island beach closure memo',
    text: `TOWN OF AMITY - CONFIDENTIAL MEMO
Office of the Mayor. Reference MEM-1975-0704. Dated July 3, 2026.

To: Mayor Larry Vaughn. From: Chief Martin Brody, 41 Ocean Avenue, Amity, NY 11930.
Phone 631-555-0127. Email brody@amity-police.example. Badge number B-4417.

Subject: request to close all beaches for the holiday weekend.

The Chief reports a "very large fish". The Mayor replies that the summer economy of $2,300,000.00
depends on the weekend and asks that the sign wording be softened.

Medical: the Chief reports a fear of open water and mild seasickness, and asks that this not go
into the personnel file. Deputy Hendricks has also taken three days of sick leave.

Outside experts: Matt Hooper of the Oceanographic Institute, invoice $4,800.00. Local fisherman
Quint, invoice $10,000.00 and one boat.

Please pay the consultants by transfer to account 3381-702-5518.

A reminder from the clerk: purchase orders for boats must be approved by the Mayor, not the Chief.`,
  },
  {
    title: 'Cyberdyne personnel file: Connor, S.',
    text: `PERSONNEL FILE - HUMAN RESOURCES ONLY
Cyberdyne Systems, Sunnyvale, CA 94085. File HR-1984-0829. Reviewed August 29, 2026 by Miles Dyson.

Employee: Sarah Connor. Date of birth February 13, 1959. Social Security number 412-67-8830.
Home 2144 Elm Court, Sunnyvale, CA 94086. Phone 408-555-0166. Email sconnor@cyberdyne-staff.example.

Occupation: waitress, part time. Annual earnings: $19,400.00.

Notes for the file:
- The employee has reported "a future of machines" to three managers.
- A request for leave to attend a medical appointment was denied: Dr. Peter Silberman records a
  diagnosis of anxiety and delusions.
- The employee asked whether the company could stop a certain research project. It cannot.

Contact for emergencies: her son John, age 10, c/o Janelle Voight. Pay to account 7790-446-1120.

Security flagged a visitor who arrived in no clothes and asked for the employee by her full name.
This is the third such visit this quarter.`,
  },
  {
    title: 'Nostromo crew expense report',
    text: `CREW EXPENSE REPORT - COMMERCIAL TOWING VESSEL NOSTROMO
Weyland Corporation, Accounts. Report XR-79-0518. Filed May 18, 2026 by Dallas Maddox, Captain.

Crew of record: Ellen Ripley (warrant officer, Social Security number 536-90-4417), Arthur Kane,
Joan Lambert, Dennis Parker and Samuel Brett. Medical officer: Ash, engineer, passport A4471209.

Items claimed:
- Emergency rations, seven crew: $2,180.00
- Replacement hatch, one, "chewed": $14,500.00
- Medical treatment for one crew member after a face incident: $31,250.00
- Cat food, one cat, for "morale": $18.75

Medical note: Mr. Kane reports a sore throat and a sensation of being full. Dr. Ash has signed him
off as fit.

The company has asked that all samples be returned to head office at 1 Corporate Way, Houston,
TX 77002. Contact weyland.claims@wy-corp.example or 713-555-0138.

Deposit refunds to account 2204-558-1307.`,
  },
  {
    title: 'Corleone Olive Oil tax audit',
    text: `NOTICE OF TAX AUDIT - TAXPAYER CONFIDENTIAL
Internal Revenue Service, Business Division. Case TX-1972-0314. Issued March 14, 2026.

Taxpayer: Genco Pura Olive Oil Imports Inc., employer ID number 11-2345678, 128 Mulberry Street,
New York, NY 10013. Owner: Vito Corleone, born December 7, 1892.
Phone 212-555-0149. Email accounts@genco-pura.example.

Reported income: $412,000.00. Our review found deposits of $2,900,000.00 labelled "favours" and
"consulting".

Disallowed items:
- Funeral flowers, 14 arrangements: $5,600.00
- A horse's veterinary bill: $3,250.00
- "Special arrangements" with local suppliers: $75,000.00

Medical note: the owner has a documented heart condition, reviewed by Dr. Michael Corleone's
family doctor, and asks that audit meetings be held at his home in the morning.

Please bring all books to the meeting. Payment due: $182,600.30 to account 4410-927-3366.
Agent Sonny Russo will attend. Bring cannoli.`,
  },
  {
    title: 'McCallister household insurance claim',
    text: `HOMEOWNER INSURANCE CLAIM - PERSONAL INFORMATION
Winnetka Family Mutual. Claim HC-1990-1220. Filed December 22, 2026.

Policyholders: Peter and Kate McCallister, 671 Lincoln Avenue, Winnetka, IL 60093.
Phone 847-555-0121. Email kate.mccallister@family-mutual.example.
Driver's license D6612904. Social Security number 421-88-7765.

Summary: the family left for Paris on December 23 and left one child, Kevin, age 8, at home
"by accident". The house was then visited twice by two men, Harry Lime and Marv Murchins.

Damage claimed:
- Broken staircase, ice and paint: $3,140.00
- One iron, one tarantula, one blowtorch, "found not where they were put": $780.50
- Neighbour's paint-splashed car: $2,400.00
- Plane tickets, nine, change fee: $1,260.00

The policyholders also ask whether leaving a minor child at home counts as an accident, a hazard
or a decision. The adjuster, Ms. Talbot, has no answer.

Pay to account 8812-440-9027. Kevin's pediatric records: asthma, mild.`,
  },
  {
    title: 'Nakatomi Plaza security incident report',
    text: `SECURITY INCIDENT REPORT - INTERNAL USE ONLY
Nakatomi Trading Corporation, Century City, CA 90067. Report SEC-1988-1224.
Prepared December 24, 2026 by Takagi Joseph, Head of Operations.

Persons involved: John McClane, visiting from New York, NY 10001, phone 212-555-0183, email
jmcclane@nypd-visitor.example, date of birth April 19, 1955. Also Hans Gruber, claiming to be a
caterer, and Ellis Hobbs, a colleague of Ms. Genero.

Summary: during the holiday party, a group of people seized the lobby. Mr. McClane, wearing no shoes,
is reported to have "changed their plans". Damage to the building includes 4 floors, 3 elevators,
a helicopter and a window.

Costs to date: $38,000,000.00 in property loss. Medical claims: broken glass in both feet, treated by
the paramedic on site, $2,640.00.

A personal note: Mr. McClane's marriage is under strain. Please pay compensation to account
5503-221-0846 and send a gift basket to Mrs. Holly Gennero-McClane.`,
  },
  {
    title: 'Kansas storm damage claim',
    text: `STORM DAMAGE CLAIM - PERSONAL INFORMATION
Emerald Plains Insurance, Wamego Office. Claim OZ-1939-0926. Filed September 26, 2026.

Policyholder: Henry Gale, Rural Route 3, Wamego, KS 66547. Phone 785-555-0108.
Email henry.gale@kansas-farm.example. Policy POL-39-KAN-004.

Loss: one farmhouse, lifted off its foundation during a storm and set down "in another place."
It landed on a person, who has not made a claim. Occupants: Dorothy Gale, age 12, and her dog Toto.

Items claimed:
- Farmhouse and contents: $18,400.00
- Four fence posts, one scarecrow, "left in the field": $210.00
- Travel costs, by tornado, one way: $0.00 (not covered)

Medical note: Miss Gale reports vivid dreams and a conviction that she met a lion. Dr. Auntie Em
Gale asks that this be treated as concussion.

The claimant will be a few hours from the farm. Contact Aunt Emily Gale at 785-555-0111.
Pay the settlement to account 3350-119-4472 by Friday, November 6, 2026.`,
  },
  {
    title: 'White Star Line refund request',
    text: `PASSENGER REFUND REQUEST - CONFIDENTIAL
White Star Line, Customer Accounts. Request WS-1912-0415. Received April 15, 2026.

Passenger: Rose DeWitt Bukater, born April 18, 1894. Home: 12 Beacon Hill, Boston, MA 02108.
Phone 617-555-0151. Email rose.bukater@bostonsociety.example. Passport number 884231907.

Ticket number 17582, first class. Fare paid: $4,350.00. The passenger requests a full refund of the
fare and a further $6,900.00 for lost luggage, one painting and one very large necklace.

Companion: Jack Dawson, third class, ticket 1124, $18.00, won in a card game.

The passenger also reports "an iceberg" and asks whether the company has considered a warning
system. Her fiance, Mr. Caledon Hockley, asks that any reply be sent to his lawyer, Mr. Lovejoy.

Medical note: mild hypothermia, treated aboard the rescue ship, no lasting effects.

Please send the refund to account 5524-380-1912. The company regrets that the vessel is not
available for inspection.`,
  },
  {
    title: 'Fighter Weapons School disciplinary file',
    text: `DISCIPLINARY AND MEDICAL FILE - COMMANDING OFFICER ONLY
Naval Fighter Weapons School, Miramar, CA 92145. File TG-1986-0516. Opened May 16, 2026.

Student: Lieutenant Pete Mitchell, call sign "Maverick". Date of birth July 3, 1962.
Social Security number 531-44-7021. Phone 858-555-0132. Email pmitchell@navy-school.example.
Radar intercept officer: Nick Bradshaw.

Incident summary: three low passes over the control tower, one inverted flight past a colleague,
and an unauthorised helicopter to a love interest, Charlotte Blackwood.

Cost of aircraft hours: $187,400.00. Fine for the control tower coffee: $64.25.

Medical: mild stress and trouble sleeping. Dr. Iceman Kazansky notes the student is overconfident
and has recommended a rest period. Instructor Viper has asked for this to stay confidential.

A request for transfer to the east coast was denied. Pay all damages to account
7740-318-2096. Contact the school at 619-555-0140.`,
  },
  {
    title: 'Duloc zoning complaint file',
    text: `ZONING AND PROPERTY COMPLAINT - PUBLIC RECORD COPY
Kingdom of Duloc, Planning Office. Complaint ZC-2001-0518. Filed May 18, 2026.

Complainant: Lord Farquaad, 1 Castle Road, Duloc, FL 32801. Phone 407-555-0192.
Email farquaad@duloc-city.example. Height recorded as "adequate".

Property in question: a swamp at 14 Marsh Lane, held by Mr. Shrek, born "a long time ago".
Occupant details: Princess Fiona, a Donkey, three blind mice, and "a gingerbread man, who was
not consulted".

Complaints:
- Unlicensed ogre on a protected wetland
- Excess noise, onion smell and one swamp-side karaoke night
- Several fairy-tale creatures resettled without a permit

Fine levied: $12,500.00. Shrek has offered $300.00 and a loaf of bread.

Please send correspondence to Shrek c/o shrek@swamp-mail.example or 407-555-0104.
Payment to account 6615-882-7013. The planning office asks that the next ogre arrive in a
vehicle with a permit.`,
  },
  {
    title: 'Davis household moving inventory',
    text: `HOUSEHOLD MOVING INVENTORY - PERSONAL INFORMATION
Pizza Planet Movers, Emeryville, CA 94608. Job MV-1995-0301. Dated March 1, 2026.

Customer: Mrs. Davis, 1234 Elm Street, Emeryville, CA 94608. Phone 510-555-0122.
Email davis.family@toybox-mail.example. Child: Andy Davis, age 6, birth date June 21, 2020.

Inventory, as recorded by the mover, Mr. Whistler:
- One cowboy figure, sheriff, hat attached: $42.00
- One space ranger, wings, battery warning: $64.99
- One dinosaur, nervous: $18.50
- One potato-shaped toy, interchangeable parts: $9.99
- One piggy bank, fragile, full of cash: $14.00

Special instructions: do not pack any of the above in the box labelled "Garage Sale". Several items
have been reported as "moving on their own", and one has asked to be addressed by the name Woody.

A neighbour, Sid Phillips, has been reported for aggressive handling of toys.

Moving fee: $1,860.00. Pay to account 4409-731-0285.`,
  },
  {
    title: 'Wallaby Way dental patient file',
    text: `PATIENT FILE - DENTAL, CONFIDENTIAL
Sherman Dental Practice, 42 Wallaby Way, Sydney NSW 2000. File DP-2003-0530. Opened May 30, 2026.

Patient: Nemo Clownfish, age 6, born November 4, 2019. Parent: Marlin Clownfish, 14 Reef Drive,
Sydney NSW 2000. Phone 02-555-0147. Email marlin@reef-family.example.

Notes by P. Sherman, dentist:
- Left fin smaller than the right, congenital: noted, not billed
- One incident with a fish tank, with a bag and a bucket, three weeks ago
- Visit cost: $240.00, includes one sticker

Medical: the patient is "lucky". The father reports severe separation anxiety and has telephoned
the clinic 31 times. A friend, Dory Blue, has short-term memory loss and was asked to wait outside.

Insurance: policy POL-03-REE-922. Payments to account 2230-844-1709.

A reminder to staff: keep the tank away from the street. Patients have been known to leave
through the drain.`,
  },
  {
    title: 'Wasteland fuel and vehicle registration',
    text: `VEHICLE REGISTRATION AND FUEL ALLOCATION - CONFIDENTIAL
Citadel Transport Authority. File FR-2015-0515. Issued May 15, 2026.

Registrant: Max Rockatansky, last known address 14 Bartertown Road, Adelaide SA 5000.
Phone 08-555-0161. Email max@wasteland-road.example. Date of birth March 21, 1979.
Licence number D8841260.

Vehicle: V8 Interceptor, black, licence plate 3MAX977, VIN 1FTEW1E50JKD11204.
Modifications: "a few". Fuel allocation: 40 litres a month, current balance "none".

Fines and charges:
- Riding without a permit: $1,200.00
- One tanker, borrowed and not returned: $64,000.00
- Damage to a bridge, a gate and a bus: $22,850.00

Passengers: Imperator Furiosa and five wives, claiming protection of the transport authority. Also
Immortan Joe's lawyers, who dispute all of the above.

Medical: recurring headaches, post-traumatic stress. Pay fines to account 5529-170-2216.

Escorts on the road are advised not to use the word "ride" in any application.`,
  },
  {
    title: 'Athletic Commission licence review',
    text: `BOXING LICENCE REVIEW - CONFIDENTIAL
Pennsylvania Athletic Commission, Philadelphia, PA 19103. File AC-1976-0125. Dated January 25, 2026.

Applicant: Rocky Balboa, 1818 East Passyunk Avenue, Philadelphia, PA 19148. Date of birth July 6, 1945.
Social Security number 213-56-8841. Phone 215-555-0117. Email rocky@philly-gym.example.

Manager: Mickey Goldmill, of Mighty Mick's Gym. Opponent: Apollo Creed. Spouse: Adrian Pennino.

Earnings, last fight: $150,000.00. Purse for the rematch: $35,000.00. Cost of raw eggs, 96, claimed
as a training expense: $38.40.

Medical: the applicant has reduced vision in one eye, a thickened nose and a mild stutter, reviewed
by Dr. Cappadonna. The commission asks that the applicant not run up the museum steps without a permit.

Training location: a slaughterhouse, "unregulated". Pay the fine to account 6628-014-3375.
The commission has received a number of letters about the pet turtles.`,
  },
  {
    title: 'Shermer High attendance office record',
    text: `ATTENDANCE OFFICE RECORD - STUDENT PRIVACY ACT
Shermer High School, Shermer, IL 60062. File AT-1986-0606. Reviewed June 6, 2026 by Mr. Edward Rooney, Dean.

Student: Ferris Bueller, age 17, born June 11, 2008. Home: 4160 Sycamore Lane, Shermer, IL 60062.
Phone 847-555-0136. Email ferris@shermer-high.example. Parents: Tom and Katie Bueller.

Absences: nine days this semester. Reasons given: "illness" (seven), "a grave illness" (one),
"a parade" (one).

Documents on file: one doctor's note, forged; one parent's phone call, voice suspicious.

Friend: Cameron Frye, age 17, parent contact 847-555-0140. Girlfriend: Sloane Peterson,
reported absent for "a death in the family".

Medical note: the student says he has a heart condition. The nurse's file says he does not.

Fines: $28.00 for a missed locker. Pay to account 7794-663-2051. Mr. Rooney has asked for a
vehicle to be towed. He has been advised against it.`,
  },
  {
    title: 'Florin castle vendor agreement',
    text: `VENDOR AGREEMENT - ROYAL WEDDING - CONFIDENTIAL
Kingdom of Florin, Office of the Crown Prince. Agreement RW-1987-1010. Dated October 10, 2026.

Parties: Prince Humperdinck, 1 Castle Hill, Florin City, ON K1A 0B1; and Miracle Max,
sole trader, 14 Thieves Forest Road, Florin City. Phone 613-555-0134.
Email max@miracle-pills.example. Business number 81234 5678 RT0001.

Services: one resurrection, partial, at $1,500.00 deposit and $3,500.00 on delivery. One pill,
chocolate coated, "to make it go down". One Fire Swamp tour: $780.00.

Bride: Princess Buttercup. Her bodyguard: Westley, also known as a masked pirate. A man named
Inigo Montoya is owed one revenge.

Medical: the vendor reports that the patient was barely alive. His wife, Valerie, disputes this.

Please pay to account 4403-218-5509. Delays beyond ten days will be treated as a breach.`,
  },
  {
    title: 'Round Table expense claim',
    text: `KNIGHTLY EXPENSE CLAIM - CONFIDENTIAL
Camelot Treasury, Accounts. Claim KC-0932-0501. Filed May 1, 2026 by King Arthur of the Britons.

Claimants: Sir Lancelot, Sir Galahad, Sir Robin, Sir Bedevere and Patsy, servant. Addresses: all
c/o the Round Table, Camelot, GL1 1AA. Phone 020-555-0172. Email knights@camelot-court.example.

Items claimed:
- Two coconuts, used as a stand-in for a horse: $4.50
- One wooden rabbit, large, for an assault: $6,400.00
- One shrubbery, requested by a knight: $90.00
- Retreat, quick, Sir Robin: $15.00

Quest: to find a grail. Outcome: partial. Sir Lancelot reports a minor injury to a limb.
The Black Knight reports he is "fine", and has fewer limbs than before.

A taunting by French guards has been logged under insurance claim IC-0932-017. Please pay to
account 3326-540-0932.

The treasury asks that the next quest begin with a map.`,
  },
  {
    title: 'Lebowski rug damage claim',
    text: `HOME CONTENTS INSURANCE CLAIM - PERSONAL INFORMATION
Venice Beach Mutual. Claim HC-1998-0306. Filed March 6, 2026.

Policyholder: Jeffrey Lebowski, 5227 Doheny Road, Los Angeles, CA 90069. Phone 310-555-0144.
Email dude@lebowski-bowling.example. Driver's license D7712058. Date of birth August 18, 1962.

Item damaged: one rug, of great sentimental value. Value declared: $1,250.00. Value claimed:
$17,500.00. Damage: a stranger, a situation, and a beverage.

Others involved: Walter Sobchak, who "was shouting"; Donny Kerabatsos, who "was out of his
element"; the other Jeffrey Lebowski, a wealthy man of the same name, who disputes the claim.

Medical: the policyholder reports a sore back and a regular intake of white Russians.
Dr. Jackie Treehorn has declined to comment.

Please pay the claim to account 5501-846-3306. The adjuster has asked everyone to stop shouting
in the office.`,
  },
  {
    title: 'WPBH payroll and absence record',
    text: `PAYROLL AND ABSENCE RECORD - STAFF ONLY
WPBH Television, Pittsburgh, PA 15201. Record PR-1993-0202. Reviewed February 2, 2026.

Employee: Phil Connors, weatherman. Social Security number 417-52-9930. Date of birth
February 2, 1960. Home 14 Main Street, Punxsutawney, PA 15767. Phone 814-555-0129.
Email phil.connors@wpbh-news.example.

Producer: Rita Hanson. Camera operator: Larry Chesterton. Annual salary: $82,500.00.

Attendance: the employee has reported for work on February 2 over and over. The payroll office
records one day only, but pay has been issued 312 times: $77,240.00 in overpayments.

Notes: the employee has been seen in a bar, a diner, a bowling alley and one groundhog's car.
He has also learned the piano and ice sculpture. Dr. Ned Ryerson has been sighted twice.

Medical: the employee reports persistent deja vu. Insurance: policy POL-93-WEA-202.
Recover overpayments to account 7723-411-0202. Please do not rehire him on February 3.`,
  },
];
