# TuringResearch Plus API Freeze v0.1.0

This document freezes the public Python package structure and stable API surface for TuringResearch Plus `v0.1.0`.

## Package Structure

Frozen packages:

- `turing_research`
- `turing_research.pdf`
- `turing_research_plus`
- `turing_research_plus.artifacts`
- `turing_research_plus.budget`
- `turing_research_plus.campaign`
- `turing_research_plus.context`
- `turing_research_plus.convergence`
- `turing_research_plus.experiment`
- `turing_research_plus.hypothesis`
- `turing_research_plus.ideation`
- `turing_research_plus.insight`
- `turing_research_plus.ledger`
- `turing_research_plus.north_star`
- `turing_research_plus.paper`
- `turing_research_plus.race`
- `turing_research_plus.semantic_graph`
- `turing_research_plus.sop`
- `turing_research_plus.stress`
- `turing_research_plus.subtask`
- `turing_research_plus.survey`
- `turing_research_plus.vault`

## Frozen Model Families

- `EvidenceRef`
- `ResearchArtifact`
- `BudgetGate`
- `StateLedger`
- `CampaignSpec`
- `TaskProfile`
- PDF Markdown models
- Semantic Graph models
- Survey models
- Vault models
- Context models
- Race Mode models
- Paper pipeline models
- SOP graph models

## Frozen Capabilities

The `v0.1.0` API is limited to:

- Core local tools
- PDF Markdown Phase A
- Semantic Graph fake adapter / dry-run
- Literature Survey dry-run
- Vault / Context basic capabilities
- Race Mode basics
- Feature Capsule skeleton
- DocFlow
- Figure registry
- Paper draft gate
- Contract tests
- Workflow dry-run tests
- Examples fake mode

## Excluded From v0.1.0

- real network API execution by default
- heavy OCR
- complex PDF layout parsing
- full automatic paper generation
- real GPU experiment execution
- automatic PyPI publishing
- private or unauthorized source idea implementation

## Compatibility Rule

Before `v0.1.0` release, changes to public models, contracts, package paths, and MCP tool names require explicit release-candidate review and a ledger entry.

After `v0.1.0`, breaking changes require a new compatibility note and versioned migration plan.
