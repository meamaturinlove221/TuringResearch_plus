# Lane 04: Yogsoth Fusion

## Scope

Map public research workflow ideas into TulingResearch Plus Fusion concepts while preserving TulingResearch naming.

## Outputs

- `docs/yogsoth-module-map.md`
- `contracts/fusion_workflows.yaml`
- `src/tuling_research_plus/campaign/models.py`

## Status

Phase 1 complete. This lane contains mapping and boundary models only.

## Round 4 Update

2026-05-19: Completed Yogsoth module audit for public repositories listed in `docs/yogsoth-module-map.md`.

Created or updated:

- `docs/yogsoth-module-map.md`
- `docs/fusion-priority.md`
- `docs/reuse-boundary.md`

Key decisions:

- Reuse architecture ideas, workflow patterns, contracts, quality gates, and data-model concepts only.
- Do not copy external code, prompt text, repository structure, or names.
- Prioritize `context`, `subtask`, `survey`, `semantic_graph`, and `vault` as P0.
- Keep all future Python module names under `src/tuling_research_plus/`.
- Treat all external APIs as adapter protocols with mocked tests.

## Round 6 Update

2026-05-19: Implemented the TulingResearch Plus Semantic Graph layer under `src/tuling_research_plus/semantic_graph/`.

Implemented graph tools through a service and adapter boundary:

- `graph.paper_lookup`
- `graph.paper_batch`
- `graph.references`
- `graph.citations`
- `graph.recommendations`
- `graph.author`
- `graph.author_papers`
- `graph.citation_graph_expand`
- `graph.author_network`

Citation graph expansion supports backward references, forward citations, both directions, depth limit, max node limit, year filter, citation count filter, open access filter, duplicate node merge, frontier nodes, and recommended next reads.

Tests use fake Semantic Scholar adapters only. No API keys, real network calls, or external API implementations were added.

## Round 7 Update

2026-05-19: Implemented the TulingResearch Plus Literature Survey workflow under `src/tuling_research_plus/survey/`.

Supported strategies:

- `scoping_survey`
- `systematic_survey`
- `deep_survey`
- `narrative_review`
- `snowball_survey`

Implemented tool wrappers:

- `research.survey_plan`
- `research.survey_run`
- `research.survey_status`
- `research.survey_export`

Hard gates now cover overview conclusion blocking, abstract-only survey blocking, deep survey `full_text_ratio`, PDF Markdown full-text counting, snowball citation expansion lineage, and evidence-backed final gaps.

All service dependencies are Protocol boundaries with fake services in tests. No Core internals or real network calls were used.

## Round 9A Update

2026-05-19: Implemented the TulingResearch Plus North Star workflow under `src/tuling_research_plus/north_star/`.

Implemented outputs:

- `NorthStarStatement`
- `ResearchBrief`
- `GoalTree`
- `ObstacleMap`
- `DirectionCandidates`

Implemented tool wrappers:

- `research.north_star_init`
- `research.research_brief_generate`
- `research.goal_decompose`
- `research.obstacle_analyze`
- `research.direction_rank`

The workflow supports cold-start, warm-start, and hot-start intent shaping, uses fake paper/web services behind Protocol boundaries, and backtracks when obstacle analysis rejects the top direction. No Core internals or real network calls were used.

## Round 9B Update

2026-05-19: Implemented the TulingResearch Plus Deep Insight workflow under `src/tuling_research_plus/insight/`.

Implemented outputs:

- `GapValidationReport`
- `InsightReport`
- `BoundaryMap`
- `SensitivityReport`
- `ReformulatedProblemSet`

Implemented tool wrappers:

- `research.gap_analyze`
- `research.insight_generate`
- `research.boundary_map`
- `research.sensitivity_probe`
- `research.problem_reformulate`

Quality gates now enforce evidence-backed gaps, insights with supporting and contradicting evidence, boundary maps with valid and invalid conditions, sensitivity reports with load-bearing assumptions, and reformulations that state both changes and invariants.

The workflow uses fake survey artifacts in tests and does not call a network service or LLM.

## Round 9C Update

2026-05-19: Implemented the TulingResearch Plus Hypothesis Formation workflow under `src/tuling_research_plus/hypothesis/`.

