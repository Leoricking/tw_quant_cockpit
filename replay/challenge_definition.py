"""
replay/challenge_definition.py — ChallengeDefinitionManager v1.2.7

[!] Challenge Training Only. Simulation Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ChallengeDefinitionManager:
    """
    Load, save, validate, and archive challenge definitions.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self) -> None:
        self._definitions: Dict[str, Dict[str, Any]] = {}

    def load(self, challenge_id: str) -> Optional[Dict[str, Any]]:
        """Load a challenge definition by ID."""
        return self._definitions.get(challenge_id)

    def save(self, definition: Dict[str, Any]) -> Dict[str, Any]:
        """Save a challenge definition."""
        cid = definition.get("challenge_id", "")
        if not cid:
            return {"status": "ERROR", "message": "challenge_id required"}
        definition["research_only"] = True
        definition["no_real_orders"] = True
        self._definitions[cid] = definition
        return {"status": "OK", "challenge_id": cid}

    def validate(self, definition: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a challenge definition."""
        warnings: List[str] = []
        errors: List[str] = []
        if not definition.get("title"):
            errors.append("title is required")
        if not definition.get("challenge_type"):
            errors.append("challenge_type is required")
        pw = definition.get("process_weight", 0.80)
        ow = definition.get("outcome_weight", 0.20)
        if pw < ow:
            errors.append("process_weight must be >= outcome_weight")
        if ow > 0.20:
            errors.append("outcome_weight max 0.20")
        if not definition.get("research_only", True):
            errors.append("research_only must be True")
        if definition.get("no_real_orders") is False:
            errors.append("no_real_orders must be True")
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "research_only": True,
            "no_real_orders": True,
        }

    def archive(self, challenge_id: str) -> Dict[str, Any]:
        """Archive a challenge definition (non-destructive)."""
        if challenge_id not in self._definitions:
            return {"status": "NOT_FOUND", "challenge_id": challenge_id}
        self._definitions[challenge_id]["archived"] = True
        return {"status": "ARCHIVED", "challenge_id": challenge_id}

    def list_all(self) -> List[Dict[str, Any]]:
        """List all definitions."""
        return list(self._definitions.values())

    def summary(self) -> Dict[str, Any]:
        total = len(self._definitions)
        archived = sum(1 for d in self._definitions.values() if d.get("archived"))
        return {
            "total": total,
            "active": total - archived,
            "archived": archived,
            "research_only": True,
            "no_real_orders": True,
        }
