"""
data/import_plan.py - Import planning for TW Quant Cockpit.

Based on DataAuditor results, generates a prioritized import plan
telling the user what data is still missing before running backtests.

Usage:
    from data.import_plan import ImportPlan
    plan = ImportPlan()
    result = plan.build_plan()
    plan.print_plan()
    plan.export_plan()
"""

import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_TARGET_MIN         = 50
_TARGET_RECOMMENDED = 100
_TARGET_IDEAL       = 200


class ImportPlan:
    """Generate a prioritized data import plan from audit results."""

    def build_plan(self) -> dict:
        """
        Build the import plan based on current DataAuditor state.

        Returns a dict with:
            universe_status, data_gaps, priorities, commands
        """
        from data.data_auditor import DataAuditor
        audit = DataAuditor().audit_all()
        return self._build_from_audit(audit)

    def print_plan(self) -> None:
        """Print the import plan to stdout."""
        plan = self.build_plan()
        self._print(plan)

    def export_plan(self, output_dir: str = "data/import_reports") -> dict:
        """
        Export the import plan to a Markdown file.

        Returns dict with output file path and the plan dict.
        """
        from data.import_reporter import ImportReporter

        plan = self.build_plan()
        abs_dir = os.path.join(_BASE_DIR, output_dir.replace('/', os.sep))
        os.makedirs(abs_dir, exist_ok=True)

        date_str  = datetime.now().strftime('%Y%m%d')
        out_file  = os.path.join(abs_dir, f'import_plan_{date_str}.md')

        reporter = ImportReporter()
        reporter.write_import_plan(plan, out_file)

        logger.info("ImportPlan: exported plan to %s", out_file)
        return {'file': out_file, 'plan': plan}

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _build_from_audit(self, audit: dict) -> dict:
        readiness = audit.get('readiness', {})
        profile_count = readiness.get('profile_count', 0)

        # Compute per data-type missing symbols
        daily_sym   = audit.get('daily', {}).get('per_symbol', {})
        inst_sym    = audit.get('institutional', {}).get('per_symbol', {})
        margin_sym  = audit.get('margin', {}).get('per_symbol', {})
        rev_sym     = audit.get('monthly_revenue', {}).get('per_symbol', {})
        holder_sym  = audit.get('holder', {}).get('per_symbol', {})
        tc_sym      = audit.get('trust_cost', {}).get('per_symbol', {})

        # Profile symbols
        profile_syms = set(audit.get('profile', {}).get('per_symbol', {}).keys())

        def _missing(per_sym_dict, threshold, all_syms):
            present  = {s for s, v in per_sym_dict.items() if v.get('rows', 0) >= threshold}
            return sorted(all_syms - present)

        def _short_count(per_sym_dict, threshold):
            return [s for s, v in per_sym_dict.items() if v.get('rows', 0) < threshold]

        gaps = {
            'daily_missing_120d':         _missing(daily_sym, 120, profile_syms),
            'daily_missing_any':          sorted(profile_syms - set(daily_sym.keys())),
            'institutional_missing_40d':  _missing(inst_sym, 40, profile_syms),
            'institutional_missing_any':  sorted(profile_syms - set(inst_sym.keys())),
            'margin_missing_40d':         _missing(margin_sym, 40, profile_syms),
            'margin_missing_any':         sorted(profile_syms - set(margin_sym.keys())),
            'revenue_missing_12m':        _missing(rev_sym, 12, profile_syms),
            'revenue_missing_any':        sorted(profile_syms - set(rev_sym.keys())),
            'holder_missing_4':           _missing(holder_sym, 4, profile_syms),
            'holder_missing_any':         sorted(profile_syms - set(holder_sym.keys())),
            'trust_cost_missing_20d':     _missing(tc_sym, 20, profile_syms),
            'trust_cost_missing_any':     sorted(profile_syms - set(tc_sym.keys())),
        }

        # Build priorities
        p1 = []
        p2 = []
        p3 = []

        if profile_count < _TARGET_MIN:
            p1.append(
                f"Profile: need {_TARGET_MIN - profile_count} more symbols "
                f"(current: {profile_count}, min: {_TARGET_MIN})"
            )

        n_daily = len(gaps['daily_missing_120d'])
        if n_daily:
            p1.append(
                f"Daily K: {n_daily} symbol(s) need >= 120 trading days"
            )

        n_inst = len(gaps['institutional_missing_40d'])
        if n_inst:
            p2.append(
                f"Institutional: {n_inst} symbol(s) need >= 40 days"
            )

        n_margin = len(gaps['margin_missing_40d'])
        if n_margin:
            p2.append(
                f"Margin: {n_margin} symbol(s) need >= 40 days"
            )

        n_rev = len(gaps['revenue_missing_12m'])
        if n_rev:
            p2.append(
                f"Monthly revenue: {n_rev} symbol(s) need >= 12 months"
            )

        n_holder = len(gaps['holder_missing_4'])
        if n_holder:
            p3.append(
                f"Holder: {n_holder} symbol(s) need >= 4 periods"
            )

        n_tc = len(gaps['trust_cost_missing_20d'])
        if n_tc:
            p3.append(
                f"Trust cost: {n_tc} symbol(s) need >= 20 days"
            )

        if not p1 and not p2 and not p3:
            p1.append(
                "All priority data requirements met. "
                "You may run: python main.py validate-score --mode real"
            )

        commands = [
            "python main.py build-universe --template top50 --replace",
            "python main.py batch-import --bundle D:\\XQ\\twqc_bundle --dry-run",
            "python main.py batch-import --bundle D:\\XQ\\twqc_bundle",
            "python main.py data-audit --export",
            "python main.py import-plan",
            "python main.py validate-score --mode real",
        ]

        return {
            'universe_status': {
                'current_symbols':           profile_count,
                'target_symbols_min':        _TARGET_MIN,
                'target_symbols_recommended': _TARGET_RECOMMENDED,
                'target_symbols_ideal':      _TARGET_IDEAL,
                'validation_stage':          readiness.get('validation_stage', 'FUNCTIONAL_TEST'),
                'statistical_confidence':    readiness.get('statistical_confidence', 'INSUFFICIENT'),
            },
            'data_gaps':  gaps,
            'priority_1': p1,
            'priority_2': p2,
            'priority_3': p3,
            'commands':   commands,
            'readiness':  readiness,
        }

    def _print(self, plan: dict) -> None:
        uni = plan.get('universe_status', {})
        p1  = plan.get('priority_1', [])
        p2  = plan.get('priority_2', [])
        p3  = plan.get('priority_3', [])
        cmds = plan.get('commands', [])

        print('')
        print('=' * 65)
        print('  TW Quant Cockpit Import Plan')
        print('=' * 65)
        print('')
        print('Current:')
        print(f'  symbols           : {uni.get("current_symbols", 0)}')
        print(f'  stage             : {uni.get("validation_stage", "N/A")}')
        print(f'  confidence        : {uni.get("statistical_confidence", "N/A")}')
        print('')
        print('Target:')
        print(f'  min               : {uni.get("target_symbols_min")}')
        print(f'  recommended       : {uni.get("target_symbols_recommended")}')
        print(f'  ideal             : {uni.get("target_symbols_ideal")}')
        print('')
        print('Priority 1 (must-have for short-term analysis):')
        for item in p1:
            print(f'  - {item}')
        if not p1:
            print('  - No critical gaps.')
        print('')
        print('Priority 2 (for mid-term analysis):')
        for item in p2:
            print(f'  - {item}')
        if not p2:
            print('  - No gaps at this level.')
        print('')
        print('Priority 3 (for long-term analysis):')
        for item in p3:
            print(f'  - {item}')
        if not p3:
            print('  - No gaps at this level.')
        print('')
        print('Commands:')
        for cmd in cmds:
            print(f'  {cmd}')
        print('')
        print('=' * 65)
        print('[!] For research and simulation only. Not investment advice.')
