# Upstream Refresh: 2026-05-20

This refresh records a manual upstream snapshot for TuringResearch Plus v0.3
planning. No live scan was run in this round, and no upstream code was copied.

## Target Policy Change

`Pthahnix/Neocortica` is no longer a required watch target. It is retained only
as a legacy alias / historical umbrella name. Active Neocortica monitoring now
tracks the split repositories:

- `Pthahnix/Neocortica-Scholar`
- `Pthahnix/Neocortica-Web`
- `Pthahnix/Neocortica-Session`

An unresolved umbrella repository must not be treated as a failure.

## Manual Snapshot Status

No prior machine-readable baseline beyond placeholder README files is available
in `upstream_watch/baselines/`. Therefore this refresh is a current manual
snapshot, not a claim of newly added upstream functionality.

Input note: `docs/upstream-learning-report.md` was not present in the current
workspace, so adoption planning is based on the manual snapshot and existing
roadmap documents.

## Neocortica-Session Signals

- v2 rewrite.
- Git-based context transfer replacing SSH session JSONL teleport.
- `CLAUDE.md` plus `MEMORY` as durable context.
- skill SOPs plus atomic shell scripts.
- scripts: `install-node`, `create-cc-user`, `install-cc`, `setup-env`,
  `deploy-context`.
- local to pod via Git.
- pod to local outputs as structured files via git push.
- `MEMORY` is not bidirectionally synced.
- `deploy-context` dotfile handling fixed via `find` excluding dotfiles.

## Neocortica-Web Signals

- Apify REST API client.
- `web_fetching` and `web_content` tools.
- MCP server entry.
- real Apify integration test.
- removed dotenv in favor of `.mcp.json` env block.
- README / LICENSE / `.gitignore` / `CLAUDE.md` handling.

## Neocortica-Scholar Signals

- `paper_searching` pipeline: arXiv > Semantic Scholar > Unpaywall.
- Semantic Scholar references pagination.
- `paper_content` reads cached markdown locally.
- `paper_reference` uses Semantic Scholar API primary and markdown fallback.
- `paper_reading` uses three-pass Keshav method.
- `arxiv2md` fallback to arXiv PDF plus MinerU.
- `.mcp.example.json` config pattern.
- `SKILL.md` usage guide.
- README with tool list / pipelines / MCP test results.

## Yogsoth AI Watch Signals

- `ENTRY.md` / campaign routing table.
- skill routing.
- wiki / vault / edge audit.
- inline `[[wikilink]]`.
- ontology SOPs.
- convergence / stress-test / subagent-spawning.

## Planning Impact

The near-term v0.3 plan changes. Sprint 1 should focus on Git-based Context
Handoff / Pod Workflow instead of NAS / SMB / SSH / GitHub artifact sync as a
general sync layer.
