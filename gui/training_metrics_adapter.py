"""
gui/training_metrics_adapter.py — TrainingMetricsAdapter v0.8.2

Bridge between the GUI panel and the training_metrics package.
All methods catch exceptions and return safe defaults.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice. No BUY/SELL/ORDER output.
"""
from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_METRICS_DIR = os.path.join(_BASE_DIR, "data", "backtest_results", "training_metrics")

_FORBIDDEN_CMD_KEYWORDS = ["BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER", "AUTO_TRADE", "REAL_TRADE"]


def _is_safe_command(cmd: str) -> bool:
    """Return False if cmd contains any forbidden keyword."""
    upper = cmd.upper()
    return not any(kw in upper for kw in _FORBIDDEN_CMD_KEYWORDS)


class TrainingMetricsAdapter:
    """Provides GUI-safe access to training metrics data.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(self, output_dir: str = _DEFAULT_METRICS_DIR) -> None:
        self.output_dir = output_dir

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_summary(self) -> dict:
        """Return latest summary dict, or empty dict on error."""
        try:
            from training_metrics.training_metrics_store import TrainingMetricsStore
            store   = TrainingMetricsStore(output_dir=self.output_dir)
            summary = store.load_latest_summary()
            if summary is not None:
                return summary.to_dict()
        except Exception as exc:
            logger.warning("TrainingMetricsAdapter.get_summary: %s", exc)
        return {}

    def get_metrics(self) -> list:
        """Return latest metrics as list of dicts, or [] on error."""
        try:
            from training_metrics.training_metrics_store import TrainingMetricsStore
            store   = TrainingMetricsStore(output_dir=self.output_dir)
            metrics = store.load_latest_metrics()
            return [m.to_dict() for m in metrics]
        except Exception as exc:
            logger.warning("TrainingMetricsAdapter.get_metrics: %s", exc)
        return []

    def run_engine(self, mode: str = "real") -> dict:
        """Run the training metrics engine and return result dict."""
        try:
            from training_metrics.training_metrics_engine import TrainingMetricsEngine
            engine = TrainingMetricsEngine(
                project_root=_BASE_DIR,
                output_dir=self.output_dir,
            )
            result = engine.run(mode=mode)
            return {
                "metrics": [m.to_dict() for m in result.get("metrics", [])],
                "summary": result["summary"].to_dict() if result.get("summary") else {},
                "mode":    result.get("mode", mode),
            }
        except Exception as exc:
            logger.warning("TrainingMetricsAdapter.run_engine: %s", exc)
        return {"metrics": [], "summary": {}, "mode": mode}

    def get_safe_commands(self) -> list:
        """Return safe CLI commands for the training_metrics feature."""
        raw_cmds = [
            "python main.py training-metrics --mode real",
            "python main.py training-metrics-summary",
            "python main.py training-metrics-report --mode real",
            "python main.py training-metrics-trend",
        ]
        return [c for c in raw_cmds if _is_safe_command(c)]
