import logging
import requests
import time

from src.common.config import get_settings
from src.common.constants import TELEGRAM_API_BASE

logger = logging.getLogger(__name__)


def build_url(method: str) -> str:
    return TELEGRAM_API_BASE.format(
        token=get_settings().BOT_TOKEN,
        method=method
    )


class TelegramBot:
    def __init__(self, ai_service):
        self.ai_service = ai_service
        self.offset = 0

    def get_updates(self):
        url = build_url("getUpdates")
        params = {"offset": self.offset, "timeout": 30}

        response = requests.get(url, params=params)
        return response.json()

    def send_message(self, chat_id, text):
        url = build_url("sendMessage")
        data = {"chat_id": chat_id, "text": text}
        requests.post(url, json=data)

    def run(self):
        logger.info("Bot started...")

        while True:
            updates = self.get_updates()

            for update in updates.get("result", []):
                self.offset = update["update_id"] + 1

                message = update.get("message")
                if not message:
                    continue

                chat_id = message["chat"]["id"]
                text = message.get("text", "")

                if not text:
                    continue

                answer = self.ai_service.process_query(text)
                self.send_message(chat_id, answer)

            time.sleep(1)