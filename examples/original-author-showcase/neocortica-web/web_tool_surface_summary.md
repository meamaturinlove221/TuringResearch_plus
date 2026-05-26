# Neocortica-Web Tool Surface Summary

## Source

- Upstream repository: `Pthahnix/Neocortica-Web`
- Upstream path: README and web tool materials
- Upstream commit: to be filled by local migration pass
- Migration type: `summarized_with_attribution`
- Authorization: user-reported authorization from the original developer

## Short Summary

Neocortica-Web demonstrates a web-oriented MCP tool surface that separates web fetching, content extraction, caching, source metadata, and optional Apify-backed live collection. It emphasizes public-safe configuration, no hard-coded secrets, and fake/live separation.

## What This Demonstrates in TuringResearch

TuringResearch uses this showcase to explain its web and source-ingestion layer:

- web fetching and content extraction;
- URL normalization;
- cache manifest and source metadata;
- optional Apify workflows;
- live output redaction;
- no-dotenv public configuration.

## Safety Notes

This showcase does not include API keys, cookies, private pages, login-protected scraping, or raw live outputs. Live web and Apify usage remains opt-in and disabled by default.

## Attribution

This workflow summary is derived from the authorized reference project `Pthahnix/Neocortica-Web` and is included as an attributed academic showcase inside TuringResearch.
