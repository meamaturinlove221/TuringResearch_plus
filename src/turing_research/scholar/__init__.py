"""Scholar content services for TulingResearch Core."""

from tuling_research.scholar.content_service import PaperContentService
from tuling_research.scholar.models import PaperContentRequest, PaperContentResult

__all__ = ["PaperContentRequest", "PaperContentResult", "PaperContentService"]
