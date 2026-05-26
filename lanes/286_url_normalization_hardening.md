# Round 308 - URL Normalization Hardening

Status: completed.

Scope:

- Add WebMeta / `normUrl`-style URL normalization helpers.
- Normalize scheme, host, path, query ordering, default ports, fragments, and
  tracking query params.
- Block non-HTTP(S) schemes by default.
- Do not fetch URLs or enable live networking.

Artifacts:

- `src/turing_research_plus/web_tools/url_normalization.py`
- `tests/unit/test_url_normalization_hardening.py`
- `docs/url-normalization-hardening.md`

Safety:

- No network request.
- No cookie storage.
- No private content access.
- No paywall bypass.
- No credential handling.
- Human review required.

Validation:

- URL normalization tests, privacy/security checks, targeted scans, large-file
  checks, and whitespace checks were run for Round 308.

Push:

- Not pushed from this workspace because the target branch is absent locally or
  not safe to push from the current dirty worktree.
