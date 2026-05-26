# Paper Deep Review Mode Skill

Status: planning skill draft.

Use this skill for citation-grade paper review planning. It does not generate
camera-ready related-work text or fabricate citations.

## Inputs

- PaperDigest
- PaperMethodCard
- RelatedWorkPositioningReport
- CitationSafetyReport
- CollisionRiskReport

## Outputs

- PaperDeepReviewReport
- CitationGradeChecklist
- RelatedWorkReviewDecision

## Safety Rules

- Require source status for every citation.
- Do not treat fake fixtures as citation-grade.
- Do not bypass paywalls.
- Require human review.

## Related Contracts

- paper_deep_review_mode.yaml
- paper_digest.yaml
- related_work_draft.yaml
