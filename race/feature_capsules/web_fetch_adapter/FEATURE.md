# Feature Capsule: web_fetch_adapter

## Problem

TuringResearch Plus needs safe public web retrieval for project pages, GitHub
README files, method pages, and arXiv HTML pages without making networking the
default path.

## VGGT motivating example

VGGT related-work analysis needs public project pages and README files for
NeuralBody, HumanRAM, HART, HGGT, and Fus3D context. Retrieved pages can seed
method cards and positioning notes, but they must not become verified claims.

## Upstream inspiration

Neocortica-Web shows useful patterns around web content tools, MCP entry
configuration, and env-block discipline. TuringResearch adopts the architecture
idea and testing boundary, not upstream code.

## User story

As a researcher, I want public web content to enter TuringResearch with source
metadata, cache policy, and source hygiene boundaries, so that I can use it for
review without treating it as verified evidence.

## Inputs

- public URL
- source hygiene status
- adapter request context
- cache policy

## Outputs

- `WebFetchResult`
- normalized content
- source URL
- retrieval time
- content hash
- warnings and limitations

## Data model

- `WebFetchRequest`
- `WebFetchResult`
- `WebContentCacheRecord`
- `SourceMetadata`

## Proposed commands / tools

- command: `turing web fetch`
- tool: `web.fetch`
- output: `WebFetchResult`

The tool is proposed only until a contracts-first implementation round accepts
the public namespace.

## Related contracts

- `contracts/live_adapters.yaml`
- `contracts/web_fetch_adapter.yaml`

## Related skills

- `turingresearch-architecture-contracts`
- `turingresearch-core-reproduction`
- `turingresearch-qa-release`

## Required tests

- fake adapter test
- no-network default test
- source hygiene block test
- cache metadata test
- source metadata test
- live skipped-by-default test

## Risks

- accidental default network access
- restricted content fetch
- retrieved content treated as verified
- unsafe cache content

## Done criteria

- fake adapter exists
- default tests require no network
- live mode requires explicit opt-in
- source metadata includes source URL, retrieval time, and content hash
- restricted content is blocked

## Release target

v0.3 Sprint 2.

## Non-goals

- no login or paywall bypass
- no restricted content fetch
- no final paper conclusion generation
- no automatic human verification
