---
name: turingresearch-fusion-context-management
description: Use when maintaining context init, checkpoint, recover, index, or summarize behavior.
---

# TuringResearch Plus Skill: turingresearch-fusion-context-management

## Role

Maintain recoverable context files, checkpoints, index entries, artifacts, and evidence refs.

## When to use

Use this skill when work touches the owner lane, related contracts, modules, tests, or release gates listed below.

## Inputs

- User request naming `turingresearch-fusion-context-management` or the matching TuringResearch Plus lane.
- Existing contracts, Pydantic models, tests, docs, and ledger entries.
- Fake-service or dry-run fixtures when workflow behavior is involved.

## Outputs

- Updated TuringResearch Plus files in the listed required paths.
- Passing focused tests and release-safe documentation updates.
- Ledger updates in `lanes/00_master_ledger.md` and the owner lane.

## Required files

- `src/turing_research_plus/context/`

## Related contracts

- `contracts/fusion_workflows.yaml`
- `contracts/artifact_schema.yaml`

## Related lanes

- `lanes/05_vault_memory.md`

## Required tests

- `tests/unit/test_context_models.py`
- `tests/unit/test_context_service.py`
- `tests/unit/test_context_index.py`

## Rules / constraints

- Project display name is TuringResearch Plus.
- Core package is `turing_research` and Plus package is `turing_research_plus`.
- MCP server name is `turingresearch-plus`.
- Skill names must use the `turingresearch-` prefix.
- Keep work inside `TuringResearch/TuringResearch_plus`.
- Do not require real network access, external API keys, or live service calls in tests.
- Preserve EvidenceRef, ResearchArtifact, BudgetGate, and StateLedger boundaries when relevant.
- Use service protocols or adapters for external APIs.
- Update the owner lane and `lanes/00_master_ledger.md` after meaningful changes.

## Done criteria

- Implementation status: `locked`.
- Release requirement: `release-critical`.
- Related tests pass or a release blocker is explicitly recorded.
- Documentation and contracts remain aligned with current TuringResearch Plus naming.

## Round 240 SOP Parity

- `workflow`: pod workflow
- `when_to_use`: prepare or validate handoff bundles, context packs, pod
  lifecycle safety docs, structured return manifests, or context recovery.
- `inputs`: project context, memory notes, route spec, forbidden file policy,
  transfer policy, and return manifest requirements.
- `outputs`: context pack manifest, preflight report, proposed return updates,
  structured return manifest, and safety report.
- `safety`: no SSH, tmux, Modal execution, remote command execution, automatic
  git push, or bidirectional memory sync.
- `non-goals`: no remote executor, no automatic evidence ledger mutation, no
  private path transfer.
- `handoff`: record proposed updates only, conflict policy, missing metadata,
  and human-review status.
- `tests`: pod lifecycle, session context pack, archive safety, return manifest,
  and platform compatibility tests.
- `related_docs`: `docs/pod-context-lifecycle-safety.md`,
  `docs/neo` `cortica-session-parity.md`,
  `docs/git-based-context-handoff.md`.
