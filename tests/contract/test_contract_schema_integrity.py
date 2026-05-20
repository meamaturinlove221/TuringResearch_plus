from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACTS = sorted((ROOT / "contracts").glob("*.yaml"))
REQUIRED_HEADER_FIELDS = {
    "name",
    "version",
    "status",
    "description",
    "mcp_server",
    "project",
    "tool_contract_fields",
}
REQUIRED_TOOL_FIELDS = {
    "tool_name",
    "namespace",
    "input_model",
    "output_model",
    "cache_behavior",
    "network_behavior",
    "error_behavior",
    "evidence_requirement",
    "required_tests",
    "implementation_status",
}
DOC_ROW_PATTERN = re.compile(
    r"\| `(?P<tool>[a-z_]+\.[a-z0-9_]+)` \| `[^`]+` \| `[^`]+` \| `(?P<status>[^`]+)` \|"
)


def parse_doc_statuses() -> dict[str, str]:
    text = (ROOT / "docs" / "mcp-tools.md").read_text(encoding="utf-8")
    return {match.group("tool"): match.group("status") for match in DOC_ROW_PATTERN.finditer(text)}


def parse_contract_statuses() -> dict[str, str]:
    statuses: dict[str, str] = {}
    for path in CONTRACTS:
        current_tool: str | None = None
        for line in path.read_text(encoding="utf-8").splitlines():
            tool_match = re.match(r"\s*tool_name:\s*([a-z_]+\.[a-z0-9_]+)\s*$", line)
            if tool_match:
                current_tool = tool_match.group(1)
                continue
            status_match = re.match(r"\s*implementation_status:\s*([a-z_]+)\s*$", line)
            if status_match and current_tool:
                statuses[current_tool] = status_match.group(1)
    return statuses


def tool_blocks(content: str) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    matches = list(re.finditer(r"^  ([a-z_]+\.[a-z0-9_]+):\s*$", content, re.MULTILINE))
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
        block = content[start:end]
        name_match = re.search(r"^\s*tool_name:\s*([a-z_]+\.[a-z0-9_]+)\s*$", block, re.MULTILINE)
        if name_match:
            blocks.append((name_match.group(1), block))
    return blocks


def test_contract_files_have_release_header_fields() -> None:
    offenders: list[str] = []
    for path in CONTRACTS:
        text = path.read_text(encoding="utf-8")
        for field in REQUIRED_HEADER_FIELDS:
            if not re.search(rf"^{field}:", text, re.MULTILINE):
                offenders.append(f"{path.relative_to(ROOT)} missing {field}")

    assert offenders == []


def test_tool_contract_blocks_have_required_fields() -> None:
    offenders: list[str] = []
    for path in CONTRACTS:
        text = path.read_text(encoding="utf-8")
        for tool_name, block in tool_blocks(text):
            for field in REQUIRED_TOOL_FIELDS:
                if not re.search(rf"^\s+{field}:", block, re.MULTILINE):
                    offenders.append(f"{path.relative_to(ROOT)} {tool_name} missing {field}")

    assert offenders == []


def test_contract_statuses_match_mcp_docs() -> None:
    assert parse_contract_statuses() == parse_doc_statuses()


def test_contract_yaml_has_no_status_type_concatenation() -> None:
    offenders: list[str] = []
    for path in CONTRACTS:
        text = path.read_text(encoding="utf-8")
        if re.search(r"implementation_status:\s*\S+types:", text):
            offenders.append(str(path.relative_to(ROOT)))

    assert offenders == []
