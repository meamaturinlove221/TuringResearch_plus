# Round 279 - Vault Wiki Export Demo

Status: completed.

Scope:
- Add a public-safe vault/wiki/edge audit demo.
- Show wikilink export, backlinks, dangling links, missing edges, weak edges,
  requires-review nodes, and graph summary.
- Do not add a graph database or live sync.

Files:
- `examples/vault_wiki_demo/`
- `docs/vault-wiki-export-demo.md`
- `tests/workflow/test_vault_wiki_export_demo.py`

Safety:
- Fake/demo only.
- No private data.
- No raw data.
- No graph database.
- No Evidence Ledger mutation.
- No automatic truth inference.

Validation:
- Vault wiki demo tests, existing vault parity tests, privacy/security gate,
  name integrity, targeted sensitive scans, large-file checks, and whitespace
  checks were run for Round 279.

Push:
- Not pushed from this workspace because the target branch is absent locally and
  the worktree contains historical unrelated changes.
