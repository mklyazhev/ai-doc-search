import requests
from typing import List, Dict

from src.common.config import get_settings
from src.common.constants import YANDEX_GPT_URL, PROMPT_TEMPLATE


def build_context(chunks):
    return "\n\n".join(
        [f"{c['title']}:\n{c['chunk']}" for c in chunks]
    )


class YandexGPTClient:
    def generate_answer(self, query: str, context: List[Dict]) -> str:
        context_text = build_context(context)

        prompt = PROMPT_TEMPLATE.format(
            query=query,
            context=context_text
        )

        headers = {
            "Authorization": f"Api-Key {get_settings().YANDEX_API_KEY}"
        }

        payload = {
            "modelUri": f"gpt://{get_settings().YANDEX_FOLDER_ID}/yandexgpt-lite",
            "completionOptions": {
                "temperature": 0.3,
                "maxTokens": 500
            },
            "messages": [
                {"role": "user", "text": prompt}
            ]
        }

        response = requests.post(YANDEX_GPT_URL, headers=headers, json=payload)

        if response.status_code != 200:
            return f"LLM error: {response.text}"

        data = response.json()

        try:
            return data["result"]["alternatives"][0]["message"]["text"]
        except Exception:
            return "Ошибка обработки ответа LLM"
