# Community Idea and Skill Intake

This directory is for trusted collaborators who want to contribute **idea documents** and **skill proposals** to TuringResearch without submitting implementation code.

The goal is to turn collaborator ideas into reviewable research-product assets:

- idea briefs;
- skill proposals;
- SOP proposals;
- campaign proposals;
- feature capsule candidates;
- docs-only product demonstrations.

## Contribution Scope

Allowed:

- Markdown idea documents;
- skill design proposals;
- workflow diagrams in Mermaid Markdown;
- feature capsule drafts;
- public-safe examples;
- references to public papers or public repositories;
- non-code pseudocode if clearly marked as design notes.

Not allowed in this directory:

- implementation code;
- copied source code from another project;
- secrets, tokens, `.env`, cookies, API keys;
- private logs or private user data;
- raw datasets or model files;
- unlicensed third-party PDFs or images;
- changes to `src/`, `tests/`, package metadata, CI, or release files.

## Suggested Workflow

1. Create a contributor branch from `main`.
2. Add one Markdown file under `community/ideas/<github-username>/` or `community/skills/<github-username>/`.
3. Use the corresponding template.
4. Open a pull request with the label `community-idea` or `skill-proposal`.
5. The maintainer reviews it for scope, safety, attribution, and usefulness.
6. Accepted ideas may later be converted into feature capsules, skills, SOPs, or roadmap items.

## Directory Layout

```text
community/
  README.md
  CONTRIBUTOR_GUIDE.md
  REVIEW_POLICY.md
  ideas/
    README.md
    _template.md
    example-friend/
      example-idea.md
  skills/
    README.md
    _template.md
    example-friend/
      example-skill-proposal.md
  intake-log.md
```

## Status

This intake area is documentation-only. It is safe for collaborators who should not touch implementation code.
