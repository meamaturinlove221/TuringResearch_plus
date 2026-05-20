# TulingResearch Plus Workflows

TulingResearch Plus workflows are dry-run and fake-service friendly by default. They use `BudgetGate`, `StateLedger`, `ResearchArtifact`, and `EvidenceRef` boundaries.

## Campaign Runtime

Campaigns route from CampaignSpec to Strategy, Tactic, and SOP execution. The runtime records ledger events, artifacts, blockers, quality gates, and checkpoints.

## North Star

North Star turns vague research intent into:

- NorthStarStatement
- ResearchBrief
- GoalTree
- ObstacleMap
- DirectionCandidates

It supports cold-start, warm-start, and hot-start flows with fake paper/web service protocols.

## Literature Survey

Literature Survey supports:

- scoping survey
- systematic survey
- deep survey
- narrative review
- snowball survey

Hard gates prevent strong conclusions from shallow overview runs, require evidence-backed final gaps, and count local PDF Markdown as full text when available.

## Deep Insight

Deep Insight transforms survey artifacts into:

- GapValidationReport
- InsightReport
- BoundaryMap
- SensitivityReport
- ReformulatedProblemSet

No gap or insight is accepted without supporting evidence.

## Hypothesis / Ideation / Convergence

The hypothesis workflow ranks validated gaps, generates falsifiable hypotheses, operationalizes variables, and formulates research questions. Ideation creates diverse candidates, and convergence ranks them into decisions with feasibility notes, sensitivity analysis, rejected candidates, and next actions.

## Stress / Experiment

Stress tests red-team claims, hypotheses, ideas, and experiment plans. Experiment execution produces plans, constraints, scenarios, implementation steps, result schemas, and dry-run result analysis.

## Vault / Context

Vault stores markdown knowledge graph pages and evidence edges. Context creates checkpoint files, indexes them, and recovers the latest workflow state.

## Race Mode

Race Mode extracts IdeaCards from public or authorized sources, checks source hygiene, scores priority, creates Feature Capsule skeletons, builds 16-box architecture plans, and watches public upstream changes.

## Paper Pipeline

Paper workflows manage article blocks, SOP graphs, figures, captions, draft gates, missing evidence reports, and LaTeX export. Draft generation is blocked without `ExperimentReport`.
