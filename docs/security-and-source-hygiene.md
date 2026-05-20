# TulingResearch Plus Security And Source Hygiene

Date: 2026-05-20

## Security Posture

- Default tests require no real API keys.
- Default tests require no real network access.
- STDIO MCP mode does not write operational logs to stdout.
- Live/manual tests must be explicitly marked and skipped by default.
- Secrets must not be committed to docs, examples, fixtures, or config files.

## Source Hygiene Policy

Allowed source categories:

- public repos
- public README files
- public issues
- public release notes
- user-owned notes
- authorized transcripts

Blocked source categories:

- private repository content
- leaked roadmap material
- NDA content
- proprietary code
- copied implementation details from incompatible licenses

## Safe Implementation Modes

- independent clean-room implementation
- concept-level reimplementation
- compatible-license reuse
- documentation-only watch

## Release Gate

Race Mode cannot create implementation tasks until Source Hygiene Gate passes. Unknown or blocked sources can only produce watch or documentation outputs.
