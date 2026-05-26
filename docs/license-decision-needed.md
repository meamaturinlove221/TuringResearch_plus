# TuringResearch Plus License Decision Needed

The current project metadata declares a proprietary license:

```toml
license = { text = "Proprietary" }
```

Round 28 created a `LICENSE` file that matches this existing metadata. If TuringResearch Plus should be released publicly under an open source license, maintainers must make an explicit license decision before publication.

## Required Updates For A License Change

- `LICENSE`
- `pyproject.toml`
- `docs/license-review.md`
- `docs/public-release-checklist.md`
- `README.md`
- release notes

## Review Points

- Dependency license compatibility.
- Public reference material usage.
- Contributor license expectations.
- Whether examples and generated artifacts can be distributed.
- Whether any private or restricted source material exists in the repository.
