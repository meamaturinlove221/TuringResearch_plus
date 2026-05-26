# Feature Capsule: apify_adapter

## Problem

TuringResearch Plus needs an optional Apify-backed public web retrieval path
without making Apify or network access required for default workflows.

## VGGT motivating example

VGGT related-work workflows may need richer retrieval of public project pages
or README-style pages. Apify can help later, but default VGGT examples must stay
offline and fake-mode friendly.

## Upstream inspiration

Neocortica-Web includes an Apify REST API client and real integration tests.
TuringResearch should absorb the adapter boundary, env policy, and test
discipline, not copy code.

## User story

As a maintainer, I want Apify behind an optional adapter so live retrieval can
be manually tested without affecting fake/default workflows.

## Inputs

- public URL or search request
- optional `APIFY_TOKEN`
- adapter request context
- source hygiene status

## Outputs

- `ApifyRunResult`
- normalized web content
- source metadata
- run id metadata
- content hash
- typed errors

## Data model

- `ApifyRequest`
- `ApifyRunResult`
- `SourceMetadata`
- `AdapterError`

## Proposed commands / tools

- command: `turing web apify-run`
- tool: `web.apify_run_optional`
- output: `ApifyRunResult`

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

- fake Apify adapter test
- missing token typed error test
- live skipped-by-default test
- source hygiene test
- cache metadata test

## Risks

- accidental network in default tests
- token leakage
- provider rate limits
- over-trusting fetched pages

## Done criteria

- fake adapter implemented
- live adapter guarded by explicit opt-in
- `APIFY_TOKEN` optional outside live mode
- source metadata records provider, source URL, retrieval time, and content hash

## Release target

v0.3 Sprint 2.

## Non-goals

- no default network
- no login or paywall bypass
- no restricted content fetch
- no final research claim generation
