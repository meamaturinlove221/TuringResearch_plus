# yogsoth Tool Surface Matrix

Status: completed.

Round: 261.

## Matrix

| Reference tool surface | Current TuringResearch surface | Surface type | Status | Gap |
| --- | --- | --- | --- | --- |
| campaign routing | `route_campaign`, `build_campaign_execution_plan` | `local-python` | covered | Does not execute agents. |
| research catalog | Research Catalog docs, routing map, skill map | `config-docs` | partial | Needs one callable trace artifact. |
| vault | `build_wiki_vault_export`, backlinks, dangling link report, edge quality | `local-python` | covered | Review-only, no graph database. |
| ontology | alias resolver, gap detector, ontology SOP runner | `local-python` | covered | Does not generate a final knowledge graph. |
| convergence | convergence services and stress/convergence recommendations | `local-python` | partial | Needs clearer integration into catalog trace. |
| stress test | `run_stress_test`, fixed scenario catalog, report renderer | `local-python` | covered | Deterministic review runner, not multi-agent runtime. |
| experiment execution | `build_experiment_execution_plan`, artifact requirements, runbook renderer | `local-python` | covered | Does not execute experiments or write observed results. |

## Safety Summary

- Campaign routing is advisory and deterministic.
- Research Catalog routing does not execute skills.
- Vault and ontology outputs require review.
- Stress tests are deterministic review gates.
- Experiment execution parity produces runbooks and artifact requirements only.

## Gap Summary

The yogsoth surface gap is integration, not individual helpers. v1.3 needs a
single Research Catalog trace that shows campaign routing, vault/ontology,
stress, and runbook surfaces working together without adding agent runtime.
