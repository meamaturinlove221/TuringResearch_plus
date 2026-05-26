# Scholar MCP Usage Guide

Status: v1.2 MCP usage guide.

Round: 237.

## Default Config

- Server name: `turingresearch-plus`
- Command: `turingresearch-plus-mcp`
- Args: `["--manifest"]`
- Mode: `TURINGRESEARCH_MODE=fake`
- Live tests: `TURINGRESEARCH_ENABLE_LIVE_TESTS=0`
- Semantic Scholar live adapter:
  `TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE=0`

The committed `.mcp.example.json` must not contain real keys. Provider
credentials belong only in private local environment configuration.

## Usage Boundary

Scholar MCP output is review context. It does not prove that a paper was fully
read, does not create final paper claims, and does not bypass human review.

## Live Mode

Live mode is opt-in only. A maintainer may enable live adapters in a private
local config, but public tests and committed docs must remain fake/default.
