"""
experiments/experiment_metadata.py — ExperimentMetadata dataclass and constants (v0.3.29).
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""

import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Status constants
# ---------------------------------------------------------------------------
CREATED = "CREATED"
RUNNING = "RUNNING"
COMPLETED = "COMPLETED"
PARTIAL = "PARTIAL"
FAILED = "FAILED"
ARCHIVED = "ARCHIVED"

# ---------------------------------------------------------------------------
# Type constants
# ---------------------------------------------------------------------------
DAILY_RESEARCH = "daily_research"
HARDENED_BACKTEST = "hardened_backtest"
SIGNAL_QUALITY = "signal_quality"
RULE_WEIGHT_TUNING = "rule_weight_tuning"
INTRADAY_RESEARCH = "intraday_research"
UNIVERSE_RESEARCH = "universe_research"
PORTFOLIO_SIMULATION = "portfolio_simulation"
MANUAL_NOTE = "manual_note"

_ACTIVE_STATUSES = {RUNNING, CREATED, PARTIAL}


# ---------------------------------------------------------------------------
# ID generation helper
# ---------------------------------------------------------------------------

def generate_experiment_id() -> str:
    """EXP-YYYYMMDD-HHMMSS-shortuuid (8 hex chars)"""
    import datetime
    import uuid
    now = datetime.datetime.now()
    short = uuid.uuid4().hex[:8]
    return f"EXP-{now.strftime('%Y%m%d')}-{now.strftime('%H%M%S')}-{short}"


# ---------------------------------------------------------------------------
# ExperimentMetadata dataclass
# ---------------------------------------------------------------------------

@dataclass
class ExperimentMetadata:
    """
    Immutable research-only metadata for a single experiment run.
    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    experiment_id: str

    # Descriptive
    experiment_name: str = ""
    experiment_type: str = DAILY_RESEARCH
    status: str = CREATED
    mode: str = "real"
    profile: str = "standard"

    # Timestamps & identity
    created_at: str = ""          # ISO format
    created_by: str = "TW Quant Cockpit"
    git_commit: str = ""
    git_tag: str = ""

    # Research scope
    universe_name: str = ""
    universe_size: int = 0
    strategy_scope: str = ""
    data_start: str = ""
    data_end: str = ""
    notes: str = ""
    tags: list = field(default_factory=list)

    # Safety invariants — must never be changed
    read_only: bool = True
    no_real_orders: bool = True
    production_blocked: bool = True

    # Provenance
    source_command: str = ""
    parent_experiment_id: str = ""

    # Linked artefacts
    # snapshot_type -> {path, summary, generated_at}
    snapshots: dict = field(default_factory=dict)
    # list of {name, path, summary, generated_at}
    reports: list = field(default_factory=list)

    # ------------------------------------------------------------------
    # Serialisation helpers
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Return all fields as a plain dict."""
        return {
            "experiment_id": self.experiment_id,
            "experiment_name": self.experiment_name,
            "experiment_type": self.experiment_type,
            "status": self.status,
            "mode": self.mode,
            "profile": self.profile,
            "created_at": self.created_at,
            "created_by": self.created_by,
            "git_commit": self.git_commit,
            "git_tag": self.git_tag,
            "universe_name": self.universe_name,
            "universe_size": self.universe_size,
            "strategy_scope": self.strategy_scope,
            "data_start": self.data_start,
            "data_end": self.data_end,
            "notes": self.notes,
            "tags": list(self.tags),
            "read_only": self.read_only,
            "no_real_orders": self.no_real_orders,
            "production_blocked": self.production_blocked,
            "source_command": self.source_command,
            "parent_experiment_id": self.parent_experiment_id,
            "snapshots": self.snapshots,
            "reports": self.reports,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ExperimentMetadata":
        """Reconstruct from a plain dict (e.g. loaded from JSON)."""
        try:
            return cls(
                experiment_id=d.get("experiment_id", ""),
                experiment_name=d.get("experiment_name", ""),
                experiment_type=d.get("experiment_type", DAILY_RESEARCH),
                status=d.get("status", CREATED),
                mode=d.get("mode", "real"),
                profile=d.get("profile", "standard"),
                created_at=d.get("created_at", ""),
                created_by=d.get("created_by", "TW Quant Cockpit"),
                git_commit=d.get("git_commit", ""),
                git_tag=d.get("git_tag", ""),
                universe_name=d.get("universe_name", ""),
                universe_size=int(d.get("universe_size", 0)),
                strategy_scope=d.get("strategy_scope", ""),
                data_start=d.get("data_start", ""),
                data_end=d.get("data_end", ""),
                notes=d.get("notes", ""),
                tags=list(d.get("tags", [])),
                read_only=bool(d.get("read_only", True)),
                no_real_orders=bool(d.get("no_real_orders", True)),
                production_blocked=bool(d.get("production_blocked", True)),
                source_command=d.get("source_command", ""),
                parent_experiment_id=d.get("parent_experiment_id", ""),
                snapshots=dict(d.get("snapshots", {})),
                reports=list(d.get("reports", [])),
            )
        except Exception:
            logger.exception("ExperimentMetadata.from_dict failed; returning minimal object")
            return cls(experiment_id=d.get("experiment_id", "UNKNOWN"))

    def is_active(self) -> bool:
        """Return True if the experiment is in an active state."""
        return self.status in _ACTIVE_STATUSES
