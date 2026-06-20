"""
data/providers/tpex/parser_v141.py — TPEx data parser v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TPEx Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
[!] Mainboard Common Stocks Only By Default.
"""
from __future__ import annotations

import datetime
import re
from typing import Any, Dict, List, Optional, Tuple

from data.providers.tpex.models_v141 import (
    TPExCorporateActionPreview,
    TPExDailyBar,
    TPExIndexRecord,
    TPExInstitutionalFlow,
    TPExMarginRecord,
    TPExMarketSummary,
    TPExSecurity,
    TPExSuspensionRecord,
    TPExValuationRecord,
)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_MISSING_MARKERS = {"--", "---", "-", "N/A", "", "暫停交易", "除權", "除息", "除權息", "NA", "N/A"}
_PROVIDER_ID = "tpex_official"


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class TPExParser:
    """
    Parser for TPEx OpenAPI responses.

    Handles:
    - Chinese field names → standard field mapping
    - ROC date (民國年 + 1911) → CE date
    - ISO dates
    - Comma-separated numbers
    - Percentages, +/- signs
    - "--", "---", "-", "N/A", empty → None
    - No-trade, suspended, resumed, ex-rights, ex-dividend markers
    - New OTC listing, delisted markers
    - ETF, ETN, warrant, emerging, pioneer markers
    - Duplicate row detection
    - Malformed row isolation
    - Unknown fields: forward-compatible (ignore gracefully)
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
        # Strip % suffix for raw number (caller should use _parse_percentage for %)
        if s.endswith("%"):
            s = s[:-1]
        try:
            return float(s)
        except (ValueError, TypeError):
            return None

    def _parse_percentage(self, s: Any) -> Optional[float]:
        """Parse a percentage string. '5.23%' -> 5.23. Returns None for missing."""
        if s is None:
            return None
        s = str(s).strip()
        if s in _MISSING_MARKERS:
            return None
        if s.endswith("%"):
            s = s[:-1]
        # Remove commas
        s = s.replace(",", "")
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
        """Convert ROC date (民國年) to CE date (YYYY-MM-DD). '1130101' -> '2024-01-01'."""
        if roc_str is None:
            return None
        s = str(roc_str).strip()
        # Format "1130101" (YYYMMDD in ROC)
        m = re.match(r"^(\d{3})(\d{2})(\d{2})$", s)
        if m:
            roc_year = int(m.group(1))
            month = int(m.group(2))
            day = int(m.group(3))
            ce_year = roc_year + 1911
            return f"{ce_year:04d}-{month:02d}-{day:02d}"
        # Format "113/01/01"
        m = re.match(r"^(\d{2,3})/(\d{2})/(\d{2})$", s)
        if m:
            roc_year = int(m.group(1))
            month = int(m.group(2))
            day = int(m.group(3))
            ce_year = roc_year + 1911
            return f"{ce_year:04d}-{month:02d}-{day:02d}"
        # ISO format
        m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", s)
        if m:
            return s
        # 8-digit YYYYMMDD
        m = re.match(r"^(\d{4})(\d{2})(\d{2})$", s)
        if m:
            year = int(m.group(1))
            if year < 1912:
                year += 1911
            return f"{year:04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
        return None

    def _classify_security_type(self, raw_type: Optional[str], symbol: str) -> str:
        """Classify security type from raw string."""
        if not raw_type:
            return "UNKNOWN"
        s = str(raw_type).upper().strip()
        if "ETN" in s:
            return "ETN"
        if "ETF" in s:
            return "ETF"
        if "REIT" in s or "REITs" in raw_type:
            return "REIT"
        if "WARRANT" in s or "認購" in raw_type or "認售" in raw_type:
            return "WARRANT"
        if "TDR" in s:
            return "TDR"
        if "EMERGING" in s or "興櫃" in raw_type:
            return "EMERGING_STOCK"
        if "PIONEER" in s or "先驅" in raw_type:
            return "PIONEER_STOCK"
        if "GO_INCUBATION" in s or "創櫃" in raw_type:
            return "GO_INCUBATION"
        if "CONVERTIBLE" in s or "可轉換" in raw_type:
            return "CONVERTIBLE_BOND"
        if "BOND" in s or "債" in raw_type:
            return "BOND"
        if "FOREIGN" in s or "外國" in raw_type:
            return "FOREIGN_STOCK"
        if "COMMON" in s or "普通股" in raw_type:
            return "COMMON_STOCK"
        return "UNKNOWN"

    def _classify_board(self, raw_board: Optional[str], security_type: str) -> str:
        """Classify board from raw string or security type."""
        if raw_board:
            s = str(raw_board).upper()
            if "EMERGING" in s or "興櫃" in raw_board:
                return "EMERGING"
            if "PIONEER" in s or "先驅" in raw_board:
                return "PIONEER"
            if "INCUBATION" in s or "創櫃" in raw_board:
                return "GO_INCUBATION"
            if "MAINBOARD" in s or "上櫃" in raw_board:
                return "MAINBOARD"
        # Infer from security type
        if security_type in ("EMERGING_STOCK",):
            return "EMERGING"
        if security_type in ("PIONEER_STOCK",):
            return "PIONEER"
        if security_type in ("GO_INCUBATION",):
            return "GO_INCUBATION"
        return "MAINBOARD"

    def parse_security_master(
        self, raw_data: List[Dict[str, Any]]
    ) -> Tuple[List[TPExSecurity], List[str]]:
        """Parse security master data."""
        records: List[TPExSecurity] = []
        warnings: List[str] = []
        seen_symbols: set = set()
        now = _now_iso()

        for i, row in enumerate(raw_data):
            if not isinstance(row, dict):
                warnings.append(f"Row {i}: not a dict, skipping")
                continue
            try:
                symbol = self._parse_str(
                    row.get("SecuritiesCompanyCode") or row.get("Code")
                    or row.get("公司代號") or row.get("證券代號")
                )
                if not symbol:
                    warnings.append(f"Row {i}: no symbol, skipping")
                    continue
                if symbol in seen_symbols:
                    warnings.append(f"Row {i}: duplicate symbol {symbol}, keeping first")
                    continue
                seen_symbols.add(symbol)

                name = self._parse_str(
                    row.get("CompanyName") or row.get("Name")
                    or row.get("公司簡稱") or row.get("證券名稱")
                )
                raw_type = self._parse_str(
                    row.get("SecurityType") or row.get("security_type")
                    or row.get("類別") or row.get("Type")
                )
                security_type = self._classify_security_type(raw_type, symbol)
                raw_board = self._parse_str(row.get("Board") or row.get("board"))
                board = self._classify_board(raw_board, security_type)

                is_common = (security_type == "COMMON_STOCK" and board == "MAINBOARD")
                universe_eligible = is_common

                industry_code = self._parse_str(
                    row.get("Industry") or row.get("IndustryCode") or row.get("產業別")
                )
                listing_date_raw = (
                    row.get("ListingDate") or row.get("上櫃日期") or row.get("listing_date")
                )
                listing_date = self.parse_roc_date(listing_date_raw) if listing_date_raw else None
                isin = self._parse_str(row.get("ISIN") or row.get("ISIN碼"))

                sec = TPExSecurity(
                    symbol=symbol,
                    name=name,
                    market="TPEx",
                    board=board,
                    security_type=security_type,
                    industry_code=industry_code,
                    industry_name=None,
                    listing_date=listing_date,
                    isin=isin,
                    currency="TWD",
                    status="LISTED",
                    is_common_stock=is_common,
                    universe_eligible=universe_eligible,
                    source_timestamp=None,
                    fetched_at=now,
                    provider_id=_PROVIDER_ID,
                    provenance=None,
                    warnings=[],
                    metadata={},
                )
                records.append(sec)
            except Exception as exc:
                warnings.append(f"Row {i}: parse error {exc}, skipping")

        return records, warnings

    def parse_daily_ohlcv(
        self, raw_data: List[Dict[str, Any]], trade_date: str
    ) -> Tuple[List[TPExDailyBar], List[str]]:
        """Parse daily OHLCV data."""
        records: List[TPExDailyBar] = []
        warnings: List[str] = []
        seen_symbols: set = set()
        now = _now_iso()

        for i, row in enumerate(raw_data):
            if not isinstance(row, dict):
                warnings.append(f"Row {i}: not a dict, skipping")
                continue
            try:
                symbol = self._parse_str(
                    row.get("SecuritiesCompanyCode") or row.get("Code")
                    or row.get("證券代號") or row.get("symbol")
                )
                if not symbol:
                    warnings.append(f"Row {i}: no symbol, skipping")
                    continue
                if symbol in seen_symbols:
                    warnings.append(f"Row {i}: duplicate symbol {symbol}, keeping first")
                    continue
                seen_symbols.add(symbol)

                open_p = self._parse_str(row.get("Open") or row.get("開盤價"))
                high_p = self._parse_str(row.get("High") or row.get("最高價"))
                low_p = self._parse_str(row.get("Low") or row.get("最低價"))
                close_p = self._parse_str(row.get("Close") or row.get("收盤價"))
                prev_close = self._parse_str(row.get("PreviousClose") or row.get("昨收"))
                change = self._parse_str(row.get("Change") or row.get("漲跌"))
                change_pct = self._parse_str(row.get("ChangePercent") or row.get("漲跌幅"))
                volume_raw = self._parse_number(row.get("Volume") or row.get("成交股數"))
                turnover_raw = self._parse_number(row.get("Turnover") or row.get("成交金額"))
                tx_raw = self._parse_number(row.get("Transaction") or row.get("成交筆數"))
                bid = self._parse_str(row.get("Bid") or row.get("買進"))
                ask = self._parse_str(row.get("Ask") or row.get("賣出"))

                # OHLC validation: reject bar if high < low
                if high_p is not None and low_p is not None:
                    try:
                        h = float(high_p)
                        lv = float(low_p)
                        if h < lv:
                            warnings.append(
                                f"Symbol {symbol}: high ({high_p}) < low ({low_p}), rejecting bar"
                            )
                            continue
                    except (ValueError, TypeError):
                        pass

                # Reject bar with volume > 0 and open or close <= 0
                if volume_raw is not None and volume_raw > 0:
                    for price_label, price_str in [("open", open_p), ("close", close_p)]:
                        if price_str is not None:
                            try:
                                if float(price_str) <= 0:
                                    warnings.append(
                                        f"Symbol {symbol}: {price_label} ({price_str}) <= 0 with volume > 0, rejecting bar"
                                    )
                                    break
                            except (ValueError, TypeError):
                                pass
                    else:
                        bar = TPExDailyBar(
                            symbol=symbol,
                            trade_date=trade_date,
                            open=open_p,
                            high=high_p,
                            low=low_p,
                            close=close_p,
                            previous_close=prev_close,
                            price_change=change,
                            price_change_percent=change_pct,
                            volume=volume_raw,
                            turnover=turnover_raw,
                            transaction_count=tx_raw,
                            bid=bid,
                            ask=ask,
                            adjusted_status="NOT_ADJUSTED",
                            trading_status=None,
                            source_timestamp=None,
                            fetched_at=now,
                            provider_id=_PROVIDER_ID,
                            provenance=None,
                            warnings=[],
                            metadata={},
                        )
                        records.append(bar)
                        continue
                else:
                    bar = TPExDailyBar(
                        symbol=symbol,
                        trade_date=trade_date,
                        open=open_p,
                        high=high_p,
                        low=low_p,
                        close=close_p,
                        previous_close=prev_close,
                        price_change=change,
                        price_change_percent=change_pct,
                        volume=volume_raw,
                        turnover=turnover_raw,
                        transaction_count=tx_raw,
                        bid=bid,
                        ask=ask,
                        adjusted_status="NOT_ADJUSTED",
                        trading_status=None,
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
    ) -> Tuple[List[TPExInstitutionalFlow], List[str]]:
        """Parse institutional investor flow data (dealer proprietary and hedge are separate)."""
        records: List[TPExInstitutionalFlow] = []
        warnings: List[str] = []
        now = _now_iso()

        for i, row in enumerate(raw_data):
            if not isinstance(row, dict):
                warnings.append(f"Row {i}: not a dict, skipping")
                continue
            try:
                symbol = self._parse_str(
                    row.get("SecuritiesCompanyCode") or row.get("Code")
                    or row.get("證券代號") or row.get("symbol")
                )
                if not symbol:
                    warnings.append(f"Row {i}: no symbol, skipping")
                    continue

                foreign_buy = self._parse_number(
                    row.get("ForeignInvestorBuy") or row.get("外資買進")
                )
                foreign_sell = self._parse_number(
                    row.get("ForeignInvestorSell") or row.get("外資賣出")
                )
                foreign_net = self._parse_number(
                    row.get("ForeignInvestorNet") or row.get("外資買賣超")
                )
                trust_buy = self._parse_number(
                    row.get("InvestmentTrustBuy") or row.get("投信買進")
                )
                trust_sell = self._parse_number(
                    row.get("InvestmentTrustSell") or row.get("投信賣出")
                )
                trust_net = self._parse_number(
                    row.get("InvestmentTrustNet") or row.get("投信買賣超")
                )
                # Dealer proprietary and hedge are SEPARATE (TPEx provides split)
                dealer_prop_buy = self._parse_number(
                    row.get("DealerProprietaryBuy") or row.get("自營商自行買進")
                )
                dealer_prop_sell = self._parse_number(
                    row.get("DealerProprietarySell") or row.get("自營商自行賣出")
                )
                dealer_prop_net = self._parse_number(
                    row.get("DealerProprietaryNet") or row.get("自營商自行買賣超")
                )
                dealer_hedge_buy = self._parse_number(
                    row.get("DealerHedgeBuy") or row.get("自營商避險買進")
                )
                dealer_hedge_sell = self._parse_number(
                    row.get("DealerHedgeSell") or row.get("自營商避險賣出")
                )
                dealer_hedge_net = self._parse_number(
                    row.get("DealerHedgeNet") or row.get("自營商避險買賣超")
                )
                dealer_total_net = self._parse_number(
                    row.get("DealerTotalNet") or row.get("自營商合計買賣超")
                )
                total_net = self._parse_number(
                    row.get("TotalNet") or row.get("三大法人買賣超")
                )

                flow = TPExInstitutionalFlow(
                    symbol=symbol,
                    trade_date=trade_date,
                    foreign_buy=foreign_buy,
                    foreign_sell=foreign_sell,
                    foreign_net=foreign_net,
                    investment_trust_buy=trust_buy,
                    investment_trust_sell=trust_sell,
                    investment_trust_net=trust_net,
                    dealer_proprietary_buy=dealer_prop_buy,
                    dealer_proprietary_sell=dealer_prop_sell,
                    dealer_proprietary_net=dealer_prop_net,
                    dealer_hedge_buy=dealer_hedge_buy,
                    dealer_hedge_sell=dealer_hedge_sell,
                    dealer_hedge_net=dealer_hedge_net,
                    dealer_total_net=dealer_total_net,
                    total_net=total_net,
                    source_timestamp=None,
                    published_at=None,
                    fetched_at=now,
                    provenance=None,
                    warnings=[],
                    metadata={},
                )
                records.append(flow)
            except Exception as exc:
                warnings.append(f"Row {i}: parse error {exc}, skipping")

        return records, warnings

    def parse_margin(
        self, raw_data: List[Dict[str, Any]], trade_date: str
    ) -> Tuple[List[TPExMarginRecord], List[str]]:
        """Parse margin and short sales data."""
        records: List[TPExMarginRecord] = []
        warnings: List[str] = []
        now = _now_iso()

        for i, row in enumerate(raw_data):
            if not isinstance(row, dict):
                warnings.append(f"Row {i}: not a dict, skipping")
                continue
            try:
                symbol = self._parse_str(
                    row.get("SecuritiesCompanyCode") or row.get("Code")
                    or row.get("股票代號") or row.get("symbol") or row.get("證券代號")
                )
                if not symbol:
                    warnings.append(f"Row {i}: no symbol, skipping")
                    continue

                record = TPExMarginRecord(
                    symbol=symbol,
                    trade_date=trade_date,
                    margin_buy=self._parse_number(row.get("MarginBuy") or row.get("融資買進")),
                    margin_sell=self._parse_number(row.get("MarginSell") or row.get("融資賣出")),
                    cash_redemption=self._parse_number(row.get("CashRedemption") or row.get("融資現金償還")),
                    margin_previous_balance=self._parse_number(row.get("MarginPreviousBalance") or row.get("融資前日餘額")),
                    margin_balance=self._parse_number(row.get("MarginBalance") or row.get("融資餘額")),
                    margin_limit=self._parse_number(row.get("MarginLimit") or row.get("融資限額")),
                    short_sell=self._parse_number(row.get("ShortSell") or row.get("融券賣出")),
                    short_cover=self._parse_number(row.get("ShortCover") or row.get("融券買進")),
                    stock_redemption=self._parse_number(row.get("StockRedemption") or row.get("融券現券償還")),
                    short_previous_balance=self._parse_number(row.get("ShortPreviousBalance") or row.get("融券前日餘額")),
                    short_balance=self._parse_number(row.get("ShortBalance") or row.get("融券餘額")),
                    short_limit=self._parse_number(row.get("ShortLimit") or row.get("融券限額")),
                    source_timestamp=None,
                    fetched_at=now,
                    provenance=None,
                    warnings=[],
                    metadata={},
                )
                records.append(record)
            except Exception as exc:
                warnings.append(f"Row {i}: parse error {exc}, skipping")

        return records, warnings

    def parse_market_summary(
        self, raw_data: List[Dict[str, Any]]
    ) -> Tuple[List[TPExMarketSummary], List[str]]:
        """Parse market summary data."""
        records: List[TPExMarketSummary] = []
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

                summary = TPExMarketSummary(
                    trade_date=trade_date,
                    market="TPEx",
                    board="MAINBOARD",
                    trading_value=self._parse_number(row.get("TradingValue") or row.get("成交金額")),
                    trading_volume=self._parse_number(row.get("TradingVolume") or row.get("成交股數")),
                    transaction_count=self._parse_number(row.get("Transaction") or row.get("成交筆數")),
                    index_close=self._parse_str(row.get("Index") or row.get("指數")),
                    index_change=self._parse_str(row.get("Change") or row.get("漲跌")),
                    advancing=self._parse_number(row.get("Advancing") or row.get("上漲")),
                    declining=self._parse_number(row.get("Declining") or row.get("下跌")),
                    unchanged=self._parse_number(row.get("Unchanged") or row.get("不變")),
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
    ) -> Tuple[List[TPExIndexRecord], List[str]]:
        """Parse TPEx composite index data."""
        records: List[TPExIndexRecord] = []
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

                record = TPExIndexRecord(
                    index_code=str(row.get("IndexCode") or row.get("index_code") or "TPEX"),
                    index_name=self._parse_str(row.get("IndexName") or row.get("index_name")),
                    trade_date=trade_date,
                    open=self._parse_str(row.get("Open") or row.get("開盤")),
                    high=self._parse_str(row.get("High") or row.get("最高")),
                    low=self._parse_str(row.get("Low") or row.get("最低")),
                    close=self._parse_str(row.get("Close") or row.get("收盤")),
                    change=self._parse_str(row.get("Change") or row.get("漲跌")),
                    change_percent=self._parse_str(row.get("ChangePercent") or row.get("漲跌幅")),
                    source_timestamp=None,
                    fetched_at=now,
                    provenance=None,
                    metadata={},
                )
                records.append(record)
            except Exception as exc:
                warnings.append(f"Row {i}: parse error {exc}, skipping")

        return records, warnings

    def parse_suspensions(
        self, raw_data: List[Dict[str, Any]]
    ) -> Tuple[List[TPExSuspensionRecord], List[str]]:
        """Parse suspension/resumption data."""
        records: List[TPExSuspensionRecord] = []
        warnings: List[str] = []
        now = _now_iso()

        for i, row in enumerate(raw_data):
            if not isinstance(row, dict):
                warnings.append(f"Row {i}: not a dict, skipping")
                continue
            try:
                symbol = self._parse_str(
                    row.get("SecuritiesCompanyCode") or row.get("Code")
                    or row.get("symbol") or row.get("證券代號")
                )
                if not symbol:
                    warnings.append(f"Row {i}: no symbol, skipping")
                    continue

                record = TPExSuspensionRecord(
                    symbol=symbol,
                    name=self._parse_str(row.get("CompanyName") or row.get("name")),
                    announcement_date=self._parse_str(row.get("AnnouncementDate") or row.get("announcement_date")),
                    effective_date=self._parse_str(row.get("EffectiveDate") or row.get("effective_date")),
                    resume_date=self._parse_str(row.get("ResumeDate") or row.get("resume_date")),
                    action=self._parse_str(row.get("Action") or row.get("action")),
                    reason=self._parse_str(row.get("Reason") or row.get("reason") or row.get("原因")),
                    status=self._parse_str(row.get("Status") or row.get("status")),
                    source_timestamp=None,
                    fetched_at=now,
                    provenance=None,
                    metadata={},
                )
                records.append(record)
            except Exception as exc:
                warnings.append(f"Row {i}: parse error {exc}, skipping")

        return records, warnings

    def parse_valuation(
        self, raw_data: List[Dict[str, Any]], trade_date: str
    ) -> Tuple[List[TPExValuationRecord], List[str]]:
        """Parse valuation metrics. '--' -> None (never 0). Negative PE is preserved."""
        records: List[TPExValuationRecord] = []
        warnings: List[str] = []
        now = _now_iso()

        for i, row in enumerate(raw_data):
            if not isinstance(row, dict):
                warnings.append(f"Row {i}: not a dict, skipping")
                continue
            try:
                symbol = self._parse_str(
                    row.get("SecuritiesCompanyCode") or row.get("Code")
                    or row.get("symbol") or row.get("證券代號")
                )
                if not symbol:
                    warnings.append(f"Row {i}: no symbol, skipping")
                    continue

                pe_raw = row.get("PEratio") or row.get("本益比")
                pb_raw = row.get("PBratio") or row.get("股價淨值比")
                dy_raw = row.get("DividendYield") or row.get("殖利率")
                cap_raw = row.get("MarketCap") or row.get("市值")

                record = TPExValuationRecord(
                    symbol=symbol,
                    trade_date=trade_date,
                    pe_ratio=self._parse_number(pe_raw),  # negative preserved, '--' -> None
                    dividend_yield=self._parse_percentage(dy_raw),
                    price_to_book=self._parse_number(pb_raw),
                    market_cap=self._parse_number(cap_raw),
                    source_timestamp=None,
                    fetched_at=now,
                    provenance=None,
                    warnings=[],
                    metadata={},
                )
                records.append(record)
            except Exception as exc:
                warnings.append(f"Row {i}: parse error {exc}, skipping")

        return records, warnings
