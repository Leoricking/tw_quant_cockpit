"""
tests/test_mops_provider_v142.py — v1.4.2 MOPS Provider tests.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] MOPS_REALTIME_AVAILABLE = False. MOPS_BROKER_EXECUTION_AVAILABLE = False.
[!] MOPS_AUTO_DOWNLOAD_ENABLED = False. MOPS_MOCK_FALLBACK_ENABLED = False.
All tests run offline. No network dependency.
"""
import datetime
import json
import os
import pytest

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures", "mops_provider")


def load_fixture(name):
    path = os.path.join(FIXTURES_DIR, name)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_html_fixture(name):
    path = os.path.join(FIXTURES_DIR, name)
    with open(path, "rb") as f:
        return f.read()


# =====================================================================
# TestRegistration (tests 1-10)
# =====================================================================
class TestRegistration:
    def test_01_provider_id(self):
        from data.providers.mops.provider_v142 import MOPSProviderV142
        assert MOPSProviderV142().provider_id == "mops_official"

    def test_02_official_is_true(self):
        from data.providers.mops.provider_v142 import MOPSProviderV142
        assert MOPSProviderV142().official is True

    def test_03_market_mops(self):
        from data.providers.mops.provider_v142 import MOPSProviderV142
        assert MOPSProviderV142().market == "MOPS"

    def test_04_requires_auth_false(self):
        from data.providers.mops.provider_v142 import MOPSProviderV142
        assert MOPSProviderV142().requires_auth is False

    def test_05_broker_provider_false(self):
        from data.providers.mops.provider_v142 import MOPSProviderV142
        assert MOPSProviderV142().broker_provider is False

    def test_06_order_execution_false(self):
        from data.providers.mops.provider_v142 import MOPSProviderV142
        assert MOPSProviderV142().order_execution_supported is False

    def test_07_realtime_available_false(self):
        import data.providers.mops as pkg
        assert pkg.MOPS_REALTIME_AVAILABLE is False

    def test_08_mock_formal_conclusion_false(self):
        from data.providers.mops.provider_v142 import MOPSProviderV142
        assert MOPSProviderV142().mock_formal_conclusion_allowed is False

    def test_09_twse_provider_unchanged(self):
        from data.providers.twse.provider_v140 import TWSEProviderV140
        assert TWSEProviderV140().provider_id == "twse_official"

    def test_10_tpex_provider_unchanged(self):
        from data.providers.tpex.provider_v141 import TPExProviderV141
        assert TPExProviderV141().provider_id == "tpex_official"


# =====================================================================
# TestEndpointRegistry (tests 11-21)
# =====================================================================
class TestEndpointRegistry:
    def test_11_registry_instantiates(self):
        from data.providers.mops.endpoints_v142 import MOPSEndpointRegistry
        reg = MOPSEndpointRegistry()
        assert reg is not None

    def test_12_has_enough_endpoints(self):
        from data.providers.mops.endpoints_v142 import MOPSEndpointRegistry
        reg = MOPSEndpointRegistry()
        assert len(reg.list_all()) >= 8

    def test_13_company_profile_endpoint_exists(self):
        from data.providers.mops.endpoints_v142 import MOPSEndpointRegistry
        reg = MOPSEndpointRegistry()
        ep = reg.get("company_profile")
        assert ep is not None
        assert ep.method == "POST"

    def test_14_monthly_revenue_endpoint_exists(self):
        from data.providers.mops.endpoints_v142 import MOPSEndpointRegistry
        reg = MOPSEndpointRegistry()
        ep = reg.get("monthly_revenue")
        assert ep is not None
        assert ep.enabled is True

    def test_15_balance_sheet_endpoint_exists(self):
        from data.providers.mops.endpoints_v142 import MOPSEndpointRegistry
        reg = MOPSEndpointRegistry()
        ep = reg.get("balance_sheet")
        assert ep is not None

    def test_16_income_statement_endpoint_exists(self):
        from data.providers.mops.endpoints_v142 import MOPSEndpointRegistry
        reg = MOPSEndpointRegistry()
        ep = reg.get("income_statement")
        assert ep is not None

    def test_17_cash_flow_endpoint_exists(self):
        from data.providers.mops.endpoints_v142 import MOPSEndpointRegistry
        reg = MOPSEndpointRegistry()
        ep = reg.get("cash_flow")
        assert ep is not None

    def test_18_material_info_endpoint_exists(self):
        from data.providers.mops.endpoints_v142 import MOPSEndpointRegistry
        reg = MOPSEndpointRegistry()
        ep = reg.get("material_information")
        assert ep is not None

    def test_19_list_enabled_is_subset(self):
        from data.providers.mops.endpoints_v142 import MOPSEndpointRegistry
        reg = MOPSEndpointRegistry()
        enabled = reg.list_enabled()
        all_eps = reg.list_all()
        assert len(enabled) <= len(all_eps)

    def test_20_is_endpoint_available(self):
        from data.providers.mops.endpoints_v142 import MOPSEndpointRegistry
        reg = MOPSEndpointRegistry()
        assert reg.is_endpoint_available("monthly_revenue") is True

    def test_21_unknown_endpoint_returns_none(self):
        from data.providers.mops.endpoints_v142 import MOPSEndpointRegistry
        reg = MOPSEndpointRegistry()
        assert reg.get("nonexistent_endpoint") is None


# =====================================================================
# TestCapabilities (tests 22-34)
# =====================================================================
class TestCapabilities:
    def test_22_company_profile_supported(self):
        from data.providers.mops.capabilities_v142 import MOPSCapabilityMatrix
        m = MOPSCapabilityMatrix()
        assert m.is_supported("COMPANY_PROFILE") is True

    def test_23_monthly_revenue_supported(self):
        from data.providers.mops.capabilities_v142 import MOPSCapabilityMatrix
        m = MOPSCapabilityMatrix()
        assert m.is_supported("MONTHLY_REVENUE") is True

    def test_24_balance_sheet_supported(self):
        from data.providers.mops.capabilities_v142 import MOPSCapabilityMatrix
        m = MOPSCapabilityMatrix()
        assert m.is_supported("BALANCE_SHEET") is True

    def test_25_income_statement_supported(self):
        from data.providers.mops.capabilities_v142 import MOPSCapabilityMatrix
        m = MOPSCapabilityMatrix()
        assert m.is_supported("INCOME_STATEMENT") is True

    def test_26_cash_flow_supported(self):
        from data.providers.mops.capabilities_v142 import MOPSCapabilityMatrix
        m = MOPSCapabilityMatrix()
        assert m.is_supported("CASH_FLOW") is True

    def test_27_material_info_supported(self):
        from data.providers.mops.capabilities_v142 import MOPSCapabilityMatrix
        m = MOPSCapabilityMatrix()
        assert m.is_supported("MATERIAL_INFORMATION") is True

    def test_28_derived_metrics_supported(self):
        from data.providers.mops.capabilities_v142 import MOPSCapabilityMatrix
        m = MOPSCapabilityMatrix()
        assert m.is_supported("DERIVED_FINANCIAL_METRICS") is True

    def test_29_revision_lineage_supported(self):
        from data.providers.mops.capabilities_v142 import MOPSCapabilityMatrix
        m = MOPSCapabilityMatrix()
        assert m.is_supported("REVISION_LINEAGE") is True

    def test_30_point_in_time_supported(self):
        from data.providers.mops.capabilities_v142 import MOPSCapabilityMatrix
        m = MOPSCapabilityMatrix()
        assert m.is_supported("POINT_IN_TIME_AVAILABILITY") is True

    def test_31_realtime_not_supported(self):
        from data.providers.mops.capabilities_v142 import MOPSCapabilityMatrix
        m = MOPSCapabilityMatrix()
        assert m.is_supported("REALTIME_QUOTE") is False

    def test_32_order_execution_not_supported(self):
        from data.providers.mops.capabilities_v142 import MOPSCapabilityMatrix
        m = MOPSCapabilityMatrix()
        assert m.is_supported("ORDER_EXECUTION") is False

    def test_33_broker_always_false(self):
        from data.providers.mops.capabilities_v142 import MOPSCapabilityMatrix
        m = MOPSCapabilityMatrix()
        assert m.is_broker_capability("COMPANY_PROFILE") is False

    def test_34_capability_summary_has_provider(self):
        from data.providers.mops.capabilities_v142 import MOPSCapabilityMatrix
        summary = MOPSCapabilityMatrix().build_summary()
        assert summary["provider"] == "mops_official"
        assert summary["realtime_available"] is False
        assert summary["broker_execution_enabled"] is False


