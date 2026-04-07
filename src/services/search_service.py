from src.core.document_store import DocumentStore
from src.common.config import get_settings


class SearchService:
    def __init__(self, store: DocumentStore):
        self.store = store

    def handle(self, query: str):
        indices = self.store.index.search(query, get_settings().TOP_K)
        results = [self.store.chunks[i] for i in indices]
        return results
