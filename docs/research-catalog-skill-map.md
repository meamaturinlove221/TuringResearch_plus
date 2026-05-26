# Research Catalog Skill Map

Status: v1.2 integration.

Round: 248.

This map connects Research Catalog surfaces to existing TuringResearch skills
and docs.

| Catalog surface | Primary skill | Supporting docs |
| --- | --- | --- |
| Campaign Catalog | `turingresearch-fusion-campaign-engine` | `docs/turingresearch-campaign-catalog.md` |
| Skill routing | `turingresearch-master-orchestrator` | `.agents/ROUTING_TABLE.md` |
| Vault graph | `turingresearch-fusion-wiki-vault` | `docs/yogsoth-vault-parity.md` |
| Ontology SOPs | `turingresearch-fusion-semantic-graph` | `docs/yogsoth-ontology-parity.md` |
| Stress tests | `turingresearch-fusion-stress-test` | `docs/yogsoth-stress-test-parity.md` |
| Experiment runbooks | `turingresearch-fusion-experiment-execution` | `docs/yogsoth-experiment-execution-parity.md` |
| Advisor pack | `turingresearch-paper-writing-pipeline` | `docs/advisor-pack-builder.md` |
| Public release | `turingresearch-qa-release` | `docs/v1.0.0-public-launch-rc-report.md` |

## Handoff Policy

- Skills are SOP descriptions and handoff aids.
- The master orchestrator remains authoritative for round-level execution.
- Plugin and live tools remain disabled unless explicitly enabled by policy.
- Public output must pass privacy/security and fake/live boundary checks.
