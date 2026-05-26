# VGGT Research Knowledge Pack

Status: v0.3 Sprint 2 review artifact.

The VGGT Research Knowledge Pack consolidates the current TuringResearch Plus
materials for the VGGT / SMPL-X Human Prior line into a review-oriented package.
It is intended for future VGGT-side experiments, advisor discussion, and paper
planning. It is not a final paper, not an experiment result, and not a claim of
SparseConv3D success.

## Location

`examples/vggt-human-prior-survey/research_knowledge_pack/`

## Included Sections

- North star: `SMPL-X direct replacement -> SMPL-X feature encoding for VGGT`.
- Current state for V770 / V129 / V260 / V900 / V930 / V999 and later planned
  routes.
- Evidence status summary.
- Artifact and visual readiness summary.
- Failure taxonomy and mitigation.
- Modal SparseConv3D planned route, hard gates, and artifact requirements.
- Related-work positioning for NeuralBody, HumanRAM, HART, VGGT-HPE, HGGT, and
  Fus3D.
- Method taxonomy and vault graph review notes.
- Advisor brief and next actions.
- Manifest with source files, missing inputs, and claim boundaries.

## Safety Boundary

The pack is generated from committed local review artifacts. It does not:

- run VGGT;
- run Modal;
- read private VGGT paths;
- use network access;
- download papers;
- generate final paper prose;
- fabricate experiment results;
- mark planned work as observed;
- claim SparseConv3D success.

## Current Interpretation

The pack supports a conservative statement: TuringResearch Plus has organized
the evidence, risks, routes, related-work positioning, and review graph needed
for a future artifact-backed VGGT experiment. It does not support a final
success claim.

## Expected Follow-up

Future VGGT-side work should provide a real sparse backend probe log,
predictions or thin prediction summary, board inventory, visual close-ups,
sha256 manifest, cleanup report, and failure analysis. Those outputs can then
flow through run ingest, artifact audit, evidence proposed updates, and advisor
pack regeneration.
