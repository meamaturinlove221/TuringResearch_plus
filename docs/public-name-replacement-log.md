# Public Name Replacement Log

Round: 360.2
Status: complete

## Replacements Applied

| Area | Files | Replacement |
| --- | --- | --- |
| README | `README.md` | Public title and project prose now say TuringResearch. |
| Current docs entry points | `docs/README.md`, `docs/install.md`, `docs/faq.md`, `docs/examples.md`, `docs/docs-index.md`, `docs/mcp-tools.md`, `docs/local-install-smoke.md`, `docs/troubleshooting.md` | Public titles and display prose now say TuringResearch. |
| Package metadata | `pyproject.toml` | Display description now says TuringResearch; package name and scripts remain compatibility names. |
| MCP example | `.mcp.example.json` | Display description now says TuringResearch; server key, command, and module paths remain compatibility names. |
| Examples | `examples/` public README, portfolio, public demo, split export, split repo, VGGT review fixture, and plugin metadata files | Public-facing brand text now says TuringResearch. |
| Split bundles | `split_ready/`, `split_manual/` | Public-safe bundle text now says TuringResearch. |
| Changelog | `CHANGELOG.md` | Current display prose now says TuringResearch while compatibility package names remain literal. |
| Docs-site manifests | `docs-site/dist_manifest.yaml`, `docs-site/release_bundle/dist_manifest.yaml`, `docs-site/release_bundle_manifest.yaml` | Local absolute `dist_root` path was replaced with a relative path and the bundle manifest hash was refreshed. |
| Tests | `tests/contract/test_local_install_assumptions.py`, `tests/workflow/test_vggt_public_case_study.py`, `tests/workflow/test_vggt_split_pack_freshness.py` | Assertions now expect the public repository name TuringResearch. |

## Non-replacements

| Name | Why retained |
| --- | --- |
| `turingresearch-plus` | Current package distribution and MCP server key. |
| `turingresearch-plus-mcp` | Current console command. |
| `turing_research_plus` | Python compatibility namespace and module paths. |
| Historical release prose | Kept as audit history unless it is a current public entry point. |

## Safety Notes

- No Python import compatibility was removed.
- No CLI or MCP command was renamed.
- No fake GitHub URL was added.
- No release, tag, PyPI upload, child repository creation, or deployment was performed.
