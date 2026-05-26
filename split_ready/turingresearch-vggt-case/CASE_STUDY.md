# VGGT Human Prior Dogfooding Case Study

Status: public-safe draft / requires human review
Round: Optional 338.5 integrated on newer cloud baseline

This split-ready draft describes how TuringResearch organizes a VGGT human-prior research workflow. It is not a VGGT experiment source repository, not a data package, and does not claim experiment success.

The main TuringResearch repository remains flagship. This split case is a small, reviewable artifact for explaining the VGGT dogfooding workflow and claim-safety boundaries.

## Problem Background

The safest public framing is the shift from direct SMPL-X replacement toward SMPL-X feature encoding for VGGT. This case study explains the workflow and evidence controls around that shift.

## Evidence Summary

| Evidence area | Status | Public-safe summary |
| --- | --- | --- |
| Case-study workflow | observed | TuringResearch generated public-safe case-study documentation. |
| Local scan summaries | local-observed | Local scan metadata informs the draft but does not become public observed evidence without review. |
| VGGT report metadata | local-observed | Lightweight report and manifest evidence existed for selected work streams. |
| Visual inventory metadata | local-observed | Visual evidence classes were inventoried without copying images or pointclouds. |
| SparseConv3D success | requires-human-review | The current evidence does not support a success claim. |
| Advisor approval | requires-human-review | No advisor approval is claimed. |
| Public release readiness | requires-human-review | This directory is a draft that needs human approval. |

## What Remains Human Work

- Run real VGGT-side or Modal-side experiments outside this case-study repo.
- Review papers manually before final related-work wording.
- Interpret failures and approve final claims.
- Review privacy, license, and publication boundaries before release.

## Exclusions

- No raw data.
- No SMPL-X model files.
- No private paths.
- No huge artifacts.
- No VGGT experiment archives.
- No unsupported success claims.

## Release Posture

This case is ready for human review, not public release. A maintainer must review the claim safety report and privacy report before any package is published or linked externally.
