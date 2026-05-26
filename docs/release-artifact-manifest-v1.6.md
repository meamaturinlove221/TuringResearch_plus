# Release Artifact Manifest v1.6

Round: 380
Status: local manifest

## Manifest Policy

Release artifacts are local-only until a human maintainer approves a release
action. This manifest records what was built or skipped during Round 380. It is
not a publication record.

## Artifacts

| id | type | status | path | size_bytes | sha256 | notes |
| --- | --- | --- | --- | ---: | --- | --- |
| wheel-v1.6-local | wheel | built-local | `dist/turingresearch_plus-1.5.0rc0-py3-none-any.whl` | 745087 | `012b7b289386b5c2eae4e059c990ae8af56e16d5b983f32eada6e7ab318bc744` | Local wheel produced by `python -m pip wheel --no-deps --no-build-isolation -w dist .`. |
| sdist-v1.6-local | sdist | skipped | n/a | 0 | n/a | Graceful skip: `python -m build` is unavailable in this environment and no network install was attempted. |

## Wheel Contents Summary

- zip_entries: `666`
- includes Python packages under `turing_research*`
- includes package metadata under `turingresearch_plus-1.5.0rc0.dist-info/`
- excludes `docs-site/`
- excludes raw data
- excludes private data
- excludes `.env`
- excludes SMPL-X files

## Git Tracking

- `dist/` is ignored by `.gitignore`.
- The wheel is a local generated artifact.
- The wheel is not committed.
- This manifest and the build report are committed for release review.

## Safety Assertions

- no secrets;
- no API keys;
- no raw data;
- no private paths;
- no SMPL-X model files;
- no docs-site private data;
- no fake publication URL;
- no PyPI publish;
- no GitHub release publish.

## Rebuild Guidance

To rebuild the local wheel:

```powershell
python -m pip wheel --no-deps --no-build-isolation -w dist .
```

To build both wheel and sdist in a prepared release environment:

```powershell
python -m build
```

If `python -m build` is unavailable, record the skipped reason rather than
installing new tooling during the release gate.
