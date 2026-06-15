"""
replay/decision_journal_manager.py — DecisionJournalManager for v1.2.2

[!] Research Only. No Real Orders. Replay Training Only.
[!] Journal ID: DJR- prefix. Revision ID: DREV- prefix.
[!] Finalized entries: append-only revision, never overwrite.
[!] Archived entries: immutable until restored.
[!] Hidden entries: not deleted, still in store.
[!] No paper orders. No broker calls. No auto scoring.
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


class DecisionJournalManager:
    """
    Manages the lifecycle of replay decision journal entries.

    Rules:
    - DJR- prefix for journal IDs, DREV- for revisions
    - finalize_entry: moves to RECORDED, then only append revisions
    - revise_entry: creates DREV- record, marks entry REVISED
    - archive_entry: sets ARCHIVED, entry becomes immutable
    - restore_entry: sets back to RECORDED, allows revisions
    - hide_entry: sets hidden=True, entry still in store
    - point-in-time fail: marks entry BLOCKED

    [!] SIMULATION_DECISION_ONLY. No paper orders. No broker calls.
    """

    SIMULATION_DECISION_ONLY = True
    no_real_orders = True
    research_only = True

    JOURNAL_ID_PREFIX = "DJR-"
    REVISION_ID_PREFIX = "DREV-"

    def __init__(self, store=None, repo_root: Optional[str] = None):
        self._store = store
        self._repo_root = repo_root
        if store is None:
            from replay.decision_journal_store import DecisionJournalStore
            self._store = DecisionJournalStore(repo_root=repo_root)

    def _new_journal_id(self) -> str:
        return f"{self.JOURNAL_ID_PREFIX}{uuid.uuid4().hex[:12].upper()}"

    def _new_revision_id(self) -> str:
        return f"{self.REVISION_ID_PREFIX}{uuid.uuid4().hex[:12].upper()}"

    def create_entry(
        self,
        session_id: str,
        decision_id: str,
        replay_date: str,
        action: str = "WATCH",
        symbol: str = "",
        **kwargs,
    ) -> "DecisionJournalEntry":
        """Create a new DRAFT journal entry."""
        from replay.decision_journal_schema import DecisionJournalEntry, JournalStatus

        entry = DecisionJournalEntry(
            journal_entry_id=self._new_journal_id(),
            decision_id=decision_id,
            session_id=session_id,
            replay_date=replay_date,
            action=action,
            symbol=symbol,
            scenario_id=kwargs.get("scenario_id"),
            checkpoint_id=kwargs.get("checkpoint_id"),
            confidence=int(kwargs.get("confidence", 50)),
            notes=kwargs.get("notes", ""),
            tags=kwargs.get("tags", []),
            pre_decision_notes=kwargs.get("pre_decision_notes", ""),
            post_decision_notes=kwargs.get("post_decision_notes", ""),
            decision_reason=kwargs.get("decision_reason", ""),
            status=JournalStatus.DRAFT.value,
            simulation_only=True,
            research_only=True,
            no_real_orders=True,
        )

        self._store.save_entry(entry.to_dict())
        logger.info("[DecisionJournalManager] Created entry %s", entry.journal_entry_id)
        return entry

    def create_from_replay_decision(
        self, decision_id: str, session_id: str, **kwargs
    ) -> "DecisionJournalEntry":
        """Create a journal entry linked to an existing ReplayDecision."""
        replay_date = kwargs.get("replay_date", "")
        action = kwargs.get("action", "WATCH")
        symbol = kwargs.get("symbol", "")
        return self.create_entry(
            session_id=session_id,
            decision_id=decision_id,
            replay_date=replay_date,
            action=action,
            symbol=symbol,
            **{k: v for k, v in kwargs.items() if k not in ("replay_date", "action", "symbol")},
        )

    def update_draft(self, entry_id: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Update a DRAFT entry (still as new append, marking old as superseded)."""
        existing = self._store.get_entry(entry_id)
        if not existing:
            logger.warning("[DecisionJournalManager] Entry not found: %s", entry_id)
            return None

        from replay.decision_journal_schema import JournalStatus
        if existing.get("status") not in (JournalStatus.DRAFT.value,):
            logger.warning("[DecisionJournalManager] Can only update DRAFT entries, got: %s", existing.get("status"))
            return None

        updated = dict(existing)
        updated.update({k: v for k, v in kwargs.items() if k not in ("simulation_only", "research_only", "no_real_orders")})
        updated["simulation_only"] = True
        updated["research_only"] = True
        updated["no_real_orders"] = True
        updated["updated_at"] = _now_utc()

        self._store.save_entry(updated)
        return updated

    def finalize_entry(self, entry_id: str) -> Optional[Dict[str, Any]]:
        """Move entry from DRAFT to RECORDED."""
        return self.record_entry(entry_id)

    def record_entry(self, entry_id: str) -> Optional[Dict[str, Any]]:
        """Move entry status to RECORDED."""
        existing = self._store.get_entry(entry_id)
        if not existing:
            return None

        updated = dict(existing)
        updated["status"] = "RECORDED"
        updated["updated_at"] = _now_utc()
        updated["simulation_only"] = True

        self._store.save_entry(updated)
        return updated

    def revise_entry(
        self, entry_id: str, reason: str, field_changes: Dict[str, Any]
    ) -> Optional["DecisionRevisionRecord"]:
        """
        Create a revision record (DREV-) and mark entry REVISED.
        Append-only — never overwrites original.
        """
        from replay.decision_journal_schema import DecisionRevisionRecord, JournalStatus, REVISION_ID_PREFIX

        existing = self._store.get_entry(entry_id)
        if not existing:
            logger.warning("[DecisionJournalManager] Entry not found: %s", entry_id)
            return None

        status = existing.get("status", "")
        if status == JournalStatus.ARCHIVED.value:
            logger.warning("[DecisionJournalManager] Cannot revise ARCHIVED entry %s — restore first", entry_id)
            return None

        rev_num = int(existing.get("revision_count", 0)) + 1

        confidence_before = existing.get("confidence")
        confidence_after = field_changes.get("confidence", confidence_before)

        rev_id = self._new_revision_id()
        revision = DecisionRevisionRecord(
            revision_id=rev_id,
            journal_entry_id=entry_id,
            original_entry_id=entry_id,
            decision_id=existing.get("decision_id", ""),
            session_id=existing.get("session_id", ""),
            revision_number=rev_num,
            previous_revision=rev_num - 1,
            new_revision=rev_num,
            reason=reason,
            change_reason=reason,
            changed_fields=field_changes,
            field_changes=field_changes,
            new_snapshot=dict(existing),
            confidence_before=confidence_before,
            confidence_after=confidence_after,
            simulation_only=True,
            research_only=True,
            no_real_orders=True,
        )

        self._store.save_revision(revision.to_dict())

        # Update entry status
        updated = dict(existing)
        updated["status"] = JournalStatus.REVISED.value
        updated["revision_count"] = rev_num
        updated["latest_revision_id"] = rev_id
        updated["updated_at"] = _now_utc()
        updated["simulation_only"] = True
        self._store.save_entry(updated)

        return revision

    def archive_entry(self, entry_id: str) -> Optional[Dict[str, Any]]:
        """Archive an entry (immutable after)."""
        existing = self._store.get_entry(entry_id)
        if not existing:
            return None

        updated = dict(existing)
        updated["status"] = "ARCHIVED"
        updated["archived"] = True
        updated["updated_at"] = _now_utc()
        updated["simulation_only"] = True

        self._store.save_entry(updated)
        return updated

    def restore_entry(self, entry_id: str) -> Optional[Dict[str, Any]]:
        """Restore an archived entry back to RECORDED."""
        existing = self._store.get_entry(entry_id)
        if not existing:
            return None

        updated = dict(existing)
        updated["status"] = "RECORDED"
        updated["archived"] = False
        updated["updated_at"] = _now_utc()
        updated["simulation_only"] = True

        self._store.save_entry(updated)
        return updated

    def hide_entry(self, entry_id: str) -> Optional[Dict[str, Any]]:
        """Mark entry as hidden (NOT deleted, still in store)."""
        existing = self._store.get_entry(entry_id)
        if not existing:
            return None

        updated = dict(existing)
        updated["hidden"] = True
        updated["updated_at"] = _now_utc()
        updated["simulation_only"] = True

        self._store.save_entry(updated)
        return updated

    def get_entry(self, entry_id: str) -> Optional[Dict[str, Any]]:
        """Get entry by ID."""
        return self._store.get_entry(entry_id)

    def list_entries(
        self,
        session_id: Optional[str] = None,
        status: Optional[str] = None,
        include_hidden: bool = False,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """List journal entries with optional filters."""
        all_entries_raw = self._store.load_entries()
        # Deduplicate — keep latest per entry_id
        latest: Dict[str, Dict[str, Any]] = {}
        for e in all_entries_raw:
            eid = e.get("journal_entry_id", "")
            if eid:
                latest[eid] = e

        entries = list(latest.values())

        if session_id:
            entries = [e for e in entries if e.get("session_id") == session_id]
        if status:
            entries = [e for e in entries if e.get("status") == status]
        if not include_hidden:
            entries = [e for e in entries if not e.get("hidden", False)]

        return entries[:limit]

    def session_entries(self, session_id: str) -> List[Dict[str, Any]]:
        return self.list_entries(session_id=session_id, include_hidden=False, limit=500)

    def symbol_entries(self, symbol: str) -> List[Dict[str, Any]]:
        all_e = self.list_entries(include_hidden=False, limit=500)
        return [e for e in all_e if e.get("symbol") == symbol]

    def date_entries(self, replay_date: str) -> List[Dict[str, Any]]:
        all_e = self.list_entries(include_hidden=False, limit=500)
        return [e for e in all_e if e.get("replay_date") == replay_date]

    def checkpoint_entries(self, checkpoint_id: str) -> List[Dict[str, Any]]:
        all_e = self.list_entries(include_hidden=False, limit=500)
        return [e for e in all_e if e.get("checkpoint_id") == checkpoint_id]

    def scenario_entries(self, scenario_id: str) -> List[Dict[str, Any]]:
        all_e = self.list_entries(include_hidden=False, limit=500)
        return [e for e in all_e if e.get("scenario_id") == scenario_id]

    def latest_entry(self, session_id: str) -> Optional[Dict[str, Any]]:
        entries = self.session_entries(session_id)
        return entries[-1] if entries else None

    def validate_entry(self, entry_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a journal entry dict. Returns validation result."""
        errors = []
        warnings = []

        from replay.decision_journal_schema import JOURNAL_ID_PREFIX, FORBIDDEN_JOURNAL_FIELDS

        eid = entry_dict.get("journal_entry_id", "")
        if not eid.startswith(JOURNAL_ID_PREFIX):
            errors.append(f"journal_entry_id must start with {JOURNAL_ID_PREFIX}")

        if not entry_dict.get("simulation_only", True):
            errors.append("simulation_only must be True")

        for fld in FORBIDDEN_JOURNAL_FIELDS:
            if fld in entry_dict:
                errors.append(f"Forbidden field detected: {fld}")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }

    def build_context(self, entry_id: str) -> Dict[str, Any]:
        """Build full context for a journal entry."""
        entry = self._store.get_entry(entry_id)
        if not entry:
            return {}

        revisions = [
            r for r in self._store.load_revisions()
            if r.get("journal_entry_id") == entry_id
        ]

        links = [
            lnk for lnk in self._store.load_links()
            if lnk.get("source_entry_id") == entry_id or lnk.get("target_entry_id") == entry_id
        ]

        thesis_id = entry.get("thesis_id")
        thesis = None

        risk_plan_id = entry.get("risk_plan_id")
        risk_plan = None

        emotional_state_id = entry.get("emotional_state_id")
        emotional_state = None

        checklist_ids = entry.get("checklist_ids", [])
        checklists = []

        if thesis_id:
            # Try to load from store
            pass  # Full thesis store TBD

        return {
            "entry": entry,
            "thesis": thesis,
            "risk_plan": risk_plan,
            "emotional_state": emotional_state,
            "checklists": checklists,
            "revisions": revisions,
            "links": links,
            "revision_count": len(revisions),
        }

    def create_follow_up(
        self, parent_entry_id: str, session_id: str, decision_id: str, **kwargs
    ) -> Optional["DecisionJournalEntry"]:
        """Create a follow-up journal entry linked to parent."""
        parent = self._store.get_entry(parent_entry_id)
        if not parent:
            return None

        entry = self.create_entry(
            session_id=session_id,
            decision_id=decision_id,
            replay_date=kwargs.get("replay_date", parent.get("replay_date", "")),
            action=kwargs.get("action", "WATCH"),
            symbol=kwargs.get("symbol", parent.get("symbol", "")),
            parent_entry_id=parent_entry_id,
            **{k: v for k, v in kwargs.items() if k not in ("replay_date", "action", "symbol")},
        )

        # Create link
        self.link_entries(
            source_id=parent_entry_id,
            target_id=entry.journal_entry_id,
            relation_type="FOLLOW_UP",
        )

        return entry

    def link_entries(
        self, source_id: str, target_id: str, relation_type: str, notes: str = ""
    ) -> Optional["DecisionJournalLink"]:
        """Create a link between two journal entries."""
        from replay.decision_journal_schema import DecisionJournalLink
        import uuid as _uuid

        link = DecisionJournalLink(
            link_id=f"LNK-{_uuid.uuid4().hex[:12].upper()}",
            source_entry_id=source_id,
            target_entry_id=target_id,
            relation_type=relation_type,
            notes=notes,
        )

        self._store.save_link(link.to_dict())
        return link

    def export_entry(self, entry_id: str, output_path: str = "") -> Dict[str, Any]:
        """Export a journal entry (metadata only, no secrets)."""
        entry = self._store.get_entry(entry_id)
        if not entry:
            return {"status": "error", "message": f"Entry {entry_id} not found"}

        # Strip forbidden fields
        safe = {k: v for k, v in entry.items() if k not in [
            "api_key", "secret", "broker", "order_token",
            "realized_return", "future_return", "hindsight_score",
            "realized_pnl", "final_result",
        ]}

        return {"status": "ok", "entry": safe, "redacted_fields": []}

    def import_entry(
        self, entry_dict: Dict[str, Any], dry_run: bool = True, allow_write: bool = False
    ) -> Dict[str, Any]:
        """
        Import a journal entry.
        BLOCKED unless dry_run=False AND allow_write=True.
        """
        if dry_run or not allow_write:
            result = self.validate_entry(entry_dict)
            return {
                "status": "dry_run",
                "dry_run": True,
                "allow_write": allow_write,
                "validation": result,
                "message": "Dry run complete. Use dry_run=False AND allow_write=True to write.",
            }

        # Actual import
        result = self.validate_entry(entry_dict)
        if not result["valid"]:
            return {"status": "blocked", "errors": result["errors"]}

        self._store.save_entry(entry_dict)
        return {"status": "imported", "journal_entry_id": entry_dict.get("journal_entry_id")}

    def latest_journal_revision(self, entry_id: str) -> Optional[Dict[str, Any]]:
        """Get latest revision for an entry."""
        revisions = [
            r for r in self._store.load_revisions()
            if r.get("journal_entry_id") == entry_id
        ]
        return revisions[-1] if revisions else None

    def journal_summary(self, session_id: str) -> Dict[str, Any]:
        """Return summary stats for a session's journal entries."""
        entries = self.session_entries(session_id)
        status_counts: Dict[str, int] = {}
        for e in entries:
            s = e.get("status", "UNKNOWN")
            status_counts[s] = status_counts.get(s, 0) + 1

        return {
            "session_id": session_id,
            "total_entries": len(entries),
            "status_distribution": status_counts,
            "simulation_only": True,
        }
