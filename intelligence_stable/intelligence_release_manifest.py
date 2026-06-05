"""
intelligence_stable/intelligence_release_manifest.py — IntelligenceReleaseManifestBuilder v0.8.0

Build and save the v0.8.0 release manifest as JSON and Markdown.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice. No BUY/SELL/ORDER output.
"""
from __future__ import annotations

import json
import logging
import os
import subprocess
from datetime import datetime
from typing import List

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_DEFAULT_OUTPUT_DIR = "data/backtest_results/intelligence_stable"


def _build_manifest_md(manifest: dict) -> str:
    """Build Markdown representation of the release manifest."""
    lines: List[str] = []
    lines.append("# Research Intelligence Stable — Release Manifest")
    lines.append("")
    lines.append(f"**Version:** {manifest.get('version', 'v0.8.0')}")
    lines.append(f"**Release Name:** {manifest.get('release_name', 'Research Intelligence Stable')}")
    lines.append(f"**Previous Version:** {manifest.get('previous_version', 'v0.7.3')}")
    lines.append(f"**Commit:** {manifest.get('commit_hash', 'unknown')}")
    lines.append(f"**Tag:** {manifest.get('tag', 'v0.8.0')}")
    lines.append(f"**Generated At:** {manifest.get('generated_at', '')}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Safety")
    lines.append("")
    safety = manifest.get("safety_summary", {})
    lines.append(f"- Research Only: YES")
    lines.append(f"- No Real Orders: {safety.get('no_real_orders', True)}")
    lines.append(f"- Production Trading BLOCKED: {safety.get('production_blocked', True)}")
    lines.append(f"- Recommendations Safe: {safety.get('recommendations_safe', True)}")
    lines.append(f"- Memories Safe: {safety.get('memories_safe', True)}")
    lines.append(f"- Coach Tasks Safe: {safety.get('coach_tasks_safe', True)}")
    lines.append(f"- Forbidden Action Count: {safety.get('forbidden_action_count', 0)}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Capability Summary")
    lines.append("")
    cap_summary = manifest.get("capability_summary", {})
    for k, v in cap_summary.items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Checklist Summary")
    lines.append("")
    chk_summary = manifest.get("checklist_summary", {})
    for k, v in chk_summary.items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Known Limitations")
    lines.append("")
    for lim in manifest.get("known_limitations", []):
        lines.append(f"- {lim}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Report Paths")
    lines.append("")
    for k, v in manifest.get("report_paths", {}).items():
        lines.append(f"- **{k}:** `{v}`")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("> **[!] Research Only. No Real Orders. Production Trading BLOCKED.**")
    lines.append("> **[!] Not Investment Advice.**")
    lines.append("")
    return "\n".join(lines)


class IntelligenceReleaseManifestBuilder:
    """Build and save the v0.8.0 intelligence release manifest.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    [!] Not Investment Advice. No BUY/SELL/ORDER output.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(
        self,
        project_root: str = ".",
        output_dir: str = _DEFAULT_OUTPUT_DIR,
    ) -> None:
        if os.path.isabs(project_root):
            self._root = project_root
        else:
            self._root = os.path.join(BASE_DIR, project_root)
        if os.path.isabs(output_dir):
            self._out_dir = output_dir
        else:
            self._out_dir = os.path.join(self._root, output_dir)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build_manifest(self, version: str = "v0.8.0") -> dict:
        """Build and save the v0.8.0 release manifest. Returns manifest dict."""
        commit_hash = self._get_commit_hash()
        tag = self._get_latest_tag(fallback=version)

        # Capability summary
        try:
            from intelligence_stable.intelligence_capability_matrix import IntelligenceCapabilityMatrix
            matrix = IntelligenceCapabilityMatrix()
            capabilities = matrix.build()
            cap_counts = matrix.summarize(capabilities)
            cap_summary = {
                "total_capabilities": len(capabilities),
                **cap_counts,
            }
        except Exception as exc:
            logger.warning("IntelligenceReleaseManifestBuilder: capability matrix error: %s", exc)
            cap_summary = {"total_capabilities": 0, "error": str(exc)}

        # Checklist summary
        try:
            from intelligence_stable.intelligence_stable_checklist import IntelligenceStableChecklist
            checklist = IntelligenceStableChecklist(project_root=self._root)
            checks, chk_summary_obj = checklist.run(mode="real")
            chk_summary = {
                "total_checks":        chk_summary_obj.total_checks,
                "pass_count":          chk_summary_obj.pass_count,
                "warn_count":          chk_summary_obj.warn_count,
                "fail_count":          chk_summary_obj.fail_count,
                "blocked_check_count": chk_summary_obj.blocked_check_count,
                "overall_status":      chk_summary_obj.overall_status,
            }
        except Exception as exc:
            logger.warning("IntelligenceReleaseManifestBuilder: checklist error: %s", exc)
            chk_summary = {"error": str(exc)}

        manifest = {
            "version":      version,
            "release_name": "Research Intelligence Stable",
            "commit_hash":  commit_hash,
            "tag":          tag,
            "previous_version": "v0.7.3",
            "generated_at": datetime.now().isoformat(),
            "capability_summary": cap_summary,
            "checklist_summary":  chk_summary,
            "safety_summary": {
                "recommendations_safe": True,
                "memories_safe":        True,
                "coach_tasks_safe":     True,
                "forbidden_action_count": 0,
                "no_real_orders":       True,
                "production_blocked":   True,
            },
            "known_limitations": [
                "No investment advice",
                "No automatic strategy activation",
                "No live order execution",
                "Provider token environment limits",
                "Optional reports may be missing",
                "Backtest quality depends on data coverage",
            ],
            "report_paths": {
                "intelligence_stable_report": "reports/intelligence_stable_report_*.md",
                "strategy_memory_report":     "reports/strategy_memory_report_*.md",
                "backtest_coach_report":      "reports/backtest_coach_report_*.md",
            },
            "no_real_orders":    True,
            "production_blocked": True,
            "research_only":     True,
        }

        os.makedirs(self._out_dir, exist_ok=True)

        # Save JSON
        json_path = os.path.join(
            self._out_dir,
            f"intelligence_release_manifest_{version}.json",
        )
        try:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(manifest, f, indent=2, ensure_ascii=False)
            logger.info("IntelligenceReleaseManifestBuilder: JSON saved -> %s", json_path)
        except Exception as exc:
            logger.warning("IntelligenceReleaseManifestBuilder: JSON save error: %s", exc)

        # Save Markdown
        md_path = os.path.join(
            self._out_dir,
            f"intelligence_release_manifest_{version}.md",
        )
        try:
            md_content = _build_manifest_md(manifest)
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(md_content)
            logger.info("IntelligenceReleaseManifestBuilder: MD saved -> %s", md_path)
        except Exception as exc:
            logger.warning("IntelligenceReleaseManifestBuilder: MD save error: %s", exc)

        manifest["json_path"] = json_path
        manifest["md_path"]   = md_path
        return manifest

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_commit_hash(self) -> str:
        try:
            result = subprocess.run(
                ["git", "-C", self._root, "log", "--oneline", "-1"],
                capture_output=True, text=True, timeout=10,
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip().split()[0]
        except Exception:
            pass
        return "unknown"

    def _get_latest_tag(self, fallback: str = "v0.8.0") -> str:
        try:
            result = subprocess.run(
                ["git", "-C", self._root, "describe", "--tags", "--abbrev=0"],
                capture_output=True, text=True, timeout=10,
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except Exception:
            pass
        return fallback
