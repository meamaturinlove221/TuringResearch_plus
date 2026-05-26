# Scholar Live Optional Guide

Status: optional live polish.

Round: 345.

Scholar live mode is optional, private, and disabled by default. Fake Scholar
tests and demos must continue to run without any API key, network access, paper
download, MinerU, OCR, or paywall bypass.

## Default Fake Mode

Default mode is fake:

```text
TURINGRESEARCH_MODE=fake
TURINGRESEARCH_ENABLE_LIVE_TESTS=0
TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE=0
SEMANTIC_SCHOLAR_API_KEY=
```

Fake mode requires no key and should always pass in the normal test suite.

## Optional Live Mode

Private live mode requires all of the following outside the repository:

```text
TURINGRESEARCH_ENABLE_LIVE_TESTS=1
TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE=1
SEMANTIC_SCHOLAR_API_KEY=<private local value>
```

Do not commit real values. Do not paste real values into docs, examples, test
fixtures, logs, or reports.

## Test Policy

- fake Scholar tests run by default;
- live Scholar tests are skipped by default;
- live Scholar tests require explicit env opt-in;
- live Scholar output remains review context;
- live Scholar output is not observed evidence;
- fake citations are never verified citations.

## Boundaries

- no paper download by default;
- no paywall bypass;
- no MinerU or heavy OCR default;
- no camera-ready paper conclusion;
- no final paper claim;
- no automatic Evidence Ledger write.

## Example

See `examples/scholar_demo/live_optional/README.md` for a local private
configuration shape with blank placeholders only.
