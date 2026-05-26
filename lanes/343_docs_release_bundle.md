# Round 365 - Docs Release Bundle

Status: completed.

## Objective

Generate a docs release bundle for human inspection or future manual
deployment. This round does not publish the bundle.

## Files

- `docs-site/release_bundle/`
- `docs-site/release_bundle_manifest.yaml`
- `docs-site/release_bundle_report.md`
- `docs/docs-release-bundle.md`
- `tests/workflow/test_docs_release_bundle.py`
- `lanes/343_docs_release_bundle.md`
- `lanes/00_master_ledger.md`

## Bundle Contents

- Static HTML from `docs-site/dist/`.
- `site.css`.
- `nav.yaml`.
- `site_manifest.yaml`.
- `dist_manifest.yaml`.
- `preflight_report.md`.
- `deployment_dry_run_report.md`.
- Hash report for every included file.

## Safety

- No public deployment.
- No fake public URL.
- No secrets.
- No private paths.
- No raw data.
- No restricted model payloads.
- No analytics.
- No live network.
- Human review required.
