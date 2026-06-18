"""
replay/session_registry_schema.py — Session Registry Schemas v1.2.8

Dataclasses and enums for Replay Session Registry, Bindings, and Lineage.

[!] Research Only. No Real Orders. Session Registry Only. No Broker.
[!] Session Registry does not execute trades. Not Investment Advice.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
SESSION_REGISTRY_ONLY = True


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class SessionType(str, Enum):
    STANDARD_REPLAY       = "STANDARD_REPLAY"
    SCENARIO_REPLAY       = "SCENARIO_REPLAY"
    MULTI_TIMEFRAME_REPLAY = "MULTI_TIMEFRAME_REPLAY"
    CHALLENGE_REPLAY      = "CHALLENGE_REPLAY"
    REVIEW_ONLY           = "REVIEW_ONLY"
    IMPORTED_REPLAY       = "IMPORTED_REPLAY"


class SessionStatus(str, Enum):
    ACTIVE       = "ACTIVE"
    PAUSED       = "PAUSED"
    COMPLETED    = "COMPLETED"
    ARCHIVED     = "ARCHIVED"
    ORPHANED     = "ORPHANED"
    BLOCKED      = "BLOCKED"
    INSUFFICIENT = "INSUFFICIENT"


class BindingType(str, Enum):
    DATASET     = "DATASET"
    SCENARIO    = "SCENARIO"
    JOURNAL     = "JOURNAL"
    SCORE       = "SCORE"
    MISTAKE     = "MISTAKE"
    STRATEGY    = "STRATEGY"
    TIMEFRAME   = "TIMEFRAME"
    REVIEW      = "REVIEW"
    CHALLENGE   = "CHALLENGE"
    REPORT      = "REPORT"
    CHECKPOINT  = "CHECKPOINT"
    FORK_PARENT = "FORK_PARENT"


class BindingStatus(str, Enum):
    VALID           = "VALID"
    MISSING         = "MISSING"
    STALE           = "STALE"
    HASH_MISMATCH   = "HASH_MISMATCH"
    VERSION_MISMATCH = "VERSION_MISMATCH"
    ORPHANED        = "ORPHANED"
    BLOCKED         = "BLOCKED"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ReplaySessionBinding:
    """Binding between a session and another artifact (dataset, scenario, etc.)."""
    binding_id:        str
    session_id:        str
    binding_type:      str                    # BindingType value
    target_id:         str
    target_version:    Optional[str]  = None
    target_fingerprint: Optional[str] = None
    required:          bool           = True
    status:            str            = BindingStatus.VALID.value
    created_at:        str            = ""
    updated_at:        str            = ""
    warning:           str            = ""

    research_only:     bool           = True
    no_real_orders:    bool           = True


@dataclass
class ReplaySessionRegistryRecord:
    """Full registry record for a replay session."""
    registry_record_id:       str
    session_id:               str
    session_type:             str                  = SessionType.STANDARD_REPLAY.value
    session_status:           str                  = SessionStatus.ACTIVE.value
    symbol:                   str                  = ""
    scenario_id:              Optional[str]        = None
    challenge_id:             Optional[str]        = None
    challenge_attempt_id:     Optional[str]        = None
    dataset_id:               Optional[str]        = None
    dataset_version:          Optional[str]        = None
    dataset_fingerprint:      Optional[str]        = None
    session_fingerprint:      Optional[str]        = None
    replay_start:             str                  = ""
    replay_end:               str                  = ""
    current_timestamp:        str                  = ""
    primary_timeframe:        str                  = "D1"
    enabled_timeframes:       List[str]            = field(default_factory=list)
    checkpoint_ids:           List[str]            = field(default_factory=list)
    fork_parent_session_id:   Optional[str]        = None
    lineage_root_session_id:  Optional[str]        = None
    journal_entry_ids:        List[str]            = field(default_factory=list)
    process_score_ids:        List[str]            = field(default_factory=list)
    outcome_score_ids:        List[str]            = field(default_factory=list)
    mistake_ids:              List[str]            = field(default_factory=list)
    strategy_snapshot_ids:    List[str]            = field(default_factory=list)
    timeframe_snapshot_ids:   List[str]            = field(default_factory=list)
    review_snapshot_ids:      List[str]            = field(default_factory=list)
    report_ids:               List[str]            = field(default_factory=list)
    point_in_time_verified:   bool                 = False
    mode:                     str                  = "MOCK"
    qualification:            str                  = "MOCK_DEMO_ONLY"
    created_at:               str                  = ""
    updated_at:               str                  = ""
    archived_at:              Optional[str]        = None
    warnings:                 List[str]            = field(default_factory=list)
    research_only:            bool                 = True
    no_real_orders:           bool                 = True
