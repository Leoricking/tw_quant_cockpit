"""
final_rollup/release_history.py — v1.0.x Release History for TW Quant Cockpit v1.0.9.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] VALIDATED does not enable trading. Final Maintenance Rollup.
"""
from __future__ import annotations

import logging
import os
from typing import List, Optional

from final_rollup.rollup_schema import ReleaseEntry

logger = logging.getLogger(__name__)


class ReleaseHistoryBuilder:
    """Builds the v1.0.x release history.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    Does not use git as the sole source — uses inline data.
    Tag existence is checked optionally; missing tag = WARN, not crash.
    """

    no_real_orders = True
    broker_disabled = True
    external_api_disabled = True

    _RELEASE_DATA = [
        {
            "version": "1.0.0",
            "title": "Research Trading Cockpit Stable",
            "commit": "1595e0c",
            "tag": "v1.0.0",
            "release_type": "STABLE_BASELINE",
            "summary": "First v1.0.x stable release. Research cockpit stable baseline, stable checklist, release notes.",
            "key_modules": ["release.research_cockpit_stable", "release.version_info"],
            "key_commands": ["research-cockpit-stable", "version-info"],
            "safety_status": "STABLE",
            "validation_summary": "59/59 PASS",
            "known_warnings": [],
        },
        {
            "version": "1.0.1",
            "title": "Maintenance & Polish",
            "commit": "9ce72d8",
            "tag": "v1.0.1",
            "release_type": "MAINTENANCE",
            "summary": "Maintenance flags, stable checklist accepts 1.0.x, docs maintenance polish.",
            "key_modules": ["release.version_info", "docs"],
            "key_commands": ["version-info", "research-cockpit-stable"],
            "safety_status": "STABLE",
            "validation_summary": "PASS",
            "known_warnings": [],
        },
        {
            "version": "1.0.2",
            "title": "Data & Report Hygiene",
            "commit": "1e03325",
            "tag": "v1.0.2",
            "release_type": "MAINTENANCE",
            "summary": "Data/report hygiene scanner, manifest, runtime output inventory.",
            "key_modules": ["maintenance.data_report_hygiene"],
            "key_commands": ["data-report-hygiene", "data-report-hygiene-summary"],
            "safety_status": "STABLE",
            "validation_summary": "PASS",
            "known_warnings": [],
        },
        {
            "version": "1.0.3",
            "title": "GUI Stability & Usability Polish",
            "commit": "ba94fd6",
            "tag": "v1.0.3",
            "release_type": "MAINTENANCE",
            "summary": "GUI safety helpers, health check, usability report.",
            "key_modules": ["gui.gui_health_check"],
            "key_commands": ["gui-health-check", "gui-usability-report"],
            "safety_status": "STABLE",
            "validation_summary": "PASS",
            "known_warnings": [],
        },
        {
            "version": "1.0.4",
            "title": "Regression & Release Gate Hardening",
            "commit": "0343b86",
            "tag": "v1.0.4",
            "release_type": "MAINTENANCE",
            "summary": "Safety scanner, release gate health, regression hardening.",
            "key_modules": ["maintenance.safety_scanner", "maintenance.release_gate_health"],
            "key_commands": ["release-gate-health", "safety-scan", "regression-hardening-summary"],
            "safety_status": "STABLE",
            "validation_summary": "448/448 PASS",
            "known_warnings": [],
        },
        {
            "version": "1.0.5",
            "title": "Documentation & User Guide Polish",
            "commit": "5011589",
            "tag": "v1.0.5",
            "release_type": "MAINTENANCE",
            "summary": "User guides, docs index, docs health check.",
            "key_modules": ["docs_health"],
            "key_commands": ["docs-health-check", "docs-index", "documentation-report"],
            "safety_status": "STABLE",
            "validation_summary": "PASS",
            "known_warnings": [],
        },
        {
            "version": "1.0.6",
            "title": "Example Workflows & Templates",
            "commit": "0340254",
            "tag": "v1.0.6",
            "release_type": "MAINTENANCE",
            "summary": "Example workflow templates, workflow health check.",
            "key_modules": ["docs.examples", "docs.templates"],
            "key_commands": ["workflow-templates-health", "workflow-templates-index"],
            "safety_status": "STABLE",
            "validation_summary": "PASS",
            "known_warnings": [],
        },
        {
            "version": "1.0.7",
            "title": "Knowledge Base Search Polish",
            "commit": "3f49de4",
            "tag": "v1.0.7",
            "release_type": "MAINTENANCE",
            "summary": "Local KB index, safe KB search, no external API.",
            "key_modules": ["knowledge_base.kb_indexer", "knowledge_base.kb_search_engine"],
            "key_commands": ["kb-index", "kb-health-check", "kb-search", "kb-report"],
            "safety_status": "STABLE",
            "validation_summary": "PASS",
            "known_warnings": [],
        },
        {
            "version": "1.0.8",
            "title": "Local Research Assistant Polish",
            "commit": "1342425",
            "tag": "v1.0.8",
            "release_type": "MAINTENANCE",
            "summary": "Local assistant, safe answers, unsafe query blocking. No external API.",
            "key_modules": ["local_assistant.local_assistant_engine", "local_assistant.safe_answer_builder"],
            "key_commands": ["local-assistant", "local-assistant-health", "local-assistant-report"],
            "safety_status": "STABLE",
            "validation_summary": "11/11 PASS",
            "known_warnings": [],
        },
        {
            "version": "1.0.9",
            "title": "Final Maintenance Rollup",
            "commit": "current",
            "tag": "v1.0.9",
            "release_type": "FINAL_ROLLUP",
            "summary": "Final v1.0.x maintenance rollup: release history, final health checks, smoke summaries, long-term maintenance plan.",
            "key_modules": ["final_rollup.final_rollup_engine", "final_rollup.release_history"],
            "key_commands": ["final-rollup", "final-rollup-history", "final-rollup-health", "final-rollup-maintenance-plan"],
            "safety_status": "STABLE",
            "validation_summary": "v1.0 Maintenance Line Complete",
            "known_warnings": [],
        },
    ]

    def __init__(self, project_root: Optional[str] = None) -> None:
        self._root = project_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def build(self) -> List[ReleaseEntry]:
        """Build and return the full v1.0.x release history."""
        entries = []
        for d in self._RELEASE_DATA:
            entry = ReleaseEntry(
                version=d["version"],
                title=d["title"],
                commit=d["commit"],
                tag=d["tag"],
                release_type=d["release_type"],
                summary=d["summary"],
                key_modules=d.get("key_modules", []),
                key_commands=d.get("key_commands", []),
                safety_status=d.get("safety_status", "STABLE"),
                validation_summary=d.get("validation_summary", ""),
                known_warnings=d.get("known_warnings", []),
                no_real_orders=True,
                broker_disabled=True,
                validated_does_not_enable_trading=True,
            )
            # Check tag existence (warn, don't crash)
            tag_status = self._check_tag(entry.tag)
            if tag_status != "OK":
                if entry.known_warnings is None:
                    entry.known_warnings = []
                entry.known_warnings.append(f"tag {entry.tag}: {tag_status}")
            entries.append(entry)
        return entries

    def _check_tag(self, tag: str) -> str:
        """Check if a git tag exists. Returns 'OK' or a warning string."""
        try:
            import subprocess
            result = subprocess.run(
                ["git", "-C", self._root, "rev-parse", "--verify", tag],
                capture_output=True, text=True, timeout=5,
            )
            if result.returncode == 0:
                return "OK"
            return f"tag not found (git: {result.stderr.strip()[:60]})"
        except Exception as exc:
            return f"tag check skipped: {exc}"

    def get_summary(self) -> dict:
        """Return a summary dict of the release history."""
        entries = self.build()
        return {
            "total_releases": len(entries),
            "versions": [e.version for e in entries],
            "latest": entries[-1].version if entries else "",
            "no_real_orders": True,
            "broker_disabled": True,
            "external_api_disabled": True,
        }
