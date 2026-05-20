from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_examples_are_fake_mode_and_documented() -> None:
    examples = [
        "vggt-human-prior-survey",
        "smplx-feature-adapter-hypothesis",
        "citation-graph-demo",
        "pdf-to-markdown-demo",
    ]

    for example in examples:
        readme = ROOT / "examples" / example / "README.md"
        content = readme.read_text(encoding="utf-8").lower()
        assert "mode:" in content
        assert "no real network" in content or "no semantic scholar api key" in content
        assert "tulingresearch plus" in content
