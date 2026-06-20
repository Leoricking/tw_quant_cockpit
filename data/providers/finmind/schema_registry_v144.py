"""
data/providers/finmind/schema_registry_v144.py — FinMind schema definitions v1.4.4.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Schemas define expected fields for drift detection.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


def _schema_hash(schema_dict: Dict[str, Any]) -> str:
    """Compute stable hash of schema definition."""
    canonical = json.dumps(schema_dict, sort_keys=True, ensure_ascii=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]


FINMIND_SCHEMAS: Dict[str, Dict[str, Any]] = {
    "TaiwanStockPrice": {
        "dataset": "TaiwanStockPrice",
        "schema_id": "taiwan_stock_price_v4",
        "schema_version": "4.0",
        "required_fields": ["date", "stock_id", "Trading_Volume", "Trading_money",
                            "open", "max", "min", "close", "spread", "Trading_turnover"],
        "optional_fields": [],
        "field_types": {
            "date": "str", "stock_id": "str", "Trading_Volume": "number",
            "Trading_money": "number", "open": "number", "max": "number",
            "min": "number", "close": "number", "spread": "number",
            "Trading_turnover": "number",
        },
        "primary_key": ["date", "stock_id"],
        "date_fields": ["date"],
        "numeric_fields": ["Trading_Volume", "Trading_money", "open", "max", "min", "close", "spread", "Trading_turnover"],
        "canonical_mapping": {
            "date": "trade_date", "stock_id": "symbol", "Trading_Volume": "volume",
            "Trading_money": "turnover", "open": "open", "max": "high", "min": "low",
            "close": "close", "spread": "price_change", "Trading_turnover": "transaction_count",
        },
    },
    "TaiwanStockInstitutionalInvestorsBuySell": {
        "dataset": "TaiwanStockInstitutionalInvestorsBuySell",
        "schema_id": "taiwan_institutional_narrow_v4",
        "schema_version": "4.0",
        "required_fields": ["date", "stock_id", "name", "buy", "sell"],
        "optional_fields": ["type"],
        "field_types": {
            "date": "str", "stock_id": "str", "name": "str", "buy": "number", "sell": "number",
            "type": "str",
        },
        "primary_key": ["date", "stock_id", "name"],
        "date_fields": ["date"],
        "numeric_fields": ["buy", "sell"],
        "canonical_mapping": {
            "date": "trade_date", "stock_id": "symbol",
        },
    },
    "TaiwanStockInstitutionalInvestorsBuySellWide": {
        "dataset": "TaiwanStockInstitutionalInvestorsBuySellWide",
        "schema_id": "taiwan_institutional_wide_v4",
        "schema_version": "4.0",
        "required_fields": ["date", "stock_id",
                            "Foreign_Investor_Buy", "Foreign_Investor_Sell",
                            "Investment_Trust_Buy", "Investment_Trust_Sell",
                            "Dealer_Buy", "Dealer_Sell"],
        "optional_fields": ["Foreign_Dealer_Self_Buy", "Foreign_Dealer_Self_Sell",
                             "Dealer_Hedging_Buy", "Dealer_Hedging_Sell"],
        "field_types": {
            "date": "str", "stock_id": "str",
            "Foreign_Investor_Buy": "number", "Foreign_Investor_Sell": "number",
            "Investment_Trust_Buy": "number", "Investment_Trust_Sell": "number",
            "Dealer_Buy": "number", "Dealer_Sell": "number",
        },
        "primary_key": ["date", "stock_id"],
        "date_fields": ["date"],
        "numeric_fields": ["Foreign_Investor_Buy", "Foreign_Investor_Sell",
                           "Investment_Trust_Buy", "Investment_Trust_Sell",
                           "Dealer_Buy", "Dealer_Sell"],
        "canonical_mapping": {
            "date": "trade_date", "stock_id": "symbol",
        },
    },
    "TaiwanStockMarginPurchaseShortSale": {
        "dataset": "TaiwanStockMarginPurchaseShortSale",
        "schema_id": "taiwan_margin_v4",
        "schema_version": "4.0",
        "required_fields": ["date", "stock_id",
                            "MarginPurchaseTodayBalance", "ShortSaleTodayBalance"],
        "optional_fields": ["MarginPurchaseBuy", "MarginPurchaseSell",
                             "MarginPurchaseCashRepayment",
                             "ShortSaleBuy", "ShortSaleSell", "ShortSaleStockRepayment"],
        "field_types": {
            "date": "str", "stock_id": "str",
            "MarginPurchaseTodayBalance": "number", "ShortSaleTodayBalance": "number",
        },
        "primary_key": ["date", "stock_id"],
        "date_fields": ["date"],
        "numeric_fields": ["MarginPurchaseTodayBalance", "ShortSaleTodayBalance"],
        "canonical_mapping": {
            "date": "trade_date", "stock_id": "symbol",
            "MarginPurchaseTodayBalance": "margin_balance",
            "ShortSaleTodayBalance": "short_balance",
        },
    },
    "TaiwanStockMonthRevenue": {
        "dataset": "TaiwanStockMonthRevenue",
        "schema_id": "taiwan_monthly_revenue_v4",
        "schema_version": "4.0",
        "required_fields": ["date", "stock_id", "revenue"],
        "optional_fields": ["revenue_month", "cumulative_revenue", "country"],
        "field_types": {
            "date": "str", "stock_id": "str", "revenue": "number",
            "revenue_month": "str", "cumulative_revenue": "number",
        },
        "primary_key": ["date", "stock_id"],
        "date_fields": ["date"],
        "numeric_fields": ["revenue", "cumulative_revenue"],
        "canonical_mapping": {
            "date": "trade_date", "stock_id": "symbol", "revenue": "monthly_revenue",
        },
    },
    "TaiwanStockFinancialStatements": {
        "dataset": "TaiwanStockFinancialStatements",
        "schema_id": "taiwan_financial_statements_v4",
        "schema_version": "4.0",
        "required_fields": ["date", "stock_id", "type", "value"],
        "optional_fields": ["origin_name", "industry_id"],
        "field_types": {
            "date": "str", "stock_id": "str", "type": "str", "value": "number",
            "origin_name": "str", "industry_id": "str",
        },
        "primary_key": ["date", "stock_id", "type"],
        "date_fields": ["date"],
        "numeric_fields": ["value"],
        "canonical_mapping": {
            "date": "trade_date", "stock_id": "symbol",
        },
    },
}

# Compute schema hashes
for _ds_name, _schema in FINMIND_SCHEMAS.items():
    _schema["schema_hash"] = _schema_hash(_schema)


class FinMindSchemaRegistry:
    """Registry for FinMind dataset schemas."""

    def get_schema(self, dataset: str) -> Optional[Dict[str, Any]]:
        """Return schema for dataset, or None."""
        return FINMIND_SCHEMAS.get(dataset)

    def get_schema_hash(self, dataset: str) -> Optional[str]:
        """Return schema hash for dataset, or None."""
        schema = FINMIND_SCHEMAS.get(dataset)
        return schema.get("schema_hash") if schema else None

    def list_schemas(self) -> List[str]:
        """Return list of all known dataset names."""
        return list(FINMIND_SCHEMAS.keys())
