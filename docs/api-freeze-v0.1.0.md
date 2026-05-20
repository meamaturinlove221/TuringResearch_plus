# TulingResearch Plus API Freeze v0.1.0

This document freezes the public Python package structure and stable API surface for TulingResearch Plus `v0.1.0`.

## Package Structure

Frozen packages:

- `tuling_research`
- `tuling_research.pdf`
- `tuling_research_plus`
- `tuling_research_plus.artifacts`
- `tuling_research_plus.budget`
- `tuling_research_plus.campaign`
- `tuling_research_plus.context`
- `tuling_research_plus.convergence`
- `tuling_research_plus.experiment`
- `tuling_research_plus.hypothesis`
- `tuling_research_plus.ideation`
- `tuling_research_plus.insight`
- `tuling_research_plus.ledger`
- `tuling_research_plus.north_star`
- `tuling_research_plus.paper`
- `tuling_research_plus.race`
- `tuling_research_plus.semantic_graph`
- `tuling_research_plus.sop`
- `tuling_research_plus.stress`
- `tuling_research_plus.subtask`
- `tuling_research_plus.survey`
- `tuling_research_plus.vault`

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
