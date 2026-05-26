# MCP Config Troubleshooting

Status: v1.2 parity troubleshooting.

Round: 239.

## The MCP Server Does Not Start

Check that the command is:

```powershell
turingresearch-plus-mcp --manifest
```

Then confirm the local package is installed in editable mode if you are running
from a checkout.

## A Live Adapter Is Skipped

This is expected by default. Live tests require:

- `TURINGRESEARCH_ENABLE_LIVE_TESTS=1`;
- the provider-specific live flag;
- private local credentials where required.

Do not change `.mcp.example.json` to contain real credentials.

## Apify Reports Missing Token

That is the safe no-key behavior. Provide `APIFY_TOKEN` only in a private local
environment if you are intentionally running a live Apify check.

## Web Fetch Returns Dry-run

That is expected in fake/default mode. Web live mode requires explicit private
opt-in and must not fetch private or restricted content.

## Semantic Scholar Uses Fake Mode

That is expected in public docs and default tests. Enable Semantic Scholar live
only in private local configuration.

## Plugin Tools Are Missing

Plugin tools are disabled by default. This protects public users from unknown
plugin execution and keeps the MCP surface reviewable.

## What Not To Paste Into Issues

Do not paste API keys, tokens, `.env` files, private paths, raw data paths,
cookies, local project link files, or private logs.
