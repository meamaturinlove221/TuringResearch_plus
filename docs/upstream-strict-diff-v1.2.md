# Upstream Strict Diff v1.2

Status: baseline-created-with-unresolved-targets.

Round: 234.

This report summarizes the strict upstream baseline diff attempt for the v1.2
reference-parity line. The round is an upstream scan round, so live public
metadata access was allowed. The scan did not produce a usable upstream diff
because no prior machine-readable baseline existed and all configured public
metadata requests were unresolved in this environment.

## Strict Diff Rules

- If a prior machine baseline exists, added, modified, and deleted files may be
  reported by comparing the current scan against that baseline.
- If no prior machine baseline exists, the only valid result is
  `baseline-created`.
- A current snapshot is not a change by itself.
- Unresolved repositories are reported as unresolved, not deleted.
- Manual snapshots can guide planning, but they are not machine diff baselines.

## Scope

Tracked Neocortica split repositories:

- `Pthahnix/Neocortica-Session`
- `Pthahnix/Neocortica-Scholar`
- `Pthahnix/Neocortica-Web`

Tracked yogsoth-ai repositories came from `upstream_watch/targets.yaml`.
The legacy umbrella alias is not part of the strict target set.

## Result

- Baseline file: `upstream_watch/baselines/v1.2_strict_baseline.json`
- Baseline ID: `v1.2-strict-baseline-2026-05-22`
- Scan mode: `live-public-metadata-attempted`
- Diff mode: `initial-baseline-no-prior-machine-baseline`
- Configured repositories: 21
- Resolved repositories: 0
- Unresolved repositories: 21
- Unresolved reason: GitHub public metadata returned HTTP 403 rate limit
  responses for the configured targets.

## Valid Claims

- A first machine-readable v1.2 upstream baseline was created.
- The strict diff did not have a prior machine baseline to compare against.
- No added, modified, or deleted upstream file claim is made in this round.
- No current upstream snapshot is treated as a new change.

## Invalid Claims

- Do not claim that a target repository added files in this round.
- Do not claim that a target repository modified files in this round.
- Do not claim that a target repository deleted files in this round.
- Do not treat unresolved repositories as removed or inactive.
- Do not use manual snapshot notes as machine diff evidence.

## Follow-up

The next resolved upstream scan may compare against
`upstream_watch/baselines/v1.2_strict_baseline.json`. Only that future
comparison can create strict added, modified, or deleted records.
