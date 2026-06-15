"""
replay/discipline_checklist.py — DisciplineChecklistEngine for v1.2.2

[!] Research Only. No Real Orders. Replay Training Only.
[!] Checklist only records. No auto-scoring. No trading trigger.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Standard checklist items
# ---------------------------------------------------------------------------

STANDARD_DATA_ITEMS = [
    {"item_id": "DATA_01", "category": "DATA", "label": "Price data available", "required": True, "checked": False, "note": ""},
    {"item_id": "DATA_02", "category": "DATA", "label": "Point-in-time verified", "required": True, "checked": False, "note": ""},
    {"item_id": "DATA_03", "category": "DATA", "label": "Future firewall passed", "required": True, "checked": False, "note": ""},
    {"item_id": "DATA_04", "category": "DATA", "label": "Required dataset available", "required": True, "checked": False, "note": ""},
]

STANDARD_SETUP_ITEMS = [
    {"item_id": "SET_01", "category": "SETUP", "label": "Setup clearly identified", "required": True, "checked": False, "note": ""},
    {"item_id": "SET_02", "category": "SETUP", "label": "Confirmation condition written", "required": True, "checked": False, "note": ""},
    {"item_id": "SET_03", "category": "SETUP", "label": "Invalidation condition written", "required": True, "checked": False, "note": ""},
    {"item_id": "SET_04", "category": "SETUP", "label": "No-trade condition written", "required": False, "checked": False, "note": ""},
]

STANDARD_RISK_ITEMS = [
    {"item_id": "RSK_01", "category": "RISK", "label": "Position size planned", "required": True, "checked": False, "note": ""},
    {"item_id": "RSK_02", "category": "RISK", "label": "Stop plan written", "required": True, "checked": False, "note": ""},
    {"item_id": "RSK_03", "category": "RISK", "label": "Maximum loss considered", "required": True, "checked": False, "note": ""},
    {"item_id": "RSK_04", "category": "RISK", "label": "Event risk considered", "required": False, "checked": False, "note": ""},
    {"item_id": "RSK_05", "category": "RISK", "label": "Liquidity risk considered", "required": False, "checked": False, "note": ""},
]

STANDARD_EMOTION_ITEMS = [
    {"item_id": "EMO_01", "category": "EMOTION", "label": "Emotional state recorded", "required": True, "checked": False, "note": ""},
    {"item_id": "EMO_02", "category": "EMOTION", "label": "FOMO checked", "required": True, "checked": False, "note": ""},
    {"item_id": "EMO_03", "category": "EMOTION", "label": "Revenge risk checked", "required": True, "checked": False, "note": ""},
    {"item_id": "EMO_04", "category": "EMOTION", "label": "Loss aversion checked", "required": False, "checked": False, "note": ""},
    {"item_id": "EMO_05", "category": "EMOTION", "label": "Urgency checked", "required": False, "checked": False, "note": ""},
]

STANDARD_DISCIPLINE_ITEMS = [
    {"item_id": "DIS_01", "category": "DISCIPLINE", "label": "Not chasing", "required": True, "checked": False, "note": ""},
    {"item_id": "DIS_02", "category": "DISCIPLINE", "label": "Not panic selling", "required": True, "checked": False, "note": ""},
    {"item_id": "DIS_03", "category": "DISCIPLINE", "label": "Not buying back too early", "required": False, "checked": False, "note": ""},
    {"item_id": "DIS_04", "category": "DISCIPLINE", "label": "No unplanned size increase", "required": True, "checked": False, "note": ""},
    {"item_id": "DIS_05", "category": "DISCIPLINE", "label": "No decision solely from one indicator", "required": False, "checked": False, "note": ""},
]


class DisciplineChecklistEngine:
    """
    Engine for discipline checklists.

    [!] Checklist only records decisions. Does NOT auto-score trades.
    [!] required=True items WARN or BLOCK depending on item policy.
    [!] Never triggers orders.
    """

    no_real_orders = True
    research_only = True

    def __init__(self, templates_dir: Optional[str] = None, repo_root: Optional[str] = None):
        self._templates_dir = templates_dir
        self._repo_root = repo_root

    def load_checklist_template(self, name: str) -> List[Dict[str, Any]]:
        """Load checklist items from a template."""
        from replay.decision_templates import DecisionTemplateLibrary
        lib = DecisionTemplateLibrary(repo_root=self._repo_root)
        tmpl = lib.load_template(name)
        return tmpl.get("checklist_items", [])

    def build_default(
        self, action: str = "WATCH", setup_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Build default checklist for an action/setup combination."""
        items = []
        items.extend(STANDARD_DATA_ITEMS[:])
        items.extend(STANDARD_SETUP_ITEMS[:])
        items.extend(STANDARD_RISK_ITEMS[:])
        items.extend(STANDARD_EMOTION_ITEMS[:])
        items.extend(STANDARD_DISCIPLINE_ITEMS[:])
        return [dict(i) for i in items]  # fresh copy

    def get_standard_checklists(self) -> List[Dict[str, Any]]:
        """Return list of standard checklist definitions."""
        return [
            {"name": "default", "categories": ["DATA", "SETUP", "RISK", "EMOTION", "DISCIPLINE"]},
            {"name": "breakout", "categories": ["SETUP", "ENTRY", "RISK", "EMOTION", "DISCIPLINE"]},
            {"name": "pullback", "categories": ["SETUP", "ENTRY", "RISK", "EMOTION", "DISCIPLINE"]},
            {"name": "no_chase", "categories": ["DISCIPLINE", "EMOTION", "RISK"]},
            {"name": "risk_reduction", "categories": ["RISK", "DISCIPLINE", "EMOTION", "EXIT"]},
        ]

    def validate_items(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate checklist items format."""
        errors = []
        for i, item in enumerate(items):
            if "item_id" not in item:
                errors.append(f"Item {i} missing item_id")
            if "label" not in item and "text" not in item:
                errors.append(f"Item {i} missing label/text")
        return {"valid": len(errors) == 0, "errors": errors}

    def complete_item(
        self, items: List[Dict[str, Any]], item_id: str, checked: bool, note: str = ""
    ) -> List[Dict[str, Any]]:
        """Mark a checklist item as checked/unchecked."""
        updated = []
        for item in items:
            new_item = dict(item)
            if new_item.get("item_id") == item_id:
                new_item["checked"] = checked
                new_item["note"] = note
            updated.append(new_item)
        return updated

    def calculate_completion(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate completion stats."""
        total = len(items)
        checked = sum(1 for i in items if i.get("checked", False))
        required = [i for i in items if i.get("required", False)]
        required_passed = sum(1 for i in required if i.get("checked", False))
        return {
            "total_count": total,
            "completed_count": checked,
            "passed_count": checked,
            "required_count": len(required),
            "required_passed": required_passed,
            "all_required_passed": required_passed == len(required),
            "completion_rate": (checked / total) if total > 0 else 0.0,
        }

    def required_passed(self, items: List[Dict[str, Any]]) -> bool:
        """Return True if all required items are checked."""
        required = [i for i in items if i.get("required", False)]
        if not required:
            return True
        return all(i.get("checked", False) for i in required)

    def blocking_items(self, items: List[Dict[str, Any]]) -> List[str]:
        """Return item IDs of required items not checked."""
        return [
            i.get("item_id", "?")
            for i in items
            if i.get("required", False) and not i.get("checked", False)
        ]

    def summary(self, items: List[Dict[str, Any]]) -> str:
        """Return human-readable summary."""
        stats = self.calculate_completion(items)
        return (
            f"Checklist: {stats['completed_count']}/{stats['total_count']} checked, "
            f"Required: {stats['required_passed']}/{stats['required_count']} passed"
        )

    def evaluate_checklist(
        self,
        items: List[Dict[str, Any]],
        responses: Dict[str, bool],
        session_id: str = "",
        decision_id: str = "",
        checklist_name: str = "",
    ) -> "DisciplineChecklistResult":
        """Evaluate checklist items with responses and return a result."""
        from replay.decision_journal_schema import DisciplineChecklistResult

        updated_items = []
        for item in items:
            new_item = dict(item)
            item_id = item.get("item_id", "")
            if item_id in responses:
                new_item["checked"] = bool(responses[item_id])
            updated_items.append(new_item)

        stats = self.calculate_completion(updated_items)
        blocking = self.blocking_items(updated_items)
        warnings = [f"Required item not checked: {bid}" for bid in blocking]

        return DisciplineChecklistResult(
            checklist_id=f"CHK-{uuid.uuid4().hex[:12].upper()}",
            session_id=session_id,
            decision_id=decision_id,
            checklist_name=checklist_name,
            items=updated_items,
            passed_count=stats["passed_count"],
            total_count=stats["total_count"],
            completed_count=stats["completed_count"],
            all_required_passed=stats["all_required_passed"],
            passed=stats["all_required_passed"],
            warnings=warnings,
            blocked_items=blocking,
            simulation_only=True,
            research_only=True,
            no_real_orders=True,
        )


# Backward-compat alias from spec
ReplayDisciplineChecklist = DisciplineChecklistEngine
