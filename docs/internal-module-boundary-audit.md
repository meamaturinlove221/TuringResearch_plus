# Internal Module Boundary Audit

Status: audit report.

Round: 152.

This audit reviews current internal module boundaries without moving code or
splitting repositories. It uses a read-only scan of `src/`, `contracts/`, the
capability docs, and the repository split policy.

## Executive Summary

The current monorepo is appropriate. Most top-level modules are already
organized around clear domains, but several boundaries should be stabilized
before any future repository split:

- plugin modules need a cleaner one-way boundary between plugin manifests and
  MCP exposure;
- dashboard/export and case-study modules are good future split candidates
  after local server dashboard scope stabilizes;
- examples and case studies are the safest early split candidates because they
  can stand alone as public showcase material;
- core evidence, privacy, quality, workspace, and templates should remain in
  the flagship repository for now;
- artifact and paper modules need API and docs stabilization before any split.

## Audited Sources

- `src/`
- `contracts/`
- `docs/tool-capability-manifest.md`
- `docs/capability-index.md`
- `docs/repository-strategy.md`
- `docs/module-split-policy.md`

## Module Groups

| Group | Modules | Current posture |
| --- | --- | --- |
| core | `workspace`, `cross_project`, `privacy`, `quality`, `project_template`, `artifacts`, `ledger`, `north_star`, `vggt` | Keep in flagship; these define evidence and research OS semantics. |
| paper | `scholar_pipeline`, `paper_digest`, `paper_method`, `citation_graph`, `collision`, `related_work`, `paper_write`, `paper_review`, `paper` | Candidate for later package once paper beta APIs stabilize. |
| artifact | `artifact_audit`, `handoff`, `remote_artifacts`, `github_sync`, `remote_readers`, `shared_store`, `object_store`, `run_ingest`, `git_handoff`, `pod_workflow` | Needs safety and adapter boundaries before split. |
| experiment | `experiment_route`, `hard_gates`, `failure`, `run_compare`, `dashboard`, `experiment` | Keep close to core until route/run/failure APIs stabilize. |
| dashboard_export | `ui`, `dashboard`, `advisor`, `advisor_export`, `case_study`, `vault_ui` | Good future split candidate after local dashboard and export APIs stabilize. |
| plugins | `plugins`, `mcp_plugins`, `skill_market`, `capabilities`, `extension_safety`, `skills`, `sop` | Candidate after registry and sandbox policies mature; current circular risk needs cleanup. |
| examples_cases | `examples/public_demo`, `examples/vggt-human-prior-survey`, `examples/project_templates`, `examples/workspaces`, `examples/benchmarks` | Best early split candidates after demo-safe review. |

## Current Import Dependency Risks

Read-only AST scan findings:

- `turing_research_plus.plugins` imports `capabilities`, `extension_safety`,
  and `mcp_plugins`.
- `turing_research_plus.mcp_plugins` imports `plugins`.
- This creates a two-way dependency risk between plugin manifests and MCP tool
  exposure.
- `turing_research_plus.remote_artifacts` aggregates `github_sync`,
  `object_store`, `remote_readers`, and `shared_store`; this is a useful facade
  but should not become a hidden sync-adapter implementation path.
- `turing_research_plus.advisor` imports `artifact_audit`, `artifacts`, and
  `vggt`; this makes the advisor pack useful for the current dogfooding case
  but less ready as a standalone export package.
- `turing_research_plus.paper` imports `turing_research.pdf` and `artifacts`,
  so a future paper split needs a stable PDF/artifact contract.
- `turing_research_plus.dashboard` imports `failure` and `run_ingest`;
  dashboard extraction should preserve explicit run/failure interfaces.

## Circular Dependency Risk

| Risk | Severity | Recommendation |
| --- | --- | --- |
| `plugins` <-> `mcp_plugins` | Medium | Move shared manifest-to-tool mapping contracts into a lower-level metadata module or keep MCP mapping as one-way adapter over plugin manifests. |
| Dashboard pulling run/failure internals | Low | Define stable dashboard DTOs before local server dashboard work. |
| Advisor pack importing VGGT-specific helpers | Medium | Extract generic advisor inputs from case-specific builders before any export split. |
| Remote artifact facade aggregating many adapters | Medium | Keep fake/default and safety policies explicit; do not hide live adapter behavior behind generic imports. |

No large circular graph was detected in the top-level scan, but the plugin/MCP
two-way edge should be addressed before repository or package split.

## Best Future Split Candidates

1. `examples_cases`: public demos, VGGT case, project templates.
2. `dashboard_export`: dashboard, advisor export, case study, vault UI.
3. `plugins`: after plugin registry and sandbox policy mature.
4. `paper`: after research paper writing beta stabilizes.

## Modules That Must Stay In Main Repo For Now

- `workspace`
- `privacy`
- `quality`
- `project_template`
- `artifacts`
- `ledger`
- `hard_gates`
- `failure`
- `experiment_route`
- release, docs, examples, and integration gates

These modules define shared semantics and safety gates. Moving them out early
would make the flagship repository hard to understand and hard to test.

## Modules Needing API Stabilization

- `plugins` / `mcp_plugins`: remove two-way dependency and define clear
  manifest, registry, mapping, and runtime boundaries.
- `dashboard` / `ui` / `advisor_export`: define stable DTOs for dashboard cards,
  export plans, and quality reports.
- `paper_write` / `paper_review`: define stable section, citation, and claim
  status contracts before paper beta.
- `remote_artifacts` and related adapter modules: keep live, fake, safety, and
  import/export boundaries explicit.
- `case_study`: define stable redaction and claim-safety reports before a
  standalone case-study repo.

## Modules Needing Docs Completion

- module-level ownership map;
- public API surface docs;
- stable DTO docs for dashboard/export;
- plugin manifest to MCP mapping guide;
- paper beta API guide;
- adapter safety guide for artifact modules;
- case-study split readiness guide.

## Recommendation

Do not split repositories now. Use v0.8 to improve local dashboard boundaries,
paper beta APIs, plugin registry metadata, case-study public surfaces, and
plugin sandbox research. Re-run this audit after those scope locks and
integration gates complete.
