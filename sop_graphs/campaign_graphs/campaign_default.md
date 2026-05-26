# TuringResearch Plus SOP: Campaign Graph

Graph type: `campaign`

Inputs:

- `CampaignSpec`
- `BudgetGate`
- `StateLedger`

Outputs:

- `CampaignResult`
- `ResearchArtifact`

Quality gates:

- BudgetGate passes.
- Campaign quality gates pass.

Failure gates:

- BudgetGate blocked.
- StateLedger blocker recorded.
