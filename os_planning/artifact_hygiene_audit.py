"""
os_planning/artifact_hygiene_audit.py — ArtifactHygieneAudit (v0.5.0).

Checks .gitignore coverage for all known research OS artifact patterns.
Ensures no generated data, logs, journals, or ML outputs are accidentally committed.

[!] OS Planning Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import csv
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ---------------------------------------------------------------------------
# Patterns to check — (pattern_to_search, risk_level, suggested_gitignore_rule)
# covered is determined at runtime by reading .gitignore
# ---------------------------------------------------------------------------

_PATTERNS: list[dict] = [
    {
        "pattern":               "data/backtest_results/",
        "risk_level":            "CRITICAL",
        "suggested_gitignore_rule": "data/backtest_results/",
        "covered":               "unknown",
    },
    {
        "pattern":               "reports/auto_report_center/",
        "risk_level":            "CRITICAL",
        "suggested_gitignore_rule": "reports/auto_report_center/",
        "covered":               "unknown",
    },
    {
        "pattern":               "logs/",
        "risk_level":            "CRITICAL",
        "suggested_gitignore_rule": "logs/",
        "covered":               "unknown",
    },
    {
        "pattern":               "journal_data/",
        "risk_level":            "CRITICAL",
        "suggested_gitignore_rule": "journal_data/",
        "covered":               "unknown",
    },
    {
        "pattern":               "experiments/EXP-",
        "risk_level":            "HIGH",
        "suggested_gitignore_rule": "experiments/EXP-*/",
        "covered":               "unknown",
    },
    {
        "pattern":               "experiments/registry.json",
        "risk_level":            "HIGH",
        "suggested_gitignore_rule": "experiments/registry.json",
        "covered":               "unknown",
    },
    {
        "pattern":               "data_cache/",
        "risk_level":            "HIGH",
        "suggested_gitignore_rule": "data_cache/",
        "covered":               "unknown",
    },
    {
        "pattern":               "knowledge/transcripts/",
        "risk_level":            "MEDIUM",
        "suggested_gitignore_rule": "knowledge/transcripts/",
        "covered":               "unknown",
    },
    {
        "pattern":               "data/backtest_results/research_workflow/",
        "risk_level":            "MEDIUM",
        "suggested_gitignore_rule": "data/backtest_results/research_workflow/",
        "covered":               "unknown",
    },
    {
        "pattern":               "data/backtest_results/research_coach/",
        "risk_level":            "MEDIUM",
        "suggested_gitignore_rule": "data/backtest_results/research_coach/",
        "covered":               "unknown",
    },
    {
        "pattern":               "data/backtest_results/research_review/",
        "risk_level":            "MEDIUM",
        "suggested_gitignore_rule": "data/backtest_results/research_review/",
        "covered":               "unknown",
    },
    {
        "pattern":               "logs/notifications/",
        "risk_level":            "HIGH",
        "suggested_gitignore_rule": "logs/notifications/",
        "covered":               "unknown",
    },
    {
        "pattern":               "data/ml_features/",
        "risk_level":            "HIGH",
        "suggested_gitignore_rule": "data/ml_features/",
        "covered":               "unknown",
    },
    {
        "pattern":               "replay_sessions/",
        "risk_level":            "HIGH",
        "suggested_gitignore_rule": "replay_sessions/",
        "covered":               "unknown",
    },
    {
        "pattern":               "model_monitoring/",
        "risk_level":            "HIGH",
        "suggested_gitignore_rule": "model_monitoring/",
        "covered":               "unknown",
    },
]


class ArtifactHygieneAudit:
    """Audits .gitignore coverage for all known research OS artifact patterns.

    [!] OS Planning Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True
    real_order_ready:   bool = False

    def __init__(self, base_dir: str | None = None) -> None:
        self.base_dir = base_dir or BASE_DIR
        self._gitignore_path = os.path.join(self.base_dir, ".gitignore")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self) -> dict:
        """Run the audit and return a summary dict."""
        try:
            gitignore_content = self._read_gitignore()
            rows = self._evaluate_patterns(gitignore_content)

            covered_count  = sum(1 for r in rows if r["covered"] == "yes")
            missing_count  = sum(1 for r in rows if r["covered"] == "no")
            critical_missing = [
                r["pattern"] for r in rows
                if r["covered"] == "no" and r["risk_level"] == "CRITICAL"
            ]
            high_missing = [
                r["pattern"] for r in rows
                if r["covered"] == "no" and r["risk_level"] == "HIGH"
            ]

            status = "PASS"
            if critical_missing:
                status = "CRITICAL"
            elif high_missing:
                status = "WARNING"

            return {
                "status":              status,
                "total_patterns":      len(rows),
                "covered":             covered_count,
                "missing":             missing_count,
                "critical_missing":    critical_missing,
                "high_missing":        high_missing,
                "gitignore_found":     os.path.isfile(self._gitignore_path),
                "rows":                rows,
                "read_only":           True,
                "no_real_orders":      True,
                "production_blocked":  True,
            }
        except Exception as exc:
            logger.warning("ArtifactHygieneAudit.run error: %s", exc)
            return {
                "status":             "ERROR",
                "error":              str(exc),
                "read_only":          True,
                "no_real_orders":     True,
                "production_blocked": True,
            }

    def export_audit(self, output_dir: str) -> str:
        """Write artifact_hygiene_audit.csv to output_dir. Returns path."""
        fieldnames = [
            "pattern", "covered", "risk_level", "suggested_gitignore_rule",
        ]
        try:
            os.makedirs(output_dir, exist_ok=True)
            today = datetime.now().strftime("%Y-%m-%d")
            path = os.path.join(output_dir, f"artifact_hygiene_audit_{today}.csv")
            gitignore_content = self._read_gitignore()
            rows = self._evaluate_patterns(gitignore_content)
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
                writer.writeheader()
                writer.writerows(rows)
            logger.info("artifact_hygiene_audit CSV saved: %s", path)
            return path
        except Exception as exc:
            logger.warning("export_audit error: %s", exc)
            fallback = os.path.join(output_dir or ".", "artifact_hygiene_audit_error.csv")
            return fallback

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _read_gitignore(self) -> str:
        """Read .gitignore content; return empty string if not found."""
        try:
            if not os.path.isfile(self._gitignore_path):
                logger.warning(".gitignore not found at %s", self._gitignore_path)
                return ""
            with open(self._gitignore_path, "r", encoding="utf-8", errors="replace") as f:
                return f.read()
        except Exception as exc:
            logger.warning("_read_gitignore error: %s", exc)
            return ""

    def _evaluate_patterns(self, gitignore_content: str) -> list[dict]:
        """Evaluate each pattern against .gitignore content."""
        rows: list[dict] = []
        try:
            for entry in _PATTERNS:
                covered = "yes" if entry["pattern"] in gitignore_content else "no"
                rows.append({
                    "pattern":               entry["pattern"],
                    "covered":               covered,
                    "risk_level":            entry["risk_level"],
                    "suggested_gitignore_rule": entry["suggested_gitignore_rule"],
                })
        except Exception as exc:
            logger.warning("_evaluate_patterns error: %s", exc)
        return rows
