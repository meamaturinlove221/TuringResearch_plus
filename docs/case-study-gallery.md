# Case Study Gallery

Status: demo-only gallery.

Round: 224.

The Case Study Gallery organizes public-safe TuringResearch demo and case-study
entries so visitors can browse examples beyond one VGGT-like project.

The source manifest is:

- `examples/public_demo/case_gallery/gallery_manifest.yaml`

## Included Cases

- `vggt_public_safe_case`
- `robotics_paper_survey_demo`
- `medical_imaging_experiment_demo`
- `software_tooling_research_demo`
- `multimodal_model_eval_demo`

## Gallery Fields

Each case records:

- case id;
- domain;
- research type;
- demo status;
- privacy level;
- available artifacts;
- dashboard link;
- advisor pack link;
- limitations.

## Boundary

- Gallery entries are demo-only or public-safe case-study material.
- No gallery item claims experiment success.
- No gallery item includes raw data, private local paths, credentials, or
  private datasets.
- Child repositories are not implied by this gallery.
- Human review is required before any case is reused outside the demo.

## Validation

- `tests/unit/test_case_study_gallery.py`
- `tests/workflow/test_case_gallery_public_demo.py`
