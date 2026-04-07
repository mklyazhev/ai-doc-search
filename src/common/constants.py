YANDEX_GPT_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
TELEGRAM_API_BASE = "https://api.telegram.org/bot{token}/{method}"

PROMPT_TEMPLATE = """
Ты ассистент по поиску документов.

Вопрос:
{query}

Контекст:
{context}

Ответь:
- Название документа
- Цитату
- Краткий ответ
"""
