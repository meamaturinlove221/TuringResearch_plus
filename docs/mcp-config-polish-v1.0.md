# MCP Config Polish v1.0

Status: implemented minimal.

Round: 176 upstream adjustment.

The v1.0 MCP config polish absorbs upstream `.mcp.example.json` env-block
patterns while keeping TuringResearch fake/default and public-safe.

## Required Defaults

- MCP server name: `turingresearch-plus`
- command: `turingresearch-plus-mcp`
- fake/default mode: `TURINGRESEARCH_MODE=fake`
- live tests disabled: `TURINGRESEARCH_ENABLE_LIVE_TESTS=0`
- Semantic Scholar live disabled by default
- Apify live disabled by default
- Web live disabled by default
- plugin tools disabled by default
- plugin live mode disabled by default
- credential fields are blank

## Live Mode

Live mode is opt-in. A private local config may set:

- `TURINGRESEARCH_ENABLE_LIVE_TESTS=1`
- provider-specific live flags;
- provider credentials.

Do not commit private live configs.

## Tool List / Test Results Pattern

Public docs may list MCP smoke commands and expected fake/default behavior, but
they must not claim live provider success unless a live upstream-scan or live
test round records evidence.
