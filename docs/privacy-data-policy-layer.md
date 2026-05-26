# Privacy / Data Policy Layer

Status: v0.6 minimal implementation.

Round 107 adds a local privacy and data safety gate. It supports workspace,
handoff, remote artifact, public demo, and advisor export review workflows.

It is a scanner and report layer. It is not an encryption system, permission
system, or destructive cleanup tool.

## Safety Levels

- `public-demo`: safe demo material with no private data.
- `internal-research`: internal notes that still require review.
- `private-research`: private paths, personal paths, or project-private notes.
- `restricted-data`: raw data, licensed files, private model payloads.
- `secret-forbidden`: credentials and secrets that must not be exported.

## Detection Surface

The default policy detects:

- `.env`
- API key-like patterns
- access token-like patterns
- `private_data`
- `local_project_links.yaml`
- raw data markers
- SMPL-X model files
- huge `npz`
- personal paths
- private advisor feedback markers
- licensed model files

## Output

`PrivacyScanReport` contains:

- `scanned_paths`
- `findings`
- `severity`
- `recommended_action`
- `redaction_possible`
- `release_blocker`
- `requires_human_review`
- proposed redactions
- limitations

## Rules

- No network access.
- No automatic deletion.
- No automatic redaction overwrite.
- No upload of scan results.
- No private VGGT path reads.
- Only reports and proposed redactions are produced.
- Human review is required.

## Related Workflows

- Public Release Hardening uses this scanner before release.
- Handoff Bundle Export / Import can use the report as a preflight gate.
- Remote Artifact Integration can map unsafe artifacts to findings.
- Public Demo Suite should scan clean.
- Advisor Export can scan bundle sources before handoff.

## Limitations

- Pattern-based scanning can miss secrets or produce false positives.
- It does not inspect encrypted archives.
- It does not validate licenses automatically.
- It does not replace human review.
