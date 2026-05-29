"""
risk/position_sizing.py - Position sizing using fixed-fractional risk approach.

Sizes each trade so that if the stop-loss is hit, the portfolio loses at most
``RISK_PER_TRADE`` (default 1.5%) of its current value.  Position size is
also capped at ``MAX_POSITION_SIZE`` (10%) of portfolio.
"""

import logging
from typing import Optional

import numpy as np
import pandas as pd

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

logger = logging.getLogger(__name__)


def fixed_fractional_size(
    portfolio_value: float,
    entry_price: float,
    stop_loss_price: float,
    risk_pct: float = None,
    max_position_pct: float = None,
    min_shares: int = 1,
) -> dict:
    """
    Compute position size using the fixed-fractional method.

    Position size = (portfolio_value × risk_pct) / (entry_price − stop_loss_price)

    The result is further capped at ``max_position_pct`` of portfolio and
    floored at ``min_shares``.

    Parameters
    ----------
    portfolio_value : float
        Current total portfolio value (NTD).
    entry_price : float
        Expected entry price per share.
    stop_loss_price : float
        Stop-loss price per share.
    risk_pct : float, optional
        Fraction of portfolio to risk per trade.  Defaults to
        ``config.RISK_PER_TRADE`` (1.5%).
    max_position_pct : float, optional
        Maximum fraction of portfolio for a single position.  Defaults to
        ``config.MAX_POSITION_SIZE`` (10%).
    min_shares : int
        Minimum number of shares (Taiwan lots are 1000 shares; we use 1
        for simplicity).

    Returns
    -------
    dict
        Keys:
        - shares       : float – recommended number of shares
        - position_value : float – total position value at entry
        - risk_amount  : float – dollar risk if stop is hit
        - position_pct : float – position as % of portfolio
        - capped       : bool – whether position was capped by max_position_pct
    """
    if risk_pct is None:
        risk_pct = config.RISK_PER_TRADE
    if max_position_pct is None:
        max_position_pct = config.MAX_POSITION_SIZE

    if portfolio_value <= 0:
        raise ValueError("portfolio_value must be positive.")
    if entry_price <= 0:
        raise ValueError("entry_price must be positive.")
    if stop_loss_price >= entry_price:
        logger.warning(
            "stop_loss_price (%.2f) >= entry_price (%.2f); using 2%% below entry.",
            stop_loss_price, entry_price,
        )
        stop_loss_price = entry_price * 0.98

    risk_amount = portfolio_value * risk_pct
    risk_per_share = entry_price - stop_loss_price

    if risk_per_share <= 0:
        return {
            "shares": 0.0,
            "position_value": 0.0,
            "risk_amount": 0.0,
            "position_pct": 0.0,
            "capped": False,
        }

    shares = risk_amount / risk_per_share

    # Cap at max position size
    max_shares = (portfolio_value * max_position_pct) / entry_price
    capped = shares > max_shares
    shares = min(shares, max_shares)
    shares = max(shares, float(min_shares))

    position_value = shares * entry_price
    position_pct = position_value / portfolio_value

    return {
        "shares": shares,
        "position_value": position_value,
        "risk_amount": min(risk_amount, shares * risk_per_share),
        "position_pct": position_pct,
        "capped": capped,
    }


def kelly_fraction(
    win_rate: float,
    avg_win: float,
    avg_loss: float,
    max_fraction: float = 0.25,
) -> float:
    """
    Compute the Kelly fraction for position sizing.

    Kelly f = (win_rate / avg_loss) - ((1 - win_rate) / avg_win)

    Parameters
    ----------
    win_rate : float
        Historical win rate (0 to 1).
    avg_win : float
        Average gain on winning trades (as fraction, e.g. 0.05 for 5%).
    avg_loss : float
        Average loss on losing trades (as positive fraction, e.g. 0.03 for 3%).
    max_fraction : float
        Cap the Kelly fraction (full Kelly is often too aggressive).

    Returns
    -------
    float
        Recommended fraction of portfolio to allocate (half-Kelly is common).
    """
    if avg_loss <= 0 or avg_win <= 0:
        return 0.0

    kelly = (win_rate / avg_loss) - ((1 - win_rate) / avg_win)
    # Half-Kelly for safety
    half_kelly = kelly / 2
    return float(max(0.0, min(half_kelly, max_fraction)))


