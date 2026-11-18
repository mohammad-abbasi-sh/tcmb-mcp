# tcmb-mcp 🇹🇷

mcp-name: io.github.mohammad-abbasi-sh/tcmb-mcp

Unofficial **read-only** MCP server for the **Central Bank of the Republic of Türkiye (TCMB)** indicative exchange rates — live TRY rates for 22 currencies, plus history.

> Pilot of the "Turkey MCP factory" (Sepehr-style pipeline). Not affiliated with TCMB.

## For AI agents

Add to your MCP client config (stdio):

```json
{
  "mcpServers": {
    "tcmb": {
      "command": "uvx",
      "args": ["tcmb-mcp==0.1.2"]
    }
  }
}
```

Or run locally: `python -m tcmb_mcp.server` (needs `mcp<2`, `httpx`).

## Tools

| Tool | Description |
|------|-------------|
| `tcmb_get_rates` | Today's indicative rates for all 22 currencies (TRY) |
| `tcmb_get_rate` | One currency today — `code`: USD, EUR, GBP… (case-insensitive) |
| `tcmb_list_currencies` | All currency codes + names in today's bulletin |
| `tcmb_get_rates_on` | Historical rates — `date`: YYYY-MM-DD (business days only) |

Example output (`tcmb_get_rate` / USD):

```json
{"date": "03.11.2026", "code": "USD", "name": "US DOLLAR", "unit": 1,
 "forex_buying": 49.9094, "forex_selling": 49.9993,
 "banknote_buying": 49.8744, "banknote_selling": 50.0743}
```

Notes:
- Rates are Turkish Lira per `<unit>` of foreign currency.
- Forex = interbank; banknote = physical cash.
- TCMB publishes no bulletin on weekends/holidays (`tcmb_get_rates_on` returns an error then).
- Data: TCMB public feed `tcmb.gov.tr/kurlar` — no key, no login, read-only.

## Development

```bash
python3 -m venv .venv && .venv/bin/pip install "mcp<2" httpx pytest
.venv/bin/python -m pytest tests/ -q
```

- `tests/test_rates.py` — offline, parses a real captured bulletin fixture
- `tests/test_live.py` — 2 cautious live requests against tcmb.gov.tr

## Cite this project

If you use tcmb-mcp, build on it, or write about it, please credit the source:

> Abbasi, Mohammad. *tcmb-mcp*. v0.1.2, 2026. https://github.com/mohammad-abbasi-sh/tcmb-mcp

A ready-to-copy citation is also available from GitHub's **Cite this repository** button (see `CITATION.cff`). Commercial use needs a separate license (see below).

## License

[PolyForm Noncommercial 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0/) — free for personal and non-commercial use; commercial use needs a separate license (see LICENSE).

---

Built by [Mohammad Abbasi](https://github.com/mohammad-abbasi-sh) — [Almanibama](https://almanibama.ir) · [mabbasi.ir](https://mabbasi.ir)
