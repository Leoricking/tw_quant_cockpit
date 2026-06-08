"""
strategy_lab/strategy_lab_release_manifest.py — StrategyLabReleaseManifestBuilder v0.9.0

Generates the v0.9.0 Strategy Lab release manifest (JSON + Markdown).

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice. No BUY/SELL/ORDER output.
"""
from __future__ import annotations

import json
import logging
import os
import subprocess
from datetime import datetime

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_DEFAULT_OUTPUT_DIR = "data/backtest_results/strategy_lab"


class StrategyLabReleaseManifestBuilder:
    """Builds v0.9.0 Strategy Lab release manifest.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(self, output_dir: str = _DEFAULT_OUTPUT_DIR) -> None:
        if os.path.isabs(output_dir):
            self._out_dir = output_dir
        else:
            self._out_dir = os.path.join(BASE_DIR, output_dir)

    def build_manifest(self, version: str = "v0.9.0") -> dict:
        """Build and save manifest. Returns manifest dict."""
        manifest = self._build_dict(version)
        self._save_json(manifest, version)
        self._save_markdown(manifest, version)
        return manifest

    # ------------------------------------------------------------------
    # Internal: build dict
    # ------------------------------------------------------------------

    def _build_dict(self, version: str) -> dict:
        commit_hash = self._get_git_commit()
        tag         = self._get_git_tag()
        cap_summary = self._get_capability_summary()
        chk_summary = self._get_check_summary()
        report_paths = self._get_report_paths()

        return {
            "version":          version,
            "release_name":     "Strategy Lab Stable",
            "commit_hash":      commit_hash,
            "tag":              tag,
            "previous_version": "v0.8.3",
            "generated_at":     datetime.now().isoformat(),
            "capability_summary": cap_summary,
            "checklist_summary":  chk_summary,
            "safety_summary": {
                "no_real_orders":        True,
                "production_blocked":    True,
                "real_order_ready":      False,
                "broker_connected":      False,
                "auto_trading":          False,
                "forbidden_action_count": 0,
                "research_only":         True,
                "not_investment_advice": True,
            },
            "known_limitations": [
                "No investment advice — all outputs are research tasks only",
                "No automatic strategy activation",
                "No live order execution — production trading is BLOCKED",
                "Provider token environment limits may affect some reports",
                "Optional reports may be missing if not yet generated",
                "Backtest quality depends on data coverage",
                "Evidence graph quality depends on available research outputs",
                "Training metrics may show INSUFFICIENT_DATA until enough history accumulates",
            ],
            "report_paths":      report_paths,
            "no_real_orders":    True,
            "production_blocked": True,
        }

    # ------------------------------------------------------------------
    # Internal: git info
    # ------------------------------------------------------------------

    def _get_git_commit(self) -> str:
        try:
            result = subprocess.run(
                ["git", "-C", BASE_DIR, "rev-parse", "--short", "HEAD"],
                capture_output=True, text=True, timeout=10,
            )
            return result.stdout.strip() if result.returncode == 0 else "unknown"
        except Exception:
            return "unknown"

    def _get_git_tag(self) -> str:
        try:
            result = subprocess.run(
                ["git", "-C", BASE_DIR, "describe", "--tags", "--exact-match"],
                capture_output=True, text=True, timeout=10,
            )
            return result.stdout.strip() if result.returncode == 0 else "v0.9.0"
        except Exception:
            return "v0.9.0"

    # ------------------------------------------------------------------
    # Internal: summaries
    # ------------------------------------------------------------------

    def _get_capability_summary(self) -> dict:
        try:
            from strategy_lab.strategy_lab_store import StrategyLabStore
            store = StrategyLabStore(output_dir=self._out_dir)
            caps  = store.load_capabilities()
            if caps:
                stable  = sum(1 for c in caps if c.get("stable_status") == "STABLE")
                usable  = sum(1 for c in caps if c.get("stable_status") == "USABLE")
                partial = len(caps) - stable - usable
                return {"total": len(caps), "stable": stable, "usable": usable, "partial": partial}
        except Exception as exc:
            logger.debug("StrategyLabReleaseManifestBuilder._get_capability_summary: %s", exc)
        return {"total": 0, "stable": 0, "usable": 0, "partial": 0}

    def _get_check_summary(self) -> dict:
        try:
            from strategy_lab.strategy_lab_store import StrategyLabStore
            store  = StrategyLabStore(output_dir=self._out_dir)
            checks = store.load_latest_checks()
            if checks:
                passes = sum(1 for c in checks if c.get("status") == "PASS")
                warns  = sum(1 for c in checks if c.get("status") == "WARN")
                fails  = sum(1 for c in checks if c.get("status") == "FAIL")
                blk    = sum(1 for c in checks if c.get("status") == "BLOCKED")
                return {"total": len(checks), "pass": passes, "warn": warns,
                        "fail": fails, "blocked": blk}
        except Exception as exc:
            logger.debug("StrategyLabReleaseManifestBuilder._get_check_summary: %s", exc)
        return {"total": 0, "pass": 0, "warn": 0, "fail": 0, "blocked": 0}

    def _get_report_paths(self) -> dict:
        import glob
        reports_dir = os.path.join(BASE_DIR, "reports")
        paths: dict = {}
        patterns = {
            "strategy_lab_stable_report": "strategy_lab_stable_report_*.md",
            "intelligence_stable_report": "intelligence_stable_report_*.md",
            "evidence_graph_report":      "evidence_graph_report_*.md",
            "training_metrics_report":    "training_metrics_report_*.md",
        }
        for key, pat in patterns.items():
            files = sorted(glob.glob(os.path.join(reports_dir, pat)))
            paths[key] = files[-1] if files else ""
        return paths

    # ------------------------------------------------------------------
    # Internal: save
    # ------------------------------------------------------------------

    def _save_json(self, manifest: dict, version: str) -> str:
        os.makedirs(self._out_dir, exist_ok=True)
        fname = f"strategy_lab_release_manifest_{version}.json"
        path  = os.path.join(self._out_dir, fname)
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(manifest, f, indent=2, ensure_ascii=False)
            logger.info("StrategyLabReleaseManifestBuilder: JSON -> %s", path)
        except Exception as exc:
            logger.warning("StrategyLabReleaseManifestBuilder._save_json: %s", exc)
        return path

    def _save_markdown(self, manifest: dict, version: str) -> str:
        lines = [
            f"# Strategy Lab Release Manifest {version}",
            "",
            "> **[!] Research Only. No Real Orders. Production Trading BLOCKED.**",
            "",
            f"**Version:** {manifest['version']}",
            f"**Release Name:** {manifest['release_name']}",
            f"**Previous Version:** {manifest['previous_version']}",
            f"**Commit:** {manifest['commit_hash']}",
            f"**Tag:** {manifest['tag']}",
            f"**Generated At:** {manifest['generated_at']}",
            "",
            "## Capability Summary",
            "",
            f"- Total: {manifest['capability_summary'].get('total', 0)}",
            f"- STABLE: {manifest['capability_summary'].get('stable', 0)}",
            f"- USABLE: {manifest['capability_summary'].get('usable', 0)}",
            f"- PARTIAL/OTHER: {manifest['capability_summary'].get('partial', 0)}",
            "",
            "## Checklist Summary",
            "",
            f"- Total: {manifest['checklist_summary'].get('total', 0)}",
            f"- PASS: {manifest['checklist_summary'].get('pass', 0)}",
            f"- WARN: {manifest['checklist_summary'].get('warn', 0)}",
            f"- FAIL: {manifest['checklist_summary'].get('fail', 0)}",
            f"- BLOCKED: {manifest['checklist_summary'].get('blocked', 0)}",
            "",
            "## Safety Summary",
            "",
            "| Safety Item | Value |",
            "|-------------|-------|",
            "| No Real Orders | True |",
            "| Production Trading | BLOCKED |",
            "| Real Order Ready | False |",
            "| Broker Connected | False |",
            "| Auto Trading | False |",
            "| Forbidden Action Count | 0 |",
            "| Research Only | True |",
            "| Not Investment Advice | True |",
            "",
            "## Known Limitations",
            "",
        ]
        for lim in manifest.get("known_limitations", []):
            lines.append(f"- {lim}")
        lines += [
            "",
            "---",
            "",
            "> **Research Only** — No Real Orders — Production Trading BLOCKED — Not Investment Advice",
            "",
        ]

        os.makedirs(self._out_dir, exist_ok=True)
        fname = f"strategy_lab_release_manifest_{version}.md"
        path  = os.path.join(self._out_dir, fname)
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            logger.info("StrategyLabReleaseManifestBuilder: Markdown -> %s", path)
        except Exception as exc:
            logger.warning("StrategyLabReleaseManifestBuilder._save_markdown: %s", exc)
        return path
