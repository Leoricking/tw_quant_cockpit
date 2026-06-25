"""
reports/tpex_provider_report.py — TPEx Provider Report v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Do NOT commit generated output.
"""
import datetime


class TPExProviderReport:
    TITLE = "TPEx Provider Report v1.4.1"

    def generate(self) -> dict:
        from release.version_info import VERSION, RELEASE_NAME
        return {
            "title": self.TITLE,
            "overview": {
                "version": VERSION,
                "release": RELEASE_NAME,
                "provider": "tpex_official",
                "official_source": True,
                "market": "TPEx",
                "board_scope": "MAINBOARD",
                "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z',
                "research_only": True,
                "no_real_orders": True,
            },
            "capability_status": self._capabilities(),
            "safety": {
                "official_tpex_public_data": True,
                "mainboard_common_stocks_only_by_default": True,
                "research_only": True,
                "no_real_orders": True,
                "broker_disabled": True,
                "production_trading_blocked": True,
                "no_mock_fallback": True,
                "not_realtime": True,
                "no_auto_download": True,
            },
            "planned_provider_phase": [{"next": "v1.4.2 MOPS Provider"}],
        }

    def _capabilities(self) -> dict:
        try:
            from data.providers.tpex.capabilities_v141 import TPExCapabilityMatrix
            return TPExCapabilityMatrix().build_summary()
        except Exception as exc:
            return {"error": str(exc)}

    def render_text(self) -> str:
        data = self.generate()
        ov = data.get("overview", {})
        lines = [
            "=" * 70,
            f"  {self.TITLE}",
            "=" * 70,
            f"  Version:       {ov.get('version', 'N/A')}",
            f"  Release:       {ov.get('release', 'N/A')}",
            f"  Provider:      {ov.get('provider', 'N/A')}",
            f"  Market:        {ov.get('market', 'TPEx')}",
            f"  Board Scope:   {ov.get('board_scope', 'MAINBOARD')}",
            f"  Official:      {ov.get('official_source', True)}",
            f"  Generated:     {ov.get('generated_at', 'N/A')}",
            f"  Research Only: {ov.get('research_only', True)}",
            f"  No Real Orders:{ov.get('no_real_orders', True)}",
            "=" * 70,
            "  [!] Official TPEx Public Data Only.",
            "  [!] Mainboard Common Stocks Only By Default.",
            "  [!] Not Real-Time. Historical data only.",
            "  [!] No Mock Fallback in Real mode.",
            "  [!] No Broker. No Order Execution.",
            "  [!] Not Investment Advice.",
            "  [!] Next: v1.4.2 MOPS Provider",
            "=" * 70,
        ]
        return "\n".join(lines)
