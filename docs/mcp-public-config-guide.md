# MCP Public Config Guide

Round: 360.5
Status: public hygiene guide

## Purpose

`.mcp.example.json` is a public-safe template for local MCP review. It is not a
private live config and must not contain credentials, tokens, private local
paths, raw data paths, cookies, or deployment-specific targets.

## Default Mode

The committed template must run in fake/default mode:

```json
{
  "TURINGRESEARCH_MODE": "fake",
  "TURINGRESEARCH_ENABLE_LIVE_TESTS": "0",
  "TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE": "0",
  "TURINGRESEARCH_ENABLE_WEB_LIVE": "0",
  "TURINGRESEARCH_ENABLE_APIFY_LIVE": "0",
  "TURINGRESEARCH_ENABLE_SFTP_LIVE": "0",
  "TURINGRESEARCH_ENABLE_PLUGINS": "0",
  "TURINGRESEARCH_ENABLE_PLUGIN_LIVE_MODE": "0"
}
```

## Credential Placeholders

Credential fields must be blank strings in the committed template:

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

Blank strings are placeholders, not secrets. Real values belong only in private
local environment variables or private local config files that are not
committed.

## Optional Live Boundary

Scholar, Web, Apify, and SFTP live modes are optional and disabled by default.
Live mode requires explicit private env:

```text
TURINGRESEARCH_ENABLE_LIVE_TESTS=1
TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE=1
TURINGRESEARCH_ENABLE_WEB_LIVE=1
TURINGRESEARCH_ENABLE_APIFY_LIVE=1
TURINGRESEARCH_ENABLE_SFTP_LIVE=1
```

Provider credentials must never be committed. SFTP live must not run remote
commands, remote delete, or implicit remote writes.

## Public Hygiene Rules

- Do not commit `.env`.
- Do not commit real API keys or tokens.
- Do not commit private local paths.
- Do not commit cookies or login material.
- Do not commit raw data paths.
- Do not enable live adapters in the public template.
- Do not promote live retrieved context to observed evidence without human
  review.
