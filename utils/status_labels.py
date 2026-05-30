"""
utils/status_labels.py - Unified status label constants and helpers (v0.3.22).

[!] Research Only. Read Only. No Real Orders.
[!] Production Trading: BLOCKED.
"""

from __future__ import annotations

from typing import Optional

# ---------------------------------------------------------------------------
# Operational status constants
# ---------------------------------------------------------------------------

OK               = "OK"
PARTIAL          = "PARTIAL"
WARN             = "WARN"
FAILED           = "FAILED"
BLOCKED          = "BLOCKED"
SKIPPED          = "SKIPPED"
MISSING          = "MISSING"
NOT_CONFIGURED   = "NOT_CONFIGURED"
DISABLED         = "DISABLED"
PLANNED          = "PLANNED"

# Safety / scope constants
READ_ONLY          = "READ_ONLY"
NO_REAL_ORDERS     = "NO_REAL_ORDERS"
PRODUCTION_BLOCKED = "PRODUCTION_BLOCKED"
RESEARCH_ONLY      = "RESEARCH_ONLY"

# Data quality constants
OBSERVATIONAL  = "OBSERVATIONAL"
INSUFFICIENT   = "INSUFFICIENT"
RELIABLE       = "RELIABLE"

# Freshness constants
FRESH  = "FRESH"
STALE  = "STALE"
OLD    = "OLD"
UNKNOWN = "UNKNOWN"

# ---------------------------------------------------------------------------
# Canonical order (for sorting / display ordering)
# ---------------------------------------------------------------------------

_STATUS_ORDER = [
    OK, RELIABLE, FRESH,
    PARTIAL, WARN, OBSERVATIONAL, STALE,
    NOT_CONFIGURED, PLANNED, DISABLED, SKIPPED,
    MISSING, OLD, INSUFFICIENT,
    FAILED, BLOCKED,
    UNKNOWN,
]

_ORDER_MAP = {s: i for i, s in enumerate(_STATUS_ORDER)}

# ---------------------------------------------------------------------------
# Normalization map — maps variant spellings to canonical form
# ---------------------------------------------------------------------------

_NORMALIZE_MAP = {
    # OK variants
    "OK":           OK,
    "PASS":         OK,
    "SUCCESS":      OK,
    "PASSED":       OK,
    # PARTIAL
    "PARTIAL":      PARTIAL,
    # WARN
    "WARN":         WARN,
    "WARNING":      WARN,
    # FAILED
    "FAILED":       FAILED,
    "FAIL":         FAILED,
    "FAILURE":      FAILED,
    "ERROR":        FAILED,
    # BLOCKED
    "BLOCKED":      BLOCKED,
    # SKIPPED
    "SKIPPED":      SKIPPED,
    "SKIP":         SKIPPED,
    # MISSING
    "MISSING":      MISSING,
    "NOT_FOUND":    MISSING,
    # NOT_CONFIGURED
    "NOT_CONFIGURED": NOT_CONFIGURED,
    "UNCONFIGURED":   NOT_CONFIGURED,
    # DISABLED
    "DISABLED":     DISABLED,
    # PLANNED
    "PLANNED":      PLANNED,
    # OBSERVATIONAL
    "OBSERVATIONAL": OBSERVATIONAL,
    # INSUFFICIENT
    "INSUFFICIENT": INSUFFICIENT,
    # RELIABLE
    "RELIABLE":     RELIABLE,
    # FRESH
    "FRESH":        FRESH,
    # STALE
    "STALE":        STALE,
    # OLD
    "OLD":          OLD,
    # UNKNOWN
    "UNKNOWN":      UNKNOWN,
    "N/A":          UNKNOWN,
    "NA":           UNKNOWN,
    "":             UNKNOWN,
}


def normalize_status(raw: Optional[str]) -> str:
    """Return canonical status string for *raw*.

    Case-insensitive. Falls back to UNKNOWN for unrecognised values.
    """
    if raw is None:
        return UNKNOWN
    upper = str(raw).strip().upper()
    return _NORMALIZE_MAP.get(upper, UNKNOWN)


def format_status(raw: Optional[str], width: int = 0) -> str:
    """Return a padded, bracketed status string, e.g. '[OK]     '.

    Normalizes first so all variants display consistently.
    """
    normalized = normalize_status(raw)
    label = f"[{normalized}]"
    if width > 0:
        label = label.ljust(width)
    return label


def is_success_status(raw: Optional[str]) -> bool:
    """Return True if status represents a fully successful outcome."""
    return normalize_status(raw) in (OK, RELIABLE, FRESH)


def is_warning_status(raw: Optional[str]) -> bool:
    """Return True if status represents a degraded-but-usable outcome."""
    return normalize_status(raw) in (PARTIAL, WARN, OBSERVATIONAL, STALE, NOT_CONFIGURED, PLANNED)


def is_failure_status(raw: Optional[str]) -> bool:
    """Return True if status represents a failure or blocking condition."""
    return normalize_status(raw) in (FAILED, BLOCKED, MISSING, INSUFFICIENT, OLD)


def status_sort_key(raw: Optional[str]) -> int:
    """Return an integer sort key (lower = better) for ordering status values."""
    normalized = normalize_status(raw)
    return _ORDER_MAP.get(normalized, len(_STATUS_ORDER))


def safe_status_message(raw: Optional[str], fallback: str = "Status unknown") -> str:
    """Return a human-readable status message.

    If *raw* is None / empty / UNKNOWN, return *fallback* instead.
    """
    normalized = normalize_status(raw)
    if normalized == UNKNOWN:
        return fallback
    return normalized
