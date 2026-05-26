# TuringResearch Plus Artifact Auditor

The Artifact Auditor is a v0.2.0 Sprint 1 minimal implementation for local,
read-only artifact evidence checks.

## Purpose

It turns manifest-like indexes and committed VGGT dry-run scan summaries into an
`ArtifactAuditReport` without running VGGT or reading private project paths by
default.

## Supported Inputs

- JSON manifest-like files with `records` or `artifacts`.
- Markdown local scan index files.
- Explicit fixture files in tests.

## Supported Metadata

- path
- file type
- file size
- optional sha256
- included / omitted
- omitted reason
- safety flags
- NPZ summary placeholder or header metadata

## Safety

Paths under private VGGT-like roots such as `D:/vggt` are treated as external
references in default tests and are not read. They are marked omitted with
`private-path-not-read`.

## Non-Goals

- No recursive VGGT scan without explicit user config.
- No write into VGGT directories.
- No experiment success inference from filenames.
- No cross-machine sync.

