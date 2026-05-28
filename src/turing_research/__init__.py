"""Compatibility alias for the historical ``tuling_research`` package.

The public project name is TuringResearch. Earlier internal code used the
``tuling_research`` module path. This package keeps the public spelling usable
without breaking the existing implementation modules.
"""

from __future__ import annotations

import tuling_research as _legacy
from tuling_research import *  # noqa: F403

PACKAGE_NAME = "turing_research"
__version__ = _legacy.__version__
__path__ = _legacy.__path__

__all__ = ["PACKAGE_NAME", "__version__"]
