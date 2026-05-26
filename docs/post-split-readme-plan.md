# Post-split README Plan

Status: planning policy.

Round: 171.

If `turingresearch-vggt-case` or `turingresearch-examples` becomes a real
repository later, the main README must still be the flagship entry point.

## Main README Structure

The main README should keep this order:

1. local-first Research OS positioning;
2. quick value summary;
3. quickstart and install;
4. core capability map;
5. fake/demo vs live boundary;
6. public demo links;
7. optional case/example spoke links;
8. architecture and visual tour;
9. safety and privacy;
10. roadmap.

Spoke links should not appear before the main product is understandable.

## Required Main README Language

The main README should say:

- TuringResearch is the flagship repository.
- Install and develop from the main repo.
- Split repos are optional demos or case studies.
- Live adapters remain optional.
- Human review remains required.
- Demo outputs are not research results.

## Spoke README Requirements

Each spoke README should include:

- a first-section link back to the flagship;
- a one-paragraph scope statement;
- a clear demo/case-only label;
- privacy and safety boundary;
- statement that it does not replace the main repo;
- statement that the main repo remains the install path.

## README Anti-patterns

Avoid:

- making spoke repos look like the canonical package;
- claiming the case repo proves research success;
- implying examples are required for install;
- hiding safety boundaries behind links;
- splitting the quickstart across repositories.
