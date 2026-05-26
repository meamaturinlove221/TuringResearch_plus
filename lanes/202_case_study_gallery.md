# Lane 202 - Case Study Gallery

Status: completed.

Round: 224.

## Goal

Create a public-safe case study gallery for the VGGT dogfooding case and the
new v1.1 public demo cases.

## Outputs

- `docs/case-study-gallery.md`
- `docs-site/pages/case-study-gallery.md`
- `examples/public_demo/case_gallery/gallery_manifest.yaml`
- `src/turing_research_plus/case_study/gallery.py`
- `tests/unit/test_case_study_gallery.py`
- `tests/workflow/test_case_gallery_public_demo.py`

## Gallery Fields

- case id
- domain
- research type
- demo status
- privacy level
- available artifacts
- dashboard link
- advisor pack link
- limitations

## Safety

- Demo-only or public-safe case material only.
- No external child repository URLs.
- No private data, raw data, credentials, or private paths.
- No experiment success claim.
- Human review required.
