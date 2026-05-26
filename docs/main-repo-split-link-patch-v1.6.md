# Main Repo Split Link Patch v1.6

Round: 371
Status: complete

## Objective

Update the main repository README and split docs so external readers understand
that split repositories are planned / manual-ready only. This round does not
write real child repository URLs, create repositories, push remotes, publish
releases, or change install targets.

## Files Updated

- `README.md`
- `docs/future-split-repos.md`
- `docs/split-manual-packs.md`

## Split Status

| Planned split repo | Status | Role | URL state |
| --- | --- | --- | --- |
| `turingresearch-vggt-case` | planned / manual-ready | public-safe case/demo spoke | placeholder only |
| `turingresearch-examples` | planned / manual-ready | demo-only examples spoke | placeholder only |
| `turingresearch-plugins` | deferred | plugin policy/registry draft | no public URL |

## Main Repository Boundary

The main TuringResearch repository remains the only install, quickstart, public
API, release, roadmap, docs, issue triage, and star entry.

Future split repositories are optional case/demo spokes. They must not replace
the flagship install path and must not disperse star focus away from the
flagship.

## URL Boundary

- No fake GitHub URL is written.
- No real child repository URL is written before creation.
- Existing docs point to local `split_ready/` and `split_manual/` materials.
- Child README files must keep a flagship placeholder until a real URL is
  approved.
- Real URL updates require the manual process in
  [`split-repo-url-update-after-creation.md`](split-repo-url-update-after-creation.md).

## Reader-facing Summary

The README now describes planned split repositories as local manual-ready packs
only. It also links the URL placeholder policy so future maintainers know that
external child links are blocked until human creation and approval.

## Validation

- Docs deployment preflight/gate tests passed with 11 tests.
- URL placeholder tests passed with 6 tests.
- Privacy/release hygiene tests passed with 18 tests.
- `python -m ruff check .` passed.
- `git diff --check` passed.
