# TuringResearch Docs Site

Status: local-first static docs-site skeleton.

Round: 215.

This directory defines a future static documentation site for TuringResearch.
It does not deploy anything, does not depend on cloud services, and does not
introduce a large frontend framework.

## Scope

The docs site is a navigation and generation layer over existing repository
Markdown docs. The flagship repository remains the source of truth.

## Local-first Strategy

- Source content stays in `README.md`, `docs/`, `examples/`, and
  `split_ready/`.
- `docs-site/nav.yaml` defines navigation.
- `docs-site/site_manifest.yaml` defines scope and generation rules.
- `docs-site/pages/` contains lightweight page stubs that link back to source
  docs.

## Non-goals

- No deployment.
- No hosted SaaS surface.
- No cloud service dependency.
- No large frontend framework.
- No private data reads.
- No fake external links.
