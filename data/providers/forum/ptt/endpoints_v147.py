"""
data/providers/forum/ptt/endpoints_v147.py — PTT URL constants v1.4.7.
[!] Research Only. No Real Orders. Public URLs only. No credentials.
"""

BOARD = "Stock"
BOARD_INDEX = "https://www.ptt.cc/bbs/Stock/index.html"
BOARD_INDEX_PAGINATED = "https://www.ptt.cc/bbs/Stock/index{page}.html"
ARTICLE_URL_PATTERN = "https://www.ptt.cc/bbs/Stock/{article_id}.html"
MOBILE_BASE_URL = "https://www.ptt.cc/bbs/Stock/"
BEPTT_BASE_URL = "https://www.beptt.cc/b/Stock/"
MEOWPTT_BASE_URL = "https://meowptt.com/bbs/Stock/"

# Rate limit defaults (requests per second)
DEFAULT_RATE_LIMIT_SEC = 2.0
DEFAULT_TIMEOUT_SEC = 10
DEFAULT_MAX_RETRIES = 3
DEFAULT_MAX_PAGES = 10

# Adult content cookie (only for pages that normally require it, public boards)
ADULT_COOKIE_NAME = "over18"
ADULT_COOKIE_VALUE = "1"
ADULT_COOKIE_DOMAIN = ".ptt.cc"

# Encoding detection order
ENCODING_CANDIDATES = ("utf-8", "big5", "cp950")

NO_REAL_ORDERS = True
CREDENTIAL_STORAGE_ENABLED = False
LOGIN_BYPASS_ENABLED = False
PROXY_ROTATION_ENABLED = False
