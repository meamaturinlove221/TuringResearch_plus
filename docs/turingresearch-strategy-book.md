# TuringResearch Strategy Book

Status: v1.2 campaign parity.

Round: 243.

The TuringResearch Strategy Book is a static, review-only view of the Campaign
Catalog. It helps an operator select a campaign and skill handoff before any
implementation work begins.

## Strategy Book Fields

Each entry contains:

- campaign id;
- display id;
- purpose;
- when to use;
- primary skill;
- expected outputs;
- safety notes;
- related docs;
- related tests.

## Required Campaign Set

| Display campaign | Canonical campaign |
| --- | --- |
| `north_star` | `north_star` |
| `knowledge_acquisition` | `knowledge_acquisition` |
| `deep_insight` | `deep_insight` |
| `hypothesis` | `hypothesis_formation` |
| `ideation` | `creative_ideation` |
| `convergence` | `convergence` |
| `stress_test` | `stress_test` |
| `experiment_execution` | `experiment_planning` |
| `public_release` | `public_release` |

## Execution Plan Boundary

The execution plan is a handoff checklist. It is not execution:

- no skill execution;
- no LLM call;
- no network;
- no replacement for the master orchestrator;
- no automatic experiment execution;
- no automatic release action.

## Usage

Use `build_campaign_strategy_book()` to inspect available strategies,
`evaluate_campaign_preconditions()` to identify missing inputs, and
`build_campaign_execution_plan()` to prepare a manual handoff.
