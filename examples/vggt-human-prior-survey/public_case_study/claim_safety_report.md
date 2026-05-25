# VGGT Case Study Claim Safety Report

Status: public-safe draft / requires human review
Round: Optional 338.5 integrated on newer cloud baseline

## Claim Inventory

| Claim area | Status | Allowed wording | Blocked wording |
| --- | --- | --- | --- |
| Case-study workflow | observed | "TuringResearch Plus organized a public-safe case-study draft." | "The public case proves the VGGT result." |
| VGGT work-stream evidence | local-observed | "File-level evidence exists for selected work streams." | "The experiments were rerun and validated." |
| Visual evidence | local-observed | "Visual evidence metadata exists and needs review." | "The advisor-ready visual package is accepted." |
| V120/V121 | requires-human-review | "Goal manifests and tool evidence need review." | "SparseConv3D success is confirmed." |
| V900/V930/V999 | local-observed | "Reports and controller evidence exist." | "Promotion is approved." |
| Public split package | requires-human-review | "The split case is a draft awaiting review." | "The split package is release-ready." |

## Guardrails

- No claim may be upgraded from `local-observed` to `observed` without a reviewed public-safe evidence source.
- No claim may state SparseConv3D success unless a reviewed evidence item explicitly supports it.
- No claim may state advisor approval or promotion.
- No claim may include private paths, raw data identifiers, SMPL-X model-file details, or huge artifact filenames.

## Current Decision

The case study is safe as a draft and unsafe as a final public release. The next action is human review, not automatic promotion.
