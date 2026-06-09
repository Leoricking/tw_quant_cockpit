# strategy_rules/crash_reversal_pack.py
# TW Quant Cockpit — Crash Reversal & Risk Discipline Strategy Pack
# v0.9.0.1 — Research Only / No Real Orders / Production Trading BLOCKED
#
# DISCLAIMER: This module is for research and educational purposes ONLY.
# It does NOT issue, suggest, or authorise any real trading orders.
# NOT investment advice. Production trading is BLOCKED.

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from typing import Any

VERSION = "v0.9.0.1"

# ---------------------------------------------------------------------------
# String constants — cause types
# ---------------------------------------------------------------------------
CAUSE_FUNDAMENTAL_BREAKDOWN = "FUNDAMENTAL_BREAKDOWN"
CAUSE_FINANCIAL_DELEVERAGING = "FINANCIAL_DELEVERAGING"
CAUSE_TECHNICAL_OVERHEAT_CORRECTION = "TECHNICAL_OVERHEAT_CORRECTION"
CAUSE_SYSTEMIC_CRISIS = "SYSTEMIC_CRISIS"
CAUSE_UNKNOWN = "UNKNOWN"

CAUSE_TYPES = [
    CAUSE_FUNDAMENTAL_BREAKDOWN,
    CAUSE_FINANCIAL_DELEVERAGING,
    CAUSE_TECHNICAL_OVERHEAT_CORRECTION,
    CAUSE_SYSTEMIC_CRISIS,
    CAUSE_UNKNOWN,
]

# ---------------------------------------------------------------------------
# String constants — risk levels
# ---------------------------------------------------------------------------
RISK_LOW = "LOW"
RISK_MEDIUM = "MEDIUM"
RISK_HIGH = "HIGH"
RISK_EXTREME = "EXTREME"
RISK_UNKNOWN = "UNKNOWN"

RISK_LEVELS = [RISK_LOW, RISK_MEDIUM, RISK_HIGH, RISK_EXTREME, RISK_UNKNOWN]

# ---------------------------------------------------------------------------
# String constants — stabilization status
# ---------------------------------------------------------------------------
STAB_NOT_STABILIZED = "NOT_STABILIZED"
STAB_FIRST_REBOUND_ONLY = "FIRST_REBOUND_ONLY"
STAB_STABILIZING = "STABILIZING"
STAB_HIGH_QUALITY_DIP = "HIGH_QUALITY_DIP"
STAB_UNKNOWN = "UNKNOWN"

STABILIZATION_STATUS = [
    STAB_NOT_STABILIZED,
    STAB_FIRST_REBOUND_ONLY,
    STAB_STABILIZING,
    STAB_HIGH_QUALITY_DIP,
    STAB_UNKNOWN,
]

# ---------------------------------------------------------------------------
# String constants — relative-strength ratings
# ---------------------------------------------------------------------------
RS_HIGH_RELATIVE_STRENGTH = "HIGH_RELATIVE_STRENGTH"
RS_WATCHLIST_CANDIDATE = "WATCHLIST_CANDIDATE"
RS_NORMAL = "NORMAL"
RS_WEAK = "WEAK"
RS_UNKNOWN = "UNKNOWN"

RS_RATINGS = [
    RS_HIGH_RELATIVE_STRENGTH,
    RS_WATCHLIST_CANDIDATE,
    RS_NORMAL,
    RS_WEAK,
    RS_UNKNOWN,
]

# ---------------------------------------------------------------------------
# String constants — trend status
# ---------------------------------------------------------------------------
TREND_HEALTHY = "TREND_HEALTHY"
TREND_WASHOUT = "WASHOUT"
TREND_MA20_WARNING = "MA20_WARNING"
TREND_MA60_TREND_BREAK = "MA60_TREND_BREAK"
TREND_RECOVERY_WATCH = "RECOVERY_WATCH"
TREND_UNKNOWN = "UNKNOWN"

TREND_STATUS = [
    TREND_HEALTHY,
    TREND_WASHOUT,
    TREND_MA20_WARNING,
    TREND_MA60_TREND_BREAK,
    TREND_RECOVERY_WATCH,
    TREND_UNKNOWN,
]

# ---------------------------------------------------------------------------
# Allowed / forbidden actions
# ---------------------------------------------------------------------------
ALLOWED_ACTIONS = frozenset([
    "WAIT",
    "REVIEW",
    "WATCH",
    "BUILD_WATCHLIST",
    "BACKTEST_MORE",
    "REVIEW_EARNINGS",
    "REVIEW_CHIPS",
    "REVIEW_RISK",
    "HOLD_REVIEW",
    "REDUCE_RISK_REVIEW",
    "DO_NOT_CHASE",
    "REVIEW_REENTRY",
    "PRACTICE_REPLAY",
])