Implemented outputs:

- `GapPriorityReport`
- `HypothesisSet`
- `OperationalizedHypothesis`
- `ResearchQuestion`
- `HypothesisPortfolio`

Implemented tool wrappers:

- `research.gap_prioritize`
- `research.hypothesis_generate`
- `research.hypothesis_operationalize`
- `research.research_question_formulate`
- `research.hypothesis_portfolio_build`

Each generated hypothesis includes statement, mechanism, independent variables, dependent variables, control variables, falsifiability criteria, success criteria, failure interpretation, required experiment, boundary conditions, evidence refs, and risk level.

The workflow uses fake `GapValidationReport` inputs in tests and does not call a network service or LLM.

## Round 10A Update

2026-05-19: Implemented the TulingResearch Plus Creative Ideation workflow under `src/tuling_research_plus/ideation/`.

Implemented outputs:

- `IdeaCandidate`
- `MorphologicalMatrix`
- `IdeaGenerationResult`
- `DiversityFilterReport`
- `IdeaPortfolio`

Implemented tool wrappers:

- `research.idea_generate`
- `research.idea_cross_domain`
- `research.idea_morphological_matrix`
- `research.idea_quality_diversity_filter`

The diversity gate rejects near-duplicate candidates and clusters retained ideas by mechanism, required data, model component, evaluation target, and risk profile.

The workflow uses deterministic fake generators, keeps evidence refs on every idea, and does not call a network service or LLM.

## Round 10B Update

2026-05-19: Implemented the TulingResearch Plus Convergence workflow under `src/tuling_research_plus/convergence/`.

Implemented outputs:

- `ConvergenceCandidate`
- `CandidateScore`
- `PairwisePreference`
- `FeasibilityAssessment`
- `PromotionDecisionResult`
- `DecisionReport`

Implemented tool wrappers:

- `research.candidate_score`
- `research.candidate_pairwise_rank`
- `research.feasibility_assess`
- `research.portfolio_optimize`
- `research.decision_steelman`
- `research.promotion_decide`

`DecisionReport` now contains ranked candidates, scoring matrix, optional pairwise matrix, sensitivity analysis, feasibility notes, rejected candidates, steelman notes, final recommendation, confidence, and next actions.

The workflow is deterministic and can rank hypotheses, select experiment candidates, promote or reject implementation variants, select paper directions, and select public release feature sets without network or LLM calls.

## Round 10C Update

2026-05-19: Implemented the TulingResearch Plus Stress Test workflow under `src/tuling_research_plus/stress/`.

Implemented outputs:

- `Claim`
- `ExperimentPlan`
- `StressWeakness`
- `FailureMode`
- `StressTestReport`

Implemented tool wrappers:

- `research.artifact_stress_test`
- `research.claim_red_team`
- `research.hypothesis_debate`
- `research.experiment_premortem`
- `research.counterfactual_probe`
- `research.failure_mode_analyze`

Stress reports include artifact id, weaknesses, severity, attack paths, counterarguments, failure modes, mitigations, residual risk, pass/fail, and rerun recommendations.

Quality gates now flag unsupported claims, unfalsifiable hypotheses, and weak experiment plans. Mitigations can lower residual risk, and tests remain deterministic without network or LLM calls.

## Round 11 Update

2026-05-19: Implemented the TulingResearch Plus Experiment Execution workflow under `src/tuling_research_plus/experiment/`.

Implemented outputs:

- `ExperimentPlan`
- `ConstraintAnalysis`
- `ScenarioPlan`
- `ImplementationPlan`
- `ResultSchema`
- `ExperimentResultAnalysis`

Implemented tool wrappers:

- `research.experiment_design`
- `research.constraint_analyze`
- `research.scenario_plan`
- `research.implementation_plan`
- `research.result_schema_generate`
- `research.result_analyze`

`ExperimentPlan` now contains hypothesis, variables, controls, datasets, metrics, baselines, ablations, expected outcomes, failure modes, compute budget, implementation steps, reproducibility checklist, and statistical comparison plan.

The workflow is deterministic, generates result schemas, preserves evidence refs, and does not call a network service or LLM.
