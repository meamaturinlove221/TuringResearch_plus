# Public Release Checklist Final

Round: 400R
Status: checklist, not executed

## Required Before Public Release

- [ ] PR #1 closed or explicitly not merged.
- [ ] PR #2 merged or explicitly approved as docs-only.
- [ ] Open-source safety gate rerun after final branch selection.
- [ ] README reviewed for TuringResearch public naming.
- [ ] Upstream references use Reference / Inspiration / Related Projects only.
- [ ] No migrated academic publication claim.
- [ ] No fake benchmark.
- [ ] No fake GitHub Pages URL.
- [ ] No fake split repo URL.
- [ ] No fake users or fake stars.
- [ ] No `.env`.
- [ ] No API key / token / cookie / password payload.
- [ ] No SSH private key.
- [ ] No raw data.
- [ ] No SMPL-X payload.
- [ ] No third-party PDF payload.
- [ ] No unsupported VGGT or SparseConv3D success claim.
- [ ] No automatic remote execution.
- [ ] No ARIS implementation claim.

## Manual Release Decisions

- [ ] GitHub repository rename.
- [ ] Repository visibility.
- [ ] Default branch.
- [ ] GitHub Release.
- [ ] Tag.
- [ ] PyPI.
- [ ] GitHub Pages.
- [ ] Split repository creation.

## Final Local Checks

```powershell
python -m pytest tests/contract/test_public_name_integrity_turingresearch.py tests/contract/test_name_integrity.py -q
python -m pytest tests/contract/test_open_source_hygiene_gate.py tests/contract/test_public_release_hygiene.py -q
python -m pytest tests/contract/test_v1_6_release_contracts.py tests/workflow/test_v1_6_full_replay.py -q
python -m ruff check .
git diff --check
```
