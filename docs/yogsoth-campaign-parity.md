# yogsoth Campaign Parity

Status: v1.2 parity implementation.

Round: 243.

This round aligns TuringResearch Campaign Catalog with stable yogsoth-ai ideas:
research catalog, campaign routing, strategy book entries, preconditions, skill
handoff, and review-only execution planning.

It does not implement a complex agent runtime.

## Covered Campaigns

- `north_star`
- `knowledge_acquisition`
- `deep_insight`
- `hypothesis`
- `ideation`
- `convergence`
- `stress_test`
- `experiment_execution`
- `public_release`

Compatibility aliases map:

- `hypothesis` -> `hypothesis_formation`
- `ideation` -> `creative_ideation`
- `experiment_execution` -> `experiment_planning`

## Implemented

- Strategy book export from the campaign catalog.
- Campaign precondition report.
- Review-only campaign execution plan.
- v1.2 campaign parity contract.
- Unit and workflow tests.

## Boundaries

- Does not execute skills.
- Does not call an LLM.
- Does not use the network.
- Does not replace `turingresearch-master-orchestrator`.
- Does not turn planned work into observed evidence.

## Tests

- `tests/unit/test_campaign_strategy_book.py`
- `tests/unit/test_campaign_preconditions.py`
- `tests/unit/test_campaign_execution_plan.py`
- `tests/workflow/test_yogsoth_campaign_parity_fake.py`
