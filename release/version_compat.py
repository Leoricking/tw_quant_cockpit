"""
release/version_compat.py — Semantic version compatibility helper v1.2.8

Provides parse_version() and version_at_least() for forward-compatible
health checks.  Does NOT use string comparison.

Supports: "1.2.5", "1.2.8", "1.2.10", "1.3.0", "v1.2.8"
Graceful on invalid input (returns False from version_at_least).

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import re
from typing import Tuple

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

_VERSION_RE = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)(?:[.-].*)?$")


def parse_version(value: str) -> Tuple[int, ...]:
    """
    Parse a version string into a (major, minor, patch) integer tuple.

    Supports optional leading "v" and ignores pre-release suffixes.

    Returns (0, 0, 0) for invalid input so callers get a safe comparable value.

    Examples:
        parse_version("1.2.5")  -> (1, 2, 5)
        parse_version("v1.2.8") -> (1, 2, 8)
        parse_version("1.2.10") -> (1, 2, 10)
        parse_version("1.3.0")  -> (1, 3, 0)
        parse_version("bad")    -> (0, 0, 0)
    """
    if not isinstance(value, str):
        return (0, 0, 0)
    m = _VERSION_RE.match(value.strip())
    if not m:
        return (0, 0, 0)
    try:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except (ValueError, IndexError):
        return (0, 0, 0)


def version_at_least(current: str, minimum: str) -> bool:
    """
    Return True if current >= minimum using semantic (integer) comparison.

    Both strings are parsed via parse_version().
    Returns False if either string is invalid.

    Examples:
        version_at_least("1.2.8",  "1.2.5")  -> True
        version_at_least("1.2.10", "1.2.5")  -> True   # string "1.2.10" < "1.2.5" but int 10 > 5
        version_at_least("1.3.0",  "1.2.7")  -> True
        version_at_least("1.2.4",  "1.2.5")  -> False
        version_at_least("1.2.6",  "1.2.7")  -> False
        version_at_least("bad",    "1.2.5")  -> False
    """
    cur = parse_version(current)
    mim = parse_version(minimum)
    if cur == (0, 0, 0) or mim == (0, 0, 0):
        return False
    return cur >= mim
