# Security Checklist

Status: active.

## Before Public Release

- [ ] Confirm `.env` is absent.
- [ ] Confirm `.env.example` contains variable names only.
- [ ] Confirm `.mcp.example.json` contains blank credentials only.
- [ ] Confirm no secret values are committed.
- [ ] Confirm no token-like values are committed.
- [ ] Confirm no private project link files are committed.
- [ ] Confirm no raw data, restricted datasets, or private papers are committed.
- [ ] Confirm no private model files are committed.
- [ ] Confirm no SMPL-X model files are committed.
- [ ] Confirm live adapters are disabled by default.
- [ ] Confirm live tests are skipped by default.
- [ ] Confirm all public examples are demo-safe.
- [ ] Confirm README and release notes state limitations clearly.

## Runtime Boundary

Default commands, examples, and tests must not require network access, provider
credentials, GPU services, Modal, or private local projects.
