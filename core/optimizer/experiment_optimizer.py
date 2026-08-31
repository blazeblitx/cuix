"""
CUIX Task 11: Intervention Utility Optimizer & Benchmark Experiment
Evaluates objective utility selection against greedy highest-success-probability selection.
Enforces safety constraints and minimum performance improvement threshold.
"""

from typing import Dict, Any, List, Optional
from core.adaptive_layer.safety_policy import SafetyPolicyEngine

class EvaluatedOptimizer:
    def __init__(
        self,
        lambda_disruption: float = 0.35,
        lambda_cost: float = 0.15,
        min_improvement_threshold: float = 0.10
    ):
        self.lambda_disruption = lambda_disruption
        self.lambda_cost = lambda_cost
        self.min_improvement_threshold = min_improvement_threshold
        self.safety_engine = SafetyPolicyEngine()

    def compute_utility(self, candidate: Dict[str, Any]) -> float:
        gain = candidate.get('predicted_gain', 0.0)
        disruption = candidate.get('disruption', 0.0)
        cost = candidate.get('cost', 0.0)
        risk = candidate.get('risk', 0.0)

        utility = gain - (self.lambda_disruption * disruption) - (self.lambda_cost * cost) - risk
        return round(utility, 4)

    def select_utility_optimized_intervention(
        self, candidates: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        best_cand = None
        best_utility = -float('inf')

        for cand in candidates:
            # 1. Safety Policy Check
            safety_res = self.safety_engine.evaluate_intervention_safety(cand)
            if not safety_res['allowed']:
                continue

            # 2. Minimum Improvement Threshold Check
            gain = cand.get('predicted_gain', 0.0)
            if gain < self.min_improvement_threshold:
                continue

            # 3. Compute Objective Utility
            utility = self.compute_utility(cand)
            cand_copy = dict(cand)
            cand_copy['utility_score'] = utility

            if utility > best_utility:
                best_utility = utility
                best_cand = cand_copy

        return best_cand

    def run_strategy_comparison_experiment(
        self, candidates: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Compares:
        Strategy A: Naive Greedy Selection (Max raw success rate)
        Strategy B: CUIX Utility Optimizer (Minimum effective disruption)
        """
        # Strategy A: Max Success Rate
        valid_a = [c for c in candidates if self.safety_engine.evaluate_intervention_safety(c)['allowed']]
        greedy_selected = max(valid_a, key=lambda x: x.get('predicted_task_success_rate', 0.0)) if valid_a else None

        # Strategy B: CUIX Utility Optimizer
        utility_selected = self.select_utility_optimized_intervention(candidates)

        greedy_disruption = greedy_selected.get('disruption', 0.0) if greedy_selected else 0.0
        utility_disruption = utility_selected.get('disruption', 0.0) if utility_selected else 0.0

        disruption_reduction = round(greedy_disruption - utility_disruption, 3)

        return {
            "strategy_a_greedy": greedy_selected,
            "strategy_b_utility_optimizer": utility_selected,
            "experiment_metrics": {
                "greedy_disruption_cls": greedy_disruption,
                "utility_disruption_cls": utility_disruption,
                "disruption_reduction_pct": round((disruption_reduction / max(greedy_disruption, 0.01)) * 100.0, 1),
                "utility_optimization_successful": (utility_selected['utility_score'] >= (greedy_selected.get('predicted_gain', 0.0) - greedy_disruption) if (utility_selected and greedy_selected) else True)
            }
        }
