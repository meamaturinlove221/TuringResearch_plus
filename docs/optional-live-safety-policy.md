# Optional Live Safety Policy

Status: policy locked.

Round: 344.

Optional live surfaces must remain private, explicit, and disabled by default.
Fake/default operation must continue to work without credentials, network, SSH,
or remote machines.

## Global Rules

1. Live tests are skipped unless `TURINGRESEARCH_ENABLE_LIVE_TESTS=1`.
2. Provider-specific live flags must also be enabled.
3. Credentials must never be committed.
4. Reports must not log secrets.
5. Live output is retrieved context, not observed evidence.
6. Human review is required before live output can support a public claim.

## Scholar Live

- Optional only.
- No API key required for fake mode.
- No automatic paper download.
- No paywall bypass.
- No fake citation marked verified.

## Web / Apify Live

- Optional only.
- No default network access.
- No login bypass.
- No private content scraping.
- No cookie storage.
- No automatic evidence promotion.

## SFTP Live

- Optional only.
- No default SSH or SFTP.
- No remote command execution.
- No remote delete.
- No remote write except a future reviewed explicit transfer target.
- Path traversal must remain blocked.

## MCP Env Block

Committed MCP example config must keep live flags disabled and credential
fields blank. Private local MCP config may override those values only outside
the repository.

## Safety Decision

If any live flag or credential is missing, live surfaces should skip with a
reviewable status instead of attempting network or remote access.
