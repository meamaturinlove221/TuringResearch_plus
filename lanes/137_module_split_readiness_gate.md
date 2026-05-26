# Lane 137 - Module Split Readiness Gate

Status: gate complete.

Round: 156.

## Goal

Evaluate whether the current monorepo modular layout has reached the minimum
bar for future repository splitting. This lane does not split repositories or
move code.

## Inputs

- `docs/monorepo-modular-layout.md`
- `docs/module-split-readiness-matrix.md`
- `docs/module-public-api-contracts.md`
- `tests/contract/test_new_namespace_imports.py`
- `tests/contract/test_legacy_namespace_compat.py`

## Outputs

- `docs/module-split-readiness-gate.md`
- `docs/first-split-candidate-report.md`
- `docs/do-not-split-yet-list.md`
- `lanes/00_master_ledger.md`

## Decision

Overall status: `not-ready-for-code-split`.

The monorepo is ready for continued internal modularization. It is not ready
for an actual repository split.

## Candidate Order

1. `turingresearch-vggt-case`
2. `turingresearch-examples`
3. `turingresearch-plugins`
4. `turingresearch-paper`
5. `turingresearch-artifact`
6. `turingresearch-dashboard`
7. `turingresearch-core`

## Rationale

- Case studies and examples are best first candidates because they can stand
  alone without moving core runtime behavior.
- Core should stay in the flagship because it carries workspace, privacy,
  quality, template, and evidence semantics.
- Paper and artifact need stronger API stabilization and independent demo
  coverage before extraction.
- Splitting should not scatter repository stars or make the main repo feel
  empty.
- The main repository must retain a complete demo path.

## Boundaries

- No repository split.
- No code movement.
- No package rename.
- No import removal.
- No network access.
- No private path read.
- No plugin execution.
- No final paper or experiment result claim.
- No prior project naming.
