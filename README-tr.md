# tcmb-mcp 🇹🇷

**Türkiye Cumhuriyet Merkez Bankası (TCMB)** gösterge döviz kurları için gayriresmî, **salt-okunur** MCP sunucusu — 22 para birimi için canlı TRY kurları ve tarihçe.

> "Türkiye MCP fabrikası" pilotu (Sepehr tarzı pipeline). TCMB ile bağlantısı yoktur.

## Yapay zekâ ajanları için

MCP istemcinize ekleyin (stdio):

```json
{
  "mcpServers": {
    "tcmb": {
      "command": "uvx",
      "args": ["tcmb-mcp==0.1.1"]
    }
  }
}
```

## Araçlar

| Araç | Açıklama |
|------|----------|
| `tcmb_get_rates` | 22 para birimi için bugünkü gösterge kurları (TRY) |
| `tcmb_get_rate` | Tek para birimi — `code`: USD, EUR, GBP… (büyük/küçük harf duyarsız) |
| `tcmb_list_currencies` | Bugünkü bültendeki tüm para birimi kodları + adları |
| `tcmb_get_rates_on` | Tarihçeli kurlar — `date`: YYYY-MM-DD (yalnızca iş günleri) |

## Kurallar

Gayriresmî ve salt-okunur — giriş yok, API anahtarı yok, yazma yok. Testler: çevrimdışı fixture + canlı testler (14/14 yeşil).
