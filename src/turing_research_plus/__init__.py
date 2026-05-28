"""Compatibility alias for the historical ``tuling_research_plus`` package.

The public project name is TuringResearch Plus. Earlier internal code used the
``tuling_research_plus`` module path. This package keeps the public spelling
usable while preserving backward compatibility.
"""

from __future__ import annotations

import tuling_research_plus as _legacy
from tuling_research_plus import *  # noqa: F403

PACKAGE_NAME = "turing_research_plus"
__version__ = _legacy.__version__
__path__ = _legacy.__path__

__all__ = ["PACKAGE_NAME", "__version__"]
