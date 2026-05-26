# Privacy Boundary

Status: public-safe policy note.

This bundle is intended for fake/demo examples only. It must not contain
private research data, private logs, secrets, or local machine paths.

## Allowed

- public-safe demo text;
- public-safe template descriptions;
- fake/demo evidence ledgers;
- fake/demo dashboard examples;
- fake/demo advisor pack examples;
- documentation that explains safety boundaries.

## Excluded

- raw data;
- API keys, tokens, and `.env` files;
- private local paths;
- huge `npz` artifacts;
- restricted model files;
- real private logs;
- private advisor feedback;
- non-public VGGT files;
- unsupported success claims.

## Live/Fake Boundary

Examples are fake/demo by default. Live adapters remain optional and must be
enabled explicitly in the flagship repository. The future examples repository
must not require network access or credentials for its default walkthrough.

## Human Review

Before creating a real repository, a maintainer must review the exact file set,
privacy boundary, public demo outputs, and release hygiene scan results.
