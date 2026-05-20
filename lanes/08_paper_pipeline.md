# Lane 08: Paper Pipeline

## Scope

Define ExperimentReport, ArticleBlock, and PaperDraftRequest boundaries.

## Outputs

- `contracts/paper_pipeline.yaml`
- `src/tuling_research_plus/paper/models.py`
- `tests/unit/test_article_block.py`

## Status

Phase 1 complete. Paper draft requests are blocked without ExperimentReport.

## Round 13A Update

2026-05-19: Implemented DocFlow Article Blocks for TulingResearch Plus under `src/tuling_research_plus/paper/`.

Article blocks:

- `research_brief`
- `related_work`
- `method_design`
- `experiments`
- `paper_draft`

Inputs tracked by the readiness model:

- `ResearchBrief`
- `LiteratureSurveyArtifact`
- `GapReport`
- `HypothesisPortfolio`
- `IdeaPortfolio`
- `DecisionReport`
- `ExperimentPlan`
- `StressTestReport`
- `ExperimentReport`
- `PDFMarkdownOutput`

Hard gates:

- `paper_draft` is blocked until `ExperimentReport` exists.
- Blocks with missing `required_figures` are not ready.
- Blocks without EvidenceRef entries appear in the missing evidence report.

Created local paper planning artifacts:

- `paper/blocks/01_research_brief.md`
- `paper/blocks/02_related_work.md`
- `paper/blocks/03_method_design.md`
- `paper/blocks/04_experiments.md`
- `paper/blocks/05_paper_draft.md`
- `paper/docflow.mmd`

Thin wrappers now cover `paper.docflow_status`, `paper.article_block_update`, and `paper.missing_evidence`. Tests cover missing upstream artifacts, readiness calculation, graph generation, missing evidence, required figure blocking, and the ExperimentReport draft gate.

## Round 13B Update

2026-05-19: Implemented the SOP Graph Generator under `src/tuling_research_plus/sop/`.

Supported graph types:

- campaign graph
- feature graph
- paper graph
- experiment graph
- release graph

Each `SOPGraph` records nodes, edges, input artifacts, output artifacts, tools, quality gates, and failure gates. The generator can emit Mermaid `.mmd` text, Markdown SOP documents, optional repo-scoped skill skeletons, and optional Codex prompts.

Created default graph artifacts:

- `sop_graphs/campaign_graphs/campaign_default.mmd`
- `sop_graphs/campaign_graphs/campaign_default.md`
- `sop_graphs/feature_graphs/feature_default.mmd`
- `sop_graphs/feature_graphs/feature_default.md`
- `sop_graphs/paper_graphs/paper_default.mmd`
- `sop_graphs/paper_graphs/paper_default.md`

Thin wrapper `paper.sop_graph_generate` now returns a JSON payload with graph, Mermaid text, SOP Markdown, and optional skill/prompt outputs. Tests cover campaign graph generation, feature graph generation, quality/failure gates, and Mermaid rendering.

## Round 14A Update

2026-05-19: Implemented the Figure Asset Pipeline under `src/tuling_research_plus/paper/`.

Managed asset inputs:

- Mermaid files
- SVG files
- PNG files
- CSV tables
- PDF extracted figures
- PDF extracted tables
- experiment result JSON
- architecture docs
- SOP graphs

Each `FigureAsset` records figure id, title, source file, stable SVG/PNG outputs, caption, linked article blocks, status, asset kind, and original PDF source when applicable.

Rules now enforced:

- No orphan figure.
- Every paper figure must have caption.
- Every figure must link to at least one ArticleBlock.
- Generated diagrams receive stable filenames under `paper/figures/`.
- PDF extracted figures/tables must record `original_pdf_source`.

Created asset roots and indexes:

- `paper/paper_asset_registry.yaml`
- `paper/figures/`
- `paper/captions/`
- `paper/tables/`
- `paper/figure_index.md`

Thin wrappers now cover `paper.figure_register` and `paper.caption_generate`. Tests cover registry validation, orphan detection, missing captions, article-block links, PDF extracted figure provenance, and evidence-backed caption generation.

## Round 14B Update

2026-05-19: Implemented the Paper Writing Pipeline Gate under `src/tuling_research_plus/paper/`.

Hard gate inputs:

- `ResearchBrief`
- `LiteratureSurveyArtifact`
- `MethodDesign`
- `ExperimentPlan`
- `ExperimentReport`
- `FigureAssetRegistry`

Generated paper sections:

- Abstract
- Introduction
- Related Work
- Method
- Experiments
- Results
- Limitations
- Conclusion
- Appendix

Gate behavior:

- If `ExperimentReport` is absent, no complete `paper_draft` is generated.
- Missing artifacts, evidence, figures, tables, captions, and stress test results are reported.
- Method section must link architecture figures.
- Experiment and Results sections must link metrics/tables from the supplied ExperimentReport and FigureAsset registry.
- Limitations must include stress test results.
- Result text is constrained to supplied ExperimentReport metrics; no fabricated result claims are generated.

Created draft artifacts:

- `paper/draft/paper_draft.md`
- `paper/draft/section_status.yaml`
- `paper/draft/missing_evidence.md`

Thin wrappers now cover `paper.draft_generate`, writing-gate `paper.missing_evidence`, and `paper.latex_export`. Tests cover draft blocking without ExperimentReport, section status generation, missing evidence detection, method figure references, no fabricated result text, and LaTeX export.
