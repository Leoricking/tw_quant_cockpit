"""
broker/bidask_parser.py - Bid/ask data normalizer.

Parses various input formats to the standard 5-level bid/ask dict.
"""

import logging

logger = logging.getLogger(__name__)

_ZERO_BIDASK = {
    **{f'bid_price_{i}': 0.0 for i in range(1, 6)},
    **{f'bid_volume_{i}': 0 for i in range(1, 6)},
    **{f'ask_price_{i}': 0.0 for i in range(1, 6)},
    **{f'ask_volume_{i}': 0 for i in range(1, 6)},
}


class BidAskParser:
    """
    Normalizes various bid/ask data formats into the standard 5-level dict.

    Supported input formats:
    - Standard dict: {bid_price_1..5, bid_volume_1..5, ask_price_1..5, ask_volume_1..5}
    - Shioaji-style: {bidPrice: [...], bidVolume: [...], askPrice: [...], askVolume: [...]}
    - List of tuples: [(bid_price, bid_vol), ...], [(ask_price, ask_vol), ...]
    """

    def parse(self, raw_data):
        """
        Normalize bid/ask data to standard dict format.

        Parameters
        ----------
        raw_data : dict, tuple, or any
            Raw bid/ask data in various formats.

        Returns
        -------
        dict with keys: bid_price_1..5, bid_volume_1..5, ask_price_1..5, ask_volume_1..5
        """
        if raw_data is None:
            return dict(_ZERO_BIDASK)

        try:
            if isinstance(raw_data, dict):
                return self._parse_dict(raw_data)
            elif isinstance(raw_data, (list, tuple)) and len(raw_data) == 2:
                return self._parse_tuple(raw_data)
            else:
                logger.warning("Unknown bid/ask format: %s. Returning zeroed dict.", type(raw_data))
                return dict(_ZERO_BIDASK)
        except Exception as exc:
            logger.warning("Error parsing bid/ask data: %s. Returning zeroed dict.", exc)
            return dict(_ZERO_BIDASK)

    def _parse_dict(self, d):
        """Parse from a dict (standard or Shioaji-style)."""
        result = {}

        # Check if it's already standard format
        if 'bid_price_1' in d:
            for i in range(1, 6):
                result[f'bid_price_{i}'] = float(d.get(f'bid_price_{i}', 0) or 0)
                result[f'bid_volume_{i}'] = int(d.get(f'bid_volume_{i}', 0) or 0)
                result[f'ask_price_{i}'] = float(d.get(f'ask_price_{i}', 0) or 0)
                result[f'ask_volume_{i}'] = int(d.get(f'ask_volume_{i}', 0) or 0)
            return result

        # Shioaji-style lists
        if 'bidPrice' in d or 'bid_price' in d:
            bid_prices = d.get('bidPrice', d.get('bid_price', []))
            bid_vols = d.get('bidVolume', d.get('bid_volume', []))
            ask_prices = d.get('askPrice', d.get('ask_price', []))
            ask_vols = d.get('askVolume', d.get('ask_volume', []))
            return self._from_lists(bid_prices, bid_vols, ask_prices, ask_vols)

        # Try numeric keys
        bid_prices = [d.get(f'b{i}p', d.get(f'bid{i}', 0)) for i in range(1, 6)]
        bid_vols = [d.get(f'b{i}v', d.get(f'bidv{i}', 0)) for i in range(1, 6)]
        ask_prices = [d.get(f'a{i}p', d.get(f'ask{i}', 0)) for i in range(1, 6)]
        ask_vols = [d.get(f'a{i}v', d.get(f'askv{i}', 0)) for i in range(1, 6)]
        return self._from_lists(bid_prices, bid_vols, ask_prices, ask_vols)

    def _parse_tuple(self, t):
        """Parse from tuple of (bids, asks)."""
        bids, asks = t
        bid_prices = [b[0] if isinstance(b, (list, tuple)) else b for b in (bids or [])]
        bid_vols = [b[1] if isinstance(b, (list, tuple)) and len(b) > 1 else 0 for b in (bids or [])]
        ask_prices = [a[0] if isinstance(a, (list, tuple)) else a for a in (asks or [])]
        ask_vols = [a[1] if isinstance(a, (list, tuple)) and len(a) > 1 else 0 for a in (asks or [])]
        return self._from_lists(bid_prices, bid_vols, ask_prices, ask_vols)

    def _from_lists(self, bid_prices, bid_vols, ask_prices, ask_vols):
        """Build standard dict from price/volume lists (up to 5 levels)."""
        result = {}
        for i in range(1, 6):
            idx = i - 1
            bp = bid_prices[idx] if idx < len(bid_prices) else 0
            bv = bid_vols[idx] if idx < len(bid_vols) else 0
            ap = ask_prices[idx] if idx < len(ask_prices) else 0
            av = ask_vols[idx] if idx < len(ask_vols) else 0
            result[f'bid_price_{i}'] = float(bp or 0)
            result[f'bid_volume_{i}'] = int(bv or 0)
            result[f'ask_price_{i}'] = float(ap or 0)
            result[f'ask_volume_{i}'] = int(av or 0)
        return result
