# TuringResearch Plus Source Hygiene Policy

TuringResearch Plus uses Source Hygiene Gate rules to prevent unsafe or unauthorized material from becoming implementation work.

## Allowed Sources

- Public repositories.
- Public README files.
- Public issues.
- Public release notes.
- Public documentation.
- User-owned notes.
- Authorized transcripts.
- Public datasets with compatible terms.

## Blocked Sources

- Private repository content.
- Leaked roadmap material.
- NDA content.
- Proprietary code.
- Copied implementation details from incompatible licenses.
- Private papers without authorization.
- Restricted datasets without authorization.
- Secrets, API keys, access tokens, or credentials.

## Safe Implementation Modes

- Independent clean-room implementation.
- Concept-level reimplementation.
- Compatible-license reuse after review.
- Documentation-only watch.

## Race Mode Rule

Race Mode may create implementation work only when source material is public or authorized and Source Hygiene passes. Unknown sources, speculative claims, or unclear rights remain watch-only or documentation-only.

## Paper And Research Rule

Research conclusions, paper sections, claims, gaps, hypotheses, and experiments must preserve EvidenceRef where applicable. TuringResearch Plus must not fabricate results or treat unauthorized material as evidence.

## Reporting Rule

Do not include private data, restricted datasets, private papers, API keys, tokens, or secrets in issues, pull requests, examples, docs, tests, or screenshots.
