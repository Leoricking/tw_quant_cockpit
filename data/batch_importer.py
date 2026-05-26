"""
data/batch_importer.py - Batch CSV importer for TW Quant Cockpit.

Supports:
  import_folder(data_type, folder, replace, dry_run)
  import_bundle(folder, replace, dry_run, export_report)

Bundle folder structure:
  folder/
    profile/
    daily/
    institutional/
    margin/
    monthly_revenue/
    holder/
    trust_cost/

Usage:
    from data.batch_importer import BatchImporter
    bi = BatchImporter()
    result = bi.import_folder('daily', '/path/to/daily_csvs/', dry_run=True)
    result = bi.import_bundle('/path/to/twqc_bundle/', export_report=True)
"""

import os
import glob
import logging

logger = logging.getLogger(__name__)

_IMPORT_ORDER = [
    'profile',
    'daily',
    'institutional',
    'margin',
    'monthly_revenue',
    'holder',
    'trust_cost',
]


class BatchImporter:
    """Batch CSV importer that calls CSVImporter for each file."""

    def __init__(self):
        pass

    def import_folder(
        self,
        data_type: str,
        folder: str,
        replace: bool = False,
        dry_run: bool = False,
    ) -> dict:
        """
        Import all .csv files in folder for the given data_type.

        Files are imported in alphabetical order.
        A single file failure does not abort the rest.

        Parameters
        ----------
        data_type : str
            One of: profile, daily, institutional, margin,
            monthly_revenue, holder, trust_cost
        folder : str
            Path to folder containing CSV files.
        replace : bool
            Replace existing standard CSV (default: append).
        dry_run : bool
            If True, read and clean but do not write to standard CSV.

        Returns
        -------
        dict with keys:
            success, data_type, folder, total_files,
            success_files, failed_files, total_rows_imported,
            dry_run, warnings, clean_summaries
        """
        from data.csv_importer import CSVImporter

        result = {
            'success':             False,
            'data_type':           data_type,
            'folder':              folder,
            'total_files':         0,
            'success_files':       [],
            'failed_files':        [],
            'total_rows_imported': 0,
            'dry_run':             dry_run,
            'warnings':            [],
            'clean_summaries':     [],
        }

        if not os.path.isdir(folder):
            result['warnings'].append(f"Folder not found: {folder}")
            return result

        csv_files = sorted(glob.glob(os.path.join(folder, '*.csv')))
        result['total_files'] = len(csv_files)

        if not csv_files:
            result['warnings'].append(f"No .csv files found in {folder}")
            result['success'] = True
            return result

        if dry_run:
            result = self._dry_run_folder(data_type, csv_files, result)
            return result

        importer = CSVImporter()
        # First file: replace if requested; subsequent files: always append
        for i, fpath in enumerate(csv_files):
            append = not (replace and i == 0)
            try:
                res = importer.import_csv(data_type, fpath, append=append)
                clean_sum = res.get('clean_summary', {})
                if res.get('success'):
                    result['success_files'].append({
                        'file':              os.path.basename(fpath),
                        'rows':              res.get('rows_imported', 0),
                        'duplicates_removed': res.get('duplicates_removed', 0),
                        'warnings':          res.get('warnings', []),
                    })
                    result['total_rows_imported'] += res.get('rows_imported', 0)
                    result['warnings'].extend(res.get('warnings', []))
                    if clean_sum:
                        result['clean_summaries'].append({
                            'file': os.path.basename(fpath),
                            **clean_sum,
                        })
                else:
                    err = '; '.join(res.get('errors', res.get('warnings', ['unknown error'])))
                    result['failed_files'].append({
                        'file':  os.path.basename(fpath),
                        'error': err,
                    })
                    logger.warning("batch_importer: failed %s: %s", fpath, err)
            except Exception as exc:
                result['failed_files'].append({
                    'file':  os.path.basename(fpath),
                    'error': str(exc),
                })
                logger.warning("batch_importer: exception %s: %s", fpath, exc)

        result['success'] = True
        return result

    def import_bundle(
        self,
        folder: str,
        replace: bool = False,
        dry_run: bool = False,
        export_report: bool = False,
    ) -> dict:
        """
        Import a structured bundle folder.

        Expected sub-directories: profile, daily, institutional,
        margin, monthly_revenue, holder, trust_cost.

        Parameters
        ----------
        folder : str
            Path to bundle root folder.
        replace : bool
            Replace existing standard CSVs (default: append).
        dry_run : bool
            Read and clean but do not write standard CSVs.
        export_report : bool
            Write a Markdown report to data/import_reports/.

        Returns
        -------
        dict with keys:
            success, folder, results, dry_run, warnings
        """
        result = {
            'success':  False,
            'folder':   folder,
            'results':  {},
            'dry_run':  dry_run,
            'warnings': [],
        }

        if not os.path.isdir(folder):
            result['warnings'].append(f"Bundle folder not found: {folder}")
            return result

        for data_type in _IMPORT_ORDER:
            sub = os.path.join(folder, data_type)
            if not os.path.isdir(sub):
                result['warnings'].append(f"Sub-folder not found, skipping: {sub}")
                result['results'][data_type] = {
                    'success':             True,
                    'data_type':           data_type,
                    'folder':              sub,
                    'total_files':         0,
                    'success_files':       [],
                    'failed_files':        [],
                    'total_rows_imported': 0,
                    'dry_run':             dry_run,
                    'warnings':            [f"Sub-folder missing: {sub}"],
                }
                continue

            sub_result = self.import_folder(
                data_type, sub, replace=replace, dry_run=dry_run
            )
            result['results'][data_type] = sub_result
            result['warnings'].extend(sub_result.get('warnings', []))

        result['success'] = True

        if export_report:
            try:
                self._export_bundle_report(result)
            except Exception as exc:
                logger.warning("batch_importer: export_report failed: %s", exc)

        return result

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _dry_run_folder(self, data_type: str, csv_files: list, result: dict) -> dict:
        """Read and clean files but do not write to standard CSV."""
        from data.csv_importer import CSVImporter
        from data.csv_cleaner import CSVCleaner

        importer = CSVImporter()
        cleaner  = CSVCleaner()

        for fpath in csv_files:
            try:
                import pandas as pd
                df = importer._read_with_encoding(fpath, [])
                if df is None:
                    result['failed_files'].append({
                        'file': os.path.basename(fpath),
                        'error': 'Cannot read file',
                    })
                    continue

                df = importer.normalize_columns(data_type, df)
                validation = importer.validate_columns(data_type, df)

                if not validation['ok']:
                    result['failed_files'].append({
                        'file': os.path.basename(fpath),
                        'error': f"Missing columns: {validation['missing']}",
                    })
                    continue

                cleaned_df, clean_sum = cleaner.clean_dataframe(data_type, df)
                result['success_files'].append({
                    'file':              os.path.basename(fpath),
                    'rows':              len(cleaned_df),
                    'duplicates_removed': clean_sum.get('duplicates_removed', 0),
                    'warnings':          clean_sum.get('warnings', []),
                })
                result['total_rows_imported'] += len(cleaned_df)
                result['clean_summaries'].append({
                    'file': os.path.basename(fpath),
                    **clean_sum,
                })
                result['warnings'].extend(clean_sum.get('warnings', []))

            except Exception as exc:
                result['failed_files'].append({
                    'file': os.path.basename(fpath),
                    'error': str(exc),
                })
                logger.warning("batch_importer dry_run: exception %s: %s", fpath, exc)

        result['success'] = True
        return result

    def _export_bundle_report(self, result: dict) -> None:
        """Write a batch import Markdown report."""
        import os
        from datetime import datetime
        from data.import_reporter import ImportReporter

        _BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        abs_dir   = os.path.join(_BASE_DIR, 'data', 'import_reports')
        os.makedirs(abs_dir, exist_ok=True)

        date_str  = datetime.now().strftime('%Y%m%d_%H%M%S')
        out_file  = os.path.join(abs_dir, f'batch_import_report_{date_str}.md')

        reporter = ImportReporter()
        reporter.write_batch_import_report(result, out_file)
        logger.info("batch_importer: export report -> %s", out_file)
