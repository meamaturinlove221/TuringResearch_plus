# Public Name Migration Plan

Round: 360.1
Status: staged plan

## Goal

Move public-facing materials to the TuringResearch name while preserving
runtime compatibility until package, CLI, and MCP migration decisions are made.

## Execution Order

1. Scope lock: document canonical public name, compatibility names, and risks.
2. Public docs pass: update README and release-facing docs to lead with
   TuringResearch.
3. Docs-site pass: update docs-site titles and public navigation.
4. Release docs pass: update GitHub release drafts and changelog display names.
5. CLI / MCP audit: decide whether command names and MCP server names can be
   changed without breaking local workflows.
6. Package audit: check package name availability and compatibility impact
   before any distribution rename.
7. Import compatibility plan: decide whether compatibility imports remain,
   deprecate, or move behind explicit aliases.
8. Final name integrity update: adjust tests only after public docs and
   compatibility policy agree.

## Current Round Boundary

Round 360.1 completes only step 1. It does not rename package metadata, import
paths, entry points, docs-site pages, or existing release artifacts.

## Required Follow-up Audits

- Package name availability and ownership.
- CLI command compatibility.
- MCP server compatibility.
- Docs-site title and nav sweep.
- Release notes and changelog display sweep.
- Split repository backlink wording.
- GitHub repository rename consequences.

## Stop Conditions

Stop the migration if any of these would happen without a separate approval:

- package import breakage;
- CLI command breakage;
- MCP server breakage;
- PyPI publication;
- GitHub release publication;
- tag creation;
- unreviewed rename of split packs;
- loss of historical rename traceability.
