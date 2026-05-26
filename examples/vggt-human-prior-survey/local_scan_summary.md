# VGGT Local Freshness Scan Summary

Round: Optional 367.5
Date: 2026-05-26
Mode: VGGT desktop local freshness recheck, read-only
Repository: TuringResearch

## Safety Envelope

- observed: the recheck ran on a machine with local VGGT workspaces present.
- observed: only lightweight file metadata and small report summaries were inspected.
- observed: no VGGT code, training, viewer, evaluator, or experiment command was run.
- observed: no local VGGT workspace file was written, deleted, renamed, or copied.
- observed: no raw dataset, restricted body-model payload, large array, point-cloud, archive, checkpoint, or experiment bundle was copied into TuringResearch.
- observed: no network action was required for the local scan itself.
- local-private: the machine-local project-links config remains intentionally untracked and absent from the repository checkout.

## Current Integration Note

This file refreshes the earlier Round 337.5 local scan on top of the current
`feature/v1.6-split-execution-pack` branch. The branch already contains the
Round 338.5 public-safe case draft and the Round 343.5 manual split pack
freshness check. Round 367.5 does not upgrade either package into a public
release, a model-success result, or an advisor-approved result.

## Freshness Signals

| Signal | Status | Evidence scope |
| --- | --- | --- |
| VGGT desktop co-location | local-observed | Redacted local VGGT workspace labels were present during the recheck. |
| Primary VGGT checkout | local-observed | A local checkout with recent report metadata was present; exact path is redacted. |
| Feature-adapter workspace | local-observed | Tool, report, and goal-manifest metadata existed; files were not executed. |
| Alternate VGGT checkouts | local-observed | Additional local checkouts existed and were treated as contextual only. |
| V3000 final status metadata | local-observed | Small JSON metadata reported ready-not-promoted wording; this is not promotion. |
| V2900 bundle sidecar metadata | local-observed | Small JSON metadata reported hash and bundle checks; large payloads were not copied. |
| V2600 viewer metadata | local-observed | Viewer metadata existed; no viewer was opened and no visual pass was claimed. |
| V2000/V2010 training metadata | local-observed | Small manifest metadata existed; no training or evaluation was run. |
| V900/V930/V999/V120/V121 file evidence | local-observed | Tool and goal-manifest files existed; backend and advisor claims remain review-gated. |
| split-ready case package | observed | `split_ready/turingresearch-vggt-case` exists as a public-safe documentation draft. |
| split-manual case package | observed | `split_manual/turingresearch-vggt-case` exists as a manual human-review pack. |

## Mentor Visual Gate

| Gate | Round 367.5 status | Reason |
| --- | --- | --- |
| full-scene RGB point cloud | missing | No point-cloud file was copied or opened in this recheck. |
| human is the main subject | missing | Metadata alone cannot prove human-main visual evidence. |
| partial environment visible | missing | No full-scene board or point-cloud content was inspected. |
| baseline / adapter / controls same-scene comparison | missing | Existing metadata references boards, but the content was not revalidated. |
| teacher/student separation | requires-human-review | Local reports remain metadata-only for this round. |
| advisor-ready conclusion | blocked | The mentor visual gate must fail closed without inspected full-scene evidence. |

## Interpretation

- local-observed: the VGGT desktop still has relevant local metadata for a human reviewer.
- observed: the current main repository already contains split-ready and split-manual case packages.
- requires-human-review: whether private local VGGT evidence should refresh the public case package.
- blocked claim: this recheck does not prove backend completion, advisor approval, promotion, public release readiness, or visual improvement.

## split_manual Update Decision

No automatic content upgrade is required for `split_manual/turingresearch-vggt-case`.
The manual pack remains a human-review pack and should not be used to create or
push an external repository until a reviewer inspects any private VGGT evidence
selected for public release. Round 367.5 adds a freshness recheck record rather
than moving new private evidence into the manual pack.

## Output Policy

The scan outputs are summaries only. Raw datasets, restricted model payloads,
large arrays, point clouds, archives, checkpoints, and VGGT experiment bundles
stay outside this repository.
