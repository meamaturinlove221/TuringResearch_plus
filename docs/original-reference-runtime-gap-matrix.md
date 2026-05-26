# Original Reference Runtime Gap Matrix

Status: completed.

Round: 260.

This matrix separates structural parity from runnable workflow parity.

| Reference area | Workflow | Current status | Current execution path | Missing execution path | v1.3 action |
| --- | --- | --- | --- | --- | --- |
| Neocortica Session | Pod lifecycle safety | `partial` | `run_pod_context_preflight`, archive safety, context pack manifest, structured return manifest, return metadata verifier. | End-to-end session runtime, transfer runner, remote lifecycle, cleanup. | Build a fake-first Session Runtime replay. |
| Neocortica Session | Context pack generation | `fake-runnable` | `build_session_context_pack_manifest` with fixture files. | Real transfer packaging and operator handoff command. | Add runtime entry docs/tests around context pack generation. |
| Neocortica Session | Structured return verification | `fake-runnable` | `build_structured_return_manifest` plus `verify_pod_context_return`. | Full checksum/file safety verification for returned bundle. | Add runtime return verifier before any ledger ingest. |
| Neocortica Session | SSH/tmux/provision | `deferred` | None. | Safe opt-in transport with no command execution by default. | Keep deferred unless explicitly scoped. |
| Neocortica Scholar | Paper source priority | `runnable` | `build_scholar_source_priority_plan`. | None for fake/default ordering. | Add command-like demo surface. |
| Neocortica Scholar | Tool list and MCP guide | `runnable` | `build_scholar_tool_list`, `build_scholar_mcp_usage_guide`. | None for docs/export. | Integrate into parity dashboard. |
| Neocortica Scholar | Live search / paper retrieval | `unsafe-by-default` | Disabled by config and tests. | Opt-in live provider gate and source cache review. | Defer live proof until separate live gate. |
| Neocortica Scholar | MinerU / heavy PDF fallback | `deferred` | Policy only. | Heavy PDF fallback runtime. | Keep out of v1.3 full original parity unless separately scoped. |
| Neocortica Web | Web fetching | `fake-runnable` | `run_web_fetching_tool` returns dry-run public metadata. | Default live retrieval. | Add fake CLI-like workflow first. |
| Neocortica Web | Web content review | `fake-runnable` | `web_content_from_fetch_result`. | Human-verified live content ingestion. | Keep review-only. |
| Neocortica Web | Apify optional path | `fake-runnable` | Missing-token/no-key graceful path and usage export. | Live Apify templates and token-gated runs. | Defer live template proof. |
| MCP / SKILL | Config parity | `runnable` | `.mcp.example.json` contract tests and env block checks. | None for fake/default config. | Keep docs synced with runtime demos. |
| MCP / SKILL | Skill SOP parity | `docs-only` | SOP docs and routing tables. | Callable skill runtime is outside this repo's code path. | Link SOPs to actual fake workflow tests. |
| yogsoth Campaign | Campaign routing | `runnable` | `build_campaign_execution_plan`, precondition evaluation, strategy book. | Agent execution trace with step artifacts. | Add deterministic campaign trace demo. |
| yogsoth Vault / Wiki | Wiki export | `runnable` | `build_wiki_vault_export`, backlinks, dangling links, edge quality. | Browseable demo bundle integrated with dashboard. | Add public wiki/vault demo page. |
| yogsoth Ontology | SOP runner and gaps | `runnable` | Alias resolution, gap detection, SOP run plan. | Final knowledge graph generation. | Keep review-only; improve demo visibility. |
| yogsoth Stress / Convergence | Stress scenarios | `runnable` | `run_stress_test` over fixed scenarios. | Multi-agent convergence runtime. | Keep deterministic runner; add trace. |
| yogsoth Experiment Execution | Execution runbook | `runnable` | `build_experiment_execution_plan`, runbook renderer, artifact requirements. | Actual experiment execution, Modal/GPU run, observed result writing. | Keep human-run runbook; add return verifier path later. |
| Research Catalog | Integrated catalog | `partial` | Docs and routing map integrate campaigns, skills, vault, stress, runbooks. | One runtime trace that invokes the pieces together. | Build full original parity replay. |
| ARIS | Study items | `deferred` | Roadmap and backlog only. | Any ARIS runtime. | Keep out of v1.3 implementation line. |

## Matrix Conclusion

The biggest runtime gap is not lack of components. It is lack of a single
operator-facing replay path that runs the safe components together.

v1.3 should therefore build coherent fake/default replays before expanding live
or remote capability.
