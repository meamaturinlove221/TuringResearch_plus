# Live / Fake Config Examples

Status: implemented minimal.

Round: 176 upstream adjustment.

## Fake / Default

Use the committed `.mcp.example.json`. It is safe for public docs:

- fake/default mode;
- no real API key;
- no live network access;
- plugin tools disabled by default;
- no private local paths.

## Private Live Config Shape

Do not commit this. A maintainer may create a private local config with:

```json
{
  "TURINGRESEARCH_MODE": "live",
  "TURINGRESEARCH_ENABLE_LIVE_TESTS": "1",
  "TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE": "1",
  "TURINGRESEARCH_ENABLE_APIFY_LIVE": "1",
  "TURINGRESEARCH_ENABLE_WEB_LIVE": "1",
  "TURINGRESEARCH_ENABLE_PLUGINS": "0",
  "TURINGRESEARCH_ENABLE_PLUGIN_LIVE_MODE": "0"
}
```

Provider credentials belong only in private local configuration or environment
variables. They must not be committed.

## Boundary

Live retrieval is retrieved material, not human-verified evidence. It must pass
source hygiene, evidence, privacy, and human-review gates before public claims.
