# Quality Metrics

Status: implemented minimal.

The quality metrics layer provides lightweight local checks for release and
regression readiness. It does not publish, tag, or run live services.

## Metrics

- Docs completeness
- Test coverage proxy
- Contract consistency
- Example readiness
- Safety readiness
- Fake/live boundary
- Prior project name absence
- Privacy gate pass
- Release readiness

## Output

`QualityReport` records:

- report id
- metrics
- status
- warnings
- release readiness
- human review requirement

## Boundary

- Metrics are local proxy checks.
- Passing metrics do not mean public release is approved.
- Human review is still required.
