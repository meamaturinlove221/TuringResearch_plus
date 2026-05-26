---
name: turingresearch-paper-to-method-card
description: Use when planning or implementing Sprint 2 paper-to-method-card extraction.
---

# TuringResearch Plus Skill: paper_to_method_card

## Role

Maintain provenance-backed Method Card extraction from paper metadata and PDF
Phase B outputs.

## When to use

Use when a task touches method cards, paper provenance, PDF asset references, or
method architecture cues.

## Inputs

- Paper metadata.
- PDF Phase B reports.
- EvidenceRefs.
- Hard Gate results.

## Outputs

- `PaperMethodCard`
- method component summary
- method limitations

## Required files

- `race/feature_capsules/paper_to_method_card/FEATURE.md`
- `race/feature_capsules/paper_to_method_card/contract.yaml`
- `race/feature_capsules/paper_to_method_card/sop.mmd`
- `race/feature_capsules/paper_to_method_card/test_plan.md`

## Related contracts

- `contracts/method_cards.yaml`
- `contracts/pdf_markdown.yaml`
- `contracts/paper_pipeline.yaml`

## Related lanes

- `lanes/25_v0.2_sprint_2_scope.md`
- `lanes/26_v0.2_sprint_2_feature_capsules.md`

## Required tests

- metadata validation
- EvidenceRef requirement
- missing real paper fallback
- no fabricated method component

## Rules / constraints

- Do not copy copyrighted paper text.
- Do not infer method details from missing inputs.
- Do not require network.

## Done criteria

- Method Cards can feed Figure-to-Architecture and Advisor Pack summaries.
