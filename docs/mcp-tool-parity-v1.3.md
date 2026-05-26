# MCP Tool Parity v1.3

Status: parity mapping complete.

Round: 275.

This round aligns the v1.3 Scholar, Web, Session, Campaign, Vault, and Stress
tool surfaces with the MCP configuration story. It is a configuration and
contract pass, not a server runtime pass.

## Covered Surfaces

| Surface | MCP mapping status | Evidence |
| --- | --- | --- |
| Scholar tools | mapped | `docs/scholar-full-tool-surface.md` |
| Web tools | mapped | `docs/web-full-tool-surface.md` |
| Apify optional | mapped as disabled optional live | `docs/apify-workflow-templates.md` |
| Session runtime fake tools | mapped | `docs/session-runtime-gate-report.md` |
| Campaign catalog | mapped | `docs/turingresearch-campaign-catalog.md` |
| Vault tools | mapped | `docs/yogsoth-vault-parity.md` |
| Stress test tools | mapped | `docs/yogsoth-stress-test-parity.md` |

## What Changed

- `.mcp.example.json` now includes `tool_surface_v1_3`.
- The mapping is explicit, local-first, and fake/default.
- The mapping does not add or enable runtime MCP handlers.
- Contract tests assert the expected groups, tool names, and disabled defaults.

## Safety Rules

- no real key in `.mcp.example.json`;
- live mode disabled by default;
- plugin tools disabled by default;
- Apify optional remains opt-in;
- no remote command execution;
- no default network;
- no automatic Evidence Ledger mutation;
- no fake result promoted to observed evidence.

## Operator Interpretation

Use this mapping as the v1.3 public explanation of the tool surface. Use the
current stdio smoke registry for what is actually enabled today.

Promotion from mapping to active MCP tools requires a separate runtime gate.
