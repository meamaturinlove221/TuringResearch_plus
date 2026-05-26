# Local-first Research Vault UI Skill

Status: planning skill draft.

Use this skill for local vault UI planning. It keeps generated views local and
does not upload private research data.

## Inputs

- workspace overview
- vault graph
- evidence summaries
- paper assembly report
- dashboard bundle

## Outputs

- ResearchVaultUIBundle
- VaultNavigationIndex
- VaultUISafetyReport

## Safety Rules

- Do not upload data.
- Do not require network access.
- Do not leak private paths.
- Do not treat vault or ontology graph as final truth.

## Related Contracts

- local_first_research_vault_ui.yaml
- vault_graph.yaml
- multi_project_workspace.yaml
