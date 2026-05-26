# Git-based Context Handoff

Status: v0.3 Sprint 1 design draft.

Git-based Context Handoff uses Git as a transport for reviewable context
packages between local machines, pods, and review environments. It does not
transfer full ChatGPT or Codex sessions and does not execute remote code.

## Design Goal

TuringResearch Plus should hand off durable context using structured files:

- project summary;
- memory summary;
- route pack;
- hard gates;
- artifact requirements;
- failure taxonomy;
- advisor intent;
- handoff manifest.

Git is the carrier. TuringResearch remains responsible for ingest, audit,
evidence discipline, and advisor-ready summaries.

## Context Package

A TuringResearch context package contains:

- `PROJECT_CONTEXT.md`
- `MEMORY.md`
- `ROUTE_SPEC.yaml`
- `HARD_GATES.md`
- `ARTIFACT_REQUIREMENTS.md`
- `FAILURE_TAXONOMY.md`
- `ADVISOR_INTENT.md`
- `HANDOFF_MANIFEST.yaml`
- `README.md`

The package is not a raw session dump. It is a compact, reviewable, durable
handoff.

## Output Return

Remote pod outputs should return as structured files:

- `RUN_STATUS.json`
- `FINAL_STATUS.json`
- `ARTIFACT_INDEX.md`
- `FAILURE_REPORT.md`
- `PROPOSED_EVIDENCE_UPDATES.json`
- `ADVISOR_SUMMARY_DRAFT.md`
- `SHA256SUMS.txt`

These files can be returned through git push or wrapped in a v0.2 handoff
bundle. They are then consumed by Run Ingestor, Artifact Auditor, Evidence
Ledger, Failure Taxonomy, and Advisor Pack workflows.

## Difference From Neocortica-Session

TuringResearch Plus does not copy Neocortica-Session scripts. It does not
depend on Claude-specific paths and does not treat `MEMORY.md` as the only
truth. Git handoff is a transport layer, not an execution engine.

TuringResearch keeps structured foundations:

- Evidence Ledger
- Artifact Auditor
- Run Ingestor
- Advisor Pack
- Experiment Route DSL
- Hard Gates
- Failure Taxonomy

## Safety

- Do not include API keys.
- Do not include `.env`.
- Do not include raw data.
- Do not include SMPL-X body model files.
- Large files are represented by manifest, sha256, and omitted reason.
- `MEMORY.md` includes only public or handoff-safe summaries.
- Pod outputs must be auditable and must not overwrite ledgers automatically.

## Non-Goals

- No remote execution.
- No Modal or RunPod control.
- No NAS / SMB / SSH / cloud sync.
- No full session teleport.
- No bidirectional memory sync by default.
