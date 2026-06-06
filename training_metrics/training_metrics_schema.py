"""
training_metrics/training_metrics_schema.py — TrainingMetrics schema v0.8.2

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice. No BUY/SELL/ORDER output.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Safety guard
# ---------------------------------------------------------------------------

_FORBIDDEN = ["BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER", "AUTO_TRADE", "REAL_TRADE"]


def _guard(text: str) -> None:
    """Raise ValueError if text contains a forbidden keyword."""
    upper = str(text).upper()
    for word in _FORBIDDEN:
        if word in upper:
            raise ValueError(
                f"[SAFETY] Forbidden keyword '{word}' detected in training_metrics output. "
                "Research Only. No Real Orders."
            )


# ---------------------------------------------------------------------------
# Metric type constants
# ---------------------------------------------------------------------------

METRIC_TASK_COMPLETION    = "TASK_COMPLETION"
METRIC_REPLAY_SCORE       = "REPLAY_SCORE"
METRIC_MISTAKE_REDUCTION  = "MISTAKE_REDUCTION"
METRIC_BACKTEST_ISSUE     = "BACKTEST_ISSUE"
METRIC_JOURNAL_IMPROVEMENT = "JOURNAL_IMPROVEMENT"
METRIC_MEMORY_VALIDATION  = "MEMORY_VALIDATION"
METRIC_RULE_REVIEW        = "RULE_REVIEW"
METRIC_DATA_FIX_PROGRESS  = "DATA_FIX_PROGRESS"
METRIC_TRAINING_STREAK    = "TRAINING_STREAK"
METRIC_QUALITY_SCORE      = "QUALITY_SCORE"

ALL_METRIC_TYPES = [
    METRIC_TASK_COMPLETION,
    METRIC_REPLAY_SCORE,
    METRIC_MISTAKE_REDUCTION,
    METRIC_BACKTEST_ISSUE,
    METRIC_JOURNAL_IMPROVEMENT,
    METRIC_MEMORY_VALIDATION,
    METRIC_RULE_REVIEW,
    METRIC_DATA_FIX_PROGRESS,
    METRIC_TRAINING_STREAK,
    METRIC_QUALITY_SCORE,
]

# ---------------------------------------------------------------------------
# Trend constants
# ---------------------------------------------------------------------------

TREND_IMPROVING  = "IMPROVING"
TREND_STABLE     = "STABLE"
TREND_WORSENING  = "WORSENING"
TREND_UNKNOWN    = "UNKNOWN"

# ---------------------------------------------------------------------------
# Status constants
# ---------------------------------------------------------------------------

STATUS_OK                = "OK"
STATUS_WARN              = "WARN"
STATUS_INSUFFICIENT_DATA = "INSUFFICIENT_DATA"

# ---------------------------------------------------------------------------
# Source constants
# ---------------------------------------------------------------------------

SOURCE_BACKTEST_COACH    = "backtest_coach"
SOURCE_REPLAY_TRAINING   = "replay_training"
SOURCE_STRATEGY_MEMORY   = "strategy_memory"
SOURCE_JOURNAL           = "journal"
SOURCE_REGRESSION        = "regression"
SOURCE_REPORT_PACK       = "report_pack"


# ---------------------------------------------------------------------------
# Dataclass: TrainingMetric
# ---------------------------------------------------------------------------

@dataclass
class TrainingMetric:
    """A single training effectiveness measurement.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    metric_id:       str
    metric_type:     str
    source_module:   str
    label:           str
    value:           float
    unit:            str
    trend:           str          = TREND_UNKNOWN
    status:          str          = STATUS_OK
    description:     str          = ""
    period:          str          = ""          # e.g. "2026-06-05" or "2026-W22"
    baseline:        Optional[float] = None
    delta:           Optional[float] = None
    note:            str          = ""
    generated_at:    str          = field(default_factory=lambda: datetime.now().isoformat())

    # Safety flags — always True
    read_only:          bool = field(default=True,  init=False)
    no_real_orders:     bool = field(default=True,  init=False)
    production_blocked: bool = field(default=True,  init=False)

    def __post_init__(self) -> None:
        _guard(self.label)
        _guard(self.description)
        _guard(self.note)
        # Safety flags are immutable
        object.__setattr__(self, "read_only",          True)
        object.__setattr__(self, "no_real_orders",     True)
        object.__setattr__(self, "production_blocked", True)

    def to_dict(self) -> dict:
        return {
            "metric_id":       self.metric_id,
            "metric_type":     self.metric_type,
            "source_module":   self.source_module,
            "label":           self.label,
            "value":           self.value,
            "unit":            self.unit,
            "trend":           self.trend,
            "status":          self.status,
            "description":     self.description,
            "period":          self.period,
            "baseline":        self.baseline,
            "delta":           self.delta,
            "note":            self.note,
            "generated_at":    self.generated_at,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "TrainingMetric":
        return cls(
            metric_id      = d.get("metric_id",     ""),
            metric_type    = d.get("metric_type",   ""),
            source_module  = d.get("source_module", ""),
            label          = d.get("label",         ""),
            value          = float(d.get("value",   0.0) or 0.0),
            unit           = d.get("unit",          ""),
            trend          = d.get("trend",         TREND_UNKNOWN),
            status         = d.get("status",        STATUS_OK),
            description    = d.get("description",   ""),
            period         = d.get("period",        ""),
            baseline       = float(d["baseline"]) if d.get("baseline") not in (None, "", "None") else None,
            delta          = float(d["delta"])    if d.get("delta")    not in (None, "", "None") else None,
            note           = d.get("note",          ""),
            generated_at   = d.get("generated_at",  ""),
        )


# ---------------------------------------------------------------------------
# Dataclass: TrainingMetricsSummary
# ---------------------------------------------------------------------------

@dataclass
class TrainingMetricsSummary:
    """Summary of all training effectiveness metrics.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    version:              str   = "v0.8.2"
    mode:                 str   = "real"
    period:               str   = ""
    total_metrics:        int   = 0
    improving_count:      int   = 0
    stable_count:         int   = 0
    worsening_count:      int   = 0
    insufficient_count:   int   = 0
    overall_trend:        str   = TREND_UNKNOWN
    overall_score:        float = 0.0
    task_completion_rate: float = 0.0
    replay_score_avg:     float = 0.0
    mistake_reduction_pct: float = 0.0
    memory_validation_rate: float = 0.0
    training_streak_days: int   = 0
    top_improving_metric: str   = ""
    top_worsening_metric: str   = ""
    no_real_orders:       bool  = True
    production_blocked:   bool  = True
    generated_at:         str   = field(default_factory=lambda: datetime.now().isoformat())

    # Safety flags — always True
    read_only: bool = field(default=True, init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "read_only",          True)
        object.__setattr__(self, "no_real_orders",     True)
        object.__setattr__(self, "production_blocked", True)

    def to_dict(self) -> dict:
        return {
            "version":               self.version,
            "mode":                  self.mode,
            "period":                self.period,
            "total_metrics":         self.total_metrics,
            "improving_count":       self.improving_count,
            "stable_count":          self.stable_count,
            "worsening_count":       self.worsening_count,
            "insufficient_count":    self.insufficient_count,
            "overall_trend":         self.overall_trend,
            "overall_score":         self.overall_score,
            "task_completion_rate":  self.task_completion_rate,
            "replay_score_avg":      self.replay_score_avg,
            "mistake_reduction_pct": self.mistake_reduction_pct,
            "memory_validation_rate": self.memory_validation_rate,
            "training_streak_days":  self.training_streak_days,
            "top_improving_metric":  self.top_improving_metric,
            "top_worsening_metric":  self.top_worsening_metric,
            "no_real_orders":        self.no_real_orders,
            "production_blocked":    self.production_blocked,
            "generated_at":          self.generated_at,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "TrainingMetricsSummary":
        return cls(
            version               = d.get("version",               "v0.8.2"),
            mode                  = d.get("mode",                  "real"),
            period                = d.get("period",                ""),
            total_metrics         = int(d.get("total_metrics",         0) or 0),
            improving_count       = int(d.get("improving_count",       0) or 0),
            stable_count          = int(d.get("stable_count",          0) or 0),
            worsening_count       = int(d.get("worsening_count",       0) or 0),
            insufficient_count    = int(d.get("insufficient_count",    0) or 0),
            overall_trend         = d.get("overall_trend",         TREND_UNKNOWN),
            overall_score         = float(d.get("overall_score",       0.0) or 0.0),
            task_completion_rate  = float(d.get("task_completion_rate", 0.0) or 0.0),
            replay_score_avg      = float(d.get("replay_score_avg",     0.0) or 0.0),
            mistake_reduction_pct = float(d.get("mistake_reduction_pct", 0.0) or 0.0),
            memory_validation_rate= float(d.get("memory_validation_rate", 0.0) or 0.0),
            training_streak_days  = int(d.get("training_streak_days",  0) or 0),
            top_improving_metric  = d.get("top_improving_metric",  ""),
            top_worsening_metric  = d.get("top_worsening_metric",  ""),
            no_real_orders        = bool(d.get("no_real_orders",   True)),
            production_blocked    = bool(d.get("production_blocked", True)),
            generated_at          = d.get("generated_at",          ""),
        )
