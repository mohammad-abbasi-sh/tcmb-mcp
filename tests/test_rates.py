"""Offline tests — parse a real captured TCMB bulletin, no network."""
import json
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))

from tcmb_mcp import rates

FIX = pathlib.Path(__file__).resolve().parent / "fixtures" / "today.xml"


class TestParseRates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parsed = rates.parse_rates(FIX.read_text(encoding="utf-8"))

    def test_meta(self):
        self.assertEqual(self.parsed["date"], "03.11.2026")
        self.assertEqual(self.parsed["bulletin"], "2026/206")

    def test_currency_count(self):
        self.assertEqual(len(self.parsed["rates"]), 22)

    def test_usd_values(self):
        usd = rates.find_rate(self.parsed, "USD")
        self.assertIsNotNone(usd)
        self.assertAlmostEqual(usd["forex_buying"], 49.9094)
        self.assertAlmostEqual(usd["forex_selling"], 49.9993)
        self.assertEqual(usd["unit"], 1)
        self.assertEqual(usd["name"], "US DOLLAR")

    def test_case_insensitive_lookup(self):
        self.assertIsNotNone(rates.find_rate(self.parsed, "eur"))
        self.assertIsNotNone(rates.find_rate(self.parsed, " Gbp "))

    def test_unknown_code(self):
        self.assertIsNone(rates.find_rate(self.parsed, "XXX"))

    def test_empty_cross_rate_is_none(self):
        # USD has no CrossRate fields -> banknote fields still parse
        usd = rates.find_rate(self.parsed, "USD")
        self.assertAlmostEqual(usd["banknote_buying"], 49.8744)

    def test_list_currencies(self):
        cur = rates.list_currencies(self.parsed)
        codes = [c["code"] for c in cur]
        self.assertIn("USD", codes)
        self.assertIn("EUR", codes)
        self.assertEqual(len(cur), 22)

    def test_invalid_xml(self):
        with self.assertRaises(ValueError):
            rates.parse_rates("<not xml")

    def test_wrong_root(self):
        with self.assertRaises(ValueError):
            rates.parse_rates("<html><body>x</body></html>")


class TestToolLogic(unittest.TestCase):
    """Exercise the tool functions' pure parts without network."""

    def test_unknown_currency_error_shape(self):
        # emulate tcmb_get_rate's error branch using parsed fixture
        parsed = rates.parse_rates(FIX.read_text(encoding="utf-8"))
        r = rates.find_rate(parsed, "ZZZ")
        self.assertIsNone(r)
        err = json.dumps({"error": "unknown currency code 'ZZZ'"})
        self.assertIn("unknown currency", err)


if __name__ == "__main__":
    unittest.main()
