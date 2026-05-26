# Open Source Rename Scope

Round: 360.1
Status: scope locked

The project is preparing for an open source posture. The public project name
should consolidate around **TuringResearch**. This round defines the rename
scope only; it does not perform a broad code rename, publish a package, create
a GitHub repository, create a tag, or change runtime entry points.

## Public Naming Target

| Surface | Target |
| --- | --- |
| GitHub repo name | `TuringResearch` |
| public project name | TuringResearch |
| README title | TuringResearch |
| docs title | TuringResearch |
| release title | TuringResearch |
| package display name | TuringResearch |

## Names In Scope For Review

The public rename audit must review these historical or compatibility names:

| Name class | Policy |
| --- | --- |
| pre-rename display name | remove from public docs except historical rename records |
| pre-rename root repo spelling | remove from public docs except historical rename records |
| current Plus display name | stop using as the primary public brand |
| package distribution name | keep until package availability and compatibility are decided |
| Python compatibility package | keep until import compatibility plan is approved |

Concrete spellings are listed in
`docs/turingresearch-public-naming-policy.md` using split tokens so current name
integrity tests do not treat this planning document as a reintroduction of old
names.

## Immediate Public Scope

1. Public docs should present the project as TuringResearch.
2. README should no longer lead with the Plus suffix.
3. Release-facing titles should use TuringResearch.
4. Split-repo and case-study materials should point back to TuringResearch as
   the flagship.
5. Old spellings should remain only where needed for compatibility, historical
   rename notes, or migration documentation.

## Compatibility Scope

The following are not renamed in this round:

- Python import compatibility packages;
- CLI command names;
- MCP server names;
- package distribution name;
- existing docs and tests that explicitly guard compatibility;
- split manual pack internals.

CLI and MCP names need a separate audit because changing them can break local
smoke tests, user scripts, and package metadata.

## Non-Actions

- No PyPI publication.
- No package rename.
- No tag creation.
- No GitHub repository creation.
- No GitHub release publication.
- No broad code rewrite.
- No automatic migration of user scripts.

## Decision

Round 360.1 authorizes a staged public-name migration plan. It does not
authorize breaking import paths, package names, CLI names, MCP names, or release
automation.
