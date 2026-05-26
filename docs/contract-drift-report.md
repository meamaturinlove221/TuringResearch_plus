# TuringResearch Plus Contract Drift Report

Round 17 audited the frozen MCP tool namespace and contract/docs alignment for `v0.1.0`.

## Scope

- Contract files: `contracts/*.yaml`
- Public tool documentation: `docs/mcp-tools.md`
- Approved namespaces: `core.*`, `pdf.*`, `graph.*`, `research.*`, `vault.*`, `context.*`, `race.*`, `paper.*`

## Tool Count

| Namespace | Tools |
| --- | ---: |
| `core.*` | 11 |
| `pdf.*` | 9 |
| `graph.*` | 9 |
| `research.*` | 22 |
| `vault.*` | 8 |
| `context.*` | 5 |
| `race.*` | 7 |
| `paper.*` | 8 |
| Total | 79 |

## Findings

- Contract tools and `docs/mcp-tools.md` tools are symmetric: 79 to 79.
- No unapproved MCP namespace is declared in contracts or public tool docs.
- Implementation status drift was fixed: contract statuses now match public docs.
- YAML status/type concatenation was fixed in Core, PDF, Fusion, Race, and Paper contracts.
- `contracts/artifact_schema.yaml` now includes `implemented_dry_run` as an approved `implementation_status`.

## Status Distribution

| Status | Count |
| --- | ---: |
| `implemented_minimal` | 42 |
| `implemented_dry_run` | 24 |
| `contract_only` | 13 |

## Fixes Applied

- Synchronized contract `implementation_status` values with `docs/mcp-tools.md`.
- Updated stale Round 3 rules in Fusion, Race, and Paper contracts to the v0.1.0 release-candidate scope.
- Added `tests/contract/test_tool_namespace_integrity.py`.
- Added `tests/contract/test_contract_schema_integrity.py`.

## Remaining Contract Risks

The frozen v0.1.0 namespace is internally consistent. Remaining risk is intentional release scope: contract-only tools still require future implementation rounds and must not be advertised as default live capabilities.
