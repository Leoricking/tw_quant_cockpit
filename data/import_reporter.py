"""
data/import_reporter.py - Markdown report generator for TW Quant Cockpit.

Produces plain-text Markdown reports for:
- Data audit results
- Import plans
- Batch import results

No emojis. No HTML. Plain Markdown only.

Usage:
    from data.import_reporter import ImportReporter
    reporter = ImportReporter()
    reporter.write_audit_report(audit_result, 'data/import_reports/audit.md')
    reporter.write_import_plan(plan, 'data/import_reports/import_plan.md')
    reporter.write_batch_import_report(result, 'data/import_reports/batch.md')
"""

import os
from datetime import datetime


class ImportReporter:
    """Generate plain Markdown reports for import and audit workflows."""

    # ------------------------------------------------------------------
    # Audit report
    # ------------------------------------------------------------------

    def write_audit_report(self, audit_result: dict, output_file: str) -> str:
        """
        Write a data audit Markdown report.

        Returns the output file path.
        """
        lines = []
        date_str = audit_result.get('audit_date', datetime.now().strftime('%Y-%m-%d'))

        lines.append(f"# TW Quant Cockpit Data Audit Report")
        lines.append(f"")
        lines.append(f"Date: {date_str}")
        lines.append(f"")
        lines.append(f"[!] For research and simulation only. Not investment advice.")
        lines.append(f"")
        lines.append(f"---")
        lines.append(f"")

        # Readiness summary
        readiness = audit_result.get('readiness', {})
        lines.append(f"## Readiness Summary")
        lines.append(f"")
        lines.append(f"| Item | Value |")
        lines.append(f"|------|-------|")
        lines.append(f"| Profile symbols | {readiness.get('profile_count', 0)} |")
        lines.append(f"| Validation stage | {readiness.get('validation_stage', 'N/A')} |")
        lines.append(f"| Statistical confidence | {readiness.get('statistical_confidence', 'N/A')} |")
        lines.append(f"| Short-ready symbols | {readiness.get('short_ready_count', 0)} |")
        lines.append(f"| Mid-ready symbols | {readiness.get('mid_ready_count', 0)} |")
        lines.append(f"| Long-ready symbols | {readiness.get('long_ready_count', 0)} |")
        lines.append(f"")

        # Coverage table
        lines.append(f"## Data Coverage")
        lines.append(f"")
        lines.append(f"| Data Type | Threshold | Symbols Meeting Threshold |")
        lines.append(f"|-----------|-----------|--------------------------|")
        lines.append(f"| Daily K | >= 120 days | {readiness.get('daily_120', 0)} |")
        lines.append(f"| Institutional | >= 40 days | {readiness.get('institutional_40', 0)} |")
        lines.append(f"| Margin | >= 40 days | {readiness.get('margin_40', 0)} |")
        lines.append(f"| Monthly Revenue | >= 12 months | {readiness.get('revenue_12', 0)} |")
        lines.append(f"| Holder | >= 4 periods | {readiness.get('holder_4', 0)} |")
        lines.append(f"| Trust Cost | >= 20 days | {readiness.get('trust_cost_20', 0)} |")
        lines.append(f"")

        # Per data-type details
        lines.append(f"## Per Data-Type Audit")
        lines.append(f"")

        data_types = ['profile', 'daily', 'institutional', 'margin',
                      'monthly_revenue', 'holder', 'trust_cost']

        for dt in data_types:
            info = audit_result.get(dt, {})
            found = info.get('found', False)
            total = info.get('total_rows', 0)
            sym_count = info.get('symbol_count', 0)
            path = info.get('path', 'N/A')

            lines.append(f"### {dt}")
            lines.append(f"")
            lines.append(f"- Found: {found}")
            lines.append(f"- Path: {path}")
            lines.append(f"- Total rows: {total}")
            lines.append(f"- Symbol count: {sym_count}")

            if dt == 'daily' and found:
                lines.append(f"- Symbols < 20 days: {info.get('symbols_less_than_20d', 0)}")
                lines.append(f"- Symbols < 60 days: {info.get('symbols_less_than_60d', 0)}")
                lines.append(f"- Symbols < 120 days: {info.get('symbols_less_than_120d', 0)}")
                lines.append(f"- Duplicate rows: {info.get('duplicate_rows', 0)}")
                lines.append(f"- Invalid close (<= 0): {info.get('invalid_close', 0)}")
                lines.append(f"- High < Low: {info.get('high_lt_low', 0)}")
                lines.append(f"- Negative volume: {info.get('negative_volume', 0)}")

            elif dt in ('institutional', 'holder') and found:
                lines.append(f"- Duplicate rows: {info.get('duplicate_rows', 0)}")
                lines.append(f"- Symbols < 5 days: {info.get('symbols_less_than_5d', 0)}")
                lines.append(f"- Symbols < 40 days: {info.get('symbols_less_than_40d', 0)}")

            elif dt == 'margin' and found:
                lines.append(f"- Duplicate rows: {info.get('duplicate_rows', 0)}")
                lines.append(f"- Symbols < 5 days: {info.get('symbols_less_than_5d', 0)}")
                lines.append(f"- Symbols < 40 days: {info.get('symbols_less_than_40d', 0)}")
                lines.append(f"- Negative margin_balance: {info.get('negative_margin_balance', 0)}")
                lines.append(f"- Negative short_balance: {info.get('negative_short_balance', 0)}")

            elif dt == 'monthly_revenue' and found:
                lines.append(f"- Symbols < 6 months: {info.get('symbols_less_than_6m', 0)}")
                lines.append(f"- Symbols < 12 months: {info.get('symbols_less_than_12m', 0)}")
                lines.append(f"- Duplicate rows: {info.get('duplicate_rows', 0)}")

            elif dt == 'trust_cost' and found:
                lines.append(f"- Symbols < 3 days: {info.get('symbols_less_than_3d', 0)}")
                lines.append(f"- Symbols < 20 days: {info.get('symbols_less_than_20d', 0)}")
                lines.append(f"- Symbols < 40 days: {info.get('symbols_less_than_40d', 0)}")

            lines.append(f"")

        self._write(output_file, lines)
        return output_file

    # ------------------------------------------------------------------
    # Import plan report
    # ------------------------------------------------------------------

    def write_import_plan(self, plan: dict, output_file: str) -> str:
        """
        Write an import plan Markdown report.

        Returns the output file path.
        """
        lines = []
        uni  = plan.get('universe_status', {})
        p1   = plan.get('priority_1', [])
        p2   = plan.get('priority_2', [])
        p3   = plan.get('priority_3', [])
        cmds = plan.get('commands', [])
        date_str = datetime.now().strftime('%Y-%m-%d')

        lines.append(f"# TW Quant Cockpit Import Plan")
        lines.append(f"")
        lines.append(f"Date: {date_str}")
        lines.append(f"")
        lines.append(f"[!] For research and simulation only. Not investment advice.")
        lines.append(f"")
        lines.append(f"---")
        lines.append(f"")
        lines.append(f"## Current Status")
        lines.append(f"")
        lines.append(f"- Symbols: {uni.get('current_symbols', 0)}")
        lines.append(f"- Stage: {uni.get('validation_stage', 'N/A')}")
        lines.append(f"- Confidence: {uni.get('statistical_confidence', 'N/A')}")
        lines.append(f"")
        lines.append(f"## Target")
        lines.append(f"")
        lines.append(f"- Min: {uni.get('target_symbols_min', 50)}")
        lines.append(f"- Recommended: {uni.get('target_symbols_recommended', 100)}")
        lines.append(f"- Ideal: {uni.get('target_symbols_ideal', 200)}")
        lines.append(f"")
        lines.append(f"## Priority 1 (short-term analysis requirements)")
        lines.append(f"")
        for item in p1:
            lines.append(f"- {item}")
        if not p1:
            lines.append(f"- No critical gaps.")
        lines.append(f"")
        lines.append(f"## Priority 2 (mid-term analysis requirements)")
        lines.append(f"")
        for item in p2:
            lines.append(f"- {item}")
        if not p2:
            lines.append(f"- No gaps at this level.")
        lines.append(f"")
        lines.append(f"## Priority 3 (long-term analysis requirements)")
        lines.append(f"")
        for item in p3:
            lines.append(f"- {item}")
        if not p3:
            lines.append(f"- No gaps at this level.")
        lines.append(f"")
        lines.append(f"## Recommended Commands")
        lines.append(f"")
        for cmd in cmds:
            lines.append(f"    {cmd}")
        lines.append(f"")

        self._write(output_file, lines)
        return output_file

    # ------------------------------------------------------------------
    # Batch import report
    # ------------------------------------------------------------------

    def write_batch_import_report(self, result: dict, output_file: str) -> str:
        """
        Write a batch import result Markdown report.

        Returns the output file path.
        """
        lines = []
        date_str = datetime.now().strftime('%Y-%m-%d')

        lines.append(f"# TW Quant Cockpit Batch Import Report")
        lines.append(f"")
        lines.append(f"Date: {date_str}")
        lines.append(f"")
        lines.append(f"---")
        lines.append(f"")

        # Bundle-level summary
        folder   = result.get('folder', result.get('bundle', 'N/A'))
        dry_run  = result.get('dry_run', False)
        success  = result.get('success', False)

        lines.append(f"## Summary")
        lines.append(f"")
        lines.append(f"- Source: {folder}")
        lines.append(f"- Dry-run: {dry_run}")
        lines.append(f"- Overall success: {success}")
        lines.append(f"")

        # Per data-type results
        sub_results = result.get('results', {})
        if sub_results:
            lines.append(f"## Per Data-Type Results")
            lines.append(f"")
            lines.append(f"| Data Type | Files | OK | Failed | Rows |")
            lines.append(f"|-----------|-------|----|--------|------|")
            for dt, sub in sub_results.items():
                total  = sub.get('total_files', 0)
                ok     = len(sub.get('success_files', []))
                failed = len(sub.get('failed_files', []))
                rows   = sub.get('total_rows_imported', 0)
                lines.append(f"| {dt} | {total} | {ok} | {failed} | {rows} |")
            lines.append(f"")

            # Failed file details
            for dt, sub in sub_results.items():
                for ff in sub.get('failed_files', []):
                    lines.append(f"- FAIL [{dt}] {ff.get('file', '')}: {ff.get('error', '')}")
            lines.append(f"")

        # Warnings
        warnings = result.get('warnings', [])
        if warnings:
            lines.append(f"## Warnings")
            lines.append(f"")
            for w in warnings[:20]:
                lines.append(f"- {w}")
            lines.append(f"")

        # Single-folder result
        if not sub_results and 'success_files' in result:
            ok    = len(result.get('success_files', []))
            fail  = len(result.get('failed_files', []))
            rows  = result.get('total_rows_imported', 0)
            total = result.get('total_files', 0)
            lines.append(f"## Import Result")
            lines.append(f"")
            lines.append(f"- Data type: {result.get('data_type', 'N/A')}")
            lines.append(f"- Total files: {total}")
            lines.append(f"- Succeeded: {ok}")
            lines.append(f"- Failed: {fail}")
            lines.append(f"- Total rows imported: {rows}")
            lines.append(f"")

        self._write(output_file, lines)
        return output_file

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _write(self, output_file: str, lines: list) -> None:
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(lines) + '\n')
