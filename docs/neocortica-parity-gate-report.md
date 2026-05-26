# Neocortica Parity Gate Report

Status: pass with deferred gaps.

Round: 242.

This gate decides whether the stable capabilities from the three tracked
Neocortica split repositories have reached parity inside TuringResearch.

Tracked references:

- `Pthahnix/Neocortica-Session`
- `Pthahnix/Neocortica-Scholar`
- `Pthahnix/Neocortica-Web`

## Gate Decision

Stable reference parity is complete for the safe, fake/default, review-only
surfaces needed by TuringResearch v1.2.

The gate is not a claim that every upstream feature is implemented. Heavy,
live, or risky features remain deferred or rejected.

## Complete

| Area | Complete parity |
| --- | --- |
| Session context pack | Durable context package manifest with required context files. |
| Session archive safety | Dotfile exclusion, path traversal guard, shell risk check, archive compatibility notes. |
| Structured return | Return manifest, metadata validation, proposed evidence updates only. |
| Scholar source priority | Cached Markdown first, arXiv/metadata, fake/live Scholar surface, manual fallback. |
| Scholar tool / MCP docs | Tool list export, MCP usage guide, fake/default config. |
| Web fetching/content | `web_fetching`, `web_content`, cache/source metadata, review-only output. |
| Apify optional live | Fake/default guide, no-key graceful skip, live opt-in only. |
| MCP config | Env block, fake mode default, provider live flags disabled, plugin tools disabled. |
| Skill SOP | Priority workflows have `when_to_use`, inputs, outputs, safety, non-goals, handoff, tests, and related docs. |

## Partial

| Area | Why partial |
| --- | --- |
| Upstream strict diff | A strict baseline exists, but the latest scan was unresolved due to public metadata rate limiting. |
| Live web/scholar/apify checks | Optional live tests exist or are documented, but public default remains fake/offline. |
| Session lifecycle manager | Safety model exists; a full manager/runtime remains future work. |

## Deferred

| Area | Deferral reason |
| --- | --- |
| MinerU / heavy PDF fallback | Heavy dependency, copyright, and reliability review needed. |
| Remote execution orchestration | Requires stronger design and safety review. |
| SSH/tmux/provision | Risky remote lifecycle surface; not needed for v1.2 parity. |
| Real Apify workflow templates | Requires live provider and cost/token review. |
| Full live provider regression | Requires private credentials and explicit live-test round. |
| ARIS features | Out of v1.2 scope by decision; study in v1.3 or later. |

## Rejected

| Area | Reason |
| --- | --- |
| Paywall bypass | Not allowed. |
| Private content fetching | Not allowed. |
| Cookie storage in public workflow | Not allowed. |
| Unknown remote execution | Not allowed. |
| Automatic evidence ledger mutation from pod output | Not allowed. |
| Automatic git push from parity workflow | Not allowed. |

## Safety Result

- No default network path is required.
- No remote execution path is enabled.
- No secrets are required.
- No old project naming is reintroduced.
- Fake/demo outputs remain fake/demo and are not observed evidence.

## Final Gate Status

Neocortica stable parity is complete for TuringResearch's safe v1.2 scope.
Remaining high-risk or heavy features are intentionally deferred or rejected.
