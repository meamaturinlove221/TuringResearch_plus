# Paper Digest Engine

Status: v0.4 minimal implementation.

The Paper Digest Engine expands the Scholar Pipeline three-pass reading template
into a reusable local report. It creates a `PaperDigest` from cached Markdown,
PDF Markdown, HTML summaries, manual notes, or fixture notes.

It does not download papers, copy long paper text, fabricate citations, or claim
that a paper has been fully read.

## Output

`PaperDigest` contains:

- `paper_id`
- `title`
- `source_status`
- `pass1_summary`
- `pass2_notes`
- `pass3_deep_notes`
- `method_contribution`
- `figures_to_inspect`
- `equations_to_inspect`
- `experiment_table_notes`
- `what_to_borrow`
- `what_not_to_copy`
- `collision_notes`
- `related_work_positioning`
- `requires_human_review`

## Three-Pass Expansion

- Pass 1: bird's-eye scan and relevance triage.
- Pass 2: method, representation, experiment, and VGGT mapping notes.
- Pass 3: deep mechanics, assumptions, collision questions, and missing evidence.

All three passes remain review scaffolding until a human checks the real paper.

## Method Card Bridge

`digest_to_method_card` converts a digest into a conservative `PaperMethodCard`
using the existing Paper-to-Method Card extractor. The resulting method card is
still `requires_human_review` and `requires-real-paper-review` for fixture notes.

## VGGT Use

The committed NeuralBody and HumanRAM digest fixtures are local testing examples.
They help organize:

- what to inspect in figures and tables;
- what to borrow as method vocabulary;
- what not to copy;
- collision notes for SMPL / SMPL-X, voxel, sparse, tri-plane, token, and geometry
  overlaps;
- related-work positioning notes.

They are not complete related-work review and do not establish final claims.

## Non-Goals

- No default networking.
- No paper download.
- No OCR-heavy pipeline.
- No long text reproduction.
- No fabricated citation.
- No automatic final paper writing.
