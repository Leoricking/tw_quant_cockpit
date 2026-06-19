"""
data/providers/local_file_provider_adapter.py — Local file provider adapter v1.3.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Never invents symbols, dates, or OHLCV. Never accepts TEST_FIXTURE in Real mode.
[!] NaN is NOT converted to 0. Missing institutional data is NOT set to 0.
"""
from __future__ import annotations

import csv
import logging
import math
import os
from typing import Any, List

from data.providers.real_data_provider_models import (
    CacheStatus,
    ProviderCapability,
    ProviderErrorCategory,
    ProviderMetadata,
    ProviderRequest,
    ProviderResponse,
    ProviderStatus,
    ProviderType,
    _now_iso,
)
from data.providers.real_data_provider_adapter import RealDataProviderAdapter

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

# ---------------------------------------------------------------------------
# Supported capabilities
# ---------------------------------------------------------------------------
_LOCAL_FILE_CAPABILITIES = [
    ProviderCapability.DAILY_OHLCV,
    ProviderCapability.MONTHLY_REVENUE,
    ProviderCapability.INSTITUTIONAL,
    ProviderCapability.MARGIN,
]

# Required columns for DAILY_OHLCV
_OHLCV_REQUIRED_COLUMNS = {"date", "open", "high", "low", "close", "volume"}


def _is_fixture_path(path: str) -> bool:
    """Returns True if path contains fixture or test_fixture markers."""
    lowered = path.lower().replace("\\", "/")
    return "fixture" in lowered or "test_fixture" in lowered


