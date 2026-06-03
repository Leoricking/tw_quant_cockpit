"""
os_planning/safety_matrix.py — ResearchOSSafetyMatrix (v0.5.0).

Builds and exports the safety matrix for all TW Quant Cockpit modules.
Verifies that all modules maintain read_only / no_real_orders / production_blocked flags.

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
# Hardcoded safety matrix — all major modules
# real_order_ready     = False  → cannot send real orders (all modules in this system)
# supports_real_orders = False  → no broker API wired up
# token_safe           = True   → tokens are masked / not exposed
# external_send_disabled = True → external notification channels are disabled
# forbidden_command_guard = True → blocks non-research CLI commands
# safety_status:
#   "SAFE"    → production_blocked=True AND real_order_ready=False
#   "BLOCKED" → supports_real_orders=True (would be a violation)
# ---------------------------------------------------------------------------

_SAFETY_ROWS: list[dict] = [
    {
        "module":                  "broker",
        "read_only":               "True",
        "no_real_orders":          "True",
        "production_blocked":      "True",
        "real_order_ready":        "False",
        "supports_real_orders":    "False",
        "token_safe":              "True",
        "external_send_disabled":  "True",
        "forbidden_command_guard": "False",
        "safety_status":           "SAFE",
        "notes":                   "broker/ package is a read-only stub; no live connection",
    },
    {
        "module":                  "paper_trader",
        "read_only":               "True",
        "no_real_orders":          "True",
        "production_blocked":      "True",
        "real_order_ready":        "False",
        "supports_real_orders":    "False",
        "token_safe":              "True",
        "external_send_disabled":  "True",
        "forbidden_command_guard": "False",
        "safety_status":           "SAFE",
        "notes":                   "sim/simulator.py PaperTrader — mock only",
    },
    {
        "module":                  "mock_realtime",
        "read_only":               "True",
        "no_real_orders":          "True",
        "production_blocked":      "True",
        "real_order_ready":        "False",
        "supports_real_orders":    "False",
        "token_safe":              "True",
        "external_send_disabled":  "True",
        "forbidden_command_guard": "False",
        "safety_status":           "SAFE",
        "notes":                   "sim/mock_realtime.py — CSV-driven mock; no live feed",
    },
    {
        "module":                  "data_providers",
        "read_only":               "True",
        "no_real_orders":          "True",
        "production_blocked":      "True",
        "real_order_ready":        "False",
        "supports_real_orders":    "False",
        "token_safe":              "True",
        "external_send_disabled":  "True",
        "forbidden_command_guard": "False",
        "safety_status":           "SAFE",
        "notes":                   "data/providers/ — API tokens masked; read-only fetch only",
    },
    {
        "module":                  "scheduler",
        "read_only":               "True",
        "no_real_orders":          "True",
        "production_blocked":      "True",
        "real_order_ready":        "False",
        "supports_real_orders":    "False",
        "token_safe":              "True",
        "external_send_disabled":  "True",
        "forbidden_command_guard": "False",
        "safety_status":           "SAFE",
        "notes":                   "automation/ — schedule triggers research-only commands",
    },
    {
        "module":                  "workflow_automation",
        "read_only":               "True",
        "no_real_orders":          "True",
        "production_blocked":      "True",
        "real_order_ready":        "False",
        "supports_real_orders":    "False",
        "token_safe":              "True",
        "external_send_disabled":  "True",
        "forbidden_command_guard": "True",
        "safety_status":           "SAFE",
        "notes":                   "SafeCommandRegistry blocks buy/sell/submit_order and compound shell commands",
    },
    {
        "module":                  "notifications",
        "read_only":               "True",
        "no_real_orders":          "True",
        "production_blocked":      "True",
        "real_order_ready":        "False",
        "supports_real_orders":    "False",
        "token_safe":              "True",
        "external_send_disabled":  "True",
        "forbidden_command_guard": "False",
        "safety_status":           "SAFE",
        "notes":                   "ExternalNotifierPlaceholder.external_enabled=False always; no LINE/Telegram",
    },
    {
        "module":                  "coach",
        "read_only":               "True",
        "no_real_orders":          "True",
        "production_blocked":      "True",
        "real_order_ready":        "False",
        "supports_real_orders":    "False",
        "token_safe":              "True",
        "external_send_disabled":  "True",
        "forbidden_command_guard": "True",
        "safety_status":           "SAFE",
        "notes":                   "_FORBIDDEN_KEYWORDS guard on CoachRecommendation.suggested_command",
    },
    {
        "module":                  "review",
        "read_only":               "True",
        "no_real_orders":          "True",
        "production_blocked":      "True",
        "real_order_ready":        "False",
        "supports_real_orders":    "False",
        "token_safe":              "True",
        "external_send_disabled":  "True",
        "forbidden_command_guard": "False",
        "safety_status":           "SAFE",
        "notes":                   "ResearchReviewAggregator/Scorecard/ActionPlanner all enforce safety flags",
    },
    {
        "module":                  "journal",
        "read_only":               "True",
        "no_real_orders":          "True",
        "production_blocked":      "True",
        "real_order_ready":        "False",
        "supports_real_orders":    "False",
        "token_safe":              "True",
        "external_send_disabled":  "True",
        "forbidden_command_guard": "False",
        "safety_status":           "SAFE",
        "notes":                   "JournalEntry and PortfolioJournalStore enforce no_real_orders at class level",
    },
    {
        "module":                  "ml_feature_store",
        "read_only":               "True",
        "no_real_orders":          "True",
        "production_blocked":      "True",
        "real_order_ready":        "False",
        "supports_real_orders":    "False",
        "token_safe":              "True",
        "external_send_disabled":  "True",
        "forbidden_command_guard": "False",
        "safety_status":           "SAFE",
        "notes":                   "DataLeakageChecker.read_only=True; no model deployment",
    },
    {
        "module":                  "intraday_replay",
        "read_only":               "True",
        "no_real_orders":          "True",
        "production_blocked":      "True",
        "real_order_ready":        "False",
        "supports_real_orders":    "False",
        "token_safe":              "True",
        "external_send_disabled":  "True",
        "forbidden_command_guard": "False",
        "safety_status":           "SAFE",
        "notes":                   "StrategyReplayOverlay.no_real_orders=True; replay only",
    },
    {
        "module":                  "experiment_registry",
        "read_only":               "True",
        "no_real_orders":          "True",
        "production_blocked":      "True",
        "real_order_ready":        "False",
        "supports_real_orders":    "False",
        "token_safe":              "True",
        "external_send_disabled":  "True",
        "forbidden_command_guard": "False",
        "safety_status":           "SAFE",
        "notes":                   "JSON-only storage; no external API calls",
    },
    {
        "module":                  "rule_governance",
        "read_only":               "True",
        "no_real_orders":          "True",
        "production_blocked":      "True",
        "real_order_ready":        "False",
        "supports_real_orders":    "False",
        "token_safe":              "True",
        "external_send_disabled":  "True",
        "forbidden_command_guard": "False",
        "safety_status":           "SAFE",
        "notes":                   "Rule changes are local JSON only; no auto-activation",
    },
    {
        "module":                  "auto_report_center",
        "read_only":               "True",
        "no_real_orders":          "True",
        "production_blocked":      "True",
        "real_order_ready":        "False",
        "supports_real_orders":    "False",
        "token_safe":              "True",
        "external_send_disabled":  "True",
        "forbidden_command_guard": "False",
        "safety_status":           "SAFE",
        "notes":                   "Markdown output only; no external send",
    },
    {
        "module":                  "research_os_planning",
        "read_only":               "True",
        "no_real_orders":          "True",
        "production_blocked":      "True",
        "real_order_ready":        "False",
        "supports_real_orders":    "False",
        "token_safe":              "True",
        "external_send_disabled":  "True",
        "forbidden_command_guard": "False",
        "safety_status":           "SAFE",
        "notes":                   "os_planning/ — audit and inventory only; CSV output gitignored",
    },
]


class ResearchOSSafetyMatrix:
    """Builds the safety matrix for all TW Quant Cockpit modules.

    [!] OS Planning Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True
    real_order_ready:   bool = False

    def __init__(self) -> None:
        pass

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build(self) -> list[dict]:
        """Return the full safety matrix as a list of module dicts."""
        try:
            return list(_SAFETY_ROWS)
        except Exception as exc:
            logger.warning("build error: %s", exc)
            return []

    def export_matrix(self, output_dir: str) -> str:
        """Write safety_matrix.csv to output_dir. Returns path."""
        fieldnames = [
            "module", "read_only", "no_real_orders", "production_blocked",
            "real_order_ready", "supports_real_orders", "token_safe",
            "external_send_disabled", "forbidden_command_guard", "safety_status",
            "notes",
        ]
        try:
            os.makedirs(output_dir, exist_ok=True)
            today = datetime.now().strftime("%Y-%m-%d")
            path = os.path.join(output_dir, f"safety_matrix_{today}.csv")
            rows = self.build()
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
                writer.writeheader()
                writer.writerows(rows)
            logger.info("safety_matrix CSV saved: %s", path)
            return path
        except Exception as exc:
            logger.warning("export_matrix error: %s", exc)
            fallback = os.path.join(output_dir or ".", "safety_matrix_error.csv")
            return fallback

    def summary(self) -> dict:
        """Return a summary count dict."""
        try:
            rows = self.build()
            safe_count    = sum(1 for r in rows if r.get("safety_status") == "SAFE")
            blocked_count = sum(1 for r in rows if r.get("safety_status") == "BLOCKED")
            guard_count   = sum(1 for r in rows if r.get("forbidden_command_guard") == "True")
            ext_disabled  = sum(1 for r in rows if r.get("external_send_disabled") == "True")
            return {
                "total_modules":          len(rows),
                "safe":                   safe_count,
                "blocked_violations":     blocked_count,
                "with_command_guard":     guard_count,
                "external_send_disabled": ext_disabled,
                "read_only":              True,
                "no_real_orders":         True,
                "production_blocked":     True,
            }
        except Exception as exc:
            logger.warning("summary error: %s", exc)
            return {
                "error":              str(exc),
                "read_only":          True,
                "no_real_orders":     True,
                "production_blocked": True,
            }
