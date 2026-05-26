# MCP Tool Surface v1.3

Status: documentation-contract surface.

Round: 275.

This document maps v1.3 original-parity local tools into an MCP-facing surface
without starting a real MCP server or enabling the tools by default.

The current stdio smoke registry remains intentionally small. The v1.3 mapping
is a public-safe configuration and contract view so the project can explain how
Scholar, Web, Session, Campaign, Vault, and Stress surfaces would be exposed
when promoted through a future MCP runtime gate.

## Boundary

- Does not start the MCP server.
- Does not add live networking.
- Does not require API keys.
- Does not enable plugin tools.
- Does not execute remote commands.
- Does not mutate the Evidence Ledger.
- Does not turn fake/demo output into observed evidence.

## Tool Groups

| Group | Tools | Default |
| --- | --- | --- |
| Scholar | `scholar.paper_searching`, `scholar.paper_content`, `scholar.paper_reference`, `scholar.paper_reading` | fake/local |
| Web | `web.web_fetching`, `web.web_content`, `web.cache`, `web.source_metadata`, `web.apify_optional` | fake/local; Apify optional live disabled |
| Session | `session.preflight`, `session.context_pack`, `session.fake_transfer`, `session.return_verifier`, `session.workflow_replay` | fake/local |
| Campaign | `campaign.catalog`, `campaign.preconditions`, `campaign.execution_plan` | review-only |
| Vault | `vault.wiki_export`, `vault.backlinks`, `vault.edge_quality`, `vault.ontology_sop` | review-only |
| Stress | `stress.scenario_catalog`, `stress.runner`, `stress.report` | review-only |

## Config Location

The mapping is stored in `.mcp.example.json` under:

```text
mcpServers.turingresearch-plus.tool_surface_v1_3
```

The mapping status is `documentation-contract-only`. Every listed entry has
`mcp_enabled_by_default: false`.

## Apify Optional Boundary

`web.apify_optional` is listed so users can discover the optional Apify
workflow templates. It remains disabled by default and requires explicit live
mode outside this public example config.

## Relationship To Current Stdio Smoke Tools

`docs/mcp-tool-surface.md` still describes the currently enabled stdio smoke
tools. This v1.3 document is broader: it maps local parity surfaces into a
candidate MCP-facing catalog, but it does not change runtime availability.
