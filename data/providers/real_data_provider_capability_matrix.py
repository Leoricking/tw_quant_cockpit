"""
data/providers/real_data_provider_capability_matrix.py — Capability matrix v1.3.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Dict

from data.providers.real_data_provider_models import (
    CapabilitySupport,
    ProviderCapability,
    ProviderStatus,
)
from data.providers.real_data_provider_registry_v132 import RealDataProviderRegistryV132

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False


class ProviderCapabilityMatrix:
    """
    Builds and formats the capability matrix for all registered providers.
    """

    _EXTRA_FIELDS = [
        "TWSE_SUPPORT", "TPEX_SUPPORT",
        "BATCH", "HISTORICAL", "INTRADAY",
        "AUTH_REQUIRED", "ENABLED", "CURRENT_STATUS",
    ]

    def __init__(self, registry: RealDataProviderRegistryV132) -> None:
        self._registry = registry

    def build(self) -> Dict[str, Dict[str, str]]:
        """
        Build full matrix: {provider_id: {field: CapabilitySupport or str}}.
        Fields: all ProviderCapability values + extra metadata fields.
        """
        matrix: Dict[str, Dict[str, str]] = {}
        all_caps = ProviderCapability.all_capabilities()

        for meta in self._registry.list():
            pid = meta.provider_id
            adapter = self._registry.get(pid)
            row: Dict[str, str] = {}

            # Capability support
            for cap in all_caps:
                if cap in meta.capabilities:
                    if not meta.enabled:
                        row[cap] = CapabilitySupport.DISABLED
                    elif meta.requires_auth:
                        row[cap] = CapabilitySupport.AUTH_REQUIRED
                    else:
                        row[cap] = CapabilitySupport.SUPPORTED
                else:
                    row[cap] = CapabilitySupport.UNSUPPORTED

            # Market support
            row["TWSE_SUPPORT"] = CapabilitySupport.SUPPORTED if (not meta.markets or "TWSE" in meta.markets) else CapabilitySupport.UNSUPPORTED
            row["TPEX_SUPPORT"] = CapabilitySupport.SUPPORTED if (not meta.markets or "TPEX" in meta.markets or "TPEx" in meta.markets) else CapabilitySupport.UNSUPPORTED

            # Metadata flags as capability support strings
            row["BATCH"] = CapabilitySupport.SUPPORTED if meta.supports_batch else CapabilitySupport.UNSUPPORTED
            row["HISTORICAL"] = CapabilitySupport.SUPPORTED if meta.supports_historical else CapabilitySupport.UNSUPPORTED
            row["INTRADAY"] = CapabilitySupport.SUPPORTED if meta.supports_intraday else CapabilitySupport.UNSUPPORTED
            row["AUTH_REQUIRED"] = CapabilitySupport.AUTH_REQUIRED if meta.requires_auth else CapabilitySupport.UNSUPPORTED
            row["ENABLED"] = CapabilitySupport.SUPPORTED if meta.enabled else CapabilitySupport.DISABLED

            # Live status
            if adapter is not None:
                try:
                    status = adapter.get_status()
                except Exception:
                    status = ProviderStatus.UNAVAILABLE
            else:
                status = ProviderStatus.UNAVAILABLE
            row["CURRENT_STATUS"] = status

            matrix[pid] = row
        return matrix

    def get_summary(self) -> Dict[str, dict]:
        """
        Per capability: count of SUPPORTED, PARTIAL, UNSUPPORTED, DISABLED, AUTH_REQUIRED.
        """
        matrix = self.build()
        summary: Dict[str, dict] = {}
        for cap in ProviderCapability.all_capabilities():
            counts = {
                CapabilitySupport.SUPPORTED: 0,
                CapabilitySupport.PARTIAL: 0,
                CapabilitySupport.UNSUPPORTED: 0,
                CapabilitySupport.DISABLED: 0,
                CapabilitySupport.AUTH_REQUIRED: 0,
                CapabilitySupport.UNKNOWN: 0,
            }
            for row in matrix.values():
                val = row.get(cap, CapabilitySupport.UNKNOWN)
                if val in counts:
                    counts[val] += 1
                else:
                    counts[CapabilitySupport.UNKNOWN] += 1
            summary[cap] = counts
        return summary

    def format_text(self) -> str:
        """Format capability matrix as ASCII table."""
        matrix = self.build()
        if not matrix:
            return "No providers registered."

        provider_ids = sorted(matrix.keys())
        all_fields = ProviderCapability.all_capabilities() + self._EXTRA_FIELDS

        col_w = max(14, max((len(p) for p in provider_ids), default=14))
        field_w = max(len(f) for f in all_fields)
        header = f"{'CAPABILITY':<{field_w}}  " + "  ".join(f"{p:<{col_w}}" for p in provider_ids)
        sep = "-" * len(header)
        lines = [sep, header, sep]
        for field in all_fields:
            row_vals = []
            for pid in provider_ids:
                val = matrix.get(pid, {}).get(field, CapabilitySupport.UNKNOWN)
                row_vals.append(f"{val:<{col_w}}")
            lines.append(f"{field:<{field_w}}  " + "  ".join(row_vals))
        lines.append(sep)
        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {
            "matrix": self.build(),
            "summary": self.get_summary(),
        }
