# Scholar Optional Live Smoke

Round: 373
Status: fake smoke ready / live skipped by default

## Objective

Define a Scholar optional live smoke path that keeps fake mode runnable by
default and keeps live mode skipped unless a maintainer explicitly opts in with
private environment variables.

This round does not call live Scholar services, download papers, require an API
key, verify fake citations, or write live output as observed evidence.

## Default Fake Smoke

Default smoke uses committed fake fixtures only:

```text
TURINGRESEARCH_MODE=fake
TURINGRESEARCH_ENABLE_LIVE_TESTS=0
TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE=0
SEMANTIC_SCHOLAR_API_KEY=
```

Expected result:

- fake smoke pass;
- no API key required;
- no network required;
- no paper download;
- no fake citation verified;
- all outputs require human review.

## Optional Live Smoke

Private live smoke requires all of the following outside the repository:

```text
TURINGRESEARCH_ENABLE_LIVE_TESTS=1
TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE=1
SEMANTIC_SCHOLAR_API_KEY=<private local value>
```

If any flag or key is missing, the live smoke test must skip. Skipping is the
correct default behavior.

## Example Files

See `examples/scholar_demo/live_smoke/`:

- `README.md`
- `fake_smoke_input.json`
- `expected_fake_smoke_report.md`
- `live_skip_report.md`

## Safety Rules

- live skipped by default;
- live requires explicit env;
- no API key in repo;
- no paper download by default;
- no paywall bypass;
- no fake citation verified;
- no automatic Evidence Ledger write;
- no public claim from fake or skipped live output.

## Decision

Scholar optional live smoke is ready for fake/default review. It remains
NO-GO for default live networking.
