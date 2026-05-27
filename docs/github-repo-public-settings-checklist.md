# GitHub Repo Public Settings Checklist

Round: 399R
Status: manual checklist

## Visibility

- [ ] Maintainer has decided whether to make the repository public.
- [ ] No visibility change is made automatically by Codex.
- [ ] Repository contents were reviewed after PR #1 NO-GO.
- [ ] Open-source safety gate was rerun after final merges.

## Branches

- [ ] Launch branch selected.
- [ ] PR #1 not merged.
- [ ] PR #2 decision recorded.
- [ ] Default branch decision recorded.
- [ ] Branch protection reviewed if needed.

## Security

- [ ] No `.env`.
- [ ] No committed API key / token / cookie / password.
- [ ] No SSH private key.
- [ ] No raw data.
- [ ] No SMPL-X payload.
- [ ] No third-party PDF payload.
- [ ] No private local path payload.

## Claims

- [ ] No VGGT success claim.
- [ ] No SparseConv3D success claim.
- [ ] No migrated academic publication claim.
- [ ] Upstream is described only as Reference / Inspiration / Related Projects.
- [ ] README does not mention fake users or fake stars.

## Releases / Pages / Packages

- [ ] No GitHub Release is published automatically.
- [ ] No tag is created automatically.
- [ ] No GitHub Pages deployment is enabled automatically.
- [ ] No PyPI publication is performed automatically.
- [ ] No split repository is created automatically.

## Final Gate

- [ ] Run name integrity.
- [ ] Run README/open-source hygiene checks.
- [ ] Run privacy/security gate.
- [ ] Run final smoke.
