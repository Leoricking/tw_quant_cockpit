"""
screener/chip_filter.py - Chip/institutional flow filter for screener pipeline.
"""

import logging

logger = logging.getLogger(__name__)


class ChipFilter:
    """
    Filters symbols based on chip/institutional flow criteria.

    Scoring:
    - Foreign buying (+points)
    - Investment trust buying (+points)
    - Major holder ratio increasing (+points)
    - Retail ratio decreasing (+points)
    - Margin balance surging (-points)
    - Trust selling (-points)
    """

    def filter(self, symbols, chip_data=None):
        """
        Filter symbols by chip criteria.

        Parameters
        ----------
        symbols : list of str
        chip_data : dict, optional
            Mapping symbol -> chip data dict.

        Returns
        -------
        list of dicts, each with:
            symbol, chip_score, passes, data_missing, warning
        """
        from features.chip_features import ChipFeatures
        cf = ChipFeatures()
        results = []

        for sym in symbols:
            sym_str = str(sym)
            cdata = None
            if chip_data and sym_str in chip_data:
                cdata = chip_data[sym_str]

            feat = cf.compute_chip_features(sym_str, cdata)

            results.append({
                'symbol': sym_str,
                'chip_score': feat['chip_score'],
                'passes': feat['chip_score'] >= 4.0 or feat['data_missing'],
                'data_missing': feat['data_missing'],
                'warning': feat.get('warning', ''),
            })

        return results
