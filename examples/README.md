# TuringResearch Plus Examples

These examples are end-to-end dry-run fixtures for the TuringResearch Plus `v0.1.0` release candidate. They do not require real network access, a Semantic Scholar key, an Apify token, or large private PDF files.

## Examples

| Example | Mode | Expected artifacts |
| --- | --- | --- |
| `vggt-human-prior-survey/` | fake-service dry run | ResearchBrief, LiteratureSurveyArtifact, GapReport, HypothesisPortfolio, ExperimentPlan |
| `smplx-feature-adapter-hypothesis/` | fake-service dry run | HypothesisPortfolio, IdeaPortfolio, DecisionReport, StressTestReport |
| `citation-graph-demo/` | fake semantic graph adapter | CitationGraph, recommended_next_reads, frontier nodes |
| `pdf-to-markdown-demo/` | local fixture dry run | PDFMarkdownOutput, markdown artifact, quality report, cache hit test |

## Directory Contract

Each example contains:

- `input/`
- `expected_outputs/`
- `README.md`
- `fake_run_config.yaml`
- `expected_outputs/artifact_list.json`

The workflow tests read these fixtures and verify that outputs can serialize to Markdown and JSON.
