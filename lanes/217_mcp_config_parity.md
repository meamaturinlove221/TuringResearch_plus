# Lane 217 - MCP Config Parity

Status: completed.

Round: 239.

## Goal

Unify the public MCP config template, env block policy, live/fake examples, and
provider troubleshooting so Scholar and Web parity can share a clear
fake/default setup path.

## Implemented

- Hardened `.mcp.example.json` with schema/status/capability metadata.
- Added MCP config parity docs.
- Added MCP config cookbook.
- Added MCP config troubleshooting.
- Added contract tests for MCP config shape and env block policy.

## Defaults

- Fake mode is default.
- Live mode is opt-in.
- Semantic Scholar live is optional and disabled by default.
- Apify live is optional and disabled by default.
- Web fetch live is optional and disabled by default.
- Plugin tools are disabled by default.
- Credential placeholders are blank.

## Explicit Non-goals

- No new adapter feature.
- No live provider call.
- No real API key.
- No plugin enablement.
- No public release action.

## Safety

- The committed template contains no secrets.
- Provider credentials belong only in private local configuration.
- Live outputs remain retrieved context and require human review.
