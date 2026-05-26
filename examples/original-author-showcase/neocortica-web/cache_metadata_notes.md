# Web Cache and Metadata Notes

## Source

- Upstream repository: `Pthahnix/Neocortica-Web`
- Source basis: web cache, source metadata, URL normalization, and web content workflow
- Upstream reference commit: `94449c7b77241d97f052b462c397caa5aab654c0`
- Migration type: `summarized_with_attribution`
- Code migration: none

## Summary

This showcase captures a web-ingestion idea: research systems should keep provenance for fetched web content. A cached web result should record where it came from, when it was fetched, whether it was fake or live, and how it was normalized.

## Metadata Fields

A public-safe web cache record should include:

- original URL;
- normalized URL;
- retrieval mode: fake / cached / live;
- content hash;
- extraction timestamp;
- source title if available;
- extraction warnings;
- redaction status;
- downstream artifact IDs.

## TuringResearch Demonstration

This maps to:

- URL normalization;
- cache manifest;
- source metadata;
- upstream watch;
- artifact provenance;
- public-source evidence references.

## Safety Boundary

Do not cache private pages, cookies, login-protected content, raw user messages, or unredacted live output.

## Attribution

Summarized with attribution from authorized Neocortica-Web workflow materials.
