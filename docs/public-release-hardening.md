# Public Release Hardening

Status: v0.5 beta planning / hardening.

Round 101 establishes the public release hygiene checklist for TuringResearch
Plus. It does not publish the package, create a tag, or push a release.

## Required Gates

- Full tests pass on a clean branch.
- `python -m mypy src` passes.
- Name integrity passes.
- Secret scan policy passes.
- Public examples are demo-safe.
- README accurately describes fake/default behavior and limitations.
- License status is clear.
- SECURITY, CONTRIBUTING, and Code of Conduct are present.
- Issue and pull request templates warn against secrets and private data.

## Repository Hygiene

Do not commit:

- `.env`
- real API keys or tokens
- `local_project_links.yaml`
- raw data
- private model files
- huge `npz` payloads
- private papers or restricted datasets

## Release Boundary

v0.5 alpha/beta artifacts are local, fake/default, review-first workflows.
They must not be described as a PyPI release, a full SaaS UI, automatic
experiment execution, or automatic paper writing.
