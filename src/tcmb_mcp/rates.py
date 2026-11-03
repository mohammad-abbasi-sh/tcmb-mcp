"""Domain logic: parse TCMB indicative-rates XML into compact dicts (stdlib only)."""
from __future__ import annotations

import xml.etree.ElementTree as ET


def _f(text: str | None) -> float | None:
    if text is None or not text.strip():
        return None
    try:
        return float(text.strip())
    except ValueError:
        return None


def parse_rates(xml_text: str) -> dict:
    """Parse a TCMB kurlar XML document.

    Returns {"date": "03.11.2026", "bulletin": "2026/206", "rates": [...]}.
    Each rate: {"code","name","unit","forex_buying","forex_selling",
                "banknote_buying","banknote_selling"}.
    """
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as e:
        raise ValueError(f"invalid TCMB XML: {e}") from e
    if root.tag != "Tarih_Date":
        raise ValueError(f"unexpected TCMB root element: {root.tag!r}")

    rates = []
    for cur in root.findall("Currency"):
        code = cur.get("Kod") or cur.get("CurrencyCode") or ""
        name_el = cur.find("CurrencyName")
        unit_el = cur.find("Unit")
        rates.append(
            {
                "code": code,
                "name": (name_el.text or "").strip() if name_el is not None else "",
                "unit": int((unit_el.text or "1").strip()) if unit_el is not None else 1,
                "forex_buying": _f(cur.findtext("ForexBuying")),
                "forex_selling": _f(cur.findtext("ForexSelling")),
                "banknote_buying": _f(cur.findtext("BanknoteBuying")),
                "banknote_selling": _f(cur.findtext("BanknoteSelling")),
            }
        )
    return {
        "date": root.get("Tarih", ""),
        "bulletin": root.get("Bulten_No", ""),
        "rates": rates,
    }


def find_rate(parsed: dict, code: str) -> dict | None:
    """Find one currency by code (case-insensitive)."""
    want = code.strip().upper()
    for r in parsed["rates"]:
        if r["code"].upper() == want:
            return r
    return None


def list_currencies(parsed: dict) -> list[dict]:
    return [{"code": r["code"], "name": r["name"]} for r in parsed["rates"]]
