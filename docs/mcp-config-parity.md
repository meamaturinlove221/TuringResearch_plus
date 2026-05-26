# MCP Config Parity

Status: v1.2 parity hardening.

Round: 239.

This document locks the MCP config shape used by TuringResearch after the
Scholar and Web parity rounds. The goal is easy local setup without weakening
the fake/default safety boundary.

## Required Shape

The committed `.mcp.example.json` must contain:

- one server named `turingresearch-plus`;
- command `turingresearch-plus-mcp`;
- args `["--manifest"]`;
- an explicit `env` block;
- blank credential placeholders;
- provider live flags disabled by default;
- SFTP live flag disabled by default;
- plugin tools disabled by default;
- notes that live mode belongs only in private local config.

## Required Defaults

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

## Optional Live Providers

Semantic Scholar, Apify, Web fetch, and SFTP are optional live surfaces.
Enabling any of them requires a private local config,
`TURINGRESEARCH_ENABLE_LIVE_TESTS=1`, the provider-specific live flag, and a
private credential where applicable.

Live output remains retrieved context. It is not observed evidence, not a paper
claim, and not a release result without human review.

## Plugin Boundary

Plugin tools stay disabled by default. A plugin proposal must pass permission,
review, and safety gates before any plugin surface is exposed.

## Public Safety

The committed example must not include real keys, private paths, raw data paths,
cookies, private dataset locations, or local project link files.
