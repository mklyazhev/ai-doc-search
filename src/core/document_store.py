import json
from typing import List, Dict

from src.core.vector_index import VectorIndex
from src.common.config import get_settings


class DocumentStore:
    def __init__(self):
        self.documents: List[Dict] = []
        self.chunks: List[Dict] = []
        self.index = VectorIndex()

    def load_documents(self, data_path: str) -> None:
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.documents = data.get("documents", [])
        print(f"Loaded {len(self.documents)} documents from {data_path}")

    def build_chunks(self, chunk_size: int = None, overlap: int = None) -> None:
        if chunk_size is None:
            chunk_size = get_settings().CHUNK_SIZE
        if overlap is None:
            overlap = get_settings().CHUNK_OVERLAP
            
        self.chunks = []

        for doc in self.documents:
            text = doc.get("text", "")

            for chunk in self.chunk_text(text, chunk_size, overlap):
                self.chunks.append({
                    "doc_id": doc.get("document_id"),
                    "title": doc.get("title"),
                    "chunk": chunk
                })

        texts = [c["chunk"] for c in self.chunks]
        self.index.build(texts)
        print(f"Built {len(self.chunks)} chunks from {len(self.documents)} documents")

    @staticmethod
    def chunk_text(text: str, size: int, overlap: int = 0):
        if not text:
            return []
            
        if overlap >= size:
            overlap = size // 2
            
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + size
            chunk = text[start:end]
            chunks.append(chunk)
            
            if end >= len(text):
                break
                
            start = end - overlap
            
        return chunks
