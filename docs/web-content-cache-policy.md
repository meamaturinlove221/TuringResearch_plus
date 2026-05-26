# Web Content Cache Policy

Status: v0.3 Sprint 3 design draft.

The Web Content Cache stores public fetched web content for review workflows. It
must preserve provenance and avoid storing secrets or restricted material.

## Required Fields

- `source_url`
- `retrieval_time`
- `content_hash`
- provider
- adapter name
- content type
- cache key
- source hygiene status
- `human_verified: false`

## Cache Key

Cache keys must be hashes of normalized request fields. Raw URLs and prompts
must not be used as filenames.

## Allowed Content

- public project pages;
- public GitHub README files;
- public release notes;
- public arXiv HTML pages;
- public documentation pages.

## Blocked Content

- private repositories;
- login-only pages;
- paywalled pages;
- restricted papers;
- private datasets;
- secrets;
- API keys.

## Review Boundary

Cached web content is retrieved context, not verified evidence. Any output that
feeds method cards, collision reports, advisor packs, or paper claims must keep
`requires_human_review`.

## Round 71 Minimal Implementation

The minimal implementation uses an in-memory cache for tests and dry-runs:

- cache key: sha256 of normalized URL;
- content hash: sha256 of HTML or error text;
- metadata: source URL, retrieval time, content hash, provider, source type,
  source hygiene status, and `human_verified: false`;
- status: hit, miss, or stale;
- fixture mode: recorded for local HTML fixtures.

Persistent disk cache remains future work.
