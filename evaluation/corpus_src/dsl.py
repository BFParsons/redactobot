"""Tiny authoring helpers for corpus document definitions.

A batch module defines DOCS = [D(...), D(...), ...].

Inline markup inside any document text (body, email headers, table cells,
spreadsheet string cells):

    [[value|TAG]]            or            [[value|TAG|why]]

TAG for names:   p1:full   o2:short   p3:surname!   p1:caps:caption name
                 (entity id, variant, optional "!" = hard, optional subtype)
TAG for others:  cat   cat:subtype   cat!:subtype     ("!" = hard)

Category aliases are listed in generate.py (ALIAS).
"""


def D(id, fmt, doc_type, audience, jur, **kw):
    d = dict(id=id, fmt=fmt, doc_type=doc_type, audience=audience, jur=jur)
    d.update(kw)
    return d


def dt(iso, fmt="mm/dd/yyyy", tag="date"):
    """Real spreadsheet date cell. iso='1961-03-14'. tag e.g. 'dob', 'date:hire date'."""
    return ("date", iso, fmt, tag)


def amt(value, fmt="usd", tag="money"):
    """Real spreadsheet currency/number cell. fmt: usd, usd0, acct, num, numacct, cad, gbp, eur."""
    return ("amt", value, fmt, tag)


def num(value, tag):
    """Sensitive value stored as a plain number cell (e.g. an account number typed as a number)."""
    return ("num", value, "General", tag)
