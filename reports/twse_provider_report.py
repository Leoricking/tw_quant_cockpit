"""
reports/twse_provider_report.py — TWSE Provider Report v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Do NOT commit generated output.
"""
import datetime


class TWSEProviderReport:
    TITLE = "TWSE Provider Report v1.4.0"

    def generate(self) -> dict:
        from release.version_info import VERSION, RELEASE_NAME
        return {
            "title": self.TITLE,
            "overview": {
                "version": VERSION,
                "release": RELEASE_NAME,
                "provider": "twse_official",
                "official_source": True,
                "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z",
                "research_only": True,
                "no_real_orders": True,
            },
            "capability_status": self._capabilities(),
            "safety": {
                "official_public_data": True,
                "research_only": True,
                "no_real_orders": True,
                "broker_disabled": True,
                "production_trading_blocked": True,
                "no_mock_fallback": True,
                "not_realtime": True,
            },
            "planned_provider_phase": [{"next": "v1.4.1 TPEx Provider"}],
        }

    def _capabilities(self) -> dict:
        try:
            from data.providers.twse.capabilities_v140 import TWSECapabilityMatrix
            return TWSECapabilityMatrix().build_summary()
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
            f"  Official:      {ov.get('official_source', True)}",
            f"  Generated:     {ov.get('generated_at', 'N/A')}",
            f"  Research Only: {ov.get('research_only', True)}",
            f"  No Real Orders:{ov.get('no_real_orders', True)}",
            "=" * 70,
            "  [!] Not Real-Time. Historical data only.",
            "  [!] No Mock Fallback in Real mode.",
            "  [!] No Broker. No Order Execution.",
            "  [!] Next: v1.4.1 TPEx Provider",
            "=" * 70,
        ]
        return "\n".join(lines)
