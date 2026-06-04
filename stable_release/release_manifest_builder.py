"""stable_release/release_manifest_builder.py — ReleaseManifestBuilder for v0.6.0.

Builds release_manifest_v0.6.0.json and release_manifest_v0.6.0.md.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import json
import logging
import os
import subprocess
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_OUTPUT_DIR = os.path.join(BASE_DIR, "data", "backtest_results", "stable_release")


class ReleaseManifestBuilder:
    """Builds release manifest JSON and Markdown for v0.6.0.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    VERSION = "v0.6.0"

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def build_manifest(self, version: str = "v0.6.0") -> dict:
        """Build the release manifest. Returns paths and summary."""
        os.makedirs(_OUTPUT_DIR, exist_ok=True)

        commit_hash = self._get_commit_hash()
        capability_summary = self._get_capability_summary()
        checklist_summary = self._get_checklist_summary()
        limitations_count = self._get_limitations_count()

        manifest = {
            "version":            version,
            "release_name":       "Research OS Stable Release",
            "release_type":       "stable",
            "created_at":         datetime.now().isoformat(),
            "previous_version":   "v0.5.6",
            "branch":             "main",
            "commit_hash":        commit_hash,
            "tag":                version,
            "status":             "STABLE",
            # Safety flags
            "research_only":      True,
            "no_real_orders":     True,
            "production_blocked": True,
            "real_order_ready":   False,
            # Capability summary
            "capability_count":        capability_summary.get("total", 0),
            "stable_count":            capability_summary.get("stable_count", 0),
            "usable_count":            capability_summary.get("usable_count", 0),
            "partial_count":           capability_summary.get("partial_count", 0),
            "experimental_count":      capability_summary.get("experimental_count", 0),
            # Checklist / Status
            "regression_status":       checklist_summary.get("regression_status", "UNKNOWN"),
            "safety_status":           "BLOCKED — Research Only",
            "report_pack_status":      checklist_summary.get("report_pack_status", "UNKNOWN"),
            "checklist_overall":       checklist_summary.get("overall_status", "UNKNOWN"),
            "checklist_total":         checklist_summary.get("total_checks", 0),
            "checklist_passed":        checklist_summary.get("pass_count", 0),
            "checklist_warnings":      checklist_summary.get("warning_count", 0),
            "checklist_failed":        checklist_summary.get("fail_count", 0),
            # Limitations
            "known_limitations_count": limitations_count,
            # Paths
            "output_dir":         _OUTPUT_DIR,
        }

        json_path = os.path.join(_OUTPUT_DIR, f"release_manifest_{version}.json")
        md_path   = os.path.join(_OUTPUT_DIR, f"release_manifest_{version}.md")

        manifest["output_paths"] = {
            "json": json_path,
            "markdown": md_path,
        }

        # Write JSON
        try:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(manifest, f, ensure_ascii=False, indent=2)
            logger.info("[ReleaseManifestBuilder] JSON → %s", json_path)
        except Exception as exc:
            logger.error("[ReleaseManifestBuilder] JSON write error: %s", exc)
            json_path = ""

        # Write Markdown
        try:
            md_content = self._build_markdown(manifest, version)
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(md_content)
            logger.info("[ReleaseManifestBuilder] Markdown → %s", md_path)
        except Exception as exc:
            logger.error("[ReleaseManifestBuilder] Markdown write error: %s", exc)
            md_path = ""

        print("=" * 60)
        print("  TW Quant Cockpit — Research OS Stable Release v0.6.0")
        print("  [!] Research Only | No Real Orders | Production BLOCKED")
        print("=" * 60)
        print(f"  Release Manifest Built")
        print(f"  Version   : {version}")
        print(f"  Commit    : {commit_hash[:12] if commit_hash else 'N/A'}")
        print(f"  JSON      : {json_path}")
        print(f"  Markdown  : {md_path}")
        print(f"  Capabilities : {manifest['capability_count']}")
        print(f"  STABLE       : {manifest['stable_count']}")
        print(f"  Checklist    : {manifest['checklist_overall']}")
        print("=" * 60)

        return {
            "version":          version,
            "json_path":        json_path,
            "markdown_path":    md_path,
            "commit_hash":      commit_hash,
            "capability_count": manifest["capability_count"],
            "stable_count":     manifest["stable_count"],
            "overall_status":   manifest["checklist_overall"],
            "no_real_orders":   True,
            "production_blocked": True,
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _get_commit_hash(self) -> str:
        try:
            result = subprocess.run(
                ["git", "-C", BASE_DIR, "rev-parse", "--short", "HEAD"],
                capture_output=True, text=True, timeout=10,
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
        return "unknown"

    def _get_capability_summary(self) -> dict:
        try:
            from stable_release.capability_matrix import StableCapabilityMatrix
            matrix = StableCapabilityMatrix()
            matrix.build()
            caps = matrix.list_capabilities()
            by_status: dict[str, int] = {}
            for c in caps:
                by_status[c.status] = by_status.get(c.status, 0) + 1
            return {
                "total":             len(caps),
                "stable_count":      by_status.get("STABLE", 0),
                "usable_count":      by_status.get("USABLE", 0),
                "partial_count":     by_status.get("PARTIAL", 0),
                "experimental_count": by_status.get("EXPERIMENTAL", 0),
            }
        except Exception as exc:
            logger.warning("[ReleaseManifestBuilder] capability summary error: %s", exc)
            return {}

    def _get_checklist_summary(self) -> dict:
        try:
            from stable_release.stable_release_checklist_v060 import StableReleaseChecklistV060
            result = StableReleaseChecklistV060().run(mode="real")
            return result
        except Exception as exc:
            logger.warning("[ReleaseManifestBuilder] checklist summary error: %s", exc)
            return {}

    def _get_limitations_count(self) -> int:
        try:
            from stable_release.known_limitations import _LIMITATIONS
            return len(_LIMITATIONS)
        except Exception:
            return 11

    def _build_markdown(self, manifest: dict, version: str) -> str:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines = [
            f"# TW Quant Cockpit — Release Manifest {version}",
            "",
            f"> **[!] Research Only. No Real Orders. Production Trading: BLOCKED.**",
            f"> **Generated:** {now}",
            "",
            "---",
            "",
            "## Release Info",
            "",
            f"| Field | Value |",
            f"|-------|-------|",
            f"| Version | {manifest.get('version', 'N/A')} |",
            f"| Release Name | {manifest.get('release_name', 'N/A')} |",
            f"| Release Type | {manifest.get('release_type', 'N/A')} |",
            f"| Created At | {manifest.get('created_at', 'N/A')} |",
            f"| Previous Version | {manifest.get('previous_version', 'N/A')} |",
            f"| Branch | {manifest.get('branch', 'N/A')} |",
            f"| Commit Hash | {manifest.get('commit_hash', 'N/A')} |",
            f"| Tag | {manifest.get('tag', 'N/A')} |",
            f"| Status | {manifest.get('status', 'N/A')} |",
            "",
            "## Safety Flags",
            "",
            f"| Flag | Value |",
            f"|------|-------|",
            f"| research_only | {manifest.get('research_only', True)} |",
            f"| no_real_orders | {manifest.get('no_real_orders', True)} |",
            f"| production_blocked | {manifest.get('production_blocked', True)} |",
            f"| real_order_ready | {manifest.get('real_order_ready', False)} |",
            "",
            "## Capability Summary",
            "",
            f"| Status | Count |",
            f"|--------|-------|",
            f"| Total | {manifest.get('capability_count', 0)} |",
            f"| STABLE | {manifest.get('stable_count', 0)} |",
            f"| USABLE | {manifest.get('usable_count', 0)} |",
            f"| PARTIAL | {manifest.get('partial_count', 0)} |",
            f"| EXPERIMENTAL | {manifest.get('experimental_count', 0)} |",
            "",
            "## Checklist Status",
            "",
            f"| Check | Value |",
            f"|-------|-------|",
            f"| Overall Status | {manifest.get('checklist_overall', 'N/A')} |",
            f"| Total Checks | {manifest.get('checklist_total', 0)} |",
            f"| Passed | {manifest.get('checklist_passed', 0)} |",
            f"| Warnings | {manifest.get('checklist_warnings', 0)} |",
            f"| Failed | {manifest.get('checklist_failed', 0)} |",
            f"| Known Limitations | {manifest.get('known_limitations_count', 0)} |",
            "",
            "---",
            "",
            f"*Generated by TW Quant Cockpit {version} — Research Only / No Real Orders / Production Trading BLOCKED*",
            "",
        ]
        return "\n".join(lines)
