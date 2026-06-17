"""
replay/strategy_module_evaluator.py — Module evaluator for v1.2.4.

[!] Research Only. No Real Orders. Replay Training Only.
[!] Does NOT implement strategy rules itself.
[!] Calls adapter, verifies point-in-time, builds StrategyModuleReplayResult.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


class StrategyReplayModuleEvaluator:
    """
    Calls adapter, verifies point-in-time, builds StrategyModuleReplayResult.
    Does NOT implement strategy rules itself.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self):
        from replay.strategy_knowledge_adapter import ReplayStrategyKnowledgeAdapter
        from replay.strategy_point_in_time import StrategyPointInTimeVerifier
        self.adapter = ReplayStrategyKnowledgeAdapter()
        self.verifier = StrategyPointInTimeVerifier()

    def _evaluate(
        self, module_name: str, symbol: str, replay_date: str,
        context: Dict[str, Any], mode: str = "real"
    ) -> "StrategyModuleReplayResult":
        from replay.strategy_replay_schema import StrategyModuleReplayResult
        raw = self.adapter.evaluate_module(module_name, symbol, replay_date, context, mode)
        pit_report = self.verifier.verify_module_output(module_name, raw, replay_date)
        return self.build_module_result(module_name, raw, replay_date, pit_report)

    def evaluate_kd(self, symbol, replay_date, context, mode="real"):
        return self._evaluate("KD_ADVANCED", symbol, replay_date, context, mode)

    def evaluate_short_interest(self, symbol, replay_date, context, mode="real"):
        return self._evaluate("SHORT_INTEREST", symbol, replay_date, context, mode)

    def evaluate_bottom_reversal(self, symbol, replay_date, context, mode="real"):
        return self._evaluate("BOTTOM_REVERSAL", symbol, replay_date, context, mode)

    def evaluate_sector_rotation(self, symbol, replay_date, context, mode="real"):
        return self._evaluate("SECTOR_ROTATION", symbol, replay_date, context, mode)

    def evaluate_fundamental_quality(self, symbol, replay_date, context, mode="real"):
        return self._evaluate("FUNDAMENTAL_QUALITY", symbol, replay_date, context, mode)

    def evaluate_no_chase(self, symbol, replay_date, context, mode="real"):
        return self._evaluate("NO_CHASE", symbol, replay_date, context, mode)

    def evaluate_no_panic_sell(self, symbol, replay_date, context, mode="real"):
        return self._evaluate("NO_PANIC_SELL", symbol, replay_date, context, mode)

    def evaluate_do_not_rebuy_yet(self, symbol, replay_date, context, mode="real"):
        return self._evaluate("DO_NOT_REBUY_YET", symbol, replay_date, context, mode)

    def evaluate_abc_buy_point(self, symbol, replay_date, context, mode="real"):
        return self._evaluate("ABC_BUY_POINT", symbol, replay_date, context, mode)

    def build_module_result(
        self,
        module_name: str,
        raw_result: Dict[str, Any],
        replay_date: str,
        point_in_time_report: Dict[str, Any],
    ) -> "StrategyModuleReplayResult":
        """Build StrategyModuleReplayResult from normalized adapter output."""
        from replay.strategy_replay_schema import StrategyModuleReplayResult
        pit_verified = point_in_time_report.get("verified", False)
        blocked = point_in_time_report.get("blocked_fields", [])
        timing_warning = raw_result.get("timing_warning", "")
        if blocked:
            timing_warning = f"BLOCKED fields: {blocked}; " + timing_warning
        return StrategyModuleReplayResult(
            module_name=module_name,
            replay_date=replay_date,
            available=bool(raw_result.get("available", False)),
            signal=raw_result.get("signal", "UNAVAILABLE"),
            score=raw_result.get("score"),
            warning=raw_result.get("warning", ""),
            reason=raw_result.get("reason", ""),
            evidence=raw_result.get("evidence", []),
            source_fields=raw_result.get("source_fields", []),
            source_dates=raw_result.get("source_dates", []),
            timing_warning=timing_warning,
            point_in_time_verified=pit_verified,
            confidence=raw_result.get("confidence", "INSUFFICIENT"),
            qualification=raw_result.get("qualification", "OBSERVATIONAL_ONLY"),
            limitations=raw_result.get("limitations", []),
            generated_at=_now_utc(),
            research_only=True,
            no_real_orders=True,
        )
