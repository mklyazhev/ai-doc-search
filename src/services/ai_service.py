from src.services.search_service import SearchService
from src.core.ai_client import YandexGPTClient


class AIService:
    def __init__(self, search_service: SearchService):
        self.search_service = search_service
        self.llm = YandexGPTClient()

    def process_query(self, query: str) -> str:
        top_chunks = self.search_service.handle(query)
        return self.llm.generate_answer(query, top_chunks)
