# Neocortica Parity Matrix

Status: planning matrix.

Round: 232.

This matrix covers only the active Neocortica split references:

- `Pthahnix/Neocortica-Session`
- `Pthahnix/Neocortica-Scholar`
- `Pthahnix/Neocortica-Web`

The historical umbrella repository is treated as a legacy alias only.

## Matrix

| Upstream repo | Upstream module / feature | Upstream purpose | Current TuringResearch equivalent | Status | Implementation priority | Risk | Test requirement | Docs requirement | Target round |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Pthahnix/Neocortica-Session` | Git-based context transfer | durable context transfer without fragile session teleport | Pod Context Lifecycle Safety, handoff bundle policy | partial | P0 | unsafe transfer, path traversal | pod preflight and transfer policy tests | transfer policy doc | R234-R235 tentative |
| `Pthahnix/Neocortica-Session` | durable context package | package context as files like project context, memory, route spec | `PROJECT_CONTEXT.md`, `MEMORY.md`, `ROUTE_SPEC.yaml` policy | partial | P0 | stale memory or source-of-truth confusion | lifecycle model tests | lifecycle safety doc | R234-R235 tentative |
| `Pthahnix/Neocortica-Session` | preflight / provision / transfer / launch modules | break session workflow into explicit phases | preflight and transfer policy only; no launch | partial | P0 | remote execution creep | no SSH/Modal/tmux assertions | non-goals doc | R234-R235 tentative |
| `Pthahnix/Neocortica-Session` | dotfile handling safety | prevent unsafe hidden config transfer | forbidden dotfile policy | partial | P0 | secret leakage | forbidden file tests | transfer checklist | R234-R235 tentative |
| `Pthahnix/Neocortica-Session` | shell injection risk fix | avoid shell metacharacter abuse | shell metacharacter risk awareness | partial | P0 | command injection | shell-risk preflight tests | preflight checklist | R234-R235 tentative |
| `Pthahnix/Neocortica-Session` | Windows tar / Linux unpack compatibility | safe cross-platform archive handling | archive relative path policy | partial | P1 | path traversal | archive path validation tests | transfer policy doc | R235 tentative |
| `Pthahnix/Neocortica-Session` | return metadata handling | validate returned files and metadata | return verifier and proposed updates | partial | P0 | automatic evidence mutation | return verifier tests | return verification doc | R235 tentative |
| `Pthahnix/Neocortica-Scholar` | `.mcp.example.json` pattern | safe MCP config with env block | `.mcp.example.json`, MCP env block policy | partial | P0 | credential leakage | MCP config tests | MCP config parity doc | R235-R236 tentative |
| `Pthahnix/Neocortica-Scholar` | README tool list / MCP test results | visible tool surface and test status | MCP docs and release/test summaries | partial | P1 | stale docs | docs/workflow tests | scholar parity doc | R235-R236 tentative |
| `Pthahnix/Neocortica-Scholar` | SKILL.md usage guide | operator-friendly scholar workflow | skill routing/docs | partial | P1 | skill drift | skill routing tests | skill SOP parity doc | R235-R236 tentative |
| `Pthahnix/Neocortica-Scholar` | arxiv2md fallback to PDF/MinerU | fallback paper content extraction | cached Markdown and fake adapters; MinerU deferred | deferred | P3 | heavy dependency/copyright | planning-only test gate | v1.3 heavy PDF roadmap | v1.3+ |
| `Pthahnix/Neocortica-Scholar` | env var naming normalization | consistent live/fake env naming | MCP fake/live config polish | partial | P0 | confusing live behavior | config/default tests | MCP env policy | R235-R236 tentative |
| `Pthahnix/Neocortica-Web` | Apify REST API client | optional live Apify workflow | Fake/live Apify adapter docs | partial | P2 | token/cost/network risk | fake adapter tests; live skipped | Apify template docs | R236-R237 tentative |
| `Pthahnix/Neocortica-Web` | `web_fetching` tool | fetch public web content | web fetch adapter | partial | P1 | default networking | fake web fetch tests | web adapter docs | R236-R237 tentative |
| `Pthahnix/Neocortica-Web` | `web_content` tool | parse/return web content | web content cache/metadata | partial | P1 | unverified content overclaim | content metadata tests | web content docs | R236-R237 tentative |
| `Pthahnix/Neocortica-Web` | MCP server entry | expose web tools through MCP config | MCP registry/config docs | partial | P1 | accidental live path | MCP config tests | MCP distribution docs | R236-R237 tentative |
| `Pthahnix/Neocortica-Web` | real Apify integration test | validate live integration | live tests opt-in only | deferred | P2 | requires token/network | skipped live marker only | live test policy | v1.3+ |
| `Pthahnix/Neocortica-Web` | remove dotenv, use `.mcp.json` env block | avoid implicit dotenv loading | env block policy | partial | P0 | secret leakage | config denylist tests | MCP env block policy | R235 |

## Not In Parity Scope

- copying Neocortica code;
- SSH provisioning;
- tmux launch;
- Modal execution;
- live web/scholar tests by default;
- MinerU as a default v1.2 runtime path.
