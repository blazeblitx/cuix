"""
CUIX Task 4: Gemini Semantic Interface Analyzer & Validation Guardrail
Provides LLM-assisted semantic UI classification ONLY when deterministic DOM/A11y confidence < 0.70.
Enforces strict JSON schema validation and safety bounds.
"""

import json
import os
import urllib.request
from typing import Dict, Any, Optional

ALLOWED_ROLES = {'navigation', 'search', 'filter', 'action', 'input', 'form', 'menu', 'heading', 'content'}

class GeminiInterfaceAnalyzer:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get('GEMINI_API_KEY')

    def sanitize_node_representation(self, node: Dict[str, Any]) -> Dict[str, Any]:
        """Strips raw text payloads, input contents, and sensitive attributes."""
        return {
            "tag": node.get("tag", "div"),
            "selector": node.get("selector", ""),
            "ariaLabel": node.get("ariaLabel", ""),
            "boundingBox": node.get("boundingBox", {}),
            "children_count": len(node.get("children", []))
        }

    def validate_llm_response(self, raw_response: str) -> Dict[str, Any]:
        """Guards against malformed or hallucinated LLM output."""
        try:
            parsed = json.loads(raw_response)
        except Exception:
            return {"valid": False, "role": "content", "confidence": 0.50, "reason": "JSON_PARSE_ERROR"}

        role = str(parsed.get("role", "")).lower()
        confidence = float(parsed.get("confidence", 0.0))

        if role not in ALLOWED_ROLES:
            return {"valid": False, "role": "content", "confidence": 0.50, "reason": "INVALID_ROLE"}

        confidence = max(0.0, min(1.0, confidence))
        return {
            "valid": True,
            "role": role,
            "confidence": round(confidence, 2),
            "reasoning": str(parsed.get("reasoning", "Validated Gemini analysis"))
        }

    def analyze_ambiguous_node(self, node: Dict[str, Any]) -> Dict[str, Any]:
        """Analyzes low-confidence node using Gemini API if key is present, or deterministic fallback."""
        sanitized = self.sanitize_node_representation(node)

        if not self.api_key:
            # Deterministic fallback when Gemini API key is unconfigured
            tag = sanitized["tag"]
            if tag in ['button', 'a']:
                fallback_role = 'action'
            elif tag in ['input', 'select']:
                fallback_role = 'input'
            else:
                fallback_role = 'content'

            return {
                "valid": True,
                "role": fallback_role,
                "confidence": 0.75,
                "source": "DETERMINISTIC_FALLBACK",
                "reasoning": "Gemini API key unconfigured; applied fallback validator."
            }

        # Live Gemini API call if key is set
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
            prompt = (
                "You are an interface classification engine. Analyze this sanitized UI element node:\n"
                f"{json.dumps(sanitized)}\n\n"
                "Respond ONLY with a JSON object in this exact schema:\n"
                '{"role": "<search|filter|navigation|action|input|heading|content>", "confidence": <float 0.0-1.0>, "reasoning": "<short string>"}'
            )
            req_body = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode('utf-8')
            req = urllib.request.Request(url, data=req_body, headers={'Content-Type': 'application/json'})
            
            with urllib.request.urlopen(req, timeout=5) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                text_out = result['candidates'][0]['content']['parts'][0]['text']
                validated = self.validate_llm_response(text_out)
                validated['source'] = 'GEMINI_LIVE_API'
                return validated
        except Exception as e:
            return {
                "valid": False,
                "role": "content",
                "confidence": 0.50,
                "source": "GEMINI_ERROR",
                "reasoning": f"Gemini API invocation error: {str(e)}"
            }
