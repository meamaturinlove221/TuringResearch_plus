# Lane 44: Upstream Refresh and v0.3 Re-scope

## Scope

Round 63 updates upstream watch targets and rescopes v0.3 planning from the
latest manual upstream snapshot. No code is implemented.

Input note: `docs/upstream-learning-report.md` was not present, and no prior
machine-readable upstream baseline beyond placeholder README files was used.

## Target Update

- Removed `Pthahnix/Neocortica` from active required watch targets.
- Retained `Pthahnix/Neocortica` only as a legacy alias / historical umbrella.
- Active Neocortica targets are:
  - `Pthahnix/Neocortica-Scholar`
  - `Pthahnix/Neocortica-Web`
  - `Pthahnix/Neocortica-Session`

## Manual Snapshot Recorded

- Neocortica-Session: Git-based context transfer, durable context files, skill
  SOPs, atomic scripts, pod/local Git output flow, dotfile handling.
- Neocortica-Web: Apify REST client, web fetching/content tools, MCP entry,
  `.mcp.json` env block.
- Neocortica-Scholar: arXiv > Semantic Scholar > Unpaywall pipeline, reference
  pagination, cached markdown, Keshav reading.
- Yogsoth AI: `ENTRY.md`, skill routing, wiki/vault edge audit, wikilinks,
  ontology SOPs.

## v0.3 Scope Change

Sprint 1 is now Git-based Context Handoff / Pod Workflow. NAS / SMB / SSH /
GitHub Artifact Sync is deferred as a broad sync track.

## Boundaries

- No code implementation.
- No live scan.
- No upstream code copying.
- No private VGGT path reading.
- No claim of new upstream changes without baseline.
