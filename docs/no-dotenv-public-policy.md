# No `.env` Public Policy

Round: 360.5
Status: policy locked

## Rule

Do not commit `.env` files. The repository may include `.env.example` with
variable names only, but committed examples must not contain real values.

## Why

`.env` files often contain provider keys, API tokens, SSH/SFTP targets, private
paths, or local machine details. Public release surfaces must not expose those
values.

## Allowed

- `.env.example` with blank values.
- `.mcp.example.json` with blank credential placeholders.
- Documentation that explains which private env variables a user may set
  locally.

## Forbidden

- real API keys;
- real tokens;
- private SSH keys;
- passwords;
- cookies;
- private local paths;
- raw data paths;
- enabled live flags in committed public templates.

## Live Mode

Live mode belongs in private local environment variables only. It must require
explicit env, and it must remain skipped by default in the public test suite.
