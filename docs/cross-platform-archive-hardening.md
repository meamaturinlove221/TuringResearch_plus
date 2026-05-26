# Cross-platform Archive Hardening

Status: v1.4 production parity hardening.

Round: 294.

This hardening layer aligns Session runtime archive handling with the stable
Neocortica-Session ideas around Windows tar, Linux unpack, dotfile handling,
path traversal, and checksum validation. It validates archive member names and
return package directories before ingest review. It does not unpack archives,
run remote commands, or write to the Evidence Ledger.

## What It Covers

- Windows path spelling is normalized to POSIX archive paths.
- Absolute paths and `..` traversal are blocked.
- Sensitive dotfiles are denylisted.
- Only explicitly allowlisted dotfiles are allowed.
- Manual unpack guidance says not to preserve same-owner metadata.
- Symlink members are blocked by default.
- File checksums are validated before ingest review.
- Structured return archives must contain required return files.

## Runtime Surfaces

- `archive_platform.py` provides cross-platform notes and path display helpers.
- `path_normalization.py` converts and validates archive member paths.
- `dotfile_policy.py` enforces denylist / allowlist dotfile handling.
- `unpack_safety.py` validates archive members and return directories.

## Return Archive Validation

Return archive validation requires:

- `RUN_STATUS.json`
- `FINAL_STATUS.json`
- `ARTIFACT_INDEX.md`
- `FAILURE_REPORT.md`
- `PROPOSED_EVIDENCE_UPDATES.json`
- `SHA256SUMS.txt`

All files except `SHA256SUMS.txt` must have checksum entries. A checksum
mismatch blocks ingest review. Missing required files are reported as blockers.

## Boundaries

- No automatic unpack.
- No remote execution.
- No default live network.
- No symlink extraction by default.
- No `--same-owner` style ownership preservation.
- No automatic Evidence Ledger write.
- Human review remains required.

## Example

```python
from turing_research_plus.session_runtime import (
    ArchiveMember,
    validate_archive_members,
)

report = validate_archive_members(
    [
        ArchiveMember(path="PROJECT_CONTEXT.md"),
        ArchiveMember(path="../escape.md"),
        ArchiveMember(path=".env"),
    ]
)
```

The report lists safe paths and blocker findings before any unpack or ingest
review.
