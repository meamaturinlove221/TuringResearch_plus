# Lane 120: Local-first Research Vault UI

Round: 139

Status: implemented minimal.

## Goal

Add a local-first static research vault UI for browsing vault graph, method
taxonomy, related work, evidence nodes, missing edges, and review markers.

## Implemented

- `src/turing_research_plus/vault_ui/`
- `contracts/local_research_vault_ui.yaml`
- `docs/local-first-research-vault-ui.md`
- `examples/vggt-human-prior-survey/vault_ui/index.html`
- Vault UI unit and workflow tests.

## Required Views

- concept nodes
- paper nodes
- method nodes
- artifact nodes
- claim nodes
- failure nodes
- route nodes
- missing edges
- requires review nodes
- optional wikilinks

## Boundaries

- No server.
- No login.
- No network access.
- No graph database.
- No private VGGT path reads.
- Graph view is not final truth.
- SparseConv3D success is not claimed.
- Human review remains required.

## Validation

- `tests/unit/test_vault_ui_models.py`
- `tests/unit/test_static_vault_ui.py`
- `tests/unit/test_vault_graph_view.py`
- `tests/unit/test_vault_search_index.py`
- `tests/workflow/test_vggt_vault_ui_fake.py`
