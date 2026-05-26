# Research Catalog Routing

Status: v1.2 integration.

Round: 248.

Research Catalog routing maps a task to a campaign, skill, capability surface,
and safety gate. It is advisory only.

| User intent | Campaign | Skill | Capability surface | Required gate |
| --- | --- | --- | --- | --- |
| Clarify research target | `north_star` | `turingresearch-fusion-north-star` | campaign strategy book | human review |
| Gather papers or source context | `knowledge_acquisition` | `turingresearch-fusion-literature-survey` | scholar pipeline / web fetch | fake/live boundary |
| Organize concepts | `deep_insight` | `turingresearch-fusion-semantic-graph` | vault graph / ontology SOPs | edge and gap audit |
| Draft hypothesis | `hypothesis_formation` | `turingresearch-fusion-hypothesis-formation` | campaign strategy book | missing evidence check |
| Compare options | `convergence` | `turingresearch-fusion-convergence` | stress-test report | blocker review |
| Stress a plan or claim | `stress_test` | `turingresearch-fusion-stress-test` | stress-test runner | privacy and overclaim guard |
| Plan experiment route | `experiment_planning` | `turingresearch-fusion-experiment-execution` | experiment runbook | hard gates |
| Audit artifacts | `artifact_audit` | `turingresearch-cache-and-ledger` | artifact audit / evidence ledger | no fake observed result |
| Prepare advisor output | `advisor_pack` | `turingresearch-paper-writing-pipeline` | advisor pack | unsupported claim guard |
| Prepare public release | `public_release` | `turingresearch-qa-release` | release gate | privacy/security gate |

## Rules

- Routing does not execute the skill.
- Routing does not call an LLM.
- Routing does not use the network.
- Routing does not replace the master orchestrator.
- Routing does not convert planned work into observed evidence.

## Recommended Sequence

Use the smallest campaign that explains the next action. If a route involves
claims, artifacts, privacy, or release posture, run stress-test review before
convergence.
