# Advisor PDF / PPTX Export



Status: feature capsule skeleton.



## Problem



Advisor Pack is Markdown-only; advisor communication may need portable PDF or PPTX exports that preserve caveats.



## VGGT motivating example



The VGGT Research Knowledge Pack should export a short advisor deck or PDF while keeping V260 hard-blocked, visual readiness blocked, and SparseConv3D unproven.



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



- `AdvisorExportReport`.

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



- command: `turing advisor export`

- tool: `advisor.export_review_pack`

- output: `AdvisorExportReport`



## Related contracts



- `contracts/advisor_export.yaml`

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



Formatted export can look more final than the evidence supports.



## Done criteria



Markdown-to-export plan, manifest, limitation slide/page checks, and no invented evidence.



## Release target



v0.4 Sprint 1 / advisor phase



## Non-goals



- No default networking.

- No permission bypass.

- No automatic large-file download.

- No remote code execution.

- No saved secrets.

- No raw data or SMPL-X model file packaging.

- No remote artifact treated as verified evidence.

- No legacy project naming.
