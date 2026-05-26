# Final Release Checklist: turingresearch-vggt-case

Status: final human checklist / not released.

This checklist is required before any future release of the optional
`turingresearch-vggt-case` child repository. It does not create a repository,
tag a release, publish a release, or push an external remote.

## Required Before Repository Creation

- [ ] repository owner approved;
- [ ] repository name approved: `turingresearch-vggt-case`;
- [ ] visibility approved;
- [ ] initial branch approved: `main`;
- [ ] initial commit message approved: `Initial public-safe VGGT case study`;
- [ ] remote URL is real and approved;
- [ ] main TuringResearch repository remains the flagship;
- [ ] child README backlink wording reviewed;
- [ ] issue templates reviewed or explicitly deferred.

## Required Content Review

- [ ] `README.md` reviewed;
- [ ] `QUICKSTART.md` reviewed;
- [ ] `CASE_STUDY.md` reviewed;
- [ ] `CLAIM_SAFETY.md` reviewed;
- [ ] `PRIVACY.md` reviewed;
- [ ] `LICENSE_NOTE.md` reviewed;
- [ ] `manifest.yaml` reviewed;
- [ ] `safety_report.md` reviewed;
- [ ] `.gitignore` reviewed.

## Required Safety Review

- [ ] no secrets;
- [ ] no raw data;
- [ ] no private paths;
- [ ] no restricted model payloads;
- [ ] no unsupported claims;
- [ ] no fake success claim;
- [ ] no placeholder URL used as a real URL;
- [ ] no fake/demo output written as observed evidence;
- [ ] no automatic repository creation;
- [ ] no automatic external push.

## Required Claim Boundary

- [ ] repository is a case study, not a VGGT experiment source repository;
- [ ] no VGGT success claim;
- [ ] no SparseConv3D success claim;
- [ ] no advisor approval claim without evidence;
- [ ] no local-only metadata promoted to public observed result evidence.

## Final Human Gate

Do not create, push, tag, or publish anything until every required item is
reviewed and maintainer approval is recorded.
