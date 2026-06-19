"""
universe/importer_v131.py — Universe metadata importer for v1.3.1.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Default: dry-run. No destructive replace. No deleting existing universes.
[!] No auto-activating all stocks after import. No auto-download. No network.
[!] Test fixtures cannot be accepted by Real mode as official market master.
[!] Unrecognized security type -> UNKNOWN. Market conflict -> BLOCKED. Not Investment Advice.
"""
from __future__ import annotations

import csv
import json
import logging
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from universe.models import SecurityType, UniverseMarket, UniverseTier, ListingStatus
from universe.symbol_normalizer import SymbolNormalizer

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS             = True
BROKER_DISABLED            = True
PRODUCTION_TRADING_BLOCKED = True
DRY_RUN_DEFAULT            = True  # Default: dry-run only

_SUPPORTED_FORMATS = {"csv", "json"}
_normalizer = SymbolNormalizer()

# Supported import fields
_SUPPORTED_FIELDS = {
    "symbol", "name", "market", "exchange", "industry", "security_type",
    "listing_status", "listing_date", "tier", "enabled", "tags",
}


@dataclass
class ImportRow:
    symbol: str = ""
    name: str = ""
    market: str = ""
    exchange: str = ""
    industry: str = ""
    security_type: str = SecurityType.UNKNOWN.value
    listing_status: str = ListingStatus.UNKNOWN.value
    listing_date: str = ""
    tier: str = UniverseTier.EXTENDED.value
    enabled: bool = True
    tags: List[str] = field(default_factory=list)
    row_index: int = 0
    raw: dict = field(default_factory=dict)


@dataclass
class ImportPreviewResult:
    path: str = ""
    format: str = ""
    row_count: int = 0
    detected_fields: List[str] = field(default_factory=list)
    missing_required: List[str] = field(default_factory=list)
    sample_rows: List[dict] = field(default_factory=list)
    ok: bool = False
    error: str = ""
    note: str = "TEST_FIXTURE — NOT REAL_MARKET_MASTER. Research Only."


@dataclass
class ImportValidationResult:
    path: str = ""
    format: str = ""
    valid_rows: int = 0
    invalid_rows: int = 0
    duplicate_symbols: List[str] = field(default_factory=list)
    market_conflicts: List[str] = field(default_factory=list)
    unknown_security_types: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    ok: bool = False
    note: str = "TEST_FIXTURE — NOT REAL_MARKET_MASTER. Research Only."


@dataclass
class ImportDryRunResult:
    path: str = ""
    format: str = ""
    would_add: List[str] = field(default_factory=list)
    would_skip: List[str] = field(default_factory=list)
    would_block: List[dict] = field(default_factory=list)
    duplicate_detected: List[str] = field(default_factory=list)
    ok: bool = False
    note: str = "DRY_RUN — no changes made. TEST_FIXTURE — NOT REAL_MARKET_MASTER."


@dataclass
class ImportResult:
    path: str = ""
    format: str = ""
    added: List[str] = field(default_factory=list)
    skipped: List[str] = field(default_factory=list)
    blocked: List[dict] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    ok: bool = False
    note: str = "TEST_FIXTURE — NOT REAL_MARKET_MASTER. Research Only. Not Investment Advice."


