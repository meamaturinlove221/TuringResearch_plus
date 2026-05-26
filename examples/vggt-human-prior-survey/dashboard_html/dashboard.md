# VGGT Research Dashboard



- Project: VGGT / SMPL-X Human Prior

- Status: static review dashboard

- Requires human review: true

- No Modal execution

- No VGGT execution

- Not an experiment result



## Project Overview



# VGGT Research Knowledge Pack



Status: review pack / requires human review.



This pack organizes the current TuringResearch Plus materials for the VGGT /

SMPL-X Human Prior line. It is designed for planning, advisor discussion, and

future experiment handoff. It does not run VGGT, does not run Modal, does not

read private VGGT paths, does not use network access, and does not claim final

research results.



## Contents



- `north_star.md` - the route pivot from SMPL-X direct replacement to feature encoding.

- `current_state.md` - V770 / V129 / V260 / V900 / V930 / V999 status summary.

- `evidence_summary.md` - evidence labels and non-promotion boundaries.

- `artifact_summary.md` - available, missing, omitted, and unsafe artifacts.

- `visual_readiness.md` - visual proof status and missing board views.

- `failure_taxonomy.md` - blockers, recurring failure modes, and mitigation.

- `experiment_routes.md` - Modal SparseConv3D route, hard gates, artifacts, and fallbacks.

- `related_work_positioning.md` - conservative related-work positioning.

- `method_taxonomy.md` - method clusters and concept taxonomy.

- `vault_graph.md` - graph and wikilink review notes.

- `advisor_brief.md` - concise advisor-ready update with caveats.

- `next_actions.md` - next actions for experiments, reading, advisor communication, and TuringResearch.

- `manifest.yaml` - source files and status labels for this pack.



## Claim Boundary



The current evidence supports route planning and review-oriented engineering

context. It does not prove SparseConv3D success, does not provide advisor-ready

visual proof, and does not replace manual paper review.



SparseConv3D success is not claimed by this pack.



## Evidence Status



# Evidence Summary



## Status Buckets



### observed



- V129: SMPL-X anchored completion is recorded as engineering context.

- V900: Feature adapter entrypoint is recorded as observed engineering context.

- V930: HumanRAM-style tri-plane adapter has an observed short-training signal.

- V999: Long-run tri-plane-only route status is observed as engineering context.



### local-observed



- V770: Diagnostic crop residual milestone is tracked as local dogfooding context.



### planned



- Modal Real SparseConv3D route.

- SMPL-X voxel feature encoding route.

- Future artifact-backed run ingest from VGGT-side outputs.



### hard-blocked



- V260: Required semantic assets are unavailable in the current scan.



### not-enough-evidence



- V999-SparseConv3D: no local evidence ledger, backend artifact, or run output

  confirms SparseConv3D success.

- `modal_sparseconv_v0`: current fixture ingest proposes `not-enough-evidence`.



### requires-human-review



- V120: no committed local evidence ledger JSON.

- V121: no committed local visual inventory.

- Related work claims: fake/manual method cards and citation graph are not enough

  for final related-work claims.

- Visual readiness: full body, hairline, and hand close-up evidence are missing.



## Evidence Boundary



Missing evidence is not negative proof and is not success proof. Any final claim

must be backed by a source artifact, evidence reference, and human review when

the evidence is ambiguous.



## Artifact Completeness



# Artifact Summary



## Available Artifacts



The committed TuringResearch example tree contains review artifacts, not raw

VGGT experiment outputs:



- Advisor pack Markdown files.

- Modal SparseConv3D route pack.

- Run ingest fixture and dry-run reports.

- Paper method card fixtures.

- Citation graph, collision risk, related work, and vault graph fixtures.

- Web fetch fixture HTML pages.

- Pod workflow and handoff bundle fixtures.



## Missing Artifacts



The current local scan reports no scanned artifacts. Required missing items

include:



- `local_scan_evidence_ledger.json`

- `local_scan_visual_inventory.md`

- `predictions.npz` or thin prediction summary

- board inventory

- full-body visual board

- hairline close-up visual board

- hand close-up visual board

- real sparse backend probe log

- sha256 manifest for real run outputs

- cleanup report



## Omitted Large Files



Large arrays and raw result payloads are not part of this review pack. Future

large files should be summarized with keys, shapes, dtypes, file size, and

sha256 hashes rather than copied into the repo.



## Unsafe or Unavailable Files



The pack must not include private configs, raw datasets, API keys, secrets,

SMPL-X body model files, cache folders, or huge NPZ payloads. Missing files

should stay missing in the report until a future local VGGT dry-run supplies

auditable summaries.



## Visual Readiness



# Visual Readiness



Status: blocked / not advisor-ready.



## Current Visual Support



Current committed materials contain a visual evidence dry-run report, but no

visual inventory and no board artifacts. The dry-run confirms that no visual

item can be promoted to `local-observed`.



## Missing Board Views



- Full-body reconstruction evidence.

- Hairline close-up evidence.

- Hand close-up evidence.

- Board inventory with provenance.

- Visual inventory linking board files to evidence refs.



## Weak Visual Evidence



Root candidate paths, proxy boards, masks, deltas, heatmaps, and absent board

files are not accepted as advisor-ready proof. If future scans provide only

proxy views, they must remain separate from true visual evidence.



## Advisor Readiness



Advisor visual readiness is blocked until full body, hairline, and hand close-up

visual evidence exists with provenance and evidence ledger links.



