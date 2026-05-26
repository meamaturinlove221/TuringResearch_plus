# TuringResearch Plus Example: PDF to Markdown Demo

Mode: local fixture dry run.

This example demonstrates Phase A local PDF to Markdown conversion with a generated tiny fixture PDF.

## Expected Artifacts

- PDFMarkdownOutput
- markdown artifact
- quality report
- cache hit test

## Inputs

- `input/request.json` defines the fixture title and local output paths used by the dry-run test.
- `fake_run_config.yaml` fixes local fixture mode and no-network execution.

## Outputs

- `expected_outputs/artifact_list.json` lists required PDF artifacts.
- `expected_outputs/expected_summary.md` documents expected conversion, quality, and cache-hit behavior.

No real network access, real API key, external OCR service, or large PDF file is required.
