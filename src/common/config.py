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
    LLM_MODEL_NAME = get_env("LLM_MODEL_NAME")

    EMBEDDING_MODEL_NAME = get_env("EMBEDDING_MODEL_NAME")

    DATA_PATH = get_env("DATA_PATH")

    USE_PROXY = get_env("USE_PROXY", "false").lower() == "true"
    PROXY_URL = get_env("PROXY_URL", "")

    TOP_K = get_env("TOP_K", 5)
    CHUNK_SIZE = get_env("CHUNK_SIZE", 800)
    CHUNK_OVERLAP = get_env("CHUNK_OVERLAP", 150)


_settings = Settings()


def get_settings():
    return _settings
