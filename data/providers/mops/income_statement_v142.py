"""
data/providers/mops/income_statement_v142.py — MOPS income statement parser v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] MOPS_REALTIME_AVAILABLE = False. MOPS_BROKER_EXECUTION_AVAILABLE = False.
[!] MOPS_AUTO_DOWNLOAD_ENABLED = False. MOPS_MOCK_FALLBACK_ENABLED = False.
"""
from __future__ import annotations

import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple

from data.providers.mops.models_v142 import MOPSFetchStatus, MOPSIncomeStatement

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class MOPSIncomeStatementParser:
    """Parses income statement data from MOPS HTML tables."""

    def __init__(self, transport: Optional[Callable] = None) -> None:
        self._transport = transport

    def fetch(
        self,
        symbol: str,
        fiscal_year: int,
        fiscal_period: str,
        is_consolidated: bool = True,
    ) -> Tuple[MOPSFetchStatus, Optional[MOPSIncomeStatement], Dict[str, Any]]:
        """Fetch and parse income statement."""
        from data.providers.mops.client_v142 import MOPSHttpClient
        from data.providers.mops.parser_v142 import MOPSParser
        from data.providers.mops.normalizer_v142 import MOPSNormalizer

        client = MOPSHttpClient(transport=self._transport)
        parser = MOPSParser()
        normalizer = MOPSNormalizer()
        warnings: List[str] = []

        roc_year = fiscal_year - 1911
        form_data = {
            "encodeURIComponent": "1",
            "step": "1",
            "co_id": symbol,
            "year": str(roc_year),
        }

        status, content, prov = client.post_form(
            "https://mops.twse.com.tw/mops/web/t26sb04_ifrs",
            form_data,
        )

        if status != MOPSFetchStatus.SUCCESS or not content:
            return status, None, {**prov, "warnings": warnings}

        if parser.is_maintenance_page(content):
            return MOPSFetchStatus.MAINTENANCE, None, {**prov, "warnings": ["Maintenance"]}

        html_text, _ = parser.decode_content(content)
        tables = parser.extract_html_tables(html_text)
        if not tables:
            return MOPSFetchStatus.EMPTY_RESPONSE, None, {**prov, "warnings": ["No tables"]}

        is_obj = self._parse_income_statement(
            tables, symbol, fiscal_year, fiscal_period, is_consolidated,
            parser, normalizer, warnings
        )
        if is_obj is None:
            return MOPSFetchStatus.MALFORMED, None, {**prov, "warnings": warnings}

        return MOPSFetchStatus.SUCCESS, is_obj, {**prov, "warnings": warnings}

    def _parse_income_statement(
        self, tables, symbol, fiscal_year, fiscal_period, is_consolidated,
        parser, normalizer, warnings
    ) -> Optional[MOPSIncomeStatement]:
        now = _now_iso()
        data: Dict[str, Any] = {}

        for table in tables:
            for row in table:
                if len(row) >= 2:
                    key = str(row[0]).strip()
                    val = normalizer.normalize_amount(row[1])
                    self._map_is_field(data, key, val)

        return MOPSIncomeStatement(
            symbol=normalizer.canonical_symbol(symbol),
            fiscal_year=fiscal_year,
            fiscal_period=fiscal_period,
            currency="TWD",
            unit="TWD_THOUSAND",
            revenue=data.get("revenue"),
            cost_of_revenue=data.get("cost_of_revenue"),
            gross_profit=data.get("gross_profit"),
            operating_expenses=data.get("operating_expenses"),
            operating_income=data.get("operating_income"),
            non_operating_income=data.get("non_operating_income"),
            income_before_tax=data.get("income_before_tax"),
            income_tax=data.get("income_tax"),
            net_income=data.get("net_income"),
            net_income_attributable_to_parent=data.get("net_income_attributable_to_parent"),
            eps_basic=data.get("eps_basic"),
            eps_diluted=data.get("eps_diluted"),
            is_consolidated=is_consolidated,
            is_restated=False,
            source_timestamp=None,
            fetched_at=now,
            provider_id="mops_official",
            provenance=None,
            warnings=warnings,
            metadata={},
        )

    def _map_is_field(self, data: Dict[str, Any], key: str, val: Optional[float]) -> None:
        if "營業收入" in key:
            data["revenue"] = val
        elif "營業成本" in key:
            data["cost_of_revenue"] = val
        elif "營業毛利" in key:
            data["gross_profit"] = val
        elif "營業費用" in key:
            data["operating_expenses"] = val
        elif "營業利益" in key:
            data["operating_income"] = val
        elif "營業外收入及支出" in key or "非營業" in key:
            data["non_operating_income"] = val
        elif "稅前淨利" in key or "稅前損益" in key:
            data["income_before_tax"] = val
        elif "所得稅費用" in key:
            data["income_tax"] = val
        elif "本期淨利" in key or "本期損益" in key:
            data["net_income"] = val
        elif "母公司業主" in key:
            data["net_income_attributable_to_parent"] = val
        elif "基本每股盈餘" in key:
            data["eps_basic"] = val
        elif "稀釋每股盈餘" in key:
            data["eps_diluted"] = val

    def parse_from_fixture(
        self,
        symbol: str,
        fiscal_year: int,
        fiscal_period: str,
        fixture_data: Dict[str, Any],
    ) -> MOPSIncomeStatement:
        """Parse income statement from fixture dict (for offline tests)."""
        from data.providers.mops.normalizer_v142 import MOPSNormalizer
        normalizer = MOPSNormalizer()
        now = _now_iso()
        return MOPSIncomeStatement(
            symbol=normalizer.canonical_symbol(symbol),
            fiscal_year=fiscal_year,
            fiscal_period=fiscal_period,
            currency=fixture_data.get("currency", "TWD"),
            unit=fixture_data.get("unit", "TWD_THOUSAND"),
            revenue=fixture_data.get("revenue"),
            cost_of_revenue=fixture_data.get("cost_of_revenue"),
            gross_profit=fixture_data.get("gross_profit"),
            operating_expenses=fixture_data.get("operating_expenses"),
            operating_income=fixture_data.get("operating_income"),
            non_operating_income=fixture_data.get("non_operating_income"),
            income_before_tax=fixture_data.get("income_before_tax"),
            income_tax=fixture_data.get("income_tax"),
            net_income=fixture_data.get("net_income"),
            net_income_attributable_to_parent=fixture_data.get("net_income_attributable_to_parent"),
            eps_basic=fixture_data.get("eps_basic"),
            eps_diluted=fixture_data.get("eps_diluted"),
            is_consolidated=fixture_data.get("is_consolidated", True),
            is_restated=fixture_data.get("is_restated", False),
            source_timestamp=fixture_data.get("source_timestamp"),
            fetched_at=now,
            provider_id="mops_official",
            provenance=None,
            warnings=[],
            metadata={},
        )