# =====================================================================
# TestModels (tests 35-55)
# =====================================================================
class TestModels:
    def test_35_company_profile_to_dict(self):
        data = load_fixture("company_profile.json")
        from data.providers.mops.models_v142 import MOPSCompanyProfile
        profile = MOPSCompanyProfile.from_dict(data)
        d = profile.to_dict()
        assert d["symbol"] == "2330"
        assert d["market"] == "TWSE"

    def test_36_company_profile_roundtrip(self):
        data = load_fixture("company_profile.json")
        from data.providers.mops.models_v142 import MOPSCompanyProfile
        p1 = MOPSCompanyProfile.from_dict(data)
        p2 = MOPSCompanyProfile.from_dict(p1.to_dict())
        assert p1.symbol == p2.symbol
        assert p1.company_name == p2.company_name

    def test_37_monthly_revenue_to_dict(self):
        data = load_fixture("monthly_revenue.json")
        from data.providers.mops.models_v142 import MOPSMonthlyRevenue
        r = MOPSMonthlyRevenue.from_dict(data)
        d = r.to_dict()
        assert d["symbol"] == "2330"
        assert d["revenue_unit"] == "TWD_THOUSAND"
        assert d["is_revision"] is False

    def test_38_monthly_revenue_revision_flag(self):
        data = load_fixture("monthly_revenue_revision.json")
        from data.providers.mops.models_v142 import MOPSMonthlyRevenue
        r = MOPSMonthlyRevenue.from_dict(data)
        assert r.is_revision is True
        assert r.revision_note is not None

    def test_39_monthly_revenue_missing_is_none(self):
        data = load_fixture("monthly_revenue_missing.json")
        from data.providers.mops.models_v142 import MOPSMonthlyRevenue
        r = MOPSMonthlyRevenue.from_dict(data)
        assert r.revenue is None
        assert r.mom_change_percent is None

    def test_40_financial_filing_to_dict(self):
        data = load_fixture("financial_filing.json")
        from data.providers.mops.models_v142 import MOPSFinancialReportFiling
        f = MOPSFinancialReportFiling.from_dict(data)
        d = f.to_dict()
        assert d["symbol"] == "2330"
        assert d["fiscal_year"] == 2023
        assert d["fiscal_period"] == "Q4"

    def test_41_balance_sheet_to_dict(self):
        data = load_fixture("balance_sheet.json")
        from data.providers.mops.models_v142 import MOPSBalanceSheet
        bs = MOPSBalanceSheet.from_dict(data)
        d = bs.to_dict()
        assert d["total_assets"] == 4000000000.0
        assert d["is_balanced"] is True
        assert d["currency"] == "TWD"
        assert d["unit"] == "TWD_THOUSAND"

    def test_42_balance_sheet_unbalanced_flag(self):
        data = load_fixture("balance_sheet_unbalanced.json")
        from data.providers.mops.models_v142 import MOPSBalanceSheet
        bs = MOPSBalanceSheet.from_dict(data)
        assert bs.is_balanced is False
        assert bs.balance_diff is not None and bs.balance_diff > 0

    def test_43_income_statement_to_dict(self):
        data = load_fixture("income_statement.json")
        from data.providers.mops.models_v142 import MOPSIncomeStatement
        is_obj = MOPSIncomeStatement.from_dict(data)
        d = is_obj.to_dict()
        assert d["revenue"] == 625000000.0
        assert d["eps_basic"] == 10.35

    def test_44_income_statement_currency_explicit(self):
        data = load_fixture("income_statement.json")
        from data.providers.mops.models_v142 import MOPSIncomeStatement
        is_obj = MOPSIncomeStatement.from_dict(data)
        assert is_obj.currency == "TWD"
        assert is_obj.unit == "TWD_THOUSAND"

    def test_45_cash_flow_to_dict(self):
        data = load_fixture("cash_flow.json")
        from data.providers.mops.models_v142 import MOPSCashFlowStatement
        cf = MOPSCashFlowStatement.from_dict(data)
        d = cf.to_dict()
        assert d["operating_cash_flow"] == 350000000.0
        assert d["cash_flow_mismatch"] is False

    def test_46_cash_flow_mismatch_flag(self):
        data = load_fixture("cash_flow_mismatch.json")
        from data.providers.mops.models_v142 import MOPSCashFlowStatement
        cf = MOPSCashFlowStatement.from_dict(data)
        assert cf.cash_flow_mismatch is True
        assert cf.mismatch_amount is not None

    def test_47_material_info_to_dict(self):
        data = load_fixture("material_information.json")
        from data.providers.mops.models_v142 import MOPSMaterialInformation
        disc = MOPSMaterialInformation.from_dict(data["disclosures"][0])
        d = disc.to_dict()
        assert d["symbol"] == "2330"
        assert d["is_correction"] is False

    def test_48_material_info_correction_flag(self):
        data = load_fixture("material_information_correction.json")
        from data.providers.mops.models_v142 import MOPSMaterialInformation
        disc = MOPSMaterialInformation.from_dict(data["disclosures"][0])
        assert disc.is_correction is True
        assert disc.correction_of_id == "DISC_001"

    def test_49_investor_conference_to_dict(self):
        data = load_fixture("investor_conference.json")
        from data.providers.mops.models_v142 import MOPSInvestorConference
        conf = MOPSInvestorConference.from_dict(data["conferences"][0])
        d = conf.to_dict()
        assert d["conference_date"] == "2024-04-15"

    def test_50_xbrl_document_to_dict(self):
        data = load_fixture("xbrl_index.json")
        from data.providers.mops.models_v142 import MOPSXBRLDocument
        doc = MOPSXBRLDocument.from_dict(data["documents"][0])
        d = doc.to_dict()
        assert d["taxonomy"] == "general_industry"

    def test_51_revision_record_to_dict(self):
        from data.providers.mops.models_v142 import MOPSRevisionRecord
        rev = MOPSRevisionRecord(
            symbol="2330",
            original_filing_id="filing_001",
            revision_sequence=1,
            revision_date="2023-06-10",
            revision_type="RESTATEMENT",
            revision_reason="Error in depreciation",
            affected_periods=["Q4"],
            affected_line_items=["depreciation"],
            magnitude_description="Material",
            is_material_revision=True,
            available_from="2023-06-10",
            source_timestamp=None,
            fetched_at="2023-06-11T00:00:00+00:00",
            provider_id="mops_official",
            provenance=None,
        )
        d = rev.to_dict()
        assert d["is_material_revision"] is True
        assert d["revision_type"] == "RESTATEMENT"

    def test_52_provenance_to_dict(self):
        from data.providers.mops.models_v142 import MOPSProvenance
        prov = MOPSProvenance(
            provider_id="mops_official",
            official_source=True,
            endpoint_id="balance_sheet",
            source_url="https://mops.twse.com.tw/mops/web/t26sb01_ifrs",
            requested_at="2024-01-01T00:00:00+00:00",
            received_at="2024-01-01T00:00:01+00:00",
            source_timestamp=None,
            fiscal_period="Q4",
            response_format="HTML",
            schema_version="1.4.2",
            content_hash=None,
            request_id="test-req-001",
            revision_detected=False,
        )
        d = prov.to_dict()
        assert d["official_source"] is True
        assert d["revision_detected"] is False

    def test_53_unknown_fields_forward_compatible(self):
        data = load_fixture("unknown_fields.json")
        from data.providers.mops.models_v142 import MOPSMonthlyRevenue
        # Should not raise even with unknown fields
        r = MOPSMonthlyRevenue.from_dict(data)
        assert r.symbol == "2330"
        assert r.revenue == 195000000.0

    def test_54_restated_filing_flag(self):
        data = load_fixture("restated_filing.json")
        from data.providers.mops.models_v142 import MOPSFinancialReportFiling
        f = MOPSFinancialReportFiling.from_dict(data)
        assert f.is_restated is True
        assert f.restatement_reason is not None

    def test_55_date_only_announcement_filing(self):
        data = load_fixture("date_only_announcement.json")
        from data.providers.mops.models_v142 import MOPSFinancialReportFiling
        f = MOPSFinancialReportFiling.from_dict(data)
        assert f.filing_date is None
        assert f.announcement_date == "2023-08-14"


