# TulingResearch Plus Security Policy

## Supported Versions

`v0.1.0` is a release candidate for local, fake-mode, and dry-run workflows.

## Reporting Security Issues

Do not open public issues containing secrets, private data, private papers, restricted datasets, or exploit details. Use a private maintainer contact channel when available.

## Secrets Policy

Do not commit:

- API keys.
- Access tokens.
- Private SSH keys.
- Service account credentials.
- `.env` files with real values.
- Private papers or restricted datasets.

Use `.env.example` for variable names only.

## Source Hygiene Gate

TulingResearch Plus blocks implementation work from:

- Private repository content.
- Leaked roadmap material.
- NDA content.
- Proprietary code.
- Copied implementation details from incompatible licenses.
- Private papers or restricted datasets without explicit authorization.

Allowed sources include public repositories, public README files, public issues, public release notes, user-owned notes, and authorized transcripts.

## Default Safety Boundary

Default tests and examples do not require live network access, real API keys, LLM provider credentials, cloud credentials, or GPU services.
