# Lane 134 - Package Namespace Refactor Plan

Status: complete.

Round: 153.

## Goal

Plan a future package namespace refactor from the current broad
`turing_research_plus` module layout toward clearer domain namespaces. This
lane does not rename modules, move code, change package discovery, or modify
imports.

## Inputs

- `src/`
- `pyproject.toml`
- `docs/internal-module-boundary-audit.md`
- `docs/module-public-api-surface.md`
- `docs/future-repository-map.md`

## Outputs

- `docs/package-namespace-refactor-plan.md`
- `docs/package-namespace-target-layout.md`
- `docs/import-compatibility-policy.md`
- `docs/deprecation-policy-for-module-move.md`
- `lanes/00_master_ledger.md`

## Target Namespaces

- `turing_research_core`
- `turing_research_paper`
- `turing_research_artifact`
- `turing_research_experiment`
- `turing_research_dashboard`
- `turing_research_plugins`
- `turing_research_cases`

Compatibility namespace:

- `turing_research_plus`

## Strategy

1. Add target namespaces first.
2. Keep `turing_research_plus` compatibility.
3. Gradually move internals into target namespaces.
4. Cover old and new imports in tests.
5. Recommend new namespaces in docs after they exist.
6. Do not remove compatibility before v1.0.

## Required Outputs Covered

- migration stages;
- import compatibility table;
- deprecation timeline;
- test impact;
- risks;
- rollback plan.

## Boundaries

- No code movement.
- No module rename.
- No import rewrite.
- No package discovery change.
- No repository split.
- No network access.
- No release action.
- No prior project naming.

## Result

Round 153 creates a conservative namespace refactor plan for future rounds. The
main compatibility decision is that `turing_research_plus` remains supported
through the v0.x line while target namespaces are introduced gradually.
