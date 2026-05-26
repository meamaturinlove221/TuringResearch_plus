# Already Implemented vs Upstream

Status: parity summary.

Round: 232.

This document summarizes current TuringResearch equivalents to stable upstream
ideas. It does not claim exact code parity and does not copy upstream source.

## Implemented Or Mostly Implemented

| Upstream idea | Current TuringResearch equivalent | Status | Notes |
| --- | --- | --- | --- |
| Campaign routing / strategy book | Campaign Catalog and deterministic router | implemented | Local, review-only, no LLM call, no skill execution. |
| Ontology SOPs | Ontology SOPs | implemented | Review steps for concepts, aliases, edges, hierarchy, and exports. |
| Vault graph review | Vault Graph Enhancement | partial | Typed nodes/edges and audit reports exist; parity gate still needed. |
| Web fetch fake/default path | Web Fetch Adapter | partial | Fake/local fixture path exists; live remains opt-in. |
| Apify optional adapter concept | Apify Adapter | partial | Fake adapter exists; live path remains optional and gated. |
| Scholar pipeline refinement | Scholar Pipeline Refinement | partial | Cache/fake-first flow exists; heavy fallback deferred. |
| Pod context lifecycle safety | Pod Context Lifecycle Safety | partial | Safety model exists; parity hardening still needed. |
| MCP fake/live config polish | `.mcp.example.json` and MCP docs | partial | Needs strict parity pass against Scholar/Web config style. |
| Skill routing | skill routing docs/tests and campaign-to-skill map | partial | Needs SOP parity matrix and gate. |
| Stress/claim safety | claim guards, privacy/security, regression gates | partial | Needs yogsoth stress-test parity report. |
| Experiment planning | route DSL, hard gates, failure taxonomy | partial | Needs experiment-execution parity report. |

## Current Gaps

- strict upstream diff gate;
- Neocortica-Session parity gate;
- Neocortica-Scholar parity gate;
- Neocortica-Web parity gate;
- yogsoth campaign/vault/ontology parity gate;
- skill SOP parity gate;
- v1.3 ARIS study roadmap.

## Why Some Items Are Not Implemented Now

The missing/deferred items are mostly heavy, live-capable, or runtime-expanding
features. v1.2 should not destabilize the runnable mainline by adding remote
execution, default live networking, paper-writing automation, or OS-level
plugin sandbox promises before stable reference parity is complete.
