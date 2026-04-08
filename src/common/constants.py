OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
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
