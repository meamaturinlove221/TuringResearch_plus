# Lane 136 - Monorepo Modular Layout

Status: implemented minimal.

Round: 155.

## Goal

Start implementing monorepo internal modular layout without splitting the
repository. This lane adds target namespace facade packages and a compatibility
alias registry while preserving legacy `turing_research_plus` imports.

## Inputs

- `docs/package-namespace-refactor-plan.md`
- `docs/package-namespace-target-layout.md`
- module API contracts

## Outputs

- `src/turing_research_core/`
- `src/turing_research_paper/`
- `src/turing_research_artifact/`
- `src/turing_research_experiment/`
- `src/turing_research_dashboard/`
- `src/turing_research_plugins/`
- `src/turing_research_cases/`
- `src/turing_research_plus/compat/`
- `tests/contract/test_new_namespace_imports.py`
- `tests/contract/test_legacy_namespace_compat.py`
- `docs/monorepo-modular-layout.md`
- `docs/import-examples.md`
- `pyproject.toml`
- `lanes/00_master_ledger.md`

## Implementation Notes

- New namespaces are facade/re-export packages.
- Implementations remain in `turing_research_plus`.
- Package discovery and mypy package list include the new namespaces.
- Legacy imports remain supported.
- No runtime plugin execution or live behavior is enabled.

## Boundaries

- No repository split.
- No implementation move.
- No old import removal.
- No large refactor.
- No default network access.
- No private path read.
- No plugin execution.
- No final paper or experiment result claim.
- No prior project naming.

## Result

Round 155 creates the first monorepo modular namespace layer while preserving
compatibility with the existing package layout.
