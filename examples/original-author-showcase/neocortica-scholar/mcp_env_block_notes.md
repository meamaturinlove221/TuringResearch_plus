# Scholar MCP Env Block Notes

## Source

- Upstream repository: `Pthahnix/Neocortica-Scholar`
- Source basis: README / MCP configuration style / public configuration notes
- Upstream reference commit: `105ab8b7aa8d8db4b9c296e3c1c339b5952eabb1`
- Migration type: `summarized_with_attribution`
- Code migration: none

## Summary

The academic/product workflow output here is a public configuration pattern: keep the MCP example explicit, keep live adapters optional, and avoid publishing `.env`-style files that may encourage secrets to enter the repository.

## Public Configuration Principles

1. Fake mode should work without keys.
2. Live mode should require explicit environment variables.
3. `.mcp.example.json` should contain only placeholders.
4. README should explain which tools are fake, cached, optional-live, or unavailable.
5. CI should skip live tests by default.
6. No token, API key, cookie, SSH path, or private host should appear in public config.

## TuringResearch Demonstration

This maps to:

- `.mcp.example.json` public hygiene;
- optional Scholar / Web / Apify / SFTP live mode;
- no-dotenv public policy;
- no-secrets-in-public-config tests;
- README quickstart with fake mode default.

## Safety Boundary

This is a configuration policy note, not a live adapter. It contains no credential and no real endpoint.

## Attribution

Summarized with attribution from authorized Neocortica-Scholar public configuration materials.
