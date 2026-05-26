# Lane 16: VGGT Feature Capsules

## Scope

Round 37 creates TuringResearch Plus Feature Capsule skeletons for the v0.2.0
Sprint 1 VGGT dogfooding Top 5. This lane is planning-only until a later
implementation round starts.

## Inputs

- `docs/v0.2.0-sprint-1-final-scope.md`
- `docs/v0.2.0-sprint-1-implementation-order.md`
- `docs/v0.2.0-sprint-1-test-plan.md`
- `docs/dogfooding-vggt-smplx.md`
- `examples/vggt-human-prior-survey/local_scan_summary.md`
- `examples/vggt-human-prior-survey/local_scan_artifact_index.md`

Missing inputs:

- `examples/vggt-human-prior-survey/local_scan_evidence_ledger.json`
- `examples/vggt-human-prior-survey/local_scan_visual_inventory.md`

## Created Capsules

| Capsule | Status | Release target |
| --- | --- | --- |
| `vggt_smplx_evidence_ledger` | skeleton | v0.2.0 Sprint 1 |
| `artifact_auditor` | skeleton | v0.2.0 Sprint 1 |
| `visual_evidence_auditor` | skeleton | v0.2.0 Sprint 1 |
| `advisor_pack_builder` | skeleton | v0.2.0 Sprint 1 |
| `pdf_phase_b_figure_table_extraction` | skeleton | v0.2.0 Sprint 1 |

## Files Created

Each capsule contains:

- `FEATURE.md`
- `contract.yaml`
- `SKILL.md`
- `sop.mmd`
- `test_plan.md`

Round 37 also creates:

- `docs/v0.2.0-feature-capsules.md`
- `docs/v0.2.0-sprint-1-feature-capsules.md`
- `docs/v0.2.0-p0-implementation-order.md`

## Constraints

- No complex implementation logic.
- No network access.
- No VGGT execution.
- No private local path reads by default.
- No `local_project_links.yaml` commit.
- No Future Sync Adapters in Sprint 1.
- No public API change without root contract updates.

## Next Step

Start with `vggt_smplx_evidence_ledger` contract promotion, model design, and
tests. Keep `vggt.evidence_ledger_build`, `artifact.audit`,
`visual.audit_evidence`, and `advisor.pack_build` as capsule-local proposals
until a contracts-first round accepts or renames them.

