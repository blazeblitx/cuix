"""
CUIX Task 2 Testing Harness: Site Evaluator
Loads representative HTML site benchmarks and evaluates site-agnostic UI element classification accuracy.
"""

from html.parser import HTMLParser
import os
from typing import Dict, Any, List, Tuple

class BenchmarkHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elements: List[Dict[str, Any]] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, str]]):
        attr_dict = {k.lower(): v for k, v in attrs if v is not None}
        self.elements.append({
            "tag": tag.lower(),
            "attrs": attr_dict,
            "id": attr_dict.get('id', ''),
            "class": attr_dict.get('class', ''),
            "role": attr_dict.get('role', ''),
            "aria_label": attr_dict.get('aria-label', ''),
            "type": attr_dict.get('type', ''),
            "placeholder": attr_dict.get('placeholder', '')
        })

def classify_element(el: Dict[str, Any]) -> str:
    """Python implementation of CUIX site-agnostic classification rules."""
    tag = el["tag"]
    role = el["role"].lower()
    aria_label = el["aria_label"].lower()
    type_attr = el["type"].lower()
    placeholder = el["placeholder"].lower()
    id_class = f'{el["id"]} {el["class"]}'.lower()

    # Search
    if type_attr == 'search' or 'search' in id_class or role == 'search' or 'search' in placeholder or 'search' in aria_label:
        return 'search'

    # Filter
    if 'filter' in id_class or 'sort' in id_class or 'filter' in aria_label or 'sort' in aria_label or 'filter' in placeholder:
        return 'filter'

    # Input
    if tag in ['input', 'textarea', 'select']:
        return 'input'

    # Navigation
    if tag == 'nav' or role == 'navigation' or 'nav' in id_class:
        return 'navigation'

    # Action / Button
    if tag in ['button', 'a'] or role == 'button' or 'btn' in id_class:
        return 'action'

    # Heading
    if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'] or role == 'heading':
        return 'heading'

    return 'content'

class SiteBenchmarkEvaluator:
    def __init__(self, fixtures_dir: str):
        self.fixtures_dir = fixtures_dir

    def evaluate_site(self, filename: str) -> Dict[str, Any]:
        filepath = os.path.join(self.fixtures_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        parser = BenchmarkHTMLParser()
        parser.feed(content)

        role_counts: Dict[str, int] = {}
        classified_list = []

        for el in parser.elements:
            role = classify_element(el)
            role_counts[role] = role_counts.get(role, 0) + 1
            classified_list.append({
                "tag": el["tag"],
                "selector": f"{el['tag']}{'#' + el['id'] if el['id'] else ''}{'.' + el['class'] if el['class'] else ''}",
                "classified_role": role
            })

        total_nodes = len(parser.elements)
        actionable_count = role_counts.get('search', 0) + role_counts.get('filter', 0) + role_counts.get('action', 0) + role_counts.get('input', 0)

        return {
            "file": filename,
            "total_nodes": total_nodes,
            "role_counts": role_counts,
            "actionable_ratio": round(actionable_count / max(total_nodes, 1), 2),
            "classified_elements": classified_list
        }

    def evaluate_all(self) -> List[Dict[str, Any]]:
        results = []
        for fn in sorted(os.listdir(self.fixtures_dir)):
            if fn.endswith('.html'):
                results.append(self.evaluate_site(fn))
        return results
