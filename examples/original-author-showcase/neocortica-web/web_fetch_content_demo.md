# Web Fetch / Content Showcase

## Source

- Upstream repository: `Pthahnix/Neocortica-Web`
- Source basis: web fetching, web content, cache, metadata, and MCP web tool workflow
- Upstream reference commit: `94449c7b77241d97f052b462c397caa5aab654c0`
- Migration type: `adapted_with_authorization`
- Code migration: none

## Summary

This academic workflow output separates web ingestion into fetch, content extraction, cache, and metadata layers. The key idea is that a research workflow should not treat a webpage as an unstructured blob; it should preserve source URL, fetch mode, cache state, extraction quality, and safety status.

## Workflow

### 1. Web Fetch

Retrieve public web content or load a fake fixture. Record the requested URL, normalized URL, retrieval mode, and timestamp.

### 2. Web Content Extraction

Extract title, main content, relevant links, and structured metadata. Keep extraction warnings and quality flags.

### 3. Cache Manifest

Store cache records with source URL, content hash, created time, and fake/live status.

### 4. Research Use

Convert extracted content into upstream watch reports, project summaries, paper/source notes, or reference parity dashboards.

## TuringResearch Demonstration

This showcase maps to:

- web tool surface;
- URL normalization;
- cache manifest;
- source metadata;
- upstream watch;
- public-source research intake.

## Safety Boundary

No private pages, cookies, login-protected content, tokens, or raw private web output are included here. Live web access remains opt-in.

## Attribution

Adapted with attribution from authorized Neocortica-Web workflow materials.
