# Lane 135 - Module Public API Contracts

Status: complete.

Round: 154.

## Goal

Define draft public API contracts for future module namespaces so later
repository or namespace splits do not create unclear interfaces. This lane does
not move code, split repositories, add namespaces, or change imports.

## Inputs

- `docs/module-public-api-surface.md`
- `docs/package-namespace-target-layout.md`
- `contracts/`
- `src/`

## Outputs

- `contracts/core_api.yaml`
- `contracts/paper_api.yaml`
- `contracts/artifact_api.yaml`
- `contracts/experiment_api.yaml`
- `contracts/dashboard_api.yaml`
- `contracts/plugin_api.yaml`
- `contracts/case_api.yaml`
- `docs/module-public-api-contracts.md`
- `tests/contract/test_module_public_api_contracts.py`
- `lanes/00_master_ledger.md`

## Contract Requirements

Each contract includes:

- module name;
- purpose;
- public models;
- public functions/tools;
- input schema;
- output schema;
- stability;
- internal-only modules;
- deprecated aliases;
- tests;
- docs.

## Stability Policy

Allowed values:

- `experimental`
- `beta`
- `stable`
- `internal`

No Round 154 contract is marked `stable`. Core and experiment are marked
`beta`; paper, artifact, dashboard, plugin, and case APIs remain
`experimental`.

## Boundaries

- No code movement.
- No import rewrite.
- No namespace creation.
- No package discovery change.
- No repository split.
- No internal helper promoted to public API.
- No experimental module marked stable.
- No network access.
- No release action.
- No prior project naming.

## Result

Round 154 adds module API contract drafts and contract tests that protect the
required fields, stability values, compatibility namespace, and documentation
links.
