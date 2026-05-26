# Project Template Generator

Status: v0.5 minimal implementation.

Round 94 adds a local project skeleton generator for new research directions.
It creates standard directories and Markdown seed files, but it does not add
experiment results or observed evidence.

## Generated Structure

- `README.md`
- `docs/north_star.md`
- `docs/evidence_ledger.md`
- `docs/artifact_plan.md`
- `docs/experiment_routes.md`
- `docs/related_work.md`
- `docs/advisor_pack.md`
- `lanes/00_master_ledger.md`
- `examples/README.md`
- `contracts/README.md`
- `race/feature_capsules/README.md`

## Models

- `ProjectTemplateRequest`
- `ProjectTemplateFile`
- `ProjectTemplateResult`

## Local Helper

- command: `turing project template-generate`
- tool: `research.project_template_generate`
- output: `ProjectTemplateResult`

The helper is local-only and not a public MCP API surface.

## Safety Policy

- No network access.
- No private VGGT path reads.
- No experiment execution.
- No observed evidence generated from templates.
- No secrets, raw data, or private model files.
- Existing files are not overwritten unless `overwrite=True`.
- Human review is required before using a generated project publicly.

## Fixture

`examples/project_templates/vggt_like_project/` demonstrates the generated
structure for a VGGT-like research topic. It is a skeleton only, not a VGGT
result and not a paper conclusion.
