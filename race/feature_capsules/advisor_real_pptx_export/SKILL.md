# Advisor Real PPTX Export Skill

Status: planning skill draft.

Use this skill for optional advisor PPTX export planning. It does not generate
charts or final claims from missing evidence.

## Inputs

- AdvisorMarkdownBundle
- slide outline
- slide section mapping
- figure list
- evidence refs

## Outputs

- AdvisorPPTXExportPlan
- AdvisorPPTXArtifactManifest
- PPTXExportSafetyReport

## Safety Rules

- Do not generate binary PPTX by default.
- Do not fabricate charts or result values.
- Keep missing evidence visible.
- Require human review.

## Related Contracts

- advisor_real_pptx_export.yaml
- advisor_export.yaml
