import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def get_env(key: str, default=None) -> str:
    value = os.getenv(key)

    if not value:
        if not default:
            raise ValueError("Environment variable {%s} is not set", key)
        else:
            return default

    return value


class Settings:
    BOT_TOKEN = get_env("BOT_TOKEN")

    OPENROUTER_API_KEY = get_env("OPENROUTER_API_KEY")
    MODEL_NAME = get_env("MODEL_NAME")

    DATA_PATH = get_env("DATA_PATH")

    TOP_K = get_env("TOP_K", 5)
    CHUNK_SIZE = get_env("CHUNK_SIZE", 300)
    CHUNK_OVERLAP = get_env("CHUNK_OVERLAP", 50)


_settings = Settings()


def get_settings():
    return _settings
