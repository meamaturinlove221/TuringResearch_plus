# TuringResearch MCP Tools

MCP server name: `turingresearch-plus`.

Round 3 defined the interface surface for all planned MCP namespaces. Later rounds added deterministic minimal implementations or dry-run paths for Core, PDF Markdown, Semantic Graph, North Star, Literature Survey, Vault, Context, Race Mode, SOP, and Paper pipeline tools. No default test requires real networking or API keys.

Every tool contract includes `tool_name`, `namespace`, `input_model`, `output_model`, `cache_behavior`, `network_behavior`, `error_behavior`, `evidence_requirement`, `required_tests`, and `implementation_status`.

## core.*

| Tool | Input | Output | Status |
| --- | --- | --- | --- |
| `core.health_check` | `CoreHealthCheckInput` | `CoreHealthCheckOutput` | `implemented_minimal` |
| `core.paper_searching` | `PaperSearchingInput` | `PaperSearchResult` | `contract_only` |
| `core.paper_fetching` | `PaperFetchingInput` | `PaperFetchResult` | `contract_only` |
| `core.paper_content` | `PaperContentInput` | `PaperContentOutput` | `implemented_minimal` |
| `core.paper_reference` | `PaperReferenceInput` | `PaperReferenceOutput` | `contract_only` |
| `core.paper_reading` | `PaperReadingInput` | `PaperReadingOutput` | `contract_only` |
| `core.web_fetching` | `WebFetchingInput` | `WebFetchResult` | `contract_only` |
| `core.web_content` | `WebContentInput` | `WebContentOutput` | `implemented_minimal` |
| `core.session_export` | `SessionExportInput` | `SessionExportOutput` | `contract_only` |
| `core.session_import` | `SessionImportInput` | `SessionImportOutput` | `contract_only` |
| `core.session_list` | `SessionListInput` | `SessionListOutput` | `implemented_minimal` |

## pdf.*

| Tool | Input | Output | Status |
| --- | --- | --- | --- |
| `pdf.inspect` | `PDFInspectInput` | `PDFInspectOutput` | `implemented_minimal` |
| `pdf.to_markdown` | `PDFMarkdownInput` | `PDFMarkdownOutput` | `implemented_minimal` |
| `pdf.batch_to_markdown` | `PDFBatchMarkdownInput` | `PDFBatchMarkdownOutput` | `contract_only` |
| `pdf.extract_figures` | `PDFFigureExtractInput` | `PDFAssetExtractionReport` | `implemented_minimal` |
| `pdf.extract_tables` | `PDFTableExtractInput` | `PDFAssetExtractionReport` | `implemented_minimal` |
| `pdf.ocr_pages` | `PDFOCRPagesInput` | `PDFOCRPagesOutput` | `contract_only` |
| `pdf.sectionize` | `PDFSectionizeInput` | `PDFAssetExtractionReport` | `implemented_minimal` |
| `pdf.cache_lookup` | `PDFCacheLookupInput` | `PDFMarkdownOutput` | `implemented_minimal` |
| `pdf.markdown_content` | `PDFMarkdownContentInput` | `PDFMarkdownContentOutput` | `implemented_minimal` |

## graph.*

| Tool | Input | Output | Status |
| --- | --- | --- | --- |
| `graph.paper_lookup` | `GraphPaperLookupInput` | `GraphPaperLookupOutput` | `implemented_minimal` |
| `graph.paper_batch` | `GraphPaperBatchInput` | `GraphPaperBatchOutput` | `implemented_minimal` |
| `graph.references` | `GraphReferencesInput` | `GraphReferencesOutput` | `implemented_minimal` |
| `graph.citations` | `GraphCitationsInput` | `GraphCitationsOutput` | `implemented_minimal` |
| `graph.recommendations` | `GraphRecommendationsInput` | `GraphRecommendationsOutput` | `implemented_minimal` |
| `graph.author` | `GraphAuthorInput` | `GraphAuthorOutput` | `implemented_minimal` |
| `graph.author_papers` | `GraphAuthorPapersInput` | `GraphAuthorPapersOutput` | `implemented_minimal` |
| `graph.citation_graph_expand` | `GraphCitationGraphExpandInput` | `GraphCitationGraphExpandOutput` | `implemented_minimal` |
| `graph.author_network` | `GraphAuthorNetworkInput` | `GraphAuthorNetworkOutput` | `implemented_minimal` |

## research.*

