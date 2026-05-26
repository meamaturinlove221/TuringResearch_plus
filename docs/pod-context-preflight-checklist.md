# Pod Context Preflight Checklist

Status: v1.0 prelaunch checklist.

Run this checklist before a pod context package is handed to any external
environment.

## Required Context Files

- `PROJECT_CONTEXT.md`
- `MEMORY.md`
- `ROUTE_SPEC.yaml`

## Forbidden Content

- `.env`
- API keys or token assignments
- `local_project_links.yaml`
- private data markers
- raw data
- SMPL-X model payloads
- huge `npz` payloads
- private local paths

## Path Safety

- No absolute archive paths.
- No `..` traversal.
- No shell metacharacters in identifiers or package paths.
- No secret-like filenames.
- No forbidden dotfiles such as `.git`, `.ssh`, `.codex`, or `.aws`.

## Review Boundary

Preflight can only produce a report. It does not SSH, start tmux, run Modal,
create branches, push git, or update ledgers.
