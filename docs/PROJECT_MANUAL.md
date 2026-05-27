# TuringResearch Project Manual

TuringResearch is a local-first research workflow system for AI-assisted scientific iteration.

## 1. Positioning

TuringResearch is not only a paper summarizer and not only a coding helper. It is a structure for managing the research loop:

```text
intent → evidence → hypothesis → experiment → artifact → report → next step
```

It is especially useful when research work involves long conversations, changing requirements, many artifacts, and repeated route planning.

## 2. Operating principles

- **Docs-first**: describe purpose and boundaries before promotion.
- **Evidence-first**: separate observed, planned, fake-data, missing-paper, and missing-experiment states.
- **Contract-first**: define inputs, outputs, and gates before treating a workflow as stable.
- **Local-first**: live adapters should be optional and disabled by default.
- **Honest scope**: never present planning-only outputs as verified research results.

## 3. Main workflow layers

| Layer | Purpose |
|---|---|
| Intake | Capture goals, constraints, blockers, non-goals. |
| Literature | Turn papers and references into structured method cards. |
| Gap / Hypothesis | Convert missing pieces into testable routes. |
| Experiment Route | Define hard gates, fallbacks, and expected artifacts. |
| Artifact Audit | Check bundles, logs, boards, hashes, reports, and unsupported claims. |
| Advisor Pack | Prepare mentor-facing summaries and next actions. |
| Community Intake | Accept documentation-only ideas and skill proposals. |

## 4. Evidence labels

Use conservative labels:

- `observed`: actually verified in this repo or experiment logs;
- `planned`: described but not implemented;
- `fake-data`: demo fixture only;
- `requires-real-paper`: needs source paper or citation;
- `requires-real-experiment`: needs actual experimental output;
- `reference`: inspired by external public projects.

## 5. What not to do

Do not:

- invent publication claims;
- overstate upstream reference material;
- merge unreviewed source code from a reference project;
- publish private paths or secrets;
- use README polish to hide missing evidence;
- treat proxy results as advisor-ready results.

## 6. Contribution paths

### Implementation contributions

Require normal code review, tests, and safety checks.

### Idea / skill proposal contributions

Use documentation-only files under `community/`. These can later become feature capsules, skills, SOPs, campaign entries, or roadmap items.

## 7. Release checklist

Before public release:

- README and README_CN are consistent;
- mascot SVG renders at the top of README;
- no misleading academic-output migration wording remains;
- live features are disabled by default;
- no secrets or private paths exist;
- reference projects are described as reference / inspiration only;
- planned modules are not written as finished features.

## 8. Final rule

When uncertain, choose the more conservative claim.

TuringResearch should make research work clearer, not more magical.
