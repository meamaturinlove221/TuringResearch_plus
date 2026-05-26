# Campaign Routing Table

Status: implemented minimal.

Round: 176 upstream adjustment.

The router maps a task description to a recommended campaign and
`turingresearch-*` skill. It uses deterministic keyword matching only.

## Routing Table

| Task signal | Recommended campaign | Recommended skill |
| --- | --- | --- |
| north star, scope, goal, non-goal | `north_star` | `turingresearch-fusion-north-star` |
| paper, source, literature, web fetch | `knowledge_acquisition` | `turingresearch-fusion-literature-survey` |
| insight, gap, claim, advisor, uncertainty | `deep_insight` | `turingresearch-fusion-deep-insight` |
| hypothesis, falsify, experiment idea | `hypothesis_formation` | `turingresearch-fusion-hypothesis-formation` |
| idea, candidate, roadmap | `creative_ideation` | `turingresearch-fusion-creative-ideation` |
| selection, priority, scope lock, go/no-go | `convergence` | `turingresearch-fusion-convergence` |
| stress, risk, unsafe, blocker, gate | `stress_test` | `turingresearch-fusion-stress-test` |
| experiment, route, metrics, planned | `experiment_planning` | `turingresearch-fusion-experiment-execution` |
| artifact, manifest, export, missing | `artifact_audit` | `turingresearch-cache-and-ledger` |
| advisor, meeting, decision, summary | `advisor_pack` | `turingresearch-paper-writing-pipeline` |
| release, public, launch, privacy, RC | `public_release` | `turingresearch-qa-release` |

## Fallback

If no campaign matches, the router recommends `north_star` with low confidence.

## Non-execution Boundary

The router returns a recommendation only. It does not execute skills, spawn
subagents, call an LLM, or access the network.
