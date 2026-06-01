"""
journal/journal_schema.py — JournalEntry schema (v0.4.6).

Defines the research-only portfolio journal entry dataclass and all constants.

[!] Journal Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Not investment advice. No broker order ID. No real execution fills.
[!] Does NOT contain token / password / secret.
"""
from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Entry type constants
# ---------------------------------------------------------------------------
ENTRY_SIMULATED_TRADE  = "simulated_trade"
ENTRY_PAPER_TRADE      = "paper_trade"
ENTRY_REPLAY_NOTE      = "replay_note"
ENTRY_SIGNAL_REVIEW    = "signal_review"
ENTRY_PORTFOLIO_REVIEW = "portfolio_review"
ENTRY_MANUAL_NOTE      = "manual_note"

ALL_ENTRY_TYPES = [
    ENTRY_SIMULATED_TRADE,
    ENTRY_PAPER_TRADE,
    ENTRY_REPLAY_NOTE,
    ENTRY_SIGNAL_REVIEW,
    ENTRY_PORTFOLIO_REVIEW,
    ENTRY_MANUAL_NOTE,
]

# ---------------------------------------------------------------------------
# Status constants
# ---------------------------------------------------------------------------
STATUS_PLANNED          = "PLANNED"
STATUS_OPEN_SIMULATED   = "OPEN_SIMULATED"
STATUS_CLOSED_SIMULATED = "CLOSED_SIMULATED"
STATUS_REVIEWED         = "REVIEWED"
STATUS_CANCELLED        = "CANCELLED"
STATUS_INVALIDATED      = "INVALIDATED"
STATUS_ARCHIVED         = "ARCHIVED"

ALL_STATUSES = [
    STATUS_PLANNED,
    STATUS_OPEN_SIMULATED,
    STATUS_CLOSED_SIMULATED,
    STATUS_REVIEWED,
    STATUS_CANCELLED,
    STATUS_INVALIDATED,
    STATUS_ARCHIVED,
]

# ---------------------------------------------------------------------------
# Outcome label constants
# ---------------------------------------------------------------------------
OUTCOME_WIN                  = "WIN"
OUTCOME_LOSS                 = "LOSS"
OUTCOME_BREAKEVEN            = "BREAKEVEN"
OUTCOME_MISSED_OPPORTUNITY   = "MISSED_OPPORTUNITY"
OUTCOME_AVOIDED_BAD_TRADE    = "AVOIDED_BAD_TRADE"
OUTCOME_FALSE_SIGNAL         = "FALSE_SIGNAL"
OUTCOME_GOOD_PROCESS_BAD_OUTCOME = "GOOD_PROCESS_BAD_OUTCOME"
OUTCOME_BAD_PROCESS_GOOD_OUTCOME = "BAD_PROCESS_GOOD_OUTCOME"
OUTCOME_NEEDS_REVIEW         = "NEEDS_REVIEW"
OUTCOME_UNKNOWN              = "UNKNOWN"

ALL_OUTCOME_LABELS = [
    OUTCOME_WIN,
    OUTCOME_LOSS,
    OUTCOME_BREAKEVEN,
    OUTCOME_MISSED_OPPORTUNITY,
    OUTCOME_AVOIDED_BAD_TRADE,
    OUTCOME_FALSE_SIGNAL,
    OUTCOME_GOOD_PROCESS_BAD_OUTCOME,
    OUTCOME_BAD_PROCESS_GOOD_OUTCOME,
    OUTCOME_NEEDS_REVIEW,
    OUTCOME_UNKNOWN,
]

# ---------------------------------------------------------------------------
# Mistake tag constants
# ---------------------------------------------------------------------------
MISTAKE_CHASE_HIGH                   = "chase_high"
MISTAKE_IGNORED_STOP                 = "ignored_stop"
MISTAKE_OVERSIZED_POSITION           = "oversized_position"
MISTAKE_BOUGHT_WEAK_STOCK            = "bought_weak_stock"
MISTAKE_IGNORED_DATA_QUALITY         = "ignored_data_quality"
MISTAKE_IGNORED_PROVIDER_WARNING     = "ignored_provider_warning"
MISTAKE_IGNORED_FAKE_BREAKOUT        = "ignored_fake_breakout"
MISTAKE_IGNORED_VWAP_LOSS            = "ignored_vwap_loss"
MISTAKE_IGNORED_TOP_PATTERN          = "ignored_top_pattern"
MISTAKE_IGNORED_FUNDAMENTAL_DETERIORATION = "ignored_fundamental_deterioration"
MISTAKE_NO_PLAN                      = "no_plan"
MISTAKE_EMOTIONAL_TRADE              = "emotional_trade"
MISTAKE_OVERTRADING                  = "overtrading"

