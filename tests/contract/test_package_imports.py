from __future__ import annotations

import importlib
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]





def pyproject() -> dict[str, object]:

    return tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))





def test_core_and_plus_packages_import() -> None:

    core = importlib.import_module("turing_research")

    plus = importlib.import_module("turing_research_plus")

    pdf = importlib.import_module("turing_research.pdf")

    vggt = importlib.import_module("turing_research_plus.vggt")

    artifact_audit = importlib.import_module("turing_research_plus.artifact_audit")



    assert core.__version__ == "1.5.0rc0"
    assert core.PACKAGE_NAME == "turing_research"

    assert plus.__version__ == "1.5.0rc0"
    assert plus.PACKAGE_NAME == "turing_research_plus"

    assert hasattr(pdf, "PDFMarkdownOutput")

    assert hasattr(vggt, "VGGTEvidenceLedger")

    assert hasattr(artifact_audit, "ArtifactAuditReport")





def test_round38_package_surface_imports() -> None:

    modules = [

        "turing_research_plus.vggt.evidence_models",

        "turing_research_plus.vggt.evidence_ledger",

        "turing_research_plus.vggt.edge_audit",

        "turing_research_plus.vggt.markdown_export",

        "turing_research_plus.artifact_audit.models",

        "turing_research_plus.artifact_audit.auditor",

        "turing_research_plus.artifact_audit.npz_summary",

        "turing_research_plus.artifact_audit.manifest",

    ]



    for module_name in modules:

        assert importlib.import_module(module_name)





def test_mcp_server_module_import_is_safe(capsys) -> None:

    sys.modules.pop("turing_research.mcp_server", None)



    module = importlib.import_module("turing_research.mcp_server")

    captured = capsys.readouterr()



    assert module.MCP_SERVER_NAME == "turingresearch-plus"

    assert callable(module.main)

    assert captured.out == ""

    assert captured.err == ""





def test_package_metadata_is_readable_from_pyproject() -> None:

    metadata = pyproject()

    project = metadata["project"]

    assert isinstance(project, dict)



    assert project["name"] == "turingresearch-plus"

    assert project["requires-python"] == ">=3.11"

    assert "pydantic>=2.7" in project["dependencies"]

    assert "pydantic-settings>=2.2" in project["dependencies"]

    assert "httpx>=0.27" in project["dependencies"]





def test_package_discovery_covers_core_and_plus_packages() -> None:

    metadata = pyproject()

    tool = metadata["tool"]

    assert isinstance(tool, dict)

    setuptools = tool["setuptools"]

    assert isinstance(setuptools, dict)

    find = setuptools["packages"]["find"]

    assert isinstance(find, dict)



    assert find["where"] == ["src"]

    assert "turing_research*" in find["include"]

    assert "turing_research_plus*" in find["include"]
