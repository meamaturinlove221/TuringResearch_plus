# Web Fetch Adapter

Status: implemented minimal.

The Web Fetch Adapter gives TuringResearch Plus a fake-first way to ingest
public web pages, local HTML fixtures, and optional live HTTP fetches. Default
tests and workflows do not access the network.

## Behavior

- Default path: fake or local fixture.
- Live path: requires explicit `live_enabled=True` and `dry_run=False`.
- Live tests: skipped unless `TURINGRESEARCH_ENABLE_LIVE_TESTS=1`.
- Outputs are retrieved content, not human-verified evidence.

## Output

`WebFetchResult` records:

- `url`
- `retrieval_status`
- `retrieval_time`
- `source_type`
- `content_type`
- optional `title`
- optional `text_content`
- optional `html_content`
- `content_hash`
- `cache_key`
- warnings
- limitations
- `requires_human_review`

## Cache

`WebContentCache` stores records by hashed URL and records retrieval time,
content hash, source metadata, hit/miss/stale status, and manual fixture mode.

## Safety

- Do not bypass login or paywalls.
- Do not fetch restricted or private content.
- Do not store cookies or tokens.
- Do not mark web content as verified by default.
- Do not turn web content directly into paper conclusions.

## VGGT Use

VGGT workflows can use local fixtures or explicitly retrieved public pages to
seed method cards, Figure-to-Architecture notes, and related-work positioning.
The adapter does not replace real paper reading.
