# Paper Deep Review Mode

Status: feature capsule draft.

Release target: v0.7.

## 1. Problem

Paper digest and related-work scaffolds need a deeper review mode that tracks
citation-grade source status without pretending fake fixtures are full paper
reading.

## 2. Research Motivating Example

Before a related-work section can become camera-ready, each citation candidate
must have source status, notes, limitations, and human review.

## 3. Inputs

- PaperDigest
- PaperMethodCard
- RelatedWorkPositioningReport
- CitationSafetyReport
- CollisionRiskReport

## 4. Outputs

- PaperDeepReviewReport
- CitationGradeChecklist
- RelatedWorkReviewDecision

## 5. Proposed Commands / Tools

- command: `turing paper deep-review`
- tool: `paper.deep_review`
- output: `PaperDeepReviewReport`

## 6. Related Contracts

- paper_deep_review_mode.yaml
- paper_digest.yaml
- related_work_draft.yaml

## 7. Related Skills

- turingresearch-paper-writing-pipeline
- turingresearch-fusion-literature-survey

## 8. Required Tests

- citation-grade checklist tests
- fake fixture rejection tests
- requires-human-review tests

## 9. Risks

- fake digest treated as citation
- incomplete paper reading overclaimed
- unsafe related-work claims

## 10. Done Criteria

- every citation candidate has source status
- fake fixtures are blocked as citation-grade sources
- human review remains required

## 11. Non-goals

- no automatic final related-work prose
- no citation fabrication
- no paywall bypass
