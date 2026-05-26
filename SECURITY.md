# TuringResearch Security Policy

## Supported Status

TuringResearch is currently in release-candidate preparation for local,
fake/default, dry-run, and public-demo workflows. The repository does not
publish PyPI packages, GitHub releases, or hosted services automatically.

## Reporting Security Issues

Do not open public issues containing secrets, private data, private papers,
restricted datasets, exploit details, credentials, or private local paths. Use a
private maintainer contact channel when available.

If a private channel is not available, open a public issue with only a minimal
non-sensitive description and ask maintainers for a private reporting path.

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

TuringResearch blocks implementation work from:

- private repository content;
- leaked roadmap material;
- NDA content;
- proprietary code;
- copied implementation details from incompatible licenses;
- private papers or restricted datasets without explicit authorization.

Allowed sources include public repositories, public README files, public issues,
public release notes, user-owned notes, and authorized transcripts. Any code
reuse still requires license review before copying or adapting implementation
material.

## Default Safety Boundary

Default tests and examples do not require live network access, real API keys,
LLM provider credentials, cloud credentials, GPU services, SSH, SFTP, or remote
execution.

Live adapters must remain opt-in and disabled by default. Retrieved material is
not automatically human-verified evidence and must not be promoted to observed
claims without review.
