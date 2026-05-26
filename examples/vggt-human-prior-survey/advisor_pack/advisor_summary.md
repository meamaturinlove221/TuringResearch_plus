# Advisor Summary



Goal: Summarize VGGT / SMPL-X dogfooding status without overclaiming.



## Current Route



The current route is SMPL-X feature encoding rather than direct SMPL-X replacement. The pack treats VGGT milestone labels according to the evidence ledger status and keeps planned Modal Real SparseConv3D work as a next action rather than an observed result.



## What Changed



- The working direction is now SMPL-X feature encoding, not direct SMPL-X replacement.

- Evidence is summarized from the VGGT evidence ledger, artifact audit, and visual dry-run outputs.

- Missing visual proof is explicitly blocked instead of being presented as advisor-ready.



## Observed Evidence



- V770: local-observed - Diagnostic crop residual milestone is tracked as local dogfooding context.

- V129: observed - SMPL-X anchored completion is recorded as engineering context.

- V900: observed - Feature adapter entrypoint is recorded as observed engineering context.

- V930: observed - HumanRAM-style tri-plane adapter has an observed short-training signal.

- V999: observed - Long-run triplane-only route status is observed as engineering context.



## Limitations



- V770: Local scan confirms project co-location, not result artifact quality.

- V129: Full-body completion and hairline regression remain unresolved.

- V260: No committed artifact confirms adjacent predictions or semantic assets.

- V900: Architecture entrypoint is not enough to prove experiment success.

- V930: Short-training signal is not a completed VGGT result.

- V999: SparseConv3D success is not proven by this route status.

- V999-SparseConv3D: Artifact index reports no scanned artifacts.

- V120: No local evidence ledger JSON is committed.

- V121: No visual inventory is committed.

- No artifacts were scanned in this dry run.

- Artifact audit found no artifact records.

- Visual proof is missing; proxy or absent boards cannot support advisor-ready proof.

- This advisor pack is Markdown-only. It does not generate PPTX or PDF, does not run VGGT, does not read private VGGT paths, and does not fabricate experiment or visual results.



## Blockers



- V260: Required semantic assets are unavailable in the local scan.

- V999-SparseConv3D: No local evidence ledger or backend artifact confirms SparseConv3D success.

- V120: V120 cannot be local-observed without explicit local evidence.

- V121: V121 cannot be local-observed without visual inventory evidence.

- Artifact audit found no scanned artifacts.

- Full body, hairline, and hand close-up visual proof are missing.



## Visual Readiness



- Status: blocked



## Not-Ready Claims



- V260 is hard-blocked and must not be described as a successful route.

- V999 long-run route status is not final target achievement.

- SparseConv3D success is not complete without real evidence.

- Modal Real SparseConv3D is planned / next action, not an observed result.

- V260: Semantic-temporal fusion route is hard-blocked for Sprint 1 evidence use. (hard-blocked).

- V999-SparseConv3D: SparseConv3D backend success is not established by current local evidence. (not-enough-evidence).

- V120: Modal real spconv backend success requires human review. (requires-human-review).

- V121: True region pointcloud visual gate requires human review. (requires-human-review).

- Advisor visual readiness is not ready because required visual proof is missing.



## Next Actions



- V770: Attach artifact-backed diagnostic output before promotion.

- V129: Require artifact-backed visual and metric evidence.

- V260: Keep out of advisor-ready claims until artifacts are supplied.

- V900: Attach run artifacts and metrics when available.

- V930: Collect repeatable run evidence and visual comparisons.

- V999: Separate route status from SparseConv3D backend success.

- V999-SparseConv3D: Require real run artifact, sidecar, and evidence ledger entry.

- V120: Provide local_scan_evidence_ledger.json or artifact-backed report.

- V121: Provide local_scan_visual_inventory.md with provenance.

- Produce local_scan_visual_inventory.md with board provenance.

- Collect full-body, hairline, and hand close-up visual evidence.

- Keep proxy, mask, and delta boards separate from advisor-ready proof.

- Run Modal Real SparseConv3D only as a future planned experiment with artifact-backed evidence.



## Suggested Advisor Message



We have shifted from direct SMPL-X replacement toward SMPL-X feature encoding. The current evidence supports engineering context and local dogfooding status, but it does not yet support a final success claim. V260 is hard-blocked, V999 long-run route status is not final target achievement, SparseConv3D success is not established, and the visual proof gate remains not-ready until full body, hairline, and hand close-up evidence are available.



## Required Human Review



- Missing input requires review: docs\visual-evidence-auditor.md

- Missing input requires review: examples\vggt-human-prior-survey\local_scan_evidence_ledger.json

- Human review is required before any visual readiness claim.



## Missing Inputs



- `docs\visual-evidence-auditor.md`

- `examples\vggt-human-prior-survey\local_scan_evidence_ledger.json`
