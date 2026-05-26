# Redaction Policy

Status: active policy draft.

## Principle

Redaction in TuringResearch Plus is proposed-only by default. The scanner never
overwrites source files.

## Allowed

- Generate a `RedactionProposal`.
- Replace detected key-like values with `[REDACTED]` in preview text.
- Replace personal paths in preview text.
- Ask a human reviewer to approve edits.

## Not Allowed

- Automatic destructive cleanup.
- Automatic overwrite of original research notes.
- Automatic deletion of files.
- Redacting evidence in a way that changes scientific meaning.
- Treating a redacted file as verified.

## Public Release Use

Before public release, redaction proposals should be reviewed and applied in a
separate explicit edit. The final release gate should run the scanner again.