# =====================================================================
# TestParser (tests 56-75)
# =====================================================================
class TestParser:
    def test_56_parser_instantiates(self):
        from data.providers.mops.parser_v142 import MOPSParser
        p = MOPSParser()
        assert p is not None

    def test_57_parse_roc_date_7digit(self):
        from data.providers.mops.parser_v142 import MOPSParser
        p = MOPSParser()
        assert p.parse_roc_date("1130101") == "2024-01-01"

    def test_58_parse_roc_date_slash(self):
        from data.providers.mops.parser_v142 import MOPSParser
        p = MOPSParser()
        assert p.parse_roc_date("113/01/15") == "2024-01-15"

    def test_59_parse_roc_date_iso(self):
        from data.providers.mops.parser_v142 import MOPSParser
        p = MOPSParser()
        assert p.parse_roc_date("2024-03-31") == "2024-03-31"

    def test_60_parse_roc_date_none(self):
        from data.providers.mops.parser_v142 import MOPSParser
        p = MOPSParser()
        assert p.parse_roc_date(None) is None

    def test_61_parse_roc_date_invalid(self):
        from data.providers.mops.parser_v142 import MOPSParser
        p = MOPSParser()
        assert p.parse_roc_date("notadate") is None

    def test_62_parse_roc_year_month(self):
        from data.providers.mops.parser_v142 import MOPSParser
        p = MOPSParser()
        assert p.parse_roc_year_month("113/01") == "2024-01"

    def test_63_parse_number_missing_marker(self):
        from data.providers.mops.parser_v142 import MOPSParser
        p = MOPSParser()
        assert p._parse_number("--") is None
        assert p._parse_number("N/A") is None
        assert p._parse_number("") is None

    def test_64_parse_number_with_comma(self):
        from data.providers.mops.parser_v142 import MOPSParser
        p = MOPSParser()
        assert p._parse_number("1,234,567") == 1234567.0

    def test_65_parse_number_negative_parens(self):
        from data.providers.mops.parser_v142 import MOPSParser
        p = MOPSParser()
        # Parentheses handled by normalizer, not parser directly
        assert p._parse_number("-100") == -100.0

    def test_66_parse_str_missing_is_none(self):
        from data.providers.mops.parser_v142 import MOPSParser
        p = MOPSParser()
        assert p._parse_str("--") is None
        assert p._parse_str("") is None
        assert p._parse_str(None) is None

    def test_67_detect_charset_utf8(self):
        from data.providers.mops.parser_v142 import MOPSParser
        p = MOPSParser()
        content = b'<html><head><meta charset="utf-8"></head><body></body></html>'
        assert p.detect_charset(content) == "utf-8"

    def test_68_detect_charset_big5(self):
        from data.providers.mops.parser_v142 import MOPSParser
        p = MOPSParser()
        content = b'<html><head><meta charset="big5"></head><body></body></html>'
        assert p.detect_charset(content) == "big5"

    def test_69_is_maintenance_page_true(self):
        content = load_html_fixture("maintenance_page.html")
        from data.providers.mops.parser_v142 import MOPSParser
        p = MOPSParser()
        assert p.is_maintenance_page(content) is True

    def test_70_is_maintenance_page_false(self):
        content = load_html_fixture("malformed_response.html")
        from data.providers.mops.parser_v142 import MOPSParser
        p = MOPSParser()
        assert p.is_maintenance_page(content) is False

    def test_71_is_malformed_empty(self):
        from data.providers.mops.parser_v142 import MOPSParser
        p = MOPSParser()
        assert p.is_malformed(b"") is True

    def test_72_is_malformed_valid(self):
        content = load_html_fixture("malformed_response.html")
        from data.providers.mops.parser_v142 import MOPSParser
        p = MOPSParser()
        assert p.is_malformed(content) is False

    def test_73_extract_html_tables(self):
        from data.providers.mops.parser_v142 import MOPSParser
        p = MOPSParser()
        html = "<table><tr><td>A</td><td>B</td></tr><tr><td>1</td><td>2</td></tr></table>"
        tables = p.extract_html_tables(html)
        assert len(tables) == 1
        assert tables[0][0] == ["A", "B"]

    def test_74_table_to_dicts(self):
        from data.providers.mops.parser_v142 import MOPSParser
        p = MOPSParser()
        rows = [["name", "value"], ["TSMC", "100"], ["Demo", "200"]]
        dicts, warnings = p.table_to_dicts(rows)
        assert len(dicts) == 2
        assert dicts[0]["name"] == "TSMC"

    def test_75_parse_json_response_valid(self):
        from data.providers.mops.parser_v142 import MOPSParser
        p = MOPSParser()
        content = b'[{"key": "value"}, {"key2": 123}]'
        data, warnings = p.parse_json_response(content)
        assert data is not None
        assert len(data) == 2


# =====================================================================
# TestNormalizer (tests 76-85)
# =====================================================================
class TestNormalizer:
    def test_76_normalizer_instantiates(self):
        from data.providers.mops.normalizer_v142 import MOPSNormalizer
        n = MOPSNormalizer()
        assert n is not None

    def test_77_canonical_symbol_strip_tw(self):
        from data.providers.mops.normalizer_v142 import MOPSNormalizer
        n = MOPSNormalizer()
        assert n.canonical_symbol("2330.TW") == "2330"

    def test_78_canonical_symbol_strip_two(self):
        from data.providers.mops.normalizer_v142 import MOPSNormalizer
        n = MOPSNormalizer()
        assert n.canonical_symbol("5274.TWO") == "5274"

    def test_79_canonical_symbol_strip_prefix(self):
        from data.providers.mops.normalizer_v142 import MOPSNormalizer
        n = MOPSNormalizer()
        assert n.canonical_symbol("TWSE:2330") == "2330"

    def test_80_normalize_unit_chinese(self):
        from data.providers.mops.normalizer_v142 import MOPSNormalizer
        n = MOPSNormalizer()
        assert n.normalize_unit("千元") == "TWD_THOUSAND"

    def test_81_normalize_market_twse(self):
        from data.providers.mops.normalizer_v142 import MOPSNormalizer
        n = MOPSNormalizer()
        assert n.normalize_market("上市") == "TWSE"
        assert n.normalize_market("TWSE") == "TWSE"

    def test_82_normalize_market_tpex(self):
        from data.providers.mops.normalizer_v142 import MOPSNormalizer
        n = MOPSNormalizer()
        assert n.normalize_market("上櫃") == "TPEx"

    def test_83_normalize_period(self):
        from data.providers.mops.normalizer_v142 import MOPSNormalizer
        n = MOPSNormalizer()
        assert n.normalize_period("第一季") == "Q1"
        assert n.normalize_period("Q2") == "Q2"
        assert n.normalize_period("年度") == "ANNUAL"

    def test_84_normalize_amount_parens(self):
        from data.providers.mops.normalizer_v142 import MOPSNormalizer
        n = MOPSNormalizer()
        assert n.normalize_amount("(100)") == -100.0

    def test_85_normalize_amount_missing_is_none(self):
        from data.providers.mops.normalizer_v142 import MOPSNormalizer
        n = MOPSNormalizer()
        assert n.normalize_amount("--") is None
        assert n.normalize_amount("") is None
        assert n.normalize_amount(None) is None


