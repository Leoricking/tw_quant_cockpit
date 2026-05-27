"""
data/providers/ - Market data provider abstraction layer.

All data providers implement BaseMarketDataProvider.  Use the factory
function ``get_provider()`` to obtain the default active provider.

Provider registry (v0.3.4):
    csv         — CSV files in data/import/ (active)
    xq_export   — XQ technical-analysis export wrapper (transition)
    twse        — TWSE / TPEx / MOPS OpenAPI  (planned — not active)
    mega        — Chiao-Tung Securities API    (planned — disabled)

Real order execution is DISABLED across all providers.
"""

from data.providers.base_provider import BaseMarketDataProvider
from data.providers.csv_provider import CSVProvider

__all__ = [
    "BaseMarketDataProvider",
    "CSVProvider",
]


def get_provider(name: str = "csv") -> BaseMarketDataProvider:
    """
    Return a provider instance by name.

    Parameters
    ----------
    name : str
        'csv' | 'xq_export' | 'twse' | 'mega'

    Returns
    -------
    BaseMarketDataProvider
    """
    name = name.lower()
    if name == "csv":
        return CSVProvider()
    if name in ("xq_export", "xq"):
        from data.providers.xq_export_provider import XQExportProvider
        return XQExportProvider()
    if name in ("twse", "tpex", "openapi"):
        from data.providers.twse_openapi_provider import TWSEOpenAPIProvider
        return TWSEOpenAPIProvider()
    if name in ("mega", "cgb"):
        from data.providers.mega_provider import MegaProvider
        return MegaProvider()
    raise ValueError(f"Unknown provider: {name!r}")