ALL_MISTAKE_TAGS = [
    MISTAKE_CHASE_HIGH,
    MISTAKE_IGNORED_STOP,
    MISTAKE_OVERSIZED_POSITION,
    MISTAKE_BOUGHT_WEAK_STOCK,
    MISTAKE_IGNORED_DATA_QUALITY,
    MISTAKE_IGNORED_PROVIDER_WARNING,
    MISTAKE_IGNORED_FAKE_BREAKOUT,
    MISTAKE_IGNORED_VWAP_LOSS,
    MISTAKE_IGNORED_TOP_PATTERN,
    MISTAKE_IGNORED_FUNDAMENTAL_DETERIORATION,
    MISTAKE_NO_PLAN,
    MISTAKE_EMOTIONAL_TRADE,
    MISTAKE_OVERTRADING,
]

# ---------------------------------------------------------------------------
# Blocked fields (never include in journal metadata)
# ---------------------------------------------------------------------------
_BLOCKED_FIELDS = {
    "token", "password", "secret", "api_key", "access_key",
    "env", "credential", "private_key", "auth", "broker_order_id",
    "execution_id", "fill_price", "real_order",
}


def _sanitize(meta: dict) -> dict:
    """Remove any keys matching security patterns."""
    return {
        k: v for k, v in (meta or {}).items()
        if not any(b in k.lower() for b in _BLOCKED_FIELDS)
    }


# ---------------------------------------------------------------------------
# JournalEntry
# ---------------------------------------------------------------------------

@dataclass
class JournalEntry:
    """
    A single research-only portfolio journal / trade review entry.

    Safety:
      read_only          = True  (always)
      no_real_orders     = True  (always)
      production_blocked = True  (always)
      No broker order ID. No real execution fills. No token.

    [!] Journal Only. Research Only. No Real Orders.
    """
    # Core identity
    journal_id:         str  = field(default_factory=lambda: f"JOURNAL-{uuid.uuid4().hex[:12].upper()}")
    created_at:         str  = field(default_factory=lambda: datetime.now().isoformat())
    updated_at:         str  = field(default_factory=lambda: datetime.now().isoformat())

    # Classification
    entry_type:         str  = ENTRY_MANUAL_NOTE
    mode:               str  = "simulation"
    status:             str  = STATUS_PLANNED

    # Instrument
    symbol:             str  = ""
    name:               str  = ""
    side:               str  = ""        # long / short / flat / unknown
    timeframe:          str  = ""

    # Signal / strategy linkage
    strategy_tags:      List[str] = field(default_factory=list)
    signal_source:      str  = ""
    signal_id:          str  = ""
    rule_ids:           List[str] = field(default_factory=list)
    experiment_id:      str  = ""
    replay_session_id:  str  = ""
    portfolio_scenario: str  = ""

    # Price plan
    planned_entry_price:  Optional[float] = None
    planned_exit_price:   Optional[float] = None
    planned_stop_loss:    Optional[float] = None
    planned_take_profit:  Optional[float] = None

    # Actual outcome (filled during review)
    actual_entry_price:  Optional[float] = None
    actual_exit_price:   Optional[float] = None
    actual_return_pct:   Optional[float] = None
    max_favorable_excursion: Optional[float] = None   # MFE
    max_adverse_excursion:   Optional[float] = None   # MAE
    holding_days:        Optional[int]   = None
    position_size_pct:   Optional[float] = None

    # Research notes
    reason:              str  = ""
    thesis:              str  = ""
    invalidation_condition: str = ""
    review_notes:        str  = ""

    # Review / outcome
    mistake_tags:        List[str] = field(default_factory=list)
    outcome_label:       str  = OUTCOME_UNKNOWN
    confidence_before:   Optional[int] = None   # 1-10
    confidence_after:    Optional[int] = None   # 1-10

    # Related resources
    related_reports:     List[str] = field(default_factory=list)
    related_notifications: List[str] = field(default_factory=list)

    # Safety invariants (always True)
    read_only:           bool = True
    no_real_orders:      bool = True
    production_blocked:  bool = True

    def __post_init__(self):
        # Enforce safety invariants
        self.read_only         = True
        self.no_real_orders    = True
        self.production_blocked = True
        # Validate enum fields
        if self.entry_type not in ALL_ENTRY_TYPES:
            self.entry_type = ENTRY_MANUAL_NOTE
        if self.status not in ALL_STATUSES:
            self.status = STATUS_PLANNED
        if self.outcome_label not in ALL_OUTCOME_LABELS:
            self.outcome_label = OUTCOME_UNKNOWN
        # Validate mistake_tags
        self.mistake_tags = [t for t in self.mistake_tags if t in ALL_MISTAKE_TAGS]

    def touch(self) -> None:
        """Update updated_at timestamp."""
        self.updated_at = datetime.now().isoformat()

    def needs_review(self) -> bool:
        return self.status in (STATUS_CLOSED_SIMULATED,) and self.outcome_label == OUTCOME_UNKNOWN

    def to_dict(self) -> dict:
        d = asdict(self)
        # Never leak safety-sensitive keys
        for k in list(d.keys()):
            if any(b in k.lower() for b in _BLOCKED_FIELDS):
                del d[k]
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_dict(cls, d: dict) -> "JournalEntry":
        """Reconstruct from dict. Enforces safety invariants."""
        safe = {
            k: v for k, v in d.items()
            if k in cls.__dataclass_fields__
            and k not in ("read_only", "no_real_orders", "production_blocked")
        }
        obj = cls(**safe)
        return obj
