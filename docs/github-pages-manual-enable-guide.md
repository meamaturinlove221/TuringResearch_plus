# GitHub Pages Manual Enable Guide

Status: manual guide.

Round: 364.

This guide describes a future maintainer-controlled path for enabling GitHub
Pages. It does not enable Pages, deploy a site, create a branch, or write a
public URL.

## Before Manual Enablement

1. Review `docs/docs-deployment-preflight.md`.
2. Review `docs/docs-deployment-blockers.md`.
3. Review `docs-site/preflight_report.md`.
4. Review `docs-site/dist/` locally.
5. Review `docs-site/dist_manifest.yaml`.
6. Confirm no private paths, secrets, raw data, restricted model payloads, or
   fake deployment URLs appear.
7. Confirm ARIS remains deferred.
8. Confirm a maintainer approves public docs publication.

## Manual Enablement Shape

If approved later, a maintainer may choose one of these routes:

- commit reviewed static output and enable Pages manually;
- create a separate reviewed Pages workflow with deployment permissions;
- use a separate docs branch.

This Round 364 draft does not choose or execute any of those routes.

## URL Policy

Do not write a public URL into docs until:

1. a maintainer enables Pages manually;
2. GitHub returns the actual Pages URL;
3. the published site is reviewed;
4. the URL is recorded in a reviewed commit.

## Required Manual Confirmation

Manual deployment requires all of:

- docs preflight passed;
- privacy/security scan passed;
- release branch is clean;
- generated pages were reviewed;
- no analytics are enabled unless separately approved;
- no credentials or private material are present;
- rollback plan is available.
