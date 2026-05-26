# Lane 86 - General Research Project Template

Status: implemented minimal.

Round: 105.

## Scope

Generalized the original project template generator into typed reusable
research project templates. This round added schema models, template registry,
research type definitions, typed renderers, generated fixtures, tests, docs,
and a contract.

## Added

- `src/turing_research_plus/project_template/schema.py`
- `src/turing_research_plus/project_template/template_registry.py`
- `src/turing_research_plus/project_template/research_types.py`
- `src/turing_research_plus/project_template/renderers.py`
- `contracts/research_project_template.yaml`
- `docs/general-research-project-template.md`
- typed template tests and workflow tests

## Template Types

1. `vggt_like_experiment_project`
2. `paper_survey_project`
3. `experiment_heavy_project`
4. `software_tooling_project`
5. `mixed_research_project`

## Fixtures

- `examples/project_templates/vggt_like_project/`
- `examples/project_templates/paper_survey_project/`
- `examples/project_templates/experiment_heavy_project/`
- `examples/project_templates/software_tooling_project/`

## Boundaries

- Generated content is template / placeholder.
- No false research conclusions.
- No real citations.
- No network access.
- No private VGGT path reads.
- No planned-as-observed promotion.
- Human review required.
