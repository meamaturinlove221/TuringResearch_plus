"""Public API facade for experiment workflow modules."""

from turing_research_plus.experiment_route import ExperimentRouteSpec, compile_experiment_route
from turing_research_plus.failure import FailureAttributionReport
from turing_research_plus.hard_gates import HardGateValidationReport, validate_hard_gates

NAMESPACE = "turing_research_experiment"
COMPATIBILITY_NAMESPACE = "turing_research_plus"
STABILITY = "beta"
PUBLIC_MODULE_ALIASES = {
    "experiment_route": "turing_research_plus.experiment_route",
    "hard_gates": "turing_research_plus.hard_gates",
    "failure": "turing_research_plus.failure",
    "run_compare": "turing_research_plus.run_compare",
}

__all__ = [
    "COMPATIBILITY_NAMESPACE",
    "NAMESPACE",
    "PUBLIC_MODULE_ALIASES",
    "STABILITY",
    "ExperimentRouteSpec",
    "FailureAttributionReport",
    "HardGateValidationReport",
    "compile_experiment_route",
    "validate_hard_gates",
]
