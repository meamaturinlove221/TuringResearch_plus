# Module Split Readiness Matrix

Status: audit artifact.

Round: 152.

This matrix evaluates future repository split readiness. It does not approve a
split and does not move code.

## Readiness Legend

- `not-ready`: keep in main repo.
- `candidate-after-stabilization`: revisit after API/docs/tests improve.
- `early-showcase-candidate`: possible first split after public-safe review.
- `must-stay-main`: should remain anchored in flagship.

## Matrix

| Group | Readiness | Why | Needed before split |
| --- | --- | --- | --- |
| core | must-stay-main | Defines shared workspace, evidence, privacy, quality, and template semantics. | Keep in flagship; document stable APIs but do not split early. |
| paper | candidate-after-stabilization | Paper workflows have strong value but section/citation/claim APIs are still evolving. | Paper beta scope, API docs, citation safety docs, independent demo. |
| artifact | candidate-after-stabilization | Artifact workflows are useful but tightly coupled to privacy, adapters, and live/fake boundaries. | Adapter safety API, import/export docs, independent fake demo, compliance review. |
| experiment | must-stay-main | Routes, hard gates, failures, and run status are shared evidence semantics. | Stable route DTOs and dashboard DTOs before any partial extraction. |
| dashboard_export | candidate-after-stabilization | Strong user-facing value and a good future split candidate. | Local server dashboard scope, stable DTOs, export API docs, privacy gate. |
| plugins | candidate-after-stabilization | Good ecosystem candidate, but plugin/MCP two-way dependency needs cleanup. | One-way registry architecture, sandbox docs, compatibility harness, disabled defaults. |
| examples_cases | early-showcase-candidate | Most suitable early split because demos/case studies can stand alone and link back. | Public-safe data review, redaction, compliance report, workflow tests, flagship links. |

## First Split Candidates

1. `turingresearch-vggt-case`
2. `turingresearch-examples`
3. `turingresearch-plugins`
4. `turingresearch-dashboard`

## Must Stay In Main Repo

- workspace and project registry;
- privacy and quality gates;
- core contracts and release gates;
- package identity and CLI/MCP smoke path;
- docs index and README;
- integration replay and public demo path;
- route/failure/evidence status semantics.

## Needs API Stabilization

- `plugins` and `mcp_plugins`;
- `dashboard`, `ui`, and `advisor_export`;
- `paper_write`, `paper_review`, and related paper modules;
- `remote_artifacts`, `github_sync`, `object_store`, `remote_readers`, and
  `shared_store`;
- `case_study` redaction and claim safety outputs.

## Needs Docs Completion

- dashboard DTOs and local server boundaries;
- paper beta section and claim-safety API;
- plugin registry split and compatibility guide;
- artifact adapter safety guide;
- case-study standalone README template;
- examples repository demo-safe policy;
- module ownership and migration docs.

## Recommendation

Keep the monorepo. Treat examples/case studies as the first realistic split
candidates only after v0.8 dashboard and case-study refresh work gives them
standalone polish. Keep core and experiment semantics anchored in the flagship.
