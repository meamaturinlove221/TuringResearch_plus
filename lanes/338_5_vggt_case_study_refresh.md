# Lane 338.5 - VGGT Case Study Refresh

Status: complete
Date: 2026-05-25
Owner skill: `tulingresearch-master-orchestrator`

## Objective

Refresh the public-safe VGGT case study and split-ready draft from local scan outputs, without packaging real data, copying private paths, or claiming unsupported experiment success.

## Inputs

| Input | Status |
| --- | --- |
| Local scan summary | observed |
| Local scan artifact index | observed |
| Local scan missing-items report | observed |
| Local scan evidence ledger | observed |
| Local scan visual inventory | observed |
| Split-ready case directory | missing at start, created |
| Public safety checklist doc | missing |
| Original replication progress report | missing |

## Outputs

- `examples/vggt-human-prior-survey/public_case_study/case_study_draft.md`
- `examples/vggt-human-prior-survey/public_case_study/redaction_report.md`
- `examples/vggt-human-prior-survey/public_case_study/claim_safety_report.md`
- `split_ready/turingresearch-vggt-case/CASE_STUDY.md`
- `split_ready/turingresearch-vggt-case/CLAIM_SAFETY.md`
- `split_ready/turingresearch-vggt-case/PRIVACY.md`
- `docs/vggt-case-study-refresh-v1.5.md`
- `tests/workflow/test_vggt_public_case_study.py`

## Safety Claims

- No raw data included.
- No SMPL-X model files included.
- No private paths included in public case files.
- No huge artifacts included.
- No unsupported claims included.
- No SparseConv3D success claimed.
- Main TulingResearch Plus repo remains flagship.

## Validation

- `python -m pytest tests\workflow\test_vggt_public_case_study.py tests\workflow\test_example_vggt_human_prior.py tests\contract\test_release_gate_contract.py tests\contract\test_skills_integrity.py` passes with 11 tests.
- Privacy/compliance gate passes: no tracked private config, no blocked artifact extensions, no large changed files, no secret-like patterns, and no private local paths in public case files.
- `git diff --check` passes. PowerShell reported only an LF-to-CRLF working-copy warning for an existing text file.
