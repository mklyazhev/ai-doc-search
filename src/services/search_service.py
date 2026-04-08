from src.core.document_store import DocumentStore
from src.common.config import get_settings


class SearchService:
    def __init__(self, store: DocumentStore):
        self.store = store

    def handle(self, query: str):
        results = self.store.index.search(
            query,
            get_settings().TOP_K
        )

        return [
            {
                "title": self.store.chunks[r["index"]]["title"],
                "chunk": r["text"],
                "score": r["score"]
            }
            for r in results
        ]
