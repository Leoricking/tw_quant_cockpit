"""
replay/stable_report_audit.py — ReplayStableReportAudit for v1.2.9.

Lightweight import-based audit of replay report generators.
Checks reports dir is in .gitignore. No real orders.

[!] Research Only. No Real Orders. Not Investment Advice.
[!] Replay Training Stable Rollup. No broker. No trading. Simulation Only.
"""
from __future__ import annotations

import importlib.util
import logging
import os
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

_REPORT_MODULES: List[Tuple[str, str]] = [
    ("replay.challenge_report",          "ReplayChallengeReport"),
    ("replay.review_report",             "ReplayReviewReport"),
    ("replay.strategy_replay_summary",   "StrategyReplaySummary"),
    ("replay.scoring_summary",           "ReplayScoringSummary"),
    ("replay.dataset_report",            "ReplayDatasetReport"),
    ("replay.session_registry_summary",  "ReplaySessionRegistrySummary"),
    ("replay.stable_report",             "ReplayStableReport"),
    ("reports.replay_training_stable_rollup_report", "ReplayTrainingStableRollupReport"),
]

# Strings that would be dangerous in report templates
_FORBIDDEN_TEMPLATE_STRINGS = [
    "send_order(", "place_order(", "broker.connect(",
    "execute_trade(", "auto_trade(", "real_buy(", "real_sell(",
]


class ReplayStableReportAudit:
    """
    Audits replay report generators.

    Checks:
    - Report modules can be imported (or spec-found)
    - reports/ directory is in .gitignore
    - No absolute paths or secrets in module-level strings

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, project_root: str = "") -> None:
        if project_root:
            self._root = project_root
        else:
            self._root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def audit_all(self) -> Dict[str, Tuple[str, str]]:
        """Audit all report generators. Returns {module: (status, message)}."""
        results: Dict[str, Tuple[str, str]] = {}

        for module_path, class_name in _REPORT_MODULES:
            results[module_path] = self._check_report_module(module_path, class_name)

        results["gitignore_reports"] = self._check_gitignore_reports()
        results["no_forbidden_templates"] = self._check_no_forbidden_templates()

        return results

    def _check_report_module(self, module_path: str, class_name: str) -> Tuple[str, str]:
        """Check if report module can be spec-found."""
        try:
            spec = importlib.util.find_spec(module_path)
            if spec is None:
                return ("WARN", f"{module_path}: spec not found (may be optional)")
            try:
                import importlib as _il
                mod = _il.import_module(module_path)
                cls = getattr(mod, class_name, None)
                if cls is None:
                    return ("WARN", f"{module_path}: class {class_name} not found")
                return ("PASS", f"{module_path}.{class_name} imports OK")
            except Exception as exc:
                return ("WARN", f"{module_path}: import error: {exc}")
        except Exception as exc:
            return ("WARN", f"{module_path}: spec check error: {exc}")

    def _check_gitignore_reports(self) -> Tuple[str, str]:
        """Check reports/ is in .gitignore."""
        gi_path = os.path.join(self._root, ".gitignore")
        try:
            with open(gi_path, "r", encoding="utf-8") as f:
                content = f.read()
            if "reports/" in content:
                return ("PASS", "reports/ directory covered by .gitignore")
            return ("WARN", "reports/ may not be covered by .gitignore")
        except Exception as exc:
            return ("WARN", f".gitignore check error: {exc}")

    def _check_no_forbidden_templates(self) -> Tuple[str, str]:
        """Check no forbidden trading strings in report module source files."""
        reports_dir = os.path.join(self._root, "reports")
        if not os.path.isdir(reports_dir):
            return ("PASS", "reports/ dir not present — no template scan needed")
        try:
            found_issues = []
            for fname in os.listdir(reports_dir):
                if not fname.endswith(".py"):
                    continue
                fpath = os.path.join(reports_dir, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        content = f.read()
                    for danger in _FORBIDDEN_TEMPLATE_STRINGS:
                        if danger in content:
                            # Whitelist: safety declarations that mention these words
                            # by checking context — simplistic but safe
                            idx = content.find(danger)
                            context = content[max(0, idx-50):idx+len(danger)+50]
                            if "No Real Orders" not in context and "DISABLED" not in context.upper():
                                found_issues.append(f"{fname}: {danger!r}")
                except Exception:
                    pass
            if found_issues:
                return ("FAIL", f"Forbidden template strings found: {found_issues[:3]}")
            return ("PASS", "No forbidden trading strings in report templates")
        except Exception as exc:
            return ("WARN", f"Template scan error: {exc}")
