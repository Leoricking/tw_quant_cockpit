"""
data/providers/mops/cash_flow_v142.py — MOPS cash flow statement parser v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] MOPS_REALTIME_AVAILABLE = False. MOPS_BROKER_EXECUTION_AVAILABLE = False.
[!] MOPS_AUTO_DOWNLOAD_ENABLED = False. MOPS_MOCK_FALLBACK_ENABLED = False.
Cash flow mismatch check: operating+investing+financing should equal net_change_in_cash.
"""
from __future__ import annotations

import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple

from data.providers.mops.models_v142 import MOPSCashFlowStatement, MOPSFetchStatus

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_CF_TOLERANCE = 1.0


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class MOPSCashFlowParser:
    """Parses cash flow statement from MOPS HTML tables."""

    def __init__(self, transport: Optional[Callable] = None) -> None:
        self._transport = transport

    def fetch(
        self,
        symbol: str,
        fiscal_year: int,
        fiscal_period: str,
        is_consolidated: bool = True,
    ) -> Tuple[MOPSFetchStatus, Optional[MOPSCashFlowStatement], Dict[str, Any]]:
        """Fetch and parse cash flow statement."""
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
            "https://mops.twse.com.tw/mops/web/t26sb07_ifrs",
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

        cf = self._parse_cash_flow(
            tables, symbol, fiscal_year, fiscal_period, is_consolidated,
            parser, normalizer, warnings
        )
        if cf is None:
            return MOPSFetchStatus.MALFORMED, None, {**prov, "warnings": warnings}

        return MOPSFetchStatus.SUCCESS, cf, {**prov, "warnings": warnings}

    def _parse_cash_flow(
        self, tables, symbol, fiscal_year, fiscal_period, is_consolidated,
        parser, normalizer, warnings
    ) -> Optional[MOPSCashFlowStatement]:
        now = _now_iso()
        data: Dict[str, Any] = {}

        for table in tables:
            for row in table:
                if len(row) >= 2:
                    key = str(row[0]).strip()
                    val = normalizer.normalize_amount(row[1])
                    self._map_cf_field(data, key, val)

        ocf = data.get("operating_cash_flow")
        icf = data.get("investing_cash_flow")
        fcf_fin = data.get("financing_cash_flow")
        net_change = data.get("net_change_in_cash")
        capex = data.get("capex")

        # Cash flow mismatch check
        cash_flow_mismatch = False
        mismatch_amount = None
        if all(v is not None for v in [ocf, icf, fcf_fin, net_change]):
            expected = ocf + icf + fcf_fin
            diff = abs(expected - net_change)
            if diff > _CF_TOLERANCE:
                cash_flow_mismatch = True
                mismatch_amount = diff
                warnings.append(f"Cash flow mismatch: O+I+F={expected}, net_change={net_change}, diff={diff}")

        free_cash_flow = None
        if ocf is not None and capex is not None:
            free_cash_flow = ocf - abs(capex)

        return MOPSCashFlowStatement(
            symbol=normalizer.canonical_symbol(symbol),
            fiscal_year=fiscal_year,
            fiscal_period=fiscal_period,
            currency="TWD",
            unit="TWD_THOUSAND",
            operating_cash_flow=ocf,
            investing_cash_flow=icf,
            financing_cash_flow=fcf_fin,
            net_change_in_cash=net_change,
            beginning_cash=data.get("beginning_cash"),
            ending_cash=data.get("ending_cash"),
            capex=capex,
            free_cash_flow=free_cash_flow,
            cash_flow_mismatch=cash_flow_mismatch,
            mismatch_amount=mismatch_amount,
            is_consolidated=is_consolidated,
            is_restated=False,
            source_timestamp=None,
            fetched_at=now,
            provider_id="mops_official",
            provenance=None,
            warnings=warnings,
            metadata={},
        )

    def _map_cf_field(self, data: Dict[str, Any], key: str, val: Optional[float]) -> None:
        if "營業活動" in key:
            data["operating_cash_flow"] = val
        elif "投資活動" in key:
            data["investing_cash_flow"] = val
        elif "籌資活動" in key:
            data["financing_cash_flow"] = val
        elif "本期現金及約當現金增減" in key or "現金淨增減" in key:
            data["net_change_in_cash"] = val
        elif "期初現金" in key:
            data["beginning_cash"] = val
        elif "期末現金" in key:
            data["ending_cash"] = val
        elif "購置不動產" in key or "資本支出" in key:
            data["capex"] = val

    def parse_from_fixture(
        self,
        symbol: str,
        fiscal_year: int,
        fiscal_period: str,
        fixture_data: Dict[str, Any],
    ) -> MOPSCashFlowStatement:
        """Parse cash flow from fixture dict (for offline tests)."""
        from data.providers.mops.normalizer_v142 import MOPSNormalizer
        normalizer = MOPSNormalizer()
        now = _now_iso()
        warnings: List[str] = []

        ocf = fixture_data.get("operating_cash_flow")
        icf = fixture_data.get("investing_cash_flow")
        fcf_fin = fixture_data.get("financing_cash_flow")
        net_change = fixture_data.get("net_change_in_cash")
        capex = fixture_data.get("capex")

        cash_flow_mismatch = fixture_data.get("cash_flow_mismatch", False)
        mismatch_amount = fixture_data.get("mismatch_amount")

        if not cash_flow_mismatch and all(v is not None for v in [ocf, icf, fcf_fin, net_change]):
            expected = ocf + icf + fcf_fin
            diff = abs(expected - net_change)
            if diff > _CF_TOLERANCE:
                cash_flow_mismatch = True
                mismatch_amount = diff
                warnings.append(f"Cash flow mismatch: diff={diff}")

        free_cash_flow = fixture_data.get("free_cash_flow")
        if free_cash_flow is None and ocf is not None and capex is not None:
            free_cash_flow = ocf - abs(capex)

        return MOPSCashFlowStatement(
            symbol=normalizer.canonical_symbol(symbol),
            fiscal_year=fiscal_year,
            fiscal_period=fiscal_period,
            currency=fixture_data.get("currency", "TWD"),
            unit=fixture_data.get("unit", "TWD_THOUSAND"),
            operating_cash_flow=ocf,
            investing_cash_flow=icf,
            financing_cash_flow=fcf_fin,
            net_change_in_cash=net_change,
            beginning_cash=fixture_data.get("beginning_cash"),
            ending_cash=fixture_data.get("ending_cash"),
            capex=capex,
            free_cash_flow=free_cash_flow,
            cash_flow_mismatch=cash_flow_mismatch,
            mismatch_amount=mismatch_amount,
            is_consolidated=fixture_data.get("is_consolidated", True),
            is_restated=fixture_data.get("is_restated", False),
            source_timestamp=fixture_data.get("source_timestamp"),
            fetched_at=now,
            provider_id="mops_official",
            provenance=None,
            warnings=warnings,
            metadata={},
        )
