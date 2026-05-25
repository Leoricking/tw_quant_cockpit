"""
screener/theme_pool.py - Theme pool loader and symbol lookup.
"""

import os
import logging

logger = logging.getLogger(__name__)

_DEFAULT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'config', 'theme_pools'
)


class ThemePool:
    """
    Loads theme pool CSVs and provides symbol-theme lookup.
    """

    def __init__(self):
        """Initialize with empty pool data."""
        self._pools = {}
        self._loaded = False

    def load(self, theme_pools_dir=None):
        """
        Load all CSV files from the theme_pools directory.

        Parameters
        ----------
        theme_pools_dir : str, optional
            Directory containing theme pool CSV files.
        """
        try:
            import pandas as pd
        except ImportError:
            logger.error("pandas not available; cannot load theme pools.")
            return

        directory = theme_pools_dir or _DEFAULT_DIR
        if not os.path.isdir(directory):
            logger.warning("Theme pools directory not found: %s", directory)
            return

        self._pools = {}
        for fname in os.listdir(directory):
            if not fname.endswith('.csv'):
                continue
            key = fname.replace('.csv', '')
            fpath = os.path.join(directory, fname)
            try:
                df = pd.read_csv(fpath, dtype={'symbol': str})
                if 'enabled' in df.columns:
                    df = df[df['enabled'].astype(str) == '1']
                self._pools[key] = df
            except Exception as exc:
                logger.warning("Failed to load %s: %s", fpath, exc)

        self._loaded = True
        logger.info("ThemePool loaded %d pools.", len(self._pools))

    def get_symbols(self):
        """
        Return a set of all symbol strings across all pools.

        Returns
        -------
        set of str
        """
        symbols = set()
        for df in self._pools.values():
            if 'symbol' in df.columns:
                for s in df['symbol'].astype(str).str.strip():
                    symbols.add(s)
        return symbols

    def get_symbol_themes(self, symbol):
        """
        Return list of theme names for a symbol.

        Parameters
        ----------
        symbol : str or int

        Returns
        -------
        list of str
        """
        sym = str(symbol).strip()
        themes = []
        for df in self._pools.values():
            if 'symbol' not in df.columns:
                continue
            match = df[df['symbol'].astype(str).str.strip() == sym]
            if not match.empty and 'theme' in df.columns:
                for t in match['theme'].tolist():
                    t_str = str(t)
                    if t_str not in themes:
                        themes.append(t_str)
        return themes

    def get_theme_weight(self, symbol):
        """
        Return the maximum weight for a symbol across all theme pools.

        Parameters
        ----------
        symbol : str or int

        Returns
        -------
        float (0.0 if not found)
        """
        sym = str(symbol).strip()
        max_w = 0.0
        for df in self._pools.values():
            if 'symbol' not in df.columns:
                continue
            match = df[df['symbol'].astype(str).str.strip() == sym]
            if not match.empty and 'weight' in df.columns:
                w = match['weight'].max()
                if w > max_w:
                    max_w = float(w)
        return max_w
