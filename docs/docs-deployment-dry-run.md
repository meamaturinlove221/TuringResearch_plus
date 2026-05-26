# Docs Deployment Dry-run

Status: completed.

Round: 335.

This round generated a deployable static docs package under `docs-site/dist/`
without publishing it. The dry-run is a local artifact for human review, not a
public deployment.

## Outputs

- `docs-site/dist/`
- `docs-site/dist_manifest.yaml`
- `docs-site/deployment_dry_run_report.md`

## What The Dry-run Confirms

- The docs-site can generate static HTML and CSS.
- The dist manifest records every page, asset kind, byte size, and SHA-256
  hash.
- The package is local-only and review-first.
- No public URL is written.
- No deployment is performed.
- No analytics are enabled.

## Safety Boundary

The dry-run must not contain:

- secrets;
- API keys;
- private paths;
- raw private data;
- restricted model payloads;
- fake deployment URLs;
- unsupported observed experiment claims.

## Human Review Before Publication

Before any future manual publication, a human should review:

1. `docs-site/dist_manifest.yaml`;
2. `docs-site/deployment_dry_run_report.md`;
3. generated HTML in `docs-site/dist/`;
4. docs-site navigation and source docs;
5. security/privacy gates.

The dry-run is **GitHub Pages-ready evidence**, not a GitHub Pages deployment.
