# VGGT Human Prior Dogfooding Case Study Draft

Status: public-safe draft / requires human review
Round: Optional 338.5 integrated on newer cloud baseline
Published: false
Public demo only: true

## Safety Notice

This draft is documentation-only. It does not include source datasets, SMPL-X model files, private machine paths, huge artifacts, experiment archives, or copied VGGT outputs.

## Problem Background

The VGGT dogfooding line explored how human-prior structure could be organized for a future VGGT-side experiment. The safest public framing is the North Star shift from direct SMPL-X replacement to SMPL-X feature encoding for VGGT.

This draft is public-demo material and not a final research result.

## Why TuringResearch Was Useful

TuringResearch organized evidence states, artifacts, visual readiness, routes, related work, advisor notes, and public communication boundaries into reviewable artifacts.

It kept planned routes separate from observed engineering context and made missing evidence visible before public-facing writing.

## Route Changes

- The route changed away from direct replacement toward feature encoding and hard-gated experiment planning.
- V260 remains hard-blocked.
- Modal SparseConv3D remains planned / requires-real-experiment.
- V999-SparseConv3D remains not-enough-evidence.

## Evidence Management

- Evidence buckets distinguish observed engineering context, local-observed context, planned routes, hard-blocked states, and not-enough-evidence states.
- Local scan metadata can inform public-safe writing, but local-only evidence does not become public observed evidence without review.
- No workspace index or dashboard display is treated as evidence by itself.

## Failures And Blockers

- Failure taxonomy records missing assets, fallback-only paths, insufficient visual proof, and not-enough-evidence states.
- Sparse backend proof, visual readiness, and public-release approval remain guarded.
- Failures are presented as research learning, not as successful results.

## Advisor Pack

- Advisor material can state what is organized, what is missing, and what should be run next.
- Advisor-ready visual proof still requires human review.
- The recommended advisor ask is whether the planned route and hard gates are acceptable before larger experiment investment.

## What Remains Human Work

- Run real VGGT-side or Modal-side experiments outside this public case study draft.
- Review papers manually before final related-work wording.
- Interpret failures and approve final claims.
- Review privacy, license, and publication boundaries before release.

## What Not To Claim

- Do not claim SparseConv3D success.
- Do not describe planned routes as executed or observed.
- Do not claim final paper conclusions.
- Do not include private local paths, restricted datasets, model files, non-public advisor notes, or non-public artifacts.

## Safety Boundary

- This case study is not a publication.
- It does not claim experiment success.
- It does not claim SparseConv3D success.
- It does not include private local paths, restricted datasets, model files, or non-public advisor notes.
- Human review is required before release.
