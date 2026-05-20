from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ALLOWED_NAMESPACES = {"core", "pdf", "graph", "research", "vault", "context", "race", "paper"}
DOC_ROW_PATTERN = re.compile(
    r"\| `(?P<tool>[a-z_]+\.[a-z0-9_]+)` \| `(?P<input>[^`]+)` "
    r"\| `(?P<output>[^`]+)` \| `(?P<status>[^`]+)` \|"
)


def contract_tools() -> set[str]:
    tools: set[str] = set()
    for path in sorted((ROOT / "contracts").glob("*.yaml")):
        content = path.read_text(encoding="utf-8")
        for match in re.finditer(
            r"^\s*tool_name:\s*([a-z_]+\.[a-z0-9_]+)\s*$",
            content,
            re.MULTILINE,
        ):
            tools.add(match.group(1))
    return tools


def documented_tools() -> set[str]:
    text = (ROOT / "docs" / "mcp-tools.md").read_text(encoding="utf-8")
    return {match.group("tool") for match in DOC_ROW_PATTERN.finditer(text)}


def test_all_tool_namespaces_are_release_approved() -> None:
    offenders: list[str] = []

    for tool in contract_tools() | documented_tools():
        namespace = tool.split(".", 1)[0]
        if namespace not in ALLOWED_NAMESPACES:
            offenders.append(f"{tool} uses unapproved namespace {namespace}")

    assert offenders == []


def test_contract_tools_and_mcp_docs_are_symmetric() -> None:
    from_contracts = contract_tools()
    from_docs = documented_tools()

    assert from_contracts - from_docs == set()
    assert from_docs - from_contracts == set()


def test_mcp_docs_status_values_are_release_approved() -> None:
    allowed_status = {"implemented_minimal", "implemented_dry_run", "contract_only", "blocked"}
    text = (ROOT / "docs" / "mcp-tools.md").read_text(encoding="utf-8")
    statuses = {match.group("status") for match in DOC_ROW_PATTERN.finditer(text)}

    assert statuses <= allowed_status
