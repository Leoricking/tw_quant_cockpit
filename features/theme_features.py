"""
features/theme_features.py - Theme-based feature computation for Taiwan stocks.

Loads theme pool CSV files and computes theme-related features for a given symbol.
"""

import os
import logging

logger = logging.getLogger(__name__)

_DEFAULT_THEME_POOLS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'config', 'theme_pools'
)

# Mainstream themes considered high-priority
_MAINSTREAM_THEMES = {
    'AI伺服器', 'AI CCL', 'ASIC', 'IC設計', '交換器', '散熱', '電源', '機器人', '主動ETF重疊'
}


class ThemeFeatures:
    """Computes theme-based features from theme pool CSV files."""

    def __init__(self, theme_pools_dir=None):
        """Initialize with optional custom theme pools directory."""
        self.theme_pools_dir = theme_pools_dir or _DEFAULT_THEME_POOLS_DIR
        self._cache = None

    def load_theme_pools(self, theme_pools_dir=None):
        """
        Load all CSV files from the theme_pools directory.

        Parameters
        ----------
        theme_pools_dir : str, optional
            Directory containing theme pool CSV files.

        Returns
        -------
        dict
            Mapping of theme_name -> pandas DataFrame with columns:
            symbol, name, theme, weight, enabled, note
        """
        import pandas as pd

        directory = theme_pools_dir or self.theme_pools_dir
        result = {}

        if not os.path.isdir(directory):
            logger.warning("Theme pools directory not found: %s", directory)
            return result

        for fname in os.listdir(directory):
            if not fname.endswith('.csv'):
                continue
            theme_key = fname.replace('.csv', '')
            fpath = os.path.join(directory, fname)
            try:
                df = pd.read_csv(fpath, dtype={'symbol': str})
                # Only include enabled rows
                if 'enabled' in df.columns:
                    df = df[df['enabled'].astype(str) == '1'].copy()
                result[theme_key] = df
                logger.debug("Loaded theme pool '%s' with %d entries.", theme_key, len(df))
            except Exception as exc:
                logger.warning("Failed to load theme pool '%s': %s", fpath, exc)

        return result

    def _get_pools(self, theme_pools_data=None):
        """Return theme pools data, loading if not provided."""
        if theme_pools_data is not None:
            return theme_pools_data
        if self._cache is None:
            self._cache = self.load_theme_pools()
        return self._cache

    def compute_theme_features(self, symbol, theme_pools_data=None):
        """
        Compute theme-based features for a given symbol.

        Parameters
        ----------
        symbol : str or int
            Stock symbol to look up.
        theme_pools_data : dict, optional
            Pre-loaded theme pools dict (from load_theme_pools). If None, loads automatically.

        Returns
        -------
        dict with keys:
            theme_tags (list of str)
            theme_score (float, 0-20)
            is_mainstream_theme (bool)
            theme_weight_max (float)
            data_missing (bool)
        """
        symbol_str = str(symbol).strip()
        pools = self._get_pools(theme_pools_data)

        if not pools:
            logger.warning("No theme pool data available for symbol %s.", symbol_str)
            return {
                'theme_tags': [],
                'theme_score': 0.0,
                'is_mainstream_theme': False,
                'theme_weight_max': 0.0,
                'data_missing': True,
            }

        theme_tags = []
        weights = []

        for pool_name, df in pools.items():
            if 'symbol' not in df.columns:
                continue
            match = df[df['symbol'].astype(str).str.strip() == symbol_str]
            if match.empty:
                continue
            # Collect themes
            if 'theme' in df.columns:
                for _, row in match.iterrows():
                    theme_name = str(row.get('theme', pool_name))
                    if theme_name not in theme_tags:
                        theme_tags.append(theme_name)
                    w = float(row.get('weight', 0.5))
                    weights.append(w)
            else:
                if pool_name not in theme_tags:
                    theme_tags.append(pool_name)
                weights.append(1.0)

        if not theme_tags:
            return {
                'theme_tags': [],
                'theme_score': 0.0,
                'is_mainstream_theme': False,
                'theme_weight_max': 0.0,
                'data_missing': False,
            }

        theme_weight_max = max(weights) if weights else 0.0
        n_themes = len(theme_tags)
        # Score: base from weight, bonus for more themes and mainstream membership
        base_score = theme_weight_max * 10.0
        multi_theme_bonus = min(n_themes - 1, 3) * 2.0
        is_mainstream = any(t in _MAINSTREAM_THEMES for t in theme_tags)
        mainstream_bonus = 3.0 if is_mainstream else 0.0

        theme_score = min(base_score + multi_theme_bonus + mainstream_bonus, 20.0)

        return {
            'theme_tags': theme_tags,
            'theme_score': round(theme_score, 2),
            'is_mainstream_theme': is_mainstream,
            'theme_weight_max': round(theme_weight_max, 4),
            'data_missing': False,
        }
