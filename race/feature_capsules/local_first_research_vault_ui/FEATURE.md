# Local-first Research Vault UI

Status: feature capsule draft.

Release target: v0.7.

## 1. Problem

Researchers need a local way to browse workspace, vault graph, evidence, paper,
dashboard, and replay material without uploading private data.

## 2. Research Motivating Example

A lab can inspect multiple research cases and evidence gaps from local static
views while keeping private artifacts on the machine.

## 3. Inputs

- workspace overview
- vault graph
- evidence summaries
- paper assembly report
- dashboard bundle

## 4. Outputs

- ResearchVaultUIBundle
- VaultNavigationIndex
- VaultUISafetyReport

## 5. Proposed Commands / Tools

- command: `turing vault ui-build`
- tool: `vault.ui_build_local`
- output: `ResearchVaultUIBundle`

## 6. Related Contracts

- local_first_research_vault_ui.yaml
- vault_graph.yaml
- multi_project_workspace.yaml

## 7. Related Skills

- turingresearch-fusion-wiki-vault
- turingresearch-qa-release

## 8. Required Tests

- static local UI bundle tests
- no upload tests
- privacy boundary tests

## 9. Risks

- UI scope creeps into hosted product
- private paths leak into generated pages
- graph view implies final truth

## 10. Done Criteria

- UI remains local-first
- generated pages are privacy-gated
- ontology/vault graphs remain review material

## 11. Non-goals

- no SaaS
- no login
- no cloud deployment
