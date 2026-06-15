"""
replay/decision_templates.py — DecisionTemplateLibrary for v1.2.2

[!] Research Only. No Real Orders. Replay Training Only.
[!] Templates never contain future answers, realized returns, or labels.
"""
from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class DecisionTemplateLibrary:
    """
    Library of decision journal templates.

    Templates are loaded from replay/journal_templates/*.json.
    [!] Templates must not contain future answers or performance data.
    """

    no_real_orders = True
    research_only = True

    BUILTIN_TEMPLATES = [
        "free_form", "breakout", "pullback", "bottom_reversal",
        "no_chase", "risk_reduction", "exit_review", "wait_confirmation",
    ]

    def __init__(self, templates_dir: Optional[str] = None, repo_root: Optional[str] = None):
        if templates_dir:
            self._templates_dir = Path(templates_dir)
        elif repo_root:
            self._templates_dir = Path(repo_root) / "replay" / "journal_templates"
        else:
            base = Path(os.path.dirname(os.path.abspath(__file__)))
            self._templates_dir = base / "journal_templates"

        self._cache: Dict[str, Dict[str, Any]] = {}

    def list_templates(self) -> List[str]:
        """List all available template names."""
        names = []
        if self._templates_dir.exists():
            for f in sorted(self._templates_dir.glob("*.json")):
                names.append(f.stem)
        else:
            names = list(self.BUILTIN_TEMPLATES)
        return names

    def load_template(self, template_name: str) -> Dict[str, Any]:
        """Load a template by name."""
        if template_name in self._cache:
            return self._cache[template_name]

        path = self._templates_dir / f"{template_name}.json"
        if not path.exists():
            logger.warning("[DecisionTemplateLibrary] Template not found: %s", template_name)
            return self._get_fallback_template(template_name)

        try:
            with open(path, "r", encoding="utf-8") as f:
                tmpl = json.load(f)
            self._cache[template_name] = tmpl
            return tmpl
        except Exception as exc:
            logger.error("[DecisionTemplateLibrary] Failed to load template %s: %s", template_name, exc)
            return self._get_fallback_template(template_name)

    def get_template(self, template_id: str) -> Dict[str, Any]:
        """Get template by ID (alias for load_template)."""
        return self.load_template(template_id)

    def apply_template(
        self, template_id: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Apply template to get a pre-filled journal entry structure."""
        tmpl = self.load_template(template_id)
        result = {
            "template_name": tmpl.get("template_name", template_id),
            "setup_type": tmpl.get("setup_type", "FREE_FORM"),
            "time_horizon": tmpl.get("time_horizon", "UNDEFINED"),
            "checklist_items": tmpl.get("checklist_items", []),
            "pre_decision_prompts": tmpl.get("pre_decision_prompts", []),
            "post_decision_prompts": tmpl.get("post_decision_prompts", []),
            "simulation_only": True,
        }
        if context:
            result.update({k: v for k, v in context.items() if k not in ("simulation_only",)})
        return result

    def validate_template(self, template_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a template dict."""
        errors = []
        warnings = []

        FORBIDDEN_TEMPLATE_FIELDS = [
            "future_return", "outcome", "final_label", "answer",
            "realized_pnl", "broker", "order_token", "api_key", "secret",
        ]

        if "template_name" not in template_dict:
            errors.append("Missing template_name")
        if not template_dict.get("simulation_only", True):
            errors.append("simulation_only must be True")

        for fld in FORBIDDEN_TEMPLATE_FIELDS:
            if fld in template_dict:
                errors.append(f"Forbidden field in template: {fld}")

        return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}

    def duplicate_template(self, template_name: str, new_name: str) -> Dict[str, Any]:
        """Duplicate a template with a new name."""
        tmpl = self.load_template(template_name)
        new_tmpl = dict(tmpl)
        new_tmpl["template_name"] = new_name
        return new_tmpl

    def custom_template(
        self,
        template_name: str,
        setup_type: str = "FREE_FORM",
        checklist_items: Optional[List[Dict[str, Any]]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a custom template."""
        return {
            "template_name": template_name,
            "display_name": kwargs.get("display_name", template_name),
            "setup_type": setup_type,
            "time_horizon": kwargs.get("time_horizon", "UNDEFINED"),
            "checklist_items": checklist_items or [],
            "pre_decision_prompts": kwargs.get("pre_decision_prompts", []),
            "post_decision_prompts": kwargs.get("post_decision_prompts", []),
            "simulation_only": True,
        }

    def _get_fallback_template(self, template_name: str) -> Dict[str, Any]:
        """Return a minimal fallback template."""
        return {
            "template_name": template_name,
            "display_name": template_name.replace("_", " ").title(),
            "setup_type": "FREE_FORM",
            "time_horizon": "UNDEFINED",
            "checklist_items": [],
            "pre_decision_prompts": ["What is your observation?"],
            "post_decision_prompts": ["What did you decide?"],
            "simulation_only": True,
        }
