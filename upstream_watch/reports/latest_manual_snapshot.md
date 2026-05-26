# Latest Manual Upstream Snapshot

Date: 2026-05-20

Mode: manual snapshot supplied by project operator. No live scan was run in this
round. If no prior baseline exists, this file is a current snapshot, not a diff
or new-feature claim.

## Active Neocortica Split Targets

- `Pthahnix/Neocortica-Scholar`
- `Pthahnix/Neocortica-Web`
- `Pthahnix/Neocortica-Session`

`Pthahnix/Neocortica` is retained only as a legacy alias / historical umbrella
name and is not an active required scan target.

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
- `web_fetching` tool.
- `web_content` tool.
- MCP server entry.
- real Apify integration test.
- remove dotenv and use `.mcp.json` env block.
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

## Yogsoth AI Signals To Continue Watching

- `ENTRY.md` / campaign routing table.
- skill routing.
- wiki / vault / edge audit.
- inline `[[wikilink]]`.
- ontology SOPs.
- convergence / stress-test / subagent-spawning.
