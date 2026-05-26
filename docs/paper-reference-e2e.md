# Paper Reference E2E

Status: fake/default workflow.

Round: 303.

This document describes the v1.4 `paper_reference` E2E path:

```text
paper metadata
-> scholar.paper_reference
-> references / citations review seed
-> related-work seed
-> collision matrix input
```

The goal is to make paper reference handling feel like a runnable production
surface while keeping public demos safe and fake-first.

## Inputs

- `paper_id`: stable paper identifier.
- `title`: paper title used for report display.
- `url`: public URL string used as context only.

## E2E Steps

1. Run `scholar.paper_reference` with a fake/default paper id.
2. Resolve fake/default references through the existing adapter boundary.
3. Resolve fake/default citations as review context.
4. Convert references and citations into a related-work seed.
5. Build a conservative collision matrix input.
6. Keep downstream reports human-reviewed and proposed-only.

## Demo Fixture

The public demo lives under:

```text
examples/scholar_demo/paper_reference_e2e/
```

It contains paper metadata, related-work seed data, collision matrix input, and
a short E2E report.

## Safety Boundary

- fake/default workflow only;
- no API key required;
- no live provider required;
- no automatic full paper download;
- no paywall bypass;
- no fake citation is marked as verified;
- no final novelty claim;
- no final collision claim;
- human review required.

## Validation

Run:

```powershell
python -m pytest tests/workflow/test_paper_reference_e2e_fake.py -q
```
