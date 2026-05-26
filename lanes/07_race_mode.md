# Lane 07: Race Mode

## Scope

Define Source Hygiene Gate, IdeaCard, and FeatureCapsule boundaries.

## Outputs

- `docs/race_mode.md`
- `contracts/race_features.yaml`
- `src/turing_research_plus/race/models.py`
- `tests/unit/test_idea_card.py`

## Status

Phase 1 complete. Race Mode blocks feature output when source hygiene fails.

## Round 12A Update

2026-05-19: Implemented deterministic `race.source_hygiene_check` under `src/turing_research_plus/race/source_hygiene.py`.

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

Safe implementation modes:

- independent clean-room implementation
- concept-level reimplementation
- compatible-license reuse
- documentation-only watch

Unknown source material becomes documentation-only watch and cannot become an implementation task. Tests cover public allowed, private blocked, unknown watch, and incompatible license blocking code copying.

## Round 12B Update

2026-05-19: Implemented deterministic Idea Radar extraction with `race.idea_extract` under `src/turing_research_plus/race/idea_radar.py`.

`IdeaCard` now records:

- `raw_text`
- `normalized_summary`
- `inferred_intent`
- `source`
- value, feasibility, urgency, and novelty scores
- `priority`
- `recommended_action`
- `evidence_refs`
- `uncertain_terms`

TTS correction rules now recover project-context terms such as MCP, cache, ledger, and Race Mode while preserving uncertain terms for review. High-confidence public or authorized ideas may become implementation candidates only when Source Hygiene Gate passes. Unknown or blocked sources can only produce watch or documentation items.

Created Race workspace files:

- `race/idea_cards/.gitkeep`
- `race/priority_board.md`

## Round 12C Update

2026-05-19: Implemented deterministic Priority Elevator scoring with `race.priority_score` under `src/turing_research_plus/race/priority_elevator.py`.

Scoring formula:

`PriorityScore = 0.30 * value_score + 0.25 * urgency_score + 0.20 * feasibility_score + 0.15 * novelty_score + 0.10 * strategic_fit`

Priority rules:

- P0: prototype immediately
- P1: create feature capsule this sprint
- P2: document and monitor
- P3: archive

Source hygiene that does not pass prevents P0/P1 and forces those candidates to P2. Feature Capsule recommendation is generated only for P1 ideas with passing source hygiene.

## Round 12D Update

2026-05-19: Implemented Feature Capsule Factory with `race.feature_capsule_create` under `src/turing_research_plus/race/feature_capsule.py`.

The factory generates the minimum capsule skeleton:

- `race/feature_capsules/<feature_name>/FEATURE.md`
- `race/feature_capsules/<feature_name>/contract.yaml`
- `race/feature_capsules/<feature_name>/SKILL.md`
- `src/turing_research_plus/<domain>/<feature_name>.py`
- `tests/unit/test_<feature_name>.py`
- `docs/features/<feature_name>.md`
- `sop_graphs/feature_graphs/<feature_name>.mmd`

`FEATURE.md` includes Problem, User story, Input, Output, Data model, Public tools, Internal service, Risks, Tests, and Done criteria. Each capsule links its source `IdeaCard`, carries evidence, requires passed Source Hygiene Gate, and includes a test plus SOP graph.

Created directory roots:

- `race/feature_capsules/.gitkeep`
- `docs/features/.gitkeep`
- `sop_graphs/feature_graphs/.gitkeep`

## Round 12E Update

2026-05-19: Implemented the 16-Box Architecture Builder with `race.architecture_box_build` under `src/turing_research_plus/race/architecture_box.py`.

Default architecture boxes:

- Idea Radar
- Priority Elevator
- Source Hygiene
- Upstream Watch
- Feature Capsule
- SOP Graph
- Core Paper Tools
- Core Web Tools
- PDF Markdown
- Semantic Graph
- Literature Survey
- Vault
- Context
- Hypothesis / Ideation
- Convergence / Stress / Experiment
- Paper / Figure Pipeline

Each box records goal, owner skill, public tools, internal modules, input artifacts, output artifacts, tests, priority, and dependencies. The builder rejects orphan dependencies and emits a Mermaid dependency graph for release planning.

Updated planning artifacts:

- `docs/architecture_16box.md`
- `docs/architecture_16box.mmd`
- `race/feature_capsules/index.md`

Tests cover 16 default boxes, owner skill assignment, dependency closure, graph generation, and the thin tool wrapper payload.

## Round 15A Update

2026-05-19: Implemented Upstream Watch with `race.upstream_watch` under `src/turing_research_plus/race/upstream_watch.py`.

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

Outputs:

- `race/upstream_reports/*.md`
- `race/upstream_reports/*.json`
- optional `IdeaCard` entries for public/authorized sources only

Source rules:

- Public or authorized upstream snapshots may produce watch items.
- Private repo content, leaked roadmaps, NDA content, and proprietary code are blocked.
- Unknown sources are watch-only and cannot produce implementation IdeaCards.

Tests cover README diffs, release reports, suspicious version changes, private-source blocking, unknown-source watch-only behavior, and the thin tool wrapper payload.
