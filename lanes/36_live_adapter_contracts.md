# Lane 36: Live Adapter Contracts

Round 55 defines beta live adapter contracts, protocols, fake adapters, and
test policy.

## Scope

- Live adapter contract update.
- Shared models and typed errors.
- Protocol declarations.
- Deterministic fake adapters.
- API key policy.
- Live test policy refresh.

## Adapter Protocols

- `SemanticScholarAdapter`
- `ArxivAdapter`
- `WebSearchAdapter`
- `WebFetchAdapter`
- `OpenAICompatibleLLMAdapter`
- `PDFConverterAdapter`

## Boundaries

- No real network calls.
- No real API keys.
- No `D:/vggt` reads.
- No concrete Semantic Scholar live client.
- Existing fake workflows remain default.
- No old project naming reintroduced.

## Validation

- Adapter focused tests: 22 passed.
- Package import / public import / name integrity tests: 18 passed.
- Contract tests: 81 passed.
- Full pytest suite: 446 passed.
- `mypy src`: passed.
- Focused ruff check: passed.
- Focused Round 55 old-name scan: passed.

## Next Step

Implement the optional live Semantic Scholar adapter behind this contract,
keeping fake mode as the default and live tests opt-in only.
