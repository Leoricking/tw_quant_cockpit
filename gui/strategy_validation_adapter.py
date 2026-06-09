# gui/strategy_validation_adapter.py
# TW Quant Cockpit — Strategy Validation GUI Adapter
# v0.9.2 — Research Only / No Real Orders / VALIDATED does not enable trading
#
# DISCLAIMER: Research purposes ONLY. No real orders. Production trading BLOCKED.
# VALIDATED grade = research validated ONLY. Does NOT enable trading.

from __future__ import annotations

import logging
import os
from typing import List

logger = logging.getLogger(__name__)

VERSION = "v0.9.2"

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _as_list(obj) -> list:
    if isinstance(obj, list):
        return obj
    if obj is None:
        return []
    return [obj]


def _to_dict(obj) -> dict:
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    return {}


def _to_dicts(objs) -> list:
    return [_to_dict(o) for o in _as_list(objs)]


class StrategyValidationAdapter:
    """
    GUI ↔ backend bridge for StrategyValidation package.

    All methods catch exceptions and return safe defaults.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    [!] VALIDATED does not enable trading.
    """

    read_only = True
    no_real_orders = True
    production_blocked = True
    validated_does_not_enable_trading = True

    _FORBIDDEN = frozenset([
        "BUY", "SELL", "ORDER", "EXECUTE",
        "SUBMIT_ORDER", "AUTO_TRADE", "REAL_TRADE",
    ])

    def __init__(self, output_dir: str = "data/strategy_validation") -> None:
        if not os.path.isabs(output_dir):
            output_dir = os.path.join(_BASE_DIR, output_dir)
        self._output_dir = output_dir

    # ------------------------------------------------------------------
    # Engine
    # ------------------------------------------------------------------

    def run_validation(self, mode: str = "real") -> dict:
        """
        Run StrategyValidationEngine and return result dict.
        Returns error dict on failure.
        """
        try:
            from strategy_validation.validation_engine import StrategyValidationEngine
            engine = StrategyValidationEngine()
            result = engine.run(mode=mode)
            if not isinstance(result, dict):
                result = {}
            scores = _to_dicts(result.get("scores", []))
            components = _to_dicts(result.get("components", []))
            raw_summary = result.get("summary")
            summary = _to_dict(raw_summary) if raw_summary is not None else {}
            return {
                "ok": True,
                "scores": scores,
                "components": components,
                "summary": summary,
                "no_real_orders": True,
                "production_blocked": True,
                "validated_does_not_enable_trading": True,
            }
        except Exception as exc:
            logger.warning("StrategyValidationAdapter.run_validation: %s", exc)
            return {
                "ok": False,
                "error": str(exc),
                "scores": [],
                "components": [],
                "summary": {},
                "no_real_orders": True,
                "production_blocked": True,
            }

    # ------------------------------------------------------------------
    # Store loaders
    # ------------------------------------------------------------------

    def load_latest_summary(self) -> dict:
        """Load latest validation summary. Returns dict."""
        try:
            from strategy_validation.validation_store import StrategyValidationStore
            store = StrategyValidationStore()
            raw = store.load_latest_summary()
            return _to_dict(raw) if raw is not None else {}
        except Exception as exc:
            logger.warning("StrategyValidationAdapter.load_latest_summary: %s", exc)
            return {}

    def load_scores(self) -> list:
        """Load latest validation scores. Returns list of dicts."""
        try:
            from strategy_validation.validation_store import StrategyValidationStore
            store = StrategyValidationStore()
            return _to_dicts(store.load_latest_scores() or [])
        except Exception as exc:
            logger.warning("StrategyValidationAdapter.load_scores: %s", exc)
            return []

    def load_components(self) -> list:
        """Load latest evidence components. Returns list of dicts."""
        try:
            from strategy_validation.validation_store import StrategyValidationStore
            store = StrategyValidationStore()
            return _to_dicts(store.load_latest_components() or [])
        except Exception as exc:
            logger.warning("StrategyValidationAdapter.load_components: %s", exc)
            return []

    # ------------------------------------------------------------------
    # Query helpers
    # ------------------------------------------------------------------

    def get_top_validated(self, limit: int = 10) -> list:
        """Return top VALIDATED strategies by score."""
        try:
            from strategy_validation.validation_query import StrategyValidationQuery
            query = StrategyValidationQuery()
            return _to_dicts(query.top_validated(limit=limit) or [])
        except Exception as exc:
            logger.warning("StrategyValidationAdapter.get_top_validated: %s", exc)
            return []

    def get_needs_backtest(self, limit: int = 10) -> list:
        """Return strategies that need backtest."""
        try:
            from strategy_validation.validation_query import StrategyValidationQuery
            query = StrategyValidationQuery()
            return _to_dicts(query.needs_backtest(limit=limit) or [])
        except Exception as exc:
            logger.warning("StrategyValidationAdapter.get_needs_backtest: %s", exc)
            return []

    def get_conflicted(self, limit: int = 10) -> list:
        """Return conflicted strategies."""
        try:
            from strategy_validation.validation_query import StrategyValidationQuery
            query = StrategyValidationQuery()
            scores = _to_dicts(query.list_scores() or [])
            conflicted = [
                s for s in scores
                if str(s.get("validation_grade", "")).upper() == "CONFLICTED"
            ]
            return conflicted[:limit]
        except Exception as exc:
            logger.warning("StrategyValidationAdapter.get_conflicted: %s", exc)
            return []

    def explain_score(self, strategy_id: str) -> dict:
        """Return explanation dict for a strategy score."""
        try:
            from strategy_validation.validation_query import StrategyValidationQuery
            query = StrategyValidationQuery()
            raw = query.explain_score(strategy_id)
            return _to_dict(raw) if raw is not None else {}
        except Exception as exc:
            logger.warning("StrategyValidationAdapter.explain_score: %s", exc)
            return {}

    # ------------------------------------------------------------------
    # Report
    # ------------------------------------------------------------------

    def build_report(self, mode: str = "real", output_dir: str = "reports") -> str:
        """Build Markdown report. Returns file path."""
        try:
            from reports.strategy_validation_report import StrategyValidationReportBuilder
            if not os.path.isabs(output_dir):
                output_dir = os.path.join(_BASE_DIR, output_dir)
            builder = StrategyValidationReportBuilder()
            return builder.build(mode=mode, output_dir=output_dir)
        except Exception as exc:
            logger.warning("StrategyValidationAdapter.build_report: %s", exc)
            return ""

    # ------------------------------------------------------------------
    # Safe helpers
    # ------------------------------------------------------------------

    def get_safe_next_step(self, strategy_id: str) -> str:
        """
        Return the safe suggested next step for a strategy.
        Never returns BUY/SELL/ORDER.
        """
        try:
            explanation = self.explain_score(strategy_id)
            step = explanation.get("suggested_next_step", "")
            if not step:
                scores = self.load_scores()
                for s in scores:
                    if s.get("strategy_id") == strategy_id:
                        step = s.get("suggested_next_step", "")
                        break
            return self._sanitize(step) if step else "Run backtest or collect more evidence"
        except Exception as exc:
            logger.warning("StrategyValidationAdapter.get_safe_next_step: %s", exc)
            return ""

    def copy_explanation(self, strategy_id: str) -> str:
        """
        Return explanation text suitable for clipboard.
        No forbidden actions included.
        """
        try:
            explanation = self.explain_score(strategy_id)
            if not explanation:
                return f"No explanation available for strategy: {strategy_id}"
            parts = [
                f"Strategy: {explanation.get('strategy_name', strategy_id)}",
                f"Grade: {explanation.get('validation_grade', '—')}",
                f"Score: {explanation.get('final_score', '—')}",
                f"Status: {explanation.get('status', '—')}",
                f"Reason: {explanation.get('reason', '—')}",
                f"Limitations: {explanation.get('limitations', '—')}",
                f"Safe Next Step: {self._sanitize(explanation.get('suggested_next_step', '—'))}",
                "",
                "[!] Research Only. No Real Orders. VALIDATED does not enable trading.",
            ]
            return self._sanitize("\n".join(parts))
        except Exception as exc:
            logger.warning("StrategyValidationAdapter.copy_explanation: %s", exc)
            return ""

    def is_available(self) -> bool:
        """Return True if strategy_validation package is importable."""
        try:
            import strategy_validation  # noqa: F401
            return True
        except ImportError:
            return False

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _sanitize(self, text: str) -> str:
        """Remove forbidden tokens from text."""
        if not text:
            return text
        for token in self._FORBIDDEN:
            text = text.replace(token, "REVIEW")
            text = text.replace(token.lower(), "review")
            text = text.replace(token.capitalize(), "Review")
        return text
