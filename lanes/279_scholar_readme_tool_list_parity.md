# Round 301 - Scholar README Tool List Parity

Status: completed.

Scope:
- Add README-style Scholar production tool list docs.
- Add public pipeline section and fake MCP test result display.
- Add demo `TOOL_LIST.md`.
- Do not add adapter functionality or live behavior.

Tool list:
- `scholar.paper_searching`.
- `scholar.paper_content`.
- `scholar.paper_reference`.
- `scholar.paper_reading`.

Safety:
- Fake mode default.
- No API key required.
- No automatic full paper download.
- No paywall bypass.
- No fake citation is marked as verified.
- Human review required.

Validation:
- Scholar docs tests, targeted sensitive scans, large-file checks, and
  whitespace checks were run for Round 301.

Push:
- Not pushed from this workspace because the target branch is absent locally or
  not safe to push from the current dirty worktree.
