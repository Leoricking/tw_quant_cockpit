"""
release/version_info.py — Centralized version info for TW Quant Cockpit (v0.5.0).
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations
import logging
import os

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class VersionInfo:
    """Centralized version and safety metadata for v0.5.1."""

    version            = "v0.5.1"
    release_name       = "CLI Alias / Command UX Polish"
    release_stage      = "cli_ux_polish"
    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False
    supported_modes    = ["real", "mock"]
    major_features     = [
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
    ]
    safety_flags = [
        "read_only=True",
        "no_real_orders=True",
        "production_blocked=True",
        "real_order_ready=False",
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
        "[!] v0.5.1 Research Only | No Real Orders | "
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
