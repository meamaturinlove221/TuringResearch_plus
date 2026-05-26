# Package Namespace Target Layout

Status: planning draft.

Round: 153.

This document maps current module groups to future target namespaces. It is a
target layout only; no modules are moved in this round.

## Target Layout

```text
src/
  turing_research_core/
  turing_research_paper/
  turing_research_artifact/
  turing_research_experiment/
  turing_research_dashboard/
  turing_research_plugins/
  turing_research_cases/
  turing_research_plus/        # compatibility layer
```

## Namespace Responsibilities

| Target namespace | Responsibility |
| --- | --- |
| `turing_research_core` | Workspace, evidence status, privacy, quality, project templates, shared models, core gates. |
| `turing_research_paper` | Scholar pipeline, paper digest, method cards, citation graph, collision risk, related work, paper writing, deep review. |
| `turing_research_artifact` | Artifact audit, handoff, remote artifact metadata, remote readers, shared/object stores, run ingest. |
| `turing_research_experiment` | Experiment routes, hard gates, failure taxonomy, run comparison, run dashboard layer. |
| `turing_research_dashboard` | Static UI, local dashboard, advisor export, case-study exports, vault UI. |
| `turing_research_plugins` | Plugin manifests, MCP plugin registry, skill market, capability manifest, extension safety, sandbox policy. |
| `turing_research_cases` | Public demos, VGGT dogfooding case, project templates, benchmark fixtures, case-study examples. |
| `turing_research_plus` | Compatibility layer for old imports until v1.0 or later. |

## Current-to-target Map

| Current modules | Target namespace |
| --- | --- |
| `workspace`, `cross_project`, `privacy`, `quality`, `project_template`, `artifacts`, `ledger`, `north_star`, `vggt` | `turing_research_core` |
| `scholar_pipeline`, `paper_digest`, `paper_method`, `citation_graph`, `collision`, `related_work`, `paper_write`, `paper_review`, `paper` | `turing_research_paper` |
| `artifact_audit`, `handoff`, `remote_artifacts`, `github_sync`, `remote_readers`, `shared_store`, `object_store`, `run_ingest`, `git_handoff`, `pod_workflow` | `turing_research_artifact` |
| `experiment_route`, `hard_gates`, `failure`, `run_compare`, `dashboard`, `experiment` | `turing_research_experiment` |
| `ui`, `advisor`, `advisor_export`, `case_study`, `vault_ui` | `turing_research_dashboard` |
| `plugins`, `mcp_plugins`, `skill_market`, `capabilities`, `extension_safety`, `skills`, `sop` | `turing_research_plugins` |
| `examples/public_demo`, `examples/vggt-human-prior-survey`, `examples/project_templates`, `examples/workspaces`, `examples/benchmarks` | `turing_research_cases` or future example repository |

## Compatibility Layout

During migration:

```text
turing_research_plus.ui -> turing_research_dashboard.ui
turing_research_plus.paper_write -> turing_research_paper.write
turing_research_plus.plugins -> turing_research_plugins.plugins
```

The exact module names should be decided one namespace at a time. The first
implementation should prefer direct re-export wrappers rather than duplicated
implementation.

## Package Discovery Implication

Future implementation rounds must update package discovery to include:

```toml
include = [
  "turing_research*",
  "turing_research_plus*",
  "turing_research_core*",
  "turing_research_paper*",
  "turing_research_artifact*",
  "turing_research_experiment*",
  "turing_research_dashboard*",
  "turing_research_plugins*",
  "turing_research_cases*",
]
```

Do not change package discovery until the first target namespace exists and
package import tests cover it.

## Layout Risks

- Too many namespaces at once can make imports noisy.
- Moving core early can weaken the flagship package.
- Examples/cases may not belong in installable Python packages; they may become
  repositories rather than import namespaces.
- Plugin namespaces must avoid circular imports with MCP mappings.

## Recommendation

Start with one low-risk namespace wrapper, likely `turing_research_dashboard`
or `turing_research_cases`, then prove old/new import compatibility before
moving paper, artifact, experiment, plugin, or core implementations.
