# Round 274 - Apify Workflow Templates

Status: completed.

Scope:
- Add public-safe Apify workflow templates for optional web adapter usage.
- Keep templates review-only and fake/default.
- Do not call Apify by default.
- Do not require a token for examples, tests, or documentation review.

Templates:
- `examples/apify_workflows/project_page_fetch.yaml`
- `examples/apify_workflows/search_result_fetch.yaml`
- `examples/apify_workflows/content_extract.yaml`

Safety:
- `APIFY_TOKEN` is optional.
- Live mode is disabled by default.
- Examples contain no key or token value.
- No login bypass, paywall bypass, private content scraping, cookie storage, or
  automatic evidence promotion is allowed.
- Fetched content remains review context until a human verifies it.

Validation:
- Apify workflow template tests, existing Apify/Web focused tests,
  privacy/security gate, name integrity, targeted sensitive scans, large-file
  checks, and whitespace checks were run for Round 274.

Push:
- Not pushed from this workspace because the target branch is absent locally and
  the worktree contains historical unrelated changes.
