# Research Data Safety Levels

Status: active policy draft.

## `public-demo`

Fake or fully authorized public examples. This is the only default level for
public demo material.

## `internal-research`

Internal planning and review material. It can be useful for research operations
but still requires review before sharing.

## `private-research`

Project-private paths, notes, advisor feedback, or local machine details.
Private research material should not be included in public examples.

## `restricted-data`

Raw datasets, licensed model payloads, private papers, or data that may require
special authorization. These files should be omitted or represented by
metadata-only references.

## `secret-forbidden`

Credentials, `.env`, API keys, access tokens, private SSH keys, and provider
secrets. These are release blockers and should not be committed or exported.

## Review Rule

Lowering a safety level requires human review. A scanner report is a gate, not
an authorization system.