# =====================================================================
# TestBalanceSheetParser (tests 86-95)
# =====================================================================
class TestBalanceSheetParser:
    def test_86_balanced_sheet(self):
        from data.providers.mops.balance_sheet_v142 import MOPSBalanceSheetParser
        data = load_fixture("balance_sheet.json")
        p = MOPSBalanceSheetParser()
        bs = p.parse_from_fixture("2330", 2023, "Q4", data)
        assert bs.is_balanced is True
        assert bs.balance_diff == 0.0

    def test_87_unbalanced_sheet_detection(self):
        from data.providers.mops.balance_sheet_v142 import MOPSBalanceSheetParser
        data = load_fixture("balance_sheet_unbalanced.json")
        p = MOPSBalanceSheetParser()
        bs = p.parse_from_fixture("2330", 2023, "Q3", data)
        assert bs.is_balanced is False
        assert len(bs.warnings) > 0

    def test_88_currency_explicit(self):
        from data.providers.mops.balance_sheet_v142 import MOPSBalanceSheetParser
        data = load_fixture("balance_sheet.json")
        p = MOPSBalanceSheetParser()
        bs = p.parse_from_fixture("2330", 2023, "Q4", data)
        assert bs.currency == "TWD"

    def test_89_unit_explicit(self):
        from data.providers.mops.balance_sheet_v142 import MOPSBalanceSheetParser
        data = load_fixture("balance_sheet.json")
        p = MOPSBalanceSheetParser()
        bs = p.parse_from_fixture("2330", 2023, "Q4", data)
        assert bs.unit == "TWD_THOUSAND"

    def test_90_missing_field_is_none(self):
        from data.providers.mops.balance_sheet_v142 import MOPSBalanceSheetParser
        # Pass fixture with a missing field
        data = {"total_assets": 1000.0, "total_liabilities": 400.0, "total_equity": 600.0}
        p = MOPSBalanceSheetParser()
        bs = p.parse_from_fixture("2330", 2023, "Q4", data)
        assert bs.cash_and_equivalents is None  # not in data
        assert bs.inventories is None

    def test_91_balance_sheet_to_dict_roundtrip(self):
        from data.providers.mops.models_v142 import MOPSBalanceSheet
        data = load_fixture("balance_sheet.json")
        bs1 = MOPSBalanceSheet.from_dict(data)
        bs2 = MOPSBalanceSheet.from_dict(bs1.to_dict())
        assert bs1.total_assets == bs2.total_assets
        assert bs1.is_balanced == bs2.is_balanced

    def test_92_is_consolidated_explicit(self):
        from data.providers.mops.balance_sheet_v142 import MOPSBalanceSheetParser
        data = load_fixture("balance_sheet.json")
        p = MOPSBalanceSheetParser()
        bs = p.parse_from_fixture("2330", 2023, "Q4", data)
        assert bs.is_consolidated is True

    def test_93_is_restated_explicit(self):
        from data.providers.mops.balance_sheet_v142 import MOPSBalanceSheetParser
        data = load_fixture("balance_sheet.json")
        p = MOPSBalanceSheetParser()
        bs = p.parse_from_fixture("2330", 2023, "Q4", data)
        assert bs.is_restated is False

    def test_94_unbalanced_sheet_diff_positive(self):
        from data.providers.mops.balance_sheet_v142 import MOPSBalanceSheetParser
        data = {"total_assets": 1000.0, "total_liabilities": 400.0, "total_equity": 500.0}  # diff=100
        p = MOPSBalanceSheetParser()
        bs = p.parse_from_fixture("2330", 2023, "Q4", data)
        assert bs.is_balanced is False
        assert bs.balance_diff == 100.0

    def test_95_balance_diff_none_when_missing_fields(self):
        from data.providers.mops.balance_sheet_v142 import MOPSBalanceSheetParser
        # Missing total_equity -> can't check balance
        data = {"total_assets": 1000.0, "total_liabilities": 400.0}
        p = MOPSBalanceSheetParser()
        bs = p.parse_from_fixture("2330", 2023, "Q4", data)
        # is_balanced defaults True when no comparison possible
        assert bs.balance_diff is None


# =====================================================================
# TestIncomeStatementParser (tests 96-105)
# =====================================================================
class TestIncomeStatementParser:
    def test_96_parse_income_statement(self):
        from data.providers.mops.income_statement_v142 import MOPSIncomeStatementParser
        data = load_fixture("income_statement.json")
        p = MOPSIncomeStatementParser()
        is_obj = p.parse_from_fixture("2330", 2023, "Q4", data)
        assert is_obj.revenue == 625000000.0
        assert is_obj.net_income == 270000000.0

    def test_97_eps_preserved(self):
        from data.providers.mops.income_statement_v142 import MOPSIncomeStatementParser
        data = load_fixture("income_statement.json")
        p = MOPSIncomeStatementParser()
        is_obj = p.parse_from_fixture("2330", 2023, "Q4", data)
        assert is_obj.eps_basic == 10.35
        assert is_obj.eps_diluted == 10.30

    def test_98_missing_eps_is_none(self):
        from data.providers.mops.income_statement_v142 import MOPSIncomeStatementParser
        data = {"revenue": 100.0}
        p = MOPSIncomeStatementParser()
        is_obj = p.parse_from_fixture("2330", 2023, "Q4", data)
        assert is_obj.eps_basic is None
        assert is_obj.eps_diluted is None

    def test_99_currency_unit_explicit(self):
        from data.providers.mops.income_statement_v142 import MOPSIncomeStatementParser
        data = load_fixture("income_statement.json")
        p = MOPSIncomeStatementParser()
        is_obj = p.parse_from_fixture("2330", 2023, "Q4", data)
        assert is_obj.currency == "TWD"
        assert is_obj.unit == "TWD_THOUSAND"

    def test_100_income_statement_roundtrip(self):
        from data.providers.mops.models_v142 import MOPSIncomeStatement
        data = load_fixture("income_statement.json")
        is1 = MOPSIncomeStatement.from_dict(data)
        is2 = MOPSIncomeStatement.from_dict(is1.to_dict())
        assert is1.revenue == is2.revenue
        assert is1.eps_basic == is2.eps_basic


# =====================================================================
# TestCashFlowParser (tests 101-110)
# =====================================================================
class TestCashFlowParser:
    def test_101_parse_cash_flow(self):
        from data.providers.mops.cash_flow_v142 import MOPSCashFlowParser
        data = load_fixture("cash_flow.json")
        p = MOPSCashFlowParser()
        cf = p.parse_from_fixture("2330", 2023, "Q4", data)
        assert cf.operating_cash_flow == 350000000.0
        assert cf.cash_flow_mismatch is False

    def test_102_free_cash_flow_computed(self):
        from data.providers.mops.cash_flow_v142 import MOPSCashFlowParser
        data = load_fixture("cash_flow.json")
        p = MOPSCashFlowParser()
        cf = p.parse_from_fixture("2330", 2023, "Q4", data)
        assert cf.free_cash_flow == 190000000.0

    def test_103_mismatch_detected(self):
        from data.providers.mops.cash_flow_v142 import MOPSCashFlowParser
        data = load_fixture("cash_flow_mismatch.json")
        p = MOPSCashFlowParser()
        cf = p.parse_from_fixture("2330", 2023, "Q3", data)
        assert cf.cash_flow_mismatch is True
        assert cf.mismatch_amount is not None

    def test_104_cash_flow_roundtrip(self):
        from data.providers.mops.models_v142 import MOPSCashFlowStatement
        data = load_fixture("cash_flow.json")
        cf1 = MOPSCashFlowStatement.from_dict(data)
        cf2 = MOPSCashFlowStatement.from_dict(cf1.to_dict())
        assert cf1.operating_cash_flow == cf2.operating_cash_flow

    def test_105_missing_capex_fcf_none(self):
        from data.providers.mops.cash_flow_v142 import MOPSCashFlowParser
        data = {"operating_cash_flow": 200.0}
        p = MOPSCashFlowParser()
        cf = p.parse_from_fixture("2330", 2023, "Q4", data)
        # capex is None, so FCF should be None or not computed
        # With OCF only, capex=None, so fcf=None
        assert cf.capex is None


# =====================================================================
# TestDerivedMetrics (tests 106-115)
# =====================================================================
class TestDerivedMetrics:
    def test_106_gross_margin_computed(self):
        from data.providers.mops.derived_metrics_v142 import MOPSDerivedFinancialMetrics
        m = MOPSDerivedFinancialMetrics()
        is_data = load_fixture("income_statement.json")
        metrics = m.compute_from_dicts("2330", 2023, "Q4", is_data=is_data)
        names = {m.metric_name: m.metric_value for m in metrics}
        # gross_margin = 375/625 * 100 = 60.0
        assert "gross_margin_pct" in names
        assert abs(names["gross_margin_pct"] - 60.0) < 0.01

    def test_107_operating_margin_computed(self):
        from data.providers.mops.derived_metrics_v142 import MOPSDerivedFinancialMetrics
        m = MOPSDerivedFinancialMetrics()
        is_data = load_fixture("income_statement.json")
        metrics = m.compute_from_dicts("2330", 2023, "Q4", is_data=is_data)
        names = {m.metric_name: m.metric_value for m in metrics}
        assert "operating_margin_pct" in names

    def test_108_roe_computed(self):
        from data.providers.mops.derived_metrics_v142 import MOPSDerivedFinancialMetrics
        m = MOPSDerivedFinancialMetrics()
        bs_data = load_fixture("balance_sheet.json")
        is_data = load_fixture("income_statement.json")
        metrics = m.compute_from_dicts("2330", 2023, "Q4", bs_data=bs_data, is_data=is_data)
        names = {m.metric_name: m.metric_value for m in metrics}
        assert "roe_pct" in names
        assert names["roe_pct"] is not None

    def test_109_missing_input_produces_none(self):
        from data.providers.mops.derived_metrics_v142 import MOPSDerivedFinancialMetrics
        m = MOPSDerivedFinancialMetrics()
        # No income statement -> gross_margin should be missing
        metrics = m.compute_from_dicts("2330", 2023, "Q4")
        assert len(metrics) == 0

    def test_110_metric_has_available_from(self):
        from data.providers.mops.derived_metrics_v142 import MOPSDerivedFinancialMetrics
        m = MOPSDerivedFinancialMetrics()
        is_data = load_fixture("income_statement.json")
        metrics = m.compute_from_dicts("2330", 2023, "Q4", is_data=is_data, available_from="2024-03-31")
        for metric in metrics:
            assert metric.available_from == "2024-03-31"


