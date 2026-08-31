"""
CUIX Phase 2: Python Interface Graph Builder & Parser
Parses, queries, and analyzes site-agnostic UI graphs.
"""

from typing import Dict, Any, List, Optional
import json

class InterfaceGraphAnalyzer:
    def __init__(self, raw_graph_data: Dict[str, Any]):
        self.graph_data = raw_graph_data
        self.page_url: str = raw_graph_data.get('pageUrl', '')
        self.domain: str = raw_graph_data.get('domain', '')
        self.title: str = raw_graph_data.get('title', '')
        self.root: Dict[str, Any] = raw_graph_data.get('root', {})
        self.summary: Dict[str, int] = raw_graph_data.get('summary', {})

    @classmethod
    def from_json(cls, json_str: str) -> 'InterfaceGraphAnalyzer':
        return cls(json.loads(json_str))

    def find_nodes_by_role(self, target_role: str) -> List[Dict[str, Any]]:
        """Recursively retrieves all UI elements matching a specific role."""
        results: List[Dict[str, Any]] = []

        def traverse(node: Dict[str, Any]):
            if node.get('role') == target_role:
                results.append(node)
            for child in node.get('children', []):
                traverse(child)

        if self.root:
            traverse(self.root)
        return results

    def get_actionable_elements(self) -> List[Dict[str, Any]]:
        """Returns all buttons, links, search inputs, and filters."""
        actionable_roles = {'action', 'search', 'filter', 'input'}
        results: List[Dict[str, Any]] = []

        def traverse(node: Dict[str, Any]):
            if node.get('role') in actionable_roles:
                results.append(node)
            for child in node.get('children', []):
                traverse(child)

        if self.root:
            traverse(self.root)
        return results

    def compute_interface_complexity_score(self) -> float:
        """
        Calculates interface complexity based on visual visual clutter and node density.
        Score from 0.0 (Minimalist) to 1.0 (Highly Cluttered).
        """
        total_nodes = self.summary.get('totalNodes', 0)
        action_count = self.summary.get('actionCount', 0)
        
        # Heuristic calculation for interface visual load
        density_score = min(total_nodes / 500.0, 1.0)
        action_density = min(action_count / 100.0, 1.0)
        
        complexity = (0.6 * density_score) + (0.4 * action_density)
        return round(complexity, 3)