class LocalFileProviderAdapter(RealDataProviderAdapter):
    """
    Adapter that reads data from local CSV files.

    [!] NaN is NOT converted to 0.
    [!] Missing institutional data is NOT set to 0.
    [!] Fixture paths blocked in REAL mode.
    [!] No synthetic data generation.
    """

    def __init__(self, base_dir: str = "", data_mode: str = "REAL") -> None:
        self._base_dir = base_dir
        self._data_mode = data_mode
        self._provider_id = "local_file"
        self._provider_type = ProviderType.LOCAL_FILE

    # ------------------------------------------------------------------
    # Abstract method implementations
    # ------------------------------------------------------------------

    def get_metadata(self) -> ProviderMetadata:
        is_available = bool(self._base_dir) and os.path.isdir(self._base_dir)
        return ProviderMetadata(
            provider_id=self._provider_id,
            provider_name="Local File Provider",
            provider_type=self._provider_type,
            description="Reads OHLCV and other data from local CSV files.",
            enabled=is_available,
            priority=50,
            capabilities=list(_LOCAL_FILE_CAPABILITIES),
            markets=[],
            security_types=[],
            requires_auth=False,
            supports_batch=False,
            supports_incremental=False,
            supports_historical=True,
            supports_intraday=False,
            terms_note="Local files only. No external data.",
            source_url_type="LOCAL_PATH",
            data_mode=self._data_mode,
        )

    def get_status(self) -> str:
        if not self._base_dir:
            return ProviderStatus.MISCONFIGURED
        if not os.path.isdir(self._base_dir):
            return ProviderStatus.UNAVAILABLE
        if self._data_mode == "REAL" and _is_fixture_path(self._base_dir):
            return ProviderStatus.BLOCKED
        try:
            os.listdir(self._base_dir)
        except PermissionError:
            return ProviderStatus.UNAVAILABLE
        return ProviderStatus.AVAILABLE

    def get_capabilities(self) -> List[str]:
        return list(_LOCAL_FILE_CAPABILITIES)

    def supports(self, capability: str, market: str = "") -> bool:
        return capability in _LOCAL_FILE_CAPABILITIES

    def validate_request(self, request: ProviderRequest) -> List[str]:
        errors = []
        if not request.capability:
            errors.append("capability is required.")
        if request.capability not in _LOCAL_FILE_CAPABILITIES:
            errors.append(f"Capability '{request.capability}' not supported by local_file provider.")
        if not request.symbols:
            errors.append("At least one symbol is required.")
        return errors

    def fetch(self, request: ProviderRequest) -> ProviderResponse:
        # Block fixture paths in REAL mode
        if self._data_mode == "REAL" and _is_fixture_path(self._base_dir):
            return ProviderResponse(
                request_id=request.request_id,
                provider_id=self._provider_id,
                capability=request.capability,
                status=ProviderStatus.BLOCKED,
                data_mode=self._data_mode,
                errors=["Fixture path detected. Blocked in REAL data_mode."],
                metadata={"error_category": ProviderErrorCategory.BLOCKED},
            )

        # Validate
        errs = self.validate_request(request)
        if errs:
            return ProviderResponse(
                request_id=request.request_id,
                provider_id=self._provider_id,
                capability=request.capability,
                status=ProviderStatus.UNAVAILABLE,
                data_mode=self._data_mode,
                errors=errs,
                metadata={"error_category": ProviderErrorCategory.INVALID_REQUEST},
            )

        cap = request.capability
        if cap == ProviderCapability.DAILY_OHLCV:
            return self._fetch_daily_ohlcv(request)
        elif cap in (ProviderCapability.MONTHLY_REVENUE, ProviderCapability.INSTITUTIONAL, ProviderCapability.MARGIN):
            return self._fetch_unsupported_graceful(request, cap)
        else:
            return ProviderResponse(
                request_id=request.request_id,
                provider_id=self._provider_id,
                capability=cap,
                status=ProviderStatus.UNAVAILABLE,
                data_mode=self._data_mode,
                errors=[f"Capability '{cap}' not implemented in local_file adapter."],
                metadata={"error_category": ProviderErrorCategory.UNSUPPORTED_CAPABILITY},
            )

    def health_check(self) -> dict:
        status = self.get_status()
        note = ""
        if not self._base_dir:
            note = "base_dir not configured."
        elif not os.path.isdir(self._base_dir):
            note = f"base_dir '{self._base_dir}' not found."
        elif self._data_mode == "REAL" and _is_fixture_path(self._base_dir):
            note = "Fixture path detected — blocked in REAL mode."
        else:
            try:
                files = os.listdir(self._base_dir)
                note = f"{len(files)} items in base_dir."
            except Exception as exc:
                note = f"Cannot list base_dir: {exc}"
        return {
            "ok": status == ProviderStatus.AVAILABLE,
            "provider": self._provider_id,
            "status": status,
            "base_dir": self._base_dir,
            "note": note,
        }

    def normalize_response(self, raw_response: Any, request: ProviderRequest) -> ProviderResponse:
        """
        Normalize raw dict data into a ProviderResponse.
        [!] NaN values are preserved, NOT converted to 0.
        """
        if isinstance(raw_response, ProviderResponse):
            return raw_response
        records = raw_response if isinstance(raw_response, list) else []
        return ProviderResponse(
            request_id=request.request_id,
            provider_id=self._provider_id,
            capability=request.capability,
            status=ProviderStatus.AVAILABLE if records else ProviderStatus.UNAVAILABLE,
            data_mode=self._data_mode,
            records=records,
            record_count=len(records),
        )

    def build_provenance(self, request: ProviderRequest, response: ProviderResponse) -> dict:
        return {
            "provider_id": self._provider_id,
            "provider_type": self._provider_type,
            "capability": request.capability,
            "request_id": request.request_id,
            "base_dir": self._base_dir,
            "data_mode": self._data_mode,
            "fetched_at": _now_iso(),
            "record_count": response.record_count,
            "schema_version": "1.3.2",
        }

    def close(self) -> None:
        pass

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _fetch_daily_ohlcv(self, request: ProviderRequest) -> ProviderResponse:
        all_records = []
        warnings = []
        errors = []

        for symbol in request.symbols:
            csv_path = os.path.join(self._base_dir, f"{symbol}.csv")
            if not os.path.isfile(csv_path):
                warnings.append(f"CSV file not found for symbol '{symbol}': {csv_path}")
                continue

            try:
                rows = self._read_ohlcv_csv(csv_path, symbol, request.start_date, request.end_date)
                if isinstance(rows, str):
                    # Schema mismatch error string returned
                    errors.append(rows)
                    return ProviderResponse(
                        request_id=request.request_id,
                        provider_id=self._provider_id,
                        capability=request.capability,
                        status=ProviderStatus.UNAVAILABLE,
                        data_mode=self._data_mode,
                        errors=[rows],
                        warnings=warnings,
                        metadata={"error_category": ProviderErrorCategory.SCHEMA_MISMATCH},
                    )
                all_records.extend(rows)
            except Exception as exc:
                errors.append(f"Error reading '{csv_path}': {exc}")

        status = ProviderStatus.AVAILABLE if all_records else ProviderStatus.UNAVAILABLE
        return ProviderResponse(
            request_id=request.request_id,
            provider_id=self._provider_id,
            capability=request.capability,
            status=status,
            data_mode=self._data_mode,
            records=all_records,
            record_count=len(all_records),
            warnings=warnings,
            errors=errors,
        )

    def _read_ohlcv_csv(
        self, csv_path: str, symbol: str, start_date: str, end_date: str
    ):
        """
        Read OHLCV CSV. Returns list of dicts or error string on schema mismatch.
        [!] NaN values are preserved, NOT converted to 0.
        """
        records = []
        try:
            with open(csv_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                if reader.fieldnames is None:
                    return f"SCHEMA_MISMATCH: '{csv_path}' has no headers."
                cols = {c.strip().lower() for c in reader.fieldnames}
                missing = _OHLCV_REQUIRED_COLUMNS - cols
                if missing:
                    return f"SCHEMA_MISMATCH: '{csv_path}' missing columns: {sorted(missing)}."
                for row in reader:
                    date_val = row.get("date", "").strip()
                    if start_date and date_val < start_date:
                        continue
                    if end_date and date_val > end_date:
                        continue
                    record = {"symbol": symbol, "date": date_val}
                    for col in ("open", "high", "low", "close", "volume"):
                        raw = row.get(col, "").strip()
                        if raw == "" or raw.lower() in ("nan", "none", "null"):
                            record[col] = float("nan")  # Preserve NaN, NOT 0
                        else:
                            try:
                                record[col] = float(raw)
                            except ValueError:
                                record[col] = float("nan")
                    records.append(record)
        except UnicodeDecodeError:
            # Try latin-1 fallback
            with open(csv_path, newline="", encoding="latin-1") as f:
                reader = csv.DictReader(f)
                if reader.fieldnames is None:
                    return f"SCHEMA_MISMATCH: '{csv_path}' has no headers."
                cols = {c.strip().lower() for c in reader.fieldnames}
                missing = _OHLCV_REQUIRED_COLUMNS - cols
                if missing:
                    return f"SCHEMA_MISMATCH: '{csv_path}' missing columns: {sorted(missing)}."
                for row in reader:
                    date_val = row.get("date", "").strip()
                    if start_date and date_val < start_date:
                        continue
                    if end_date and date_val > end_date:
                        continue
                    record = {"symbol": symbol, "date": date_val}
                    for col in ("open", "high", "low", "close", "volume"):
                        raw = row.get(col, "").strip()
                        if raw == "" or raw.lower() in ("nan", "none", "null"):
                            record[col] = float("nan")
                        else:
                            try:
                                record[col] = float(raw)
                            except ValueError:
                                record[col] = float("nan")
                    records.append(record)
        return records

    def _fetch_unsupported_graceful(self, request: ProviderRequest, cap: str) -> ProviderResponse:
        """For declared-but-not-implemented capabilities: return UNAVAILABLE gracefully."""
        return ProviderResponse(
            request_id=request.request_id,
            provider_id=self._provider_id,
            capability=cap,
            status=ProviderStatus.UNAVAILABLE,
            data_mode=self._data_mode,
            errors=[f"Capability '{cap}' declared but data files not found."],
            metadata={"error_category": ProviderErrorCategory.EMPTY_RESPONSE},
        )
