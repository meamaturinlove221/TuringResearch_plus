# Secret Scan Policy

Status: active.

## Scope

Secret scanning applies to source code, docs, contracts, examples, lanes,
GitHub templates, and configuration examples.

## Forbidden In Repo

- `.env` with real values
- API keys
- access tokens
- private SSH keys
- provider credentials
- `local_project_links.yaml`
- private project paths
- raw data
- private model files
- huge `npz` payloads

## Allowed Placeholders

- blank variables in `.env.example`
- blank variables in `.mcp.example.json`
- safety-policy text that says secrets must not be committed

## Suggested Patterns

- token-like provider keys
- private key headers
- private local path markers
- private model file names
- large binary data extensions

Any match must be reviewed before release.
