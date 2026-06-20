"""
reports/research_foundation_stable_rollup_report.py
Research Foundation Stable Rollup Report generator for v1.3.9.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] This report is generated at runtime. Do NOT commit generated output.
"""
from __future__ import annotations

import datetime
from typing import Any


class ResearchFoundationStableRollupReport:
    """
    Generates Research Foundation Stable Rollup Report v1.3.9.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    REPORT_TITLE = "Research Foundation Stable Rollup Report v1.3.9"

    def generate(self) -> dict:
        return {
            "title": self.REPORT_TITLE,
            "overview": self._overview(),
            "stable_capabilities": self._stable_capabilities(),
            "capability_dependencies": self._capability_dependencies(),
            "health_summary": self._health_summary(),
            "compatibility": self._compatibility(),
            "regression": self._regression(),
            "runtime_hygiene": self._runtime_hygiene(),
            "safety": self._safety(),
            "planned_provider_phase": self._planned_provider_phase(),
            "final_readiness": self._final_readiness(),
            "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
            "research_only": True,
            "no_real_orders": True,
        }

    def _overview(self) -> dict:
        try:
            from release.version_info import VERSION, RELEASE_NAME, BASE_RELEASE, REPLAY_STABLE_BASELINE
            import subprocess, os
            try:
                git_result = subprocess.run(
                    ["git", "rev-parse", "--short", "HEAD"],
                    capture_output=True, text=True,
                    cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                )
                git_commit = git_result.stdout.strip()
            except Exception:
                git_commit = "unknown"
            return {
                "version": VERSION,
                "release": RELEASE_NAME,
                "base_release": BASE_RELEASE,
                "replay_stable_baseline": REPLAY_STABLE_BASELINE,
                "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
                "git_commit": git_commit,
                "research_only": True,
                "no_real_orders": True,
            }
        except Exception as exc:
            return {"error": str(exc)}

    def _stable_capabilities(self) -> list:
        try:
            from release.capability_registry import get_capabilities
            return [
                {"id": c["id"], "display_name": c["display_name"],
                 "status": c["status"], "available": c["available"]}
                for c in get_capabilities() if c.get("stable", False)
            ]
        except Exception as exc:
            return [{"error": str(exc)}]

    def _capability_dependencies(self) -> dict:
        try:
            from release.capability_registry import validate_capability_dependencies
            return validate_capability_dependencies()
        except Exception as exc:
            return {"error": str(exc)}

    def _health_summary(self) -> dict:
        try:
            from release.research_foundation_health_v139 import ResearchFoundationStableHealthCheck
            return ResearchFoundationStableHealthCheck().get_health_summary()
        except Exception as exc:
            return {"error": str(exc)}

    def _compatibility(self) -> dict:
        try:
            from release.version_alignment import load_snapshot_gracefully
            results = {}
            for ver in ["1.4.0", "1.4.1", "1.4.2"]:
                p = {"application_version": ver, "_fixture": "TEST_FIXTURE"}
                enriched = load_snapshot_gracefully(p)
                results[ver] = {
                    "canonical": enriched.get("canonical_release_version"),
                    "note": enriched.get("version_alignment_note", ""),
                }
            return {"old_payload_compatibility": results, "schema_compatible": True}
        except Exception as exc:
            return {"error": str(exc)}

    def _regression(self) -> dict:
        return {
            "note": "Run: pytest tests/ — must be 0 failed / 0 errors",
            "full_suite": "EXTERNAL_VERIFICATION_REQUIRED",
            "exit_code": "EXTERNAL_VERIFICATION_REQUIRED",
        }

    def _runtime_hygiene(self) -> dict:
        import os
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        gitignore = os.path.join(root, ".gitignore")
        try:
            with open(gitignore) as f:
                content = f.read()
            ignored = [
                "data/research_foundation/",
                "reports/research_foundation_*.md",
            ]
            missing = [p for p in ignored if p not in content]
            return {"gitignore_ok": len(missing) == 0, "missing_patterns": missing}
        except Exception as exc:
            return {"error": str(exc)}

    def _safety(self) -> dict:
        try:
            from release.version_info import (
                NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
                MOCK_FALLBACK_ENABLED, AUTO_OPTIMIZATION_ENABLED, AUTO_TRADING_ENABLED,
            )
            return {
                "NO_REAL_ORDERS": NO_REAL_ORDERS,
                "BROKER_EXECUTION_ENABLED": BROKER_EXECUTION_ENABLED,
                "PRODUCTION_TRADING_BLOCKED": PRODUCTION_TRADING_BLOCKED,
                "MOCK_FALLBACK_ENABLED": MOCK_FALLBACK_ENABLED,
                "AUTO_OPTIMIZATION_ENABLED": AUTO_OPTIMIZATION_ENABLED,
                "AUTO_TRADING_ENABLED": AUTO_TRADING_ENABLED,
                "research_only": True,
            }
        except Exception as exc:
            return {"error": str(exc)}

    def _planned_provider_phase(self) -> list:
        return [
            {"version": "v1.4.0", "name": "TWSE Provider", "status": "PLANNED"},
            {"version": "v1.4.1", "name": "TPEx Provider", "status": "PLANNED"},
            {"version": "v1.4.2", "name": "MOPS Provider", "status": "PLANNED"},
            {"version": "v1.4.3", "name": "data.gov.tw Provider", "status": "PLANNED"},
            {"version": "v1.4.4", "name": "FinMind Adapter Hardening", "status": "PLANNED"},
            {"version": "v1.4.5", "name": "Source Lineage & Rate Limit", "status": "PLANNED"},
            {"version": "v1.4.6", "name": "Provider Quality Gates", "status": "PLANNED"},
            {"version": "v1.4.7", "name": "Forum Intelligence & Market Sentiment", "status": "PLANNED"},
            {"version": "v1.4.9", "name": "Data Provider Stable Rollup", "status": "PLANNED"},
        ]

    def _final_readiness(self) -> dict:
        try:
            from release.research_foundation_release_gate_v139 import ResearchFoundationReleaseGate
            summary = ResearchFoundationReleaseGate().get_gate_summary()
            if summary["blocking_failures"] > 0:
                action = "FIX_BLOCKING_ISSUES"
            elif summary["warnings"] > 0:
                action = "REVIEW_WARNINGS"
            else:
                action = "READY_FOR_PUBLIC_PROVIDER_INTEGRATION"
            return {
                "overall_gate": summary["overall"],
                "recommended_action": action,
                "blockers": summary["blocking_gate_names"],
                "warnings_count": summary["warnings"],
            }
        except Exception as exc:
            return {"error": str(exc), "recommended_action": "FIX_BLOCKING_ISSUES"}

    def render_text(self) -> str:
        data = self.generate()
        lines = [
            "=" * 70,
            f"  {self.REPORT_TITLE}",
            "=" * 70,
        ]
        ov = data.get("overview", {})
        lines += [
            f"  Version:              {ov.get('version', 'N/A')}",
            f"  Release:              {ov.get('release', 'N/A')}",
            f"  Base Release:         {ov.get('base_release', 'N/A')}",
            f"  Replay Baseline:      {ov.get('replay_stable_baseline', 'N/A')}",
            f"  Git Commit:           {ov.get('git_commit', 'N/A')}",
            f"  Generated:            {ov.get('generated_at', 'N/A')}",
            f"  Research Only:        {ov.get('research_only', True)}",
            f"  No Real Orders:       {ov.get('no_real_orders', True)}",
            "",
        ]
        readiness = data.get("final_readiness", {})
        lines += [
            f"  Gate Status:          {readiness.get('overall_gate', 'N/A')}",
            f"  Recommended Action:   {readiness.get('recommended_action', 'N/A')}",
            "=" * 70,
        ]
        return "\n".join(lines)
