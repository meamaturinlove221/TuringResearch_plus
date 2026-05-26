# SSH / SFTP Remote Artifact Reader

Status: v0.4 minimal implementation.

The SSH / SFTP Remote Artifact Reader indexes selected remote artifact metadata
and small review files without becoming a remote executor. Default workflows use
fake or local fixture data. Live SFTP is optional and must be explicitly enabled.

## Scope

The minimal implementation supports:

- fake reader;
- local JSON fixture index;
- optional live SFTP reader surface;
- credential-absent graceful skip;
- path policy checks;
- safety policy checks;
- selected small review files;
- omitted unsafe or large files;
- proposed imports only.

## Output

`RemoteReaderReport` contains:

- `host_label`
- `root_path`
- `scanned_paths`
- `selected_files`
- `omitted_files`
- `errors`
- `safety_warnings`
- `proposed_imports`
- `requires_human_review`

## Safety Rules

- Default mode does not connect to a remote host.
- Live mode requires explicit opt-in.
- The reader does not execute remote commands.
- The reader does not delete remote files.
- The reader does not write remote files.
- Forbidden paths are omitted.
- `.env`, secrets, raw data, and cache paths are omitted.
- Large files are metadata-only by default.
- Symlinks require manual review.
- Credentials are read only from environment variables and are not stored.
- Remote artifacts are indexed or retrieved, not verified.

## VGGT Use

For VGGT / Modal review, the remote reader should inspect only thin review
outputs such as `final_status.json`, `failure_report.md`, `artifact_index.md`,
board inventories, sha256 manifests, and small Markdown/JSON summaries. Large
arrays, raw datasets, body model files, and private config files remain omitted
or summary-only.

## Live Mode

Live mode requires:

- `TURINGRESEARCH_ENABLE_LIVE_TESTS=1`
- `TURINGRESEARCH_SFTP_CREDENTIAL`

The current minimal live surface is intentionally conservative. Without
explicit opt-in and credentials, live tests skip or return a typed
`missing-credential` state. Default workflows use fake or fixture input.

## Evidence Boundary

Remote artifacts do not become observed evidence automatically. The reader only
produces proposed imports. Evidence Ledger promotion remains a separate manual
review step.
