# GitHub Pages Workflow Draft

Status: dry-run workflow draft.

Round: 364.

This document describes `.github/workflows/docs-pages-dry-run.yml`. The
workflow is a manual dry-run draft for reviewing docs-site build readiness. It
does not deploy to GitHub Pages and does not enable Pages settings.

## Workflow Shape

- Trigger: `workflow_dispatch` only.
- Required input: `dry_run_only`, default `true`.
- Permissions: `contents: read`.
- Mode: fake/default and live-disabled.
- Build target: `docs-site/dist/` dry-run output and reports.
- Artifact: `turingresearch-docs-site-dry-run`.

## What It Runs

The workflow runs:

```bash
python -m pytest tests/workflow/test_docs_deployment_preflight.py -q
python -m pytest tests/workflow/test_docs_deployment_dry_run.py -q
python -m pytest tests/contract/test_public_release_hygiene.py -q
```

It then uploads the reviewed dry-run docs-site files as a GitHub Actions
artifact.

## What It Does Not Do

- no `actions/deploy-pages`;
- no `pages: write` permission;
- no `id-token: write` permission;
- no public Pages deployment;
- no real public URL;
- no analytics;
- no API key;
- no workflow secrets;
- no live provider call;
- no SSH/SFTP connection;
- no remote command execution.

## Manual Enablement Boundary

If a maintainer later wants real Pages deployment, this dry-run workflow should
be copied into a new reviewed deployment workflow only after the safety
checklist passes. This draft should remain dry-run by default.
