# TuringResearch Plus Example: VGGT Human Prior Survey

Mode: fake-service dry run.

This example demonstrates a depth-gated literature survey for a VGGT-style human-prior research question.

## Expected Artifacts

- ResearchBrief
- LiteratureSurveyArtifact
- GapReport
- HypothesisPortfolio
- ExperimentPlan

## Inputs

- `input/request.json` defines the topic, survey strategy, seed papers, and research goal.
- `fake_run_config.yaml` fixes dry-run mode, fake paper service, fake PDF Markdown service, and no-network execution.

## Outputs

- `expected_outputs/artifact_list.json` lists the required artifacts.
- `expected_outputs/expected_summary.md` documents the expected dry-run result.

No real network access, real API key, Semantic Scholar key, Apify token, or private paper corpus is required.
