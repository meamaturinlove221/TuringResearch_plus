# Lane 01: Architecture Contracts

## Scope

Define TuringResearch Plus architecture, Mermaid diagram, 16-box overview, and stable YAML contracts.

## Outputs

- `docs/architecture.md`
- `docs/architecture_16box.md`
- `contracts/*.yaml`

## Status

Phase 1 complete. Contracts are draft interfaces and contain no complex business implementation.

## Round 3 Update

2026-05-19: Added the full TuringResearch Plus MCP namespace contract surface for:

- `core.*`
- `pdf.*`
- `graph.*`
- `research.*`
- `vault.*`
- `context.*`
- `race.*`
- `paper.*`

Each tool contract includes `tool_name`, `namespace`, `input_model`, `output_model`, `cache_behavior`, `network_behavior`, `error_behavior`, `evidence_requirement`, `required_tests`, and `implementation_status`.

Round 3 remains contract-only except for previously implemented minimal local `core.*` and `pdf.*` tools. No real networking or complex business implementation was added.
