# TuringResearch Plus Public Repo Hygiene

Round 28 prepares TuringResearch Plus for public GitHub repository presentation without adding business features.

## Added Repository Files

- `LICENSE`
- `NOTICE.md`
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- `.gitignore`
- `.env.example`
- `.github/ISSUE_TEMPLATE/bug_report.md`
- `.github/ISSUE_TEMPLATE/feature_request.md`
- `.github/ISSUE_TEMPLATE/research_workflow_request.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `docs/source-hygiene-policy.md`
- `docs/license-decision-needed.md`

## License Status

`pyproject.toml` currently declares `license = { text = "Proprietary" }`. The `LICENSE` file matches that metadata. A public open source license has not been selected. Any license change requires explicit maintainer review and synchronized updates.

## Secret Hygiene

`.gitignore` excludes:

- `.env`
- `.cache/`
- `__pycache__/`
- `.pytest_cache/`
- `.mypy_cache/`
- `.ruff_cache/`
- `dist/`
- `build/`
- `*.egg-info/`
- `private_data/`
- `secrets/`
- `*.pem`
- `*.key`

`.env.example` contains variable names only and no real tokens.

## Issue And PR Hygiene

Issue templates ask reporters to avoid secrets, private papers, restricted datasets, private repository content, leaked roadmaps, NDA material, proprietary code, and incompatible-license implementation details.

The pull request template requires:

- Source Hygiene confirmation.
- Contract and public API impact declaration.
- Test commands.
- Documentation impact.

## Release Safety

No business feature or public API change was introduced. This round only added repository metadata, policy files, templates, and hygiene documentation.

## Validation

Run:

```powershell
python -m pytest tests/contract/test_name_integrity.py
python -m pytest tests/contract/test_skills_integrity.py
```