## Run Dashboard



# Run Dashboard: modal-sparseconv-fixture-001



[ROUTE_EXHAUSTED] [NOT_ENOUGH_EVIDENCE] [REQUIRES_HUMAN_REVIEW]



- Route id: `modal_sparseconv_v0`

- Run status: `ROUTE_EXHAUSTED_WITH_FAILURE_ANALYSIS`

- Backend status: `real_backend_missing`

- Candidate count: `1`

- Best candidate: `fallback-proxy`

- Visual readiness: `blocked: visual proof insufficient`

- Advisor readiness: `not-ready: backend evidence missing`

- Next action: collect real sparse backend log before making success claims



## Hard Gates



- [x] `not_report_only` - passed in fixture metadata

- [ ] `not_fallback_only` - failed in fixture metadata

- [ ] `real_backend_required` - failed in fixture metadata

- [ ] `candidate_predictions_required` - failed in fixture metadata

- [ ] `visual_board_required` - failed in fixture metadata

- [ ] `cleanup_required` - failed in fixture metadata

- [ ] `real_sparse_backend_required` - real sparse backend log is required

- [x] `final_status.json_required` - required artifact present

- [x] `ranked_candidates.csv_required` - required artifact present

- [ ] `predictions.npz_required` - required artifact missing

- [ ] `board_inventory.md_required` - required artifact missing

- [x] `advisor_summary.md_required` - required artifact present

- [x] `failure_report.md_required` - required artifact present

- [ ] `sha256_manifest.txt_required` - required artifact missing

- [ ] `cleanup_report.md_required` - required artifact missing



## Artifact Completeness



- Present: `4`

- Missing: `4`



- missing `predictions.npz`

- missing `board_inventory.md`

- missing `sha256_manifest.txt`

- missing `cleanup_report.md`



## Failure Categories



- `REAL_BACKEND_UNAVAILABLE`

- `SPARSE_BACKEND_UNAVAILABLE`

- `MISSING_ASSETS`

- `VISUAL_PROOF_INSUFFICIENT`

- `PACKAGE_INCOMPLETE`



## Boundary



- Dashboard did not run Modal.

- Dashboard did not run VGGT.

- Dashboard displays already ingested evidence only.

- Dashboard is not an experiment result.



## Related Work



# Related Work Positioning



Status: conservative positioning / requires real paper review.



## NeuralBody



NeuralBody can be used as a comparison lens for SMPL structured latent code and

sparse voxel / SparseConvNet-style inspiration. Its target is not VGGT point

completion, so it should not be treated as direct equivalence.



## HumanRAM



HumanRAM can be used as a comparison lens for SMPL-X canonical points, tri-plane

neural texture, and rasterized pose features. Its output target differs from the

VGGT / SMPL-X feature encoding line.



## HART



HART may be closer to human reconstruction and requires focused manual paper

review before any collision or differentiation claim.



## VGGT-HPE



If VGGT-HPE is primarily head pose, collision risk may be lower, but the task,

inputs, outputs, and claimed contribution still require real paper review.



## HGGT / Fus3D



HGGT and Fus3D remain `requires-real-paper-review`. They must not be dismissed

or used as final positioning evidence from fixture notes alone.



## Safe Claims



- The current VGGT direction should be described as SMPL-X feature encoding.

- NeuralBody and HumanRAM are useful comparison lenses, not proof of novelty.

- Some related work requires focused manual review before strong positioning.



## Unsafe Claims



- Definitive no-collision with existing papers.

- Complete related-work review.

- SparseConv3D integration success.

- Ignoring HumanRAM, NeuralBody, HART, VGGT-HPE, HGGT, or Fus3D without review.



## Failure Taxonomy



# Failure Taxonomy



## Current Blockers



- V260: `MISSING_ASSETS` / hard-blocked due to missing adjacent predictions or

  semantic assets.

- V999-SparseConv3D: `NOT_ENOUGH_EVIDENCE` because no real backend artifact or

  evidence ledger entry confirms success.

- Modal SparseConv3D fixture: `REAL_BACKEND_UNAVAILABLE`,

  `SPARSE_BACKEND_UNAVAILABLE`, `MISSING_ASSETS`,

  `VISUAL_PROOF_INSUFFICIENT`, and `PACKAGE_INCOMPLETE`.

- Visual readiness: missing board inventory, full body, hairline, and hand

  close-up evidence.



## Recurring Failure Modes



- `REPORT_ONLY`: narrative output without artifacts.

- `FALLBACK_ONLY`: fallback path used instead of real sparse route.

- `IDENTITY_COPY`: unchanged baseline output presented as progress.

- `MISSING_ASSETS`: required predictions, boards, NPZ diff, or manifest absent.

- `VISUAL_PROOF_INSUFFICIENT`: visual proof does not cover full body, hairline,

  and hand/object behavior.

- `NOT_ENOUGH_EVIDENCE`: route status exists but promotion evidence is absent.



## Next Mitigation



1. Require real sparse backend probe logs before any SparseConv3D promotion.

2. Require predictions or a thin prediction summary.

3. Require board inventory and visual close-up evidence.

4. Require sha256 manifest and cleanup report.

5. Generate failure analysis even when the route fails or is blocked.



## Advisor Next Actions



# Next Actions



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



## Limitations



- Static dashboard only; no login, server, or cloud deployment.

- UI displays existing review artifacts only.

- UI is not an experiment result.

- SparseConv3D success is not claimed without evidence.
