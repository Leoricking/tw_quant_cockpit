"""coverage_repair/report.py — CoverageRepairReport for v1.3.3.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class CoverageRepairReport:
    """Generate coverage repair workflow reports.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    no_real_orders = True
    production_trading_blocked = True

    def generate(self, queue=None, execution_results: Optional[List[Any]] = None) -> Dict[str, Any]:
        """Generate a report dict from queue and execution results."""
        tasks = []
        if queue is not None:
            try:
                tasks = queue.list_tasks()
            except Exception as exc:
                logger.warning("report: queue.list_tasks error: %s", exc)

        by_status: Dict[str, int] = {}
        by_priority: Dict[str, int] = {}
        by_issue: Dict[str, int] = {}
        blocked_symbols: List[str] = []
        resolved_count = 0
        failed_count = 0
        open_count = 0

        for t in tasks:
            by_status[t.status] = by_status.get(t.status, 0) + 1
            by_priority[t.priority] = by_priority.get(t.priority, 0) + 1
            by_issue[t.issue_type] = by_issue.get(t.issue_type, 0) + 1
            if t.status in ("BLOCKED", "CONFLICT_REVIEW", "WAITING_AUTH"):
                blocked_symbols.append(t.symbol)
            if t.status == "RESOLVED":
                resolved_count += 1
            if t.status == "FAILED":
                failed_count += 1
            if t.status == "OPEN":
                open_count += 1

        exec_summary: Dict[str, Any] = {}
        if execution_results:
            exec_summary = {
                "total_executions": len(execution_results),
                "resolved": sum(1 for r in execution_results if getattr(r, "resolved", False)),
                "partial": sum(1 for r in execution_results if getattr(r, "partial", False)),
                "errors": sum(1 for r in execution_results if getattr(r, "errors", [])),
            }

        return {
            "schema_version": "1.3.3",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_tasks": len(tasks),
            "open": open_count,
            "resolved": resolved_count,
            "failed": failed_count,
            "by_status": by_status,
            "by_priority": by_priority,
            "by_issue_type": by_issue,
            "blocked_symbols": list(set(blocked_symbols)),
            "execution_summary": exec_summary,
            "no_real_orders": True,
            "broker_execution_enabled": False,
            "production_trading_blocked": True,
            "coverage_repair_auto_execution_enabled": False,
            "coverage_repair_destructive_actions_enabled": False,
            "coverage_repair_mock_fallback_enabled": False,
        }

    def format_text(self, report_dict: Dict[str, Any]) -> str:
        """Format report as plain text."""
        lines = [
            "=" * 70,
            "  TW Quant Cockpit v1.3.3 — Coverage Repair Workflow Report",
            "  [!] Research Only | No Real Orders | Production Trading BLOCKED",
            "=" * 70,
            f"  Generated At      : {report_dict.get('generated_at', '')}",
            f"  Schema Version    : {report_dict.get('schema_version', '')}",
            "",
            "  Task Summary:",
            f"    Total Tasks     : {report_dict.get('total_tasks', 0)}",
            f"    Open            : {report_dict.get('open', 0)}",
            f"    Resolved        : {report_dict.get('resolved', 0)}",
            f"    Failed          : {report_dict.get('failed', 0)}",
            "",
            "  By Priority:",
        ]
        for p, c in (report_dict.get("by_priority") or {}).items():
            lines.append(f"    {p:<12}: {c}")
        lines.append("")
        lines.append("  By Status:")
        for s, c in (report_dict.get("by_status") or {}).items():
            lines.append(f"    {s:<24}: {c}")
        lines.append("")
        lines.append("  By Issue Type:")
        for it, c in (report_dict.get("by_issue_type") or {}).items():
            lines.append(f"    {it:<36}: {c}")

        blocked = report_dict.get("blocked_symbols") or []
        if blocked:
            lines.append("")
            lines.append(f"  Blocked/Conflict Symbols: {', '.join(blocked[:20])}")

        exec_s = report_dict.get("execution_summary") or {}
        if exec_s:
            lines.extend([
                "",
                "  Execution Summary:",
                f"    Total Executions : {exec_s.get('total_executions', 0)}",
                f"    Resolved         : {exec_s.get('resolved', 0)}",
                f"    Partial          : {exec_s.get('partial', 0)}",
                f"    With Errors      : {exec_s.get('errors', 0)}",
            ])

        lines.extend([
            "",
            "  Safety:",
            f"    No Real Orders                       : True",
            f"    Broker Execution Enabled             : False",
            f"    Production Trading BLOCKED           : True",
            f"    Auto Execution Enabled               : False",
            f"    Destructive Actions Enabled          : False",
            f"    Mock Fallback Enabled                : False",
            "=" * 70,
            "[!] Research Only. Not Investment Advice.",
        ])
        return "\n".join(lines)

    def format_markdown(self, report_dict: Dict[str, Any]) -> str:
        """Format report as Markdown."""
        lines = [
            "# TW Quant Cockpit v1.3.3 — Coverage Repair Workflow Report",
            "",
            "> [!] Research Only | No Real Orders | Production Trading BLOCKED",
            "",
            f"**Generated At:** {report_dict.get('generated_at', '')}  ",
            f"**Schema Version:** {report_dict.get('schema_version', '')}",
            "",
            "## Task Summary",
            "",
            f"| Metric | Count |",
            f"|--------|-------|",
            f"| Total Tasks | {report_dict.get('total_tasks', 0)} |",
            f"| Open | {report_dict.get('open', 0)} |",
            f"| Resolved | {report_dict.get('resolved', 0)} |",
            f"| Failed | {report_dict.get('failed', 0)} |",
            "",
            "## By Priority",
            "",
            "| Priority | Count |",
            "|----------|-------|",
        ]
        for p, c in (report_dict.get("by_priority") or {}).items():
            lines.append(f"| {p} | {c} |")
        lines.extend([
            "",
            "## By Status",
            "",
            "| Status | Count |",
            "|--------|-------|",
        ])
        for s, c in (report_dict.get("by_status") or {}).items():
            lines.append(f"| {s} | {c} |")
        lines.extend([
            "",
            "## Safety Flags",
            "",
            "| Flag | Value |",
            "|------|-------|",
            "| No Real Orders | True |",
            "| Broker Execution Enabled | False |",
            "| Production Trading BLOCKED | True |",
            "| Auto Execution Enabled | False |",
            "| Destructive Actions Enabled | False |",
            "| Mock Fallback Enabled | False |",
            "",
            "_[!] Research Only. Not Investment Advice._",
        ])
        return "\n".join(lines)
