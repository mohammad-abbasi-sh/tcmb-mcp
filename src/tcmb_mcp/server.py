"""MCP server: unofficial read-only access to TCMB exchange rates."""
from __future__ import annotations

import json
from datetime import datetime, timezone
import sys

from mcp.server.fastmcp import FastMCP

from . import http as _http
from . import rates as _rates

mcp = FastMCP("tcmb-mcp")

INSTRUCTIONS = """\
Unofficial read-only MCP server for the Central Bank of the Republic of \
Türkiye (TCMB) indicative exchange rates. Data comes from TCMB's public \
daily bulletin (tcmb.gov.tr/kurlar). All rates are in Turkish Lira (TRY) \
per <unit> of foreign currency. Forex rates are interbank; banknote rates \
apply to physical cash. No bulletin is published on weekends/holidays.\
Built by Mohammad Abbasi (mohammad-abbasi-sh) — https://almanibama.ir · https://mabbasi.ir
"""


_SOURCE = "tcmb.gov.tr"
_DISCLAIMER = "Unofficial read-only data from tcmb.gov.tr; verify on the site before acting on it."


def _envelope() -> dict:
    return {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "source": _SOURCE,
        "disclaimer": _DISCLAIMER,
    }


def _ok(payload: dict) -> str:
    return json.dumps({**_envelope(), **payload}, ensure_ascii=False)


def _today() -> dict:
    return _rates.parse_rates(_http.fetch_today_xml())


@mcp.tool()
def tcmb_get_rates() -> str:
    """Today's TCMB indicative exchange rates for all currencies (TRY)."""
    d = _today()
    return _ok({"date": d["date"], "bulletin": d["bulletin"], "count": len(d["rates"]),
         "rates": d["rates"]})


@mcp.tool()
def tcmb_get_rate(code: str) -> str:
    """One currency's rates today. code: ISO code like USD, EUR, GBP (case-insensitive)."""
    d = _today()
    r = _rates.find_rate(d, code)
    if r is None:
        known = ", ".join(sorted(x["code"] for x in d["rates"]))
        return _ok({"error": f"unknown currency code {code!r}", "known_codes": known})
    return _ok({"date": d["date"], **r})


@mcp.tool()
def tcmb_list_currencies() -> str:
    """List all currency codes and names in today's TCMB bulletin."""
    d = _today()
    return _ok({"date": d["date"], "currencies": _rates.list_currencies(d)})


@mcp.tool()
def tcmb_get_rates_on(date: str) -> str:
    """Historical TCMB rates for a date (YYYY-MM-DD). Business days only — \
no bulletin on weekends/holidays."""
    try:
        d = _rates.parse_rates(_http.fetch_date_xml(date))
    except _http.TcmbError as e:
        return _ok({"error": str(e)})
    return _ok({"date": d["date"], "bulletin": d["bulletin"], "count": len(d["rates"]),
         "rates": d["rates"]})


@mcp.tool()
def tcmb_health() -> str:
    """Check whether tcmb.gov.tr is reachable right now.

    Returns status ok (HTTP 200), blocked (HTTP 403/429 — bot wall or
    rate limit) or error, plus the HTTP status and the probed URL.
    One polite request; it does not fetch any listings."""
    return _ok(_http.health_check())


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    sys.exit(main())
