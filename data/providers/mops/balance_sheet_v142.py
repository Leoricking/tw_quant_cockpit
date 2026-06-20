"""
data/providers/mops/balance_sheet_v142.py — MOPS balance sheet parser v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] MOPS_REALTIME_AVAILABLE = False. MOPS_BROKER_EXECUTION_AVAILABLE = False.
[!] MOPS_AUTO_DOWNLOAD_ENABLED = False. MOPS_MOCK_FALLBACK_ENABLED = False.
Balance check: total_assets == total_liabilities + total_equity (within tolerance).
"""
from __future__ import annotations

import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple

from data.providers.mops.models_v142 import MOPSBalanceSheet, MOPSFetchStatus

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_BALANCE_TOLERANCE = 1.0  # 1 unit tolerance for rounding


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class MOPSBalanceSheetParser:
    """Parses balance sheet data from MOPS HTML tables."""

    def __init__(self, transport: Optional[Callable] = None) -> None:
        self._transport = transport

    def fetch(
        self,
        symbol: str,
        fiscal_year: int,
        fiscal_period: str,
        is_consolidated: bool = True,
    ) -> Tuple[MOPSFetchStatus, Optional[MOPSBalanceSheet], Dict[str, Any]]:
        """Fetch and parse balance sheet."""
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
            "https://mops.twse.com.tw/mops/web/t26sb01_ifrs",
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

        bs = self._parse_balance_sheet(
            tables, symbol, fiscal_year, fiscal_period, is_consolidated,
            parser, normalizer, warnings
        )
        if bs is None:
            return MOPSFetchStatus.MALFORMED, None, {**prov, "warnings": warnings}

        return MOPSFetchStatus.SUCCESS, bs, {**prov, "warnings": warnings}

    def _parse_balance_sheet(
        self, tables, symbol, fiscal_year, fiscal_period, is_consolidated,
        parser, normalizer, warnings
    ) -> Optional[MOPSBalanceSheet]:
        """Parse balance sheet from HTML tables as key-value pairs."""
        now = _now_iso()
        data: Dict[str, Any] = {}

        for table in tables:
            for row in table:
                if len(row) >= 2:
                    key = str(row[0]).strip()
                    val = normalizer.normalize_amount(row[1])
                    self._map_bs_field(data, key, val)

        total_assets = data.get("total_assets")
        total_liabilities = data.get("total_liabilities")
        total_equity = data.get("total_equity")

        # Balance check
        is_balanced = True
        balance_diff = None
        if total_assets is not None and total_liabilities is not None and total_equity is not None:
            expected = total_liabilities + total_equity
            balance_diff = abs(total_assets - expected)
            is_balanced = balance_diff <= _BALANCE_TOLERANCE
            if not is_balanced:
                warnings.append(f"Balance sheet unbalanced: assets={total_assets}, L+E={expected}, diff={balance_diff}")

        return MOPSBalanceSheet(
            symbol=normalizer.canonical_symbol(symbol),
            fiscal_year=fiscal_year,
            fiscal_period=fiscal_period,
            currency="TWD",
            unit="TWD_THOUSAND",
            report_date=data.get("report_date"),
            total_assets=total_assets,
            current_assets=data.get("current_assets"),
            non_current_assets=data.get("non_current_assets"),
            cash_and_equivalents=data.get("cash_and_equivalents"),
            receivables=data.get("receivables"),
            inventories=data.get("inventories"),
            total_liabilities=total_liabilities,
            current_liabilities=data.get("current_liabilities"),
            non_current_liabilities=data.get("non_current_liabilities"),
            short_term_borrowings=data.get("short_term_borrowings"),
            long_term_borrowings=data.get("long_term_borrowings"),
            total_equity=total_equity,
            common_stock=data.get("common_stock"),
            retained_earnings=data.get("retained_earnings"),
            is_balanced=is_balanced,
            balance_diff=balance_diff,
            is_consolidated=is_consolidated,
            is_restated=False,
            source_timestamp=None,
            fetched_at=now,
            provider_id="mops_official",
            provenance=None,
            warnings=warnings,
            metadata={},
        )

    def _map_bs_field(self, data: Dict[str, Any], key: str, val: Optional[float]) -> None:
        if "資產總計" in key or "資產合計" in key:
            data["total_assets"] = val
        elif "流動資產" in key and "非" not in key:
            data["current_assets"] = val
        elif "非流動資產" in key:
            data["non_current_assets"] = val
        elif "現金及約當現金" in key:
            data["cash_and_equivalents"] = val
        elif "應收帳款" in key:
            data["receivables"] = val
        elif "存貨" in key:
            data["inventories"] = val
        elif "負債總計" in key or "負債合計" in key:
            data["total_liabilities"] = val
        elif "流動負債" in key and "非" not in key:
            data["current_liabilities"] = val
        elif "非流動負債" in key:
            data["non_current_liabilities"] = val
        elif "短期借款" in key:
            data["short_term_borrowings"] = val
        elif "長期借款" in key:
            data["long_term_borrowings"] = val
        elif "權益總計" in key or "股東權益總計" in key:
            data["total_equity"] = val
        elif "普通股股本" in key or "股本" in key:
            data["common_stock"] = val
        elif "保留盈餘" in key or "累積盈虧" in key:
            data["retained_earnings"] = val

    def parse_from_fixture(
        self,
        symbol: str,
        fiscal_year: int,
        fiscal_period: str,
        fixture_data: Dict[str, Any],
    ) -> MOPSBalanceSheet:
        """Parse balance sheet from fixture dict (for offline tests)."""
        from data.providers.mops.normalizer_v142 import MOPSNormalizer
        normalizer = MOPSNormalizer()
        now = _now_iso()
        warnings: List[str] = []

        total_assets = fixture_data.get("total_assets")
        total_liabilities = fixture_data.get("total_liabilities")
        total_equity = fixture_data.get("total_equity")

        is_balanced = True
        balance_diff = None
        if all(v is not None for v in [total_assets, total_liabilities, total_equity]):
            expected = total_liabilities + total_equity
            balance_diff = abs(total_assets - expected)
            is_balanced = balance_diff <= _BALANCE_TOLERANCE
            if not is_balanced:
                warnings.append(f"Balance sheet unbalanced: diff={balance_diff}")

        return MOPSBalanceSheet(
            symbol=normalizer.canonical_symbol(symbol),
            fiscal_year=fiscal_year,
            fiscal_period=fiscal_period,
            currency=fixture_data.get("currency", "TWD"),
            unit=fixture_data.get("unit", "TWD_THOUSAND"),
            report_date=fixture_data.get("report_date"),
            total_assets=total_assets,
            current_assets=fixture_data.get("current_assets"),
            non_current_assets=fixture_data.get("non_current_assets"),
            cash_and_equivalents=fixture_data.get("cash_and_equivalents"),
            receivables=fixture_data.get("receivables"),
            inventories=fixture_data.get("inventories"),
            total_liabilities=total_liabilities,
            current_liabilities=fixture_data.get("current_liabilities"),
            non_current_liabilities=fixture_data.get("non_current_liabilities"),
            short_term_borrowings=fixture_data.get("short_term_borrowings"),
            long_term_borrowings=fixture_data.get("long_term_borrowings"),
            total_equity=total_equity,
            common_stock=fixture_data.get("common_stock"),
            retained_earnings=fixture_data.get("retained_earnings"),
            is_balanced=is_balanced,
            balance_diff=balance_diff,
            is_consolidated=fixture_data.get("is_consolidated", True),
            is_restated=fixture_data.get("is_restated", False),
            source_timestamp=fixture_data.get("source_timestamp"),
            fetched_at=now,
            provider_id="mops_official",
            provenance=None,
            warnings=warnings,
            metadata={},
        )
