# Lane 239 - Tool Surface Audit

Status: completed.

Round: 261.

## Goal

Audit whether TuringResearch has tool surfaces corresponding to the original
reference repositories, without adding new functionality.

## Result

Overall status: `PARTIAL TOOL SURFACE PARITY`.

The repository has broad local Python surfaces and a narrow safe MCP stdio
smoke surface. Some original-reference workflows still need a clearer
operator-facing fake/default tool path.

## Covered

Neocortica-Session:

- preflight
- context pack
- transfer policy
- launch policy
- return manifest
- memory policy

Neocortica-Scholar:

- paper search
- paper content
- paper reference
- paper reading
- cached markdown
- fallback policy

Neocortica-Web:

- web_fetching
- web_content
- Apify optional
- cache
- source metadata

yogsoth:

- campaign routing
- research catalog
- vault
- ontology
- convergence
- stress test
- experiment execution

## Key Gap

The next gap is not more capability names. It is clearer fake/default tool paths
that connect the local Python surfaces into operator-facing workflows.

## Safety

- No new tool implementation was added.
- No MCP server was started.
- No live network, remote command execution, SSH/tmux/provision, automatic
  experiment execution, evidence ledger mutation, ARIS runtime, or child repo
  creation was performed.
- Planned and fake/default surfaces remain separate from observed results.

## Outputs

- `docs/original-reference-tool-surface-audit.md`
- `docs/neo` + `cortica-tool-surface-matrix.md`
- `docs/yogsoth-tool-surface-matrix.md`
- `docs/missing-tool-surface-actions.md`
- `contracts/original_reference_tool_surface.yaml`
- `tests/contract/test_original_reference_tool_surface.py`