class UniverseImporter:
    """
    Local file importer for universe metadata (CSV, JSON).

    Rules:
    - Default: dry-run
    - No interactive Yes/No
    - No destructive replace
    - No deleting existing universes
    - No auto-activating all stocks after import
    - Unrecognized security type -> UNKNOWN
    - Market conflict -> BLOCKED
    - Invalid symbol -> not formally registered
    - Test fixtures cannot be accepted by Real mode as official market master
    - No auto-download, no network

    [!] Research Only. No Real Orders.
    """

    NO_REAL_ORDERS             = True
    BROKER_DISABLED            = True
    PRODUCTION_TRADING_BLOCKED = True
    DRY_RUN_DEFAULT            = True

    def preview(self, path: str, fmt: str = "csv") -> ImportPreviewResult:
        """Preview file structure without making any changes."""
        result = ImportPreviewResult(path=path, format=fmt)
        try:
            rows = self._read_file(path, fmt)
            result.row_count = len(rows)
            if rows:
                result.detected_fields = list(rows[0].raw.keys())
                result.sample_rows = [r.raw for r in rows[:3]]
            if "symbol" not in result.detected_fields:
                result.missing_required.append("symbol")
            result.ok = "symbol" in result.detected_fields
        except Exception as exc:
            result.error = str(exc)
            result.ok = False
        return result

    def validate(self, path: str, fmt: str = "csv") -> ImportValidationResult:
        """Validate file content without modifying registry."""
        result = ImportValidationResult(path=path, format=fmt)
        try:
            rows = self._read_file(path, fmt)
            seen_symbols: Dict[str, str] = {}  # symbol -> market
            for row in rows:
                if not row.symbol:
                    result.invalid_rows += 1
                    result.errors.append(f"Row {row.row_index}: missing symbol")
                    continue
                norm = _normalizer.normalize(row.symbol)
                if not norm.is_valid:
                    result.invalid_rows += 1
                    result.errors.append(
                        f"Row {row.row_index}: invalid symbol '{row.symbol}': {norm.warning}"
                    )
                    continue
                sym = norm.normalized_symbol
                mkt = row.market or norm.detected_market
                if sym in seen_symbols:
                    if seen_symbols[sym] != mkt and seen_symbols[sym] and mkt:
                        result.market_conflicts.append(
                            f"{sym}: seen as {seen_symbols[sym]} and {mkt}"
                        )
                    if sym not in result.duplicate_symbols:
                        result.duplicate_symbols.append(sym)
                else:
                    seen_symbols[sym] = mkt
                    result.valid_rows += 1
                if row.security_type not in {e.value for e in SecurityType}:
                    result.unknown_security_types.append(
                        f"{sym}: '{row.security_type}' -> mapped to UNKNOWN"
                    )
            result.ok = not result.market_conflicts and result.valid_rows > 0
        except Exception as exc:
            result.errors.append(str(exc))
            result.ok = False
        return result

    def dry_run(self, path: str, fmt: str = "csv") -> ImportDryRunResult:
        """
        Dry-run: show what would happen without making changes.
        [!] No changes made. DRY_RUN only.
        """
        result = ImportDryRunResult(path=path, format=fmt)
        try:
            rows = self._read_file(path, fmt)
            seen: Dict[str, str] = {}
            for row in rows:
                if not row.symbol:
                    result.would_skip.append(f"row_{row.row_index}_empty_symbol")
                    continue
                norm = _normalizer.normalize(row.symbol)
                if not norm.is_valid:
                    result.would_skip.append(row.symbol)
                    continue
                sym = norm.normalized_symbol
                mkt = row.market or norm.detected_market
                if sym in seen:
                    if seen[sym] != mkt and seen[sym] and mkt:
                        result.would_block.append({
                            "symbol": sym,
                            "reason": f"market conflict: {seen[sym]} vs {mkt}",
                        })
                        continue
                    result.duplicate_detected.append(sym)
                    result.would_skip.append(sym)
                    continue
                seen[sym] = mkt
                result.would_add.append(sym)
            result.ok = True
        except Exception as exc:
            result.ok = False
            result.would_block.append({"symbol": "?", "reason": str(exc)})
        return result

    def execute(self, path: str, fmt: str, registry) -> ImportResult:
        """
        Execute import into registry.
        [!] No destructive replace. No deleting existing. Not auto-activating all.
        [!] Test fixtures will be labeled as NOT REAL_MARKET_MASTER.
        """
        result = ImportResult(path=path, format=fmt)
        try:
            rows = self._read_file(path, fmt)
            seen: Dict[str, str] = {}
            for row in rows:
                if not row.symbol:
                    result.skipped.append(f"row_{row.row_index}_empty_symbol")
                    continue
                norm = _normalizer.normalize(row.symbol)
                if not norm.is_valid:
                    result.skipped.append(row.symbol)
                    result.errors.append(
                        f"Symbol '{row.symbol}' invalid: {norm.warning}"
                    )
                    continue
                sym = norm.normalized_symbol
                mkt = row.market or norm.detected_market
                if sym in seen:
                    if seen[sym] != mkt and seen[sym] and mkt:
                        result.blocked.append({
                            "symbol": sym,
                            "reason": f"market conflict: {seen[sym]} vs {mkt}",
                        })
                        continue
                    result.skipped.append(sym)
                    continue
                seen[sym] = mkt

                # Normalize security type
                sec_type = row.security_type
                if sec_type not in {e.value for e in SecurityType}:
                    sec_type = SecurityType.UNKNOWN.value

                symbol_data = {
                    "symbol": sym,
                    "stock_name": row.name,
                    "market": mkt,
                    "exchange": row.exchange,
                    "industry": row.industry,
                    "security_type": sec_type,
                    "listing_status": row.listing_status,
                    "listing_date": row.listing_date,
                    "tags": row.tags,
                    "source": "IMPORT_FILE",  # NOT REAL_MARKET_MASTER
                    "metadata": {
                        "note": "Imported from file — NOT REAL_MARKET_MASTER",
                        "import_path": os.path.basename(path),
                    },
                }
                ok, msg = registry.register_symbol(symbol_data)
                if ok:
                    result.added.append(sym)
                else:
                    result.blocked.append({"symbol": sym, "reason": msg})
            result.ok = True
        except Exception as exc:
            result.errors.append(str(exc))
            result.ok = False
        return result

    # ------------------------------------------------------------------
    # File reading
    # ------------------------------------------------------------------

    def _read_file(self, path: str, fmt: str) -> List[ImportRow]:
        """Read file into list of ImportRow. Supports CSV and JSON."""
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Import file not found: {path}")
        fmt = fmt.lower().strip()
        if fmt == "csv":
            return self._read_csv(path)
        elif fmt == "json":
            return self._read_json(path)
        else:
            raise ValueError(f"Unsupported format: {fmt}. Use 'csv' or 'json'.")

    def _read_csv(self, path: str) -> List[ImportRow]:
        rows = []
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, raw_row in enumerate(reader, start=1):
                rows.append(self._parse_row(raw_row, i))
        return rows

    def _read_json(self, path: str) -> List[ImportRow]:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            # Support {"symbols": [...]} format
            data = data.get("symbols", data.get("items", [data]))
        rows = []
        for i, raw_row in enumerate(data, start=1):
            rows.append(self._parse_row(raw_row, i))
        return rows

    def _parse_row(self, raw: dict, row_index: int) -> ImportRow:
        tags_raw = raw.get("tags", "")
        if isinstance(tags_raw, str):
            tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
        elif isinstance(tags_raw, list):
            tags = [str(t) for t in tags_raw]
        else:
            tags = []
        enabled_raw = raw.get("enabled", "1")
        enabled = str(enabled_raw).lower() not in ("0", "false", "no")
        return ImportRow(
            symbol=str(raw.get("symbol", "")).strip(),
            name=str(raw.get("name", "")).strip(),
            market=str(raw.get("market", "")).strip(),
            exchange=str(raw.get("exchange", "")).strip(),
            industry=str(raw.get("industry", "")).strip(),
            security_type=str(raw.get("security_type", SecurityType.UNKNOWN.value)).strip(),
            listing_status=str(raw.get("listing_status", ListingStatus.UNKNOWN.value)).strip(),
            listing_date=str(raw.get("listing_date", "")).strip(),
            tier=str(raw.get("tier", UniverseTier.EXTENDED.value)).strip(),
            enabled=enabled,
            tags=tags,
            row_index=row_index,
            raw=dict(raw),
        )
