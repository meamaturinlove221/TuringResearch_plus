# Round 271 - Scholar Full Tool Surface

Status: completed.

Scope:
- Add a v1.3 Neocortica-Scholar full tool surface.
- Keep the surface fake/default and review-only.
- Do not implement MinerU, heavy OCR, automatic full paper download, paywall
  bypass, or final paper conclusions.

Tool surface:
- `scholar.paper_searching`;
- `scholar.paper_content`;
- `scholar.paper_reference`;
- `scholar.paper_reading`.

Files:
- `src/turing_research_plus/scholar_tools/`
- `contracts/scholar_full_tool_surface.yaml`
- `docs/scholar-full-tool-surface.md`
- Scholar tool unit tests
- `tests/workflow/test_scholar_full_tool_surface_fake.py`

Safety:
- Fake mode is default.
- No real API key is required.
- Live tests are skipped by default.
- Cached Markdown and fake adapter outputs are review context only.
- No MinerU, heavy OCR, automatic full paper download, paywall bypass, final
  paper conclusion, or camera-ready text generation was added.

Validation:
- Scholar tool tests, workflow fake tests, mypy, privacy/security gate, targeted
  sensitive scans, large-file checks, and whitespace checks were run for Round
  271.

Push:
- Not pushed from this workspace because the target branch is absent locally and
  the worktree contains historical unrelated changes.
