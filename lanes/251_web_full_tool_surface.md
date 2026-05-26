# Round 273 - Web Full Tool Surface

Status: completed.

Scope:
- Add a v1.3 Neocortica-Web full tool surface.
- Keep the surface fake/default, local-first, and review-only.
- Do not add default networking, cookie storage, private content fetching,
  paywall bypass, or verified-evidence promotion.

Tool surface:
- `web.web_fetching`;
- `web.web_content`;
- `web.cache`;
- `web.source_metadata`;
- `web.apify_optional`.

Files:
- `src/turing_research_plus/web_tools/`
- `contracts/web_full_tool_surface.yaml`
- `docs/web-full-tool-surface.md`
- Web tool unit tests
- `tests/workflow/test_web_full_tool_surface_fake.py`

Safety:
- Fake mode is default.
- No real API key is required for fake mode.
- Live tests are skipped by default.
- Optional Apify remains explicit live opt-in.
- Retrieved web content is review context only.

Validation:
- Web tool tests, workflow fake tests, mypy, privacy/security gate, targeted
  sensitive scans, large-file checks, and whitespace checks were run for Round
  273.

Push:
- Not pushed from this workspace because the target branch is absent locally and
  the worktree contains historical unrelated changes.
