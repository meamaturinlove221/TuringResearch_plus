# Lane 215 - Neocortica Scholar Parity

Status: completed.

Round: 237.

## Goal

Align stable Scholar reference ideas with TuringResearch's local-first,
fake/default paper pipeline.

## Implemented

- Scholar source priority plan.
- Scholar public tool list export.
- Scholar MCP usage guide export.
- Paper source fallback policy.

## Outputs

- `src/turing_research_plus/scholar_pipeline/source_priority.py`
- `src/turing_research_plus/scholar_pipeline/tool_list_export.py`
- `src/turing_research_plus/scholar_pipeline/mcp_usage_export.py`
- `src/turing_research_plus/scholar_pipeline/fallback_policy.py`
- `contracts/neocortica_scholar_parity.yaml`
- `docs/neo` `cortica-scholar-parity.md`
- `docs/scholar-tool-list.md`
- `docs/scholar-mcp-usage-guide.md`
- `docs/paper-source-fallback-policy.md`

## Explicit Non-goals

- No MinerU.
- No heavy OCR.
- No automatic full paper download.
- No paywall bypass.
- No final paper conclusion.
- No default live networking.

## Safety

- No upstream code was copied.
- No live provider call was added.
- No real API key is required.
- Cached or fake paper material remains review context, not final evidence.
