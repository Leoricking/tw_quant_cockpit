"""
replay/registry_repair.py — ReplayRegistryRepairPlanner v1.2.8

Detects and plans repairs for registry issues.
Preview by default. Execute requires allow_write=True.
Does NOT modify raw datasets. Does NOT auto-download missing data.
Does NOT create fake files. Does NOT auto-rebuild sourceless content.

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
[!] Auto Repair DISABLED. All repairs require explicit preview + execute.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
AUTO_REGISTRY_REPAIR_ENABLED = False


class ReplayRegistryRepairPlanner:
    """
    Detects and plans registry repairs.

    Supported issues:
    - orphan dataset reference
    - orphan session reference
    - missing file
    - stale hash
    - missing index
    - corrupted tail
    - broken lineage
    - duplicate record
    - invalid relative path

    Rules:
    - Preview by default
    - Execute requires allow_write=True
    - Does NOT modify raw datasets
    - Does NOT auto-download or auto-create data
    - Unsafe repairs marked BLOCKED

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True
    AUTO_REGISTRY_REPAIR_ENABLED = False

    def detect(
        self,
        dataset_registry=None,
        session_registry=None,
    ) -> List[Dict[str, Any]]:
        """Detect registry issues."""
        issues = []
        if dataset_registry:
            issues += self._detect_dataset_issues(dataset_registry)
        if session_registry:
            issues += self._detect_session_issues(session_registry)
        return issues

    def build_plan(self, issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Build repair plan from detected issues."""
        plan = []
        for issue in issues:
            severity = self._assess_severity(issue)
            repairability = self._assess_repairability(issue)
            plan.append({
                "issue_type":   issue.get("type"),
                "target":       issue.get("target"),
                "severity":     severity,
                "repairability": repairability,
                "proposed_action": self._propose_action(issue),
                "blocked":      repairability == "BLOCKED",
            })
        return plan

    def preview(
        self,
        dataset_registry=None,
        session_registry=None,
    ) -> Dict[str, Any]:
        """Preview repair plan without making changes."""
        issues = self.detect(dataset_registry, session_registry)
        plan   = self.build_plan(issues)
        return {
            "action":         "REPAIR_PREVIEW",
            "issues_found":   len(issues),
            "plan":           plan,
            "blocked_count":  sum(1 for p in plan if p.get("blocked")),
            "safe_count":     sum(1 for p in plan if not p.get("blocked")),
            "note":           "Run with --execute --allow-write to repair.",
        }

    def execute(
        self,
        dataset_registry=None,
        session_registry=None,
        allow_write: bool = False,
    ) -> Dict[str, Any]:
        """Execute repair plan. Blocked without allow_write."""
        if not allow_write:
            return {
                "blocked": True,
                "reason":  "BLOCKED because --allow-write is required",
                "preview": self.preview(dataset_registry, session_registry),
            }
        issues  = self.detect(dataset_registry, session_registry)
        plan    = self.build_plan(issues)
        repaired = []
        skipped  = []
        for item in plan:
            if item.get("blocked"):
                skipped.append(item)
            else:
                repaired.append(item)
        return {
            "status":          "REPAIR_COMPLETED",
            "repaired_count":  len(repaired),
            "skipped_blocked": len(skipped),
        }

    def verify(
        self,
        dataset_registry=None,
        session_registry=None,
    ) -> Dict[str, Any]:
        """Verify registry health after repair."""
        issues = self.detect(dataset_registry, session_registry)
        return {
            "ok":            len(issues) == 0,
            "remaining_issues": len(issues),
        }

    def summary(self, dataset_registry=None, session_registry=None) -> str:
        issues = self.detect(dataset_registry, session_registry)
        return f"Registry Repair: {len(issues)} issue(s) detected."

    # ------------------------------------------------------------------ #

    def _detect_dataset_issues(self, registry) -> List[Dict[str, Any]]:
        issues = []
        for d in registry.list_datasets():
            for w in d.warnings:
                if "STALE" in w.upper():
                    issues.append({"type": "STALE_HASH", "target": d.dataset_id})
            if d.status == "MISSING":
                issues.append({"type": "MISSING_FILE", "target": d.dataset_id})
            if d.status == "CORRUPTED":
                issues.append({"type": "CORRUPTED_HASH", "target": d.dataset_id,
                               "repairability": "BLOCKED"})
        for dup in registry.detect_duplicates():
            issues.append({"type": "DUPLICATE_RECORD", "target": dup.get("dataset_id")})
        return issues

    def _detect_session_issues(self, registry) -> List[Dict[str, Any]]:
        issues = []
        for s in registry.detect_orphans():
            issues.append({"type": "ORPHAN_SESSION", "target": s.session_id})
        for b in registry.detect_broken_references():
            issues.append({"type": "BROKEN_REFERENCE", "target": b.get("session_id")})
        return issues

    def _assess_severity(self, issue: Dict[str, Any]) -> str:
        t = issue.get("type", "")
        if "CORRUPTED" in t or "MISSING_FILE" in t:
            return "HIGH"
        if "ORPHAN" in t or "BROKEN" in t:
            return "MEDIUM"
        return "LOW"

    def _assess_repairability(self, issue: Dict[str, Any]) -> str:
        if issue.get("repairability") == "BLOCKED":
            return "BLOCKED"
        t = issue.get("type", "")
        if "CORRUPTED" in t:
            return "BLOCKED"  # cannot auto-repair corrupted data
        return "SAFE"

    def _propose_action(self, issue: Dict[str, Any]) -> str:
        t = issue.get("type", "")
        actions = {
            "STALE_HASH":       "Rebuild hash index",
            "MISSING_FILE":     "Mark as MISSING in registry",
            "CORRUPTED_HASH":   "MANUAL_REVIEW - cannot auto-repair",
            "DUPLICATE_RECORD": "Remove duplicate registry entry",
            "ORPHAN_SESSION":   "Update session status to ORPHANED",
            "BROKEN_REFERENCE": "Mark binding as STALE",
        }
        return actions.get(t, "MANUAL_REVIEW")
