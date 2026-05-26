# Docs Deployment Preflight

Status: pass with review warnings.

Round: 363.

This preflight checks whether the local docs-site is ready for a future manual
deployment decision. It does not deploy a site, write a public URL, enable
analytics, upload files, or change GitHub Pages settings.

## Inputs

- `docs-site/nav.yaml`
- `docs-site/site_manifest.yaml`
- `docs-site/pages/`
- `docs-site/dist/`
- `docs-site/dist_manifest.yaml`
- `docs-site/deployment_dry_run_report.md`
- `docs/docs-deployment-strategy.md`
- `docs/github-pages-deployment-plan.md`

## Required Checks

| Check | Result | Notes |
| --- | --- | --- |
| `nav.yaml` valid | pass | nav entries match required sections |
| index page exists | pass | `docs-site/pages/index.md` |
| quickstart page exists | pass | `docs-site/pages/quickstart.md` |
| original parity page exists | pass | `docs-site/pages/original-repo-parity.md` |
| public demo page exists | pass | `docs-site/pages/public-demo.md` |
| security/privacy page exists | pass | `docs-site/pages/privacy.md` |
| broken links | pass | 0 broken local links |
| missing pages | pass | 0 missing nav pages |
| missing source docs | pass | 0 missing source docs |
| orphan pages | warning | 16 support pages are intentionally outside public nav |
| private paths | pass | 0 hits in docs-site nav/pages |
| secrets | pass | no token-like committed values in preflight surface |
| raw data | pass | no raw data markers in preflight surface |
| fake deployment URL | pass | dry-run records `public_url: none` |

## Preflight Decision

Decision: `PASS WITH REVIEW WARNINGS`.

The docs-site is ready for manual deployment review. It is not deployed, and a
human must review the generated static output before any real publication.

## Review Warning

The orphan page count is expected. The public nav was narrowed to the external
visitor path while older support pages remain in `docs-site/pages/` for local
review and future docs work.

## Safety Boundary

- no public deployment;
- no real public URL;
- no analytics;
- no private file upload;
- no secrets;
- no raw data;
- no restricted model payloads;
- no ARIS implementation.