| Tool | Input | Output | Status |
| --- | --- | --- | --- |
| `research.north_star_init` | `ResearchNorthStarInitInput` | `ResearchNorthStarInitOutput` | `implemented_dry_run` |
| `research.research_brief_generate` | `ResearchResearchBriefGenerateInput` | `ResearchResearchBriefGenerateOutput` | `implemented_dry_run` |
| `research.survey_plan` | `ResearchSurveyPlanInput` | `ResearchSurveyPlanOutput` | `implemented_dry_run` |
| `research.survey_run` | `ResearchSurveyRunInput` | `ResearchSurveyRunOutput` | `implemented_dry_run` |
| `research.survey_status` | `ResearchSurveyStatusInput` | `ResearchSurveyStatusOutput` | `implemented_dry_run` |
| `research.survey_export` | `ResearchSurveyExportInput` | `ResearchSurveyExportOutput` | `implemented_dry_run` |
| `research.gap_analyze` | `ResearchGapAnalyzeInput` | `ResearchGapAnalyzeOutput` | `implemented_dry_run` |
| `research.insight_generate` | `ResearchInsightGenerateInput` | `ResearchInsightGenerateOutput` | `implemented_dry_run` |
| `research.boundary_map` | `ResearchBoundaryMapInput` | `ResearchBoundaryMapOutput` | `implemented_dry_run` |
| `research.sensitivity_probe` | `ResearchSensitivityProbeInput` | `ResearchSensitivityProbeOutput` | `implemented_dry_run` |
| `research.problem_reformulate` | `ResearchProblemReformulateInput` | `ResearchProblemReformulateOutput` | `implemented_dry_run` |
| `research.gap_prioritize` | `ResearchGapPrioritizeInput` | `ResearchGapPrioritizeOutput` | `implemented_dry_run` |
| `research.hypothesis_generate` | `ResearchHypothesisGenerateInput` | `ResearchHypothesisGenerateOutput` | `implemented_dry_run` |
| `research.hypothesis_operationalize` | `ResearchHypothesisOperationalizeInput` | `ResearchHypothesisOperationalizeOutput` | `implemented_dry_run` |
| `research.research_question_formulate` | `ResearchResearchQuestionFormulateInput` | `ResearchResearchQuestionFormulateOutput` | `implemented_dry_run` |
| `research.idea_generate` | `ResearchIdeaGenerateInput` | `ResearchIdeaGenerateOutput` | `implemented_dry_run` |
| `research.idea_quality_diversity_filter` | `ResearchIdeaQualityDiversityFilterInput` | `ResearchIdeaQualityDiversityFilterOutput` | `implemented_dry_run` |
| `research.candidate_score` | `ResearchCandidateScoreInput` | `ResearchCandidateScoreOutput` | `implemented_dry_run` |
| `research.portfolio_optimize` | `ResearchPortfolioOptimizeInput` | `ResearchPortfolioOptimizeOutput` | `implemented_dry_run` |
| `research.artifact_stress_test` | `ResearchArtifactStressTestInput` | `ResearchArtifactStressTestOutput` | `implemented_dry_run` |
| `research.experiment_design` | `ResearchExperimentDesignInput` | `ResearchExperimentDesignOutput` | `implemented_dry_run` |
| `research.implementation_plan` | `ResearchImplementationPlanInput` | `ResearchImplementationPlanOutput` | `implemented_dry_run` |
| `research.collision_risk_detect` | `PaperComparisonInput` | `CollisionRiskReport` | `implemented_minimal` |
| `research.run_ingest` | `RunIngestRequest` | `RunIngestReport` | `implemented_minimal` |
| `research.handoff_bundle_export` | `HandoffExportRequest` | `HandoffBundleManifest` | `implemented_minimal` |
| `research.handoff_bundle_import` | `HandoffImportRequest` | `HandoffBundleImportReport` | `implemented_minimal` |

## vault.*

| Tool | Input | Output | Status |
| --- | --- | --- | --- |
| `vault.search` | `VaultSearchInput` | `VaultSearchOutput` | `implemented_minimal` |
| `vault.ingest_source` | `VaultIngestSourceInput` | `VaultIngestSourceOutput` | `implemented_minimal` |
| `vault.compile_page` | `VaultCompilePageInput` | `VaultCompilePageOutput` | `implemented_minimal` |
| `vault.add_edge` | `VaultAddEdgeInput` | `VaultAddEdgeOutput` | `implemented_minimal` |
| `vault.query_graph` | `VaultQueryGraphInput` | `VaultQueryGraphOutput` | `implemented_minimal` |
| `vault.graph_stats` | `VaultGraphStatsInput` | `VaultGraphStatsOutput` | `implemented_minimal` |
| `vault.lint` | `VaultLintInput` | `VaultLintOutput` | `implemented_minimal` |
| `vault.edge_audit` | `VaultEdgeAuditInput` | `VaultEdgeAuditOutput` | `implemented_minimal` |

