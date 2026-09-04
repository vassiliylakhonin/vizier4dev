# The programme file

Vizier4Dev opens on a fictional action. A consortium reporting a real period
loads a programme file instead, from **Data → Load a programme file**, and gets
the same rules engine over its own framework, budget, partners and cost lines.

Nothing is uploaded. The file is read in the browser, the working period is kept
in that browser's local storage, and what leaves is what you export.

Start from **Data → Download this one as a template**: it writes the demo out as
a valid programme file. Replace its content with yours and load it back.

## What a file replaces, and what it drops

A programme file carries **data**: sources, indicators, donor rules, budget,
partners, cost lines, the partner return template, the narrative skeleton.

It does not carry **staging** — the demo's scripted moments: the pre-filled
draft, the source conflict between two of its own files, the other partners'
returns already sitting on file, the canned review, the worked findings, the
funding pipeline, the six answered questions. Those are fiction and a loaded
programme drops them. The screens that showed them then say what is missing
instead of inventing a figure.

That is the difference the demo cannot show you: on real data, the parts that
are actually computed keep working, and the parts that were staged go quiet.

## Shape

```json
{
  "schema": "vizier4dev/programme@1",
  "id": "wp-phase-2",
  "title": "Rural Water Points — Phase II",
  "line": {"en": "€1.2M · EBRD · 3-partner consortium · Q2", "ru": "…"},
  "period": {"from": "2026-04-01", "to": "2026-06-30", "label": "Q2 2026"},
  "me": "Aral Water NGO",
  "partners": ["Aral Water NGO", "Oblast Vodokanal", "Steppe Engineering LLP"],
  "procurementThreshold": 8000,
  "sources": {"ga": {"name": "Grant agreement.pdf", "type": "PDF", "size": "900 KB", "text": "…"}},
  "indicators": [...], "rules": [...], "budget": [...],
  "coreIndicators": [...], "mapping": {...}, "silo": {...},
  "costs": [...], "template": {...}, "narrative": {...},
  "learningQuestions": [...]
}
```

`me` is the partner whose desk you are sitting at, and must be one of
`partners`. `procurementThreshold` is the euro figure above which a procurement
needs a comparison of offers, from your own grant agreement.

`sources` is a map of id → document. The id is what a figure's trace points at,
so keep ids stable across periods. A trace to a document this file does not
carry degrades to plain text rather than a button that opens nothing.

## Indicators: how a consortium figure is built

The donor decides how partner returns combine, so each indicator says it:

```json
{"code": "W1", "label": "Water points rehabilitated", "unit": "points",
 "base": "0", "target": "120", "lead": "SE",
 "need": "Count + commissioning sign-off", "anchor": "W1 - Water points rehabilitated",
 "agg": {"type": "sum", "field": "Points commissioned"}}
```

| `agg.type` | What it does |
|---|---|
| `sum` | Adds `field` across every partner return. |
| `ratio` | Sums `num` and `den` separately, then divides. Never the mean of the partners' own rates. |
| `none` | Not built from returns. Give a `note` saying where the figure comes from; the cell stays empty until it does. |

Omit `agg` and the indicator reports no consortium value. That is a visible
"incomplete" flag on the consolidated report, not a silent zero.

## Template: the checks a section carries

Required fields, and a numerator larger than its denominator, are checked
everywhere. Three more checks are declared by the section that needs them:

```json
{"ind": "OP3.1", "title": "…", "why": "…", "anchor": "…",
 "reconcile": {"total": "Total certified (in-period)", "parts": ["Female", "Male"], "tol": 1},
 "floor": {"field": "Female members (%)", "min": 40, "msg": "Below the 40% floor."},
 "expect": {"field": "Narrative / barriers noted", "minLen": 50,
            "words": ["outage", "spare", "supervis"], "topic": "what drives the gap"},
 "fields": [{"l": "Total certified (in-period)", "t": "number", "req": true}]}
```

- `reconcile` — a disaggregation that has to add up to its total, within `tol`.
- `floor` — an inclusion or quality floor from the results framework.
- `expect` — a narrative field that has to be long enough and address the topic.

Field types (`t`): `number`, `percent`, `text`, `longtext`, `select`, `file`.

## Eligibility: what makes a cost ineligible beyond a missing document

Missing evidence and the procurement threshold are checked from the fields every
cost line already carries. Four further findings need rules only the grant
agreement can set, so they are declared:

```json
"eligibility": {
  "reportingCurrency": "EUR",
  "fxSource": "the central bank reference rate for the month of payment",
  "fxRates": {"KGS": 0.0102},
  "fxTolerance": 0.02,
  "indirectRate": 0.05,
  "ineligiblePayrollComponents": ["provision", "indirect overhead"],
  "errorTaxonomy": null
}
```

The cost lines opt into them:

| Field on a cost line | Raises |
|---|---|
| `"local": {"cur": "KGS", "amt": 1360000, "rate": 0.0105}` | The applied rate against `fxRates`, beyond `fxTolerance`. The finding names the euro difference, which is the part that is not eligible. |
| `"t": "advance", "cleared": false` | An advance declared before it was cleared — money moved, not expenditure incurred. |
| `"components": ["salary", "provision"]` | Any component named in `ineligiblePayrollComponents`, whatever the payroll record shows. |
| `"indirect": true, "sub": true` | A sub-implementer's overhead declared as a direct cost on top of `indirectRate`. Auditors record this as cascading. |

