"""
data/governance/request_ledger_v145.py — Request Ledger v1.4.5.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Append-only. No token stored. Auth headers redacted.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from data.governance.models_v145 import RequestLedgerEntry

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_SECRET_KEYS = {"token", "key", "cookie", "auth", "authorization", "password", "secret", "access_token", "api_key"}


class RequestLedger:
    """
    Append-only request ledger.
    [!] No token stored in plaintext.
    [!] Auth headers/tokens are redacted from safe_request_metadata.
    """

    def __init__(self) -> None:
        self._entries: Dict[str, RequestLedgerEntry] = {}
        self._order: List[str] = []

    def _redact_sensitive(self, entry: RequestLedgerEntry) -> RequestLedgerEntry:
        """Remove auth headers/tokens from safe_request_metadata."""
        clean = {}
        for k, v in entry.safe_request_metadata.items():
            if any(s in k.lower() for s in _SECRET_KEYS):
                clean[k] = "[REDACTED]"
            else:
                clean[k] = v
        entry.safe_request_metadata = clean
        # Never store token in plaintext; only fingerprint allowed
        return entry

    def record(self, entry: RequestLedgerEntry) -> str:
        entry = self._redact_sensitive(entry)
        self._entries[entry.request_id] = entry
        if entry.request_id not in self._order:
            self._order.append(entry.request_id)
        return entry.request_id

    def update_status(self, request_id: str, status: str, **kwargs: Any) -> None:
        entry = self._entries.get(request_id)
        if entry is None:
            return
        entry.status = status
        for k, v in kwargs.items():
            if hasattr(entry, k):
                setattr(entry, k, v)

    def get(self, request_id: str) -> Optional[RequestLedgerEntry]:
        return self._entries.get(request_id)

    def list_by_provider(self, provider_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        results = [
            self._entries[rid].to_dict()
            for rid in self._order
            if self._entries[rid].provider_id == provider_id
        ]
        return results[-limit:]

    def list_by_host(self, host: str, limit: int = 100) -> List[Dict[str, Any]]:
        results = [
            self._entries[rid].to_dict()
            for rid in self._order
            if self._entries[rid].host == host
        ]
        return results[-limit:]

    def list_by_fetch_run(self, fetch_run_id: str) -> List[Dict[str, Any]]:
        return [
            self._entries[rid].to_dict()
            for rid in self._order
            if self._entries[rid].fetch_run_id == fetch_run_id
        ]

    def list_by_time_range(self, start: str, end: str) -> List[Dict[str, Any]]:
        return [
            self._entries[rid].to_dict()
            for rid in self._order
            if start <= self._entries[rid].started_at <= end
        ]

    def get_stats(
        self,
        provider_id: Optional[str] = None,
        host: Optional[str] = None,
    ) -> Dict[str, Any]:
        entries = list(self._entries.values())
        if provider_id:
            entries = [e for e in entries if e.provider_id == provider_id]
        if host:
            entries = [e for e in entries if e.host == host]
        total = len(entries)
        completed = sum(1 for e in entries if e.status == "COMPLETED")
        failed = sum(1 for e in entries if e.status == "FAILED")
        rate_limited = sum(1 for e in entries if e.status == "RATE_LIMITED")
        cache_hits = sum(1 for e in entries if e.status == "CACHE_HIT")
        return {
            "total": total,
            "completed": completed,
            "failed": failed,
            "rate_limited": rate_limited,
            "cache_hits": cache_hits,
            "success_rate": (completed / total) if total > 0 else 0.0,
        }
