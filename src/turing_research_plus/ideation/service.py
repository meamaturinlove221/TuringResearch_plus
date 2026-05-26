"""Creative Ideation workflow service."""

from __future__ import annotations

from tuling_research_plus.hypothesis.models import Hypothesis, HypothesisSet
from tuling_research_plus.ideation.diversity import quality_diversity_filter
from tuling_research_plus.ideation.generators import generate_cross_domain_ideas, generate_ideas
from tuling_research_plus.ideation.models import (
    DiversityFilterReport,
    IdeaGenerationResult,
    IdeaPortfolio,
    MorphologicalMatrix,
)
from tuling_research_plus.ideation.morphological_matrix import build_morphological_matrix


class CreativeIdeationService:
    """Generate diverse research idea candidates from hypotheses."""

    def idea_generate(self, hypothesis_set: HypothesisSet) -> IdeaGenerationResult:
        """Generate deterministic idea candidates."""

        return generate_ideas(hypothesis_set)

    def idea_cross_domain(
        self,
        hypothesis_set: HypothesisSet,
        domain: str = "software reliability",
    ) -> IdeaGenerationResult:
        """Generate deterministic cross-domain candidates."""

        return generate_cross_domain_ideas(hypothesis_set, domain=domain)

    def idea_morphological_matrix(self, hypothesis: Hypothesis) -> MorphologicalMatrix:
        """Build a morphological matrix."""

        return build_morphological_matrix(hypothesis)

    def idea_quality_diversity_filter(
        self,
        generation: IdeaGenerationResult,
    ) -> DiversityFilterReport:
        """Apply the quality-diversity gate."""

        return quality_diversity_filter(generation)

    def build_portfolio(self, hypothesis_set: HypothesisSet) -> IdeaPortfolio:
        """Generate and filter ideas into an artifact-shaped portfolio."""

        generation = self.idea_generate(hypothesis_set)
        diversity = self.idea_quality_diversity_filter(generation)
        return IdeaPortfolio(
            portfolio_id="idea-portfolio-1",
            topic=hypothesis_set.topic,
            ideas=diversity.retained,
            diversity_report=diversity,
        )

