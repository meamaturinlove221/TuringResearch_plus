# Future Paper Writing Assistant

Status: future planning.

Round: 102.

TuringResearch Plus can support paper writing, but it should not become an
automatic paper author. Future writing support must preserve citation,
evidence, and human review boundaries.

## Current Baseline

Existing components already provide paper-adjacent review material:

- Scholar pipeline refinement.
- Paper digest and three-pass reading scaffold.
- Paper method card bridge.
- Citation graph expansion.
- Collision risk detector.
- Related work positioning.
- Advisor bundle and export plans.
- Research knowledge pack.

These outputs are review scaffolds. They are not final paper text.

## Future Capabilities

| Capability | Horizon | Output | Human review |
| --- | --- | --- | --- |
| Paper outline generator | near-term | section outline | required |
| Related-work paragraph planner | near-term | bullet plan, not final prose | required |
| Claim-evidence checker | near-term | unsupported claim list | required |
| Figure/table narrative planner | mid-term | caption and discussion notes | required |
| Method section scaffold | mid-term | structured draft notes | required |
| Revision response assistant | long-term | response plan | required |

## Writing Rules

- Do not generate final paper conclusions automatically.
- Do not fabricate citations.
- Do not copy long copyrighted text.
- Do not treat fake fixtures as real reading.
- Do not mark generated text as advisor-approved.
- Preserve limitations and missing evidence.
- Keep every generated section linked to source refs where possible.

## Privacy / License Risks

- Paper drafts can leak private results or private dataset details.
- Generated text can accidentally reproduce copyrighted passages.
- Public paper material can expose unreleased model or project details.
- Citation metadata can be incomplete or stale.

## Cannot Be Automated

- Final authorship.
- Final claim approval.
- Novelty judgment.
- Ethical and license review.
- Decision to submit.
- Interpretation of ambiguous experimental results.

## v0.6 Recommendation

Focus on outlines, claim checks, and structured writing plans. Defer final prose
generation until citation, evidence, and human review gates are stronger.
