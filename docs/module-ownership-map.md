# Module Ownership Map

Status: audit artifact.

Round: 152.

This map assigns current modules to ownership groups for maintenance and
future split review. Ownership here means documentation and release-gate
responsibility, not separate repository ownership.

## Ownership Groups

| Group | Modules | Current owner responsibility |
| --- | --- | --- |
| core | `workspace`, `cross_project`, `privacy`, `quality`, `project_template`, `artifacts`, `ledger`, `north_star`, `vggt` | Maintain shared research OS semantics, evidence status, privacy gates, templates, and fake/default stability. |
| paper | `scholar_pipeline`, `paper_digest`, `paper_method`, `citation_graph`, `collision`, `related_work`, `paper_write`, `paper_review`, `paper` | Maintain paper-review and writing scaffolds without generating final conclusions. |
| artifact | `artifact_audit`, `handoff`, `remote_artifacts`, `github_sync`, `remote_readers`, `shared_store`, `object_store`, `run_ingest`, `git_handoff`, `pod_workflow` | Maintain artifact metadata, import/export safety, fake/live boundaries, and no automatic remote execution. |
| experiment | `experiment_route`, `hard_gates`, `failure`, `run_compare`, `dashboard`, `experiment` | Maintain routes, gates, run status, failure taxonomy, and not-ready claim boundaries. |
| dashboard_export | `ui`, `dashboard`, `advisor`, `advisor_export`, `case_study`, `vault_ui` | Maintain local-first dashboards, advisor exports, case-study outputs, and export quality gates. |
| plugins | `plugins`, `mcp_plugins`, `skill_market`, `capabilities`, `extension_safety`, `skills`, `sop` | Maintain plugin metadata, safety policy, MCP mapping, skill catalog, capability index, and disabled defaults. |
| examples_cases | `examples/public_demo`, `examples/vggt-human-prior-survey`, `examples/project_templates`, `examples/workspaces`, `examples/benchmarks` | Maintain demo safety, public examples, case-study redaction, replay fixtures, and privacy/compliance review. |

## Main-repo Required Owners

These ownership areas should remain anchored in the main repo:

- release gates;
- privacy and quality gates;
- core workspace semantics;
- public demo path;
- package metadata;
- docs index;
- compatibility and migration guides.

## Future Split Owners

If modules later split, each satellite repository needs:

- owner or maintainer;
- release policy;
- test command;
- docs owner;
- privacy/license reviewer;
- compatibility policy;
- link back to the flagship repository.

## Review Cadence

Review ownership after:

- each roadmap round;
- each scope-lock round;
- each release prep;
- any new public demo or case study;
- any plugin registry or dashboard server expansion.
