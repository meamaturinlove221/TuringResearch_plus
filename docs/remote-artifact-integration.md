# Remote Artifact Integration

Status: v0.4 integration gate.

Remote Artifact Integration normalizes the four v0.4 remote artifact sources
into one review-first report:

- GitHub Artifact Sync
- SSH / SFTP Remote Reader
- NAS / SMB Shared Store
- Cloud Object Artifact Index

The integration layer does not fetch new data by itself. It consumes reports or
indexes produced by the source-specific modules and turns them into
`ArtifactRef` records.

## Unified Output

`UnifiedRemoteArtifactReport` contains:

- `sources`
- `normalized_artifacts`
- `duplicate_candidates`
- `selected_artifacts`
- `omitted_artifacts`
- `unsafe_artifacts`
- `proposed_imports`
- `evidence_tags`
- `requires_human_review`

## Integration Rules

- All sources normalize to the same `ArtifactRef` model.
- Large files remain metadata-only by default.
- Unsafe files are intercepted in a single `unsafe_artifacts` list.
- Proposed imports are not written to Evidence Ledger automatically.
- The report can feed Artifact Auditor, Run Ingestor, Handoff Importer, Advisor
  Pack inputs, and Evidence Ledger proposed updates.

## Evidence Boundary

Remote artifacts are indexed or retrieved, not human verified. The integration
layer does not convert remote artifacts into observed evidence. Any Evidence
Ledger promotion remains an explicit review step.

## Duplicate Candidates

Duplicate candidates are grouped by sha256 when available, otherwise by
filename. This is only a review hint, not an automatic merge.
