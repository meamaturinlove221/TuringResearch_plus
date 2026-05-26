# Docs Deployment Blockers

Status: no blocking issues found.

Round: 363.

This file records the deployment blockers checked during the v1.6 docs
deployment preflight. It is a preflight report, not a deployment approval.

## Blocking Checks

| Blocker | Status | Evidence |
| --- | --- | --- |
| invalid nav | clear | `docs-site/nav.yaml` validates against `docs-site/site_manifest.yaml` |
| missing index page | clear | `docs-site/pages/index.md` exists |
| missing quickstart page | clear | `docs-site/pages/quickstart.md` exists |
| missing original parity page | clear | `docs-site/pages/original-repo-parity.md` exists |
| missing public demo page | clear | `docs-site/pages/public-demo.md` exists |
| missing security/privacy page | clear | `docs-site/pages/privacy.md` exists |
| broken local links | clear | 0 broken links |
| missing source docs | clear | 0 missing source docs |
| private paths | clear | 0 private path hits |
| secrets | clear | scoped preflight scan clean |
| raw data | clear | scoped preflight scan clean |
| fake deployment URL | clear | `public_url: none` |

## Non-blocking Warnings

- 16 orphan docs-site support pages are not in the public navigation.

These pages are not release blockers because they are retained as local support
pages and are not part of the public nav path.

## No-go Conditions

Deployment must remain blocked if any future preflight finds:

- missing public-nav pages;
- broken local links;
- missing source docs;
- private paths;
- secrets or API key values;
- raw data;
- restricted model payloads;
- fake or unverified deployment URL;
- analytics enabled without approval;
- fake/demo output described as observed evidence.
