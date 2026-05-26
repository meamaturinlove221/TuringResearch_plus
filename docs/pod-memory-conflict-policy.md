# Pod Memory Conflict Policy

Status: v1.0 prelaunch policy.

Pod context packages may include `MEMORY.md`, but memory is a handoff-safe
summary only.

## Rules

- No bidirectional memory sync.
- No pod-side overwrite of local memory.
- Pod output may propose memory or evidence updates.
- Human reviewers resolve conflicts.
- Evidence Ledger, Artifact Audit, Run Ingest, Handoff Manifest, and Route Spec
  remain the source-of-truth surfaces.

## Conflict Handling

Conflicts are represented as proposed updates and review notes. TuringResearch
does not merge them automatically.
