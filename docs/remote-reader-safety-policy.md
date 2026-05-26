# Remote Reader Safety Policy

Status: active for v0.4 remote artifact foundations.

The remote reader safety policy keeps SSH / SFTP artifact access read-only and
review-first.

## Hard Boundaries

- No remote command execution.
- No remote experiment execution.
- No remote file deletion.
- No remote file writes.
- No credential files in the repository.
- No automatic Evidence Ledger overwrite.
- No remote artifact promoted to verified evidence.

## Forbidden Content

The reader omits paths containing private data, raw data, secrets, cache
folders, or broad root paths. It also omits `.env`, secret-like filenames,
SMPL-X body model files, large NPZ payloads, and unsupported file types.

## Symlink Policy

Symlinks are not followed by default. A symlink path is reported as omitted with
`symlink-requires-review` so a human can decide whether it is safe.

## Large File Policy

Large files are represented by metadata only. When size or type suggests an
array payload, raw dataset, or body model file, the report records the omitted
reason and safety warning.

## Live Test Policy

Live SFTP tests are skipped unless `TURINGRESEARCH_ENABLE_LIVE_TESTS=1` and the
configured credential environment variable is present. Missing credentials are
not default test failures.
