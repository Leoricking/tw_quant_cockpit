"""
data/providers/local_repository_provider_adapter.py — Local repository adapter v1.3.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Wraps existing repository/DB. Does NOT create a new DB.
[!] No data: returns UNAVAILABLE (not mock, not synthetic).
"""
from __future__ import annotations

import logging
import os
from typing import Any, List

from data.providers.real_data_provider_models import (
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

_REPO_CAPABILITIES = [
    ProviderCapability.DAILY_OHLCV,
    ProviderCapability.MONTHLY_REVENUE,
]


class LocalRepositoryProviderAdapter(RealDataProviderAdapter):
    """
    Adapter wrapping an existing local data repository/DB directory.

    [!] Does NOT create or modify the DB.
    [!] Returns UNAVAILABLE gracefully when no data found.
    [!] Never returns mock or synthetic data.
    """

    def __init__(self, repo_path: str = "", data_mode: str = "REAL") -> None:
        self._repo_path = repo_path
        self._data_mode = data_mode
        self._provider_id = "local_repository"
        self._provider_type = ProviderType.LOCAL_DATABASE

    # ------------------------------------------------------------------
    # Abstract method implementations
    # ------------------------------------------------------------------

    def get_metadata(self) -> ProviderMetadata:
        is_available = bool(self._repo_path) and os.path.isdir(self._repo_path)
        return ProviderMetadata(
            provider_id=self._provider_id,
            provider_name="Local Repository Provider",
            provider_type=self._provider_type,
            description="Wraps an existing local data repository. Read-only.",
            enabled=is_available,
            priority=40,
            capabilities=list(_REPO_CAPABILITIES),
            markets=[],
            security_types=[],
            requires_auth=False,
            supports_batch=True,
            supports_incremental=True,
            supports_historical=True,
            supports_intraday=False,
            terms_note="Local repository only. No external data. Read-only.",
            source_url_type="LOCAL_PATH",
            data_mode=self._data_mode,
        )

    def get_status(self) -> str:
        if not self._repo_path:
            return ProviderStatus.MISCONFIGURED
        if not os.path.isdir(self._repo_path):
            return ProviderStatus.UNAVAILABLE
        try:
            os.listdir(self._repo_path)
        except PermissionError:
            return ProviderStatus.UNAVAILABLE
        return ProviderStatus.AVAILABLE

    def get_capabilities(self) -> List[str]:
        return list(_REPO_CAPABILITIES)

    def supports(self, capability: str, market: str = "") -> bool:
        return capability in _REPO_CAPABILITIES

    def validate_request(self, request: ProviderRequest) -> List[str]:
        errors = []
        if not request.capability:
            errors.append("capability is required.")
        if request.capability not in _REPO_CAPABILITIES:
            errors.append(f"Capability '{request.capability}' not supported by local_repository provider.")
        if not request.symbols:
            errors.append("At least one symbol is required.")
        return errors

    def fetch(self, request: ProviderRequest) -> ProviderResponse:
        status = self.get_status()
        if status != ProviderStatus.AVAILABLE:
            return ProviderResponse(
                request_id=request.request_id,
                provider_id=self._provider_id,
                capability=request.capability,
                status=ProviderStatus.UNAVAILABLE,
                data_mode=self._data_mode,
                errors=[f"Repository not available: status={status}, repo_path='{self._repo_path}'."],
                metadata={"error_category": ProviderErrorCategory.EMPTY_RESPONSE},
            )

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

        # Attempt to read from repository
        return self._fetch_from_repo(request)

    def health_check(self) -> dict:
        status = self.get_status()
        note = ""
        if not self._repo_path:
            note = "repo_path not configured."
        elif not os.path.isdir(self._repo_path):
            note = f"repo_path '{self._repo_path}' does not exist."
        else:
            try:
                files = os.listdir(self._repo_path)
                note = f"{len(files)} items in repo_path."
            except Exception as exc:
                note = f"Cannot list repo_path: {exc}"
        return {
            "ok": status == ProviderStatus.AVAILABLE,
            "provider": self._provider_id,
            "status": status,
            "repo_path": self._repo_path,
            "note": note,
        }

    def normalize_response(self, raw_response: Any, request: ProviderRequest) -> ProviderResponse:
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
            "repo_path": self._repo_path,
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

    def _fetch_from_repo(self, request: ProviderRequest) -> ProviderResponse:
        """
        Attempt to read data from existing repository files.
        Returns UNAVAILABLE if no data found — never returns mock.
        """
        # This adapter delegates to the actual repository structure.
        # Without knowing the exact DB format, we look for symbol files.
        all_records = []
        warnings = []

        cap = request.capability
        subdir_map = {
            ProviderCapability.DAILY_OHLCV: "daily",
            ProviderCapability.MONTHLY_REVENUE: "monthly_revenue",
        }
        subdir = subdir_map.get(cap, cap.lower())
        cap_dir = os.path.join(self._repo_path, subdir)

        if not os.path.isdir(cap_dir):
            return ProviderResponse(
                request_id=request.request_id,
                provider_id=self._provider_id,
                capability=cap,
                status=ProviderStatus.UNAVAILABLE,
                data_mode=self._data_mode,
                warnings=[f"Repository subdirectory not found: '{cap_dir}'."],
                metadata={"error_category": ProviderErrorCategory.EMPTY_RESPONSE},
            )

        for symbol in request.symbols:
            # Try common file patterns
            for ext in (".csv", ".parquet", ".json"):
                fpath = os.path.join(cap_dir, f"{symbol}{ext}")
                if os.path.isfile(fpath):
                    try:
                        if ext == ".csv":
                            import csv as csv_mod
                            with open(fpath, newline="", encoding="utf-8") as f:
                                reader = csv_mod.DictReader(f)
                                for row in reader:
                                    row["symbol"] = symbol
                                    all_records.append(dict(row))
                    except Exception as exc:
                        warnings.append(f"Error reading '{fpath}': {exc}")
                    break
            else:
                warnings.append(f"No data file found for symbol '{symbol}' in '{cap_dir}'.")

        status = ProviderStatus.AVAILABLE if all_records else ProviderStatus.UNAVAILABLE
        return ProviderResponse(
            request_id=request.request_id,
            provider_id=self._provider_id,
            capability=cap,
            status=status,
            data_mode=self._data_mode,
            records=all_records,
            record_count=len(all_records),
            warnings=warnings,
        )