A currency used by a cost line with no rate in `fxRates` is a refusal, not a
silent pass: the conversion cannot be checked, so the file is rejected.

### errorTaxonomy

Optional, and `null` for most programmes. When a donor publishes a breakdown of
what its own auditors find, put it here and the financial screen shows which
categories this period's rules can raise a finding in:

```json
"errorTaxonomy": {
  "source": "European Court of Auditors, Annual Report 2024, figure 27",
  "note": "Share of the estimated level of error by type.",
  "rows": [{"key": "ineligible-cost", "share": 32, "label": "Ineligible costs"}]
}
```

`key` matches the `basis` a check carries: `ineligible-cost`, `procurement`,
`missing-docs`, `ineligible-project`, `not-incurred`, `arithmetic`. The panel
reports what the rules *can* raise, never a detection rate, and it counts
`procurement` apart because a threshold is a signal and not a judgement on the
procedure. Declare no taxonomy and the panel does not render — a programme never
borrows another donor's figures.

## The partner return, as a file

The two sides of the boundary are two copies of this page in two organisations.
A partner exports what it would send — and can read the whole file before it
goes. The lead imports it and can say what arrived and what it weighed. Nothing
passes through a server.

**Export my return** (partner boundary, or Data) writes
`vizier4dev/return@1`: the figures the donor form asks for, each local check in
one of four fixed words, and a digest binding each figure to the evidence it was
checked against. The evidence itself is not in it.

```json
{
  "schema": "vizier4dev/return@1",
  "programme": {"id": "wp-phase-2", "title": "Rural Water Points — Phase II"},
  "period": {"from": "2026-04-01", "to": "2026-06-30", "label": "Q2 2026"},
  "partner": "Oblast Vodokanal", "short": "OV", "round": 1,
  "sections": [{
    "ind": "W1",
    "figures": {"Points commissioned": "41", "Means of verification": "…"},
    "checks": [{"id": "required", "ask": "…", "attested": false, "status": "MET"}],
    "evidence": {"held_by": "OV", "documents": 3, "digest": "75f818a0d47315ed"}
  }],
  "costs": null
}
```

`examples/partner-return-oblast-vodokanal.json` is a worked one for
`examples/rural-water-points.json`: load the programme, then import the return.

### The checks a return carries

They are read off the return template, so a programme with different indicators
still sends verdicts rather than silence:

| Raised when the section declares | Check |
|---|---|
| any `req` field | `required` — every required field is filled |
| a numerator and a denominator field | `ratio`, `ratio_sane` |
| `reconcile` | `reconciliation` |
| `floor` | `floor` |
| `expect` | `narrative` |

A section may also declare checks a machine cannot settle. Those cross as the
partner's own attestation, labelled as one, and `appliesTo` names the partners
it is asked of:

```json
"localChecks": [{
  "id": "deduplication",
  "ask": "Attendance deduplicated to certified people",
  "appliesTo": ["Riverbend Community Care"],
  "status": "MET"
}]
```

A status is always one of `MET`, `NOT_MET`, `UNKNOWN`, `NOT_APPLICABLE` — fixed
words, so there is nothing for prose to soften on the way out.

### What the lead does with it

A received return is checked before it is believed, and refused whole otherwise:
the right programme id, the right period label, a partner this action has and
not yourself, indicators this framework defines, statuses in the four words, and
a well-formed digest. The figures then feed consolidation like any other
partner's, and the verdicts shown are the ones that partner made — the lead
never had the evidence to decide them and does not recompute them.

A partner that did not describe what it holds still appears, and the screen says
so rather than implying it sent nothing.

## Refusals

A file is validated before anything changes, and a bad one changes nothing. The
messages name the field:

```
period.label: required, must be a non-empty string.
costs[0].h: "No Such Heading" is not a budget heading in this file.
template.sections[0].ind: "NOPE" is not an indicator in this file.
mapping.W1: "EB-99" is not a core indicator in this file.
costs[3].local.cur: "UZS" has no rate in eligibility.fxRates, so the conversion cannot be checked.
eligibility.errorTaxonomy.source: required — a published breakdown has to say whose it is.
```

A partner return is refused the same way:

```
programme.id: this return was prepared for "someone-else", and the loaded programme is "wp-phase-2".
period.label: this return covers "Q3 2026", and the open period is "Q2 2026".
partner: this is your own return. Import the ones that came from the other partners.
sections[0].checks[0].status: "PROBABLY" is not one of MET, NOT_MET, UNKNOWN, NOT_APPLICABLE.
sections[0].evidence.digest: a 16-character hex digest is required — without it the figure is not bound to anything.
```

## The period, and getting it out

The working period — what partners filed, what the local checks said, what was
approved, the trail of who changed what — is saved in this browser after every
change and restored on reload. It is not an account and not a backup: a
different browser, a cleared cache or a private window has nothing in it.

**Data → Export the period package** writes it out as
`vizier4dev/period@1`: figures, local verdicts, approvals, comments, cost
lines, indicator mapping, narrative, what crossed the partner boundary, and the
ledger. Source documents are not in it — they stay with the partner holding
them.

**Data → Clear saved work** discards the period and returns to the demo.

## Limits worth knowing before a pilot

- One period at a time. Loading a programme starts a fresh period; there is no
  history and no comparison across quarters.
- One browser. No accounts, no sharing, no concurrent editing. Two people
  working the same period exchange exported files.
- The donor hand-over encodes and assembles, but does not submit anything.
