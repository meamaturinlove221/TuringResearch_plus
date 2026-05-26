# MCP Env Block Policy

Status: implemented minimal.

Round: 176 upstream adjustment.

`.mcp.example.json` must use an explicit `env` block so default behavior is
reviewable from the committed template.

## Required Env Values

```json
{
  "TURINGRESEARCH_MODE": "fake",
  "TURINGRESEARCH_ENABLE_LIVE_TESTS": "0",
  "TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE": "0",
  "TURINGRESEARCH_ENABLE_APIFY_LIVE": "0",
  "TURINGRESEARCH_ENABLE_WEB_LIVE": "0",
  "TURINGRESEARCH_ENABLE_SFTP_LIVE": "0",
  "TURINGRESEARCH_ENABLE_PLUGINS": "0",
  "TURINGRESEARCH_ENABLE_PLUGIN_LIVE_MODE": "0",
  "SEMANTIC_SCHOLAR_API_KEY": "",
  "APIFY_TOKEN": "",
  "OPENAI_API_KEY": "",
  "GITHUB_TOKEN": "",
  "TURINGRESEARCH_SFTP_CREDENTIAL": "",
  "TURINGRESEARCH_SFTP_KEY_PATH": "",
  "TURINGRESEARCH_SFTP_TARGET": ""
}
```

## Policy

- Blank credential fields are placeholders, not secrets.
- Live mode is opt-in.
- `TURINGRESEARCH_ENABLE_LIVE_TESTS=1` is required before live tests run.
- Scholar, Web, Apify, and SFTP live flags are disabled by default.
- Plugin tools disabled by default.
- Do not store private paths, raw data paths, or provider tokens in committed
  MCP configs.
