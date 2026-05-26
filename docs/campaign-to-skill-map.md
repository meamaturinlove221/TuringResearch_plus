# Campaign To Skill Map

Status: implemented minimal.

Round: 176 upstream adjustment.

This map connects campaign catalog entries to existing repo skills. It is a
recommendation map, not an execution engine.

| Campaign | Primary skill | Secondary skill |
| --- | --- | --- |
| `north_star` | `turingresearch-fusion-north-star` | `turingresearch-master-orchestrator` |
| `knowledge_acquisition` | `turingresearch-fusion-literature-survey` | `turingresearch-master-orchestrator` |
| `deep_insight` | `turingresearch-fusion-deep-insight` | `turingresearch-master-orchestrator` |
| `hypothesis_formation` | `turingresearch-fusion-hypothesis-formation` | `turingresearch-master-orchestrator` |
| `creative_ideation` | `turingresearch-fusion-creative-ideation` | `turingresearch-master-orchestrator` |
| `convergence` | `turingresearch-fusion-convergence` | `turingresearch-master-orchestrator` |
| `stress_test` | `turingresearch-fusion-stress-test` | `turingresearch-master-orchestrator` |
| `experiment_planning` | `turingresearch-fusion-experiment-execution` | `turingresearch-master-orchestrator` |
| `artifact_audit` | `turingresearch-cache-and-ledger` | `turingresearch-master-orchestrator` |
| `advisor_pack` | `turingresearch-paper-writing-pipeline` | `turingresearch-master-orchestrator` |
| `public_release` | `turingresearch-qa-release` | `turingresearch-master-orchestrator` |

## Policy

The master orchestrator remains authoritative for round-level execution. The
campaign router is a local recommendation helper only.
