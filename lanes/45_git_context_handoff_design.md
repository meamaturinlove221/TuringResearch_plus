# Lane 45: Git-based Context Handoff Design

## Scope

Round 64 designs v0.3 Sprint 1 Git-based Context Handoff / Pod Workflow for
TuringResearch Plus. It does not implement runtime code, run Git commands, run
pods, control Modal/RunPod, or copy upstream scripts.

## Created Design Files

- `docs/git-based-context-handoff.md`
- `docs/pod-workflow-design.md`
- `docs/context-memory-policy.md`
- `docs/structured-output-return-policy.md`
- `docs/v0.3.0-sprint-1-final-scope.md`
- `contracts/git_context_handoff.yaml`
- `contracts/pod_workflow.yaml`
- `race/feature_capsules/git_based_context_handoff/`
- `race/feature_capsules/pod_workflow_pack/`

## Design Models

- `ContextPackage`
- `MemoryPolicy`
- `PodWorkflowSpec`
- `StructuredOutputReturn`
- `HandoffSafetyPolicy`
- `GitTransportPolicy`

## Required Context Package Files

- `PROJECT_CONTEXT.md`
- `MEMORY.md`
- `ROUTE_SPEC.yaml`
- `HARD_GATES.md`
- `ARTIFACT_REQUIREMENTS.md`
- `FAILURE_TAXONOMY.md`
- `ADVISOR_INTENT.md`
- `HANDOFF_MANIFEST.yaml`
- `README.md`

## Required Pod Output Files

- `RUN_STATUS.json`
- `FINAL_STATUS.json`
- `ARTIFACT_INDEX.md`
- `FAILURE_REPORT.md`
- `PROPOSED_EVIDENCE_UPDATES.json`
- `ADVISOR_SUMMARY_DRAFT.md`
- `SHA256SUMS.txt`

## Boundaries

- Git is transport, not an experiment executor.
- TuringResearch does not directly control Modal or RunPod.
- No API keys, `.env`, raw data, SMPL-X body model files, cache folders, or
  secret dotfiles are transferred.
- `MEMORY.md` is a handoff-safe summary, not the sole source of truth.
- Pod output is auditable and produces proposed updates only.
