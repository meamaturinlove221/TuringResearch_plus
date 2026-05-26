# TuringResearch Plus Upstream Baseline Schema

Each repository baseline records:

- `repository_full_name`
- `url`
- `default_branch`
- `latest_commit_sha`
- `latest_commit_message`
- `latest_commit_time`
- `root_files`
- `markdown_files`
- `skill_files`
- `docs_files`
- `package_files`
- `mcp_config_files`
- `src_files`
- `test_files`
- `file_hashes`
- `unresolved_reason`

Focused file hashes are limited to watch-relevant paths: README, ENTRY,
package config, MCP config, `.codex/`, `.agents/`, skills, `src/`, `docs/`,
`tests/`, `examples/`, Markdown, YAML, and YML.
