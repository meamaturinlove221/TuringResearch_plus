# Pod Lifecycle SOP Showcase

## Source

- Upstream repository: `Pthahnix/Neocortica-Session`
- Source basis: session workflow, Git-context transfer, pod-deployment context, and v2 rewrite notes
- Upstream reference commit: `5a01485cbd38df83e5b44851001a2acd9334f2f7`
- Migration type: `adapted_with_authorization`
- Code migration: none

## Summary

This SOP captures the academic workflow idea behind a pod-oriented research execution lifecycle. The important contribution is not a specific script implementation, but the separation of a risky long-running remote workflow into inspectable stages.

## Stages

### 1. Preflight

Check that the local project, context files, output directories, safety policies, and expected return artifacts exist before any transfer or execution is attempted.

### 2. Context Pack

Package only the public-safe and task-relevant context. Exclude secrets, `.env`, raw private data, local caches, large binary artifacts, and hidden files unless explicitly allowlisted.

### 3. Transfer Plan

Describe what would be transferred and where it would go. In TuringResearch, this remains fake/dry-run by default. Live SFTP requires explicit opt-in and separate safety gates.

### 4. Remote Launch Plan

Generate a manual runbook rather than executing remote commands by default. A human must review any SSH, tmux, pod, or shell action.

### 5. Return Manifest

Require the remote side to return structured status files, artifact indexes, checksums, and failure reports. Claims from the remote side are not trusted automatically.

### 6. Human Confirmation

Before any returned result enters the evidence ledger, TuringResearch should create a human-confirmation packet and require accept / reject / partial_accept / requires_more_review.

## TuringResearch Demonstration

This SOP maps to:

- `SessionPreflightRunner`
- `ContextPackBuilder`
- `FakeTransferRunner`
- `RemoteReturnVerifier`
- `HumanConfirmation`
- `ProposedEvidenceUpdateReport`

## Safety Boundary

This document is an academic workflow showcase. It does not include upstream code, private hostnames, SSH credentials, raw session logs, or live command execution.

## Attribution

Adapted with attribution from authorized Neocortica-Session workflow materials.
