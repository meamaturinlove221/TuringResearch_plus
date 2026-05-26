# Lane 75 - Project Template Generator

Status: implemented minimal.

Round: 94.

## Scope

Implemented a local research project skeleton generator for new project
directions.

## Added

- `src/turing_research_plus/project_template/`
- `contracts/project_template.yaml`
- `docs/project-template-generator.md`
- `examples/project_templates/vggt_like_project/`
- Project template unit and workflow tests

## Generated Template Contents

- `README.md`
- `docs/north_star.md`
- `docs/evidence_ledger.md`
- `docs/artifact_plan.md`
- `docs/experiment_routes.md`
- `docs/related_work.md`
- `docs/advisor_pack.md`
- `lanes/00_master_ledger.md`
- `examples/`
- `contracts/`
- `race/feature_capsules/`

## Boundaries

- No network access.
- No private VGGT path reads.
- No experiment execution.
- No observed evidence generated from template files.
- No secrets, raw data, or private model files.
- Human review required before public use.
