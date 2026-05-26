# Local-first Research Vault UI

Status: v0.7 minimal implementation.

Round 139 adds a static local-first vault UI for browsing vault graph review
artifacts. It does not create a server, login system, cloud service, graph
database, or truth inference engine.

## Inputs

- `VaultGraph` nodes and edges.
- Vault graph Markdown fixtures.
- Method taxonomy notes.
- Related work graph notes.
- Edge audit reports.

## Output

- `ResearchVaultUIBundle`
- `VaultGraphView`
- `VaultSearchEntry`
- standalone `index.html`

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

## VGGT Fixture

The VGGT fixture writes:

- `examples/vggt-human-prior-survey/vault_ui/index.html`

It reads only committed review artifacts from:

- `examples/vggt-human-prior-survey/vault_graph/`

The fixture keeps SparseConv3D success unproven and explicitly displays missing
edges and review-required nodes.

## Safety Boundary

- No server.
- No login.
- No network access.
- No complex graph database.
- No private VGGT path reads.
- Graph view is not final truth.
- Wikilinks are navigation aids, not proof.
- Human review remains required.

## Limitations

- The search index is embedded JSON for local tooling, not a remote search
  service.
- The graph is fixture/review material and can be incomplete.
- Missing source refs remain visible.
- The UI does not validate papers, artifacts, or experiment results.
