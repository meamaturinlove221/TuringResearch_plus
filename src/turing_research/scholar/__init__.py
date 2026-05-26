"""Scholar content services for TuringResearch Core."""

from turing_research.scholar.content_service import PaperContentService
from turing_research.scholar.models import PaperContentRequest, PaperContentResult

__all__ = ["PaperContentRequest", "PaperContentResult", "PaperContentService"]
