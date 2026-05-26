# Campaign Preconditions

Status: implemented minimal.

Round: 176 upstream adjustment.

Campaign preconditions keep routing honest. A campaign can be recommended even
when inputs are missing, but missing preconditions should be reported as review
work, not silently filled in.

## Required Preconditions

| Campaign | Preconditions |
| --- | --- |
| `north_star` | research intent or project brief |
| `knowledge_acquisition` | source list or search intent, source hygiene boundary |
| `deep_insight` | evidence notes, claim candidates |
| `hypothesis_formation` | north star, evidence constraints |
| `creative_ideation` | problem statement, constraints |
| `convergence` | candidate list, evaluation criteria |
| `stress_test` | candidate claim or release surface |
| `experiment_planning` | north star, setup placeholder, hard gates |
| `artifact_audit` | artifact manifest or expected outputs |
| `advisor_pack` | evidence summary, artifact readiness, limitations |
| `public_release` | passing tests, public-safe docs, privacy scan |

## Safety Notes

- Missing preconditions must not be fabricated.
- Planned routes must not become observed runs.
- Fake/demo outputs must stay labeled fake/demo.
- Live adapter results require explicit opt-in and human review.
- Public release campaigns must run privacy/security checks before launch.
