"""
cli/alias_map.py — CLIAliasMap for TW Quant Cockpit v0.5.1.

Maps short CLI aliases to canonical commands with optional default args.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No buy/sell/order/broker/shioaji alias permitted.
"""
from __future__ import annotations

import logging
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class CLIAliasMap:
    """
    Registry of all CLI short aliases for TW Quant Cockpit v0.5.1.

    Each alias entry contains:
      alias           — short command name
      target_command  — canonical command it resolves to
      default_args    — extra args merged at resolution time
      category        — command category
      description     — human-readable description
      safety_level    — safety classification
      enabled         — whether alias is active
      conflict        — True if alias shadows an existing canonical command
      conflict_reason — description of the conflict (if any)
      safety_blocked  — True if alias contains a blocked keyword
      safety_reason   — reason for the block (if any)

    Safety invariants
    -----------------
    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False
    """

    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True
    real_order_ready:   bool = False

    # Blocked keywords in alias name or target
    _BLOCKED_KEYWORDS: List[str] = [
        "buy", "sell", "order", "submit_order", "place_order", "broker",
        "shioaji", "live_trade", "auto_trade", "execute_trade", "margin",
        "short_sell", "cover_order", ".env", "token", "password", "api_key",
        "git", " cd ", "&&", ";", "||", "|", ">", "<",
    ]

    def __init__(self) -> None:
        self._aliases: List[dict] = []
        self._build_aliases()

    # ------------------------------------------------------------------
    # Internal builders
    # ------------------------------------------------------------------

    def _is_safe(self, alias: str, target: str) -> Tuple[bool, str]:
        """
        Check whether an alias name and target are free of blocked keywords.

        Returns (True, "") if safe, or (False, reason) if blocked.
        """
        combined = f"{alias} {target}".lower()
        for kw in self._BLOCKED_KEYWORDS:
            if kw.lower() in combined:
                return False, f"Blocked keyword detected: '{kw}'"
        return True, ""

    def _make_entry(
        self,
        alias:          str,
        target_command: str,
        default_args:   Dict,
        category:       str,
        description:    str,
        safety_level:   str = "SAFE_READ_ONLY",
        enabled:        bool = True,
        conflict:       bool = False,
        conflict_reason: str = "",
    ) -> dict:
        safe, reason = self._is_safe(alias, target_command)
        return {
            "alias":          alias,
            "target_command": target_command,
            "default_args":   default_args,
            "category":       category,
            "description":    description,
            "safety_level":   safety_level,
            "enabled":        enabled and safe,
            "conflict":       conflict,
            "conflict_reason": conflict_reason,
            "safety_blocked": not safe,
            "safety_reason":  reason,
        }

    def _build_aliases(self) -> None:
        """Populate the alias list."""
        entries = [
            # ----------------------------------------------------------------
            # Daily / workflow
            # ----------------------------------------------------------------
            self._make_entry(
                alias="daily",
                target_command="run-research",
                default_args={"profile": "daily", "mode": "real"},
                category="workflow",
                description="Run research pipeline with daily profile",
                safety_level="RESEARCH_ONLY",
            ),
            self._make_entry(
                alias="quick",
                target_command="run-research",
                default_args={"profile": "quick", "mode": "real"},
                category="workflow",
                description="Run research pipeline with quick profile",
                safety_level="RESEARCH_ONLY",
            ),
            self._make_entry(
                alias="workflow-daily",
                target_command="research-workflow",
                default_args={"type": "daily_research"},
                category="workflow",
                description="Run daily research workflow",
                safety_level="RESEARCH_ONLY",
            ),
            self._make_entry(
                alias="workflow-weekly",
                target_command="research-workflow",
                default_args={"type": "weekly_review"},
                category="workflow",
                description="Run weekly review workflow",
                safety_level="RESEARCH_ONLY",
            ),
            self._make_entry(
                alias="coach-daily",
                target_command="research-coach",
                default_args={"period": "daily"},
                category="coach",
                description="Run daily research coach session",
                safety_level="SAFE_READ_ONLY",
            ),
            self._make_entry(
                alias="review-daily",
                target_command="research-review",
                default_args={"period": "daily"},
                category="review",
                description="Run daily research review",
                safety_level="SAFE_READ_ONLY",
            ),
            # ----------------------------------------------------------------
            # Data
            # ----------------------------------------------------------------
            self._make_entry(
                alias="dq",
                target_command="data-quality-gate",
                default_args={},
                category="quality",
                description="Run data quality gate",
                safety_level="SAFE_READ_ONLY",
            ),
            self._make_entry(
                alias="quality",
                target_command="data-quality-gate",
                default_args={},
                category="quality",
                description="Run data quality gate (full name alias)",
                safety_level="SAFE_READ_ONLY",
            ),
            self._make_entry(
                alias="freshness",
                target_command="data-freshness",
                default_args={},
                category="data",
                description="Check data freshness",
                safety_level="SAFE_READ_ONLY",
            ),
            self._make_entry(
                alias="api-check",
                target_command="api-token-check",
                default_args={},
                category="provider",
                description="Check API token validity",
                safety_level="SAFE_READ_ONLY",
            ),
            self._make_entry(
                alias="api-diag",
                target_command="api-fetch-diagnostics",
                default_args={},
                category="provider",
                description="Run API fetch diagnostics",
                safety_level="SAFE_READ_ONLY",
            ),
            # ----------------------------------------------------------------
            # Provider
            # ----------------------------------------------------------------
            self._make_entry(
                alias="provider",
                target_command="provider-health",
                default_args={},
                category="provider",
                description="Run provider health check",
                safety_level="SAFE_READ_ONLY",
            ),
            self._make_entry(
                alias="providers",
                target_command="provider-reliability",
                default_args={},
                category="provider",
                description="Show provider reliability report",
                safety_level="REPORT_ONLY",
            ),
            # ----------------------------------------------------------------
            # Strategy / rules
            # ----------------------------------------------------------------
            self._make_entry(
                alias="rules",
                target_command="rule-governance",
                default_args={},
                category="strategy",
                description="Run rule governance check",
                safety_level="SAFE_READ_ONLY",
            ),
            self._make_entry(
                alias="signals",
                target_command="signal-quality",
                default_args={},
                category="strategy",
                description="Assess signal quality",
                safety_level="SAFE_READ_ONLY",
            ),
            self._make_entry(
                alias="weights",
                target_command="tune-rule-weights",
                default_args={},
                category="strategy",
                description="Tune rule weights",
                safety_level="SIMULATION_ONLY",
            ),
            self._make_entry(
                alias="strategy-knowledge",
                target_command="strategy-knowledge-summary",
                default_args={},
                category="strategy",
                description="Summarize strategy knowledge base",
                safety_level="SAFE_READ_ONLY",
            ),
            # ----------------------------------------------------------------
            # ML
            # ----------------------------------------------------------------
            self._make_entry(
                alias="ml-summary",
                target_command="ml-knowledge-feature-summary",
                default_args={},
                category="ml",
                description="Summarize ML knowledge features",
                safety_level="SAFE_READ_ONLY",
            ),
            self._make_entry(
                alias="ml-leakage",
                target_command="ml-knowledge-leakage-check",
                default_args={},
                category="ml",
                description="Check ML knowledge for data leakage",
                safety_level="SAFE_READ_ONLY",
            ),
            self._make_entry(
                alias="feature-store",
                target_command="ml-feature-store-report",
                default_args={},
                category="ml",
                description="Generate ML feature store report",
                safety_level="REPORT_ONLY",
            ),
            # ----------------------------------------------------------------
            # Replay
            # ----------------------------------------------------------------
            self._make_entry(
                alias="replay",
                target_command="intraday-replay",
                default_args={},
                category="replay",
                description="Run intraday replay session",
                safety_level="SIMULATION_ONLY",
            ),
            self._make_entry(
                alias="replay-report",
                target_command="intraday-replay-report",
                default_args={},
                category="replay",
                description="Generate intraday replay report",
                safety_level="REPORT_ONLY",
            ),
            self._make_entry(
                alias="replay-sessions",
                target_command="replay-session-list",
                default_args={},
                category="replay",
                description="List all replay sessions",
                safety_level="SAFE_READ_ONLY",
            ),
            # ----------------------------------------------------------------
            # Journal / notifications
            # ----------------------------------------------------------------
            self._make_entry(
                alias="journal",
                target_command="journal-summary",
                default_args={},
                category="journal",
                description="Show journal summary",
                safety_level="SAFE_READ_ONLY",
            ),
            self._make_entry(
                alias="notes",
                target_command="journal-list",
                default_args={},
                category="journal",
                description="List journal entries",
                safety_level="SAFE_READ_ONLY",
            ),
            self._make_entry(
                alias="notify",
                target_command="notification-list",
                default_args={},
                category="notification",
                description="List notifications",
                safety_level="SAFE_READ_ONLY",
            ),
            self._make_entry(
                alias="alerts",
                target_command="notification-list",
                default_args={},
                category="notification",
                description="List alerts and notifications",
                safety_level="SAFE_READ_ONLY",
            ),
            # ----------------------------------------------------------------
            # OS / release
            # ----------------------------------------------------------------
            self._make_entry(
                alias="os",
                target_command="research-os-summary",
                default_args={},
                category="os_planning",
                description="Print research OS summary",
                safety_level="SAFE_READ_ONLY",
            ),
            self._make_entry(
                alias="os-audit",
                target_command="research-os-audit",
                default_args={},
                category="os_planning",
                description="Run research OS audit",
                safety_level="SAFE_READ_ONLY",
            ),
            self._make_entry(
                alias="version",
                target_command="version-info",
                default_args={},
                category="utility",
                description="Show version info",
                safety_level="SAFE_READ_ONLY",
            ),
            self._make_entry(
                alias="release-check",
                target_command="stable-release-check",
                default_args={},
                category="release",
                description="Run stable release check",
                safety_level="SAFE_READ_ONLY",
            ),
            self._make_entry(
                alias="regress",
                target_command="regression-suite",
                default_args={"quick": True},
                category="release",
                description="Run quick regression suite",
                safety_level="SIMULATION_ONLY",
            ),
            # ----------------------------------------------------------------
            # GUI
            # ----------------------------------------------------------------
            self._make_entry(
                alias="gui",
                target_command="cockpit",
                default_args={},
                category="gui",
                description="Launch the Cockpit GUI",
                safety_level="GUI_ONLY",
            ),
            self._make_entry(
                alias="dashboard",
                target_command="cockpit",
                default_args={},
                category="gui",
                description="Launch the dashboard (cockpit)",
                safety_level="GUI_ONLY",
            ),
            self._make_entry(
                alias="open",
                target_command="cockpit",
                default_args={},
                category="gui",
                description="Open the cockpit GUI",
                safety_level="GUI_ONLY",
            ),
        ]

        self._aliases = entries
        blocked = [e["alias"] for e in entries if e["safety_blocked"]]
        if blocked:
            logger.error("CLIAliasMap: safety-blocked aliases detected: %s", blocked)
        logger.debug(
            "CLIAliasMap built: %d aliases (%d blocked, %d conflicts).",
            len(entries),
            len(blocked),
            sum(1 for e in entries if e["conflict"]),
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def list_aliases(self, category: Optional[str] = None) -> List[dict]:
        """Return all alias entries, optionally filtered by category."""
        if category:
            return [a for a in self._aliases if a["category"] == category]
        return list(self._aliases)

    def get_alias(self, alias: str) -> Optional[dict]:
        """Return alias entry by alias name, or None."""
        for entry in self._aliases:
            if entry["alias"] == alias:
                return entry
        return None

    def get_target(self, alias: str) -> Optional[Tuple[str, dict]]:
        """Return (target_command, default_args) for an alias, or None."""
        entry = self.get_alias(alias)
        if entry and entry["enabled"]:
            return entry["target_command"], entry["default_args"]
        return None

    def list_conflicts(self) -> List[dict]:
        """Return alias entries that have conflict=True."""
        return [a for a in self._aliases if a["conflict"]]

    def count_aliases(self) -> int:
        """Return total number of registered aliases."""
        return len(self._aliases)

    def count_conflicts(self) -> int:
        """Return number of conflicting aliases."""
        return sum(1 for a in self._aliases if a["conflict"])

    def is_registered(self, alias: str) -> bool:
        """Return True if the alias is registered."""
        return any(a["alias"] == alias for a in self._aliases)
