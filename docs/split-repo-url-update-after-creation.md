# Split Repo URL Update After Creation

Round: 370
Status: manual update procedure

## Purpose

This procedure defines how to update URLs after a split repository is manually
created. It does not create a repository, push a remote, deploy docs, or publish
a release.

## Preconditions

- A maintainer manually created the external child repository.
- The repository owner/name/visibility were approved.
- The copied file tree matches the reviewed `split_ready/` bundle.
- Privacy, safety, and release hygiene checks passed.
- The real URL was verified by a human.
- The main TuringResearch repository remains the flagship.

## Manual Update Steps

1. Replace `<approved-real-repository-url>` only in the matching manual pack.
2. Replace the flagship placeholder only after the canonical TuringResearch URL
   is approved.
3. Update child README backlink wording so it points readers back to the
   flagship above the fold.
4. Update flagship docs only after the child repository exists.
5. Add a ledger entry that records who approved the URL update.
6. Re-run split URL placeholder tests.
7. Re-run privacy/security checks.
8. Commit the URL update as a manual follow-up.

## Still Not Allowed

- Do not invent a URL before creation.
- Do not write fake URLs for future child repositories.
- Do not replace placeholders from CI.
- Do not use a placeholder as a real `git remote`.
- Do not make the child repository the canonical install path.
- Do not claim demo outputs or case metadata are observed research evidence.

## Main README Rule

The main README must describe split repositories as planned, manual-ready, or
created only if that state is true. Before creation, it may refer to local
manual packs, but it must not link to nonexistent child repository URLs.

## Child README Rule

Each child README must point back to the flagship TuringResearch repository. If
the real URL is not yet approved, it must keep the approved flagship
placeholder.

## Audit Trail

When a real URL is added later, the commit must update:

- the relevant `split_manual/<repo>/` files;
- the relevant docs report;
- `lanes/00_master_ledger.md`;
- any release or launch checklist that mentions the child repository.
