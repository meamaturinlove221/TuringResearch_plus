# v1 Prelaunch Manual Upstream Snapshot

Date: 2026-05-21

Mode: manual snapshot plus local upstream-watch context.

GitHub API metadata access was attempted during this upstream-refresh round and
returned HTTP 403 in this environment. Therefore this file records the
operator-supplied upstream scan result and existing local watch context. It is
not a machine diff and not a claim that upstream code was copied or implemented.

## Active Neocortica Split Targets

- `Pthahnix/Neocortica-Scholar`
- `Pthahnix/Neocortica-Web`
- `Pthahnix/Neocortica-Session`

## Neocortica-Session Snapshot

- v2 rewrite.
- Git-based context transfer replacing SSH session JSONL teleport.
- `CLAUDE.md` plus `MEMORY` durable context.
- skill SOPs plus atomic shell scripts.
- preflight / provision / transfer / launch modules.
- pod deployment context.
- deploy-context dotfile handling fix.
- shell injection risk fix.
- Windows tar / Linux unpack compatibility.
- return metadata handling.

Adoption classification:

- v1.0: Pod Context Lifecycle Safety Plan docs and release safety note.
- v1.1: Pod Lifecycle Manager / Context Return Verifier.
- v1.2: remote execution orchestration research only.

## Neocortica-Web Snapshot

- Apify REST API client.
- `web_fetching` tool.
- `web_content` tool.
- MCP server entry.
- real Apify integration test.
- remove dotenv and use `.mcp.json` env block.
- README / LICENSE polish.

Adoption classification:

- v1.0: `.mcp.example.json`, MCP distribution docs, and web adapter docs.
- v1.1: web live mode polish.
- v1.2: Apify workflow templates.

## Neocortica-Scholar Snapshot

- `.mcp.example.json` pattern.
- README tool list / pipeline / MCP test results.
- `SKILL.md` usage guide.
- `arxiv2md` fallback to arXiv PDF plus MinerU.
- environment variable naming normalization.
- license link.

Adoption classification:

- v1.0: Scholar Pipeline public docs / MCP config examples.
- v1.1: paper source fallback refinement.
- v1.2: MinerU / heavy PDF fallback.

## Yogsoth AI Snapshot

- latest visible commit appears license-format level, not major feature.
- de-anthropocentric research catalog remains useful for:
  - campaign routing;
  - pre-conditions;
  - strategy book;
  - multi-campaign pipeline;
  - orchestration rules.

Adoption classification:

- v1.0: TuringResearch Campaign Catalog documentation.
- v1.1: Campaign Router model.
- v1.2: research strategy runtime experiments.

## Safety Notes

- No upstream code copied.
- No large feature implemented.
- No live adapter default enabled.
- No remote execution orchestration added.
- No heavy paper ingestion added.
