"""stable_release/stable_release_schema.py — Dataclass schema for v0.6.0 Stable Release.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class StableReleaseInfo:
    """Metadata for a TW Quant Cockpit stable release.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    version: str
    release_name: str
    release_type: str
    created_at: str
    previous_version: str
    branch: str
    commit_hash: str
    tag: str
    status: str
    research_only: bool = True
    no_real_orders: bool = True
    production_blocked: bool = True
    real_order_ready: bool = False
    known_limitations: List[str] = field(default_factory=list)
    blockers: List[str] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> dict:
        return {
            "version":            self.version,
            "release_name":       self.release_name,
            "release_type":       self.release_type,
            "created_at":         self.created_at,
            "previous_version":   self.previous_version,
            "branch":             self.branch,
            "commit_hash":        self.commit_hash,
            "tag":                self.tag,
            "status":             self.status,
            "research_only":      self.research_only,
            "no_real_orders":     self.no_real_orders,
            "production_blocked": self.production_blocked,
            "real_order_ready":   self.real_order_ready,
            "known_limitations":  self.known_limitations,
            "blockers":           self.blockers,
            "notes":              self.notes,
        }


@dataclass
class StableCapability:
    """A single capability entry in the stable capability matrix.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    capability_id: str
    name: str
    category: str  # data/provider/strategy/replay/journal/coach/review/workflow/report/regression/gui/cli/research_os/safety
    version_added: str
    status: str  # STABLE/USABLE/PARTIAL/EXPERIMENTAL/BLOCKED/DEPRECATED
    maturity: str
    cli_commands: List[str] = field(default_factory=list)
    gui_tabs: List[str] = field(default_factory=list)
    reports: List[str] = field(default_factory=list)
    regression_coverage: bool = False
    safety_status: str = "OK"
    known_limitations: List[str] = field(default_factory=list)
    no_real_orders: bool = True
    production_blocked: bool = True

    def to_dict(self) -> dict:
        return {
            "capability_id":      self.capability_id,
            "name":               self.name,
            "category":           self.category,
            "version_added":      self.version_added,
            "status":             self.status,
            "maturity":           self.maturity,
            "cli_commands":       self.cli_commands,
            "gui_tabs":           self.gui_tabs,
            "reports":            self.reports,
            "regression_coverage": self.regression_coverage,
            "safety_status":      self.safety_status,
            "known_limitations":  self.known_limitations,
            "no_real_orders":     self.no_real_orders,
            "production_blocked": self.production_blocked,
        }
