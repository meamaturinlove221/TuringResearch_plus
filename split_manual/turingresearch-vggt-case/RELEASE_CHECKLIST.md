# Release Checklist: turingresearch-vggt-case

Status: release checklist draft / not released.

This checklist is for a future human-maintained release of the
`turingresearch-vggt-case` repository. It does not publish a release, create a
tag, create a GitHub repository, or push an external remote.

## Required Before First Release

- [ ] repo created manually
- [ ] README reviewed
- [ ] license reviewed
- [ ] privacy reviewed
- [ ] no secrets
- [ ] no raw data
- [ ] no private paths
- [ ] main repo linked
- [ ] first release draft
- [ ] issue templates optional

## VGGT Case Specific Checks

- [ ] The repository is described as a case study, not a VGGT experiment source
      repository.
- [ ] No SMPL-X files or restricted model payloads are present.
- [ ] No VGGT experiment success claim is present.
- [ ] No SparseConv3D success claim is present.
- [ ] Fake/demo references are not presented as observed evidence.

## First Release Draft Shape

Suggested draft title:

```text
turingresearch-vggt-case initial public-safe case study
```

Suggested release note boundary:

```text
This is a public-safe case-study repository. The main TuringResearch
repository remains the flagship install, docs, release, public API, and star
entry point.
```

## Final Human Gate

Do not publish the release until a maintainer confirms the repository exists,
the README points back to the flagship repository, and every required checklist
item is complete.