def equal_weight_size(
    portfolio_value: float,
    entry_price: float,
    n_positions: int,
    max_position_pct: float = None,
) -> dict:
    """
    Size a position for an equal-weight portfolio.

    Parameters
    ----------
    portfolio_value : float
    entry_price : float
    n_positions : int
        Total number of target positions in the portfolio.
    max_position_pct : float, optional

    Returns
    -------
    dict
        Same keys as ``fixed_fractional_size``.
    """
    if max_position_pct is None:
        max_position_pct = config.MAX_POSITION_SIZE

    if n_positions <= 0:
        n_positions = 1

    target_pct = min(1.0 / n_positions, max_position_pct)
    target_value = portfolio_value * target_pct
    shares = target_value / entry_price if entry_price > 0 else 0.0

    return {
        "shares": shares,
        "position_value": shares * entry_price,
        "risk_amount": target_value * 0.015,  # rough estimate
        "position_pct": target_pct,
        "capped": target_pct == max_position_pct,
    }


def compute_stop_loss_price(
    entry_price: float,
    atr: float,
    atr_multiplier: float = None,
) -> float:
    """
    Compute ATR-based stop-loss price.

    stop_loss = entry_price - (atr_multiplier × ATR)

    Parameters
    ----------
    entry_price : float
    atr : float
        Average True Range value at entry.
    atr_multiplier : float, optional
        Multiplier for ATR.  Defaults to ``config.ATR_STOP_MULTIPLIER``.

    Returns
    -------
    float
        Stop-loss price.
    """
    if atr_multiplier is None:
        atr_multiplier = config.ATR_STOP_MULTIPLIER

    if pd.isna(atr) or atr <= 0:
        return entry_price * 0.97  # 3% fallback stop

    return max(0.0, entry_price - atr_multiplier * atr)


# ---------------------------------------------------------------------------
# v0.3.6 – Capital allocation engine (老王教學: 20201112 資金如何分批佈局)
# ---------------------------------------------------------------------------

def portfolio_capital_allocation(
    portfolio_value: float,
    strategy_capital_ratio: float = 0.30,
    n_positions: int = 4,
    entry_price: float = 0.0,
    atr: float = None,
    open_gap_pct: float = 0.0,
) -> dict:
    """
    Compute the overall capital plan and per-stock batch sizing.

    Rules:
    - Only ``strategy_capital_ratio`` (default 30%) of total portfolio is
      deployed into strategy trades.
    - That capital is split equally across ``n_positions`` (3–5 stocks).
    - Each stock is entered in two batches (first ~60%, second ~40%).
    - Opening gap > 3% flags a no-chase condition.

    Parameters
    ----------
    portfolio_value : float
        Total portfolio value (NTD).
    strategy_capital_ratio : float
        Fraction of portfolio to deploy in strategy (default 0.30).
    n_positions : int
        Number of target positions (3–5).
    entry_price : float
        Expected entry price per share (used to convert NTD → shares).
    atr : float, optional
        ATR for stop-loss estimation.
    open_gap_pct : float
        Today's opening gap percentage (e.g. 0.02 = +2%).

    Returns
    -------
    dict
        position_plan              : str   human-readable plan summary
        portfolio_weight_warning   : str
        first_entry_size           : float  NTD for first batch
        second_entry_size          : float  NTD for second batch
        max_single_stock_weight    : float  fraction of total portfolio
        take_profit_half_price     : float | None
        take_profit_half_reason    : str
        remaining_trailing_stop    : float | None
        breakeven_exit_price       : float | None
        capital_reallocation_suggestion : str
        no_chase_reason            : str
    """
    n_pos = max(3, min(5, n_positions))
    strat_capital = portfolio_value * strategy_capital_ratio
    per_stock_capital = strat_capital / n_pos

    # Per-stock batches (first ~60%, second ~40%)
    first_entry_size  = per_stock_capital * 0.60
    second_entry_size = per_stock_capital * 0.40

    max_single_stock_weight = per_stock_capital / portfolio_value

    # No-chase check
    no_chase_reason = ""
    if open_gap_pct > 0.03:
        no_chase_reason = (
            f"開盤跳空 {open_gap_pct*100:.1f}% > 3%，列入不追價清單"
        )

    # Take-profit half price (ATR-based or fallback +5%)
    tp_half_price  = None
    tp_half_reason = ""
    if entry_price and entry_price > 0:
        if atr and atr > 0:
            tp_half_price  = round(entry_price + 2.0 * atr, 2)
            tp_half_reason = "ATR × 2 目標達停利先賣一半"
        else:
            tp_half_price  = round(entry_price * 1.05, 2)
            tp_half_reason = "開盤小開高 +5% 或單日漲幅 5% 以上，先賣一半（ATR 不可用，使用 5% 估算）"

    # Trailing stop (breakeven if cost not yet pulled away; trail otherwise)
    breakeven_exit = round(entry_price * 1.001, 2) if entry_price and entry_price > 0 else None
    remaining_trail = (
        round(entry_price * 0.97, 2) if entry_price and entry_price > 0 else None
    )

    # Capital reallocation hint
    realloc = (
        "若第一批已停利且股票脫離低風險區，剩餘資金應轉向其他候選股，"
        "不要硬加碼原股"
    )

    plan_summary = (
        f"策略資金 {strategy_capital_ratio*100:.0f}% = "
        f"NTD {strat_capital:,.0f}，"
        f"分配 {n_pos} 檔，"
        f"每檔約 NTD {per_stock_capital:,.0f}"
        f"（第一批 {first_entry_size:,.0f} / 第二批 {second_entry_size:,.0f}）"
    )

    weight_warning = (
        f"單一持股上限 {max_single_stock_weight*100:.1f}%，"
        "不可因其他股票已噴出而任意加碼到失衡"
    )

    return {
        "position_plan":                plan_summary,
        "portfolio_weight_warning":     weight_warning,
        "first_entry_size":             round(first_entry_size, 0),
        "second_entry_size":            round(second_entry_size, 0),
        "max_single_stock_weight":      round(max_single_stock_weight, 4),
        "take_profit_half_price":       tp_half_price,
        "take_profit_half_reason":      tp_half_reason,
        "remaining_trailing_stop":      remaining_trail,
        "breakeven_exit_price":         breakeven_exit,
        "capital_reallocation_suggestion": realloc,
        "no_chase_reason":              no_chase_reason,
    }


