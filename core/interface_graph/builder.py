"""
CUIX Task 3 & Task 4: Python Interface Graph Builder & Gemini Fallback Pipeline
Parses site-agnostic UI graphs and routes low-confidence elements (< 0.70) to Gemini Semantic Analyzer.
"""

from typing import Dict, Any, List, Optional
import json
from core.interface_graph.gemini_analyzer import GeminiInterfaceAnalyzer

class InterfaceGraphAnalyzer:
    def __init__(self, raw_graph_data: Dict[str, Any], gemini_analyzer: Optional[GeminiInterfaceAnalyzer] = None):
        self.graph_data = raw_graph_data
        self.page_url: str = raw_graph_data.get('pageUrl', '')
        self.domain: str = raw_graph_data.get('domain', '')
        self.title: str = raw_graph_data.get('title', '')
        self.root: Dict[str, Any] = raw_graph_data.get('root', {})
        self.summary: Dict[str, Any] = raw_graph_data.get('summary', {})
        self.gemini = gemini_analyzer or GeminiInterfaceAnalyzer()

    @classmethod
    def from_json(cls, json_str: str) -> 'InterfaceGraphAnalyzer':
        return cls(json.loads(json_str))

    def resolve_element_role_with_fallback(self, node: Dict[str, Any]) -> Dict[str, Any]:
        """
        Task 4 Architecture:
        DOM/A11y Confidence >= 0.70?
        YES -> Use deterministic classification
        NO  -> Route to Gemini Semantic Analyzer
        """
        role = node.get('role', 'content')
        conf = float(node.get('confidence', 0.50))

        if conf >= 0.70:
            return {
                "role": role,
                "confidence": conf,
                "source": "DETERMINISTIC_DOM_A11Y"
            }

        # Fallback to Gemini
        gemini_res = self.gemini.analyze_ambiguous_node(node)
        if gemini_res.get('valid'):
            return {
                "role": gemini_res.get('role', role),
                "confidence": gemini_res.get('confidence', conf),
                "source": gemini_res.get('source', 'GEMINI')
            }

        return {"role": role, "confidence": conf, "source": "FALLBACK_UNMODIFIED"}

    def find_nodes_by_role(self, target_role: str, min_confidence: float = 0.0) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []

        def traverse(node: Dict[str, Any]):
            resolved = self.resolve_element_role_with_fallback(node)
            if resolved['role'] == target_role and resolved['confidence'] >= min_confidence:
                item = dict(node)
                item['role'] = resolved['role']
                item['confidence'] = resolved['confidence']
                item['classification_source'] = resolved['source']
                results.append(item)
            for child in node.get('children', []):
                traverse(child)

        if self.root:
            traverse(self.root)
        return results

    def get_actionable_elements(self, min_confidence: float = 0.60) -> List[Dict[str, Any]]:
        actionable_roles = {'action', 'search', 'filter', 'input'}
        results: List[Dict[str, Any]] = []

        def traverse(node: Dict[str, Any]):
            resolved = self.resolve_element_role_with_fallback(node)
            if resolved['role'] in actionable_roles and resolved['confidence'] >= min_confidence:
                item = dict(node)
                item['role'] = resolved['role']
                item['confidence'] = resolved['confidence']
                item['classification_source'] = resolved['source']
                results.append(item)
            for child in node.get('children', []):
                traverse(child)

        if self.root:
            traverse(self.root)
        return results

    def compute_interface_complexity_score(self) -> float:
        total_nodes = self.summary.get('totalNodes', 0)
        action_count = self.summary.get('actionCount', 0)
        density_score = min(total_nodes / 500.0, 1.0)
        action_density = min(action_count / 100.0, 1.0)
        complexity = (0.6 * density_score) + (0.4 * action_density)
        return round(complexity, 3)
