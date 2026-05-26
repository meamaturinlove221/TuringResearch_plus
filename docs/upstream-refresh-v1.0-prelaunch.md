# Upstream Refresh For v1.0 Prelaunch

Status: manual snapshot recorded.

Round: 175 upstream refresh.

This refresh records the upstream signals that should be considered before the
v1.0 API freeze and public launch hardening path. It does not copy upstream
code, implement large features, run remote execution, or change release status.

## Scan Mode

- Target policy: public metadata and public repository signals only.
- GitHub API attempt: attempted in this round and returned HTTP 403 for tracked
  repositories in this environment.
- Resulting mode: operator-supplied manual snapshot plus existing local
  upstream-watch context.
- Baseline note: no machine-readable prior baseline is available beyond the
  local placeholder baseline files, so this report is a current manual snapshot,
  not a machine diff.

## Active Neocortica Targets

Continue watching only the split repositories:

- `Pthahnix/Neocortica-Scholar`
- `Pthahnix/Neocortica-Web`
- `Pthahnix/Neocortica-Session`

The historical umbrella repository remains a legacy alias only. An unresolved
umbrella repository is not a scan failure.

## Yogsoth AI Focus

Continue scanning the public organization, with current planning focus on:

- `de-anthropocentric-research-engine`
- `literature-engine`
- `semantic-scholar-mcp`
- `web-browsing`
- `knowledge-structuring`
- `wiki-vault`
- `convergence`
- `stress-test`
- `experiment-execution`

## Summary

The upstream signals do not change the v1.0 main goal. They do justify two
pre-freeze planning adjustments:

1. Add a Campaign Catalog and MCP Config Polish planning item.
2. Add a Pod Context Lifecycle Safety Plan.

The following remain out of v1.0:

- MinerU / heavy paper ingestion fallback;
- remote execution orchestration;
- default live web or scholar networking;
- copying upstream implementation code.

## Safety Boundary

- No upstream source code was copied.
- No private data was read.
- No private VGGT path was read.
- No large feature was implemented.
- No planned item was marked observed.
- No final paper or experiment success claim was added.
