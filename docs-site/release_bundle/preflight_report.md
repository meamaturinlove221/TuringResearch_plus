# Docs Site Deployment Preflight Report

Status: pass with review warnings.

Round: 363.

Deployment performed: `false`.
Public URL: `none`.
Requires human review: `true`.

## Summary

- Build status: `pass_with_warnings`.
- Checked pages: 11.
- Checked source docs: 41.
- Generated files: 12.
- Missing pages: 0.
- Broken links: 0.
- Missing source docs: 0.
- Orphan pages: 16.
- Private path hits: 0.
- Secrets: 0 known committed-token hits in scoped preflight surface.
- Raw data: 0 scoped hits.
- Fake deployment URL: 0 scoped hits.

## Required Public Pages

| Page | Status |
| --- | --- |
| `pages/index.md` | present |
| `pages/quickstart.md` | present |
| `pages/original-repo-parity.md` | present |
| `pages/public-demo.md` | present |
| `pages/privacy.md` | present |

## Findings

### Broken Links

- none

### Missing Pages

- none

### Missing Source Docs

- none

### Orphan Pages

- 16 docs-site support pages are outside public nav and require human review if
  included in a future public nav.

### Safety Hits

- private paths: none
- secrets: none
- raw data: none
- fake deployment URL: none

## Decision

`PASS WITH REVIEW WARNINGS`

The docs-site is ready for future manual deployment review. This report does
not deploy anything.
