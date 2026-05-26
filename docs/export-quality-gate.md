# Export Quality Gate

Status: v0.7 minimal implementation.

Round 136 adds a local quality gate for Advisor Markdown, optional PDF,
optional PPTX, and dashboard exports. It does not add a new export format and
does not run converters. It only checks existing outputs and reports findings.

## Inputs

- Advisor export directory.
- Optional dashboard output paths.
- Required output list, or the default VGGT Advisor export output set.

## Checks

- no unsafe claims
- no planned-as-observed wording
- no missing evidence refs
- no fake result marked observed
- no broken figure refs
- no missing limitations
- no old project naming
- no secret-like values
- output files exist or skipped reason is recorded

## Status Values

- `pass`: no errors, no skipped binary outputs.
- `pass-with-warnings`: no errors, but optional PDF/PPTX outputs were skipped
  with reasons or non-blocking warnings exist.
- `fail`: at least one blocking finding exists.

## VGGT Fixture

The VGGT Advisor export fixture records skipped PDF and PPTX outputs because
the optional local backends are not default dependencies. This is acceptable
when each skipped output records a skipped reason and the Markdown review
source exists.

## Safety Boundary

- No network access.
- No file deletion.
- No new export format generation.
- No fake figures or result values.
- No planned work written as observed.
- No private VGGT path reads.
- Human review remains required before advisor delivery.
