# Three-minute Interview Version

TuringResearch is a portfolio-scale engineering project for research
workflow management.

The problem is that research state gets scattered across papers, notes,
artifacts, experiments, dashboards, and advisor feedback. TuringResearch
turns that into explicit local state: evidence ledgers, artifact audits, route
DSL, paper scaffolds, advisor packs, dashboards, plugin manifests, privacy
gates, and replay checks.

The engineering challenge is not only building features, but preventing
overclaiming. Planned work must stay planned. Fake/demo outputs must not become
observed evidence. Plugin manifests must not imply unknown code execution.

The VGGT dogfooding case shows how the system organizes a real research-style
workflow while keeping private data and unsupported claims out of public
materials.

The v1.0 direction is stable API, public demo, plugin manifest stability, and
optional case/examples split repos while keeping the main repo as the flagship.
