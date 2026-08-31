"""
CUIX Task 3 Testing Harness: Multi-Signal Site Evaluator with Confidence Scoring
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

def classify_element_with_confidence(el: Dict[str, Any]) -> Tuple[str, float]:
    """Python implementation of Task 3 multi-signal classification with confidence score."""
    tag = el["tag"]
    role = el["role"].lower()
    aria_label = el["aria_label"].lower()
    type_attr = el["type"].lower()
    placeholder = el["placeholder"].lower()
    id_class = f'{el["id"]} {el["class"]}'.lower()

    # Search
    if type_attr == 'search' or 'search' in id_class or role == 'search' or 'search' in placeholder or 'search' in aria_label:
        conf = 0.70
        if type_attr == 'search': conf += 0.25
        if role == 'search': conf += 0.20
        return 'search', min(round(conf, 2), 0.98)

    # Filter
    if 'filter' in id_class or 'sort' in id_class or 'filter' in aria_label or 'sort' in aria_label or 'filter' in placeholder:
        conf = 0.65
        if 'filter' in aria_label or 'sort' in aria_label: conf += 0.25
        return 'filter', min(round(conf, 2), 0.95)

    # Input
    if tag in ['input', 'textarea', 'select']:
        return 'input', 0.92

    # Navigation
    if tag == 'nav' or role == 'navigation' or 'nav' in id_class:
        conf = 0.65
        if tag == 'nav': conf += 0.30
        return 'navigation', min(round(conf, 2), 0.98)

    # Action / Button
    if tag in ['button', 'a'] or role == 'button' or 'btn' in id_class:
        conf = 0.60
        if tag == 'button': conf += 0.35
        if role == 'button': conf += 0.25
        return 'action', min(round(conf, 2), 0.98)

    # Heading
    if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'] or role == 'heading':
        return 'heading', 0.95

    return 'content', 0.50

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
        conf_sum = 0.0

        for el in parser.elements:
            role, conf = classify_element_with_confidence(el)
            role_counts[role] = role_counts.get(role, 0) + 1
            conf_sum += conf
            classified_list.append({
                "tag": el["tag"],
                "selector": f"{el['tag']}{'#' + el['id'] if el['id'] else ''}{'.' + el['class'] if el['class'] else ''}",
                "classified_role": role,
                "confidence": conf
            })

        total_nodes = len(parser.elements)
        avg_conf = round(conf_sum / max(total_nodes, 1), 2)

        return {
            "file": filename,
            "total_nodes": total_nodes,
            "avg_confidence": avg_conf,
            "role_counts": role_counts,
            "classified_elements": classified_list
        }

    def evaluate_all(self) -> List[Dict[str, Any]]:
        results = []
        for fn in sorted(os.listdir(self.fixtures_dir)):
            if fn.endswith('.html'):
                results.append(self.evaluate_site(fn))
        return results
