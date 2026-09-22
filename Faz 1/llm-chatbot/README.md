# LLM Chatbot (Faz 1)

Gemini API'sinin temellerini (streaming, system instruction ile persona yönlendirme, çok-turlu konuşma hafızası) uygulamalı öğrenmek için yazılmış, terminal üzerinden çalışan bir sohbet botu. BCI/nörobilim terimlerini önce teknik doğrulukla tanımlayıp sonra günlük hayattan bir benzetmeyle sadeleştiren bir persona (`BCI_SYSTEM_PROMPT`) kullanıyor.

## Kurulum

```bash
uv sync
```

`.env` dosyası oluştur:

```
GEMINI_API_KEY=...
```

## Kullanım

```bash
uv run main.py
```

Çıkmak için `exit` yaz. `MEMORY_ENABLED` sabiti (main.py) konuşma geçmişinin turlar arasında hatırlanıp hatırlanmayacağını kontrol eder.

## Test

```bash
uv run pytest -v
```

Gerçek bir API çağrısı yapmadan, yalnızca mesaj geçmişine ekleme mantığını (`append_user_message`) test eder — "LLM çıktısını değil kendi mantığını test et" prensibi.

## İlgili projeler

Bu, aynı roadmap'in ilerideki fazlarının temelini oluşturuyor: [rag-literature-assistant](https://github.com/BayramGurbuz/rag-literature-assistant) (Faz 2 — RAG) ve [mcp-literatur-server](https://github.com/BayramGurbuz/mcp-literatur-server) (Faz 3 — MCP agent), ikisi de production'a alınıp Render'a deploy edildi.
