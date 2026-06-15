"""
replay/decision_revision.py — DecisionRevisionEngine for v1.2.2

[!] Research Only. No Real Orders. Replay Training Only.
[!] Revisions are APPEND-ONLY. Never overwrite original entry.
[!] Archived entries BLOCKED from revision until restored.
[!] Confidence before/after preserved. Stop/Target revision requires reason.
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


class DecisionRevisionEngine:
    """
    Engine for creating and managing append-only decision revisions.

    Rules:
    - Never overwrites original entry
    - Creates DREV- revision record
    - Confidence: before/after preserved
    - stop/target revision: reason required
    - Archived entries: BLOCKED until restored
    """

    no_real_orders = True
    research_only = True

    REVISION_ID_PREFIX = "DREV-"

    REQUIRES_REASON_FIELDS = ["stop_price", "target_price", "action", "confidence"]

    def create_revision(
        self,
        entry: Dict[str, Any],
        reason: str,
        field_changes: Dict[str, Any],
    ) -> "DecisionRevisionRecord":
        """
        Create a revision record for a journal entry.
        [!] Append-only. Does NOT overwrite original.
        [!] ARCHIVED entries raise ValueError.
        """
        from replay.decision_journal_schema import DecisionRevisionRecord, JournalStatus, REVISION_ID_PREFIX

        status = entry.get("status", "")
        if status == JournalStatus.ARCHIVED.value:
            raise ValueError(
                f"Cannot revise ARCHIVED entry {entry.get('journal_entry_id')}. "
                "Restore entry first before creating a revision."
            )

        if not reason and field_changes:
            raise ValueError("Reason is required for any revision.")

        for fld in self.REQUIRES_REASON_FIELDS:
            if fld in field_changes and not reason:
                raise ValueError(f"Revising '{fld}' requires a reason.")

        rev_num = int(entry.get("revision_count", 0)) + 1
        entry_id = entry.get("journal_entry_id", "")

        confidence_before = entry.get("confidence")
        confidence_after = field_changes.get("confidence", confidence_before)

        rev_id = f"{REVISION_ID_PREFIX}{uuid.uuid4().hex[:12].upper()}"

        revision = DecisionRevisionRecord(
            revision_id=rev_id,
            journal_entry_id=entry_id,
            original_entry_id=entry_id,
            decision_id=entry.get("decision_id", ""),
            session_id=entry.get("session_id", ""),
            revision_number=rev_num,
            previous_revision=rev_num - 1,
            new_revision=rev_num,
            reason=reason,
            change_reason=reason,
            changed_fields=field_changes,
            field_changes=field_changes,
            new_snapshot=dict(entry),
            confidence_before=confidence_before,
            confidence_after=confidence_after,
            simulation_only=True,
            research_only=True,
            no_real_orders=True,
        )

        return revision

    def get_revision_diff(
        self,
        original_snapshot: Dict[str, Any],
        new_snapshot: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Return dict of fields that changed between two snapshots."""
        diff: Dict[str, Any] = {}
        all_keys = set(list(original_snapshot.keys()) + list(new_snapshot.keys()))
        for k in all_keys:
            old_val = original_snapshot.get(k)
            new_val = new_snapshot.get(k)
            if old_val != new_val:
                diff[k] = {"before": old_val, "after": new_val}
        return diff

    def compare_revision(
        self, revision_a: Dict[str, Any], revision_b: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare two revision records."""
        snap_a = revision_a.get("new_snapshot", {})
        snap_b = revision_b.get("new_snapshot", {})
        return self.get_revision_diff(snap_a, snap_b)

    def revision_history(
        self, entry_id: str, all_revisions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Get revisions for an entry, sorted by revision_number."""
        revs = [r for r in all_revisions if r.get("journal_entry_id") == entry_id]
        return sorted(revs, key=lambda r: int(r.get("revision_number", 0)))

    def latest_revision(
        self, entry_id: str, all_revisions: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """Get the latest revision for an entry."""
        history = self.revision_history(entry_id, all_revisions)
        return history[-1] if history else None

    def supersede(
        self,
        entry: Dict[str, Any],
        reason: str = "superseded",
    ) -> Dict[str, Any]:
        """Mark an entry as SUPERSEDED (returns updated dict)."""
        updated = dict(entry)
        updated["status"] = "SUPERSEDED"
        updated["updated_at"] = _now_utc()
        updated["simulation_only"] = True
        return updated

    def validate_revision(
        self,
        entry: Dict[str, Any],
        reason: str,
        field_changes: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Validate a proposed revision before creating it."""
        errors = []
        warnings = []

        from replay.decision_journal_schema import JournalStatus
        status = entry.get("status", "")
        if status == JournalStatus.ARCHIVED.value:
            errors.append("ARCHIVED entries cannot be revised — restore first")

        if not reason:
            errors.append("Reason is required")

        for fld in ["stop_price", "target_price"]:
            if fld in field_changes and not reason:
                errors.append(f"Revising {fld} requires explicit reason")

        from replay.decision_journal_schema import FORBIDDEN_JOURNAL_FIELDS
        for fld in FORBIDDEN_JOURNAL_FIELDS:
            if fld in field_changes:
                errors.append(f"Forbidden field in revision: {fld}")

        return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}

    def restore_revision_as_new(
        self,
        old_revision: Dict[str, Any],
        reason: str,
        current_entry: Dict[str, Any],
    ) -> "DecisionRevisionRecord":
        """
        Restore an old revision as a new revision.
        [!] Does NOT rewrite history. Creates new DREV- record.
        """
        snapshot = old_revision.get("new_snapshot", {})
        field_changes = {k: v for k, v in snapshot.items()
                         if k not in ("simulation_only", "research_only", "no_real_orders",
                                      "revision_count", "updated_at", "latest_revision_id")}
        return self.create_revision(
            entry=current_entry,
            reason=f"[RESTORE from rev {old_revision.get('revision_number', '?')}] {reason}",
            field_changes=field_changes,
        )


# Backward-compat alias
DecisionRevisionManager = DecisionRevisionEngine
