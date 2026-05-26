# Paper Digest / Three-pass Reading



Status: feature capsule skeleton.



## Problem



v0.3 has a three-pass reading plan, but paper digest output is still thin and not organized for repeated manual paper review.



## VGGT motivating example



NeuralBody, HumanRAM, HART, VGGT-HPE, HGGT, and Fus3D need digest records that separate skim, content grasp, deep understanding, borrow/not-copy, and VGGT mapping.



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



- `PaperDigestReport`.

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



- command: `turing paper digest`

- tool: `paper.digest_three_pass`

- output: `PaperDigestReport`



## Related contracts



- `contracts/paper_digest.yaml`

- `contracts/handoff_bundle.yaml`

- `contracts/run_ingest.yaml`



## Related skills



- `turingresearch-paper-writing-pipeline`

- `turingresearch-master-orchestrator`



## Required tests



- Fake/default workflow test.

- Missing credential or unavailable source test.

- Secret/raw-data/SMPL-X model exclusion test.

- JSON serialization test.

- Markdown export test.

- Evidence-boundary regression test.



## Risks



Digest may be mistaken for complete paper reading without evidence refs.



## Done criteria



Fixture digest with Pass 1/2/3 sections, method-card linkage, collision notes, and requires-human-review flag.



## Release target



v0.4 Sprint 1 / paper phase



## Non-goals



- No default networking.

- No permission bypass.

- No automatic large-file download.

- No remote code execution.

- No saved secrets.

- No raw data or SMPL-X model file packaging.

- No remote artifact treated as verified evidence.

- No legacy project naming.
