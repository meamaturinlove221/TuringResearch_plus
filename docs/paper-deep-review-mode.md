# Paper Deep Review Mode

Status: v0.7 minimal implementation.

Round 140 adds a deep review checklist mode on top of Paper Digest /
Three-pass Reading. It is for human review planning, not final paper writing.

## Inputs

- `PaperDigest`
- local manual notes or fixture notes
- method-card context
- related-work positioning context

## Output

`DeepReviewReport` contains:

- paper identity
- reading status
- figures to inspect
- equations to inspect
- tables to inspect
- implementation questions
- reproduction blockers
- relation to our project
- claims requiring verification
- notes for advisor
- `requires_human_review`

## VGGT Fixture

The NeuralBody fixture writes:

- `examples/vggt-human-prior-survey/paper_deep_review/neuralbody_review_checklist.md`

It is generated from local fixture notes and keeps:

- `source_status=fake-or-manual-note`
- `reading_status=needs-real-paper`
- reproduction blockers visible
- citation-grade use blocked until real paper review

## Safety Boundary

- No default networking.
- No PDF download.
- No long paper text copy.
- No fabricated equations.
- No final paper conclusion.
- No claim of completed real deep reading.
- Human review remains required.

## Use

Use deep review reports to decide which figures, formulas, tables, implementation
details, and reproduction blockers need manual paper review before related-work
or method claims are written.
