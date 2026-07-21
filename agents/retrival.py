import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class RetrievalAgent:
    def __init__(self, corpus_path="knowledge/privacy_corpus.json"):
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        with open(corpus_path, "r", encoding="utf-8") as f:
            self.corpus = json.load(f)

        self.texts = [chunk["text"] for chunk in self.corpus]

        self.embeddings = self.model.encode(
            self.texts,
            convert_to_numpy=True
        )

        dimension = self.embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(self.embeddings)

    def retrieve(self, query, top_k=3):
        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        )

        distances, indices = self.index.search(query_embedding, top_k)

        results = []

        for distance, idx in zip(distances[0], indices[0]):
            chunk = self.corpus[idx].copy()
            chunk["similarity_score"] = float(distance)
            results.append(chunk)

        return results