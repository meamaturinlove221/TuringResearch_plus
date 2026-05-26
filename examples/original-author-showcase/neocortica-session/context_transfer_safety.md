# Context Transfer Safety Showcase

## Source

- Upstream repository: `Pthahnix/Neocortica-Session`
- Source basis: dotfile handling, shell-injection risk, pod-deployment context, and cross-platform archive behavior
- Upstream reference commit: `5a01485cbd38df83e5b44851001a2acd9334f2f7`
- Migration type: `summarized_with_attribution`
- Code migration: none

## Summary

The academic output here is a safety model for transferring agent/research context across environments. It highlights that context transfer is not only a packaging problem; it is also a trust-boundary problem.

## Safety Lessons

### Dotfiles Are Sensitive by Default

Hidden files often contain secrets, local tool configuration, credentials, or private machine state. TuringResearch should exclude dotfiles by default and allow only explicit, reviewed allowlists.

### Shell Arguments Must Be Treated as Untrusted

Generated commands can become dangerous if user-controlled values are interpolated without quoting or validation. TuringResearch should keep live command generation behind manual review and safety checks.

### Archives Need Cross-platform Validation

Archives created on Windows and unpacked on Linux can behave differently around paths, permissions, symlinks, owners, and hidden files. TuringResearch should normalize paths and validate archives before import.

### Return Artifacts Are Claims, Not Truth

A returned `FINAL_STATUS.json` or report is only a remote claim until local verification checks files, checksums, missing artifacts, and safety policy.

## TuringResearch Demonstration

This showcase supports:

- archive safety checks;
- path traversal blocking;
- dotfile policy;
- no-secret public configuration;
- live output redaction;
- human confirmation before ledger import.

## Safety Boundary

This file is a policy summary. It contains no upstream code, no real shell commands, no private paths, and no live remote targets.

## Attribution

Summarized with attribution from authorized Neocortica-Session workflow and safety materials.
