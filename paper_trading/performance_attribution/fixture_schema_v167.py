"""
paper_trading/performance_attribution/fixture_schema_v167.py
Fixture Schema and Governance for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] All fixtures require 10 safety markers set to boolean True.
[!] Real markers in fixture → BLOCKED. Missing markers → INVALID.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Set

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True

SCHEMA_VERSION = "167"
POLICY_VERSION = "1.6.7-paper-attribution"

# ── Required fixture safety markers ──────────────────────────────────────────
REQUIRED_FIXTURE_MARKERS: Dict[str, bool] = {
    "test_fixture":            True,
    "demo_only":               True,
    "paper_only":              True,
    "research_only":           True,
    "not_live":                True,
    "no_broker":               True,
    "no_real_account":         True,
    "no_real_orders":          True,
    "not_for_production":      True,
    "paper_attribution_only":  True,
}
assert len(REQUIRED_FIXTURE_MARKERS) == 10

# ── Fields forbidden in fixtures ─────────────────────────────────────────────
FORBIDDEN_FIXTURE_FIELDS: frozenset = frozenset({
    "broker_session",
    "real_account_token",
    "api_secret",
    "password",
    "credential",
    "real_order_handle",
    "production_db_connection",
    "bank_account",
    "real_capital_control",
    "live_execution",
    "is_live",
    "is_real",
    "is_production",
    "live_mode",
    "real_mode",
    "production_mode",
    "broker_mode",
    "shioaji_login",
    "broker_api_key",
})

# ── Required fixture metadata fields ─────────────────────────────────────────
REQUIRED_FIXTURE_METADATA: List[str] = [
    "fixture_id",
    "purpose",
    "schema_version",
    "category",
]


def validate_fixture_markers(fixture: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate all 10 required safety markers are present and True.
    Returns {"valid": bool, "errors": List[str], "warnings": List[str]}.
    """
    errors: List[str] = []
    warnings: List[str] = []

    for marker, expected in REQUIRED_FIXTURE_MARKERS.items():
        if marker not in fixture:
            errors.append(f"missing_marker: {marker}")
        elif fixture[marker] is not True:
            errors.append(f"invalid_marker: {marker}={fixture[marker]!r} expected True")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "paper_only": True,
    }


def validate_fixture_forbidden_fields(fixture: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check that no forbidden (real/live/production) fields are present.
    Returns {"clean": bool, "blocked": bool, "violations": List[str]}.
    """
    violations: List[str] = []
    for field in FORBIDDEN_FIXTURE_FIELDS:
        if field in fixture and fixture[field] not in (None, False, ""):
            violations.append(f"BLOCKED: forbidden_field={field!r} value={fixture[field]!r}")

    return {
        "clean": len(violations) == 0,
        "blocked": len(violations) > 0,
        "violations": violations,
        "paper_only": True,
    }


def validate_fixture_metadata(fixture: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate required metadata fields are present and non-empty.
    """
    errors: List[str] = []
    for field in REQUIRED_FIXTURE_METADATA:
        if not fixture.get(field):
            errors.append(f"missing_metadata: {field}")
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "paper_only": True,
    }


def validate_fixture_full(fixture: Dict[str, Any]) -> Dict[str, Any]:
    """
    Full fixture validation: markers + forbidden fields + metadata.
    Returns consolidated result.
    """
    markers_result   = validate_fixture_markers(fixture)
    forbidden_result = validate_fixture_forbidden_fields(fixture)
    metadata_result  = validate_fixture_metadata(fixture)

    all_errors = (
        markers_result["errors"]
        + forbidden_result["violations"]
        + metadata_result["errors"]
    )

    valid   = len(all_errors) == 0
    blocked = forbidden_result["blocked"]

    return {
        "valid":    valid,
        "blocked":  blocked,
        "errors":   all_errors,
        "warnings": markers_result["warnings"],
        "markers_ok":   markers_result["valid"],
        "forbidden_ok": forbidden_result["clean"],
        "metadata_ok":  metadata_result["valid"],
        "paper_only":   True,
        "research_only": True,
    }


def build_fixture_template(
    fixture_id: str,
    purpose: str,
    category: str,
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Build a compliant fixture template with all required markers.
    Extra fields are merged in (forbidden fields are stripped if present).
    """
    template: Dict[str, Any] = {
        "fixture_id":            fixture_id,
        "purpose":               purpose,
        "schema_version":        SCHEMA_VERSION,
        "policy_version":        POLICY_VERSION,
        "category":              category,
        # 10 required safety markers
        "test_fixture":          True,
        "demo_only":             True,
        "paper_only":            True,
        "research_only":         True,
        "not_live":              True,
        "no_broker":             True,
        "no_real_account":       True,
        "no_real_orders":        True,
        "not_for_production":    True,
        "paper_attribution_only": True,
    }
    if extra:
        for k, v in extra.items():
            if k not in FORBIDDEN_FIXTURE_FIELDS:
                template[k] = v
    return template


def assert_fixture_safe(fixture: Dict[str, Any]) -> None:
    """
    Assert fixture passes full validation. Raises ValueError if not.
    Used in test setup to fail fast on invalid fixtures.
    """
    result = validate_fixture_full(fixture)
    if not result["valid"]:
        raise ValueError(
            f"Fixture validation failed: {result['errors']}"
        )
    if result["blocked"]:
        raise ValueError(
            f"Fixture BLOCKED (forbidden fields): {result['errors']}"
        )
