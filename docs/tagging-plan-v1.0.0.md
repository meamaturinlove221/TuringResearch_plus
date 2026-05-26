# Tagging Plan: v1.0.0

Status: plan only.

Round: 196.

This plan describes a future manual tagging flow. It does not create a tag.

## Candidate Tag

- Proposed tag: `v1.0.0-rc0`
- Version marker: `1.0.0rc0`

## Preconditions

- Maintainer approval.
- Release branch reviewed.
- Full regression report reviewed.
- Security/privacy audit reviewed.
- Changelog reviewed.
- GitHub release draft reviewed.

## Manual Tagging Steps

The following commands are examples for a human maintainer after review. They
must not be run automatically by this round.

```bash
git status
git tag -a v1.0.0-rc0 -m "TuringResearch Plus v1.0.0-rc0"
git push origin v1.0.0-rc0
```

## Rollback

If a release blocker is found before public release:

- do not publish the GitHub release;
- delete only unpublished local tags if needed;
- document the blocker in release notes;
- rerun full regression after the fix.

If a public tag was already pushed, do not rewrite history without maintainer
approval. Prefer a follow-up release candidate.
