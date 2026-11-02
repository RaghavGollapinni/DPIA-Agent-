"""Stage 5 - Legal evidence (RAG retrieval).

For each FINDING (not each raw answer) we search the DPDP corpus and attach the closest
provisions. The rules decide the risk. This step only finds supporting text.

How it works:
  1. Each corpus chunk becomes one text: title + topic + keywords + legal text.
  2. MiniLM turns each text into 384 numbers (an embedding). We normalise to length 1.
  3. FAISS stores the vectors. For normalised vectors, inner product = cosine similarity.
  4. A finding becomes a query text, is embedded the same way, and FAISS returns the top-k.
  5. We map the row numbers back to the chunks in the JSON file, with section metadata.

Similarity means "close in meaning". It does not prove the provision applies.
"""
import json
import os

import numpy as np

try:
    import faiss
except ImportError:                      # the numpy path below gives the same answer
    faiss = None

# Labels for the report. These cut-offs are NOT calibrated. Run evaluate_retrieval.py
# and adjust them to the similarity values you see for correct and wrong matches.
STRONG_AT = 0.50
MODERATE_AT = 0.35


def strength(similarity):
    if similarity >= STRONG_AT:
        return "Strong"
    if similarity >= MODERATE_AT:
        return "Moderate"
    return "Weak"


def _unit(vectors):
    vectors = np.asarray(vectors, dtype="float32")
    if vectors.ndim == 1:
        vectors = vectors.reshape(1, -1)
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    return np.ascontiguousarray(vectors / np.maximum(norms, 1e-12), dtype="float32")


class RetrievalAgent:
    def __init__(self, corpus_path=None,
                 model_name="sentence-transformers/all-MiniLM-L6-v2", embedder=None):
        """embedder: optional function(list of str) -> array. Tests pass a fake one."""
        if embedder is None:
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer(model_name)
            embedder = lambda texts: model.encode(texts, convert_to_numpy=True)
        self._embed = embedder

        if corpus_path is None:      # works from any folder
            root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            corpus_path = os.path.join(root, "knowledge", "privacy_corpus.json")
        with open(corpus_path, "r", encoding="utf-8") as f:
            self.corpus = json.load(f)

        docs = [self._doc_text(chunk) for chunk in self.corpus]
        self.vectors = _unit(self._embed(docs))
        if faiss is not None:
            self.index = faiss.IndexFlatIP(self.vectors.shape[1])
            self.index.add(self.vectors)
        else:
            self.index = None

    @staticmethod
    def _doc_text(chunk):
        keywords = ", ".join(chunk.get("keywords", []))
        return f"{chunk['title']}. {chunk['topic']}. Keywords: {keywords}. {chunk['text']}"

    def retrieve(self, query, top_k=3):
        """Return the top_k chunks. 'similarity' is cosine similarity (higher = closer)."""
        top_k = min(top_k, len(self.corpus))
        q = _unit(self._embed([query]))
        if self.index is not None:
            scores, rows = self.index.search(q, top_k)
            pairs = list(zip(scores[0], rows[0]))
        else:
            sims = (self.vectors @ q[0])
            order = np.argsort(-sims, kind="stable")[:top_k]
            pairs = [(sims[i], i) for i in order]

        results = []
        for rank, (score, row) in enumerate(pairs, start=1):
            chunk = dict(self.corpus[int(row)])
            chunk["similarity"] = round(float(score), 4)
            chunk["rank"] = rank
            results.append(chunk)
        return results

    @staticmethod
    def query_for(finding):
        # Title + what was observed. We leave out the risk sentence: it adds words
        # (for example "breach") that pull in unrelated provisions.
        return f"{finding.category}. {finding.title}. {finding.observed_practice}"

    def attach_evidence(self, finding, top_k=3):
        """Fill finding.evidence with the closest provisions. Metadata stays attached."""
        finding.evidence = [
            {
                "chunk_id": c["id"], "source": c["source"], "section": c["section"],
                "topic": c["topic"], "title": c["title"], "text": c["text"],
                "mitigation_hint": c.get("mitigation_hint", ""),
                "similarity": c["similarity"], "rank": c["rank"],
                "strength": strength(c["similarity"]),
            }
            for c in self.retrieve(self.query_for(finding), top_k=top_k)
        ]
        return finding.evidence
