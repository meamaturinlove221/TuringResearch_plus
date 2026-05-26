# TuringResearch Public Naming Policy

Round: 360.1
Status: policy locked

## Canonical Public Name

The canonical open source public name is **TuringResearch**.

Use TuringResearch for:

- README title;
- public docs title;
- release title;
- package display name;
- flagship repository references;
- screenshots, demo pages, and interview materials.

## Historical Names To Remove From Public Surfaces

The following spellings are considered old or compatibility-only. They are
written here as split tokens to avoid reintroducing forbidden literal strings
into public docs:

| Split spelling | Meaning | Public policy |
| --- | --- | --- |
| `Tul` + `ingResearch` | old display spelling | remove from public docs |
| `Tul` + `ingResearch_plus` | old repo/root spelling | remove from public docs |
| `TuringResearch` + `_plus` | current root suffix spelling | stop using as public brand |
| `turingresearch` + `-plus` | current package distribution spelling | keep until package decision |
| `turing_research` + `_plus` | current Python compatibility package | keep until import audit |

## Public Style

Preferred:

- TuringResearch
- TuringResearch repository
- TuringResearch docs
- TuringResearch release candidate
- TuringResearch local-first research workflow

Avoid in public positioning:

- leading with a suffix;
- treating compatibility package names as the brand;
- writing old project names outside migration docs;
- implying that the rename changes runtime behavior.

## Compatibility Style

Compatibility names may remain where changing them would break users or tests:

- Python import paths;
- console entry points;
- MCP server names;
- package metadata;
- historical rename reports;
- contract tests that verify compatibility.

Each compatibility name needs a later migration issue before removal.

## Release Rule

Release-facing docs should say TuringResearch. If a compatibility package name
must appear, label it as a temporary compatibility or packaging decision, not
as the public brand.
