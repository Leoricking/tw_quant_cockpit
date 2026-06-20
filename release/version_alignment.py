"""
release/version_alignment.py — Canonical version mapping for TW Quant Cockpit.

The research validation features (Empirical Backtest, A/B/C Validation, and
Strategy Robustness) were originally developed under internal v1.4.x labels.
After roadmap alignment, these releases are canonically part of the v1.3.x
Research Data & Strategy Validation Foundation line.  The v1.4.x label space is
reserved for the Public Data Provider Integration roadmap.

This module provides:
- Canonical version mapping from old internal labels to aligned labels
- Semantic version parsing helper
- Release lineage helper
- Forward-compatible snapshot enrichment (read-only; never rewrites payloads)

[!] Research Only. No Real Orders. Not Investment Advice.
[!] This module only adds metadata. It never modifies existing payloads,
    reproducibility hashes, or Git history.
"""
from __future__ import annotations

from typing import Optional

# ---------------------------------------------------------------------------
# Canonical mapping: old internal version → canonical aligned version
# ---------------------------------------------------------------------------
# Original internal labels were assigned before the public-provider roadmap
# was finalised.  These mappings are purely for display, query, and
# compatibility enrichment — they do NOT rewrite any stored data.
_CANONICAL_MAP: dict[str, str] = {
    "1.4.0": "1.3.5",   # Strategy Knowledge Empirical Backtest
    "1.4.1": "1.3.6",   # A/B/C Buy Point Validation
    "1.4.2": "1.3.7",   # Strategy Robustness & Regime Validation
}

# Hotfix mapping (commit-level precision)
_HOTFIX_MAP: dict[str, str] = {
    "f418de5": "1.3.6.1",  # Freshness Date Stability Hotfix
}

# Release names by canonical version
_RELEASE_NAMES: dict[str, str] = {
    "1.3.0": "Real Data Quality Foundation",
    "1.3.1": "Universe Expansion Foundation",
    "1.3.2": "Real Data Provider Adapter Foundation",
    "1.3.3": "Coverage Repair Workflow",
    "1.3.4": "Data Freshness Monitor",
    "1.3.5": "Strategy Knowledge Empirical Backtest",
    "1.3.6": "A/B/C Buy Point Validation",
    "1.3.6.1": "Freshness Date Stability Hotfix",
    "1.3.7": "Strategy Robustness & Regime Validation",
    "1.3.9": "Research Foundation Stable Rollup",
    # v1.4.x reserved for Public Data Provider Integration
    "1.4.0": "TWSE Provider",
    "1.4.1": "TPEx Provider",
    "1.4.2": "MOPS Provider",
    "1.4.3": "data.gov.tw Provider",
    "1.4.4": "FinMind Adapter Hardening",
    "1.4.5": "Source Lineage & Rate Limit",
    "1.4.6": "Provider Quality Gates",
    "1.4.7": "Forum Intelligence & Market Sentiment",
    "1.4.9": "Data Provider Stable Rollup",
}


def canonical_version(internal_version: str) -> str:
    """
    Return the canonical aligned version for an internal version label.
    If no mapping exists, returns the input unchanged.

    Parameters
    ----------
    internal_version : str
        e.g. "1.4.0", "1.4.1", "1.3.7"

    Returns
    -------
    str
        Canonical version string, e.g. "1.3.5".
    """
    return _CANONICAL_MAP.get(internal_version, internal_version)


def hotfix_canonical_version(commit_hash: str) -> Optional[str]:
    """
    Return canonical version for a hotfix commit, or None if unknown.
    """
    return _HOTFIX_MAP.get(commit_hash)


def release_name_for_version(version: str) -> Optional[str]:
    """
    Return the release name for a canonical version, or None if unknown.
    """
    return _RELEASE_NAMES.get(version)


def enrich_payload(payload: dict) -> dict:
    """
    Return a new dict with canonical metadata added.
    NEVER modifies the original payload dict.
    NEVER overwrites any existing key.

    Adds (only if not already present):
    - canonical_release_version
    - version_alignment_note

    Parameters
    ----------
    payload : dict
        Any stored result dict that may contain an ``application_version`` key.

    Returns
    -------
    dict
        New dict with original data plus optional enrichment keys.
    """
    enriched = dict(payload)
    app_ver = enriched.get("application_version") or enriched.get("schema_version", "")
    canonical = _CANONICAL_MAP.get(str(app_ver))
    if canonical and "canonical_release_version" not in enriched:
        enriched["canonical_release_version"] = canonical
        enriched.setdefault(
            "version_alignment_note",
            (
                f"Originally developed under internal version label {app_ver}. "
                f"Canonical roadmap version: {canonical}. "
                "Git commit history is unchanged."
            ),
        )
    return enriched


def parse_version(version_str: str) -> tuple[int, ...]:
    """
    Parse a version string into a tuple of ints for comparison.
    Non-numeric parts are dropped gracefully.

    >>> parse_version("1.3.7") == (1, 3, 7)
    True
    >>> parse_version("1.3.6.1") == (1, 3, 6, 1)
    True
    """
    parts = []
    for part in version_str.split("."):
        try:
            parts.append(int(part))
        except ValueError:
            break
    return tuple(parts)


def is_version_at_least(version_str: str, minimum: str) -> bool:
    """
    Return True if version_str >= minimum (semantic comparison).
    """
    return parse_version(version_str) >= parse_version(minimum)


def load_snapshot_gracefully(data: dict) -> dict:
    """
    Load a stored payload gracefully.  Unknown fields are preserved.
    Old application_version values (1.4.0, 1.4.1, 1.4.2) are accepted.
    Returns enriched payload (does not modify input).
    """
    return enrich_payload(data)
