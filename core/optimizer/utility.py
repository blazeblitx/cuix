"""
CUIX Intervention Utility Optimizer (Phase 10)
Calculates net utility for candidate adaptations:
Utility = Gain - Disruption - ModificationCost - Risk
"""

from typing import Dict, Any, List

class InterventionOptimizer:
    def __init__(self, lambda_disruption: float = 0.35, lambda_cost: float = 0.15):
        self.lambda_disruption = lambda_disruption
        self.lambda_cost = lambda_cost

    def evaluate_candidate(
        self,
        predicted_performance_gain: float,  # e.g. +0.25 task speedup
        disruption_score: float,            # Visual shift CLS [0.0 - 1.0]
        modification_cost: float,           # DOM DOM mutations cost
        risk_penalty: float                 # Proximity to auth/destructive controls
    ) -> float:
        """
        Computes Objective Utility score for candidate adaptation.
        """
        utility = (
            predicted_performance_gain
            - (self.lambda_disruption * disruption_score)
            - (self.lambda_cost * modification_cost)
            - risk_penalty
        )
        return round(utility, 4)

    def select_best_intervention(
        self, candidates: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Returns candidate adaptation that maximizes Objective Utility."""
        best_candidate = None
        best_score = -float('inf')

        for candidate in candidates:
            score = self.evaluate_candidate(
                predicted_performance_gain=candidate.get('predicted_gain', 0.0),
                disruption_score=candidate.get('disruption', 0.0),
                modification_cost=candidate.get('cost', 0.0),
                risk_penalty=candidate.get('risk', 0.0)
            )
            candidate['utility_score'] = score
            if score > best_score:
                best_score = score
                best_candidate = candidate

        return best_candidate or {}
