# Advisor Real PPTX Export

Status: feature capsule draft.

Release target: v0.7.

## 1. Problem

Advisor export can plan slides, but v0.7 may need an optional PPTX adapter that
keeps slide content evidence-linked and reviewable.

## 2. Research Motivating Example

An advisor meeting may need slides summarizing current state, blockers, and
next actions, but the deck must not invent charts or promote planned work.

## 3. Inputs

- AdvisorMarkdownBundle
- slide outline
- slide section mapping
- figure list
- evidence refs

## 4. Outputs

- AdvisorPPTXExportPlan
- AdvisorPPTXArtifactManifest
- PPTXExportSafetyReport

## 5. Proposed Commands / Tools

- command: `turing advisor export-pptx`
- tool: `advisor.export_pptx_optional`
- output: `AdvisorPPTXArtifactManifest`

## 6. Related Contracts

- advisor_real_pptx_export.yaml
- advisor_export.yaml

## 7. Related Skills

- turingresearch-paper-writing-pipeline
- turingresearch-qa-release

## 8. Required Tests

- slide mapping tests
- optional adapter tests
- no fabricated chart tests

## 9. Risks

- slides imply polished final claims
- generated visuals mislead reviewers
- converter dependency risk

## 10. Done Criteria

- PPTX export is optional
- slide mapping is evidence-linked
- missing evidence remains visible

## 11. Non-goals

- no default binary generation
- no generated charts without evidence
- no final paper or final presentation claims
