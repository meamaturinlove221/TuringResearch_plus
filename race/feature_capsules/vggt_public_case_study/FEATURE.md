# VGGT Public Case Study Builder

Status: feature capsule draft.

Release target: v0.7.

## 1. Problem

The VGGT dogfooding case should be explainable publicly without exposing private
data or claiming unsupported experiment success.

## 2. Research Motivating Example

A public case study can show how TuringResearch helped organize evidence,
routes, failures, advisor communication, and paper blockers while clearly
stating what remains unresolved.

## 3. Inputs

- VGGT research knowledge pack
- dogfooding replay
- route DSL
- advisor pack
- paper assembly gate
- privacy scan report

## 4. Outputs

- VGGTCaseStudyOutline
- VGGTCaseStudyEvidenceMap
- VGGTCaseStudySafetyReport

## 5. Proposed Commands / Tools

- command: `turing case-study vggt-build`
- tool: `case_study.vggt_build`
- output: `VGGTCaseStudyOutline`

## 6. Related Contracts

- vggt_public_case_study.yaml
- vggt_evidence.yaml
- paper_writing_scaffold.yaml

## 7. Related Skills

- turingresearch-master-orchestrator
- turingresearch-qa-release

## 8. Required Tests

- evidence map tests
- no private path tests
- no SparseConv3D success claim tests

## 9. Risks

- public case study overclaims experiment progress
- private VGGT paths leak
- planned routes become observed results

## 10. Done Criteria

- case study outline is evidence-linked
- missing evidence is explicit
- unsupported success claims are blocked

## 11. Non-goals

- no VGGT experiment execution
- no private artifact packaging
- no final paper conclusion
