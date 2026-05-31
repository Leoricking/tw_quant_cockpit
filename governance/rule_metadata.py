"""
governance/rule_metadata.py — Rule metadata dataclass (v0.3.28).
[!] Research Only. No Real Orders. No Auto Weight Apply. Production Trading: BLOCKED.

Safety invariants:
  read_only = True
  no_real_orders = True
  production_blocked = True
  Research Only, No Real Orders, No Auto Weight Apply, Production Trading BLOCKED
"""

import os

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Status constants
# ---------------------------------------------------------------------------
RULE_STATUS_ACTIVE = "ACTIVE"
RULE_STATUS_EXPERIMENTAL = "EXPERIMENTAL"
RULE_STATUS_DISABLED = "DISABLED"
RULE_STATUS_DEPRECATED = "DEPRECATED"
RULE_STATUS_NEEDS_REVIEW = "NEEDS_REVIEW"
RULE_STATUS_INSUFFICIENT_SAMPLE = "INSUFFICIENT_SAMPLE"
RULE_STATUS_BLOCKED = "BLOCKED"

# ---------------------------------------------------------------------------
# Confidence constants
# ---------------------------------------------------------------------------
CONFIDENCE_HIGH = "HIGH"
CONFIDENCE_GOOD = "GOOD"
CONFIDENCE_PARTIAL = "PARTIAL"
CONFIDENCE_WEAK = "WEAK"
CONFIDENCE_LOW = "LOW"
CONFIDENCE_UNKNOWN = "UNKNOWN"
CONFIDENCE_PLANNED = "PLANNED"

_USABLE_STATUSES = {RULE_STATUS_ACTIVE, RULE_STATUS_EXPERIMENTAL}


class RuleMetadata:
    """
    Metadata describing a single strategy rule.

    Safety invariants:
      read_only = True
      no_real_orders = True
      production_blocked = True
      Research Only, No Real Orders, No Auto Weight Apply, Production Trading BLOCKED
    """

    # Safety flags at class level
    read_only: bool = True
    no_real_orders: bool = True
    production_blocked: bool = True

    def __init__(self, **kwargs):
        self.rule_id: str = kwargs.get("rule_id", "")
        self.rule_name: str = kwargs.get("rule_name", "")
        # one of: buy_point, screener, strategy_knowledge, long_term, portfolio,
        #         signal_quality, rule_weight, intraday, risk, data_quality,
        #         provider, governance
        self.category: str = kwargs.get("category", "")
        self.version: str = kwargs.get("version", "V1")
        # ACTIVE, EXPERIMENTAL, DISABLED, DEPRECATED, NEEDS_REVIEW,
        # INSUFFICIENT_SAMPLE, BLOCKED
        self.status: str = kwargs.get("status", RULE_STATUS_ACTIVE)
        self.enabled: bool = kwargs.get("enabled", True)
        self.experimental: bool = kwargs.get("experimental", False)
        self.description: str = kwargs.get("description", "")
        self.source_module: str = kwargs.get("source_module", "")
        self.source_file: str = kwargs.get("source_file", "")
        self.source_function: str = kwargs.get("source_function", "")
        # buy, sell, hold, screen, filter, quality, governance
        self.signal_type: str = kwargs.get("signal_type", "")
        # intraday, short, medium, long, portfolio, universal
        self.timeframe: str = kwargs.get("timeframe", "universal")
        self.required_data: list = list(kwargs.get("required_data", []))
        # list of rule_ids this rule depends on
        self.dependencies: list = list(kwargs.get("dependencies", []))
        # HIGH, GOOD, PARTIAL, WEAK, LOW, UNKNOWN, PLANNED
        self.confidence_level: str = kwargs.get("confidence_level", CONFIDENCE_UNKNOWN)
        self.sample_count: int = int(kwargs.get("sample_count", 0))
        self.last_validated_at: str = kwargs.get("last_validated_at", "")
        self.owner: str = kwargs.get("owner", "system")
        self.notes: str = kwargs.get("notes", "")
        self.safety_flags: dict = dict(kwargs.get(
            "safety_flags",
            {"read_only": True, "no_real_orders": True, "production_blocked": True},
        ))

    # ------------------------------------------------------------------
    def to_dict(self) -> dict:
        """Return all fields as a plain dictionary."""
        return {
            "rule_id": self.rule_id,
            "rule_name": self.rule_name,
            "category": self.category,
            "version": self.version,
            "status": self.status,
            "enabled": self.enabled,
            "experimental": self.experimental,
            "description": self.description,
            "source_module": self.source_module,
            "source_file": self.source_file,
            "source_function": self.source_function,
            "signal_type": self.signal_type,
            "timeframe": self.timeframe,
            "required_data": list(self.required_data),
            "dependencies": list(self.dependencies),
            "confidence_level": self.confidence_level,
            "sample_count": self.sample_count,
            "last_validated_at": self.last_validated_at,
            "owner": self.owner,
            "notes": self.notes,
            "safety_flags": dict(self.safety_flags),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "RuleMetadata":
        """Construct a RuleMetadata from a dictionary."""
        return cls(**d)

    def is_usable(self) -> bool:
        """Return True if rule is usable (ACTIVE or EXPERIMENTAL and not BLOCKED)."""
        if self.status == RULE_STATUS_BLOCKED:
            return False
        return self.status in _USABLE_STATUSES

    def __repr__(self) -> str:
        return (
            f"RuleMetadata(rule_id={self.rule_id!r}, status={self.status!r}, "
            f"confidence_level={self.confidence_level!r}, enabled={self.enabled})"
        )
