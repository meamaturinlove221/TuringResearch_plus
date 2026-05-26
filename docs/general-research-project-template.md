# General Research Project Template

Status: v0.6 minimal implementation.

Round 105 generalizes the original VGGT-derived project skeleton into typed,
reusable research project templates. The generator creates placeholder project
structure only. It does not create observed evidence, real citations, experiment
results, or paper conclusions.

## Template Types

1. `vggt_like_experiment_project`
2. `paper_survey_project`
3. `experiment_heavy_project`
4. `software_tooling_project`
5. `mixed_research_project`

## Generated Structure

Each typed template generates:

- `README.md`
- `docs/north_star.md`
- `docs/research_questions.md`
- `docs/evidence_ledger.md`
- `docs/artifact_plan.md`
- `docs/experiment_routes.md`
- `docs/related_work.md`
- `docs/failure_taxonomy.md`
- `docs/advisor_pack.md`
- `lanes/00_master_ledger.md`
- `contracts/README.md`
- `examples/README.md`
- `race/feature_capsules/README.md`

## Models

- `ResearchProjectType`
- `ResearchTemplateSection`
- `ResearchProjectTemplate`
- `ResearchProjectTemplateRequest`
- `GeneratedResearchProjectFile`
- `ResearchProjectTemplateManifest`

## Local Helper

- command: `turing project new`
- tool: `project.research_template_generate`
- output: `ResearchProjectTemplateManifest`

This helper is local-only and not a frozen public MCP API.

## Safety Policy

- Generated content is marked template / placeholder.
- Generated content contains no observed evidence.
- Generated content contains no real citations.
- Generated content contains no research conclusion.
- No network access.
- No private VGGT path reads.
- Human review is required before public or advisor use.

## Fixtures

- `examples/project_templates/vggt_like_project/`
- `examples/project_templates/paper_survey_project/`
- `examples/project_templates/experiment_heavy_project/`
- `examples/project_templates/software_tooling_project/`

Each fixture is a generated skeleton only. It is not a real project result.
