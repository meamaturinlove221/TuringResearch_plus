# Scholar Live Optional Example

Status: example only / no key in repo.

This folder documents the private opt-in shape for Scholar live mode. It does
not contain credentials and does not require live mode for normal tests.

## Fake Default

Use fake mode unless you are deliberately testing private live access:

```text
TURINGRESEARCH_MODE=fake
TURINGRESEARCH_ENABLE_LIVE_TESTS=0
TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE=0
SEMANTIC_SCHOLAR_API_KEY=
```

## Private Live Shape

If a maintainer wants to test live Semantic Scholar locally, configure this
outside the repository:

```text
TURINGRESEARCH_ENABLE_LIVE_TESTS=1
TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE=1
SEMANTIC_SCHOLAR_API_KEY=<private local value>
```

## Safety

- no key in repo;
- no paper download by default;
- no paywall bypass;
- no fake citation verified;
- live output remains review context;
- human review required before any claim.
