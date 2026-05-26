# Public-facing Old Name Inventory

Round: 360.2
Status: reviewed

## Scope

This inventory covers the public-facing sweep for the open source name
TuringResearch. The sweep read the README, docs, docs-site, examples,
split-ready bundles, split-manual packs, MCP example config, package metadata,
changelog, version file, and the public naming policy.

## Removed From Current Public Surfaces

The public display name now uses TuringResearch in:

- top-level `README.md`;
- current docs entry points under `docs/README.md`, `docs/install.md`,
  `docs/faq.md`, `docs/examples.md`, `docs/docs-index.md`,
  `docs/mcp-tools.md`, `docs/local-install-smoke.md`, and
  `docs/troubleshooting.md`;
- `examples/` public README, portfolio, public demo, split export, split repo,
  plugin demo metadata, capability manifest, and VGGT review fixtures;
- `split_ready/` public-safe bundle text;
- `split_manual/` public-safe manual-pack text;
- `.mcp.example.json` display description;
- `pyproject.toml` display description;
- `CHANGELOG.md` current display prose.

## Compatibility Names Still Present

The following names remain intentionally because changing them would be a
package, CLI, MCP, or import compatibility change:

| Compatibility surface | Status | Reason |
| --- | --- | --- |
| `turingresearch-plus` | retained | current package distribution and MCP server key |
| `turingresearch-plus-mcp` | retained | current console script |
| `turing_research_plus` | retained | current Python compatibility namespace and module paths |
| `src/turing_research_plus/` | retained | code path and import compatibility |

These compatibility names are not the public brand. Future package and CLI
rounds must decide whether to rename them after checking package availability,
entrypoint compatibility, and migration cost.

## Prior Name Status

The old `Tul` + `ingResearch` spelling remains forbidden outside historical
rename checkpoint files. This sweep did not reintroduce that spelling.

## Historical Docs

Older release notes and planning documents may still describe historical
states. This round does not rewrite every archived release narrative. The new
contract focuses on current public entry points and public-safe bundles so the
front door reads as TuringResearch without breaking audit history.

## Public URL Boundary

No fake GitHub URL, public deployment URL, or child-repository URL was added.
Manual split-pack placeholders remain placeholders.
