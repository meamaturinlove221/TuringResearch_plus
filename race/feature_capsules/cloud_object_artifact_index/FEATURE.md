# Cloud Object Artifact Index



Status: feature capsule skeleton.



## Problem



Cloud object stores may later hold large artifacts, but direct cloud download raises high credential and governance risk.



## VGGT motivating example



A remote run publishes object metadata for review outputs. TuringResearch should index keys, sizes, hashes, and omitted reasons without downloading payloads by default.



## User story



As a TuringResearch operator, I want this feature to produce reviewable,

audit-friendly artifacts while preserving evidence boundaries, so that VGGT and

paper workflows can advance without leaking secrets or overclaiming results.



## Inputs



- Handoff bundle manifests.

- Run ingest reports.

- Artifact audit reports.

- Evidence Ledger status labels.

- VGGT Research Knowledge Pack material.

- Manual review notes when needed.



## Outputs



- `CloudObjectArtifactIndex`.

- JSON-serializable report.

- Markdown review summary.

- Proposed evidence updates only when relevant.



## Data model



- status: planned / retrieved / indexed / blocked / requires-human-review.

- source refs and sha256 metadata.

- safety warnings and omitted items.

- limitations and blockers.

- manual review flag.



## Proposed commands / tools



- command: `turing artifact cloud-index`

- tool: `artifact.cloud_index_optional`

- output: `CloudObjectArtifactIndex`



## Related contracts



- `contracts/cloud_object_artifact_index.yaml`

- `contracts/handoff_bundle.yaml`

- `contracts/run_ingest.yaml`



## Related skills



- `turingresearch-architecture-contracts`

- `turingresearch-master-orchestrator`



## Required tests



- Fake/default workflow test.

- Missing credential or unavailable source test.

- Secret/raw-data/SMPL-X model exclusion test.

- JSON serialization test.

- Markdown export test.

- Evidence-boundary regression test.



## Risks



Credential leakage and accidental download of restricted or oversized data.



## Done criteria



Fake bucket listing, index-only output, no object download by default, and credential absence skip.



## Release target



v0.4 Sprint 1 planning / optional track



## Non-goals



- No default networking.

- No permission bypass.

- No automatic large-file download.

- No remote code execution.

- No saved secrets.

- No raw data or SMPL-X model file packaging.

- No remote artifact treated as verified evidence.

- No legacy project naming.
