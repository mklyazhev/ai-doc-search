import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List


class VectorIndex:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.texts: List[str] = []

    def build(self, texts: List[str]) -> None:
        self.texts = texts

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True
        )

        embeddings = np.array(embeddings).astype("float32")

        dim = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dim)
        self.index.add(embeddings)

    def search(self, query: str, top_k: int):
        query_vec = self.model.encode([query], normalize_embeddings=True)
        query_vec = np.array(query_vec).astype("float32")

        scores, indices = self.index.search(query_vec, top_k)

        return [
            {
                "index": i,
                "score": float(scores[0][pos]),
                "text": self.texts[i]
            }
            for pos, i in enumerate(indices[0])
        ]
