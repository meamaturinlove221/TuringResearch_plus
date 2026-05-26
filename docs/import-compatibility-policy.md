# Import Compatibility Policy

Status: planning policy.

Round: 153.

This policy defines how old and new imports should coexist during a future
namespace refactor.

## Compatibility Decision

`turing_research_plus` remains a supported compatibility import namespace until
v1.0 or later. Future docs may recommend new namespaces after they exist, but
existing imports should keep working throughout the v0.x line.

## Compatibility Table

| Current import | Future preferred namespace | Compatibility rule |
| --- | --- | --- |
| `turing_research_plus.workspace` | `turing_research_core.workspace` | Keep old import as wrapper. |
| `turing_research_plus.privacy` | `turing_research_core.privacy` | Keep old import as wrapper. |
| `turing_research_plus.quality` | `turing_research_core.quality` | Keep old import as wrapper. |
| `turing_research_plus.project_template` | `turing_research_core.project_template` | Keep old import as wrapper. |
| `turing_research_plus.paper_write` | `turing_research_paper.write` | Keep old import as wrapper. |
| `turing_research_plus.paper_review` | `turing_research_paper.review` | Keep old import as wrapper. |
| `turing_research_plus.paper_digest` | `turing_research_paper.digest` | Keep old import as wrapper. |
| `turing_research_plus.paper_method` | `turing_research_paper.method` | Keep old import as wrapper. |
| `turing_research_plus.artifact_audit` | `turing_research_artifact.audit` | Keep old import as wrapper. |
| `turing_research_plus.handoff` | `turing_research_artifact.handoff` | Keep old import as wrapper. |
| `turing_research_plus.remote_artifacts` | `turing_research_artifact.remote` | Keep old import as wrapper. |
| `turing_research_plus.experiment_route` | `turing_research_experiment.route` | Keep old import as wrapper. |
| `turing_research_plus.hard_gates` | `turing_research_experiment.gates` | Keep old import as wrapper. |
| `turing_research_plus.failure` | `turing_research_experiment.failure` | Keep old import as wrapper. |
| `turing_research_plus.ui` | `turing_research_dashboard.ui` | Keep old import as wrapper. |
| `turing_research_plus.advisor_export` | `turing_research_dashboard.advisor_export` | Keep old import as wrapper. |
| `turing_research_plus.case_study` | `turing_research_dashboard.case_study` or `turing_research_cases.case_study` | Decide during implementation; keep old import. |
| `turing_research_plus.plugins` | `turing_research_plugins.plugins` | Keep old import as wrapper after circular boundary cleanup. |
| `turing_research_plus.mcp_plugins` | `turing_research_plugins.mcp` | Keep old import as wrapper. |
| `turing_research_plus.skill_market` | `turing_research_plugins.skills` | Keep old import as wrapper. |

## Import Test Requirements

For every migrated module:

- old import succeeds;
- new import succeeds;
- representative public symbols match;
- no import-time side effects;
- no network access;
- no optional backend requirement;
- no plugin execution;
- no private path read.

## Documentation Policy

- During preview stages, docs may show both old and new imports.
- After a namespace is stable, docs should recommend the new namespace.
- Migration notes must include examples for old and new imports.
- The README should keep package identity and CLI/MCP entrypoints clear.

## Deprecation Warnings

Do not add warnings immediately when wrappers are created. Add warnings only
after:

1. new namespace has existed for at least one minor release;
2. tests cover old and new imports;
3. docs and migration guide are complete;
4. no major release blocker depends on the old path.

## Removal Policy

No `turing_research_plus` compatibility import should be removed before v1.0.
After v1.0, removal still requires a migration guide, deprecation period, and
maintainer approval.
