from turing_research_plus.failure.models import FailureCategory
from turing_research_plus.failure.taxonomy import default_failure_taxonomy


def test_default_taxonomy_contains_required_categories() -> None:
    taxonomy = default_failure_taxonomy()

    assert set(FailureCategory) <= set(taxonomy)
    assert taxonomy[FailureCategory.MISSING_ASSETS].default_next_actions


def test_sparse_backend_unavailable_is_critical() -> None:
    entry = default_failure_taxonomy()[FailureCategory.SPARSE_BACKEND_UNAVAILABLE]

    assert entry.severity == "critical"
