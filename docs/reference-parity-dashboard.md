# Reference Parity Dashboard

Status: v1.3 public review dashboard.

Updated: Round 286.

This dashboard summarizes which reference-repo capabilities are aligned in
TuringResearch v1.3. It is a public-facing review dashboard, not a claim that
every upstream feature was copied or that unsafe features were adopted.

Data source:

- `examples/public_demo/reference_parity_dashboard.json`

## Neocortica Parity

| Area | Status | Evidence | Boundary |
| --- | --- | --- | --- |
| Neocortica Session parity | fake/default runtime replay complete | `docs/session-runtime-gate-report.md` | no SSH/tmux/provision by default, no remote command execution |
| Neocortica Scholar parity | fake/default full tool surface complete | `docs/scholar-web-parity-gate-report.md` | no MinerU, no heavy OCR, no automatic paper download, no paywall bypass |
| Neocortica Web parity | fake/default full tool surface complete | `docs/scholar-web-parity-gate-report.md` | no default networking, no cookies, no private scraping |
| MCP / Skill parity | documentation-contract and SOP parity complete | `docs/mcp-tool-parity-v1.3.md`, `docs/skill-sop-parity.md` | no live MCP server or runtime tool execution by default |

## yogsoth-ai Parity

| Area | Status | Evidence |
| --- | --- | --- |
| Campaign trace | complete | `docs/campaign-execution-trace.md` |
| Research Catalog dashboard | complete | `docs/research-catalog-dashboard.md` |
| Vault / wiki / edge audit demo | complete | `docs/vault-wiki-export-demo.md` |
| Ontology runbook demo | complete | `docs/ontology-runbook-demo.md` |
| Stress scenario library | complete | `docs/stress-scenario-library.md` |
| Convergence decision report | complete | `docs/convergence-decision-report.md` |
| Full parity gate | complete | `docs/yogsoth-full-parity-gate-report.md` |

## Deferred ARIS

ARIS remains deferred from v1.3 implementation. It is tracked as future
reference, not as a runtime surface:

- `docs/aris-still-deferred-v1.3.md`
- `docs/v1.3.0-aris-deferral-reconfirm.md`
- `docs/aris-implementation-blocklist-v1.3.md`

## Rejected Unsafe Features

- unknown remote execution
- automatic experiment execution
- automatic observed result writes
- fake/demo result promotion
- paywall bypass
- private content fetching
- default network access

## Public Demo

- `examples/public_demo/v1_3_original_parity_demo/`
- `docs/v1.3.0-full-original-parity-replay-report.md`

## Future Roadmap

- v1.3 release candidate hardening
- public docs polish
- optional live provider review
- separately scoped ARIS study only after safety review

## Safety Boundary

- No new core runtime is added by this dashboard.
- No live network access is required.
- No private data is required.
- No automatic remote execution is enabled.
- Fake/live boundaries remain explicit.
- Privacy-first defaults remain in force.
- Human review remains required.
