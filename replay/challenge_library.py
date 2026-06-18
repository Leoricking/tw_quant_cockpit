"""
replay/challenge_library.py — ReplayChallengeLibrary v1.2.7

[!] Challenge Training Only. Simulation Only. No Real Orders. Not Investment Advice.
[!] Built-in templates never permanently deleted.
[!] Import default dry-run; execute requires --execute --allow-write.
"""
from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayChallengeLibrary:
    """
    Library of replay challenge definitions.

    Built-in templates are always available and never permanently deleted.
    User-created challenges can be archived (non-destructive).
    Import is dry-run by default; requires --execute --allow-write to write.

    [!] Challenge Training Only. Simulation Only. No Real Orders.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    BUILTIN_PROTECTED = True

    def __init__(self) -> None:
        from replay.challenge_template import CHALLENGE_TEMPLATES
        self._builtin: Dict[str, Dict[str, Any]] = {
            t["template_id"]: dict(t) for t in CHALLENGE_TEMPLATES
        }
        self._user: Dict[str, Dict[str, Any]] = {}

    # ------------------------------------------------------------------
    # Read operations
    # ------------------------------------------------------------------

    def list_challenges(self, include_archived: bool = False) -> List[Dict[str, Any]]:
        """List all challenges (built-in + user)."""
        result = []
        for tid, t in self._builtin.items():
            result.append({"source": "builtin", **t})
        for cid, c in self._user.items():
            if include_archived or not c.get("archived", False):
                result.append({"source": "user", **c})
        return result

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search challenges by title/description/type."""
        q = query.lower()
        return [
            c for c in self.list_challenges()
            if q in c.get("title", "").lower()
            or q in c.get("description", "").lower()
            or q in c.get("challenge_type", "").lower()
            or q in c.get("template_id", "").lower()
        ]

    def filter_by_type(self, challenge_type: str) -> List[Dict[str, Any]]:
        return [
            c for c in self.list_challenges()
            if c.get("challenge_type") == challenge_type
            or c.get("template_id", "").startswith(challenge_type)
        ]

    def filter_by_difficulty(self, difficulty: str) -> List[Dict[str, Any]]:
        return [
            c for c in self.list_challenges()
            if c.get("difficulty") == difficulty
        ]

    def show(self, challenge_id: str) -> Optional[Dict[str, Any]]:
        """Return challenge by ID or template_id."""
        if challenge_id in self._builtin:
            return dict(self._builtin[challenge_id])
        if challenge_id in self._user:
            return dict(self._user[challenge_id])
        # Search by challenge_id field
        for c in self._user.values():
            if c.get("challenge_id") == challenge_id:
                return dict(c)
        return None

    # ------------------------------------------------------------------
    # Write operations
    # ------------------------------------------------------------------

    def create(self, definition: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user challenge definition."""
        from replay.challenge_schema import _new_id, _now_utc
        cid = definition.get("challenge_id") or _new_id("CHG-")
        definition["challenge_id"] = cid
        definition["research_only"] = True
        definition["no_real_orders"] = True
        definition["created_at"] = definition.get("created_at") or _now_utc()
        definition["archived"] = False
        self._user[cid] = definition
        return {"status": "CREATED", "challenge_id": cid}

    def duplicate(self, challenge_id: str) -> Dict[str, Any]:
        """Duplicate an existing challenge."""
        from replay.challenge_schema import _new_id, _now_utc
        src = self.show(challenge_id)
        if src is None:
            return {"status": "NOT_FOUND", "challenge_id": challenge_id}
        new_def = dict(src)
        new_def["challenge_id"] = _new_id("CHG-")
        new_def["title"] = f"Copy of {src.get('title', challenge_id)}"
        new_def["created_at"] = _now_utc()
        new_def["archived"] = False
        new_def["source"] = "user"
        cid = new_def["challenge_id"]
        self._user[cid] = new_def
        return {"status": "DUPLICATED", "challenge_id": cid, "source": challenge_id}

    def archive(self, challenge_id: str) -> Dict[str, Any]:
        """Archive a user challenge (built-in cannot be archived)."""
        if challenge_id in self._builtin:
            return {"status": "PROTECTED", "message": "Built-in templates cannot be archived"}
        if challenge_id not in self._user:
            return {"status": "NOT_FOUND", "challenge_id": challenge_id}
        self._user[challenge_id]["archived"] = True
        return {"status": "ARCHIVED", "challenge_id": challenge_id}

    def restore(self, challenge_id: str) -> Dict[str, Any]:
        """Restore an archived user challenge."""
        if challenge_id not in self._user:
            return {"status": "NOT_FOUND", "challenge_id": challenge_id}
        self._user[challenge_id]["archived"] = False
        return {"status": "RESTORED", "challenge_id": challenge_id}

    def validate(self, challenge_id: str) -> Dict[str, Any]:
        """Validate a challenge definition."""
        c = self.show(challenge_id)
        if c is None:
            return {"status": "NOT_FOUND", "challenge_id": challenge_id}
        errors = []
        warnings = []
        if not c.get("title"):
            errors.append("title required")
        if not c.get("challenge_type"):
            errors.append("challenge_type required")
        pw = c.get("process_weight", 0.80)
        ow = c.get("outcome_weight", 0.20)
        if pw < ow:
            errors.append("process_weight must be >= outcome_weight")
        if ow > 0.20:
            errors.append("outcome_weight max 0.20")
        return {
            "challenge_id": challenge_id,
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "research_only": True,
            "no_real_orders": True,
        }

    def import_preview(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Preview import (dry-run). Does not write."""
        errors = []
        if not data.get("title"):
            errors.append("title required")
        return {
            "status": "PREVIEW",
            "dry_run": True,
            "valid": len(errors) == 0,
            "errors": errors,
            "message": "Use import_execute(allow_write=True) to write",
            "research_only": True,
            "no_real_orders": True,
        }

    def import_execute(self, data: Dict[str, Any], allow_write: bool = False) -> Dict[str, Any]:
        """Execute import. Requires allow_write=True."""
        if not allow_write:
            return {
                "status": "BLOCKED",
                "message": "import_execute requires allow_write=True",
                "dry_run": True,
            }
        return self.create(data)

    def export_preview(self, challenge_id: str) -> Dict[str, Any]:
        """Preview export without writing."""
        c = self.show(challenge_id)
        if c is None:
            return {"status": "NOT_FOUND"}
        # Strip any sensitive or answer-key fields
        safe = {k: v for k, v in c.items() if k not in (
            "answer_key", "forward_return", "realized_pnl", "outcome_score"
        )}
        return {
            "status": "PREVIEW",
            "challenge_id": challenge_id,
            "data": safe,
            "research_only": True,
            "no_real_orders": True,
        }

    def summary(self) -> Dict[str, Any]:
        total_builtin = len(self._builtin)
        total_user = len(self._user)
        archived_user = sum(1 for c in self._user.values() if c.get("archived"))
        return {
            "total_challenges": total_builtin + total_user,
            "builtin": total_builtin,
            "user_total": total_user,
            "user_active": total_user - archived_user,
            "user_archived": archived_user,
            "research_only": True,
            "no_real_orders": True,
            "public_leaderboard_enabled": False,
            "network_submission_enabled": False,
        }
