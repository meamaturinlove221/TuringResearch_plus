# Neocortica Session Parity

Status: v1.2 parity implementation.

Round: 236.

This round aligns TuringResearch with the stable session/context/pod workflow
ideas from the tracked Session reference while keeping TuringResearch's
local-first, review-only boundary. It does not copy upstream code and does not
implement remote execution.

## Implemented

- Context pack manifest.
- Structured return manifest.
- Dotfile exclusion policy.
- Path traversal guard.
- Shell metacharacter risk check.
- Windows/Linux archive compatibility notes.
- Memory no-bidirectional-sync policy.

## Context Pack

A session context pack is a durable, reviewable file set:

- `PROJECT_CONTEXT.md`
- `MEMORY.md`
- `ROUTE_SPEC.yaml`
- optional review files such as `HARD_GATES.md` and
  `ARTIFACT_REQUIREMENTS.md`

`MEMORY.md` is not the only source of truth. Evidence Ledger, Artifact Audit,
Run Ingest, Handoff Manifest, and Route Spec remain the review surfaces.

## Archive Safety

Archive entries are checked before packaging or unpacking:

- relative paths only;
- no path traversal;
- no private local paths;
- no forbidden dotfiles;
- no secret-like path names;
- no raw data folders;
- no restricted body model payloads;
- shell metacharacter risk is reported.

Windows-to-Linux transfer must normalize path separators and validate archive
entries before unpacking.

## Structured Return

Pod output is represented by a structured manifest and required files:

- `RETURN_MANIFEST.yaml`
- `RUN_STATUS.json`
- `FINAL_STATUS.json`
- `ARTIFACT_INDEX.md`
- `FAILURE_REPORT.md`
- `PROPOSED_EVIDENCE_UPDATES.json`
- `ADVISOR_SUMMARY_DRAFT.md`
- `SHA256SUMS.txt`

Proposed evidence updates are review inputs only. They are not applied
automatically.

## Explicit Non-goals

- No SSH provision.
- No tmux attach.
- No auto pod cleanup.
- No remote command execution.
- No Modal execution.
- No automatic git push.
- No automatic Evidence Ledger write.
- No bidirectional memory sync.

## Tests

- `tests/unit/test_session_context_pack.py`
- `tests/unit/test_context_archive_safety.py`
- `tests/unit/test_structured_return_manifest.py`
- `tests/unit/test_platform_compat.py`
- `tests/workflow/test_neocortica_session_parity_fake.py`
