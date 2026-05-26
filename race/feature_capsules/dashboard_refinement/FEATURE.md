# Dashboard Refinement

Status: feature capsule draft.

Release target: v0.7.

## 1. Problem

The v0.6 static dashboard is useful but still mostly Markdown-shaped. v0.7
should refine readability and navigation without creating a SaaS surface.

## 2. Research Motivating Example

A reviewer should quickly inspect project status, evidence gaps, paper assembly
blockers, replay status, and advisor next actions from a static local page.

## 3. Inputs

- workspace overview
- evidence summary
- dashboard report
- paper assembly report
- benchmark report

## 4. Outputs

- RefinedDashboardBundle
- DashboardSectionIndex
- DashboardReadinessReport

## 5. Proposed Commands / Tools

- command: `turing dashboard render`
- tool: `dashboard.refined_render`
- output: `RefinedDashboardBundle`

## 6. Related Contracts

- dashboard_refinement.yaml
- lightweight_dashboard.yaml
- modal_run_dashboard.yaml

## 7. Related Skills

- turingresearch-qa-release
- turingresearch-paper-writing-pipeline

## 8. Required Tests

- required section tests
- static HTML tests
- no experiment-result claim tests

## 9. Risks

- UI implies live dashboard
- dashboard content becomes claimed result
- hidden dependency on JavaScript/server

## 10. Done Criteria

- dashboard remains static/local
- required sections are present
- no result overclaim appears

## 11. Non-goals

- no SaaS
- no login
- no server requirement
