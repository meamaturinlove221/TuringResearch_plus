# Runtime Gap Audit

Status: completed.

Round: 260.

This audit checks what is actually runnable after the v1.2 reference parity
line, and what is still only designed, fake/default, partial, blocked,
deferred, or unsafe by default.

It does not add new runtime behavior.

## Executive Result

Overall status: `FAKE-RUNNABLE WITH RUNTIME GAPS`.

TuringResearch has enough local fake/default runtime to demonstrate the
reference parity path, but it does not yet run like the original references in
every operational sense.

The strongest runnable areas are:

- deterministic campaign routing;
- session context pack manifest generation;
- structured return manifest building and metadata verification;
- Scholar/Web fake tool surfaces;
- wiki vault export and edge audit;
- ontology gap detection;
- stress-test runner;
- experiment execution runbook generation.

The weakest runtime areas are:

- full pod lifecycle runtime;
- live Scholar/Web/Apify execution;
- remote transport and remote command execution;
- automatic experiment execution;
- automatic evidence ledger mutation;
- final paper or observed-result production.

## Classification Definitions

| Status | Meaning |
| --- | --- |
| `runnable` | Has a deterministic local Python path that can run without live services. |
| `fake-runnable` | Has a fake/default workflow test or fixture path; safe for demos, not proof of live integration. |
| `docs-only` | Exists as a policy, plan, or guide but does not yet have an execution path. |
| `partial` | Some sub-parts run, but the workflow does not run end-to-end like the reference. |
| `blocked` | Missing required safety or execution path, so it must not be treated as runnable. |
| `deferred` | Intentionally postponed to a later round/version. |
| `unsafe-by-default` | Would be unsafe if enabled automatically; must remain opt-in, fake-only, or rejected. |

## Focus Check Results

| Check | Status | Evidence | Gap |
| --- | --- | --- | --- |
| Pod lifecycle as a full runtime | `partial` | `tests/workflow/test_neocortica_session_parity_fake.py` runs local safety/preflight/return checks. | No remote pod runtime, no lifecycle manager, no cleanup, no SSH/tmux/provision. |
| Context pack generation | `fake-runnable` | `build_session_context_pack_manifest` is exercised in Neocortica session and v1.2 full replay tests. | Still manifest-level; no actual transfer runner in this audit. |
| Structured return verification | `fake-runnable` | `build_structured_return_manifest` and `verify_pod_context_return` pass in fake workflow tests. | Does not verify full artifact checksums or apply updates. |
| Scholar pipeline fake run | `fake-runnable` | Source priority, tool list, MCP usage guide, and fallback policy are tested. | No default live Semantic Scholar or full paper download. |
| Web/Apify fake run | `fake-runnable` | Web fetching returns dry-run status; Apify missing-token path is graceful. | Live networking remains opt-in and not proved by default tests. |
| Campaign catalog routing | `runnable` | `build_campaign_execution_plan` deterministically routes tasks without network or LLM calls. | It does not execute agents or replace the master orchestrator. |
| Vault export generation | `runnable` | `build_wiki_vault_export`, backlink, dangling link, and edge quality tests run locally. | Output is review-only and not a graph database. |
| Stress scenarios | `runnable` | `run_stress_test` covers the fixed scenario catalog locally. | It is a deterministic review runner, not a multi-agent adversarial runtime. |
| Experiment runbook generation | `runnable` | `build_experiment_execution_plan` and `render_experiment_execution_runbook` run locally. | It never executes experiments or writes observed results. |

## Runtime Truth

The project can currently replay a coherent reference parity path in fake mode.
It cannot yet claim live parity with the original systems where the original
systems include remote sessions, live provider access, live web workflows,
interactive agent execution, or real experiment execution.

The v1.3 implementation line should therefore focus on making existing
fake/default runtime surfaces more cohesive before considering any live
transport or remote runtime.

## Safety Boundaries Confirmed

- No default networking.
- No unknown remote command execution.
- No automatic SSH/tmux/provision path.
- No automatic experiment execution.
- No automatic evidence ledger write.
- No fake/demo output promoted to observed result.
- No ARIS implementation in this audit.

## Recommended v1.3 Runtime Focus

1. Add a coherent Session Runtime demo around context pack, preflight,
   transfer placeholder, return manifest, and verification.
2. Promote Scholar/Web fake tool surfaces into a visible command-like workflow
   without enabling live services by default.
3. Add a Research Catalog trace that links campaigns, vault, stress tests, and
   runbooks in one fake replay.
4. Refresh the parity dashboard to show runtime status, not only feature
   parity.
5. Keep live SSH/SFTP, live web, and live Scholar as explicit opt-in work with
   separate gates.
