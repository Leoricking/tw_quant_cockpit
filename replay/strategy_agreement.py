"""
replay/strategy_agreement.py — Agreement analyzer for v1.2.4.

[!] Research Only. No Real Orders. Replay Training Only.
[!] UNAVAILABLE modules are NOT counted as bearish.
[!] Confidence INSUFFICIENT if < 3 modules available.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


class StrategyAgreementAnalyzer:
    """
    Analyzes agreement and conflict across strategy modules.

    Rules:
    - UNAVAILABLE modules are NOT counted as bearish.
    - Confidence INSUFFICIENT if < 3 modules available.
    - Agreement based on available modules only.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    BULLISH_SIGNALS = {
        "KD_ADVANCED": ["golden_cross", "low_kd_cross", "oversold_cross"],
        "SHORT_INTEREST": ["short_squeeze_fuel", "high_short_ratio"],
        "BOTTOM_REVERSAL": ["confirmed"],
        "SECTOR_ROTATION": ["sector_linkage_support", "leader_strong"],
        "FUNDAMENTAL_QUALITY": ["strong", "positive"],
        "ABC_BUY_POINT": ["A_valid", "B_valid", "C_valid"],
    }

    BEARISH_WARNING_SIGNALS = {
        "KD_ADVANCED": ["death_cross", "high_kd_cross", "overbought"],
        "SHORT_INTEREST": ["weak_stock_short_increase"],
        "SECTOR_ROTATION": ["sector_linkage_weak"],
        "FUNDAMENTAL_QUALITY": ["warning", "negative"],
        "NO_CHASE": ["chase_warning"],
        "NO_PANIC_SELL": ["panic_sell_warning"],
        "DO_NOT_REBUY_YET": ["do_not_rebuy"],
    }

    def analyze(self, snapshot) -> "StrategyAgreementResult":
        """Analyze agreement for a strategy snapshot."""
        from replay.strategy_replay_schema import StrategyAgreementResult
        snap_dict = snapshot.to_dict() if hasattr(snapshot, "to_dict") else snapshot
        modules = snap_dict.get("modules", [])
        biases: Dict[str, str] = {}
        for mod in modules:
            name = mod.get("module_name", "")
            bias = self.classify_module_bias(name, mod)
            biases[name] = bias

        bullish = [m for m, b in biases.items() if b == "BULLISH"]
        bearish = [m for m, b in biases.items() if b == "BEARISH"]
        warning = [m for m, b in biases.items() if b == "WARNING"]
        neutral = [m for m, b in biases.items() if b == "NEUTRAL"]
        unavailable = [m for m, b in biases.items() if b == "UNAVAILABLE"]

        available_count = len(bullish) + len(bearish) + len(warning) + len(neutral)
        agreement_score = self.calculate_agreement_score(biases)
        conflict_score = self.calculate_conflict_score(biases)
        aligned = self.aligned_modules(biases)
        conflicting = self.conflicting_modules(biases)

        reasons = []
        if bullish:
            reasons.append(f"Bullish: {', '.join(bullish)}")
        if bearish:
            reasons.append(f"Bearish: {', '.join(bearish)}")
        if warning:
            reasons.append(f"Warning: {', '.join(warning)}")
        if unavailable:
            reasons.append(f"Unavailable (not counted): {', '.join(unavailable)}")

        conf = self.confidence_from_count(available_count)

        if available_count < 3:
            status = "INSUFFICIENT"
        elif agreement_score >= 0.75 and len(bearish) == 0:
            status = "STRONG_ALIGNMENT"
        elif agreement_score >= 0.50:
            status = "MODERATE_ALIGNMENT"
        elif conflict_score >= 0.50:
            status = "STRONG_CONFLICT"
        elif len(bullish) > 0 and len(bearish) > 0:
            status = "MIXED"
        else:
            status = "MODERATE_ALIGNMENT"

        return StrategyAgreementResult(
            agreement_id=f"SAG-{uuid.uuid4().hex[:12].upper()}",
            session_id=snap_dict.get("session_id", ""),
            replay_date=snap_dict.get("replay_date", ""),
            bullish_count=len(bullish),
            bearish_count=len(bearish),
            neutral_count=len(neutral),
            warning_count=len(warning),
            unavailable_count=len(unavailable),
            agreement_score=agreement_score,
            conflict_score=conflict_score,
            aligned_modules=aligned,
            conflicting_modules=conflicting,
            reasons=reasons,
            confidence=conf,
            status=status,
            created_at=_now_utc(),
        )

    def classify_module_bias(
        self, module_name: str, module_result: Dict[str, Any]
    ) -> str:
        """Returns: BULLISH, BEARISH, WARNING, NEUTRAL, UNAVAILABLE"""
        if not module_result.get("available", False):
            return "UNAVAILABLE"
        signal = str(module_result.get("signal", "")).lower()
        if signal in ("unavailable", "unknown", ""):
            return "UNAVAILABLE"

        bullish_sigs = [s.lower() for s in self.BULLISH_SIGNALS.get(module_name, [])]
        bearish_sigs = [s.lower() for s in self.BEARISH_WARNING_SIGNALS.get(module_name, [])]

        for bs in bullish_sigs:
            if bs in signal:
                return "BULLISH"
        for bws in bearish_sigs:
            if bws in signal:
                warning = module_result.get("warning", "")
                if warning:
                    return "WARNING"
                return "BEARISH"
        return "NEUTRAL"

    def calculate_agreement_score(self, biases: Dict[str, str]) -> float:
        """Agreement score based on dominant bias among available modules."""
        available = [b for b in biases.values() if b != "UNAVAILABLE"]
        if not available:
            return 0.0
        from collections import Counter
        counts = Counter(available)
        dominant = counts.most_common(1)[0][1]
        return round(dominant / len(available), 3)

    def calculate_conflict_score(self, biases: Dict[str, str]) -> float:
        """Conflict score: presence of both bullish and bearish signals."""
        available = [b for b in biases.values() if b != "UNAVAILABLE"]
        if not available:
            return 0.0
        has_bullish = any(b == "BULLISH" for b in available)
        has_bearish = any(b in ("BEARISH", "WARNING") for b in available)
        if has_bullish and has_bearish:
            from collections import Counter
            counts = Counter(available)
            bull_count = counts.get("BULLISH", 0)
            bear_count = counts.get("BEARISH", 0) + counts.get("WARNING", 0)
            min_side = min(bull_count, bear_count)
            return round(min_side / len(available), 3)
        return 0.0

    def aligned_modules(self, biases: Dict[str, str]) -> List[str]:
        """Return list of modules sharing the dominant bias."""
        available = {m: b for m, b in biases.items() if b != "UNAVAILABLE"}
        if not available:
            return []
        from collections import Counter
        counts = Counter(available.values())
        dominant_bias = counts.most_common(1)[0][0]
        return [m for m, b in available.items() if b == dominant_bias]

    def conflicting_modules(self, biases: Dict[str, str]) -> List[str]:
        """Return modules not sharing the dominant bias (among available)."""
        available = {m: b for m, b in biases.items() if b != "UNAVAILABLE"}
        if not available:
            return []
        from collections import Counter
        counts = Counter(available.values())
        dominant_bias = counts.most_common(1)[0][0]
        return [m for m, b in available.items() if b != dominant_bias]

    def confidence_from_count(self, available_count: int) -> str:
        if available_count < 3:
            return "INSUFFICIENT"
        return "OBSERVATIONAL"

    def explain(self, result) -> str:
        """Generate human-readable explanation."""
        r = result.to_dict() if hasattr(result, "to_dict") else result
        lines = [
            f"Agreement: {r['status']} (score={r['agreement_score']:.2f})",
            f"Conflict: {r['conflict_score']:.2f}",
            f"Bullish: {r['bullish_count']}, Bearish: {r['bearish_count']}, "
            f"Warning: {r['warning_count']}, Unavailable: {r['unavailable_count']}",
            f"Confidence: {r['confidence']}",
        ]
        for reason in r.get("reasons", []):
            lines.append(f"  - {reason}")
        return "\n".join(lines)

    def confidence(self, result, available_count: int) -> str:
        """INSUFFICIENT if < 3 modules available, OBSERVATIONAL otherwise."""
        return self.confidence_from_count(available_count)
