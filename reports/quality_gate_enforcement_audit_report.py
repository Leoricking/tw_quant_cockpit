"""
reports/quality_gate_enforcement_audit_report.py — QualityGateEnforcementAuditReportBuilder v1.1.5

Generates Markdown audit reports for gate enforcement runs.
Research Only. No Real Orders. Not Investment Advice.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import json
import logging
import os
from datetime import date, datetime, timezone

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_DISABLED = True
RESEARCH_ONLY = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


class QualityGateEnforcementAuditReportBuilder:
    """
    Generates Quality Gate Enforcement & Audit reports in Markdown.
    Research Only. No Real Orders.
    """

    def build(self, run_id: str = None, output_dir: str = "reports") -> str:
        """
        Build audit report. Returns path to generated Markdown file.
        """
        today = date.today().strftime("%Y-%m-%d")
        filename = f"quality_gate_enforcement_audit_report_{today}.md"

        if not os.path.isabs(output_dir):
            output_dir = os.path.join(BASE_DIR, output_dir)
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, filename)

        # Gather data
        run_data = self._load_run(run_id)
        snapshot = self._load_snapshot(run_id)
        exclusion_reasons = self._load_exclusion_reasons(run_id)
        audit_events = self._load_audit_events(run_id)
        repro_hash = run_data.get("reproducibility_hash", "") if run_data else ""

        lines = []

        # Section 1: Header
        lines.append("# Quality Gate Enforcement & Audit Report v1.1.5")
        lines.append("")
        lines.append(f"Generated: {_now_utc()}")
        lines.append("")
        lines.append("> **[!] Research Only. No Real Orders. Not Investment Advice.**")
        lines.append("> Quality Gate FORMAL status does NOT enable trading.")
        lines.append("> VALIDATED does not mean tradable.")
        lines.append("")

        # Section 2: 總覽 Overview
        lines.append("## 2. 總覽 Overview")
        lines.append("")
        lines.append(f"| Field | Value |")
        lines.append(f"|-------|-------|")
        lines.append(f"| Version | 1.1.5 |")
        lines.append(f"| Research Only | True |")
        lines.append(f"| No Real Orders | True |")
        if run_data:
            lines.append(f"| Run ID | {run_data.get('run_id', 'N/A')} |")
            lines.append(f"| Command | {run_data.get('command_name', 'N/A')} |")
            lines.append(f"| Mode | N/A |")
            lines.append(f"| Gate | {run_data.get('gate_name', 'N/A')} |")
            lines.append(f"| Requested Level | {run_data.get('requested_level', 'N/A')} |")
            lines.append(f"| Applied Level | {run_data.get('applied_level', 'N/A')} |")
            lines.append(f"| Qualification | {run_data.get('status', 'N/A')} |")
            lines.append(f"| Policy Version | {run_data.get('policy_version', '1.1.5')} |")
            lines.append(f"| Reproducibility Hash | `{repro_hash or 'N/A'}` |")
        else:
            lines.append(f"| Run ID | {run_id or 'N/A'} |")
            lines.append(f"| Status | No run data found |")
        lines.append("")

        # Section 3: Symbol Universe
        lines.append("## 3. Symbol Universe")
        lines.append("")
        if run_data:
            def _count(key):
                val = run_data.get(key, "[]")
                if isinstance(val, list):
                    return len(val)
                try:
                    return len(json.loads(val))
                except Exception:
                    return 0
            lines.append(f"| Category | Count |")
            lines.append(f"|----------|-------|")
            lines.append(f"| Requested | {_count('requested_symbols')} |")
            lines.append(f"| Evaluated | {_count('evaluated_symbols')} |")
            lines.append(f"| Included | {_count('included_symbols')} |")
            lines.append(f"| Formal | {_count('formal_symbols')} |")
            lines.append(f"| Observational | {_count('observational_symbols')} |")
            lines.append(f"| Demo | {_count('demo_symbols')} |")
            lines.append(f"| Blocked | {_count('blocked_symbols')} |")
            lines.append(f"| Excluded | {_count('excluded_symbols')} |")
        else:
            lines.append("_No run data available._")
        lines.append("")

        # Section 4: Exclusion Audit
        lines.append("## 4. Exclusion Audit")
        lines.append("")
        if exclusion_reasons:
            lines.append("| Symbol | Decision | Reason Codes | Reasons | Required Actions | Override |")
            lines.append("|--------|----------|--------------|---------|-----------------|----------|")
            for sym, reasons in exclusion_reasons.items():
                reasons_str = "; ".join(reasons) if isinstance(reasons, list) else str(reasons)
                lines.append(f"| {sym} | excluded | see gate decisions | {reasons_str} | REVIEW | No |")
        else:
            lines.append("_No exclusion data available._")
        lines.append("")

        # Section 5: Gate Snapshot
        lines.append("## 5. Gate Snapshot")
        lines.append("")
        if snapshot:
            lines.append(f"| Field | Value |")
            lines.append(f"|-------|-------|")
            lines.append(f"| Policy Version | {snapshot.get('gate_policy_version', 'N/A')} |")
            lines.append(f"| Snapshot ID | {snapshot.get('snapshot_id', 'N/A')} |")
            lines.append(f"| Generated At | {snapshot.get('generated_at', 'N/A')} |")
            lines.append(f"| Statistical Confidence | {snapshot.get('statistical_confidence', 'N/A')} |")
            lines.append(f"| Payload Hash | `{snapshot.get('payload_hash', 'N/A')}` |")
        else:
            lines.append("_No snapshot data available._")
        lines.append("")

        # Section 6: Overrides
        lines.append("## 6. Overrides")
        lines.append("")
        if run_data and str(run_data.get("override_used", "")).lower() in ("true", "1"):
            lines.append(f"- Override used: YES")
            lines.append(f"- Override ID: {run_data.get('override_id', 'N/A')}")
            lines.append(f"- Limitation: Research-only. Override does NOT enable trading.")
        else:
            lines.append("- No override used in this run.")
        lines.append("")

        # Section 7: Workflow Output
        lines.append("## 7. Workflow Output")
        lines.append("")
        lines.append("| Output Type | Path | Qualification | Notes |")
        lines.append("|-------------|------|---------------|-------|")
        lines.append(f"| Enforcement Audit Report | {output_path} | Research Only | Not Investment Advice |")
        lines.append("")

        # Section 8: Reproducibility
        lines.append("## 8. Reproducibility")
        lines.append("")
        lines.append(f"| Field | Value |")
        lines.append(f"|-------|-------|")
        lines.append(f"| Run Hash | `{repro_hash or 'N/A'}` |")
        lines.append(f"| Hash Algorithm | SHA-256 |")
        lines.append(f"| Canonical Form | JSON sorted keys |")
        lines.append(f"| Verification Status | {'Stored' if repro_hash else 'Not computed'} |")
        lines.append("")

        # Section 9: Audit Chain
        lines.append("## 9. Audit Chain")
        lines.append("")
        if audit_events:
            lines.append(f"| Event Type | Timestamp | Gate | Reason |")
            lines.append(f"|-----------|-----------|------|--------|")
            for ev in audit_events[:20]:
                lines.append(
                    f"| {ev.get('event_type','')} | {ev.get('timestamp','')} | "
                    f"{ev.get('gate_name','')} | {ev.get('reason','')} |"
                )
            lines.append("")
            # Chain verification
            try:
                from gate_enforcement.audit_log import QualityGateAuditLog
                log = QualityGateAuditLog()
                chain = log.verify_chain()
                lines.append(f"- Events: {chain.get('events', 0)}")
                lines.append(f"- Chain Valid: {'YES' if chain.get('valid') else 'NO'}")
                lines.append(f"- Broken At: {chain.get('broken_at', 'N/A')}")
            except Exception as exc:
                lines.append(f"- Chain verification failed: {exc}")
        else:
            lines.append("_No audit events found for this run._")
        lines.append("")

        # Section 10: 安全聲明 Safety
        lines.append("## 10. 安全聲明 Safety Declaration")
        lines.append("")
        lines.append("- **No Real Orders**: True — No orders will be placed.")
        lines.append("- **Broker Execution Disabled**: True — No broker connectivity.")
        lines.append("- **Quality Gate does NOT enable trading**: FORMAL status ≠ trade enabled.")
        lines.append("- **VALIDATED does not enable trading**: Validation is research-only.")
        lines.append("- **Override is research-only**: Gate override cannot enable trading.")
        lines.append("- **Not Investment Advice**: All content is for research simulation only.")
        lines.append("")

        # Write file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        logger.info("Gate enforcement audit report saved: %s", output_path)
        return output_path

    def _load_run(self, run_id: str = None) -> dict:
        try:
            from gate_enforcement.enforcement_query import EnforcementQuery
            query = EnforcementQuery()
            if run_id:
                return query.get_run(run_id)
            runs = query.latest_runs(limit=1)
            return runs[-1] if runs else {}
        except Exception as exc:
            logger.warning("_load_run failed: %s", exc)
            return {}

    def _load_snapshot(self, run_id: str = None) -> dict:
        try:
            from gate_enforcement.enforcement_query import EnforcementQuery
            query = EnforcementQuery()
            if run_id:
                return query.get_snapshot(run_id)
            return {}
        except Exception as exc:
            logger.warning("_load_snapshot failed: %s", exc)
            return {}

    def _load_exclusion_reasons(self, run_id: str = None) -> dict:
        try:
            from gate_enforcement.enforcement_query import EnforcementQuery
            query = EnforcementQuery()
            if run_id:
                return query.get_exclusion_reasons(run_id)
            return {}
        except Exception as exc:
            logger.warning("_load_exclusion_reasons failed: %s", exc)
            return {}

    def _load_audit_events(self, run_id: str = None) -> list:
        try:
            from gate_enforcement.audit_log import QualityGateAuditLog
            log = QualityGateAuditLog()
            return log.list_events(run_id=run_id)
        except Exception as exc:
            logger.warning("_load_audit_events failed: %s", exc)
            return []
