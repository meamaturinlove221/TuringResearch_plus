# Web Content Usage Guide

Status: v1.2 usage guide.

Round: 238.

`web_content` is the review surface for already fetched or cached web content.
It exists to keep provenance visible and prevent fetched text from being
mistaken for verified evidence.

## Inputs

`web_content` can be created from:

- a `WebFetchResult`;
- a `WebContentCacheRecord`.

Both paths preserve source metadata, content hash, cache key, and source hygiene
status.

## Review Boundary

All `web_content` outputs keep:

- `human_verified: false`;
- `requires_human_review: true`.

This content can inform method cards, related-work notes, advisor packs, or
dashboard summaries, but it does not become a paper conclusion without human
review.

## Cache and Provenance

Cache records must use hashed keys rather than raw URLs as filenames. Cached
content should keep retrieval time, content hash, provider/source metadata, and
source hygiene status.

## Disallowed Content

`web_content` must not include secrets, private datasets, paywalled material,
login-only pages, cookies, private local paths, or restricted model files.
