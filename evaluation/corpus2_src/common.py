"""Ordinary words that were reviewed once and are never sensitive on their own.

A leftover capitalised token whose lower-case form is listed here is recorded
in the document key under reviewed_not_sensitive. Deliberately NOT listed:
month names, and any word that doubles as a personal name, surname, bank or
place (will, grant, mark, bill, rose, hope, grace, chase, wells, ...). Those
must be reviewed document by document (the `ok` list of the document).
Two-letter ALL-CAPS tokens (IN, OR, ME, PA, ON ...) are never accepted from
this list because they can be state or province abbreviations.
"""

_WORDS = """
a an the this that these those there here it its i we you he she they them his her hers their our ours my your yours
me us him who whom whose which what when where why how
if in on at by for from to with per as and but or nor not no yes all any each every both either neither some none
of off out over under up down into onto upon about above below between within without against during before after
since until while once also then than so such same other another only just still already again
is are was were be been being am has have had having do does did done can could should would shall must might
please thank thanks dear hello hi hey sincerely regards best kind warm respectfully cordially yours truly cheers
re fw fwd subject date dated time from to cc bcc attn attention via enclosure enclosures encl attachment attachments
note notes notice memo memorandum summary overview background purpose scope status update updates action actions item items
total totals subtotal balance amount amounts due paid unpaid payment payments fee fees charge charges credit credits debit debits
name names address addresses phone telephone tel email e-mail fax mobile cell office home work contact contacts
number numbers no id code type description details detail reference ref file files matter case client clients customer
account accounts invoice invoices statement statements receipt receipts check cheque wire transfer deposit withdrawal
section sections article exhibit exhibits schedule schedules appendix attachment form forms line lines part parts box
page pages paragraph item table column row sheet tab figure
first second third fourth fifth sixth seventh eighth ninth tenth last next previous prior current new old
monday tuesday wednesday thursday friday saturday sunday mon tue tues wed thu thur thurs fri sat sun
today tomorrow yesterday tonight morning afternoon evening noon midnight week weeks month months year years day days hour hours
am pm a.m p.m est edt cst cdt mst mdt pst pdt et ct mt pt utc gmt bst cet
mr mrs ms miss mx dr prof hon esq jr sr md do rn np pa cpa ea jd phd dds dmd lcsw lpn cna pt ot
inc llc llp ltd corp co plc pc pllc lp
confidential privileged draft final copy original duplicate urgent important private internal personal
attorney attorneys lawyer counsel paralegal firm court courts judge clerk plaintiff plaintiffs defendant defendants
petitioner respondent claimant applicant appellant appellee party parties witness witnesses agreement agreements contract
employer employee employees company companies corporation partnership partner partners member members manager director
officer officers president secretary treasurer trustee trustees executor executrix administrator beneficiary beneficiaries
guardian parent parents child children minor minors spouse husband wife mother father son daughter sister brother
patient patients provider providers physician doctor nurse clinic hospital pharmacy pharmacist insurance insurer insured
policy policies claim claims coverage plan plans benefit benefits premium deductible copay coinsurance
tax taxes taxpayer taxpayers return returns income expense expenses revenue wages salary payroll withholding refund
federal state county city town province provincial national local municipal district department division office bureau agency
bank banking branch credit card cards visa mastercard amex discover debit
signature signed sign print printed title dated witness notary sworn
yes no n/a na tbd tba ok okay none unknown pending approved denied complete completed open closed active inactive
see seen review reviewed prepared received sent called left spoke met asked told said advised confirmed
need needs needed want wants let make made get got take took give gave send keep kept use used using
call calls ask tell bring provide include includes including attach attached enclosed
question questions answer answers response responses reply request requests requested
start end begin began ending beginning effective expires expiration expiry term terms termination
service services product products order orders delivery shipping billing terms conditions
general specific additional other others various certain
one two three four five six seven eight nine ten eleven twelve twenty thirty forty fifty sixty hundred thousand million
usd cad gbp eur
whereas now therefore witnesseth hereby herein hereto thereof further furthermore however although though because
unless except provided notwithstanding accordingly otherwise meanwhile finally lastly additionally
his/her he/she and/or
todo fyi asap eod cob ps p.s nb
subtotal grand net gross
privileged work product
step steps task tasks list lists checklist
history plan assessment impression diagnosis diagnoses medication medications allergies allergy vitals
results result test tests lab labs normal abnormal high low range units value flag
instructions follow-up followup follow appointment appointments visit visits
information info data record records document documents report reports
required optional mandatory
signature date initials
ssn ein dob tin itin npi mrn vin ach aba iban swift bic pin cvv cvc zip hipaa phi pdf faq url
irs ssa dmv uscis cra hmrc eeoc osha medicare medicaid
"""

# Clock times (10:30, 09:14:00, 2:15pm) are never keyed and are accepted as reviewed.
TIME_RE = r"\d{1,2}:\d{2}(?::\d{2})?(?:[ap]\.?m\.?)?"

COMMON = frozenset(_WORDS.split())
