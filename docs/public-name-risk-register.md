# Public Name Risk Register

Round: 360.1
Status: active risk register

| Risk | Impact | Mitigation |
| --- | --- | --- |
| public docs keep using suffix-first branding | open source visitors see a fragmented brand | run public docs sweep after scope lock |
| package name changes too early | installs and CI break | defer package rename until availability and compatibility audit |
| Python import path changes too early | existing tests and local scripts break | keep compatibility imports for now |
| CLI or MCP names change without audit | local smoke checks and user scripts break | require separate CLI / MCP audit |
| old spelling appears in public docs | name integrity and branding regression | keep old spellings only in historical rename docs or split-token planning docs |
| release docs imply publication | user confusion | keep release docs explicit: no PyPI, no tag, no GitHub release in this round |
| GitHub repository rename happens before links are ready | broken links | defer GitHub repo creation/rename to a human-approved release operation |
| split repo materials point to obsolete flagship wording | fragmented star and install path | update split backlink wording in a later public-docs pass |

## High-Risk Items

- Package distribution rename.
- Python import compatibility removal.
- CLI and MCP command rename.
- GitHub repository rename.

All four require separate approval and focused tests.

## Low-Risk Items

- README title update.
- Docs title update.
- Release display-name update.
- Public naming policy docs.

These are suitable for the next public-docs rename pass.
