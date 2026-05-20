# TulingResearch Plus v0.1.0 Release Candidate Report

Date: 2026-05-20

## 1. Project Summary

TulingResearch Plus is a Python MCP-first research workflow engine. It provides local Core tools, PDF Markdown conversion, fake-adapter semantic graph workflows, depth-gated literature survey, claim-evidence Vault, hypothesis-to-experiment workflows, Race Mode idea capture, Feature Capsule skeletons, SOP graphs, and paper/figure pipeline dry-runs.

Packages:

- Core: `tuling_research`
- Plus: `tuling_research_plus`
- MCP server: `tulingresearch-plus`

## 2. Current Version Scope

Version: `v0.1.0` release candidate.

Included:

- Core local tools
- PDF Markdown Phase A
- Semantic Graph fake adapter / dry-run
- Literature Survey dry-run
- Vault / Context basics
- Race Mode basics
- Feature Capsule skeletons
- DocFlow
- Figure registry
- Paper draft gate
- Contract tests
- Workflow dry-run tests
- Examples fake mode
- Package metadata and local entry points
- CI test/lint matrix

Excluded:

- Default live API execution
- Heavy OCR
- Complex PDF layout parsing
- Full automatic paper generation
- Real GPU experiment execution
- Automatic PyPI publishing
- Private or unauthorized source idea implementation

## 3. Completed Features

- Contract-first MCP namespaces for `core.*`, `pdf.*`, `graph.*`, `research.*`, `vault.*`, `context.*`, `race.*`, and `paper.*`.
- STDIO-safe local MCP smoke server and tool registry.
- Deterministic fake-service workflows and examples.
- Source Hygiene Gate and Race Mode guardrails.
- Paper draft gate that blocks without `ExperimentReport`.
- Local packaging, entry points, docs, CI, and release gates.

## 4. Planned But Incomplete Features

- Contract-only Core paper/web fetching and richer reading tools.
- PDF batch conversion, figure/table extraction, OCR, and richer sectionization.
- Live graph/paper/web adapters behind explicit configuration.
- Full automatic paper drafting once real ExperimentReport artifacts exist.
- Hosted Vault/search backends and production deployment packaging.

## 5. MCP Tools Status Table

Summary by namespace:

| Namespace | Tool count |
| --- | --- |
| context | 5 |
| core | 11 |
| graph | 9 |
| paper | 8 |
| pdf | 9 |
| race | 7 |
| research | 22 |
| vault | 8 |

Summary by implementation status:

| Status | Count |
| --- | --- |
| contract_only | 13 |
| implemented_dry_run | 24 |
| implemented_minimal | 42 |