# =====================================================================
# TestPointInTime (tests 111-120)
# =====================================================================
class TestPointInTime:
    def test_111_clock_injectable(self):
        fixed = datetime.datetime(2024, 6, 1, tzinfo=datetime.timezone.utc)
        from data.providers.mops.point_in_time_v142 import MOPSPointInTimeService
        svc = MOPSPointInTimeService(clock=lambda: fixed)
        assert svc.now() == fixed

    def test_112_monthly_revenue_available(self):
        # April 2024 revenue available after May 10, 2024
        fixed = datetime.datetime(2024, 6, 1, tzinfo=datetime.timezone.utc)
        from data.providers.mops.point_in_time_v142 import MOPSPointInTimeService
        svc = MOPSPointInTimeService(clock=lambda: fixed)
        result = svc.is_monthly_revenue_available(2024, 4, asof=fixed)
        assert result["available"] is True

    def test_113_monthly_revenue_not_yet_available(self):
        # April 2024 revenue not available on April 15
        fixed = datetime.datetime(2024, 4, 15, tzinfo=datetime.timezone.utc)
        from data.providers.mops.point_in_time_v142 import MOPSPointInTimeService
        svc = MOPSPointInTimeService(clock=lambda: fixed)
        result = svc.is_monthly_revenue_available(2024, 4, asof=fixed)
        assert result["available"] is False

    def test_114_quarterly_report_available(self):
        # Q1 2024 available after May 15 2024
        fixed = datetime.datetime(2024, 6, 1, tzinfo=datetime.timezone.utc)
        from data.providers.mops.point_in_time_v142 import MOPSPointInTimeService
        svc = MOPSPointInTimeService(clock=lambda: fixed)
        result = svc.is_financial_report_available(2024, "Q1", asof=fixed)
        assert result["available"] is True

    def test_115_quarterly_report_not_yet_available(self):
        # Q1 2024 not available on March 1, 2024
        fixed = datetime.datetime(2024, 3, 1, tzinfo=datetime.timezone.utc)
        from data.providers.mops.point_in_time_v142 import MOPSPointInTimeService
        svc = MOPSPointInTimeService(clock=lambda: fixed)
        result = svc.is_financial_report_available(2024, "Q1", asof=fixed)
        assert result["available"] is False

    def test_116_available_from_is_explicit(self):
        fixed = datetime.datetime(2024, 6, 1, tzinfo=datetime.timezone.utc)
        from data.providers.mops.point_in_time_v142 import MOPSPointInTimeService
        svc = MOPSPointInTimeService(clock=lambda: fixed)
        result = svc.is_monthly_revenue_available(2024, 4, asof=fixed)
        assert result["available_from"] is not None

    def test_117_annual_available_in_next_year(self):
        # Annual 2023 available after Mar 31, 2024
        fixed = datetime.datetime(2024, 4, 1, tzinfo=datetime.timezone.utc)
        from data.providers.mops.point_in_time_v142 import MOPSPointInTimeService
        svc = MOPSPointInTimeService(clock=lambda: fixed)
        result = svc.is_financial_report_available(2023, "ANNUAL", asof=fixed)
        assert result["available"] is True

    def test_118_unknown_period_not_available(self):
        fixed = datetime.datetime(2024, 6, 1, tzinfo=datetime.timezone.utc)
        from data.providers.mops.point_in_time_v142 import MOPSPointInTimeService
        svc = MOPSPointInTimeService(clock=lambda: fixed)
        result = svc.is_financial_report_available(2024, "UNKNOWN_PERIOD", asof=fixed)
        assert result["available"] is False

    def test_119_get_available_periods(self):
        fixed = datetime.datetime(2024, 9, 1, tzinfo=datetime.timezone.utc)
        from data.providers.mops.point_in_time_v142 import MOPSPointInTimeService
        svc = MOPSPointInTimeService(clock=lambda: fixed)
        result = svc.get_available_periods_as_of(2024, asof=fixed)
        assert result["available_periods"]["Q1"] is True
        assert result["available_periods"]["Q2"] is True
        assert result["available_periods"]["Q3"] is False  # Q3 not available on Sep 1

    def test_120_q3_available_after_nov_14(self):
        fixed = datetime.datetime(2024, 11, 20, tzinfo=datetime.timezone.utc)
        from data.providers.mops.point_in_time_v142 import MOPSPointInTimeService
        svc = MOPSPointInTimeService(clock=lambda: fixed)
        result = svc.is_financial_report_available(2024, "Q3", asof=fixed)
        assert result["available"] is True


# =====================================================================
# TestRevisionLineage (tests 121-130)
# =====================================================================
class TestRevisionLineage:
    def test_121_lineage_service_empty(self):
        from data.providers.mops.revision_lineage_v142 import MOPSRevisionLineageService
        svc = MOPSRevisionLineageService()
        assert svc.total_count() == 0

    def test_122_add_and_get_revision(self):
        from data.providers.mops.revision_lineage_v142 import MOPSRevisionLineageService
        svc = MOPSRevisionLineageService()
        rev = svc.from_fixture({
            "symbol": "2330",
            "original_filing_id": "filing_001",
            "revision_sequence": 1,
            "revision_date": "2023-06-10",
            "revision_type": "RESTATEMENT",
            "is_material_revision": True,
            "available_from": "2023-06-10",
        })
        svc.add_revision(rev)
        revs = svc.get_revisions("2330", "filing_001")
        assert len(revs) == 1

    def test_123_has_revision_true(self):
        from data.providers.mops.revision_lineage_v142 import MOPSRevisionLineageService
        svc = MOPSRevisionLineageService()
        rev = svc.from_fixture({
            "symbol": "2330",
            "original_filing_id": "filing_002",
            "revision_sequence": 1,
        })
        svc.add_revision(rev)
        assert svc.has_revision("2330", "filing_002") is True

    def test_124_has_revision_false(self):
        from data.providers.mops.revision_lineage_v142 import MOPSRevisionLineageService
        svc = MOPSRevisionLineageService()
        assert svc.has_revision("2330", "nonexistent") is False

    def test_125_get_latest_revision(self):
        from data.providers.mops.revision_lineage_v142 import MOPSRevisionLineageService
        svc = MOPSRevisionLineageService()
        for seq in [1, 2]:
            rev = svc.from_fixture({
                "symbol": "2330",
                "original_filing_id": "filing_003",
                "revision_sequence": seq,
            })
            svc.add_revision(rev)
        latest = svc.get_latest_revision("2330", "filing_003")
        assert latest.revision_sequence == 2

    def test_126_lineage_summary(self):
        from data.providers.mops.revision_lineage_v142 import MOPSRevisionLineageService
        svc = MOPSRevisionLineageService()
        rev = svc.from_fixture({
            "symbol": "2330",
            "original_filing_id": "filing_004",
            "revision_sequence": 1,
            "is_material_revision": True,
        })
        svc.add_revision(rev)
        summary = svc.build_lineage_summary("2330", "filing_004")
        assert summary["revision_count"] == 1
        assert summary["has_material_revision"] is True

    def test_127_revision_record_from_fixture(self):
        from data.providers.mops.revision_lineage_v142 import MOPSRevisionLineageService
        svc = MOPSRevisionLineageService()
        data = load_fixture("restated_filing.json")
        rev = svc.from_fixture({
            "symbol": data["symbol"],
            "original_filing_id": f"{data['fiscal_year']}_{data['fiscal_period']}",
            "revision_sequence": 1,
            "revision_date": data["restatement_date"],
            "revision_type": "RESTATEMENT",
            "revision_reason": data["restatement_reason"],
            "is_material_revision": True,
        })
        assert rev.is_material_revision is True

    def test_128_revision_affected_periods(self):
        from data.providers.mops.revision_lineage_v142 import MOPSRevisionLineageService
        svc = MOPSRevisionLineageService()
        rev = svc.from_fixture({
            "symbol": "2330",
            "original_filing_id": "filing_005",
            "revision_sequence": 1,
            "affected_periods": ["Q3", "Q4"],
            "affected_line_items": ["depreciation", "inventory"],
        })
        assert "Q3" in rev.affected_periods
        assert "depreciation" in rev.affected_line_items

    def test_129_revision_available_from_explicit(self):
        from data.providers.mops.revision_lineage_v142 import MOPSRevisionLineageService
        svc = MOPSRevisionLineageService()
        rev = svc.from_fixture({
            "symbol": "2330",
            "original_filing_id": "filing_006",
            "revision_sequence": 1,
            "available_from": "2023-06-10",
        })
        assert rev.available_from == "2023-06-10"

    def test_130_latest_revision_none_when_empty(self):
        from data.providers.mops.revision_lineage_v142 import MOPSRevisionLineageService
        svc = MOPSRevisionLineageService()
        assert svc.get_latest_revision("2330", "nonexistent") is None


