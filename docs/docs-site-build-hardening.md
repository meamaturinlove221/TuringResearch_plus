# Docs Site Build Hardening

Status: implemented.

Round: 333.

The docs-site builder now has a build hardening layer for v1.5 deployment
readiness. It remains local-only: no public deployment, no live fetch, no
analytics, no provider secrets, and no real public URL.

## Added Surfaces

- `turing_research_plus.docs_site.link_checker`
- `turing_research_plus.docs_site.static_export`
- `turing_research_plus.docs_site.build_report`
- `contracts/docs_site_build_hardening.yaml`
- `docs-site/build_report.md`

## What The Hardening Checks

The hardening layer supports:

- broken local Markdown link report;
- missing docs-site page report;
- missing source-doc report;
- orphan docs-site page report;
- nav / manifest validation;
- static export manifest with file hash, size, and type;
- no private path / secret marker scan over docs-site inputs.

## Local Build Boundary

The build remains a local static export. It does not:

- deploy to GitHub Pages;
- deploy to Cloudflare Pages, Netlify, or similar hosting;
- write a real public URL;
- enable analytics;
- read private data;
- fetch live network content;
- publish generated files automatically.

## Human Review Boundary

The generated report is a readiness artifact. A human still needs to review:

- generated HTML;
- `docs-site/nav.yaml`;
- `docs-site/site_manifest.yaml`;
- public source docs referenced by nav entries;
- fake/demo wording;
- release safety claims.

## Recommended v1.5 Use

Use the hardening report before any future deployment attempt:

1. Run the local docs-site build hardening workflow.
2. Inspect `docs-site/build_report.md`.
3. Confirm no blockers, private-path hits, missing pages, or broken links.
4. Review generated output manually.
5. Only then decide whether to proceed with a manual deployment plan.
