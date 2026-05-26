# Package Namespace Refactor Plan

Status: planning draft.

Round: 153.

This plan describes how TuringResearch Plus can move from many modules under
`turing_research_plus` toward clearer domain namespaces that match future
repository boundaries. It does not rename modules, move code, change
`pyproject.toml`, or alter imports in this round.

## Decision

Use a staged namespace strategy:

1. Add target namespaces first.
2. Keep `turing_research_plus` as a compatibility layer.
3. Gradually move internal implementation into target namespaces.
4. Test both old and new import paths during migration.
5. Recommend new namespaces in docs after they exist.
6. Do not remove `turing_research_plus` compatibility before v1.0.

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

## Why This Refactor Is Needed

Current modules are well-scoped but crowded under one large package. Future
repository split work will be easier if imports already express ownership:

- core research OS semantics;
- paper workflows;
- artifact and handoff workflows;
- experiment routes and run status;
- dashboard and export surfaces;
- plugin and extension safety surfaces;
- public demos and case-study builders.

## Migration Stages

### Stage 0: Plan Only

Current round.

- Document target layout.
- Document compatibility policy.
- Do not add packages.
- Do not rewrite imports.
- Do not change `pyproject.toml`.

### Stage 1: Add Empty Target Namespaces

Future implementation round.

- Add namespace package folders.
- Add minimal `__init__.py` files.
- Add package import tests.
- Keep `turing_research_plus` as the source of implementation.
- No behavior change.

### Stage 2: Add Compatibility Re-export Modules

Future implementation round.

- Add new modules that re-export existing implementations.
- Example: `turing_research_dashboard.ui` wraps
  `turing_research_plus.ui`.
- Tests cover both old and new imports.
- Docs start mentioning new namespace as preview/experimental.

### Stage 3: Move Implementation Internally

Future implementation rounds.

- Move one group at a time.
- Keep old `turing_research_plus.<module>` wrappers.
- Update internal imports gradually to target namespace.
- Preserve public contracts and fake/default behavior.
- Add deprecation warnings only after compatibility is stable.

### Stage 4: Docs Prefer New Namespaces

Future release-prep round.

- Quickstart and developer docs recommend target namespaces.
- Compatibility docs list old imports as supported.
- Migration guide is required before this stage.

### Stage 5: Pre-v1 Compatibility Freeze

Future v1.0 planning.

- Keep compatibility entrypoints active.
- Decide which old module paths remain permanent shims.
- Do not delete compatibility until v1.0 or later and only after migration
  telemetry/issues show it is safe.

## Scope Order

Recommended order:

1. `turing_research_dashboard`
2. `turing_research_cases`
3. `turing_research_plugins`
4. `turing_research_paper`
5. `turing_research_artifact`
6. `turing_research_experiment`
7. `turing_research_core`

Reasoning: dashboard/cases/plugins have clearer future split stories, while
core should move last because it anchors the flagship repository.

## Test Impact

Every stage must update or add:

- package import tests;
- public import surface tests;
- package discovery tests;
- name integrity tests;
- module-specific regression tests;
- docs examples showing old/new import compatibility.

Default tests must still run without network access, live services, private
paths, or optional export backends.

## Risks

| Risk | Severity | Mitigation |
| --- | --- | --- |
| Broken imports | High | Add old/new import tests before moving implementation. |
| Confusing docs | Medium | Mark new namespace status clearly and keep compatibility table. |
| Circular dependencies | High | Move one group at a time and clean plugin/MCP two-way boundary first. |
| Package discovery drift | High | Update `pyproject.toml` only in a dedicated implementation round. |
| Main repo becomes hollow | High | Move core last and keep flagship demos/gates in the main repo. |
| Third-party users break before v1.0 | High | Keep `turing_research_plus` compatibility until v1.0 or later. |

## Rollback Plan

- Revert the most recent namespace group only.
- Keep compatibility wrappers untouched during rollback.
- Restore package discovery include patterns.
- Run package import and public import tests.
- Keep docs warning that target namespace is experimental until migration is
  complete.

## Non-goals

- No code movement in Round 153.
- No package rename in Round 153.
- No repository split.
- No removal of `turing_research_plus`.
- No change to CLI or MCP entrypoints.
- No import rewrite.
- No network access.
