# Lane 62 - SSH / SFTP Remote Artifact Reader

Status: implemented minimal.

Round 81 adds a fake-default, read-only SSH / SFTP Remote Artifact Reader for
remote artifact metadata and small review files.

## Added

- `src/turing_research_plus/remote_readers/`
- `contracts/ssh_sftp_remote_reader.yaml`
- `docs/ssh-sftp-remote-reader.md`
- `docs/remote-reader-safety-policy.md`
- VGGT remote reader fixture under
  `examples/vggt-human-prior-survey/remote_reader_fixture/`

## Boundaries

- Default mode does not connect to a remote host.
- Live SFTP requires explicit opt-in and credentials.
- The reader does not execute remote commands.
- The reader does not delete or write remote files.
- Forbidden paths, secrets, raw data, large payloads, and SMPL-X model files are
  omitted.
- Symlinks require manual review.
- The reader emits proposed imports only and does not overwrite Evidence Ledger.

## Validation

Round 81 validation covers fake reader models, local fixture import, path
policy, safety policy, workflow boundary checks, live optional skip behavior,
package imports, type checking, and linting.
