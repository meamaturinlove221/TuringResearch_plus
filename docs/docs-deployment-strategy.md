# Docs Deployment Strategy

Status: strategy locked.

Round: 332.

v1.5 prepares public documentation deployment without deploying anything. The
recommended target is **GitHub Pages-ready**, with static hosting, local-only
docs, and no-deploy release bundles kept as explicit alternatives.

This document is a planning artifact. It does not publish a site, create DNS
records, write a real URL, upload files, enable analytics, or move private
material outside the repository.

## Current Docs Site Baseline

The current docs-site is local-first:

- `docs-site/site_manifest.yaml` declares repository Markdown as the source of
  truth.
- `docs-site/nav.yaml` maps public pages to source docs and demo fixtures.
- `docs-site/pages/` contains lightweight page stubs.
- `docs-site/output/` is generated locally and ignored except for `.gitkeep`.
- `docs/static-docs-site-builder.md` documents a Python-only local static
  builder with no Node, network, or cloud dependency.

This is a good base for public externalization because the deployment boundary
can be reviewed before any hosting target is used.

## Route Comparison

| Route | Best use | Strengths | Risks | v1.5 recommendation |
| --- | --- | --- | --- | --- |
| GitHub Pages | repository-native public docs | simple workflow, common OSS pattern, easy manual review | accidental publish of private docs if source list is loose | prepare only |
| Cloudflare Pages / Netlify style static hosting | polished static hosting later | preview builds, redirects, custom domains | provider config sprawl, analytics temptation, accidental env vars | document as future option |
| local-only docs | internal review and demos | no upload, no public exposure, safest default | less convenient for external reviewers | keep supported |
| no-deploy release bundle | release artifact or interview packet | auditable bundle, no hosting dependency | can go stale if not regenerated | keep as fallback |

## Recommended v1.5 Path

1. Make the docs-site build reproducible locally.
2. Add public-safety checks for docs inputs and generated output.
3. Prepare GitHub Pages instructions and a reviewed artifact checklist.
4. Keep deployment manual and off by default.
5. Keep local-only and no-deploy bundle paths available for cautious release
   review.

## Deployment Readiness Gates

Before any human deploys docs, the project should pass:

- docs-site build smoke;
- docs navigation integrity;
- public-safe source allowlist review;
- no private path / secret / raw data scan;
- no fake external URL scan;
- no unsupported experiment success claim scan;
- ARIS still deferred check;
- human review of generated HTML.

## Public Content Boundary

Public docs may include:

- README and public-facing docs;
- fake/demo examples;
- parity dashboards;
- release notes and handoff docs;
- public safety policies;
- manual split pack docs.

Public docs must not include:

- `.env` or credentials;
- API keys, tokens, cookies, or provider secrets;
- raw private research data;
- restricted model payloads;
- private local paths;
- generated claims that planned work was observed;
- fake/demo outputs presented as experimental evidence;
- real deployment URLs before a human has created them.

## Decision

v1.5 should be **GitHub Pages-ready, not deployed**.

The deliverable is a reviewed deployment plan, hardened build path, and
checklist that a human can use later. The project should not automatically
deploy, configure analytics, create a live URL, or upload private files.
