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

        self.session = requests.Session()
        self.session.proxies = {
            "http": "http://127.0.0.1:10809",
            "https": "http://127.0.0.1:10809",
        }

        self.session.trust_env = False

    def get_updates(self):
        url = build_url("getUpdates")

        params = {
            "offset": self.offset,
            "timeout": 25
        }

        try:
            response = self.session.get(
                url,
                params=params,
                timeout=(10, 60)
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"get_updates error: {e}")
            return {}

    def send_message(self, chat_id, text):
        url = build_url("sendMessage")

        try:
            self.session.post(
                url,
                json={"chat_id": chat_id, "text": text},
                timeout=(5, 10)
            )
        except requests.exceptions.RequestException as e:
            logger.error(f"send_message error: {e}")

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

                try:
                    answer = self.ai_service.process_query(text)
                except Exception as e:
                    logger.error(f"AI error: {e}")
                    answer = "Ошибка обработки запроса"

                self.send_message(chat_id, answer)

            time.sleep(0.3)
