# Advisor Pack Builder

TuringResearch Plus uses the Advisor Pack Builder to turn VGGT / SMPL-X
dogfooding evidence into a concise Markdown package that can be read by an
advisor without implying a finished experiment.

Round 40 implements the minimal Markdown-only builder. It does not generate
PPTX, does not generate PDF, does not run VGGT code, does not read `D:/vggt`,
and does not fabricate experiment or visual results.

## Inputs

- VGGT dogfooding docs.
- VGGT / SMPL-X Evidence Ledger.
- Artifact Auditor output.
- Visual Evidence dry-run output.
- Sprint 1 plan and risk register.
- Local scan summary and artifact index.

Missing inputs are non-fatal. They are recorded in the pack as missing inputs
and as required human review items.

## Output Files

The VGGT dogfooding workflow writes:

- `examples/vggt-human-prior-survey/advisor_pack/advisor_summary.md`
- `examples/vggt-human-prior-survey/advisor_pack/current_status.md`
- `examples/vggt-human-prior-survey/advisor_pack/evidence_summary.md`
- `examples/vggt-human-prior-survey/advisor_pack/visual_readiness.md`
- `examples/vggt-human-prior-survey/advisor_pack/failure_analysis.md`
- `examples/vggt-human-prior-survey/advisor_pack/next_actions.md`

## Evidence Boundaries

- The current route is SMPL-X feature encoding, not direct SMPL-X replacement.
- V770, V129, V260, V900, V930, and V999 are reported only according to the
  evidence ledger status.
- V260 is hard-blocked and must not be described as a successful route.
- V999 long-run route status is not final target achievement.
- SparseConv3D success is not complete without evidence ledger proof.
- Modal Real SparseConv3D is planned / next action unless real evidence exists.
- Missing full body, hairline, and hand close-up visual proof blocks visual
  readiness.

## Tool Boundary

`advisor.pack_build` is a capsule-local proposed tool in Round 40. It is not a
frozen public MCP namespace until a later contracts-first round updates the root
contracts and `docs/mcp-tools.md`.

## Tests

- `tests/unit/test_advisor_pack_models.py`
- `tests/unit/test_advisor_pack_builder.py`
- `tests/unit/test_advisor_pack_sections.py`
- `tests/workflow/test_vggt_advisor_pack_from_sprint1_artifacts.py`
