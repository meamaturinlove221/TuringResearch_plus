# TulingResearch Plus Live Adapter Design

Round 32 defines the v0.2.0 live adapter architecture. This is design and protocol work only. It does not perform real network calls and does not mark live adapters as implemented.

## Goals

- Prepare opt-in live adapters for Semantic Scholar, arXiv, Apify, OpenAI-compatible LLMs, and replaceable PDF converters.
- Preserve fake-mode and dry-run behavior as the default path.
- Keep all external services behind protocols.
- Keep cache, timeout, retry, rate limit, and error handling explicit.
- Keep live tests skipped by default.

## Adapter Families

| Adapter | Purpose | Protocol | Fake equivalent |
| --- | --- | --- | --- |
| SemanticScholarAdapter | Paper lookup and citation graph metadata | `SemanticScholarAdapter` | `FakeSemanticScholarAdapter` |
| ArxivAdapter | arXiv search and metadata fetch | `ArxivAdapter` | `FakeArxivAdapter` |
| ApifyWebAdapter | Optional public web content adapter | `ApifyWebAdapter` | `FakeApifyWebAdapter` |
| OpenAICompatibleLLMAdapter | Optional LLM completion adapter | `OpenAICompatibleLLMAdapter` | `FakeOpenAICompatibleLLMAdapter` |
| PDFConverterAdapter | Replaceable local PDF converter | `PDFConverterAdapter` | `FakePDFConverterAdapter` |

## Shared Policy Models

Every adapter request carries:

- timeout policy
- retry policy
- rate limit policy
- cache policy
- live test marker
- fake adapter equivalent
- dry-run/live-enabled flags
- optional API key environment variable name

Shared model module:

`src/tuling_research_plus/adapters/protocols.py`

Contract:

`contracts/live_adapters.yaml`

## Timeout Policy

Adapters declare:

- connect timeout
- read timeout
- total timeout

Timeouts must produce typed adapter errors and must be retryable only when the retry policy allows it.

## Retry Policy

Retries are explicit:

- maximum attempts
- backoff seconds
- retryable error codes

Retries must not hide final failures. Exhaustion returns `AdapterError` with `retry_exhausted` or the final provider error.

## Rate Limit Policy

Rate limit behavior is explicit:

- optional requests-per-minute value
- provider quota label
- on-limit behavior

Default behavior is to return a typed error, not sleep indefinitely.

## Error Model

All adapter errors use `AdapterError` with:

- code
- message
- retryable flag
- provider
- optional status code
- details

Canonical codes:

- `missing_api_key`
- `timeout`
- `rate_limited`
- `retry_exhausted`
- `provider_error`
- `invalid_response`
- `unsupported`
- `source_hygiene_blocked`

## Cache Integration

Every adapter declares an `AdapterCachePolicy`:

- namespace
- TTL
- cache key fields
- write-through behavior

Adapters must not use raw URLs or raw prompts directly as filenames. Cache implementations should hash keys through the existing cache key utilities.

## Source Hygiene

Adapters that fetch public or upstream material must preserve enough source metadata for Source Hygiene checks. Unknown or unauthorized sources must not become implementation tasks.

## Implementation Status

All live adapters are `protocol_only` in Round 32. Future implementation rounds must add fake adapter parity and mocked contract tests before enabling optional live behavior.
