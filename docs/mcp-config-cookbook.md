# MCP Config Cookbook

Status: v1.2 parity cookbook.

Round: 239.

## Fake / Default

Use the committed `.mcp.example.json` as-is for local smoke checks.

Expected behavior:

- no API key required;
- no live network adapter enabled;
- no plugin tool enabled;
- MCP manifest can be inspected locally;
- all provider credential fields remain blank.

Smoke command:

```powershell
turingresearch-plus-mcp --manifest
```

## Private Semantic Scholar Live

Do not commit this configuration. In a private local config only, a maintainer
may set:

```json
{
  "TURINGRESEARCH_MODE": "live",
  "TURINGRESEARCH_ENABLE_LIVE_TESTS": "1",
  "TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE": "1",
  "SEMANTIC_SCHOLAR_API_KEY": "<private value>"
}
```

Semantic Scholar output is retrieved source context and still requires human
review.

## Private Apify Live

Do not commit this configuration. In a private local config only, a maintainer
may set:

```json
{
  "TURINGRESEARCH_MODE": "live",
  "TURINGRESEARCH_ENABLE_LIVE_TESTS": "1",
  "TURINGRESEARCH_ENABLE_APIFY_LIVE": "1",
  "APIFY_TOKEN": "<private value>"
}
```

If no token is present, Apify should return a graceful missing-token result.

## Private Web Fetch Live

Do not commit this configuration. In a private local config only, a maintainer
may set:

```json
{
  "TURINGRESEARCH_MODE": "live",
  "TURINGRESEARCH_ENABLE_LIVE_TESTS": "1",
  "TURINGRESEARCH_ENABLE_WEB_LIVE": "1"
}
```

Web live mode must not bypass login, bypass paywalls, fetch private content, or
store cookies.

## Plugins

Keep these defaults unless a future plugin review explicitly changes them:

```json
{
  "TURINGRESEARCH_ENABLE_PLUGINS": "0",
  "TURINGRESEARCH_ENABLE_PLUGIN_LIVE_MODE": "0"
}
```