FORBIDDEN_ACTIONS = frozenset([
    "BUY",
    "SELL",
    "ORDER",
    "EXECUTE",
    "SUBMIT_ORDER",
    "AUTO_TRADE",
    "REAL_TRADE",
])

_FORBIDDEN_ACTION_GUARD = frozenset([
    "BUY", "SELL", "ORDER", "EXECUTE",
    "SUBMIT_ORDER", "AUTO_TRADE", "REAL_TRADE",
])


def _safe_action(action: str, default: str = "REVIEW") -> str:
    """Return action unchanged unless it is a forbidden trading action."""
    if action in _FORBIDDEN_ACTION_GUARD:
        return default
    return action


# ---------------------------------------------------------------------------
# High-risk industry list
# ---------------------------------------------------------------------------
HIGH_RISK_INDUSTRIES = [
    "新藥生技", "新藥臨床", "生技臨床", "處置股",
    "純題材小型股", "低流動性股", "事件型無EPS",
    "biotech_drug", "clinical_trial", "disposition_stock",
    "pure_theme_small", "low_liquidity", "event_no_eps",
]


# ===========================================================================
# Dataclasses
# ===========================================================================

@dataclass
class CrashCauseClassification:
    cause_type: str = "UNKNOWN"
    score: float = 0.0
    evidence: list = field(default_factory=list)
    risk_level: str = "UNKNOWN"
    action_hint: str = "REVIEW"
    no_real_orders: bool = True
    production_blocked: bool = True

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "CrashCauseClassification":
        try:
            return cls(
                cause_type=d.get("cause_type", "UNKNOWN"),
                score=float(d.get("score", 0.0)),
                evidence=list(d.get("evidence", [])),
                risk_level=d.get("risk_level", "UNKNOWN"),
                action_hint=_safe_action(d.get("action_hint", "REVIEW")),
                no_real_orders=bool(d.get("no_real_orders", True)),
                production_blocked=bool(d.get("production_blocked", True)),
            )
        except Exception:
            return cls()


@dataclass
class PostCrashStabilizationSignal:
    item: str = ""
    passed: bool = False
    score: float = 0.0
    evidence: str = ""
    weight: float = 10.0

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "PostCrashStabilizationSignal":
        try:
            return cls(
                item=d.get("item", ""),
                passed=bool(d.get("passed", False)),
                score=float(d.get("score", 0.0)),
                evidence=d.get("evidence", ""),
                weight=float(d.get("weight", 10.0)),
            )
        except Exception:
            return cls()


@dataclass
class PostCrashStabilizationSummary:
    stabilization_score: float = 0.0
    status: str = "UNKNOWN"
    passed_count: int = 0
    total_count: int = 0
    signals: list = field(default_factory=list)
    action_hint: str = "WAIT"
    evidence: list = field(default_factory=list)
    no_real_orders: bool = True
    production_blocked: bool = True

    def to_dict(self) -> dict:
        d = asdict(self)
        # signals are PostCrashStabilizationSignal instances; asdict handles them
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "PostCrashStabilizationSummary":
        try:
            signals_raw = d.get("signals", [])
            signals = [
                PostCrashStabilizationSignal.from_dict(s)
                if isinstance(s, dict) else s
                for s in signals_raw
            ]
            return cls(
                stabilization_score=float(d.get("stabilization_score", 0.0)),
                status=d.get("status", "UNKNOWN"),
                passed_count=int(d.get("passed_count", 0)),
                total_count=int(d.get("total_count", 0)),
                signals=signals,
                action_hint=_safe_action(d.get("action_hint", "WAIT")),
                evidence=list(d.get("evidence", [])),
                no_real_orders=bool(d.get("no_real_orders", True)),
                production_blocked=bool(d.get("production_blocked", True)),
            )
        except Exception:
            return cls()


@dataclass
class RelativeStrengthAfterCrashScore:
    symbol: str = ""
    score: float = 0.0
    rating: str = "UNKNOWN"
    conditions: list = field(default_factory=list)
    evidence: list = field(default_factory=list)
    forbidden_trap: bool = False
    no_real_orders: bool = True
    production_blocked: bool = True

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "RelativeStrengthAfterCrashScore":
        try:
            return cls(
                symbol=d.get("symbol", ""),
                score=float(d.get("score", 0.0)),
                rating=d.get("rating", "UNKNOWN"),
                conditions=list(d.get("conditions", [])),
                evidence=list(d.get("evidence", [])),
                forbidden_trap=bool(d.get("forbidden_trap", False)),
                no_real_orders=bool(d.get("no_real_orders", True)),
                production_blocked=bool(d.get("production_blocked", True)),
            )
        except Exception:
            return cls()


