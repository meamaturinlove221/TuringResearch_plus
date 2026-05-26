# Upstream Change Classification For v1.0

Status: planning classification.

Round: 175 upstream refresh.

This document classifies the v1.0 prelaunch upstream signals into v1.0, v1.1,
and v1.2 adoption windows. It is based on the manual upstream snapshot and does
not claim live feature implementation.

## Neocortica-Session

Observed planning signals:

- v2 rewrite;
- Git-based context transfer replacing SSH session JSONL teleport;
- `CLAUDE.md` plus `MEMORY` durable context;
- skill SOPs plus atomic shell scripts;
- preflight, provision, transfer, and launch modules;
- pod deployment context;
- deploy-context dotfile handling fix;
- shell injection risk fix;
- Windows tar / Linux unpack compatibility;
- return metadata handling.

Classification:

| Release window | Action |
| --- | --- |
| v1.0 | Add Pod Context Lifecycle Safety Plan docs and release safety note. |
| v1.1 | Implement Pod Lifecycle Manager and Context Return Verifier. |
| v1.2 | Reconsider remote execution orchestration after safety and return verification mature. |

## Neocortica-Web

Observed planning signals:

- Apify REST API client;
- `web_fetching` tool;
- `web_content` tool;
- MCP server entry;
- real Apify integration test;
- remove dotenv and use `.mcp.json` env block;
- README / LICENSE polish.

Classification:

| Release window | Action |
| --- | --- |
| v1.0 | Polish `.mcp.example.json`, MCP distribution docs, and web adapter docs. |
| v1.1 | Web live mode polish with explicit opt-in and guarded test policy. |
| v1.2 | Apify workflow templates after live-mode policy stabilizes. |

## Neocortica-Scholar

Observed planning signals:

- `.mcp.example.json` pattern;
- README tool list, pipeline, and MCP test results;
- `SKILL.md` usage guide;
- `arxiv2md` fallback to arXiv PDF plus MinerU;
- environment variable naming normalization;
- license link.

Classification:

| Release window | Action |
| --- | --- |
| v1.0 | Polish Scholar Pipeline public docs and MCP config examples. |
| v1.1 | Refine paper source fallback behavior. |
| v1.2 | Evaluate MinerU / heavy PDF fallback, still optional and disabled by default. |

## Yogsoth AI

Observed planning signals:

- latest visible commit appears license-format level, not major feature work;
- de-anthropocentric research catalog remains useful for campaign routing;
- pre-conditions;
- strategy book;
- multi-campaign pipeline;
- orchestration rules.

Classification:

| Release window | Action |
| --- | --- |
| v1.0 | Add TuringResearch Campaign Catalog documentation. |
| v1.1 | Design Campaign Router model. |
| v1.2 | Consider research strategy runtime experiments. |

## Adoption Boundary

- Upstream ideas may influence docs, safety plans, contracts, and test planning.
- Upstream code must not be copied.
- Manual snapshot items must not be described as locally implemented.
- Remote execution, heavy PDF fallback, and default live networking remain out
  of v1.0.
