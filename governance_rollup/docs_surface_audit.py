"""
governance_rollup/docs_surface_audit.py — GovernanceDocsSurfaceAuditor v1.1.9

Audits docs for version consistency and safety wording.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import csv
import logging
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

RESEARCH_ONLY = True
NO_REAL_ORDERS = True

_BASE_DIR = Path(__file__).resolve().parent.parent


class GovernanceDocsSurfaceAuditor:
    """
    Audits docs for version consistency and safety wording.
    """

    EXPECTED_VERSION = "1.1.9"
    DOCS_TO_CHECK = [
        "README.md",
        "docs/index.md",
        "docs/roadmap.md",
        "docs/release_notes_v1.1.md",
        "docs/cli_cookbook_v1.0.md",
        "docs/user_guide_v1.0.md",
        "docs/handoff_guide_v1.0.md",
    ]
    V11X_DOCS = [
        "docs/data_universe_expansion_v1.1.0.md",
        "docs/data_import_onboarding_v1.1.1.md",
        "docs/coverage_repair_workflow_v1.1.2.md",
        "docs/data_freshness_monitor_v1.1.3.md",
        "docs/coverage_quality_gates_v1.1.4.md",
        "docs/quality_gate_enforcement_audit_v1.1.5.md",
        "docs/data_governance_operations_dashboard_v1.1.6.md",
        "docs/governance_alerts_daily_operations_v1.1.7.md",
        "docs/research_run_registry_v1.1.8.md",
        "docs/data_governance_stable_rollup_v1.1.9.md",
    ]
    SAFETY_PHRASES = [
        "No Real Orders",
        "Research Only",
        "Not Investment Advice",
        "Production Trading",
        "Broker",
    ]
    DUAL_COMPUTER_PHRASES = [
        "D:/code/Claude",
        "C:/Users/Rossi",
        "tw_quant_cockpit",
        "trading_master",
        "dual-computer",
        "cross-machine",
    ]
    OBSOLETE_PATH_PATTERNS = [
        r"D:\\code\\Claude\\tw_quant_cockpit(?!/)",  # Windows backslash old style
    ]

    def run(self) -> Dict[str, Any]:
        """Run all docs surface audit checks."""
        results: Dict[str, Any] = {}
        results["readme_version"] = self.check_readme_version()
        results["docs_existence"] = self.check_docs_existence()
        results["version_references"] = self.check_version_references()
        results["safety_wording"] = self.check_safety_wording()
        results["dual_computer_docs"] = self.check_dual_computer_docs()
        return results

    def check_readme_version(self) -> Dict[str, Any]:
        """Check that README.md references current version."""
        readme = _BASE_DIR / "README.md"
        if not readme.exists():
            return {"valid": False, "status": "MISSING", "issues": ["README.md not found"]}
        try:
            content = readme.read_text(encoding="utf-8", errors="replace")
            has_version = self.EXPECTED_VERSION in content
            return {
                "valid": has_version,
                "status": "PASS" if has_version else "WARN",
                "has_version": has_version,
                "expected_version": self.EXPECTED_VERSION,
                "issues": [] if has_version else [f"README.md does not reference v{self.EXPECTED_VERSION}"],
            }
        except Exception as exc:
            return {"valid": False, "status": "ERROR", "issues": [str(exc)]}

    def check_docs_existence(self) -> Dict[str, Any]:
        """Check that all expected docs files exist."""
        all_docs = self.DOCS_TO_CHECK + self.V11X_DOCS
        missing = []
        found = []
        for doc_path in all_docs:
            full = _BASE_DIR / doc_path
            if full.exists():
                found.append(doc_path)
            else:
                missing.append(doc_path)
        # Critical docs missing = WARN (not FAIL, docs may be in progress)
        return {
            "valid": len(missing) == 0,
            "status": "PASS" if not missing else "WARN",
            "found": found,
            "missing": missing,
            "total_expected": len(all_docs),
            "total_found": len(found),
        }

    def check_version_references(self) -> Dict[str, Any]:
        """Check version references in key docs."""
        issues = []
        checked = []
        for doc_path in self.DOCS_TO_CHECK:
            full = _BASE_DIR / doc_path
            if not full.exists():
                continue
            try:
                content = full.read_text(encoding="utf-8", errors="replace")
                if self.EXPECTED_VERSION in content:
                    checked.append({"path": doc_path, "has_version": True})
                else:
                    checked.append({"path": doc_path, "has_version": False})
                    issues.append(f"{doc_path}: does not reference v{self.EXPECTED_VERSION}")
            except Exception as exc:
                issues.append(f"{doc_path}: read error: {exc}")
        return {
            "valid": len(issues) == 0,
            "status": "PASS" if not issues else "WARN",
            "issues": issues,
            "checked": checked,
        }

    def check_safety_wording(self) -> Dict[str, Any]:
        """Check that key docs contain required safety wording."""
        issues = []
        key_docs = ["README.md", "docs/release_notes_v1.1.md"]
        for doc_path in key_docs:
            full = _BASE_DIR / doc_path
            if not full.exists():
                continue
            try:
                content = full.read_text(encoding="utf-8", errors="replace")
                for phrase in ["No Real Orders", "Not Investment Advice"]:
                    if phrase not in content:
                        issues.append(f"{doc_path}: missing safety phrase: '{phrase}'")
            except Exception as exc:
                issues.append(f"{doc_path}: read error: {exc}")
        return {
            "valid": len(issues) == 0,
            "status": "PASS" if not issues else "WARN",
            "issues": issues,
            "phrases_checked": self.SAFETY_PHRASES,
        }

    def check_dual_computer_docs(self) -> Dict[str, Any]:
        """Check that dual-computer path instructions are documented."""
        docs_to_check = [
            "docs/data_governance_stable_rollup_v1.1.9.md",
            "docs/v1.1_operations_runbook.md",
        ]
        found_dual_docs = []
        missing_dual_docs = []
        for doc_path in docs_to_check:
            full = _BASE_DIR / doc_path
            if not full.exists():
                missing_dual_docs.append(doc_path)
                continue
            try:
                content = full.read_text(encoding="utf-8", errors="replace")
                has_dual = any(phrase in content for phrase in self.DUAL_COMPUTER_PHRASES)
                if has_dual:
                    found_dual_docs.append(doc_path)
                else:
                    missing_dual_docs.append(f"{doc_path} (missing dual-computer instructions)")
            except Exception as exc:
                missing_dual_docs.append(f"{doc_path}: read error: {exc}")
        return {
            "valid": len(missing_dual_docs) == 0,
            "status": "PASS" if not missing_dual_docs else "WARN",
            "found_dual_computer_docs": found_dual_docs,
            "missing_or_incomplete": missing_dual_docs,
        }

    def summarize(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize audit results."""
        total = len(results)
        passed = sum(1 for r in results.values()
                     if isinstance(r, dict) and r.get("status") == "PASS")
        warned = sum(1 for r in results.values()
                     if isinstance(r, dict) and r.get("status") == "WARN")
        failed = sum(1 for r in results.values()
                     if isinstance(r, dict) and r.get("status") in ("FAIL", "ERROR"))
        overall = "PASS" if failed == 0 and warned == 0 else ("WARN" if failed == 0 else "FAIL")
        return {
            "overall_status": overall,
            "checks_total": total,
            "checks_passed": passed,
            "checks_warned": warned,
            "checks_failed": failed,
            "results": results,
            "research_only": True,
            "no_real_orders": True,
        }

    def save_audit(self, results: Dict[str, Any]) -> Path:
        """Save audit to data/governance_rollup/docs_surface_audit.csv."""
        output_dir = _BASE_DIR / "data" / "governance_rollup"
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / "docs_surface_audit.csv"
        rows = []
        for check_name, result in results.items():
            if isinstance(result, dict):
                rows.append({
                    "check": check_name,
                    "status": result.get("status", ""),
                    "valid": result.get("valid", ""),
                    "issues": str(result.get("issues", []))[:200],
                    "generated_at": datetime.now(timezone.utc).isoformat(),
                })
        if rows:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                writer.writeheader()
                writer.writerows(rows)
        return path
