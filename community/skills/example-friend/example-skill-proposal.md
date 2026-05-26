# Skill Proposal: Example Idea Intake Reviewer

## Contributor

- GitHub username: example-friend
- Display name to credit: Example Friend
- Date: 2026-05-26

## One-line Summary

A skill that reviews community idea documents and decides whether they should become roadmap items, feature capsules, SOPs, or skill proposals.

## Trigger Conditions

Use this skill when a collaborator submits a Markdown idea document under `community/ideas/`.

## Goal

Help maintainers turn raw collaborator ideas into structured TuringResearch assets without allowing unreviewed code or unsafe content into the project.

## Inputs

- idea Markdown file;
- contributor metadata;
- references / attribution;
- target module;
- expected artifacts.

## Outputs

- review summary;
- decision label;
- safety notes;
- suggested conversion path;
- follow-up issue or feature capsule draft.

## Procedure

1. Check whether the file only touches `community/`.
2. Check whether the idea has a problem statement and proposed direction.
3. Check whether references and attribution are clear.
4. Check whether private data, secrets, or unsupported claims are present.
5. Decide one of: accept-as-idea, accept-as-skill-candidate, convert-to-feature-capsule, defer, reject.
6. Write review notes.

## Safety / Boundaries

- Do not edit implementation code.
- Do not run code.
- Do not accept private data.
- Do not accept copied third-party text without attribution.
- Do not create release claims from unimplemented ideas.

## Required Tests or Review Gates

- community path-only check;
- no-secrets check;
- attribution check;
- maintainer review.

## Related TuringResearch Modules

- research intake
- docs / dashboard
- campaign catalog
- MCP / plugin
- release / open source

## Conversion Notes

If accepted, maintainers can convert this into `.agents/skills/community-idea-reviewer/SKILL.md` in a separate implementation branch.
