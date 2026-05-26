# Optional Heavy PDF Backend Slot

Status: interface only.

Round: 305.

This document reserves an optional backend slot for future heavy PDF processing
such as MinerU or arxiv2md fallback. It does not implement MinerU, does not add
heavy dependencies, and does not enable OCR.

## What Exists

- `HeavyPdfBackendRequest`
- `HeavyPdfBackendSlot`
- `HeavyPdfBackendKind`
- `HeavyPdfBackendStatus`
- `build_heavy_pdf_backend_slot`
- `render_heavy_pdf_backend_slot`

## Default Behavior

- MinerU not implemented.
- arxiv2md fallback not implemented.
- heavy backend disabled by default.
- no OCR default.
- no large PDF processing.
- interface / skipped reason / future backend notes only.

## Skip Reason

The slot exists so production parity docs and tests can point to a clear future
extension point without pretending that a heavy backend is available.

## Safety Boundary

- no heavy PDF dependency;
- no OCR;
- no automatic full paper download;
- no paywall bypass;
- no large PDF processing;
- no final paper conclusion;
- human review required.

## Validation

Run:

```powershell
python -m pytest tests/unit/test_heavy_pdf_backend_slot.py -q
```
