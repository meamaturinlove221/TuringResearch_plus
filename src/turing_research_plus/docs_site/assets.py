"""Asset helpers for the static docs site builder."""

from __future__ import annotations

import shutil
from pathlib import Path

ASSET_SUFFIXES = {".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".mmd"}


def copy_docs_site_assets(source_root: Path, output_root: Path) -> list[Path]:
    """Copy supported assets from docs-site/assets when present."""

    assets_root = source_root / "assets"
    if not assets_root.exists():
        return []

    copied: list[Path] = []
    for source in sorted(assets_root.rglob("*")):
        if not source.is_file() or source.suffix.lower() not in ASSET_SUFFIXES:
            continue
        relative = source.relative_to(assets_root)
        target = output_root / "assets" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        copied.append(target)
    return copied
