# Lane 310 - Docs Deployment Strategy

Status: completed.

Round: 332.

## Goal

Create a public docs deployment strategy for v1.5 without deploying anything.

## Scope

- Compare GitHub Pages, Cloudflare Pages / Netlify style static hosting,
  local-only docs, and no-deploy release bundle routes.
- Recommend GitHub Pages-ready as the v1.5 target.
- Keep deployment manual and disabled by default.
- Preserve public-safety boundaries.

## Deliverables

- `docs/docs-deployment-strategy.md`
- `docs/github-pages-deployment-plan.md`
- `docs/static-hosting-deployment-plan.md`
- `docs/local-only-docs-plan.md`
- `docs/docs-deployment-risk-register.md`
- `docs/docs-deployment-non-goals.md`

## Safety

- No deployment.
- No real public URL.
- No private file upload.
- No analytics.
- No provider secrets.
- No live fetch.
- No ARIS implementation.

## Validation

- Docs deployment strategy reviewed against the current docs-site skeleton.
- Name integrity and public hygiene checks must remain green.
- Pre-push checks must confirm no private paths, secrets, fake deployment
  claims, or old naming entered the new docs.
