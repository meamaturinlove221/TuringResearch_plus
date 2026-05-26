# Open Source Compliance Checklist

Round: 360.4
Status: draft checklist for human review

## Repository Files

| Item | Status | Notes |
| --- | --- | --- |
| `LICENSE` | present | Proprietary until human license decision changes it |
| `CITATION.cff` | present | Uses TuringResearch public name |
| `CONTRIBUTING.md` | present | Documents fake/live and no-private-data boundaries |
| `CODE_OF_CONDUCT.md` | present | Conduct and source-hygiene expectations |
| `SECURITY.md` | present | Tells users not to submit secrets in public issues |
| README license section | present | Links license review and decision docs |

## Human Review Required

- Final public license choice.
- Dependency license compatibility.
- Contributor license expectations.
- Whether examples and generated artifacts are redistributable.
- Whether split manual packs can be published.
- Whether citation metadata should include a DOI, URL, or named authors.
- Whether security contact details should be added before public launch.

## Safety Checks

- No secrets.
- No API keys.
- No `.env` with real values.
- No raw data.
- No private local paths.
- No restricted model payloads.
- No fake GitHub URL.
- No fake GitHub Pages URL.
- No fake split-repo URL.
- No planned work written as observed evidence.

## Boundaries

- This checklist is not legal advice.
- It does not approve an open source license.
- It does not approve public release.
- It does not approve PyPI publication.
- It does not approve GitHub release publication.
- It does not override Source Hygiene or privacy gates.
