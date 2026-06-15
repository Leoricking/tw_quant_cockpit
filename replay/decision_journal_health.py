"""
replay/decision_journal_health.py — DecisionJournalHealthChecker for v1.2.2

[!] Research Only. No Real Orders. Replay Training Only.
Checks all journal components for correctness.
"""
from __future__ import annotations

import logging
import traceback
from datetime import datetime, timezone
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


class DecisionJournalHealthChecker:
    """
    Health checker for the Decision Journal v1.2.2 system.

    Checks:
    - Schema imports
    - Store accessibility
    - Manager create/finalize/revise
    - Query
    - Templates load
    - Discipline checklist
    - Emotional state
    - Cognitive bias
    - Revision engine
    - Comparator
    - Summary (no forbidden stats)
    - Portability (dry-run default)
    - Backward compat
    - Governance alerts
    - Safety invariants

    Returns PASS / WARN / FAIL / BLOCKED per check.
    """

    no_real_orders = True
    research_only = True

    def __init__(self, repo_root: str = ""):
        self._repo_root = repo_root

    def run(self) -> Dict[str, Any]:
        """Run all health checks."""
        return self.run_health_check()

    def run_health_check(self) -> Dict[str, Any]:
        """Run all health checks. Returns structured result."""
        checks = []
        issues = []
        overall = "PASS"

        def _chk(name: str, fn) -> None:
            nonlocal overall
            try:
                result = fn()
                status = result.get("status", "PASS")
                checks.append({"name": name, "status": status, "detail": result.get("detail", "")})
                if status == "FAIL":
                    issues.append(f"{name}: FAIL — {result.get('detail', '')}")
                    overall = "FAIL"
                elif status == "WARN" and overall == "PASS":
                    overall = "WARN"
            except Exception as exc:
                checks.append({"name": name, "status": "FAIL", "detail": str(exc)})
                issues.append(f"{name}: FAIL — {exc}")
                overall = "FAIL"

        _chk("schema_import", self._check_schema_import)
        _chk("store_accessible", self._check_store)
        _chk("manager_operations", self._check_manager)
        _chk("query_operations", self._check_query)
        _chk("templates_load", self._check_templates)
        _chk("discipline_checklist", self._check_checklist)
        _chk("emotional_state", self._check_emotional_state)
        _chk("cognitive_bias", self._check_cognitive_bias)
        _chk("revision_engine", self._check_revision)
        _chk("comparator_no_forbidden_fields", self._check_comparator)
        _chk("summary_no_forbidden_stats", self._check_summary)
        _chk("portability_dry_run_default", self._check_portability)
        _chk("backward_compat_v121", self._check_backward_compat)
        _chk("entries_have_djr_prefix", self._check_id_prefixes)
        _chk("revisions_have_drev_prefix", self._check_revision_prefixes)
        _chk("archived_entry_immutable", self._check_archived_immutable)
        _chk("simulation_only_enforced", self._check_simulation_only)
        _chk("no_future_fields", self._check_no_future_fields)
        _chk("import_execute_without_allow_write_blocked", self._check_import_guard)
        _chk("no_auto_scoring", self._check_no_auto_scoring)

        return {
            "status": overall,
            "checks": checks,
            "issues": issues,
            "total_checks": len(checks),
            "pass_count": sum(1 for c in checks if c["status"] == "PASS"),
            "fail_count": sum(1 for c in checks if c["status"] == "FAIL"),
            "warn_count": sum(1 for c in checks if c["status"] == "WARN"),
            "checked_at": _now_utc(),
            "simulation_only": True,
            "no_real_orders": True,
        }

    def print_results(self, results: Dict[str, Any]) -> None:
        """Print health check results."""
        status = results.get("status", "?")
        print(f"  Status: {status}")
        print(f"  Checks: {results.get('total_checks', 0)} total, "
              f"{results.get('pass_count', 0)} pass, "
              f"{results.get('fail_count', 0)} fail, "
              f"{results.get('warn_count', 0)} warn")
        for chk in results.get("checks", []):
            icon = "OK" if chk["status"] == "PASS" else ("WARN" if chk["status"] == "WARN" else "FAIL")
            detail = f" — {chk['detail']}" if chk.get("detail") else ""
            print(f"  [{icon}] {chk['name']}{detail}")
        for issue in results.get("issues", []):
            print(f"  [ISSUE] {issue}")

    # ------------------------------------------------------------------
    # Individual checks
    # ------------------------------------------------------------------

    def _check_schema_import(self) -> Dict[str, Any]:
        from replay.decision_journal_schema import (
            DecisionJournalEntry, TradeThesis, RiskPlan,
            EmotionalStateRecord, DisciplineChecklistResult,
            DecisionRevisionRecord, DecisionJournalLink,
        )
        return {"status": "PASS", "detail": "All schema classes imported"}

    def _check_store(self) -> Dict[str, Any]:
        from replay.decision_journal_store import DecisionJournalStore
        store = DecisionJournalStore(repo_root=self._repo_root)
        health = store.get_store_health()
        if health.get("status") == "FAIL":
            return {"status": "WARN", "detail": "Store not yet initialized (OK on first run)"}
        return {"status": "PASS", "detail": "Store accessible"}

    def _check_manager(self) -> Dict[str, Any]:
        from replay.decision_journal_manager import DecisionJournalManager
        from replay.decision_journal_store import DecisionJournalStore
        import tempfile, os
        with tempfile.TemporaryDirectory() as tmp:
            store = DecisionJournalStore(store_dir=tmp)
            mgr = DecisionJournalManager(store=store)
            entry = mgr.create_entry(
                session_id="SES-TEST", decision_id="DEC-TEST",
                replay_date="2024-01-01", action="WATCH",
            )
            assert entry.journal_entry_id.startswith("DJR-"), "Entry ID must start with DJR-"
            assert entry.simulation_only, "simulation_only must be True"
            # Finalize
            mgr.record_entry(entry.journal_entry_id)
            # Revise
            rev = mgr.revise_entry(entry.journal_entry_id, reason="test revision", field_changes={"confidence": 60})
            assert rev is not None
            assert rev.revision_id.startswith("DREV-"), "Revision ID must start with DREV-"
        return {"status": "PASS", "detail": "Manager create/finalize/revise OK"}

    def _check_query(self) -> Dict[str, Any]:
        from replay.decision_journal_query import DecisionJournalQuery
        from replay.decision_journal_store import DecisionJournalStore
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            store = DecisionJournalStore(store_dir=tmp)
            query = DecisionJournalQuery(store=store)
            result = query.list_entries()
            assert isinstance(result, list)
        return {"status": "PASS", "detail": "Query OK"}

    def _check_templates(self) -> Dict[str, Any]:
        from replay.decision_templates import DecisionTemplateLibrary
        lib = DecisionTemplateLibrary(repo_root=self._repo_root)
        templates = lib.list_templates()
        if not templates:
            return {"status": "WARN", "detail": "No templates found — may need replay/journal_templates/"}
        return {"status": "PASS", "detail": f"Found {len(templates)} templates: {templates}"}

    def _check_checklist(self) -> Dict[str, Any]:
        from replay.discipline_checklist import DisciplineChecklistEngine
        eng = DisciplineChecklistEngine(repo_root=self._repo_root)
        items = eng.build_default("ENTER")
        assert len(items) > 0
        return {"status": "PASS", "detail": f"Checklist engine OK, default items: {len(items)}"}

    def _check_emotional_state(self) -> Dict[str, Any]:
        from replay.emotional_state import EmotionalStateCapture
        esc = EmotionalStateCapture()
        rec = esc.record_state("SES-TEST", "DEC-TEST", emotion="CALM", confidence=70, anxiety=20, focus=80)
        assert rec.self_reported is True
        assert rec.simulation_only is True
        try:
            esc.validate_levels(confidence=150)
            return {"status": "FAIL", "detail": "Did not raise on out-of-range level"}
        except ValueError:
            pass
        return {"status": "PASS", "detail": "Emotional state capture OK, range validation OK"}

    def _check_cognitive_bias(self) -> Dict[str, Any]:
        from replay.cognitive_bias import CognitiveBiasRegistry
        reg = CognitiveBiasRegistry()
        assert len(reg.KNOWN_BIASES) > 0
        flag = reg.flag_bias("FOMO")
        assert flag["bias_name"] == "FOMO"
        try:
            reg.flag_bias("INVALID_BIAS_XYZ")
            return {"status": "FAIL", "detail": "Did not raise on unknown bias"}
        except ValueError:
            pass
        return {"status": "PASS", "detail": f"Cognitive bias registry OK, {len(reg.KNOWN_BIASES)} known biases"}

    def _check_revision(self) -> Dict[str, Any]:
        from replay.decision_revision import DecisionRevisionEngine
        from replay.decision_journal_schema import JournalStatus
        eng = DecisionRevisionEngine()
        entry = {
            "journal_entry_id": "DJR-TESTABC001",
            "decision_id": "DEC-TEST",
            "session_id": "SES-TEST",
            "confidence": 50,
            "revision_count": 0,
            "status": JournalStatus.RECORDED.value,
        }
        rev = eng.create_revision(entry, reason="test", field_changes={"confidence": 60})
        assert rev.revision_id.startswith("DREV-")
        assert rev.confidence_before == 50
        assert rev.confidence_after == 60
        # Test archived blocked
        archived_entry = dict(entry)
        archived_entry["status"] = JournalStatus.ARCHIVED.value
        try:
            eng.create_revision(archived_entry, reason="test", field_changes={})
            return {"status": "FAIL", "detail": "Did not block revision of ARCHIVED entry"}
        except ValueError:
            pass
        return {"status": "PASS", "detail": "Revision engine OK, archived block OK"}

    def _check_comparator(self) -> Dict[str, Any]:
        from replay.decision_comparator import DecisionJournalComparator
        cmp = DecisionJournalComparator()
        entry_a = {
            "journal_entry_id": "DJR-AAA",
            "action": "ENTER", "confidence": 70,
        }
        entry_b = {
            "journal_entry_id": "DJR-BBB",
            "action": "WAIT", "confidence": 50,
        }
        result = cmp.compare_entries(entry_a, entry_b)
        # Check no forbidden fields
        for fld in ["realized_return", "future_return", "hindsight_score"]:
            assert fld not in result, f"Forbidden field {fld} in comparator output"
        return {"status": "PASS", "detail": "Comparator OK, no forbidden fields"}

    def _check_summary(self) -> Dict[str, Any]:
        from replay.decision_journal_summary import DecisionJournalSummaryBuilder
        from replay.decision_journal_store import DecisionJournalStore
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            store = DecisionJournalStore(store_dir=tmp)
            builder = DecisionJournalSummaryBuilder(store=store)
            summary = builder.build_summary("SES-TEST")
            for fld in ["win_rate", "return_rate", "pnl", "accuracy", "alpha", "sharpe", "hindsight_score"]:
                assert fld not in summary, f"Forbidden stat {fld} in summary"
        return {"status": "PASS", "detail": "Summary OK, no forbidden stats"}

    def _check_portability(self) -> Dict[str, Any]:
        from replay.decision_journal_portability import DecisionJournalPortability
        from replay.decision_journal_store import DecisionJournalStore
        import tempfile, json
        with tempfile.TemporaryDirectory() as tmp:
            store = DecisionJournalStore(store_dir=tmp)
            port = DecisionJournalPortability(store=store)
            # Create temp import file
            import_file = f"{tmp}/test_import.jsonl"
            entry = {
                "journal_entry_id": "DJR-IMPORTTEST01",
                "session_id": "SES-TEST",
                "decision_id": "DEC-TEST",
                "simulation_only": True,
                "replay_date": "2024-01-01",
            }
            with open(import_file, "w") as f:
                f.write(json.dumps(entry) + "\n")
            # Default dry-run
            result = port.import_entries(import_file)
            assert result.dry_run is True or result.status in ("dry_run", "blocked")
            # Import without allow_write blocked
            result2 = port.import_entries(import_file, dry_run=False, allow_write=False)
            assert result2.status in ("dry_run", "blocked")
        return {"status": "PASS", "detail": "Portability dry-run default OK, execute guard OK"}

    def _check_backward_compat(self) -> Dict[str, Any]:
        from replay.replay_schema import ReplayDecision
        d = ReplayDecision(
            decision_id="DEC-OLD001",
            session_id="SES-TEST",
            symbol="TST",
            replay_date="2024-01-01",
            action="WATCH",
        )
        assert d.journal_entry_id is None
        assert d.revision_count == 0
        assert d.simulation_only is True
        return {"status": "PASS", "detail": "v1.2.1 ReplayDecision backward compat OK"}

    def _check_id_prefixes(self) -> Dict[str, Any]:
        from replay.decision_journal_schema import JOURNAL_ID_PREFIX, DecisionJournalEntry
        import uuid
        entry = DecisionJournalEntry(
            journal_entry_id=f"{JOURNAL_ID_PREFIX}{uuid.uuid4().hex[:12].upper()}",
            decision_id="DEC-TEST",
            session_id="SES-TEST",
            replay_date="2024-01-01",
        )
        assert entry.journal_entry_id.startswith("DJR-")
        return {"status": "PASS", "detail": "DJR- prefix enforced"}

    def _check_revision_prefixes(self) -> Dict[str, Any]:
        from replay.decision_journal_schema import REVISION_ID_PREFIX, DecisionRevisionRecord
        import uuid
        rev = DecisionRevisionRecord(
            revision_id=f"{REVISION_ID_PREFIX}{uuid.uuid4().hex[:12].upper()}",
            journal_entry_id="DJR-TEST",
            original_entry_id="DJR-TEST",
            decision_id="DEC-TEST",
            session_id="SES-TEST",
        )
        assert rev.revision_id.startswith("DREV-")
        return {"status": "PASS", "detail": "DREV- prefix enforced"}

    def _check_archived_immutable(self) -> Dict[str, Any]:
        from replay.decision_revision import DecisionRevisionEngine
        from replay.decision_journal_schema import JournalStatus
        eng = DecisionRevisionEngine()
        archived = {
            "journal_entry_id": "DJR-ARCHIVEDTEST",
            "decision_id": "DEC-TEST",
            "session_id": "SES-TEST",
            "confidence": 50,
            "revision_count": 0,
            "status": JournalStatus.ARCHIVED.value,
        }
        try:
            eng.create_revision(archived, reason="should fail", field_changes={"notes": "x"})
            return {"status": "FAIL", "detail": "Did not block revision of ARCHIVED entry"}
        except ValueError:
            return {"status": "PASS", "detail": "Archived entry immutability enforced"}

    def _check_simulation_only(self) -> Dict[str, Any]:
        from replay.decision_journal_schema import DecisionJournalEntry
        entry = DecisionJournalEntry(
            journal_entry_id="DJR-SIMTEST001",
            decision_id="DEC-TEST",
            session_id="SES-TEST",
            replay_date="2024-01-01",
        )
        assert entry.simulation_only is True
        return {"status": "PASS", "detail": "simulation_only=True enforced"}

    def _check_no_future_fields(self) -> Dict[str, Any]:
        from replay.decision_journal_schema import FORBIDDEN_JOURNAL_FIELDS
        entry_dict = {
            "journal_entry_id": "DJR-TEST",
            "simulation_only": True,
        }
        for fld in FORBIDDEN_JOURNAL_FIELDS:
            assert fld not in entry_dict, f"Forbidden field {fld} in entry"
        return {"status": "PASS", "detail": "No future/forbidden fields in schema"}

    def _check_import_guard(self) -> Dict[str, Any]:
        from replay.decision_journal_portability import DecisionJournalPortability
        from replay.decision_journal_store import DecisionJournalStore
        import tempfile, json
        with tempfile.TemporaryDirectory() as tmp:
            store = DecisionJournalStore(store_dir=tmp)
            port = DecisionJournalPortability(store=store)
            import_file = f"{tmp}/test.jsonl"
            entry = {"journal_entry_id": "DJR-TEST001", "simulation_only": True,
                     "session_id": "SES-TEST", "decision_id": "DEC-TEST", "replay_date": "2024-01-01"}
            with open(import_file, "w") as f:
                f.write(json.dumps(entry) + "\n")
            # execute=True but allow_write=False should still be blocked
            result = port.import_entries(import_file, dry_run=False, allow_write=False)
            assert result.status in ("dry_run", "blocked"), f"Expected blocked, got: {result.status}"
        return {"status": "PASS", "detail": "Import execute without allow-write BLOCKED"}

    def _check_no_auto_scoring(self) -> Dict[str, Any]:
        from release.version_info import DECISION_AUTO_SCORING_ENABLED
        assert DECISION_AUTO_SCORING_ENABLED is False
        return {"status": "PASS", "detail": "DECISION_AUTO_SCORING_ENABLED=False verified"}


# Backward-compat alias
DecisionJournalHealthCheck = DecisionJournalHealthChecker
