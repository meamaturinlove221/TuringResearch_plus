# Pod Context Transfer Policy

Status: v1.0 prelaunch policy.

The approved v1.0 transfer shape is `git_context_package`: a reviewable package
of text manifests and structured route files.

## Allowed

- Git-based context package as a carrier.
- Relative paths inside archive/package entries.
- Generated context files such as `PROJECT_CONTEXT.md`, `MEMORY.md`, and
  `ROUTE_SPEC.yaml`.
- Structured output template files.

## Blocked

- Remote command execution.
- SSH provision.
- Modal execution.
- Automatic git push.
- Shell execution.
- Secret dotfiles.
- Absolute archive paths.
- Path traversal.
- Raw data and restricted model payloads.

## Compatibility Note

Windows archive creation and Linux unpack are allowed only when package entries
are validated as relative paths. Archive extraction must reject traversal and
absolute path entries before unpack.
