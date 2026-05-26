# TuringResearch Plus Live Adapter Design

Status: beta contract draft with fake adapters.

Round 55 defined the live adapter contract surface for v0.2 beta. Round 56 adds
the first optional live client for Semantic Scholar while keeping fake mode as
the default.

## Goals

- Keep every external service behind an adapter Protocol.
- Keep fake mode as the default test and workflow path.
- Make timeout, retry, rate limit, cache, source metadata, and error behavior
  explicit.
- Require a fake adapter equivalent before any live adapter is accepted.
- Prevent live search results from becoming human-verified evidence by default.

## Adapter Families

| Adapter | Purpose | Fake equivalent | Default enabled |
| --- | --- | --- | --- |
| `SemanticScholarAdapter` | Optional live paper lookup and citation metadata. | `FakeSemanticScholarAdapter` | false |
| `ArxivAdapter` | Optional arXiv search and metadata. | `FakeArxivAdapter` | false |
| `WebSearchAdapter` | Optional public web search. | `FakeWebSearchAdapter` | false |
| `WebFetchAdapter` | Optional public web fetch with source hygiene metadata. | `FakeWebFetchAdapter` | false |
| `OpenAICompatibleLLMAdapter` | Optional OpenAI-compatible LLM completion. | `FakeOpenAICompatibleLLMAdapter` | false |
| `PDFConverterAdapter` | Replaceable local PDF converter backend. | `FakePDFConverterAdapter` | false |

`ApifyWebAdapter` and `FakeApifyWebAdapter` remain compatibility aliases for
older planning docs. New code should use `WebFetchAdapter` and
`FakeWebFetchAdapter`.

## Module Layout

- `src/turing_research_plus/adapters/models.py`
- `src/turing_research_plus/adapters/errors.py`
- `src/turing_research_plus/adapters/protocols.py`
- `src/turing_research_plus/adapters/fake.py`
- `src/turing_research_plus/adapters/semantic_scholar.py`
- `src/turing_research_plus/adapters/cache.py`
- `src/turing_research_plus/adapters/rate_limit.py`
- `src/turing_research_plus/adapters/live_test_markers.py`
- `contracts/live_adapters.yaml`

## Shared Policies

Every adapter request carries:

- timeout policy;
- retry policy;
- rate limit policy;
- cache policy;
- live test marker;
- fake adapter equivalent;
- required env vars;
- dry-run/live-enabled flags;
- `default_enabled: false`.

## Source Metadata

Every live or fake result must include source metadata when it returns source
records:

- provider;
- source id or URL when available;
- retrieval time;
- `human_verified: false` by default;
- optional license label.

Live retrieval does not imply human verification.

## Cache Policy

Adapters declare cache namespaces and cache-key fields. Implementations must
hash cache keys and must not use raw URLs or raw prompts as filenames.

## Error Policy

Errors use `AdapterError` with stable codes:

- `missing_api_key`
- `timeout`
- `rate_limited`
- `retry_exhausted`
- `provider_error`
- `invalid_response`
- `unsupported`
- `source_hygiene_blocked`
- `live_disabled`

Missing API keys must not fail default tests.

## Implementation Status

Round 56 status: Semantic Scholar has an optional minimal live adapter. Other
adapter families remain fake-adapter ready and live-not-implemented.
