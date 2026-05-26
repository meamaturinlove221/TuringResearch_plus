# TuringResearch Plus Skill Entry

Status: active routing entry.

Use this file when choosing a repo-scoped `turingresearch-*` skill for a task.
This entry point recommends skills only; it does not execute tools, start
agents, or change files by itself.

## Default Rule

If no specific route matches, use:

- `turingresearch-master-orchestrator`

## Fast Routes

- Upstream watch: `turingresearch-race-upstream-watch`
- Campaign catalog: `turingresearch-fusion-campaign-engine`
- Scholar pipeline: `turingresearch-fusion-literature-survey`
- Web fetch: `turingresearch-core-reproduction`
- Pod workflow: `turingresearch-fusion-context-management`
- VGGT dogfooding: `turingresearch-master-orchestrator`
- Evidence ledger: `turingresearch-cache-and-ledger`
- Artifact audit: `turingresearch-cache-and-ledger`
- Visual audit: `turingresearch-master-orchestrator`
- Advisor pack: `turingresearch-paper-writing-pipeline`
- PDF extraction: `turingresearch-pdf-markdown-core`
- Route DSL / hard gates: `turingresearch-fusion-experiment-execution`
- Failure taxonomy: `turingresearch-fusion-stress-test`
- Paper method / related work: `turingresearch-paper-writing-pipeline`
- Figure architecture: `turingresearch-paper-figure-asset-pipeline`
- Citation graph: `turingresearch-fusion-semantic-graph`
- Web fetch / Apify: `turingresearch-core-reproduction`
- Handoff / pod workflow: `turingresearch-fusion-context-management`
- Vault graph / ontology: `turingresearch-fusion-wiki-vault`

## SOP Parity Fields

Priority workflow skills should include a `Round 240 SOP Parity` section with:

- `when_to_use`
- `inputs`
- `outputs`
- `safety`
- `non-goals`
- `handoff`
- `tests`
- `related_docs`

## Safety

- Routing is recommendation only.
- Do not run live network tools unless the round explicitly allows it.
- Do not read private VGGT paths unless the round explicitly runs on the VGGT
  computer.
- Do not convert planned work into observed evidence.
- Do not claim SparseConv3D success without evidence-ledger proof.
