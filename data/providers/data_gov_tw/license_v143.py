"""
data/providers/data_gov_tw/license_v143.py — License validation for data.gov.tw v1.4.3.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] License unknown → formal_use_allowed=False.
[!] License change → revision created.
[!] This is NOT legal advice. Users must comply with each dataset's license.
[!] Not all data.gov.tw data is unconditionally usable.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

# Known approved license identifiers (case-insensitive matching)
_APPROVED_LICENSE_IDENTIFIERS = [
    "政府資料開放授權條款",
    "government data open license",
    "open government data license",
    "creative commons",
    "cc by",
    "cc0",
    "public domain",
    "odbl",
]

_RESTRICTED_KEYWORDS = [
    "非商業",
    "non-commercial",
    "nc",
    "禁止",
    "restricted",
    "all rights reserved",
    "授權期限",
    "計費",
]

_BLOCKED_KEYWORDS = [
    "不得再利用",
    "prohibition",
    "prohibited",
    "not for redistribution",
]


def _lower(s: Optional[str]) -> str:
    return (s or "").lower().strip()


class DataGovTwLicenseValidator:
    """
    Validates license metadata for data.gov.tw datasets.

    Rules:
    - Known open government license → APPROVED
    - Unknown license → REVIEW_REQUIRED, formal_use_allowed=False
    - Restricted (NC or similar) → RESTRICTED, formal_use_allowed=False
    - Prohibited → BLOCKED, formal_use_allowed=False
    - Blank/missing → UNKNOWN, formal_use_allowed=False
    - This is NOT a legal opinion — users must verify compliance.
    """

    def validate(
        self,
        license_name: Optional[str],
        license_url: Optional[str] = None,
        pricing_policy: Optional[str] = None,
    ) -> Dict[str, Any]:
        name_lower = _lower(license_name)
        url_lower = _lower(license_url)
        price_lower = _lower(pricing_policy)

        warnings: List[str] = []
        restrictions: List[str] = []

        # No license info at all
        if not license_name and not license_url:
            return {
                "license_name": license_name,
                "license_url": license_url,
                "license_status": "UNKNOWN",
                "commercial_use_allowed": None,
                "attribution_required": None,
                "redistribution_allowed": None,
                "modification_allowed": None,
                "restrictions": ["License information missing"],
                "review_required": True,
                "formal_use_allowed": False,
                "reasons": ["License information missing — cannot determine usage rights"],
                "legal_disclaimer": "This is not legal advice. Verify license compliance independently.",
            }

        # Check for blocked keywords
        combined = name_lower + " " + url_lower
        for kw in _BLOCKED_KEYWORDS:
            if kw in combined:
                return {
                    "license_name": license_name,
                    "license_url": license_url,
                    "license_status": "BLOCKED",
                    "commercial_use_allowed": False,
                    "attribution_required": True,
                    "redistribution_allowed": False,
                    "modification_allowed": False,
                    "restrictions": [f"Blocked keyword detected: {kw}"],
                    "review_required": True,
                    "formal_use_allowed": False,
                    "reasons": [f"License contains prohibited terms: {kw}"],
                    "legal_disclaimer": "This is not legal advice.",
                }

        # Check for restricted keywords
        for kw in _RESTRICTED_KEYWORDS:
            if kw in combined:
                restrictions.append(f"Restriction keyword: {kw}")
                warnings.append(f"License may restrict usage: {kw}")

        # Check for pricing
        if pricing_policy and _lower(pricing_policy) not in ("", "free", "免費", "open"):
            restrictions.append(f"Pricing policy: {pricing_policy}")
            warnings.append("Dataset may have fees")

        if restrictions:
            return {
                "license_name": license_name,
                "license_url": license_url,
                "license_status": "RESTRICTED",
                "commercial_use_allowed": False,
                "attribution_required": True,
                "redistribution_allowed": False,
                "modification_allowed": False,
                "restrictions": restrictions,
                "review_required": True,
                "formal_use_allowed": False,
                "reasons": warnings,
                "legal_disclaimer": "This is not legal advice. Verify license compliance independently.",
            }

        # Check for known approved licenses
        for approved_id in _APPROVED_LICENSE_IDENTIFIERS:
            if approved_id in name_lower or approved_id in url_lower:
                return {
                    "license_name": license_name,
                    "license_url": license_url,
                    "license_status": "APPROVED",
                    "commercial_use_allowed": True,
                    "attribution_required": "cc by" in combined or "attribution" in combined,
                    "redistribution_allowed": True,
                    "modification_allowed": True,
                    "restrictions": [],
                    "review_required": False,
                    "formal_use_allowed": True,
                    "reasons": [f"Matched known open license: {approved_id}"],
                    "legal_disclaimer": "This is not legal advice. Verify license compliance independently.",
                }

        # Default: unknown license — review required
        return {
            "license_name": license_name,
            "license_url": license_url,
            "license_status": "REVIEW_REQUIRED",
            "commercial_use_allowed": None,
            "attribution_required": None,
            "redistribution_allowed": None,
            "modification_allowed": None,
            "restrictions": ["License not recognized — manual review required"],
            "review_required": True,
            "formal_use_allowed": False,
            "reasons": ["License not in known approved list"],
            "legal_disclaimer": "This is not legal advice. Verify license compliance independently.",
        }
