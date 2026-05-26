# NAS / SMB Shared Artifact Store



Status: feature capsule skeleton.



## Problem



Local lab workflows may share artifacts through NAS or SMB paths, but v0.3 handoff is local directory based and does not define shared-store safety.



## VGGT motivating example



A VGGT workstation writes review summaries to a shared folder. The main machine should index allowed summaries while rejecting raw data, cache folders, and body model files.



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



- `SharedArtifactStoreIndex`.

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



- command: `turing artifact shared-store-index`

- tool: `artifact.shared_store_index`

- output: `SharedArtifactStoreIndex`



## Related contracts



- `contracts/nas_smb_artifact_store.yaml`

- `contracts/handoff_bundle.yaml`

- `contracts/run_ingest.yaml`



## Related skills



- `turingresearch-cache-and-ledger`

- `turingresearch-master-orchestrator`



## Required tests



- Fake/default workflow test.

- Missing credential or unavailable source test.

- Secret/raw-data/SMPL-X model exclusion test.

- JSON serialization test.

- Markdown export test.

- Evidence-boundary regression test.



## Risks



Path traversal, accidental inclusion of raw datasets, and ambiguous ownership of shared files.



## Done criteria



Local fixture shared-store index, allow/deny rules, summary-only large file handling, and safety warnings.



## Release target



v0.4 Sprint 1



## Non-goals



- No default networking.

- No permission bypass.

- No automatic large-file download.

- No remote code execution.

- No saved secrets.

- No raw data or SMPL-X model file packaging.

- No remote artifact treated as verified evidence.

- No legacy project naming.
