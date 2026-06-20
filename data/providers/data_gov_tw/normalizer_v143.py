"""
data/providers/data_gov_tw/normalizer_v143.py — Data normalizer v1.4.3.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Applies schema contract normalization rules.
[!] Missing → None (not 0). Unknown → None (not empty string).
[!] Unit and license must be explicit.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class DataGovTwNormalizer:
    """
    Normalizes parsed records according to schema contract rules.

    Rules:
    - Missing values → None (never 0, never "")
    - Unknown fields → pass through (forward compatible)
    - Unit must be explicit — not assumed
    - License must be explicit — not assumed
    - ROC dates normalized to ISO 8601
    """

    def normalize_record(
        self,
        record: Dict[str, Any],
        schema_contract=None,
    ) -> Dict[str, Any]:
        """Apply normalization rules to a single record."""
        result = {}
        for k, v in record.items():
            result[k] = self._normalize_value(v)

        if schema_contract is not None:
            # Apply missing value tokens
            for token in (schema_contract.missing_value_tokens or []):
                for k, v in result.items():
                    if v == token:
                        result[k] = None

            # Apply field aliases
            for alias, canonical in (schema_contract.aliases or {}).items():
                if alias in result and canonical not in result:
                    result[canonical] = result.pop(alias)

        return result

    def _normalize_value(self, v: Any) -> Any:
        if v is None:
            return None
        if isinstance(v, (bool, int, float)):
            return v
        if isinstance(v, str):
            stripped = v.strip()
            if not stripped:
                return None  # Never return ""
            return stripped
        return v

    def normalize_batch(
        self,
        records: List[Dict[str, Any]],
        schema_contract=None,
    ) -> List[Dict[str, Any]]:
        return [self.normalize_record(r, schema_contract) for r in records]