| Tool name | Namespace | Implementation status | Test status | Docs status | Release status |
| --- | --- | --- | --- | --- | --- |
| core.health_check | core | implemented_minimal | covered | documented | included in v0.1.0 |
| core.paper_searching | core | contract_only | covered | documented | planned after v0.1.0 |
| core.paper_fetching | core | contract_only | covered | documented | planned after v0.1.0 |
| core.paper_content | core | implemented_minimal | covered | documented | included in v0.1.0 |
| core.paper_reference | core | contract_only | covered | documented | planned after v0.1.0 |
| core.paper_reading | core | contract_only | covered | documented | planned after v0.1.0 |
| core.web_fetching | core | contract_only | covered | documented | planned after v0.1.0 |
| core.web_content | core | implemented_minimal | covered | documented | included in v0.1.0 |
| core.session_export | core | contract_only | covered | documented | planned after v0.1.0 |
| core.session_import | core | contract_only | covered | documented | planned after v0.1.0 |
| core.session_list | core | implemented_minimal | covered | documented | included in v0.1.0 |
| pdf.inspect | pdf | implemented_minimal | covered | documented | included in v0.1.0 |
| pdf.to_markdown | pdf | implemented_minimal | covered | documented | included in v0.1.0 |
| pdf.batch_to_markdown | pdf | contract_only | covered | documented | planned after v0.1.0 |
| pdf.extract_figures | pdf | contract_only | covered | documented | planned after v0.1.0 |
| pdf.extract_tables | pdf | contract_only | covered | documented | planned after v0.1.0 |
| pdf.ocr_pages | pdf | contract_only | covered | documented | planned after v0.1.0 |
| pdf.sectionize | pdf | contract_only | covered | documented | planned after v0.1.0 |
| pdf.cache_lookup | pdf | implemented_minimal | covered | documented | included in v0.1.0 |
| pdf.markdown_content | pdf | implemented_minimal | covered | documented | included in v0.1.0 |
| graph.paper_lookup | graph | implemented_minimal | covered | documented | included in v0.1.0 |
| graph.paper_batch | graph | implemented_minimal | covered | documented | included in v0.1.0 |
| graph.references | graph | implemented_minimal | covered | documented | included in v0.1.0 |
| graph.citations | graph | implemented_minimal | covered | documented | included in v0.1.0 |
| graph.recommendations | graph | implemented_minimal | covered | documented | included in v0.1.0 |
| graph.author | graph | implemented_minimal | covered | documented | included in v0.1.0 |
| graph.author_papers | graph | implemented_minimal | covered | documented | included in v0.1.0 |
| graph.citation_graph_expand | graph | implemented_minimal | covered | documented | included in v0.1.0 |
| graph.author_network | graph | implemented_minimal | covered | documented | included in v0.1.0 |
| research.north_star_init | research | implemented_dry_run | covered | documented | included in v0.1.0 |
| research.research_brief_generate | research | implemented_dry_run | covered | documented | included in v0.1.0 |
| research.survey_plan | research | implemented_dry_run | covered | documented | included in v0.1.0 |
| research.survey_run | research | implemented_dry_run | covered | documented | included in v0.1.0 |
| research.survey_status | research | implemented_dry_run | covered | documented | included in v0.1.0 |
| research.survey_export | research | implemented_dry_run | covered | documented | included in v0.1.0 |
| research.gap_analyze | research | implemented_dry_run | covered | documented | included in v0.1.0 |
| research.insight_generate | research | implemented_dry_run | covered | documented | included in v0.1.0 |
| research.boundary_map | research | implemented_dry_run | covered | documented | included in v0.1.0 |
| research.sensitivity_probe | research | implemented_dry_run | covered | documented | included in v0.1.0 |
| research.problem_reformulate | research | implemented_dry_run | covered | documented | included in v0.1.0 |
| research.gap_prioritize | research | implemented_dry_run | covered | documented | included in v0.1.0 |
| research.hypothesis_generate | research | implemented_dry_run | covered | documented | included in v0.1.0 |
| research.hypothesis_operationalize | research | implemented_dry_run | covered | documented | included in v0.1.0 |
| research.research_question_formulate | research | implemented_dry_run | covered | documented | included in v0.1.0 |
| research.idea_generate | research | implemented_dry_run | covered | documented | included in v0.1.0 |
| research.idea_quality_diversity_filter | research | implemented_dry_run | covered | documented | included in v0.1.0 |
| research.candidate_score | research | implemented_dry_run | covered | documented | included in v0.1.0 |
| research.portfolio_optimize | research | implemented_dry_run | covered | documented | included in v0.1.0 |
| research.artifact_stress_test | research | implemented_dry_run | covered | documented | included in v0.1.0 |
| research.experiment_design | research | implemented_dry_run | covered | documented | included in v0.1.0 |
| research.implementation_plan | research | implemented_dry_run | covered | documented | included in v0.1.0 |
| vault.search | vault | implemented_minimal | covered | documented | included in v0.1.0 |
| vault.ingest_source | vault | implemented_minimal | covered | documented | included in v0.1.0 |
| vault.compile_page | vault | implemented_minimal | covered | documented | included in v0.1.0 |
| vault.add_edge | vault | implemented_minimal | covered | documented | included in v0.1.0 |
| vault.query_graph | vault | implemented_minimal | covered | documented | included in v0.1.0 |
| vault.graph_stats | vault | implemented_minimal | covered | documented | included in v0.1.0 |
| vault.lint | vault | implemented_minimal | covered | documented | included in v0.1.0 |
| vault.edge_audit | vault | implemented_minimal | covered | documented | included in v0.1.0 |
| context.init | context | implemented_minimal | covered | documented | included in v0.1.0 |
| context.checkpoint | context | implemented_minimal | covered | documented | included in v0.1.0 |
| context.recover | context | implemented_minimal | covered | documented | included in v0.1.0 |
| context.index | context | implemented_minimal | covered | documented | included in v0.1.0 |
| context.summarize | context | implemented_minimal | covered | documented | included in v0.1.0 |
| race.idea_extract | race | implemented_minimal | covered | documented | included in v0.1.0 |
| race.source_hygiene_check | race | implemented_minimal | covered | documented | included in v0.1.0 |
| race.priority_score | race | implemented_minimal | covered | documented | included in v0.1.0 |
| race.feature_capsule_create | race | implemented_minimal | covered | documented | included in v0.1.0 |
| race.architecture_box_build | race | implemented_minimal | covered | documented | included in v0.1.0 |
| race.upstream_watch | race | implemented_minimal | covered | documented | included in v0.1.0 |
| race.launch_gate_status | race | contract_only | covered | documented | planned after v0.1.0 |
| paper.docflow_status | paper | implemented_minimal | covered | documented | included in v0.1.0 |
| paper.article_block_update | paper | implemented_minimal | covered | documented | included in v0.1.0 |
| paper.sop_graph_generate | paper | implemented_minimal | covered | documented | included in v0.1.0 |
| paper.figure_register | paper | implemented_minimal | covered | documented | included in v0.1.0 |
| paper.caption_generate | paper | implemented_minimal | covered | documented | included in v0.1.0 |
| paper.draft_generate | paper | implemented_dry_run | covered | documented | included in v0.1.0 |
| paper.missing_evidence | paper | implemented_dry_run | covered | documented | included in v0.1.0 |
| paper.latex_export | paper | implemented_minimal | covered | documented | included in v0.1.0 |

