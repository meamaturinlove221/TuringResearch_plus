# MCP Config Examples

Status: v0.7 distribution polish.

All examples are safe templates. They use blank credential values and keep live
mode disabled by default.

## Fake / Default Config

Use `.mcp.example.json`:

```json
{
  "mcpServers": {
    "turingresearch-plus": {
      "command": "turingresearch-plus-mcp",
      "args": ["--manifest"],
      "env": {
        "TURINGRESEARCH_MODE": "fake",
        "TURINGRESEARCH_ENABLE_LIVE_TESTS": "0",
        "TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE": "0",
        "TURINGRESEARCH_ENABLE_APIFY_LIVE": "0",
        "TURINGRESEARCH_ENABLE_WEB_LIVE": "0",
        "TURINGRESEARCH_ENABLE_PLUGINS": "0",
        "TURINGRESEARCH_ENABLE_PLUGIN_LIVE_MODE": "0",
        "SEMANTIC_SCHOLAR_API_KEY": "",
        "APIFY_TOKEN": "",
        "OPENAI_API_KEY": "",
        "GITHUB_TOKEN": ""
      }
    }
  }
}
```

## Private Live Config Pattern

Do not commit private live configs. If a maintainer explicitly opts in locally,
use a private file outside the repo with provider credentials supplied by the
user.

Required boundaries:

- live mode is opt-in;
- `TURINGRESEARCH_ENABLE_LIVE_TESTS=1` is required before live tests run;
- Semantic Scholar, Apify, and Web live adapters remain disabled until their
  provider-specific live flags are also enabled;
- credentials remain outside committed files;
- live adapter output is retrieved material;
- plugin tools remain disabled unless separately reviewed.

## Plugin Registry Pattern

Plugin registry entries can be reviewed with local helpers, but they are not
enabled by `.mcp.example.json`.

Safe default:

- `TURINGRESEARCH_ENABLE_PLUGINS=0`
- `TURINGRESEARCH_ENABLE_PLUGIN_LIVE_MODE=0`

## What Not To Commit

- real API keys;
- provider tokens;
- private project paths;
- raw data paths;
- local live configs;
- generated logs containing credentials.
