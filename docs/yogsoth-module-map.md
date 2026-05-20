# TulingResearch Plus Yogsoth Module Map

Round 4 audits public `yogsoth-ai` repositories as architecture references for TulingResearch Plus. This document maps reusable public ideas into TulingResearch Plus Python modules, contracts, future skills, and lanes. It does not copy source code, prompts, skill files, schemas, or project naming.

## Sources Consulted

- [de-anthropocentric-research-engine](https://github.com/yogsoth-ai/de-anthropocentric-research-engine)
- [literature-engine](https://github.com/yogsoth-ai/literature-engine)
- [literature-survey](https://github.com/yogsoth-ai/literature-survey)
- [web-browsing](https://github.com/yogsoth-ai/web-browsing)
- [semantic-scholar-mcp](https://github.com/yogsoth-ai/semantic-scholar-mcp)
- [knowledge-acquisition](https://github.com/yogsoth-ai/knowledge-acquisition)
- [north-star-crystallization](https://github.com/yogsoth-ai/north-star-crystallization)
- [deep-insight](https://github.com/yogsoth-ai/deep-insight)
- [hypothesis-formation](https://github.com/yogsoth-ai/hypothesis-formation)
- [creative-ideation](https://github.com/yogsoth-ai/creative-ideation)
- [convergence](https://github.com/yogsoth-ai/convergence)
- [stress-test](https://github.com/yogsoth-ai/stress-test)
- [experiment-execution](https://github.com/yogsoth-ai/experiment-execution)
- [context-management](https://github.com/yogsoth-ai/context-management)
- [subagent-spawning](https://github.com/yogsoth-ai/subagent-spawning)
- [wiki-vault](https://github.com/yogsoth-ai/wiki-vault)
- [knowledge-structuring](https://github.com/yogsoth-ai/knowledge-structuring)

## Target TulingResearch Plus Modules

- `src/tuling_research_plus/survey/`
- `src/tuling_research_plus/semantic_graph/`
- `src/tuling_research_plus/north_star/`
- `src/tuling_research_plus/insight/`
- `src/tuling_research_plus/hypothesis/`
- `src/tuling_research_plus/ideation/`
- `src/tuling_research_plus/convergence/`
- `src/tuling_research_plus/stress/`
- `src/tuling_research_plus/experiment/`
- `src/tuling_research_plus/vault/`
- `src/tuling_research_plus/context/`
- `src/tuling_research_plus/subtask/`

## Cross-Cutting Patterns To Reuse

- Campaign, strategy, tactic, SOP layering as a typed workflow decomposition pattern.
- Strategy-book execution: workflows expose options and gates; runtime selects paths under explicit constraints.
- BudgetGate and StateLedger as first-class workflow invariants.
- Source and evidence hygiene gates before conclusions or implementation tasks.
- Context checkpoints and resumability through explicit files and ledger events.
- Adapterized external APIs with mocked network tests.
- Persistent vault as a typed graph of sources, concepts, claims, relations, questions, evidence, failures, and topics.

## Project Audits

### de-anthropocentric-research-engine

1. Original purpose: A single-clone autonomous research orchestration system that unifies many Yogsoth research skills and MCP integrations.
2. Original architecture: Markdown-skill ecosystem with orchestrator layer, Campaign -> Strategy -> Tactic -> SOP hierarchy, spec execution, backtracking, context protocol, and multiple MCP integrations.
3. Reusable concepts: Multi-layer workflow hierarchy, executable research specs, backtrack conditions, deviation bounds, strategy catalog.
4. Reusable modules: Orchestrator, campaign registry, spec model, strategy catalog, context protocol.
5. Do not transplant: Project philosophy branding, markdown skill files, npm/MCP package layout, external project names, autonomous behavior without TulingResearch gates.
6. Python equivalent: `src/tuling_research_plus/context/`, `src/tuling_research_plus/subtask/`, and campaign models already started under `src/tuling_research_plus/campaign/`.
7. Planned MCP tools: `research.north_star_init`, `research.survey_plan`, `research.survey_run`, `context.checkpoint`, `context.recover`.
8. Core service protocol dependency: Core content services, PDF Markdown service, graph adapter protocol, vault service protocol.
9. Test strategy: Contract tests for spec schemas, dry-run campaign routing, fake-service backtrack tests, StateLedger assertions.
10. Priority: P0 for orchestration contracts; P2 for autonomous routing.
11. Lane: `lanes/04_yogsoth_fusion.md` and `lanes/06_workflow_orchestration.md`.
12. Feature Capsule: No for the whole repo; yes for individual gates and spec recovery features.

### literature-engine

1. Original purpose: Enforce rigorous academic literature reading and prevent abstract-only conclusions.
2. Original architecture: Depth-tiered skills for overview, search, and research; each tier has a HARD-GATE tied to evidence depth and tool responsibility.
3. Reusable concepts: Evidence-depth tiers, full-text gate, paper summary versus raw full-text distinction, citation traversal responsibility matrix.
4. Reusable modules: Paper reading policy, literature content gate, source evidence classifier.
5. Do not transplant: AlphaXiv-specific workflow as a hard dependency, skill text, public endpoint assumptions, tool names.
6. Python equivalent: `src/tuling_research_plus/survey/` plus Core `core.paper_content`, `core.paper_reference`, `pdf.markdown_content`.
7. Planned MCP tools: `research.survey_plan`, `research.survey_run`, `core.paper_content`, `core.paper_reference`, `pdf.markdown_content`.
8. Core service protocol dependency: `CoreToolService`, PDF Markdown service, future paper adapter protocol.
9. Test strategy: Mocked paper adapter tests, local cache hit/miss, contract tests that block conclusions without EvidenceRef.
10. Priority: P0.
11. Lane: `lanes/04_yogsoth_fusion.md`.
12. Feature Capsule: Yes, as "full-text evidence gate".

### literature-survey

1. Original purpose: Autonomous academic literature survey across scoping, systematic, deep, narrative, and snowball paradigms.
2. Original architecture: Strategy-book pattern with three layers: strategies, tactics, SOPs; quantitative budgets, State Ledger, and deviation documentation.
3. Reusable concepts: Survey paradigms, paper budget floors, saturation detection, PRISMA-like flow outputs, lineage maps.
4. Reusable modules: SurveyPlan, SurveyRun, SurveyStatus, SurveyExport, saturation policy.
5. Do not transplant: Fixed paper counts, exact playbooks, repository skill structure, external MCP assumptions.
6. Python equivalent: `src/tuling_research_plus/survey/`.
7. Planned MCP tools: `research.survey_plan`, `research.survey_run`, `research.survey_status`, `research.survey_export`.
8. Core service protocol dependency: Core paper search/fetch/content protocols, graph citation protocols, PDF Markdown service.
9. Test strategy: Dry-run survey planning, fake paper service, BudgetGate floors, StateLedger event sequence, no-network unit tests.
10. Priority: P0.
11. Lane: `lanes/04_yogsoth_fusion.md`.
12. Feature Capsule: Yes.

### web-browsing

1. Original purpose: Enforce rigorous web research by separating snippet discovery from full-page content reading.
2. Original architecture: Two depth-tiered skills, discovery and full-page research, with HARD-GATE rules around evidence quality.
3. Reusable concepts: Snippet-only prohibition, full-page evidence requirement, discovery versus content separation.
4. Reusable modules: Web source hygiene, web content gate, cached web markdown service policy.
5. Do not transplant: Brave/Apify direct usage, external MCP config, web skill text.
6. Python equivalent: Core `core.web_content`; future Plus source hygiene under `src/tuling_research_plus/survey/` and `src/tuling_research_plus/context/`.
7. Planned MCP tools: `core.web_fetching`, `core.web_content`, `research.survey_run`.
8. Core service protocol dependency: Web fetching adapter protocol and local web content cache service.
9. Test strategy: Mock web adapter, local cache hit/miss, evidence gate tests that reject snippets as conclusions.
10. Priority: P1.
11. Lane: `lanes/02_core_reproduction.md` and `lanes/04_yogsoth_fusion.md`.
12. Feature Capsule: Yes, as "web source evidence gate".

### semantic-scholar-mcp

1. Original purpose: MCP server for Semantic Scholar paper metadata, citation tracing, author information, recommendations, and advanced search.
2. Original architecture: TypeScript MCP server exposing paper, batch, references, citations, recommendations, relevance search, author, and author papers tools.
3. Reusable concepts: Graph-oriented paper metadata model, batch lookup, citation graph expansion, author network surfaces.
4. Reusable modules: Semantic graph adapter protocol, paper lookup model, citation edge model.
5. Do not transplant: TypeScript server implementation, API client code, package names, direct network calls in tests.
6. Python equivalent: `src/tuling_research_plus/semantic_graph/`.
7. Planned MCP tools: `graph.paper_lookup`, `graph.paper_batch`, `graph.references`, `graph.citations`, `graph.recommendations`, `graph.author`, `graph.author_papers`, `graph.citation_graph_expand`, `graph.author_network`.
8. Core service protocol dependency: External graph adapter protocol with mocked network boundary.
9. Test strategy: Contract tests, mocked Semantic Scholar-like adapter, cache behavior tests, citation edge evidence tests.
10. Priority: P0 for contract; P1 for fake-service implementation.
11. Lane: `lanes/04_yogsoth_fusion.md`.
12. Feature Capsule: No; foundational adapter surface.

### knowledge-acquisition

1. Original purpose: Research intelligence pipeline covering literature survey, patent mining, benchmark archaeology, meta-analysis, and baseline establishment.
2. Original architecture: Entry router, five campaigns, 25 strategies, 15 tactics, about 50 SOPs, import SOPs, subagents, context checkpoints, and external MCP tools.
3. Reusable concepts: Knowledge acquisition as campaign family, domain-natural budget units, baseline inventory, benchmark validity audit.
4. Reusable modules: Survey orchestration, baseline artifact model, benchmark audit artifact model.
5. Do not transplant: Patent-specific workflows until adapters exist, fixed campaign counts, direct dependency on external MCP servers.
6. Python equivalent: `src/tuling_research_plus/survey/`, `src/tuling_research_plus/semantic_graph/`, `src/tuling_research_plus/context/`.
7. Planned MCP tools: `research.survey_plan`, `research.survey_run`, `research.survey_export`, `vault.ingest_source`, `vault.compile_page`.
8. Core service protocol dependency: Core paper/web content protocols, semantic graph protocol, vault service protocol.
9. Test strategy: Fake-service survey runs, BudgetGate target/current tests, StateLedger progress tests, artifact evidence checks.
10. Priority: P0 for survey subset; P3 for patent/meta-analysis extensions.
11. Lane: `lanes/04_yogsoth_fusion.md`.
12. Feature Capsule: Yes for baseline and benchmark audit modules.

### north-star-crystallization

1. Original purpose: Transform fuzzy research intent into a North Star statement and ResearchBrief.
2. Original architecture: Strategy-book pattern with cold/warm/hot strategies, six tactics, dialogue/subagent/import SOPs, and external skills.
3. Reusable concepts: Intent density routing, actor profile, landscape reconnaissance, obstacle analysis, goal decomposition, ResearchBrief.
4. Reusable modules: NorthStarInput, ActorProfile, ResearchBrief, GoalTree, ObstacleReport.
5. Do not transplant: Dialogue scripts, exact KAOS prompt flows, external web/paper requirements as mandatory behavior.
6. Python equivalent: `src/tuling_research_plus/north_star/`.
7. Planned MCP tools: `research.north_star_init`, `research.research_brief_generate`.
8. Core service protocol dependency: Core web content, paper content, semantic graph, context ledger.
9. Test strategy: Dry-run routing for cold/warm/hot inputs, fake landscape service, blocked missing evidence tests.
10. Priority: P1.
11. Lane: `lanes/04_yogsoth_fusion.md`.
12. Feature Capsule: Yes.

### deep-insight

1. Original purpose: Transform surface-level research gaps into structural understanding.
2. Original architecture: Five campaigns: gap analysis, insight generation, boundary analysis, sensitivity analysis, and problem reformulation.
3. Reusable concepts: Gap taxonomy, boundary mapping, sensitivity probes, reframing workflows, insight artifacts.
4. Reusable modules: GapAnalysis, InsightArtifact, BoundaryMap, SensitivityProbe, ProblemReformulation.
5. Do not transplant: Prompt methods verbatim, large campaign inventory, subagent SOP files.
6. Python equivalent: `src/tuling_research_plus/insight/`.
7. Planned MCP tools: `research.gap_analyze`, `research.insight_generate`, `research.boundary_map`, `research.sensitivity_probe`, `research.problem_reformulate`.
8. Core service protocol dependency: Survey outputs, semantic graph, vault, context ledger.
9. Test strategy: Contract tests for evidence-backed insight artifacts, fake survey inputs, dry-run workflow tests.
10. Priority: P1.
11. Lane: `lanes/04_yogsoth_fusion.md`.
12. Feature Capsule: Yes.

### hypothesis-formation

1. Original purpose: Turn prioritized gaps and insights into hypotheses and precise research questions.
2. Original architecture: Three campaigns for gap prioritization, hypothesis formulation, and research question formation; four-level hierarchy with budget enforcement.
3. Reusable concepts: Gap ranking, falsifiability criteria, competing hypothesis matrix, research question frameworks, operationalization.
4. Reusable modules: GapPriority, HypothesisCandidate, HypothesisOperationalization, ResearchQuestion.
5. Do not transplant: Exact AHP/PICO prompt playbooks, imported external skill paths, fixed strategy inventory.
6. Python equivalent: `src/tuling_research_plus/hypothesis/`.
7. Planned MCP tools: `research.gap_prioritize`, `research.hypothesis_generate`, `research.hypothesis_operationalize`, `research.research_question_formulate`.
8. Core service protocol dependency: Insight outputs, survey evidence, context ledger, vault storage.
9. Test strategy: Evidence requirement tests, falsifiability field contract tests, BudgetGate dry-run workflow tests.
10. Priority: P1.
11. Lane: `lanes/04_yogsoth_fusion.md`.
12. Feature Capsule: Yes.

### creative-ideation

1. Original purpose: Generate diverse solution spaces from research hypotheses.
2. Original architecture: Ten parallel creative campaigns with strategy/tactic/SOP hierarchy, State Ledgers, HARD-GATEs, and saturation detection.
3. Reusable concepts: Divergent idea generation, diversity filters, saturation stop, idea families, method provenance.
4. Reusable modules: IdeaGenerationPlan, IdeaCandidate, DiversityFilter, IdeationLedger.
5. Do not transplant: Named creativity method prompts verbatim, exhaustive campaign inventory, implementation planning.
6. Python equivalent: `src/tuling_research_plus/ideation/`.
7. Planned MCP tools: `research.idea_generate`, `research.idea_quality_diversity_filter`.
8. Core service protocol dependency: Hypothesis outputs, vault lookup, context ledger.
9. Test strategy: Dry-run generation contracts, diversity-score tests with fake inputs, Race Source Hygiene Gate compatibility tests.
10. Priority: P2.
11. Lane: `lanes/04_yogsoth_fusion.md` and `lanes/07_race_mode.md`.
12. Feature Capsule: Yes.

### convergence

1. Original purpose: Transform candidate sets into ranked selections, portfolios, and validated decisions.
2. Original architecture: Six campaigns for scoring, pairwise ranking, consensus, feasibility, optimization, and steel-manning.
3. Reusable concepts: Candidate scoring, portfolio optimization, pairwise consistency, decision audit, adversarial verification.
4. Reusable modules: CandidateScore, PortfolioPlan, ConvergenceDecision, DecisionAudit.
5. Do not transplant: Specific decision-method prompt recipes, fixed multi-campaign orchestration.
6. Python equivalent: `src/tuling_research_plus/convergence/`.
7. Planned MCP tools: `research.candidate_score`, `research.portfolio_optimize`.
8. Core service protocol dependency: Ideation outputs, stress-test outputs, BudgetGate, StateLedger.
9. Test strategy: Deterministic scoring contract tests, fake candidate fixtures, decision audit evidence checks.
10. Priority: P2.
11. Lane: `lanes/04_yogsoth_fusion.md`.
12. Feature Capsule: Yes.

### stress-test

1. Original purpose: Adversarially validate research artifacts and produce weakness-annotated reports.
2. Original architecture: Five campaigns for debate, red-teaming, failure anticipation, counterfactual probing, and boundary stress testing; hard constraints include BudgetGate, StateLedger, context checkpoints, and saturation detection.
3. Reusable concepts: Weakness taxonomy, severity classification, mitigation proposals, artifact stress reports.
4. Reusable modules: StressTestPlan, WeaknessReport, MitigationProposal, ArtifactStressResult.
5. Do not transplant: Adversarial prompt text, large multi-agent debate mechanics, claims without evidence.
6. Python equivalent: `src/tuling_research_plus/stress/`.
7. Planned MCP tools: `research.artifact_stress_test`.
8. Core service protocol dependency: Artifact store, vault service, context ledger.
9. Test strategy: Fake artifact stress test, severity schema tests, blocked missing evidence tests.
10. Priority: P2.
11. Lane: `lanes/04_yogsoth_fusion.md`.
12. Feature Capsule: Yes.

### experiment-execution

1. Original purpose: Design experiments, analyze constraints, plan scenarios, and execute result collection.
2. Original architecture: Four campaigns: experiment design, constraint analysis, scenario planning, and implementation planning; flat skills with frontmatter hierarchy.
3. Reusable concepts: ExperimentDesign, constraint analysis, scenario robustness, implementation planning, result collection envelope.
4. Reusable modules: ExperimentDesign, ConstraintReport, ScenarioPlan, ImplementationPlan, ExperimentReport.
5. Do not transplant: Execution automation, real experiment running, external MCP dependencies, any unverified procedure code.
6. Python equivalent: `src/tuling_research_plus/experiment/`.
7. Planned MCP tools: `research.experiment_design`, `research.implementation_plan`.
8. Core service protocol dependency: Hypothesis outputs, convergence decisions, context ledger, vault storage.
9. Test strategy: Contract tests for ExperimentReport prerequisite, dry-run design fixtures, blocked execution tests.
10. Priority: P3.
11. Lane: `lanes/08_paper_pipeline.md` and `lanes/04_yogsoth_fusion.md`.
12. Feature Capsule: Yes, but only after ExperimentReport schema stabilizes.

### context-management

1. Original purpose: Persist long-running research process and results as markdown checkpoints.
2. Original architecture: `context-init` and `context-checkpoint` skills, phase files, INDEX, plan-driven checkpoint triggers.
3. Reusable concepts: Checkpoint protocol, index file, session recovery material, write-only process log.
4. Reusable modules: ContextCheckpoint, ContextIndex, RecoverableContext.
5. Do not transplant: Minimum 500-line requirement, exact file templates, script implementation.
6. Python equivalent: `src/tuling_research_plus/context/`.
7. Planned MCP tools: `context.init`, `context.checkpoint`, `context.recover`, `context.index`, `context.summarize`.
8. Core service protocol dependency: StateLedger, artifact schema, local filesystem adapter.
9. Test strategy: Local filesystem fake tests, checkpoint append tests, recovery index tests.
10. Priority: P0.
11. Lane: `lanes/06_workflow_orchestration.md`.
12. Feature Capsule: No; foundational runtime capability.

### subagent-spawning

1. Original purpose: Standardize subagent dispatch for SOPs with role-specific prompts and inherited tools.
2. Original architecture: Pure markdown spawn-agent skill; SOP declares `execution: subagent`, prompt path, input, and output.
3. Reusable concepts: Subtask declaration schema, role prompt metadata, output contract, isolated execution policy.
4. Reusable modules: SubtaskSpec, SubtaskRuntime, SubtaskResult, SubtaskPolicy.
5. Do not transplant: Automatic subagent spawning in this single-window project, Opus model assumption, prompt files.
6. Python equivalent: `src/tuling_research_plus/subtask/`.
7. Planned MCP tools: No public MCP namespace initially; supports `research.*` workflows internally through contract models.
8. Core service protocol dependency: StateLedger and BudgetGate; no Core tool dependency required.
9. Test strategy: Dry-run subtask scheduling, dependency graph validation, no actual second-window spawning.
10. Priority: P0 for model contracts; P3 for runtime.
11. Lane: `lanes/06_workflow_orchestration.md`.
12. Feature Capsule: No.

### wiki-vault

1. Original purpose: Structured wiki and knowledge graph MCP server with BM25 search, typed edges, linting, and graph stats.
2. Original architecture: MCP server tools over filesystem vault, index module, graph module, lint module, markdown pages with YAML frontmatter and wikilinks.
3. Reusable concepts: Typed vault entities, immutable sources, evolving wiki pages, edge audit, graph stats, orphan detection, search-before-create.
4. Reusable modules: VaultRecord, VaultEdge, VaultIndex, VaultLintReport, VaultGraphStats.
5. Do not transplant: TypeScript implementation, package name, direct file schema without TulingResearch contracts.
6. Python equivalent: `src/tuling_research_plus/vault/`.
7. Planned MCP tools: `vault.search`, `vault.ingest_source`, `vault.compile_page`, `vault.add_edge`, `vault.query_graph`, `vault.graph_stats`, `vault.lint`, `vault.edge_audit`.
8. Core service protocol dependency: Local vault storage protocol; optionally Core content services for source ingestion.
9. Test strategy: Local temp vault tests, edge dedup tests, lint fixture tests, search fake index tests.
10. Priority: P0.
11. Lane: `lanes/05_vault_memory.md`.
12. Feature Capsule: Yes.

### knowledge-structuring

1. Original purpose: Public repository description frames it as structured knowledge construction; current public entry material overlaps heavily with wiki-vault concepts.
2. Original architecture: Entry routing to knowledge compilation and vault maintenance, SOPs for search, graph query, add edge, ingest source, compile page, lint fix, plus typed entity and edge models.
3. Reusable concepts: Ontology-like entity typing, causal/argument/relationship modeling as typed graph structures, search-before-create policy.
4. Reusable modules: KnowledgeStructure, OntologyNode, ArgumentMap, CausalEdge, EvidenceEdge.
5. Do not transplant: Any unclear or duplicated repository content without verification, TypeScript server code, external branding.
6. Python equivalent: `src/tuling_research_plus/semantic_graph/` and `src/tuling_research_plus/vault/`.
7. Planned MCP tools: `vault.add_edge`, `vault.query_graph`, `vault.edge_audit`, `graph.citation_graph_expand`.
8. Core service protocol dependency: Vault service protocol and semantic graph adapter protocol.
9. Test strategy: Typed-edge schema tests, local graph traversal fixtures, evidence-preservation tests.
10. Priority: P2.
11. Lane: `lanes/05_vault_memory.md` and `lanes/04_yogsoth_fusion.md`.
12. Feature Capsule: Yes.

## Resulting Future Skills

- `tulingresearch-fusion-literature-survey`
- `tulingresearch-fusion-semantic-graph`
- `tulingresearch-fusion-north-star`
- `tulingresearch-fusion-deep-insight`
- `tulingresearch-fusion-hypothesis-formation`
- `tulingresearch-fusion-creative-ideation`
- `tulingresearch-fusion-convergence`
- `tulingresearch-fusion-stress-test`
- `tulingresearch-fusion-experiment-execution`
- `tulingresearch-fusion-wiki-vault`
- `tulingresearch-fusion-context-management`
- `tulingresearch-fusion-subtask-runtime`

## Round 4 Decision

TulingResearch Plus should reuse architecture patterns, workflow decomposition, contracts, quality gates, evidence rules, and data-model ideas. It must not copy incompatible code, prompt text, repository structure, package naming, or external MCP runtime assumptions.
