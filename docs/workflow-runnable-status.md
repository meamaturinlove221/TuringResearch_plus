# Workflow Runnable Status

Status: completed.

Round: 260.

## Runnable

These workflows have local deterministic code paths:

- Campaign route recommendation and precondition evaluation.
- Scholar source priority, tool list, MCP usage guide, and fallback policy
  export.
- Vault wiki export, backlink index, dangling link report, and edge quality
  audit.
- Ontology alias resolution, gap detection, and SOP run plan.
- Stress scenario catalog and deterministic stress-test runner.
- Experiment execution plan, artifact requirement extraction, and runbook
  rendering.
- MCP fake/default config validation.

## Fake-Runnable

These workflows have fake/default tests and fixtures, but do not prove live
provider or remote execution parity:

- Neocortica Session parity fake flow.
- Context pack manifest fixture.
- Structured return manifest fixture.
- Web fetch dry-run tool.
- Web content review object from dry-run fetch.
- Apify optional live guide and missing-token graceful skip.
- v1.2 full fake replay.
- v1.2 public demo refresh.

## Docs-Only

These are documented but not implemented as runtime workflows:

- Full pod lifecycle manager.
- SSH/tmux/provision lifecycle.
- Automatic pod cleanup.
- Skill SOP invocation as a runtime engine.
- ARIS study features.

## Partial

These have useful runnable sub-parts but do not yet run end-to-end like a
reference workflow:

- Pod lifecycle as a full session runtime.
- Research Catalog as a single execution trace.
- Public parity dashboard as a runtime status dashboard.
- MCP / SKILL / README parity as a single guided user path.

## Blocked

These must stay blocked until a future round adds explicit safety gates:

- Automatic evidence ledger mutation from returned pod outputs.
- Treating fake/demo output as observed result.
- Claiming live provider success from dry-run or missing-token paths.
- Writing final paper conclusions from scaffold or draft beta output.

## Deferred

- MinerU / heavy PDF fallback.
- Live Semantic Scholar workflow proof.
- Live Apify workflow templates.
- Remote execution orchestration.
- OS-level plugin sandbox.
- ARIS runtime features.

## Unsafe By Default

These are only acceptable with explicit opt-in and separate review:

- Live networking.
- SSH/SFTP transfer.
- Remote shell execution.
- Modal/GPU execution.
- Unknown plugin execution.
- Private content fetching.
- Paywall bypass is rejected, not merely deferred.

## Current Best Demo Path

The current best safe path is:

1. Run the v1.2 full fake replay.
2. Inspect Reference Parity Dashboard JSON/docs.
3. Show campaign routing.
4. Show vault/ontology/stress/runbook outputs.
5. Explain that remote/live behaviors remain opt-in or deferred.
