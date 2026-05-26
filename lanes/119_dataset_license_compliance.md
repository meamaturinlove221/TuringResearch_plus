# Lane 119: Dataset / License Compliance Assistant

Round: 138

Status: implemented minimal.

## Goal

Add a local dataset / license compliance assistant for research project assets:
datasets, models, papers, and code repositories.

## Implemented

- `src/turing_research_plus/compliance/`
- `contracts/dataset_license_compliance.yaml`
- `docs/dataset-license-compliance-assistant.md`
- `docs/compliance-disclaimer.md`
- VGGT fake compliance report fixture.
- Unit and workflow tests for registries, risk checking, and report boundaries.

## VGGT Rules

- SMPL-X model files are license restricted and not bundled.
- Raw datasets are not public packaged by default.
- Third-party paper figures require reuse permission review.
- GitHub code with missing license metadata is marked unknown.
- Compliance report is not legal advice.

## Boundaries

- No legal advice.
- No automatic license download.
- No restricted data bundling.
- No network access.
- No private VGGT path reads.
- No old project naming.
- Human review remains required.

## Validation

- `tests/unit/test_compliance_models.py`
- `tests/unit/test_license_registry.py`
- `tests/unit/test_dataset_registry.py`
- `tests/unit/test_model_registry.py`
- `tests/unit/test_compliance_risk_checker.py`
- `tests/workflow/test_vggt_compliance_fake.py`
