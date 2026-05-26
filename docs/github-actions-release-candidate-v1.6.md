# GitHub Actions Release Candidate v1.6

Round: 381
Status: configured for release-candidate checks

## Objective

Round 381 strengthens GitHub Actions so TuringResearch can run v1.6 release
candidate checks on push and pull request events. It does not publish to PyPI,
create a GitHub release, upload release artifacts, or run live tests.

## Workflows

| Workflow | Purpose | Release boundary |
| --- | --- | --- |
| `.github/workflows/ci.yml` | Unit, contract, package metadata, install smoke, release manifest, name integrity, and privacy checks. | No publish, no live tests. |
| `.github/workflows/docs-check.yml` | Docs build hardening, deployment preflight, deployment dry-run, release bundle dry-run, public docs hygiene. | Docs build dry-run only. |
| `.github/workflows/privacy-gate.yml` | Privacy, public release hygiene, split bundle safety, and release artifact manifest safety. | No secrets, no private data upload. |
| `.github/workflows/release-artifact-dry-run.yml` | Build local wheel dry-run and run artifact/install smoke checks. | No artifact upload, no PyPI publish, no GitHub release publish. |

## Default Environment

All release-candidate workflows set fake/default live guards:

```yaml
TURINGRESEARCH_MODE: "fake"
TURINGRESEARCH_ENABLE_LIVE_TESTS: "0"
TURINGRESEARCH_ENABLE_WEB_LIVE: "0"
TURINGRESEARCH_ENABLE_APIFY_LIVE: "0"
TURINGRESEARCH_ENABLE_SFTP_LIVE: "0"
```

The workflows do not require API keys or repository secrets.

## Release Artifact Dry-run

The release artifact workflow runs:

```powershell
python -m pip wheel --no-deps --no-build-isolation -w dist .
python -m pytest tests/workflow/test_release_artifact_manifest.py -q
python -m pytest tests/workflow/test_install_smoke_fake.py -q
```

If the `build` frontend is unavailable, the workflow records an sdist skip file
instead of installing tooling or publishing anything.

If the `build` frontend is available, the workflow uses `--no-isolation` for
sdist dry-run generation so the release-candidate check does not fetch build
dependencies from the network.

## Non-actions

- No PyPI publish.
- No TestPyPI publish.
- No GitHub release publish.
- No tag creation.
- No release artifact upload.
- No workflow secrets.
- No live tests.
- No default networking.
- No VGGT access.
- No private data upload.

## Manual Release Boundary

Human maintainers must still review package metadata, license status, release
notes, artifacts, and publication instructions before any real release action.
These workflows are release-candidate checks, not release automation.
