# Package Metadata Audit

Round: 378
Status: complete

## Scope

This audit checks TuringResearch package metadata for v1.6 release-candidate
readiness. It focuses on packaging correctness, public naming hygiene, and
release boundary safety.

## Audit Results

| Area | Result | Notes |
| --- | --- | --- |
| Package name | Review pass | `turingresearch-plus` is intentionally retained as the v1.6 compatibility distribution name. |
| Public display name | Pass | README, install guide, and package description use TuringResearch. |
| Version | Pass | `pyproject.toml` matches `VERSION` at `1.5.0rc0`. |
| Description | Pass | Description avoids the old public `Plus` branding. |
| License | Blocker for public publish | Metadata is present, but final human license approval is still required before PyPI. |
| Authors | Pass | Author metadata names TuringResearch. |
| Entry points | Pass | Existing CLI/MCP/session entry points remain available. |
| Dependencies | Pass | Runtime dependencies are explicit and minimal. |
| Optional extras | Pass | `dev`, `pdf`, `mcp`, and `all` extras are declared. |
| README render safety | Pass | README is local-first, fake/default, and does not advertise fake URLs or unsupported claims. |
| Old naming | Pass with compatibility exception | Public docs use TuringResearch; compatibility names remain only for package/import/CLI surfaces. |

## Entry Points

- `turingresearch-plus = turing_research.mcp_server:main`
- `turingresearch-plus-mcp = turing_research.mcp_server:main`
- `turingresearch-session = turing_research_plus.session_runtime.cli:main`

The first two entry points retain the existing `plus` suffix for compatibility.
Round 378 does not change CLI names.

## Dependency Audit

Runtime dependencies:

- `pydantic>=2.7`
- `pydantic-settings>=2.2`
- `httpx>=0.27`

Optional extras:

- `dev`
- `pdf`
- `mcp`
- `all`

No live provider credential is required by default.

## Compatibility Exceptions

The following names are intentionally allowed in package metadata and install
instructions:

- `turingresearch-plus`: current distribution name and compatibility CLI prefix.
- `turingresearch-plus-mcp`: current MCP CLI entry point.
- `turing_research_plus`: compatibility Python import namespace.

These are not public project names. The public project name remains
TuringResearch.

## PyPI Decision

NO-GO for PyPI publication in Round 378.

Reasons:

- final license decision must be manually reviewed;
- package distribution-name migration is still undecided;
- release artifact build and publish steps are future/manual;
- this round is metadata readiness only.
