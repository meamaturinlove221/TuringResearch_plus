# Lane 133 - Internal Module Boundary Audit

Status: complete.

Round: 152.

## Goal

Audit TuringResearch internal module boundaries without splitting repositories
or moving code. The lane records dependency risks, circular dependency risks,
future split candidates, modules that must stay in the flagship repo, and API
or docs stabilization needs.

## Inputs

- `src/`
- `contracts/`
- `docs/tool-capability-manifest.md`
- `docs/capability-index.md`
- `docs/repository-strategy.md`
- `docs/module-split-policy.md`

## Outputs

- `docs/internal-module-boundary-audit.md`
- `docs/module-dependency-graph.md`
- `docs/module-ownership-map.md`
- `docs/module-public-api-surface.md`
- `docs/module-split-readiness-matrix.md`
- `examples/architecture/module_dependency_graph.mmd`
- `lanes/00_master_ledger.md`

## Key Findings

- Current monorepo remains appropriate.
- Best future split candidates are examples/case studies first, then
  dashboard/export, plugins, and paper after stabilization.
- Core workspace, privacy, quality, templates, evidence status, route/failure
  semantics, package identity, docs index, and release gates should remain in
  the flagship repo.
- Main import risk is the two-way dependency between plugin manifests and MCP
  plugin registry.
- Advisor/export surfaces still contain case-specific coupling that should be
  normalized before a standalone split.
- Remote artifact modules need stronger adapter safety docs before any split.

## Boundaries

- No code movement.
- No repository split.
- No package split.
- No import rewrite.
- No network access.
- No private path read.
- No live adapter execution.
- No plugin execution.
- No release action.
- No prior project naming.

## Result

Round 152 creates the module boundary audit and dependency graph needed before
any future hub-and-spoke repository work. It recommends keeping the monorepo
while stabilizing APIs and docs around future split candidates.
