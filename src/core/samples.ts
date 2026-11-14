/**
 * @license
 * Copyright 2026 The Redactobot Authors
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
];
