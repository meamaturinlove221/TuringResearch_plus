# Capability Index

Status: generated from the Round 111 static capability catalog.

| Category | Capability | Tool | Live | Fake | Safety |
| --- | --- | --- | --- | --- | --- |
| evidence | `evidence.ledger` | `research.evidence_ledger` | false | true | local-review |
| artifact | `artifact.audit` | `artifact.audit` | false | true | local-review |
| visual | `visual.audit` | `visual.audit` | false | true | local-review |
| advisor | `advisor.pack` | `advisor.pack_build` | false | true | local-review |
| pdf | `pdf.phase_b` | `pdf.extract_figures` | false | true | local-review |
| paper | `paper.digest` | `paper.digest` | false | true | local-review |
| citation | `citation.graph` | `graph.citation_graph_expand` | true | true | live-optional |
| collision | `collision.risk` | `research.collision_risk_detect` | false | true | local-review |
| related work | `related_work.positioning` | `paper.related_work_position` | false | true | local-review |
| route | `route.dsl` | `research.route_compile` | false | true | local-review |
| failure | `failure.taxonomy` | `research.failure_classify` | false | true | local-review |
| dashboard | `dashboard.modal_run` | `dashboard.modal_run` | false | true | local-review |
| remote artifact | `remote_artifacts.unified` | `remote_artifacts.unify` | true | true | live-optional |
| handoff | `handoff.bundle` | `research.handoff_bundle_export` | false | true | local-review |
| plugin | `plugin.registry` | `plugins.registry_validate` | false | true | local-review |
| workspace | `workspace.registry` | `workspace.overview` | false | true | local-review |

## Notes

- `live=true` means the capability has an optional live path, not that default
  tests use the network.
- `fake=true` means fake/default workflows are supported.
- This index does not verify research results and does not promote planned work
  to observed evidence.
