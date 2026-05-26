# Lane 159 - CLI / MCP Install Sanity

Status: sanity check complete.

Round: 178.

## Goal

Check v1.0 CLI, MCP, install, fake mode, live mode, and config example
surfaces without publishing or creating a release.

## Outputs

- `docs/v1.0.0-install-sanity-report.md`
- `docs/v1.0.0-cli-mcp-sanity.md`
- `docs/v1.0.0-fake-live-mode-guide.md`
- `tests/contract/test_v1_cli_entrypoints.py`
- `tests/contract/test_v1_mcp_config_examples.py`
- `tests/contract/test_v1_fake_live_mode_defaults.py`
- `lanes/00_master_ledger.md`

## Checked

- package name: `turingresearch-plus`;
- CLI commands: `turingresearch-plus`, `turingresearch-plus-mcp`;
- MCP server name: `turingresearch-plus`;
- `.mcp.example.json` contains no real key values;
- fake mode is default;
- live mode is opt-in;
- plugin tools are disabled by default;
- old project naming is absent.

## Boundaries

- No PyPI publish.
- No GitHub release.
- No real MCP server start.
- No live networking.
- No real credentials.
- No plugin execution.