def first_batch_entry(
    entry_price: float,
    open_price: float,
    risk_acceptable: bool = True,
) -> dict:
    """
    Determine whether the first batch entry is valid.

    Rules (老王 20201112):
    - Small gap-up 0%–1.5% at open: first batch OK if risk is acceptable.
    - Gap > 3%: no chase, list in no_chase_reason.
    - No pre-market market-order chasing.

    Parameters
    ----------
    entry_price : float   Reference / previous close.
    open_price  : float   Today's opening price.
    risk_acceptable : bool  External risk gate (volatility, stop distance, etc.).

    Returns
    -------
    dict
        can_enter_first_batch : bool
        gap_pct               : float
        no_chase_reason       : str
    """
    gap_pct = (open_price - entry_price) / entry_price if entry_price > 0 else 0.0

    if gap_pct > 0.03:
        return {
            "can_enter_first_batch": False,
            "gap_pct": round(gap_pct, 4),
            "no_chase_reason": (
                f"開盤跳空 {gap_pct*100:.1f}% > 3%，禁止追高，列入不追價清單"
            ),
        }

    if 0.0 <= gap_pct <= 0.015 and risk_acceptable:
        return {
            "can_enter_first_batch": True,
            "gap_pct": round(gap_pct, 4),
            "no_chase_reason": "",
        }

    return {
        "can_enter_first_batch": False,
        "gap_pct": round(gap_pct, 4),
        "no_chase_reason": (
            "風險不在可接受範圍，或開盤漲幅不符合第一批條件"
        ),
    }


def second_batch_entry(
    current_price: float,
    entry_cost: float,
    ma5: float = None,
    ma10: float = None,
    ma20: float = None,
    support_price: float = None,
    first_batch_sold: bool = False,
    stock_left_low_risk_zone: bool = False,
) -> dict:
    """
    Determine whether adding a second batch is justified.

    Rules (老王 20201112):
    - Only add when price pulls back to MA5 / MA10 / MA20 or near cost and holds.
    - Never chase after a breakout spike.
    - If first batch already sold and stock has left the low-risk zone,
      redirect capital to other candidates instead.

    Returns
    -------
    dict
        can_add_second_batch     : bool
        second_batch_reason      : str
        redirect_capital_reason  : str
    """
    redirect_reason = ""
    if first_batch_sold and stock_left_low_risk_zone:
        redirect_reason = (
            "第一批已停利且股票脫離低風險區，剩餘資金應轉向其他候選股，不要硬加原股"
        )
        return {
            "can_add_second_batch": False,
            "second_batch_reason":  "",
            "redirect_capital_reason": redirect_reason,
        }

    tolerance = 0.02  # 2% tolerance for "near" support
    candidates = []

    for label, level in [
        ("MA5", ma5), ("MA10", ma10), ("MA20", ma20), ("支撐價", support_price), ("成本", entry_cost)
    ]:
        if level and level > 0:
            if abs(current_price - level) / level <= tolerance and current_price >= level:
                candidates.append(label)

    if candidates:
        return {
            "can_add_second_batch": True,
            "second_batch_reason": (
                f"回測 {' / '.join(candidates)} 附近不破，可加第二批"
            ),
            "redirect_capital_reason": "",
        }

    # Check if price already broke far above cost (spike-chasing risk)
    if entry_cost and entry_cost > 0:
        gap = (current_price - entry_cost) / entry_cost
        if gap > 0.05:
            return {
                "can_add_second_batch": False,
                "second_batch_reason":  "",
                "redirect_capital_reason": (
                    f"股價已大幅高於成本 {gap*100:.1f}%，不可因股價噴出而追高加碼"
                ),
            }

    return {
        "can_add_second_batch": False,
        "second_batch_reason":  "尚未回測任何均線或成本支撐，等待更好的加碼點",
        "redirect_capital_reason": "",
    }


