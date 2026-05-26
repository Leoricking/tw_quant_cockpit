"""
analysis/buy_point_analyzer.py - Strong stock pullback buy point engine.

Classifies buy opportunities into A/B/C grades:
  A: MA10 pullback — volume contraction, KD turning up, no institutional selling
  B: MA5 intraday pullback — stand above VWAP, positive orderbook imbalance
  C: Platform consolidation breakout — volume expansion above 20d average

Output fields:
    symbol, buy_point_grade, buy_point_type, decision,
    support_price, confirm_price, invalid_price,
    add_position_price, exit_price, stop_loss_price,
    no_entry_conditions, reasoning, data_completeness, warning

First version: simulation/mock mode only. Real order execution is NOT implemented.
"""

import logging
import random

from utils.stable_hash import stable_hash_int as _stable_seed

logger = logging.getLogger(__name__)

_SEED_PRICES = {
    '2330': 850.0, '2454': 1050.0, '2382': 280.0, '2317': 210.0,
    '6669': 1200.0, '3661': 2100.0, '2345': 580.0, '3017': 190.0,
    '2308': 390.0, '2383': 470.0,
}


class BuyPointAnalyzer:
    """
    Buy point grading engine for strong stocks.

    Grades buy points as A (MA10 pullback), B (MA5 intraday),
    or C (platform breakout). Returns a structured decision dict.
    """

    def analyze(self, symbol, price_data=None, chip_data=None, realtime_data=None,
                mode: str = 'mock'):
        """
        Analyze and grade the buy point for a symbol.

        Parameters
        ----------
        symbol : str
        price_data : list of dict or None
            Daily OHLCV bars (newest last).
        chip_data : dict or None
            Institutional flow; keys: foreign_net_3d, trust_net_3d.
        realtime_data : dict or None
            Intraday data; keys: price, vwap, orderbook_imbalance, change_pct.

        Returns
        -------
        dict with keys:
            symbol, buy_point_grade, buy_point_type, decision,
            support_price, confirm_price, invalid_price,
            add_position_price, exit_price, stop_loss_price,
            no_entry_conditions, reasoning, data_completeness, warning
        """
        sym = str(symbol)

        # Real mode firewall: no real price data → block all grades
        has_real_data = bool(price_data or realtime_data)
        if mode == 'real' and not has_real_data:
            return {
                'symbol': sym,
                'buy_point_grade': None,
                'buy_point_type': None,
                'decision': 'WATCH',
                'support_price': None,
                'confirm_price': None,
                'invalid_price': None,
                'add_position_price': None,
                'exit_price': None,
                'stop_loss_price': None,
                'no_entry_conditions': ['缺少真實資料，禁止正式進場判斷'],
                'reasoning': 'REAL MODE 缺真實資料，禁止使用 mock 買點',
                'data_completeness': 0.0,
                'warning': 'REAL MODE 缺真實資料，禁止使用 mock 買點',
            }

        from features.pullback_features import compute_pullback_features
        feat = compute_pullback_features(price_data, chip_data, realtime_data)

        n = feat['data_bars']
        if n >= 20:
            data_completeness = 80.0
        elif n >= 10:
            data_completeness = 50.0
        elif n >= 5:
            data_completeness = 30.0
        else:
            data_completeness = 10.0

        warning = None
        if data_completeness < 50:
            warning = "資料不足，只能做盤中初估，不能當正式短中長線操作依據"

        # Use seed prices for mock mode when data is missing
        rng = random.Random(_stable_seed(sym + 'buypoint') % 99991)
        current_price = feat['current_price'] or _SEED_PRICES.get(sym, 100.0)
        ma10 = feat['ma10'] or current_price * rng.uniform(0.96, 1.01)
        ma5 = feat['ma5'] or current_price * rng.uniform(0.98, 1.02)
        ma20 = feat['ma20'] or current_price * rng.uniform(0.93, 0.99)
        today_low = feat['today_low'] or current_price * rng.uniform(0.97, 1.0)
        avg_vol_5d = feat['avg_volume_5d'] or 10000.0
        avg_vol_20d = feat['avg_volume_20d'] or 10000.0
        today_vol = feat['today_volume'] or avg_vol_5d * rng.uniform(0.6, 1.4)
        k_val = feat['k'] if feat['k'] is not None else rng.uniform(30, 70)
        d_val = feat['d'] if feat['d'] is not None else rng.uniform(30, 70)
        vwap = feat['vwap'] or current_price * rng.uniform(0.99, 1.01)
        ob_imbalance = feat['orderbook_imbalance']
        if ob_imbalance is None:
            ob_imbalance = rng.uniform(-0.3, 0.5)
        foreign_net = feat['foreign_net_3d']
        trust_net = feat['trust_net_3d']
        box_high = feat['box_high'] or current_price * rng.uniform(0.98, 1.02)
        box_range_pct = feat['box_range_pct']
        if box_range_pct is None:
            box_range_pct = rng.uniform(0.03, 0.1)
        upper_shadow_pct = feat['upper_shadow_pct'] if feat['upper_shadow_pct'] is not None else rng.uniform(0.0, 0.3)

        change_pct = 0.0
        if realtime_data and isinstance(realtime_data, dict):
            change_pct = float(realtime_data.get('change_pct', 0) or 0)

        # --- No-entry conditions ---
        no_entry_conditions = []

        if change_pct > 5.0:
            no_entry_conditions.append("早盤急拉 5% 以上，不追高")
        if change_pct > 9.5:
            no_entry_conditions.append("漲停打開爆量，不追")

        _foreign_heavy_sell = (foreign_net is not None and float(foreign_net) < -3000)
        _trust_heavy_sell = (trust_net is not None and float(trust_net) < -1000)
        if _foreign_heavy_sell:
            no_entry_conditions.append("外資連續大賣，不追")
        if _trust_heavy_sell:
            no_entry_conditions.append("投信連續大賣，不追")

        if current_price < ma20 * 0.995:
            no_entry_conditions.append("跌破 20 日線，不低接")

        if upper_shadow_pct > 0.5:
            no_entry_conditions.append("高檔長上影線，不追")

        if current_price < ma10 * 0.98 and avg_vol_5d > 0 and today_vol > avg_vol_5d * 1.3:
            no_entry_conditions.append("跌破 10 日線且放量，不接")

        # --- Grade A: MA10 pullback ---
        buy_point_grade = None
        buy_point_type = None
        support_price = None
        confirm_price = None
        invalid_price = None
        decision = 'WATCH'
        reasoning_parts = []

        ma_aligned = (ma5 > ma10 > ma20) or (current_price > ma20)
        touch_ma10 = today_low <= ma10 * 1.01
        stand_ma10 = current_price >= ma10
        vol_contraction = avg_vol_5d > 0 and today_vol < avg_vol_5d
        no_big_black_k = not (change_pct < -2.0 and avg_vol_5d > 0 and today_vol > avg_vol_5d * 1.5)
        kd_turn_up = k_val > d_val
        no_inst_heavy_sell = not (_foreign_heavy_sell or _trust_heavy_sell)

        if (ma_aligned and touch_ma10 and stand_ma10 and vol_contraction
                and no_big_black_k and kd_turn_up and no_inst_heavy_sell
                and not no_entry_conditions):
            buy_point_grade = 'A'
            buy_point_type = 'A_PULLBACK_MA10'
            support_price = round(ma10, 1)
            confirm_price = round(ma10 * 1.02, 1)
            invalid_price = round(ma10 * 0.98, 1)
            decision = 'BUY_PULLBACK'
            reasoning_parts.append(
                f"A 級買點：MA5({ma5:.1f}) > MA10({ma10:.1f}) > MA20({ma20:.1f})，"
                f"量縮回測 MA10 不破，KD({k_val:.0f}/{d_val:.0f}) 翻上"
            )

        # --- Grade B: MA5 intraday pullback ---
        if buy_point_grade is None:
            touch_ma5 = today_low <= ma5 * 1.01
            stand_ma5 = current_price >= ma5
            stand_vwap = current_price >= vwap
            ob_positive = ob_imbalance > 0

            if (touch_ma5 and stand_ma5 and stand_vwap and ob_positive
                    and not no_entry_conditions):
                buy_point_grade = 'B'
                buy_point_type = 'B_PULLBACK_MA5'
                support_price = round(ma5, 1)
                confirm_price = round(vwap, 1)
                invalid_price = round(ma5 * 0.985, 1)
                decision = 'BUY_PULLBACK'
                reasoning_parts.append(
                    f"B 級買點：回測 MA5({ma5:.1f}) 不破，站回 VWAP({vwap:.1f})，"
                    f"五檔買賣比 {ob_imbalance:+.2f} 偏多"
                )

        # --- Grade C: platform breakout ---
        if buy_point_grade is None:
            platform_tight = box_range_pct < 0.08
            vol_expansion = avg_vol_20d > 0 and today_vol > avg_vol_20d * 1.5
            close_above_box = current_price > box_high * 0.998
            no_long_upper_shadow = upper_shadow_pct < 0.4

            if (platform_tight and vol_expansion and close_above_box
                    and no_long_upper_shadow and not no_entry_conditions):
                buy_point_grade = 'C'
                buy_point_type = 'C_PLATFORM_BREAKOUT'
                support_price = round(box_high, 1)
                confirm_price = round(box_high, 1)
                invalid_price = round(box_high * 0.98, 1)
                decision = 'BUY_BREAKOUT'
                reasoning_parts.append(
                    f"C 級買點：盤整 {min(20, n)} 日（區間 {box_range_pct:.1%}），"
                    f"突破平台 {box_high:.1f}，成交量 {today_vol:.0f} > 20日均量 {avg_vol_20d:.0f} × 1.5"
                )

        if buy_point_grade is None:
            reasoning_parts.append("未符合 A/B/C 任一買點條件")
            if no_entry_conditions:
                reasoning_parts.append("不可買：" + "；".join(no_entry_conditions))

        # Price targets
        if decision in ('BUY_PULLBACK', 'BUY_BREAKOUT'):
            add_position_price = round(current_price * 1.003, 1)
            exit_price = round(current_price * 1.08, 1)
            stop_loss_price = invalid_price if invalid_price else round(current_price * 0.97, 1)
        else:
            add_position_price = None
            exit_price = round(current_price * 1.05, 1)
            stop_loss_price = round(current_price * 0.97, 1)

        reasoning = "；".join(reasoning_parts) if reasoning_parts else "觀望"

        return {
            'symbol': sym,
            'buy_point_grade': buy_point_grade,
            'buy_point_type': buy_point_type,
            'decision': decision,
            'support_price': support_price,
            'confirm_price': confirm_price,
            'invalid_price': invalid_price,
            'add_position_price': add_position_price,
            'exit_price': exit_price,
            'stop_loss_price': stop_loss_price,
            'no_entry_conditions': no_entry_conditions,
            'reasoning': reasoning,
            'data_completeness': data_completeness,
            'warning': warning,
        }
