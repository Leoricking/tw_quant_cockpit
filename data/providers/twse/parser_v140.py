"""
data/providers/twse/parser_v140.py — TWSE data parser v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TWSE Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
"""
from __future__ import annotations

import datetime
import re
from typing import Any, Dict, List, Optional, Tuple

from data.providers.twse.models_v140 import (
    TWSECorporateActionPreview,
    TWSEDailyBar,
    TWSEIndexRecord,
    TWSEInstitutionalFlow,
    TWSEMarginRecord,
    TWSEMarketSummary,
    TWSESecurity,
)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_MISSING_MARKERS = {"--", "-", "N/A", "", "暫停交易", "除權", "除息", "除權息", "N/A", "NA"}
_PROVIDER_ID = "twse_official"


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class TWSEParser:
    """
    Parser for TWSE OpenAPI responses.

    Handles:
    - Chinese field names → standard field mapping
    - Comma-separated numbers
    - "--" and "-" → None
    - ROC date (民國年) → CE date
    - OHLC validation
    - Duplicate row detection
    - Malformed row isolation
    """

    def _parse_number(self, s: Any) -> Optional[float]:
        """Parse a number string. Returns None for missing/invalid markers."""
        if s is None:
            return None
        s = str(s).strip()
        if s in _MISSING_MARKERS:
            return None
        # Remove commas
        s = s.replace(",", "")
        # Remove + prefix
        if s.startswith("+"):
            s = s[1:]
        try:
            return float(s)
        except (ValueError, TypeError):
            return None

    def _parse_str(self, s: Any) -> Optional[str]:
        """Parse a string field. Returns None for missing markers."""
        if s is None:
            return None
        s = str(s).strip()
        if s in _MISSING_MARKERS:
            return None
        return s if s else None

    def parse_roc_date(self, roc_str: Any) -> Optional[str]:
        """Convert ROC date (民國年) to CE date (YYYY-MM-DD)."""
        if roc_str is None:
            return None
        s = str(roc_str).strip()
        # Handle format like "1130101" (YYYMMDD in ROC)
        m = re.match(r"^(\d{3})(\d{2})(\d{2})$", s)
        if m:
            roc_year = int(m.group(1))
            month = int(m.group(2))
            day = int(m.group(3))
            ce_year = roc_year + 1911
            return f"{ce_year:04d}-{month:02d}-{day:02d}"
        # Handle format like "113/01/01"
        m = re.match(r"^(\d{2,3})/(\d{2})/(\d{2})$", s)
        if m:
            roc_year = int(m.group(1))
            month = int(m.group(2))
            day = int(m.group(3))
            ce_year = roc_year + 1911
            return f"{ce_year:04d}-{month:02d}-{day:02d}"
        # Handle ISO-ish format already
        m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", s)
        if m:
            return s
        # Handle 8-digit YYYYMMDD
        m = re.match(r"^(\d{4})(\d{2})(\d{2})$", s)
        if m:
            year = int(m.group(1))
            if year < 1912:
                year += 1911
            return f"{year:04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
        return None

    def parse_security_master(
        self, raw_data: List[Dict[str, Any]]
    ) -> Tuple[List[TWSESecurity], List[str]]:
        """Parse security master data."""
        records: List[TWSESecurity] = []
        warnings: List[str] = []
        seen_symbols: set = set()
        now = _now_iso()

        for i, row in enumerate(raw_data):
            if not isinstance(row, dict):
                warnings.append(f"Row {i}: not a dict, skipping")
                continue
            try:
                # Support multiple field name formats
                symbol = self._parse_str(
                    row.get("Code") or row.get("公司代號") or row.get("證券代號")
                )
                if not symbol:
                    warnings.append(f"Row {i}: no symbol, skipping")
                    continue
                if symbol in seen_symbols:
                    warnings.append(f"Row {i}: duplicate symbol {symbol}, keeping first")
                    continue
                seen_symbols.add(symbol)

                name = self._parse_str(
                    row.get("Name") or row.get("公司簡稱") or row.get("證券名稱")
                )
                industry_code = self._parse_str(
                    row.get("IndustryCode") or row.get("產業別") or row.get("industry_code")
                )
                industry_name = self._parse_str(
                    row.get("IndustryName") or row.get("industry_name")
                )
                listing_date_raw = row.get("ListingDate") or row.get("上市日期") or row.get("listing_date")
                listing_date = self.parse_roc_date(listing_date_raw) if listing_date_raw else None
                isin = self._parse_str(row.get("ISIN") or row.get("ISIN碼"))
                # Determine security type from CFI code
                cfi = self._parse_str(row.get("CFICode") or row.get("CFI碼"))
                sec_type = self._classify_from_cfi(cfi, symbol)

                sec = TWSESecurity(
                    symbol=symbol,
                    name=name,
                    market="TWSE",
                    security_type=sec_type,
                    industry_code=industry_code,
                    industry_name=industry_name,
                    listing_date=listing_date,
                    isin=isin,
                    currency="TWD",
                    status="LISTED",
                    source_timestamp=None,
                    fetched_at=now,
                    provider_id=_PROVIDER_ID,
                    provenance=None,
                    metadata={},
                )
                records.append(sec)
            except Exception as exc:
                warnings.append(f"Row {i}: parse error {exc}, skipping")

        return records, warnings

    def _classify_from_cfi(self, cfi: Optional[str], symbol: str) -> str:
        """Classify security type from CFI code."""
        if cfi:
            if cfi.startswith("ES"):
                return "COMMON_STOCK"
            if cfi.startswith("EU"):
                return "ETF"
            if cfi.startswith("RW") or cfi.startswith("CW"):
                return "WARRANT"
        # Heuristic by symbol
        if len(symbol) == 4 and symbol.isdigit():
            return "COMMON_STOCK"
        if len(symbol) == 4 and symbol.startswith("0"):
            return "ETF"
        return "UNKNOWN"

    def parse_daily_ohlcv(
        self, raw_data: List[Dict[str, Any]], trade_date: str
    ) -> Tuple[List[TWSEDailyBar], List[str]]:
        """Parse daily OHLCV data."""
        records: List[TWSEDailyBar] = []
        warnings: List[str] = []
        seen_symbols: set = set()
        now = _now_iso()

        for i, row in enumerate(raw_data):
            if not isinstance(row, dict):
                warnings.append(f"Row {i}: not a dict, skipping")
                continue
            try:
                symbol = self._parse_str(
                    row.get("證券代號") or row.get("Code") or row.get("symbol")
                )
                if not symbol:
                    warnings.append(f"Row {i}: no symbol, skipping")
                    continue
                if symbol in seen_symbols:
                    warnings.append(f"Row {i}: duplicate symbol {symbol}, keeping first")
                    continue
                seen_symbols.add(symbol)

                open_p = self._parse_str(row.get("開盤價"))
                high_p = self._parse_str(row.get("最高價"))
                low_p = self._parse_str(row.get("最低價"))
                close_p = self._parse_str(row.get("收盤價"))
                change = self._parse_str(row.get("漲跌價差"))
                volume_raw = self._parse_number(row.get("成交股數"))
                turnover_raw = self._parse_number(row.get("成交金額"))
                tx_raw = self._parse_number(row.get("成交筆數"))

                # OHLC validation
                if high_p is not None and low_p is not None:
                    try:
                        h = float(high_p)
                        l = float(low_p)
                        if h < l:
                            warnings.append(
                                f"Symbol {symbol}: high ({high_p}) < low ({low_p}), rejecting bar"
                            )
                            continue
                    except (ValueError, TypeError):
                        pass

                bar = TWSEDailyBar(
                    symbol=symbol,
                    trade_date=trade_date,
                    open=open_p,
                    high=high_p,
                    low=low_p,
                    close=close_p,
                    volume=volume_raw,
                    turnover=turnover_raw,
                    transaction_count=tx_raw,
                    price_change=change,
                    adjusted_status="NOT_ADJUSTED",
                    source_timestamp=None,
                    fetched_at=now,
                    provider_id=_PROVIDER_ID,
                    provenance=None,
                    warnings=[],
                    metadata={},
                )
                records.append(bar)
            except Exception as exc:
                warnings.append(f"Row {i}: parse error {exc}, skipping")

        return records, warnings

    def parse_institutional(
        self, raw_data: List[Dict[str, Any]], trade_date: str
    ) -> Tuple[List[TWSEInstitutionalFlow], List[str]]:
        """Parse institutional investor flow data."""
        records: List[TWSEInstitutionalFlow] = []
        warnings: List[str] = []
        now = _now_iso()

        for i, row in enumerate(raw_data):
            if not isinstance(row, dict):
                warnings.append(f"Row {i}: not a dict, skipping")
                continue
            try:
                symbol = self._parse_str(
                    row.get("證券代號") or row.get("Code") or row.get("symbol")
                )
                if not symbol:
                    warnings.append(f"Row {i}: no symbol, skipping")
                    continue

                foreign_buy = self._parse_number(
                    row.get("外陸資買進股數(不含外資自營商)")
                    or row.get("外資買進")
                )
                foreign_sell = self._parse_number(
                    row.get("外陸資賣出股數(不含外資自營商)")
                    or row.get("外資賣出")
                )
                foreign_net = self._parse_number(
                    row.get("外陸資買賣超股數")
                    or row.get("外資買賣超")
                )
                trust_buy = self._parse_number(row.get("投信買進股數"))
                trust_sell = self._parse_number(row.get("投信賣出股數"))
                trust_net = self._parse_number(row.get("投信買賣超股數"))
                dealer_buy = self._parse_number(
                    row.get("自營商買進股數(自行買賣)")
                    or row.get("自營商買進")
                )
                dealer_sell = self._parse_number(
                    row.get("自營商賣出股數(自行買賣)")
                    or row.get("自營商賣出")
                )
                dealer_net = self._parse_number(row.get("自營商買賣超股數"))
                total_net = self._parse_number(row.get("三大法人買賣超股數"))

                flow = TWSEInstitutionalFlow(
                    symbol=symbol,
                    trade_date=trade_date,
                    foreign_buy=foreign_buy,
                    foreign_sell=foreign_sell,
                    foreign_net=foreign_net,
                    investment_trust_buy=trust_buy,
                    investment_trust_sell=trust_sell,
                    investment_trust_net=trust_net,
                    dealer_buy=dealer_buy,
                    dealer_sell=dealer_sell,
                    dealer_net=dealer_net,
                    total_net=total_net,
                    source_timestamp=None,
                    fetched_at=now,
                    provenance=None,
                    metadata={},
                )
                records.append(flow)
            except Exception as exc:
                warnings.append(f"Row {i}: parse error {exc}, skipping")

        return records, warnings

    def parse_margin(
        self, raw_data: List[Dict[str, Any]], trade_date: str
    ) -> Tuple[List[TWSEMarginRecord], List[str]]:
        """Parse margin and short sales data."""
        records: List[TWSEMarginRecord] = []
        warnings: List[str] = []
        now = _now_iso()

        for i, row in enumerate(raw_data):
            if not isinstance(row, dict):
                warnings.append(f"Row {i}: not a dict, skipping")
                continue
            try:
                symbol = self._parse_str(
                    row.get("股票代號") or row.get("Code") or row.get("symbol") or row.get("證券代號")
                )
                if not symbol:
                    warnings.append(f"Row {i}: no symbol, skipping")
                    continue

                record = TWSEMarginRecord(
                    symbol=symbol,
                    trade_date=trade_date,
                    margin_buy=self._parse_number(row.get("融資買進")),
                    margin_sell=self._parse_number(row.get("融資賣出")),
                    margin_redemption=self._parse_number(row.get("融資現金償還")),
                    margin_balance=self._parse_number(row.get("融資餘額")),
                    short_sell=self._parse_number(row.get("融券賣出")),
                    short_cover=self._parse_number(row.get("融券買進")),
                    short_balance=self._parse_number(row.get("融券餘額")),
                    source_timestamp=None,
                    fetched_at=now,
                    provenance=None,
                    metadata={},
                )
                records.append(record)
            except Exception as exc:
                warnings.append(f"Row {i}: parse error {exc}, skipping")

        return records, warnings

    def parse_market_summary(
        self, raw_data: List[Dict[str, Any]]
    ) -> Tuple[List[TWSEMarketSummary], List[str]]:
        """Parse market summary data."""
        records: List[TWSEMarketSummary] = []
        warnings: List[str] = []
        now = _now_iso()

        for i, row in enumerate(raw_data):
            if not isinstance(row, dict):
                warnings.append(f"Row {i}: not a dict, skipping")
                continue
            try:
                date_raw = row.get("date") or row.get("Date") or row.get("日期")
                if not date_raw:
                    warnings.append(f"Row {i}: no date, skipping")
                    continue
                trade_date = self.parse_roc_date(str(date_raw)) or str(date_raw)

                summary = TWSEMarketSummary(
                    trade_date=trade_date,
                    market="TWSE",
                    trading_value=self._parse_str(row.get("TradeValue") or row.get("成交金額")),
                    trading_volume=self._parse_str(row.get("TradeVolume") or row.get("成交股數")),
                    transaction_count=self._parse_str(row.get("Transaction") or row.get("成交筆數")),
                    index_close=self._parse_str(row.get("TAIEX") or row.get("加權指數")),
                    index_change=self._parse_str(row.get("Change") or row.get("漲跌")),
                    source_timestamp=None,
                    fetched_at=now,
                    provenance=None,
                    metadata={},
                )
                records.append(summary)
            except Exception as exc:
                warnings.append(f"Row {i}: parse error {exc}, skipping")

        return records, warnings

    def parse_index(
        self, raw_data: List[Dict[str, Any]]
    ) -> Tuple[List[TWSEIndexRecord], List[str]]:
        """Parse TAIEX or sub-index data."""
        records: List[TWSEIndexRecord] = []
        warnings: List[str] = []
        now = _now_iso()

        for i, row in enumerate(raw_data):
            if not isinstance(row, dict):
                warnings.append(f"Row {i}: not a dict, skipping")
                continue
            try:
                date_raw = row.get("Date") or row.get("date") or row.get("日期")
                if not date_raw:
                    warnings.append(f"Row {i}: no date, skipping")
                    continue
                trade_date = self.parse_roc_date(str(date_raw)) or str(date_raw)

                record = TWSEIndexRecord(
                    index_code="TAIEX",
                    index_name="Taiwan Capitalization Weighted Stock Index",
                    trade_date=trade_date,
                    open=self._parse_str(row.get("Open") or row.get("開盤")),
                    high=self._parse_str(row.get("High") or row.get("最高")),
                    low=self._parse_str(row.get("Low") or row.get("最低")),
                    close=self._parse_str(row.get("Close") or row.get("收盤")),
                    change=self._parse_str(row.get("Change") or row.get("漲跌")),
                    source_timestamp=None,
                    fetched_at=now,
                    provenance=None,
                    metadata={},
                )
                records.append(record)
            except Exception as exc:
                warnings.append(f"Row {i}: parse error {exc}, skipping")

        return records, warnings

    def parse_corporate_actions(
        self, raw_data: List[Dict[str, Any]]
    ) -> Tuple[List[TWSECorporateActionPreview], List[str]]:
        """Parse corporate action data."""
        records: List[TWSECorporateActionPreview] = []
        warnings: List[str] = []
        now = _now_iso()

        for i, row in enumerate(raw_data):
            if not isinstance(row, dict):
                warnings.append(f"Row {i}: not a dict, skipping")
                continue
            try:
                symbol = self._parse_str(
                    row.get("symbol") or row.get("Code") or row.get("證券代號")
                )
                if not symbol:
                    warnings.append(f"Row {i}: no symbol, skipping")
                    continue

                action = TWSECorporateActionPreview(
                    symbol=symbol,
                    event_type=str(row.get("event_type") or row.get("type") or "UNKNOWN"),
                    announcement_date=self._parse_str(row.get("announcement_date")),
                    effective_date=self._parse_str(
                        row.get("effective_date") or row.get("ExRightsDate") or row.get("ExDividendDate")
                    ),
                    details=self._parse_str(row.get("details") or row.get("備註")),
                    status=self._parse_str(row.get("status") or row.get("Status")),
                    source_timestamp=None,
                    fetched_at=now,
                    provenance=None,
                    metadata={},
                )
                records.append(action)
            except Exception as exc:
                warnings.append(f"Row {i}: parse error {exc}, skipping")

        return records, warnings
