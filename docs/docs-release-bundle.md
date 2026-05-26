# Docs Release Bundle

Status: ready for human review.

Round: 365.

This document describes the local docs release bundle generated for manual
inspection or future manual deployment. It does not publish a site, enable
GitHub Pages, upload files, write a real public URL, or enable analytics.

## Bundle Location

- Bundle root: `docs-site/release_bundle/`
- Bundle manifest: `docs-site/release_bundle_manifest.yaml`
- Bundle report: `docs-site/release_bundle_report.md`

## Bundle Contents

The bundle includes:

- static HTML pages from `docs-site/dist/`;
- `site.css`;
- `nav.yaml`;
- `site_manifest.yaml`;
- `dist_manifest.yaml`;
- `preflight_report.md`;
- `deployment_dry_run_report.md`;
- a release-bundle manifest with size and SHA-256 hash for every included
  file.

## Safety Requirements

The bundle is intended to remain public-safe:

- no secrets;
- no private paths;
- no raw data;
- no restricted model payloads;
- no fake public URL;
- no analytics;
- no live network;
- no automatic deployment.

## Review Requirement

Human review is required before any future manual deployment. The bundle is a
review artifact, not proof that public hosting happened.

## Validation

Run:

```powershell
python -m pytest tests/workflow/test_docs_release_bundle.py -q
```