@dataclass
class SakataDipBuyEligibility:
    symbol: str = ""
    eligible: bool = False
    score: float = 0.0
    eps_supported: bool = False
    revenue_supported: bool = False
    low_position: bool = False
    technical_turning: bool = False
    chip_not_broken: bool = False
    forbidden_reason: list = field(default_factory=list)
    allowed_reason: list = field(default_factory=list)
    next_safe_action: str = "WAIT"
    no_real_orders: bool = True
    production_blocked: bool = True

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "SakataDipBuyEligibility":
        try:
            return cls(
                symbol=d.get("symbol", ""),
                eligible=bool(d.get("eligible", False)),
                score=float(d.get("score", 0.0)),
                eps_supported=bool(d.get("eps_supported", False)),
                revenue_supported=bool(d.get("revenue_supported", False)),
                low_position=bool(d.get("low_position", False)),
                technical_turning=bool(d.get("technical_turning", False)),
                chip_not_broken=bool(d.get("chip_not_broken", False)),
                forbidden_reason=list(d.get("forbidden_reason", [])),
                allowed_reason=list(d.get("allowed_reason", [])),
                next_safe_action=_safe_action(d.get("next_safe_action", "WAIT")),
                no_real_orders=bool(d.get("no_real_orders", True)),
                production_blocked=bool(d.get("production_blocked", True)),
            )
        except Exception:
            return cls()


@dataclass
class MovingAverageProfitDiscipline:
    symbol: str = ""
    trend_status: str = "UNKNOWN"
    action_hint: str = "HOLD_REVIEW"
    ma5_status: str = "UNKNOWN"
    ma10_status: str = "UNKNOWN"
    ma20_status: str = "UNKNOWN"
    ma60_status: str = "UNKNOWN"
    reclaim_rule: str = ""
    evidence: list = field(default_factory=list)
    no_real_orders: bool = True
    production_blocked: bool = True

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "MovingAverageProfitDiscipline":
        try:
            return cls(
                symbol=d.get("symbol", ""),
                trend_status=d.get("trend_status", "UNKNOWN"),
                action_hint=_safe_action(d.get("action_hint", "HOLD_REVIEW")),
                ma5_status=d.get("ma5_status", "UNKNOWN"),
                ma10_status=d.get("ma10_status", "UNKNOWN"),
                ma20_status=d.get("ma20_status", "UNKNOWN"),
                ma60_status=d.get("ma60_status", "UNKNOWN"),
                reclaim_rule=d.get("reclaim_rule", ""),
                evidence=list(d.get("evidence", [])),
                no_real_orders=bool(d.get("no_real_orders", True)),
                production_blocked=bool(d.get("production_blocked", True)),
            )
        except Exception:
            return cls()


@dataclass
class HighRiskIndustryGuard:
    symbol: str = ""
    industry: str = "UNKNOWN"
    risk_multiplier: float = 1.0
    max_position_hint: str = "N/A"
    core_holding_allowed: bool = True
    financing_allowed: bool = True
    hard_stop_required: bool = False
    warning: str = ""
    no_real_orders: bool = True
    production_blocked: bool = True

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "HighRiskIndustryGuard":
        try:
            return cls(
                symbol=d.get("symbol", ""),
                industry=d.get("industry", "UNKNOWN"),
                risk_multiplier=float(d.get("risk_multiplier", 1.0)),
                max_position_hint=d.get("max_position_hint", "N/A"),
                core_holding_allowed=bool(d.get("core_holding_allowed", True)),
                financing_allowed=bool(d.get("financing_allowed", True)),
                hard_stop_required=bool(d.get("hard_stop_required", False)),
                warning=d.get("warning", ""),
                no_real_orders=bool(d.get("no_real_orders", True)),
                production_blocked=bool(d.get("production_blocked", True)),
            )
        except Exception:
            return cls()


# ===========================================================================
# Main strategy pack class
# ===========================================================================