## 6. Contracts Status Table

| Contract file | Contract name | Version | Status | Tool count | Test status |
| --- | --- | --- | --- | --- | --- |
| contracts/artifact_schema.yaml | tulingresearch.artifact_schema | 0.2.0 | draft | 0 | covered by contract/schema integrity tests |
| contracts/core_tools.yaml | tulingresearch.core_tools | 0.2.0 | draft | 11 | covered by contract/schema integrity tests |
| contracts/error_schema.yaml | tulingresearch.error_schema | 0.2.0 | draft | 0 | covered by contract/schema integrity tests |
| contracts/fusion_workflows.yaml | tulingresearch.fusion_workflows | 0.2.0 | draft | 36 | covered by contract/schema integrity tests |
| contracts/paper_pipeline.yaml | tulingresearch.paper_pipeline | 0.2.0 | draft | 8 | covered by contract/schema integrity tests |
| contracts/pdf_markdown.yaml | tulingresearch.pdf_markdown | 0.2.0 | draft | 9 | covered by contract/schema integrity tests |
| contracts/race_features.yaml | tulingresearch.race_features | 0.2.0 | draft | 7 | covered by contract/schema integrity tests |
| contracts/vault_schema.yaml | tulingresearch.vault_schema | 0.3.0 | draft | 8 | covered by contract/schema integrity tests |

## 7. Tests Summary

Status: passed on 2026-05-20.

Validation commands:

```powershell
python -m pytest        # 301 passed
python -m ruff check .  # All checks passed
python -m mypy src      # Success: no issues found in 150 source files
```

Name integrity scan: passed with no forbidden naming hits.

## 8. Examples Summary

Release examples are fake-mode or local fixture dry-runs:

- `examples/vggt-human-prior-survey/`: ResearchBrief, LiteratureSurveyArtifact, GapReport, HypothesisPortfolio, ExperimentPlan.
- `examples/smplx-feature-adapter-hypothesis/`: HypothesisPortfolio, IdeaPortfolio, DecisionReport, StressTestReport.
- `examples/citation-graph-demo/`: CitationGraph, recommended next reads, frontier nodes.
- `examples/pdf-to-markdown-demo/`: PDFMarkdownOutput, markdown artifact, quality report, cache hit test.

## 9. PDF Markdown Status

PDF Markdown Phase A is included. It supports local PDF paths, inspection, conversion to Markdown, cache lookup, Markdown content retrieval, page maps, warnings, quality score, and cache-hit behavior. Heavy OCR and complex layout parsing are not included.

## 10. Race Mode Status

Race Mode basics are included: Source Hygiene Gate, Idea Radar, Priority Elevator, Feature Capsule skeleton generation, 16-box architecture builder, and Upstream Watch. Implementation work is blocked unless source material is public or authorized and license-compatible.

## 11. Paper Pipeline Status

Paper pipeline basics are included: DocFlow Article Blocks, SOP graph generation, figure registry, caption generation, missing-evidence reports, draft gate, and LaTeX export. Full draft generation remains gated and does not fabricate experiment results.

## 12. Source Hygiene Policy

TulingResearch Plus allows public repos, public READMEs, public issues, public release notes, user-owned notes, and authorized transcripts. It blocks private repository content, leaked roadmap material, NDA content, proprietary code, and copied implementation details from incompatible licenses.

Safe modes are independent clean-room implementation, concept-level reimplementation, compatible-license reuse, and documentation-only watch.

## 13. Known Limitations

- Default execution does not perform real networking.
- PDF OCR remains future work.
- Complex PDF layout parsing remains future work.
- Paper draft generation does not fabricate experimental results.
- Live API adapters require later explicit configuration.
- Current release primarily supports fake mode and dry-run mode.
- The project does not copy code from incompatible-license projects.

## 14. Release Blockers

Status: no active release blocker after final Round 23 validation.

All default tests, lint, typing, and naming scans passed.

## 15. v0.1.0 Go / No-Go Recommendation

Recommendation: GO for `v0.1.0` release preparation.

Rationale: the release candidate has frozen package names, MCP server name, contracts, public docs, examples, CI configuration, local packaging, and default test gates. Remaining limitations are documented and are not release blockers because they are explicitly outside `v0.1.0` scope.
