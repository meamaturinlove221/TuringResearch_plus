# TuringResearch Plus Tool Namespace Freeze

MCP server: `turingresearch-plus`

Version: `v0.1.0`

This document freezes the MCP tool namespace surface for TuringResearch Plus.

## Frozen Namespaces

- `core.*`
- `pdf.*`
- `graph.*`
- `research.*`
- `vault.*`
- `context.*`
- `race.*`
- `paper.*`

## core.*

- `core.health_check`
- `core.paper_searching`
- `core.paper_fetching`
- `core.paper_content`
- `core.paper_reference`
- `core.paper_reading`
- `core.web_fetching`
- `core.web_content`
- `core.session_export`
- `core.session_import`
- `core.session_list`

## pdf.*

- `pdf.inspect`
- `pdf.to_markdown`
- `pdf.batch_to_markdown`
- `pdf.extract_figures`
- `pdf.extract_tables`
- `pdf.ocr_pages`
- `pdf.sectionize`
- `pdf.cache_lookup`
- `pdf.markdown_content`

## graph.*

- `graph.paper_lookup`
- `graph.paper_batch`
- `graph.references`
- `graph.citations`
- `graph.recommendations`
- `graph.author`
- `graph.author_papers`
- `graph.citation_graph_expand`
- `graph.author_network`

## research.*

- `research.north_star_init`
- `research.research_brief_generate`
- `research.survey_plan`
- `research.survey_run`
- `research.survey_status`
- `research.survey_export`
- `research.gap_analyze`
- `research.insight_generate`
- `research.boundary_map`
- `research.sensitivity_probe`
- `research.problem_reformulate`
- `research.gap_prioritize`
- `research.hypothesis_generate`
- `research.hypothesis_operationalize`
- `research.research_question_formulate`
- `research.idea_generate`
- `research.idea_quality_diversity_filter`
- `research.candidate_score`
- `research.portfolio_optimize`
- `research.artifact_stress_test`
- `research.experiment_design`
- `research.implementation_plan`

## vault.*

- `vault.search`
- `vault.ingest_source`
- `vault.compile_page`
- `vault.add_edge`
- `vault.query_graph`
- `vault.graph_stats`
- `vault.lint`
- `vault.edge_audit`

## context.*

- `context.init`
- `context.checkpoint`
- `context.recover`
- `context.index`
- `context.summarize`

## race.*

- `race.idea_extract`
- `race.source_hygiene_check`
- `race.priority_score`
- `race.feature_capsule_create`
- `race.architecture_box_build`
- `race.upstream_watch`
- `race.launch_gate_status`

## paper.*

- `paper.docflow_status`
- `paper.article_block_update`
- `paper.sop_graph_generate`
- `paper.figure_register`
- `paper.caption_generate`
- `paper.draft_generate`
- `paper.missing_evidence`
- `paper.latex_export`

## Implementation Status Source

Implementation status for each tool is recorded in `docs/mcp-tools.md`.

`contract_only` tools are namespace-stable but not production-implemented in `v0.1.0`.

`implemented_minimal` and `implemented_dry_run` tools are covered by unit, contract, or workflow tests and do not require real network access.

## Freeze Rule

New tool names, removed tool names, renamed namespaces, or changed MCP server naming are blocked during release freeze unless they fix a release-blocking bug.
