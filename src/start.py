import logging

from src.common.config import get_settings
from src.core.document_store import DocumentStore
from src.services.search_service import SearchService
from src.services.ai_service import AIService
from src.services.bot_service import TelegramBot

logger = logging.getLogger(__name__)


def main():
    logger.info("Starting AI Document Search Assistant...")
    
    settings = get_settings()
    logger.info("Configuration loaded:")
    logger.info(f"  - Data path: {settings.DATA_PATH}")
    logger.info(f"  - Chunk size: {settings.CHUNK_SIZE}")
    logger.info(f"  - Chunk overlap: {settings.CHUNK_OVERLAP}")
    logger.info(f"  - Top K results: {settings.TOP_K}")
    
    logger.info("Initializing document store...")
    document_store = DocumentStore()
    document_store.load_documents(settings.DATA_PATH)
    
    logger.info("Building vector index...")
    document_store.build_chunks()
    
    logger.info("Initializing services...")
    search_service = SearchService(document_store)
    ai_service = AIService(search_service)
    
    logger.info("Starting Telegram bot...")
    bot = TelegramBot(ai_service)
    bot.run()


if __name__ == "__main__":
    main()