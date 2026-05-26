# Stress Test Demo

Status: fake/demo only.

This demo describes how the v1.2 stress-test layer reviews a public route before
convergence or release.

## Demo Input

- evidence refs: fake public evidence ledger entries
- artifact refs: fake public artifact index entries
- related work refs: fake paper references
- route hard gates: no promotion, no completion claim
- advisor claims: linked to demo evidence
- plugin permissions: read-only manifest
- live mode: disabled

## Scenarios

- missing evidence
- fake result risk
- overclaim
- artifact missing
- weak related work
- unsafe plugin
- privacy leak
- route contradiction
- advisor pack unsupported claim

## Expected Output

The clean fake route should pass local stress checks and remain human-reviewed.
Passing the demo does not mean a real experiment was run or that a public release
is approved.

## Related Docs

- `docs/yogsoth-stress-test-parity.md`
- `docs/research-route-stress-test.md`
