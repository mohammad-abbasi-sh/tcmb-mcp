"""HTTP layer for tcmb_mcp — plain httpx, no tricks needed (official public feed)."""
from __future__ import annotations

import os

import httpx

BASE = "https://www.tcmb.gov.tr/kurlar"
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)
TIMEOUT = 20.0


class TcmbError(RuntimeError):
    pass


def _client() -> httpx.Client:
    # NOTE: we read the proxy URL from the environment but never log it.
    # trust_env=False because httpx fails to parse bracketed IPv6 entries
    # (e.g. [::1]) that some environments put in no_proxy.
    proxy = os.environ.get("https_proxy") or os.environ.get("HTTPS_PROXY")
    return httpx.Client(
        headers={"User-Agent": UA},
        timeout=TIMEOUT,
        proxy=proxy or None,
        trust_env=False,
    )


def fetch_today_xml() -> str:
    """Fetch today's indicative exchange rates XML."""
    return _get(f"{BASE}/today.xml")


def fetch_date_xml(date: str) -> str:
    """Fetch historical rates for a date.

    date: YYYY-MM-DD. TCMB archive layout is /kurlar/YYYYMM/DDMMYYYY.xml.
    Raises TcmbError on HTTP errors (e.g. weekends/holidays have no bulletin).
    """
    import re

    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", date.strip())
    if not m:
        raise TcmbError(f"bad date format (expected YYYY-MM-DD): {date!r}")
    y, mo, d = m.groups()
    return _get(f"{BASE}/{y}{mo}/{d}{mo}{y}.xml")


def _get(url: str) -> str:
    try:
        with _client() as c:
            r = c.get(url)
    except httpx.HTTPError as e:
        raise TcmbError(f"network error fetching {url}: {e}") from e
    if r.status_code == 404:
        raise TcmbError(
            "no bulletin for that date (TCMB publishes on business days only)"
        )
    if r.status_code != 200:
        raise TcmbError(f"TCMB returned HTTP {r.status_code} for {url}")
    r.encoding = "utf-8"
    return r.text
