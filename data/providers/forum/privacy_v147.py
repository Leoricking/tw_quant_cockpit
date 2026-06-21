"""
data/providers/forum/privacy_v147.py — Forum Privacy Service v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] NEVER outputs full IP. NEVER infers real identity. NEVER sensitive attribute inference.
[!] IP redaction required for all PTT footer content.
"""
from __future__ import annotations

import hashlib
import re
from typing import Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
FULL_IP_OUTPUT_ENABLED = False
IDENTITY_INFERENCE_ENABLED = False
SENSITIVE_ATTRIBUTE_INFERENCE_ENABLED = False

# PTT footer IP pattern (IPv4)
_IP_PATTERN = re.compile(
    r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
)
# PTT footer country hint pattern (e.g. "來自: 123.45.67.89")
_PTT_FROM_PATTERN = re.compile(
    r"來自[:：]\s*(\S+)"
)
# Credential patterns: 密碼/password field values
_CREDENTIAL_PATTERN = re.compile(
    r"(?:密碼|password|passwd|pwd)[:：\s]+\S+",
    re.IGNORECASE,
)


class ForumPrivacyService:
    """
    Privacy service for forum data.
    [!] NEVER outputs full IP.
    [!] NEVER infers real identity from handle.
    [!] hash_author_id is one-way: cannot recover original.
    """

    def redact_ip(self, text: str) -> str:
        """Remove or hash IPs found in PTT footer. Returns redacted text."""
        if not text:
            return text
        return _IP_PATTERN.sub("[IP_REDACTED]", text)

    def hash_author_id(self, raw_id: str, salt: str) -> str:
        """
        One-way salted hash for internal analysis.
        NEVER used to re-identify real person.
        """
        if not raw_id:
            return ""
        combined = f"{salt}:{raw_id}".encode("utf-8")
        return hashlib.sha256(combined).hexdigest()[:16]

    def is_ip_present(self, text: str) -> bool:
        """Returns True if text contains an IPv4 address."""
        if not text:
            return False
        return bool(_IP_PATTERN.search(text))

    def get_country_hint(self, text: str) -> Optional[str]:
        """
        Extract country hint ONLY if PTT page explicitly shows it.
        Returns None if IP found (we don't expose it).
        Returns None by default — only safe non-IP country labels.
        [!] NEVER returns full IP.
        """
        if not text:
            return None
        # PTT does not typically show country in text — return None safely
        # If PTT ever shows a non-IP country label, it would appear here.
        # We return None to be conservative.
        return None

    def make_display_partial(self, raw_id: str) -> str:
        """Create a safe display partial like 'A****' from raw PTT ID."""
        if not raw_id:
            return ""
        if len(raw_id) <= 1:
            return raw_id[0] + "****"
        return raw_id[0] + "*" * min(4, len(raw_id) - 1)

    def hash_display_id(self, raw_id: str, salt: str = "forum_display") -> str:
        """
        Deterministic non-reversible display ID for internal tracking.
        NEVER used to re-identify real person.
        """
        return self.hash_author_id(raw_id, salt)

    def redact_text(self, text: str) -> str:
        """
        Redact IPs and other sensitive patterns from arbitrary text.
        [!] NEVER outputs full IP or credentials.
        """
        if not text:
            return text
        # Redact IPv4 addresses
        redacted = _IP_PATTERN.sub("[IP_REDACTED]", text)
        # Redact credential field values
        redacted = _CREDENTIAL_PATTERN.sub("[CREDENTIAL_REDACTED]", redacted)
        return redacted

    def process_article_footer(self, footer_text: str) -> dict:
        """
        Process a PTT article footer, redacting IP addresses.
        Returns dict with redacted_text and metadata.
        [!] NEVER returns full IP in redacted_text.
        """
        if not footer_text:
            return {"redacted_text": "", "had_ip": False}
        had_ip = self.is_ip_present(footer_text)
        redacted = self.redact_text(footer_text)
        return {
            "redacted_text": redacted,
            "had_ip": had_ip,
            "full_ip_in_output": False,
        }


# Alias for compatibility: ForumPrivacyRedactor = ForumPrivacyService
ForumPrivacyRedactor = ForumPrivacyService
