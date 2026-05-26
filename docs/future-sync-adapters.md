# Future Sync Adapters

Status: future planning only.

Round: 102.

This document is a planning note for future sync adapters. It does not implement
sync behavior, define live credentials, run network access, or change the
current default behavior.

## Current Boundary

TuringResearch Plus already has safety-gated remote artifact surfaces:

- GitHub artifact sync metadata and selected import planning.
- SSH / SFTP read-only remote artifact reader.
- NAS / SMB local mount scanner.
- Provider-neutral cloud object artifact index.
- Unified remote artifact report.

These are import and index surfaces. They do not make remote artifacts verified
evidence, do not execute remote commands, and do not automatically overwrite the
Evidence Ledger.

## Future Adapter Categories

| Adapter category | Horizon | Purpose | Risk |
| --- | --- | --- | --- |
| GitHub artifact sync | near-term refinement | Release/workflow artifact ingestion. | token and large file exposure |
| SSH / SFTP reader | near-term refinement | Read structured reports from controlled hosts. | private path and credential risk |
| NAS / SMB store | near-term refinement | Read already-mounted shared folders. | raw data exposure |
| Cloud object index | mid-term | Index object metadata from S3/R2/OSS/GCS-style stores. | credential and bucket policy risk |
| Remote execution ingest | mid-term | Read structured outputs from external runners. | output treated as verified |
| Bidirectional sync | long-term | Coordinate selected manifests across machines. | overwrite and privacy risk |

## Safety Principles

- Sync adapters must be opt-in.
- Credentials must never be stored in repo.
- Default tests must use fake clients.
- Large files are metadata-only by default.
- Raw data and private model files are omitted by default.
- Remote output is retrieved/imported, not verified.
- Evidence Ledger updates are proposed, not automatic.

## Human Review Required

- Selecting a remote root or bucket.
- Approving download of non-small files.
- Promoting remote artifacts to observed evidence.
- Publishing any remote artifact-derived result.
- Allowing a plugin to access remote artifact APIs.

## Cannot Be Automated Safely

- Credential approval.
- Privacy and license approval.
- Evidence promotion.
- Cross-machine deletion or overwrite decisions.
- Treating remote outputs as experiment success.

## v0.6 Recommendation

Do not expand sync implementation until public release hardening, privacy policy,
workspace boundaries, and capability manifests are stable. v0.6 can refine
manifests and tests, but should not introduce broad automatic synchronization.
