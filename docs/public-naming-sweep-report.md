# Public Naming Sweep Report

Round: 360.2
Status: complete

## Objective

Execute the public-layer naming sweep so the externally visible project name is
TuringResearch while runtime compatibility names remain intact.

## Decision

GO for public-facing TuringResearch naming on current entry points.

NO-GO for automatic package, import, CLI, MCP, PyPI, tag, release, repository,
or deployment rename.

## What Changed

- README public title and project prose now use TuringResearch.
- Current docs entry points now use TuringResearch in public titles and prose.
- Public examples, public demo text, split-ready bundles, and split-manual
  packs now use TuringResearch.
- Package and MCP display descriptions now use TuringResearch.
- Docs-site dry-run manifests no longer expose the local absolute root path.
- Public naming inventory, replacement log, and contract tests now document and
  enforce the boundary.

## Compatibility Boundary

Still retained by design:

- package distribution: `turingresearch-plus`;
- MCP server key and console command: `turingresearch-plus`,
  `turingresearch-plus-mcp`;
- Python compatibility namespace: `turing_research_plus`;
- code paths under `src/turing_research_plus/`;
- tests and docs that verify runtime compatibility.

These names are compatibility surfaces, not the public brand.

## Checks Required

- public name integrity tests;
- docs tests;
- pre-push check;
- no fake GitHub URL;
- no package rename;
- no import compatibility break.

## Safety

This round did not:

- create a GitHub repository;
- publish a release;
- publish to PyPI;
- rename Python packages;
- rename console scripts;
- rename the MCP server key;
- run live services;
- add private paths, secrets, raw data, or restricted model payloads.
