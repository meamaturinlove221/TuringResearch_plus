# Legacy Name Compatibility Policy

Round: 360.1
Status: compatibility policy locked

## Principle

Public branding moves to TuringResearch first. Runtime compatibility moves only
after a separate audit proves the change will not break installation, imports,
CLI commands, MCP smoke checks, or release automation.

## Compatibility Names Temporarily Allowed

The following categories may remain temporarily:

- Python import compatibility package ending in `_plus`;
- package distribution name ending in `-plus`;
- console entry points ending in `-plus`;
- MCP server names ending in `-plus`;
- historical rename reports;
- tests that guard current compatibility behavior.

These are not the public brand. They are compatibility surfaces.

## Removal Requirements

Before removing a compatibility name:

1. Add a migration issue or scope doc.
2. Prove the replacement package, import, CLI, or MCP name works.
3. Keep a deprecation window or alias where practical.
4. Update docs, examples, tests, and release notes together.
5. Run full install, name integrity, CLI, MCP, and release checks.

## Not Allowed In Round 360.1

- Removing import compatibility.
- Renaming package metadata.
- Renaming CLI commands.
- Renaming MCP server names.
- Publishing PyPI.
- Creating tags.
- Creating or renaming GitHub repositories.

## Compatibility Decision

Keep compatibility names for now. The open source public name should change to
TuringResearch in public docs first, with runtime names handled by later
package and entry-point migration rounds.
