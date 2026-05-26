# Physical Split Safety Gate

Status: required gate.

Round: 337.

Every physical split candidate must pass a safety gate before a human creates
or pushes an external repository.

## Required Gate Checks

| Check | Requirement |
| --- | --- |
| public-safe content | pass |
| README flagship backlink | present above the fold |
| no real nonexistent URL | pass |
| no secrets | pass |
| no raw data | pass |
| no private paths | pass |
| no restricted model payloads | pass |
| no huge artifacts | pass |
| no unsupported claims | pass |
| no fake/demo-as-observed wording | pass |
| no install-path replacement | pass |
| human approval recorded | required before external action |

## Candidate-Specific Notes

- `turingresearch-vggt-case` must preserve case-study and claim-safety
  boundaries.
- `turingresearch-examples` must remain fake/demo-only and not an install
  source.
- `turingresearch-plugins` remains deferred until real ecosystem demand.

## Gate Result Rules

- Any private data or secret finding blocks the split.
- Any restricted payload finding blocks the split.
- Any unsupported success claim blocks the split.
- Any missing flagship backlink blocks the split.
- Any automatic repo creation or external push blocks the split.

## Output

The gate should produce a report for human review. It should not create,
delete, push, or upload anything.
