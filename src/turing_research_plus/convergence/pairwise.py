"""Pairwise ranking for convergence candidates."""

from __future__ import annotations

from tuling_research_plus.convergence.models import CandidateScore, PairwisePreference


def pairwise_rank(scores: list[CandidateScore]) -> list[PairwisePreference]:
    """Compare every candidate pair by total score."""

    preferences: list[PairwisePreference] = []
    for left_index, left in enumerate(scores):
        for right in scores[left_index + 1:]:
            if left.total_score >= right.total_score:
                winner = left
                loser = right
            else:
                winner = right
                loser = left
            preferences.append(
                PairwisePreference(
                    left_id=left.candidate_id,
                    right_id=right.candidate_id,
                    winner_id=winner.candidate_id,
                    margin=round(abs(left.total_score - right.total_score), 3),
                    rationale=f"{winner.candidate_id} outranks {loser.candidate_id} by score.",
                )
            )
    return preferences

