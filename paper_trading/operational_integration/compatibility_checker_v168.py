"""
paper_trading/operational_integration/compatibility_checker_v168.py
Compatibility Checker for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .models_v168 import CompatibilityResult

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse_version(v: str):
    parts = []
    for p in str(v).split("."):
        try:
            parts.append(int(p))
        except ValueError:
            parts.append(0)
    return tuple(parts)


class CompatibilityChecker:
    """Checks version and schema compatibility between components."""

    def check(
        self,
        from_component: str,
        to_component: str,
        from_version: str,
        to_version: str,
        from_schema: Dict[str, Any],
        to_schema: Dict[str, Any],
    ) -> CompatibilityResult:
        """Run compatibility check between two components."""
        check_id = f"compat_{from_component}_{to_component}"
        details: Dict[str, Any] = {}

        if self.check_exact(from_version, to_version):
            status = "EXACT"
        elif self.check_backward_compatible(from_version, to_version):
            status = "BACKWARD_COMPATIBLE"
        elif not self.check_schema_compatible(from_schema, to_schema):
            status = "SCHEMA_INCOMPATIBLE"
        else:
            status = "FORWARD_INCOMPATIBLE"

        details["from_version"] = from_version
        details["to_version"] = to_version
        details["schema_compatible"] = self.check_schema_compatible(from_schema, to_schema)
        details["safety_compatible"] = self.check_safety_compatible(from_schema, to_schema)

        return CompatibilityResult(
            check_id=check_id,
            from_component=from_component,
            to_component=to_component,
            status=status,
            details=details,
            created_at=_utcnow_iso(),
        )

    def check_exact(self, v1: str, v2: str) -> bool:
        """Return True if versions are exactly equal."""
        return v1 == v2

    def check_backward_compatible(self, from_v: str, to_v: str) -> bool:
        """
        Return True if from_v is backward-compatible with to_v.
        Backward-compatible: same major.minor, from_v >= to_v.
        """
        pf = _parse_version(from_v)
        pt = _parse_version(to_v)
        if len(pf) < 2 or len(pt) < 2:
            return False
        # Same major.minor, from_v >= to_v
        if pf[0] == pt[0] and pf[1] == pt[1]:
            return pf >= pt
        return False

    def check_schema_compatible(self, s1: Dict[str, Any], s2: Dict[str, Any]) -> bool:
        """
        Return True if s1 and s2 share all required fields.
        Check that required fields in s2 are all present in s1.
        """
        if not s1 or not s2:
            return True
        s1_keys = set(s1.keys())
        s2_required = {k for k, v in s2.items() if v is not None}
        missing = s2_required - s1_keys
        return len(missing) == 0

    def check_capability(self, component_id: str, required_capability: str) -> bool:
        """Check if component has the required capability."""
        from .component_registry_v168 import ComponentRegistry
        reg = ComponentRegistry()
        comp = reg.get_component(component_id)
        if comp is None:
            return False
        return required_capability in comp.capabilities

    def check_safety_compatible(self, c1: Dict[str, Any], c2: Dict[str, Any]) -> bool:
        """Return True if both components have paper_only=True."""
        return c1.get("paper_only", False) and c2.get("paper_only", False)

    def summarize(self, results: List[CompatibilityResult]) -> Dict[str, Any]:
        """Return summary of compatibility results."""
        total = len(results)
        exact = sum(1 for r in results if r.status == "EXACT")
        backward = sum(1 for r in results if r.status == "BACKWARD_COMPATIBLE")
        incompatible = sum(1 for r in results if r.status in ("SCHEMA_INCOMPATIBLE", "FORWARD_INCOMPATIBLE"))
        return {
            "total": total,
            "exact_count": exact,
            "backward_compatible_count": backward,
            "incompatible_count": incompatible,
            "all_compatible": incompatible == 0,
            "paper_only": True,
        }
