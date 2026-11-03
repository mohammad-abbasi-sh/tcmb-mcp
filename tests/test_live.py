"""Live tests — hit the real tcmb.gov.tr. Cautious: 2 requests, then stop.

Run:  pytest tests/test_live.py -v
Skip: pytest -m "not live"  (or set TCMB_SKIP_LIVE=1)
"""
import json
import os
import pathlib
import sys
import time
import unittest

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))

from tcmb_mcp import http as _http
from tcmb_mcp import rates as _rates

pytestmark = pytest.mark.live
SKIP = os.environ.get("TCMB_SKIP_LIVE") == "1"


@pytest.mark.skipif(SKIP, reason="TCMB_SKIP_LIVE=1")
class TestLive(unittest.TestCase):
    def test_today_xml_is_real(self):
        xml = _http.fetch_today_xml()
        d = _rates.parse_rates(xml)
        self.assertTrue(d["date"], "bulletin date should not be empty")
        self.assertGreaterEqual(len(d["rates"]), 15)
        usd = _rates.find_rate(d, "USD")
        self.assertIsNotNone(usd)
        # sanity: USD/TRY should be a plausible positive number
        self.assertGreater(usd["forex_selling"], 1.0)
        print(f"\nLIVE USD/TRY today ({d['date']}): "
              f"buy={usd['forex_buying']} sell={usd['forex_selling']}")
        time.sleep(2)  # be polite

    def test_historical_date(self):
        # 2026-11-02 was a Monday -> bulletin exists
        d = _rates.parse_rates(_http.fetch_date_xml("2026-11-02"))
        self.assertEqual(d["date"], "02.11.2026")
        self.assertGreaterEqual(len(d["rates"]), 15)

    def test_weekend_has_no_bulletin(self):
        # 2026-11-01 was a Sunday -> expect TcmbError
        with self.assertRaises(_http.TcmbError):
            _http.fetch_date_xml("2026-11-01")

    def test_bad_date_format(self):
        with self.assertRaises(_http.TcmbError):
            _http.fetch_date_xml("02/11/2026")
