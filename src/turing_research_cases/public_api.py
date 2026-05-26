"""Public API facade for case-study and demo modules."""

from turing_research_plus.benchmark import (
    BenchmarkReport,
    BenchmarkScenario,
    run_benchmark_scenario,
)
from turing_research_plus.case_study import (
    CaseStudyClaimSafetyReport,
    CaseStudyDraft,
    CaseStudyRedactionReport,
    build_vggt_public_case_study,
)

NAMESPACE = "turing_research_cases"
COMPATIBILITY_NAMESPACE = "turing_research_plus"
STABILITY = "experimental"
PUBLIC_MODULE_ALIASES = {
    "benchmark": "turing_research_plus.benchmark",
    "case_study": "turing_research_plus.case_study",
    "public_demo": "examples/public_demo",
}

__all__ = [
    "COMPATIBILITY_NAMESPACE",
    "NAMESPACE",
    "PUBLIC_MODULE_ALIASES",
    "STABILITY",
    "BenchmarkReport",
    "BenchmarkScenario",
    "CaseStudyClaimSafetyReport",
    "CaseStudyDraft",
    "CaseStudyRedactionReport",
    "build_vggt_public_case_study",
    "run_benchmark_scenario",
]
