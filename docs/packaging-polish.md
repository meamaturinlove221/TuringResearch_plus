# Packaging Polish

Status: v0.5 minimal packaging hardening.

Round 95 checks package metadata, CLI entrypoints, MCP entrypoint references,
example environment files, and default fake-mode boundaries.

## Checked Surface

- package name: `turingresearch-plus`
- import package: `turing_research`
- import package: `turing_research_plus`
- console script: `turingresearch-plus`
- console script: `turingresearch-plus-mcp`
- MCP entrypoint: `turing_research.mcp_server:main`
- example MCP config: `.mcp.example.json`
- example env config: `.env.example`

## Defaults

- Live adapters disabled by default.
- Live tests skipped by default.
- No real API key required for default tests.
- Fake mode examples remain the public default.

## Secret Policy

Example files may name environment variables, but must not contain real keys,
tokens, private paths, or credentials. Provider tokens must stay blank in
examples.

## Non-Goals

- No PyPI publish.
- No automatic tag.
- No GitHub release.
- No live adapter execution.
- No promotion of proposed local helpers into frozen public MCP APIs.