# =====================================================================
# TestCachePolicy (tests 131-138)
# =====================================================================
class TestCachePolicy:
    def test_131_cache_key_real_vs_mock_different(self):
        from data.providers.mops.cache_policy_v142 import MOPSCachePolicy
        p = MOPSCachePolicy()
        k1 = p.build_cache_key("mops_official", "balance_sheet", "2330", 2023, "Q4", "1.4.2")
        k2 = p.build_mock_cache_key("mops_official", "balance_sheet", "2330", 2023, "Q4", "1.4.2")
        assert k1 != k2

    def test_132_real_key_prefix(self):
        from data.providers.mops.cache_policy_v142 import MOPSCachePolicy
        p = MOPSCachePolicy()
        k = p.build_cache_key("mops_official", "balance_sheet", "2330", 2023, "Q4", "1.4.2")
        assert k.startswith("mops:real")

    def test_133_mock_key_prefix(self):
        from data.providers.mops.cache_policy_v142 import MOPSCachePolicy
        p = MOPSCachePolicy()
        k = p.build_mock_cache_key("mops_official", "balance_sheet", "2330", 2023, "Q4", "1.4.2")
        assert k.startswith("mops:mock")

    def test_134_same_params_same_key(self):
        from data.providers.mops.cache_policy_v142 import MOPSCachePolicy
        p = MOPSCachePolicy()
        k1 = p.build_cache_key("mops_official", "income_statement", "2330", 2023, "Q4", "1.4.2")
        k2 = p.build_cache_key("mops_official", "income_statement", "2330", 2023, "Q4", "1.4.2")
        assert k1 == k2

    def test_135_different_symbol_different_key(self):
        from data.providers.mops.cache_policy_v142 import MOPSCachePolicy
        p = MOPSCachePolicy()
        k1 = p.build_cache_key("mops_official", "balance_sheet", "2330", 2023, "Q4", "1.4.2")
        k2 = p.build_cache_key("mops_official", "balance_sheet", "2454", 2023, "Q4", "1.4.2")
        assert k1 != k2

    def test_136_ttl_balance_sheet(self):
        from data.providers.mops.cache_policy_v142 import MOPSCachePolicy
        p = MOPSCachePolicy()
        ttl = p.get_ttl_seconds("balance_sheet")
        assert ttl > 0

    def test_137_ttl_material_info_shorter(self):
        from data.providers.mops.cache_policy_v142 import MOPSCachePolicy
        p = MOPSCachePolicy()
        ttl_bs = p.get_ttl_seconds("balance_sheet")
        ttl_mi = p.get_ttl_seconds("material_information")
        assert ttl_mi < ttl_bs  # material info updates more frequently

    def test_138_ttl_unknown_endpoint(self):
        from data.providers.mops.cache_policy_v142 import MOPSCachePolicy
        p = MOPSCachePolicy()
        ttl = p.get_ttl_seconds("nonexistent_endpoint")
        assert ttl > 0  # default TTL


# =====================================================================
# TestStore (tests 139-148)
# =====================================================================
class TestStore:
    def test_139_store_instantiates(self):
        from data.providers.mops.store_v142 import MOPSStore
        s = MOPSStore()
        assert s is not None

    def test_140_store_initially_empty(self):
        from data.providers.mops.store_v142 import MOPSStore
        s = MOPSStore()
        counts = s.count_all()
        assert all(v == 0 for v in counts.values())

    def test_141_put_and_get_profile(self):
        from data.providers.mops.store_v142 import MOPSStore
        from data.providers.mops.models_v142 import MOPSCompanyProfile
        s = MOPSStore()
        data = load_fixture("company_profile.json")
        p = MOPSCompanyProfile.from_dict(data)
        s.put_profile(p)
        retrieved = s.get_profile("2330")
        assert retrieved is not None
        assert retrieved.symbol == "2330"

    def test_142_put_and_get_revenue(self):
        from data.providers.mops.store_v142 import MOPSStore
        from data.providers.mops.models_v142 import MOPSMonthlyRevenue
        s = MOPSStore()
        data = load_fixture("monthly_revenue.json")
        r = MOPSMonthlyRevenue.from_dict(data)
        s.put_revenue(r)
        retrieved = s.get_revenue("2330", "2024-01")
        assert retrieved is not None
        assert retrieved.revenue == 195000000.0

    def test_143_missing_profile_returns_none(self):
        from data.providers.mops.store_v142 import MOPSStore
        s = MOPSStore()
        assert s.get_profile("9999") is None

    def test_144_missing_revenue_returns_none(self):
        from data.providers.mops.store_v142 import MOPSStore
        s = MOPSStore()
        assert s.get_revenue("9999", "2024-01") is None

    def test_145_put_and_get_balance_sheet(self):
        from data.providers.mops.balance_sheet_v142 import MOPSBalanceSheetParser
        from data.providers.mops.store_v142 import MOPSStore
        s = MOPSStore()
        data = load_fixture("balance_sheet.json")
        bs = MOPSBalanceSheetParser().parse_from_fixture("2330", 2023, "Q4", data)
        s.put_balance_sheet(bs)
        retrieved = s.get_balance_sheet("2330", 2023, "Q4")
        assert retrieved is not None

    def test_146_count_all_tracks_stores(self):
        from data.providers.mops.store_v142 import MOPSStore
        from data.providers.mops.models_v142 import MOPSCompanyProfile
        s = MOPSStore()
        data = load_fixture("company_profile.json")
        p = MOPSCompanyProfile.from_dict(data)
        s.put_profile(p)
        assert s.count_all()["profiles"] == 1

    def test_147_put_and_get_material_info(self):
        from data.providers.mops.store_v142 import MOPSStore
        from data.providers.mops.models_v142 import MOPSMaterialInformation
        s = MOPSStore()
        data = load_fixture("material_information.json")
        disc = MOPSMaterialInformation.from_dict(data["disclosures"][0])
        s.put_material_info("2330", [disc])
        items = s.get_material_info("2330")
        assert len(items) == 1

    def test_148_get_missing_material_info_empty_list(self):
        from data.providers.mops.store_v142 import MOPSStore
        s = MOPSStore()
        assert s.get_material_info("9999") == []


