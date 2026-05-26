# Round 294 - Cross-platform Archive Hardening

Status: completed.

Scope:
- Harden Session runtime archive member handling for context and return packs.
- Cover Windows path spelling, Linux unpack notes, dotfile policy, symlink
  handling, and checksum validation.
- Validate before ingest review; do not unpack or execute archives.

Implemented:
- `archive_platform.py`
- `dotfile_policy.py`
- `path_normalization.py`
- `unpack_safety.py`
- `contracts/cross_platform_archive_hardening.yaml`

Safety:
- Path traversal is blocked.
- Absolute and Windows drive paths are blocked.
- Sensitive dotfiles are denied by default.
- Symlink members are blocked by default.
- Checksum mismatch blocks return ingest review.
- Same-owner preservation is documented as not allowed for manual unpack.
- No remote execution, default network, automatic unpack, or Evidence Ledger
  write was added.

Validation:
- Archive hardening tests, privacy/security gate, targeted sensitive scans,
  large-file checks, and whitespace checks were run for Round 294.

Push:
- Not pushed from this workspace because the target branch is absent locally or
  not safe to push from the current dirty worktree.
