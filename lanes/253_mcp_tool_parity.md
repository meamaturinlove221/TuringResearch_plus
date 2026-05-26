# Round 275 - MCP Tool Parity

Status: completed.

Scope:
- Map v1.3 Scholar, Web, Session, Campaign, Vault, and Stress local tool
  surfaces into the MCP configuration story.
- Keep the mapping documentation-contract-only.
- Do not start a real MCP server or enable new runtime handlers.

Files:
- `docs/mcp-tool-parity-v1.3.md`
- `docs/mcp-tool-surface-v1.3.md`
- `.mcp.example.json`
- `tests/contract/test_mcp_tool_parity_v1_3.py`

Coverage:
- Scholar tools.
- Web tools.
- Apify optional.
- Session runtime fake tools.
- Campaign catalog.
- Vault tools.
- Stress test tools.

Safety:
- Fake mode remains default.
- Live mode remains disabled by default.
- Plugin tools remain disabled by default.
- Apify remains optional live only.
- No secrets, remote command execution, default networking, or automatic
  Evidence Ledger mutation was added.

Validation:
- MCP tool parity tests, MCP config tests, privacy/security gate, name
  integrity, targeted sensitive scans, large-file checks, and whitespace checks
  were run for Round 275.

Push:
- Not pushed from this workspace because the target branch is absent locally and
  the worktree contains historical unrelated changes.
