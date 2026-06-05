"""
release/version_info.py — Centralized version info for TW Quant Cockpit (v0.6.0).
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations
import logging
import os

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class VersionInfo:
    """Centralized version and safety metadata for v0.8.1."""

    version            = "v0.8.1"
    release_name       = "Strategy Memory UX"
    release_stage      = "STABLE"
    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False
    research_only      = True
    supported_modes    = ["real", "mock"]
    major_features     = [
        "Strategy Memory UX v0.8.1",
        "Status lifecycle: NEW→REVIEWING→VALIDATING→ACCEPTED/REJECTED/NEEDS_MORE_EVIDENCE",
        "accepted_is_research_only=True invariant — ACCEPTED ≠ trading enabled",
        "UX fields: needs_action, validation_ready, status_hint, next_step, last_action_at",
        "Safe command labels: SAFE_READ_ONLY/SAFE_REPORT/SAFE_REGRESSION/SAFE_REPLAY/SAFE_DATA_CHECK",
        "3 new CLI views: validation-queue, active-threads, repeated-patterns",
        "7-tab detail panel in GUI: Summary/Hypothesis/Evidence/Validation/Commands/Links/Safety",
        "Memory link improvements: target_title, why_linked, suggested_next_step",
        "Conservative duplicate detection (>80% similarity + same type + same module)",
        "Research/Coach integration: memory_summary/memory_items params",
        "Research Intelligence Stable v0.8.0",
        "Intelligence Stable Schema (29 capabilities)",
        "Intelligence Capability Matrix",
        "Intelligence Stable Checklist (7 categories)",
        "Intelligence Release Manifest Builder",
        "Intelligence Stable Engine + Store",
        "Intelligence Stable Report (11 sections)",
        "Intelligence Stable GUI Panel",
        "6 new CLI commands (intelligence-stable, etc.)",
        "Safety audit: recommendations/memories/coach tasks",
        "Forbidden action count = 0",
        "Research Intelligence Engine (v0.7.0)",
        "Research Intelligence UX Polish (v0.7.1)",
        "Strategy Research Memory (v0.7.2)",
        "Backtest-to-Coach Loop (v0.7.3)",
        "Research OS Stable Release v0.6.0",
        "Stable Capability Matrix (30+ capabilities)",
        "v0.6.0 Stable Release Checklist",
        "Release Manifest Builder",
        "Known Limitations Registry",
        "Stable Release Report",
        "Stable Release GUI Panel",
        "Daily Workflow Engine",
        "Data Quality Gate",
        "Provider Reliability & Fallback Matrix",
        "Universe Expansion & Sector Classification",
        "Hardened Backtest Engine",
        "Intraday / Tick Data Pipeline",
        "Strategy Rule Governance",
        "Research Notebook / Experiment Registry",
        "Auto Report Center",
        "Signal Quality Dashboard",
        "Rule Weight Tuning Lab",
        "Portfolio Cockpit",
        "Automation Scheduler",
        "Usability QA",
        "Release Status & Regression Suite",
        "Research OS Module Inventory",
        "Research OS CLI Inventory",
        "Research OS GUI Tab Inventory",
        "Research OS Regression Audit",
        "Research OS Artifact Hygiene",
        "Research OS Safety Matrix",
        "Research OS Stabilization Report",
        "CLI Command Registry",
        "CLI Alias Map (35 aliases)",
        "CLI Command Discovery",
        "CLI Help Examples",
        "CLI UX Report",
        "CLI UX GUI Panel",
        "GUI Tab Registry",
        "GUI Navigation Panel",
        "GUI Navigation Report",
    ]
    safety_flags = [
        "read_only=True",
        "no_real_orders=True",
        "production_blocked=True",
        "real_order_ready=False",
        "research_only=True",
        "no_broker_connection=True",
        "no_auto_weight_apply=True",
        "no_shioaji=True",
        "no_mega_broker=True",
    ]


def get_version_info() -> dict:
    """Return all VersionInfo fields as a dict."""
    return {
        "version":            VersionInfo.version,
        "release_name":       VersionInfo.release_name,
        "release_stage":      VersionInfo.release_stage,
        "read_only":          VersionInfo.read_only,
        "no_real_orders":     VersionInfo.no_real_orders,
        "production_blocked": VersionInfo.production_blocked,
        "real_order_ready":   VersionInfo.real_order_ready,
        "supported_modes":    VersionInfo.supported_modes,
        "major_features":     VersionInfo.major_features,
        "safety_flags":       VersionInfo.safety_flags,
    }


def print_version_info() -> None:
    """Print formatted version info to stdout."""
    info = get_version_info()
    print("=" * 60)
    print(f"  TW Quant Cockpit {info['version']}")
    print(f"  {info['release_name']}")
    print(f"  Stage: {info['release_stage']}")
    print("=" * 60)
    print(f"  Read Only          : {info['read_only']}")
    print(f"  No Real Orders     : {info['no_real_orders']}")
    print(f"  Production BLOCKED : {info['production_blocked']}")
    print(f"  Real Order Ready   : {info['real_order_ready']}")
    print(f"  Supported Modes    : {', '.join(info['supported_modes'])}")
    print()
    print("  Safety Flags:")
    for flag in info["safety_flags"]:
        print(f"    [{flag}]")
    print()
    print("  Major Features:")
    for i, feat in enumerate(info["major_features"], 1):
        print(f"    {i:2d}. {feat}")
    print("=" * 60)


def get_safety_banner() -> str:
    """Return one-line safety banner string."""
    return (
        "[!] v0.8.1 Research Only | No Real Orders | "
        "Production BLOCKED | real_order_ready=False"
    )


def get_feature_summary() -> str:
    """Return formatted multi-line feature list string."""
    lines = [
        f"TW Quant Cockpit {VersionInfo.version} — Major Features",
        "-" * 50,
    ]
    for i, feat in enumerate(VersionInfo.major_features, 1):
        lines.append(f"  {i:2d}. {feat}")
    lines.append("-" * 50)
    lines.append(
        f"Total: {len(VersionInfo.major_features)} features | "
        f"Stage: {VersionInfo.release_stage}"
    )
    return "\n".join(lines)
