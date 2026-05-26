# Demo Video Script v1.0

Status: draft.

Round: 197.

Target length: 5-7 minutes.

## 0:00 - Opening

TuringResearch Plus is a local-first Research OS. It helps keep evidence,
artifacts, routes, paper review, dashboards, advisor packs, plugin safety, and
privacy gates connected.

It does not automate research judgment or write final papers.

## 0:30 - README

Show the README first screen:

- local-first positioning;
- fake/demo-first boundary;
- quickstart;
- limitations.

Say: the main repository is the flagship install and docs entry point.

## 1:15 - Public Demo

Open:

- `examples/public_demo/README.md`
- `examples/public_demo/WALKTHROUGH.md`
- `examples/public_demo/dashboard/index.html`

Explain that the demo uses fake/demo data and does not need API keys or private
VGGT files.

## 2:15 - Evidence And Artifacts

Show evidence ledger and artifact index examples.

Emphasize:

- planned is not observed;
- missing evidence remains visible;
- artifacts do not become claims automatically.

## 3:00 - Paper / Related Work

Show paper review and related-work surfaces.

Say clearly: this scaffolds review material; it does not generate final paper
conclusions.

## 3:45 - Dashboard / Advisor Pack

Show dashboard and advisor pack documents.

Explain that these are review surfaces for humans.

## 4:30 - Plugin Safety

Show plugin policy:

- manifest required;
- unknown third-party plugins disabled;
- no secrets access;
- no `execute_code` default.

## 5:15 - VGGT Dogfooding

Show the public-safe case study.

Say: this is dogfooding for evidence management and route discipline, not a
claim that the VGGT experiment succeeded.

## 6:00 - Close

Close with tests and gates:

- full pytest;
- mypy;
- privacy gate;
- public release hygiene;
- split readiness.

End line: TuringResearch Plus is not magic automation. It is infrastructure for
reviewable research state.
