# Round 305 - Optional Heavy PDF Backend Slot

Status: completed.

Scope:

- Reserve an optional backend slot for future MinerU or arxiv2md fallback.
- Add interface-only request/result models.
- Add skipped reason and Markdown renderer.
- Do not implement heavy PDF processing.

Artifacts:

- `src/turing_research_plus/scholar_pipeline/heavy_pdf_backend_slot.py`
- `contracts/heavy_pdf_backend_slot.yaml`
- `tests/unit/test_heavy_pdf_backend_slot.py`
- `docs/optional-heavy-pdf-backend-slot.md`

Safety:

- MinerU not implemented.
- Heavy backend disabled by default.
- No OCR default.
- No large PDF processing.
- No heavy dependency.
- Interface / skipped reason / future backend only.

Validation:

- Backend slot tests, privacy/security checks, targeted scans, large-file
  checks, and whitespace checks were run for Round 305.

Push:

- Not pushed from this workspace because the target branch is absent locally or
  not safe to push from the current dirty worktree.
