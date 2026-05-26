# Interview Demo Script

Status: portfolio draft.

Round: 158.

This script is a short local demo path for interviews. It uses fake/demo
material and does not require live network access.

## 0. Setup

```powershell
python -m pip install -e .[dev]
python -m pytest tests/contract/test_name_integrity.py -q
```

Message:

> The default path is fake/demo first. I am not running real experiments or
> using private data in this demo.

## 1. Open README

Show:

- local-first Research OS;
- evidence-led workflow;
- what it does not claim;
- public demo and VGGT dogfooding case.

Message:

> The key idea is not to automate science, but to keep research state honest.

## 2. Show Public Demo

Open:

- `examples/public_demo/`
- `examples/public_demo/dashboard/`

Show:

- demo projects;
- evidence ledger;
- artifact index;
- advisor pack;
- dashboard.

Message:

> All public demo data is fake/demo and marked as such.

## 3. Show VGGT Dogfooding Case

Open:

- `examples/vggt-human-prior-survey/public_case_study/case_study_draft.md`
- `examples/vggt-human-prior-survey/public_case_study/claim_safety_report.md`

Message:

> This is a dogfooding case. It shows process and tooling value, not experiment
> success.

## 4. Show Architecture

Open:

- `examples/portfolio/turingresearch_architecture.mmd`
- `docs/interview-architecture-explanation.md`

Message:

> The architecture separates project state, research workflow, review surfaces,
> and extension/release gates.

## 5. Show Testing And Contracts

Run:

```powershell
python -m pytest tests/contract/test_new_namespace_imports.py tests/contract/test_legacy_namespace_compat.py -q
```

Message:

> The project uses contracts and compatibility tests to make module evolution
> safer.

## 6. Close With Roadmap

Show:

- `docs/module-split-readiness-gate.md`
- `docs/star-growth-plan.md`

Message:

> I kept the flagship monorepo intact first, then added module boundaries and
> split-readiness gates. The first future split candidates are case studies and
> examples, not core.
