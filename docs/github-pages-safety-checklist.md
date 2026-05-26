# GitHub Pages Safety Checklist

Status: manual safety checklist.

Round: 364.

This checklist must pass before a maintainer turns any dry-run workflow into a
real GitHub Pages deployment workflow.

## Required Checks

- [ ] `docs-site/nav.yaml` validates.
- [ ] `docs-site/pages/index.md` exists.
- [ ] `docs-site/pages/quickstart.md` exists.
- [ ] `docs-site/pages/original-repo-parity.md` exists.
- [ ] `docs-site/pages/public-demo.md` exists.
- [ ] `docs-site/pages/privacy.md` exists.
- [ ] Broken links are zero.
- [ ] Missing pages are zero.
- [ ] Missing source docs are zero.
- [ ] Orphan pages are reviewed.
- [ ] Private path scan is clean.
- [ ] Secret scan is clean.
- [ ] Raw data scan is clean.
- [ ] Restricted model payload scan is clean.
- [ ] Fake deployment URL scan is clean.
- [ ] Analytics are absent unless separately approved.
- [ ] ARIS is still deferred.
- [ ] Human review is recorded.

## Workflow Safety Checks

- [ ] Dry-run workflow uses `workflow_dispatch`.
- [ ] Dry-run workflow has `contents: read` only.
- [ ] Dry-run workflow does not use `actions/deploy-pages`.
- [ ] Dry-run workflow does not request `pages: write`.
- [ ] Dry-run workflow does not request `id-token: write`.
- [ ] Dry-run workflow does not require API keys.
- [ ] Dry-run workflow does not reference secrets.
- [ ] Dry-run workflow only uploads reviewed public-safe artifacts.

## Stop Conditions

Stop and do not deploy if any of these are true:

- any preflight blocker exists;
- any credential or token appears in generated output;
- any private path appears in generated output;
- any raw data appears in generated output;
- any fake/demo output is presented as observed evidence;
- any real URL is guessed before GitHub provides it;
- maintainer approval is missing.
