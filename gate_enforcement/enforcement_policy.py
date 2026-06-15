"""
gate_enforcement.enforcement_policy — QualityGateEnforcementPolicy v1.1.5

Maps commands to gates, resolves default levels, and enforces policy rules.
Research Only. No Real Orders. Gate does NOT enable trading.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_DISABLED = True
RESEARCH_ONLY = True


class QualityGateEnforcementPolicy:
    """
    Policy rules for quality gate enforcement.

    [!] Research Only. No Real Orders.
    - mode=mock => DEMO_ONLY
    - off mode => QUALITY GATE DISABLED label
    - unknown gate => FAILED (no silent default)
    """

    POLICY_VERSION = "1.1.5"

    COMMAND_GATE_MAP = {
        "validate-score":               "PRICE_BACKTEST_GATE",
        "backtest-buy-points":          "BUY_POINT_GATE",
        "backtest-screener":            "SCREENER_GATE",
        "backtest-strategy-knowledge":  "STRATEGY_KNOWLEDGE_GATE",
        "strategy-validation":          "STRATEGY_KNOWLEDGE_GATE",
        "strategy-lab-dashboard":       "STRATEGY_KNOWLEDGE_GATE",
        "stock-report":                 "STOCK_REPORT_GATE",
        "screener":                     "SCREENER_GATE",
        "selector":                     "SCREENER_GATE",
        "local-assistant":              "LOCAL_ASSISTANT_GATE",
        "kb-context":                   "KB_CONTEXT_GATE",
    }

    # Gates that allow observational
    _ALLOW_OBSERVATIONAL = {
        "PRICE_BACKTEST_GATE",
        "BUY_POINT_GATE",
        "SCREENER_GATE",
        "STRATEGY_KNOWLEDGE_GATE",
        "STOCK_REPORT_GATE",
    }

    # Gates that allow demo
    _ALLOW_DEMO = {
        "PRICE_BACKTEST_GATE",
        "BUY_POINT_GATE",
        "SCREENER_GATE",
        "STRATEGY_KNOWLEDGE_GATE",
        "STOCK_REPORT_GATE",
        "LOCAL_ASSISTANT_GATE",
        "KB_CONTEXT_GATE",
    }

    # Gates that require enforcement
    _ENFORCEMENT_REQUIRED = {
        "PRICE_BACKTEST_GATE",
        "BUY_POINT_GATE",
        "SCREENER_GATE",
        "STRATEGY_KNOWLEDGE_GATE",
        "STOCK_REPORT_GATE",
    }

    # All audit-required gates
    _AUDIT_REQUIRED = set(COMMAND_GATE_MAP.values()) if False else None  # lazily built

    # Default levels per command/mode
    _DEFAULT_LEVELS = {
        "real": "FORMAL",
        "mock": "DEMO",
    }

    def resolve_gate(self, command_name: str) -> str:
        """Resolve gate name for command. Returns FAILED if unknown."""
        gate = self.COMMAND_GATE_MAP.get(command_name)
        if gate is None:
            # Unknown gate — do not silently default
            return "UNKNOWN_GATE"
        return gate

    def resolve_default_level(self, command_name: str, mode: str) -> str:
        """Resolve default quality level. mode=mock => DEMO."""
        if mode == "mock":
            return "DEMO"
        return self._DEFAULT_LEVELS.get(mode, "FORMAL")

    def allow_observational(self, command_name: str) -> bool:
        gate = self.resolve_gate(command_name)
        return gate in self._ALLOW_OBSERVATIONAL

    def allow_demo(self, command_name: str) -> bool:
        gate = self.resolve_gate(command_name)
        return gate in self._ALLOW_DEMO

    def module_gate(self, command_name: str, module_name: str = "") -> str:
        return self.resolve_gate(command_name)

    def enforcement_required(self, command_name: str) -> bool:
        gate = self.resolve_gate(command_name)
        return gate in self._ENFORCEMENT_REQUIRED

    def audit_required(self, command_name: str) -> bool:
        gate = self.resolve_gate(command_name)
        return gate != "UNKNOWN_GATE"

    def policy_version(self) -> str:
        return self.POLICY_VERSION

    def off_mode_label(self) -> str:
        return "QUALITY GATE DISABLED \u2014 RESULTS NOT FORMALLY QUALIFIED"

    def is_known_gate(self, gate_name: str) -> bool:
        all_gates = set(self.COMMAND_GATE_MAP.values())
        return gate_name in all_gates