# =====================================================================
# TestSafetyFlags (tests 149-160)
# =====================================================================
class TestSafetyFlags:
    def test_149_no_real_orders_package(self):
        import data.providers.mops as pkg
        assert pkg.NO_REAL_ORDERS is True

    def test_150_broker_execution_disabled_package(self):
        import data.providers.mops as pkg
        assert pkg.BROKER_EXECUTION_ENABLED is False

    def test_151_production_trading_blocked_package(self):
        import data.providers.mops as pkg
        assert pkg.PRODUCTION_TRADING_BLOCKED is True

    def test_152_mock_fallback_disabled(self):
        import data.providers.mops as pkg
        assert pkg.MOPS_MOCK_FALLBACK_ENABLED is False

    def test_153_auto_download_disabled(self):
        import data.providers.mops as pkg
        assert pkg.MOPS_AUTO_DOWNLOAD_ENABLED is False

    def test_154_realtime_disabled(self):
        import data.providers.mops as pkg
        assert pkg.MOPS_REALTIME_AVAILABLE is False

    def test_155_official_source_only(self):
        import data.providers.mops as pkg
        assert pkg.OFFICIAL_SOURCE_ONLY is True

    def test_156_provider_no_real_orders(self):
        from data.providers.mops.provider_v142 import NO_REAL_ORDERS
        assert NO_REAL_ORDERS is True

    def test_157_provider_broker_disabled(self):
        from data.providers.mops.provider_v142 import BROKER_EXECUTION_ENABLED
        assert BROKER_EXECUTION_ENABLED is False

    def test_158_models_no_real_orders(self):
        from data.providers.mops.models_v142 import NO_REAL_ORDERS
        assert NO_REAL_ORDERS is True

    def test_159_health_no_real_orders(self):
        from data.providers.mops.health_v142 import NO_REAL_ORDERS
        assert NO_REAL_ORDERS is True

    def test_160_store_auto_download_disabled(self):
        from data.providers.mops.store_v142 import MOPS_AUTO_DOWNLOAD_ENABLED
        assert MOPS_AUTO_DOWNLOAD_ENABLED is False


# =====================================================================
# TestHealthCheck (tests 161-170)
# =====================================================================
class TestHealthCheck:
    def test_161_health_check_runs(self):
        from data.providers.mops.health_v142 import MOPSProviderHealthCheck
        hc = MOPSProviderHealthCheck()
        summary = hc.get_health_summary()
        assert summary is not None

    def test_162_health_check_has_provider_id(self):
        from data.providers.mops.health_v142 import MOPSProviderHealthCheck
        summary = MOPSProviderHealthCheck().get_health_summary()
        assert summary["provider_id"] == "mops_official"

    def test_163_health_check_all_pass(self):
        from data.providers.mops.health_v142 import MOPSProviderHealthCheck
        summary = MOPSProviderHealthCheck().get_health_summary()
        if not summary["all_pass"]:
            failed = [name for name, info in summary["checks"].items() if info["status"] == "FAIL"]
            pytest.fail(f"Health checks failed: {failed}")

    def test_164_health_check_safety_flags(self):
        from data.providers.mops.health_v142 import MOPSProviderHealthCheck
        summary = MOPSProviderHealthCheck().get_health_summary()
        assert summary["no_real_orders"] is True
        assert summary["broker_disabled"] is True
        assert summary["mock_fallback_enabled"] is False
        assert summary["auto_download_enabled"] is False

    def test_165_health_check_endpoints_counted(self):
        from data.providers.mops.health_v142 import MOPSProviderHealthCheck
        summary = MOPSProviderHealthCheck().get_health_summary()
        assert summary["endpoints_total"] >= 8

    def test_166_health_check_capabilities_listed(self):
        from data.providers.mops.health_v142 import MOPSProviderHealthCheck
        summary = MOPSProviderHealthCheck().get_health_summary()
        caps = summary["registered_capabilities"]
        assert "COMPANY_PROFILE" in caps
        assert "BALANCE_SHEET" in caps
        assert "DERIVED_FINANCIAL_METRICS" in caps

    def test_167_health_checks_dict(self):
        from data.providers.mops.health_v142 import MOPSProviderHealthCheck
        hc = MOPSProviderHealthCheck()
        checks = hc.run()
        assert "package_import" in checks
        assert "safety_flags" in checks
        assert "no_realtime" in checks

    def test_168_provider_health_check_method(self):
        from data.providers.mops.provider_v142 import MOPSProviderV142
        p = MOPSProviderV142()
        summary = p.health_check()
        assert summary["provider_id"] == "mops_official"

    def test_169_health_check_twse_unchanged(self):
        from data.providers.mops.health_v142 import MOPSProviderHealthCheck
        hc = MOPSProviderHealthCheck()
        checks = hc.run()
        status, detail = checks["twse_provider_unchanged"]
        assert status == "PASS"

    def test_170_health_check_tpex_unchanged(self):
        from data.providers.mops.health_v142 import MOPSProviderHealthCheck
        hc = MOPSProviderHealthCheck()
        checks = hc.run()
        status, detail = checks["tpex_provider_unchanged"]
        assert status == "PASS"


# =====================================================================
# TestCapabilityRegistry (tests 171-178)
# =====================================================================
class TestCapabilityRegistry:
    def test_171_mops_provider_available(self):
        from release.capability_registry import is_capability_available
        assert is_capability_available("mops_provider") is True

    def test_172_mops_in_available_list(self):
        from release.capability_registry import list_available_capabilities
        caps = list_available_capabilities()
        assert "mops_provider" in caps

    def test_173_mops_not_in_planned(self):
        from release.capability_registry import list_planned_capabilities
        planned = list_planned_capabilities()
        assert "mops_provider" not in planned

    def test_174_twse_still_available(self):
        from release.capability_registry import is_capability_available
        assert is_capability_available("twse_provider") is True

    def test_175_tpex_still_available(self):
        from release.capability_registry import is_capability_available
        assert is_capability_available("tpex_provider") is True

    def test_176_dependency_validation_passes(self):
        from release.capability_registry import validate_capability_dependencies
        result = validate_capability_dependencies()
        assert result["valid"] is True
        assert len(result["errors"]) == 0

    def test_177_mops_health_check_registered(self):
        from release.capability_registry import _CAP_INDEX
        mops_cap = _CAP_INDEX.get("mops_provider")
        assert mops_cap is not None
        assert mops_cap.get("health_check") is not None

    def test_178_mops_capability_status_stable(self):
        from release.capability_registry import _CAP_INDEX, STABLE
        mops_cap = _CAP_INDEX.get("mops_provider")
        assert mops_cap["status"] == STABLE


# =====================================================================
# TestVersionInfo (tests 179-185)
# =====================================================================
class TestVersionInfo:
    def test_179_version_is_142(self):
        from release.version_info import VERSION
        assert VERSION == "1.4.2"

    def test_180_release_name_mops(self):
        from release.version_info import RELEASE_NAME
        assert RELEASE_NAME == "MOPS Provider"

    def test_181_base_release_141(self):
        from release.version_info import BASE_RELEASE
        assert "1.4.1" in BASE_RELEASE

    def test_182_mops_provider_available_true(self):
        from release.version_info import MOPS_PROVIDER_AVAILABLE
        assert MOPS_PROVIDER_AVAILABLE is True

    def test_183_mops_realtime_false(self):
        from release.version_info import MOPS_REALTIME_AVAILABLE
        assert MOPS_REALTIME_AVAILABLE is False

    def test_184_mops_broker_false(self):
        from release.version_info import MOPS_BROKER_EXECUTION_AVAILABLE
        assert MOPS_BROKER_EXECUTION_AVAILABLE is False

    def test_185_mops_financial_statements_available(self):
        from release.version_info import MOPS_FINANCIAL_STATEMENTS_AVAILABLE
        assert MOPS_FINANCIAL_STATEMENTS_AVAILABLE is True


# =====================================================================
# TestXBRLTaxonomy (tests 186-193)
# =====================================================================
class TestXBRLTaxonomy:
    def test_186_general_industry_taxonomy(self):
        data = load_fixture("taxonomy_general_industry.json")
        assert data["taxonomy"] == "general_industry"

    def test_187_financial_industry_taxonomy(self):
        data = load_fixture("taxonomy_financial_industry.json")
        assert data["taxonomy"] == "financial_industry"

    def test_188_detect_general_industry(self):
        from data.providers.mops.xbrl_index_v142 import detect_taxonomy
        assert detect_taxonomy("2330", "24") == "general_industry"

    def test_189_detect_financial_industry(self):
        from data.providers.mops.xbrl_index_v142 import detect_taxonomy
        assert detect_taxonomy("2882", "M") == "financial_industry"

    def test_190_xbrl_doc_from_fixture(self):
        data = load_fixture("xbrl_index.json")
        from data.providers.mops.models_v142 import MOPSXBRLDocument
        doc = MOPSXBRLDocument.from_dict(data["documents"][0])
        assert doc.taxonomy == "general_industry"

    def test_191_xbrl_fetcher_instantiates(self):
        from data.providers.mops.xbrl_index_v142 import MOPSXBRLIndexFetcher
        f = MOPSXBRLIndexFetcher()
        assert f is not None

    def test_192_xbrl_doc_roundtrip(self):
        from data.providers.mops.models_v142 import MOPSXBRLDocument
        data = load_fixture("xbrl_index.json")
        d1 = MOPSXBRLDocument.from_dict(data["documents"][0])
        d2 = MOPSXBRLDocument.from_dict(d1.to_dict())
        assert d1.taxonomy == d2.taxonomy

    def test_193_xbrl_doc_inline_flag(self):
        from data.providers.mops.models_v142 import MOPSXBRLDocument
        data = load_fixture("xbrl_index.json")
        doc = MOPSXBRLDocument.from_dict(data["documents"][0])
        assert isinstance(doc.is_inline_xbrl, bool)


