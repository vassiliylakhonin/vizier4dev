# Vizier4Dev

**Trace reporting figures to sources, review partner returns, and prepare donor handover exports.**

[![Demo](https://img.shields.io/badge/Demo-Open_in_browser-blue.svg)](https://vizier4dev.pages.dev/)
[![CI](https://github.com/vassiliylakhonin/vizier4dev/actions/workflows/ci.yml/badge.svg)](https://github.com/vassiliylakhonin/vizier4dev/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A bilingual **English / Russian** browser prototype for quarterly reporting in grant-funded consortia. Explore indicator aggregation, cost rules, source references, and review gates in one local workflow. **No installation, account, or backend required.**

Status: working demo on fictional data, with no backend, accounts, customers, or pilot. Donor handover prepares exports; it submits nothing.

[Open the demo](https://vizier4dev.pages.dev/) · [Quick start](#quick-start) · [Load your own period](#load-your-own-period) · [Programme-file contract](docs/programme-file.md)

## Quick start

Open [index.html](index.html) in a browser, or use the hosted demo.

There is no build step or dependency installation. [landing.html](landing.html) is the public introduction.

### Try the hosted demo

1. [Open the demo](https://vizier4dev.pages.dev/) and choose English or Russian.
2. Inspect a fictional reporting period and follow a figure to its source reference.
3. Review indicator and cost findings, then inspect partner returns.
4. Follow the review gates and export the handover when its requirements are satisfied.

The result is a local export for review; nothing is submitted to a donor. Role switching is a workflow demonstration, not authenticated access.

### Load your own period

Use Data → Download this one as a template, edit the resulting programme file, then choose Data → Load a programme file. Review the [file contract](docs/programme-file.md) first.

Included worked files:

- [Rural water points](examples/rural-water-points.json)
- [Partner return](examples/partner-return-oblast-vodokanal.json)

Loading your own programme removes staged narratives, canned review, and demo findings. Missing information stays missing; the checks, aggregation, partner-return validation, and handover gates continue to operate on the actual file contents.

## Why this project exists

Reporting in grant-funded programmes often breaks down when figures, donor rules, and partner returns are not aligned. Vizier4Dev gives a lightweight browser-based workflow for reviewing that structure before a donor handoff.

It helps teams:

- trace reported figures back to source references
- check indicator and cost-eligibility rules
- review partner returns in a controlled local workflow
- prepare a donor export without exposing a real backend
- test a bilingual reporting flow in English and Russian

This is a prototype and a workflow demonstrator, not a production reporting system.

## What it does

The demo walks a fictional quarterly reporting period through four phases:

1. Framework and collection
2. Checks and rule validation
3. Partner returns
4. Review and handover

Role switching demonstrates the workflow in one browser. It does not authenticate a person or provide server-enforced access control.

## Data flow

```text
Programme file → indicators and cost checks → partner returns → review gates → local export
```

Programme files are read in the browser. The working period stays in browser local storage; partners exchange exported files. See the [file contract](docs/programme-file.md) for required fields and aggregation rules.

## Languages and limits

The interface supports English and Russian, with the selection remembered locally. Donor indicator codes, field labels, document contents, and partner names retain their source language.

The prototype supports one period in one browser. Partners exchange files; there is no shared workspace, concurrent editing, or quarterly history. The fictional demo illustrates rule handling, workflow logic, and review steps, not a live operational reporting environment.

No network APIs or external scripts are used by the workspace. Local storage is not a managed confidential-data service. Outputs require human review before donor filing and do not constitute legal or donor-certified submissions.

## What this is not

This project does not:

- provide a backend or multi-user reporting service
- authenticate real users or enforce access control
- connect to real donor systems or customer data
- produce operationally accepted reporting submissions
- replace human review, audit, or compliance decisions

## Development and deployment

```bash
python3 scripts/check_static.py
```

CI checks both pages, local links, the bilingual contract, absence of network APIs and external scripts, and response headers.

[deploy.sh](deploy.sh) validates and publishes only `index.html`, `landing.html`, `robots.txt`, and `_headers` to Cloudflare Pages. The [manual deployment workflow](.github/workflows/deploy.yml) updates the hosted site.

The hosted demo is publicly reachable by its address, although crawling is disallowed. Use fictional data for the public demo. The landing page includes founder and pricing drafts and personal contact details for demonstration only.

## Feedback and contributions

[Open an issue](https://github.com/vassiliylakhonin/vizier4dev/issues) with the language, workflow step, expected result, and a minimal fictional programme file. Useful contributions include reproducible rule cases, clearer bilingual labels, and accessibility fixes. Do not include confidential programme or partner data.

## License

[MIT license](LICENSE).
