"""
reports/mops_provider_report.py — MOPS Provider Report v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Do NOT commit generated output.
"""
import datetime


class MOPSProviderReport:
    TITLE = "MOPS Provider Report v1.4.2"

    def generate(self) -> dict:
        from release.version_info import VERSION, RELEASE_NAME
        return {
            "title": self.TITLE,
            "overview": {
                "version": VERSION,
                "release": RELEASE_NAME,
                "provider": "mops_official",
                "official_source": True,
                "market": "MOPS",
                "data_domain": "financial_disclosure",
                "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
                "research_only": True,
                "no_real_orders": True,
            },
            "capability_status": self._capabilities(),
            "safety": {
                "official_mops_public_disclosure": True,
                "financial_disclosure_only": True,
                "research_only": True,
                "no_real_orders": True,
                "broker_disabled": True,
                "production_trading_blocked": True,
                "no_mock_fallback": True,
                "not_realtime": True,
                "no_auto_download": True,
                "official_source_only": True,
            },
            "data_types": [
                "company_profile",
                "monthly_revenue",
                "financial_report_filing",
                "balance_sheet",
                "income_statement",
                "cash_flow_statement",
                "equity_statement",
                "material_information",
                "investor_conference",
                "xbrl_document",
                "revision_record",
            ],
        }

    def _capabilities(self) -> dict:
        try:
            from data.providers.mops.capabilities_v142 import MOPSCapabilityMatrix
            return MOPSCapabilityMatrix().build_summary()
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
            f"  Market:        {ov.get('market', 'MOPS')}",
            f"  Data Domain:   {ov.get('data_domain', 'financial_disclosure')}",
            f"  Official:      {ov.get('official_source', True)}",
            f"  Generated:     {ov.get('generated_at', 'N/A')}",
            f"  Research Only: {ov.get('research_only', True)}",
            f"  No Real Orders:{ov.get('no_real_orders', True)}",
            "=" * 70,
            "  [!] Official MOPS Public Disclosure Data Only.",
            "  [!] Financial Disclosure Only. Not Market Price Data.",
            "  [!] Not Real-Time. Historical data only.",
            "  [!] No Mock Fallback in Real mode.",
            "  [!] No Broker. No Order Execution.",
            "  [!] No Auto Download.",
            "  [!] Not Investment Advice.",
            "=" * 70,
        ]
        return "\n".join(lines)
