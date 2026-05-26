# Quickstart

Status: public-safe review path / no install required.

This bundle is a future split-repository export candidate. It is not an
installed package and not a published GitHub repository.

## Review Path

1. Read `README.md` for the repository boundary.
2. Read `examples_manifest.yaml` for intended example groups and safety gates.
3. Read `PRIVACY.md` for public/demo/private data rules.
4. Read `safety_report.md` for the current export safety result.

## What To Copy Later

After human approval, the future repository may receive public-safe copies of:

- the public demo suite;
- project templates;
- workspace demo material;
- dashboard demo material;
- advisor pack demo material;
- paper demo material.

Only files that pass the same privacy, public demo, and release hygiene checks
should be copied.

## What Not To Copy

Do not copy:

- raw data;
- API keys or `.env` files;
- private local paths;
- huge `npz` artifacts;
- restricted model files;
- real private logs;
- private advisor feedback;
- unsupported experiment claims.

## Expected Result

A reviewer should be able to confirm that the future examples repository is a
demo-only companion to the flagship TuringResearch repository. It should not be
presented as an independent product, a research result archive, or an install
source.