class CrashReversalStrategyPack:
    """
    TW Quant Cockpit — Crash Reversal & Risk Discipline Strategy Pack
    Version: v0.9.0.1

    RESEARCH ONLY — No Real Orders — Production Trading BLOCKED
    NOT investment advice.
    """

    VERSION = VERSION
    no_real_orders = True
    production_blocked = True

    # ------------------------------------------------------------------
    # 1. Classify crash cause
    # ------------------------------------------------------------------
    def classify_crash_cause(self, market_context: dict) -> CrashCauseClassification:
        """
        Classify the likely cause of a market crash from market_context signals.
        Returns CrashCauseClassification with cause_type, score, risk_level, action_hint.
        All missing context keys default to False / 0 — never raises.
        """
        try:
            ctx = market_context if isinstance(market_context, dict) else {}

            def _b(key: str, default=False):
                return bool(ctx.get(key, default))

            def _n(key: str, default=0.0):
                try:
                    return float(ctx.get(key, default))
                except (TypeError, ValueError):
                    return float(default)

            # --- SYSTEMIC_CRISIS conditions ---
            systemic_keys = [
                "liquidity_crisis", "credit_event", "war_event",
                "financial_institution_risk", "global_risk_off", "vix_spike_extreme",
            ]
            systemic_hits = [k for k in systemic_keys if _b(k)]
            systemic_score = len(systemic_hits) / len(systemic_keys) * 100

            # --- FUNDAMENTAL_BREAKDOWN conditions ---
            fundamental_keys = [
                "revenue_yoy", "eps_revision_down", "gross_margin_declining",
                "operating_margin_declining", "ai_demand_invalidated",
                "capex_cut", "major_order_cut",
            ]
            fundamental_hits = [k for k in fundamental_keys if _b(k)]
            fundamental_score = len(fundamental_hits) / len(fundamental_keys) * 100

            # --- FINANCIAL_DELEVERAGING conditions ---
            delever_keys = [
                "nasdaq_drop_large", "sox_drop_large", "futures_night_panic",
                "forced_liquidation", "margin_balance_high", "leverage_unwind",
            ]
            delever_hits = [k for k in delever_keys if _b(k)]
            # fundamentals_intact is a positive signal for this type
            delever_evidence = list(delever_hits)
            if _b("fundamentals_intact"):
                delever_evidence.append("fundamentals_intact")
            delever_score = len(delever_hits) / len(delever_keys) * 100

            # --- TECHNICAL_OVERHEAT_CORRECTION conditions ---
            overextension_score = _n("overextension_score", 0.0)
            tech_keys_bool = [
                "high_volume_profit_taking", "price_far_above_ma20",
                "rsi_overheated", "kd_overheated",
            ]
            tech_hits = [k for k in tech_keys_bool if _b(k)]
            tech_evidence = list(tech_hits)
            if overextension_score >= 70:
                tech_evidence.append(f"overextension_score={overextension_score}")
            if _b("fundamentals_intact"):
                tech_evidence.append("fundamentals_intact")
            # score: overextension counts as one boolean hit
            tech_total_keys = tech_keys_bool + ["overextension_score>=70"]
            tech_total_hits = len(tech_hits) + (1 if overextension_score >= 70 else 0)
            tech_score = tech_total_hits / len(tech_total_keys) * 100

            # --- Priority resolution ---
            # SYSTEMIC_CRISIS > FUNDAMENTAL_BREAKDOWN > FINANCIAL_DELEVERAGING > TECHNICAL_OVERHEAT_CORRECTION > UNKNOWN
            candidates = [
                (CAUSE_SYSTEMIC_CRISIS,               systemic_score,    systemic_hits,  RISK_EXTREME, "REVIEW_RISK"),
                (CAUSE_FUNDAMENTAL_BREAKDOWN,          fundamental_score, fundamental_hits, RISK_HIGH,  "REVIEW_RISK"),
                (CAUSE_FINANCIAL_DELEVERAGING,         delever_score,    delever_evidence, RISK_MEDIUM, "WATCH"),
                (CAUSE_TECHNICAL_OVERHEAT_CORRECTION,  tech_score,       tech_evidence,   RISK_MEDIUM, "WAIT"),
            ]

            # Pick the highest-priority candidate that has at least one hit,
            # respecting the priority order (index 0 = highest priority).
            chosen_cause = CAUSE_UNKNOWN
            chosen_score = 0.0
            chosen_evidence: list = []
            chosen_risk = RISK_UNKNOWN
            chosen_action = "REVIEW"

            for cause, score, evidence, risk, action in candidates:
                # At least 2 signals must fire to claim a cause, except SYSTEMIC which needs 1
                min_hits = 1 if cause == CAUSE_SYSTEMIC_CRISIS else 2
                hit_count = len([e for e in evidence if e])
                if hit_count >= min_hits:
                    chosen_cause = cause
                    chosen_score = round(score, 1)
                    chosen_evidence = evidence
                    chosen_risk = risk
                    chosen_action = _safe_action(action)
                    break

            # Upgrade FUNDAMENTAL risk to EXTREME if score >= 85
            if chosen_cause == CAUSE_FUNDAMENTAL_BREAKDOWN and chosen_score >= 85:
                chosen_risk = RISK_EXTREME

            return CrashCauseClassification(
                cause_type=chosen_cause,
                score=chosen_score,
                evidence=chosen_evidence,
                risk_level=chosen_risk,
                action_hint=chosen_action,
                no_real_orders=True,
                production_blocked=True,
            )
        except Exception:
            return CrashCauseClassification()

    # ------------------------------------------------------------------
    # 2. Post-crash stabilization evaluation
    # ------------------------------------------------------------------
    def evaluate_post_crash_stabilization(self, market_context: dict) -> PostCrashStabilizationSummary:
        """
        Evaluate 8 stabilization signals from market_context.
        Returns PostCrashStabilizationSummary with weighted score and status.
        All missing keys default to False — never raises.
        """
        try:
            ctx = market_context if isinstance(market_context, dict) else {}

            def _b(key: str) -> bool:
                return bool(ctx.get(key, False))

            # Define signals: (context_key, label, weight, evidence_text_if_passed, evidence_text_if_failed)
            signal_definitions = [
                ("ma20_held",               "MA20 Held / Recovered within 3 days",          15,
                 "Market index closed above 20MA or reclaimed within 3 days",
                 "MA20 not held / not recovered within 3 days"),
                ("volume_contracting",      "Volume Contracting from Panic High",            15,
                 "Volume decreasing from the panic-sell high",
                 "Volume has not contracted from the panic high"),
                ("margin_balance_declining","Margin / Financing Balance Declining",          15,
                 "Financing balance is dropping (leverage unwinding)",
                 "Financing balance not yet declining"),
                ("tsmc_not_breaking_low",   "TSMC Not Making New Lows",                     15,
                 "TSMC holding and not printing new lows",
                 "TSMC is breaking to new lows — caution"),
                ("blue_chips_stabilizing",  "Blue Chips Stabilizing (Delta / MediaTek / Foxconn)", 10,
                 "Major blue chips showing stabilization",
                 "Blue chips have not stabilized"),
                ("ai_leaders_outperforming","AI Leaders Outperforming Index",                10,
                 "AI-sector leaders falling less than the broad index",
                 "AI leaders not outperforming index"),
                ("close_near_high",         "Closing Price Near Daily High",                 10,
                 "Candles closing near the high of day",
                 "Candles closing far from daily high"),
                ("long_lower_shadow",       "Long Lower Shadow Candles Appearing",           10,
                 "Long lower-shadow / hammer candles present",
                 "No long lower-shadow candles observed"),
            ]

            signals: list[PostCrashStabilizationSignal] = []
            total_weight = 0.0
            earned_weight = 0.0
            passed_count = 0
            evidence_list: list[str] = []

            for key, label, weight, ev_pass, ev_fail in signal_definitions:
                passed = _b(key)
                sig_score = float(weight) if passed else 0.0
                ev_text = ev_pass if passed else ev_fail
                signals.append(PostCrashStabilizationSignal(
                    item=label,
                    passed=passed,
                    score=sig_score,
                    evidence=ev_text,
                    weight=float(weight),
                ))
                total_weight += weight
                if passed:
                    earned_weight += weight
                    passed_count += 1
                    evidence_list.append(ev_pass)

            # Normalise to 0-100
            stabilization_score = round((earned_weight / total_weight * 100) if total_weight > 0 else 0.0, 1)

            # Determine status and action
            if stabilization_score >= 80:
                status = STAB_HIGH_QUALITY_DIP
                action = "BUILD_WATCHLIST"
            elif stabilization_score >= 60:
                status = STAB_STABILIZING
                action = "WATCH"
            elif stabilization_score >= 40:
                status = STAB_FIRST_REBOUND_ONLY
                action = "WAIT"
            else:
                status = STAB_NOT_STABILIZED
                action = "WAIT"

            return PostCrashStabilizationSummary(
                stabilization_score=stabilization_score,
                status=status,
                passed_count=passed_count,
                total_count=len(signals),
                signals=signals,
                action_hint=_safe_action(action),
                evidence=evidence_list,
                no_real_orders=True,
                production_blocked=True,
            )
        except Exception:
            return PostCrashStabilizationSummary()

    # ------------------------------------------------------------------
    # 3. Relative strength after crash
    # ------------------------------------------------------------------
    def score_relative_strength_after_crash(
        self,
        symbol: str,
        stock_context: dict,
        market_context: dict,
    ) -> RelativeStrengthAfterCrashScore:
        """
        Score a stock's relative strength during/after a crash.
        Returns RelativeStrengthAfterCrashScore. Never raises.
        """
        try:
            sc = stock_context if isinstance(stock_context, dict) else {}
            mc = market_context if isinstance(market_context, dict) else {}

            def _b(d: dict, key: str) -> bool:
                return bool(d.get(key, False))

            score = 0.0
            conditions: list[str] = []
            evidence: list[str] = []

            # +20: did NOT hit limit down
            if _b(sc, "no_limit_down"):
                score += 20
                conditions.append("no_limit_down")
                evidence.append("Stock did not hit limit down during crash")

            # +20: close decline less than market
            close_decline = float(sc.get("close_decline", 0.0) or 0.0)
            market_decline = float(mc.get("market_decline", 0.0) or 0.0)
            if sc.get("close_decline_less_than_market", None) is not None:
                if _b(sc, "close_decline_less_than_market"):
                    score += 20
                    conditions.append("close_decline_less_than_market")
                    evidence.append("Stock declined less than the market index")
            elif close_decline < market_decline and market_decline > 0:
                score += 20
                conditions.append("close_decline_less_than_market")
                evidence.append(f"Stock decline ({close_decline}%) < market decline ({market_decline}%)")

            # +20: close near daily high
            if _b(sc, "close_near_daily_high"):
                score += 20
                conditions.append("close_near_daily_high")
                evidence.append("Closing price near the daily high")

            # +15: long lower shadow
            if _b(sc, "long_lower_shadow"):
                score += 15
                conditions.append("long_lower_shadow")
                evidence.append("Long lower shadow / hammer candle present")

            # +15: institutional not retreating
            if _b(sc, "institutional_not_retreating"):
                score += 15
                conditions.append("institutional_not_retreating")
                evidence.append("Institutional investors not retreating")

            # +10: strong revenue or earnings
            if _b(sc, "strong_revenue_or_earnings"):
                score += 10
                conditions.append("strong_revenue_or_earnings")
                evidence.append("Strong revenue or earnings support")

            score = min(score, 100.0)

            # --- Forbidden trap check ---
            trap_keys = [
                "limit_down_not_open", "margin_surge", "no_eps",
                "revenue_declining", "pure_theme", "disposition_stock", "low_liquidity",
            ]
            forbidden_trap = any(_b(sc, k) for k in trap_keys)
            if forbidden_trap:
                trap_reasons = [k for k in trap_keys if _b(sc, k)]
                evidence.append(f"FORBIDDEN TRAP triggered: {', '.join(trap_reasons)}")

            # --- Rating ---
            if forbidden_trap:
                # Cap at NORMAL
                if score >= 40:
                    rating = RS_NORMAL
                else:
                    rating = RS_WEAK
            else:
                if score >= 80:
                    rating = RS_HIGH_RELATIVE_STRENGTH
                elif score >= 60:
                    rating = RS_WATCHLIST_CANDIDATE
                elif score >= 40:
                    rating = RS_NORMAL
                else:
                    rating = RS_WEAK

            return RelativeStrengthAfterCrashScore(
                symbol=str(symbol),
                score=round(score, 1),
                rating=rating,
                conditions=conditions,
                evidence=evidence,
                forbidden_trap=forbidden_trap,
                no_real_orders=True,
                production_blocked=True,
            )
        except Exception:
            return RelativeStrengthAfterCrashScore(symbol=str(symbol) if symbol else "")

    # ------------------------------------------------------------------
    # 4. Sakata dip-buy eligibility
    # ------------------------------------------------------------------
    def evaluate_sakata_dip_buy(
        self,
        symbol: str,
        stock_context: dict,
        market_context: dict,
    ) -> SakataDipBuyEligibility:
        """
        Evaluate whether a stock meets Sakata dip-buy criteria.
        Returns SakataDipBuyEligibility. Never raises.
        """
        try:
            sc = stock_context if isinstance(stock_context, dict) else {}

            def _b(key: str) -> bool:
                return bool(sc.get(key, False))

            score = 0.0
            allowed_reason: list[str] = []

            # Positive conditions
            eps_growth = _b("eps_growth")
            if eps_growth:
                score += 20
                allowed_reason.append("EPS growth confirmed (+20)")

            revenue_strong = _b("revenue_strong")
            if revenue_strong:
                score += 20
                allowed_reason.append("Revenue strong (+20)")

            low_price_position = _b("low_price_position")
            if low_price_position:
                score += 15
                allowed_reason.append("Low price position (+15)")

            technical_turning = _b("technical_turning")
            if technical_turning:
                score += 15
                allowed_reason.append("Technical turning point (+15)")

            institutional_present = _b("institutional_present")
            if institutional_present:
                score += 15
                allowed_reason.append("Institutional investors present (+15)")

            less_decline_than_market = _b("less_decline_than_market")
            if less_decline_than_market:
                score += 10
                allowed_reason.append("Declined less than market (+10)")

            key_level_holds = _b("key_level_holds")
            if key_level_holds:
                score += 5
                allowed_reason.append("Key MA / neckline holding (+5)")

            score = min(score, 100.0)

            # --- Forbidden reasons ---
            forbidden_checks = {
                "two_highs_not_exceeded":   "Two recent highs not exceeded (structure not bullish)",
                "market_high_but_stock_weak": "Market at high but stock is weak — divergence warning",
                "eps_miss":                 "EPS miss — earnings not supporting dip buy",
                "revenue_declining":        "Revenue declining — no fundamental backing",
                "margin_surge":             "Margin / financing surging — chip quality broken",
                "pure_theme":               "Pure theme play — no earnings support",
                "limit_down_not_open":      "Limit-down day without recovery open",
                "no_eps":                   "No EPS / no earnings — speculative only",
                "high_risk_no_guard":       "High-risk industry without position guard",
            }
            forbidden_reason = [
                desc for key, desc in forbidden_checks.items() if _b(key)
            ]

            # Eligibility: score >= 70 AND no forbidden reasons
            eligible = (score >= 70) and (len(forbidden_reason) == 0)

            # Next safe action
            if eligible:
                next_safe_action = "WATCH"
            else:
                has_eps_rev_issue = _b("eps_miss") or _b("revenue_declining") or _b("no_eps")
                has_chip_issue = _b("margin_surge")
                if has_eps_rev_issue:
                    next_safe_action = "REVIEW_EARNINGS"
                elif has_chip_issue:
                    next_safe_action = "REVIEW_CHIPS"
                else:
                    next_safe_action = "DO_NOT_CHASE"

            return SakataDipBuyEligibility(
                symbol=str(symbol),
                eligible=eligible,
                score=round(score, 1),
                eps_supported=eps_growth,
                revenue_supported=revenue_strong,
                low_position=low_price_position,
                technical_turning=technical_turning,
                chip_not_broken=not _b("margin_surge"),
                forbidden_reason=forbidden_reason,
                allowed_reason=allowed_reason,
                next_safe_action=_safe_action(next_safe_action),
                no_real_orders=True,
                production_blocked=True,
            )
        except Exception:
            return SakataDipBuyEligibility(symbol=str(symbol) if symbol else "")

    # ------------------------------------------------------------------
    # 5. Moving-average profit discipline
    # ------------------------------------------------------------------
    def evaluate_ma_profit_discipline(
        self,
        symbol: str,
        stock_context: dict,
    ) -> MovingAverageProfitDiscipline:
        """
        Evaluate moving-average-based profit/position discipline.
        Returns MovingAverageProfitDiscipline. Never raises.
        """
        try:
            sc = stock_context if isinstance(stock_context, dict) else {}

            def _b(key: str) -> bool:
                return bool(sc.get(key, False))

            def _n(key: str, default=0) -> float:
                try:
                    return float(sc.get(key, default) or default)
                except (TypeError, ValueError):
                    return float(default)

            above_ma5  = _b("above_ma5")
            above_ma10 = _b("above_ma10")
            above_ma20 = _b("above_ma20")
            above_ma60 = _b("above_ma60")

            broke_ma20_days_ago              = _n("broke_ma20_days_ago", 0)
            reclaimed_ma20_within_3_days     = _b("reclaimed_ma20_within_3_days")
            broke_ma60_with_volume           = _b("broke_ma60_with_volume")

            ma5_status  = "ABOVE" if above_ma5  else "BELOW"
            ma10_status = "ABOVE" if above_ma10 else "BELOW"
            ma20_status = "ABOVE" if above_ma20 else "BELOW"
            ma60_status = "ABOVE" if above_ma60 else "BELOW"

            evidence: list[str] = []
            trend_status = TREND_UNKNOWN
            action_hint = "HOLD_REVIEW"
            reclaim_rule = ""

            # Priority logic
            if broke_ma60_with_volume:
                trend_status = TREND_MA60_TREND_BREAK
                action_hint = "REDUCE_RISK_REVIEW"
                reclaim_rule = "Wait for MA60 reclaim with confirming volume before re-evaluation"
                evidence.append("Broke MA60 with high volume — trend break signal")
            elif above_ma5 and above_ma10 and above_ma20:
                trend_status = TREND_HEALTHY
                action_hint = "HOLD_REVIEW"
                reclaim_rule = "Position above MA5/MA10/MA20 — trend intact"
                evidence.append("Price above MA5, MA10, MA20 — trend healthy")
                if above_ma60:
                    evidence.append("Also above MA60 — strong trend alignment")
            elif (1 <= broke_ma20_days_ago <= 3) and reclaimed_ma20_within_3_days:
                trend_status = TREND_WASHOUT
                action_hint = "HOLD_REVIEW"
                reclaim_rule = "Washout dip — reclaimed MA20 within 3 days"
                evidence.append(f"Broke MA20 {int(broke_ma20_days_ago)} day(s) ago but reclaimed within 3 days — washout pattern")
            elif reclaimed_ma20_within_3_days and above_ma60:
                trend_status = TREND_RECOVERY_WATCH
                action_hint = "REVIEW_REENTRY"
                reclaim_rule = "Reclaimed MA20 within 3 days and above MA60 — recovery candidate"
                evidence.append("Reclaimed MA20 within 3 days and still above MA60 — recovery watch")
            elif broke_ma20_days_ago > 3 and not reclaimed_ma20_within_3_days:
                trend_status = TREND_MA20_WARNING
                action_hint = "REDUCE_RISK_REVIEW"
                reclaim_rule = "Below MA20 for more than 3 days without recovery — reduce risk"
                evidence.append(f"Below MA20 for {int(broke_ma20_days_ago)} days without reclaim — warning")
            else:
                trend_status = TREND_UNKNOWN
                action_hint = "HOLD_REVIEW"
                reclaim_rule = "Insufficient data to determine MA trend status"
                evidence.append("MA trend status could not be determined from available context")

            return MovingAverageProfitDiscipline(
                symbol=str(symbol),
                trend_status=trend_status,
                action_hint=_safe_action(action_hint),
                ma5_status=ma5_status,
                ma10_status=ma10_status,
                ma20_status=ma20_status,
                ma60_status=ma60_status,
                reclaim_rule=reclaim_rule,
                evidence=evidence,
                no_real_orders=True,
                production_blocked=True,
            )
        except Exception:
            return MovingAverageProfitDiscipline(symbol=str(symbol) if symbol else "")

    # ------------------------------------------------------------------
    # 6. High-risk industry guard
    # ------------------------------------------------------------------
    def evaluate_high_risk_industry_guard(
        self,
        symbol: str,
        stock_context: dict,
    ) -> HighRiskIndustryGuard:
        """
        Check if the stock belongs to a high-risk industry and apply position guards.
        Returns HighRiskIndustryGuard. Never raises.
        """
        try:
            sc = stock_context if isinstance(stock_context, dict) else {}

            def _b(key: str) -> bool:
                return bool(sc.get(key, False))

            industry = str(sc.get("industry", "UNKNOWN") or "UNKNOWN")

            # Check industry name match
            industry_high_risk = industry in HIGH_RISK_INDUSTRIES

            # Check flag keys
            flag_high_risk = (
                _b("disposition_stock")
                or _b("pure_theme")
                or _b("no_eps")
                or _b("low_liquidity")
            )

            is_high_risk = industry_high_risk or flag_high_risk

            if is_high_risk:
                warning_parts: list[str] = []
                if industry_high_risk:
                    warning_parts.append(f"Industry '{industry}' is classified high-risk")
                if _b("disposition_stock"):
                    warning_parts.append("Disposition stock flag active")
                if _b("pure_theme"):
                    warning_parts.append("Pure theme play — no earnings backing")
                if _b("no_eps"):
                    warning_parts.append("No EPS — speculative only")
                if _b("low_liquidity"):
                    warning_parts.append("Low liquidity — slippage risk elevated")
                warning = "; ".join(warning_parts) if warning_parts else "High-risk classification triggered"

                return HighRiskIndustryGuard(
                    symbol=str(symbol),
                    industry=industry,
                    risk_multiplier=2.5,
                    max_position_hint="<=15% total high-risk exposure",
                    core_holding_allowed=False,
                    financing_allowed=False,
                    hard_stop_required=True,
                    warning=warning,
                    no_real_orders=True,
                    production_blocked=True,
                )
            else:
                return HighRiskIndustryGuard(
                    symbol=str(symbol),
                    industry=industry,
                    risk_multiplier=1.0,
                    max_position_hint="N/A",
                    core_holding_allowed=True,
                    financing_allowed=True,
                    hard_stop_required=False,
                    warning="",
                    no_real_orders=True,
                    production_blocked=True,
                )
        except Exception:
            return HighRiskIndustryGuard(symbol=str(symbol) if symbol else "")

    # ------------------------------------------------------------------
    # 7. Combined symbol-level evaluation
    # ------------------------------------------------------------------
    def evaluate_symbol(
        self,
        symbol: str,
        stock_context: dict,
        market_context: dict,
    ) -> dict:
        """
        Run all symbol-level evaluations and return a combined dict.
        Never raises.
        """
        try:
            rs      = self.score_relative_strength_after_crash(symbol, stock_context, market_context)
            sakata  = self.evaluate_sakata_dip_buy(symbol, stock_context, market_context)
            ma_disc = self.evaluate_ma_profit_discipline(symbol, stock_context)
            ind_gd  = self.evaluate_high_risk_industry_guard(symbol, stock_context)
            return {
                "symbol":           str(symbol),
                "relative_strength": rs.to_dict(),
                "sakata_dip_buy":   sakata.to_dict(),
                "ma_discipline":    ma_disc.to_dict(),
                "industry_guard":   ind_gd.to_dict(),
                "no_real_orders":   True,
                "production_blocked": True,
            }
        except Exception:
            return {
                "symbol":           str(symbol) if symbol else "",
                "relative_strength": {},
                "sakata_dip_buy":   {},
                "ma_discipline":    {},
                "industry_guard":   {},
                "no_real_orders":   True,
                "production_blocked": True,
                "error":            "evaluate_symbol failed gracefully",
            }

    # ------------------------------------------------------------------
    # 8. Combined market-level evaluation
    # ------------------------------------------------------------------
    def evaluate_market(self, market_context: dict) -> dict:
        """
        Run crash-cause classification + stabilization evaluation.
        Returns combined dict. Never raises.
        """
        try:
            crash_cause   = self.classify_crash_cause(market_context)
            stabilization = self.evaluate_post_crash_stabilization(market_context)
            return {
                "crash_cause":      crash_cause.to_dict(),
                "stabilization":    stabilization.to_dict(),
                "no_real_orders":   True,
                "production_blocked": True,
            }
        except Exception:
            return {
                "crash_cause":      {},
                "stabilization":    {},
                "no_real_orders":   True,
                "production_blocked": True,
                "error":            "evaluate_market failed gracefully",
            }
