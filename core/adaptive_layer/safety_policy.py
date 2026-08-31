"""
CUIX Task 9: Intervention Safety Policy Engine & Element Risk Classifier
Classifies UI target elements into LOW, MEDIUM, or PROHIBITED risk levels.
Strictly prohibits automatic DOM modification of authentication, payment, security, consent, legal, and destructive controls.
"""

from typing import Dict, Any, List, Tuple
import re

PROHIBITED_SELECTORS_REGEX = [
    r'password', r'autocomplete.*cc', r'cvv', r'card.*number', r'ssn',
    r'stripe', r'paypal', r'2fa', r'captcha', r'terms.*agree',
    r'delete', r'remove.*account', r'pay.*now', r'checkout.*submit'
]

MEDIUM_RISK_SELECTORS_REGEX = [
    r'reposition', r'form.*reorder', r'modal.*trigger', r'navigation.*override'
]

class ElementRiskClassifier:
    def classify_target_risk(self, selector: str, tag: str = "", text: str = "") -> str:
        """Classifies target element into 'PROHIBITED', 'MEDIUM', or 'LOW' risk level."""
        combined_string = f"{selector} {tag} {text}".lower()

        # 1. Prohibited Risk Check
        for pattern in PROHIBITED_SELECTORS_REGEX:
            if re.search(pattern, combined_string):
                return "PROHIBITED"

        # 2. Medium Risk Check
        for pattern in MEDIUM_RISK_SELECTORS_REGEX:
            if re.search(pattern, combined_string):
                return "MEDIUM"

        return "LOW"

class SafetyPolicyEngine:
    def __init__(self):
        self.risk_classifier = ElementRiskClassifier()
        self.audit_logs: List[Dict[str, Any]] = []

    def evaluate_intervention_safety(
        self, candidate: Dict[str, Any]
    ) -> Dict[str, Any]:
        selector = candidate.get('targetSelector', 'body')
        tag = candidate.get('target_tag', '')
        text = candidate.get('target_text', '')

        risk_level = self.risk_classifier.classify_target_risk(selector, tag, text)

        allowed = False
        requires_user_confirmation = False
        rejection_reason = None

        if risk_level == "PROHIBITED":
            allowed = False
            rejection_reason = f"Prohibited Target: Proximity to authentication, payment, security, or destructive action ({selector})."
        elif risk_level == "MEDIUM":
            allowed = True
            requires_user_confirmation = True
        else:
            allowed = True
            requires_user_confirmation = False

        decision = {
            "candidate_id": candidate.get("id", "cand_1"),
            "targetSelector": selector,
            "risk_level": risk_level,
            "allowed": allowed,
            "requires_user_confirmation": requires_user_confirmation,
            "rejection_reason": rejection_reason
        }

        self.audit_logs.append(decision)
        return decision
