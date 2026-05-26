---
name: turingresearch-apify-adapter
description: Design and implement optional Apify-backed public web retrieval for TuringResearch Plus.
---

## Role

Design and maintain the optional Apify adapter.

## When to use

Use when public web retrieval needs an Apify-backed live adapter while keeping
fake mode as the default.

## Inputs

- public URL or search request
- adapter request context
- optional `APIFY_TOKEN`
- source hygiene status

## Outputs

- normalized web content
- source metadata
- content hash
- typed errors

## Required files

- `docs/apify-adapter-plan.md`
- `contracts/web_fetch_adapter.yaml`

## Related contracts

- `contracts/live_adapters.yaml`
- `contracts/web_fetch_adapter.yaml`

## Related lanes

- `lanes/48_web_fetch_adapter_planning.md`

## Required tests

- fake Apify adapter tests
- missing token tests
- live skipped-by-default tests
- source metadata tests

## Rules / constraints

- Do not require `APIFY_TOKEN` for default tests.
- Do not bypass login or paywall.
- Do not fetch restricted content.
- Do not mark live results as human verified.

## Done criteria

- fake adapter exists
- live adapter is explicitly opt-in
- source metadata and cache policy are implemented
- default tests remain offline
