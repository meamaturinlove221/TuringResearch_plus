# TuringResearch Plus Security Policy

## Supported Versions

`v0.5.0a0` is an alpha release-preparation state for local, fake-mode, and
dry-run workflows. It is not published to PyPI by this repository workflow.

## Reporting Security Issues

Do not open public issues containing secrets, private data, private papers, restricted datasets, or exploit details. Use a private maintainer contact channel when available.

## Secrets Policy

Do not commit:

- API keys.
- Access tokens.
- Private SSH keys.
- Service account credentials.
- `.env` files with real values.
- `local_project_links.yaml`.
- Private papers or restricted datasets.
- Raw data.
- Private model files.
- Huge binary experiment payloads.

Use `.env.example` for variable names only.

## Source Hygiene Gate

TuringResearch Plus blocks implementation work from:

- Private repository content.
- Leaked roadmap material.
- NDA content.
- Proprietary code.
- Copied implementation details from incompatible licenses.
- Private papers or restricted datasets without explicit authorization.

Allowed sources include public repositories, public README files, public issues, public release notes, user-owned notes, and authorized transcripts.

## Default Safety Boundary

Default tests and examples do not require live network access, real API keys, LLM provider credentials, cloud credentials, or GPU services.

Live adapters must remain opt-in and disabled by default. Retrieved material is
not automatically human-verified evidence.
