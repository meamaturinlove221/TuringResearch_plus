# TuringResearch Plus Failure Taxonomy Engine

Status: implemented minimal for v0.2 Sprint 2.

The Failure Taxonomy Engine standardizes VGGT and Codex long-route failure
language. It turns raw failure text into canonical categories, severity, retry
policy, likely causes, and next actions.

## Categories

- `FAST_RETURN`
- `REPORT_ONLY`
- `IDENTITY_COPY`
- `FALLBACK_ONLY`
- `REAL_BACKEND_UNAVAILABLE`
- `MISSING_ASSETS`
- `VISUAL_PROOF_INSUFFICIENT`
- `FULL_BODY_REGRESSION`
- `HAIRLINE_REGRESSION`
- `HAND_OBJECT_CONFUSION`
- `DEPTH_POINT_SCHEMA_MISMATCH`
- `PACKAGE_INCOMPLETE`
- `SPARSE_BACKEND_UNAVAILABLE`
- `SMPLX_ALIGNMENT_WEAK`
- `NOT_ENOUGH_EVIDENCE`
- `PROMOTION_FORBIDDEN`
- `STRICT_REGISTRY_FORBIDDEN`
- `HUMAN_REVIEW_REQUIRED`

## Core Models

- `FailureInstance`
- `FailureAttributionReport`
- `FailureTaxonomyEntry`
- `FailureAnalysisInput`

## Rules

- Attribution must be based on EvidenceRef or marked `requires_human_review`.
- Failure reports do not imply experiment success.
- Missing assets and visual proof remain separate categories.
- Sparse backend unavailability is distinct from generic not-enough-evidence.

## Tool Boundary

Proposed capsule-local tool:

- command: `turing failure analyze`
- tool: `experiment.failure_analyze`
- output: `FailureAttributionReport`

This is not a frozen public MCP API until root contracts and `docs/mcp-tools.md`
accept it.
