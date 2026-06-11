"""
Regression Summary — classification and formatting for release gate results.
Research Only. No Real Orders. Production Trading BLOCKED.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional

# Warning classifications
KNOWN_CP950_WARNING = "KNOWN_CP950_WARNING"
KNOWN_PAPER_SMOKE_WARNING = "KNOWN_PAPER_SMOKE_WARNING"
KNOWN_REPORT_PACK_OPTIONAL = "KNOWN_REPORT_PACK_OPTIONAL"
KNOWN_NO_REAL_ORDERS_FALSE_POSITIVE = "KNOWN_NO_REAL_ORDERS_FALSE_POSITIVE"
UNKNOWN_WARNING = "UNKNOWN_WARNING"

# Blocked classifications
KNOWN_NO_REAL_ORDERS_FLAG_CHECK = "KNOWN_NO_REAL_ORDERS_FLAG_CHECK"
KNOWN_RESEARCH_ONLY_BLOCK = "KNOWN_RESEARCH_ONLY_BLOCK"
UNKNOWN_BLOCKED = "UNKNOWN_BLOCKED"

_KNOWN_WARN_PATTERNS = [
    ("cp950", KNOWN_CP950_WARNING),
    ("charmap", KNOWN_CP950_WARNING),
    ("UnicodeDecodeError", KNOWN_CP950_WARNING),
    ("paper_state.json missing", KNOWN_PAPER_SMOKE_WARNING),
    ("paper smoke", KNOWN_PAPER_SMOKE_WARNING),
    ("ENV_LIMITED", KNOWN_REPORT_PACK_OPTIONAL),
    ("optional report", KNOWN_REPORT_PACK_OPTIONAL),
    ("NOT_GENERATED", KNOWN_REPORT_PACK_OPTIONAL),
    ("no_real_orders flag", KNOWN_NO_REAL_ORDERS_FALSE_POSITIVE),
    ("No Real Orders flag", KNOWN_NO_REAL_ORDERS_FALSE_POSITIVE),
    ("pre-existing check", KNOWN_NO_REAL_ORDERS_FALSE_POSITIVE),
]

_KNOWN_BLOCKED_PATTERNS = [
    ("no_real_orders flag check", KNOWN_NO_REAL_ORDERS_FLAG_CHECK),
    ("no_real_orders pre-existing", KNOWN_NO_REAL_ORDERS_FLAG_CHECK),
    ("research only block", KNOWN_RESEARCH_ONLY_BLOCK),
    ("RESEARCH_ONLY", KNOWN_RESEARCH_ONLY_BLOCK),
]


@dataclass
class NormalizedResult:
    name: str
    status: str
    message: str = ""
    warn_class: str = ""
    blocked_class: str = ""
    is_known: bool = False


@dataclass
class ReleaseSummary:
    total: int = 0
    pass_count: int = 0
    warn_count: int = 0
    fail_count: int = 0
    blocked_count: int = 0
    known_warn_count: int = 0
    known_blocked_count: int = 0
    unknown_warn_count: int = 0
    unknown_fail_count: int = 0
    unknown_blocked_count: int = 0
    overall_status: str = "PASS"
    no_real_orders: bool = True
    production_blocked: bool = True
    results: List[NormalizedResult] = field(default_factory=list)


def normalize_regression_result(raw_result: dict) -> NormalizedResult:
    """Normalize a raw regression result dict into a NormalizedResult."""
    name = raw_result.get("name", raw_result.get("test", "unknown"))
    status = str(raw_result.get("status", "UNKNOWN")).upper()
    message = raw_result.get("message", raw_result.get("detail", ""))
    nr = NormalizedResult(name=name, status=status, message=message)
    if status == "WARN":
        nr.warn_class, nr.is_known = classify_warning(message)
    elif status == "BLOCKED":
        nr.blocked_class, nr.is_known = classify_blocked(message + " " + name)
    return nr


def classify_warning(message: str) -> tuple:
    """Return (classification, is_known) for a warning message."""
    for pattern, cls in _KNOWN_WARN_PATTERNS:
        if pattern.lower() in message.lower():
            return cls, True
    return UNKNOWN_WARNING, False


def classify_blocked(message: str) -> tuple:
    """Return (classification, is_known) for a blocked message."""
    for pattern, cls in _KNOWN_BLOCKED_PATTERNS:
        if pattern.lower() in message.lower():
            return cls, True
    return UNKNOWN_BLOCKED, False


def build_release_summary(results: List[dict]) -> ReleaseSummary:
    """Build a ReleaseSummary from a list of raw result dicts."""
    summary = ReleaseSummary(total=len(results))
    normalized = [normalize_regression_result(r) for r in results]
    summary.results = normalized
    for nr in normalized:
        if nr.status == "PASS":
            summary.pass_count += 1
        elif nr.status == "WARN":
            summary.warn_count += 1
            if nr.is_known:
                summary.known_warn_count += 1
            else:
                summary.unknown_warn_count += 1
        elif nr.status in ("FAIL", "ERROR"):
            summary.fail_count += 1
            summary.unknown_fail_count += 1
        elif nr.status == "BLOCKED":
            summary.blocked_count += 1
            if nr.is_known:
                summary.known_blocked_count += 1
            else:
                summary.unknown_blocked_count += 1

    if summary.unknown_fail_count > 0:
        summary.overall_status = "FAIL"
    elif summary.unknown_blocked_count > 0:
        summary.overall_status = "BLOCKED"
    elif summary.unknown_warn_count > 0:
        summary.overall_status = "WARN"
    elif summary.warn_count > 0 or summary.blocked_count > 0:
        summary.overall_status = "WARN"
    else:
        summary.overall_status = "PASS"

    return summary


def format_console_summary(summary: ReleaseSummary) -> str:
    lines = [
        "=" * 60,
        "TW Quant Cockpit \u2014 Regression Summary",
        "Research Only | No Real Orders | Production Trading BLOCKED",
        "=" * 60,
        f"  Total:           {summary.total}",
        f"  PASS:            {summary.pass_count}",
        f"  WARN:            {summary.warn_count}  (known: {summary.known_warn_count}, unknown: {summary.unknown_warn_count})",
        f"  FAIL:            {summary.fail_count}  (unknown: {summary.unknown_fail_count})",
        f"  BLOCKED:         {summary.blocked_count}  (known: {summary.known_blocked_count}, unknown: {summary.unknown_blocked_count})",
        "-" * 60,
        f"  OVERALL:         {summary.overall_status}",
        "=" * 60,
    ]
    # List known blocked
    known_blocked = [r for r in summary.results if r.status == "BLOCKED" and r.is_known]
    if known_blocked:
        lines.append("  Known BLOCKED (expected, not failures):")
        for r in known_blocked:
            lines.append(f"    [{r.blocked_class}] {r.name}")
    # List unknown failures
    unknown_fails = [r for r in summary.results if r.status in ("FAIL", "ERROR")]
    if unknown_fails:
        lines.append("  Unknown FAIL (investigate):")
        for r in unknown_fails:
            lines.append(f"    [FAIL] {r.name}: {r.message[:60]}")
    return "\n".join(lines)


def format_markdown_summary(summary: ReleaseSummary) -> str:
    lines = [
        "## Regression Summary",
        "",
        "| Metric | Count |",
        "|--------|-------|",
        f"| Total | {summary.total} |",
        f"| PASS | {summary.pass_count} |",
        f"| WARN | {summary.warn_count} (known: {summary.known_warn_count}) |",
        f"| FAIL | {summary.fail_count} |",
        f"| BLOCKED | {summary.blocked_count} (known: {summary.known_blocked_count}) |",
        f"| Unknown FAIL | {summary.unknown_fail_count} |",
        f"| Unknown BLOCKED | {summary.unknown_blocked_count} |",
        f"| **Overall** | **{summary.overall_status}** |",
        "",
    ]
    return "\n".join(lines)
