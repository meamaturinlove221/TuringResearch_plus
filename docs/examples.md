# TulingResearch Plus Examples

The `examples/` tree contains release-candidate dry-run fixtures for TulingResearch Plus. Every example runs in fake mode or local fixture mode and does not require real network access, a Semantic Scholar key, an Apify token, private repositories, or large PDF files.

## Directory Contract

Every example contains:

- `input/`
- `expected_outputs/`
- `README.md`
- `fake_run_config.yaml`
- `expected_outputs/artifact_list.json`

Workflow tests read these fixtures and verify that expected outputs can serialize to Markdown and JSON.

## `examples/vggt-human-prior-survey/`

Mode: fake-service dry run.

Expected artifacts:

- ResearchBrief
- LiteratureSurveyArtifact
- GapReport
- HypothesisPortfolio
- ExperimentPlan

Coverage: `tests/workflow/test_example_vggt_human_prior.py`

## `examples/smplx-feature-adapter-hypothesis/`

Mode: fake-service dry run.

Expected artifacts:

- HypothesisPortfolio
- IdeaPortfolio
- DecisionReport
- StressTestReport

Coverage: `tests/workflow/test_example_smplx_feature_adapter.py`

## `examples/citation-graph-demo/`

Mode: fake semantic graph adapter.

Expected artifacts:

- CitationGraph
- recommended_next_reads
- frontier nodes

Coverage: `tests/workflow/test_example_citation_graph.py`

## `examples/pdf-to-markdown-demo/`

Mode: generated local fixture PDF.

Expected artifacts:

- PDFMarkdownOutput
- markdown artifact
- quality report
- cache hit test

Coverage: `tests/workflow/test_example_pdf_to_markdown.py`

## Release Rule

Examples must remain runnable in fake mode or local fixture mode. They must not require real API keys, real network calls, private sources, or private datasets.
