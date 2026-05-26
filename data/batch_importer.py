"""
data/batch_importer.py - Batch CSV importer for TW Quant Cockpit.

Supports:
  import_folder(data_type, folder)  - import all .csv in a folder for one data type
  import_bundle(folder)             - import a structured bundle folder

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
    result = bi.import_folder('daily', '/path/to/daily_csvs/')
    result = bi.import_bundle('/path/to/twqc_bundle/')
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

    def import_folder(self, data_type: str, folder: str, replace: bool = False) -> dict:
        """
        Import all .csv files in folder for the given data_type.

        Files are imported in alphabetical order.
        A single file failure does not abort the rest.

        Returns:
            {
                "success": bool,
                "data_type": str,
                "folder": str,
                "total_files": int,
                "success_files": [{"file": ..., "rows": ...}],
                "failed_files":  [{"file": ..., "error": ...}],
                "total_rows_imported": int,
                "warnings": [],
            }
        """
        from data.csv_importer import CSVImporter

        result = {
            'success': False,
            'data_type': data_type,
            'folder': folder,
            'total_files': 0,
            'success_files': [],
            'failed_files': [],
            'total_rows_imported': 0,
            'warnings': [],
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

        importer = CSVImporter()
        # First file: replace if requested, subsequent: always append
        for i, fpath in enumerate(csv_files):
            append = not (replace and i == 0)
            try:
                res = importer.import_csv(data_type, fpath, append=append)
                if res.get('success'):
                    result['success_files'].append({
                        'file': os.path.basename(fpath),
                        'rows': res.get('rows_imported', 0),
                    })
                    result['total_rows_imported'] += res.get('rows_imported', 0)
                    result['warnings'].extend(res.get('warnings', []))
                else:
                    err = res.get('error', 'unknown error')
                    result['failed_files'].append({
                        'file': os.path.basename(fpath),
                        'error': err,
                    })
                    logger.warning("batch_importer: failed %s: %s", fpath, err)
            except Exception as exc:
                result['failed_files'].append({
                    'file': os.path.basename(fpath),
                    'error': str(exc),
                })
                logger.warning("batch_importer: exception %s: %s", fpath, exc)

        result['success'] = True
        return result

    def import_bundle(self, folder: str, replace: bool = False) -> dict:
        """
        Import a structured bundle folder.

        Expected sub-directories: profile, daily, institutional,
        margin, monthly_revenue, holder, trust_cost.

        Returns:
            {
                "success": bool,
                "folder": str,
                "results": {data_type: folder_result, ...},
                "warnings": [],
            }
        """
        result = {
            'success': False,
            'folder': folder,
            'results': {},
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
                    'success': True,
                    'data_type': data_type,
                    'folder': sub,
                    'total_files': 0,
                    'success_files': [],
                    'failed_files': [],
                    'total_rows_imported': 0,
                    'warnings': [f"Sub-folder missing: {sub}"],
                }
                continue

            sub_result = self.import_folder(data_type, sub, replace=replace)
            result['results'][data_type] = sub_result
            result['warnings'].extend(sub_result.get('warnings', []))

        result['success'] = True
        return result
