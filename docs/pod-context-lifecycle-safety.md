# Pod Context Lifecycle Safety

Status: v1.0 prelaunch safety plan.

Round 177B adds a review-only Pod Context Lifecycle layer. It absorbs the
useful upstream idea of durable Git-based context transfer, but it does not
copy upstream scripts and does not execute remote work.

## Lifecycle Object

`PodContextLifecycle` records:

- `context_package_id`
- `source_machine_label`
- `target_environment_label`
- `route_id`
- `memory_policy`
- `transfer_policy`
- `preflight_checks`
- `forbidden_files`
- `structured_output_requirements`
- `return_verification`
- `conflict_policy`
- `requires_human_review`

## Durable Context Package

The v1.0 context package uses reviewable files:

- `PROJECT_CONTEXT.md`
- `MEMORY.md`
- `ROUTE_SPEC.yaml`

`MEMORY.md` is a summary, not the only source of truth. Evidence Ledger,
Artifact Audit, Run Ingest, Handoff Manifest, and Route Spec remain the
structured review surfaces.

## Structured Pod Return

Pod outputs must return structured files:

- `RETURN_MANIFEST.yaml`
- `RUN_STATUS.json`
- `FINAL_STATUS.json`
- `ARTIFACT_INDEX.md`
- `FAILURE_REPORT.md`
- `PROPOSED_EVIDENCE_UPDATES.json`
- `ADVISOR_SUMMARY_DRAFT.md`
- `SHA256SUMS.txt`

`PROPOSED_EVIDENCE_UPDATES.json` is never applied automatically.

## Safety Boundary

- Git-based context transfer is a transport concept, not an execution engine.
- No bidirectional memory sync.
- Dotfiles are blocked unless generated and explicitly safe.
- Shell metacharacter risk is reported before any transfer.
- Archive entries must be relative paths only.
- Windows archive creation and Linux unpack require path validation.
- Return metadata must match context package, route, and target environment.

## v1.0 Non-goals

- No remote command execution.
- No tmux launch.
- No SSH provision.
- No Modal execution.
- No automatic git push.
- No Evidence Ledger auto-write from pod output.

## Review Result

The lifecycle layer produces preflight, transfer, return verification, and
safety reports. It can block unsafe packages, but it cannot run a pod.
