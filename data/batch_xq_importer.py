"""
data/batch_xq_importer.py - Batch XQ export importer for TW Quant Cockpit.

Scans a folder for XQ Excel / CSV files matching universe symbols and
imports each using the existing XQExportImporter logic.

Usage:
    from data.batch_xq_importer import BatchXQImporter
    bxi = BatchXQImporter()
    result = bxi.import_all(folder='D:/XQ/twqc_bundle/raw', universe=10, dry_run=True)
    result = bxi.import_all(folder='D:/XQ/twqc_bundle/raw', universe=10)
"""

import glob
import logging
import os

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class BatchXQImporter:
    """
    Batch-imports XQ Excel / CSV files for all symbols in a universe.

    File matching rules (for each symbol, e.g. '2454'):
        2454.xlsx
        2454.csv
        2454_*.xlsx
        2454_*.csv
        *_2454.xlsx
        *_2454.csv

    Does NOT modify the existing import-xq-export single-file workflow.
    """

    def scan_folder(self, folder: str, symbols: list) -> dict:
        """
        Scan folder for XQ files matching universe symbols.

        Returns
        -------
        dict mapping symbol -> list of matching file paths (may be empty)
        """
        result = {}
        if not os.path.isdir(folder):
            logger.warning("BatchXQImporter: folder not found: %s", folder)
            for sym in symbols:
                result[sym] = []
            return result

        all_files = []
        for ext in ('*.xlsx', '*.xls', '*.csv'):
            all_files.extend(glob.glob(os.path.join(folder, ext)))
        all_files = [os.path.abspath(f) for f in all_files]

        for sym in symbols:
            matches = []
            for fpath in all_files:
                fname = os.path.basename(fpath)
                name_no_ext = os.path.splitext(fname)[0]
                # Match: exact symbol, symbol_prefix, _symbol_suffix, or "symbol name" (space-separated)
                if (name_no_ext == sym
                        or name_no_ext.startswith(sym + '_')
                        or name_no_ext.endswith('_' + sym)
                        or name_no_ext.startswith(sym + ' ')):
                    matches.append(fpath)
            result[sym] = sorted(matches)

        return result

    def import_all(
        self,
        folder: str,
        universe: int = 10,
        manifest_path: str = None,
        symbols: list = None,
        dry_run: bool = False,
        replace: bool = False,
    ) -> dict:
        """
        Scan folder and import all matching XQ files for the universe.

        Parameters
        ----------
        folder       : directory containing XQ export files
        universe     : 10 / 30 / 50 — selects symbol list
        manifest_path: optional explicit path to universe_manifest.csv
        symbols      : explicit symbol list (overrides universe lookup)
        dry_run      : True → list files only, do not import
        replace      : pass to XQExportImporter (replace existing rows)

        Returns
        -------
        dict:
            found:   list of (symbol, file_path) tuples
            missing: list of symbols with no matching file
            results: dict symbol -> import outcome dict (empty in dry_run)
            dry_run: bool
        """
        from data.universe_manifest import UniverseManifest, get_universe_stocks

        # Resolve symbol list
        if symbols:
            sym_list = [str(s) for s in symbols]
            name_map  = {s: s for s in sym_list}
        else:
            stocks   = get_universe_stocks(universe)
            sym_list = [s['symbol'] for s in stocks]
            name_map  = {s['symbol']: s['name'] for s in stocks}

        # Optionally load names from manifest
        if manifest_path and os.path.isfile(manifest_path):
            try:
                import pandas as pd
                mdf = pd.read_csv(manifest_path, dtype=str)
                for _, row in mdf.iterrows():
                    sym = str(row.get('symbol', '')).strip()
                    nm  = str(row.get('name', '')).strip()
                    if sym and nm:
                        name_map[sym] = nm
                # Use manifest symbols if no explicit symbols given
                if not symbols:
                    sym_list = list(mdf['symbol'].dropna().astype(str).unique())
            except Exception as exc:
                logger.warning("Could not load manifest for names: %s", exc)

        # Scan
        file_map = self.scan_folder(folder, sym_list)
        found    = [(sym, paths[0]) for sym, paths in file_map.items() if paths]
        missing  = [sym for sym, paths in file_map.items() if not paths]

        if dry_run:
            return {
                'found':   found,
                'missing': missing,
                'results': {},
                'dry_run': True,
                'folder':  folder,
            }

        # Import each found file
        from data.xq_export_importer import XQExportImporter
        um      = UniverseManifest(manifest_path=manifest_path) if manifest_path else UniverseManifest()
        importer = XQExportImporter()
        results  = {}

        for sym, fpath in found:
            name = name_map.get(sym, sym)
            logger.info("BatchXQImporter: importing %s from %s", sym, fpath)
            try:
                outcome = importer.import_file(fpath, symbol=sym, name=name, replace=replace)
                results[sym] = outcome

                # Update manifest
                res = outcome.get('results', {})
                daily_rows = res.get('daily', {}).get('rows', 0) or 0
                margin_rows = res.get('margin', {}).get('rows', 0) or 0
                inst_rows   = res.get('institutional', {}).get('rows', 0) or 0
                holder_rows = res.get('holder', {}).get('rows', 0) or 0
                tc_rows     = res.get('trust_cost', {}).get('rows', 0) or 0

                status = 'imported' if outcome.get('success') else 'partial'
                warnings_all = []
                for dt_res in res.values():
                    warnings_all.extend(dt_res.get('warnings', []))
                warn_str = '; '.join(warnings_all[:3]) if warnings_all else ''

                if os.path.isfile(um.manifest_path):
                    um.update_import_status(
                        sym,
                        import_status=status,
                        xq_file=os.path.basename(fpath),
                        daily_rows=daily_rows,
                        margin_rows=margin_rows,
                        institutional_rows=inst_rows,
                        holder_rows=holder_rows,
                        trust_cost_rows=tc_rows,
                        warning=warn_str,
                    )
            except Exception as exc:
                logger.warning("BatchXQImporter: failed for %s: %s", sym, exc)
                results[sym] = {'success': False, 'error': str(exc)}

        return {
            'found':   found,
            'missing': missing,
            'results': results,
            'dry_run': False,
            'folder':  folder,
        }
