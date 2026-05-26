# Round 360.5 - MCP Example / Env Block Public Hygiene

Status: complete

## Objective

Harden the public MCP example and env block documentation so public config
remains fake/default, placeholder-only, and live-disabled by default.

## Files

- `.mcp.example.json`
- `docs/mcp-public-config-guide.md`
- `docs/env-block-public-hygiene.md`
- `docs/no-dotenv-public-policy.md`
- `tests/contract/test_mcp_public_hygiene.py`
- `tests/contract/test_no_secrets_in_public_config.py`
- `lanes/360_5_mcp_env_public_hygiene.md`
- `lanes/00_master_ledger.md`

## Decisions

- Public MCP template keeps compatibility server key and command.
- Scholar, Web, Apify, SFTP, plugins, and live tests remain disabled by
  default.
- Credential fields remain blank placeholders.
- `.env` remains forbidden outside explicit test fixtures.
- Live mode requires explicit private env.

## Non-actions

- No `.env` file committed.
- No token committed.
- No real API key committed.
- No live provider enabled.
- No SFTP connection enabled.
- No package, CLI, MCP, or import rename.

## Validation

- MCP public hygiene tests: passed.
- Secret scan: passed.
- Regression gate: passed.
- Full test suite: passed (`2023 passed, 10 deselected`).
- `python -m ruff check .`: passed.
- `python -m mypy src`: passed.
- `git diff --check`: passed with LF-to-CRLF working-copy warning only.
