"""
reports/rule_governance_report.py — Rule Governance Markdown report builder (v0.3.28).
[!] Research Only. No Real Orders. No Auto Weight Apply. Production Trading: BLOCKED.
Output: reports/rule_governance_report_YYYY-MM-DD.md

Safety invariants:
  read_only = True
  no_real_orders = True
  production_blocked = True
  Research Only, No Real Orders, No Auto Weight Apply, Production Trading BLOCKED
"""

import os
import logging
import datetime

_LOG = logging.getLogger(__name__)

_SAFETY_BANNER = (
    "[!] Research Only. No Real Orders. "
    "No Auto Weight Apply. Production Trading: BLOCKED."
)


class RuleGovernanceReportBuilder:
    """
    Generates a Markdown governance report for all registered rules.

    Safety invariants:
      read_only = True
      no_real_orders = True
      production_blocked = True
      Research Only, No Real Orders, No Auto Weight Apply, Production Trading BLOCKED
    """

    read_only: bool = True
    no_real_orders: bool = True
    production_blocked: bool = True

    def __init__(
        self,
        report_date: str = None,
        mode: str = "real",
        registry=None,
        confidence_result: dict = None,
        dependency_graph=None,
        snapshot: dict = None,
    ):
        self.report_date = report_date or datetime.date.today().isoformat()
        self.mode = mode
        self._registry = registry
        self._confidence_result = confidence_result or {}
        self._dependency_graph = dependency_graph
        self._snapshot = snapshot or {}

    # ------------------------------------------------------------------
    # Main build entry point
    # ------------------------------------------------------------------

    def build(self, output_dir: str = "reports") -> str:
        """
        Generate the Markdown report and write it to output_dir.
        Returns the absolute path of the written report.
        """
        if not os.path.isabs(output_dir):
            # Resolve relative to project root (two levels up from this file)
            _base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            output_dir = os.path.join(_base, output_dir)

        os.makedirs(output_dir, exist_ok=True)

        filename = f"rule_governance_report_{self.report_date}.md"
        out_path = os.path.join(output_dir, filename)

        lines = self._generate_lines()
        content = "\n".join(lines)

        try:
            with open(out_path, "w", encoding="utf-8") as fh:
                fh.write(content)
        except Exception as exc:
            _LOG.warning("RuleGovernanceReportBuilder.build write error: %s", exc)

        return out_path

    # ------------------------------------------------------------------
    # Line generators for each section
    # ------------------------------------------------------------------

    def _generate_lines(self) -> list:
        lines = []
        lines += self._header()
        lines += self._section_overview()
        lines += self._section_categories()
        lines += self._section_confidence()
        lines += self._section_dependencies()
        lines += self._section_review_queue()
        lines += self._section_signal_quality_linkage()
        lines += self._section_safety()
        lines += self._section_recommendations()
        lines += self._footer()
        return lines

    # --- Header ---

    def _header(self) -> list:
        return [
            f"# Strategy Rule Governance Report — {self.report_date}",
            "",
            f"> {_SAFETY_BANNER}",
            "",
            f"**Mode**: {self.mode}  ",
            f"**Generated**: {self.report_date}  ",
            "**Version**: v0.3.28  ",
            "",
            "---",
            "",
        ]

    # --- Section 1: Overview ---

    def _section_overview(self) -> list:
        lines = ["## 1. 總覽 (Overview)", ""]

        if self._registry is None and not self._snapshot:
            lines += ["> No data available.", ""]
            return lines

        summary = self._snapshot.get("summary", {})
        if not summary and self._registry is not None:
            try:
                summary = self._registry.build_rule_summary()
            except Exception:
                summary = {}

        total = summary.get("total_rules", 0)
        by_status = summary.get("by_status", {})
        active = by_status.get("ACTIVE", 0)
        experimental = by_status.get("EXPERIMENTAL", 0)
        disabled = by_status.get("DISABLED", 0)
        deprecated = by_status.get("DEPRECATED", 0)
        needs_review = by_status.get("NEEDS_REVIEW", 0)

        lines += [
            f"| Item | Value |",
            f"|------|-------|",
            f"| Mode | {self.mode} |",
            f"| Total Rules | {total} |",
            f"| Active | {active} |",
            f"| Experimental | {experimental} |",
            f"| Disabled | {disabled} |",
            f"| Deprecated | {deprecated} |",
            f"| Needs Review | {needs_review} |",
            f"| read_only | True |",
            f"| no_real_orders | True |",
            f"| production_blocked | True |",
            "",
        ]
        return lines

    # --- Section 2: Rule Categories ---

    def _section_categories(self) -> list:
        lines = ["## 2. Rule Categories", ""]

        summary = self._snapshot.get("summary", {})
        if not summary and self._registry is not None:
            try:
                summary = self._registry.build_rule_summary()
            except Exception:
                summary = {}

        by_category = summary.get("by_category", {})
        if not by_category:
            lines += ["> No data available.", ""]
            return lines

        lines += ["| Category | Count |", "|----------|-------|"]
        for cat, cnt in sorted(by_category.items()):
            lines.append(f"| {cat} | {cnt} |")
        lines.append("")
        return lines

    # --- Section 3: Rule Confidence ---

    def _section_confidence(self) -> list:
        lines = ["## 3. Rule Confidence", ""]

        cr = self._confidence_result
        if not cr:
            lines += ["> No confidence scoring data available.", ""]
            return lines

        buckets = [
            ("HIGH", "high_confidence"),
            ("GOOD", "good_confidence"),
            ("PARTIAL", "partial_confidence"),
            ("WEAK", "weak_confidence"),
            ("LOW", "low_confidence"),
            ("UNKNOWN", "unknown_confidence"),
            ("PLANNED", "planned"),
        ]

        lines += ["| Confidence Level | Count |", "|-----------------|-------|"]
        for label, key in buckets:
            count = len(cr.get(key, []))
            lines.append(f"| {label} | {count} |")
        lines.append("")

        # List rules with known high/good confidence
        high = cr.get("high_confidence", [])
        good = cr.get("good_confidence", [])
        if high or good:
            lines.append("**High / Good confidence rules:**")
            lines.append("")
            for rid in high:
                lines.append(f"- {rid} — HIGH")
            for rid in good:
                lines.append(f"- {rid} — GOOD")
            lines.append("")

        return lines

    # --- Section 4: Dependency Graph ---

    def _section_dependencies(self) -> list:
        lines = ["## 4. Dependency Graph", ""]

        dg = self._dependency_graph
        if dg is None:
            lines += ["> No dependency graph available.", ""]
            return lines

        try:
            edges = dg.export_edges()
            cycles = dg.detect_cycles()
            high_impact = dg.get_high_impact_rules(min_dependents=2)

            lines.append(f"**Dependency edges**: {len(edges)}")
            lines.append("")

            if cycles:
                lines.append("**Cycle Warnings:**")
                lines.append("")
                for c in cycles:
                    lines.append(f"- :warning: {c}")
                lines.append("")
            else:
                lines.append("**Cycles**: None detected.")
                lines.append("")

            if high_impact:
                lines.append("**High-Impact Rules (2+ dependents):**")
                lines.append("")
                lines += ["| Rule ID | Dependent Count |", "|---------|----------------|"]
                for rid in high_impact:
                    dep_count = len(dg.get_dependents(rid))
                    lines.append(f"| {rid} | {dep_count} |")
                lines.append("")
            else:
                lines.append("No high-impact rules found.")
                lines.append("")

        except Exception as exc:
            lines += [f"> Error building dependency section: {exc}", ""]

        return lines

    # --- Section 5: Rules Needing Review ---

    def _section_review_queue(self) -> list:
        lines = ["## 5. Rules Needing Review", ""]

        if self._registry is None:
            lines += ["> No data available.", ""]
            return lines

        try:
            review_rules = self._registry.list_rules(status="NEEDS_REVIEW")
            insuff_rules = self._registry.list_rules(status="INSUFFICIENT_SAMPLE")
            experimental_rules = [
                r for r in self._registry.list_rules()
                if r.experimental and r.status not in ("DISABLED", "DEPRECATED")
            ]

            candidates = []
            for r in review_rules:
                candidates.append((r.rule_id, "Status: NEEDS_REVIEW", "HIGH", "Review and update status"))
            for r in insuff_rules:
                candidates.append((r.rule_id, "Insufficient sample count", "MEDIUM", "Collect more backtest data"))
            for r in experimental_rules:
                candidates.append((r.rule_id, "Marked experimental", "LOW", "Validate before production use"))

            if not candidates:
                lines += ["> No rules currently require review.", ""]
                return lines

            lines += [
                "| Rule ID | Reason | Severity | Recommended Action |",
                "|---------|--------|----------|--------------------|",
            ]
            for rule_id, reason, severity, action in candidates:
                lines.append(f"| {rule_id} | {reason} | {severity} | {action} |")
            lines.append("")

        except Exception as exc:
            lines += [f"> Error building review queue: {exc}", ""]

        return lines

    # --- Section 6: Signal Quality Linkage ---

    def _section_signal_quality_linkage(self) -> list:
        lines = ["## 6. Rule Weight / Signal Quality Linkage", ""]

        if self._registry is None:
            lines += ["> No data available.", ""]
            return lines

        try:
            signal_rules = self._registry.list_rules(category="signal_quality")
            weight_rules = self._registry.list_rules(category="rule_weight")

            lines.append(
                "The following rules connect to signal weighting. "
                "**No weights are auto-applied** — all changes require manual review."
            )
            lines.append("")

            if signal_rules:
                lines.append("**Signal Quality Rules:**")
                lines.append("")
                for r in signal_rules:
                    lines.append(f"- `{r.rule_id}` — {r.description}")
                lines.append("")

            if weight_rules:
                lines.append("**Rule Weight Rules:**")
                lines.append("")
                for r in weight_rules:
                    lines.append(f"- `{r.rule_id}` — {r.description}")
                lines.append("")

            if not signal_rules and not weight_rules:
                lines.append("> No signal quality or rule weight rules registered.")
                lines.append("")

        except Exception as exc:
            lines += [f"> Error: {exc}", ""]

        return lines

    # --- Section 7: Safety ---

    def _section_safety(self) -> list:
        return [
            "## 7. Safety",
            "",
            "| Safety Flag | Value |",
            "|-------------|-------|",
            "| read_only | True |",
            "| no_real_orders | True |",
            "| production_blocked | True |",
            "",
            "- This system is for **research and backtesting only**.",
            "- No real orders are generated or submitted.",
            "- Rule weight changes are **never auto-applied** to live portfolios.",
            "- Production trading is **BLOCKED** at all levels.",
            "- All outputs are for analysis purposes only.",
            "",
        ]

    # --- Section 8: Recommendations ---

    def _section_recommendations(self) -> list:
        lines = ["## 8. Recommendations", ""]

        cr = self._confidence_result

        if cr:
            unknown = cr.get("unknown_confidence", [])
            weak = cr.get("weak_confidence", [])
            low = cr.get("low_confidence", [])

            if unknown:
                lines.append("**Rules requiring validation data:**")
                lines.append("")
                for rid in unknown[:10]:
                    lines.append(f"- {rid}")
                if len(unknown) > 10:
                    lines.append(f"- ... and {len(unknown) - 10} more")
                lines.append("")

            if weak or low:
                lines.append("**Rules to consider disabling (weak/low confidence):**")
                lines.append("")
                for rid in (weak + low)[:10]:
                    lines.append(f"- {rid}")
                lines.append("")

        lines += [
            "**General recommendations:**",
            "",
            "- Run walk-forward validation for any rule graded A or B.",
            "- Review NEEDS_REVIEW rules before using in active screens.",
            "- Collect at least 20 samples before upgrading to HIGH confidence.",
            "- Do not apply rule weights automatically — always require manual approval.",
            "",
        ]
        return lines

    # --- Footer ---

    def _footer(self) -> list:
        return [
            "---",
            "",
            f"> {_SAFETY_BANNER}",
            "",
            f"*Report generated {self.report_date} by TW Quant Cockpit v0.3.28*",
            "",
        ]
