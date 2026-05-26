# Context Memory Policy

Status: v0.3 Sprint 1 design draft.

`MEMORY.md` inside a Git-based context package is a handoff-safe summary, not a
complete private memory store and not the only source of truth.

## Allowed Memory Content

- project summary;
- route summary;
- current blockers;
- accepted evidence ledger summary;
- artifact summary;
- advisor intent;
- known limitations;
- next actions.

## Forbidden Memory Content

- API keys;
- `.env` values;
- private raw data;
- model weights or SMPL-X body model files;
- full chat transcripts with sensitive content;
- unreviewed private paths;
- claims not supported by evidence.

## Sync Policy

Memory is not bidirectionally synced by default. Pod outputs may propose memory
updates, but TuringResearch treats them as proposed updates requiring review.

## Source of Truth

The source of truth remains structured artifacts:

- Evidence Ledger;
- Artifact Audit;
- Run Ingest report;
- Handoff Manifest;
- Hard Gate reports;
- Failure Attribution reports.
