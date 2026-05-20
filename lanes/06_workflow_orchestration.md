# Lane 06: Workflow Orchestration

## Scope

Define workflow support models for BudgetGate, StateLedger, campaigns, and subtasks.

## Outputs

- `src/tuling_research_plus/budget/models.py`
- `src/tuling_research_plus/ledger/models.py`
- `src/tuling_research_plus/campaign/models.py`
- `src/tuling_research_plus/subtask/models.py`

## Status

Phase 1 complete. No workflow engine is implemented.

## Round 5A Update

2026-05-19: Implemented the abstract TulingResearch Plus Campaign Runtime:

- `CampaignSpec`
- `StrategySpec`
- `TacticSpec`
- `SOPSpec`
- `CampaignRun`
- `CampaignResult`
- `CampaignRunner`
- `CampaignRouter`
- `CampaignRegistry`
- `TaskProfile`
- `SubtaskRunner`

Supported SOP execution modes:

- `direct`
- `imported`
- `subtask`

Runtime behavior:

- Selects a strategy through router.
- Initializes `StateLedger`.
- Executes tactics and SOPs.
- Checks `BudgetGate`.
- Allows controlled completion when `deviation_reason` is present.
- Collects `ResearchArtifact`.
- Runs quality gates.
- Triggers checkpoint hook.
- Returns markdown-serializable `CampaignResult`.

No concrete survey, hypothesis, or network behavior was implemented.

## Round 5B Update

2026-05-19: Implemented the single-window Subtask Runtime:

- `TaskProfile`
- `SubtaskExecutionMode`
- `SubtaskRunner`
- role prompt rendering
- deterministic `dry_run`
- `manual_codex_role` prompt mode
- reserved `llm_client` mode with explicit unsupported behavior
- quality gate evaluation

This replaces Claude Code specific subagent-spawning assumptions with TulingResearch Plus models that work inside one Codex window.

No LLM client calls, network calls, or external agent-tool dependencies were added.

## Round 7 Update

2026-05-19: Added a depth-gated Literature Survey workflow on top of the workflow runtime. The workflow returns structured `LiteratureSurveyArtifact`, `PaperScreeningTable`, `MethodTaxonomy`, `EvidenceMatrix`, `GapList`, optional `PRISMAFlow`, and optional `CitationLineage`.

The workflow uses Protocol dependencies only:

- `PaperService`
- `WebService`
- `PDFMarkdownService`
- `SemanticGraphService`
- `VaultService`
- `ContextService`

Dry-run workflow tests use fake services and do not perform network calls.

## Round 9A Update

2026-05-19: Added the North Star workflow as the first research-direction shaping workflow. It turns vague intent, constraints, resources, current context, and advisor comments into a structured `ResearchBrief`, `NorthStarStatement`, `GoalTree`, `ObstacleMap`, and ranked `DirectionCandidates`.

The workflow is deterministic for tests, uses Protocol service dependencies, and exercises obstacle rejection backtracking without introducing concrete literature, hypothesis, or network behavior.

## Round 11 Update

2026-05-19: Added the Experiment Execution workflow as a dry-run planning layer after hypothesis validation. It produces experiment plans, constraints, scenarios, implementation plans, result schemas, and dry-run result analyses without executing real experiments.

The workflow keeps controls, metrics, ablations, reproducibility checklist, and statistical comparison plan as required model fields so downstream paper drafting can continue to rely on explicit experiment artifacts.
