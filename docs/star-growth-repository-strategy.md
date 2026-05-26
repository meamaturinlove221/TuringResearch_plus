# Star Growth Repository Strategy

Status: planning policy.

Round: 151.

The repository strategy should help public users understand and star the
flagship project before the ecosystem is split into many repositories.

## Main Principle

Concentrate public attention on `turingresearch` first.

Satellite repositories should act as spokes that point back to the flagship.
They should not compete with it for the first impression, quickstart, public
demo, or release story.

## Why Stars Matter Here

Stars are not the technical goal, but they are a visibility signal:

- they help new users find the project;
- they make internship and portfolio review easier;
- they concentrate issues, feedback, and community attention;
- they reduce confusion about which repository is the real entry point.

## Short-term Star Strategy

- Keep the flagship repository complete and useful.
- Put the clearest README, screenshots or demo links, and quickstart in the
  flagship.
- Keep public demos in the flagship until they are strong enough to stand
  alone.
- Keep the case-study summary in the flagship even if the detailed case study
  later gets its own repository.
- Avoid splitting core modules before the main repo has enough visible value.

## Satellite Repository Rules

Every satellite repository should:

- link back to the flagship at the top of its README;
- explain its scope in one paragraph;
- state whether it is demo-only, optional, experimental, or release-ready;
- include independent tests and docs;
- avoid implying it replaces the flagship;
- avoid carrying private data or unsupported claims.

## Good First Satellite Candidates

Case studies and examples can grow stars without hollowing the main repo:

- `turingresearch-vggt-case`: tells a concrete dogfooding story.
- `turingresearch-examples`: gives demo-safe workflows for new users.

Plugin and dashboard repositories should wait until their surfaces are clearer:

- `turingresearch-plugins`: after public registry draft and review workflow.
- `turingresearch-dashboard`: after local server dashboard matures.

## What To Avoid

- Splitting many small repos before users understand the flagship.
- Moving core code out so the main repo becomes a landing page only.
- Creating separate repos with incomplete docs or tests.
- Creating separate repos that contain private data, license uncertainty, or
  unsupported research claims.
- Creating separate repos with unclear install paths.

## Public Portfolio Angle

The flagship repo should communicate:

- product thinking;
- engineering breadth;
- testing and safety discipline;
- research workflow understanding;
- plugin and MCP ecosystem design;
- public-demo and case-study discipline.

Satellite repos should deepen this story, not fragment it.
