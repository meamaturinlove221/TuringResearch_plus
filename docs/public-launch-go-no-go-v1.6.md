# Public Launch Go / No-Go v1.6

Status: review-ready / no automatic launch.

Round: 385.

## Decision

`GO FOR HUMAN LAUNCH REVIEW / NO-GO FOR AUTOMATIC PUBLICATION`

TuringResearch has enough public launch material for a maintainer review:

- README launch front door;
- docs bundle and GitHub Pages-ready dry-run path;
- dashboard and screenshot/demo asset pack;
- split manual packs;
- optional live disabled-by-default policy;
- open-source hygiene gate;
- v1.6 final archive and handoff docs.

This is not approval to publish automatically.

## Go Conditions

The following conditions must be true before a human launch:

- README is approved as the public project homepage.
- Docs bundle is reviewed from local release output.
- Security/privacy scan is rerun on the exact launch commit.
- No secrets, raw data, private paths, restricted model payloads, or fake URLs
  are present.
- License decision is approved by the maintainer.
- Tag name and source branch are approved.
- GitHub release draft is approved.
- PyPI decision is approved or explicitly deferred.
- Split repository creation is approved or explicitly deferred.

## No-Go Conditions

Stop the launch if any of these are true:

- a secret or API key is present;
- a private path appears in public docs or assets;
- raw data or restricted model payloads are included;
- a fake GitHub, Pages, or split-repo URL appears;
- fake/demo output is described as observed research evidence;
- VGGT or SparseConv3D `success` is claimed without evidence-ledger proof;
- ARIS is described as implemented;
- live networking, SSH/SFTP, or provider calls become default;
- release artifacts are unreviewed;
- license approval is unresolved.

## Current Round 385 Result

Public launch remains a maintainer decision. The repository is organized for
review, but this round does not create a release, tag, package publication,
docs deployment, or split repository.
