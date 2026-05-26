# First Split Candidate Report

Status: recommendation complete.

Round: 156.

This report ranks the first realistic future repository split candidates. It is
not approval to create repositories or move code.

## Recommended First Candidates

1. `turingresearch-vggt-case`
2. `turingresearch-examples`

These candidates are best because they are presentation and demo surfaces, not
core runtime surfaces. They can be made standalone while preserving the flagship
repo as the canonical product.

## Candidate 1: `turingresearch-vggt-case`

Recommended timing: after one more public-safe case-study audit.

Why it is strong:

- clear narrative value;
- shows real dogfooding process;
- can demonstrate route changes, failures, evidence management, advisor packs,
  privacy/compliance gates, dashboard, and paper scaffold outputs;
- can link back to the main repo as the engine.

Required before split:

- no private local paths;
- no raw data;
- no bundled model files;
- no unsupported experiment claims;
- no private advisor feedback;
- no claim that SparseConv3D succeeded unless evidence is added later;
- license/compliance disclaimer included;
- all outputs marked as case-study/demo material where appropriate.

## Candidate 2: `turingresearch-examples`

Recommended timing: after public demo expansion has a stable index and clean
privacy gate.

Why it is strong:

- gives users a low-risk place to inspect demos;
- can include fake/demo projects without shipping core internals;
- can help stars flow back to the flagship through links and install docs;
- reduces main repo visual clutter only after examples are polished.

Required before split:

- demo-safe data policy;
- no real private project data;
- no API keys or secrets;
- no raw data payloads;
- no model payloads;
- public demo tests and privacy gates passing;
- clear README that points back to the flagship.

## Later Candidates

| Candidate | Timing | Reason |
| --- | --- | --- |
| `turingresearch-plugins` | after sandbox and registry contracts mature | Strong ecosystem value, but unsafe to split before compatibility and disabled-by-default behavior are frozen. |
| `turingresearch-paper` | after paper beta API stabilizes | Valuable, but citation and claim boundaries need more real review usage. |
| `turingresearch-artifact` | after adapter safety hardening | Useful surface, but coupled to privacy and fake/live boundaries. |
| `turingresearch-dashboard` | after local server dashboard scope | Good public product surface, but current version is static/local-first. |
| `turingresearch-core` | last, if ever | Splitting core too early weakens the flagship. |

## Star Strategy

The first split should increase trust in the flagship, not compete with it.
Spoke repositories should:

- link to the flagship in the first viewport;
- use the same package identity and install guidance;
- state that the flagship remains the primary repo;
- avoid duplicating release notes or confusing version ownership.

## Recommendation

Do not split now. Prepare `turingresearch-vggt-case` and
`turingresearch-examples` as the first future candidates once they pass a
dedicated public-safe extraction gate.
