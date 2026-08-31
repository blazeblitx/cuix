"""
CUIX Task 10: Reversible UI Interventions Engine
Implements 4 site-agnostic reversible UI adaptations adhering to a common BaseIntervention interface.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseIntervention(ABC):
    def __init__(
        self,
        intervention_id: str,
        target_selector: str,
        expected_benefit: float,
        modification_cost: float,
        disruption_estimate: float,
        risk_level: str = "LOW"
    ):
        self.intervention_id = intervention_id
        self.target_selector = target_selector
        self.expected_benefit = expected_benefit
        self.modification_cost = modification_cost
        self.disruption_estimate = disruption_estimate
        self.risk_level = risk_level

    @abstractmethod
    def get_payload(self) -> Dict[str, Any]:
        pass

class HighlightIntervention(BaseIntervention):
    def __init__(self, intervention_id: str, target_selector: str, expected_benefit: float = 0.28):
        super().__init__(
            intervention_id, target_selector,
            expected_benefit=expected_benefit,
            modification_cost=0.01,
            disruption_estimate=0.05,
            risk_level="LOW"
        )

    def get_payload(self) -> Dict[str, Any]:
        return {
            "id": self.intervention_id,
            "type": "HIGHLIGHT_ELEMENT",
            "targetSelector": self.target_selector,
            "cssClass": "cuix-adapted-highlight",
            "expected_benefit": self.expected_benefit,
            "cost": self.modification_cost,
            "disruption": self.disruption_estimate,
            "risk": 0.0
        }

class ProminenceIntervention(BaseIntervention):
    def __init__(self, intervention_id: str, target_selector: str, expected_benefit: float = 0.35):
        super().__init__(
            intervention_id, target_selector,
            expected_benefit=expected_benefit,
            modification_cost=0.05,
            disruption_estimate=0.15,
            risk_level="LOW"
        )

    def get_payload(self) -> Dict[str, Any]:
        return {
            "id": self.intervention_id,
            "type": "INCREASE_PROMINENCE",
            "targetSelector": self.target_selector,
            "styleMutations": {"font-weight": "bold", "transform": "scale(1.05)"},
            "expected_benefit": self.expected_benefit,
            "cost": self.modification_cost,
            "disruption": self.disruption_estimate,
            "risk": 0.0
        }

class ContextualHintIntervention(BaseIntervention):
    def __init__(self, intervention_id: str, target_selector: str, hint_text: str = "Try using this option", expected_benefit: float = 0.40):
        super().__init__(
            intervention_id, target_selector,
            expected_benefit=expected_benefit,
            modification_cost=0.08,
            disruption_estimate=0.25,
            risk_level="LOW"
        )
        self.hint_text = hint_text

    def get_payload(self) -> Dict[str, Any]:
        return {
            "id": self.intervention_id,
            "type": "CONTEXTUAL_HINT",
            "targetSelector": self.target_selector,
            "hintText": self.hint_text,
            "expected_benefit": self.expected_benefit,
            "cost": self.modification_cost,
            "disruption": self.disruption_estimate,
            "risk": 0.0
        }

class ShortcutOverlayIntervention(BaseIntervention):
    def __init__(self, intervention_id: str, target_selector: str, key_shortcut: str = "Alt+S", expected_benefit: float = 0.30):
        super().__init__(
            intervention_id, target_selector,
            expected_benefit=expected_benefit,
            modification_cost=0.02,
            disruption_estimate=0.02,
            risk_level="LOW"
        )
        self.key_shortcut = key_shortcut

    def get_payload(self) -> Dict[str, Any]:
        return {
            "id": self.intervention_id,
            "type": "ADAPTIVE_SHORTCUT",
            "targetSelector": self.target_selector,
            "keyShortcut": self.key_shortcut,
            "expected_benefit": self.expected_benefit,
            "cost": self.modification_cost,
            "disruption": self.disruption_estimate,
            "risk": 0.0
        }
