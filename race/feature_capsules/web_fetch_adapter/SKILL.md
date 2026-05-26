---
name: turingresearch-web-fetch-adapter
description: Design and implement optional safe web fetch adapters for TuringResearch Plus.
---

## Role

Design and maintain the optional Web Fetch Adapter capability.

## When to use

Use when public web pages need to enter TuringResearch workflows with source
metadata, cache policy, and source hygiene boundaries.

## Inputs

- public URL
- adapter request context
- cache policy
- source hygiene status

## Outputs

- fetched content
- source metadata
- content hash
- limitations

## Required files

- `docs/web-fetch-adapter-plan.md`
- `docs/web-content-cache-policy.md`
- `contracts/web_fetch_adapter.yaml`

## Related contracts

- `contracts/live_adapters.yaml`
- `contracts/web_fetch_adapter.yaml`

## Related lanes

- `lanes/48_web_fetch_adapter_planning.md`

## Required tests

- fake adapter tests
- no-network default tests
- source metadata tests
- cache policy tests

## Rules / constraints

- Do not fetch restricted content.
- Do not bypass login or paywall.
- Do not treat retrieved content as human verified.
- Do not require API keys for default tests.

## Done criteria

- fake adapter exists
- live adapter is opt-in
- source metadata includes URL, retrieval time, and content hash
- default tests pass without network
