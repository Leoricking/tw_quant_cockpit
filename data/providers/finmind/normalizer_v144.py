"""
data/providers/finmind/normalizer_v144.py — FinMind canonical normalizer v1.4.4.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] authority="SECONDARY_AGGREGATOR", source="finmind" on all output records.
[!] Never mix narrow/wide institutional formats.
[!] Never mix margin/short/securities lending fields.
[!] Preserve unknown fields with warning.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_SOURCE = "finmind"
_AUTHORITY = "SECONDARY_AGGREGATOR"


class FinMindNormalizer:
    """
    Maps raw FinMind records to canonical field names.
    All output records include source="finmind" and authority="SECONDARY_AGGREGATOR".
    """

    def normalize_price(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Normalize TaiwanStockPrice records.
        Maps: date→trade_date, stock_id→symbol, Trading_Volume→volume,
              Trading_money→turnover, open→open, max→high, min→low, close→close,
              spread→price_change, Trading_turnover→transaction_count
        """
        result = []
        for rec in records:
            warnings: List[str] = []
            normalized: Dict[str, Any] = {
                "source": _SOURCE,
                "authority": _AUTHORITY,
            }
            # Known mappings
            known = {
                "date": "trade_date",
                "stock_id": "symbol",
                "Trading_Volume": "volume",
                "Trading_money": "turnover",
                "open": "open",
                "max": "high",
                "min": "low",
                "close": "close",
                "spread": "price_change",
                "Trading_turnover": "transaction_count",
            }
            consumed = set()
            for src_key, dst_key in known.items():
                if src_key in rec:
                    normalized[dst_key] = rec[src_key]
                    consumed.add(src_key)
            # Unknown fields → preserve with warning
            for k, v in rec.items():
                if k not in consumed:
                    warnings.append(f"Unknown price field preserved: {k!r}")
                    normalized[k] = v
            if warnings:
                normalized["_warnings"] = warnings
            result.append(normalized)
        return result

    def normalize_institutional_narrow(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Normalize TaiwanStockInstitutionalInvestorsBuySell (narrow format).
        One row per institution per date. Maps to: foreign_net, trust_net, dealer_net,
        dealer_proprietary, dealer_hedge.
        Never mix with wide format.
        """
        # Group by (date, stock_id) and aggregate institution rows
        groups: Dict[str, Dict[str, Any]] = {}
        for rec in records:
            date_val = rec.get("date", "")
            stock_id = rec.get("stock_id", "")
            key = f"{date_val}|{stock_id}"
            if key not in groups:
                groups[key] = {
                    "trade_date": date_val,
                    "symbol": stock_id,
                    "source": _SOURCE,
                    "authority": _AUTHORITY,
                    "foreign_net": None,
                    "trust_net": None,
                    "dealer_net": None,
                    "dealer_proprietary": None,
                    "dealer_hedge": None,
                    "_warnings": [],
                }
            entry = groups[key]
            name = str(rec.get("name", "")).strip()
            buy = rec.get("buy", 0) or 0
            sell = rec.get("sell", 0) or 0
            net = buy - sell
            if "外資" in name or "Foreign" in name:
                entry["foreign_net"] = net
            elif "投信" in name or "Investment Trust" in name:
                entry["trust_net"] = net
            elif "自營商" in name or "Dealer" in name:
                dealer_type = rec.get("type", "")
                if "自行" in dealer_type or "Proprietary" in dealer_type:
                    entry["dealer_proprietary"] = net
                elif "避險" in dealer_type or "Hedge" in dealer_type:
                    entry["dealer_hedge"] = net
                else:
                    entry["dealer_net"] = net
            else:
                entry["_warnings"].append(f"Unrecognized institution: {name!r}")
                entry[f"unknown_{name[:20]}"] = net
        result = list(groups.values())
        return result

    def normalize_institutional_wide(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Normalize TaiwanStockInstitutionalInvestorsBuySellWide (wide format).
        Never mix with narrow format output.
        """
        result = []
        for rec in records:
            warnings: List[str] = []
            normalized: Dict[str, Any] = {
                "source": _SOURCE,
                "authority": _AUTHORITY,
                "format": "wide",
            }
            wide_mappings = {
                "date": "trade_date",
                "stock_id": "symbol",
                "Foreign_Investor_Buy": "foreign_buy",
                "Foreign_Investor_Sell": "foreign_sell",
                "Foreign_Dealer_Self_Buy": "foreign_dealer_buy",
                "Foreign_Dealer_Self_Sell": "foreign_dealer_sell",
                "Investment_Trust_Buy": "trust_buy",
                "Investment_Trust_Sell": "trust_sell",
                "Dealer_Buy": "dealer_buy",
                "Dealer_Sell": "dealer_sell",
                "Dealer_Hedging_Buy": "dealer_hedge_buy",
                "Dealer_Hedging_Sell": "dealer_hedge_sell",
            }
            consumed = set()
            for src_key, dst_key in wide_mappings.items():
                if src_key in rec:
                    normalized[dst_key] = rec[src_key]
                    consumed.add(src_key)
            for k, v in rec.items():
                if k not in consumed:
                    warnings.append(f"Unknown wide institutional field preserved: {k!r}")
                    normalized[k] = v
            if warnings:
                normalized["_warnings"] = warnings
            result.append(normalized)
        return result

    def normalize_margin(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Normalize TaiwanStockMarginPurchaseShortSale records.
        Maps: MarginPurchaseTodayBalance→margin_balance,
              ShortSaleTodayBalance→short_balance.
        Never mix margin/short/securities lending.
        """
        result = []
        for rec in records:
            warnings: List[str] = []
            normalized: Dict[str, Any] = {
                "source": _SOURCE,
                "authority": _AUTHORITY,
            }
            margin_mappings = {
                "date": "trade_date",
                "stock_id": "symbol",
                "MarginPurchaseTodayBalance": "margin_balance",
                "MarginPurchaseBuy": "margin_buy",
                "MarginPurchaseSell": "margin_sell",
                "MarginPurchaseCashRepayment": "margin_cash_repayment",
                "ShortSaleTodayBalance": "short_balance",
                "ShortSaleBuy": "short_buy",
                "ShortSaleSell": "short_sell",
                "ShortSaleStockRepayment": "short_stock_repayment",
            }
            consumed = set()
            for src_key, dst_key in margin_mappings.items():
                if src_key in rec:
                    normalized[dst_key] = rec[src_key]
                    consumed.add(src_key)
            for k, v in rec.items():
                if k not in consumed:
                    warnings.append(f"Unknown margin field preserved: {k!r}")
                    normalized[k] = v
            if warnings:
                normalized["_warnings"] = warnings
            result.append(normalized)
        return result
