# TulingResearch Plus Race Mode

Race Mode turns public, authorized source material into idea cards and feature capsules. It cannot create implementation tasks until Source Hygiene Gate passes.

## Source Hygiene Gate

The gate records:

- Source authorization status.
- Public-source evidence references.
- Blocked reason when source material is private, non-public, or unclear.

Allowed source classes:

- public repos
- public README files
- public issues
- public release notes
- user-owned notes
- authorized transcripts

Blocked source classes:

- private repo content
- leaked roadmap material
- NDA content
- proprietary code
- copied implementation details from incompatible licenses

Unknown or unclear sources become documentation-only watch items and cannot become implementation tasks.

Safe implementation modes:

- independent clean-room implementation
- concept-level reimplementation
- compatible-license reuse
- documentation-only watch

## Outputs

Race Mode defines boundary models for:

- `IdeaCard`
- `FeatureCapsule`
- `SourceHygieneGate`

Round 12A adds `race.source_hygiene_check` for deterministic local source hygiene checks. It does not call external network services.

Round 12B adds `race.idea_extract` for deterministic Idea Radar extraction from noisy text, public transcripts, README changes, issues, commit summaries, and manual notes.

Idea Radar rules:

- Do not blindly preserve TTS errors.
- Recover likely terms from TulingResearch Plus context.
- Put uncertain terms in `uncertain_terms`.
- Do not invent proper nouns when confidence is low.
- Distinguish high-confidence ideas from speculative ideas.
- Allow implementation only when source hygiene passes and the source is public or authorized.
- Unknown or blocked sources can only produce watch or documentation items.

All important Race Mode outputs must be convertible to `ResearchArtifact`.

## Feature Capsules

Feature Capsule generation creates a minimal skeleton for P0/P1 ideas whose source hygiene has passed. The skeleton includes feature docs, a contract placeholder, a skill skeleton, a module placeholder, tests, and an SOP graph. It does not copy implementation details from protected or incompatible sources.

## Upstream Watch

Round 15A adds `race.upstream_watch` for deterministic comparison of public upstream snapshots. It does not call external network services.

Watch dimensions:

- new release
- README changed
- docs added
- new examples
- new feature branch
- new MCP tool
- new architecture diagram
- sudden stars/forks increase
- issue discussion suggests roadmap
- version anomaly

Rules:

- Only public or authorized sources can produce implementation-relevant IdeaCards.
- Private repos, leaked roadmap material, NDA content, and proprietary code are blocked by Source Hygiene Gate.
- Unknown sources can only produce watch reports and never implementation tasks.
- Reports are written under `race/upstream_reports/` as Markdown and JSON when requested.