## context.*

| Tool | Input | Output | Status |
| --- | --- | --- | --- |
| `context.init` | `ContextInitInput` | `ContextInitOutput` | `implemented_minimal` |
| `context.checkpoint` | `ContextCheckpointInput` | `ContextCheckpointOutput` | `implemented_minimal` |
| `context.recover` | `ContextRecoverInput` | `ContextRecoverOutput` | `implemented_minimal` |
| `context.index` | `ContextIndexInput` | `ContextIndexOutput` | `implemented_minimal` |
| `context.summarize` | `ContextSummarizeInput` | `ContextSummarizeOutput` | `implemented_minimal` |

## race.*

| Tool | Input | Output | Status |
| --- | --- | --- | --- |
| `race.idea_extract` | `RaceIdeaExtractInput` | `RaceIdeaExtractOutput` | `implemented_minimal` |
| `race.source_hygiene_check` | `RaceSourceHygieneCheckInput` | `RaceSourceHygieneCheckOutput` | `implemented_minimal` |
| `race.priority_score` | `RacePriorityScoreInput` | `RacePriorityScoreOutput` | `implemented_minimal` |
| `race.feature_capsule_create` | `RaceFeatureCapsuleCreateInput` | `RaceFeatureCapsuleCreateOutput` | `implemented_minimal` |
| `race.architecture_box_build` | `RaceArchitectureBoxBuildInput` | `RaceArchitectureBoxBuildOutput` | `implemented_minimal` |
| `race.upstream_watch` | `RaceUpstreamWatchInput` | `RaceUpstreamWatchOutput` | `implemented_minimal` |
| `race.launch_gate_status` | `RaceLaunchGateStatusInput` | `RaceLaunchGateStatusOutput` | `contract_only` |

## paper.*

| Tool | Input | Output | Status |
| --- | --- | --- | --- |
| `paper.docflow_status` | `PaperDocflowStatusInput` | `PaperDocflowStatusOutput` | `implemented_minimal` |
| `paper.article_block_update` | `PaperArticleBlockUpdateInput` | `PaperArticleBlockUpdateOutput` | `implemented_minimal` |
| `paper.sop_graph_generate` | `PaperSopGraphGenerateInput` | `PaperSopGraphGenerateOutput` | `implemented_minimal` |
| `paper.figure_register` | `PaperFigureRegisterInput` | `PaperFigureRegisterOutput` | `implemented_minimal` |
| `paper.caption_generate` | `PaperCaptionGenerateInput` | `PaperCaptionGenerateOutput` | `implemented_minimal` |
| `paper.draft_generate` | `PaperDraftGenerateInput` | `PaperDraftGenerateOutput` | `implemented_dry_run` |
| `paper.missing_evidence` | `PaperMissingEvidenceInput` | `PaperMissingEvidenceOutput` | `implemented_dry_run` |
| `paper.latex_export` | `PaperLatexExportInput` | `PaperLatexExportOutput` | `implemented_minimal` |
| `paper.search_pipeline` | `ScholarPipelineRequest` | `ScholarPipelineResult` | `implemented_minimal` |
| `paper.reference_pipeline` | `ReferencePipelineRequest` | `ReferencePipelineResult` | `implemented_minimal` |
| `paper.three_pass_reading_plan` | `ThreePassReadingPlanInput` | `ThreePassReadingPlan` | `implemented_minimal` |

## Round 6 Semantic Graph

Round 6 implements `graph.*` through `src/turing_research_plus/semantic_graph/`. The service uses an adapter protocol and tests use a fake Semantic Scholar adapter. No real network calls or API keys are included.

Citation graph expansion supports backward references, forward citations, both directions, depth limits, max node limits, year filters, citation-count filters, open-access filters, duplicate node merge, frontier nodes, and recommended next reads.

## Release Notes

`implemented_minimal` means a local deterministic implementation exists for the release candidate. `implemented_dry_run` means the workflow produces structured fake-service output without real external calls. `contract_only` means the public tool name and schema are frozen, but implementation is intentionally deferred.