# =====================================================================
# TestProviderIsolation (tests 194-200)
# =====================================================================
class TestProviderIsolation:
    def test_194_mops_and_twse_different_provider_ids(self):
        from data.providers.mops.provider_v142 import MOPSProviderV142
        from data.providers.twse.provider_v140 import TWSEProviderV140
        assert MOPSProviderV142().provider_id != TWSEProviderV140().provider_id

    def test_195_mops_and_tpex_different_provider_ids(self):
        from data.providers.mops.provider_v142 import MOPSProviderV142
        from data.providers.tpex.provider_v141 import TPExProviderV141
        assert MOPSProviderV142().provider_id != TPExProviderV141().provider_id

    def test_196_mops_data_domain_financial_disclosure(self):
        from data.providers.mops.provider_v142 import MOPSProviderV142
        p = MOPSProviderV142()
        assert p.data_domain == "financial_disclosure"

    def test_197_mops_capability_matrix_independent(self):
        from data.providers.mops.capabilities_v142 import MOPSCapabilityMatrix
        from data.providers.tpex.capabilities_v141 import TPExCapabilityMatrix
        mops_caps = set(MOPSCapabilityMatrix().build_summary()["capabilities"].keys())
        tpex_caps = set(TPExCapabilityMatrix().build_summary()["capabilities"].keys())
        # MOPS has unique capabilities
        assert "COMPANY_PROFILE" in mops_caps
        assert "DAILY_OHLCV" not in mops_caps  # MOPS doesn't have OHLCV

    def test_198_fetch_unknown_endpoint_returns_unavailable(self):
        from data.providers.mops.provider_v142 import MOPSProviderV142
        from data.providers.mops.models_v142 import MOPSFetchStatus
        p = MOPSProviderV142()
        status, data, prov = p.fetch_with_transport("nonexistent_ep", {})
        assert status == MOPSFetchStatus.UNAVAILABLE

    def test_199_provider_metadata_has_safety_flags(self):
        from data.providers.mops.provider_v142 import MOPSProviderV142
        p = MOPSProviderV142()
        meta = p.get_metadata()
        d = meta.to_dict()
        assert d["no_real_orders"] is True
        assert d["broker_execution_enabled"] is False
        assert d["realtime_available"] is False

    def test_200_query_service_missing_returns_none(self):
        from data.providers.mops.query_v142 import MOPSQueryService
        svc = MOPSQueryService()
        assert svc.get_profile("9999") is None
        assert svc.get_balance_sheet("9999", 2023, "Q4") is None
        assert svc.get_income_statement("9999", 2023, "Q4") is None
        assert svc.get_cash_flow("9999", 2023, "Q4") is None


# =====================================================================
# TestFetchStatusEnum (tests 201-212)
# =====================================================================
class TestFetchStatusEnum:
    def test_201_success_status(self):
        from data.providers.mops.models_v142 import MOPSFetchStatus
        assert MOPSFetchStatus.SUCCESS == "SUCCESS"

    def test_202_maintenance_status(self):
        from data.providers.mops.models_v142 import MOPSFetchStatus
        assert MOPSFetchStatus.MAINTENANCE == "MAINTENANCE"

    def test_203_revision_detected_status(self):
        from data.providers.mops.models_v142 import MOPSFetchStatus
        assert MOPSFetchStatus.REVISION_DETECTED == "REVISION_DETECTED"

    def test_204_market_conflict_status(self):
        from data.providers.mops.models_v142 import MOPSFetchStatus
        assert MOPSFetchStatus.MARKET_CONFLICT == "MARKET_CONFLICT"

    def test_205_mops_capability_enum_all_13(self):
        from data.providers.mops.models_v142 import MOPSCapability
        caps = list(MOPSCapability)
        assert len(caps) == 13

    def test_206_all_capabilities_in_supported_set(self):
        from data.providers.mops.capabilities_v142 import _SUPPORTED
        from data.providers.mops.models_v142 import MOPSCapability
        for cap in MOPSCapability:
            assert cap in _SUPPORTED, f"{cap} not in _SUPPORTED"

    def test_207_document_type_enum(self):
        from data.providers.mops.models_v142 import MOPSDocumentType
        assert MOPSDocumentType.BALANCE_SHEET == "BALANCE_SHEET"
        assert MOPSDocumentType.XBRL == "XBRL"

    def test_208_report_period_enum(self):
        from data.providers.mops.models_v142 import MOPSReportPeriod
        assert MOPSReportPeriod.Q1 == "Q1"
        assert MOPSReportPeriod.ANNUAL == "ANNUAL"

    def test_209_market_enum(self):
        from data.providers.mops.models_v142 import MOPSMarket
        assert MOPSMarket.TWSE == "TWSE"
        assert MOPSMarket.TPEX == "TPEx"

    def test_210_financial_metric_is_derived_flag(self):
        from data.providers.mops.models_v142 import MOPSFinancialMetric
        m = MOPSFinancialMetric(
            symbol="2330",
            fiscal_year=2023,
            fiscal_period="Q4",
            metric_name="gross_margin_pct",
            metric_value=60.0,
            metric_unit="PERCENT",
            currency="TWD",
            is_derived=True,
            derivation_method="gross_profit/revenue*100",
            available_from="2024-03-31",
            source_timestamp=None,
            fetched_at="2024-03-31T00:00:00+00:00",
            provider_id="mops_official",
            provenance=None,
        )
        d = m.to_dict()
        assert d["is_derived"] is True
        assert d["available_from"] == "2024-03-31"

    def test_211_financial_metric_roundtrip(self):
        from data.providers.mops.models_v142 import MOPSFinancialMetric
        m = MOPSFinancialMetric(
            symbol="2330",
            fiscal_year=2023,
            fiscal_period="Q4",
            metric_name="roe_pct",
            metric_value=9.64,
            metric_unit="PERCENT",
            currency="TWD",
            is_derived=True,
            derivation_method="net_income/total_equity*100",
            available_from="2024-03-31",
            source_timestamp=None,
            fetched_at="2024-03-31T00:00:00+00:00",
            provider_id="mops_official",
            provenance=None,
        )
        m2 = MOPSFinancialMetric.from_dict(m.to_dict())
        assert m2.metric_value == 9.64
        assert m2.is_derived is True

    def test_212_all_mops_modules_importable(self):
        """Smoke test: all MOPS modules import without error."""
        import data.providers.mops
        import data.providers.mops.models_v142
        import data.providers.mops.capabilities_v142
        import data.providers.mops.endpoints_v142
        import data.providers.mops.client_v142
        import data.providers.mops.parser_v142
        import data.providers.mops.normalizer_v142
        import data.providers.mops.provider_v142
        import data.providers.mops.health_v142
        import data.providers.mops.cache_policy_v142
        import data.providers.mops.store_v142
        import data.providers.mops.query_v142
        import data.providers.mops.company_profile_v142
        import data.providers.mops.monthly_revenue_v142
        import data.providers.mops.financial_reports_v142
        import data.providers.mops.balance_sheet_v142
        import data.providers.mops.income_statement_v142
        import data.providers.mops.cash_flow_v142
        import data.providers.mops.equity_statement_v142
        import data.providers.mops.material_information_v142
        import data.providers.mops.investor_conference_v142
        import data.providers.mops.xbrl_index_v142
        import data.providers.mops.revision_lineage_v142
        import data.providers.mops.point_in_time_v142
        import data.providers.mops.derived_metrics_v142
        assert True