def take_profit_half(
    current_price: float,
    entry_price: float,
    take_profit_target: float = None,
    previous_high: float = None,
    daily_gain_pct: float = None,
) -> dict:
    """
    Determine whether to take half profit now.

    Rules (老王 20201112):
    - Trigger: reached take-profit target, broke previous high resistance,
      or single-day gain >= 5%.
    - Action: sell half position.

    Returns
    -------
    dict
        take_profit_half_price  : float | None
        take_profit_half_reason : str
        should_take_half        : bool
    """
    reasons = []

    at_target = take_profit_target and current_price >= take_profit_target * 0.99
    at_prev_high = previous_high and current_price >= previous_high * 0.99
    single_day_surge = daily_gain_pct is not None and daily_gain_pct >= 0.05

    if at_target:
        reasons.append(f"達停利目標 ({take_profit_target:.2f})")
    if at_prev_high:
        reasons.append(f"突破前高壓力 ({previous_high:.2f})")
    if single_day_surge:
        reasons.append(f"單日漲幅 {daily_gain_pct*100:.1f}% ≥ 5%")

    should_take = bool(reasons)
    return {
        "take_profit_half_price":  round(current_price, 2) if should_take else None,
        "take_profit_half_reason": "；".join(reasons) if reasons else "",
        "should_take_half":        should_take,
    }


def remaining_position_management(
    current_price: float,
    entry_price: float,
    holding_mode: str = "SHORT_TERM",
    ma5: float = None,
    ma10: float = None,
    ma20: float = None,
) -> dict:
    """
    Manage the remaining half position after the first half was sold.

    Rules (老王 20201112):
    - SHORT_TERM   → trail MA5
    - TRUST_TREND  → trail MA10
    - SWING        → trail MA20 / monthly MA
    - If remaining position hasn't pulled away from cost → use breakeven exit.
    - If remaining position has pulled well above cost → use trailing stop.

    Returns
    -------
    dict
        primary_trailing_ma    : int
        trailing_stop_price    : float | None
        breakeven_exit_price   : float | None
        management_reason      : str
    """
    mode_map = {
        "SHORT_TERM":  (5,  ma5),
        "TRUST_TREND": (10, ma10),
        "SWING":       (20, ma20),
    }
    ma_period, ma_value = mode_map.get(holding_mode, (20, ma20))

    pulled_away = (
        entry_price and entry_price > 0
        and current_price > entry_price * 1.03
    )

    trailing_stop = round(ma_value, 2) if (ma_value and ma_value > 0) else None
    breakeven     = round(entry_price * 1.001, 2) if (entry_price and entry_price > 0) else None

    if pulled_away:
        reason = (
            f"剩餘持股已拉開成本，使用 MA{ma_period} "
            f"({ma_value:.2f}) 作移動停利"
        ) if ma_value else "剩餘持股已拉開成本，使用移動停利"
        return {
            "primary_trailing_ma":  ma_period,
            "trailing_stop_price":  trailing_stop,
            "breakeven_exit_price": None,
            "management_reason":    reason,
        }
    else:
        reason = (
            f"剩餘持股尚未拉開成本，使用損益平衡出場價 ({breakeven})"
        ) if breakeven else "剩餘持股尚未拉開成本，守損益平衡"
        return {
            "primary_trailing_ma":  ma_period,
            "trailing_stop_price":  None,
            "breakeven_exit_price": breakeven,
            "management_reason":    reason,
        }


def compute_take_profit_price(
    entry_price: float,
    atr: float,
    atr_multiplier: float = None,
) -> float:
    """
    Compute ATR-based take-profit price.

    take_profit = entry_price + (atr_multiplier × ATR)

    Parameters
    ----------
    entry_price : float
    atr : float
    atr_multiplier : float, optional
        Defaults to ``config.ATR_TARGET_MULTIPLIER``.

    Returns
    -------
    float
        Take-profit price.
    """
    if atr_multiplier is None:
        atr_multiplier = config.ATR_TARGET_MULTIPLIER

    if pd.isna(atr) or atr <= 0:
        return entry_price * 1.06  # 6% fallback target

    return entry_price + atr_multiplier * atr
