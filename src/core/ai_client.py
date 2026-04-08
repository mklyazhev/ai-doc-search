import requests
from typing import List, Dict

from src.common.config import get_settings
from src.common.constants import OPENROUTER_URL, PROMPT_TEMPLATE


def build_context(chunks):
    return "\n\n".join(
        [f"{c['title']}:\n{c['chunk']}" for c in chunks]
    )


class OpenRouterClient:
    def generate_answer(self, query: str, context: List[Dict]) -> str:
        context_text = build_context(context)

        prompt = PROMPT_TEMPLATE.format(
            query=query,
            context=context_text
        )

        headers = {
            "Authorization": f"Bearer {get_settings().OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",  # можно поменять
            "X-Title": "doc-search-bot"          # опционально
        }

        payload = {
            "model": f"{get_settings().MODEL_NAME}",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 500
        }

        response = requests.post(OPENROUTER_URL, headers=headers, json=payload)

        if response.status_code != 200:
            return f"LLM error: {response.text}"

        data = response.json()

        try:
            return data["choices"][0]["message"]["content"]
        except Exception:
            return "Ошибка обработки ответа LLM"
