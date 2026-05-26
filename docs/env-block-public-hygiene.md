# Env Block Public Hygiene

Round: 360.5
Status: policy locked

## Public Env Blocks

Public env blocks in README, docs, examples, and `.mcp.example.json` must use
fake/default mode and disabled live flags. They may show variable names, but
must not include real credentials.

## Required Disabled Live Flags

```text
TURINGRESEARCH_MODE=fake
TURINGRESEARCH_ENABLE_LIVE_TESTS=0
TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE=0
TURINGRESEARCH_ENABLE_WEB_LIVE=0
TURINGRESEARCH_ENABLE_APIFY_LIVE=0
TURINGRESEARCH_ENABLE_SFTP_LIVE=0
TURINGRESEARCH_ENABLE_PLUGINS=0
TURINGRESEARCH_ENABLE_PLUGIN_LIVE_MODE=0
```

## Allowed Placeholder Values

The only committed credential placeholders are blank strings or documented
placeholder text in prose. Public config files must use blank strings:

```json
{
  "SEMANTIC_SCHOLAR_API_KEY": "",
  "APIFY_TOKEN": "",
  "OPENAI_API_KEY": "",
  "GITHUB_TOKEN": "",
  "TURINGRESEARCH_SFTP_CREDENTIAL": "",
  "TURINGRESEARCH_SFTP_KEY_PATH": "",
  "TURINGRESEARCH_SFTP_TARGET": ""
}
```

## Secret Scan Expectations

Public config checks should fail if they find:

- token-like values;
- private local paths;
- `.env` files;
- private key files;
- live flags enabled in committed templates;
- fake/demo or live output written as observed evidence.
